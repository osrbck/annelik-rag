"""Bir yazar partisini madde metni göstermeden denetler.

Kullanım: parti_denetim.py KOK SET A B ONCEKI_KOPYA ASAMA1_YEDEK HAM_RAPOR GUVENLI_RAPOR
Yalnız sayı, kimlik ve evet/hayır yazdırır. Çıkış kodu 0: parti kabul; 1: sorun var.
"""
import collections
import json
import re
import subprocess
import sys

kok, set_adi, a, b, onceki, yedek, ham_rapor, guvenli_rapor = sys.argv[1:9]
a, b = int(a), int(b)
sys.path.insert(0, kok)
from eval.runner import veri  # noqa: E402

SABIT = ("id", "set", "bolme", "profil", "soru", "konu", "beklenen_davranis", "sinif",
         "aile_id", "ebeveyn_id", "saldiri_turu", "yazar")
dosya = f"{kok}/eval/datasets/{set_adi}/test.jsonl"


def satirlar(yol):
    with open(yol, encoding="utf-8", newline="") as f:
        return f.read().split("\n")


simdi, once, ilk = satirlar(dosya), satirlar(onceki), satirlar(yedek)
sorun = []


def say(kosul, ad):
    if not kosul:
        sorun.append(ad)


say(len(simdi) == len(ilk) and simdi[-1] == "", "satır sayısı ya da dosya sonu değişmiş")
disarida = [i + 1 for i, (x, y) in enumerate(zip(simdi, once)) if x != y and not a <= i + 1 <= b]
say(not disarida, f"parti dışında değişen satır: {len(disarida)} (ilk {disarida[:5]})")

parti = []
for i in range(a - 1, min(b, len(simdi) - 1)):
    try:
        yeni, eski = json.loads(simdi[i]), json.loads(ilk[i])
    except ValueError:
        sorun.append(f"satır {i + 1}: JSON okunamıyor")
        continue
    kimlik = eski["id"]
    for alan in SABIT:
        if yeni.get(alan) != eski.get(alan):
            sorun.append(f"{kimlik}: sabit alan değişmiş ({alan})")
    if list(yeni)[: len(eski)] != list(eski):
        sorun.append(f"{kimlik}: alan sırası değişmiş")
    if simdi[i] != json.dumps(yeni, ensure_ascii=False) and ilk[i] == json.dumps(eski, ensure_ascii=False):
        sorun.append(f"{kimlik}: satır biçimi değişmiş")
    parti.append(yeni)

durum = collections.Counter()
etiket = collections.Counter()
oge = collections.Counter()
belge = collections.Counter()
yasakli = 0
t1_bos = []
for k in parti:
    kodlar, bozuk = veri.a2_etiketleri(k.get("yazar_notu") or "")
    if bozuk:
        sorun.append(f"{k['id']}: bozuk karar etiketi")
    for kod in kodlar:
        etiket[kod] += 1
    d = k.get("altin_durumu")
    durum[d] += 1
    if d == "bekliyor":
        if not any(kod in veri.A2_KARAR for kod in kodlar):
            sorun.append(f"{k['id']}: işlenmemiş (bekliyor ve karar etiketi yok)")
    elif d == "yazildi":
        oge[len(k.get("zorunlu_ogeler") or [])] += 1
        yasakli += bool(k.get("yasak_ogeler"))
        for kay in k.get("kaynak") or []:
            belge[kay.get("belge_id")] += 1
        if k.get("sinif") == "T1" and not k.get("kaynak"):
            t1_bos.append(k["id"])
    else:
        sorun.append(f"{k['id']}: altin_durumu beklenmeyen değer")
    if set_adi == "s_ana" and not k.get("bilgi_turu"):
        sorun.append(f"{k['id']}: bilgi_turu yok")

# Doğrulayıcı: yalnız bu partinin kimliklerine ait satırlar sayılır, metinleri yazdırılmaz.
kimlikler = {k["id"] for k in parti}
cikti = subprocess.run([sys.executable, "-m", "eval.runner", "dogrula", "--bolme", "test", "--asama2"],
                       cwd=kok, capture_output=True, text=True).stdout
hata = collections.Counter()
uyari = collections.Counter()
for satir in cikti.splitlines():
    m = re.match(r"(HATA|UYARI)\s+(\S+)", satir)
    if m and (m.group(2) in kimlikler or m.group(2).rstrip(":") in kimlikler
              or any(m.group(2).startswith(x[:-2]) and x.endswith(("-a", "-b")) for x in kimlikler)):
        (hata if m.group(1) == "HATA" else uyari)[m.group(2)] += 1
say(not hata, f"doğrulayıcı hatası olan madde: {len(hata)} ({sorted(hata)[:8]})")


# Rapor sızıntı denetimi: rapordaki hiçbir satır test maddelerinden 25 karakterlik bir parça taşımamalı.
def duz(s):
    return re.sub(r"\s+", " ", s.lower()).strip()


N = 25
sabitler = {duz(x) for x in veri.SABIT_OGE.values()}
parcalar = set()
for s in ("s_ana", "s_yas", "s_tuz", "s_adv"):
    for satir in satirlar(f"{kok}/eval/datasets/{s}/test.jsonl"):
        if not satir:
            continue
        k = json.loads(satir)
        metinler = [k.get("soru") or "", k.get("yazar_notu") or ""]
        metinler += k.get("zorunlu_ogeler") or []
        metinler += k.get("yasak_ogeler") or []
        for m in metinler:
            m = re.sub(r"\[A2:[A-Z0-9_]+", " ", m)
            m = duz(m)
            if m in sabitler:
                continue
            for i in range(0, max(0, len(m) - N + 1)):
                parcalar.add(m[i:i + N])
sizan = 0
guvenli = []
with open(ham_rapor, encoding="utf-8") as f:
    for satir in f.read().splitlines():
        d = duz(satir)
        if any(d[i:i + N] in parcalar for i in range(0, max(0, len(d) - N + 1))):
            sizan += 1
            guvenli.append("[satır çıkarıldı: test maddesinden metin taşıyor]")
        else:
            guvenli.append(satir)
with open(guvenli_rapor, "w", encoding="utf-8") as f:
    f.write("\n".join(guvenli) + "\n")

print(f"{set_adi} satır {a}-{b}: {len(parti)} madde")
print("  durum:", dict(durum), "| etiket:", dict(etiket))
print("  öğe sayısı dağılımı (yazildi):", dict(sorted(oge.items())), "| yasak öğeli:", yasakli)
print("  kaynak belgeleri:", dict(belge))
if set_adi == "s_tuz":
    print("  kaynağı boş T1:", len(t1_bos), t1_bos)
print("  doğrulayıcı: hata", sum(hata.values()), "| uyarı", sum(uyari.values()), sorted(uyari)[:10])
print("  rapor: çıkarılan satır", sizan)
if sorun:
    print("  SORUN:")
    for s in sorun[:25]:
        print("   -", s)
    if len(sorun) > 25:
        print("   - … toplam", len(sorun))
    sys.exit(1)
print("  KABUL")
