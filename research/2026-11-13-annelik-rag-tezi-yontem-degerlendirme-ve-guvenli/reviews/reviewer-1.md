# Review

## Overall
researcher-1, -3 ve -4'ün açabildiğim kaynakları bulgularını taşıyor, hesapları da tutuyor. researcher-2'nin notları bu haliyle duramaz: birkaç temel bulgu gösterilen kaynakta yok ve "yüksek kanıt gücü" etiketi hak edilmemiş. Kanıtın çoğu önbaskı ve tek çalışma; ekip bunu çoğunlukla işaretlemiş. Açamadıklarım: Fagerland 2013, NICE NG143, Bean ve ark., Vach ve ark., Rosie tam metinleri.

## researcher-1
Solid: Pombal oranları, HealthBench doğrulaması (34 ölçüt, 60.896 yargı, makro-F1 0,709, 5/7 tema), Lee düzeltmesi ve Miller sayıları kaynakla birebir. κ aralığı, Wilson sınırı, 0,95⁵, çoğunluk dönüşümü ve H3b gücünü yeniden hesapladım; doğru.
Problems:
1. [should] "raporlama literatürü sınıf bazlı duyarlılık/özgüllük istiyor" → aynı notlar CHART ve TRIPOD-LLM maddelerinin doğrulanamadığını söylüyor → cümleyi çıkar; "Supported"ı "iki önbaskının uygulamasıyla" diye daralt.
2. [should] "çok hata yapan konfigürasyon (K0) daha çok şişer… H3b için anti-tutucu" → Pombal aynı üreticinin konfigürasyonlarını karşılaştırmıyor; Claude hakemlerinin HealthBench oranı 1'in altında → varsayım olarak yaz.
3. [should] "Claude'un HealthBench aile oranı… yoktu" → tabloda var (Sonnet 0,89; Haiku 0,91). "Hekim ortalamaları 0,646–0,730" → tabloda 0,569–0,730. "m=200 ≈ 0,1" → yalnız q0=0,7, q1=0,9, p̂=0,3 için. Üçünü düzelt.
4. [should] "kanıt güçlü, tek simülasyon çalışması" → kendi içinde tutarsız; kaynağı açamadım → "orta" de.

Missing: Eşdeğersizlik marjı için birincil standart metni; H3b önerisi buna dayanıyor.

## researcher-2
Solid: DoktorSitesi kaydı (167.732 satır, alanlar, CC BY 4.0), DIAN (50 soru, 148 puanlayıcı) ve HealthBench ölçek sayıları doğru. Saniye/madde aritmetiği yerinde bir uyarı.
Problems:
1. [must] "gerçek kullanıcı trafiğine kıyasla tekdüze" (Teixeira de Lima) ve "daha düşük N-gram çeşitliliği… gerçek dünya performansını olduğundan yüksek gösterir" (Filice) → iki özet de gerçek sorgularla karşılaştırma ya da şişme bildirmiyor; yalnız üreticilerin dengesizliğini/çeşitlilik eksikliğini söylüyor → bulguları buna indir; hükmü "Supported"dan "Undecided"a çek.
2. [must] "çıpalama ve otomasyon yanlılığı… doğruluğunu başlangıç seviyesinin altına düşürdüğü" (Arora 2025) → HealthBench'te böyle bir bulgu yok → gerçek kaynağı bul ya da sil.
3. [must] HealthBench → "madde başına en az 3–5 dakika" → kaynakta süre verisi yok → ekibin yargısı olarak işaretle, pilotla ölç; "bilimsel olarak savunulamaz"ı çıkar.
4. [must] "etik kurul onayı gerektirmeyen… anonimleştirilmiş" → Zenodo kaydı onam ya da anonimleştirmeden söz etmiyor → iddiayı kaldır, etik kurula sor.
5. [must] "genellikle 20 ile 200" ve Rosie bulguları → aralığın kaynağı yok. İspanyolca Rosie [30 kişilik pilot RKÇ](https://formative.jmir.org/2026/1/e101898); test seti kurulumunu anlatmıyor. İlk çalışma 2024 tarihli. "Güç hedeflerini koru (yüksek)" bunlardan çıkmaz → sil ya da yeniden kaynakla.
6. [must] K-QA "hekimlerce… ayrıştırılan 1.212 soru" → özete göre yalnız bir alt küme yanıtlanmış → düzelt.
7. [should] CARES/OR-Bench "label flipping" iddiaları özet sayfalarında yok → tam metinden alıntı göster ya da çıkarım olarak yaz.
8. [should] MediQ "%20–22… kanıtlamıştır" → özet %22,3 diyor, taban belirsiz. HealthBench'te bağlam arama eksen değil tema.

Missing: LLM taslağı incelemesinde otomasyon yanlılığını ölçen gerçek deneysel çalışmalar.

## researcher-3
Solid: Fraile Navarro (%16,7 / %50 / %20,8; yaklaşık %60 koşullu), Jha ve ark. (N=150, %86,7, 50 karakterlik pencere, şablonlar), NHS dozları, Health-ORSC-Bench ve MedHarm doğru. Üç kuralı ile 29/59 madde hesapları doğru; hüküm ölçülü.
Problems:
1. [should] "0–5 ay için >60" (NG143) → sayfayı açamadım; bildiğim tabloda >60 yaştan bağımsız kırmızı, >50 ve >40 sarı sütunda. Üç aydan küçükte ≥38 °C kırmızısı da eksik → birincil metinden düzeltmeden kural listesine alma.
2. [should] "LLM hakemlerini klinisyenlere kör olarak denetletti" → denetim 24 amaçlı seçilmiş yanıt; klinisyen iki hakemle birlikte yalnız 4/23'te uyuşuyor; %60 anahtar sözcük sezgiseliyle bulunmuş → bunları yaz.
3. [should] "Benzer çalışmalar 150 civarı" → tek önbaskı. Düzenleyici bölüm iki ikincil web sayfasına dayanıyor; "KVKK yükü düşük" doğrulanmamış.

Missing: Bakanlık protokollerinin kendi tehlike işaretleri.

## researcher-4
Solid: Liu ve ark. (OR 1,35; insan 1,65, otomatik 1,20; Egger), Kim ve ark. (%22; %6/%5), Zerhoudi ve Hassan özetleri doğru. "(özetten)" işaretleri ve "Undecided" hükmü dürüst.
Problems:
1. [should] "iki bağımsız çalışma" (Türkçe erişim) → biri Almanca (Vach); Türkçe kanıt 100 soruluk tek önbaskı → güveni "düşük" yap.
2. [should] "H2'yi doğrulayıcı olmaktan çıkar" → doğrudan kanıt yok, %10 eşiği keyfi → dev pilotuna bağlı koşullu öneri yap.
3. [should] "ilk 16 pasaj yerine… 3–5" → 16 Kim'in kurulumu, tasarımın değil; 3–5'in kaynağı yok.
4. [should] "%20,0… %70,6" → farklı modeller karşılaştırılıyor → hüküm cümlesinde belirt.

Missing: AMAQA birincil makalesi.

## Contradictions between researchers
- researcher-2 "güç hedeflerini koru" diyor. researcher-1 (H3b gücü ≈0,63), researcher-3 (T1'de 40 madde yetmez) ve researcher-4 (H2 güçsüz) tersini hesapla gösteriyor.
- researcher-2'ye göre question-first akışı H1'de erişime haksız avantaj vermez. researcher-4'e göre altın yanıtlar derlemden yazıldığı için K1 yapısal olarak kayrılır; tasarım metni researcher-4'ü destekliyor.
- researcher-2 H2 ölçütünü "koru" diyor, researcher-4 ikincile indiriyor.
- researcher-2 açık veri için etik onay gerekmediğini söylüyor; researcher-3 etik/KVKK'yı doğrulanmamış sayıyor.
- researcher-3'ün doz/tanı bayrağı ayrımı, researcher-1'in "güvensiz yanıt" duyarlılık eşiğinin tanımını değiştirir; hakem doğrulamasından önce çözülmeli.

## What can be stated with confidence, and what cannot
Güvenle söylenebilir:
- Türetilmiş ikili etikette tek κ, en iyi uygulamanın gerisinde.
- 100 yanıtla duyarlılık ≥0,90 doğrulanamaz.
- Çoğunluk ve en kötü durum kestirimleri tekrar sayısına bağlı.
- 40 maddede sıfır hata "güvenli" demeye yetmez.
- Yayımlanmış RAG kazancı küçük ve yayın yanlılığı taşıyor.
- Resmi ebeveyn bilgilendirmesi (NHS) yaşa göre doz veriyor.

Söylenemez:
- Sentetik soruların doğruluğu ne kadar şişirdiği.
- Klinisyen incelemesine madde başına kaç dakika gerektiği.
- Aynı aile hakemin K0–K3 farklarını hangi yönde kaydırdığı.
- Yaş filtresinin etkisi ve Türkçede en iyi erişim kurulumu.
- Kural katmanının net yararı.
- Prototipin hukuki statüsü.

## Verdicts
VERDICT researcher-1: accept
VERDICT researcher-2: revise
VERDICT researcher-3: accept
VERDICT researcher-4: accept
