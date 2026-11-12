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
