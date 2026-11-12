# Annelik Asistanı — RAG Tabanlı, Güvenlik Katmanlı Soru-Cevap Çerçevesi

Yüksek lisans tezi (Mersin Üniversitesi, EEM). Gebelikten 18 yaşa kadar anneye eşlik eden
mobil asistanın **yaş-farkında, modüler RAG çekirdeği** ve **deterministik tıbbi güvenlik katmanı**.

## Depo yapısı

| Klasör | İçerik | Faz |
|---|---|---|
| `kb/raw/` | Orijinal rehber PDF'leri (git'e girmez, `.gitignore`) | 0 |
| `kb/registry/` | Belge kayıt defteri: kaynak, sürüm, lisans, yaş kapsamı | 0 |
| `kb/processed/` | Parçalanmış + yaş etiketli metin (JSONL) | 2–3 |
| `eval/datasets/` | S-ANA, S-YAS, S-TUZ, S-ADV setleri (`dev.jsonl`, `test.jsonl`) | 1–3 |
| `eval/runner/` | Konfigürasyon-bağımsız değerlendirme koşturucusu | 1 |
| `eval/judge/` | Hakem model istemi ve kural tabanlı tarama | 1 |
| `eval/results/` | Tarih damgalı ham çıktılar ve metrik tabloları | 1+ |
| `rag/loaders/` | PDF / tablo / kayıt yükleyicileri | 2 |
| `rag/core/` | Chunker, Embedder, VectorStore, Retriever, Reranker, Generator arayüzleri | 2–3 |
| `safety/` | Girdi sınıflandırıcı, çıktı denetleyici, kırmızı bayrak sözlüğü | 4 |
| `app/api/` | FastAPI servis | 6 |
| `app/mobile/` | Flutter / RN istemci | 6 |
| `configs/` | K0–K4 konfigürasyon dosyaları | 1+ |
| `docs/ethics/` | Etik kurul başvurusu, onam/uzman formları | 0 |
| `docs/thesis/` | Tez bölümleri, değerlendirme protokolü, sapma günlüğü, toplantı notları | 0+ |
| `scripts/` | Bilgi tabanı hash'leme, güç analizi | 0+ |

## Konfigürasyonlar

| Kod | Tanım |
|---|---|
| K0 | Çıplak LLM (bilgi tabanı yok) |
| K1 | Düz RAG (yaş filtresi yok) |
| K2 | Yaş-farkında RAG |
| K3 | K2 + tıbbi güvenlik katmanı |
| K4 | K3, yerel kuantalanmış model |

Her konfigürasyon bir öncekinden tek bir bileşenle ayrılır; ayrıntı ve K4 için yorum sınırı: [değerlendirme protokolü](docs/thesis/degerlendirme_protokolu.md) §2.

## Değerlendirme

Hipotezler, veri seti tanımları, ölçütler, puanlama ve istatistik [docs/thesis/degerlendirme_protokolu.md](docs/thesis/degerlendirme_protokolu.md) içinde sabitlenir. Örneklem büyüklüklerinin gerekçesi: `python scripts/guc_analizi.py`.

## Kurallar
- `kb/raw/` ve `eval/results/raw/` git'e girmez; her ikisi de yerel yedeklenir. Ham sonuçların hash listesi (`eval/results/<koşum>.sha256`) git'e girer.
- Her koşumdan önce `python scripts/hash_kb.py --kontrol` temiz çıkmalıdır.
- Her koşum; konfigürasyon, veri seti ve bilgi tabanı hash'leri, git commit'i ve tarih damgasıyla kaydedilir.
- Dondurmadan sonraki her değişiklik `docs/thesis/sapma_gunlugu.md` dosyasına yazılır.
- Geliştirme yalnız `dev.jsonl` ile yapılır; `test.jsonl` bütün konfigürasyonlar dondurulduktan sonra **bir kez** koşturulur. `dev` ayrı yazılır, test setinden bölünmez (protokol §4).
- S-TUZ ve S-ADV test bölmeleri, güvenlik katmanı (Faz 4) yazılmadan önce dondurulur.
- Gerçek anne-çocuk verisi hiçbir zaman depoya girmez; tüm profiller sentetiktir.
