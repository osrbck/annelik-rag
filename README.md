# Annelik Asistanı — RAG Tabanlı, Güvenlik Katmanlı Soru-Cevap Çerçevesi

Yüksek lisans tezi (Mersin Üniversitesi, EEM). Gebelikten 18 yaşa kadar anneye eşlik eden
mobil asistanın **yaş-farkında, modüler RAG çekirdeği** ve **deterministik tıbbi güvenlik katmanı**.

## Depo yapısı

| Klasör | İçerik | Faz |
|---|---|---|
| `kb/raw/` | Orijinal rehber PDF'leri (git'e girmez, `.gitignore`) | 0 |
| `kb/registry/` | Belge kayıt defteri: kaynak, sürüm, lisans, yaş kapsamı | 0 |
| `kb/processed/` | Parçalanmış + yaş etiketli metin (JSONL) | 2–3 |
| `eval/datasets/` | S-ANA, S-YAS, S-TUZ, S-ADV test setleri | 1–4 |
| `eval/runner/` | Konfigürasyon-bağımsız değerlendirme koşturucusu | 1 |
| `eval/results/` | Tarih damgalı ham çıktılar ve metrik tabloları | 1+ |
| `rag/loaders/` | PDF / tablo / kayıt yükleyicileri | 2 |
| `rag/core/` | Chunker, Embedder, VectorStore, Retriever, Reranker, Generator arayüzleri | 2–3 |
| `safety/` | Girdi sınıflandırıcı, çıktı denetleyici, kırmızı bayrak sözlüğü | 4 |
| `app/api/` | FastAPI servis | 6 |
| `app/mobile/` | Flutter / RN istemci | 6 |
| `configs/` | K0–K4 konfigürasyon dosyaları | 1+ |
| `docs/ethics/` | Etik kurul başvurusu, onam/uzman formları | 0 |
| `docs/thesis/` | Tez bölümleri, protokol, toplantı notları | 0+ |

## Konfigürasyonlar

| Kod | Tanım |
|---|---|
| K0 | Çıplak LLM (bilgi tabanı yok) |
| K1 | Düz RAG (yaş filtresi yok) |
| K2 | Yaş-farkında RAG |
| K3 | K2 + tıbbi güvenlik katmanı |
| K4 | K3, yerel kuantalanmış model |

## Kurallar
- `kb/raw/` ve `eval/results/raw/` git'e girmez; her ikisi de yerel yedeklenir.
- Her koşum `configs/` altındaki dosyanın hash'i ve tarih damgasıyla kaydedilir.
- Test setlerinin %10'u `dev/`, %90'ı `test/` — `test/` yalnızca nihai değerlendirmede kullanılır.
- Gerçek anne-çocuk verisi hiçbir zaman depoya girmez; tüm profiller sentetiktir.
