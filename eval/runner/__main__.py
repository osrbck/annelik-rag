"""Değerlendirme koşturucusu.

Kullanım:
  python3 -m eval.runner dogrula [--bolme dev|test|hepsi] [--hedef] [--asama2]
  python3 -m eval.runner kos --konfig configs/K0.yaml [--konfig ...] [--bolme dev]
                             [--setler s_ana,s_yas] [--uretici sahte] [--sinir N]
                             [--nihai] [--cikti KLASÖR]

Çıkış kodu: 0 = tamam, 1 = hata (doğrulama hatası, koruma, eksik veri).
"""
import argparse
import pathlib
import sys

from . import kosum, veri


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="eval.runner", description=__doc__.splitlines()[0])
    alt = ap.add_subparsers(dest="komut", required=True)

    d = alt.add_parser("dogrula", help="veri setlerini doğrula")
    d.add_argument("--bolme", choices=[*veri.BOLMELER, "hepsi"], default="hepsi")
    d.add_argument("--hedef", action="store_true", help="protokol §4 sayı hedeflerini de denetle")
    d.add_argument("--asama2", action="store_true",
                   help="altın yanıt koşumu bitti say: işlenmemiş madde, etiketsiz S-ANA ve yarım aile hata olur")
    d.add_argument("--kok", type=pathlib.Path, default=veri.VERI_KOKU, help="veri seti kökü")
    d.add_argument("--kayit", type=pathlib.Path, default=veri.KAYIT, help=argparse.SUPPRESS)

    k = alt.add_parser("kos", help="konfigürasyonları koştur")
    k.add_argument("--konfig", action="append", required=True, type=pathlib.Path)
    k.add_argument("--bolme", choices=list(veri.BOLMELER))
    k.add_argument("--setler", help="virgülle ayrılmış set listesi")
    k.add_argument("--uretici", choices=["anthropic", "sahte"], default="anthropic")
    k.add_argument("--sinir", type=int, help="en çok N madde")
    k.add_argument("--nihai", action="store_true", help="test bölmesi için nihai koşum")
    k.add_argument("--cikti", help="devam edilecek mevcut koşum klasörü")
    k.add_argument("--depo", type=pathlib.Path, default=kosum.ROOT, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)

    if args.komut == "dogrula":
        bolmeler = veri.BOLMELER if args.bolme == "hepsi" else (args.bolme,)
        sonuc = veri.dogrula(args.kok, bolmeler, args.kayit, args.hedef, args.asama2)
        veri.rapor_yaz(sonuc)
        return 1 if sonuc.hatalar else 0

    try:
        return kosum.kos(
            args.konfig, bolme=args.bolme,
            setler=args.setler.split(",") if args.setler else None,
            uretici=args.uretici, sinir=args.sinir, nihai=args.nihai,
            cikti=args.cikti, depo=args.depo)
    except (kosum.KosumHatasi, RuntimeError) as e:
        print(f"HATA: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
