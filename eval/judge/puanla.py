"""Bir koşumun yanıtlarını hakeme puanlatır (protokol §6.2).

Girdi: `eval/results/raw/<koşum>/` (manifest.json, yanitlar.jsonl) ve koşumun bölmesindeki maddeler.
Çıktı (aynı klasöre): `hakem.<ad>.jsonl` (yanıt başına bir satır) ve `hakem.<ad>.manifest.json`.
Hash listesi (`eval/results/<koşum>.sha256`) yeniden yazılır.

Konsola yalnızca madde kimliği ve sayılar yazılır; soru, öğe ya da yanıt metni asla.
"""
import dataclasses
import datetime as dt
import hashlib
import json
import pathlib
import re
import subprocess
import sys

import yaml

from eval.runner import kosum, veri
from eval.runner.uretici import EFFORT_DUZEYLERI, YENIDEN_DENEME

from . import istem
from .hakem import AnthropicHakem, HakemYaniti, SahteHakem

ROOT = kosum.ROOT
_AD = re.compile(r"[a-z0-9_]+")
# Devam edilirken ilk puanlamayla aynı olması gereken manifest alanları.
DEVAM_ALANLARI = ("hakem_adi", "kosum_kimligi", "hakem", "konfig_sha256", "istem_dosyasi_sha256",
                  "istisna_dosyasi_sha256", "sistem_metni_sha256", "sema_sha256", "veri_dosyalari", "sinir")


class HakemHatasi(Exception):
    """Puanlamanın başlamasını engelleyen, kullanıcıya gösterilecek hata."""


def _sha256_metin(metin: str) -> str:
    return hashlib.sha256(metin.encode("utf-8")).hexdigest()


def konfig_yukle(yol: pathlib.Path, depo: pathlib.Path) -> dict:
    try:
        k = yaml.safe_load(yol.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as e:
        raise HakemHatasi(f"{yol}: hakem konfigürasyonu okunamadı ({type(e).__name__})") from e
    if not isinstance(k, dict) or not isinstance(k.get("name"), str) or not _AD.fullmatch(k["name"]):
        raise HakemHatasi(f"{yol}: 'name' eksik ya da geçersiz (küçük harf, rakam, alt çizgi)")
    j = k.get("judge")
    if not isinstance(j, dict):
        raise HakemHatasi(f"{yol}: 'judge' bloğu eksik")
    model = j.get("model")
    if not isinstance(model, str) or not model or model.startswith("<"):
        raise HakemHatasi(f"{yol}: judge.model henüz belirlenmemiş (yer tutucu)")
    if j.get("api", "anthropic") != "anthropic":
        raise HakemHatasi(f"{yol}: yalnız anthropic hakemi destekleniyor (ikinci hakem henüz yok)")
    if j.get("effort") not in EFFORT_DUZEYLERI:
        raise HakemHatasi(f"{yol}: judge.effort şunlardan biri olmalı: {', '.join(EFFORT_DUZEYLERI)}")
    mot = j.get("max_output_tokens")
    if not veri._tam(mot) or mot <= 0:
        raise HakemHatasi(f"{yol}: judge.max_output_tokens eksik ya da geçersiz")
    for alan in ("prompt_file", "exemption_file"):
        if not isinstance(j.get(alan), str) or not (depo / j[alan]).is_file():
            raise HakemHatasi(f"{yol}: judge.{alan} bulunamadı")
    return k


def varsayilan_hakem(tur: str, j: dict):
    if tur == "sahte":
        return SahteHakem()
    return AnthropicHakem(j["model"], j["effort"], j["max_output_tokens"])


def _say(satirlar: dict) -> dict:
    return {"puanlanan": sum(1 for d in satirlar.values() if not d.get("hata")),
            "hakem_hatasi": sum(1 for d in satirlar.values() if d.get("hata"))}


def izlenen_degismis(depo: pathlib.Path) -> bool:
    """İzlenen dosyalarda commit'lenmemiş değişiklik var mı? (İzlenmeyen dosyalar, ör. yeni hash listeleri, sayılmaz.)"""
    r = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=depo,
                       capture_output=True, text=True, check=False)
    return r.returncode != 0 or bool(r.stdout.strip())


def puanla(kosum_dizini, konfig_yolu, hakem: str = "anthropic", sinir: int | None = None,
           yeniden: bool = False, depo: pathlib.Path = ROOT, hakem_fabrikasi=varsayilan_hakem,
           git_fn=kosum.git_bilgisi, izlenen_degismis_fn=izlenen_degismis, simdi=None, yaz=print) -> int:
    """Koşumdaki her (madde, tekrar) yanıtını puanlatır; engelleyici sorunlarda HakemHatasi fırlatır.

    Puanlanmayanlar sayılır, atlanmaz: altın yanıtı yazılmamış maddeler (`altin_yok`), üreticinin
    kalıcı hatayla bitirdiği yanıtlar (`uretici_hatasi`) ve metni boş yanıtlar (`bos_yanit`); son ikisi
    analizde hakemsiz sonuçlanır (§7.3, eval/analiz/turet.py).
    Hakem hatasıyla biten satırlar bir sonraki çağrıda yeniden denenir.
    """
    simdi = simdi or (lambda: dt.datetime.now(dt.timezone.utc))
    dizin = pathlib.Path(kosum_dizini)
    if sinir is not None and (not veri._tam(sinir) or sinir < 1):
        raise HakemHatasi("--sinir en az 1 olmalı")
    try:
        km = json.loads((dizin / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise HakemHatasi("koşum klasöründe okunabilir manifest.json yok") from e
    if not km.get("tamamlandi"):
        raise HakemHatasi("koşum tamamlanmamış; önce `kos --cikti` ile bitirin")
    bolme = km["bolme"]
    k = konfig_yukle(pathlib.Path(konfig_yolu), depo)
    j = k["judge"]
    ad = k["name"]

    veri_koku = depo / "eval" / "datasets"
    kayit = depo / "kb" / "registry" / "belge_kayit_defteri.csv"
    sonuc = veri.dogrula(veri_koku, [bolme], kayit, hedef=False)
    if sonuc.hatalar:
        veri.rapor_yaz(sonuc, sys.stdout)
        raise HakemHatasi(f"{len(sonuc.hatalar)} doğrulama hatası var; puanlama durdu")
    maddeler = {kyt.veri["id"]: kyt.veri for kyt in sonuc.kayitlar}
    veri_hash = {yol: kosum.sha256_dosya(depo / yol) for yol in sorted(km.get("veri_dosyalari") or {})
                 if (depo / yol).is_file()}
    degisen = sorted(y for y, h in (km.get("veri_dosyalari") or {}).items() if veri_hash.get(y) != h)
    if degisen:
        # Üretim yalnız soru ve profile bakar; altın yanıt sonradan düzeltilmiş olabilir. Dev'de uyarı,
        # test'te (veri dondurulmuştur) hata.
        if bolme == "test":
            raise HakemHatasi("veri dosyaları koşumdan sonra değişmiş: " + ", ".join(degisen))
        yaz("UYARI  veri dosyaları koşumdan sonra değişmiş: " + ", ".join(degisen))

    istem_yolu, istisna_yolu = depo / j["prompt_file"], depo / j["exemption_file"]
    try:
        sistem = istem.sistem_metni(istem_yolu, istisna_yolu)
    except istem.IstemHatasi as e:
        raise HakemHatasi(str(e)) from e
    git = git_fn(depo)
    if bolme == "test":
        # Dondurulmuş kodla puanlanır: koşumla aynı commit ve izlenen dosyalarda değişiklik yok (§7.2).
        if git["commit"] is None or git["commit"] != km.get("git_commit"):
            raise HakemHatasi("test koşumu, yapıldığı commit'te puanlanır (HEAD koşumun commit'i değil)")
        if izlenen_degismis_fn(depo):
            raise HakemHatasi("izlenen dosyalarda commit'lenmemiş değişiklik var (protokol §7.2)")
    manifest = {
        "hakem_adi": ad, "kosum_kimligi": dizin.name, "bolme": bolme,
        "hakem": {"api": j.get("api", "anthropic"), "tur": hakem, "model": j["model"], "effort": j["effort"],
                  "max_output_tokens": j["max_output_tokens"], "yeniden_deneme_siniri": YENIDEN_DENEME,
                  "ornekleme_parametresi": None},
        "konfig_sha256": kosum.sha256_dosya(pathlib.Path(konfig_yolu)),
        "istem_dosyasi_sha256": kosum.sha256_dosya(istem_yolu),
        "istisna_dosyasi_sha256": kosum.sha256_dosya(istisna_yolu),
        "sistem_metni_sha256": _sha256_metin(sistem),
        "sema_sha256": _sha256_metin(json.dumps(istem.SEMA, sort_keys=True)),
        "veri_dosyalari": veri_hash, "sinir": sinir,
        "git_commit": git["commit"], "git_etiketi": git["etiket"], "git_kirli": git["kirli"],
        "ortam": kosum.ortam_bilgisi(), "donen_modeller": [], "baslangic": None, "bitis": None,
        "tamamlandi": False, "devam_sayisi": 0, "sayilar": {},
    }

    cikti_yolu = dizin / f"hakem.{ad}.jsonl"
    manifest_yolu = dizin / f"hakem.{ad}.manifest.json"
    onceki_satirlar: dict = {}
    if manifest_yolu.is_file() and not yeniden:
        try:
            onceki = json.loads(manifest_yolu.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise HakemHatasi("devam edilemez: hakem manifesti okunamadı (--yeniden ile baştan puanlayın)") from e
        for alan in DEVAM_ALANLARI:
            if onceki.get(alan) != manifest[alan]:
                raise HakemHatasi(f"devam edilemez: '{alan}' ilk puanlamadan farklı "
                                  "(hakem konfigürasyonuna yeni bir ad verin ya da --yeniden kullanın)")
        onceki["devam_sayisi"] = onceki.get("devam_sayisi", 0) + 1
        onceki["tamamlandi"] = False
        onceki["bitis"] = None
        manifest = onceki
        onceki_satirlar = kosum._yanitlari_temizle(cikti_yolu)
    elif cikti_yolu.exists():
        cikti_yolu.unlink()
    manifest["baslangic"] = manifest["baslangic"] or simdi().isoformat()

    hakem_nesnesi = hakem_fabrikasi(hakem, j)
    yanitlar = list(kosum._yanitlari_oku(dizin / "yanitlar.jsonl").values())
    if sinir is not None:
        yanitlar = yanitlar[:sinir]
    bilinmeyen = sorted({y["madde_id"] for y in yanitlar if y["madde_id"] not in maddeler})
    if bilinmeyen:
        raise HakemHatasi(f"koşumdaki {len(bilinmeyen)} madde veri setinde yok (ilk: {bilinmeyen[0]})")

    satirlar = dict(onceki_satirlar)
    altin_yok: set = set()
    uretici_hatasi = bos_yanit = 0
    tamam = False
    kosum._json_yaz(manifest_yolu, manifest)
    try:
        with cikti_yolu.open("a", encoding="utf-8") as f:
            for i, y in enumerate(yanitlar, 1):
                madde = maddeler[y["madde_id"]]
                anahtar = (y["madde_id"], y["tekrar"])
                if not veri._yazilmis(madde):
                    altin_yok.add(y["madde_id"])
                    continue
                if y.get("hata"):
                    uretici_hatasi += 1
                    continue
                if not (y.get("metin") or "").strip():
                    bos_yanit += 1
                    continue
                if anahtar in satirlar:
                    continue
                getirilen = y.get("getirilen") or []
                h: HakemYaniti = hakem_nesnesi.puanla(
                    sistem, istem.girdi_metni(madde, y.get("metin") or "", getirilen))
                if h.hata is None and isinstance(h.etiket, dict) and not getirilen:
                    # Bağlam yokken dayanak etiketi anlamsızdır; hakem doldurmuşsa boşa çekilir.
                    h.etiket.update({alan: None for alan in istem.DAYANAK if alan in h.etiket})
                if h.hata is None:
                    sorun = istem.cikti_denetle(h.etiket, len(madde["zorunlu_ogeler"]), bool(getirilen))
                    if sorun:
                        h = dataclasses.replace(h, etiket=None, hata="geçersiz çıktı: " + "; ".join(sorun)[:300])
                satir = {"madde_id": y["madde_id"], "tekrar": y["tekrar"], **dataclasses.asdict(h)}
                f.write(json.dumps(satir, ensure_ascii=False) + "\n")
                f.flush()
                satirlar[anahtar] = satir
                yaz(f"[{i}/{len(yanitlar)}] {y['madde_id']} t{y['tekrar']}" + ("  hakem hatası" if h.hata else ""))
        tamam = True
    finally:
        manifest["sayilar"] = {**_say(satirlar), "altin_yok_madde": len(altin_yok),
                               "uretici_hatasi": uretici_hatasi, "bos_yanit": bos_yanit,
                               "yanit": len(yanitlar)}
        manifest["donen_modeller"] = sorted({d["model"] for d in satirlar.values() if d.get("model")})
        manifest["bitis"] = simdi().isoformat()
        manifest["tamamlandi"] = tamam and manifest["sayilar"]["hakem_hatasi"] == 0
        kosum._json_yaz(manifest_yolu, manifest)
        kosum.hash_listesi_yaz(dizin, depo / "eval" / "results")

    s = manifest["sayilar"]
    yaz(f"ÖZET {dizin.name} · {ad}: {s['puanlanan']} puanlandı, {s['hakem_hatasi']} hakem hatası, "
        f"{s['uretici_hatasi']} üretici hatası ve {s['bos_yanit']} boş yanıt (hakeme sorulmaz), "
        f"altın yanıtı olmayan {s['altin_yok_madde']} madde")
    return 0 if manifest["tamamlandi"] else 1
