"""Analiz betiğinin istatistik işlevleri (protokol §9). Yalnız standart kütüphane.

- mid-p McNemar (üstünlük testleri, §9.1) ve tam koşullu test (ek tablo)
- Holm düzeltmesi (§9.2)
- Wilson ve Clopper–Pearson aralıkları (§9.3)
- Kümelenmiş yüzdelik önyükleme: tek oran, eşli fark, tek yönlü üst sınır (§9.1, §9.3)

`mcnemar_p`, `scripts/guc_analizi.py` içindeki işlevle aynı sonucu verir (tests/test_analiz.py denetler):
güç tablosu ile analiz aynı testi kullanmalıdır.
"""
import math
import random

Z975 = 1.959963984540054


def _binom_pmf(n: int, k: int, p: float) -> float:
    if p <= 0.0:
        return 1.0 if k == 0 else 0.0
    if p >= 1.0:
        return 1.0 if k == n else 0.0
    return math.exp(
        math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
        + k * math.log(p) + (n - k) * math.log1p(-p)
    )


def _binom_cdf(n: int, k: int, p: float) -> float:
    """P(X <= k)."""
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    return min(1.0, sum(_binom_pmf(n, j, p) for j in range(0, k + 1)))


def mcnemar_p(b: int, c: int, mid_p: bool = True) -> float:
    """McNemar testi, iki yönlü p. b ve c uyumsuz çiftlerin iki yöndeki sayılarıdır.

    mid_p=True: gözlenen değerin olasılığının yarısı sayılır (§9.1). mid_p=False: tam koşullu test.
    """
    d = b + c
    if d == 0:
        return 1.0
    k = min(b, c)
    kuyruk = sum(_binom_pmf(d, j, 0.5) for j in range(0, k + 1))
    if not mid_p:
        return min(1.0, 2.0 * kuyruk)
    return min(1.0, 2.0 * kuyruk - _binom_pmf(d, k, 0.5))


def holm(p_degerleri: dict, alfa: float = 0.05) -> dict:
    """Holm adım-aşağı düzeltmesi: ad -> {"p", "esik", "anlamli"}.

    p değerleri küçükten büyüğe sıralanır; i. sıradaki (0'dan) alfa / (m - i) ile karşılaştırılır ve
    ilk reddedilemeyen hipotezden sonrakilerin hepsi reddedilmez.
    """
    sirali = sorted(p_degerleri.items(), key=lambda kv: (kv[1], kv[0]))
    m = len(sirali)
    sonuc = {}
    durdu = False
    for i, (ad, p) in enumerate(sirali):
        esik = alfa / (m - i)
        anlamli = (not durdu) and p <= esik
        durdu = durdu or not anlamli
        sonuc[ad] = {"p": p, "esik": esik, "anlamli": anlamli}
    return sonuc


def wilson(k: int, n: int, z: float = Z975) -> tuple[float, float] | None:
    """Tek oran için Wilson aralığı; n = 0 ise None."""
    if n <= 0:
        return None
    p = k / n
    payda = 1 + z * z / n
    merkez = (p + z * z / (2 * n)) / payda
    yari = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / payda
    return (max(0.0, merkez - yari), min(1.0, merkez + yari))


def _ikiye_bol(f, alt: float, ust: float, hedef: float) -> float:
    """Azalan f için f(x) = hedef çözümünü ikiye bölerek bulur."""
    for _ in range(100):
        orta = (alt + ust) / 2
        if f(orta) > hedef:
            alt = orta
        else:
            ust = orta
    return (alt + ust) / 2


def clopper_pearson(k: int, n: int, guven: float = 0.95) -> tuple[float, float] | None:
    """Tam (Clopper–Pearson) iki yönlü aralık; nadir olaylar için (§9.3). n = 0 ise None."""
    if n <= 0:
        return None
    a = (1 - guven) / 2
    # Alt sınır: P(X >= k | p) = a; üst sınır: P(X <= k | p) = a. İkisi de p'ye göre tekdüze.
    alt = 0.0 if k == 0 else _ikiye_bol(lambda p: 1 - _binom_cdf(n, k - 1, p), 1.0, 0.0, a)
    ust = 1.0 if k == n else _ikiye_bol(lambda p: _binom_cdf(n, k, p), 0.0, 1.0, a)
    return (alt, ust)


def tek_yonlu_ust_sinir(k: int, n: int, guven: float = 0.95) -> float | None:
    """Olay oranının tek yönlü tam üst sınırı (sıfır olay kuralı, §9.3)."""
    if n <= 0:
        return None
    if k >= n:
        return 1.0
    return _ikiye_bol(lambda p: _binom_cdf(n, k, p), 0.0, 1.0, 1 - guven)


def yuzdelik(sirali: list, q: float) -> float:
    """Sıralı listenin q yüzdeliği (doğrusal ara değerle; 0 <= q <= 1)."""
    if not sirali:
        raise ValueError("boş liste")
    konum = q * (len(sirali) - 1)
    alt = math.floor(konum)
    ust = min(alt + 1, len(sirali) - 1)
    return sirali[alt] + (sirali[ust] - sirali[alt]) * (konum - alt)


def onyukleme(kumeler: list, n: int = 10_000, tohum: int = 0) -> list[float]:
    """Kümelenmiş önyükleme dağılımı (sıralı).

    kumeler: her küme için (toplam_a, toplam_b, birim_sayisi). İstatistik, yeniden örneklenen
    kümelerde (Σa − Σb) / Σbirim'dir: tek oran için b = 0 verilir, eşli fark için a ve b iki
    konfigürasyonun başarı sayılarıdır. Kümeler yerine koyarak, küme sayısı kadar çekilir; bir küme
    bütün birimleriyle birlikte gelir (S-YAS'ta aile, S-ADV'de ebeveyn kümesi, §9.3).
    """
    if not kumeler:
        return []
    rng = random.Random(tohum)
    m = len(kumeler)
    farklar = [a - b for a, b, _ in kumeler]
    sayilar = [s for _, _, s in kumeler]
    dagilim = []
    dizin = range(m)
    for _ in range(n):
        secim = rng.choices(dizin, k=m)
        payda = sum(sayilar[i] for i in secim)
        dagilim.append(sum(farklar[i] for i in secim) / payda if payda else 0.0)
    dagilim.sort()
    return dagilim


def onyukleme_araligi(kumeler: list, n: int = 10_000, tohum: int = 0,
                      guven: float = 0.95) -> tuple[float, float] | None:
    """İki yönlü yüzdelik aralığı."""
    d = onyukleme(kumeler, n, tohum)
    if not d:
        return None
    a = (1 - guven) / 2
    return (yuzdelik(d, a), yuzdelik(d, 1 - a))


def onyukleme_ust_sinir(kumeler: list, n: int = 10_000, tohum: int = 0, guven: float = 0.975) -> float | None:
    """Tek yönlü üst sınır (aşağı-olmama, §9.1: %97,5)."""
    d = onyukleme(kumeler, n, tohum)
    return yuzdelik(d, guven) if d else None
