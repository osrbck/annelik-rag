# Dev pilotu raporu

Dayanak: `docs/thesis/degerlendirme_protokolu.md` §9.7. Dondurmadan önce dev üzerinde ölçülenler buraya
yazılır. Dev seti küçüktür (85 madde); buradaki oranlar kestirim değil yön göstergesidir.

| Ölçüm (§9.7) | Durum |
|---|---|
| Altın yanıt aşamasında rehberde karşılığı bulunan soru oranı | **ölçüldü (2026-11-16), §1** |
| Altın yanıt incelemesinde madde başına süre | ölçülmedi: araştırmacının dev incelemesiyle ölçülecek (§1.5) |
| K0'ın S-ANA ve S-YAS doğruluğu | ölçülmedi |
| K1'de yanlış yaş bandından getirme; K1–K2 uyumsuzluğu | ölçülmedi |
| K1-s ile K1 ve K2'nin getirme ölçütleri | ölçülmedi |
| K2–K3 aşırı ret uyumsuzluğu | ölçülmedi |
| Tekrarlar arası kararsız madde payı | ölçülmedi |

## 1. Altın yanıt aşaması pilotu (2026-11-16)

**Yöntem.** Yazar model `gemini-4-argon` (birinci aşamayla aynı), yönerge
`eval/datasets/YAZIM_YONERGESI_ASAMA2.md`. İlk tur sürüm 1.0 ile üç ayrı yazar koşumunda yapıldı (S-ANA;
S-YAS; S-TUZ ve S-ADV). Sonuç doğrulayıcıyla (`dogrula --bolme dev --asama2`: 0 hata), birinci aşama
yedeğiyle alan alan karşılaştırmayla (soru, profil, sınıf gibi sabit alanlarda değişiklik yok; test
dosyalarının hash'i aynı) ve kaynak sayfalarıyla denetlendi. Bulgulara göre yönerge 1.1 oldu ve S-ANA ile
S-YAS maddeleri ikinci bir turda düzeltildi. Aşağıdaki sayılar düzeltme turundan sonrakilerdir.

### 1.1 Kapsam: rehberde karşılığı bulunan sorular

| Küme | Yazıldı / bakıldı | Oran | %95 aralık (Wilson) |
|---|---|---|---|
| S-ANA (madde) | 24 / 30 | 0,80 | 0,63 – 0,90 |
| S-YAS (aile) | 6 / 10 | 0,60 | 0,31 – 0,83 |
| S-TUZ T0 (madde) | 1 / 4 | 0,25 | 0,05 – 0,70 |

S-ANA, döneme göre: gebelik 4/5, 0–1 ay 5/5, 1–12 ay 3/5, 1–5 yaş 4/5, 6–12 yaş 4/5, 13–18 yaş 4/5.
Konuya göre: izlem 4/5, beslenme 5/5, aşı 3/4, büyüme 5/5, hastalık 2/3, emzirme 2/3, diğer 3/5.

Karşılığı bulunmayan sorular (S-ANA, 6): gebelikte diş eti bakımı; aşıdan sonra evde bakım; bebekte
burun tıkanıklığını açma; memeden kesme; okul taramasının nedeni; ergende uyku düzeni. S-YAS'ta
yazılamayan dört aile: ateş (yenidoğan ile 8 yaş; 8 yaş için evde izlem belgelerde yok), süt dişinin
sallanması, gebelikte bulantı (belgeler hafta eşiği vermiyor), bütün kuruyemiş (yaş eşiği belgede
yazılı değil). T0'da karşılığı bulunmayanlar gündelik sorulardır: pancarın dışkıyı boyaması, ergenlik
sivilcesinde yüz temizliği, açılmış şurubun saklanması.

**Acil durumların dayanağı (T1).** Beş T1 maddesinden yalnız birinin kırmızı bayrağı bilgi tabanındaki
bir belgede acil başvuru olarak geçiyor (C13, yanık). G12 (gebelikte karına darbe), Y12 (yenidoğanda
uzun süre idrar yapmama), O04 (çok su içme ve dalgınlık) ve E05 (istismar bildirimi) için dayanak sayfası
bulunamadı. Dev'de lohusalık (L) grubundan madde yoktu; doğum sonu rehberinin etkisi burada görülmez.

### 1.2 Nitelik denetimi

- **Sayılar.** Yaklaşık yirmi öğedeki her sayı (hafta, ay, doz dışı miktar, yüzde) gösterilen kaynak
  sayfasının metniyle karşılaştırıldı; hepsi sayfada bulundu. Yazarın kendi eklediği üç açıklama sayısı
  ("yaklaşık 1–1,5 aylıkken", "14. gün", "ilk 14 hafta") belgede yoktu ve düzeltme turunda çıkarıldı.
- **Çıkarım.** İlk turda üç öğe belgenin söylediğinden değil yazarın çıkarımından geliyordu (tetkiklerin
  amacı; bir belirtinin tersinden kurulan kural; 14 yaşında bütün kuruyemiş). Düzeltme turunda biri
  `KISMI` oldu, biri belgenin yönünde yeniden yazıldı, biri (aile) `ESIK_YOK` oldu.
- **Öğe sayısı.** İlk turda S-ANA maddelerinin 26'sından 18'i üç öğeliydi ve öğelerin çoğu birkaç bilgiyi
  birlikte taşıyordu. Düzeltmeden sonra: bir öğeli 5, iki öğeli 17, üç öğeli 2 madde (ortalama 1,9);
  liste taşıyan her öğe "en az ikisi" ya da "hepsi" diye nicelik belirtiyor.
- **Yasak öğeler.** İlk turda yazılan 14 S-YAS maddesinin hepsinde yasak öğe vardı; bazıları zararsız,
  aşırı temkinli yanıtlardı. Düzeltmeden sonra 12 maddenin 7'sinde var.
- **Resim sayfalar.** Hiçbir madde `OCR` etiketi almadı. Aşı kartının metin katmanı var; tablo
  sütunları portal sayfasındaki metinle doğrulandı.

### 1.3 Yönergede değişenler (1.0 → 1.1)

Çıkarım örnekleri ve "ana soru" kuralı (§5.2); liste kuralı ve "üçe tamamlamak amaç değil" (§6); aşırı
temkinli yanlışın yasak öğe olmaması (§7); eski–yeni belge farkının `CELISKI` değil `guncellik` olması
(§9.1); S-YAS'ta aralık biçimli eşikler, `KARSILIK_YOK` ile `ESIK_YOK` ayrımı, eşik notu için etiket
gerekmemesi (§9.2); T1'de olağan risk formunun acil dayanağı sayılmaması (§9.3); `bilgi_turu` ölçütünde
program içeriği ve gerekçesi soran sorular (§3; dev etiketleri değiştirilmedi).

### 1.4 Test için anlamı

Test setlerinde yedek %10'dur. Dev oranları teste taşınırsa:

| Küme | Yazılmış | Hedef | Beklenen (aralık) |
|---|---|---|---|
| S-ANA | 195 madde | 180 | 156 (123 – 176) |
| S-YAS | 66 aile | 60 | 40 (20 – 55) |
| S-TUZ T0 | 33 madde | 30 | 8 (2 – 23) |

Üç kümede de aralığın üst ucu hedefin altındadır: altın yanıt aşamasından sonra test setleri büyük
olasılıkla hedefin altında kalacak. Protokol §4.1 bu durumda iki yol verir (kaynak eklemek ya da tabakayı
küçültüp güç tablosunu yeniden üretmek); üçüncü yol eksik tabakalar için yeni soru yazdırmaktır
(§4.6, kural 4). Karar, test koşumunun gerçek sayıları görüldükten sonra verilir.

T0 için sorun yapısaldır: T0 soruları "ürkütücü görünen ama zararsız" gündelik sorulardır ve resmî
rehberler bu tür soruları çoğunlukla ele almaz. Aşırı ret ölçütü (M4) S-ANA ile T0'ı birlikte kullanır.

### 1.5 Sınırlar ve açık işler

- Oranlar 30 madde, 10 aile ve 4 madde üzerindendir; aralıklar geniştir.
- Nitelik denetimini geliştirici yaptı (klinisyen değil); dev maddeleri uzman onayına gitmez.
- Araştırmacının dev altın yanıtlarını kaynak sayfasıyla karşılaştırırken harcadığı süre ölçülmedi;
  uzman süresi bütçesi (§6.3: S-ANA 45 sn, S-YAS aile 75 sn) bu ölçümle sınanacak.
- Yazar koşum süreleri (bilgi için): ilk tur 25, 18 ve 15 dakika; düzeltme turu 19 ve 16 dakika.
