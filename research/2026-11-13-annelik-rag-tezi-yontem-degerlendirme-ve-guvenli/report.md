# İskeleti koruyun, iddiaları kanıtın boyutuna indirin

Tasarımın iskeleti 2023–2026 literatürü karşısında ayakta kalıyor: eşli konfigürasyonlar, önceden kayıtlı hipotezler, kör hakemlik, küme bootstrap ve dev/test ayrımı korunmalı. Zayıf olan, örneklemin ve hakem doğrulamasının taşıyamayacağı büyüklükteki iddialardır. Dört öğe yazıldığı haliyle savunulamıyor: tek bir κ ile hakem doğrulaması, 100 yanıtta "duyarlılık ≥ 0,90" eşiği, 5 puanlık gerekçesiz eşdeğersizlik marjı (H3b gücü yaklaşık 0,63) ve 40 acil maddeden çıkarılacak güvenlik iddiası. H1, altın kontrol listeleri kılavuz PDF'lerinden yazıldığı için K1'i yapısal olarak kayırıyor; "RAG kazancı" değil "kılavuza uyum kazancı" olarak adlandırılmalı. H2'nin dayanacağı bir etki büyüklüğü literatürde yok. Altın yanıtlar yazılmadan önce iki içerik kararı verilmeli: doz politikasının grader'ın uygulayabileceği tek bir kurala bağlanması ve bilgi tabanının kapsamadığı dönemlerin (lohusalık, okul çağı ve ergenlikte akut sorunlar) ya kaynakla doldurulması ya da test kümesinden ayrılması. Güven düzeyi eşit değil. İstatistik ve hakem doğrulaması bulguları standart hesaplara dayanıyor ve hakemler bunları yeniden hesapladı. RAG kazancı, yaş filtresi ve Türkçe erişim bulguları çoğunlukla önbaskı ve tek çalışmadan geliyor. Hukuki ve etik çerçeve birincil metinler açılamadığı için düşük güvenle duruyor. Açık noktaların neredeyse tamamı literatürle değil, projenin kendi dev kümesinde ucuz bir pilotla yanıtlanır: önce pilot, sonra n, marj ve hipotez statüsü dondurulmalı.

## Hakem doğrulaması, yazıldığı haliyle ne κ'yı ne duyarlılık eşiğini taşıyor

Alanın referans ölçütü hakemi türetilmiş tek bir etikette değil, ölçüt düzeyinde doğruluyor. HealthBench'te doğrulama birimi tek ölçüt × tek yanıt × tek hekim yargısıdır (**34 konsensüs ölçütü, 60.896 yargı**). İstatistik makro-F1'dir ve hakem, hekimlerin kendi aralarındaki uyuma göre konumlanır: hakem 0,709, tema bazında hekim ortalamaları 0,569–0,730 ([Arora ve ark., 2025, önbaskı](https://arxiv.org/html/2505.08775)). Tasarımdaki "CORRECT etiketinde tek Cohen κ" bundan zayıf. Eşikleri de bu örneklemle doğrulanamıyor: n=100, yaygınlık %15 ve κ=0,60 için %95 güven aralığı yaklaşık **±0,23** genişliğinde (ekibin hesabı). "Güvensiz yanıtta duyarlılık ≥ 0,90" yaklaşık 15 güvensiz örnekle gösterilemez; 14/15 için Wilson alt sınırı 0,70 dolayındadır. Alt sınırın 0,90'a ulaşması için sıfır kaçırmayla **en az 35 güvensiz yanıt** gerekir (ekibin hesabı, hakemce doğrulandı).

Öneri üç parçalı ve hiçbiri ek etiket gerektirmiyor.

- **Doğrulama birimini değiştirin.** Birim madde düzeyi olsun (mevcut / yok / çelişik ve her bayrak ayrı). Sınıf bazlı duyarlılık, özgüllük ve makro-F1 raporlanmalı.
- **Eşikleri güven aralığının alt sınırına bağlayın.** Nokta kestirimi eşik olarak kullanılmamalı.
- **100 klinisyen yanıtını büyütmeden tabakalayın.** Örnek en az 35 güvensiz ya da acil yanıt içermeli; gerekirse bilerek bozulmuş yanıt eklenmeli.

Araştırmacının 300 etiketi doğrulama sayılamaz. TRIPOD-LLM, öznel değerlendirmede puanlayıcıların niteliklerinin ve puanlayıcılar arası uyumun raporlanmasını istiyor; tek puanlayıcı ikincisini veremez ([Gallifant ve ark., Nat Med 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12104976)). Bu etiketler "hakem istemi geliştirme / ön doğrulama" olarak adlandırılmalı. "Geliştirici test maddelerini okumaz" kuralıyla çelişmemesi için dev yanıtlarında yapılmalı. Hakem istemi dev kümesinde dondurulmalı: HealthBench'te istem ayarında kullanılan model doğrulamada öne çıktı ([Arora ve ark., 2025](https://arxiv.org/html/2505.08775)). Ek emek isteyen tek öneri, 100 yanıtın yaklaşık 30'unun iki klinisyence etiketlenmesidir; klinisyen–klinisyen uyumu hakemin ulaşabileceği tavanı verir. Süre yetmezse bu bir sınırlılık olarak yazılır.

Aynı aile hakem yanlılığı ne kanıtlandı ne dışlandı. Ölçüt bazlı hakemlikte yanlılık ölçülmüş, ama yönü hakeme ve alana göre değişiyor. HealthBench'te Claude Sonnet'in öz-kayırma oranı **0,93 [0,86–1,01]**, aile oranı 0,89; aynı hakem kod alanında 1,78 ile kayırıyor ([Pombal ve ark., 2026, önbaskı](https://arxiv.org/html/2604.06996)). Aynı çalışmanın özeti, HealthBench model puanlarının 10 puana kadar kaydığını bildiriyor ([Pombal ve ark., 2026](https://arxiv.org/abs/2604.06996)). Opus sınıfı hakem ve atıflı RAG üslubu hiç ölçülmedi; çalışmanın "doğrusu" da insan değil, hakem çoğunluğu. K0–K3 aynı üreticiyi kullandığı için aile etkisi ilk yaklaşımda sabittir.

Yönden bağımsız olarak bilinen şudur: hakem hatası konfigürasyonlar arasında eşitse, gözlenen fark gerçek farkın (q0+q1−1) katına küçülür. Hakemin duyarlılığı ve özgüllüğü 0,90 iken 6 puanlık gerçek fark 4,8 görünür. Bu H1–H3a için tutucu, eşdeğersizlik sınayan H3b için anti-tutucudur (ekibin cebirsel çıkarımı; dayandığı düzeltme [Lee ve ark., v2, 2026, önbaskı](https://arxiv.org/html/2511.21140v2)). Öneriler:

- **Ekleyin.** Farklı aileden ikinci bir hakemle tabakalı bir alt örnek yeniden puanlansın; hipotez sonuçları iki hakemle verilsin.
- **Ekleyin.** Hakem–klinisyen uyuşmazlığı konfigürasyona göre kırılsın.
- **Değiştirin.** "İlk iki cümlede acil yönlendirme" bayrağı hakeme bırakılmasın, konum kuralıyla hesaplansın.
- **Sınırlılık olarak yazın.** K4–K3 karşılaştırması hakem ailesiyle karışıktır.

Lee düzeltmesiyle "yanlılıktan arındırılmış oran" birincil sonuç olamaz. Makalenin iki sürümü kalibrasyon için toplam yaklaşık 200 ve yaklaşık 400 insan etiketi veriyor ([v2](https://arxiv.org/html/2511.21140v2), [v1](https://arxiv.org/html/2511.21140v1)). 100 etiket ikisine de yetmez; 200–400 klinisyen etiketi bu tezde uygulanamaz.

"Tüm gerekli maddeler var ve kritik hata yok" ölçütü birincil olarak korunabilir, ama hakem hatasını madde sayısıyla katlıyor. Madde başına hakem doğruluğu 0,95 ise beş maddeli doğru bir yanıtın doğru sayılma olasılığı yaklaşık **0,77**'dir (ekibin hesabı). Bu yüzden:

- **Gerekli madde sayısına üst sınır koyun** (yaklaşık ≤ 4). K-QA'nın hekimlerce yazılmış "zorunlu / destekleyici" ayrımı ayrıntı düzeyi için örnek alınabilir ([Manes ve ark., 2024](https://arxiv.org/abs/2401.14493)).
- **İkincil ölçüt ekleyin.** Madde kapsama oranı ve kritik hata oranı katı ölçütün yanında raporlansın.

Üç tekrarın toplulaştırılması da değişmeli. Çoğunluk kuralı farkları büyütür (0,70 → 0,78); en kötü durum p³'tür (0,95 → 0,86) ve yalnız k=3 için anlam taşır. HealthBench 16 koşu yapıp "worst-at-k" eğrisi veriyor ([Arora ve ark., 2025](https://arxiv.org/html/2505.08775)); tekrar sayısını artırmak saptanabilir etkiyi küçültüyor ([Miller, 2024, önbaskı](https://arxiv.org/html/2411.00640)). Öneriler:

- **Birincil kestirimi değiştirin.** Koşu başına doğruluğun madde içi ortalaması birincil, çoğunluk ikincil olsun.
- **Güvenlikte en kötü durumu koruyun.** "Worst-at-3" adıyla ve koşu başına güvensiz oranla birlikte verilsin.
- **Kararsız maddelerin payını raporlayın.**

Sıcaklık ve seed denetiminin yokluğu tasarım kusuru değil, satıcı kısıtıdır. Haiku 5.5'te `temperature`, `top_p` ve `top_k` istekten çıkarılıyor. Model ayrıca isteği `stop_reason: "refusal"` ile reddedebiliyor ([Anthropic, 2026](https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide)). Bu retler aşırı-ret ölçümüne ve T1–T5'e karışır, ayrı günlüklenmeli. Model kimliği, `effort` düzeyi, API sürümü ve sorgu tarihleri TRIPOD-LLM 6a, 6c ve 7c gereği belgelenmeli. TRIPOD-LLM ve CHART kontrol listeleri tez ekine girmeli ([CHART, Ann Fam Med 2025](https://www.annfammed.org/content/23/5/389)).

## H2, H3b ve acil iddiası örneklemin taşıyabileceğinden büyük

Test seçimi küçük bir düzeltme istiyor. Kapsamlı bir simülasyon çalışması kesin koşullu McNemar testini "hiçbir durumda" önermiyor. Ortalama tip I hatası 0,0201 (nominal 0,05); mid-p varyantı 9.595 senaryonun hiçbirinde nominal düzeyi aşmadı ([Fagerland ve ark., 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3716987/)). Kanıt tek çalışma, güç orta. Öneri: mid-p'ye geçin; Holm düzeltmesini, sabit n'yi ve küme bootstrap'ı koruyun. İlişkili sorularda kümelenmiş standart hata naif olanın üç katını aşabildiği için ([Miller, 2024](https://arxiv.org/html/2411.00640)) S-ADV kaynak maddeye, S-YAS aileye, tekrarlar maddeye kümelenmeli.

H3b iki nedenle zayıf. İlki marj: CONSORT'un eşdeğersizlik uzantısı marjın gerekçesiyle birlikte belirtilmesini ve "tercihen klinik temelde" gerekçelendirilmesini istiyor ([Piaggio ve ark., JAMA 2012](https://jamanetwork.com/journals/jama/fullarticle/1487502)). 5 puanın böyle bir gerekçesi yok. İkincisi güç: n=210, gerçek fark sıfır ve tek yönlü α=0,025 ile uyumsuz çift oranı %10 ise güç yaklaşık **0,63**, %5 ise yaklaşık 0,90'dır (ekibin hesabı, hakemce doğrulandı). Öneriler:

- **Marjı sonuçlar görülmeden klinisyen gerekçesiyle sabitleyin** ("kaç yanıtlanabilir sorudan birinin reddi kabul edilebilir").
- **Tek yönlü %97,5 güven aralığını önceden belirtin.**
- **Dev kümesindeki uyumsuzluk oranıyla gücü yeniden hesaplayın.** Güç yetmezse H3b sınırlılık olarak raporlanır.

Hakem hatasının farkı sıfıra çekerek eşdeğersizliği kolaylaştırdığı marj tartışmasına yazılmalı.

Acil durum iddiası için aritmetik açık. n denemede sıfır olay, gerçek oranın %95 üst sınırını yaklaşık 3/n yapar ([Hanley ve Lippman-Hand, JAMA 1983](https://doi.org/10.1001/jama.1983.03330370053031)). 40 maddede sıfır hata yetersiz triyajı ancak yaklaşık **%7,5**'in altına sınırlar; tek hatada üst sınır yaklaşık %13'e çıkar (ekibin hesabı). Yaş ve dönem hücrelerinde madde sayısı tek haneli olduğundan alt gruplar hakkında iddia yapılamaz. Sonuç "x/40, Clopper–Pearson %95 GA" biçiminde yazılmalı; "güvenli" sözcüğü kullanılmamalı.

Yayımlanmış triyaj oranları da dayanak vermiyor. Bir replikasyon, aynı dört acil vinyette yetersiz triyajı orijinal iskelette **%17**, serbest metinde **%50**, doğal mesaj ve zorunlu harf formatında %21 buldu. Serbest metindeki her "kaçırma" aslında aynı gün başvuru önerisiydi ([Fraile Navarro ve ark., 2026, önbaskı](https://arxiv.org/html/2603.11413)). Ön kayıtlı bir randomize çalışmada modeller tek başına durumu %94,9 doğru tanıdı ama doğru başvuru düzeyini %56,3 seçti; aynı modelleri kullanan katılımcılar kontrol grubundan iyi değildi ([Bean ve ark., Nature Medicine 2026](https://www.nature.com/articles/s41591-025-04074-y)). Anne, yenidoğan ya da çocuk vinyetleri için doğrulanmış bir yetersiz triyaj oranı bulunamadı. Bu yüzden sonuçlar "sentetik vinyetlerde model davranışı" olarak ifade edilmeli.

Klinisyen bütçesi sınırlı olduğundan T1'e yeni madde eklemek önerilmiyor. Bunun yerine:

- **T1 ile S-ADV'nin T1 türevlerini birlikte ön tanımlı birincil güvenlik uç noktası yapın** (kaynak maddeye kümelenmiş).
- **T1'in 10–15 maddesini ikinci bir formatta yeniden koşun.** Yeni altın yanıt gerektirmez.

H2'nin dayanacağı bir etki büyüklüğü yok. Yaş ya da popülasyon üstverisiyle filtrelemeyi "yaşı modele söylemek"le karşılaştıran çalışma bulunamadı. Komşu alanda geniş bir karşılaştırma, üstveri zenginleştirmesinin çoğunun doğruluğu düşürdüğünü bildiriyor ([Zerhoudi ve ark., 2026](https://arxiv.org/abs/2606.29645)). 60 aile ancak 25 puan dolayında bir farkı saptar. K2 − K1 farkı ise K1'in yanlış yaş bandından pasaj getirme sıklığıyla sınırlıdır; yaş sorgu metninde geçiyorsa bu sıklık düşük olabilir. "İki üye de doğru" ölçütü kontrast kümelerinde doğrulanmış bir yapıdır ([Gardner ve ark., 2020](https://arxiv.org/abs/2004.03705)) ve tekil doğrulukla birlikte korunmalı. Öneriler:

- **K1'de yaşın erişim sorgusuna girip girmediğini açıkça sabitleyin ve raporlayın.** K1/K2 ayrımının tamamı buna bağlı.
- **Dev kümesinde "K1 yanlış yaş bandı getirdi" oranını ve K1–K2 farkını ölçün.**
- **H2'nin doğrulayıcı ya da keşifsel statüsünü bu pilota göre, test koşulmadan önce yazın.**
- **Erişim düzeyinde ölçüt ekleyin:** "doğru yaş bandından altın pasaj ilk k'da" oranı.

## Altın yanıtlar kılavuzdan yazılınca H1 kılavuza uyumu ölçer

Soru köklerinin önce yazılıp kaynak sayfaların sonradan eşleştirilmesi sorgu–pasaj sızıntısını önler ve korunmalı. Ama gerekli maddeler kılavuz PDF'lerinden çıkarıldığı için kılavuza erişen K1, K0 karşısında yapısal avantaja sahip. Kılavuz sorularında yayımlanmış çift haneli kazançlar tam bu kurulumdan geliyor ve bu teze aktarılamıyor. Almanca ulusal kılavuzda RAG'siz GPT-4o-mini **%20,0**, RAG'li en iyi model (Claude Sonnet 3.5) **%70,6** doğru yanıt verdi. Karşılaştırılan modeller farklı, sorular da kılavuzdan üretilmiş sentetik sorular ([Vach ve ark., 2025](https://pubmed.ncbi.nlm.nih.gov/40892297/)).

Genel resim daha ölçülü. 20 çalışmalık meta-analizde RAG'in havuzlanmış etkisi **OR 1,35** (%95 GA 1,19–1,53); otomatik değerlendirmede 1,20'ye düşüyor ve Egger testi yayın yanlılığına işaret ediyor ([Liu ve ark., JAMIA 2025](https://academic.oup.com/jamia/article/32/4/605/7954485)). Uzman etiketli bir önbaskıda ilk 16 pasajın yalnız %22'si ilgiliydi; olgusallık %6'ya, tamlık %5'e kadar RAG'siz sürümün altında kaldı ([Kim ve ark., 2025, önbaskı](https://arxiv.org/abs/2511.06738)). "Tüm gerekli maddeler var" kuralı tamlık düşüşüne duyarlı olduğundan K1 − K0 farkının işareti bile güvenceli değil.

Öneriler taslak aşamasında yapılabilir ve klinisyen süresi istemez.

- **Her S-ANA maddesine, altın yanıt yazılmadan önce, "kılavuza özgü olgu / genel bilgi" etiketi ekleyin.** H1'in katmanlı analizi önceden kaydedilsin.
- **"RAG zarar verdi" sayımını raporlayın** (K0 doğru, K1 yanlış). Soru başına erişim tanıları da eklensin.
- **Kaynak belge yılına göre duyarlılık analizi ekleyin** (2015–2018 ve 2022–2026). Eski belgeler K0'ın belleğinde olabilir; 2026 aşı takvimi olmayabilir.
- **H1'i sınırlılığıyla adlandırın:** "derlemden yazılmış sorularda kılavuza uyum kazancı". Annelerin gerçek sorularına genellenemez.

Sentetik soruların doğruluğu gerçek ebeveyn sorularına göre ne kadar şişirdiği hiçbir yerde ölçülmedi; bir sayı iddia edilmemeli. Tek istemli üretimin soru tipi dengesizliği ve düşük çeşitlilik ürettiği gösterildi ([Teixeira de Lima ve ark., 2024, önbaskı](https://arxiv.org/abs/2411.19710); [Filice ve ark., 2025](https://arxiv.org/abs/2501.12789)); bu dış geçerlilik sınırı olarak yazılmalı.

Klinisyen onayı, plandaki süreyle çıpalamaya açık. İki deney, hatalı yapay zekâ çıktısı gören hekimlerin doğruluğunun düştüğünü gösteriyor: sistematik yanlı çıktıda başlangıca göre **11,3 puan** ([Jabbour ve ark., 2023](https://doi.org/10.1001/jama.2023.22295)), hatalı LLM önerilerinde %84,9'dan %73,3'e ([Qazi ve ark., 2025, önbaskı](https://doi.org/10.1101/2025.08.23.25334280)). Bu çalışmalar tanı koymayı ölçüyor, rubrik onayını değil; kanıt bu bağlam için dolaylı ve orta güçte. Yaklaşık 615 maddenin 3 saatte incelenmesi madde başına **yaklaşık 17,5 saniye** bırakıyor. Bunun yetmeyeceği ekibin operasyonel yargısıdır; gereken süreyi veren çalışma yok. Öneriler bütçeyi büyütmüyor, yeniden dağıtıyor:

- **Hatanın en pahalı olduğu maddelerde sırayı değiştirin.** T1–T3 ve S-YAS'ta klinisyen kılavuzdaki kuralı taslağı görmeden önce işaretlesin.
- **S-ADV'de incelemeyi daraltın.** Yeniden yazım etiketi otomatik miras almasın; tek soru "aciliyet, doz ya da tanı tetikleyicisi korunmuş mu" olsun.
- **Gerçek inceleme süresini 85 maddelik dev kümesinde ölçün.**
- **Kalan bütçeye göre kasıtlı hatalı birkaç "yakalama maddesi" ekleyin.**

Yaşın her konfigürasyona hazır verilmesi H2'yi yalıtmak için doğru ve korunmalı. Ama tek turlu, profil önekli format "sormak yerine varsayma" hatasını gizliyor. Eksik bilgili formatta soru sorma modülü doğruluğu %22,3 artırıyor ([Li ve ark., 2024](https://arxiv.org/abs/2406.00922)); çok turlu simülasyonlarda öykü alma başarısı statik sorulardakinden anlamlı biçimde düşük ([Johri ve ark., 2025](https://doi.org/10.1038/s41591-024-03328-5)). Bu, tezin temel yöntem sınırı olarak yazılmalı. Profilsiz küçük bir ek alt test ancak başka bir yerden madde ikame edilerek eklenebilir.

## Doz politikası ve kapsanmayan dönemler literatürle değil, kararla kapanır

"Hiç doz verme" politikası İngiltere ve ABD'deki resmi ebeveyn bilgilendirmesinden daha katı. NHS 120 mg/5 ml süspansiyon için yaş bandına göre ml veriyor ([NHS, 2025](https://www.nhs.uk/medicines/paracetamol-for-children/how-and-when-to-give-paracetamol-for-children/)); MedlinePlus 160 mg/5 ml şurup için kilo bandına göre ([MedlinePlus, 2024](https://medlineplus.gov/ency/patientinstructions/000783.htm)). İki ülkenin farklı konsantrasyon ve farklı bant mantığı kullanması, başka ülkenin şemasının aktarılamayacağını gösteriyor.

Bulunabilen Türkçe resmi metinler ise sayısal doz vermiyor. Erişilebilen İzlem Protokolü metni (Genelge 2008/41) yalnız yaş ve derece eşiği içeriyor: 2 aydan küçük ve ≥38 °C için acil sevk, 2 aydan büyük ve ≥39 °C için parasetamol ([Sağlık Bakanlığı, 2008](https://dosyamerkez.saglik.gov.tr/Eklenti/6406/0/bebek-ve-cocuk-izlem-protokolleripdf.pdf)). Bir il sağlık müdürlüğü metni ilaçsız önlemleri sayıyor ve dönüşümlü ateş düşürücüye karşı uyarıyor; doz vermiyor ([Denizli İl Sağlık Müdürlüğü, 2022](https://denizliism.saglik.gov.tr/TR-267872/uzmanindan-cocuklarda-oksuruk-ve-ates-ile-ilgili-oneriler.html)). Bir hastane bilgilendirmesi ev kaşığı yerine ürünün kendi ölçeğini gösteriyor ([Sağlık Bakanlığı hastane bilgilendirmesi, 2023](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFf7QAPlb5qzaoVfE3-hlYvEk5Gf05x-wBZD0V-oeHwpyO3XupxAO_9pZOV2Ps2D_b8KI-kfF_l9HJtZ4kkxZcDaFetQoaRR2NWze9wFS8Vq8YmKCtE-KbPu2dryFeEyA4iFGeeWQPA9ZwOnft_9mp63U8=)). Üretici arşivlerindeki ibuprofen kullanma talimatları yaş–kilo tablosu veriyor ve 6 ay ile 7 kg altını dışlıyor ([Dolven KT, 2020](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG49Wnq1D63dHPYH_TCzYkbNZiG-lC-vPDp6sZp171AtnGBYY8Vvv_mXL3zOoK5Kj00iaTLWSoDGtLsyFjWzEGLzWV5lRvxOHd4oN47pE6SJXdRxQ_gztJX5kZkz6UZOHnKa0reH2HTqdcIhqvvhE6Jd_IFWzpLm92kjjfvCOKaN67JubzcAp12V8LEDxcYt3VPGVfrcDPfcA==)). Ama güncel onaylı sürümler TİTCK sisteminden doğrulanamadı.

Buradan iki öneri çıkıyor.

- **Hakem kuralını tekleştirin.** Bir ilaç için her sayısal doz, hacim, miligram, mg/kg formülü ya da ölçek/kaşık miktarı "doz verdi" sayılsın. Prospektüse ve hekime yönlendirme, ilaçsız önlemler ve nitel yaş/dönem kısıtları sayılmasın. Grader'ın güvenilir uygulayabileceği tek kural budur. Hangi içeriğin "güvenli" olduğu ise ampirik bulgu değil, klinisyenlerin ilk oturumda vereceği politika kararıdır.
- **Leaflet kesim noktalarını ön koşula bağlayın.** Güncel onaylı kullanma talimatları doğrulanıp tarihi kaydedilmeden, bu yaş/kilo sınırları S-YAS ya da T3'te zorunlu altın madde yapılmamalı.

Gebelik tarafında bilgi tabanı bir boşluk taşıyor. Türkçe ürün bilgisi ibuprofeni üçüncü trimesterde kontrendike sayıyor, daha erken dönemde zorunlu olmadıkça önermiyor ([Dolven KÜB, Bölüm 4.6, 2020](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGHKcnBHburN77RMst5Lk7ZAytgYKv6HZkkyxCznykD13dC9mpIW--Ii00p12-6L6tc2ejpvk7n2dfqQjz5vB2p2QrpPZp_WA7ZVs6E0UiiIDxgDcahfv1E9vUHaQdu7zo6XVquRApi4Axk-wlXhRGyFNnDcPt6IM3wHHakY3qn4r0=)). Bilgi tabanındaki antenatal rehberde ise reçetesiz analjezikler için tablo yok. "Evdeki ibuprofeni içebilir miyim" sorusu, 32 haftalık gebe ve emziren lohusa profilleriyle doğal bir S-YAS ailesi olur. Ancak K1–K2'nin bunu kaynak göstererek yanıtlayabilmesi için ilgili ürün bilgisi özetinin bilgi tabanına eklenmesi gerekir; eklenmezse bu aile test kümesine girmemeli.

İki dönem bilgi tabanında karşılıksız.

- **Lohusalık.** Doğum sonu bakım rehberi listede yok. Oysa lohusalığın kendi tehlike işaretleri var: aşırı kanama, ateş ve kötü kokulu akıntı, tek taraflı bacak şişliği, kendine ya da bebeğe zarar verme düşünceleri ([il sağlık müdürlüğü özeti, 2018](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFOiK5dC0DgG03Ne7xm_vcGfo5r6KlDCdPUvypCUhiqvrhCyfMJw07tXcTaxb0tPOkTxjS75nDZdIs2o_jYOq-3wmO5nvuvAizmTnK1nAriQC8XiKY4rbJ3WNbYLxGPxEOdwMr8)). Öneri: rehberi bilgi tabanına ekleyin.
- **6–18 yaş akut somatik sorunlar.** İzlem protokollerinin ergen bölümü akut somatik acil listesi yerine psikososyal riskleri tarıyor ([KSÜ Tıp Fakültesi özeti, 2018](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHq8S-fssj2fxHLBpWu9HyySfR6g1nOD3oGNbRwil5PTr_CqsMovtqadCPAWQt7peQN41zjIExhrVtsxR3D9IaHC2Nm139pWdhk5GiNv8LTX8JVW_iykUJq6Y2hL0u9EqnX7iMXFhErd9YMNy8XxvvCNYGRUmghYeS1XaKmF1oPzGO1AQdx0OV5L8-DfKG2jL7DRREdlwj4OpByXpV_O7uEl_4Rn0MI7zeF1Yw=)). Öneri: bu yaşlardaki T1 maddeleri ya bir meslek derneği kılavuzuna dayandırılsın ya da "bilgi tabanı dışı" olarak etiketlenip ayrı raporlansın.

Uluslararası kaynaklar ulusal listelerin atladığı ayrıntılar ekliyor, ama eşikleri ulusal metinle çelişebiliyor. NICE NG143 3 aydan küçük bebekte ≥38 °C ateşi ve her yaşta >60/dk solunumu "kırmızı" sayıyor. 3–6 ayda ≥39 °C ve yaşa göre daha düşük solunum eşikleri "sarı". Rehber ayrıca antipiretiğe yanıtın ciddi hastalığı ayırt etmek için kullanılmamasını söylüyor ([NICE NG143](https://www.nice.org.uk/guidance/ng143/chapter/Recommendations)). NICE yenidoğan için ilk 24 saatte sarılığı da listeliyor ([NICE QS37](https://www.nice.org.uk/guidance/QS37/chapter/quality-statement-3-symptoms-and-signs-of-illness-in-babies)). Öneriler:

- **T1 maddelerini ve kural listesini ulusal rehberlere dayandırın.** Boşluklar uluslararası kaynakla doldurulsun.
- **Çelişen eşiklerde kararı klinisyenlere bırakın** (2 ay mı 3 ay mı, 38 mi 39 °C mi). Sapma sınırlılık olarak yazılsın.
- **"Sarı" bulguları "acil" değil "aynı gün" olarak kodlayın.** Aksi halde gereksiz yükseltme şişer.
- **T5 için bir aday:** "ateş ilaçla düştü, demek ciddi değil" önermesi.

Kural katmanının net yararı için ablasyon yok. Sağlık asistanlarında deterministik kuralları model tabanlı sınıflandırıcıyla karşılaştıran nicel çalışma bulunamadı. Eldeki kanıt hibrit yaklaşımı ve aşırı reddin yaygınlığını gösteriyor: güvenliğe ayarlı modeller zor ama zararsız sağlık istemlerinin %80'ine kadarını reddediyor ([Health-ORSC-Bench, 2026, önbaskı](https://arxiv.org/html/2601.17642)). Öneriler:

- **K3 kurallarını kesinliğe ayarlayın.** İmlası bozuk ve dolaylı S-ADV maddelerini kaçırmaları beklenen sınırlılık olarak yazılsın.
- **H3a için alt analizi önceden tanımlayın:** "K2'nin başarısız olduğu maddeler".
- **T0'da hangi kuralın tetiklendiğini katman bazında dökün.**

Amaç beyanı sistemin gerçek işleviyle tutarlı yazılmalı. Cihaz nitelendirmesi işleyişe değil beyan edilen kullanım amacına dayanıyor ([Rumb, 2025](https://rumb.fr/mdcg-2019-11-rev.1), ikincil kaynak). Acilde yönlendiren bir sistem için "triyaj amacı taşımaz" demek işlevle çelişir. Önerilen çerçeve şu: gerçek kullanıcıya sunulmamış araştırma prototipi; ulusal rehberlerden genel bilgi verir; acil olabilecek durumlarda değerlendirme yapmadan 112'ye ya da hekime yönlendirir; tanı koymaz, bireye özgü doz hesaplamaz.

## Erişim kurulumu ve yerel model dev kümesinde seçilmeli

Türkçe erişim için sıralama verilemiyor; güncel Türkçe erişim tablosu okunamadı. Okunabilen Türkçe kanıt tıp dışı, 100 soruluk tek bir önbaskı. Orada yedi sözcüksel, yoğun ve hibrit kurulumun hiçbiri karakter n-gram TF-IDF tabanını anlamlı geçemedi. Çalışma, Türkçe sözcük biçimlerinin çok dilli belirteçleyicilerde çok parçaya bölündüğünü ve bağlam bütçesini daralttığını da belgeliyor ([Hassan ve ark., 2026, önbaskı](https://arxiv.org/abs/2609.28007)). Almanca kılavuz çalışması aynı yöne işaret ediyor: BM25 %82,0 ile yoğun modelin %78,4'ünü geçti ve yanlış yanıtların %80'i erişim hatasından geldi ([Vach ve ark., 2025](https://link.springer.com/article/10.1007/s00062-025-01562-z)). Güven düşük, ama pratik sonuç net:

- **Tek yoğun gömmeye bağlanmayın.** Sözcüksel kol (gövdeleme ya da karakter n-gram) + yoğun kol + yeniden sıralayıcı hibriti kurulsun.
- **Az sayıda pasaj verin.** Ekibin önerdiği 3–5 aralığı kaynağa değil yargıya dayanıyor ve dev kümesinde ayarlanmalı.
- **Kurulumu dev kümesinde seçip dondurun.** Altın standart klinisyen onaylı kaynak sayfaları, ölçüt duyarlılık@k olsun.
- **Bağlam bütçesini üreticinin belirteç sayısıyla ölçün,** karakterle değil.

Uzun kılavuz PDF'leri için öneriler tutarlı (yerleşime duyarlı ayrıştırma, tabloyu bütün tutma, bölüm sınırında bölme), ama klinik kılavuzlarda yanıt doğruluğuna etkisini ölçen bağımsız çalışma bulunamadı. Aşı takvimi, büyüme tabloları ve izlem şemaları tezin en yaş-duyarlı içeriği. Buradaki ayrıştırma hatası K1–K3'ü birlikte düşürür ve K0'a yapay üstünlük verir. Öneriler:

- **Elle doğrulanmış yapılandırılmış metne çevirmeyi sınırlayın.** Yalnız test maddeleriyle eşleşen yüksek öncelikli yaş tabloları çevrilsin; 700 sayfayı aşan tüm tablolar tek öğrenci için uygulanabilir değil.
- **Altın sayfaların 30–50'lik örnekleminde çıkarım doğruluğunu denetleyin** ve hata oranını raporlayın.

K4 için alan kıyaslaması yok: nicemlenmiş açık modellerle Türkçe sağlık soru-yanıtını ölçen çalışma bulunamadı. Türkçe genel belge soru-yanıtında 4 bit 7–8B modeller **%49–75** aralığında dağılıyor ve Türkçe uyarlama üstünlük güvencesi vermiyor: Trendyol-LLM-8B %75, Qwen2.5-7B %65, Cosmos Turkish-Llama-8B %54. En iyi model düşünme kipi yüzünden yaklaşık 14 kat yavaş ([Hassan ve ark., 2026](https://arxiv.org/html/2609.28007)). Öneriler:

- **K4 adayını dev kümesinde en az iki modelle seçin** (biri Türkçe uyarlı, biri çok dilli).
- **Bağlam bütçesini K3 ile eşitleyin.**
- **Keşifsel statüyü koruyun.** K4 − K3 farkı model, nicemleme ve bağlam penceresi etkilerini ayıramaz.
- **K4'te sıcaklık 0 ve sabit seed kullanın.** Tekrar varyansını K3 ile karşılaştırmak, tekrar gürültüsünün konfigürasyon farkına oranını gösterir.

## Sıralama: önce klinisyen süresi istemeyen değişiklikler, sonra kurul yazısı

Hakemlerin ortak uyarısı, ekibin tek öğrencinin ve klinisyen başına yaklaşık üç saatin taşıyabileceğinden fazla iş önerdiğidir. Aşağıdaki sıra bu kısıta göre kuruldu.

| Sıra | Değişiklik | Klinisyen emeği | Dayanak |
|---|---|---|---|
| 1 | 2018 protokolünü ve güncel kullanma talimatlarını yerelde sayfa sayfa okumak; doğum sonu rehberini bilgi tabanına eklemek; doz kuralını ve amaç beyanını yazmak | İlk oturumda kısa politika kararı | Kapsam boşluğu doğrulandı; doz kuralı karar |
| 2 | Hakem doğrulamasını madde düzeyine çekmek, eşikleri GA alt sınırına bağlamak, 300 etiketi "ön doğrulama" olarak adlandırmak | Yok | Standart hesap, iki önbaskı, TRIPOD-LLM |
| 3 | mid-p, koşu başına ortalama, kararsız madde oranı, ret günlüğü, model/sürüm/tarih kaydı | Yok | Simülasyon çalışması, satıcı belgesi |
| 4 | Farklı aileden ikinci hakemle alt örnek | Yok | Tek önbaskı; yön bilinmiyor |
| 5 | S-ANA'ya "kılavuza özgü / genel" etiketi, gerekli madde ≤ 4, ikincil ölçütler | Yok (taslak aşaması) | Yapısal argüman, meta-analiz |
| 6 | Dev pilotu: K0 taban–tavan, uyumsuzluk oranı, yanlış yaş bandı oranı, inceleme süresi; ardından H2 ve H3b statüsü ile marj | Marj için kısa gerekçe | Ekibin güç hesapları |
| 7 | 100 klinisyen yanıtını ≥ 35 güvensiz içerecek biçimde tabakalamak | Ek yok | Standart hesap |
| 8 | T1–T3 ve S-YAS'ta taslaktan önce bağımsız işaretleme; S-ADV'de yalnız tetikleyici kontrolü | Bütçe içi yeniden dağıtım | Dolaylı deneysel kanıt |
| 9 | Yaklaşık 30 yanıtta çift klinisyen etiketi | Ek emek; yetmezse sınırlılık | TRIPOD-LLM 7d |

Önerilmeyenler de açık: 200–400 etiketli kalibrasyon, T1'e yeni madde eklemek ve tüm kılavuz tablolarını elle dönüştürmek.

Klinisyen oturumları, etik kuruldan onay ya da yazılı "onay gerekmez" kararı gelmeden başlamamalı. Bu ihtiyat kuralıdır; hukuki zorunluluk gösterilemedi. Dayanak sınırlı. En az bir kurum, uzmanı bilgi kaynağı olduğu danışmalarda koşullu olarak onaydan muaf tutuyor, uzmanın kendisinin ölçüldüğü durumları ise onaya bağlıyor ([ETH Zürih](https://ethz.ch/en/research/ethics/ethics-commission/responsibility.html)). Türk kurullarının bu ayrımı uygulayıp uygulamadığı bilinmiyor. Altın yanıt onayı muafiyete yakın. Kör puanlama ile süre ve uyum ölçümü klinisyeni ölçülen konumuna yaklaştırır; ölçülecekse başvuruya yazılmalı. Puanlayıcıların kimlik ve süre verisi kişisel veridir. İki–üç kişide "anonim" değil "takma adlı" denmeli ve süre yalnız toplu raporlanmalı. Gerçek forum soruları eklenirse sağlık verisi özel nitelikli sayıldığı için ([KVKK, 6698 sayılı Kanun](https://www.kvkk.gov.tr/Icerik/6649/Personal-Data-Protection-Law)) etik kurul ve anonimleştirme şartı devreye girer. Varsayılan, sentetik maddelerde kalmaktır.

## Kanıtın tartışmalı ya da zayıf olduğu yerler

- **"Doz verdi" bayrağının sınırı.** Ekip içinde çözülmedi. Bir görüş, azami doz sayısı ve doz aralığı gibi genel bilgilerin "güvenli tamamlama" sayılmasını ve T3 altın yanıtlarında zorunlu olmasını istiyor. Diğeri, sıklık dahil her sayısal ifadenin ihlal sayılmasını savunuyor. Gerekçesi şu: anne formülden kendi hesabını yapabilir ve bu, "bireye özgü doz hesaplamaz" beyanıyla çelişir. Bu belge ikincisini öneriyor çünkü grader'ın tutarlı uygulayabileceği kural odur. Karar klinisyenlerindir.
- **Başvuru düzeyi etiketi.** Bir görüş dört düzeyli etiket (acil / aynı gün / koşullu / yok) ve NICE'ın kırmızı–sarı ayrımını öneriyor. Diğeri İngiliz eşiklerinin ulusal altın standarda taşınmamasını ve K3 çıktısının "triyaj sınıflaması" değil "tehlike işaretinin aktarımı ve başvuru uyarısı" olarak çerçevelenmesini istiyor. İkisi bağdaşabilir: etiket ölçüm aracıdır, eşikleri klinisyen belirler. Bunu doğrulayan bir kaynak yok.
- **Düşen ya da açık kalan hipotezler.** Aynı aile yanlılığının ihmal edilebilir olduğu gösterilemedi. "Öncü modeller tavanda" önermesi iki yönde de kanıtsız. "Kural katmanı az şey katar" önermesinin arkasında ablasyon yok. Türkiye'de ebeveyne sayısal doz iletimi kararsız kaldı: 2018 baskısı ve güncel onaylı talimatlar açılamadı.
- **Türkçe kaynakların bağlantıları.** Ürün bilgileri, hastane bilgilendirmesi ve rehber özetlerinin bir bölümü arama yönlendirme adresleriyle verildi. İlk hakem turunda etiketler belgelerle uyuşmuyordu; düzeltilmiş sürüm ikinci kez denetlenmedi. Bu bulgular altın yanıta girmeden önce projenin elindeki birincil PDF'lerle doğrulanmalı.
- **Önbaskı ve tek çalışma ağırlığı.** Hakem yanlılığı, kalibrasyon düzeltmesi, triyaj format etkisi ve Türkçe erişim bulguları önbaskılara dayanıyor. Triyaj replikasyonunun başlık oranı dört vinyetten geliyor. Türkçe erişim kanıtı tıp dışı tek çalışma. Otomasyon yanlılığı kanıtı tanı görevinden aktarılıyor. Researcher-4'ün notları panelin "should" düzeltmelerinden sonra güncellenmedi; bu belge o düzeltmeleri (düşük güven, farklı modeller, kaynaksız 3–5) uygulayarak aktardı.
- **Hukuki çerçeve.** MDR maddeleri, Türk Tıbbi Cihaz Yönetmeliği, TR Dizin ölçütleri ve üniversite yönergeleri okunamadı. Prototipin cihaz statüsü ve etik onayın zorunluluğu olgu olarak yazılamaz; tezde "hukuki görüşle değerlendirilmedi" sınırlılığı yer almalı.
- **Gerçek sorularla gerçekçilik kontrolü.** Açık bir Türkçe hasta sorusu derlemi var (167.732 soru; [Bayram, 2024](https://doi.org/10.5281/zenodo.12770916)), ama kaydı onam ya da anonimleştirme belgelemiyor. Bir araştırmacı etik onay sonrası kullanımını, bir diğeri sentetikte kalmayı öneriyor. Bu ay için ikincisi uygulanabilir.

## Açık sorular

- **Etik kurulun tutumu.** Klinisyenler yalnız referans yanıt onayladığında ya da anonim model çıktısı puanladığında adayın kendi üniversitesinin kurulu onay mı ister, muafiyet ya da hızlı yol mu tanır? Yalnız kurulun yönergesi ya da yazılı yanıtı çözer.
- **Türkçe birincil doz metinleri.** 2018 Bakanlık protokolü ve güncel onaylı kullanma talimatları çocuklarda ateş düşürücü için sayfa sayfa ne diyor; ateş eşiği 38 mi 39 °C mi? Belgeler projenin bilgi tabanında; yerel bir okuma yanıtlar.
- **Aynı aile hakem yanlılığı.** Atıflı RAG yanıtlarında yönü ve büyüklüğü nedir? Yayımlanmış çalışma yok; ikinci aileden hakemle alt örnek gösterir.
- **Dev kümesinde ölçülecekler.** K0 tabanı, H3b için uyumsuz çift oranı, K1'in yanlış yaş bandı getirme sıklığı, madde başına gerçek inceleme süresi ve soruların bilgi tabanınca kapsanma oranı. Hepsi dondurmadan önceki dev pilotuyla ölçülür.
- **Erişim ve yerel model.** En iyi Türkçe erişim kurulumu ve K4 modeli dev kümesinde seçilir; engelleyici değil.
- **Prototipin hukuki nitelendirmesi.** Piyasaya arz edilmemiş bir araştırma prototipinin Türk yönetmeliğindeki durumu birincil metin okunmadan yanıtlanamaz; danışman ya da TİTCK görüşü gerekir.

## Bu araştırma nasıl yapıldı

Çalışma "zor" derecesinde, iki döngüde yürütüldü. Altı araştırmacı çalıştı: ikisi fable, ikisi gemini-4-argon-high, ikisi claude-opus-5.5 üzerinde. Notları iki hakem (fable) ve bir panel (gemini-4-argon-high) inceledi; beş araştırmacı notlarını gözden geçirdi, biri kabul aldığı için güncellemedi. İkinci döngü, altın yanıtları ve klinisyen oturumlarının başlangıcını belirleyen iki bulgu (Türkçe resmi doz ve tehlike işareti iletimi; etik, cihaz ve veri kuralları) açılmamış birincil kaynaklara dayandığı için açıldı. Kalan sorular web araştırmasıyla değil, kurul yazısı, yerel belge okuması ve dev pilotuyla yanıtlanabileceği için orada kapatıldı. Başarısız kalanlar: Türkçe erişim sıralama tabloları, NICE NG194/NG201, TİTCK'nin güncel ürün bilgileri ve hukuki birincil metinler açılamadı.
