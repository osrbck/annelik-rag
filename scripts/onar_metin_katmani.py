"""Metin katmanı bozuk bir PDF'in yazı tiplerine harf eşlemesi (ToUnicode) ekler.

Sorun: bazı belgelerde (ör. MoH-BCE-2018) Türkçe harf içeren sözcükler, harf eşlemesi taşımayan
ayrı bir alt yazı tipiyle (Type0, Identity-H) basılmıştır. Metin çıkarıcılar bu durumda harf yerine
glif numarasını verir: "değerlendirin" yerine "ĚĞŒĞƌůĞŶĚŝƌŝŶ", "İ" yerine "7".

Onarım: glif numarası -> harf tablosu **belgenin kendisinden** öğrenilir. Aynı yazı tipi ailesinin
(Calibri, Arial ...) eşlemesi sağlam alt kümeleri aynı glif numaralarını kullanır; onların ToUnicode
tabloları birleştirilir ve eşlemesiz alt kümelere yazılır. Belgede hiç eşlemesi bulunmayan glifler
aşağıdaki EK_TABLO'dan alınır; orada da yoksa metne ⟦aile:numara⟧ işareti düşer ki gözden kaçmasın.

Ham dosyaya dokunulmaz (hash'i kayıt defterinde sabittir). Çıktı kb/raw/_onarilmis/ altına yazılır;
kb/raw/ depoya girmez. Sayfa içeriği (çizim komutları) değişmez, yalnız yazı tipi sözlüklerine
/ToUnicode eklenir.

İkinci sorun (ör. MoH-DSB-2014): yazı tipinin eşlemesi vardır ama üç Türkçe harfi yanlış harfe
bağlar ("ş" yerine "Ģ"). Bunlar YANLIS_HARF tablosuyla aynı kopyada düzeltilir.

Metni resim olarak basılmış sayfalar (akış şeması görselleri, kapak) bu yolla onarılamaz; onlar
için --ocr ile sayfa başına OCR metni üretilir. OCR metni metin katmanı kadar güvenilir değildir
(özellikle sayılarda) ve yalnız ek olarak kullanılır.

Kullanım:
  .venv/bin/python scripts/onar_metin_katmani.py MoH-BCE-2018
  .venv/bin/python scripts/onar_metin_katmani.py MoH-BCE-2018 --rapor   yalnız say, dosya yazma
  .venv/bin/python scripts/onar_metin_katmani.py MoH-BCE-2018 --ocr 1,61-65,150,215,233-236

Bu betik scripts/ altındaki diğerlerinden farklı olarak pypdf ister (requirements.txt); --ocr için
ayrıca sistemde pdftoppm, pdftotext (poppler-utils) ve tesseract (Türkçe dil paketiyle) gerekir.
Çıkış kodu: 0 = bütün glifler eşlendi, 2 = eşlenmeyen glif kaldı (dosya yine yazılır).
"""
import argparse
import collections
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "kb" / "raw"
CIKTI = RAW / "_onarilmis"

# Uzun ad önce gelmeli: "arialunicodems", "arial"dan farklı bir glif sırası kullanır.
AILELER = ("calibri", "arialunicodems", "arial", "timesnewroman", "symbol", "wingdings", "cambria",
           "myriadpro", "segoeuisymbol", "msgothic", "tahoma", "batang")
METIN_AILELERI = ("calibri", "arialunicodems", "arial", "timesnewroman", "cambria", "tahoma")

# Glif numarası ASCII kodundan sabit bir kayma ile elde edilen aileler: (ilk, son, kayma).
# Arial ve Times New Roman'da boşluk 3, "A" 36, "a" 68'dir (kod - 29); Batang'da kod + 39.
# Belgeden öğrenilen tabloyla çakışan her değer koşumda karşılaştırılır.
KURAL = {
    "arial": (3, 97, 29), "arialunicodems": (3, 97, 29), "timesnewroman": (3, 97, 29),
    "batang": (71, 165, -39),
}

# Belgede eşlemesi hiç bulunmayan glifler. Her satır, onarılmış metindeki ⟦aile:numara⟧ işaretinin
# sayfa görüntüsündeki karşılığına bakılarak belirlendi (MoH-BCE-2018, 2026-11-13). Derece işaretinin
# üç ayrı biçimi (halka, üst simge o) "°" olarak, görünmeyen glifler boşluk olarak yazıldı.
EK_TABLO: dict[str, dict[int, str]] = {
    "calibri": {425: "tt", 449: "w", 465: "°", 535: "°", 892: "•", 919: '"', 1085: "+", 1103: " ",
                1111: "→"},
    "timesnewroman": {103: "Ö", 179: "“", 180: "”", 213: "ı", 247: "ğ", 249: "Ş", 250: "ş", 846: "☐"},
    "arialunicodems": {243: "ı", 288: "Ş", 289: "ş"},
    "batang": {205: "Ç", 220: "Ö", 310: "İ"},
    "symbol": {3: " ", 16: "–", 106: "♥", 113: "°", 120: "•"},
    "wingdings": {57: "✓", 59: "☑", 121: "•", 131: "▪", 134: "☐", 190: "➢"},
    "myriadpro": {1: " ", 116: "•"},
    "segoeuisymbol": {1407: "☐"},
}

# Eşlemesi olan yazı tiplerinde özel kullanım alanına (PUA) düşmüş değerler. Metin ailelerinde
# U+F0F5 noktasız ı'dır (Mac Roman 0xF5); simge ailelerinde U+F0A3 boş onay kutusudur.
PUA_METIN = {"\uf0f5": "ı"}
PUA_SIMGE = {"\uf0a3": "☐", "\uf0b7": "•"}

# Eşlemesi olan ama Türkçe harfi yanlış harfe bağlayan yazı tipleri (ör. MoH-DSB-2014, Word 2010
# çıktısı): "ş" yerine "Ģ", "Ş" yerine "ġ", "İ" yerine "Ġ" çıkar ("başkanlığı" -> "baĢkanlığı").
# Bu üç harf Türkçede yoktur (Letonca ve Maltaca harfleridir); metin ailelerinde düzeltilir.
YANLIS_HARF = {"\u0122": "ş", "\u0121": "Ş", "\u0120": "İ"}


def aile(temel_ad: str) -> str:
    """'ABCDEE+Calibri,Bold' -> 'calibri'. Biçemler (kalın, eğik) aynı glif sırasını paylaşır."""
    ad = temel_ad.split("+")[-1].lower()
    ad = re.sub(r"#[0-9a-f]{2,6}", "", ad).replace(" ", "")
    for a in AILELER:
        if ad.startswith(a):
            return a
    return re.split(r"[,\-]", ad)[0]


def cmap_coz(veri: bytes) -> dict[int, str]:
    """ToUnicode CMap akışından kod -> metin sözlüğü."""
    m: dict[int, str] = {}
    t = veri.decode("latin-1")

    def u(hexmetin: str) -> str:
        return bytes.fromhex(hexmetin).decode("utf-16-be", "replace")

    for blok in re.findall(r"beginbfchar(.*?)endbfchar", t, re.S):
        for a, b in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]*)>", blok):
            m[int(a, 16)] = u(b)
    for blok in re.findall(r"beginbfrange(.*?)endbfrange", t, re.S):
        for a, b, liste in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*\[(.*?)\]", blok, re.S):
            for i, c in enumerate(re.findall(r"<([0-9A-Fa-f]*)>", liste)):
                m[int(a, 16) + i] = u(c)
        blok = re.sub(r"\[.*?\]", "", blok, flags=re.S)
        for a, b, c in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", blok):
            ilk = u(c)
            for i in range(int(b, 16) - int(a, 16) + 1):
                m[int(a, 16) + i] = ilk[:-1] + chr(ord(ilk[-1]) + i)
    return m


def cmap_yaz(esleme: dict[int, str], genislik: int = 2) -> bytes:
    """kod -> metin sözlüğünden ToUnicode CMap akışı. genislik: kodun bayt sayısı (Type0'da 2)."""
    h = 2 * genislik
    satirlar = [f"<{k:0{h}X}> <{v.encode('utf-16-be').hex().upper()}>" for k, v in sorted(esleme.items())]
    govde = []
    for i in range(0, len(satirlar), 100):
        parca = satirlar[i:i + 100]
        govde.append(f"{len(parca)} beginbfchar\n" + "\n".join(parca) + "\nendbfchar")
    return ("/CIDInit /ProcSet findresource begin\n12 dict begin\nbegincmap\n"
            "/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def\n"
            "/CMapName /Adobe-Identity-UCS def\n/CMapType 2 def\n"
            f"1 begincodespacerange\n<{'00' * genislik}> <{'FF' * genislik}>\nendcodespacerange\n"
            + "\n".join(govde) +
            "\nendcmap\nCMapName currentdict /CMap defineresource pop\nend\nend\n").encode("ascii")


def _ozel_alan(metin: str) -> bool:
    return any(0xE000 <= ord(c) <= 0xF8FF or c == "�" for c in metin)


def yazi_tipleri(belge):
    """Belgedeki bütün yazı tipi sözlüklerini (sayfa ve iç içe form kaynakları) bir kez verir:
    (nesne numarası, sözlük, ilk görüldüğü sayfa)."""
    gorulen: set = set()
    kaynak_gorulen: set = set()

    def gez(kaynaklar, sayfa_no):
        if kaynaklar is None:
            return
        kaynaklar = kaynaklar.get_object()
        if id(kaynaklar) in kaynak_gorulen:
            return
        kaynak_gorulen.add(id(kaynaklar))
        for f in (kaynaklar.get("/Font") or {}).values():
            ref = getattr(f, "indirect_reference", None)
            nesne = f.get_object()
            anahtar = ref.idnum if ref is not None else id(nesne)
            if anahtar not in gorulen:
                gorulen.add(anahtar)
                yield anahtar, nesne, sayfa_no
        for x in (kaynaklar.get("/XObject") or {}).values():
            x = x.get_object()
            if x.get("/Subtype") == "/Form":
                yield from gez(x.get("/Resources"), sayfa_no)

    for no, sayfa in enumerate(belge.pages, 1):
        yield from gez(sayfa.get("/Resources"), no)


def genislik_cidleri(tip0) -> set[int]:
    """Alt yazı tipinin /W dizisinde genişliği verilen CID'ler."""
    alt = tip0["/DescendantFonts"][0].get_object()
    w = alt.get("/W")
    cidler: set[int] = set()
    if w is None:
        return cidler
    w = [x.get_object() if hasattr(x, "get_object") else x for x in w.get_object()]
    i = 0
    while i < len(w):
        ilk = int(w[i])
        if isinstance(w[i + 1], list):
            cidler.update(range(ilk, ilk + len(w[i + 1])))
            i += 2
        else:
            cidler.update(range(ilk, int(w[i + 1]) + 1))
            i += 3
    return cidler


def tablo_ogren(belge) -> tuple[dict, dict]:
    """Eşlemesi sağlam Type0 yazı tiplerinden aile -> {CID: harf}. Çelişkiler ayrıca döner."""
    oylar: dict = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for _, f, _ in yazi_tipleri(belge):
        if f.get("/Subtype") != "/Type0" or "/ToUnicode" not in f:
            continue
        a = aile(str(f.get("/BaseFont", "/?"))[1:])
        for cid, metin in cmap_coz(f["/ToUnicode"].get_object().get_data()).items():
            if metin and not _ozel_alan(metin):
                oylar[a][cid][metin] += 1
    tablo = {a: {c: o.most_common(1)[0][0] for c, o in cidler.items()} for a, cidler in oylar.items()}
    celiski = {a: {c: dict(o) for c, o in cidler.items() if len(o) > 1} for a, cidler in oylar.items()}
    return tablo, {a: c for a, c in celiski.items() if c}


def onar(kaynak: pathlib.Path, hedef: pathlib.Path | None) -> dict:
    try:
        from pypdf import PdfReader, PdfWriter
        from pypdf.generic import DecodedStreamObject, NameObject
    except ImportError as e:
        raise SystemExit("'pypdf' kurulu değil: .venv/bin/pip install -r requirements.txt") from e

    belge = PdfWriter(clone_from=str(kaynak)) if hedef else PdfReader(str(kaynak))
    tablo, celiski = tablo_ogren(belge)
    kural_celiski: dict = {}
    for a, (ilk, son, kayma) in KURAL.items():
        ogrenilen = tablo.setdefault(a, {})
        for cid in range(ilk, son + 1):
            harf = chr(cid + kayma)
            if cid in ogrenilen and ogrenilen[cid] != harf:
                kural_celiski.setdefault(a, {})[cid] = (ogrenilen[cid], harf)
            ogrenilen.setdefault(cid, harf)
    for a, ek in EK_TABLO.items():
        tablo.setdefault(a, {})
        for cid, harf in ek.items():
            tablo[a].setdefault(cid, harf)

    # 1) Eşlemesi olan yazı tiplerindeki yanlış harfleri ve özel alan (PUA) değerlerini düzelt.
    harf_duzeltilen = collections.Counter()
    pua_duzeltilen = collections.Counter()
    pua_kalan = collections.Counter()
    for _, f, _ in list(yazi_tipleri(belge)):
        if "/ToUnicode" not in f:
            continue
        a = aile(str(f.get("/BaseFont", "/?"))[1:])
        cm = cmap_coz(f["/ToUnicode"].get_object().get_data())
        pua = PUA_METIN if a in METIN_AILELERI else PUA_SIMGE
        degisti = False
        for kod, metin in cm.items():
            if a in METIN_AILELERI and any(c in YANLIS_HARF for c in metin):
                metin = cm[kod] = "".join(YANLIS_HARF.get(c, c) for c in metin)
                harf_duzeltilen[a] += 1
                degisti = True
            if not _ozel_alan(metin):
                continue
            yeni = "".join(pua.get(c, c) for c in metin)
            if _ozel_alan(yeni):
                pua_kalan[(a, yeni)] += 1
                continue
            cm[kod] = yeni
            pua_duzeltilen[a] += 1
            degisti = True
        if degisti and hedef:
            genislik = 2 if f.get("/Subtype") == "/Type0" else 1
            akis = DecodedStreamObject()
            akis.set_data(cmap_yaz(cm, genislik))
            f[NameObject("/ToUnicode")] = belge._add_object(akis)

    # 2) Eşlemesi olmayan Type0 yazı tiplerine eşleme ekle.

    onarilan = collections.Counter()
    eslenmeyen: dict = collections.defaultdict(dict)  # aile -> {CID: (yazı tipi sayısı, örnek sayfa)}
    for _, f, sayfa_no in list(yazi_tipleri(belge)):
        if f.get("/Subtype") != "/Type0" or "/ToUnicode" in f:
            continue
        a = aile(str(f.get("/BaseFont", "/?"))[1:])
        bilinen = tablo.get(a, {})
        esleme = dict(bilinen)
        for cid in genislik_cidleri(f):
            if cid not in bilinen:
                esleme[cid] = f"⟦{a}:{cid}⟧"
                n, ilk = eslenmeyen[a].get(cid, (0, sayfa_no))
                eslenmeyen[a][cid] = (n + 1, ilk)
        onarilan[a] += 1
        if hedef:
            akis = DecodedStreamObject()
            akis.set_data(cmap_yaz(esleme))
            f[NameObject("/ToUnicode")] = belge._add_object(akis)
    if hedef:
        hedef.parent.mkdir(parents=True, exist_ok=True)
        with hedef.open("wb") as cikti:
            belge.write(cikti)
    return {"onarilan": dict(onarilan), "eslenmeyen": {a: dict(v) for a, v in eslenmeyen.items()},
            "celiski": celiski, "kural_celiski": kural_celiski,
            "harf_duzeltilen": dict(harf_duzeltilen),
            "pua_duzeltilen": dict(pua_duzeltilen), "pua_kalan": dict(pua_kalan),
            "tablo_boyutu": {a: len(t) for a, t in tablo.items()}}


def sayfa_listesi(metin: str) -> list[int]:
    """'1,61-65,150' -> [1, 61, 62, 63, 64, 65, 150]"""
    sayfalar: set[int] = set()
    for parca in metin.split(","):
        ilk, _, son = parca.strip().partition("-")
        sayfalar.update(range(int(ilk), int(son or ilk) + 1))
    return sorted(sayfalar)


def _sozcukler(metin: str) -> list[str]:
    kucuk = metin.replace("İ", "i").replace("I", "ı").lower()
    return [w for w in re.findall(r"[^\W\d_]+", kucuk) if len(w) >= 4]


def pgm_dondur(veri: bytes, aci: int) -> bytes:
    """Gri (P5) görüntüyü saat yönünün tersine 90 ya da 270 derece döndürür."""
    m = re.match(rb"P5\s+(\d+)\s+(\d+)\s+(\d+)\s", veri)
    if not m or aci not in (90, 270):
        raise ValueError("yalnız P5 görüntü ve 90/270 derece desteklenir")
    g, y = int(m.group(1)), int(m.group(2))
    piksel = veri[m.end():m.end() + g * y]
    if aci == 90:
        satirlar = [piksel[(g - 1 - j)::g] for j in range(g)]
    else:
        satirlar = [piksel[j::g][::-1] for j in range(g)]
    return b"P5\n%d %d\n%s\n" % (y, g, m.group(3)) + b"".join(satirlar)


def ocr(kaynak: pathlib.Path, onarilmis: pathlib.Path, sayfalar: list[int], hedef: pathlib.Path) -> list:
    """Verilen sayfaları üç yönde OCR'lar; belgenin kendi sözcük dağarcığına en çok uyan yönü yazar."""
    def calistir(*komut) -> str:
        return subprocess.run(komut, check=True, capture_output=True, text=True).stdout

    dagarcik = set(_sozcukler(calistir("pdftotext", "-layout", str(onarilmis), "-")))
    hedef.mkdir(parents=True, exist_ok=True)
    sonuc = []
    with tempfile.TemporaryDirectory() as gecici:
        g = pathlib.Path(gecici)
        for no in sayfalar:
            calistir("pdftoppm", "-r", "200", "-gray", "-f", str(no), "-l", str(no), "-singlefile",
                     str(kaynak), str(g / "sayfa"))
            ham = (g / "sayfa.pgm").read_bytes()
            en_iyi = (-1, 0, "")
            for aci in (0, 90, 270):
                (g / "yon.pgm").write_bytes(ham if aci == 0 else pgm_dondur(ham, aci))
                metin = calistir("tesseract", str(g / "yon.pgm"), "-", "-l", "tur", "--psm", "3")
                puan = sum(1 for w in _sozcukler(metin) if w in dagarcik)
                if puan > en_iyi[0]:
                    en_iyi = (puan, aci, metin)
            (hedef / f"s{no:03d}.txt").write_text(en_iyi[2], encoding="utf-8")
            sonuc.append((no, en_iyi[1], en_iyi[0]))
    return sonuc


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("belge_id", help="kb/raw/<belge_id>.pdf")
    ap.add_argument("--rapor", action="store_true", help="dosya yazma, yalnız say")
    ap.add_argument("--ocr", metavar="SAYFALAR", help="metni resim olan sayfalar için OCR, ör. 1,61-65")
    a = ap.parse_args()
    kaynak = RAW / f"{a.belge_id}.pdf"
    if not kaynak.is_file():
        print(f"bulunamadı: {kaynak}", file=sys.stderr)
        return 1
    if a.ocr:
        onarilmis = CIKTI / kaynak.name
        if not onarilmis.is_file():
            print(f"önce onarılmış kopyayı üretin: {onarilmis.relative_to(ROOT)}", file=sys.stderr)
            return 1
        hedef = CIKTI / f"{a.belge_id}.ocr"
        for no, aci, puan in ocr(kaynak, onarilmis, sayfa_listesi(a.ocr), hedef):
            print(f"s.{no}: yön {aci}°, belgenin dağarcığından {puan} sözcük")
        print(f"yazıldı: {hedef.relative_to(ROOT)}/")
        return 0
    hedef = None if a.rapor else CIKTI / kaynak.name
    s = onar(kaynak, hedef)
    print("onarılan yazı tipi (aile: adet): " + ", ".join(f"{k}: {v}" for k, v in sorted(s["onarilan"].items())))
    for aile_adi, c in s["celiski"].items():
        print(f"öğrenilen tabloda çelişki, çoğunluk alındı ({aile_adi}): {len(c)} glif")
    for aile_adi, c in s["kural_celiski"].items():
        print(f"kural ile öğrenilen tablo uyuşmuyor ({aile_adi}): {c}")
    if s["harf_duzeltilen"]:
        print("yanlış harfi düzeltilen eşleme (aile: adet): "
              + ", ".join(f"{k}: {v}" for k, v in sorted(s["harf_duzeltilen"].items())))
    if s["pua_duzeltilen"]:
        print("özel alan değeri düzeltilen eşleme (aile: adet): "
              + ", ".join(f"{k}: {v}" for k, v in sorted(s["pua_duzeltilen"].items())))
    for (aile_adi, deger), n in sorted(s["pua_kalan"].items()):
        print(f"özel alan değeri kaldı ({aile_adi}): {[hex(ord(c)) for c in deger]} × {n}")
    for aile_adi, cidler in sorted(s["eslenmeyen"].items()):
        print(f"eşlenmeyen ({aile_adi}): " + " ".join(
            f"{cid}[{n} yazı tipi, ilk s.{ilk}]" for cid, (n, ilk) in sorted(cidler.items())))
    if hedef:
        print(f"yazıldı: {hedef.relative_to(ROOT)}")
    return 2 if s["eslenmeyen"] or s["kural_celiski"] else 0


if __name__ == "__main__":
    sys.exit(main())
