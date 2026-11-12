"""kb/raw altındaki belgelerin SHA-256'sını hesaplar ve kayıt defterine yazar.

Bir kayıt (belge_id) iki biçimde saklanabilir:
  kb/raw/<belge_id>.<uzantı>   tek dosya (pdf, html, xlsx ...)
  kb/raw/<belge_id>/           birden çok dosya (ör. dernek rehberleri, WHO tabloları)

Klasör için hash, içindeki dosyaların "<sha256>  <göreli yol>" satırlarının
sıralı listesinin SHA-256'sıdır; dosya eklenir, silinir ya da değişirse değişir.

Kullanım:
  python scripts/hash_kb.py              yeni hash'leri yazar; kayıtlı hash'i ASLA ezmez
  python scripts/hash_kb.py --kontrol    hiçbir şey yazmaz, yalnız doğrular
  python scripts/hash_kb.py --guncelle   değişen belgelerin hash'ini bilerek günceller

Çıkış kodu: 0 = tutarlı, 1 = kayıtlı hash ile dosya uyuşmuyor ya da kayıt hatalı.
"""
import argparse
import csv
import hashlib
import os
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "kb" / "raw"
REG = ROOT / "kb" / "registry" / "belge_kayit_defteri.csv"

# kb/registry/README.md ile aynı tutulmalı.
GECERLI_DURUM = {"araştırılacak", "indirilecek", "izin yazısı", "onaylı", "işlendi"}
HASH_ZORUNLU = {"onaylı", "işlendi"}


def sha256_dosya(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for parca in iter(lambda: f.read(1 << 20), b""):
            h.update(parca)
    return h.hexdigest()


def sha256_klasor(d: pathlib.Path) -> tuple[str, int]:
    dosyalar = sorted(
        p for p in d.rglob("*")
        if p.is_file() and not any(b.startswith(".") for b in p.relative_to(d).parts)
    )
    h = hashlib.sha256()
    for p in dosyalar:
        h.update(f"{sha256_dosya(p)}  {p.relative_to(d).as_posix()}\n".encode("utf-8"))
    return h.hexdigest(), len(dosyalar)


def belge_hash(raw: pathlib.Path, belge_id: str) -> tuple[str | None, str]:
    """(hash, açıklama) döndürür; belge yoksa hash None'dır."""
    klasor = raw / belge_id
    tekler = [p for p in raw.glob(f"{belge_id}.*") if p.is_file()]
    if klasor.is_dir() and tekler:
        raise ValueError(f"hem klasör hem dosya var: {klasor.name}/ ve {tekler[0].name}")
    if len(tekler) > 1:
        raise ValueError("birden çok dosya eşleşti: " + ", ".join(sorted(p.name for p in tekler)))
    if klasor.is_dir():
        h, n = sha256_klasor(klasor)
        if n == 0:
            return None, "klasör boş"
        return h, f"{n} dosya"
    if tekler:
        return sha256_dosya(tekler[0]), tekler[0].name
    return None, "eksik"


def atomik_yaz(hedef: pathlib.Path, alanlar: list[str], satirlar: list[dict]) -> None:
    """Kayıt defteri tek doğruluk kaynağıdır: önce geçici dosyaya yaz, sonra yer değiştir."""
    fd, gecici = tempfile.mkstemp(dir=hedef.parent, prefix=hedef.name, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as out:
            w = csv.DictWriter(out, fieldnames=alanlar, lineterminator="\n")
            w.writeheader()
            w.writerows(satirlar)
        os.replace(gecici, hedef)
    except BaseException:
        pathlib.Path(gecici).unlink(missing_ok=True)
        raise


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mod = ap.add_mutually_exclusive_group()
    mod.add_argument("--kontrol", action="store_true", help="yazma, yalnız doğrula")
    mod.add_argument("--guncelle", action="store_true", help="değişen hash'leri güncelle")
    ap.add_argument("--raw", type=pathlib.Path, default=RAW, help=argparse.SUPPRESS)
    ap.add_argument("--kayit", type=pathlib.Path, default=REG, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)

    with args.kayit.open(encoding="utf-8", newline="") as f:
        okuyucu = csv.DictReader(f)
        alanlar = list(okuyucu.fieldnames or [])
        satirlar = list(okuyucu)
    if "belge_id" not in alanlar:
        print(f"HATA: {args.kayit} içinde 'belge_id' sütunu yok", file=sys.stderr)
        return 1
    if "hash" not in alanlar:
        alanlar.append("hash")

    sorun = False
    degisti = False
    gorulen: set[str] = set()
    for r in satirlar:
        bid = (r.get("belge_id") or "").strip()
        eski = (r.get("hash") or "").strip()
        r["hash"] = eski
        if not bid or bid in gorulen:
            print(f"{bid or '(boş)':16} HATA   belge_id boş ya da yinelenmiş")
            sorun = True
            continue
        gorulen.add(bid)
        try:
            yeni, aciklama = belge_hash(args.raw, bid)
        except ValueError as e:
            print(f"{bid:16} HATA   {e}")
            sorun = True
            continue
        if yeni is None:
            # Hash kayıtlıysa belge bir kez indirilmiş demektir; şimdi yoksa sessiz geçme.
            if eski:
                print(f"{bid:16} KAYIP  kayıtlı hash var ama dosya yok ({aciklama})")
                sorun = True
            else:
                print(f"{bid:16} {aciklama}")
        elif not eski:
            print(f"{bid:16} YENİ   {yeni[:12]}  ({aciklama})")
            if not args.kontrol:
                r["hash"] = yeni
                degisti = True
        elif eski == yeni:
            print(f"{bid:16} OK     {yeni[:12]}  ({aciklama})")
        elif args.guncelle:
            print(f"{bid:16} GÜNC.  {eski[:12]} -> {yeni[:12]}  ({aciklama})")
            r["hash"] = yeni
            degisti = True
        else:
            print(f"{bid:16} DEĞİŞTİ kayıtlı {eski[:12]} != dosya {yeni[:12]}  ({aciklama})")
            sorun = True

        durum = (r.get("durum") or "").strip()
        if "durum" in alanlar and durum not in GECERLI_DURUM:
            print(f"{bid:16} HATA   geçersiz durum: {durum!r}")
            sorun = True
        elif durum in HASH_ZORUNLU and not r["hash"] and yeni is None:
            print(f"{bid:16} HATA   durum '{durum}' ama belge kb/raw altında yok")
            sorun = True

    # Yalnızca içerik değiştiyse yaz: boş koşumda git farkı üretme.
    if degisti and not args.kontrol:
        atomik_yaz(args.kayit, alanlar, satirlar)
    if sorun:
        print("\nUyuşmazlık var. Belge bilerek yenilendiyse --guncelle ile çalıştırın "
              "ve değişikliği sapma günlüğüne yazın.", file=sys.stderr)
    return 1 if sorun else 0


if __name__ == "__main__":
    sys.exit(main())
