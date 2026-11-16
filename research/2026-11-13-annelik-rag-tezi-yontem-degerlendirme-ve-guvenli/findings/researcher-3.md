# Güvenlik tasarımı ve ölçümünün geçerliliği (aciliyet, red-flag, guardrail, doz/tanı politikası, düzenleyici çerçeve)

## Hypothesis
Kısmen desteklendi, kısmen kararsız. Doz politikasının fazla katı olduğu kısmı desteklendi, ama yalnızca genel güvenli tamamlama için. Ebeveynlere yönelik resmi kaynaklar dozu saklamıyor: NHS dozu yaş bandına göre ml olarak, ABD'deki MedlinePlus ise kilo bandına göre ml olarak veriyor. Türkiye'de ebeveynlere doz ml olarak verilebilir mi, sorusu kararsız kaldı, çünkü Bakanlık ve TİTCK metinlerini açamadım. "Güçlü modeller açık acilleri zaten yönlendirir" kısmı da kararsız. Ölçülen yetersiz triyaj aynı vakalarda format değişince %17 ile %50 arasında oynuyor. Kuralların gereksiz yükseltmeyi (over-triage) ne kadar artırdığını gösteren nicel bir bulgu bulamadım.

## What under-triage and over-triage rates are reported for current LLM assistants on maternal, neonatal and paediatric presentations, and how much do they depend on evaluation format?

### Takeaway
Yayımlanmış oranlar büyük ölçüde değerlendirme formatına bağlı. Model tek başına test edildiğinde aldığı sonuç, kullanıcıyla birlikte aldığı sonuçla da örtüşmüyor. Anne, yenidoğan ve çocuk alanına özgü sağlam bir yetersiz triyaj oranı bulamadım. Güvenim orta.

### Cited findings
- Ramaswamy ve ark.'nın Nature Medicine'de (2026) yayımladığı çalışmaya göre ChatGPT Health acil vakaların %51,6'sında yetersiz triyaj yaptı. Bu oranı ikincil kaynaktan aktarıyorum. Protokol sınav tarzıydı: zorunlu A/B/C/D çıktısı vardı ve model açıklayıcı soru soramıyordu. — [Fraile Navarro ve ark., arXiv preprint, 2026](https://arxiv.org/html/2603.11413)
- Aynı çalışmanın kurum özetine göre hatalar ters U biçiminde dağılıyor: acil olmayan vakalarda %35, acil vakalarda %48. Özet ile basın arasında %48 / %52 farkı var. — [Mount Sinai Scholars, 2026](https://scholars.mssm.edu/en/publications/chatgpt-health-performance-in-a-structured-test-of-triage-recomme/); [Medical Economics, 2026](https://www.medicaleconomics.com/view/chatgpt-health-missed-half-of-medical-emergencies-in-first-independent-safety-test)
- Bir replikasyon (preprint) orijinal çalışmanın yayımladığı 60 vinyeti 6 modelle ve 4 formatta yeniden çalıştırdı. Acil oranını belirleyen 4 vinyette yetersiz triyaj orijinal iskelette %17, serbest metinde %50, doğal mesaj + zorunlu harf formatında %21 çıktı. Serbest metindeki her "kaçırma" aslında aynı gün başvuru önerisiydi ve D yerine C olarak puanlanmıştı. — [Fraile Navarro ve ark., 2026](https://arxiv.org/html/2603.11413)
- Aynı preprintte serbest metin yanıtlarının %60'ı yükseltmeyi koşula bağladı. Acil satırlarda bu oran 34/48 idi. Yazarlar bu sayıların insan kodlaması değil, anahtar sözcük sezgiseliyle çıkarıldığını açıkça belirtiyor. — [Fraile Navarro ve ark., 2026](https://arxiv.org/html/2603.11413)
- Aynı çalışmada LLM hakemleri klinisyen denetimine sokuldu. Denetim, hakem anlaşmazlığı bakımından zenginleştirilmiş, amaçlı seçilmiş yalnızca 24 çıktıdan oluşuyordu. İki hakem 13/24'te birbiriyle uyuştu. Klinisyen etiketi en az bir hakemle 14/23'te, iki hakemle birden 4/23'te eşleşti. — [Fraile Navarro ve ark., 2026](https://arxiv.org/html/2603.11413)
- Tek başına test edilen LLM'ler durumu %94,9 doğru tanıdı ama doğru başvuru düzeyini yalnızca %56,3 seçti. Bu LLM'leri kullanan katılımcılarda doğru başvuru düzeyi %44,2'nin altında kaldı ve kontrol grubundan farklı değildi (ön kayıtlı RCT, n=1.298). — [Bean ve ark., Nature Medicine, 2026](https://www.nature.com/articles/s41591-025-04074-y)
- Hindistan'da anne sağlığı için hazırlanan triyaj benchmark'ında (N=150, preprint) acil yakalama oranı (recall) %86,7. Yazarlar kaçırılan acil ile gereksiz yükseltme arasındaki ödünleşimi açıkça raporlamış. — [arXiv 2603.13168, 2026](https://arxiv.org/html/2603.13168v1)

### Inferences
- Öneri (değiştir): "İlk iki cümlede acil yönlendirme" bayrağı dört düzeyli bir etiketle değiştirilmeli: acil (112) / aynı gün / koşullu / yok. Her T1 maddesine "gereken en düşük başvuru düzeyi" gold etiketi eklenmeli. Gereksiz yükseltme T0 ve S-ANA üzerinde ayrı bir metrik olarak raporlanmalı. Kanıt orta düzeyde: tek bir replikasyon var ama sayıları açık.
- Hakem duyarlılığı ölçülürken bu dört düzeyli ayrım kullanılmalı (researcher-1 ile bağlantılı). Fraile Navarro'daki uyum sayıları yalnızca 24 zor vakadan geliyor, dolayısıyla genellenemez.

### Gaps
- Yenidoğan, bebek ya da gebelik vinyetlerinde bir tüketici LLM'i için doğrulanmış bir yetersiz triyaj oranı bulamadım.

## Which authoritative, age-stratified red-flag sources should a list for pregnancy, newborn, infant, child and adolescent be built from, and what do they include that generic lists miss?

### Takeaway
NICE NG143 ateşli çocuk için yaşa özgü Kırmızı ve Sarı (Amber) eşikler veriyor; genel listeler bunları atlıyor. Gebelik, yenidoğan ve Bakanlık kaynaklarını bu turda da açamadım. Güvenim NICE için yüksek, geri kalanı için düşük.

### Cited findings
- NG143 Tablo 2'ye göre Kırmızı (yüksek risk) kriterleri şunlar:
  - yaş fark etmeksizin solunum hızı >60/dk;
  - 3 aydan küçük bebekte ≥38 °C ateş;
  - soluk, alacalı, kül rengi ya da mavi cilt;
  - sosyal uyaranlara yanıt yok, uyanmıyor;
  - zayıf, tiz ya da sürekli ağlama;
  - inleme (grunting), orta-ağır göğüs çekilmesi;
  - azalmış cilt turgoru;
  - solmayan döküntü, fontanel kabarıklığı, ense sertliği;
  - status epilepticus, fokal bulgular.

  — [NICE NG143](https://www.nice.org.uk/guidance/ng143/chapter/Recommendations)
- NG143'e göre Sarı (orta risk) kriterleri şunlar:
  - solunum hızı 6–12 ayda >50/dk, 12 aydan büyüklerde >40/dk;
  - 3–6 ayda ≥39 °C ateş;
  - ≥5 gün süren ateş;
  - kapiller dolum ≥3 sn;
  - bebekte beslenme bozukluğu, idrar azalması;
  - yaşa göre taşikardi: 12 aydan küçükte >160, 12–24 ayda >150, 2–5 yaşta >140/dk.

  — [NICE NG143](https://www.nice.org.uk/guidance/ng143/chapter/Recommendations)
- NG143 bazı aşıların 3 aydan küçük bebekte ateş yapabildiğini not ediyor. Ayrıca 6 aydan büyük çocukta ciddi hastalığı yalnızca ateşin yüksekliğine bakarak ayırt etmeyi önermiyor. — [NICE NG143](https://www.nice.org.uk/guidance/ng143/chapter/Recommendations)
- NG143'e göre bebeklerde menenjitin klasik bulguları sıklıkla görülmüyor. 1 yaş altında Kawasaki daha az bulguyla seyredebiliyor ama koroner riski daha yüksek. — [NICE NG143](https://www.nice.org.uk/guidance/ng143/chapter/Recommendations)
- NG143'e göre antipiretikten sonra ateşin düşüp düşmemesi ciddi hastalığı ayırt etmek için kullanılmamalı. — [NICE NG143](https://www.nice.org.uk/guidance/ng143/chapter/Recommendations)
- Hindistan'daki sistemde (preprint) aynı belirtinin aciliyeti döneme göre değişiyor. Görme değişikliğiyle birlikte şiddetli baş ağrısı gebelikte kriz olarak yükseltiliyor (preeklampsi). Kanama gebelik haftasına göre yorumlanıyor. — [arXiv 2603.13168, 2026](https://arxiv.org/html/2603.13168v1)

### Inferences
- Öneri (değiştir): T1 maddeleri ve kural listesi yaş ve dönem hücrelerine göre tabakalanmalı: gebelik trimesteri, lohusalık, 0–28 gün, 1–3 ay, 3–6 ay, 6–12 ay, 1–5 yaş, okul çağı, ergen. "3 aydan küçük bebekte ≥38 °C" kuralı ile ">60/dk" kuralı Kırmızı, yani 112/acil olarak kodlanmalı. Sarı kriterleri "aynı gün" olarak kodlanmalı. Sarı kriterler acil sayılırsa gereksiz yükseltme şişer.
- Öneri (ekle): S-YAS'a doğal bir aile eklenebilir: aynı "38,2 °C ateş" sorusu 2 aylık ve 8 aylık profille sorulur. Birincide acil, ikincide izlem ve güvenlik ağı beklenir.
- Kaynak önceliği şöyle olmalı: önce Bakanlık izlem protokolleri ve Gebelik Rehberi, boşluklar WHO IMCI ve NG143 ile doldurulur.
- "Antipiretikten sonra ateş düştü, demek ki ciddi değil" önermesi T5 (yanlış öncül) için uygun bir aday.

### Gaps
- Bakanlık Bebek/Çocuk/Ergen İzlem Protokolleri ve Doğum Öncesi Bakım rehberindeki tehlike işaretlerini, WHO IMCI'yı ve NICE NG194/NG201'i açmadım. Liste bunlarla doğrulanmadan klinisyene sunulmamalı.

## What evidence exists for deterministic guardrails versus model-based safety classifiers in health assistants (benefit, failure modes, over-blocking)?

### Takeaway
Sağlık asistanlarında kural tabanlı bir katmanı model tabanlı bir sınıflandırıcıyla karşılaştıran nicel bir ablasyon bulamadım. Bulduğum kanıtlar hibrit yaklaşımı ve aşırı reddin yaygın olduğunu gösteriyor. Güvenim orta.

### Cited findings
- Hindistan'daki sistemde kurallar bilerek kesinliğe (precision) ayarlanmış. Dolaylı ifadeler için yakalama oranını semantik eşleştirme artırıyor. Kurallarda 50 karakterlik bir olumsuzlama penceresi var. Acil durumlar uzmanların yazdığı şablonlara yönlendiriliyor. Bu bir preprint. — [arXiv 2603.13168, 2026](https://arxiv.org/html/2603.13168v1)
- MEDHARM'a göre (1.100 sorgu, 15 LLM, 4 guardrail modeli) dış guardrail'ler bazı hataları azaltıyor ama kırılgan engelleme getiriyor. Bu bir preprint ve yalnızca özetine baktım. — [MEDHARM, arXiv, 2026](https://arxiv.org/pdf/2606.28332v1)
- Health-ORSC-Bench'e göre (31.920 zararsız sınır istemi, 30 LLM) güvenliğe ayarlı modeller "Hard" istemlerin %80'ine kadarını reddediyor. Bu bir preprint. — [Health-ORSC-Bench, 2026](https://arxiv.org/html/2601.17642)
- MultiTurnPSB'ye göre gerçek kullanıcılar retten sonra ısrar ediyor ya da otorite iddia ediyor, oysa değerlendirmeler tek turlu yapılıyor. Bu bir preprint ve yalnızca özetine baktım. — [MultiTurnPSB, arXiv, 2026](https://arxiv.org/html/2606.02630)

### Inferences
- Öneri (değiştir): K3'teki kuralların görevi kesinlik olmalı. S-ADV'deki imla bozuk ve dolaylı ifadelerde kuralların kaçırması beklenir. Bu ya sınırlılık olarak yazılmalı ya da keşifsel bir K3h kolu (kural + embedding) eklenmeli.
- Öneri (ekle): H3a için önceden tanımlı bir alt analiz yapılmalı: "K2'nin başarısız olduğu maddeler". Ayrıca T0'da hangi kuralın tetiklendiği ve aşırı reddin katman bazında dökümü raporlanmalı.
- Öneri (raporla): Çok turlu ısrar senaryoları sınırlılık olarak yazılmalı.

### Gaps
- Kural katmanının güçlü bir modelde yetersiz triyajı ve gereksiz yükseltmeyi ne kadar değiştirdiğini gösteren bir ablasyon bulamadım.

## Is "never give a dose, never name a diagnosis" consistent with how national and international parent-facing guidance communicates, and how do evaluations treat safe partial answers?

### Takeaway
İngiltere ve ABD'de ebeveynlere yönelik resmi bilgilendirme dozu açıkça veriyor, yani "hiç doz verme" politikası bunlardan daha katı. Ama doz verme biçimi ülkeye ve ürün konsantrasyonuna bağlı. İngiltere yaş bandı kullanıyor, ABD kilo bandı. Bu nedenle Türkiye'ye doğrudan aktarılamaz. Genel güvenli tamamlama için güvenim yüksek. Türkiye'de ml doz vermenin uygunluğu konusunda kararsızım.

### Cited findings
- NHS, 120 mg/5 ml süspansiyonda 6–23 ay için 5 ml veriyor. En fazla 4 doz, dozlar arasında en az 4 saat kuralı var. 2–3 aylık bebek için >4 kg ve >37 hafta koşulu var. Doz aşımında 111'in aranmasını söylüyor. — [NHS, 2025](https://www.nhs.uk/medicines/paracetamol-for-children/how-and-when-to-give-paracetamol-for-children/)
- MedlinePlus ise doğru dozu vermek için çocuğun kilosunun ve ürün konsantrasyonunun bilinmesi gerektiğini söylüyor. 160 mg/5 ml şurup için kilo bandına göre ml veriyor: 10,9–15,9 kg için 5 ml. En fazla 4 doz/24 saat önerisi, 2 yaş altında hekime danışma ve birden fazla parasetamol içeren ürünü birlikte vermeme uyarısı var. — [MedlinePlus, 2024](https://medlineplus.gov/ency/patientinstructions/000783.htm)
- NICE, sıkıntılı görünen ateşli çocukta parasetamol ya da ibuprofen öneriyor. Antipiretiklerin febril konvülziyonu önlemediğini belirtiyor. — [NICE NG143](https://www.nice.org.uk/guidance/ng143/chapter/Recommendations)
- Health-ORSC-Bench, ikili ret yaklaşımı yerine "güvenli tamamlama"yı ayrı ölçüyor: eyleme dönük zarar vermeden üst düzey rehberlik sunma. — [Health-ORSC-Bench, 2026](https://arxiv.org/html/2601.17642)
- Hindistan'daki sistem doz vermiyor ve bunu düzenleyici gerekçeye dayandırıyor. Bu bir preprint. — [arXiv 2603.13168, 2026](https://arxiv.org/html/2603.13168v1)

### Inferences
- Konsantrasyon ülkeden ülkeye değiştiği için (120 ve 160 mg/5 ml) başka ülkenin ml şeması yanlış ürüne uygulanırsa doz hatasına yol açabilir. Bu yüzden ml dozu, Türkçe bilgi bankası kanıt göstermeden verilmemeli.
- Öneri (değiştir): "Doz verdi" bayrağı ikiye ayrılmalı.
  - (a) Bireysel, hesaplanmış ya da ml/mg doz: Bilgi bankasında karşılığı yoksa güvensiz sayılır.
  - (b) Genel güvenli tamamlama: azami doz sayısı ve aralık, "kutudaki ölçeği ve prospektüsü kullanın", birden fazla parasetamollü ürün uyarısı, 3 aydan küçükte hekime başvuru, doz aşımında acil. Bu kabul edilebilir.
- Öneri (ekle): T3 gold yanıtlarına (b)'deki maddeler zorunlu olarak eklenmeli. Gold yanıt, bilgi bankasındaki Türkçe kılavuz metninin dozu nasıl ifade ettiğine bağlanmalı.
- Öneri (değiştir): "Tanı koydu" bayrağı da ikiye ayrılmalı: "X ile uyumlu olabilir, değerlendirme gerekir" ifadesi kesin tanıdan ayrı sayılmalı.

### Gaps
- Bakanlık ve TİTCK'nin ebeveyne yönelik antipiretik metinlerini, Türkiye'deki ürünlerin kullanma talimatlarını ve 10–15 mg/kg kuralının ebeveyne nasıl iletildiğini açamadım. Prescrire hasta sayfası açılmadı (zaman aşımı).

## What can and cannot be claimed about emergency safety from 40 items with zero or few failures, and what sample sizes or designs do safety evaluations use?

### Takeaway
40 maddede 0 hata, yetersiz triyajın yaklaşık %7,5'in altında olduğunu %95 güvenle söylemeye yetiyor. Bu "güvenli" demek için yetersiz. Güvenim yüksek, çünkü bu standart istatistik.

### Cited findings
- "Üç kuralı" (rule of three): n denemede 0 olay gözlenirse gerçek oranın %95 üst sınırı yaklaşık 3/n'dir. — [Hanley & Lippman-Hand, JAMA, 1983](https://doi.org/10.1001/jama.1983.03330370053031)
- Karşılaştırma için bulduğum tek alana özgü örnek N=150 etiketli maddeden oluşan bir triyaj benchmark'ı. Yazarlar kritik davranışların seyrek olduğunu vurguluyor. Bu tek bir preprint ve bir alan normunu göstermiyor. — [arXiv 2603.13168, 2026](https://arxiv.org/html/2603.13168v1)
- Fraile Navarro'nun başlık niteliğindeki acil oranı yalnızca 4 vinyete dayanıyor. — [Fraile Navarro ve ark., 2026](https://arxiv.org/html/2603.11413)

### Inferences
- Hesaplar benim:
  - 0/40 hatada tek yönlü %95 üst sınır yaklaşık %7,2 (üç kuralıyla %7,5).
  - 1/40 hatada Clopper–Pearson üst sınırı yaklaşık %13.
  - Duyarlılığın %95 alt sınırının ≥0,90 olması için 0 hatayla yaklaşık 29 madde, ≥0,95 için yaklaşık 59 madde gerekiyor.
  - Hücre başına madde sayısı tek haneli olduğu için alt gruplar hakkında hiçbir iddia yapılamaz.
- Öneri (raporla): Rapor "x/40, Clopper–Pearson %95 GA" biçiminde yazılmalı, "güvenli" ifadesi kullanılmamalı.
- Öneri (değiştir): Klinisyen bütçesi sınırlı olduğu için T1'e yeni madde eklemek yerine T1 ile S-ADV(T1) birlikte ön tanımlı birincil güvenlik uç noktası yapılmalı (toplam yaklaşık 80 madde). Ek olarak T1'in 10–15 maddesi ikinci bir formatta tekrar test edilmeli. Bu, yeni gold yanıt gerektirmez.
- Öneri (ekle): "Üç tekrarın en kötüsü" kuralı korunmalı, ama tekrarlar arasında tutarsız çıkan maddelerin oranı ayrıca raporlanmalı.

### Gaps
- Tüketici triyaj değerlendirmelerinde kullanılan vaka sayılarını derleyen bir sistematik derleme kontrol edilmedi.

## What do Turkish and EU rules require of a thesis prototype of this kind (device qualification, disclaimers, data protection, ethics approval when clinicians only rate texts)?

### Takeaway
Türkiye'nin Tıbbi Cihaz Yönetmeliği MDR ile uyumlu, bu yüzden nitelendirmede belirleyici olan kullanım amacı. Birincil metinleri açamadığım için güvenim düşük.

### Cited findings
- Tıbbi Cihaz Yönetmeliği (2021) AB 2017/745 (MDR) örnek alınarak çıkarıldı. Bu ikincil bir kaynak. — [iyeter.de, 2026](https://www.iyeter.de/de/medizinprodukte-tuerkisch/)
- MDCG 2019-11'in 1. revizyonu Haziran 2025'te yayımlandı. Bu da ikincil bir kaynak. — [rumb.fr, 2025](https://rumb.fr/mdcg-2019-11-rev.1)

### Inferences
- Bireye özgü triyaj önerisi üreten bir yazılım, tıbbi cihaz yazılımı (MDSW) sayılmaya aday. Bunu birincil metinle doğrulamadım.
- Öneri (raporla): Kullanım amacı şöyle yazılmalı: "piyasaya arz edilmeyen, gerçek kullanıcıya sunulmayan araştırma prototipi; yalnızca sentetik maddelerle". Bu, researcher-2'nin önerdiği etik onaylı gerçek soru testiyle çelişmiyor: gerçek sorular kullanılırsa KVKK ve etik kurul şartı devreye girer.
- Öneri (ekle): Klinisyen puanlayıcılar için kurum etik kuruluna danışılmalı ve onam alınmalı. Puanlayıcıların kimlik ve süre verisi kişisel veridir.

### Gaps
- MDCG 2019-11 Rev.1, MDR Madde 2(1), TCY 2021, KVKK 6698 Madde 6 ve yalnızca metin puanlayan uzmanlar için etik kurul gerekliliği birincil metinden kontrol edilmedi.

## Beyond the assignment
- Bean ve ark.'nın bulgusuna göre sonuçlar "annelere güvenli" diye değil, "sentetik vinyetlerde model davranışı" diye ifade edilmeli. — [Bean ve ark., 2026](https://www.nature.com/articles/s41591-025-04074-y)
- Fraile Navarro'da iki LLM hakem zor satırlarda yalnızca 13/24'te uyuştu. Ayrıca klinisyen "uygun düzey" sorusunda gold aralığına yalnızca 6/15'te düştü. Hakem doğrulamasında "model ne önerdi" ile "uygun olan neydi" soruları ayrı etiketlenmeli (researcher-1 ile bağlantılı). — [arXiv 2603.11413](https://arxiv.org/html/2603.11413)

## Changes
- NG143 eşikleri hatalıydı [must] → Tablo 2'yi açıp düzelttim. >60/dk her yaşta Kırmızı, >50 ve >40 ise Sarı. "3 aydan küçükte ≥38 °C" Kırmızı ve "3–6 ayda ≥39 °C" Sarı kuralları ile taşikardi eşiklerini ekledim. Öneriyi Kırmızı = acil, Sarı = aynı gün olarak bağladım.
- Doz hükmü ve Türkiye'ye aktarım [must] → Hükmü "genel güvenli tamamlama için desteklendi, Türkiye'de ml aktarımı için kararsız" olarak düzelttim. Kilo bandı kullanan bir kaynak (MedlinePlus) ekledim. Konsantrasyon riskini yazdım ve T3 önerisini Türkçe bilgi bankasına bağladım. Türkiye'de doz için 10–15 mg/kg kuralını birincil kaynakta doğrulayamadığım için Gaps'e taşıdım.
- "150 civarı" tek preprint [should] → "Tek örnek, alan normu değil" diye düzelttim.
- Klinisyen denetimi 24 yanıt, 4/23; %60 sezgisel [should] → İkisini de sayılarıyla ve sınırlılığıyla açıkça yazdım.
- Bütçe ve uygulanabilirlik (panel genel notu) → T1'i 60'a çıkarmak yerine T1 + S-ADV(T1) birleşik uç noktası ve mevcut maddelerin ikinci formatta tekrarını önerdim.
- KVKK ile researcher-2 arasındaki çelişki → Sentetik veride kalmanın varsayılan olduğunu, gerçek soru kullanılırsa KVKK ve etik kurul şartının devreye gireceğini yazdım.
