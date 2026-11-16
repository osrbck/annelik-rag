"""eval.runner.veri testleri. Bütün veriler geçici klasörlerde üretilir; gerçek veri dosyası okunmaz."""
import io
import json
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from eval.runner import veri  # noqa: E402

KAYIT_CSV = "belge_id,baslik,hash\nBEL-1,Bir,\nBEL-2,Iki,\n"
GIZLI = "GIZLI-SORU-METNI"


def temel(set_adi, no, bolme="dev", **ek):
    """Geçerli, 'bekliyor' durumunda bir madde."""
    onek = veri.ONEK[set_adi]
    kimlik = f"{onek}-{'D' if bolme == 'dev' else ''}{no:04d}"
    m = {
        "id": kimlik, "set": set_adi, "bolme": bolme,
        "profil": {"donem": "cocuk", "yas_ay": 8},
        "soru": f"{GIZLI} numara {no} hakkında ne yapmalıyım",
        "konu": "izlem", "beklenen_davranis": "yanitla",
        "zorunlu_ogeler": [], "yasak_ogeler": [], "kaynak": [],
        "altin_durumu": "bekliyor", "yazar": "test-yazar",
    }
    m.update(ek)
    return m


def ana(no, bolme="dev", **ek):
    return temel("s_ana", no, bolme, **ek)


def tuz(no, sinif="T1", bolme="dev", **ek):
    alanlar = {"sinif": sinif, "beklenen_davranis": veri.SINIF_DAVRANIS.get(sinif),
               "soru": f"tuzak sorusu {no} alfa beta gama delta", **ek}
    return temel("s_tuz", no, bolme, **alanlar)


def adv(no, ebeveyn, tur="A1", bolme="dev", davranis="acil_yonlendir", **ek):
    return temel("s_adv", no, bolme, ebeveyn_id=ebeveyn, saldiri_turu=tur, beklenen_davranis=davranis,
                 soru=f"saldırı sorusu {no} epsilon zeta eta theta", **ek)


def yas_cifti(no, bolme="dev", **ek):
    d = "D" if bolme == "dev" else ""
    aile = f"YAS-{d}{no:04d}"
    ortak = {"soru": f"yaş ailesi {no} ortak soru metni", "aile_id": aile}
    a = temel("s_yas", 0, bolme, **ortak, **ek)
    b = temel("s_yas", 0, bolme, **ortak, **ek)
    a["id"], b["id"] = f"{aile}-a", f"{aile}-b"
    b["profil"] = {"donem": "cocuk", "yas_ay": 30}
    return [a, b]


def yazildi(m, **ek):
    """Aşama 2 kurallarına uyan yazılmış madde: davranış maddesinde sabit öğe, kaynakta öğe numarası."""
    m = dict(m, altin_durumu="yazildi")
    if m["set"] == "s_ana":
        m["bilgi_turu"] = "rehbere_ozgu"  # altın yanıtı yazılmış S-ANA maddesinde zorunlu
    m.update(ek)
    if "zorunlu_ogeler" not in ek:
        sabit = veri.SABIT_OGE.get(m.get("beklenen_davranis"))
        m["zorunlu_ogeler"] = [sabit] if sabit else ["bir öğe"]
    if "kaynak" not in ek:
        n = len(m["zorunlu_ogeler"]) if isinstance(m["zorunlu_ogeler"], list) else 1
        onek = ",".join(f"Ö{i}" for i in range(1, max(n, 1) + 1))
        m["kaynak"] = [{"belge_id": "BEL-1", "sayfa": [3, 4], "bolum": f"[{onek}] Bölüm"}]
    return m


def yaz_veri(kok: pathlib.Path, set_adi: str, bolme: str, maddeler: list) -> None:
    (kok / set_adi).mkdir(parents=True, exist_ok=True)
    (kok / set_adi / f"{bolme}.jsonl").write_text(
        "".join(json.dumps(m, ensure_ascii=False) + "\n" for m in maddeler), encoding="utf-8")


class VeriTestTabani(unittest.TestCase):
    def setUp(self):
        self._gecici = tempfile.TemporaryDirectory()
        self.addCleanup(self._gecici.cleanup)
        self.kok = pathlib.Path(self._gecici.name) / "datasets"
        self.kok.mkdir()
        self.kayit = pathlib.Path(self._gecici.name) / "kayit.csv"
        self.kayit.write_text(KAYIT_CSV, encoding="utf-8")

    def calistir(self, veriler: dict, bolmeler=("dev", "test"), hedef=False):
        """veriler: {(set, bolme): [madde, ...]}"""
        for (s, b), maddeler in veriler.items():
            yaz_veri(self.kok, s, b, maddeler)
        return veri.dogrula(self.kok, bolmeler, self.kayit, hedef)

    def hatalar(self, *a, **k):
        return [str(s) for s in self.calistir(*a, **k).hatalar]

    def uyarilar(self, *a, **k):
        return [str(s) for s in self.calistir(*a, **k).uyarilar]

    def assertHata(self, hatalar, parca):
        self.assertTrue(any(parca in h for h in hatalar), f"{parca!r} yok: {hatalar}")


class TemelKurallar(VeriTestTabani):
    def test_gecerli_madde_ve_eksik_dosya(self):
        s = self.calistir({("s_ana", "dev"): [ana(1)]})
        self.assertEqual(s.sorunlar, [])
        self.assertEqual(s.bulunan, [("s_ana", "dev")])

    def test_json_hatasi_metin_sizdirmaz(self):
        (self.kok / "s_ana").mkdir()
        (self.kok / "s_ana" / "dev.jsonl").write_text(f'{{"soru": "{GIZLI}", bozuk\n', encoding="utf-8")
        h = [str(s) for s in veri.dogrula(self.kok, ("dev",), self.kayit).hatalar]
        self.assertHata(h, "s_ana/dev:1 json")
        self.assertFalse(any(GIZLI in x for x in h))

    def test_id_kalibi_ve_dev_d(self):
        self.assertHata(self.hatalar({("s_ana", "dev"): [ana(1, id="ANA-0001")]}), "id: kalıba")
        self.assertHata(self.hatalar({("s_ana", "test"): [ana(1, "test", id="ANA-D0001")]}, ("test",)), "id: kalıba")
        self.assertEqual(self.hatalar({("s_ana", "test"): [ana(1, "test")]}, ("test",)), [])

    def test_id_tekil(self):
        h = self.hatalar({("s_ana", "dev"): [ana(1), ana(1, soru="tamamen başka bir kelime dizisi burada")]})
        self.assertHata(h, "id: yinelenmiş")

    def test_set_ve_bolme_dosyayla_uyumlu(self):
        h = self.hatalar({("s_ana", "dev"): [ana(1, **{"set": "s_tuz"}), ana(2, bolme="test")]})
        self.assertHata(h, "set:")
        self.assertHata(h, "bolme:")

    def test_profil(self):
        gecerli = [{"donem": "gebelik", "gebelik_haftasi": 4}, {"donem": "gebelik", "gebelik_haftasi": 42},
                   {"donem": "cocuk", "yas_ay": 0, "yas_gun": 30}, {"donem": "cocuk", "yas_ay": 216}]
        gecersiz = [{"donem": "gebelik", "gebelik_haftasi": 3}, {"donem": "gebelik", "gebelik_haftasi": 43},
                    {"donem": "cocuk", "yas_ay": 217}, {"donem": "cocuk", "yas_ay": 5, "yas_gun": 2},
                    {"donem": "cocuk", "yas_ay": 0, "yas_gun": 31}, {"donem": "cocuk", "yas_ay": True},
                    {"donem": "diger"}, {"donem": "gebelik", "gebelik_haftasi": 10, "yas_ay": 1}, "x"]
        for i, p in enumerate(gecerli, 1):
            self.assertEqual(veri._profil_hatasi(p), None, p)
        for p in gecersiz:
            self.assertIsNotNone(veri._profil_hatasi(p), p)
        self.assertHata(self.hatalar({("s_ana", "dev"): [ana(1, profil={"donem": "cocuk", "yas_ay": 999})]}), "ANA-D0001 profil")

    def test_alan_degerleri(self):
        for alan, deger in [("soru", "  "), ("konu", "baska"), ("beklenen_davranis", "x"), ("altin_durumu", "x"),
                            ("yazar", ""), ("guncellik", "evet"), ("yasak_ogeler", "metin")]:
            with self.subTest(alan=alan):
                self.assertHata(self.hatalar({("s_ana", "dev"): [ana(1, **{alan: deger})]}), f"ANA-D0001 {alan}:")

    def test_bilinmeyen_alan(self):
        h = self.hatalar({("s_ana", "dev"): [ana(1, ekstra="x", ebeveyn_id="TUZ-D0001")]})
        self.assertHata(h, "ANA-D0001 ekstra: bilinmeyen alan")
        self.assertHata(h, "ANA-D0001 ebeveyn_id: bilinmeyen alan")

    def test_istege_bagli_alanlar(self):
        m = ana(1, guncellik=True, yazar_notu="", uzman_onay=None)
        m2 = ana(2, yazar_notu="serbest not", uzman_onay=None)
        self.assertEqual(self.hatalar({("s_ana", "dev"): [m, m2]}), [])
        self.assertHata(self.hatalar({("s_ana", "dev"): [ana(1, yazar_notu=5)]}), "yazar_notu")
        self.assertHata(self.hatalar({("s_ana", "dev"): [ana(1, uzman_onay="x")]}), "uzman_onay")

    def test_bilgi_turu(self):
        # Soru aşamasında isteğe bağlı, altın yanıt yazılınca zorunlu; yalnız S-ANA'da.
        self.assertEqual(self.hatalar({("s_ana", "dev"): [ana(1), ana(2, bilgi_turu="genel")]}), [])
        self.assertHata(self.hatalar({("s_ana", "dev"): [ana(1, bilgi_turu="baska")]}),
                        "ANA-D0001 bilgi_turu: geçerli")
        eksik = yazildi(ana(1))
        del eksik["bilgi_turu"]
        self.assertHata(self.hatalar({("s_ana", "dev"): [eksik]}), "ANA-D0001 bilgi_turu: altın")
        self.assertHata(self.hatalar({("s_tuz", "dev"): [tuz(1, bilgi_turu="genel")]}),
                        "TUZ-D0001 bilgi_turu: bilinmeyen alan")
        s = self.calistir({("s_ana", "dev"): [yazildi(ana(1)), ana(2, bilgi_turu="genel"), ana(3)]})
        self.assertEqual(dict(s.istatistik[("s_ana", "dev")]["bilgi_turu"]), {"rehbere_ozgu": 1, "genel": 1})

    def test_yazar_notu_yazdirilmaz(self):
        not_ = "OZEL-YAZAR-NOTU"
        m = ana(1, yazar_notu=not_, konu="yok")
        s = self.calistir({("s_ana", "test"): [dict(m, id="ANA-0001", bolme="test")]}, ("test",))
        tampon = io.StringIO()
        veri.rapor_yaz(s, tampon)
        cikti = tampon.getvalue()
        self.assertIn("ANA-0001 konu", cikti)
        for gizli in (not_, GIZLI):
            self.assertNotIn(gizli, cikti)


class UcDurumlar(VeriTestTabani):
    def test_sadelesince_bos_metin_reddedilir(self):
        for alan in ("soru", "yazar"):
            self.assertHata(self.hatalar({("s_ana", "dev"): [ana(1, **{alan: "???"})]}), f"ANA-D0001 {alan}:")
        self.assertHata(self.hatalar({("s_ana", "dev"): [yazildi(ana(1), zorunlu_ogeler=["..."])]}), "zorunlu_ogeler")

    def test_dev_uzman_onay_bos_nesne_reddedilir(self):
        self.assertHata(self.hatalar({("s_ana", "dev"): [ana(1, uzman_onay={})]}), "ANA-D0001 uzman_onay")
        self.assertEqual(self.hatalar({("s_ana", "dev"): [ana(1, uzman_onay=None)]}), [])

    def test_zorunlu_ogeler_bekliyorda_dort_ustu_olamaz(self):
        self.assertHata(self.hatalar({("s_ana", "dev"): [ana(1, zorunlu_ogeler=list("abcde"))]}), "zorunlu_ogeler")
        self.assertEqual(self.hatalar({("s_ana", "dev"): [ana(1, zorunlu_ogeler=list("abcd"))]}), [])


class AltinDurumu(VeriTestTabani):
    def test_bekliyor_bos_listelere_izin_verir(self):
        self.assertEqual(self.hatalar({("s_ana", "dev"): [ana(1)]}), [])

    def test_yazildi_gecerli(self):
        self.assertEqual(self.hatalar({("s_ana", "dev"): [yazildi(ana(1))]}), [])

    def test_zorunlu_ogeler_sayisi(self):
        self.assertHata(self.hatalar({("s_ana", "dev"): [yazildi(ana(1), zorunlu_ogeler=[])]}), "zorunlu_ogeler")
        self.assertHata(self.hatalar({("s_ana", "dev"): [yazildi(ana(1), zorunlu_ogeler=list("abcde"))]}), "zorunlu_ogeler")
        self.assertEqual(self.hatalar({("s_ana", "dev"): [yazildi(ana(1), zorunlu_ogeler=list("abcd"))]}), [])
        self.assertHata(self.hatalar({("s_ana", "dev"): [yazildi(ana(1), zorunlu_ogeler=["a", ""])]}), "zorunlu_ogeler")

    def test_kaynak(self):
        kotu = [
            [], [{"belge_id": "YOK", "sayfa": [1, 2], "bolum": "b"}],
            [{"belge_id": "BEL-1", "sayfa": [0, 2], "bolum": "b"}],
            [{"belge_id": "BEL-1", "sayfa": [5, 2], "bolum": "b"}],
            [{"belge_id": "BEL-1", "sayfa": [1], "bolum": "b"}],
            [{"belge_id": "BEL-1", "sayfa": ["1", "2"], "bolum": "b"}],
            [{"belge_id": "BEL-1", "sayfa": [1, 2]}],
        ]
        for k in kotu:
            with self.subTest(k=k):
                self.assertHata(self.hatalar({("s_ana", "dev"): [yazildi(ana(1), kaynak=k)]}), "ANA-D0001 kaynak")
        self.assertEqual(self.hatalar({("s_ana", "dev"): [yazildi(ana(1), kaynak=[
            {"belge_id": "BEL-2", "sayfa": [7, 7], "bolum": "[Ö1] b"}])]}), [])

    def test_bos_kaynak_yalniz_yanitla_disinda_serbest(self):
        m = yazildi(tuz(1, "T1"), kaynak=[])
        self.assertEqual(self.hatalar({("s_tuz", "dev"): [m]}), [])

    def test_onayli(self):
        m = yazildi(ana(1, "test", id="ANA-0001"), altin_durumu="onayli")
        self.assertHata(self.hatalar({("s_ana", "test"): [m]}, ("test",)), "uzman_onay")
        ok = dict(m, uzman_onay={"durum": "onay", "kod": "U1", "tarih": "2026-12-01"})
        self.assertEqual(self.hatalar({("s_ana", "test"): [ok]}, ("test",)), [])
        ret = dict(m, uzman_onay={"durum": "ret"})
        self.assertHata(self.hatalar({("s_ana", "test"): [ret]}, ("test",)), "uzman_onay")

    def test_dev_onayli_olamaz(self):
        m = yazildi(ana(1), altin_durumu="onayli", uzman_onay={"durum": "onay"})
        h = self.hatalar({("s_ana", "dev"): [m]})
        self.assertHata(h, "dev maddesi onaylı olamaz")


class SeteOzgu(VeriTestTabani):
    def test_s_ana_yalniz_yanitla(self):
        self.assertHata(self.hatalar({("s_ana", "dev"): [ana(1, beklenen_davranis="doz_reddet")]}), "beklenen_davranis")

    def test_s_yas_gecerli_aile(self):
        self.assertEqual(self.hatalar({("s_yas", "dev"): yas_cifti(1)}), [])

    def test_s_yas_aile_hatalari(self):
        a, b = yas_cifti(1)
        self.assertHata(self.hatalar({("s_yas", "dev"): [a]}), "tam olarak iki üye")
        self.assertHata(self.hatalar({("s_yas", "dev"): [a, dict(b, soru="farklı soru metni burada")]}), "soru:")
        self.assertHata(self.hatalar({("s_yas", "dev"): [a, dict(b, profil=a["profil"])]}), "profil:")
        self.assertHata(self.hatalar({("s_yas", "dev"): [dict(a, aile_id="YAS-D0009"), b]}), "aile_id")
        c = dict(a, id="YAS-D0001-c")
        self.assertHata(self.hatalar({("s_yas", "dev"): [a, b, c]}), "tam olarak iki üye")
        x = {k: v for k, v in a.items() if k != "aile_id"}
        self.assertHata(self.hatalar({("s_yas", "dev"): [x, b]}), "aile_id: zorunlu")

    def test_s_yas_zorunlu_ogeler_ayrismali(self):
        a, b = (yazildi(m) for m in yas_cifti(1))
        self.assertHata(self.hatalar({("s_yas", "dev"): [a, b]}), "zorunlu_ogeler: aile")
        b2 = dict(b, zorunlu_ogeler=["başka öğe"])
        self.assertEqual(self.hatalar({("s_yas", "dev"): [a, b2]}), [])
        # biri bekliyor ise kural henüz uygulanmaz
        a0, b0 = yas_cifti(1)
        self.assertEqual(self.hatalar({("s_yas", "dev"): [yazildi(a0), b0]}), [])

    def test_s_yas_varyantlar_farkli_davranista_olabilir(self):
        a, b = yas_cifti(1)
        b = dict(b, beklenen_davranis="acil_yonlendir")
        self.assertEqual(self.hatalar({("s_yas", "dev"): [a, b]}), [])

    def test_s_tuz_sinif_davranis(self):
        for sinif, d in veri.SINIF_DAVRANIS.items():
            self.assertEqual(self.hatalar({("s_tuz", "dev"): [tuz(1, sinif)]}), [], sinif)
        self.assertHata(self.hatalar({("s_tuz", "dev"): [tuz(1, "T2", beklenen_davranis="yanitla")]}), "beklenen_davranis")
        self.assertHata(self.hatalar({("s_tuz", "dev"): [tuz(1, "T9")]}), "sinif")

    def test_s_adv_ebeveyn(self):
        t = tuz(1, "T1")
        self.assertEqual(self.hatalar({("s_tuz", "dev"): [t], ("s_adv", "dev"): [adv(1, "TUZ-D0001")]}), [])
        h = self.hatalar({("s_tuz", "dev"): [t], ("s_adv", "dev"): [adv(1, "TUZ-D0099")]})
        self.assertHata(h, "ebeveyn_id")
        h = self.hatalar({("s_tuz", "dev"): [tuz(1, "T4")], ("s_adv", "dev"): [adv(1, "TUZ-D0001", davranis="kapsam_disi")]})
        self.assertHata(h, "ebeveynin sınıfı")
        h = self.hatalar({("s_tuz", "dev"): [t], ("s_adv", "dev"): [adv(1, "TUZ-D0001", davranis="doz_reddet")]})
        self.assertHata(h, "beklenen_davranis: ebeveynle")
        h = self.hatalar({("s_tuz", "dev"): [t], ("s_adv", "dev"): [adv(1, "TUZ-D0001", tur="A9")]})
        self.assertHata(h, "saldiri_turu")

    def test_s_adv_ebeveyn_ayni_bolmede(self):
        t = tuz(1, "T1", bolme="test")
        h = self.hatalar({("s_tuz", "test"): [t], ("s_adv", "dev"): [adv(1, "TUZ-0001")]})
        self.assertHata(h, "ebeveyn_id")


class Asama2(VeriTestTabani):
    """Altın yanıt aşamasının kuralları (eval/datasets/YAZIM_YONERGESI_ASAMA2.md)."""

    def a2(self, veriler, bolmeler=("dev",)):
        for (s, b), maddeler in veriler.items():
            yaz_veri(self.kok, s, b, maddeler)
        return veri.dogrula(self.kok, bolmeler, self.kayit, asama2=True)

    def test_yonerge_ile_sabitler_ayni(self):
        """Yazar modele verilen yönergedeki sabit cümleler ve etiket kodları doğrulayıcıdakilerle aynıdır."""
        yonerge = (pathlib.Path(veri.VERI_KOKU) / "YAZIM_YONERGESI_ASAMA2.md").read_text(encoding="utf-8")
        for davranis, cumle in veri.SABIT_OGE.items():
            self.assertIn(f"`{cumle}`", yonerge, davranis)
        for kod in veri.A2_ETIKETLERI:
            self.assertIn(f"`{kod}`", yonerge, kod)

    def test_etiket_cozumleme(self):
        self.assertEqual(veri.a2_etiketleri("Y12 [A2:OCR: s. 61] [A2:KISMI]"), (["OCR", "KISMI"], False))
        self.assertEqual(veri.a2_etiketleri("eşik: 12 ay"), ([], False))
        self.assertEqual(veri.a2_etiketleri(None), ([], False))
        self.assertTrue(veri.a2_etiketleri("[A2:ocr]")[1])          # küçük harf: biçim bozuk
        self.assertTrue(veri.a2_etiketleri("[A2:OCR: [iç] not]")[1])  # açıklamada köşeli parantez

    def test_etiket_ve_durum_uyumu(self):
        h = self.hatalar({("s_ana", "dev"): [ana(1, yazar_notu="[A2:UYDURMA]")]})
        self.assertHata(h, "bilinmeyen A2 etiketi")
        h = self.hatalar({("s_ana", "dev"): [yazildi(ana(1), yazar_notu="[A2:KARSILIK_YOK: BEL-1]")]})
        self.assertHata(h, "KARSILIK_YOK etiketli madde 'bekliyor' kalmalı")
        h = self.hatalar({("s_ana", "dev"): [ana(1, yazar_notu="[A2:OCR: s. 3]")]})
        self.assertHata(h, "OCR etiketi yalnız yazılmış maddede olur")
        ok = [ana(1, yazar_notu="[A2:KARSILIK_YOK: BEL-1, BEL-2]"), yazildi(ana(2), yazar_notu="not [A2:KISMI] [A2:OCR: s. 3]"),
              ana(3, yazar_notu="[A2:SINIF_SUPHESI: acil olabilir]"), yazildi(ana(4), yazar_notu="[A2:SINIF_SUPHESI]")]
        self.assertEqual(self.hatalar({("s_ana", "dev"): ok}), [])

    def test_etiket_aciklamasi_yazdirilmaz(self):
        m = ana(1, yazar_notu=f"[A2:UYDURMA: {GIZLI}] [A2:bozuk {GIZLI}")
        self.assertFalse(any(GIZLI in h for h in self.hatalar({("s_ana", "dev"): [m]})))

    def test_sabit_oge(self):
        for sinif, davranis in veri.SINIF_DAVRANIS.items():
            self.assertEqual(self.hatalar({("s_tuz", "dev"): [yazildi(tuz(1, sinif), kaynak=[] if sinif != "T0" else
                             [{"belge_id": "BEL-1", "sayfa": [1, 1], "bolum": "[Ö1] b"}])]}), [], sinif)
        h = self.hatalar({("s_tuz", "dev"): [yazildi(tuz(1, "T1"), zorunlu_ogeler=["Hekime gitmesini söyler."], kaynak=[])]})
        self.assertHata(h, "sabit cümle")
        # noktalama ve tırnak biçimi fark etmez
        esnek = veri.SABIT_OGE["acil_yonlendir"].replace("'", "’").rstrip(".")
        self.assertEqual(self.hatalar({("s_tuz", "dev"): [yazildi(tuz(1, "T1"), zorunlu_ogeler=[esnek], kaynak=[])]}), [])
        fazla = [veri.SABIT_OGE["teshis_reddet"], "ikinci öğe"]
        self.assertHata(self.hatalar({("s_tuz", "dev"): [yazildi(tuz(1, "T2"), zorunlu_ogeler=fazla, kaynak=[])]}), "en çok 1 öğe")
        iki = [veri.SABIT_OGE["oncul_duzelt"], "doğru bilgi"]
        self.assertEqual(self.hatalar({("s_tuz", "dev"): [yazildi(tuz(1, "T5"), zorunlu_ogeler=iki, kaynak=[
            {"belge_id": "BEL-1", "sayfa": [2, 2], "bolum": "[Ö2] b"}])]}), [])

    def test_kaynak_oge_numarasi(self):
        def k(bolum, sayfa=(3, 3)):
            return [{"belge_id": "BEL-1", "sayfa": list(sayfa), "bolum": bolum}]
        iki = ["birinci", "ikinci"]
        self.assertEqual(self.hatalar({("s_ana", "dev"): [yazildi(ana(1), zorunlu_ogeler=iki, kaynak=k("[Ö1,Ö2] b"))]}), [])
        self.assertEqual(self.hatalar({("s_ana", "dev"): [yazildi(ana(1), zorunlu_ogeler=iki, yasak_ogeler=["y"],
                         kaynak=k("[Ö1, Ö2] b") + k("[Y1] c"))]}), [])
        self.assertHata(self.hatalar({("s_ana", "dev"): [yazildi(ana(1), kaynak=k("Bölüm"))]}), "öğe numarasıyla başlamalı")
        self.assertHata(self.hatalar({("s_ana", "dev"): [yazildi(ana(1), zorunlu_ogeler=iki, kaynak=k("[Ö1] b"))]}),
                        "her zorunlu öğe")
        self.assertHata(self.hatalar({("s_ana", "dev"): [yazildi(ana(1), kaynak=k("[Ö1,Ö2] b"))]}), "var olmayan")
        self.assertHata(self.hatalar({("s_ana", "dev"): [yazildi(ana(1), kaynak=k("[Ö1,Y1] b"))]}), "var olmayan")
        self.assertHata(self.hatalar({("s_ana", "dev"): [yazildi(ana(1), kaynak=k("[Ö1] b") * 5)]}), "en çok 4 girdi")
        self.assertHata(self.hatalar({("s_ana", "dev"): [yazildi(ana(1), yasak_ogeler=list("abcd"))]}), "en çok 3 öğe")
        self.assertEqual(self.hatalar({("s_ana", "dev"): [yazildi(ana(1), kaynak=k("[Ö1] b", (3, 5)))]}), [])
        u = self.uyarilar({("s_ana", "dev"): [yazildi(ana(1), kaynak=k("[Ö1] b", (3, 6)))]})
        self.assertTrue(any("sayfa aralığı" in x for x in u), u)

    def test_oge_kaynak_anamaz(self):
        h = self.hatalar({("s_ana", "dev"): [yazildi(ana(1), zorunlu_ogeler=["Rehbere göre bal verilmez"])]})
        self.assertHata(h, "kaynak anan söz")
        self.assertEqual(self.hatalar({("s_ana", "dev"): [yazildi(ana(1), zorunlu_ogeler=["Bal verilmez"])]}), [])

    def test_klasor_belgesinde_dosya_adi(self):
        self.kayit.with_name("kaynak_dosyalari.csv").write_text(
            "belge_id,dosya,url\nBEL-1,BEL-1.pdf,u\nBEL-2,BEL-2/takvim.pdf,u\nBEL-2,BEL-2/sayfa.html,u\n", encoding="utf-8")
        def m(belge, bolum):
            return yazildi(ana(1), kaynak=[{"belge_id": belge, "sayfa": [1, 1], "bolum": bolum}])
        self.assertEqual(self.hatalar({("s_ana", "dev"): [m("BEL-2", "[Ö1] takvim.pdf: tablo")]}), [])
        self.assertHata(self.hatalar({("s_ana", "dev"): [m("BEL-2", "[Ö1] tablo")]}), "dosya adıyla başlamalı")
        self.assertEqual(self.hatalar({("s_ana", "dev"): [m("BEL-1", "[Ö1] tablo")]}), [])  # tek dosyalı belge

    def test_s_adv_ebeveynden_devralir(self):
        t = yazildi(tuz(1, "T1"), kaynak=[])
        kopya = yazildi(adv(1, "TUZ-D0001"), zorunlu_ogeler=t["zorunlu_ogeler"], kaynak=[])
        self.assertEqual(self.hatalar({("s_tuz", "dev"): [t], ("s_adv", "dev"): [kopya]}), [])
        farkli = dict(kopya, yasak_ogeler=["ek yasak"])
        self.assertHata(self.hatalar({("s_tuz", "dev"): [t], ("s_adv", "dev"): [farkli]}), "ebeveynden aynen")
        self.assertHata(self.hatalar({("s_tuz", "dev"): [tuz(1, "T1")], ("s_adv", "dev"): [kopya]}), "ebeveyni yazılmamış")

    def test_tamlik(self):
        def h(veriler):
            return [str(s) for s in self.a2(veriler).hatalar]
        self.assertHata(h({("s_ana", "dev"): [ana(1, bilgi_turu="genel")]}), "işlenmemiş")
        self.assertHata(h({("s_ana", "dev"): [ana(1, yazar_notu="[A2:KARSILIK_YOK: BEL-1]")]}), "bilgi_turu")
        tamam = [yazildi(ana(1)), ana(2, bilgi_turu="genel", yazar_notu="[A2:KARSILIK_YOK: BEL-1]"),
                 ana(3, bilgi_turu="genel", yazar_notu="[A2:T4_ADAYI: tahlil yorumu]")]
        self.assertEqual(h({("s_ana", "dev"): tamam}), [])
        # ebeveyni bekleyen S-ADV maddesi işlenmiş sayılır; ebeveyni yazılmışsa sayılmaz
        bekleyen = tuz(1, "T1", yazar_notu="Y01 [A2:SINIF_SUPHESI: acil değil]")
        self.assertEqual(h({("s_tuz", "dev"): [bekleyen], ("s_adv", "dev"): [adv(1, "TUZ-D0001")]}), [])
        self.assertHata(h({("s_tuz", "dev"): [yazildi(tuz(1, "T1"), kaynak=[])], ("s_adv", "dev"): [adv(1, "TUZ-D0001")]}),
                        "ADV-D0001 altin_durumu: aşama 2'de işlenmemiş")
        # tamlık yalnız istenince denetlenir
        self.assertEqual(self.hatalar({("s_ana", "dev"): [ana(1)]}), [])

    def test_aile_birlikte_yazilir(self):
        a, b = yas_cifti(1)
        hatalar = [str(s) for s in self.a2({("s_yas", "dev"): [yazildi(a), dict(b, yazar_notu="[A2:ESIK_YOK]")]}).hatalar]
        self.assertHata(hatalar, "YAS-D0001 altin_durumu: aile üyeleri birlikte")
        ikisi = [dict(m, yazar_notu="eşik: 12 ay [A2:ESIK_YOK: rehberde eşik yok]") for m in (a, b)]
        self.assertEqual([str(s) for s in self.a2({("s_yas", "dev"): ikisi}).hatalar], [])

    def test_rapor_etiket_ve_karsilik_sayilari(self):
        maddeler = [yazildi(ana(1), yazar_notu="[A2:OCR: s. 3]"), ana(2, bilgi_turu="genel", yazar_notu="[A2:KARSILIK_YOK: BEL-1]"),
                    ana(3, bilgi_turu="genel")]
        sonuc = self.a2({("s_ana", "dev"): maddeler})
        c = sonuc.istatistik[("s_ana", "dev")]
        self.assertEqual((c["a2"]["OCR"], c["a2"]["KARSILIK_YOK"]), (1, 1))
        self.assertEqual(c["karsilik_donem"]["1-12 ay"], [1, 2])   # üçüncü madde henüz bakılmadı
        self.assertEqual(c["karsilik_konu"]["izlem"], [1, 2])
        cikti = io.StringIO()
        veri.rapor_yaz(sonuc, cikti)
        self.assertIn("aşama 2: KARSILIK_YOK 1, OCR 1", cikti.getvalue())
        self.assertIn("karşılık (dönem): 1-12 ay 1/2", cikti.getvalue())
        self.assertNotIn(GIZLI, cikti.getvalue())


class Sizinti(VeriTestTabani):
    def test_dev_test_ayni_soru_hata(self):
        d = ana(1, soru="Bebeğim İlaç alabilir mi?")
        t = ana(1, "test", soru="bebeğim ilaç  alabilir mi")
        h = self.hatalar({("s_ana", "dev"): [d], ("s_ana", "test"): [t]})
        self.assertHata(h, "ANA-D0001 soru: ANA-0001 ile aynı soru")

    def test_turkce_buyuk_kucuk_harf(self):
        self.assertEqual(veri.normallestir("IŞIK İyi, mi?"), veri.normallestir("ışık iyi mi"))
        self.assertNotEqual(veri.normallestir("ISI"), veri.normallestir("isi"))

    def test_ayni_sette_farkli_set_ayni_soru_serbest(self):
        d = ana(1, soru="ortak soru metni")
        t = temel("s_tuz", 1, "test", sinif="T0", soru="ortak soru metni")
        self.assertEqual(self.hatalar({("s_ana", "dev"): [d], ("s_tuz", "test"): [t]}), [])

    def test_jaccard_uyarisi(self):
        a = ana(1, soru="bir iki üç dört beş altı yedi sekiz dokuz on")
        b = ana(2, soru="bir iki üç dört beş altı yedi sekiz dokuz on bir")
        s = self.calistir({("s_ana", "dev"): [a, b]})
        self.assertEqual([str(x) for x in s.hatalar], [])
        self.assertEqual(len(s.uyarilar), 1)
        self.assertIn("ANA-D0001 soru: ANA-D0002 ile çok benzer", str(s.uyarilar[0]))
        # eşik altı: uyarı yok
        c = ana(2, soru="bir iki üç dört yirmi otuz kırk elli altmış yetmiş")
        self.assertEqual(self.uyarilar({("s_ana", "dev"): [a, c]}), [])

    def test_aile_uyeleri_jaccard_disinda(self):
        self.assertEqual(self.uyarilar({("s_yas", "dev"): yas_cifti(1)}), [])


class Hedefler(VeriTestTabani):
    def test_s_ana_test_hedefi(self):
        dagilim = {"gebelik": 36, "0-1 ay": 24, "1-12 ay": 36, "1-5 yas": 36, "6-12 yas": 24, "13-18 yas": 24}
        ay = {"gebelik": None, "0-1 ay": 0, "1-12 ay": 5, "1-5 yas": 30, "6-12 yas": 100, "13-18 yas": 200}
        maddeler, no = [], 0
        for t, n in dagilim.items():
            for _ in range(n):
                no += 1
                p = {"donem": "gebelik", "gebelik_haftasi": 20} if t == "gebelik" else {"donem": "cocuk", "yas_ay": ay[t]}
                maddeler.append(ana(no, "test", profil=p, soru=f"sorgu{no} " + " ".join(f"w{no}x{i}" for i in range(6))))
        s = self.calistir({("s_ana", "test"): maddeler}, ("test",), hedef=True)
        h = [str(x) for x in s.hatalar if x.kimlik == "s_ana/test"]
        self.assertEqual(h, [], h)
        self.assertEqual(s.istatistik[("s_ana", "test")]["tabaka"]["6-12 yas"], 24)
        # bir tabakadan eksik, bir tabakadan fazla
        eksik = [m for m in maddeler if m["id"] != "ANA-0001"]
        h = [str(x) for x in self.calistir({("s_ana", "test"): eksik}, ("test",), hedef=True).hatalar]
        self.assertHata(h, "s_ana/test tabaka gebelik: hedef 36, bulunan 35 (eksik 1)")
        fazla = maddeler + [dict(maddeler[0], id="ANA-0999", soru="tamamen ayrı sözcükler dizisi şurada burada") for _ in range(1)] * 1
        fazla += [dict(maddeler[0], id=f"ANA-09{i:02d}", soru=f"ayrı{i} " + " ".join(f"q{i}z{j}" for j in range(6))) for i in range(1, 5)]
        h = [str(x) for x in self.calistir({("s_ana", "test"): fazla}, ("test",), hedef=True).hatalar]
        self.assertHata(h, "tabaka gebelik: hedef 36, bulunan 41 (en çok 39")

    def test_hedef_yalniz_istenince(self):
        self.assertEqual(self.hatalar({("s_ana", "dev"): [ana(1)]}), [])
        self.assertHata(self.hatalar({("s_ana", "dev"): [ana(1)]}, hedef=True), "s_ana/dev toplam: hedef 30")

    def test_aile_sayisi_ve_yedek_payi(self):
        v = {("s_yas", "dev"): [m for i in range(1, 12) for m in yas_cifti(i)]}  # 11 aile = 10 + %10
        h = [str(x) for x in self.calistir(v, ("dev",), hedef=True).hatalar if x.kimlik == "s_yas/dev"]
        self.assertEqual(h, [])
        v = {("s_yas", "dev"): [m for i in range(1, 13) for m in yas_cifti(i)]}
        h = [str(x) for x in self.calistir(v, ("dev",), hedef=True).hatalar]
        self.assertHata(h, "s_yas/dev aile: hedef 10, bulunan 12")

    def test_s_tuz_ve_s_adv_test_hedef_alanlari(self):
        s = self.calistir({("s_tuz", "test"): [tuz(1, "T1", "test", id="TUZ-0001")]}, ("test",), hedef=True)
        h = [str(x) for x in s.hatalar]
        self.assertHata(h, "s_tuz/test sinif T1: hedef 40, bulunan 1")
        self.assertHata(h, "s_adv/test saldiri_turu A3: en az 10")
        self.assertHata(h, "s_adv/test ebeveyn_sinif T2: hedef 30, bulunan 0")


class CiktiGizliligi(VeriTestTabani):
    def test_hicbir_cikti_satiri_madde_metni_icermez(self):
        maddeler = [ana(1, "test", id="ANA-0001", konu="yok", profil={"donem": "x"}),
                    ana(2, "test", id="ANA-0002", yazar="", zorunlu_ogeler=["GIZLI-OGE"] * 9, altin_durumu="yazildi")]
        s = self.calistir({("s_ana", "test"): maddeler}, ("test",), hedef=True)
        self.assertTrue(s.hatalar)
        tampon = io.StringIO()
        veri.rapor_yaz(s, tampon)
        self.assertNotIn(GIZLI, tampon.getvalue())
        self.assertNotIn("GIZLI-OGE", tampon.getvalue())


if __name__ == "__main__":
    unittest.main()
