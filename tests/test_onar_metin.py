"""scripts/onar_metin_katmani.py: PDF gerektirmeyen yardımcıların testleri."""
import importlib.util
import pathlib
import unittest

YOL = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "onar_metin_katmani.py"
_spec = importlib.util.spec_from_file_location("onar_metin_katmani", YOL)
onar = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(onar)


class Yardimcilar(unittest.TestCase):
    def test_aile(self):
        self.assertEqual(onar.aile("ABCDEE+Calibri,Bold"), "calibri")
        self.assertEqual(onar.aile("ZYIQWP+Calibri-Bold"), "calibri")
        self.assertEqual(onar.aile("XYZABC+ArialUnicodeMS"), "arialunicodems")
        self.assertEqual(onar.aile("RUFUOF+Arial-BoldMT"), "arial")
        self.assertEqual(onar.aile("ABCDEF+Times#2320New#2320Roman,Bold"), "timesnewroman")
        self.assertEqual(onar.aile("QWERTY+Bilinmeyen-Italic"), "bilinmeyen")

    def test_cmap_gidis_donus(self):
        esleme = {3: " ", 55: "İ", 338: "ğ", 358: "ı", 425: "tt", 1111: "→"}
        self.assertEqual(onar.cmap_coz(onar.cmap_yaz(esleme)), esleme)
        tek_bayt = {0x41: "A", 0xF5: "ı"}
        akis = onar.cmap_yaz(tek_bayt, genislik=1)
        self.assertIn(b"<00> <FF>", akis)
        self.assertEqual(onar.cmap_coz(akis), tek_bayt)

    def test_cmap_yuz_satirlik_bloklar(self):
        esleme = {i: chr(0x100 + i) for i in range(250)}
        akis = onar.cmap_yaz(esleme)
        self.assertEqual(akis.count(b"beginbfchar"), 3)
        self.assertEqual(onar.cmap_coz(akis), esleme)

    def test_cmap_aralik_bicimleri(self):
        akis = (b"2 beginbfrange\n<0010> <0012> <0041>\n<0020> <0021> [<011E> <015E>]\nendbfrange\n"
                b"1 beginbfchar\n<0030> <00660069>\nendbfchar\n")
        self.assertEqual(onar.cmap_coz(akis),
                         {0x10: "A", 0x11: "B", 0x12: "C", 0x20: "Ğ", 0x21: "Ş", 0x30: "fi"})

    def test_kural_ve_ek_tablo_tutarli(self):
        for aile_adi, (ilk, son, kayma) in onar.KURAL.items():
            self.assertEqual(chr(ilk + kayma), " ", aile_adi)   # aralık boşlukla başlar
            self.assertEqual(chr(son + kayma), "~", aile_adi)   # ve ASCII'nin sonunda biter
            for cid in onar.EK_TABLO.get(aile_adi, {}):
                self.assertFalse(ilk <= cid <= son, f"{aile_adi}:{cid} hem kuralda hem ek tabloda")

    def test_yanlis_harf_tablosu(self):
        turkce = set("abcçdefgğhıijklmnoöprsştuüvyzABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ")
        for yanlis, dogru in onar.YANLIS_HARF.items():
            self.assertNotIn(yanlis, turkce)   # düzeltilen harf Türkçe metinde geçemez
            self.assertIn(dogru, turkce)
        metin = "".join(onar.YANLIS_HARF.get(c, c) for c in "BaĢkanlığı, SUNUġ, Ġl")
        self.assertEqual(metin, "Başkanlığı, SUNUŞ, İl")

    def test_sayfa_listesi(self):
        self.assertEqual(onar.sayfa_listesi("1,61-65, 150"), [1, 61, 62, 63, 64, 65, 150])

    def test_pgm_dondur(self):
        # 3x2 görüntü:  1 2 3
        #               4 5 6
        veri = b"P5\n3 2\n255\n" + bytes([1, 2, 3, 4, 5, 6])
        self.assertEqual(onar.pgm_dondur(veri, 90), b"P5\n2 3\n255\n" + bytes([3, 6, 2, 5, 1, 4]))
        self.assertEqual(onar.pgm_dondur(veri, 270), b"P5\n2 3\n255\n" + bytes([4, 1, 5, 2, 6, 3]))
        with self.assertRaises(ValueError):
            onar.pgm_dondur(veri, 180)


if __name__ == "__main__":
    unittest.main()
