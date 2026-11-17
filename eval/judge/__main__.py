"""Hakem koşturucusu.

Kullanım:
  python3 -m eval.judge puanla --kosum eval/results/raw/<koşum> [--konfig configs/hakem.yaml]
                               [--hakem sahte] [--sinir N] [--yeniden]

Çıkış kodu: 0 = bütün yanıtlar puanlandı, 1 = hata ya da hakem hatasıyla kalan yanıt var
(aynı komut yeniden çalıştırılınca yalnız eksikler puanlanır).
"""
import argparse
import pathlib
import sys

from . import puanla as puanlama


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="eval.judge", description=__doc__.splitlines()[0])
    alt = ap.add_subparsers(dest="komut", required=True)
    p = alt.add_parser("puanla", help="bir koşumun yanıtlarını hakeme puanlat")
    p.add_argument("--kosum", required=True, type=pathlib.Path, help="ham koşum klasörü")
    p.add_argument("--konfig", type=pathlib.Path, default=puanlama.ROOT / "configs" / "hakem.yaml")
    p.add_argument("--hakem", choices=["anthropic", "sahte"], default="anthropic")
    p.add_argument("--sinir", type=int, help="en çok N yanıt")
    p.add_argument("--yeniden", action="store_true", help="önceki puanlamayı at, baştan puanla")
    p.add_argument("--depo", type=pathlib.Path, default=puanlama.ROOT, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    try:
        return puanlama.puanla(args.kosum, args.konfig, hakem=args.hakem, sinir=args.sinir,
                               yeniden=args.yeniden, depo=args.depo)
    except (puanlama.HakemHatasi, RuntimeError) as e:
        print(f"HATA: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
