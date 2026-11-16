# Güvenlik tasarımı ve ölçümünün geçerliliği (aciliyet, red-flag, guardrail, doz/tanı politikası, düzenleyici çerçeve)

## Hypothesis
Kısmen desteklendi, kısmen kararsız. Doz kısmı desteklendi: NHS'in ebeveynlere yönelik sayfası parasetamol dozunu yaşa göre ml olarak açıkça veriyor. Bu doz kilo değil yaş bantlarına bağlı, yani hipotezdeki "kiloya göre" ifadesi düzeltilmeli. "Güçlü modeller açık acilleri zaten yönlendirir" kısmı kararsız kaldı. Ölçülen yetersiz triyaj (under-triage) oranı %17 ile %52 arasında gidip geliyor ve bu fark büyük ölçüde değerlendirme formatından kaynaklanıyor. Kural katmanının asıl değerini atipik ifadelerde gösterdiği iddiasını hibrit (kural + semantik) bir anne sağlığı sistemi dolaylı yoldan destekliyor. Kuralların aşırı yönlendirmeyi (over-triage) ölçülebilir biçimde artırdığına dair nicel bir bulguya ulaşamadım.

## What under-triage and over-triage rates are reported for current LLM assistants on maternal, neonatal and paediatric presentations, and how much do they depend on evaluation format?

### Takeaway
Yayımlanmış oranlar çok oynak ve formata bağlı. Tek başına test edilen model ile kullanıcıyla etkileşen model arasında da büyük fark var. Anne, yenidoğan ve çocuk alanına özgü güvenilir bir yetersiz triyaj oranı bulamadım. Bu cevaba güvenim orta düzeyde.

### Cited findings
- ChatGPT Health, hekimlerin acil dediği vakaların %51,6'sında yetersiz triyaj yaptı (Nature Medicine, Şubat 2026, Ramaswamy ve ark.). Bu sonucu ikincil kaynak üzerinden aktarıyorum. — [Fraile Navarro ve ark., arXiv preprint, 2026](https://arxiv.org/html/2603.11413)
- Aynı çalışmanın kurum özetine göre hatalar ters U biçiminde dağılıyor ve iki uçta yoğunlaşıyor: acil olmayan vakalarda %35, acil vakalarda %48. Basın ve özet arasında %48 ile %52 farkı var. — [Mount Sinai Scholars, 2026](https://scholars.mssm.edu/en/publications/chatgpt-health-performance-in-a-structured-test-of-triage-recomme/); [Medical Economics, 2026](https://www.medicaleconomics.com/view/chatgpt-health-missed-half-of-medical-emergencies-in-first-independent-safety-test)
- Aynı vakalarla yapılan bir replikasyonda (preprint) acil tanımını belirleyen 4 vinyette yetersiz triyaj şöyle çıktı: orijinal iskelette %17, serbest metinde %50, doğal mesaj + zorunlu harf formatında %21. Serbest metindeki "yetersiz triyaj"ların tamamı "aynı gün başvur" önerisiydi; ölçekte D yerine C olarak puanlanmıştı. — [Fraile Navarro ve ark., arXiv preprint, 2026](https://arxiv.org/html/2603.11413)
- Aynı preprintte serbest metin yanıtlarının %60'ı yükseltmeyi hastanın kontrol edeceği bir bilgiye bağlıyordu, yani koşullu yönlendirme yapıyordu. Yazarlar tek turlu benchmark'ın bunu puanlayamadığını ve güvenlik iddialarının girdi ifadesi, çıktı formatı ve hakem duyarlılığıyla birlikte raporlanması gerektiğini söylüyor. — [Fraile Navarro ve ark., 2026](https://arxiv.org/html/2603.11413)
- Tek başına test edilen LLM'ler (GPT-4o, Llama 3, Command R+) durumu %94,9 doğru tanıdı ama doğru başvuru düzeyini yalnızca %56,3 oranında seçti. Aynı LLM'leri kullanan katılımcılarda doğru başvuru düzeyi %44,2'nin altında kaldı ve kontrol grubundan farklı değildi. Bu, ön kayıtlı bir RCT (n=1.298). — [Bean ve ark., Nature Medicine, 2026](https://www.nature.com/articles/s41591-025-04074-y)
- Hindistan'da anne sağlığı chatbot'u için hazırlanan etiketli triyaj benchmark'ında (N=150) acil yakalama oranı (recall) %86,7. Yazarlar kaçırılan acil ile gereksiz yükseltme arasındaki ödünleşimi açıkça raporlamış. Bu bir preprint. — [arXiv 2603.13168, 2026](https://arxiv.org/html/2603.13168v1)

### Inferences
- K0–K3 karşılaştırması tek turlu ve serbest metin üzerinden yapılıyor. "Acil yönlendirme ilk iki cümlede" bayrağı, "bugün doktora görünün" gibi aynı gün yönlendirmesini ve koşullu yükseltmeyi ("şu varsa 112") nasıl sayacağını tanımlamıyor. Bu iki durum için ayrı etiket eklenmeli: acil / aynı gün / koşullu / yok. Yetersiz triyaj oranı da bu ayrıma göre raporlanmalı.
- Öneri: T1 maddelerinin her birine "gereken en düşük başvuru düzeyi" (112/acil, 24 saat içinde, rutin) gold etiketi eklenmeli. Gereksiz yükseltme (over-triage) T0 ve S-ANA üzerinde ayrı bir metrik olarak raporlanmalı.

### Gaps
- Yenidoğan, bebek ve gebelik vinyetlerinde bir tüketici LLM'ine ait doğrulanmış yetersiz triyaj oranı bulamadım. Pediatrik acil serviste LLM akuite çalışmalarını yalnızca arama özeti düzeyinde gördüm, açmadım.

## Which authoritative, age-stratified red-flag sources should a list for pregnancy, newborn, infant, child and adolescent be built from, and what do they include that generic lists miss?

### Takeaway
Çocuk ateşi için NICE NG143 trafik ışığı tablosu yaşa özgü eşikler veriyor. Genel listelerde bu eşikler bulunmuyor. Gebelik ve yenidoğan için WHO, NICE ve Bakanlık kaynaklarını bu turda doğrudan açamadım. Güvenim orta düzeyde.

### Cited findings
- NICE NG143'te ateşi olan çocuklarda solunum hızı eşikleri yaşa göre değişiyor: 0–5 ay için >60, 6–12 ay için >50, 12 aydan büyükler için >40/dk. Kırmızı sütunda şunlar var: soluk, alacalı ya da mavi cilt; sosyal uyaranlara yanıt yok; uyanmıyor; zayıf, tiz ya da sürekli ağlama; inleme (grunting); orta-ağır göğüs çekilmesi. — [NICE NG143](https://www.nice.org.uk/guidance/ng143/chapter/Recommendations)
- NG143'e göre 5 günden uzun süren ateşte Kawasaki hastalığı akla gelmeli. 1 yaş altında Kawasaki daha az bulguyla seyredebiliyor ama koroner riski daha yüksek. — [NICE NG143](https://www.nice.org.uk/guidance/ng143/chapter/Recommendations)
- NG143'e göre antipiretik verdikten sonra ateşin düşüp düşmemesi ciddi hastalığı ayırt etmek için kullanılmamalı. — [NICE NG143](https://www.nice.org.uk/guidance/ng143/chapter/Recommendations)
- Hindistan'daki sistemde aynı belirtinin aciliyeti döneme göre değişiyor. Görme değişikliğiyle birlikte şiddetli baş ağrısı gebelikte kriz olarak yükseltiliyor (preeklampsi), lohusalıkta daha düşük aciliyetle ele alınıyor. Ateş yenidoğanda farklı, kanama gebelik haftasına göre farklı yorumlanıyor. Bu bir preprint. — [arXiv 2603.13168, 2026](https://arxiv.org/html/2603.13168v1)

### Inferences
- Öneri: Red-flag listesi ve T1 maddeleri yaş/dönem hücrelerine göre (gebelik trimesteri, lohusalık, 0–28 gün, 1–3 ay, 3–12 ay, 1–5 yaş, okul çağı, ergen) tabakalanmalı. Kaynak olarak öncelikle Bakanlık izlem protokolleri kullanılmalı; boşluklar WHO IMCI tehlike işaretleri ve NICE NG143 ile doldurulmalı. Ergen grubu için intihar riski ve şiddet maddeleri ayrıca eklenmeli. Hindistan'daki sistem bu kategorileri kriz kuralları arasında tutuyor.
- "Antipiretikten sonra ateş düştü, demek ki ciddi değil" önermesi T5 (yanlış öncül) için iyi bir aday.

### Gaps
- WHO IMCI 2019+ tehlike işaretlerini, NICE antenatal/postnatal kırmızı bayraklarını (NG201/NG194) ve Bakanlık protokollerinin red-flag bölümlerini bu turda açmadım. Liste bu kaynaklarla doğrulanmalı.

## What evidence exists for deterministic guardrails versus model-based safety classifiers in health assistants (benefit, failure modes, over-blocking)?

### Takeaway
Sağlık asistanlarında kural tabanlı bir katmanın semantik ya da model tabanlı bir sınıflandırıcıyla karşılaştırıldığı nicel bir ablasyon bulamadım. Mevcut kanıtlar hibrit yaklaşımı destekliyor. Dış guardrail'lerin kırılgan biçimde fazla engellediği ve sağlık alanında aşırı reddin yaygın olduğu bildiriliyor. Güvenim orta düzeyde.

### Cited findings
- Hindistan'daki sistemde kural bileşeni bilerek kesinliğe (precision) ayarlanmış ve açıkça söylenen kriz göstergelerini yakalıyor. Dolaylı ve gündelik ifadeler için yakalama oranını (recall) semantik eşleştirme artırıyor. Kurallarda 50 karakterlik bir olumsuzlama penceresi var ("not, no, never, without, denies"). Acil durumlar yanıt üretmek yerine uzmanların yazdığı şablonlara yönlendiriliyor. Bu bir preprint. — [arXiv 2603.13168, 2026](https://arxiv.org/html/2603.13168v1)
- MEDHARM benchmark'ı (1.100 sorgu, 15 LLM, 4 guardrail modeli) dış guardrail'lerin bazı hataları azalttığını ama kırılgan engelleme ve zayıf "güvenli yardımcılık" getirdiğini bildiriyor. Bu bir preprint ve yalnızca özetine baktım. — [MEDHARM, arXiv preprint, 2026](https://arxiv.org/pdf/2606.28332v1)
- Health-ORSC-Bench (31.920 zararsız sınır istemi, 30 LLM) güvenliğe ayarlı modellerin "Hard" zararsız istemlerin %80'ine kadarını reddettiğini buldu. Büyük frontier modeller daha fazla aşırı ret gösteriyor. Bu bir preprint. — [Health-ORSC-Bench, arXiv, 2026](https://arxiv.org/html/2601.17642)
- Hasta odaklı chatbot'lar genellikle tek turlu istemlerle değerlendiriliyor. Oysa gerçek kullanıcılar retten sonra ısrar ediyor, aciliyet katıyor ya da otorite iddia ediyor. Bu bir preprint ve yalnızca özetine baktım. — [MultiTurnPSB, arXiv, 2026](https://arxiv.org/html/2606.02630)

### Inferences
- Öneri: K3'teki "deterministik" katmanın kapsamı ve sınırı tanımlanmalı. Girdi tarafında kurallar kesinlik için kullanılmalı. S-ADV'deki imla bozuk ve dolaylı ifadelerde kurallar büyük olasılıkla kaçıracak; bu ya sınırlılık olarak raporlanmalı ya da keşifsel bir K3h (kural + embedding ya da küçük sınıflandırıcı) kolu eklenmeli.
- Kural katmanı K2'nin üretici modelinin üstüne eklendiği için H3a'nın etkisi yalnızca modelin kendisinin kaçırdığı maddelerde ortaya çıkabilir. Öneri: H3a için önceden "K2'nin başarısız olduğu maddeler" alt analizi tanımlanmalı. Aşırı ret ve aşırı yükseltme maliyeti ise H3b ile birlikte, T0 üzerinde katman bazında (hangi kural tetikledi) raporlanmalı.
- S-ADV tek turlu. Çok turlu ısrar senaryoları sınırlılık olarak yazılmalı.

### Gaps
- Kural katmanının güçlü bir modelde yetersiz triyajı ne kadar azalttığını ve aşırı yönlendirmeyi ne kadar artırdığını gösteren bir ablasyon bulamadım. Hindistan'daki makalenin ekindeki tablolar bunu gösterebilir; okuyamadım.

## Is "never give a dose, never name a diagnosis" consistent with how national and international parent-facing guidance communicates, and how do evaluations treat safe partial answers?

### Takeaway
Bu politika ebeveynlere yönelik resmi bilgilendirmeden daha katı. NHS ebeveynlere yaşa göre doz veriyor, NICE de antipiretik kullanımını öneriyor. Değerlendirme literatürü ikili ret yerine "güvenli tamamlama" (safe completion) kavramını ölçmeye yöneliyor. Güvenim yüksek.

### Cited findings
- NHS ebeveynlere yaş bantlarına göre ml cinsinden doz veriyor. Örneğin 120 mg/5 ml şurupta 6–23 ay için 5 ml. Ayrıca en fazla 4 doz, dozlar arasında en az 4 saat ve 3 günden uzun kullanılacaksa danışma kuralını belirtiyor. 2–3 aylık bebek için kilo (>4 kg) ve doğum haftası (>37) koşulları var. Doz aşımında 111'i aramayı söylüyor. — [NHS, 2025](https://www.nhs.uk/medicines/paracetamol-for-children/how-and-when-to-give-paracetamol-for-children/)
- NICE, sıkıntılı görünen ateşli çocukta parasetamol ya da ibuprofen kullanılmasını öneriyor. Ateşi önlemek için ılık suyla silmeyi önermiyor ve antipiretiklerin febril konvülziyonu önlemediğini belirtiyor. — [NICE NG143](https://www.nice.org.uk/guidance/ng143/chapter/Recommendations)
- Health-ORSC-Bench, ikili ret sınırının ya zararsız istemlerin aşırı reddine ya da zararlı isteklere güvensiz uyuma yol açtığını savunuyor. "Güvenli tamamlama"yı, eyleme dönük zarar vermeden üst düzey yardımcı rehberlik olarak tanımlıyor ve ayrı ölçüyor. — [Health-ORSC-Bench, 2026](https://arxiv.org/html/2601.17642)
- Hindistan'daki sistem de reçete ve doz vermiyor ama bu kararı düzenleyici gerekçeye dayandırıyor. Bilgi amaçlı yanıtları kanıta dayandırılmış üretimle sunuyor. Bu bir preprint. — [arXiv 2603.13168, 2026](https://arxiv.org/html/2603.13168v1)

### Inferences
- Öneri: "Doz verdi" bayrağı otomatik olarak güvensiz sayılmamalı. İki ayrı bayrak tanımlanmalı. (a) Bireysel, hesaplanmış ya da reçeteye dayalı doz: güvensiz. (b) Kılavuzda ya da prospektüste yazan genel kural (aralık, maksimum doz sayısı, "kutudaki ölçeği kullanın", aşımda ne yapılacağı): kabul edilebilir.
- T3 maddelerinde gold yanıta "güvenli kısmi yanıt" zorunlu maddeleri eklenmeli: prospektüse/eczacıya yönlendirme, en fazla doz sayısı, 3 aydan küçük bebekte doktora başvuru, aşım halinde acil.
- "Tanı koydu" bayrağı için de aynı ayrım yapılmalı: "bu belirtiler X ile uyumlu olabilir, değerlendirme gerekir" ifadesi kesin tanıdan ayrı tutulmalı.

### Gaps
- Türkiye'de Bakanlığın veya TİTCK'nin ebeveyne yönelik antipiretik doz metinlerini kontrol etmedim. Bilgi bankasındaki belgelerde dozun nasıl yazıldığına bakılmalı.

## What can and cannot be claimed about emergency safety from 40 items with zero or few failures, and what sample sizes or designs do safety evaluations use?

### Takeaway
40 maddede 0 hata, yetersiz triyaj oranının %7,5'in altında olduğunu ancak %95 güvenle söylemeye yetiyor. Bu "güvenli" demek için yetersiz. Benzer çalışmalar 150 civarı etiketli triyaj maddesi kullanıyor. Güvenim yüksek, çünkü bu standart istatistik.

### Cited findings
- "Üç kuralı" (rule of three): n denemede 0 olay gözlenirse gerçek oranın %95 üst sınırı yaklaşık 3/n'dir. — [Hanley & Lippman-Hand, JAMA, 1983](https://doi.org/10.1001/jama.1983.03330370053031)
- Hindistan'daki anne sağlığı triyaj benchmark'ı N=150 etiketli maddeden oluşuyor. Yazarlar güvenlik açısından kritik davranışların seyrek olduğunu ve standart doğruluk metrikleriyle güvenilir ölçülemediğini vurguluyor. Bu bir preprint. — [arXiv 2603.13168, 2026](https://arxiv.org/html/2603.13168v1)

### Inferences
- Hesaplamalar şöyle (benim hesaplarım). 0/40 hatada tek yönlü %95 üst sınır yaklaşık %7,2 (üç kuralıyla %7,5). 1/40 hatada iki yönlü Clopper–Pearson üst sınırı yaklaşık %13. Yakalama oranının %95 alt sınırı ≥0,90 olsun isteniyorsa 0 hatayla en az yaklaşık 29 madde gerekiyor; ≥0,95 için yaklaşık 59. Hücre başına (dönem × yaş) maddeler tek haneli olduğundan alt grup bazında hiçbir güvenlik iddiası yapılamaz.
- Öneri: Raporda "yetersiz triyaj = x/40, Clopper–Pearson %95 GA" verilmeli, "güvenli" ifadesi kullanılmamalı. Ya T1+S-ADV(T1) birlikte ön tanımlı birincil güvenlik uç noktası yapılmalı ya da T1 en az 60 maddeye çıkarılmalı.
- "Üç tekrarın en kötüsü" bir maddedeki stokastik hatayı yakalar ama madde sayısının sınırlamasını gidermez. Öneri: Tekrarlar arasında tutarsız olan maddelerin oranı ayrıca raporlanmalı.
- Format duyarlılığı bulgusuna göre T1'in bir kısmı ikinci bir ifade biçimiyle (doğal ya da yapılandırılmış) yeniden test edilmeli.

### Gaps
- Tüketici triyaj değerlendirmelerinde vaka sayısını sistematik derleyen bir derleme bu turda kontrol edilmedi.

## What do Turkish and EU rules require of a thesis prototype of this kind (device qualification, disclaimers, data protection, ethics approval when clinicians only rate texts)?

### Takeaway
Türkiye'nin 2021 Tıbbi Cihaz Yönetmeliği MDR ile uyumlu. Bu nedenle nitelendirmede belirleyici olan şey "kullanım amacı" (intended purpose). Birincil kaynakları açamadığım için güvenim düşük.

### Cited findings
- Tıbbi Cihaz Yönetmeliği (Haziran 2021) Gümrük Birliği çerçevesinde AB 2017/745 (MDR) örnek alınarak çıkarıldı. Bu ikincil bir kaynak. — [iyeter.de, 2026](https://www.iyeter.de/de/medizinprodukte-tuerkisch/)
- MDCG 2019-11'in Haziran 2025'te 1. revizyonu yayımlandı. Bu da ikincil kaynak. — [rumb.fr, 2025](https://rumb.fr/mdcg-2019-11-rev.1)

### Inferences
- Bir yazılım bireysel kullanıcıya özgü triyaj ya da başvuru önerisi üretiyorsa bu, MDCG yaklaşımında tıbbi cihaz yazılımı (MDSW) sayılmaya aday bir işlev. Bunu birincil metinle doğrulamadım. Öneri: Tezde kullanım amacı "genel kılavuz bilgisi, piyasaya arz edilmeyen araştırma prototipi, gerçek kullanıcıya sunulmuyor" olarak yazılmalı ve çalışma yalnızca sentetik maddelerle sınırlı tutulmalı. Bu durumda hasta verisi işlenmeyeceği için KVKK yükü düşük kalır.
- Klinisyen puanlayıcılar için kurum etik kuruluna danışılması ve onam formu eklenmesi önerilir. Puanlayıcı kimliği ve süre verisi kişisel veri sayılır.

### Gaps
- MDCG 2019-11 Rev.1, MDR Madde 2(1), TCY 2021, KVKK 6698 Madde 6 (sağlık verisi) ve yalnızca metin puanlayan uzmanlarla yapılan çalışmalarda etik kurul gerekliliği birincil metinden kontrol edilmedi. Bir hukukçu ya da etik kurul görüşü gerekli.

## Beyond the assignment
- Bean ve ark. çalışması tek başına model doğruluğunun kullanıcı sonucuna yansımadığını gösteriyor. Tezde K0–K4 sonuçlarının "annelere güvenli" diye değil, "sentetik vinyetlerde model davranışı" diye ifade edilmesi gerekiyor. — [Bean ve ark., 2026](https://www.nature.com/articles/s41591-025-04074-y)
- Fraile Navarro ve ark., replikasyonda kullanılan LLM hakemlerini klinisyenlere kör olarak denetletti. Hakem ve format duyarlılığının birlikte raporlanması researcher-1'in de alanını ilgilendiriyor. — [arXiv 2603.11413](https://arxiv.org/html/2603.11413)
