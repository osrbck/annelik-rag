# Beklenen sonuçlara karşı en güçlü kanıta dayalı sav: RAG kazancı, yaş filtresi, Türkçe erişim, PDF ayrıştırma ve yerel model

Yöntem notu: 20 arama/okuma yapıldı. "(özetten)" işaretli bulgular yalnızca arama özetinden veya makale özetinden alınmıştır; tam metin açılamadı (PubMed, Springer, JACC erişimi engellendi).

## Hypothesis
Undecided: İlk yarı kılavuza özgü sorular için çürütülmeye yakın, çünkü Almanca ulusal kılavuzda RAG'siz %20,0 doğruya karşı RAG'li çok daha yüksek oranlar bildirilmiş; genel tıbbi sorularda ise uzman değerlendirmesi RAG'in doğruluğu düşürdüğünü gösteriyor. İkinci yarı (yaş filtresi) için doğrudan kanıt bulunamadı; hiçbir çalışma 2026 sınıfı bir modeli sınamıyor.

## What do 2024–2026 studies report for RAG versus no-RAG accuracy with strong models in medicine, where does RAG hurt, and what explains the differences (question type, corpus, retrieval quality)?

### Takeaway
Ortalama etki olumlu ama küçük ve yayın yanlılığı taşıyor. Genel tıbbi sorularda standart RAG güçlü modelin doğruluğunu düşürebiliyor; belirleyici etken erişim kalitesi ve sorunun derleme özgü olup olmaması. Güven: orta.

### Cited findings
- 20 çalışmalık meta-analizde RAG'in temel modele göre havuzlanmış etkisi OR 1,35 (%95 GA 1,19–1,53), I² = %37, öngörü aralığı 1,01–1,8. — [Liu, McCoy, Wright, JAMIA 2025](https://academic.oup.com/jamia/article/32/4/605/7954485)
- Aynı meta-analizde insan değerlendirmesiyle OR 1,65, otomatik değerlendirmeyle 1,20 (P < .01); Egger testi küçük çalışma etkisi ve olası yayın yanlılığı gösteriyor. — [Liu ve ark., 2025](https://academic.oup.com/jamia/article/32/4/605/7954485)
- 18 uzman, 80.502 etiket, 800 çıktı (GPT-4o ve Llama-3.1-8B, 200 hasta ve USMLE tarzı soru): ilk 16 pasajın yalnızca %22'si ilgili; olgusallık %6'ya, tamlık %5'e kadar RAG'siz sürümün altında (ön baskı). — [Kim ve ark., 2025](https://arxiv.org/abs/2511.06738)
- Aynı çalışmada modelin kanıt seçimi kesinliği %41–43, duyarlılığı %27–49; kanıt süzme ve sorgu yeniden yazımı MedMCQA'da %12'ye, MedXpertQA'da %8,2'ye kadar kazanç sağlıyor. — [Kim ve ark., 2025](https://arxiv.org/abs/2511.06738)
- MedQA-USMLE'de BM25, yoğun ve hibrit RAG'in üçü de erişimsiz tabanın altında; erişim soruların %6–7'sine zarar verip %5–6'sına yarıyor (Qwen3-8B; özetten). — [When Retrieval Hurts, ACM 2025](https://dl.acm.org/doi/10.1145/3797161.3797211)
- RAG PubMedQA'da kazandırıyor, MedMCQA'da yalnız LLM hafifçe daha iyi (özetten). — [MDPI MAKE, 2026](https://www.mdpi.com/2504-4990/8/3/64)
- Öncü modeller de tıbbi metne eklenen ilgisiz içerikle yanıltılıyor; yazarlar kötü erişimli RAG'in benzer davranabileceğini belirtiyor (ön baskı, özetten). — [MedDistractQA, 2025](https://arxiv.org/html/2504.01201v1)

### Inferences
- K1 − K0 farkının işareti güvenceli değil. S-ANA'nın ne kadarının "genel pediatri bilgisi", ne kadarının "kılavuza özgü olgu" olduğu sonucu belirler.
- "Tüm zorunlu maddeler var" kuralı tamlık düşüşüne duyarlıdır; RAG yanıtı erişilen pasaja daraltırsa K1, K0'ın altında kalabilir.
- **Ekle:** her S-ANA maddesine altın yanıt yazılmadan önce "kılavuza özgü / genel bilgi" etiketi ve H1'in önceden kayıtlı katmanlı analizi.
- **Ekle:** soru başına erişim tanıları (altın sayfa ilk k'da mı, ilgili pasaj oranı) ve "RAG zarar verdi" sayımı (K0 doğru, K1 yanlış).
- **Değiştir:** K1'i ilk 16 pasaj yerine yeniden sıralayıcı sonrası az sayıda (3–5) pasajla kur.

### Gaps
- 2026 sınıfı küçük öncü modelde RAG'li/RAG'siz uzman değerlendirmesi bulunamadı. Bunu ancak dev kümesinde K0 pilotu yanıtlar.

## How large are effects for local-guideline-specific or recently updated facts, and is there evidence from non-English or national-guideline settings?

### Takeaway
Kılavuza özgü sorularda çift haneli kazanç belgelenmiş, İngilizce dışı bir örnek de var. Ancak bu sorular kılavuzdan üretildiği için etki yapısal olarak şişkin; kazancın büyüklüğü bu tez için aktarılamaz. Güven: düşük–orta.

### Cited findings
- Almanca S3 karotis ve S2e inme kılavuzlarında RAG'siz GPT-4o-mini %20,0 doğru; RAG'li en iyi model (Claude Sonnet 3.5) %70,6 doğru, %10,6 yanlış (özetten). — [Vach ve ark., Clin Neuroradiol 2025](https://pubmed.ncbi.nlm.nih.gov/40892297/)
- Aynı çalışmada yanlış yanıtların %80'i erişim hatasından; 384 sentetik soruda BM25 %82,0 ile bge-m3'ün %78,4'ünü geçiyor (özetten). — [Vach ve ark., 2025](https://link.springer.com/article/10.1007/s00062-025-01562-z)
- AKS kılavuz sorularında RAG, GPT-4o doğruluğunu %71,1'den %92,1'e çıkarıyor (İngilizce; özetten). — [JACC Cardiovasc Interv, 2025](https://www.jacc.org/doi/10.1016/j.jcin.2025.08.019)
- Singapur'da 35 yerel ameliyat öncesi kılavuzla GPT-4 RAG %92,9, uluslararası kılavuzla %96,4 (özetten; RAG'siz taban doğrulanamadı). — [npj Digital Medicine, 2025](https://www.nature.com/articles/s41746-025-01519-z)

### Inferences
- Hipotezin "K1 − K0 15 puanın epey altında" kısmı, S-ANA kılavuza özgü olgular içeriyorsa tutmaz. Asıl risk tavan değil, H1'in dolaylı yoldan doğrulanmasıdır: maddeler ve altın yanıtlar derlemden yazıldığı için K1 yapısal olarak kayrılır.
- **Ekle:** altın yanıt yazılırken, kılavuzu görmeyen bir klinisyenin de doğru sayacağı maddeleri "kılavuzdan bağımsız doğru" diye işaretle; H1'i bu alt kümede de raporla.
- **Ekle:** "yakın zamanda değişen olgu" alt kümesi (2026 aşı takvimindeki değişiklikler); eğitim verisindeki eski bilginin etkisi en net burada ölçülür.
- **Kısıt olarak raporla:** H1 "derlemden yazılmış sorularda RAG kazancı"dır; annelerin gerçek sorularına genellenemez.

### Gaps
- Türkçe ulusal kılavuz üzerinde RAG'li/RAG'siz karşılaştırma bulunamadı.
- Güncellenen olgular için RAG kazancını ayrı ölçen çalışma bulunamadı.
- Vach ve ark.'da öncü modelin RAG'siz tabanı görülemedi (tam metin gerekli).

## What is the evidence for metadata or population filtering in retrieval versus leaving conditioning to the generator, and how are such gains measured?

### Takeaway
Yaş ya da popülasyon koşullu tıbbi erişimde filtreyi "yaşı modele söylemek"le karşılaştıran çalışma bulunamadı. Komşu alanlarda sonuçlar çelişkili: filtre ancak yoğun erişim koşulu yakalayamadığında büyük kazandırıyor. Güven: düşük.

### Cited findings
- 6 kıyaslama, 4 model, 24.000'den fazla yanıt: "zenginleştirmenin çoğu doğruluğu düşürüyor"; belirleyici olan üstverinin hacmi değil, modelin onu görevde kullanabilmesi (ECML-PKDD 2026). — [Zerhoudi, Granitzer, Mitrović, 2026](https://arxiv.org/abs/2606.29645)
- AMAQA'da LLM'in kurduğu üstveri filtresi doğruluğu 0,12'den 0,61'e çıkarıyor (ikincil özetten; birincil makale açılmadı). — [AMAQA incelemesi](https://www.themoonlight.io/review/amaqa-a-metadata-based-qa-dataset-for-rag-systems)
- Finansal soru-yanıtta üstveri, erişim sonrası filtre yerine içerikle birlikte gömüldüğünde yarıyor; şirket ve yıl alanları en güçlü sinyal (ön baskı, özetten). — [Virginia Tech, 2026](https://arxiv.org/abs/2601.11863)

### Inferences
- K2 − K1 farkı, K1'in yanlış yaş bandından pasaj getirme sıklığıyla sınırlıdır. Sorgu metni yaşı içeriyorsa bu sıklık düşük olabilir; fark, 60 ailede saptanabilen 25 puanın çok altında kalır.
- **Değiştir:** H2'yi doğrulayıcı olmaktan çıkar. Birincil ölçüt erişim düzeyinde olsun: "doğru yaş bandından altın pasaj ilk k'da" oranı; aile-tutarlı doğruluk ikincil kalsın.
- **Ekle:** K1'de yaşın erişim sorgusuna girip girmediğini açıkça sabitle ve raporla; K1/K2 ayrımının tamamı buna bağlı.
- **Ekle:** dev kümesinde "K1 yanlış yaş bandı getirdi" oranını ölç; %10'un altındaysa H2 güçsüzdür, kısıt olarak yaz.
- **Ekle:** sert filtrenin bedeli: yaş bandı etiketi yanlış ya da yaşlar-üstü pasajlarda duyarlılık kaybı.

### Gaps
- Yaş koşullu erişimi üretici koşullamasıyla doğrudan karşılaştıran çalışma yok; tez bu boşluğu doldurabilir ama doğrulayıcı güçle değil.

## Which embedding, re-ranking and hybrid setups perform best for Turkish retrieval on current benchmarks, and what Turkish-specific pitfalls are documented?

### Takeaway
Güncel TR-MTEB erişim sıralaması okunamadı. Okunabilen iki bağımsız çalışma, sözcüksel tabanın (BM25, karakter n-gram TF-IDF) yoğun erişimle başa baş ya da üstün olduğunu gösteriyor. Güven: orta (küçük örneklemler).

### Cited findings
- TR-MTEB: 6 görev, yerli ve çeviri karışık 26 veri kümesi, 34,2 milyon çiftle eğitilmiş iki Türkçe model; özet "rekabetçi" diyor, en iyi modeli vermiyor. — [Baysan ve Güngör, Findings of EMNLP 2025](https://aclanthology.org/2025.findings-emnlp.471/)
- Türkçe belge soru-yanıtında yedi sözcüksel/yoğun/hibrit kurulumun hiçbiri karakter TF-IDF tabanını anlamlı geçemiyor (McNemar, hepsi p > 0,05). — [Hassan ve ark., 2026](https://arxiv.org/abs/2609.28007)
- Aynı çalışmada kanıt duyarlılığı (birincil / ikincil rapor): karakter TF-IDF %57 / %91, BM25 %65 / %86, multilingual-E5-base %59 / %90, en iyi hibrit %63 / %91 (ön baskı). — [Hassan ve ark., 2026](https://arxiv.org/html/2609.28007)
- Türkçe sözcük biçimleri çok dilli belirteçleyicilerde çok parçaya bölünüyor; bağlam bütçesine sığan belge metni azalıyor. — [Hassan ve ark., 2026](https://arxiv.org/html/2609.28007)
- Bir Türkçe erişim modelinin kartı 17 görevli "MTEB-Turkish"te 56,87 bildiriyor (satıcı beyanı, bağımsız değil; özetten). — [Mursit-Large-TR-Retrieval](https://huggingface.co/newmindai/Mursit-Large-TR-Retrieval)

### Inferences
- **Değiştir:** erişimi "tek yoğun gömme" yerine sözcüksel + yoğun (bge-m3 ya da multilingual-e5) + yeniden sıralayıcı hibritine çevir; sözcüksel kolda gövdeleme ya da karakter n-gram kullan (ekli biçimler ham BM25'te eşleşmez; bu benim çıkarımım).
- **Ekle:** klinisyen onaylı kaynak sayfalarını erişim altın standardı say; dev kümesinde duyarlılık@k ile kurulum seç ve dondur.
- **Ekle:** bağlam bütçesini karakterle değil, üreticinin belirteç sayısıyla ölç.

### Gaps
- TR-MTEB erişim tablosu, MMTEB Türkçe dilimi, Türkçe yeniden sıralayıcı karşılaştırması okunamadı (PDF ikili geldi). Tablo 3–5'in elle okunması gerekir.
- Türkçe tıbbi erişim kıyaslaması bulunamadı.

## What is recommended for parsing and chunking long clinical guideline PDFs with tables, flowcharts and two-page spreads, and how much does this move answer accuracy?

### Takeaway
Öneriler tutarlı: yerleşime duyarlı ayrıştırma, tabloyu bütün tutma, bölüm sınırında bölme. Klinik kılavuzlarda yanıt doğruluğuna etkiyi ölçen bağımsız çalışma bulunamadı. Güven: düşük.

### Cited findings
- PDF'lerde metin çıkarma hataları ve tablo satır-sütun ilişkisinin bozulması RAG'in yaygın hata kaynakları (ön baskı, özetten). — [arXiv 2401.12599, 2024](https://ar5iv.labs.arxiv.org/html/2401.12599)
- Ayrıştırıcı × parçalama bileşimlerini uçtan uca karşılaştıran çalışma finansal belgelerde; yazarlar parçalama literatürünün sınırlı olduğunu belirtiyor (ön baskı, özetten). — [arXiv 2604.12047, 2026](https://arxiv.org/pdf/2604.12047)
- Metin bölme tabloları parçalayıp erişimde veri bozulmasına yol açabiliyor (özetten). — [FHIR-RAG-MEDS, 2025](https://arxiv.org/pdf/2509.07706)

### Inferences
- Aşı takvimi, büyüme tabloları ve izlem şemaları tezin en yaş-duyarlı içeriği; burada ayrıştırma hatası K1–K3'ü birlikte düşürür ve K0'a yapay üstünlük verir.
- **Ekle:** tablo ve akış şemalarını elle doğrulanmış yapılandırılmış metne çevir, bütün parça olarak sakla; her parçaya bölüm başlığı ve yaş bandı ekle.
- **Ekle:** altın sayfaların 30–50'lik örnekleminde çıkarım doğruluğu denetimi; hata oranını raporla.
- **Ekle:** "tablo / akış şeması kaynaklı" madde etiketi ve bu alt kümede ayrı doğruluk.

### Gaps
- Türkçe taranmış PDF'lerde OCR ve iki sayfalık yayılım için ölçülmüş kanıt yok; kendi denetim örneklemi gerekir.

## Which open-weight models, at which quantisation, are documented to handle Turkish health or general question answering well enough for a local configuration, and what quality drop is reported?

### Takeaway
Nicemlenmiş açık modellerle Türkçe sağlık soru-yanıtı kıyaslaması bulunamadı. Türkçe genel belge soru-yanıtında 4 bit 7–8B modeller %49–75 aralığında; Türkçe uyarlama üstünlük güvencesi vermiyor. Güven: düşük–orta.

### Cited findings
- Q4_K_M, Ollama, 6 GB GPU, 4.096 belirteç bağlam, 100 soru: Trendyol-LLM-8B-T1 %75, Qwen2.5-7B %65, Cosmos Turkish-Llama-8B %54, Mistral-7B %51, Kocdigital-LLM-8B %49. — [Hassan ve ark., 2026](https://arxiv.org/html/2609.28007)
- Trendyol modeli düşünme kipi yüzünden soru başına yaklaşık 14 kat yavaş; tam duyarlık ya da bulut karşılaştırması yok. — [Hassan ve ark., 2026](https://arxiv.org/html/2609.28007)
- Tıbbi kıyaslama takımında 8 bit nicemleme zararsız bulunmuş (İngilizce; özetten, düşük bit sonuçları görülemedi). — [Medmarks, 2026](https://arxiv.org/pdf/2605.01417)
- Türkçe tıbbi RAG için Qwen3-8B QLoRA çalışması erişimi yalnızca 15 sorguyla sınıyor (özetten). — [Diagnostics, 2026](https://doi.org/10.3390/diagnostics16193142)

### Inferences
- K4 − K3 farkı model, nicemleme ve bağlam penceresi etkilerini ayıramaz.
- **Değiştir:** K4 adayını dev kümesinde en az iki modelle (biri Türkçe uyarlı, biri çok dilli) seç; bağlam bütçesini K3 ile eşitle.
- **Ekle:** olanak varsa aynı modelin 8 bit ya da tam duyarlıklı koşumu; yoksa nicemleme etkisini ayrılamayan kısıt olarak yaz.
- **Koru:** K4'ün keşifsel statüsü.

### Gaps
- 12B ve üstü modeller (Gemma 3, Qwen3) için Türkçe nicemleme kaybı bulunamadı; Cetvel ve TurkishMMLU tabloları okunmadı.

## Beyond the assignment
- K0–K3 üreticisinde sıcaklık ve tohum denetimi yok; Hassan ve ark. sıcaklık 0 ve sabit tohum kullanıyor. K4 için aynısını yapıp üç tekrar varyansını K3 ile karşılaştırmak, tekrar gürültüsünün yapılandırma farkına oranını gösterir.
- Hassan ve ark. Türkçe yanıtlarda çekim ve biçim çeşitliliği nedeniyle yanıt türüne göre kural tabanlı puanlamaya geçmiş; sayısal maddelerde (doz, ay, kilo) aynı sorun beklenir (researcher-1'e).
- "Nicemleme doğruluğu korur ama kanıtı korumaz" başlıklı bir ön baskı var; yalnız başlığı görüldü, K4'ün kaynak gösterme davranışı için okunmalı. — [arXiv 2609.24799, 2026](https://arxiv.org/pdf/2609.24799)
