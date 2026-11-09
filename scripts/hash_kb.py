"""kb/raw altındaki her belgenin SHA-256'sını hesaplar ve kayıt defterine yazar."""
import csv, hashlib, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "kb" / "raw"
REG = ROOT / "kb" / "registry" / "belge_kayit_defteri.csv"

def sha256(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    rows = list(csv.DictReader(REG.open(encoding="utf-8")))
    fields = list(rows[0].keys())
    if "hash" not in fields:
        fields.append("hash")
    for r in rows:
        f = RAW / f"{r['belge_id']}.pdf"
        r["hash"] = sha256(f) if f.exists() else r.get("hash", "")
        print(f"{r['belge_id']:16} {'OK ' + r['hash'][:12] if f.exists() else 'eksik'}")
    with REG.open("w", encoding="utf-8", newline="") as out:
        w = csv.DictWriter(out, fieldnames=fields); w.writeheader(); w.writerows(rows)

if __name__ == "__main__":
    sys.exit(main())
