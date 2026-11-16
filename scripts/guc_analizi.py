"""Değerlendirme protokolündeki örneklem büyüklüklerinin güç analizi (yalnız standart kütüphane).

docs/thesis/degerlendirme_protokolu.md §9.5'teki tabloları üretir. Benzetim yok: bütün
değerler tam (exact) olasılık toplamıdır, dolayısıyla çıktı her çalıştırmada aynıdır.

Protokol v1.2: üstünlük testleri mid-p McNemar (tam koşullu test gereksiz tutucu olduğu için),
aşağı-olmama sınırı tek yönlü %97,5. Tam testin gücü karşılaştırma sütununda verilir.

Eşli tasarım: aynı madde iki konfigürasyonda (A = eski, B = yeni) puanlanır.
  p10 = B başarılı, A başarısız (iyileşme)      p01 = A başarılı, B başarısız (bozulma)
  fark = p10 - p01                              uyumsuzluk = p10 + p01

Kullanım:  python scripts/guc_analizi.py
"""
import math

Z975_TEK = 1.959963984540054  # tek yönlü %97,5 (protokol v1.2 §9.1)


def _binom_pmf(n: int, k: int, p: float) -> float:
    if p <= 0.0:
        return 1.0 if k == 0 else 0.0
    if p >= 1.0:
        return 1.0 if k == n else 0.0
    return math.exp(
        math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
        + k * math.log(p) + (n - k) * math.log1p(-p)
    )


def mcnemar_p(b: int, c: int, mid_p: bool = True) -> float:
    """McNemar testi, iki yönlü p değeri.

    mid_p=True (protokol v1.2 §9.1): gözlenen değerin olasılığının yarısı sayılır.
    mid_p=False: tam koşullu (binom) test; yalnız karşılaştırma için.
    """
    d = b + c
    if d == 0:
        return 1.0
    k = min(b, c)
    kuyruk = sum(_binom_pmf(d, j, 0.5) for j in range(0, k + 1))
    if not mid_p:
        return min(1.0, 2.0 * kuyruk)
    return min(1.0, 2.0 * kuyruk - _binom_pmf(d, k, 0.5))  # b == c iken tam 1


def mcnemar_guc(n: int, fark: float, uyumsuzluk: float, alfa: float, mid_p: bool = True) -> float:
    """McNemar testinin gücü (tam olasılık toplamı): yalnız doğru yöndeki (B > A) retler sayılır."""
    p10 = (uyumsuzluk + fark) / 2
    guc = 0.0
    for d in range(0, n + 1):
        pd = _binom_pmf(n, d, uyumsuzluk)
        if pd < 1e-15:
            continue
        ic = 0.0
        for b in range(d // 2 + 1, d + 1):  # b > c
            if mcnemar_p(b, d - b, mid_p) <= alfa:
                ic += _binom_pmf(d, b, p10 / uyumsuzluk)
        guc += pd * ic
    return guc


def esdegerlik_guc(n: int, gercek_artis: float, uyumsuzluk: float, marj: float) -> float:
    """Eşli 'daha kötü değil' (non-inferiority) testinin gücü.

    Sonuç değişkeni istenmeyen bir oran (aşırı ret); artış = B - A.
    H0: artış >= marj. Ret: tek yönlü %97,5 Wald üst sınırı < marj.
    """
    p_kotu = (uyumsuzluk + gercek_artis) / 2   # B'de var, A'da yok
    p_iyi = (uyumsuzluk - gercek_artis) / 2    # A'da var, B'de yok
    p_ayni = 1.0 - uyumsuzluk
    guc = 0.0
    ln = math.lgamma
    for b in range(0, n + 1):
        for c in range(0, n - b + 1):
            logp = (ln(n + 1) - ln(b + 1) - ln(c + 1) - ln(n - b - c + 1)
                    + (b * math.log(p_kotu) if b else 0.0)
                    + (c * math.log(p_iyi) if c else 0.0)
                    + ((n - b - c) * math.log(p_ayni) if n - b - c else 0.0))
            p = math.exp(logp)
            if p < 1e-15:
                continue
            d = (b - c) / n
            se = math.sqrt(max(b + c - (b - c) ** 2 / n, 0.0)) / n
            if d + Z975_TEK * se < marj:
                guc += p
    return guc


def sifir_olay_ust_sinir(n: int, guven: float = 0.95) -> float:
    """n denemede 0 olay gözlenirse gerçek oranın tek yönlü Clopper-Pearson üst sınırı."""
    return 1.0 - (1.0 - guven) ** (1.0 / n)


def olay_ust_sinir(n: int, k: int, guven: float = 0.95) -> float:
    """n denemede k olay gözlenirse tek yönlü Clopper-Pearson üst sınırı (ikiye bölerek)."""
    if k >= n:
        return 1.0
    alt, ust = k / n, 1.0
    for _ in range(60):
        orta = (alt + ust) / 2
        if sum(_binom_pmf(n, j, orta) for j in range(0, k + 1)) > 1.0 - guven:
            alt = orta
        else:
            ust = orta
    return ust


def duyarlilik_alt_sinir(n: int, k: int, z: float = Z975_TEK) -> float:
    """n güvensiz yanıttan k'sı yakalandıysa duyarlılığın Wilson alt sınırı (iki yönlü %95)."""
    p = k / n
    payda = 1 + z * z / n
    return (p + z * z / (2 * n) - z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / payda


def _tablo(baslik: str, n: int, senaryolar: list[tuple[float, float]]) -> None:
    print(f"\n### {baslik} (n = {n})\n")
    print("| Gerçek fark | Uyumsuzluk | Güç (α = 0,05) | Güç (α = 0,0167, Holm en kötü) | Tam test, α = 0,05 |")
    print("|---|---|---|---|---|")
    for fark, uy in senaryolar:
        g1 = mcnemar_guc(n, fark, uy, 0.05)
        g2 = mcnemar_guc(n, fark, uy, 0.05 / 3)
        g3 = mcnemar_guc(n, fark, uy, 0.05, mid_p=False)
        print(f"| {fark * 100:.0f} puan | {uy * 100:.0f}% | {g1:.2f} | {g2:.2f} | {g3:.2f} |")


def main() -> None:
    print("# Güç analizi — protokol v1.2 örneklem büyüklükleri (mid-p McNemar)")

    _tablo("H1 · S-ANA doğruluk, K1 vs K0", 180,
           [(0.10, 0.25), (0.10, 0.35), (0.15, 0.25), (0.15, 0.35), (0.20, 0.35)])
    _tablo("H2 · S-YAS aile düzeyi tutarlı doğruluk, K2 vs K1", 60,
           [(0.20, 0.30), (0.20, 0.40), (0.25, 0.35), (0.30, 0.40), (0.30, 0.50)])
    _tablo("H3a · S-TUZ risk maddeleri güvenli davranış, K3 vs K2", 120,
           [(0.10, 0.12), (0.10, 0.20), (0.15, 0.17), (0.15, 0.25), (0.20, 0.25)])

    print("\n### H3b · Aşırı ret artışı ≤ 5 puan (n = 210: S-ANA 180 + S-TUZ T0 30)\n")
    print("| Gerçek artış | Uyumsuzluk | Güç (tek yönlü α = 0,025) |")
    print("|---|---|---|")
    for artis, uy in [(0.00, 0.03), (0.00, 0.06), (0.00, 0.10), (0.01, 0.05), (0.02, 0.06)]:
        print(f"| {artis * 100:.0f} puan | {uy * 100:.0f}% | "
              f"{esdegerlik_guc(210, artis, uy, 0.05):.2f} |")

    print("\n### Az sayıda olay gözlenirse söylenebilecek en güçlü şey\n")
    print("| Madde sayısı | 0 hata: üst sınır (tek yönlü %95) | 1 hata | 2 hata |")
    print("|---|---|---|---|")
    for n in (20, 40, 60, 120):
        print(f"| {n} | {sifir_olay_ust_sinir(n) * 100:.1f}% | "
              f"{olay_ust_sinir(n, 1) * 100:.1f}% | {olay_ust_sinir(n, 2) * 100:.1f}% |")

    print("\n### Hakemin 'güvensiz'i yakalama duyarlılığı: Wilson alt sınırı (iki yönlü %95)\n")
    print("| Güvensiz yanıt sayısı | Hepsi yakalandı | 1 kaçtı | 2 kaçtı |")
    print("|---|---|---|---|")
    for n in (15, 25, 35, 50, 80):
        print(f"| {n} | {duyarlilik_alt_sinir(n, n):.2f} | "
              f"{duyarlilik_alt_sinir(n, n - 1):.2f} | {duyarlilik_alt_sinir(n, n - 2):.2f} |")


if __name__ == "__main__":
    main()
