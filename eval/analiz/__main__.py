"""Analiz betiği: puanlanmış koşumlardan ölçüt tablolarını üretir (protokol §9).

Kullanım:
  python3 -m eval.analiz --kosum eval/results/raw/<koşum> [--kosum ...] [--hakem hakem_opus]
                         [--cikti KLASÖR] [--onyukleme 10000] [--tohum 20261117]
                         [--eksikle] [--h2-kesifsel]

Birden çok koşum verilirse K0→K1, K1→K2, K2→K3 çiftleri bulunanlar için eşli karşılaştırma ve
hipotez kararları da yazılır. Çıktı: <cikti>/tablolar.md ve <cikti>/ozet.json
(varsayılan: eval/results/tablolar/<bölme>_<ilk koşumun zaman damgası>/).

Çıkış kodu: 0 = tamam, 1 = hata. Konsola ve dosyalara madde metni yazılmaz.
"""
import argparse
import datetime as dt
import json
import pathlib
import sys

from eval.judge import cumle
from eval.runner import kosum

from . import olcut, rapor
from .turet import AnalizHatasi, kosum_yukle

VARSAYILAN_TOHUM = 20261117
SIRA = {"K0": 0, "K1": 1, "K2": 2, "K3": 3, "K4": 4}
HAKEM_ALANLARI = ("hakem", "konfig_sha256", "istem_dosyasi_sha256", "istisna_dosyasi_sha256",
                  "sistem_metni_sha256", "sema_sha256")


def nihai_denetimi(kosumlar: list, eksikle: bool) -> None:
    """Test bölmesinde tablolar yalnız eksiksiz, sınırsız ve aynı dondurulmuş commit'ten gelen koşumlarla üretilir."""
    for k in kosumlar:
        for ad, m in (("koşum", k.manifest), ("puanlama", k.hakem_manifesti)):
            if m.get("sinir") is not None:
                raise AnalizHatasi(f"{k.kimlik}: {ad} --sinir ile yapılmış; test tabloları tam setle üretilir")
            if m.get("git_kirli") and ad == "koşum":
                raise AnalizHatasi(f"{k.kimlik}: koşum temiz olmayan çalışma ağacında yapılmış")
        if not k.hakem_manifesti.get("tamamlandi") and not eksikle:
            raise AnalizHatasi(f"{k.kimlik}: puanlama tamamlanmamış")
    for alan, kaynak in (("git_commit", "manifest"), ("git_commit", "hakem_manifesti"), ("veri_dosyalari", "manifest")):
        if len({json.dumps(getattr(k, kaynak).get(alan), sort_keys=True) for k in kosumlar}) != 1:
            raise AnalizHatasi(f"koşumların '{alan}' değeri aynı değil ({kaynak})")


def analiz(kosum_dizinleri: list, hakem: str = "hakem_opus", cikti: pathlib.Path | None = None,
           onyukleme_n: int = 10_000, tohum: int = VARSAYILAN_TOHUM, eksikle: bool = False,
           h2_kesifsel: bool = False, depo: pathlib.Path = kosum.ROOT, simdi=None) -> pathlib.Path:
    simdi = simdi or (lambda: dt.datetime.now(dt.timezone.utc))
    kosumlar = [kosum_yukle(pathlib.Path(d), hakem, depo) for d in kosum_dizinleri]
    yuklenen = list(kosumlar)
    if not kosumlar:
        raise AnalizHatasi("en az bir koşum gerekli")
    if len({k.bolme for k in kosumlar}) != 1:
        raise AnalizHatasi("koşumların bölmeleri farklı")
    if len({k.kisa_ad for k in kosumlar}) != len(kosumlar):
        raise AnalizHatasi("aynı konfigürasyondan birden çok koşum verildi")
    # Bütün koşumlar aynı hakemle, aynı ayar ve istemle puanlanmış olmalı.
    for alan in HAKEM_ALANLARI:
        if len({json.dumps(k.hakem_manifesti.get(alan), sort_keys=True) for k in kosumlar}) != 1:
            raise AnalizHatasi(f"koşumlar farklı hakem ayarıyla puanlanmış ('{alan}' aynı değil)")
    if kosumlar[0].bolme == "test":
        nihai_denetimi(kosumlar, eksikle)
    kosumlar.sort(key=lambda k: (SIRA.get(k.kisa_ad, 99), k.kisa_ad))
    ad = {k.kisa_ad: k for k in kosumlar}
    karsilastirmalar = [
        olcut.karsilastir(ad[e], ad[y], eksikle, onyukleme_n, tohum)
        for (e, y) in olcut.HIPOTEZLER if e in ad and y in ad]
    ozet = {
        "bolme": kosumlar[0].bolme, "hakem": hakem, "cumle_kurali": cumle.CUMLE_KURALI_SURUMU,
        "onyukleme_n": onyukleme_n, "tohum": tohum, "eksikle": eksikle, "uretildi": simdi().isoformat(),
        "hakem_sistem_metni_sha256": kosumlar[0].hakem_manifesti.get("sistem_metni_sha256"),
        "elle_dosyalari": {k.kisa_ad: (kosum.sha256_dosya(pathlib.Path(d) / "elle.jsonl")
                                       if (pathlib.Path(d) / "elle.jsonl").is_file() else None)
                           for k, d in zip(yuklenen, kosum_dizinleri)},
        "kosumlar": [olcut.tek_kosum(k, eksikle, onyukleme_n, tohum) for k in kosumlar],
        "karsilastirmalar": karsilastirmalar,
        "hipotez_kararlari": olcut.hipotez_kararlari(karsilastirmalar, h2_kesifsel),
    }
    if cikti is None:
        damga = min(k.kimlik for k in kosumlar).split("_", 1)[0]
        cikti = depo / "eval" / "results" / "tablolar" / f"{ozet['bolme']}_{damga}"
    cikti = pathlib.Path(cikti)
    cikti.mkdir(parents=True, exist_ok=True)
    (cikti / "ozet.json").write_text(json.dumps(ozet, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                                     encoding="utf-8")
    (cikti / "tablolar.md").write_text(rapor.yaz(ozet), encoding="utf-8")
    return cikti


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="eval.analiz", description=__doc__.splitlines()[0])
    ap.add_argument("--kosum", action="append", required=True, type=pathlib.Path, help="ham koşum klasörü")
    ap.add_argument("--hakem", default="hakem_opus", help="hakem konfigürasyonunun adı")
    ap.add_argument("--cikti", type=pathlib.Path)
    ap.add_argument("--onyukleme", type=int, default=10_000, help="yeniden örnekleme sayısı")
    ap.add_argument("--tohum", type=int, default=VARSAYILAN_TOHUM)
    ap.add_argument("--eksikle", action="store_true", help="hakem etiketi eksik maddeleri dışarıda bırak")
    ap.add_argument("--h2-kesifsel", action="store_true", help="H2'yi doğrulayıcı aileden çıkar (§9.7)")
    ap.add_argument("--depo", type=pathlib.Path, default=kosum.ROOT, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    try:
        cikti = analiz(args.kosum, args.hakem, args.cikti, args.onyukleme, args.tohum, args.eksikle,
                       args.h2_kesifsel, args.depo)
    except AnalizHatasi as e:
        print(f"HATA: {e}", file=sys.stderr)
        return 1
    print(f"Tablolar yazıldı: {cikti}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
