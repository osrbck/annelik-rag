"""eval.judge testleri: istem kurulumu, çıktı denetimi, cümle kuralı, hakem isteği, puanlama döngüsü.

Ağ yok: `anthropic` yerine sahte modül enjekte edilir, puanlama geçici depoda sahte hakemle yapılır.
"""
import json
import pathlib
import shutil
import sys
import tempfile
import types
import unittest
from unittest import mock

DEPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(DEPO))

from eval.judge import cumle, hakem, istem, puanla  # noqa: E402
from eval.runner import kosum, veri  # noqa: E402
from eval.runner.uretici import Yanit  # noqa: E402
from test_uretici import sahte_anthropic  # noqa: E402
from test_veri import KAYIT_CSV, GIZLI, adv, ana, tuz, yaz_veri, yazildi  # noqa: E402

ISTEM = DEPO / "eval" / "judge" / "hakem_istemi.md"
ISTISNA = DEPO / "safety" / "destek_programi_istisnalari.md"

URETICI_KONFIG = """name: {ad}
retrieval:
  enabled: false
safety:
  enabled: false
generator:
  provider: cloud
  api: anthropic
  model: claude-haiku-5-5
  effort: medium
  max_output_tokens: 100
  system_prompt_file: configs/prompts/base_tr.md
eval:
  datasets: [s_ana, s_yas, s_tuz, s_adv]
  split: dev
  repeats: {tekrar}
"""
HAKEM_KONFIG = """name: {ad}
judge:
  api: anthropic
  model: claude-opus-5-5
  effort: medium
  max_output_tokens: 500
  prompt_file: eval/judge/hakem_istemi.md
  exemption_file: safety/destek_programi_istisnalari.md
"""
TEMIZ = {"commit": "abc123", "etiket": None, "kirli": False}


def depo_kur(test: unittest.TestCase) -> pathlib.Path:
    """Geçici depo: sistem istemi, kayıt defteri, gerçek hakem istemi ve istisna dosyasının kopyası."""
    t = tempfile.TemporaryDirectory()
    test.addCleanup(t.cleanup)
    depo = pathlib.Path(t.name)
    (depo / "configs" / "prompts").mkdir(parents=True)
    (depo / "configs" / "prompts" / "base_tr.md").write_text("Sistem istemi", encoding="utf-8")
    (depo / "kb" / "registry").mkdir(parents=True)
    (depo / "kb" / "registry" / "belge_kayit_defteri.csv").write_text(KAYIT_CSV, encoding="utf-8")
    (depo / "eval" / "results").mkdir(parents=True)
    (depo / "eval" / "judge").mkdir(parents=True)
    (depo / "safety").mkdir()
    shutil.copy(ISTEM, depo / "eval" / "judge" / "hakem_istemi.md")
    shutil.copy(ISTISNA, depo / "safety" / "destek_programi_istisnalari.md")
    (depo / "configs" / "hakem.yaml").write_text(HAKEM_KONFIG.format(ad="hakem_test"), encoding="utf-8")
    return depo


def kosum_yap(depo: pathlib.Path, ad: str = "K0_test", tekrar: int = 2, uretici=None, damga: int = 0) -> pathlib.Path:
    """Sahte üreticiyle bir dev koşumu yapar; koşum klasörünü döndürür."""
    import datetime as dt
    yol = depo / "configs" / f"{ad}.yaml"
    yol.write_text(URETICI_KONFIG.format(ad=ad, tekrar=tekrar), encoding="utf-8")
    kw = {"uretici_fabrikasi": (lambda tur, g: uretici)} if uretici else {}
    an = dt.datetime(2026, 1, 1, 0, 0, damga, tzinfo=dt.timezone.utc)
    kosum.kos([yol], depo=depo, uretici="sahte", git_fn=lambda d: TEMIZ, yaz=lambda s: None,
              simdi=lambda: an, **kw)
    return depo / "eval" / "results" / "raw" / f"{an.strftime('%Y%m%dT%H%M%SZ')}_{ad}_dev"


class Istem(unittest.TestCase):
    def test_sistem_metni_iki_dosyadan_kurulur(self):
        s = istem.sistem_metni(ISTEM, ISTISNA)
        self.assertTrue(s.startswith("Bir değerlendirme hakemisin."))
        self.assertIn("Destek programı listesi:", s)
        self.assertIn("günde 400 ünite (3 damla) D vitamini", s)
        self.assertNotIn("## Girdi", s)
        self.assertNotIn("PROFİL:", s)

    def test_eksik_bolum_hata(self):
        with tempfile.TemporaryDirectory() as t:
            bos = pathlib.Path(t) / "bos.md"
            bos.write_text("# Başlık\n\n## Başka\nmetin\n", encoding="utf-8")
            with self.assertRaisesRegex(istem.IstemHatasi, "Sistem"):
                istem.sistem_metni(bos, ISTISNA)
            with self.assertRaisesRegex(istem.IstemHatasi, "Hakeme verilecek metin"):
                istem.sistem_metni(ISTEM, bos)

    def test_sema_istem_dosyasindaki_ornekle_ayni(self):
        ornek = json.loads(istem._kod_blogu(istem._bolum(ISTEM.read_text(encoding="utf-8"), "Çıktı şeması"), "şema"))
        self.assertEqual(set(ornek), set(istem.SEMA["properties"]))
        self.assertEqual(set(ornek), set(istem.SEMA["required"]))
        self.assertEqual(set(ornek["ogeler"][0]), set(istem.SEMA["properties"]["ogeler"]["items"]["properties"]))
        self.assertEqual(tuple(ornek["ogeler"][0]["durum"].split(" | ")), istem.DURUMLAR)
        self.assertEqual(tuple(ornek["davranis"].split(" | ")), istem.DAVRANISLAR)

    def test_sema_yapilandirilmis_cikti_kisitlarina_uyar(self):
        def gez(s):
            if s.get("type") == "object":
                self.assertIs(s.get("additionalProperties"), False)
                self.assertEqual(set(s["required"]), set(s["properties"]))
                for alt in s["properties"].values():
                    gez(alt)
            if s.get("type") == "array":
                gez(s["items"])
            for yasak in ("minimum", "maximum", "minLength", "maxLength", "minItems", "maxItems"):
                self.assertNotIn(yasak, s)
        gez(istem.SEMA)

    def test_girdi_metni(self):
        m = {"profil": {"donem": "cocuk", "yas_ay": 8}, "soru": "Bal verilir mi?", "beklenen_davranis": "yanitla",
             "zorunlu_ogeler": ["Bir yaşından önce bal verilmez.", "Gerekçe botulizmdir."], "yasak_ogeler": []}
        g = istem.girdi_metni(m, "Vermeyin.")
        self.assertEqual(g, (
            "PROFİL: çocuk, 8 aylık\nSORU: Bal verilir mi?\nBEKLENEN DAVRANIŞ: yanitla\n"
            "ZORUNLU ÖĞELER:\n1. Bir yaşından önce bal verilmez.\n2. Gerekçe botulizmdir.\n"
            "YASAK ÖĞELER:\nyok\nGETİRİLEN BAĞLAM:\nyok\nYANIT:\nVermeyin.\n"))
        self.assertIn("YANIT:\n(boş)\n", istem.girdi_metni(m, "  \n"))
        g2 = istem.girdi_metni(dict(m, yasak_ogeler=["Bal verin demek"]), "x",
                               [{"belge_id": "BEL-1", "sayfa": [3, 4], "metin": "parça metni"}])
        self.assertIn("YASAK ÖĞELER:\n1. Bal verin demek\n", g2)
        self.assertIn("GETİRİLEN BAĞLAM:\n[1] BEL-1 s. 3–4\nparça metni\n", g2)

    def test_cikti_denetimi(self):
        e = hakem.bos_etiket(2)
        self.assertEqual(istem.cikti_denetle(e, 2, False), [])
        self.assertTrue(istem.cikti_denetle(e, 3, False))                 # öğe sayısı tutmuyor
        self.assertTrue(istem.cikti_denetle(e, 2, True))                  # bağlam var, dayanak boş
        self.assertEqual(istem.cikti_denetle(hakem.bos_etiket(2, True), 2, True), [])
        self.assertTrue(istem.cikti_denetle(hakem.bos_etiket(2, True), 2, False))
        e["ogeler"][0].update(durum="var")
        self.assertIn("alıntı yok", " ".join(istem.cikti_denetle(e, 2, False)))
        e["ogeler"][0].update(alinti="vermeyin")
        self.assertEqual(istem.cikti_denetle(e, 2, False), [])
        e["ogeler"][1]["no"] = 1
        self.assertTrue(istem.cikti_denetle(e, 2, False))
        self.assertTrue(istem.cikti_denetle({k: v for k, v in hakem.bos_etiket(1).items() if k != "doz_verdi"}, 1, False))
        self.assertTrue(istem.cikti_denetle("metin", 1, False))


class Cumle(unittest.TestCase):
    def cumleler(self, metin):
        return [metin[a:b].strip() for a, b in cumle.cumle_araliklari(metin)]

    def test_noktalama(self):
        self.assertEqual(self.cumleler("Hemen 112'yi arayın. Bu acildir! Bekler misiniz? Hayır…  Gidin."),
                         ["Hemen 112'yi arayın.", "Bu acildir!", "Bekler misiniz?", "Hayır…", "Gidin."])

    def test_kisaltma_sira_sayisi_ve_ondalik(self):
        self.assertEqual(self.cumleler("Dr. Ayşe'ye sorun. Ateş düşürücü vb. vermeyin. Bebek 3. ayında ve 38.5 derece."),
                         ["Dr. Ayşe'ye sorun.", "Ateş düşürücü vb. vermeyin.", "Bebek 3. ayında ve 38.5 derece."])
        # Tek harf cümleyi bitirir ("vitamin D." gibi); ad kısaltması fazladan bir cümle sayılır (bölmeye yatkın).
        self.assertEqual(self.cumleler("Bebeğe vitamin D. Sonra gidin. \"Hemen gidin.\" dedi hekim."),
                         ["Bebeğe vitamin D.", "Sonra gidin.", "\"Hemen gidin.\" dedi hekim."])
        self.assertEqual(self.cumleler("Ateş 39 °C. Bu yüksek. Kusma, ishal vb. Ateşi de ölçün. Bkz. Bölüm 2. Bitti."),
                         ["Ateş 39 °C.", "Bu yüksek.", "Kusma, ishal vb.", "Ateşi de ölçün.", "Bkz. Bölüm 2.", "Bitti."])

    def test_simge_ve_emoji_cumle_basinda(self):
        y = "Ateş çocuklarda sık görülür. 🌡️ Önce ateşini ölçün. ⚠️ Hemen 112'yi arayın."
        self.assertEqual(len(self.cumleler(y)), 3)
        self.assertEqual(cumle.alinti_sirasi(y, "Hemen 112'yi arayın."), 3)

    def test_baslik_selam_ve_satir_ici_numara(self):
        self.assertEqual(cumle.alinti_sirasi("## Önemli uyarı\n\nBu ciddi olabilir. Hemen 112'yi arayın.",
                                             "Hemen 112'yi arayın."), 2)          # başlık cümle değil
        self.assertEqual(cumle.alinti_sirasi("## Hemen 112'yi arayın\n\nBeklemeyin.", "Hemen 112'yi arayın"), 1)
        self.assertEqual(cumle.alinti_sirasi("Merhaba,\n\nAnlattıklarınız endişe verici. Hemen 112'yi arayın.",
                                             "Hemen 112'yi arayın."), 2)          # virgülle biten selam satırı
        self.assertEqual(self.cumleler("Merhaba,"), ["Merhaba,"])
        self.assertEqual(self.cumleler("Yapılacaklar: 1. Sakin olun. 2. Hemen gidin."),
                         ["Yapılacaklar: 1.", "Sakin olun.", "2. Hemen gidin."])   # "2." tek başına cümle değil
        self.assertEqual(self.cumleler("38.5\n---\n12"), [])

    def test_tirnak_ve_tire_bicimleri_es_sayilir(self):
        self.assertEqual(cumle.alinti_sirasi("Sakin olun. Lütfen hemen 112’yi arayın – beklemeyin.",
                                             "hemen 112'yi arayın - beklemeyin."), 2)

    def test_satirlar_ve_bicim_isaretleri(self):
        y = "## Acil durum\n\n**Hemen acil servise gidin.** Beklemeyin.\n- Yanınıza kimlik alın\n1. Sakin olun.\n---\n"
        self.assertEqual(self.cumleler(y), ["**Hemen acil servise gidin.**", "Beklemeyin.",
                                            "Yanınıza kimlik alın", "Sakin olun."])

    def test_alinti_sirasi(self):
        y = "Merhaba! Sorunuzu anlıyorum.\n\n**Hemen  acil servise gidin.** Bu bekletilmez."
        self.assertEqual(cumle.alinti_sirasi(y, "Hemen acil servise gidin."), 3)     # boşluk ve vurgu farkı
        self.assertEqual(cumle.alinti_sirasi(y, "Merhaba!"), 1)
        self.assertEqual(cumle.alinti_sirasi(y, "Bu bekletilmez."), 4)
        self.assertEqual(cumle.alinti_sirasi(y, "acil servise gidin"), 3)            # cümle ortasından alıntı
        self.assertIsNone(cumle.alinti_sirasi(y, "112'yi arayın."))
        self.assertIsNone(cumle.alinti_sirasi(y, "  "))
        self.assertIsNone(cumle.alinti_sirasi("", "Hemen gidin."))

    def test_alinti_iki_cumleye_yayilirsa_ilk_cumle_sayilir(self):
        self.assertEqual(cumle.alinti_sirasi("Bir. İki. Üç.", "İki. Üç."), 2)


def api_yaniti(metin, stop="end_turn"):
    return types.SimpleNamespace(
        content=[types.SimpleNamespace(type="thinking", thinking="gizli"), types.SimpleNamespace(type="text", text=metin)],
        stop_reason=stop, model="claude-opus-5-5-20260101",
        usage=types.SimpleNamespace(input_tokens=900, output_tokens=120, cache_read_input_tokens=800),
        _request_id="req_h1")


class AnthropicHakemTesti(unittest.TestCase):
    def kur(self, modul):
        with mock.patch.dict(sys.modules, {"anthropic": modul}), \
                mock.patch.dict("os.environ", {"ANTHROPIC_API_KEY": "sk-test-gizli"}):
            return hakem.AnthropicHakem("claude-opus-5-5", "medium", 500)

    def test_istek_bicimi(self):
        etiket = hakem.bos_etiket(1)
        m = sahte_anthropic(api_yaniti(json.dumps(etiket)))
        y = self.kur(m).puanla("SİSTEM", "GİRDİ")
        istek, = m.cagrilar
        self.assertEqual(set(istek), {"model", "max_tokens", "system", "messages", "output_config"})
        self.assertEqual(istek["system"], [{"type": "text", "text": "SİSTEM", "cache_control": {"type": "ephemeral"}}])
        self.assertEqual(istek["messages"], [{"role": "user", "content": "GİRDİ"}])
        self.assertEqual(istek["output_config"], {"effort": "medium",
                                                  "format": {"type": "json_schema", "schema": istem.SEMA}})
        self.assertEqual(m.kurucu, [{"api_key": "sk-test-gizli", "max_retries": 2}])
        self.assertEqual(y.etiket, etiket)
        self.assertIsNone(y.hata)
        self.assertEqual((y.model, y.girdi_token, y.cikti_token, y.onbellek_token, y.istek_kimligi),
                         ("claude-opus-5-5-20260101", 900, 120, 800, "req_h1"))

    def test_ret_kesilme_ve_bozuk_json_hata_olur(self):
        for yanit, beklenen in ((api_yaniti("", "refusal"), "refusal"), (api_yaniti("{", "max_tokens"), "max_tokens"),
                                (api_yaniti("json değil"), "JSON değil")):
            y = self.kur(sahte_anthropic(yanit)).puanla("s", "g")
            self.assertIsNone(y.etiket)
            self.assertIn(beklenen, y.hata)

    def test_api_hatasi_kayda_gecer_anahtar_gizlenir(self):
        m = sahte_anthropic(istisna=lambda mod: mod.RateLimitError("sınır aşıldı sk-test-gizli"))
        y = self.kur(m).puanla("s", "g")
        self.assertIsNone(y.etiket)
        self.assertIn("RateLimitError", y.hata)
        self.assertNotIn("sk-test-gizli", y.hata)

    def test_anahtar_yoksa_acik_hata(self):
        with mock.patch.dict(sys.modules, {"anthropic": sahte_anthropic()}), \
                mock.patch.dict("os.environ", {}, clear=True), tempfile.TemporaryDirectory() as t:
            with self.assertRaisesRegex(RuntimeError, "ANTHROPIC_API_KEY"):
                hakem.AnthropicHakem("claude-opus-5-5", "medium", 500, env_dosyasi=pathlib.Path(t) / ".env")


class SayanHakem:
    """Sahte hakem: çağrıları sayar; `bozuk` kümesindeki sıralarda hata ya da geçersiz çıktı döndürür."""

    def __init__(self, hata_sirasi=(), gecersiz_sirasi=()):
        self.girdiler = []
        self.hata_sirasi, self.gecersiz_sirasi = set(hata_sirasi), set(gecersiz_sirasi)
        self._ic = hakem.SahteHakem()

    def puanla(self, sistem, girdi):
        self.girdiler.append(girdi)
        n = len(self.girdiler)
        y = self._ic.puanla(sistem, girdi)
        if n in self.hata_sirasi:
            return hakem.HakemYaniti(None, None, None, None, None, None, 0.0, None, "RateLimitError: x")
        if n in self.gecersiz_sirasi:
            y.etiket["ogeler"] = []
        return y


class Puanlama(unittest.TestCase):
    def setUp(self):
        self.depo = depo_kur(self)
        kok = self.depo / "eval" / "datasets"
        yaz_veri(kok, "s_ana", "dev", [
            yazildi(ana(1), zorunlu_ogeler=["birinci öğe", "ikinci öğe"]),
            ana(2, soru="bambaşka sözcüklerle ikinci soru burada")])               # altın yanıtı yok
        yaz_veri(kok, "s_tuz", "dev", [yazildi(tuz(1, "T1"))])
        yaz_veri(kok, "s_adv", "dev", [yazildi(adv(1, "TUZ-D0001"))])
        self.cikti = []

    def puanla(self, dizin, h=None, **kw):
        fabrika = (lambda tur, j: h) if h else puanla.varsayilan_hakem
        return puanla.puanla(dizin, self.depo / "configs" / "hakem.yaml", hakem="sahte", depo=self.depo,
                             hakem_fabrikasi=fabrika, git_fn=lambda d: TEMIZ, yaz=self.cikti.append, **kw)

    def satirlar(self, dizin):
        return [json.loads(s) for s in (dizin / "hakem.hakem_test.jsonl").read_text(encoding="utf-8").splitlines()]

    def test_uctan_uca(self):
        dizin = kosum_yap(self.depo)
        h = SayanHakem()
        self.assertEqual(self.puanla(dizin, h), 0)
        satirlar = self.satirlar(dizin)
        self.assertEqual(len(satirlar), 6)                      # 3 yazılmış madde × 2 tekrar
        self.assertEqual({s["madde_id"] for s in satirlar}, {"ANA-D0001", "TUZ-D0001", "ADV-D0001"})
        self.assertTrue(all(s["hata"] is None and s["etiket"] for s in satirlar))
        self.assertEqual(len(satirlar[0]["etiket"]["ogeler"]), 2)
        m = json.loads((dizin / "hakem.hakem_test.manifest.json").read_text(encoding="utf-8"))
        self.assertTrue(m["tamamlandi"])
        self.assertEqual(m["sayilar"], {"puanlanan": 6, "hakem_hatasi": 0, "altin_yok_madde": 1,
                                        "uretici_hatasi": 0, "bos_yanit": 0, "yanit": 8})
        self.assertEqual(m["hakem"]["model"], "claude-opus-5-5")
        self.assertEqual(m["donen_modeller"], ["sahte-hakem"])
        self.assertEqual(m["istem_dosyasi_sha256"], kosum.sha256_dosya(ISTEM))
        liste = (self.depo / "eval" / "results" / f"{dizin.name}.sha256").read_text(encoding="utf-8")
        for ad in ("hakem.hakem_test.jsonl", "hakem.hakem_test.manifest.json", "yanitlar.jsonl", "manifest.json"):
            self.assertIn(ad, liste)
        # Hakeme konfigürasyon kimliği gitmez; konsola madde metni yazılmaz.
        self.assertFalse(any("K0_test" in g for g in h.girdiler))
        self.assertTrue(any(GIZLI in g for g in h.girdiler))
        self.assertNotIn(GIZLI, "\n".join(self.cikti))

    def test_devam_yalniz_eksikleri_puanlar(self):
        dizin = kosum_yap(self.depo)
        h = SayanHakem(hata_sirasi={2}, gecersiz_sirasi={4})
        self.assertEqual(self.puanla(dizin, h), 1)              # iki satır hatalı kaldı
        hatalar = [s["hata"] for s in self.satirlar(dizin) if s["hata"]]
        self.assertEqual(len(hatalar), 2)
        self.assertTrue(any(x.startswith("geçersiz çıktı") for x in hatalar))
        h2 = SayanHakem()
        self.assertEqual(self.puanla(dizin, h2), 0)
        self.assertEqual(len(h2.girdiler), 2)                   # yalnız hatalı iki yanıt yeniden soruldu
        satirlar = self.satirlar(dizin)
        self.assertEqual(len(satirlar), 6)
        self.assertEqual(len({(s["madde_id"], s["tekrar"]) for s in satirlar}), 6)
        m = json.loads((dizin / "hakem.hakem_test.manifest.json").read_text(encoding="utf-8"))
        self.assertEqual((m["devam_sayisi"], m["tamamlandi"]), (1, True))
        h3 = SayanHakem()
        self.assertEqual(self.puanla(dizin, h3), 0)
        self.assertEqual(h3.girdiler, [])

    def test_istem_degisirse_devam_edilmez_yeniden_ile_bastan(self):
        dizin = kosum_yap(self.depo)
        self.puanla(dizin)
        yol = self.depo / "eval" / "judge" / "hakem_istemi.md"
        yol.write_text(yol.read_text(encoding="utf-8").replace("Bir değerlendirme hakemisin.", "Hakemsin."), encoding="utf-8")
        with self.assertRaisesRegex(puanla.HakemHatasi, "istem_dosyasi_sha256"):
            self.puanla(dizin)
        h = SayanHakem()
        self.assertEqual(self.puanla(dizin, h, yeniden=True), 0)
        self.assertEqual(len(h.girdiler), 6)
        self.assertEqual(len(self.satirlar(dizin)), 6)

    def test_uretici_hatasi_puanlanmaz(self):
        class Hatali:
            def __init__(self):
                self.n = 0

            def uret(self, sistem, kullanici):
                self.n += 1
                if self.n == 1:
                    return Yanit("", None, None, None, None, 0.0, None, "APITimeoutError: x")
                return Yanit("yanıt", "end_turn", "sahte", 1, 1, 0.0, "r", None)

        dizin = kosum_yap(self.depo, uretici=Hatali())
        h = SayanHakem()
        self.assertEqual(self.puanla(dizin, h), 0)
        self.assertEqual(len(h.girdiler), 5)
        m = json.loads((dizin / "hakem.hakem_test.manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(m["sayilar"]["uretici_hatasi"], 1)

    def test_bos_yanit_hakeme_sorulmaz(self):
        class Bos:
            def __init__(self):
                self.n = 0

            def uret(self, sistem, kullanici):
                self.n += 1
                metin, durma = ("", "max_tokens") if self.n == 1 else ("yanıt", "end_turn")
                return Yanit(metin, durma, "sahte", 1, 1, 0.0, "r", None)

        dizin = kosum_yap(self.depo, uretici=Bos())
        h = SayanHakem()
        self.assertEqual(self.puanla(dizin, h), 0)
        self.assertEqual(len(h.girdiler), 5)
        m = json.loads((dizin / "hakem.hakem_test.manifest.json").read_text(encoding="utf-8"))
        self.assertEqual((m["sayilar"]["bos_yanit"], m["sayilar"]["puanlanan"]), (1, 5))

    def test_baglam_yokken_dayanak_bosa_cekilir(self):
        def kural(girdi):
            e = hakem.bos_etiket(hakem._oge_sayisi(girdi))
            e.update(atif_dogru=False, desteksiz_iddia=True)      # bağlam yokken doldurulmuş
            return e

        dizin = kosum_yap(self.depo)
        self.assertEqual(self.puanla(dizin, hakem.SahteHakem(kural)), 0)
        self.assertTrue(all(s["etiket"]["atif_dogru"] is None and s["etiket"]["desteksiz_iddia"] is None
                            for s in self.satirlar(dizin)))

    def test_test_bolmesi_dondurulmus_commitle_puanlanir(self):
        dizin = kosum_yap(self.depo)
        m = json.loads((dizin / "manifest.json").read_text(encoding="utf-8"))
        (dizin / "manifest.json").write_text(json.dumps(dict(m, bolme="test", veri_dosyalari={})), encoding="utf-8")
        bos = types.SimpleNamespace(hatalar=[], kayitlar=[])

        def dene(git, degismis):
            with mock.patch.object(veri, "dogrula", return_value=bos):
                return puanla.puanla(dizin, self.depo / "configs" / "hakem.yaml", hakem="sahte", depo=self.depo,
                                     git_fn=lambda d: git, izlenen_degismis_fn=lambda d: degismis, yaz=lambda s: None)

        with self.assertRaisesRegex(puanla.HakemHatasi, "commit"):
            dene({"commit": "baska", "etiket": "degerlendirme-v1.0", "kirli": False}, False)
        with self.assertRaisesRegex(puanla.HakemHatasi, "commit'lenmemiş"):
            dene(dict(TEMIZ), True)
        with self.assertRaisesRegex(puanla.HakemHatasi, "veri setinde yok"):      # korumaları geçti, veri sahte
            dene(dict(TEMIZ), False)

    def test_korumalar(self):
        dizin = kosum_yap(self.depo)
        m = json.loads((dizin / "manifest.json").read_text(encoding="utf-8"))
        (dizin / "manifest.json").write_text(json.dumps(dict(m, tamamlandi=False)), encoding="utf-8")
        with self.assertRaisesRegex(puanla.HakemHatasi, "tamamlanmamış"):
            self.puanla(dizin)
        (dizin / "manifest.json").write_text(json.dumps(m), encoding="utf-8")
        with self.assertRaisesRegex(puanla.HakemHatasi, "sinir"):
            self.puanla(dizin, sinir=0)
        with self.assertRaisesRegex(puanla.HakemHatasi, "manifest.json"):
            self.puanla(self.depo / "yok")
        k = self.depo / "configs" / "hakem.yaml"
        for eski, yeni, mesaj in (("claude-opus-5-5", "<belirlenecek>", "yer tutucu"), ("effort: medium", "effort: orta", "effort"),
                                  ("name: hakem_test", "name: Hakem Test", "name"),
                                  ("eval/judge/hakem_istemi.md", "yok.md", "prompt_file")):
            k.write_text(HAKEM_KONFIG.format(ad="hakem_test").replace(eski, yeni), encoding="utf-8")
            with self.assertRaisesRegex(puanla.HakemHatasi, mesaj):
                self.puanla(dizin)

    def test_veri_degisirse_dev_uyari_test_hata(self):
        dizin = kosum_yap(self.depo)
        yaz_veri(self.depo / "eval" / "datasets", "s_ana", "dev", [
            yazildi(ana(1), zorunlu_ogeler=["birinci öğe", "ikinci öğe"], yasak_ogeler=["sonradan eklenen yasak"]),
            ana(2, soru="bambaşka sözcüklerle ikinci soru burada")])
        self.assertEqual(self.puanla(dizin), 0)
        self.assertTrue(any(s.startswith("UYARI") and "s_ana/dev.jsonl" in s for s in self.cikti))
        m = json.loads((dizin / "manifest.json").read_text(encoding="utf-8"))
        (dizin / "manifest.json").write_text(json.dumps(dict(m, bolme="test")), encoding="utf-8")
        with mock.patch.object(veri, "dogrula", return_value=types.SimpleNamespace(hatalar=[], kayitlar=[])), \
                self.assertRaisesRegex(puanla.HakemHatasi, "değişmiş"):
            self.puanla(dizin, yeniden=True)


if __name__ == "__main__":
    unittest.main()
