# Belge kayıt defteri

Her belge için `belge_kayit_defteri.csv`'de bir satır. Kurallar:
1. **Sürüm sabitleme:** İndirilen PDF'in SHA-256'sı `hash` sütununa eklenir (`scripts/hash_kb.py`).
2. **Yaş kapsamı** zorunlu: Faz 3'teki yaş-farkında filtre bu alanı kullanır.
3. **Lisans/kullanım:** Kamu belgeleri için Bakanlık'a bilgi yazısı; dernek rehberleri için yazılı izin. İzin gelmeden belge `kb/processed/`'a alınmaz.
4. `durum` değerleri: `araştırılacak` → `indirilecek` → `izin yazısı` → `onaylı` → `işlendi`.
