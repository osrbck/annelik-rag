# Belge kayıt defteri

Her belge (ya da belge grubu) için `belge_kayit_defteri.csv`'de bir satır. Kurallar:

1. **Sürüm sabitleme:** İndirilen belgenin SHA-256'sı `hash` sütununa yazılır (`scripts/hash_kb.py`).
   Hash bir kez yazıldıktan sonra betik onu kendiliğinden değiştirmez; dosya farklıysa hata verir.
   Belge bilerek yenilendiyse `--guncelle` kullanılır ve değişiklik sapma günlüğüne
   (`docs/thesis/sapma_gunlugu.md`) yazılır. Her değerlendirme koşumundan önce
   `python scripts/hash_kb.py --kontrol` temiz çıkmalıdır.
2. **Saklama biçimi:** tek dosya ise `kb/raw/<belge_id>.<uzantı>` (pdf, html, xlsx…);
   birden çok dosya ise `kb/raw/<belge_id>/` klasörü (dernek rehberleri, WHO tabloları gibi
   `çeşitli` kayıtlar). Web sayfası kaynakları (ör. aşı takvimi) erişim tarihindeki hâliyle
   PDF/HTML olarak kaydedilir; canlı sayfa kaynak sayılmaz.
   İndirilen her dosyanın tam adresi, boyutu ve kendi SHA-256'sı `kaynak_dosyalari.csv`'de
   tutulur (`kb/raw/` depoya girmediği için klasör kayıtlarının hangi adreslerden geldiği
   yalnız buradan izlenebilir). Dosya eklenir ya da yenilenirse bu döküm de güncellenir.
   **Onarılmış kopyalar:** metin katmanı bozuk bir PDF'in ham dosyasına dokunulmaz. Onarılmış
   kopya `scripts/onar_metin_katmani.py` ile `kb/raw/_onarilmis/` altına üretilir (aynı girdiden
   hep aynı dosya çıkar); hangi belgenin onarılmış kopyadan okunacağı o belgenin `notlar`
   sütununda yazar. Bu klasör bir kayıt değildir, hash denetimine girmez.
3. **Yaş kapsamı** zorunlu: Faz 3'teki yaş-farkında filtre bu alanı kullanır. Bu sütun insan
   okuması içindir; filtrenin kullanacağı makinece okunur aralıklar bölüm düzeyinde
   `bolum_yas_haritasi.csv` dosyasında tutulur.
4. **Lisans/kullanım:** Kamu belgeleri için Bakanlık'a bilgi yazısı; dernek rehberleri için yazılı
   izin. İzin gelmeden belge `kb/processed/`'a alınmaz (`kb/raw/`'a indirilebilir).
5. **`erisim_tarihi`** dosyanın fiilen indirildiği gündür; indirme günü güncellenir.
6. **`durum`** yalnızca şu değerleri alır:

   | Değer | Anlamı |
   |---|---|
   | `araştırılacak` | Hangi belge/sürüm alınacağı henüz belli değil |
   | `indirilecek` | Belge belli, henüz `kb/raw/`'da değil |
   | `izin yazısı` | İzin/bilgi yazısı gönderilecek ya da yanıt bekleniyor |
   | `onaylı` | Kullanım hakkı net (izin geldi ya da lisans uygun), `hash` dolu |
   | `işlendi` | `kb/processed/` altında parçalanmış hâli var |

   `onaylı` ve `işlendi` durumundaki her satırın `hash` değeri dolu olmalıdır. Grup kayıtları
   (`çeşitli`) için izin yazısından önce gruptaki rehberlerin tek tek adı `notlar`'a yazılır.
