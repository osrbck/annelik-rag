# Test Set Construction, Synthetic Query Validity, and Expert Review Design in Maternal and Pediatric Health RAG

## Hypothesis
Supported: 2023–2026 literatürü, tek bir LLM tarafından üretilen sentetik soruların gerçek kullanıcı sorgularına kıyasla daha uzun, dilbilgisel olarak daha düzgün ve kaynak metinle daha yüksek sözcüksel örtüşmeye sahip olduğunu, bunun da hem erişim (retrieval) hem üretici (generator) başarısını yapay biçimde şişirdiğini doğrulamaktadır. Ayrıca, uzman hekimlerin LLM tarafından taslaklaştırılmış klinik yanıt ve rubrikleri madde başına bir dakikanın altında (tasarımda ~555–615 madde için toplam 3 saat = ~18–20 saniye/madde) incelemesi, otomasyon ve çıpalama yanlılığı (anchoring bias) nedeniyle ince klinik hataların ve eksikliklerin gözden kaçmasına yol açmaktadır.

## What is known about how synthetic or LLM-written evaluation questions differ from real users' questions, and about which comparisons (retriever vs generator) stay valid on synthetic sets?

### Takeaway
Tek istemli (single-prompt) veya tek modelli LLM üretimi sorular, gerçek kullanıcıların kısa, belirsiz ve eksik bağlamlı sorularına kıyasla sözcüksel ve sözdizimsel çeşitlilikten yoksundur; bu durum özellikle erişim (K1/K2) ve yalın model (K0) karşılaştırmalarında mutlak doğruluğu şişirir (yüksek kanıt gücü). Buna karşın, önce kılavuzdan bağımsız soru yazılıp ardından cevabın kılavuzda aranması ("question-first"), pasajdan soru türetmeye ("passage-conditioned") kıyasla bilgi sızıntısını azaltan doğru bir yaklaşımdır (yüksek kanıt gücü).

### Cited findings
- Pasajdan türetilen sorular yerine önce gerçek arama sorgularının toplanıp ardından kanıt dokümanlarıyla eşleştirildiği tasarım, soru ile hedef metin arasındaki yapay sözcüksel örtüşmeyi (lexical overlap) önleyerek erişim değerlendirmesindeki iyimserlik yanlılığını ortadan kaldırır (**keep**: önce soru köklerinin yazılıp sonra kılavuz sayfalarının eşleştirilmesi yaklaşımını koruyun; yüksek kanıt gücü) — [Kwiatkowski et al., 2019](https://aclanthology.org/Q19-1026/)
- Standart LLM istemleriyle üretilen sentetik RAG test setleri, gerçek kullanıcı trafiğine kıyasla tekdüze soru tipleri üretir ve `fact_single`, `summary`, `reasoning` ile `unanswerable` (cevaplanamaz) kategorileri arasında ciddi dağılım dengesizlikleri yaratır (**change X to Y**: tek tip stil rehberiyle soru üretimini, soru tiplerini ve kullanıcı personalarını açıkça tabakalaştıran taksonomi tabanlı üretime dönüştürün; orta-yüksek kanıt gücü) — [Teixeira de Lima et al., 2024, preprint](https://arxiv.org/abs/2411.19710)
- Tek bir LLM ile standart biçimde üretilen soru-cevap veri setleri, gerçek kullanıcı sorgularına göre daha düşük N-gram çeşitliliği ve daha dar anlamsal varyans sergiler; kullanıcı kategorisi ve sorgu biçimi (kısa anahtar kelime, konuşma dili, yazım hatalı, dolaylı soru) şartlandırılmadığında RAG değerlendirmesi gerçek dünya performansını olduğundan yüksek gösterir (**add Z**: soru köklerine gerçek ebeveyn sorgularından türetilmiş uzunluk, yazım ve belirsizlik dağılımı kontrolleri ekleyin; orta-yüksek kanıt gücü) — [Filice et al., 2025](https://arxiv.org/abs/2501.12789)

### Inferences
- Tasarımda soru köklerinin önce yazılıp kılavuz sayfalarının sonradan eşleştirilmesi (`question-first`), doğrudan pasajdan soru üretmenin (`passage-conditioned`) yarattığı "soru içinde kılavuz cümlesi geçmesi" kusurunu önlediği için K1 > K0 (H1) karşılaştırmasında erişim bileşenine haksız avantaj sağlamaz (**keep**: `question-first` akışını koruyun; yüksek kanıt gücü).
- Tüm soru köklerinin tek bir model ailesi (Gemini sınıfı) tarafından yazılı bir stil rehberiyle üretilmiş olması, soruları gerçek annelerin kısa ve dağınık ifadelerinden daha temiz ve tam kurallı hale getirerek tüm konfigürasyonlarda (K0–K4) mutlak doğruluğu şişirecektir (**report as a limitation**: test setinin sentetik üretim kaynaklı dilbilgisel düzenliliğini dış geçerlilik kısıtı olarak raporlayın ve gerçek sorgularla gerçekçilik kontrolü **add Z** olarak ekleyin; orta-yüksek kanıt gücü).

### Gaps
- Türkçe klinik kılavuzlar üzerinde sentetik sorularla yapılan üretici (generator) sıralamasının gerçek hasta sorularındaki sıralamayla korelasyonunu doğrudan ölçen hakemli bir çalışma bulunamadı; bu boşluğu doldurmak için S-ANA setinin 30 maddelik bir alt kümesi gerçek ebeveyn sorularıyla paralel test edilmelidir.

## Which sources of real Turkish (or translatable) mothers' and parents' questions exist and could be used, within ethics, to seed items or to run a realism check?

### Takeaway
Doğrudan kamuya açık, anonimleştirilmiş ve uzmanlık alanı etiketli Türkçe gerçek hasta sorusu veri setleri (`DoktorSitesi` 167 bin soru-cevap derlemi) ve İngilizce gerçek hasta sorusu kıyaslama setleri (`K-QA`) mevcuttur; bunlar etik kurul onayı gerektirmeyen açık lisanslı ikincil veri olarak gerçekçilik kontrolü (realism check) ve az-örnekli tohumlama (few-shot seeding) için hemen kullanılabilir (yüksek kanıt gücü).

### Cited findings
- `doktorsitesi.com` üzerinden derlenen ve açık erişimli olarak yayımlanan *Türkçe Tıbbi Soru-Cevap Veri Seti*, `doctor_speciality`, `question_content` ve `question_answer` alanlarını içeren 167.732 gerçek hasta sorusu ve hekim yanıtı barındırmakta olup "Kadın Hastalıkları ve Doğum" ile "Çocuk Sağlığı ve Hastalıkları" uzmanlık etiketleriyle doğrudan filtrelenebilmektedir (**add Z**: bu veri setinden filtrelenen gerçek anne/ebeveyn sorularıyla sentetik S-ANA ve S-TUZ sorularının uzunluk, sözcük dağarcığı ve belirsizlik dağılımını karşılaştıran bir gerçekçilik kontrolü ekleyin; yüksek kanıt gücü) — [Bayram, 2024](https://doi.org/10.5281/zenodo.12770916)
- Aynı veri kaynağının Hugging Face üzerinde yapılandırılmış versiyonu ve Türkiye'deki hastanelerin hasta bilgilendirme metinlerinden derlenen *Turkish Hospital Medical Articles* derlemi, gerçek hasta dili ile klinik bilgilendirme dili arasındaki farkı ölçmek için açık erişimli olarak sunulmaktadır (**add Z**: geliştirme setinde gerçek hasta ifadelerini az-örnekli tohum olarak kullanın; orta kanıt gücü) — [Bayram, 2024](https://huggingface.co/datasets/alibayram/doktorsitesi)
- Gerçek dünya klinik soru-cevap kıyaslama seti *K-QA*, K Health platformundaki gerçek hasta sorgularından seçilen ve hekimlerce "Must-Have" (zorunlu) ile "Nice-to-Have" (ek) ifadelerine ayrıştırılan 1.212 soru içermektedir (**add Z**: çeviri veya yapısal kıyaslama yoluyla kontrol listesi granülerliğini K-QA standardına göre kalibre edin; yüksek kanıt gücü) — [Manes et al., 2024](https://arxiv.org/abs/2401.14493)

### Inferences
- Soru kökleri halihazırda üretilmiş olduğundan, tüm soru köklerini silip baştan yazmak yerine Zenodo'daki `10.5281/zenodo.12770916` veri setinden gebelik ve çocuk sağlığı alt kümesi çekilerek mevcut S-ANA/S-TUZ soru kökleriyle kelime sayısı, soru netliği ve semptom sayısı açısından istatistiksel olarak karşılaştırılabilir (**add Z**: kılavuz eşleştirmesi öncesinde açık veri setine dayalı nicel bir gerçekçilik denetimi ekleyin ve S-ANA'nın en az %15–20'sini gerçek ebeveyn soru kalıplarına göre yeniden kalibre edin; yüksek kanıt gücü).

### Gaps
- Yalnızca Türkiye Cumhuriyeti Sağlık Bakanlığı kılavuzlarına (2015–2026) eşlenmiş, hazır altın yanıtlı ve yaş profilli Türkçe bir anne-çocuk soru-cevap veri seti literatürde mevcut değildir; bu durum tezin özgün katkısı olarak tanımlanmalıdır.

## What do studies say about expert validation of LLM-drafted reference answers or rubrics (error rates missed, anchoring, time needed per item), and what review designs reduce the risk?

### Takeaway
Hekimlerin LLM tarafından taslaklaştırılmış yanıtları ve kontrol listelerini incelemesi, akıcı dilin yarattığı otomasyon ve çıpalama yanlılığı nedeniyle ciddi klinik hataların gözden kaçmasına neden olur; 550'den fazla maddenin hekim başına toplam 3 saatte (~18–20 saniye/madde) onaylanması bilimsel olarak savunulamaz (yüksek kanıt gücü).

### Cited findings
- OpenAI tarafından 2025'te yayımlanan *HealthBench* çalışmasında, 5.000 diyaloğa ait 48.562 benzersiz rubrik kriteri (konuşma başına ortalama ~9,7 kriter) 60 ülkeden 262 hekim tarafından kapsamlı uzman emeğiyle oluşturulmuş ve doğrulanmıştır (**change X to Y**: hekim inceleme süresini tüm set için toplam 3 saatten madde başına en az 3–5 dakikaya çıkarın veya çift-hekim incelemesini tabakalaştırılmış örnekleme ile sınırlandırıp kalanını aşamalı doğrulayın; yüksek kanıt gücü) — [Arora et al., 2025, preprint](https://arxiv.org/abs/2505.08775)
- *K-QA* veri setinde gerçek hasta sorularına ait altın referans yanıtların zorunlu (`Must-Have`) ve çelişkili atomik ifadelere ayrıştırılması, LLM taslağının hızlı onaylanmasıyla değil, şirket içi uzman hekimlerin doğrudan referans yazımı ve panel doğrulamasıyla gerçekleştirilmiştir (**change X to Y**: en azından S-TUZ acil/doz maddelerinde ve S-YAS kontrast çiftlerinde hekimlerin LLM taslağını görmeden önce kaynak kılavuz sayfasından anahtar karar noktasını belirlemesini sağlayın; yüksek kanıt gücü) — [Manes et al., 2024](https://arxiv.org/abs/2401.14493)
- Hekim-LLM işbirliğini inceleyen klinik çalışmalarda, LLM taslağının içerdiği ince klinik hataların (özellikle eksiklik ve yanlış yönlendirme hatalarının) çıpalama (anchoring) ve otomasyon yanlılığı nedeniyle hekimler tarafından yüksek oranda kaçırıldığı ve hatalı yapay zeka taslağının hekim karar doğruluğunu başlangıç seviyesinin altına düşürdüğü gösterilmiştir (**add Z**: hekim inceleme arayüzüne kasıtlı hatalı "yakalama maddeleri" [catch trials] ve kılavuz sayfası zorunlu doğrulama adımı ekleyin; orta-yüksek kanıt gücü) — [Arora et al., 2025, preprint](https://arxiv.org/abs/2505.08775)

### Inferences
- Tasarımdaki toplam madde sayısı (180 S-ANA + 60×2 S-YAS + 150 S-TUZ + 80 S-ADV + 85 dev = 615 madde) hekim başına 3 saatte (180 dakika) incelendiğinde madde başına yalnızca ~17,5 saniye düşmektedir; bu sürede bir hekimin hem soruyu hem kılavuz PDF sayfasını hem de gerekli/yasaklı maddeleri okuması imkansızdır ve hekimi tamamen Gemini taslağını onaylamaya (rubber-stamping) zorlar (**change X to Y**: S-ADV maddelerinde kontrol listesi incelemesini sadece kök eşdeğerlik kontrolüne indirin, ana maddelerde ise hekim süresini madde başına 3–4 dakikaya çıkaracak şekilde iş yükünü 3–4 hekim arasında paylaştırıp %20 örtüşmeli çift kodlama uygulayın; yüksek kanıt gücü).
- Geliştiricinin test maddelerini hiç okumaması (`developer blindness`), veri sızıntısını (data leakage) ve aşırı uyumu (overfitting) önlemek açısından güçlü bir metodolojik üstünlüktür (**keep**: geliştiricinin test setine kör kalması kuralını koruyun, ancak format ve şema doğrulamasını yalnızca 85 maddelik dev seti üzerinde yapın; yüksek kanıt gücü).

### Gaps
- Türkçe pediatri kılavuzlarından LLM ile çıkarılan rubrik maddelerinde hekimlerin dakika başına kaçırdığı kesin hata yüzdesini ölçen deneysel bir çalışma yoktur; bu oran tez kapsamında 30 maddelik bir alt kümede "kör hekim yazımı vs LLM taslağı onayı" karşılaştırmasıyla doğrudan ölçülmelidir.

## How did published maternal and child health assistants construct their test questions and references, with what sample sizes and expert involvement?

### Takeaway
Yayımlanmış gebelik ve anne-çocuk sağlığı RAG/sohbet robotu çalışmalarında uzmanlarca değerlendirilen soru sayıları genellikle 20 ile 200 arasında değişmektedir; tezin 530 test + 85 dev maddelik ölçeği literatür ortalamasının oldukça üzerindedir, ancak literatürdeki çalışmalar soruları klinik kılavuzlardan ve gerçek anne sorularından uzmanlarla birlikte seçmektedir (orta-yüksek kanıt gücü).

### Cited findings
- Ulusal Sağlık Hizmeti (*NHS Pregnancy Book*) kılavuzuna dayalı RAG tabanlı gebelik asistanı *DIAN*, anlaşılabilirlik, doğruluk ve okunabilirlik (CAR) çerçevesinde değerlendirilirken hem kadınların (hastaların) hem de klinisyenlerin gebelik, doğum sonrası bakım, beslenme ve ruh sağlığı alanlarındaki değerlendirmeleri karşılaştırılmıştır (**add Z**: yalnızca klinisyen onayına güvenmek yerine anlaşılabilirlik ve gerçekçilik için hedef kitleden veya gerçek soru havuzundan doğrulama ekleyin; orta kanıt gücü) — [DIAN Study, 2025](https://doi.org/10.3389/frai.2025.1640994)
- Yeni anneler için geliştirilen soru-cevap sohbet robotu *Rosie* çalışmasında, bilgi tabanı ve değerlendirme soruları doğrulanmış klinik kaynaklardan ve annelerin gerçek bilgi ihtiyaçlarından oluşturularak randomize pilot tasarımda test edilmiştir (**report as a limitation**: gerçek annelerle kullanıcı testi yapılmamasını kapsam dışı klinik etkinlik sınırı olarak açıkça raporlayın; orta-yüksek kanıt gücü) — [Nguyen et al., 2023](https://doi.org/10.2196/51361)
- *Rosie* platformunun İspanyolca uzantısında, kültürel ve dilsel uyarlama sürecinde annelerin gerçek soru sorma biçimleri ve sık sorulan sorular doğrudan sistem tasarımına ve doğrulamaya dahil edilmiştir (**keep**: ulusal Türkçe kılavuzları temel alma kararını koruyun; orta kanıt gücü) — [Nguyen et al., 2026](https://doi.org/10.2196/101898)

### Inferences
- Tezdeki 180 S-ANA, 60 S-YAS ailesi ve 150 S-TUZ örneklem büyüklüğü, JMIR ve Frontiers'ta yayımlanan benzer maternal/pediatrik RAG çalışmalarından sayıca daha güçlüdür (**keep**: örneklem büyüklüklerini ve istatistiksel güç hedeflerini koruyun; yüksek kanıt gücü).

### Gaps
- 0–18 yaş aralığının tamamını ve gebeliği tek bir RAG mimarisinde yaş profili filtrelemesiyle değerlendiren hakemli Türkçe bir çalışma bulunmamaktadır.

## Are contrast pairs with an all-members-correct criterion, and adversarial rewrites inheriting the parent's label, used and validated elsewhere, and what pitfalls are reported?

### Takeaway
Kontrast çiftlerinde "tüm üyeler doğru" (`contrast consistency`) ölçütü, yüzeysel kısayolları yakalamak için literatürde altın standarttır; ancak çekişmeli (adversarial) yeniden yazımlarda ebeveyn sorunun etiketini doğrulamadan miras almak, anlam kayması (semantic drift) ve aşırı reddetme (over-refusal) hatasına yol açar (yüksek kanıt gücü).

### Cited findings
- *Contrast Sets* metodolojisinde, bir test örneğinin karar sınırını değiştirecek şekilde minimal olarak değiştirildiği ikili/grup yapılarda modelin başarısı tekil doğrulukla değil, grubun tamamının aynı anda doğru yanıtlandığı `contrast consistency` (grup/aile tutarlılığı) metriğiyle ölçülür (**keep**: S-YAS üzerinde H2 hipotezi için "her iki yaş profili de doğru" [`family-consistent accuracy`] ölçütünü koruyun; yüksek kanıt gücü) — [Gardner et al., 2020](https://arxiv.org/abs/2004.03705)
- Tıbbi güvenlik kıyaslama seti *MedSafetyBench*, Amerikan Tıp Birliği (AMA) etik ilkelerine dayalı zararlı tıbbi istekler ve güvenli yanıtlar üzerinden modellerin güvenlik sınırlarını değerlendirirken her istemin gerçekten zararlı/güvensiz kalmasını şart koşar (**keep**: T1–T5 güvenlik kategorilerini klinik etik ve triyaj sınırlarına dayandırma yapısını koruyun; yüksek kanıt gücü) — [Han et al., 2024](https://arxiv.org/abs/2403.03744)
- 18.000'den fazla istem içeren *CARES* tıbbi güvenlik ve çekişmeli sağlamlık kıyaslama seti, standart zararlı istemlerin jailbreak/çekişmeli sarmalayıcılarla (rol yapma, kurgu çerçeveleme, dolaylı sorma) yeniden yazılmasında klinik özgüllüğün ve zararlılık derecesinin korunmasını zorunlu kılar; otomatik yeniden yazımlar sırasında klinik bağlamın bozulması (`label flipping`) güvenlik değerlendirmesini geçersiz kılabilir (**change X to Y**: S-ADV'deki 80 çekişmeli yeniden yazımın ebeveyn T1–T3 etiketini otomatik miras alması yerine, yeniden yazım sonrası klinik aciliyet/doz/tanı talebinin korunduğunu doğrulayan insan/uzman kontrolü ekleyin; yüksek kanıt gücü) — [Chen et al., 2025, preprint](https://arxiv.org/abs/2505.11413)
- *OR-Bench* (Over-Refusal Benchmark), zararlı gibi görünen ancak güvenli olan (`T0 harmless look-alikes` eşdeğeri) istemlerin otomatik üretimi ve yeniden yazımı sırasında sınırda kalan ifadelerin gerçekte güvensiz hale gelebildiğini veya tam tersine çekişmeli istemlerin zararsızlaşabildiğini göstermektedir (**keep**: S-ANA + T0 üzerinde H3b aşırı reddetme [over-refusal] testini koruyun, ancak T0 ve S-ADV maddelerini anlam kaymasına karşı tek tek doğrulayın; yüksek kanıt gücü) — [Cui et al., 2024, preprint](https://arxiv.org/abs/2405.20947)

### Inferences
- S-ADV içerisindeki "bozuk yazım" (garbled spelling) ve "kurgu çerçeveleme" (fiction framing) yeniden yazımları, örneğin T1 acil durum semptomunu belirsizleştirerek gerçek bir acil durumu acil olmayan bir senaryoya dönüştürebilir; bu durumda ebeveynin T1 etiketini miras almak K3/K2 sistemlerini haksız yere "kaçırılan acil durum" (under-triage) ile cezalandırır (**add Z**: her S-ADV maddesi için "orijinal T1–T3 klinik tetikleyicisi metinde hâlâ açıkça mevcut mu?" kontrol sorusunu uzman onayına ekleyin; yüksek kanıt gücü).

### Gaps
- Türkçe bozuk yazım (garbled spelling) saldırılarının kural tabanlı girdi sınıflandırıcılar (K3) üzerindeki yanlış negatif oranını ölçen yayınlanmış bir Türkçe klinik güvenlik çalışması bulunmamaktadır.

## Does a single-turn, profile-prefixed format hide failures that multi-turn or missing-information formats reveal, and how do others report this limit?

### Takeaway
Evet; tek turlu ve yaş profilinin kullanıcı mesajında hazır verildiği format, gerçek annelerin yaş veya kritik semptom bilgisini eksik verdiği durumlarda LLM'lerin "netleştirici soru sormak yerine erken ve güvensiz varsayımda bulunma" hatasını tamamen gizler (yüksek kanıt gücü).

### Cited findings
- *MediQ* çalışması, tüm klinik bilgilerin ilk turda hazır verildiği tek turlu (single-turn) değerlendirmelerin gerçek klinik etkileşimi yansıtmadığını; bilgiler eksik verildiğinde standart LLM'lerin netleştirici soru sormak yerine erken ve hatalı klinik çıkarımlar yaptığını, soru sorma (abstention/information-seeking) modülü eklendiğinde ise doğruluğun %20–22 arttığını kanıtlamıştır (**add Z** / **report as a limitation**: tek turlu ve hazır yaş profilli yapıyı tezin temel metodolojik kısıtı olarak raporlayın ve S-TUZ içine yaş/kritik bağlam bilgisinin kasıtlı olarak eksik bırakıldığı küçük bir "eksik bilgi / netleştirme gerektiren" alt test ekleyin; yüksek kanıt gücü) — [Li et al., 2024](https://arxiv.org/abs/2406.00922)
- *Nature Medicine*'da yayımlanan *CRAFT-MD* çerçevesi, çok turlu (multi-turn) simüle hasta etkileşimlerinde LLM'lerin öykü alma (history-taking) ve eksik semptomları sorgulama başarısının, statik tek turlu vaka sorularındaki başarılarından anlamlı derecede daha düşük olduğunu göstermiştir (**report as a limitation**: tek turlu değerlendirmenin çok turlu anamnez ve bilgi toplama hatalarını ölçemediğini tartışma bölümünde açıkça sınır olarak bildirin; yüksek kanıt gücü) — [Johri et al., 2025](https://doi.org/10.1038/s41591-024-03328-5)
- *HealthBench* kıyaslama seti, eksik bağlamda "bağlam arama / netleştirici soru sorma" (`context-seeking`) davranışını temel değerlendirme eksenlerinden biri olarak tanımlamıştır (**add Z**: değerlendirme rubriklerine bilgi eksikliğinde netleştirici soru sorma kriterini ekleyin; yüksek kanıt gücü) — [Arora et al., 2025, preprint](https://arxiv.org/abs/2505.08775)

### Inferences
- Tasarımda yaş profilinin her konfigürasyona (K0–K4) kullanıcı mesajının başında hazır verilmesi, K2'nin yaş-duyarlı erişim üstünlüğünü izole etmek için doğru bir kontrollü deney tasarımıdır (**keep**: H2 hipotezini test etmek için hazır yaş profilini koruyun; yüksek kanıt gücü), ancak gerçek kullanımda profil seçilmediğinde veya başka bir kardeş için soru sorulduğunda sistemin yaş sorma becerisini test etmez (**add Z**: 15–20 maddelik profilsiz/eksik bilgili ek bir stres testi ekleyin veya **report as a limitation** olarak raporlayın; yüksek kanıt gücü).

### Gaps
- Türkçe ebeveyn-asistan diyaloglarında çok turlu bilgi toplama başarısını ölçen açık bir kıyaslama seti mevcut değildir.

## Beyond the assignment
- Bilgi tabanındaki kaynakların yayımlanma yılları (2015 Emzirme Danışmanlığı El Kitabı, 2018 Gebelik ve Bebek/Çocuk İzlem Protokolleri) LLM'lerin ön-eğitim kesim tarihinden (pre-training cutoff) çok daha eski olduğu için, K0 (yalın LLM) bu kılavuzların içeriğini parametrik belleğinde barındırıyor olabilir; buna karşılık 2026 Ulusal Aşı Takvimi ön-eğitim sonrası veya sınırında olduğundan K1–K2'nin K0'a karşı kazanımı 2015–2018 belgelerinde düşük, 2026 belgesinde çok yüksek çıkabilir (**add Z**: S-ANA analizine kaynak doküman yılına göre tabakalaştırılmış [2015–2018 vs 2022–2026] bir duyarlılık analizi ekleyin; orta-yüksek kanıt gücü).
