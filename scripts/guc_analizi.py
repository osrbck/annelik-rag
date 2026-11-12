"""Değerlendirme protokolündeki örneklem büyüklüklerinin güç analizi (yalnız standart kütüphane).

docs/thesis/degerlendirme_protokolu.md §9.5'teki tabloları üretir. Benzetim yok: bütün
değerler tam (exact) olasılık toplamıdır, dolayısıyla çıktı her çalıştırmada aynıdır.

Eşli tasarım: aynı madde iki konfigürasyonda (A = eski, B = yeni) puanlanır.
  p10 = B başarılı, A başarısız (iyileşme)      p01 = A başarılı, B başarısız (bozulma)
  fark = p10 - p01                              uyumsuzluk = p10 + p01

Kullanım:  python scripts/guc_analizi.py
"""
import math

Z95_TEK = 1.6448536269514722  # tek yönlü %95


def _binom_pmf(n: int, k: int, p: float) -> float:
    if p <= 0.0:
        return 1.0 if k == 0 else 0.0
    if p >= 1.0:
        return 1.0 if k == n else 0.0
    return math.exp(
        math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
        + k * math.log(p) + (n - k) * math.log1p(-p)
    )


def mcnemar_p(b: int, c: int) -> float:
    """Tam (binom) McNemar testi, iki yönlü p değeri."""
    d = b + c
    if d == 0:
        return 1.0
    kuyruk = sum(_binom_pmf(d, k, 0.5) for k in range(0, min(b, c) + 1))
    return min(1.0, 2.0 * kuyruk)


def mcnemar_guc(n: int, fark: float, uyumsuzluk: float, alfa: float) -> float:
    """Tam McNemar testinin gücü: yalnız doğru yöndeki (B > A) retler sayılır."""
    p10 = (uyumsuzluk + fark) / 2
    guc = 0.0
    for d in range(0, n + 1):
        pd = _binom_pmf(n, d, uyumsuzluk)
        if pd < 1e-15:
            continue
        ic = 0.0
        for b in range(d // 2 + 1, d + 1):  # b > c
            if mcnemar_p(b, d - b) <= alfa:
                ic += _binom_pmf(d, b, p10 / uyumsuzluk)
        guc += pd * ic
    return guc


def esdegerlik_guc(n: int, gercek_artis: float, uyumsuzluk: float, marj: float) -> float:
    """Eşli 'daha kötü değil' (non-inferiority) testinin gücü.

    Sonuç değişkeni istenmeyen bir oran (aşırı ret); artış = B - A.
    H0: artış >= marj. Ret: tek yönlü %95 Wald üst sınırı < marj.
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
            if d + Z95_TEK * se < marj:
                guc += p
    return guc


def sifir_olay_ust_sinir(n: int, guven: float = 0.95) -> float:
    """n denemede 0 olay gözlenirse gerçek oranın tek yönlü Clopper-Pearson üst sınırı."""
    return 1.0 - (1.0 - guven) ** (1.0 / n)


def _tablo(baslik: str, n: int, senaryolar: list[tuple[float, float]]) -> None:
    print(f"\n### {baslik} (n = {n})\n")
    print("| Gerçek fark | Uyumsuzluk | Güç (α = 0,05) | Güç (α = 0,0167, Holm en kötü) |")
    print("|---|---|---|---|")
    for fark, uy in senaryolar:
        g1 = mcnemar_guc(n, fark, uy, 0.05)
        g2 = mcnemar_guc(n, fark, uy, 0.05 / 3)
        print(f"| {fark * 100:.0f} puan | {uy * 100:.0f}% | {g1:.2f} | {g2:.2f} |")


def main() -> None:
    print("# Güç analizi — protokol v1.0 örneklem büyüklükleri")

    _tablo("H1 · S-ANA doğruluk, K1 vs K0", 180,
           [(0.10, 0.25), (0.10, 0.35), (0.15, 0.25), (0.15, 0.35), (0.20, 0.35)])
    _tablo("H2 · S-YAS aile düzeyi tutarlı doğruluk, K2 vs K1", 60,
           [(0.20, 0.30), (0.20, 0.40), (0.25, 0.35), (0.30, 0.40), (0.30, 0.50)])
    _tablo("H3a · S-TUZ risk maddeleri güvenli davranış, K3 vs K2", 120,
           [(0.10, 0.12), (0.10, 0.20), (0.15, 0.17), (0.15, 0.25), (0.20, 0.25)])

    print("\n### H3b · Aşırı ret artışı ≤ 5 puan (n = 210: S-ANA 180 + S-TUZ T0 30)\n")
    print("| Gerçek artış | Uyumsuzluk | Güç (tek yönlü α = 0,05) |")
    print("|---|---|---|")
    for artis, uy in [(0.00, 0.03), (0.00, 0.06), (0.00, 0.10), (0.01, 0.05), (0.02, 0.06)]:
        print(f"| {artis * 100:.0f} puan | {uy * 100:.0f}% | "
              f"{esdegerlik_guc(210, artis, uy, 0.05):.2f} |")

    print("\n### Sıfır olay gözlenirse söylenebilecek en güçlü şey\n")
    print("| Madde sayısı | 0 hata gözlenirse gerçek hata oranı üst sınırı (tek yönlü %95) |")
    print("|---|---|")
    for n in (20, 40, 80, 120):
        print(f"| {n} | {sifir_olay_ust_sinir(n) * 100:.1f}% |")


if __name__ == "__main__":
    main()
