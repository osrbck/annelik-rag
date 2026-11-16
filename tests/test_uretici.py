"""eval.runner.uretici testleri; ağ yok, `anthropic` yerine sahte modül enjekte edilir."""
import pathlib
import sys
import tempfile
import types
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from eval.runner import uretici  # noqa: E402
from eval.runner.uretici import AnthropicUretici, SahteUretici, kullanici_mesaji, profil_satiri  # noqa: E402


class ProfilSatiri(unittest.TestCase):
    def test_durumlar(self):
        c = lambda **k: {"donem": "cocuk", **k}  # noqa: E731
        beklenen = [
            ({"donem": "gebelik", "gebelik_haftasi": 28}, "Profil: gebe, 28. hafta"),
            (c(yas_ay=0, yas_gun=12), "Profil: bebek, 12 günlük"),
            (c(yas_ay=0), "Profil: bebek, 0–1 aylık"),
            (c(yas_ay=1), "Profil: çocuk, 1 aylık"),
            (c(yas_ay=8), "Profil: çocuk, 8 aylık"),
            (c(yas_ay=23), "Profil: çocuk, 23 aylık"),
            (c(yas_ay=24), "Profil: çocuk, 2 yaşında"),
            (c(yas_ay=40), "Profil: çocuk, 3 yaş 4 aylık"),
            (c(yas_ay=216), "Profil: çocuk, 18 yaşında"),
        ]
        for profil, satir in beklenen:
            self.assertEqual(profil_satiri(profil), satir)

    def test_gecersiz_donem(self):
        with self.assertRaises(ValueError):
            profil_satiri({"donem": "x"})

    def test_kullanici_mesaji(self):
        m = {"profil": {"donem": "cocuk", "yas_ay": 8}, "soru": "Ateşi var?"}
        self.assertEqual(kullanici_mesaji(m), "Profil: çocuk, 8 aylık\n\nAteşi var?")


class Sahte(unittest.TestCase):
    def test_belirlenimci_ve_hatasiz(self):
        a = SahteUretici().uret("sistem", "mesaj")
        b = SahteUretici().uret("sistem", "mesaj")
        self.assertEqual(a, b)
        self.assertNotEqual(a, SahteUretici().uret("sistem", "başka"))
        self.assertIsNone(a.hata)
        self.assertEqual(a.model, "sahte")


def sahte_anthropic(yanit=None, istisna=None):
    """Sahte `anthropic` modülü: istekleri `cagrilar` ve `kurucu` listelerine yazar."""
    m = types.ModuleType("anthropic")
    m.cagrilar, m.kurucu = [], []

    class APIError(Exception):
        pass

    for ad, ata in [("APIConnectionError", APIError), ("APITimeoutError", "APIConnectionError"),
                    ("APIStatusError", APIError), ("BadRequestError", "APIStatusError"),
                    ("AuthenticationError", "APIStatusError"), ("PermissionDeniedError", "APIStatusError"),
                    ("NotFoundError", "APIStatusError"), ("RateLimitError", "APIStatusError")]:
        setattr(m, ad, type(ad, (getattr(m, ata) if isinstance(ata, str) else ata,), {}))
    m.APIError = APIError

    class Messages:
        def create(self, **kw):
            m.cagrilar.append(kw)
            if istisna:
                raise istisna(m)
            return yanit

    class Anthropic:
        def __init__(self, **kw):
            m.kurucu.append(kw)
            self.messages = Messages()

    m.Anthropic = Anthropic
    return m


def yanit_nesnesi(blocklar=None, stop="end_turn"):
    blocklar = blocklar if blocklar is not None else [
        types.SimpleNamespace(type="thinking", thinking="gizli"),
        types.SimpleNamespace(type="text", text="Merhaba "),
        types.SimpleNamespace(type="text", text="dünya"),
    ]
    return types.SimpleNamespace(
        content=blocklar, stop_reason=stop, model="claude-haiku-5-5-20260101",
        usage=types.SimpleNamespace(input_tokens=11, output_tokens=22), _request_id="req_123")


class AnthropicUreticiTesti(unittest.TestCase):
    def kur(self, modul, anahtar="sk-test-gizli"):
        env = {"ANTHROPIC_API_KEY": anahtar} if anahtar else {}
        yamalar = [mock.patch.dict(sys.modules, {"anthropic": modul}),
                   mock.patch.dict("os.environ", env, clear=True)]
        for y in yamalar:
            y.start()
            self.addCleanup(y.stop)
        return AnthropicUretici("claude-haiku-5-5", "medium", 4000,
                                env_dosyasi=pathlib.Path("/yok/.env"))

    def test_istek_bicimi_ornekleme_ve_thinking_yok(self):
        m = sahte_anthropic(yanit_nesnesi())
        u = self.kur(m)
        y = u.uret("SİSTEM", "KULLANICI")
        self.assertEqual(len(m.cagrilar), 1)
        kw = m.cagrilar[0]
        self.assertEqual(set(kw), {"model", "max_tokens", "system", "messages", "output_config"})
        for yasak in ("temperature", "top_p", "top_k", "seed", "thinking"):
            self.assertNotIn(yasak, kw)
        self.assertEqual(kw["output_config"], {"effort": "medium"})
        self.assertEqual(kw["model"], "claude-haiku-5-5")
        self.assertEqual(kw["max_tokens"], 4000)
        self.assertEqual(kw["system"], "SİSTEM")
        self.assertEqual(kw["messages"], [{"role": "user", "content": "KULLANICI"}])
        self.assertEqual(m.kurucu[0]["max_retries"], 2)

    def test_yanit_kaydi(self):
        u = self.kur(sahte_anthropic(yanit_nesnesi()))
        y = u.uret("s", "k")
        self.assertEqual(y.metin, "Merhaba dünya")
        self.assertEqual((y.durma_nedeni, y.model), ("end_turn", "claude-haiku-5-5-20260101"))
        self.assertEqual((y.girdi_token, y.cikti_token, y.istek_kimligi), (11, 22, "req_123"))
        self.assertIsNone(y.hata)
        self.assertGreaterEqual(y.gecikme_sn, 0)

    def test_refusal_ve_max_tokens_hata_degil(self):
        for neden in ("refusal", "max_tokens"):
            u = self.kur(sahte_anthropic(yanit_nesnesi(blocklar=[], stop=neden)))
            y = u.uret("s", "k")
            self.assertEqual(y.durma_nedeni, neden)
            self.assertIsNone(y.hata)

    def test_istisna_hataya_donusur(self):
        def at(m):
            return m.RateLimitError("çok istek sk-test-gizli")
        u = self.kur(sahte_anthropic(istisna=at))
        y = u.uret("s", "k")
        self.assertTrue(y.hata.startswith("RateLimitError: "))
        self.assertNotIn("sk-test-gizli", y.hata)  # anahtar kayda sızmaz
        self.assertEqual((y.metin, y.durma_nedeni, y.model), ("", None, None))

    def test_baglanti_ve_genel_hatalar(self):
        for ad in ("APITimeoutError", "APIStatusError", "BadRequestError", "APIError"):
            u = self.kur(sahte_anthropic(istisna=lambda m, ad=ad: getattr(m, ad)("x")))
            self.assertTrue(u.uret("s", "k").hata.startswith(ad + ": "))

    def test_anahtar_yoksa_hata(self):
        with self.assertRaises(RuntimeError):
            self.kur(sahte_anthropic(), anahtar=None)

    def test_paket_yoksa_acik_hata(self):
        with mock.patch.dict(sys.modules, {"anthropic": None}):
            with self.assertRaises(RuntimeError) as c:
                AnthropicUretici("m", "medium", 10)
        self.assertIn("anthropic", str(c.exception))

    def test_gecersiz_effort(self):
        with self.assertRaises(ValueError):
            AnthropicUretici("m", "yüksek", 10)

    def test_modul_importunda_anthropic_gerekmez(self):
        self.assertNotIn("anthropic", vars(uretici))


class EnvOku(unittest.TestCase):
    def test_ayrisma(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / ".env"
            p.write_text('# yorum\nA=1\nexport B="iki"\n\nC = \'üç\'\nbozuk\n', encoding="utf-8")
            self.assertEqual(uretici.env_oku(p), {"A": "1", "B": "iki", "C": "üç"})
            self.assertEqual(uretici.env_oku(p.with_name("yok")), {})


if __name__ == "__main__":
    unittest.main()
