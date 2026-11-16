# Puanlama ve çıkarım zinciri: hakem, doğrulama, doğruluk ölçütü, tekrarlar, istatistik

## Hypothesis
Birinci kısım **Refuted** (genel haliyle): ölçüt bazlı ikili hakemlikte de öz ve aile kayırması ölçülmüş, acil yönlendirme ölçütleri en duyarlılar arasında. Yine de Claude hakemi için HealthBench oranı ≈1 ve "atıflı RAG üslubu" etkileşimine dair doğrudan kanıt yok; K0–K3 için tehdit kanıtlanmış değil, dışlanamaz durumda. İkinci kısım **Supported**: en güçlü sağlık ölçütü ölçüt düzeyinde makro-F1 ile doğruluyor, raporlama literatürü sınıf bazlı duyarlılık/özgüllük istiyor; tek ikili κ'yı yeterli sayan kaynak bulmadım.

## What is the measured size of same-family or self-preference bias when the judge grades against explicit rubric items or a reference, as opposed to pairwise preference, and does it differ by answer style?

### Takeaway
Ölçüt bazlı hakemlikte yanlılık sürüyor ama hakeme ve göreve göre çok değişiyor; Claude hakemleri sağlık verisinde nötre yakın. Kanıt tek bir önbaskıya dayanıyor: orta-zayıf.

### Cited findings
- Ölçüt başına ikili karar veren hakemler, kendi çıktılarının karşılamadığı ölçütleri "karşılandı" saymaya %50'den fazla daha yatkın olabiliyor (özet); HealthBench'te model puanları 10 puana kadar kayıyor — [Pombal ve ark., 2026, önbaskı](https://arxiv.org/abs/2604.06996)
- Aynı çalışmada öz-kayırma oranı (>1 = kayırma): HealthBench'te GPT-5 1,54, Claude Sonnet 4.5 0,93; LiveCodeBench'te Claude Sonnet 1,78, Claude Haiku 1,71, GPT-5 20,15 — [Pombal ve ark., 2026](https://arxiv.org/html/2604.06996)
- Aile yanlılığı var ama tekdüze değil: LiveCodeBench'te GPT-5'in aile oranı 11,91; HealthBench'te Gemma-4B 1,22, Llama hakemleri 0,72–0,78 — [Pombal ve ark., 2026](https://arxiv.org/html/2604.06996)
- HealthBench'te en çok etkilenen temalar iletişim, küresel sağlık ve acil yönlendirme; negatif ("yapılırsa ceza") ölçütler pozitiflerden daha duyarlı — [Pombal ve ark., 2026](https://arxiv.org/html/2604.06996)
- Beş hakemli çoğunluk oyu yanlılığı azaltıyor ama gidermiyor (LiveCodeBench: Claude Sonnet 1,78→1,29) — [Pombal ve ark., 2026](https://arxiv.org/html/2604.06996)
- Bu çalışmanın HealthBench "doğrusu" insan değil hakem topluluğu; yazarlar bunun yanlılığı olduğundan küçük gösterebileceğini belirtiyor — [Pombal ve ark., 2026](https://arxiv.org/html/2604.06996)

### Inferences
- K0–K3 aynı üreticiyi kullandığı için aile yanlılığı ilk yaklaşımda sabittir. Ancak mekanizma "karşılanmamış ölçütü karşılandı saymak" olduğundan, çok hata yapan konfigürasyon (K0) daha çok şişer. Farklar sıkışır: H1–H3a için tutucu, H3b (eşdeğersizlik) için **anti-tutucu**.
- K4 (yerel, aile dışı) ile K3 karşılaştırması hakem ailesiyle karışıktır.
- **Ekle:** farklı aileden ikinci bir hakemle tüm yanıtları ya da tabakalı bir alt örneği yeniden puanlat; hipotez sonuçlarını iki hakemle ayrı ayrı ver (duyarlılık analizi). **Değiştir:** "ilk iki cümlede acil yönlendirme" bayrağını konum kuralı + insan denetimiyle kur, yalnız hakeme bırakma. **Sınırlılık:** K4–K3.

### Gaps
- Atıflı/kaynak gösteren RAG yanıtlarının aynı aile hakemince farklı puanlandığına dair çalışma bulamadım; kendi verinizde hakem–klinisyen uyuşmazlığını konfigürasyona göre kırarak yanıtlanır.
- Haiku yanıtlarını Opus'un puanladığı çift ve Claude'un HealthBench aile oranı okuduğum bölümde yoktu.
- Öz-kayırmanın kalite ve üslupla karıştığını savunan önbaskıyı ([arXiv 2608.18091](https://arxiv.org/abs/2608.18091)) açmadım; yalnız arama özeti.

## How do the strongest health benchmarks validate a model grader (unit of agreement, statistic, sample size, who the humans are), and how does this design compare?

### Takeaway
HealthBench ölçüt düzeyinde, hekimlerle, makro-F1 ile ve hekim–hekim uyumunu tavan alarak doğruluyor. Tasarımdaki "türetilmiş ikili etikette tek κ" bundan zayıf.

### Cited findings
- Doğrulama birimi (ölçüt, konuşma, yanıt, hekim notu) dörtlüsü; 34 konsensüs ölçütü, 60.896 hekim yargısı (ölçüt başına ortalama 1.791) — [Arora ve ark., 2025, önbaskı](https://arxiv.org/html/2505.08775)
- İstatistik makro-F1; gerekçe, birçok ölçütte "karşılanmadı" sınıfının seyrek olması — [Arora ve ark., 2025](https://arxiv.org/html/2505.08775)
- GPT-4.1 hakemin makro-F1'i 0,709 (rastgele 0,50); yedi temanın beşinde ortalama hekimi geçiyor; tema bazında hekim ortalamaları 0,646–0,730 — [Arora ve ark., 2025](https://arxiv.org/html/2505.08775)
- Hakem istemi GPT-4.1 ile ayarlandığı için üstünlüğün kısmen bundan kaynaklanabileceği yazarlarca not edilmiş — [Arora ve ark., 2025](https://arxiv.org/html/2505.08775)
- Hakemin duyarlılığı (q1) ve özgüllüğü (q0) kusurluysa ham puan yanlıdır; düzeltme θ̂ = (p̂ + q̂0 − 1)/(q̂0 + q̂1 − 1), güven aralığı test ve kalibrasyon belirsizliğini birlikte taşır — [Lee ve ark., 2025/2026, önbaskı](https://arxiv.org/html/2511.21140v2)
- Kalibrasyon örnekleri hakemin zayıf olduğu sınıfa daha çok ayrılmalı; simülasyonda m=200 yaklaşık 0,1 genişliğinde aralık veriyor — [Lee ve ark., 2025/2026](https://arxiv.org/html/2511.21140v2)

### Inferences
- Hekimler arası uyum bile ılımlıyken tek puanlayıcıya karşı κ ≥ 0,70 ya ulaşılmaz ya da puanlayıcının hakem istemine alışmış olmasını ölçer.
- Kaba yaklaşımla (benim hesabım): n=100, yaygınlık %15, κ=0,60 için %95 GA ≈ ±0,23; nokta kestirimine eşik koymak yetersiz.
- "Güvensiz yanıtta duyarlılık ≥ 0,90" 100 yanıtta ~15 güvensiz örnekle doğrulanamaz (14/15 için Wilson alt sınırı ≈ 0,70).
- **Değiştir:** doğrulama birimini madde düzeyine indir (mevcut/yok/çelişik + her bayrak). **Ekle:** sınıf bazlı duyarlılık/özgüllük, makro-F1 ve yaygınlığa dayanıklı bir katsayı; eşikleri GA alt sınırına bağla. **Değiştir:** klinisyen örneğini güvensiz ve acil yanıtlarla zenginleştir (tabakalı). **Ekle:** Lee ve ark. düzeltmeli oranları ikincil analiz olarak. **Koru:** konfigürasyona kör puanlama.

### Gaps
- Gwet AC1 / κ paradoksu kaynaklarını ([Wongpakaran 2013](https://link.springer.com/article/10.1186/1471-2288-13-61), [Zec 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5712640)) açmadım, yalnız arama özeti; karşı görüş (Vach ve Gerke 2023) da var. AC1'i tek başına değil κ ile birlikte raporlayın.
- κ için örneklem büyüklüğü formüllerine (Donner–Eliasziw, Sim–Wright) bakamadım.

## Is a single non-clinician rater (the researcher) an accepted reference for judge validation, and what do reporting standards require about raters and blinding?

### Takeaway
Kabul gördüğünü gösteren kaynak bulamadım; örnek uygulama hekim puanlayıcılardır. Standartların puanlayıcı ve körleme maddelerini doğrulayamadım: kanıt zayıf.

### Cited findings
- HealthBench'te insan referansı hekimlerdir ve hakem, hekimlerin birbirleriyle uyumuna göre konumlanır — [Arora ve ark., 2025](https://arxiv.org/html/2505.08775)
- CHART, sohbet robotu sağlık tavsiyesi çalışmaları için raporlama kılavuzudur; model tanımlayıcıları (3–4), istem geliştirme (5), sorgu stratejisi, tarih ve oturum sayısı (6), referans standardın açık tanımı ve değerlendirme süreci (7a–b), örneklem (8), veri analizi (9) maddelerini içerir — [CHART özeti, Ann Fam Med 2025](https://www.annfammed.org/content/23/5/389)

### Inferences
- Tasarım kendi içinde çelişiyor: "geliştirici test maddelerini okumaz" ama 300 yanıtı etiketleyecek. Bu etiketler dev kümesi yanıtlarında yapılmalı; test kümesinde referans yalnız klinisyenler olmalı.
- **Değiştir:** araştırmacının 300 etiketini "hakem istemi geliştirme / ön doğrulama" olarak adlandır; iddiayı taşıyan doğrulama, çift klinisyenli örtüşen alt örnek olsun (klinisyen–klinisyen uyumu tavan olarak raporlanır). **Ekle:** CHART kontrol listesi tez ekine. **Sınırlılık:** az sayıda klinisyen.

### Gaps
- CHART'ın tam madde metni (puanlayıcı sayısı, niteliği, körleme) okuduğum sayfada yoktu; BMJ Medicine sürümü 403 verdi.
- TRIPOD-LLM ve MI-CLEAR-LLM'i açamadım; EQUATOR'dan doğrulanmalı.

## Is "all required items present and no critical error" a defensible primary correctness criterion compared with partial-credit rubric scores, and what does each choice do to power and to ceiling/floor effects?

### Takeaway
Savunulabilir ama alanın referans ölçütü kısmi puan kullanıyor; "hepsi ya da hiç" hakem hatasını madde sayısıyla katlıyor. Güç etkisine dair doğrudan kaynak bulmadım (çıkarım).

### Cited findings
- HealthBench'te her ölçüt ikilidir, puanlar (−10…+10) toplanıp azami puana bölünür; genel puan örnek puanlarının ortalamasıdır ve [0,1]'e kırpılır — [Arora ve ark., 2025](https://arxiv.org/html/2505.08775)
- Soru içi varyansı azaltmak ve sürekli puan kullanmak aynı n ile saptanabilir etkiyi küçültür; güç formülü soru arası ve soru içi varyansa bağlıdır — [Miller, 2024](https://arxiv.org/html/2411.00640)

### Inferences
- Madde başına hakem doğruluğu 0,95 ise beş maddeli bir doğru yanıtın doğru sayılma olasılığı ≈ 0,77'dir; ölçüt, kontrol listesi uzunluğuyla karışır ve taban etkisi üretir.
- **Koru:** katı ölçüt birincil kalsın (klinik olarak yorumlanabilir, önceden kayıtlı). **Ekle:** ikincil sonuç olarak madde kapsama oranı (HealthBench tarzı) ve kritik hata oranı ayrı ayrı; madde sayısı dağılımı ve madde sayısına göre tabakalı doğruluk. **Değiştir:** gerekli madde sayısına üst sınır koy (ör. ≤4) ve dev kümesinde K0/K1 taban-tavan kontrolü yap.

### Gaps
- İkili ve kısmi puanlı sonuçların gücünü tıbbi SC ölçütlerinde doğrudan karşılaştıran çalışma bulamadım; dev kümesi simülasyonu yanıtlar.

## With no temperature or seed control, are three repeats with majority and worst-case aggregation adequate, and how should run-to-run variance be reported?

### Takeaway
Üç tekrar varyansı azaltmaya yeter, ama çoğunluk ve en kötü durum varyansı raporlamaz ve k'ya bağlı kestirimler üretir. Sıcaklık kontrolünün yokluğu kusur sayılmaz.

### Cited findings
- Ortalamanın varyansı (soru arası + soru içi)/n'dir; K örnek soru içi terimi K'ya böler; örnekte K=2 toplam varyansı 1/3, K=4 1/2 azaltır — [Miller, 2024](https://arxiv.org/html/2411.00640)
- n=198 ve σ²=1/6 ile K'yı 1'den 10'a çıkarmak saptanabilir etkiyi %13,2'den %7,5'e indirir — [Miller, 2024](https://arxiv.org/html/2411.00640)
- Varyansı azaltmak için sıcaklığı düşürmek önerilmez; yanlılık ekleyebilir — [Miller, 2024](https://arxiv.org/html/2411.00640)
- HealthBench 16 koşu yapar (SS ≈ 0,002; üretim ve puanlama birlikte) ve güvenilirliği "worst-at-k" eğrisiyle (k≤16) verir; o3'ün worst-at-16 puanı genel puanından yaklaşık üçte bir düşüktür — [Arora ve ark., 2025](https://arxiv.org/html/2505.08775)

### Inferences
- Çoğunluk p→3p²−2p³ dönüşümüdür (0,70→0,78): farkları büyütür ve "tek yanıt alan anne" kestirimi olmaktan çıkar. En kötü durum p³'tür (0,95→0,86) ve yalnız k=3 için anlamlıdır.
- **Değiştir:** birincil kestirim koşu başına doğruluğun madde içi ortalaması olsun; çoğunluk ikincil. **Koru:** güvenlikte en kötü durum, ama "worst-at-3" diye adlandır ve koşu başına güvensiz oranla birlikte ver. **Ekle:** madde bazında kararsızlık (flip) oranı, soru içi/soru arası varyans ayrışımı; hakemin kendisi için alt örnekte yeniden puanlama tutarlılığı; model kimliği ve sorgu tarihleri.

### Gaps
- Anthropic'in belirlenimsizlik ve sıcaklık parametresi belgelerini birincil kaynaktan doğrulayamadım. Üçüncü taraf sayfalar çelişiyor: [OpenRouter](https://openrouter.ai/docs/cookbook/evaluate-and-optimize/model-migrations/sonnet-5) parametrenin sessizce yok sayıldığını, [bir blog](https://www.digitalapplied.com/blog/which-ai-models-still-accept-temperature) 400 hatası döndüğünü yazıyor. platform.claude.com'dan teyit edilmeli.

## Are exact McNemar with Holm, a 5-point non-inferiority margin on over-refusal and percentile bootstrap intervals appropriate here, and what do standards say a non-inferiority margin must be justified by?

### Takeaway
Eşli tasarım ve küme bootstrap doğru. Kesin koşullu McNemar gereksiz tutucu (kanıt güçlü, tek simülasyon çalışması). 5 puanlık marj gerekçesiz ve muhtemelen güçsüz.

### Cited findings
- "Kesin koşullu McNemar testini hiçbir durumda önermiyoruz"; ortalama tip I hata 0,0201 (nominal 0,05); N=65–100'de senaryoların %72'sinde %3'ün altında — [Fagerland ve ark., 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3716987/)
- Mid-p varyantı 9.595 senaryonun hiçbirinde nominal düzeyi aşmadı; %80 güç için Δ=0,15'te ≈103'e karşı 113, Δ=0,25'te ≈42'ye karşı 49 çift (yazarlar tabloyu örneklem hesabı için önermiyor) — [Fagerland ve ark., 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3716987/)
- İlişkili sorularda kümelenmiş standart hata naif olanın 3 katını aşabilir (DROP 3,05; MGSM 1,88); karşılaştırmalar eşli farklarla yapılmalı — [Miller, 2024](https://arxiv.org/html/2411.00640)

### Inferences
- **Değiştir:** kesin koşullu McNemar → mid-p McNemar; Holm üzerine binen tutuculuk azalır. **Koru:** Holm (H1–H3a), sabit n, eşli/küme bootstrap. S-ADV yeniden yazımları kaynak maddeye, S-YAS aileye, üç tekrar maddeye kümelenmeli.
- H3b gücü (normal yaklaşım, benim hesabım): n=210, gerçek fark 0, tek yönlü α=0,025. Uyumsuz çift oranı %10 ise güç ≈ 0,63; %5 ise ≈ 0,90. **Ekle:** dev kümesinden uyumsuzluk oranıyla H3b güç hesabı. **Değiştir:** marjı klinisyenlerle, bulgular görülmeden, gerekçesiyle sabitle; eşli oran farkı için uygun güven aralığını önceden belirt; hakemin aşırı-ret etiketindeki hatasını marj tartışmasına kat. Güç yetmezse **sınırlılık**.

### Gaps
- CONSORT eşdeğersizlik uzantısının (Piaggio 2012) marj maddesini açmadım. Arama özetine göre marj klinik temelde belirtilip gerekçelendirilmeli ve denemelerin yalnız dörtte biri ile yarısı arasında gerekçe veriliyor ([EQUATOR kaydı](https://www.equator-network.org/?p=7626)). Tam metin ve FDA/EMA kılavuzu teyit edilmeli.
- Eşli ikili eşdeğersizlik testi (Tango skor aralığı) ve yüzdelik/BCa bootstrap'ın uç oranlardaki kapsaması için kaynak açamadım; hatırladığım kadarıyla yüzdelik bootstrap 0/1'e yakın oranlarda zayıftır, doğrulanmalı.

## Beyond the assignment
- HealthBench'te hakem istemi ayarında kullanılan modelin doğrulamada öne çıkması, sizde de riskin işaretidir: hakem istemi dev kümesinde dondurulmalı, doğrulama örneği ayarlamada hiç kullanılmamalı — [Arora ve ark., 2025](https://arxiv.org/html/2505.08775)
- Lee ve ark. düzeltmesi, hakemin karışıklık matrisi kümeler arasında kararlıysa dağılım kaymasında geçerli kalır. Dev'de ölçülen hakem hatasını teste taşımak bu varsayıma dayanır ve konfigürasyon bazında sınanmalıdır — [Lee ve ark., 2025/2026](https://arxiv.org/html/2511.21140v2)
