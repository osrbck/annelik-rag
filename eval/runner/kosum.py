"""Koşum döngüsü, koşum kaydı (manifest), hash'ler ve korumalar (protokol §7).

Sıra: maddeler dışta, konfigürasyonlar içte, tekrarlar en içte (dönüşümlü, §7.3).
Konsola yalnızca madde kimliği ve sayılar yazılır; soru metni asla.
"""
import csv
import dataclasses
import datetime as dt
import fnmatch
import hashlib
import importlib.metadata
import json
import os
import pathlib
import subprocess
import sys

import yaml

from . import veri
from .uretici import AnthropicUretici, EFFORT_DUZEYLERI, SahteUretici, Yanit, kullanici_mesaji, YENIDEN_DENEME

ROOT = pathlib.Path(__file__).resolve().parents[2]
ETIKET_KALIBI = "degerlendirme-v*"
# Devam edilirken ilk koşumla aynı olması gereken manifest alanları.
DEVAM_ALANLARI = ("konfig_adi", "bolme", "uretici", "sinir", "setler", "tekrar", "konfig_sha256",
                  "sistem_istemi_sha256", "veri_dosyalari", "kb_hashleri", "git_commit")


def ortam_bilgisi() -> dict:
    """Koşumun yapıldığı Python ve SDK sürümleri (protokol §7.5; TRIPOD-LLM raporlaması için)."""
    try:
        sdk = importlib.metadata.version("anthropic")
    except importlib.metadata.PackageNotFoundError:
        sdk = None
    return {"python": sys.version.split()[0], "anthropic_sdk": sdk}


class KosumHatasi(Exception):
    """Koşumun başlamasını engelleyen, kullanıcıya gösterilecek hata."""


def sha256_dosya(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for parca in iter(lambda: f.read(1 << 20), b""):
            h.update(parca)
    return h.hexdigest()


def git_bilgisi(depo: pathlib.Path) -> dict:
    """commit, etiket, kirli; git okunamazsa hepsi None."""
    def calistir(*a: str):
        return subprocess.run(["git", *a], cwd=depo, capture_output=True, text=True, check=False)
    try:
        r = calistir("rev-parse", "HEAD")
        if r.returncode != 0:
            return {"commit": None, "etiket": None, "kirli": None}
        etiketler = sorted(calistir("tag", "--points-at", "HEAD").stdout.split())
        kirli = bool(calistir("status", "--porcelain").stdout.strip())
    except OSError:
        return {"commit": None, "etiket": None, "kirli": None}
    uygun = [e for e in etiketler if fnmatch.fnmatch(e, ETIKET_KALIBI)]
    return {"commit": r.stdout.strip(), "etiket": (uygun or etiketler or [None])[0], "kirli": kirli}


def konfig_yukle(yol: pathlib.Path, depo: pathlib.Path) -> dict:
    try:
        k = yaml.safe_load(yol.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as e:
        raise KosumHatasi(f"{yol}: konfigürasyon okunamadı ({type(e).__name__})") from e
    if not isinstance(k, dict) or not isinstance(k.get("name"), str) or not k["name"]:
        raise KosumHatasi(f"{yol}: 'name' eksik")
    g = k.get("generator")
    if not isinstance(g, dict):
        raise KosumHatasi(f"{yol}: 'generator' bloğu eksik")
    model = g.get("model")
    if not isinstance(model, str) or not model or model.startswith("<"):
        raise KosumHatasi(f"{yol}: generator.model henüz belirlenmemiş (yer tutucu)")
    mot = g.get("max_output_tokens")
    if not veri._tam(mot) or mot <= 0:
        raise KosumHatasi(f"{yol}: generator.max_output_tokens eksik ya da geçersiz")
    if g.get("effort") not in EFFORT_DUZEYLERI:
        raise KosumHatasi(f"{yol}: generator.effort şunlardan biri olmalı: {', '.join(EFFORT_DUZEYLERI)} "
                          "(protokol §7.3: açıkça sabitlenir)")
    if g.get("provider", "cloud") != "cloud" or g.get("api", "anthropic") != "anthropic":
        raise KosumHatasi(f"{yol}: yalnız cloud/anthropic üretici destekleniyor (yerel model Faz 5)")
    for blok, ad in (("retrieval", "getirme (K1+, Faz 2)"), ("safety", "güvenlik katmanı (K3, Faz 4)")):
        if (k.get(blok) or {}).get("enabled"):
            raise KosumHatasi(f"{yol}: {ad} henüz yok")
    istem = g.get("system_prompt_file")
    if not isinstance(istem, str) or not (depo / istem).is_file():
        raise KosumHatasi(f"{yol}: generator.system_prompt_file bulunamadı")
    ev = k.get("eval") or {}
    tekrar = ev.get("repeats", 1)
    if not veri._tam(tekrar) or tekrar < 1:
        raise KosumHatasi(f"{yol}: eval.repeats geçersiz")
    setler = ev.get("datasets", list(veri.SETLER))
    if not isinstance(setler, list) or not set(setler) <= set(veri.SETLER):
        raise KosumHatasi(f"{yol}: eval.datasets geçersiz")
    return k


def test_korumasi(nihai: bool, git: dict) -> None:
    """test bölmesi: --nihai, temiz ağaç ve degerlendirme-v* etiketi (protokol §7.1, §7.2)."""
    if not nihai:
        raise KosumHatasi("test bölmesi yalnız --nihai ile koşturulur (protokol §7.1)")
    if git["commit"] is None:
        raise KosumHatasi("git bilgisi okunamadı; nihai koşum git deposunda yapılmalı")
    if git["kirli"]:
        raise KosumHatasi("çalışma ağacı temiz değil (protokol §7.2)")
    if not (git["etiket"] and fnmatch.fnmatch(git["etiket"], ETIKET_KALIBI)):
        raise KosumHatasi(f"HEAD'de '{ETIKET_KALIBI}' etiketi yok (protokol §7.2)")


def varsayilan_uretici(tur: str, g: dict):
    if tur == "sahte":
        return SahteUretici()
    return AnthropicUretici(g["model"], g["effort"], g["max_output_tokens"])


def kb_hashleri(kayit: pathlib.Path) -> dict:
    try:
        with kayit.open(encoding="utf-8", newline="") as f:
            return {(r.get("belge_id") or "").strip(): ((r.get("hash") or "").strip() or None)
                    for r in csv.DictReader(f) if (r.get("belge_id") or "").strip()}
    except OSError:
        return {}


def _json_yaz(yol: pathlib.Path, nesne) -> None:
    gecici = yol.with_name(yol.name + ".tmp")
    gecici.write_text(json.dumps(nesne, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(gecici, yol)


def _yanitlari_oku(yol: pathlib.Path) -> dict:
    """(madde_id, tekrar) -> satır; aynı çift birden çok kez varsa sonuncusu geçerlidir."""
    sonuc: dict = {}
    if not yol.is_file():
        return sonuc
    for satir in yol.read_text(encoding="utf-8").splitlines():
        try:
            d = json.loads(satir)
            sonuc[(d["madde_id"], d["tekrar"])] = d
        except (json.JSONDecodeError, KeyError, TypeError):
            continue  # yarım kalmış son satır
    return sonuc


def _yanitlari_temizle(yol: pathlib.Path) -> dict:
    """Devam için: yarım son satırı ve hatalı satırları at, (madde, tekrar) başına son geçerli satırı
    tut, dosyayı atomik olarak yeniden yaz. Sonrasında yalnız eklenir; dosyada yinelenen çift olmaz."""
    gecerli = {k: d for k, d in _yanitlari_oku(yol).items() if not d.get("hata")}
    gecici = yol.with_name(yol.name + ".tmp")
    with gecici.open("w", encoding="utf-8") as f:
        for d in gecerli.values():
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    os.replace(gecici, yol)
    return gecerli


def _say(satirlar: dict) -> dict:
    return {
        "yanit": len(satirlar),
        "hata": sum(1 for d in satirlar.values() if d.get("hata")),
        "ret": sum(1 for d in satirlar.values() if d.get("durma_nedeni") == "refusal"),
        "kesilme": sum(1 for d in satirlar.values() if d.get("durma_nedeni") == "max_tokens"),
    }


@dataclasses.dataclass
class _Kosum:
    konfig: dict
    setler: list
    dizin: pathlib.Path
    manifest: dict
    uretici: object
    sistem: str
    yanitlar: dict
    dosya: object = None


def kos(konfig_yollari, bolme: str | None = None, setler: list | None = None, uretici: str = "anthropic",
        sinir: int | None = None, nihai: bool = False, cikti: str | None = None,
        depo: pathlib.Path = ROOT, uretici_fabrikasi=varsayilan_uretici, git_fn=git_bilgisi,
        simdi=None, yaz=print) -> int:
    """Koşumu çalıştırır; engelleyici sorunlarda KosumHatasi fırlatır."""
    simdi = simdi or (lambda: dt.datetime.now(dt.timezone.utc))
    if sinir is not None and (not veri._tam(sinir) or sinir < 1):
        raise KosumHatasi("--sinir en az 1 olmalı")
    konfigler = [konfig_yukle(pathlib.Path(y), depo) for y in konfig_yollari]
    adlar = [k["name"] for k in konfigler]
    if len(set(adlar)) != len(adlar):
        raise KosumHatasi("konfigürasyon adları benzersiz olmalı")
    if bolme is None:
        bolmeler = {(k.get("eval") or {}).get("split", "dev") for k in konfigler}
        if len(bolmeler) != 1:
            raise KosumHatasi("konfigürasyonların eval.split değerleri farklı; --bolme verin")
        bolme = bolmeler.pop()
    if bolme not in veri.BOLMELER:
        raise KosumHatasi("--bolme dev ya da test olmalı")
    git = git_fn(depo)
    if bolme == "test":
        test_korumasi(nihai, git)  # veri dosyasına dokunmadan önce
    if setler is not None and not set(setler) <= set(veri.SETLER):
        raise KosumHatasi("--setler geçersiz")
    if cikti is not None:
        if len(konfigler) != 1:
            raise KosumHatasi("--cikti yalnız tek konfigürasyonla kullanılabilir")
        if not pathlib.Path(cikti).is_dir():
            raise KosumHatasi("--cikti mevcut bir koşum klasörü olmalı")

    veri_koku = depo / "eval" / "datasets"
    kayit = depo / "kb" / "registry" / "belge_kayit_defteri.csv"
    # Nihai koşumda iki bölme birlikte (sızıntı, kimlik/aile çakışması) ve §4 hedefleriyle doğrulanır;
    # dev koşumunda yalnız dev okunur (test dosyalarına dokunulmaz).
    if bolme == "test":
        sonuc = veri.dogrula(veri_koku, veri.BOLMELER, kayit, hedef=True)
    else:
        sonuc = veri.dogrula(veri_koku, [bolme], kayit, hedef=False)
    if sonuc.hatalar:
        veri.rapor_yaz(sonuc, sys.stdout)
        raise KosumHatasi(f"{len(sonuc.hatalar)} doğrulama hatası var; koşum durdu")
    for u in sonuc.uyarilar:
        yaz(f"UYARI  {u}")

    setlist = {k["name"]: (setler if setler is not None else
                           (k.get("eval") or {}).get("datasets", list(veri.SETLER))) for k in konfigler}
    kullanilan = set().union(*map(set, setlist.values()))
    maddeler = [k for k in sonuc.kayitlar if k.set_adi in kullanilan and k.bolme == bolme]
    if sinir is not None:
        maddeler = maddeler[:sinir]
    if not maddeler:
        raise KosumHatasi(f"{bolme} bölmesi için madde bulunamadı (eval/datasets/*/{bolme}.jsonl yok ya da boş)")

    veri_hash = {f"eval/datasets/{s}/{b}.jsonl": sha256_dosya(veri_koku / s / f"{b}.jsonl")
                 for s, b in sonuc.bulunan if s in kullanilan and b == bolme}
    kb = kb_hashleri(kayit)
    ts = simdi()
    # Üreticiler, koşum klasörü oluşturulmadan önce kurulur: eksik anahtar/SDK artık klasör bırakmaz.
    ureticiler = [uretici_fabrikasi(uretici, k["generator"]) for k in konfigler]
    kosumlar: list[_Kosum] = []
    for k, u, yol_ in zip(konfigler, ureticiler, konfig_yollari):
        g = k["generator"]
        istem_yolu = depo / g["system_prompt_file"]
        manifest = {
            "kosum_kimligi": None, "konfig_adi": k["name"], "bolme": bolme,
            "git_commit": git["commit"], "git_etiketi": git["etiket"], "git_kirli": git["kirli"],
            "konfig_sha256": sha256_dosya(pathlib.Path(yol_)),
            "sistem_istemi_sha256": sha256_dosya(istem_yolu),
            "veri_dosyalari": veri_hash, "kb_hashleri": kb,
            "uretici": {"provider": g.get("provider", "cloud"), "api": g.get("api", "anthropic"),
                        "tur": uretici, "model": g["model"], "effort": g["effort"],
                        "max_output_tokens": g["max_output_tokens"],
                        "yeniden_deneme_siniri": YENIDEN_DENEME,
                        "ornekleme_parametresi": None},
            "ortam": ortam_bilgisi(),
            "tekrar": (k.get("eval") or {}).get("repeats", 1), "setler": sorted(setlist[k["name"]]),
            "sinir": sinir, "donen_modeller": [], "baslangic": None, "bitis": None,
            "tamamlandi": False, "devam_sayisi": 0, "sayilar": {},
        }
        yanitlar: dict = {}
        if cikti:
            dizin = pathlib.Path(cikti)
            eski = dizin / "manifest.json"
            if not eski.is_file():
                raise KosumHatasi("devam edilemez: --cikti klasöründe manifest.json yok")
            try:
                onceki = json.loads(eski.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                raise KosumHatasi("devam edilemez: manifest.json okunamadı") from e
            for alan in DEVAM_ALANLARI:
                if onceki.get(alan) != manifest[alan]:
                    raise KosumHatasi(f"devam edilemez: '{alan}' ilk koşumdan farklı")
            onceki["devam_sayisi"] = onceki.get("devam_sayisi", 0) + 1
            onceki["tamamlandi"] = False
            onceki["bitis"] = None
            manifest = onceki
            yanitlar = _yanitlari_temizle(dizin / "yanitlar.jsonl")
        else:
            dizin = depo / "eval" / "results" / "raw" / f"{ts.strftime('%Y%m%dT%H%M%SZ')}_{k['name']}_{bolme}"
            dizin.mkdir(parents=True, exist_ok=False)
        manifest["kosum_kimligi"] = dizin.name
        manifest["baslangic"] = manifest["baslangic"] or ts.isoformat()
        kosumlar.append(_Kosum(k, setlist[k["name"]], dizin, manifest, u,
                               istem_yolu.read_text(encoding="utf-8"), yanitlar))

    tamam = False
    try:
        for ks in kosumlar:
            yol = ks.dizin / "yanitlar.jsonl"
            ks.dosya = yol.open("a", encoding="utf-8")
            _json_yaz(ks.dizin / "manifest.json", ks.manifest)
        for i, madde in enumerate(maddeler, 1):
            v = madde.veri
            mesaj = kullanici_mesaji(v)
            hatali = 0
            for ks in kosumlar:
                if madde.set_adi not in ks.setler:
                    continue
                for tekrar in range(1, ks.manifest["tekrar"] + 1):
                    onceki = ks.yanitlar.get((v["id"], tekrar))
                    if onceki is not None and not onceki.get("hata"):
                        continue
                    y: Yanit = ks.uretici.uret(ks.sistem, mesaj)
                    satir = {"madde_id": v["id"], "tekrar": tekrar, **dataclasses.asdict(y), "getirilen": []}
                    ks.dosya.write(json.dumps(satir, ensure_ascii=False) + "\n")
                    ks.dosya.flush()
                    ks.yanitlar[(v["id"], tekrar)] = satir
                    hatali += bool(y.hata)
            yaz(f"[{i}/{len(maddeler)}] {v['id']}" + (f"  hata: {hatali}" if hatali else ""))
        tamam = True
    finally:
        bitis = simdi().isoformat()
        for ks in kosumlar:
            if ks.dosya:
                ks.dosya.close()
            ks.manifest["sayilar"] = _say(ks.yanitlar)
            ks.manifest["donen_modeller"] = sorted({d["model"] for d in ks.yanitlar.values() if d.get("model")})
            ks.manifest["bitis"] = bitis
            ks.manifest["tamamlandi"] = tamam
            _json_yaz(ks.dizin / "manifest.json", ks.manifest)

    sonuclar = depo / "eval" / "results"
    for ks in kosumlar:
        satirlar = [f"{sha256_dosya(p)}  {p.name}" for p in sorted(ks.dizin.iterdir()) if p.is_file()]
        (sonuclar / f"{ks.manifest['kosum_kimligi']}.sha256").write_text("\n".join(satirlar) + "\n", encoding="utf-8")
        s = ks.manifest["sayilar"]
        yaz(f"ÖZET {ks.manifest['kosum_kimligi']}: {s['yanit']} yanıt, {s['hata']} hata, "
            f"{s['ret']} ret, {s['kesilme']} kesilme")
    return 0
