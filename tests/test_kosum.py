"""eval.runner.kosum testleri: korumalar, sahte uçtan uca koşum, devam. Geçici depo kullanır."""
import contextlib
import io
import json
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from eval.runner import __main__ as cli  # noqa: E402
from eval.runner import kosum, veri  # noqa: E402
from eval.runner.uretici import SahteUretici, Yanit  # noqa: E402
from test_veri import KAYIT_CSV, GIZLI, ana, tuz, yaz_veri  # noqa: E402

KONFIG = """name: {ad}
retrieval:
  enabled: {getirme}
safety:
  enabled: false
generator:
  provider: cloud
  api: anthropic
  model: {model}
  effort: medium
  {mot}
  system_prompt_file: configs/prompts/base_tr.md
eval:
  datasets: [s_ana, s_tuz]
  split: dev
  repeats: 2
"""

def hedefler(**ozel):
    # Küçük sahte hedefler: her (set, bolme) için 0; ozel={"s_ana/test": 2} ile değiştirilir.
    h = {(s, b): ({"aile": 0} if s == "s_yas" else {"toplam": 0}) for s in veri.SETLER for b in veri.BOLMELER}
    for ad, n in ozel.items():
        s, b = ad.split("/")
        h[(s, b)] = {"aile": n} if s == "s_yas" else {"toplam": n}
    return h


TEMIZ = {"commit": "abc123", "etiket": None, "kirli": False}


class KosumTabani(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.depo = pathlib.Path(t.name)
        (self.depo / "configs" / "prompts").mkdir(parents=True)
        (self.depo / "configs" / "prompts" / "base_tr.md").write_text("Sistem istemi", encoding="utf-8")
        (self.depo / "kb" / "registry").mkdir(parents=True)
        (self.depo / "kb" / "registry" / "belge_kayit_defteri.csv").write_text(KAYIT_CSV, encoding="utf-8")
        (self.depo / "eval" / "results").mkdir(parents=True)
        self.kok = self.depo / "eval" / "datasets"
        self.cikti = []

    def konfig(self, ad="K0_test", model="claude-haiku-5-5", getirme="false", mot="max_output_tokens: 100"):
        yol = self.depo / "configs" / f"{ad}.yaml"
        yol.write_text(KONFIG.format(ad=ad, model=model, getirme=getirme, mot=mot), encoding="utf-8")
        return yol

    def veri_yaz(self, bolme="dev"):
        yaz_veri(self.kok, "s_ana", bolme, [ana(1, bolme, id="ANA-D0001" if bolme == "dev" else "ANA-0001"),
                                             ana(2, bolme, id="ANA-D0002" if bolme == "dev" else "ANA-0002",
                                                 soru="bambaşka sözcüklerle ikinci soru burada")])
        yaz_veri(self.kok, "s_tuz", bolme, [tuz(1, "T1", bolme)])

    def kos(self, konfigler, git=TEMIZ, **kw):
        kw.setdefault("uretici", "sahte")
        return kosum.kos(konfigler, depo=self.depo, git_fn=lambda d: git, yaz=self.cikti.append, **kw)


class Korumalar(KosumTabani):
    def test_yer_tutucu_model(self):
        with self.assertRaisesRegex(kosum.KosumHatasi, "yer tutucu"):
            self.kos([self.konfig(model="<belirlenecek>")])

    def test_max_output_tokens_eksik(self):
        with self.assertRaisesRegex(kosum.KosumHatasi, "max_output_tokens"):
            self.kos([self.konfig(mot="")])

    def test_getirme_henuz_yok(self):
        with self.assertRaisesRegex(kosum.KosumHatasi, "henüz yok"):
            self.kos([self.konfig(getirme="true")])

    def test_test_bolmesi_nihai_olmadan_reddedilir(self):
        # Veri dosyası hiç yok: koruma veriye dokunmadan önce devreye girer.
        with self.assertRaisesRegex(kosum.KosumHatasi, "--nihai"):
            self.kos([self.konfig()], bolme="test")

    def test_test_bolmesi_kirli_agac_ve_etiketsiz(self):
        k = self.konfig()
        with self.assertRaisesRegex(kosum.KosumHatasi, "temiz değil"):
            self.kos([k], bolme="test", nihai=True, git={"commit": "a", "etiket": "degerlendirme-v1.0", "kirli": True})
        with self.assertRaisesRegex(kosum.KosumHatasi, "etiketi yok"):
            self.kos([k], bolme="test", nihai=True, git={"commit": "a", "etiket": "baska", "kirli": False})
        with self.assertRaisesRegex(kosum.KosumHatasi, "okunamadı"):
            self.kos([k], bolme="test", nihai=True, git={"commit": None, "etiket": None, "kirli": None})

    def test_test_bolmesi_tum_korumalarla_calisir(self):
        self.veri_yaz("test")
        git = {"commit": "a", "etiket": "degerlendirme-v1.0", "kirli": False}
        with mock.patch.dict(veri.HEDEF, hedefler(**{"s_ana/test": 2, "s_tuz/test": 1}), clear=True):
            self.kos([self.konfig()], bolme="test", nihai=True, git=git)
        self.assertTrue(list((self.depo / "eval" / "results").glob("*_test.sha256")))
        dizin, = (self.depo / "eval" / "results" / "raw").iterdir()
        m = json.loads((dizin / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(set(m["veri_dosyalari"]), {"eval/datasets/s_ana/test.jsonl", "eval/datasets/s_tuz/test.jsonl"})

    def test_nihai_hedefler_denetlenir(self):
        self.veri_yaz("test")
        git = {"commit": "a", "etiket": "degerlendirme-v1.0", "kirli": False}
        with contextlib.redirect_stdout(io.StringIO()) as o, self.assertRaisesRegex(kosum.KosumHatasi, "doğrulama hatası"):
            self.kos([self.konfig()], bolme="test", nihai=True, git=git)  # gerçek hedefler: eksik
        self.assertIn("s_ana/test toplam: hedef 180", o.getvalue())

    def test_nihai_dev_test_sizintisi(self):
        self.veri_yaz("test")
        yaz_veri(self.kok, "s_ana", "dev", [ana(1, "dev", soru=ana(1, "test")["soru"])])
        git = {"commit": "a", "etiket": "degerlendirme-v1.0", "kirli": False}
        with mock.patch.dict(veri.HEDEF, hedefler(**{"s_ana/test": 2, "s_tuz/test": 1, "s_ana/dev": 1}), clear=True), \
                contextlib.redirect_stdout(io.StringIO()) as o, \
                self.assertRaisesRegex(kosum.KosumHatasi, "doğrulama hatası"):
            self.kos([self.konfig()], bolme="test", nihai=True, git=git)
        self.assertIn("dev/test sızıntısı", o.getvalue())
        self.assertNotIn(GIZLI, o.getvalue())

    def test_dev_kosumu_test_dosyalarini_okumaz(self):
        self.veri_yaz("dev")
        (self.kok / "s_ana" / "test.jsonl").write_text("bozuk {{{ \n", encoding="utf-8")
        self.kos([self.konfig()], sinir=1)  # test.jsonl okunsaydı json hatası çıkardı

    def test_dev_dosyasi_yoksa_acik_hata(self):
        with self.assertRaisesRegex(kosum.KosumHatasi, "madde bulunamadı"):
            self.kos([self.konfig()])

    def test_dogrulama_hatasi_kosumu_durdurur(self):
        yaz_veri(self.kok, "s_ana", "dev", [ana(1, konu="yok")])
        with contextlib.redirect_stdout(io.StringIO()) as o, self.assertRaisesRegex(kosum.KosumHatasi, "doğrulama hatası"):
            self.kos([self.konfig()])
        self.assertIn("ANA-D0001 konu", o.getvalue())
        self.assertFalse((self.depo / "eval" / "results" / "raw").exists())

    def test_gecersiz_effort_ve_sinir(self):
        k = self.konfig()
        k.write_text(k.read_text(encoding="utf-8").replace("effort: medium", "effort: orta"), encoding="utf-8")
        with self.assertRaisesRegex(kosum.KosumHatasi, "effort"):
            self.kos([k])
        for n in (0, -1):
            with self.assertRaisesRegex(kosum.KosumHatasi, "--sinir"):
                self.kos([self.konfig()], sinir=n)
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(cli.main(["kos", "--konfig", str(k), "--sinir", "0", "--depo", str(self.depo)]), 1)

    def test_uretici_kurulamazsa_klasor_birakmaz(self):
        self.veri_yaz()

        def fabrika(tur, g):
            raise RuntimeError("ANTHROPIC_API_KEY bulunamadı")
        with self.assertRaisesRegex(RuntimeError, "ANTHROPIC_API_KEY"):
            self.kos([self.konfig("A"), self.konfig("B")], uretici_fabrikasi=fabrika)
        self.assertFalse((self.depo / "eval" / "results" / "raw").exists())

    def test_cli_hatalari_cikis_kodu_1(self):
        k = self.konfig(model="<x>")
        with contextlib.redirect_stderr(io.StringIO()) as e:
            rc = cli.main(["kos", "--konfig", str(k), "--uretici", "sahte", "--depo", str(self.depo)])
        self.assertEqual(rc, 1)
        self.assertIn("HATA", e.getvalue())

    def test_cli_dogrula_cikis_kodlari(self):
        self.veri_yaz()
        kayit = str(self.depo / "kb" / "registry" / "belge_kayit_defteri.csv")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(["dogrula", "--bolme", "dev", "--kok", str(self.kok), "--kayit", kayit]), 0)
            self.assertEqual(cli.main(["dogrula", "--bolme", "dev", "--hedef", "--kok", str(self.kok), "--kayit", kayit]), 1)


class UctanUca(KosumTabani):
    def calistir(self, **kw):
        self.veri_yaz()
        konfig = self.konfig()
        self.kos([konfig], **kw)
        dizin, = (self.depo / "eval" / "results" / "raw").iterdir()
        return konfig, dizin

    def test_sahte_kosum(self):
        _, dizin = self.calistir()
        self.assertTrue(dizin.name.endswith("_K0_test_dev"))
        satirlar = [json.loads(s) for s in (dizin / "yanitlar.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(len(satirlar), 3 * 2)  # 3 madde x 2 tekrar
        self.assertEqual([(s["madde_id"], s["tekrar"]) for s in satirlar][:4],
                         [("ANA-D0001", 1), ("ANA-D0001", 2), ("ANA-D0002", 1), ("ANA-D0002", 2)])
        self.assertEqual(satirlar[0]["getirilen"], [])
        self.assertEqual(set(satirlar[0]) - {"madde_id", "tekrar", "getirilen"},
                         {"metin", "durma_nedeni", "model", "girdi_token", "cikti_token",
                          "gecikme_sn", "istek_kimligi", "hata"})
        m = json.loads((dizin / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(m["kosum_kimligi"], dizin.name)
        self.assertEqual((m["konfig_adi"], m["bolme"], m["git_commit"], m["git_etiketi"], m["git_kirli"]),
                         ("K0_test", "dev", "abc123", None, False))
        self.assertEqual(len(m["konfig_sha256"]), 64)
        self.assertEqual(len(m["sistem_istemi_sha256"]), 64)
        self.assertEqual(set(m["veri_dosyalari"]), {"eval/datasets/s_ana/dev.jsonl", "eval/datasets/s_tuz/dev.jsonl"})
        self.assertEqual(m["kb_hashleri"], {"BEL-1": None, "BEL-2": None})
        self.assertEqual(m["uretici"]["effort"], "medium")
        self.assertEqual(m["uretici"]["max_output_tokens"], 100)
        self.assertEqual(set(m["ortam"]), {"python", "anthropic_sdk"})
        self.assertRegex(m["ortam"]["python"], r"^\d+\.\d+")
        self.assertEqual(m["donen_modeller"], ["sahte"])
        self.assertEqual(m["sayilar"], {"yanit": 6, "hata": 0, "ret": 0, "kesilme": 0})
        self.assertTrue(m["tamamlandi"] and m["baslangic"] and m["bitis"])
        self.assertIsNone(m["sinir"])
        sha = (self.depo / "eval" / "results" / f"{dizin.name}.sha256").read_text(encoding="utf-8").splitlines()
        self.assertEqual([s.split("  ")[1] for s in sha], ["manifest.json", "yanitlar.jsonl"])
        self.assertEqual(sha[1].split("  ")[0], kosum.sha256_dosya(dizin / "yanitlar.jsonl"))

    def test_konsol_madde_metni_icermez(self):
        self.calistir()
        metin = "\n".join(self.cikti)
        self.assertNotIn(GIZLI, metin)
        self.assertNotIn("bambaşka", metin)
        self.assertIn("[1/3] ANA-D0001", metin)

    def test_sinir_ve_setler(self):
        self.veri_yaz()
        self.kos([self.konfig()], sinir=1)
        dizin, = (self.depo / "eval" / "results" / "raw").iterdir()
        m = json.loads((dizin / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual((m["sinir"], m["sayilar"]["yanit"]), (1, 2))

    def test_setler_filtresi(self):
        self.veri_yaz()
        self.kos([self.konfig()], setler=["s_tuz"])
        dizin, = (self.depo / "eval" / "results" / "raw").iterdir()
        ids = {json.loads(s)["madde_id"] for s in (dizin / "yanitlar.jsonl").read_text(encoding="utf-8").splitlines()}
        self.assertEqual(ids, {"TUZ-D0001"})

    def test_madde_dis_dongu_konfig_ic_dongu_tekrar_en_ic(self):
        self.veri_yaz()
        a, b = self.konfig("K0_a"), self.konfig("K0_b")  # repeats: 2
        sira = []
        sayac = []

        def fabrika(tur, g):
            ad = f"u{len(sayac)}"
            sayac.append(1)

            class Casus(SahteUretici):
                def uret(self, sistem, kullanici):
                    sira.append((kullanici, ad))
                    return super().uret(sistem, kullanici)
            return Casus()
        self.kos([a, b], sinir=2, uretici_fabrikasi=fabrika)
        m1, m2 = dict.fromkeys(k for k, _ in sira)
        beklenen = [(m, u) for m in (m1, m2) for u in ("u0", "u1") for _ in range(2)]
        self.assertEqual(sira, beklenen)

    def test_devam_tamamlananlari_atlar_hatalilari_yeniden_dener(self):
        self.veri_yaz()
        konfig = self.konfig()

        class Aksak:
            def __init__(self):
                self.cagri = 0

            def uret(self, sistem, kullanici):
                self.cagri += 1
                if self.cagri == 3:
                    raise KeyboardInterrupt  # koşum yarıda kesilir
                if self.cagri == 2:
                    return Yanit("", None, None, None, None, 0.1, None, "APIConnectionError: x")
                return SahteUretici().uret(sistem, kullanici)

        with self.assertRaises(KeyboardInterrupt):
            kosum.kos([konfig], uretici="sahte", depo=self.depo, git_fn=lambda d: TEMIZ,
                      yaz=self.cikti.append, uretici_fabrikasi=lambda t, g: Aksak())
        dizin, = (self.depo / "eval" / "results" / "raw").iterdir()
        m = json.loads((dizin / "manifest.json").read_text(encoding="utf-8"))
        self.assertFalse(m["tamamlandi"])
        self.assertFalse((self.depo / "eval" / "results" / f"{dizin.name}.sha256").exists())
        self.assertEqual(len((dizin / "yanitlar.jsonl").read_text(encoding="utf-8").splitlines()), 2)

        sayac = []

        class Sayan(SahteUretici):
            def uret(self, sistem, kullanici):
                sayac.append(1)
                return super().uret(sistem, kullanici)

        kosum.kos([konfig], uretici="sahte", depo=self.depo, git_fn=lambda d: TEMIZ, yaz=self.cikti.append,
                  cikti=str(dizin), uretici_fabrikasi=lambda t, g: Sayan())
        self.assertEqual(len(sayac), 6 - 1)  # yalnız (D0001,1) tamam; hatalı olan yeniden denendi
        m = json.loads((dizin / "manifest.json").read_text(encoding="utf-8"))
        self.assertTrue(m["tamamlandi"])
        self.assertEqual(m["devam_sayisi"], 1)
        self.assertEqual(m["sayilar"], {"yanit": 6, "hata": 0, "ret": 0, "kesilme": 0})
        self.assertTrue((self.depo / "eval" / "results" / f"{dizin.name}.sha256").exists())
        self.assertEqual(self.satirlar(dizin), 6)  # hatalı satır dosyada kalmadı

    def satirlar(self, dizin):
        # Satır satır katı okuma: her satır geçerli JSON, (madde, tekrar) çiftleri tekil.
        d = [json.loads(s) for s in (dizin / "yanitlar.jsonl").read_text(encoding="utf-8").split("\n") if s]
        anahtarlar = [(x["madde_id"], x["tekrar"]) for x in d]
        self.assertEqual(len(anahtarlar), len(set(anahtarlar)))
        return len(d)

    def test_devam_yarim_satiri_atar(self):
        konfig, dizin = self.calistir()
        yol = dizin / "yanitlar.jsonl"
        satirlar = yol.read_text(encoding="utf-8").splitlines()
        yol.write_text("\n".join(satirlar[:3]) + '\n{"madde_id": "ANA-D00', encoding="utf-8")
        self.kos([konfig], cikti=str(dizin))
        self.assertEqual(self.satirlar(dizin), 6)

    def test_devam_manifest_yoksa_reddedilir(self):
        konfig, dizin = self.calistir()
        (dizin / "manifest.json").unlink()
        with self.assertRaisesRegex(kosum.KosumHatasi, "manifest.json yok"):
            self.kos([konfig], cikti=str(dizin))

    def test_devam_ilk_kosumla_farkli_olamaz(self):
        konfig, dizin = self.calistir()
        kb = self.depo / "kb" / "registry" / "belge_kayit_defteri.csv"
        for ad, kw in [("uretici", {"uretici": "anthropic", "uretici_fabrikasi": lambda t, g: SahteUretici()}), ("sinir", {"sinir": 2}), ("setler", {"setler": ["s_tuz"]}),
                       ("git_commit", {"git": {"commit": "zzz", "etiket": None, "kirli": False}})]:
            with self.subTest(ad), self.assertRaisesRegex(kosum.KosumHatasi, f"'{ad}'"):
                self.kos([konfig], cikti=str(dizin), **kw)
        kb.write_text(KAYIT_CSV.replace("BEL-1,Bir,", "BEL-1,Bir,abc"), encoding="utf-8")
        with self.assertRaisesRegex(kosum.KosumHatasi, "'kb_hashleri'"):
            self.kos([konfig], cikti=str(dizin))

    def test_devam_degisen_konfigi_reddeder(self):
        konfig, dizin = self.calistir()
        konfig.write_text(konfig.read_text(encoding="utf-8").replace("effort: medium", "effort: high"), encoding="utf-8")
        with self.assertRaisesRegex(kosum.KosumHatasi, "devam edilemez"):
            self.kos([konfig], cikti=str(dizin))

    def test_cikti_birden_cok_konfigle_reddedilir(self):
        self.veri_yaz()
        with self.assertRaisesRegex(kosum.KosumHatasi, "tek konfigürasyon"):
            self.kos([self.konfig("A"), self.konfig("B")], cikti=str(self.depo))


if __name__ == "__main__":
    unittest.main()
