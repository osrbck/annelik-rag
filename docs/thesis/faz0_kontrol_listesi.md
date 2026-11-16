# Faz 0 — Kontrol Listesi (hedef: 2–3 hafta)

## Hafta 1
- [ ] Danışmanla 30 dk toplantı: uzman paneli için 2–3 isim (çocuk sağlığı, kadın-doğum, ebe)
- [ ] ~~Etik kurul başvurusu~~ — **askıda (2026-11-12):** çalışma şu an seminer aşamasında; başvuru tez dönemine ertelendi. Taslak `docs/ethics/` altında hazır duruyor. Uzman oturumları ve nihai koşum etik karardan sonra yapılır (protokol §6.3)
- [ ] Belge kayıt defterindeki 9 kaydı indir → `kb/raw/` (tek dosya: `<belge_id>.<uzantı>`; birden çok dosya: `<belge_id>/` klasörü), hash'le (`scripts/hash_kb.py`)
  - 2026-11-13: 6/8 indirildi ve hash'lendi (MoH-BCE-2018, MoH-DOB-2018, MoH-ASI-2026, WHO-GROWTH, MoH-TUBER, MoH-ANNE-SUTU). MoH-BCE-2018 ve MoH-TUBER için kayıtlı ilk adresler tanıtım sunumu çıktı; defterde düzeltildi. TND ve TPK izin e-postasından sonra
  - 2026-11-16: 7/9. Doğum Sonu Bakım Yönetim Rehberi eklendi (MoH-DSB-2014; protokol karar 13). 2014 baskısıdır; 2018 baskısı Bakanlığa yazılacak bilgi yazısında istenecek. Metin onarılmış kopyadan okunur (üç harf yanlış eşlenmişti)
- [ ] Grup kayıtlarında (TND, TPK, emzirme rehberleri) alınacak rehberleri tek tek belirle, adlarını `notlar`'a yaz
- [x] Aşı takviminin **2026 güncel** sürümünü asi.saglik.gov.tr üzerinden doğrula (eski PDF kullanma) — 2026-11-13: aşı kartı "1 Eylül 2026 tarihi itibarıyla güncellenmiştir" notunu taşıyor; suçiçeği 2. dozu 48. ayda

## Hafta 2
- [ ] Dernek rehberleri (TND, TPK) için kullanım izni e-postası gönder (şablon: `docs/ethics/izin_talebi_sablonu.md`)
- [ ] Her belgenin bölüm başlıklarını çıkar → yaş kapsamı etiketleme taslağı (`kb/registry/bolum_yas_haritasi.csv`)
- [ ] Depo: Python ortamı (`sudo apt install python3.12-venv` gerekli — bu makinede `venv`/`pip` kurulu değil), `requirements.txt`, ilk `configs/K0.yaml`
- [ ] Uzman panelini ilk e-postayla bilgilendir (yük: kişi başı yaklaşık 3 saat 30 dk; üç oturum: ~30 dk, ~2 saat, ~1 saat) — etik karardan sonra

## Hafta 3 (tampon)
- [ ] Danışmana Faz 0 özeti: belge listesi + etik durumu + panel durumu
- [ ] Danışmana değerlendirme protokolünü sun (`docs/thesis/degerlendirme_protokolu.md`); götürülecek başlıklar §12'nin sonunda (v1.1–v1.2 değişiklikleri); §12'deki açık kararları kapat
- [ ] Faz 1 planı: değerlendirme koşturucusu iskeleti + ilk 30 soru (dev çekirdeği)

## Çıkış kriteri
Etik başvurusu askıda (tez dönemi) · 8 kayıt indirildi ve hash'lendi (`python scripts/hash_kb.py --kontrol` temiz) · değerlendirme protokolü danışmanca onaylandı (2026-11-12) · depo çalışır durumda.
