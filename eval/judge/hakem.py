"""Hakem arayüzü, sahte hakem ve Anthropic hakemi (protokol §6.2).

Bu modül import anında yalnızca standart kütüphaneyi kullanır; `anthropic` AnthropicHakem içinde,
ilk kullanımda içe aktarılır. İkinci hakem (başka aileden bir model) aynı arayüzle eklenir.
"""
import dataclasses
import json
import os
import pathlib
import time
from typing import Protocol

from eval.runner.uretici import EFFORT_DUZEYLERI, ROOT, YENIDEN_DENEME, env_oku

from . import istem


@dataclasses.dataclass
class HakemYaniti:
    etiket: dict | None            # istem.SEMA'ya uyan nesne; hata varsa None
    durma_nedeni: str | None
    model: str | None
    girdi_token: int | None
    cikti_token: int | None
    onbellek_token: int | None     # önbellekten okunan girdi token'ı (sistem istemi her çağrıda aynıdır)
    gecikme_sn: float
    istek_kimligi: str | None
    hata: str | None


class Hakem(Protocol):
    def puanla(self, sistem: str, girdi: str) -> HakemYaniti: ...


def bos_etiket(oge_sayisi: int, baglam_var: bool = False) -> dict:
    """Her öğe `yok`, bayraklar kapalı: sahte hakemin ve testlerin başlangıç etiketi."""
    dayanak = False if baglam_var else None
    return {
        "ogeler": [{"no": i, "durum": "yok", "alinti": ""} for i in range(1, oge_sayisi + 1)],
        "kritik_hata": False, "kritik_hata_gerekce": "", "davranis": "yanitladi",
        "teshis_koydu": False, "doz_verdi": False, "acil_alinti": "", "oyalayici_oneri": False,
        "atif_dogru": dayanak, "desteksiz_iddia": dayanak,
    }


def _oge_sayisi(girdi: str) -> int:
    """Girdi metnindeki zorunlu öğe sayısı (sahte hakem için)."""
    govde = girdi.split("ZORUNLU ÖĞELER:\n", 1)[1].split("\nYASAK ÖĞELER:", 1)[0]
    return 0 if govde.strip() == "yok" else len(govde.splitlines())


class SahteHakem:
    """Ağsız, belirlenimci hakem: testler ve `--hakem sahte` için. `kural(girdi) -> etiket` verilebilir."""

    def __init__(self, kural=None):
        self.kural = kural

    def puanla(self, sistem: str, girdi: str) -> HakemYaniti:
        if self.kural is not None:
            etiket = self.kural(girdi)
        else:
            baglam = girdi.split("GETİRİLEN BAĞLAM:\n", 1)[1].split("\nYANIT:", 1)[0].strip() != "yok"
            etiket = bos_etiket(_oge_sayisi(girdi), baglam)
        return HakemYaniti(etiket, "end_turn", "sahte-hakem", len(girdi.split()), 10, 0, 0.0, "sahte", None)


class AnthropicHakem:
    """Anthropic Messages API hakemi: yapılandırılmış çıktı (`output_config.format`) ile şemaya zorlanır.

    Örnekleme parametresi ve `thinking` gönderilmez (model kabul etmez); derinliği `effort` belirler.
    Sistem istemi her çağrıda aynı olduğu için önbelleğe alınır.
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

    def puanla(self, sistem: str, girdi: str) -> HakemYaniti:
        t0 = time.monotonic()
        try:
            yanit = self._istemci.messages.create(
                model=self.model,
                max_tokens=self.max_output_tokens,
                system=[{"type": "text", "text": sistem, "cache_control": {"type": "ephemeral"}}],
                messages=[{"role": "user", "content": girdi}],
                output_config={"effort": self.effort,
                               "format": {"type": "json_schema", "schema": istem.SEMA}},
            )
        except self._anthropic.APIError as e:
            return HakemYaniti(None, None, None, None, None, None, time.monotonic() - t0, None, self._hata(e))
        gecikme = time.monotonic() - t0
        kullanim = getattr(yanit, "usage", None)
        ortak = dict(
            durma_nedeni=yanit.stop_reason, model=yanit.model,
            girdi_token=getattr(kullanim, "input_tokens", None),
            cikti_token=getattr(kullanim, "output_tokens", None),
            onbellek_token=getattr(kullanim, "cache_read_input_tokens", None),
            gecikme_sn=gecikme, istek_kimligi=getattr(yanit, "_request_id", None),
        )
        # Ret ve kesilmede çıktı şemaya uymayabilir: etiket sayılmaz.
        if yanit.stop_reason in ("refusal", "max_tokens"):
            return HakemYaniti(None, hata=f"hakem çıktısı yok: {yanit.stop_reason}", **ortak)
        metin = next((b.text for b in yanit.content if getattr(b, "type", None) == "text"), "")
        try:
            etiket = json.loads(metin)
        except json.JSONDecodeError:
            return HakemYaniti(None, hata="hakem çıktısı JSON değil", **ortak)
        return HakemYaniti(etiket, hata=None, **ortak)
