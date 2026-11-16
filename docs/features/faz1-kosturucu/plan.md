# Faz 1 — evaluation runner and dataset validator: plan

Source of truth for every rule below: `docs/thesis/degerlendirme_protokolu.md` (v1.1). Read §4.5,
§4.6, §7 and §8 of it before writing code. This plan only fixes the shape of the code.

## Constraints

- Python 3.12, **standard library + PyYAML only**. `pip`/`venv` are not available on this machine;
  nothing else can be imported at module top level. The `anthropic` SDK is imported lazily inside
  the one class that needs it.
- Follow `scripts/hash_kb.py` for style: Turkish identifiers, docstrings, CLI flags and messages;
  type hints; `argparse`; exit code 0 = fine, 1 = problem.
- **Never open `eval/datasets/*/test.jsonl` while developing or testing.** Tests build their own
  fixture files in temporary directories. Nothing may print item text (`soru`, `zorunlu_ogeler`,
  `yasak_ogeler`) of a `test` item to stdout/stderr; error lines carry the item `id` and field name only.
- Tests: `python3 -m unittest discover -s tests -v` (stdlib `unittest`), no network.

## Layout

```
eval/__init__.py
eval/runner/__init__.py
eval/runner/__main__.py   CLI: `python3 -m eval.runner dogrula|kos ...`
eval/runner/veri.py       load + validate dataset items
eval/runner/uretici.py    generator interface, fake generator, Anthropic generator, profile line
eval/runner/kosum.py      run loop, run record, hashing, guards
tests/test_veri.py, tests/test_uretici.py, tests/test_kosum.py
```

`eval/datasets/` stays a data directory (no `__init__.py` there).

## 1. `veri.py` — items

Files: `eval/datasets/<set>/<bolme>.jsonl`, sets `s_ana s_yas s_tuz s_adv`, splits `dev test`,
one JSON object per line. A missing file is not an error (the set is simply not written yet).

Field rules (protocol §4.5):

- `id`: unique across all files; pattern by set: `ANA-0001`, `YAS-0001-a|b`, `TUZ-0001`, `ADV-0001`;
  dev items carry a `D` before the number (`ANA-D0001`, `YAS-D0001-a`, …).
- `set`, `bolme` must match the file the item is in.
- `profil`: `{"donem":"gebelik","gebelik_haftasi":4..42}` or `{"donem":"cocuk","yas_ay":0..216}`
  with optional `yas_gun` 0..30 allowed only when `yas_ay` is 0.
- `soru`: non-empty string. `konu` ∈ izlem, beslenme, asi, buyume, hastalik, emzirme, diger.
- `beklenen_davranis` ∈ yanitla, acil_yonlendir, teshis_reddet, doz_reddet, kapsam_disi, oncul_duzelt.
- `altin_durumu` ∈ bekliyor, yazildi, onayli. `yazar`: non-empty string.
  - `bekliyor`: `zorunlu_ogeler`, `yasak_ogeler`, `kaynak` may be empty lists.
  - `yazildi` / `onayli`: `zorunlu_ogeler` has 1–4 non-empty strings; `kaynak` has ≥ 1 entry
    `{"belge_id", "sayfa": [ilk, son], "bolum"}` with `belge_id` present in
    `kb/registry/belge_kayit_defteri.csv` and integers `1 <= ilk <= son`.
    Exception: `beklenen_davranis` other than `yanitla` may have an empty `kaynak`.
  - `onayli` additionally needs `uzman_onay.durum == "onay"`. Dev items are never `onayli`.
- Optional fields: `guncellik` (bool), `yazar_notu` (string), `uzman_onay` (object or null). Any other
  unknown field is an error. `yazar_notu` is item text and is never printed.
- `s_ana`: `beklenen_davranis` must be `yanitla`.
- `s_yas`: `aile_id` required (`YAS-0001`); each family has exactly two items (`-a`, `-b`) in the
  same split, with **identical** `soru` and **different** `profil` (their `beklenen_davranis` may differ); once both are `yazildi`, their
  `zorunlu_ogeler` must differ.
- `s_tuz`: `sinif` ∈ T0..T5 and fixes `beklenen_davranis`: T0 yanitla, T1 acil_yonlendir,
  T2 teshis_reddet, T3 doz_reddet, T4 kapsam_disi, T5 oncul_duzelt.
- `s_adv`: `ebeveyn_id` must be an `s_tuz` item of the same split whose `sinif` is T1, T2 or T3;
  `beklenen_davranis` equals the parent's; `saldiri_turu` ∈ A1..A6.
- Leakage (protocol §4.6 rule 5): within a set, no dev item and test item with the same normalized
  `soru` (casefold, Turkish-aware lowercasing of `İ/I`, punctuation and whitespace collapsed).
  Token-set Jaccard ≥ 0.8 between any two different questions of a set (families and
  parent/child pairs excluded) is a **warning** listing the two ids.

Period stratum of an item (used for counts): gebelik · `yas_ay` 0 → `0-1 ay` · 1–11 → `1-12 ay` ·
12–71 → `1-5 yas` · 72–155 → `6-12 yas` · 156–216 → `13-18 yas`.

Targets (protocol §4), checked only with `--hedef`, shortfalls and overshoots reported as errors.
Up to 10% surplus per stratum is allowed (reserve items):

| | test | dev |
|---|---|---|
| s_ana | 180: gebelik 36, 0-1 ay 24, 1-12 ay 36, 1-5 yas 36, 6-12 yas 24, 13-18 yas 24 | 30 |
| s_yas | 60 families | 10 families |
| s_tuz | 150: T1 40, T2 25, T3 25, T4 15, T5 15, T0 30 | 20 |
| s_adv | 80: parents T1 20, T2 30, T3 30; each of A1..A6 ≥ 10 | 15 |

Output of `dogrula`: per set/split counts, stratum counts, `altin_durumu` counts, then errors and
warnings as `<id> <alan>: <kısa neden>`. Flags: `--bolme dev|test|hepsi` (default `hepsi`),
`--hedef`, `--kok PATH` (dataset root, for tests).

## 2. `uretici.py` — generators

```python
@dataclass
class Yanit:
    metin: str; durma_nedeni: str | None; model: str | None
    girdi_token: int | None; cikti_token: int | None
    gecikme_sn: float; istek_kimligi: str | None; hata: str | None
```

- `profil_satiri(profil) -> str`: `Profil: gebe, 28. hafta` · `Profil: bebek, 12 günlük` (yas_ay 0
  with yas_gun) · `Profil: bebek, 0–1 aylık` (yas_ay 0, no yas_gun) · `Profil: çocuk, 8 aylık`
  (1–23) · `Profil: çocuk, 3 yaş 4 aylık` / `Profil: çocuk, 3 yaşında` (≥ 24).
- `kullanici_mesaji(madde) -> str`: profile line, blank line, `soru`. Identical for every
  configuration (protocol §2).
- `SahteUretici`: deterministic, no network; used by tests and `--uretici sahte`.
- `AnthropicUretici(model, effort, max_output_tokens)`: lazy `import anthropic`; a clear error
  telling the user to install requirements when the import fails. Request shape — follow
  `/tmp/claude-1000/bundled-skills/2.1.321/a6ae2f0afbd5cb0397a70a48fd9c7ca0/claude-api/python/claude-api/README.md`
  exactly, do not write SDK calls from memory:
  `client.messages.create(model=..., max_tokens=..., system=..., messages=[{"role":"user","content":...}], output_config={"effort": ...})`.
  **Do not send `temperature`, `top_p`, `top_k`, `seed` or a `thinking` parameter** — the chosen
  model (`claude-haiku-5-5`) rejects sampling parameters and runs adaptive thinking by default.
  Client built with `max_retries=2` (the protocol's retry limit); text = concatenation of blocks
  whose `type == "text"`; record `response.stop_reason`, `response.model`, `response.usage`,
  `response._request_id`. `refusal` and `max_tokens` stop reasons are outcomes, not errors.
  Catch the SDK's typed exceptions most-specific-first and put the class name and message in
  `hata`; a failed call is recorded, the run continues. The API key comes from the environment
  (`ANTHROPIC_API_KEY`, optionally loaded from a `.env` file at the repo root by a tiny parser);
  it is never printed or written to any file.

## 3. `kosum.py` + CLI `kos`

`python3 -m eval.runner kos --konfig configs/K0.yaml [--konfig ...] [--bolme dev] [--setler s_ana,...]
[--uretici sahte] [--sinir N] [--nihai] [--cikti PATH]`

- Reads the YAML config (see `configs/K0.yaml`). Refuses to run when `generator.model` still starts
  with `<` (placeholder) or `max_output_tokens` is missing.
- Split comes from `--bolme` (default: the config's `eval.split`). `test` is refused unless
  `--nihai` is given **and** the git tree is clean **and** HEAD carries a tag `degerlendirme-v*`
  (protocol §7.1, §7.2). With `--uretici sahte` the same guards apply.
- Runs `dogrula` logic for the chosen split first; errors stop the run.
- When `retrieval.enabled` is true: stop with "henüz yok" (K1+ is Faz 2). Same for `safety.enabled`.
- Loop: items outer, configs inner, repeats innermost (protocol §7.3, interleaving). One run
  directory per config: `eval/results/raw/<UTC yyyymmddThhmmssZ>_<name>_<bolme>/`.
- `yanitlar.jsonl`: one line per (madde, tekrar): `madde_id`, `tekrar`, all `Yanit` fields,
  `getirilen: []`. Appended and flushed per answer; restarting with `--cikti <existing dir>` skips
  pairs already present (resume) unless their `hata` is set.
- `manifest.json` (protocol §7.5): run id, config name, split, git commit, git tag (or null), dirty
  flag, SHA-256 of the config file, of the system prompt file, of each dataset file used, the
  `hash` column of the KB registry, generator parameters, model ids returned by the API (set),
  start/end time (UTC ISO), counts (answers, errors, refusals, truncations), `--sinir` if used.
- After the run: `eval/results/<run id>.sha256` listing `sha256  filename` for the files of the
  run directory (this file is committed; the raw directory is git-ignored).
- stdout: a short progress line per item (id only) and a final summary. Never the question text
  for test items.

## Done

- `python3 -m unittest discover -s tests -v` passes; tests cover every validator rule above with a
  passing and a failing fixture, the profile line cases, the request shape of `AnthropicUretici`
  (with a stub `anthropic` module injected into `sys.modules`: asserts no sampling parameters are
  sent, `output_config` carries the effort, stop reasons and usage are recorded, an exception
  becomes `hata`), the guards of `kos` (placeholder model, test split without `--nihai`), a fake
  end-to-end run in a temporary directory (answers file, manifest fields, `.sha256` file), resume.
- `python3 -m eval.runner dogrula` runs from the repo root and exits 0 on the current repository
  (dataset files may not exist yet).
- `python3 -m eval.runner kos --konfig configs/K0.yaml --uretici sahte --sinir 3` works once dev
  files exist; with no dev files it says so and exits 1.
- No file outside `eval/__init__.py`, `eval/runner/`, `tests/` is created or changed.
