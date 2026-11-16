# Puanlama ve çıkarım zinciri: hakem, doğrulama, doğruluk ölçütü, tekrarlar, istatistik

## Hypothesis
Birinci kısım genel haliyle **Refuted**, K0–K3 için **Undecided**: ölçüt bazlı ikili hakemlikte öz ve aile kayırması ölçülmüş, ama Claude hakemlerinin HealthBench oranları 1'in altında ve aynı üreticinin RAG'li/RAG'siz yanıtlarını karşılaştıran çalışma yok. İkinci kısım **Supported, kanıt zayıf-orta**: dayanak iki önbaskı (HealthBench, Lee ve ark.) ve TRIPOD-LLM'in puanlayıcı niteliği ile puanlayıcılar arası uyum maddeleri. Tek ikili κ'yı yeterli sayan kaynak bulmadım; κ istatistiği literatürünü açamadım.

## What is the measured size of same-family or self-preference bias when the judge grades against explicit rubric items or a reference, as opposed to pairwise preference, and does it differ by answer style?

### Takeaway
Yanlılık ölçüt bazlı hakemlikte de var, ama hakeme ve alana göre yön değiştiriyor: Claude hakemleri sağlıkta nötr ya da hafif ters yönde. Kanıt tek önbaskı; Opus hakemi ve atıflı RAG üslubu hiç ölçülmemiş.

### Cited findings
- Öz-kayırma oranı (>1 = kayırma), HealthBench: GPT-5 1,54; Claude Sonnet 0,93 [0,86–1,01]; Claude Haiku 0,90 [0,86–0,93] — [Pombal ve ark., 2026, önbaskı](https://arxiv.org/html/2604.06996)
- Aile oranı, HealthBench: Claude Sonnet 0,89 [0,84–0,95]; Claude Haiku 0,91 [0,88–0,94]; Gemma-4B 1,22; Llama hakemleri 0,72–0,78 — [Pombal ve ark., 2026](https://arxiv.org/html/2604.06996)
- Aynı Claude hakemleri LiveCodeBench'te kayırıyor: Sonnet öz 1,78, aile 1,62; Haiku öz 1,71, aile 1,70; GPT-5 öz 20,15, aile 11,91 — [Pombal ve ark., 2026](https://arxiv.org/html/2604.06996)
- Ölçülen büyüklük, gerçekte karşılanmamış ölçütün "karşılandı" işaretlenme sıklığıdır; özet, HealthBench'te model puanlarının 10 puana kadar kaydığını bildiriyor — [Pombal ve ark., 2026](https://arxiv.org/abs/2604.06996)
- En çok etkilenen temalar iletişim, küresel sağlık ve acil yönlendirme; negatif ölçütler daha duyarlı — [Pombal ve ark., 2026](https://arxiv.org/html/2604.06996)
- Beş hakemli çoğunluk yanlılığı azaltıyor, gidermiyor (LiveCodeBench, Claude Sonnet 1,78→1,29) — [Pombal ve ark., 2026](https://arxiv.org/html/2604.06996)
- HealthBench "doğrusu" insan değil, her aileden en büyük hakemin çoğunluk oyu; yazarlar bunun yanlılığı küçük gösterebileceğini belirtiyor. Opus hakem yok — [Pombal ve ark., 2026](https://arxiv.org/html/2604.06996)

### Inferences
- K0–K3 aynı üreticiyi kullandığından aile etkisi ilk yaklaşımda sabittir. "Çok hata yapan konfigürasyon daha çok şişer" kanıtlanmış mekanizma değil, **sınanacak varsayımdır**; Claude'un sağlık oranları (<1) ters yöne işaret ediyor.
- Yönden bağımsız sonuç (Lee formülünden cebirsel çıkarım, bkz. sonraki soru): hakem hatası konfigürasyonlar arasında aynıysa gözlenen fark gerçek farkın (q0+q1−1) katıdır. Bu H1–H3a için tutucu, H3b için anti-tutucudur. q0=q1=0,90 iken 6 puanlık gerçek fark 4,8 görünür.
- **Ekle (insan emeği gerektirmez):** farklı aileden ikinci hakemle tabakalı alt örneği yeniden puanlat; hipotez sonuçlarını iki hakemle ver. **Ekle:** hakem–klinisyen uyuşmazlığını konfigürasyona göre kır (varsayımın sınaması). **Değiştir:** "ilk iki cümlede acil yönlendirme" bayrağını konum kuralıyla hesapla, hakeme bırakma. **Sınırlılık:** K4–K3 hakem ailesiyle karışık.

### Gaps
- Atıflı RAG yanıtlarının aynı aile hakemince farklı puanlandığını ölçen çalışma bulamadım.
- Öz-kayırmanın kalite ve üslupla karıştığını savunan önbaskıyı ([arXiv 2608.18091](https://arxiv.org/abs/2608.18091)) açamadım.

## How do the strongest health benchmarks validate a model grader (unit of agreement, statistic, sample size, who the humans are), and how does this design compare?

### Takeaway
HealthBench ölçüt düzeyinde, hekimlerle, makro-F1 ile ve hekim–hekim uyumunu tavan alarak doğruluyor. Tasarımdaki "türetilmiş ikili etikette tek κ" bundan zayıf, eşikleri de bu örneklemle doğrulanamaz.

### Cited findings
- Doğrulama birimi tek ölçüt × tek yanıt × tek hekim yargısı; 34 konsensüs ölçütü, 60.896 yargı — [Arora ve ark., 2025, önbaskı](https://arxiv.org/html/2505.08775)
- İstatistik makro-F1; GPT-4.1 hakem 0,709. Tema bazında hekim ortalamaları 0,569 (yanıt derinliği) – 0,730 (sağlık verisi görevleri); acil yönlendirmede hekim 0,647, hakem 0,662 — [Arora ve ark., 2025](https://arxiv.org/html/2505.08775)
- Hakemin duyarlılığı (q1) ve özgüllüğü (q0) kusurluysa ham oran yanlıdır; düzeltme θ̂ = (p̂ + q̂0 − 1)/(q̂0 + q̂1 − 1). Çerçeve yalnız ikili etiket içindir; çok sınıflı uzantı gelecek iş — [Lee ve ark., v2, 2026, önbaskı](https://arxiv.org/html/2511.21140v2)
- Kalibrasyon büyüklüğü sürümler arasında çelişiyor. v2: 0,1'den kısa aralık için "m=m0+m1≈200", koşullar p̂=0,3, q0=0,7, q1=0,9, n→∞; simülasyon n=1000, toplam m=200 (m0=m1=100) — [Lee ve ark., v2](https://arxiv.org/html/2511.21140v2). v1: aynı örnek "m0=m1≈200" (≈400 etiket), simülasyon toplam 500 — [Lee ve ark., v1, 2025](https://arxiv.org/html/2511.21140v1)
- Hakem "yanlış" yanıtları tanımada zayıfsa kalibrasyon etiketleri o sınıfa ayrılmalı (Önerme 5.2) — [Lee ve ark., v2](https://arxiv.org/html/2511.21140v2)

### Inferences
- Hangi sürüm esas alınırsa alınsın 100 klinisyen etiketi 0,1 genişlikte aralık vermez: v2 rakamı sonsuz test kümesi varsayar, v1 ≈400 etiket ister. Tek öğrencilik tezde 200–400 klinisyen etiketi uygulanamaz. **Sınırlılık:** düzeltmeli oran yalnız geniş aralıklı duyarlılık analizi olabilir; birincil sonuç ham oran kalır.
- Düzeltme bileşik ölçüte madde düzeyinde uygulanamaz (ikili çerçeve). Tek yol q0 ve q1'i doğrudan türetilmiş CORRECT etiketinde kalibre etmektir: klinisyen kalibrasyon yanıtının tümünü puanlar.
- Kaba hesabım: n=100, yaygınlık %15, κ=0,60 için %95 GA ≈ ±0,23.
- "Güvensiz yanıtta duyarlılık ≥ 0,90" ~15 güvensiz örnekle gösterilemez (14/15 için Wilson alt sınırı ≈ 0,70). Alt sınırın 0,90 olması için sıfır kaçırmayla ≥35 güvensiz yanıt gerekir (benim hesabım).
- **Değiştir:** doğrulama birimi madde düzeyi (mevcut/yok/çelişik + her bayrak); ek etiket gerektirmez. **Ekle:** sınıf bazlı duyarlılık/özgüllük ve makro-F1; eşikleri nokta kestirimine değil GA alt sınırına bağla. **Değiştir:** 100 klinisyen yanıtını büyütmeden tabakala (≥35 güvensiz/acil; gerekirse bilerek bozulmuş yanıt ekle).
- researcher-3'ün ayrımını al: "doz verdi" bayrağı "bireysel doz/kesin tanı (güvensiz)" ve "genel güvenli tamamlama" olarak bölünsün; duyarlılık eşiği yalnız ilkine uygulansın.

### Gaps
- Gwet AC1 / κ paradoksu kaynaklarını ([Wongpakaran 2013](https://link.springer.com/article/10.1186/1471-2288-13-61), [Zec 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5712640)) ve κ örneklem formüllerini açmadım. "Yaygınlığa dayanıklı katsayı" önerisi bu yüzden kaynaksızdır; eklenirse κ ile birlikte raporlanmalı.

## Is a single non-clinician rater (the researcher) an accepted reference for judge validation, and what do reporting standards require about raters and blinding?

### Takeaway
Kabul gördüğünü gösteren kaynak yok. TRIPOD-LLM puanlayıcı niteliğinin ve puanlayıcılar arası uyumun raporlanmasını istiyor; tek puanlayıcıyla uyum raporlanamaz. Körleme şartını hiçbir standartta doğrulayamadım.

### Cited findings
- TRIPOD-LLM 7d: öznel sonuç değerlendirmesinde puanlayıcıların nitelikleri, verilen talimatlar, demografik bilgiler ve puanlayıcılar arası uyum bildirilir — [Gallifant ve ark., Nat Med 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12104976)
- TRIPOD-LLM 8b: veri kümesini kaç kişinin etiketlediği ve uyumları; 6a: model adı ve sürümü; 6c: çıkarım ayarları (seed, sıcaklık, azami token); 7c: kapalı modeller için çıkarım tarihi — [Gallifant ve ark., 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12104976)
- CHART, model tanımlayıcıları, istem geliştirme, sorgu stratejisi, referans standart ve değerlendirme süreci (7a–b) maddelerini içerir — [CHART, Ann Fam Med 2025](https://www.annfammed.org/content/23/5/389)
- HealthBench'te insan referansı hekimlerdir; hakem hekimlerin kendi aralarındaki uyuma göre konumlanır — [Arora ve ark., 2025](https://arxiv.org/html/2505.08775)

### Inferences
- "Geliştirici test maddelerini okumaz" kuralı 300 yanıtın etiketlenmesiyle çelişir; bu etiketler dev yanıtlarında yapılmalı.
- **Değiştir:** araştırmacının 300 etiketi "hakem istemi geliştirme / ön doğrulama" olarak adlandırılsın; iddiayı klinisyen doğrulaması taşısın. **Ekle:** 100 yanıtın ~30'u iki klinisyence etiketlensin (TRIPOD-LLM 7d; klinisyen–klinisyen uyumu tavan). Süre yetmezse **sınırlılık**. **Ekle:** TRIPOD-LLM ve CHART kontrol listeleri tez ekine.

### Gaps
- CHART 7bi'nin "değerlendiricilerin sayısı ve özellikleri" dediği yalnız arama özetinde; tablo sayfası 520, BMJ Medicine 403 verdi.
- Okuduğum TRIPOD-LLM bölümünde körleme ve koşu sayısı maddesi yoktu; MI-CLEAR-LLM'i açamadım.

## Is "all required items present and no critical error" a defensible primary correctness criterion compared with partial-credit rubric scores, and what does each choice do to power and to ceiling/floor effects?

### Takeaway
Savunulabilir, ama alanın referans ölçütü kısmi puan kullanıyor ve "hepsi ya da hiç" hakem hatasını madde sayısıyla katlıyor. Güç etkisi için doğrudan kaynak yok.

### Cited findings
- HealthBench'te her ölçüt ikilidir; puanlar (−10…+10) toplanıp azami puana bölünür, genel puan örnek ortalamasıdır ve [0,1]'e kırpılır — [Arora ve ark., 2025](https://arxiv.org/html/2505.08775)
- Soru içi varyansı azaltmak ve sürekli puan kullanmak aynı n ile saptanabilir etkiyi küçültür — [Miller, 2024, önbaskı](https://arxiv.org/html/2411.00640)

### Inferences
- Madde başına hakem doğruluğu 0,95 ise beş maddeli doğru bir yanıtın doğru sayılma olasılığı ≈ 0,77; ölçüt kontrol listesi uzunluğuyla karışır ve taban etkisi üretir.
- **Koru:** katı ölçüt birincil. **Ekle:** ikincil olarak madde kapsama oranı ve kritik hata oranı; madde sayısına göre tabakalı doğruluk. **Değiştir:** gerekli madde sayısına üst sınır (ör. ≤4); dev kümesinde K0/K1 taban-tavan kontrolü.

### Gaps
- Tıbbi SC ölçütlerinde ikili ve kısmi puanın gücünü karşılaştıran çalışma bulamadım; dev simülasyonu yanıtlar.

## With no temperature or seed control, are three repeats with majority and worst-case aggregation adequate, and how should run-to-run variance be reported?

### Takeaway
Üç tekrar varyansı azaltır, ama çoğunluk ve en kötü durum varyansı raporlamaz. Sıcaklık kontrolünün yokluğu tasarım kusuru değil, satıcı kısıtıdır ve belgelenmelidir.

### Cited findings
- Haiku 5.5'te `temperature`, `top_p`, `top_k` istekten çıkarılır; uyarlanabilir düşünme varsayılan olarak açıktır, yoğunluğu `effort` belirler — [Anthropic, Haiku 5.5 geçiş kılavuzu, 2026](https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide)
- K örnek soru içi varyansı K'ya böler; n=198, σ²=1/6 için K'yı 1'den 10'a çıkarmak saptanabilir etkiyi %13,2'den %7,5'e indirir. Sıcaklığı düşürmek önerilmez — [Miller, 2024](https://arxiv.org/html/2411.00640)
- HealthBench 16 koşu yapar ve güvenilirliği "worst-at-k" eğrisiyle verir; o3'ün worst-at-16 puanı genel puanından yaklaşık üçte bir düşük — [Arora ve ark., 2025](https://arxiv.org/html/2505.08775)

### Inferences
- Çoğunluk p→3p²−2p³ dönüşümüdür (0,70→0,78): farkları büyütür. En kötü durum p³'tür (0,95→0,86) ve yalnız k=3 için anlamlıdır.
- **Değiştir:** birincil kestirim koşu başına doğruluğun madde içi ortalaması; çoğunluk ikincil. **Koru:** güvenlikte en kötü durum, "worst-at-3" adıyla ve koşu başına güvensiz oranla birlikte. **Ekle:** madde bazında kararsızlık oranı; hakem için alt örnekte yeniden puanlama tutarlılığı; model kimliği, `effort` düzeyi, API sürümü ve sorgu tarihleri (TRIPOD-LLM 6a, 6c, 7c).

### Gaps
- Parametre gönderilince 400 döndüğü, varsayılan sıcaklığın 1,0 olduğu ve sıcaklık 0'ın özdeş çıktı güvence etmediği yalnız arama özetinde ([API 2026-10-21 geçiş sayfası](https://platform.claude.com/docs/en/api/migration-2026-10-21)); açmadım.

## Are exact McNemar with Holm, a 5-point non-inferiority margin on over-refusal and percentile bootstrap intervals appropriate here, and what do standards say a non-inferiority margin must be justified by?

### Takeaway
Eşli tasarım ve küme bootstrap doğru. Kesin koşullu McNemar gereksiz tutucu (tek ama kapsamlı simülasyon çalışması). 5 puanlık marj gerekçesiz ve muhtemelen güçsüz.

### Cited findings
- "Kesin koşullu McNemar testini hiçbir durumda önermiyoruz": ortalama tip I hata 0,0201 (nominal 0,05). Mid-p varyantı 9.595 senaryonun hiçbirinde nominal düzeyi aşmadı — [Fagerland ve ark., 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3716987/)
- İlişkili sorularda kümelenmiş standart hata naif olanın 3 katını aşabilir (DROP 3,05); karşılaştırmalar eşli farklarla yapılmalı — [Miller, 2024](https://arxiv.org/html/2411.00640)
- CONSORT eşdeğersizlik uzantısı 2b: hipotezler, eşdeğersizlik marjı ve seçiminin gerekçesiyle birlikte belirtilir. 7a açıklaması: marj "tercihen klinik temelde" gerekçelendirilir. 12a: tek ya da çift yönlü güven aralığı belirtilir; testler önceden belirlenmiş Δ ve α'ya bağlanır — [Piaggio ve ark., JAMA 2012](https://jamanetwork.com/journals/jama/fullarticle/1487502)

### Inferences
- **Değiştir:** kesin koşullu McNemar → mid-p. **Koru:** Holm (H1–H3a), sabit n, küme bootstrap. S-ADV kaynak maddeye, S-YAS aileye, tekrarlar maddeye kümelenmeli.
- H3b gücü (normal yaklaşım, benim hesabım): n=210, gerçek fark 0, tek yönlü α=0,025; uyumsuz çift oranı %10 ise ≈ 0,63, %5 ise ≈ 0,90.
- **Değiştir:** marjı sonuçlar görülmeden, klinisyen gerekçesiyle sabitle (ör. "kaç yanıtlanabilir sorudan birinin reddi kabul edilebilir"); tek yönlü %97,5 GA'yı önceden belirt. Hakem hatasının farkı sıfıra çektiğini marj tartışmasına yaz. **Ekle:** dev uyumsuzluk oranıyla H3b güç hesabı; güç yetmezse **sınırlılık**.

### Gaps
- EMA/FDA marj kılavuzları açılamadı (EMA 429).
- Eşli ikili eşdeğersizlik aralığı (Tango) ve yüzdelik bootstrap'ın uç oranlardaki kapsaması için kaynak açmadım.

## Beyond the assignment
- Haiku 5.5 güvenlik sınıflandırıcıları isteği `stop_reason: "refusal"` ile reddedebilir. K0–K3'ün ortak üreticisinde bu, aşırı-ret (H3b) ve T1–T5 ölçümüne karışır; ayrı günlüklenmeli — [Anthropic, 2026](https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide)
- HealthBench'te hakem istemi ayarında kullanılan model doğrulamada öne çıktı. Hakem istemi dev kümesinde dondurulmalı, doğrulama örneği ayarlamada kullanılmamalı — [Arora ve ark., 2025](https://arxiv.org/html/2505.08775)
- İş yükü önceliği (benim yargım). Klinisyen emeği gerektirmeyenler şimdi: madde düzeyi uyum, GA alt sınırı eşikleri, mid-p, koşu ortalaması, ikinci hakem, kontrol listeleri. Klinisyen emeğini büyütmeyen: 100 yanıtın tabakalanması. Ek emek isteyen tek öneri: ~30 çift etiket. 200–400 etiketli kalibrasyon önerilmez.

## Changes
- [must] "Raporlama literatürü istiyor" → hükümden çıkarıldı; kanıt iki önbaskı ve bu turda açılan TRIPOD-LLM 7d/8b ile sınırlandı.
- [must] Lee m=200 → düzeltildi, kısmen savunuldu: v2 toplam ≈200 (n→∞) diyor, hakemin "sınıf başına 200" rakamı v1'de; ikisi de aktarıldı. 100 etiketin yetmediği ve 200–400'ün uygulanamazlığı yazıldı.
- [should] Claude aile oranları, hekim aralığı 0,569–0,730, Fagerland ifadesi → üçü düzeltildi.
- [should] "K0 daha çok şişer" → sınanacak varsayım yapıldı; yerine hata eşitliği koşullu cebirsel zayıflama argümanı kondu.
- Missing, CONSORT → Piaggio 2012 açıldı (2b, 7a, 12a).
- Missing, bileşik ölçütte Lee → yalnız türetilmiş CORRECT etiketinde kalibrasyon; ikincil ve geniş aralıklı.
- Çelişki, doz/tanı bayrağı → bayrak ikiye bölündü, duyarlılık eşiği güvensiz sınıfa bağlandı.
- Klinisyen yükü → öneriler emek maliyetine göre sıralandı; örneklem büyütme önerilmedi.
