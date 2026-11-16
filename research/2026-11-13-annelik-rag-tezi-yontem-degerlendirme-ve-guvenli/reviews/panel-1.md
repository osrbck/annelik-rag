# Review

## Overall
İlk hakemin `researcher-2` için verdiği altı `[must]` maddesinin tamamı bu turda çözülmüş; `researcher-2` kaynaklarıyla uyumlu ve dürüst bir metne dönüşmüş. Buna karşılık ilk hakem `researcher-1`, `researcher-3` ve `researcher-4`'e erken `accept` vererek fazla hoşgörülü davranmış; bu üç araştırmacı notlarını hiç güncellemediği için ilk incelemedeki hatalar olduğu gibi duruyor. Üstelik ilk hakemin açamadığı NICE NG143 ve Lee ve ark. (2025) kaynaklarını açtığımda `researcher-1` ve `researcher-3`'te düzeltilmesi zorunlu (`[must]`) olgu ve kanıt hataları saptadım. Ayrıca ekip, tek bir yüksek lisans öğrencisinin 3 saatlik klinisyen bütçesiyle yapılamayacak kadar çok ek iş öneriyor.

## researcher-1
Solid: Pombal ve ark. (2026), Arora ve ark. (2025; 60.896 yargı, makro-F1 0,709), Miller (2024) ve ilk hakemin açamadığı Fagerland ve ark. (2013; 9.595 senaryo, ortalama tip I hata 0,0201) kaynaklarıyla doğrulandı; κ güven aralığı, Wilson alt sınırı ve H3b güç hesapları sağlam. CHART BMJ Medicine tam metnini ve `2608.18091` önbaskısını ben de yalnızca özet düzeyinde görebildim.
Problems:
1. [must] "İkinci kısım **Supported**: … raporlama literatürü sınıf bazlı duyarlılık/özgüllük istiyor" ve "simülasyonda m=200 yaklaşık 0,1 genişliğinde aralık veriyor" → İlk hakem bunu `[should]` sayarak fazla hoşgörülü davrandı: notların kendisi CHART, TRIPOD-LLM ve MI-CLEAR-LLM maddelerinin açılamadığını söylüyor; kanıt yalnızca iki önbaskıya dayanıyor. Ayrıca açtığım Lee ve ark. (`2511.21140`) kaynağında kalibrasyon örneklemi toplam 200 değil, sınıf başına `m0=200` ve `m1=200` (toplam 400 insan etiketi; `q0=0,7, q1=0,9, p=0,4, n=1000`). 100 klinisyen yanıtıyla bu aralık elde edilemez → Hipotezdeki "raporlama literatürü istiyor" iddiasını çıkarıp hükmü iki önbaskıyla sınırla; Lee ve ark.'nın `m0=200, m1=200` koşulunu düzelt ve tek öğrencilik tezde 400 kalibrasyon etiketinin uygulanabilirlik sınırını yaz.
2. [should] İlk incelemeden kalan üç düzeltme yapılmamış: Pombal'da Claude HealthBench aile oranı tabloda var (Sonnet 0,89; Haiku 0,91); Arora'da hekim tema ortalamaları 0,569–0,730 (0,646–0,730 değil); Fagerland için "kanıt güçlü, tek simülasyon çalışması" ifadesi kendi içinde çelişkili → Üçünü de düzelt.
3. [should] "çok hata yapan konfigürasyon (K0) daha çok şişer… H3b için anti-tutucu" → Pombal aynı üreticinin RAG konfigürasyonlarını karşılaştırmıyor ve Claude öz-kayırma oranı HealthBench'te 0,93 (<1) → Kanıtlanmış mekanizma gibi değil, test edilecek varsayım olarak yaz.
Missing: Eşdeğersizlik marjı (CONSORT non-inferiority) için birincil standart kaynağı ve bileşik doğruluk ölçütünde ("tüm zorunlu maddeler var") Lee düzeltmesinin nasıl uygulanacağı.

## researcher-2
Solid: İlk incelemedeki altı `[must]` maddesinin tamamı çözülmüş: (1) Teixeira de Lima (2024) ve Filice (2025) bulguları kategori dengesizliği ve çeşitlilik şartlandırmasına indirilip hipotez `Undecided` yapılmış; (2) Arora (2025) altındaki hatalı otomasyon yanlılığı atfı silinip doğruladığım Jabbour ve ark. (2023; -11,3 puan) ile Qazi ve ark. (2025; %84,9'dan %73,3'e, -14,0 puan) eklenmiş; (3) HealthBench süre iddiası kaldırılıp ~17,5 sn/madde hesabı "ekibin operasyonel yargısı" olarak işaretlenmiş; (4) `DoktorSitesi` için etik kurul ve KVKK şartı getirilmiş; (5) kaynaksız "20–200" aralığı ve Rosie hatası düzeltilip Peled (15 soru), DIAN (50 soru, 148 değerlendirici: 119 kadın, 29 klinisyen) ve alt küme güç kısıtları doğru yazılmış; (6) K-QA'da ayrıştırılan alt küme 201 soru olarak düzeltilmiş. İlk incelemedeki `[should]` 7 ve 8 de giderilmiş.
Problems:
1. [should] "otomasyon yanlılığına düştüğünü… göstermektedir (yüksek kanıt gücü)" ve "hekimlerin LLM taslağını görmeden önce kılavuz sayfasındaki zorunlu klinik kuralı işaretlemesini sağlayın; yüksek kanıt gücü" → İlk hakemin görmediği bağlam aktarımı sorunu: Jabbour (ABD yatan hasta vinyetleri) ve Qazi (Pakistan'da 44 hekim, 6 tanısal vinyet) hekimlerin yanlı AI öngörüsüyle klinik tanı koymasını ölçüyor; eldeki kılavuz PDF sayfasına bakarak rubrik maddesi onaylamayı değil → Kanıt gücünü rubrik doğrulaması için "orta (dolaylı kanıt)" olarak düşür.
2. [should] "S-ANA setinin 30 maddelik bir alt kümesi gerçek ebeveyn sorularıyla paralel test edilmelidir", "15–20 maddelik profilsiz/eksik bilgili ek bir stres testi ekleyin", "T1 acil madde sayısını artırın" ve "S-ADV'deki 80 çekişmeli yeniden yazımın… uzman kontrolü" → Tek bir yüksek lisans öğrencisi ve hekim başına 3 saatlik bütçe için bu eklerin tamamı aynı anda uygulanamaz → Toplam madde sayısını büyütmek yerine mevcut bütçe içinde ikame/alt-örnekleme önceliği ver.
Missing: LLM taslağı rubrik incelemesinde süreyi ve kaçırılan hata oranını doğrudan ölçen çalışma (boşluk olarak doğru belirtilmiş).

## researcher-3
Solid: Fraile Navarro ve ark. (2026), Bean ve ark. (2026; n=1.298, %94,9 / %56,3 / <%44,2), Hindistan anne sağlığı sistemi (`2603.13168`; N=150, %86,7 duyarlılık, 50 karakterlik olumsuzlama penceresi) ve Üç Kuralı hesapları kaynaklarla doğrulandı. `2603.13168` ek tablolarını ve MEDHARM tam metnini açamadım.
Problems:
1. [must] "NICE NG143'te ateşi olan çocuklarda solunum hızı eşikleri yaşa göre değişiyor: 0–5 ay için >60, 6–12 ay için >50, 12 aydan büyükler için >40/dk. Kırmızı sütunda şunlar var…" → İlk hakem sayfayı açamadığı için `[should]` diyerek fazla hoşgörülü davrandı; NICE NG143 Tablo 1'i açıp doğruladım: `>60/dk` yalnızca 0–5 ay için değil, **tüm yaşlarda** Kırmızı (yüksek risk) kriteridir; `>50/dk` (6–12 ay) ve `>40/dk` (>12 ay) ise Kırmızı değil **Sarı (orta risk)** sütunundadır. Ayrıca NG143'ün en temel yaşa özgü Kırmızı kriteri olan **<3 ay bebekte ≥38 °C ateş** atlanmış → Kırmızı ve Sarı sütun eşiklerini birincil tabloya göre düzelt, `<3 ay ≥38 °C` kuralını ekle.
2. [must] "Doz kısmı desteklendi: NHS'in ebeveynlere yönelik sayfası parasetamol dozunu yaşa göre ml olarak açıkça veriyor. Bu doz kilo değil yaş bantlarına bağlı, yani hipotezdeki 'kiloya göre' ifadesi düzeltilmeli" ve "Güvenim yüksek" → İlk hakemin kaçırdığı Türkiye birinci basamak aktarımı hatası: İngiltere'de pediatrik parasetamol süspansiyonu ulusal olarak standart `120 mg/5 ml` (ve 6+ yaş `250 mg/5 ml`) olduğu için NHS yaş bandına göre ml verir; Türkiye'de ise farklı konsantrasyonlar vardır, pediatrik antipiretik dozu kiloya göredir (10–15 mg/kg/doz) ve araştırmacının kendisi Bakanlık/TİTCK belgelerini hiç açmadığını (`Gaps`) kabul etmektedir. Türkçe bilgi bankası kontrol edilmeden İngiliz yaş bandı ml şemasından "Desteklendi / Güvenim yüksek" çıkmaz → Hükmü "genel güvenli tamamlama (maksimum sıklık, prospektüs/hekime yönlendirme, doz aşımı uyarısı) için desteklendi; Türkiye'de yaşa göre ml doz aktarımı için kararsız" olarak düzelt ve T3 önerisini Türkçe kılavuz metnine bağla.
3. [should] İlk incelemeden kalan düzeltmeler yapılmamış: "Benzer çalışmalar 150 civarı" yalnızca tek bir önbaskıya (`2603.13168`) dayanıyor; Fraile Navarro'daki klinisyen denetimi yalnız 24 amaçlı seçilmiş yanıt içeriyor (klinisyen iki hakemle yalnız 4/23'te uyuşuyor) ve %60 koşullu yönlendirme oranı anahtar sözcük sezgiseliyle hesaplanmış → Bunları açıkça belirt.
Missing: T.C. Sağlık Bakanlığı Bebek/Çocuk/Ergen İzlem Protokolleri ve Gebelik Rehberi içindeki yerel tehlike işaretleri ve doz ifadeleri.

## researcher-4
Solid: Liu ve ark. (2025; OR 1,35), Kim ve ark. (2025; 80.502 etiket, ilk 16 pasajda %22 ilgi), ilk hakemin açamadığı Vach ve ark. (2025; PMID 40892297, 384 soru, %20,0 vs %70,6, BM25 %82,0 vs bge-m3 %78,4) ve Hassan ve ark. (2026; 100 soru, Trendyol %75, Qwen2.5 %65, BM25 %65) kaynaklarla birebir doğrulandı.
Problems:
1. [should] İlk incelemedeki dört düzeltme (`accept` verildiği için) yapılmamış: (a) Türkçe erişimde "iki bağımsız çalışma"dan biri Almanca (Vach 2025), diğeri ise tıp değil 100 soruluk sanayi Ar-Ge raporları önbaskısı (Hassan 2026) olduğundan güven "orta"dan "düşük"e indirilmeli ve alan farkı yazılmalı; (b) Vach ve ark.'da %20,0 (GPT-4o-mini) ile %70,6'nın (Claude 3.5 Sonnet) farklı modeller olduğu Hipotez cümlesinde belirtilmeli; (c) "ilk 16 pasaj yerine… 3–5" önerisinde 16 tezin değil Kim'in kurulumudur; (d) H2'yi doğrudan düşürmek yerine karar dev pilotuna bağlanmalı.
2. [should] "**Ekle:** tablo ve akış şemalarını elle doğrulanmış yapılandırılmış metne çevir" → 700 sayfayı aşan Bakanlık kılavuzlarındaki tüm tabloları bir ayda tek öğrencinin elle dönüştürmesi uygulanabilir değil → Yalnızca S-ANA/S-YAS/S-TUZ ile eşleşen yüksek öncelikli yaş tablolarıyla (aşı takvimi, izlem şemaları, büyüme tabloları) sınırla.
Missing: AMAQA birincil makalesi ve TR-MTEB erişim alt tablosu.

## Contradictions between researchers
- **H2'nin statüsü:** `researcher-4` H2'yi hemen doğrulayıcı olmaktan çıkarıp birincil ölçütü erişim düzeyine çekiyor; `researcher-2` ise `family-consistent accuracy` ölçütünü koruyup H2'nin statüsünü 85 maddelik dev pilotundaki etki büyüklüğüne bağlıyor (`researcher-2` daha tutarlı).
- **Doz/tanı bayrağı ve hakem duyarlılığı:** `researcher-3` T2/T3'te "güvenli tamamlama" ile güvensiz bireysel doz/kesin tanıyı ayırıyor; `researcher-1`'in hakem doğrulaması (`duyarlılık ≥ 0,90`) bu ayrımı henüz içermiyor.
- **Klinisyen iş yükü ve gerçek veri:** `researcher-2` 3 saatin yetmeyeceğini gösterip yükü azaltmayı önerirken, dört araştırmacının önerdiği ek kontroller ve yeni maddeler toplam klinisyen yükünü katlıyor. Ayrıca `researcher-3` KVKK için yalnız sentetik maddede kalmayı önerirken `researcher-2` etik onaylı `DoktorSitesi` ve 30 gerçek soru testi öneriyor.

## What can be stated with confidence, and what cannot
Güvenle söylenebilir:
- Türetilmiş ikili etikette tek κ ve n=100 klinisyen örneğinde nokta duyarlılık eşiği (≥0,90) istatistiksel olarak yetersizdir.
- 3 saatte 615 madde (~17,5 sn/madde) incelemesi otomasyon yanlılığına açıktır.
- T1'de 40 madde (sıfır hatada üst sınır %7,5), S-YAS'ta 60 aile ve H3b (%5 marjda güç ≈ 0,63) düşük güçlüdür.
- Altın kontrol listelerinin kılavuzdan yazılması H1'de K1'i yapısal olarak kayırır; genel tıbbi sorularda gürültülü RAG doğruluğu düşürebilir.

Söylenemez:
- Sentetik soruların Türkçe ebeveyn sorularına kıyasla RAG doğruluğunu ne kadar şişirdiği.
- Yaş-duyarlı erişim filtresinin (K2) ve deterministik kural katmanının (K3) öncü model üzerindeki net nicel katkısı.
- İngiltere NHS yaş bandı ml doz şemasının Türkiye'deki kılavuz ve birinci basamak pratiğine doğrudan uygulanabilirliği.

## Verdicts
VERDICT researcher-1: revise
VERDICT researcher-2: accept
VERDICT researcher-3: revise
VERDICT researcher-4: accept
