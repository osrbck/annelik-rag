# Faz 0 — Kontrol Listesi (hedef: 2–3 hafta)

## Hafta 1
- [ ] Danışmanla 30 dk toplantı: uzman paneli için 2–3 isim (çocuk sağlığı, kadın-doğum, ebe)
- [ ] Etik kurul başvurusu: `docs/ethics/etik_basvuru_taslagi.md` → resmi forma aktar, imzaya sun
- [ ] Belge kayıt defterindeki 8 kaydı indir → `kb/raw/` (tek dosya: `<belge_id>.<uzantı>`; birden çok dosya: `<belge_id>/` klasörü), hash'le (`scripts/hash_kb.py`)
- [ ] Grup kayıtlarında (TND, TPK, emzirme rehberleri) alınacak rehberleri tek tek belirle, adlarını `notlar`'a yaz
- [ ] Aşı takviminin **2026 güncel** sürümünü asi.saglik.gov.tr üzerinden doğrula (eski PDF kullanma)

## Hafta 2
- [ ] Dernek rehberleri (TND, TPK) için kullanım izni e-postası gönder (şablon: `docs/ethics/izin_talebi_sablonu.md`)
- [ ] Her belgenin bölüm başlıklarını çıkar → yaş kapsamı etiketleme taslağı (`kb/registry/bolum_yas_haritasi.csv`)
- [ ] Depo: Python ortamı (`sudo apt install python3.12-venv` gerekli — bu makinede `venv`/`pip` kurulu değil), `requirements.txt`, ilk `configs/K0.yaml`
- [ ] Uzman panelini ilk e-postayla bilgilendir (yük: kişi başı en çok 6 saat; takvim: Faz 1 sonu ~20 dk, Faz 3 sonu ~2 saat, Faz 6 ~3 saat)

## Hafta 3 (tampon)
- [ ] Danışmana Faz 0 özeti: belge listesi + etik durumu + panel durumu
- [ ] Danışmana değerlendirme protokolünü sun (`docs/thesis/degerlendirme_protokolu.md`); §12'deki açık kararları kapat
- [ ] Faz 1 planı: değerlendirme koşturucusu iskeleti + ilk 30 soru (dev çekirdeği)

## Çıkış kriteri
Etik başvurusu verildi · 8 kayıt indirildi ve hash'lendi (`python scripts/hash_kb.py --kontrol` temiz) · en az 2 uzmandan sözlü "evet" · değerlendirme protokolü danışmanca onaylandı · depo çalışır durumda.
