"""Üretici (generator) arayüzü, sahte üretici ve Anthropic üreticisi.

Bu modül import anında yalnızca standart kütüphaneyi kullanır; `anthropic`
AnthropicUretici içinde, ilk kullanımda içe aktarılır.
"""
import dataclasses
import hashlib
import os
import pathlib
import time
from typing import Protocol

ROOT = pathlib.Path(__file__).resolve().parents[2]
EFFORT_DUZEYLERI = ("low", "medium", "high", "xhigh", "max")
YENIDEN_DENEME = 2  # protokol §7.3


@dataclasses.dataclass
class Yanit:
    metin: str
    durma_nedeni: str | None
    model: str | None
    girdi_token: int | None
    cikti_token: int | None
    gecikme_sn: float
    istek_kimligi: str | None
    hata: str | None


class Uretici(Protocol):
    def uret(self, sistem: str, kullanici: str) -> Yanit: ...


def profil_satiri(profil: dict) -> str:
    """Profili kullanıcı mesajının başına eklenen tek satıra çevirir (protokol §2)."""
    donem = profil.get("donem")
    if donem == "gebelik":
        return f"Profil: gebe, {profil['gebelik_haftasi']}. hafta"
    if donem != "cocuk":
        raise ValueError("profil.donem 'gebelik' ya da 'cocuk' olmalı")
    ay = profil["yas_ay"]
    if ay == 0:
        if profil.get("yas_gun") is not None:
            return f"Profil: bebek, {profil['yas_gun']} günlük"
        return "Profil: bebek, 0–1 aylık"
    if ay < 24:
        return f"Profil: çocuk, {ay} aylık"
    yil, kalan = divmod(ay, 12)
    if kalan == 0:
        return f"Profil: çocuk, {yil} yaşında"
    return f"Profil: çocuk, {yil} yaş {kalan} aylık"


def kullanici_mesaji(madde: dict) -> str:
    """Her konfigürasyonda aynı: profil satırı, boş satır, soru."""
    return f"{profil_satiri(madde['profil'])}\n\n{madde['soru']}"


class SahteUretici:
    """Ağsız, belirlenimci üretici: testler ve `--uretici sahte` için."""

    def uret(self, sistem: str, kullanici: str) -> Yanit:
        ozet = hashlib.sha256(f"{sistem}\n{kullanici}".encode("utf-8")).hexdigest()[:12]
        return Yanit(
            metin=f"[sahte yanıt {ozet}]", durma_nedeni="end_turn", model="sahte",
            girdi_token=len(kullanici.split()), cikti_token=3, gecikme_sn=0.0,
            istek_kimligi=f"sahte_{ozet}", hata=None,
        )


def env_oku(yol: pathlib.Path) -> dict[str, str]:
    """Küçük .env çözümleyici: ANAHTAR=değer satırları, # yorum, isteğe bağlı tırnak."""
    sonuc: dict[str, str] = {}
    try:
        satirlar = yol.read_text(encoding="utf-8").splitlines()
    except OSError:
        return sonuc
    for satir in satirlar:
        satir = satir.strip()
        if not satir or satir.startswith("#") or "=" not in satir:
            continue
        ad, _, deger = satir.partition("=")
        ad = ad.strip().removeprefix("export ").strip()
        deger = deger.strip()
        if len(deger) >= 2 and deger[0] == deger[-1] and deger[0] in "\"'":
            deger = deger[1:-1]
        sonuc[ad] = deger
    return sonuc


class AnthropicUretici:
    """Anthropic Messages API üreticisi.

    Örnekleme parametresi (temperature, top_p, top_k, seed) ve `thinking`
    GÖNDERİLMEZ: model bunları reddeder / uyarlamalı düşünmeyi kendisi yürütür.
    Derinliği output_config.effort belirler.
    """

    def __init__(self, model: str, effort: str, max_output_tokens: int,
                 env_dosyasi: pathlib.Path | None = None):
        if effort not in EFFORT_DUZEYLERI:
            raise ValueError(f"effort şunlardan biri olmalı: {', '.join(EFFORT_DUZEYLERI)}")
        try:
            import anthropic
        except ImportError as e:
            raise RuntimeError(
                "'anthropic' paketi kurulu değil; gereksinimleri kurun (pip install anthropic)"
            ) from e
        self._anthropic = anthropic
        self.model = model
        self.effort = effort
        self.max_output_tokens = max_output_tokens
        anahtar = os.environ.get("ANTHROPIC_API_KEY") or env_oku(
            env_dosyasi or ROOT / ".env").get("ANTHROPIC_API_KEY")
        if not anahtar:
            raise RuntimeError("ANTHROPIC_API_KEY bulunamadı (ortam değişkeni ya da depo kökündeki .env)")
        self._anahtar = anahtar
        self._istemci = anthropic.Anthropic(api_key=anahtar, max_retries=YENIDEN_DENEME)

    def _hata(self, e: Exception) -> str:
        mesaj = str(e).replace(self._anahtar, "***")[:500]
        return f"{type(e).__name__}: {mesaj}"

    def uret(self, sistem: str, kullanici: str) -> Yanit:
        a = self._anthropic
        t0 = time.monotonic()
        hata = None
        yanit = None
        try:
            yanit = self._istemci.messages.create(
                model=self.model,
                max_tokens=self.max_output_tokens,
                system=sistem,
                messages=[{"role": "user", "content": kullanici}],
                output_config={"effort": self.effort},
            )
        except (a.AuthenticationError, a.PermissionDeniedError, a.NotFoundError,
                a.BadRequestError, a.RateLimitError) as e:
            hata = self._hata(e)
        except (a.APITimeoutError, a.APIConnectionError) as e:
            hata = self._hata(e)
        except a.APIStatusError as e:
            hata = self._hata(e)
        except a.APIError as e:
            hata = self._hata(e)
        gecikme = time.monotonic() - t0
        if yanit is None:
            return Yanit("", None, None, None, None, gecikme, None, hata)
        metin = "".join(b.text for b in yanit.content if getattr(b, "type", None) == "text")
        kullanim = getattr(yanit, "usage", None)
        return Yanit(
            metin=metin,
            durma_nedeni=yanit.stop_reason,  # refusal ve max_tokens sonuçtur, hata değil
            model=yanit.model,
            girdi_token=getattr(kullanim, "input_tokens", None),
            cikti_token=getattr(kullanim, "output_tokens", None),
            gecikme_sn=gecikme,
            istek_kimligi=getattr(yanit, "_request_id", None),
            hata=None,
        )
