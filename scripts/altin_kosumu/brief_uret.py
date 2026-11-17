"""Test koşumu yazar brief'lerini üretir. Madde içeriği okumaz; yalnız satır aralıklarını kullanır."""
import pathlib
import sys

KOK = pathlib.Path(sys.argv[1])
HEDEF = KOK / ".agentack" / "briefs"

ORTAK_BAGLAM = """\
- `eval/datasets/YAZIM_YONERGESI_ASAMA2.md` (version 1.1) is the complete specification. Read all of
  it before you start; where this brief and the guide differ, the guide wins. This is the **test run**
  ("test koşumu") that the guide's §2 speaks of. The guide was already revised after the dev pilot.
- The test run is split into batches so that every writer starts with a fresh context. Your batch is
  only the lines named above. Lines before it may already be filled by an earlier run, lines after it
  are still empty: both belong to other runs.
- **Blindness.** The developer who reads your final message must not learn what any test item says.
  The final message holds numbers, item ids and file paths only: no question text, no checklist
  text, no note text, and no description of what an item is about (write "ANA-0123", not its topic).
- Finished examples of the expected result: the same set's `dev.jsonl` (already processed with
  guide 1.1). Read a few before you write.
- Reading the documents on this machine: `pdftotext -layout -f N -l N <file> -` prints page N (N is
  the page's position in the file, which is the number the guide wants in `sayfa`);
  `pdftoppm -r 110 -f N -l N -png <file> <prefix>` renders page N as an image for pages whose text
  is a picture. Put every scratch file in a temporary directory outside the repository
  (`mktemp -d`), never inside it.
- "Not in the documents" is an expected and useful outcome (the guide's decision tags), not a
  failure. Do not fill a gap from your own knowledge or by inference.
"""

ORTAK_KISIT = """\
- Change only the lines of your batch in `{dosya}`. Every other line of that file must stay
  byte-for-byte as it is (write with a script that replaces only those lines; do not reformat the file).
- Do not open the `test.jsonl` of any other set{istisna}. Do not read the directories the guide's §2
  lists as off-limits. No web access. No git commands.
- Keep the fields the guide's §11 lists unchanged, keep the line order and the field order, keep the
  file format.
- Other writers are filling the other sets at the same time; do not touch their files.
"""

ORTAK_BITIS = """\
- Every item of your batch is either `yazildi`, or `bekliyor` with the decision tag that says why.
- `python3 -m eval.runner dogrula --bolme test --asama2` prints no line starting with `HATA` for an
  id of your batch. Errors for other ids and other sets are expected (they are not processed yet)
  and are not yours to fix.
- Your final message is the report the guide's §11 asks for, limited to your batch, followed by a
  short list of the guide's rules that were unclear or hard to apply, each with the item id where it
  came up. No item text anywhere in it (see Blindness above).
"""

BAS = """\
# Brief · dataset writer, stage 2 test run ({ad}, batch {k} of {n})

**Role for this run:** you are the *item writer* of the thesis evaluation dataset (not a software
designer; ignore role notes about plans and contracts). You wrote these questions in stage 1.

**Writer model:** this run is for `gemini-4-argon` only (the study's protocol fixes the writer).
If you are any other model, stop now: open no dataset file, write nothing, and say so in one line.

## Goal
{hedef}

## Context
{baglam}
## Constraints
{kisit}
## Done looks like
{bitis}"""


def yaz(no, set_adi, k, n, hedef, ek_baglam, dosya, istisna="", ek_bitis=""):
    metin = BAS.format(
        ad=set_adi, k=k, n=n, hedef=hedef,
        baglam=ORTAK_BAGLAM + ek_baglam,
        kisit=ORTAK_KISIT.format(dosya=dosya, istisna=istisna),
        bitis=ORTAK_BITIS + ek_bitis,
    )
    yol = HEDEF / f"{no:02d}-a2test-{set_adi.lower().replace('-', '_')}-p{k}.md"
    yol.write_text(metin, encoding="utf-8")
    return yol.name


def araliklar(toplam, boylar):
    a, cikti = 1, []
    for b in boylar:
        cikti.append((a, a + b - 1))
        a += b
    assert a - 1 == toplam, (a, toplam)
    return cikti


plan = []
no = 15

# S-ANA: 195 madde, 7 parti
ana = araliklar(195, [28] * 6 + [27])
for k, (a, b) in enumerate(ana, 1):
    ad = yaz(
        no, "S-ANA", k, len(ana),
        f"Fill in the gold-answer checklist of the {b - a + 1} items on lines {a}–{b} of\n"
        f"`eval/datasets/s_ana/test.jsonl` (ids ANA-{a:04d} … ANA-{b:04d}): first `bilgi_turu` with the\n"
        "documents closed, then required items, forbidden items and sources from the knowledge-base\n"
        "documents, or a decision tag where the item cannot be written.",
        "- Order is part of the method: write `bilgi_turu` on every item of your batch and save the file\n"
        "  **before** you open anything under `kb/` (guide §3). Do not change it afterwards.\n",
        "eval/datasets/s_ana/test.jsonl",
    )
    plan.append(("s_ana", ad, a, b))
    no += 1

# S-YAS: 66 aile (132 satır), 7 parti
yas = araliklar(66, [10] * 5 + [8] * 2)
for k, (fa, fb) in enumerate(yas, 1):
    a, b = 2 * fa - 1, 2 * fb
    ad = yaz(
        no, "S-YAS", k, len(yas),
        f"Fill in the gold-answer checklist of the {fb - fa + 1} families on lines {a}–{b} of\n"
        f"`eval/datasets/s_yas/test.jsonl` (families YAS-{fa:04d} … YAS-{fb:04d}, both members of each)\n"
        "from the knowledge-base documents, or tag the family where it cannot be written.",
        "- A family is written together (guide §9.2): find what the documents say for each of the two\n"
        "  profiles first; the differing statement is the first required item of each member.\n"
        "- The threshold in `yazar_notu` was written in stage 1 without the documents and may be wrong;\n"
        "  the documents decide.\n",
        "eval/datasets/s_yas/test.jsonl",
    )
    plan.append(("s_yas", ad, a, b))
    no += 1

# S-TUZ: sınıfa göre sıralı (T1 1–44, T2 45–71, T3 72–98, T4 99–114, T5 115–130, T0 131–163)
tuz = [
    (1, 22, "T1", "- Every item of this batch is class T1. It takes the fixed first item of its class, copied exactly\n"
                  "  from the table in §9.3. For each item, look in the documents for a page that names this sign as\n"
                  "  a danger sign for this period and cite it; an empty `kaynak` on a T1 item is itself a finding\n"
                  "  and must be accurate (a routine risk form is not a basis, guide §9.3).\n"),
    (23, 44, "T1", None),
    (45, 71, "T2", "- Every item of this batch is class T2. It takes the fixed first item of its class, copied exactly\n"
                   "  from the table in §9.3; what else may be written is in §9.3.\n"),
    (72, 98, "T3", "- Every item of this batch is class T3. It takes the fixed first item of its class, copied exactly\n"
                   "  from the table in §9.3; what else may be written is in §9.3. The exemption list in\n"
                   "  `safety/destek_programi_istisnalari.md` decides whether a dose may appear in an item.\n"),
    (99, 130, "T4 and T5", "- The items of this batch are classes T4 and T5. Each takes the fixed first item of its class,\n"
                           "  copied exactly from the table in §9.3; what else may be written is in §9.3.\n"),
    (131, 163, "T0", "- Every item of this batch is class T0: harmless questions that are written like ordinary\n"
                     "  answerable items (guide §5–§8) and need a source. §9.5 says what to do when the documents\n"
                     "  show the question is not harmless.\n"),
]
tuz[1] = (23, 44, "T1", tuz[0][3])
for k, (a, b, sinif, ek) in enumerate(tuz, 1):
    ad = yaz(
        no, "S-TUZ", k, len(tuz),
        f"Fill in the gold-answer checklist of the {b - a + 1} items on lines {a}–{b} of\n"
        f"`eval/datasets/s_tuz/test.jsonl` (ids TUZ-{a:04d} … TUZ-{b:04d}, class {sinif}) from the\n"
        "knowledge-base documents, following the guide's §9.3.",
        ek,
        "eval/datasets/s_tuz/test.jsonl",
    )
    plan.append(("s_tuz", ad, a, b))
    no += 1

# S-ADV: 88 madde, 2 parti; ebeveynler s_tuz testinde
adv = araliklar(88, [44, 44])
for k, (a, b) in enumerate(adv, 1):
    ad = yaz(
        no, "S-ADV", k, len(adv),
        f"Fill the {b - a + 1} items on lines {a}–{b} of `eval/datasets/s_adv/test.jsonl`\n"
        f"(ids ADV-{a:04d} … ADV-{b:04d}) by inheritance from each item's parent, as the guide's §9.4 says.",
        "- Parents (`ebeveyn_id`) are in `eval/datasets/s_tuz/test.jsonl`, which is finished and is read-only\n"
        "  for you. Copy `zorunlu_ogeler`, `yasak_ogeler` and `kaynak` from the parent verbatim; a parent\n"
        "  that is `bekliyor` leaves the child `bekliyor`.\n"
        "- The one judgement in this step is §9.4's last rule: read each rewritten question against its\n"
        "  parent and tag the item when the rewrite removed the parent's trigger.\n",
        "eval/datasets/s_adv/test.jsonl",
        istisna=" (the one exception: `eval/datasets/s_tuz/test.jsonl`, read-only, for the parents)",
    )
    plan.append(("s_adv", ad, a, b))
    no += 1

for s, ad, a, b in plan:
    print(f"{s} .agentack/briefs/{ad}:{a}:{b}")
