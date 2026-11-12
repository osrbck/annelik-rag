# Etik Kurul Başvuru Taslağı (Mersin Üniversitesi)

> Taslak — danışman onayından sonra enstitünün resmi formuna aktarılacak.

## 1. Araştırmanın adı
Gebelik ve 0–18 yaş çocuk sağlığı alanında yaş-farkında, güvenlik katmanlı RAG tabanlı bir soru-cevap asistanının geliştirilmesi ve değerlendirilmesi

## 2. Araştırmanın türü
Yazılım geliştirme ve değerlendirme çalışması. **Hasta verisi ve kişisel sağlık verisi toplanmaz.** İnsan katılımı yalnızca uzman panelinin (hekim/ebe) altın yanıtları onaylaması ve sistem yanıtlarını puanlamasıyla sınırlıdır; yöntem `docs/thesis/degerlendirme_protokolu.md` belgesinde tanımlıdır.

## 3. Amaç
Kamuya açık klinik rehberlere dayanan bir yapay zekâ asistanının; (a) yaşa uygun bilgi getirme doğruluğunu, (b) tıbbi güvenlik davranışını (teşhis/doz vermeme, acil durumda yönlendirme) ve (c) yerel/bulut model farkını ölçmek.

## 4. Veri kaynakları
- Kamuya açık rehberler (Sağlık Bakanlığı, WHO, uzmanlık dernekleri) — kişisel veri içermez.
- **Sentetik** anne/çocuk profilleri ve soru setleri — araştırmacı tarafından üretilir, gerçek kişiye ait değildir.
- Uzman değerlendirme puanları — kodlanmış (U1, U2, U3); yalnız puan ve kısa gerekçe. Kod–kimlik eşlemesi yalnız araştırmacıda durur, depoya ve yayınlara girmez.

## 5. Katılımcılar
Uzman paneli: 2–3 hekim/ebe, gönüllü. Yük: kişi başı en çok 6 saat, üç çevrim içi oturuma bölünmüş (yaklaşık 20 dk, 2 saat, 3 saat). Kimlik bilgisi yayımlanmaz; isteğe bağlı teşekkür.

## 6. Riskler ve önlemler
- Hasta katılımcı yoktur. Uzman katılımcılar için risk asgari düzeydedir (zaman yükü); puanladıkları yanıtlar hiçbir hastaya sunulmamış araştırma çıktılarıdır.
- Sistem riski: Asistan tıbbi tavsiye yerine geçmez; her cevap kaynak gösterir ve hekime yönlendirir. Araştırma süresince kamuya açılmaz.

## 7. KVKK
Hastalara ait kişisel veri ve özel nitelikli sağlık verisi işlenmez. Uzman katılımcıların adı, uzmanlığı, iletişim bilgisi ve imzası kişisel veridir: yalnız onam formunda yer alır, açık rızayla işlenir, depo dışında saklanır. Uzman katılımcılardan aydınlatılmış onam alınır (bkz. `uzman_onam_formu.md`).

## 8. Talep
Hasta verisi ve özel nitelikli kişisel veri içermediği için **muafiyet**. Uzman paneli insan katılımcı sayılabileceğinden, muafiyet uygun görülmezse standart onay; başvuru her iki duruma göre hazırlanır.
