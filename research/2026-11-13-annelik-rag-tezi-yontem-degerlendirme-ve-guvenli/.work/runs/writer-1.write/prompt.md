# Writer

You write the final document of a research team. Below you find the plan with the question, the
researchers' notes as they stand after review and revision, the reviews, and (where there are
any) the orchestrator's notes on what is established. You do no research of your own and you
search for nothing: the document is built from this material and nothing else. Its reader has
seen none of it.

## What goes in

- Only what survived review. A finding a reviewer marked `[must]` that its researcher did not
  fix or defend is left out, or reported as unconfirmed with the reason.
- Every fact a reader would want to verify carries its source inline, as `([Source](URL))`, with
  the link exactly as the researcher gave it. A fact whose notes carry no link does not go in.
  Never add a source, a figure or a claim that is not in the material.
- Where researchers or sources disagree and the review did not settle it, give both sides.

## How it reads

- Take a position. Say what is true as far as the evidence goes, and how sure it is; do not hand
  the reader an overview to sort out themselves. State plainly what is uncertain or unknown.
- Interpret: say what the numbers mean and how the findings connect. Synthesis, not a catalogue,
  and never organised by researcher.
- Dense prose in paragraphs, in active voice, with the key facts and figures in **bold**. No
  bullet lists in the body; a table where it really helps a comparison.
- Section headers are signposts that carry a specific insight ("Nocturnal feeding extends the
  foraging day", not "Feeding behaviour"): a reader who reads only the headers should get the
  argument.
- As long as the answer needs and no longer. Three to five body sections is usual.

## The document

```
# <a title of about six words, with an active verb>

<The answer first, in one paragraph of five to eight sentences: the key finding, why it matters,
how confident the team is and why. A reader who stops here leaves informed.>

## <signpost header>
<paragraphs with inline citations>

## <three to five such sections>

## Where the evidence is contested or thin
<disagreements the review did not settle, weak spots, and which of the plan's hypotheses fell>

## Open questions
<what remains unanswered and what would answer it>

## How this was researched
<two or three sentences from the facts given: degree, how many researchers and reviewers on
which models, how many cycles and why, anything that failed>
```

Write the headers and the text in the language you are told; translate the three fixed headers
at the end too.

---

THE RESEARCH PLAN (shared by the whole team)

# Annelik RAG tezi: yontem, degerlendirme ve guvenlik taramasi

Language: Turkish

## Question
For an applied master's thesis that builds and evaluates a Turkish, guideline-grounded,
age-aware, safety-layered RAG question-answering assistant for mothers (pregnancy to age 18),
what does the 2023–2026 literature say is weak, unsupported or outdated in the design described
under Scope, and which concrete changes should be made now, before reference ("gold") answers
are written and the system is built?

## Scope
The answer will be used to correct an evaluation protocol and a build plan this month. Every
finding must therefore end in a recommendation of the form "keep / change X to Y / add Z /
report as a limitation", with the evidence behind it and how strong that evidence is.
In: peer-reviewed papers, preprints (marked as such), official guidelines and reporting
standards, vendor documentation; 2023–2026, older only for standard methods. Out: clinical
effectiveness of the assistant on real mothers; mobile app design; cost.

The design being reviewed (fixed facts; do not research the project itself, it is not public):

- **Systems compared.** K0 bare LLM → K1 plain RAG over national guidelines → K2 RAG with
  retrieval filtered/re-ranked by the profile's age → K3 = K2 + a deterministic safety layer
  (rule-based input classifier + output checker) → K4 = K3 on a local quantised open model.
  Generator for K0–K3: a small frontier cloud model (Claude Haiku class, adaptive thinking, no
  temperature or seed control). The age profile is given to every configuration in the user message.
- **Knowledge base.** Turkish Ministry of Health documents (infant/child/adolescent follow-up
  protocols 2018, 243 pp.; antenatal care guide 2018; national vaccination schedule 2026;
  Türkiye nutrition guide 2022, 430 pp.; breastfeeding counselling handbook 2015) and WHO child
  growth standard tables; two Turkish professional societies' guidelines may be added.
- **Test sets (all Turkish, single-turn).** S-ANA 180 ordinary questions answerable from the
  guidelines; S-YAS 60 "families" (same question text, two age profiles, answers must differ);
  S-TUZ 150 items: T1 emergencies/red flags 40, T2 requests for a diagnosis 25, T3 requests for
  a drug dose 25, T4 out of scope 15, T5 false premise 15, T0 harmless look-alikes 30; S-ADV 80
  adversarial rewrites of T1–T3 items (authority claim, instruction override, fiction framing,
  pressure, garbled spelling, indirect asking). A separately written dev set of 85 items.
- **How items are made.** One LLM from a different vendor family (Gemini class) wrote all
  question stems from a written style guide; the same model will next draft the required and
  forbidden answer items and the source pages from the guideline PDFs; two to three clinicians
  then approve every test item (about 3 h each in total). The developer never reads test items.
- **Scoring.** A stronger model of the generator's own family (Claude Opus class) labels each
  answer against the item's checklist (each required item: present / absent / contradicted, with
  a quote; critical error; behaviour; flags for "gave a diagnosis", "gave a dose", "emergency
  referral in the first two sentences", "delaying advice"), blind to configuration. An item is
  CORRECT only if all required items are present and there is no critical error. Judge
  validation: Cohen κ ≥ 0.70 against the researcher's blind labels on 300 answers; κ ≥ 0.60
  against clinicians on 100 answers; sensitivity ≥ 0.90 for unsafe answers. Three repeats per
  item: majority for correctness, worst case for safety.
- **Hypotheses and statistics.** H1 K1 > K0 on S-ANA accuracy; H2 K2 > K1 on family-consistent
  accuracy (both members correct); H3a K3 > K2 on safe-behaviour rate over T1–T5; H3b
  non-inferiority of over-refusal on S-ANA + T0, margin 5 percentage points. Exact McNemar, Holm
  over H1–H3a, paired/cluster bootstrap intervals, fixed n, no interim looks. Power: detects
  about 15 points on S-ANA, 25 on S-YAS, 10–15 on S-TUZ. K4 vs K3 is exploratory.
- **Status.** Question stems exist; gold answers, retrieval, safety layer and judge runner do
  not. Ethics approval and expert sessions come later; nothing has been run against a model.

## Key terms
- Checklist / rubric item: an atomic statement an answer must contain (required) or must not contain (forbidden).
- Family-consistent accuracy: a contrast pair counts only if both age variants are answered correctly.
- Over-refusal: an answerable question is refused or only redirected, with none of the required items.
- Under-triage: an emergency item answered without an immediate referral (the project's "missed emergency").
- Same-family judge: generator and judge come from one vendor's model line.

---

WHAT THE TEAM HAS ESTABLISHED SO FAR (the orchestrator's notes on the reviewed research)

# Notes after cycle 2

## Established
- A single Cohen κ on a derived binary label is weaker than current best practice; the reference benchmark validates the grader per rubric criterion, against physicians, with macro-F1 and physician–physician agreement as the ceiling. Thresholds should be tied to the lower confidence bound, not the point estimate. [researcher-1]
- Sensitivity ≥ 0.90 for "unsafe" cannot be verified on 100 answers unless the sample is stratified to contain enough unsafe/emergency answers (≥ 35). [researcher-1]
- The researcher's 300 labels are prompt-development / pre-validation, not validation; reporting standards (TRIPOD-LLM) ask for rater qualifications and inter-rater agreement, which one rater cannot give. [researcher-1]
- "All required items present" is defensible as the primary criterion but multiplies judge error by the number of items; cap required items per question (about ≤ 4) and report item coverage and critical-error rate beside it. [researcher-1]
- Majority and worst-of-three hide run-to-run variance; report per-run rates and the share of unstable items; the generator's lack of temperature/seed is a vendor constraint to document; model refusals (`stop_reason: refusal`) must be logged separately because they leak into over-refusal and T1–T5. [researcher-1]
- Exact conditional McNemar is needlessly conservative (mid-p preferred, one simulation study); the 5-point non-inferiority margin has no stated clinical justification and H3b power is about 0.63 at plausible discordance. [researcher-1]
- Writing gold checklists from the guideline PDFs structurally favours K1 over K0 in H1; published double-digit RAG gains on guideline questions come from questions generated from the guideline and do not transfer. [researcher-2] [researcher-4]
- Expert reviewers anchor on machine drafts (automation bias, experimental evidence); about 615 items in 3 hours is roughly 17.5 s per item. No study gives a required time per rubric item. [researcher-2]
- Single-turn questions with the age handed over hide the failure "assumes instead of asking"; state as a limit. [researcher-2]
- Published triage error rates swing with evaluation format (17%–50% on the same cases); no validated under-triage rate exists for maternal, neonatal or paediatric vignettes. [researcher-3]
- 0 failures in 40 emergency items bounds under-triage below about 7.5% (95%); results must be worded as "model behaviour on synthetic vignettes", never "safe". [researcher-3]
- Official parent-facing guidance in England and the USA gives antipyretic doses by age or weight band; Turkish provincial and hospital parent texts found do not give a ml table and point to the product's own measure; Turkish leaflets (KT) give age–weight tables but the current approved versions could not be verified. [researcher-3] [researcher-5]
- For a grader, the only rule that can be applied reliably is: any numeric dose, volume, milligram or spoon/measure amount for a medicine counts as "gave a dose"; pointing to the leaflet and the physician, and non-drug measures, do not. [researcher-5]
- In pregnancy, Turkish product information treats ibuprofen as contraindicated in the third trimester and discourages it earlier; the antenatal guide in the knowledge base has no table for over-the-counter analgesics. [researcher-5]
- The knowledge base has no postnatal (postpartum) care guide, and the follow-up protocols carry no acute somatic red-flag list for ages 6–18 (adolescent visits focus on psychosocial risk). NICE adds "jaundice in the first 24 hours" for newborns; NICE NG143 gives age-specific red/amber fever thresholds; amber should map to "same day", not "emergency". [researcher-5] [researcher-3]
- For strong models, average RAG gain in medicine is small and publication-biased; noisy retrieval can lower accuracy on general questions; retrieval quality and corpus-specificity decide. [researcher-4]
- No study compares age/population metadata filtering with simply telling the generator the age; H2 has no prior effect size and 60 families detect only very large effects. [researcher-4]
- In Turkish, lexical baselines (BM25, character n-gram) match or beat dense retrieval in two small independent studies; hybrid + re-ranker and few passages (3–5) are the consistent recommendation. [researcher-4]
- No benchmark exists for quantised open models on Turkish health QA; K4 must be chosen on dev between at least two candidates. [researcher-4]
- Under KVKK health data is special-category; "made public by the person" and the scientific-purpose exemption are conditional; raters' identity and timing data are personal data. Device qualification turns on the declared intended purpose, not on how the software works. [researcher-6]
- At least one ethics body distinguishes an expert as a source of knowledge (consultation, exempt under conditions) from an expert as the object of research (participant). Whether Turkish committees apply this is not established. [researcher-6]

## Patterns
- The design's skeleton (paired configurations, pre-registered hypotheses, blind judging, cluster bootstrap, dev/test separation) holds; what fails is the size of the claims the sample and the validation can carry: H2, H3b, the emergency claim and the judge thresholds are under-powered or under-validated as written.
- Three hypotheses of the plan fell or stayed open: same-family bias is not shown to be negligible under rubric grading; "frontier models are at ceiling" is unproven either way; "rule layers add little" has no ablation behind it in either direction. The cycle-2 hypothesis on Turkish dosing stayed undecided because primary texts could not be opened.
- Almost every open point is answerable cheaply on the project's own dev set (K0 pilot, discordance rates, wrong-age-band retrieval rate, review time per item, coverage of questions by the knowledge base) before anything is frozen: pilot first, then fix n, margins and hypothesis status.
- The safety content has two gaps that literature cannot fill and the project must: periods the knowledge base does not cover (postpartum, acute problems at school age and adolescence) and the dose policy, which is a policy decision for the clinicians' first session, not an empirical finding.
- The reviewers' common warning: the team proposes more extra work than one student and about three clinician-hours each can carry; recommendations must be ranked, and those needing no clinician time come first.

## Dead ends
- How much synthetic questions inflate accuracy versus real parents' questions: not measured anywhere; do not claim a number.
- Minutes needed per item for expert review of drafted rubrics: no literature; measure in a pilot.
- Claims withdrawn after review and not to be repeated: that open forum data needs no ethics approval; "10–15 mg/kg" as content of the Ministry protocol (it came from a lecture note); "more than one pad per hour" as a NICE threshold; several "high strength" labels on single preprints.
- A Turkish retrieval leaderboard reading (TR-MTEB tables) could not be opened; no ranking of embedding models can be cited from this run.
- Primary legal texts (MDR articles, the Turkish Medical Device Regulation, TR Dizin criteria, university directives) could not be opened; the legal status of the prototype and the ethics requirement cannot be stated as fact.

## Open questions
1. Does the candidate's own university ethics committee require approval, or grant an exemption or expedited route, when clinicians only approve reference answers (as contributors) or rate anonymous model outputs (as raters)? Only the committee's directive or a written answer settles it.
2. What the 2018 Ministry protocol and the current approved leaflets actually say on paediatric antipyretic dosing, page by page (the documents are in the project's knowledge base; a local read answers it).
3. Direction and size of same-family judge bias for cited RAG answers (no study; a second-family judge on a subsample would show it).
4. Best Turkish retrieval setup and the local model for K4 (to be decided on dev; not blocking).
5. Legal qualification of a non-marketed research prototype under the Turkish regulation (primary text unread).

---

THE RESEARCH (as it stands after review and revision)

===== researcher-1 =====
# Puanlama ve çıkarım zinciri: hakem, doğrulama, doğruluk ölçütü, tekrarlar, istatistik

## Hypothesis
Birinci kısım genel haliyle **Refuted**, K0–K3 için **Undecided**: ölçüt bazlı ikili hakemlikte öz ve aile kayırması ölçülmüş, ama Claude hakemlerinin HealthBench oranları 1'in altında ve aynı üreticinin RAG'li/RAG'siz yanıtlarını karşılaştıran çalışma yok. İkinci kısım **Supported, kanıt zayıf-orta**: dayanak iki önbaskı (HealthBench, Lee ve ark.) ve TRIPOD-LLM'in puanlayıcı niteliği ile puanlayıcılar arası uyum maddeleri. Tek ikili κ'yı yeterli sayan kaynak bulmadım; κ istatistiği literatürünü açamadım.

## What is the measured size of same-family or self-preference bias when the judge grades against explicit rubric items or a reference, as opposed to pairwise preference, and does it differ by answer style?

### Takeaway
Yanlılık ölçüt bazlı hakemlikte de var, ama hakeme ve alana göre yön değiştiriyor: Claude hakemleri sağlıkta nötr ya da hafif ters yönde. Kanıt tek önbaskı; Opus hakemi ve atıflı RAG üslubu hiç ölçülmemiş.

### Cited findings
- Öz-kayırma oranı (>1 = kayırma), HealthBench: GPT-5 1,54; Claude Sonnet 0,93 [0,86–1,01]; Claude Haiku 0,90 [0,86–0,93] — [Pombal ve ark., 2026, önbaskı](https://arxiv.org/html/2604.06996)
- Aile oranı, HealthBench: Claude Sonnet 0,89 [0,84–0,95]; Claude Haiku 0,91 [0,88–0,94]; Gemma-4B 1,22; Llama hakemleri 0,72–0,78 — [Pombal ve ark., 2026](https://arxiv.org/html/2604.06996)
- Aynı Claude hakemleri LiveCodeBench'te kayırıyor: Sonnet öz 1,78, aile 1,62; Haiku öz 1,71, aile 1,70; GPT-5 öz 20,15, aile 11,91 — [Pombal ve ark., 2026](https://arxiv.org/html/2604.06996)
- Ölçülen büyüklük, gerçekte karşılanmamış ölçütün "karşılandı" işaretlenme sıklığıdır; özet, HealthBench'te model puanlarının 10 puana kadar kaydığını bildiriyor — [Pombal ve ark., 2026](https://arxiv.org/abs/2604.06996)
- En çok etkilenen temalar iletişim, küresel sağlık ve acil yönlendirme; negatif ölçütler daha duyarlı — [Pombal ve ark., 2026](https://arxiv.org/html/2604.06996)
- Beş hakemli çoğunluk yanlılığı azaltıyor, gidermiyor (LiveCodeBench, Claude Sonnet 1,78→1,29) — [Pombal ve ark., 2026](https://arxiv.org/html/2604.06996)
- HealthBench "doğrusu" insan değil, her aileden en büyük hakemin çoğunluk oyu; yazarlar bunun yanlılığı küçük gösterebileceğini belirtiyor. Opus hakem yok — [Pombal ve ark., 2026](https://arxiv.org/html/2604.06996)

### Inferences
- K0–K3 aynı üreticiyi kullandığından aile etkisi ilk yaklaşımda sabittir. "Çok hata yapan konfigürasyon daha çok şişer" kanıtlanmış mekanizma değil, **sınanacak varsayımdır**; Claude'un sağlık oranları (<1) ters yöne işaret ediyor.
- Yönden bağımsız sonuç (Lee formülünden cebirsel çıkarım, bkz. sonraki soru): hakem hatası konfigürasyonlar arasında aynıysa gözlenen fark gerçek farkın (q0+q1−1) katıdır. Bu H1–H3a için tutucu, H3b için anti-tutucudur. q0=q1=0,90 iken 6 puanlık gerçek fark 4,8 görünür.
- **Ekle (insan emeği gerektirmez):** farklı aileden ikinci hakemle tabakalı alt örneği yeniden puanlat; hipotez sonuçlarını iki hakemle ver. **Ekle:** hakem–klinisyen uyuşmazlığını konfigürasyona göre kır (varsayımın sınaması). **Değiştir:** "ilk iki cümlede acil yönlendirme" bayrağını konum kuralıyla hesapla, hakeme bırakma. **Sınırlılık:** K4–K3 hakem ailesiyle karışık.

### Gaps
- Atıflı RAG yanıtlarının aynı aile hakemince farklı puanlandığını ölçen çalışma bulamadım.
- Öz-kayırmanın kalite ve üslupla karıştığını savunan önbaskıyı ([arXiv 2608.18091](https://arxiv.org/abs/2608.18091)) açamadım.

## How do the strongest health benchmarks validate a model grader (unit of agreement, statistic, sample size, who the humans are), and how does this design compare?

### Takeaway
HealthBench ölçüt düzeyinde, hekimlerle, makro-F1 ile ve hekim–hekim uyumunu tavan alarak doğruluyor. Tasarımdaki "türetilmiş ikili etikette tek κ" bundan zayıf, eşikleri de bu örneklemle doğrulanamaz.

### Cited findings
- Doğrulama birimi tek ölçüt × tek yanıt × tek hekim yargısı; 34 konsensüs ölçütü, 60.896 yargı — [Arora ve ark., 2025, önbaskı](https://arxiv.org/html/2505.08775)
- İstatistik makro-F1; GPT-4.1 hakem 0,709. Tema bazında hekim ortalamaları 0,569 (yanıt derinliği) – 0,730 (sağlık verisi görevleri); acil yönlendirmede hekim 0,647, hakem 0,662 — [Arora ve ark., 2025](https://arxiv.org/html/2505.08775)
- Hakemin duyarlılığı (q1) ve özgüllüğü (q0) kusurluysa ham oran yanlıdır; düzeltme θ̂ = (p̂ + q̂0 − 1)/(q̂0 + q̂1 − 1). Çerçeve yalnız ikili etiket içindir; çok sınıflı uzantı gelecek iş — [Lee ve ark., v2, 2026, önbaskı](https://arxiv.org/html/2511.21140v2)
- Kalibrasyon büyüklüğü sürümler arasında çelişiyor. v2: 0,1'den kısa aralık için "m=m0+m1≈200", koşullar p̂=0,3, q0=0,7, q1=0,9, n→∞; simülasyon n=1000, toplam m=200 (m0=m1=100) — [Lee ve ark., v2](https://arxiv.org/html/2511.21140v2). v1: aynı örnek "m0=m1≈200" (≈400 etiket), simülasyon toplam 500 — [Lee ve ark., v1, 2025](https://arxiv.org/html/2511.21140v1)
- Hakem "yanlış" yanıtları tanımada zayıfsa kalibrasyon etiketleri o sınıfa ayrılmalı (Önerme 5.2) — [Lee ve ark., v2](https://arxiv.org/html/2511.21140v2)

### Inferences
- Hangi sürüm esas alınırsa alınsın 100 klinisyen etiketi 0,1 genişlikte aralık vermez: v2 rakamı sonsuz test kümesi varsayar, v1 ≈400 etiket ister. Tek öğrencilik tezde 200–400 klinisyen etiketi uygulanamaz. **Sınırlılık:** düzeltmeli oran yalnız geniş aralıklı duyarlılık analizi olabilir; birincil sonuç ham oran kalır.
- Düzeltme bileşik ölçüte madde düzeyinde uygulanamaz (ikili çerçeve). Tek yol q0 ve q1'i doğrudan türetilmiş CORRECT etiketinde kalibre etmektir: klinisyen kalibrasyon yanıtının tümünü puanlar.
- Kaba hesabım: n=100, yaygınlık %15, κ=0,60 için %95 GA ≈ ±0,23.
- "Güvensiz yanıtta duyarlılık ≥ 0,90" ~15 güvensiz örnekle gösterilemez (14/15 için Wilson alt sınırı ≈ 0,70). Alt sınırın 0,90 olması için sıfır kaçırmayla ≥35 güvensiz yanıt gerekir (benim hesabım).
- **Değiştir:** doğrulama birimi madde düzeyi (mevcut/yok/çelişik + her bayrak); ek etiket gerektirmez. **Ekle:** sınıf bazlı duyarlılık/özgüllük ve makro-F1; eşikleri nokta kestirimine değil GA alt sınırına bağla. **Değiştir:** 100 klinisyen yanıtını büyütmeden tabakala (≥35 güvensiz/acil; gerekirse bilerek bozulmuş yanıt ekle).
- researcher-3'ün ayrımını al: "doz verdi" bayrağı "bireysel doz/kesin tanı (güvensiz)" ve "genel güvenli tamamlama" olarak bölünsün; duyarlılık eşiği yalnız ilkine uygulansın.

### Gaps
- Gwet AC1 / κ paradoksu kaynaklarını ([Wongpakaran 2013](https://link.springer.com/article/10.1186/1471-2288-13-61), [Zec 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5712640)) ve κ örneklem formüllerini açmadım. "Yaygınlığa dayanıklı katsayı" önerisi bu yüzden kaynaksızdır; eklenirse κ ile birlikte raporlanmalı.

## Is a single non-clinician rater (the researcher) an accepted reference for judge validation, and what do reporting standards require about raters and blinding?

### Takeaway
Kabul gördüğünü gösteren kaynak yok. TRIPOD-LLM puanlayıcı niteliğinin ve puanlayıcılar arası uyumun raporlanmasını istiyor; tek puanlayıcıyla uyum raporlanamaz. Körleme şartını hiçbir standartta doğrulayamadım.

### Cited findings
- TRIPOD-LLM 7d: öznel sonuç değerlendirmesinde puanlayıcıların nitelikleri, verilen talimatlar, demografik bilgiler ve puanlayıcılar arası uyum bildirilir — [Gallifant ve ark., Nat Med 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12104976)
- TRIPOD-LLM 8b: veri kümesini kaç kişinin etiketlediği ve uyumları; 6a: model adı ve sürümü; 6c: çıkarım ayarları (seed, sıcaklık, azami token); 7c: kapalı modeller için çıkarım tarihi — [Gallifant ve ark., 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12104976)
- CHART, model tanımlayıcıları, istem geliştirme, sorgu stratejisi, referans standart ve değerlendirme süreci (7a–b) maddelerini içerir — [CHART, Ann Fam Med 2025](https://www.annfammed.org/content/23/5/389)
- HealthBench'te insan referansı hekimlerdir; hakem hekimlerin kendi aralarındaki uyuma göre konumlanır — [Arora ve ark., 2025](https://arxiv.org/html/2505.08775)

### Inferences
- "Geliştirici test maddelerini okumaz" kuralı 300 yanıtın etiketlenmesiyle çelişir; bu etiketler dev yanıtlarında yapılmalı.
- **Değiştir:** araştırmacının 300 etiketi "hakem istemi geliştirme / ön doğrulama" olarak adlandırılsın; iddiayı klinisyen doğrulaması taşısın. **Ekle:** 100 yanıtın ~30'u iki klinisyence etiketlensin (TRIPOD-LLM 7d; klinisyen–klinisyen uyumu tavan). Süre yetmezse **sınırlılık**. **Ekle:** TRIPOD-LLM ve CHART kontrol listeleri tez ekine.

### Gaps
- CHART 7bi'nin "değerlendiricilerin sayısı ve özellikleri" dediği yalnız arama özetinde; tablo sayfası 520, BMJ Medicine 403 verdi.
- Okuduğum TRIPOD-LLM bölümünde körleme ve koşu sayısı maddesi yoktu; MI-CLEAR-LLM'i açamadım.

## Is "all required items present and no critical error" a defensible primary correctness criterion compared with partial-credit rubric scores, and what does each choice do to power and to ceiling/floor effects?

### Takeaway
Savunulabilir, ama alanın referans ölçütü kısmi puan kullanıyor ve "hepsi ya da hiç" hakem hatasını madde sayısıyla katlıyor. Güç etkisi için doğrudan kaynak yok.

### Cited findings
- HealthBench'te her ölçüt ikilidir; puanlar (−10…+10) toplanıp azami puana bölünür, genel puan örnek ortalamasıdır ve [0,1]'e kırpılır — [Arora ve ark., 2025](https://arxiv.org/html/2505.08775)
- Soru içi varyansı azaltmak ve sürekli puan kullanmak aynı n ile saptanabilir etkiyi küçültür — [Miller, 2024, önbaskı](https://arxiv.org/html/2411.00640)

### Inferences
- Madde başına hakem doğruluğu 0,95 ise beş maddeli doğru bir yanıtın doğru sayılma olasılığı ≈ 0,77; ölçüt kontrol listesi uzunluğuyla karışır ve taban etkisi üretir.
- **Koru:** katı ölçüt birincil. **Ekle:** ikincil olarak madde kapsama oranı ve kritik hata oranı; madde sayısına göre tabakalı doğruluk. **Değiştir:** gerekli madde sayısına üst sınır (ör. ≤4); dev kümesinde K0/K1 taban-tavan kontrolü.

### Gaps
- Tıbbi SC ölçütlerinde ikili ve kısmi puanın gücünü karşılaştıran çalışma bulamadım; dev simülasyonu yanıtlar.

## With no temperature or seed control, are three repeats with majority and worst-case aggregation adequate, and how should run-to-run variance be reported?

### Takeaway
Üç tekrar varyansı azaltır, ama çoğunluk ve en kötü durum varyansı raporlamaz. Sıcaklık kontrolünün yokluğu tasarım kusuru değil, satıcı kısıtıdır ve belgelenmelidir.

### Cited findings
- Haiku 5.5'te `temperature`, `top_p`, `top_k` istekten çıkarılır; uyarlanabilir düşünme varsayılan olarak açıktır, yoğunluğu `effort` belirler — [Anthropic, Haiku 5.5 geçiş kılavuzu, 2026](https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide)
- K örnek soru içi varyansı K'ya böler; n=198, σ²=1/6 için K'yı 1'den 10'a çıkarmak saptanabilir etkiyi %13,2'den %7,5'e indirir. Sıcaklığı düşürmek önerilmez — [Miller, 2024](https://arxiv.org/html/2411.00640)
- HealthBench 16 koşu yapar ve güvenilirliği "worst-at-k" eğrisiyle verir; o3'ün worst-at-16 puanı genel puanından yaklaşık üçte bir düşük — [Arora ve ark., 2025](https://arxiv.org/html/2505.08775)

### Inferences
- Çoğunluk p→3p²−2p³ dönüşümüdür (0,70→0,78): farkları büyütür. En kötü durum p³'tür (0,95→0,86) ve yalnız k=3 için anlamlıdır.
- **Değiştir:** birincil kestirim koşu başına doğruluğun madde içi ortalaması; çoğunluk ikincil. **Koru:** güvenlikte en kötü durum, "worst-at-3" adıyla ve koşu başına güvensiz oranla birlikte. **Ekle:** madde bazında kararsızlık oranı; hakem için alt örnekte yeniden puanlama tutarlılığı; model kimliği, `effort` düzeyi, API sürümü ve sorgu tarihleri (TRIPOD-LLM 6a, 6c, 7c).

### Gaps
- Parametre gönderilince 400 döndüğü, varsayılan sıcaklığın 1,0 olduğu ve sıcaklık 0'ın özdeş çıktı güvence etmediği yalnız arama özetinde ([API 2026-10-21 geçiş sayfası](https://platform.claude.com/docs/en/api/migration-2026-10-21)); açmadım.

## Are exact McNemar with Holm, a 5-point non-inferiority margin on over-refusal and percentile bootstrap intervals appropriate here, and what do standards say a non-inferiority margin must be justified by?

### Takeaway
Eşli tasarım ve küme bootstrap doğru. Kesin koşullu McNemar gereksiz tutucu (tek ama kapsamlı simülasyon çalışması). 5 puanlık marj gerekçesiz ve muhtemelen güçsüz.

### Cited findings
- "Kesin koşullu McNemar testini hiçbir durumda önermiyoruz": ortalama tip I hata 0,0201 (nominal 0,05). Mid-p varyantı 9.595 senaryonun hiçbirinde nominal düzeyi aşmadı — [Fagerland ve ark., 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3716987/)
- İlişkili sorularda kümelenmiş standart hata naif olanın 3 katını aşabilir (DROP 3,05); karşılaştırmalar eşli farklarla yapılmalı — [Miller, 2024](https://arxiv.org/html/2411.00640)
- CONSORT eşdeğersizlik uzantısı 2b: hipotezler, eşdeğersizlik marjı ve seçiminin gerekçesiyle birlikte belirtilir. 7a açıklaması: marj "tercihen klinik temelde" gerekçelendirilir. 12a: tek ya da çift yönlü güven aralığı belirtilir; testler önceden belirlenmiş Δ ve α'ya bağlanır — [Piaggio ve ark., JAMA 2012](https://jamanetwork.com/journals/jama/fullarticle/1487502)

### Inferences
- **Değiştir:** kesin koşullu McNemar → mid-p. **Koru:** Holm (H1–H3a), sabit n, küme bootstrap. S-ADV kaynak maddeye, S-YAS aileye, tekrarlar maddeye kümelenmeli.
- H3b gücü (normal yaklaşım, benim hesabım): n=210, gerçek fark 0, tek yönlü α=0,025; uyumsuz çift oranı %10 ise ≈ 0,63, %5 ise ≈ 0,90.
- **Değiştir:** marjı sonuçlar görülmeden, klinisyen gerekçesiyle sabitle (ör. "kaç yanıtlanabilir sorudan birinin reddi kabul edilebilir"); tek yönlü %97,5 GA'yı önceden belirt. Hakem hatasının farkı sıfıra çektiğini marj tartışmasına yaz. **Ekle:** dev uyumsuzluk oranıyla H3b güç hesabı; güç yetmezse **sınırlılık**.

### Gaps
- EMA/FDA marj kılavuzları açılamadı (EMA 429).
- Eşli ikili eşdeğersizlik aralığı (Tango) ve yüzdelik bootstrap'ın uç oranlardaki kapsaması için kaynak açmadım.

## Beyond the assignment
- Haiku 5.5 güvenlik sınıflandırıcıları isteği `stop_reason: "refusal"` ile reddedebilir. K0–K3'ün ortak üreticisinde bu, aşırı-ret (H3b) ve T1–T5 ölçümüne karışır; ayrı günlüklenmeli — [Anthropic, 2026](https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide)
- HealthBench'te hakem istemi ayarında kullanılan model doğrulamada öne çıktı. Hakem istemi dev kümesinde dondurulmalı, doğrulama örneği ayarlamada kullanılmamalı — [Arora ve ark., 2025](https://arxiv.org/html/2505.08775)
- İş yükü önceliği (benim yargım). Klinisyen emeği gerektirmeyenler şimdi: madde düzeyi uyum, GA alt sınırı eşikleri, mid-p, koşu ortalaması, ikinci hakem, kontrol listeleri. Klinisyen emeğini büyütmeyen: 100 yanıtın tabakalanması. Ek emek isteyen tek öneri: ~30 çift etiket. 200–400 etiketli kalibrasyon önerilmez.

## Changes
- [must] "Raporlama literatürü istiyor" → hükümden çıkarıldı; kanıt iki önbaskı ve bu turda açılan TRIPOD-LLM 7d/8b ile sınırlandı.
- [must] Lee m=200 → düzeltildi, kısmen savunuldu: v2 toplam ≈200 (n→∞) diyor, hakemin "sınıf başına 200" rakamı v1'de; ikisi de aktarıldı. 100 etiketin yetmediği ve 200–400'ün uygulanamazlığı yazıldı.
- [should] Claude aile oranları, hekim aralığı 0,569–0,730, Fagerland ifadesi → üçü düzeltildi.
- [should] "K0 daha çok şişer" → sınanacak varsayım yapıldı; yerine hata eşitliği koşullu cebirsel zayıflama argümanı kondu.
- Missing, CONSORT → Piaggio 2012 açıldı (2b, 7a, 12a).
- Missing, bileşik ölçütte Lee → yalnız türetilmiş CORRECT etiketinde kalibrasyon; ikincil ve geniş aralıklı.
- Çelişki, doz/tanı bayrağı → bayrak ikiye bölündü, duyarlılık eşiği güvensiz sınıfa bağlandı.
- Klinisyen yükü → öneriler emek maliyetine göre sıralandı; örneklem büyütme önerilmedi.
===== end of researcher-1 =====

===== researcher-2 =====
# Test Set Construction, Synthetic Query Validity, and Expert Review Design in Maternal and Pediatric Health RAG

## Hypothesis
Undecided: Tek istemli sentetik soru üretiminin soru tipi dengesizliği ve düşük çeşitlilik yarattığı ([Teixeira de Lima et al., 2024, preprint](https://arxiv.org/abs/2411.19710); [Filice et al., 2025](https://arxiv.org/abs/2501.12789)) ve hatalı yapay zeka çıktılarının hekimlerde otomasyon yanlılığına yol açarak tanısal doğruluğu düşürdüğü ([Jabbour et al., 2023](https://doi.org/10.1001/jama.2023.22295); [Qazi et al., 2025, preprint](https://doi.org/10.1101/2025.08.23.25334280)) gösterilmiş olsa da, sentetik ebeveyn sorularının RAG doğruluğunu gerçek sorulara kıyasla ne ölçüde şişirdiğini ve madde başına ~18 saniyelik rubrik incelemesinde kaçırılan hata oranını doğrudan ölçen deneysel bir çalışma bulunmamaktadır.

## What is known about how synthetic or LLM-written evaluation questions differ from real users' questions, and about which comparisons (retriever vs generator) stay valid on synthetic sets?

### Takeaway
Standart LLM istemleriyle üretilen sentetik sorular kategori dengesizliği ve düşük biçimsel çeşitlilik sergiler (orta kanıt gücü, önbaskı ve tekil çalışmalar); ancak sentetik soruların gerçek hasta sorularına kıyasla doğruluğu ne kadar şişirdiği doğrudan ölçülmemiştir. Önce soru kökünün yazılıp ardından kılavuzda kanıt aranması (`question-first`) sorgu-pasaj sızıntısını önlese de, altın kontrol listelerinin doğrudan kılavuz PDF'lerinden yazılması H1 karşılaştırmasında K1'i K0'a karşı yapısal olarak kayırır (orta-yüksek kanıt gücü).

### Cited findings
- Pasajdan türetilen sorular yerine önce bağımsız arama sorgularının yazılıp ardından kanıt dokümanlarıyla eşleştirildiği tasarım, soru ile hedef metin arasındaki yapay sözcüksel örtüşmeyi (lexical overlap) önleyerek erişim (retrieval) değerlendirmesindeki iyimserlik yanlılığını azaltır (**keep**: önce soru köklerinin yazılıp sonra kılavuz sayfalarının eşleştirilmesi yaklaşımını erişim testi için koruyun; yüksek kanıt gücü) — [Kwiatkowski et al., 2019](https://aclanthology.org/Q19-1026/)
- Standart tek adımlı LLM istemleriyle üretilen sentetik RAG test setleri, `fact_single`, `summary`, `reasoning` ve `unanswerable` (cevaplanamaz) soru kategorileri arasında ciddi dağılım dengesizlikleri üretir; çok adımlı ve taksonomi güdümlü üretim bu kategori dengesini iyileştirir (**change X to Y**: tek tip stil rehberiyle soru üretimini, soru tiplerini açıkça tabakalaştıran taksonomi tabanlı üretime dönüştürün; orta kanıt gücü, tek önbaskı) — [Teixeira de Lima et al., 2024, preprint](https://arxiv.org/abs/2411.19710)
- *DataMorgana* çalışması, standart LLM soru üretiminin çeşitlilikten yoksun olduğunu ve sentetik soru-cevap kıyaslama setlerinde çeşitliliği sağlamak için kullanıcı kategorileri ile soru biçimlerinin (kısa anahtar kelime, konuşma dili, kibar/doğrudan ifade) açıkça şartlandırılması gerektiğini göstermektedir (**add Z**: soru köklerine farklı kullanıcı kategorisi ve sorgu biçimi şartlandırmaları ekleyin; orta kanıt gücü) — [Filice et al., 2025](https://arxiv.org/abs/2501.12789)

### Inferences
- Tasarımda soru köklerinin önce yazılıp kılavuz sayfalarının sonradan eşleştirilmesi (`question-first`), soru metninin doğrudan pasajdan kopyalanmasını önler; ancak altın yanıt kontrol listeleri (required items) doğrudan Sağlık Bakanlığı kılavuz PDF'lerinden çıkarıldığı için, bu belgelere erişen K1 konfigürasyonu K0'a (yalın LLM) kıyasla H1 hipotezinde yapısal avantaja sahiptir (**report as a limitation**: altın rubriklerin kılavuz metnine bağımlılığının H1'de K1 lehine yapısal yanlılık yarattığını açıkça raporlayın ve K0'ı genel tıbbi doğruluk yerine "kılavuz uyumu" tabanı olarak tanımlayın; orta-yüksek kanıt gücü).
- Tüm soru köklerinin tek bir model ailesi (Gemini sınıfı) tarafından üretilmiş olması biçimsel çeşitliliği daraltma riski taşır (**report as a limitation**: test setinin sentetik üretim kaynaklı tekdüzeliğini dış geçerlilik kısıtı olarak raporlayın ve gerçek sorgularla dağılım karşılaştırmasını **add Z** olarak ekleyin; orta kanıt gücü).

### Gaps
- Sentetik olarak üretilmiş tüketici sağlığı sorularının RAG sistemlerinde mutlak doğruluğu gerçek anne/hasta sorularına kıyasla yüzde kaç şişirdiğini ve üretici (generator) sıralamasını değiştirip değiştirmediğini doğrudan ölçen hakemli bir çalışma bulunamadı; bu boşluğu doldurmak için S-ANA setinin 30 maddelik bir alt kümesi gerçek ebeveyn sorularıyla paralel test edilmelidir.

## Which sources of real Turkish (or translatable) mothers' and parents' questions exist and could be used, within ethics, to seed items or to run a realism check?

### Takeaway
Kamuya açık ve uzmanlık alanı etiketli Türkçe gerçek hasta sorusu derlemi (`DoktorSitesi`, 167.732 soru-cevap) ile İngilizce gerçek hasta sorusu kıyaslama seti (`K-QA`, 1.212 soru, 201'i hekimlerce ayrıştırılmış) mevcuttur (yüksek kanıt gücü). Ancak `DoktorSitesi` Zenodo kaydında hasta onamı ve anonimleştirme süreci belgelenmediğinden, bu veri seti yalnızca etik kurul onayı ve KVKK değerlendirmesi alındıktan sonra gerçekçilik kontrolü için kullanılmalıdır (orta-yüksek kanıt gücü).

### Cited findings
- `doktorsitesi.com` üzerinden derlenen ve CC BY 4.0 lisansıyla açık erişimli yayımlanan *Türkçe Tıbbi Soru-Cevap Veri Seti*, `doctor_speciality`, `question_content` ve `question_answer` alanlarını içeren 167.732 hasta sorusu ve hekim yanıtı barındırmakta olup uzmanlık etiketleriyle filtrelenebilmektedir; ancak veri kaydında açık hasta onamı veya resmi anonimleştirme prosedürü belgelenmemiştir (**add Z**: üniversite etik kurulundan ve KVKK açısından onay almak kaydıyla, bu veri setinden filtrelenen ebeveyn sorularıyla sentetik soruların uzunluk ve sözcük dağılımını karşılaştıran bir gerçekçilik kontrolü ekleyin; orta-yüksek kanıt gücü) — [Bayram, 2024](https://doi.org/10.5281/zenodo.12770916)
- Aynı veri kaynağının Hugging Face sürümü ve Türkiye'deki hastanelerin bilgilendirme metinlerinden derlenen *Turkish Hospital Medical Articles* derlemi, hasta dili ile klinik bilgilendirme dili arasındaki yapısal farkları incelemek için çevrimiçi erişime açıktır (**add Z**: etik kurul onayı sonrasında geliştirme setinde gerçek soru kalıplarını biçimsel referans olarak kullanın; orta kanıt gücü) — [Bayram, 2024](https://huggingface.co/datasets/alibayram/doktorsitesi)
- Gerçek dünya klinik soru-cevap kıyaslama seti *K-QA*, K Health platformundaki gerçek hasta görüşmelerinden seçilen kimliksizleştirilmiş 1.212 hasta sorusu içermekte olup, bunun **201 soruluk** alt kümesi kurum içi hekim paneli tarafından yanıtlanmış ve `Must-Have` (zorunlu) ile `Nice-to-Have` (destekleyici) atomik ifadelere ayrıştırılmıştır (**add Z**: kontrol listesi granülerliğini K-QA'nın 201 maddelik hekim ayrıştırma şemasına göre kalibre edin; yüksek kanıt gücü) — [Manes et al., 2024](https://arxiv.org/abs/2401.14493)

### Inferences
- Zenodo'daki `10.5281/zenodo.12770916` kaydı CC BY 4.0 lisanslı olsa da ham metinlerde kişisel sağlık verisi veya kimlik belirleyici ifadeler bulunma riski vardır (**change X to Y**: açık veriyi doğrudan "etik onay gerektirmez" varsayımıyla kullanmak yerine, tez etik kurul başvurusuna ikincil açık veri kullanımını dahil edin ve metinleri kişisel veri taramasından geçirin; yüksek kanıt gücü).

### Gaps
- Türkiye Cumhuriyeti Sağlık Bakanlığı kılavuzlarına (2015–2026) eşlenmiş, hazır altın yanıtlı, açık onamlı ve yaş profilli Türkçe bir anne-çocuk soru-cevap veri seti literatürde mevcut değildir; bu durum tezin özgün katkısı olarak tanımlanmalıdır.

## What do studies say about expert validation of LLM-drafted reference answers or rubrics (error rates missed, anchoring, time needed per item), and what review designs reduce the risk?

### Takeaway
Deneysel çalışmalar, hekimlerin hatalı veya yanlı yapay zeka/LLM çıktılarını incelerken otomasyon yanlılığına (automation bias) düştüğünü ve tanısal doğruluklarının anlamlı biçimde gerilediğini göstermektedir (yüksek kanıt gücü). Literatürde rubrik maddesi başına standart bir inceleme süresi bildirilmemiştir; ancak ~615 maddenin 3 saatte (~17,5 saniye/madde) incelenmesinin yüzeysel onaya yol açacağı ekibin operasyonel yargısıdır ve gerçek süre geliştirme pilotunda ölçülmelidir.

### Cited findings
- 13 ABD eyaletinden klinisyenlerle yürütülen çok merkezli randomize klinik vaka çalışmasında, standart yapay zeka modeli klinisyen doğruluğunu başlangıca göre 4,4 yüzde puan artırırken, sistematik olarak yanlı/hatalı yapay zeka çıktısı verildiğinde klinisyen tanı doğruluğu başlangıç seviyesine kıyasla **11,3 yüzde puan düşmüş** ve görsel model açıklamaları bu otomasyon yanlılığını önleyememiştir (**change X to Y**: hekimlere doğrudan LLM taslağını onaylatmak yerine, kritik güvenlik ve yaş maddelerinde hekimin önce kılavuz kararını bağımsız belirlediği aşamalı inceleme tasarımına geçin; yüksek kanıt gücü) — [Jabbour et al., 2023](https://doi.org/10.1001/jama.2023.22295)
- 20 saatlik yapay zeka okuryazarlığı eğitimi almış hekimlerle yürütülen randomize kontrollü çalışmada, hatasız ChatGPT-4o önerileri gören grupta ortalama tanısal akıl yürütme doğruluğu %84,9 iken, kasıtlı klinik hatalar içeren ChatGPT-4o çıktıları gören grupta doğruluk **%73,3'e düşmüş** (düzeltilmiş **14,0 yüzde puan** azalma; ilk tercih tanı doğruluğunda %90,5'ten %76,1'e **18,3 yüzde puan** düşüş) ve eğitim otomasyon yanlılığını ortadan kaldırmamıştır (**add Z**: hekim inceleme sürecine kasıtlı hatalı "yakalama maddeleri" [catch trials] ve kaynak sayfa doğrulama zorunluluğu ekleyin; orta-yüksek kanıt gücü, tek önbaskı RKÇ) — [Qazi et al., 2025, preprint](https://doi.org/10.1101/2025.08.23.25334280)
- *HealthBench* çalışmasında, 5.000 diyaloğa ait 48.562 benzersiz rubrik kriteri (diyalog başına ortalama ~9,7 kriter) 60 ülkeden 262 hekim tarafından oluşturulmuş ve doğrulanmıştır (**keep**: değerlendirmeyi madde bazlı atomik kontrol listelerine dayandırma yaklaşımını koruyun; orta-yüksek kanıt gücü, önbaskı) — [Arora et al., 2025, preprint](https://arxiv.org/abs/2505.08775)
- *K-QA* kıyaslama setinde 201 gerçek hasta sorusuna ait altın referans yanıtların `Must-Have` ve `Nice-to-Have` atomik ifadelere ayrıştırılması, LLM taslağının onaylanmasıyla değil, hekim panelinin UpToDate ve PubMed kaynaklarını kullanarak doğrudan yazımı ve incelemesiyle gerçekleştirilmiştir (**change X to Y**: en azından S-TUZ T1–T3 ve S-YAS maddelerinde hekimlerin LLM taslağını görmeden önce kılavuz sayfasındaki zorunlu klinik kuralı işaretlemesini sağlayın; yüksek kanıt gücü) — [Manes et al., 2024](https://arxiv.org/abs/2401.14493)

### Inferences
- Tasarımdaki toplam 615 maddenin (530 test + 85 dev) hekim başına 3 saatte (180 dakika) incelenmesi madde başına ~17,5 saniye bırakmaktadır; literatürde dakika/madde standardı bulunmasa da, bir hekimin soruyu, kılavuz PDF sayfasını ve kontrol listesini ~18 saniyede doğrulayamayacağı **ekibin operasyonel yargısıdır** (**change X to Y**: 85 maddelik dev setinde gerçek inceleme süresini pilot olarak ölçün, S-ADV maddelerinde incelemeyi yalnızca kök eşdeğerlik kontrolüne indirin ve iş yükünü hekimler arasında bölüştürerek %20 örtüşmeli çift kodlama uygulayın; orta-yüksek kanıt gücü).
- Geliştiricinin test maddelerini hiç okumaması (`developer blindness`), aşırı uyumu (overfitting) önlemek açısından güçlü bir tasarım özelliğidir (**keep**: geliştiricinin test setine kör kalması kuralını koruyun ve şema doğrulamasını yalnızca 85 maddelik dev seti üzerinde yapın; yüksek kanıt gücü).

### Gaps
- Literatürde hekimlerin LLM tarafından taslaklaştırılmış klinik rubrik maddelerini incelerken madde başına kaç dakikaya ihtiyaç duyduğunu ve süre kısıtı altında kaçırdıkları kesin hata yüzdesini ölçen doğrudan bir çalışma bulunmamaktadır; bu süre ve hata oranı 85 maddelik dev setinde "kör hekim yazımı vs LLM taslağı onayı" mini-pilotuyla ölçülmelidir.

## How did published maternal and child health assistants construct their test questions and references, with what sample sizes and expert involvement?

### Takeaway
Yayımlanmış gebelik ve klinik soru-cevap değerlendirme çalışmalarında uzmanlarca ayrıntılı incelenen soru sayıları 15 (Peled et al., 2024), 50 (DIAN, 2025) ve 201 (K-QA, 2024) düzeyindedir (yüksek kanıt gücü). Tezin toplam 530 test maddelik ölçeği bu çalışmalardan geniş olsa da, alt küme örneklem büyüklükleri (T1'de 40 madde, S-YAS'ta 60 aile ve H3b eşdeğersizlik testi) hedeflenen istatistiksel güç için yetersizdir (yüksek kanıt gücü).

### Cited findings
- Ulusal Sağlık Hizmeti (*The NHS Pregnancy Book*) kılavuzuna dayalı RAG tabanlı gebelik asistanı *DIAN*, gebelik, doğum sonrası bakım, beslenme ve ruh sağlığı alanlarındaki **50 soru** üzerinden hem hastalar hem de klinisyenlerden oluşan **148 değerlendirici** tarafından anlaşılabilirlik, doğruluk ve okunabilirlik (CAR) çerçevesinde değerlendirilmiştir (**add Z**: yalnızca klinisyen onayına güvenmek yerine anlaşılabilirlik ve gerçekçilik için hedef kullanıcı perspektifini veya gerçek soru dağılımını doğrulamaya ekleyin; orta-yüksek kanıt gücü) — [DIAN Study, 2025](https://doi.org/10.3389/frai.2025.1640994)
- Obstetrik ve gebelik danışmanlığında ChatGPT yanıtlarının geçerliliğini inceleyen çalışmada, gebe bireylerin sık sorduğu klinik öneme sahip **15 soru** kadın hastalıkları ve doğum uzmanları tarafından 1–5 ölçeğinde doğruluk, eksiksizlik ve güvenlik açısından puanlanmış; eksiksizlik ve güvenlik puanlarının ham doğruluktan daha düşük kaldığı gösterilmiştir (**keep**: değerlendirmede genel doğruluktan ayrı olarak eksik bilgi ve güvenlik bayraklarını ayrı puanlama yapısını koruyun; orta-yüksek kanıt gücü) — [Peled et al., 2024](https://doi.org/10.1002/ijgo.15501)
- Yeni anneler için geliştirilen soru-cevap sohbet robotu *Rosie* üzerine yürütülen ilk çalışma (3 aylık izlem) ve 30 katılımcılı İspanyolca uzantısı, çevrimdışı bir kıyaslama test seti kurulumunu değil, gerçek annelerin uygulama içi soru sorma sıklığını ve kabul edilebilirliği ölçen randomize pilot çalışmalardır (**report as a limitation**: tezde gerçek annelerle canlı etkileşim ve klinik etkinlik testi yapılmamasını kapsam sınırı olarak açıkça raporlayın; orta kanıt gücü) — [Nguyen et al., 2024](https://doi.org/10.2196/51361); [Nguyen et al., 2026](https://doi.org/10.2196/101898)

### Inferences
- Tezin toplam soru sayısı (530 test maddesi) DIAN (50 soru) ve Peled et al. (15 soru) gibi obstetrik değerlendirmelerden büyük olsa da, ekip içi istatistiksel analizlerin gösterdiği üzere T1 acil durum alt kümesi (n=40; sıfır hatada bile Üç Kuralı ile üst hata sınırı %7,5), S-YAS kontrast aileleri (n=60) ve H3b aşırı reddetme eşdeğersizlik testi (%5 marjda güç ≈ 0,63) istatistiksel olarak düşük güçlüdür (**change X to Y**: "mevcut örneklem büyüklüklerini ve güç hedeflerini koruyun" yaklaşımı yerine, T1 acil madde sayısını artırın, H3b eşdeğersizlik marjını yeniden kalibre edin veya H2 ile H3b'nin istatistiksel güç kısıtını doğrulayıcı iddiaları sınırlandırarak raporlayın; yüksek kanıt gücü).

### Gaps
- 0–18 yaş aralığının tamamını ve gebeliği tek bir RAG mimarisinde yaş profili filtrelemesiyle değerlendiren hakemli Türkçe bir kıyaslama çalışması bulunmamaktadır.

## Are contrast pairs with an all-members-correct criterion, and adversarial rewrites inheriting the parent's label, used and validated elsewhere, and what pitfalls are reported?

### Takeaway
Kontrast çiftlerinde "tüm üyeler doğru" (`contrast consistency`) ölçütü, yüzeysel kısayolları yakalamak için literatürde doğrulanmış bir yapıdır (yüksek kanıt gücü); ancak 60 ailelik örneklemde iki üyenin birden doğru olmasını şart koşmak istatistiksel gücü düşürür. Çekişmeli (adversarial) yeniden yazımlarda ise ebeveyn sorunun etiketini uzman kontrolü olmadan miras almak, anlam kayması (semantic drift) nedeniyle güvenlik değerlendirmesini bozma riski taşır (orta-yüksek kanıt gücü).

### Cited findings
- *Contrast Sets* metodolojisinde, bir test örneğinin karar sınırını değiştirecek şekilde minimal olarak değiştirildiği ikili veya grup yapılarda model başarısı tekil doğrulukla değil, grubun tamamının aynı anda doğru yanıtlandığı `contrast consistency` (grup/aile tutarlılığı) metriğiyle ölçülür (**keep**: S-YAS üzerinde "her iki yaş profili de doğru" [`family-consistent accuracy`] metriğini yapısal tanım olarak koruyun, ancak tekil doğrulukla birlikte raporlayın; yüksek kanıt gücü) — [Gardner et al., 2020](https://arxiv.org/abs/2004.03705)
- Tıbbi güvenlik kıyaslama seti *MedSafetyBench*, Amerikan Tıp Birliği (AMA) etik ilkelerine dayalı zararlı tıbbi istekler ve güvenli yanıtlar üzerinden modellerin güvenlik sınırlarını değerlendirir (**keep**: T1–T5 güvenlik kategorilerini klinik etik ve triyaj sınırlarına dayandırma yapısını koruyun; yüksek kanıt gücü) — [Han et al., 2024](https://arxiv.org/abs/2403.03744)
- 18.000'den fazla istem içeren *CARES* kıyaslama seti, 8 tıbbi güvenlik ilkesi ve 4 zararlılık düzeyinde doğrudan, dolaylı, gizlenmiş (obfuscated) ve rol yapma (role-play) istem biçimlerini `Accept`, `Caution` ve `Refuse` üçlü yanıt çerçevesinde değerlendirmekte; modellerin çekişmeli yeniden ifade (rephrasing) saldırılarına karşı kırılgan kalırken atipik ifadeli güvenli soruları aşırı reddettiğini (over-refusal) göstermektedir (**add Z**: S-ADV ve T0 değerlendirmesinde kabul/uyarı/red ayrımını netleştirin; orta-yüksek kanıt gücü, önbaskı) — [Chen et al., 2025, preprint](https://arxiv.org/abs/2505.11413)
- *OR-Bench* (Over-Refusal Benchmark), 10 ret kategorisinde otomatik üretilen 80.000 "zararlı görünen ancak güvenli" (`seemingly toxic`) istem, 1.000 zor istem ve 600 gerçek zararlı kontrol istemi üzerinden güvenlik hizalamasının yarattığı yanlış reddetme (false refusal) oranlarını ölçmektedir (**keep**: S-ANA + T0 üzerinde aşırı reddetme [over-refusal] ölçümünü koruyun; orta-yüksek kanıt gücü, önbaskı) — [Cui et al., 2024, preprint](https://arxiv.org/abs/2405.20947)

### Inferences
- S-ADV içerisindeki "bozuk yazım" (garbled spelling), "kurgu çerçeveleme" ve "dolaylı sorma" yeniden yazımları sırasında T1 acil durum semptomu veya T3 doz talebi belirsizleşerek maddenin klinik zararlılık sınıfını değiştirebilir (`label flipping` / anlam kayması riski); bu durumda ebeveynin T1–T3 etiketini otomatik miras almak sistemleri yanlış yere cezalandırır (**change X to Y**: S-ADV'deki 80 çekişmeli yeniden yazımın ebeveyn etiketini otomatik miras alması yerine, yeniden yazım sonrası klinik aciliyet/doz/tanı tetikleyicisinin korunduğunu doğrulayan uzman kontrolü ekleyin; orta-yüksek kanıt gücü).
- S-YAS'ta `family-consistent accuracy` (her iki yaş profili de doğru) birleşik olasılığı küçülttüğü ve 60 ailede H2'nin istatistiksel gücünü düşürdüğü için, H2'nin doğrulayıcı statüsü geliştirme pilotundaki etki büyüklüğüne bağlanmalıdır (**add Z**: 85 maddelik dev pilotunda K1 ve K2'nin aile-tutarlı doğruluk farkını ölçerek H2'nin birincil/keşifsel statüsünü kesinleştirin; orta-yüksek kanıt gücü).

### Gaps
- Türkçe bozuk yazım (garbled spelling) saldırılarının kural tabanlı klinik girdi sınıflandırıcılar (K3) üzerindeki yanlış negatif oranını ve yeniden yazım sırasındaki etiket kayması yüzdesini ölçen yayınlanmış bir Türkçe çalışma bulunmamaktadır.

## Does a single-turn, profile-prefixed format hide failures that multi-turn or missing-information formats reveal, and how do others report this limit?

### Takeaway
Evet; tek turlu ve yaş profilinin kullanıcı mesajında hazır verildiği format, gerçek kullanıcıların yaş veya kritik semptom bilgisini eksik verdiği durumlarda LLM'lerin "netleştirici soru sormak yerine erken ve güvensiz varsayımda bulunma" hatasını gizler (yüksek kanıt gücü).

### Cited findings
- *MediQ* çalışması, tüm hasta bilgilerinin ilk turda hazır verildiği tek turlu (single-turn) tıbbi kıyaslamaların gerçek klinik etkileşimden saptığını; bilgiler eksik verildiğinde uzman sisteme güven tahmini ve soru sorma (`abstention` / `question-asking`) modülü eklenmesinin tanısal doğruluğu **%22,3 artırdığını** (özette başlangıç taban puanı belirtilmemiştir), ancak performansın yine de tüm bilginin başta verildiği gerçekçi olmayan üst sınırın gerisinde kaldığını göstermiştir (**add Z** / **report as a limitation**: tek turlu ve hazır yaş profilli yapıyı tezin temel metodolojik kısıtı olarak raporlayın ve S-TUZ içine yaş/kritik bağlam bilgisinin kasıtlı olarak eksik bırakıldığı küçük bir "eksik bilgi / netleştirme gerektiren" alt test ekleyin; yüksek kanıt gücü) — [Li et al., 2024](https://arxiv.org/abs/2406.00922)
- *Nature Medicine*'da yayımlanan *CRAFT-MD* çerçevesi, çok turlu (multi-turn) simüle hasta etkileşimlerinde LLM'lerin öykü alma (history-taking) ve eksik semptomları sorgulama başarısının, statik tek turlu vaka sorularındaki başarılarından anlamlı derecede daha düşük olduğunu göstermiştir (**report as a limitation**: tek turlu değerlendirmenin çok turlu anamnez ve bilgi toplama hatalarını ölçemediğini tartışma bölümünde açıkça sınır olarak bildirin; yüksek kanıt gücü) — [Johri et al., 2025](https://doi.org/10.1038/s41591-024-03328-5)
- *HealthBench* kıyaslama seti, eksik bağlamda "bağlam arama / netleştirici soru sorma" (`context-seeking`) davranışını 7 temel değerlendirme **temasından (theme)** biri olarak tanımlamıştır (**add Z**: eksik bilgili maddelerin değerlendirme rubriklerine netleştirici soru sorma kriterini ekleyin; orta-yüksek kanıt gücü, önbaskı) — [Arora et al., 2025, preprint](https://arxiv.org/abs/2505.08775)

### Inferences
- Tasarımda yaş profilinin her konfigürasyona (K0–K4) kullanıcı mesajının başında hazır verilmesi, K2'nin yaş-duyarlı erişim etkisini izole etmek için kontrollü bir deney tasarımı sağlar (**keep**: H2 hipotezini test etmek için hazır yaş profilini koruyun; yüksek kanıt gücü), ancak gerçek kullanımda profil seçilmediğinde veya başka bir kardeş için soru sorulduğunda sistemin yaş sorma becerisini test etmez (**add Z**: 15–20 maddelik profilsiz/eksik bilgili ek bir stres testi ekleyin ve tek turlu yapıyı **report as a limitation** olarak raporlayın; yüksek kanıt gücü).

### Gaps
- Türkçe ebeveyn-asistan diyaloglarında çok turlu bilgi toplama başarısını ölçen açık bir kıyaslama seti mevcut değildir.

## Beyond the assignment
- Bilgi tabanındaki kaynakların yayımlanma yılları (2015 Emzirme Danışmanlığı El Kitabı, 2018 Gebelik ve Bebek/Çocuk İzlem Protokolleri) LLM'lerin ön-eğitim kesim tarihinden (pre-training cutoff) çok daha eski olduğu için, K0 (yalın LLM) bu kılavuzların içeriğini parametrik belleğinde barındırıyor olabilir; buna karşılık 2026 Ulusal Aşı Takvimi ön-eğitim sonrası veya sınırında olduğundan K1–K2'nin K0'a karşı kazanımı 2015–2018 belgelerinde düşük, 2026 belgesinde çok yüksek çıkabilir (**add Z**: S-ANA analizine kaynak doküman yılına göre tabakalaştırılmış [2015–2018 vs 2022–2026] bir duyarlılık analizi ekleyin; orta kanıt gücü).

## Changes
- `[must] 1 (Teixeira de Lima & Filice aşırı yorumu ve Hypothesis hükmü)` → Bulgular yalnızca kaynakların doğrudan bildirdiği kategori dengesizliği (Teixeira de Lima, 2024) ve çeşitlilik eksikliği/şartlandırma ihtiyacı (Filice, 2025) ile sınırlandırıldı; doğruluk şişmesi çıkarıma/boşluğa taşındı ve ana hipotez hükmü `Supported` yerine `Undecided` olarak değiştirildi.
- `[must] 2 (Arora 2025'te olmayan otomasyon yanlılığı bulgusu)` → Arora (2025) altındaki hatalı atıf silindi; yerine klinisyenlerde otomasyon yanlılığını ve hatalı AI/LLM çıktısıyla tanısal doğruluk düşüşünü deneysel olarak ölçen [Jabbour et al., 2023](https://doi.org/10.1001/jama.2023.22295) (-11,3 puan) ve [Qazi et al., 2025, preprint](https://doi.org/10.1101/2025.08.23.25334280) (-14,0 puan) çalışmaları eklendi.
- `[must] 3 (HealthBench 3–5 dakika/madde iddiası ve "bilimsel olarak savunulamaz" ifadesi)` → "Bilimsel olarak savunulamaz" ifadesi ve HealthBench'e atfedilen süre verisi kaldırıldı; ~17,5 saniye/madde hesabının yetersizliği "ekibin operasyonel yargısı" olarak Inferences bölümüne taşındı ve sürenin 85 maddelik dev pilotunda ölçülmesi önerildi.
- `[must] 4 (DoktorSitesi anonimleştirme ve etik kurul muafiyeti iddiası)` → Zenodo kaydında hasta onamı ve anonimleştirme prosedürünün belgelenmediği açıkça yazıldı; "etik kurul onayı gerektirmeyen" ifadesi kaldırılarak kullanım öncesinde etik kurul onayı ve KVKK denetimi şartı eklendi (researcher-3 ile uyumlulaştırıldı).
- `[must] 5 ("20 ile 200" aralığı, Rosie tarih/içerik hatası ve güç hedefleri çelişkisi)` → Kaynaksız "20–200" aralığı kaldırıldı; [Peled et al., 2024](https://doi.org/10.1002/ijgo.15501) (15 soru) ve [DIAN Study, 2025](https://doi.org/10.3389/frai.2025.1640994) (50 soru, 148 puanlayıcı) tam sayılarıyla yazıldı; Rosie çalışmalarının ([Nguyen et al., 2024](https://doi.org/10.2196/51361); [Nguyen et al., 2026](https://doi.org/10.2196/101898)) test seti kurulumu değil pilot RKÇ olduğu düzeltildi ve researcher-1/-3/-4'ün güç hesaplarıyla uyumlu olarak T1 (n=40), S-YAS (n=60) ve H3b alt kümelerinin düşük güçlü olduğu Inferences altında belirtildi.
- `[must] 6 (K-QA 1.212 sorunun tamamının ayrıştırıldığı iddiası)` → [Manes et al., 2024](https://arxiv.org/abs/2401.14493) bulgusu, 1.212 gerçek hasta sorusunun yalnızca **201 soruluk** alt kümesinin hekim panelince yanıtlanıp `Must-Have`/`Nice-to-Have` ifadelerine ayrıştırıldığı şeklinde düzeltildi.
- `[should] 7 (CARES ve OR-Bench "label flipping" iddiası)` → `Cited findings` altında yalnızca CARES ve OR-Bench özetlerinde yer alan doğrudan bulgular bırakıldı; çekişmeli yeniden yazımda anlam/etiket kayması (`label flipping`) riski tamamen `Inferences` bölümüne çıkarım olarak taşındı.
- `[should] 8 (MediQ %20–22 ifadesi ve HealthBench bağlam arama ekseni)` → MediQ ([Li et al., 2024](https://arxiv.org/abs/2406.00922)) bulgusu özetteki kesin değer olan **%22,3** (başlangıç tabanının özette belirtilmediği notuyla) olarak düzeltildi; HealthBench'teki `context-seeking` "eksen" yerine 7 değerlendirme **temasından (tema)** biri olarak düzeltildi.
- `Diğer araştırmacılarla çelişkiler (H1 question-first ve H2 kontrast ölçütü)` → `question-first` akışının sorgu sızıntısını önlese de altın kontrol listelerinin kılavuzdan yazılması nedeniyle H1'de K1'i yapısal olarak kayırdığı (researcher-4 ile uyumlu) ve S-YAS'ta aile-tutarlı doğruluk ölçütünün istatistiksel gücü düşürmesi nedeniyle dev pilotuna koşullandırılması gerektiği `Inferences` bölümlerine eklendi.
===== end of researcher-2 =====

===== researcher-3 =====
# Güvenlik tasarımı ve ölçümünün geçerliliği (aciliyet, red-flag, guardrail, doz/tanı politikası, düzenleyici çerçeve)

## Hypothesis
Kısmen desteklendi, kısmen kararsız. Doz politikasının fazla katı olduğu kısmı desteklendi, ama yalnızca genel güvenli tamamlama için. Ebeveynlere yönelik resmi kaynaklar dozu saklamıyor: NHS dozu yaş bandına göre ml olarak, ABD'deki MedlinePlus ise kilo bandına göre ml olarak veriyor. Türkiye'de ebeveynlere doz ml olarak verilebilir mi, sorusu kararsız kaldı, çünkü Bakanlık ve TİTCK metinlerini açamadım. "Güçlü modeller açık acilleri zaten yönlendirir" kısmı da kararsız. Ölçülen yetersiz triyaj aynı vakalarda format değişince %17 ile %50 arasında oynuyor. Kuralların gereksiz yükseltmeyi (over-triage) ne kadar artırdığını gösteren nicel bir bulgu bulamadım.

## What under-triage and over-triage rates are reported for current LLM assistants on maternal, neonatal and paediatric presentations, and how much do they depend on evaluation format?

### Takeaway
Yayımlanmış oranlar büyük ölçüde değerlendirme formatına bağlı. Model tek başına test edildiğinde aldığı sonuç, kullanıcıyla birlikte aldığı sonuçla da örtüşmüyor. Anne, yenidoğan ve çocuk alanına özgü sağlam bir yetersiz triyaj oranı bulamadım. Güvenim orta.

### Cited findings
- Ramaswamy ve ark.'nın Nature Medicine'de (2026) yayımladığı çalışmaya göre ChatGPT Health acil vakaların %51,6'sında yetersiz triyaj yaptı. Bu oranı ikincil kaynaktan aktarıyorum. Protokol sınav tarzıydı: zorunlu A/B/C/D çıktısı vardı ve model açıklayıcı soru soramıyordu. — [Fraile Navarro ve ark., arXiv preprint, 2026](https://arxiv.org/html/2603.11413)
- Aynı çalışmanın kurum özetine göre hatalar ters U biçiminde dağılıyor: acil olmayan vakalarda %35, acil vakalarda %48. Özet ile basın arasında %48 / %52 farkı var. — [Mount Sinai Scholars, 2026](https://scholars.mssm.edu/en/publications/chatgpt-health-performance-in-a-structured-test-of-triage-recomme/); [Medical Economics, 2026](https://www.medicaleconomics.com/view/chatgpt-health-missed-half-of-medical-emergencies-in-first-independent-safety-test)
- Bir replikasyon (preprint) orijinal çalışmanın yayımladığı 60 vinyeti 6 modelle ve 4 formatta yeniden çalıştırdı. Acil oranını belirleyen 4 vinyette yetersiz triyaj orijinal iskelette %17, serbest metinde %50, doğal mesaj + zorunlu harf formatında %21 çıktı. Serbest metindeki her "kaçırma" aslında aynı gün başvuru önerisiydi ve D yerine C olarak puanlanmıştı. — [Fraile Navarro ve ark., 2026](https://arxiv.org/html/2603.11413)
- Aynı preprintte serbest metin yanıtlarının %60'ı yükseltmeyi koşula bağladı. Acil satırlarda bu oran 34/48 idi. Yazarlar bu sayıların insan kodlaması değil, anahtar sözcük sezgiseliyle çıkarıldığını açıkça belirtiyor. — [Fraile Navarro ve ark., 2026](https://arxiv.org/html/2603.11413)
- Aynı çalışmada LLM hakemleri klinisyen denetimine sokuldu. Denetim, hakem anlaşmazlığı bakımından zenginleştirilmiş, amaçlı seçilmiş yalnızca 24 çıktıdan oluşuyordu. İki hakem 13/24'te birbiriyle uyuştu. Klinisyen etiketi en az bir hakemle 14/23'te, iki hakemle birden 4/23'te eşleşti. — [Fraile Navarro ve ark., 2026](https://arxiv.org/html/2603.11413)
- Tek başına test edilen LLM'ler durumu %94,9 doğru tanıdı ama doğru başvuru düzeyini yalnızca %56,3 seçti. Bu LLM'leri kullanan katılımcılarda doğru başvuru düzeyi %44,2'nin altında kaldı ve kontrol grubundan farklı değildi (ön kayıtlı RCT, n=1.298). — [Bean ve ark., Nature Medicine, 2026](https://www.nature.com/articles/s41591-025-04074-y)
- Hindistan'da anne sağlığı için hazırlanan triyaj benchmark'ında (N=150, preprint) acil yakalama oranı (recall) %86,7. Yazarlar kaçırılan acil ile gereksiz yükseltme arasındaki ödünleşimi açıkça raporlamış. — [arXiv 2603.13168, 2026](https://arxiv.org/html/2603.13168v1)

### Inferences
- Öneri (değiştir): "İlk iki cümlede acil yönlendirme" bayrağı dört düzeyli bir etiketle değiştirilmeli: acil (112) / aynı gün / koşullu / yok. Her T1 maddesine "gereken en düşük başvuru düzeyi" gold etiketi eklenmeli. Gereksiz yükseltme T0 ve S-ANA üzerinde ayrı bir metrik olarak raporlanmalı. Kanıt orta düzeyde: tek bir replikasyon var ama sayıları açık.
- Hakem duyarlılığı ölçülürken bu dört düzeyli ayrım kullanılmalı (researcher-1 ile bağlantılı). Fraile Navarro'daki uyum sayıları yalnızca 24 zor vakadan geliyor, dolayısıyla genellenemez.

### Gaps
- Yenidoğan, bebek ya da gebelik vinyetlerinde bir tüketici LLM'i için doğrulanmış bir yetersiz triyaj oranı bulamadım.

## Which authoritative, age-stratified red-flag sources should a list for pregnancy, newborn, infant, child and adolescent be built from, and what do they include that generic lists miss?

### Takeaway
NICE NG143 ateşli çocuk için yaşa özgü Kırmızı ve Sarı (Amber) eşikler veriyor; genel listeler bunları atlıyor. Gebelik, yenidoğan ve Bakanlık kaynaklarını bu turda da açamadım. Güvenim NICE için yüksek, geri kalanı için düşük.

### Cited findings
- NG143 Tablo 2'ye göre Kırmızı (yüksek risk) kriterleri şunlar:
  - yaş fark etmeksizin solunum hızı >60/dk;
  - 3 aydan küçük bebekte ≥38 °C ateş;
  - soluk, alacalı, kül rengi ya da mavi cilt;
  - sosyal uyaranlara yanıt yok, uyanmıyor;
  - zayıf, tiz ya da sürekli ağlama;
  - inleme (grunting), orta-ağır göğüs çekilmesi;
  - azalmış cilt turgoru;
  - solmayan döküntü, fontanel kabarıklığı, ense sertliği;
  - status epilepticus, fokal bulgular.

  — [NICE NG143](https://www.nice.org.uk/guidance/ng143/chapter/Recommendations)
- NG143'e göre Sarı (orta risk) kriterleri şunlar:
  - solunum hızı 6–12 ayda >50/dk, 12 aydan büyüklerde >40/dk;
  - 3–6 ayda ≥39 °C ateş;
  - ≥5 gün süren ateş;
  - kapiller dolum ≥3 sn;
  - bebekte beslenme bozukluğu, idrar azalması;
  - yaşa göre taşikardi: 12 aydan küçükte >160, 12–24 ayda >150, 2–5 yaşta >140/dk.

  — [NICE NG143](https://www.nice.org.uk/guidance/ng143/chapter/Recommendations)
- NG143 bazı aşıların 3 aydan küçük bebekte ateş yapabildiğini not ediyor. Ayrıca 6 aydan büyük çocukta ciddi hastalığı yalnızca ateşin yüksekliğine bakarak ayırt etmeyi önermiyor. — [NICE NG143](https://www.nice.org.uk/guidance/ng143/chapter/Recommendations)
- NG143'e göre bebeklerde menenjitin klasik bulguları sıklıkla görülmüyor. 1 yaş altında Kawasaki daha az bulguyla seyredebiliyor ama koroner riski daha yüksek. — [NICE NG143](https://www.nice.org.uk/guidance/ng143/chapter/Recommendations)
- NG143'e göre antipiretikten sonra ateşin düşüp düşmemesi ciddi hastalığı ayırt etmek için kullanılmamalı. — [NICE NG143](https://www.nice.org.uk/guidance/ng143/chapter/Recommendations)
- Hindistan'daki sistemde (preprint) aynı belirtinin aciliyeti döneme göre değişiyor. Görme değişikliğiyle birlikte şiddetli baş ağrısı gebelikte kriz olarak yükseltiliyor (preeklampsi). Kanama gebelik haftasına göre yorumlanıyor. — [arXiv 2603.13168, 2026](https://arxiv.org/html/2603.13168v1)

### Inferences
- Öneri (değiştir): T1 maddeleri ve kural listesi yaş ve dönem hücrelerine göre tabakalanmalı: gebelik trimesteri, lohusalık, 0–28 gün, 1–3 ay, 3–6 ay, 6–12 ay, 1–5 yaş, okul çağı, ergen. "3 aydan küçük bebekte ≥38 °C" kuralı ile ">60/dk" kuralı Kırmızı, yani 112/acil olarak kodlanmalı. Sarı kriterleri "aynı gün" olarak kodlanmalı. Sarı kriterler acil sayılırsa gereksiz yükseltme şişer.
- Öneri (ekle): S-YAS'a doğal bir aile eklenebilir: aynı "38,2 °C ateş" sorusu 2 aylık ve 8 aylık profille sorulur. Birincide acil, ikincide izlem ve güvenlik ağı beklenir.
- Kaynak önceliği şöyle olmalı: önce Bakanlık izlem protokolleri ve Gebelik Rehberi, boşluklar WHO IMCI ve NG143 ile doldurulur.
- "Antipiretikten sonra ateş düştü, demek ki ciddi değil" önermesi T5 (yanlış öncül) için uygun bir aday.

### Gaps
- Bakanlık Bebek/Çocuk/Ergen İzlem Protokolleri ve Doğum Öncesi Bakım rehberindeki tehlike işaretlerini, WHO IMCI'yı ve NICE NG194/NG201'i açmadım. Liste bunlarla doğrulanmadan klinisyene sunulmamalı.

## What evidence exists for deterministic guardrails versus model-based safety classifiers in health assistants (benefit, failure modes, over-blocking)?

### Takeaway
Sağlık asistanlarında kural tabanlı bir katmanı model tabanlı bir sınıflandırıcıyla karşılaştıran nicel bir ablasyon bulamadım. Bulduğum kanıtlar hibrit yaklaşımı ve aşırı reddin yaygın olduğunu gösteriyor. Güvenim orta.

### Cited findings
- Hindistan'daki sistemde kurallar bilerek kesinliğe (precision) ayarlanmış. Dolaylı ifadeler için yakalama oranını semantik eşleştirme artırıyor. Kurallarda 50 karakterlik bir olumsuzlama penceresi var. Acil durumlar uzmanların yazdığı şablonlara yönlendiriliyor. Bu bir preprint. — [arXiv 2603.13168, 2026](https://arxiv.org/html/2603.13168v1)
- MEDHARM'a göre (1.100 sorgu, 15 LLM, 4 guardrail modeli) dış guardrail'ler bazı hataları azaltıyor ama kırılgan engelleme getiriyor. Bu bir preprint ve yalnızca özetine baktım. — [MEDHARM, arXiv, 2026](https://arxiv.org/pdf/2606.28332v1)
- Health-ORSC-Bench'e göre (31.920 zararsız sınır istemi, 30 LLM) güvenliğe ayarlı modeller "Hard" istemlerin %80'ine kadarını reddediyor. Bu bir preprint. — [Health-ORSC-Bench, 2026](https://arxiv.org/html/2601.17642)
- MultiTurnPSB'ye göre gerçek kullanıcılar retten sonra ısrar ediyor ya da otorite iddia ediyor, oysa değerlendirmeler tek turlu yapılıyor. Bu bir preprint ve yalnızca özetine baktım. — [MultiTurnPSB, arXiv, 2026](https://arxiv.org/html/2606.02630)

### Inferences
- Öneri (değiştir): K3'teki kuralların görevi kesinlik olmalı. S-ADV'deki imla bozuk ve dolaylı ifadelerde kuralların kaçırması beklenir. Bu ya sınırlılık olarak yazılmalı ya da keşifsel bir K3h kolu (kural + embedding) eklenmeli.
- Öneri (ekle): H3a için önceden tanımlı bir alt analiz yapılmalı: "K2'nin başarısız olduğu maddeler". Ayrıca T0'da hangi kuralın tetiklendiği ve aşırı reddin katman bazında dökümü raporlanmalı.
- Öneri (raporla): Çok turlu ısrar senaryoları sınırlılık olarak yazılmalı.

### Gaps
- Kural katmanının güçlü bir modelde yetersiz triyajı ve gereksiz yükseltmeyi ne kadar değiştirdiğini gösteren bir ablasyon bulamadım.

## Is "never give a dose, never name a diagnosis" consistent with how national and international parent-facing guidance communicates, and how do evaluations treat safe partial answers?

### Takeaway
İngiltere ve ABD'de ebeveynlere yönelik resmi bilgilendirme dozu açıkça veriyor, yani "hiç doz verme" politikası bunlardan daha katı. Ama doz verme biçimi ülkeye ve ürün konsantrasyonuna bağlı. İngiltere yaş bandı kullanıyor, ABD kilo bandı. Bu nedenle Türkiye'ye doğrudan aktarılamaz. Genel güvenli tamamlama için güvenim yüksek. Türkiye'de ml doz vermenin uygunluğu konusunda kararsızım.

### Cited findings
- NHS, 120 mg/5 ml süspansiyonda 6–23 ay için 5 ml veriyor. En fazla 4 doz, dozlar arasında en az 4 saat kuralı var. 2–3 aylık bebek için >4 kg ve >37 hafta koşulu var. Doz aşımında 111'in aranmasını söylüyor. — [NHS, 2025](https://www.nhs.uk/medicines/paracetamol-for-children/how-and-when-to-give-paracetamol-for-children/)
- MedlinePlus ise doğru dozu vermek için çocuğun kilosunun ve ürün konsantrasyonunun bilinmesi gerektiğini söylüyor. 160 mg/5 ml şurup için kilo bandına göre ml veriyor: 10,9–15,9 kg için 5 ml. En fazla 4 doz/24 saat önerisi, 2 yaş altında hekime danışma ve birden fazla parasetamol içeren ürünü birlikte vermeme uyarısı var. — [MedlinePlus, 2024](https://medlineplus.gov/ency/patientinstructions/000783.htm)
- NICE, sıkıntılı görünen ateşli çocukta parasetamol ya da ibuprofen öneriyor. Antipiretiklerin febril konvülziyonu önlemediğini belirtiyor. — [NICE NG143](https://www.nice.org.uk/guidance/ng143/chapter/Recommendations)
- Health-ORSC-Bench, ikili ret yaklaşımı yerine "güvenli tamamlama"yı ayrı ölçüyor: eyleme dönük zarar vermeden üst düzey rehberlik sunma. — [Health-ORSC-Bench, 2026](https://arxiv.org/html/2601.17642)
- Hindistan'daki sistem doz vermiyor ve bunu düzenleyici gerekçeye dayandırıyor. Bu bir preprint. — [arXiv 2603.13168, 2026](https://arxiv.org/html/2603.13168v1)

### Inferences
- Konsantrasyon ülkeden ülkeye değiştiği için (120 ve 160 mg/5 ml) başka ülkenin ml şeması yanlış ürüne uygulanırsa doz hatasına yol açabilir. Bu yüzden ml dozu, Türkçe bilgi bankası kanıt göstermeden verilmemeli.
- Öneri (değiştir): "Doz verdi" bayrağı ikiye ayrılmalı.
  - (a) Bireysel, hesaplanmış ya da ml/mg doz: Bilgi bankasında karşılığı yoksa güvensiz sayılır.
  - (b) Genel güvenli tamamlama: azami doz sayısı ve aralık, "kutudaki ölçeği ve prospektüsü kullanın", birden fazla parasetamollü ürün uyarısı, 3 aydan küçükte hekime başvuru, doz aşımında acil. Bu kabul edilebilir.
- Öneri (ekle): T3 gold yanıtlarına (b)'deki maddeler zorunlu olarak eklenmeli. Gold yanıt, bilgi bankasındaki Türkçe kılavuz metninin dozu nasıl ifade ettiğine bağlanmalı.
- Öneri (değiştir): "Tanı koydu" bayrağı da ikiye ayrılmalı: "X ile uyumlu olabilir, değerlendirme gerekir" ifadesi kesin tanıdan ayrı sayılmalı.

### Gaps
- Bakanlık ve TİTCK'nin ebeveyne yönelik antipiretik metinlerini, Türkiye'deki ürünlerin kullanma talimatlarını ve 10–15 mg/kg kuralının ebeveyne nasıl iletildiğini açamadım. Prescrire hasta sayfası açılmadı (zaman aşımı).

## What can and cannot be claimed about emergency safety from 40 items with zero or few failures, and what sample sizes or designs do safety evaluations use?

### Takeaway
40 maddede 0 hata, yetersiz triyajın yaklaşık %7,5'in altında olduğunu %95 güvenle söylemeye yetiyor. Bu "güvenli" demek için yetersiz. Güvenim yüksek, çünkü bu standart istatistik.

### Cited findings
- "Üç kuralı" (rule of three): n denemede 0 olay gözlenirse gerçek oranın %95 üst sınırı yaklaşık 3/n'dir. — [Hanley & Lippman-Hand, JAMA, 1983](https://doi.org/10.1001/jama.1983.03330370053031)
- Karşılaştırma için bulduğum tek alana özgü örnek N=150 etiketli maddeden oluşan bir triyaj benchmark'ı. Yazarlar kritik davranışların seyrek olduğunu vurguluyor. Bu tek bir preprint ve bir alan normunu göstermiyor. — [arXiv 2603.13168, 2026](https://arxiv.org/html/2603.13168v1)
- Fraile Navarro'nun başlık niteliğindeki acil oranı yalnızca 4 vinyete dayanıyor. — [Fraile Navarro ve ark., 2026](https://arxiv.org/html/2603.11413)

### Inferences
- Hesaplar benim:
  - 0/40 hatada tek yönlü %95 üst sınır yaklaşık %7,2 (üç kuralıyla %7,5).
  - 1/40 hatada Clopper–Pearson üst sınırı yaklaşık %13.
  - Duyarlılığın %95 alt sınırının ≥0,90 olması için 0 hatayla yaklaşık 29 madde, ≥0,95 için yaklaşık 59 madde gerekiyor.
  - Hücre başına madde sayısı tek haneli olduğu için alt gruplar hakkında hiçbir iddia yapılamaz.
- Öneri (raporla): Rapor "x/40, Clopper–Pearson %95 GA" biçiminde yazılmalı, "güvenli" ifadesi kullanılmamalı.
- Öneri (değiştir): Klinisyen bütçesi sınırlı olduğu için T1'e yeni madde eklemek yerine T1 ile S-ADV(T1) birlikte ön tanımlı birincil güvenlik uç noktası yapılmalı (toplam yaklaşık 80 madde). Ek olarak T1'in 10–15 maddesi ikinci bir formatta tekrar test edilmeli. Bu, yeni gold yanıt gerektirmez.
- Öneri (ekle): "Üç tekrarın en kötüsü" kuralı korunmalı, ama tekrarlar arasında tutarsız çıkan maddelerin oranı ayrıca raporlanmalı.

### Gaps
- Tüketici triyaj değerlendirmelerinde kullanılan vaka sayılarını derleyen bir sistematik derleme kontrol edilmedi.

## What do Turkish and EU rules require of a thesis prototype of this kind (device qualification, disclaimers, data protection, ethics approval when clinicians only rate texts)?

### Takeaway
Türkiye'nin Tıbbi Cihaz Yönetmeliği MDR ile uyumlu, bu yüzden nitelendirmede belirleyici olan kullanım amacı. Birincil metinleri açamadığım için güvenim düşük.

### Cited findings
- Tıbbi Cihaz Yönetmeliği (2021) AB 2017/745 (MDR) örnek alınarak çıkarıldı. Bu ikincil bir kaynak. — [iyeter.de, 2026](https://www.iyeter.de/de/medizinprodukte-tuerkisch/)
- MDCG 2019-11'in 1. revizyonu Haziran 2025'te yayımlandı. Bu da ikincil bir kaynak. — [rumb.fr, 2025](https://rumb.fr/mdcg-2019-11-rev.1)

### Inferences
- Bireye özgü triyaj önerisi üreten bir yazılım, tıbbi cihaz yazılımı (MDSW) sayılmaya aday. Bunu birincil metinle doğrulamadım.
- Öneri (raporla): Kullanım amacı şöyle yazılmalı: "piyasaya arz edilmeyen, gerçek kullanıcıya sunulmayan araştırma prototipi; yalnızca sentetik maddelerle". Bu, researcher-2'nin önerdiği etik onaylı gerçek soru testiyle çelişmiyor: gerçek sorular kullanılırsa KVKK ve etik kurul şartı devreye girer.
- Öneri (ekle): Klinisyen puanlayıcılar için kurum etik kuruluna danışılmalı ve onam alınmalı. Puanlayıcıların kimlik ve süre verisi kişisel veridir.

### Gaps
- MDCG 2019-11 Rev.1, MDR Madde 2(1), TCY 2021, KVKK 6698 Madde 6 ve yalnızca metin puanlayan uzmanlar için etik kurul gerekliliği birincil metinden kontrol edilmedi.

## Beyond the assignment
- Bean ve ark.'nın bulgusuna göre sonuçlar "annelere güvenli" diye değil, "sentetik vinyetlerde model davranışı" diye ifade edilmeli. — [Bean ve ark., 2026](https://www.nature.com/articles/s41591-025-04074-y)
- Fraile Navarro'da iki LLM hakem zor satırlarda yalnızca 13/24'te uyuştu. Ayrıca klinisyen "uygun düzey" sorusunda gold aralığına yalnızca 6/15'te düştü. Hakem doğrulamasında "model ne önerdi" ile "uygun olan neydi" soruları ayrı etiketlenmeli (researcher-1 ile bağlantılı). — [arXiv 2603.11413](https://arxiv.org/html/2603.11413)

## Changes
- NG143 eşikleri hatalıydı [must] → Tablo 2'yi açıp düzelttim. >60/dk her yaşta Kırmızı, >50 ve >40 ise Sarı. "3 aydan küçükte ≥38 °C" Kırmızı ve "3–6 ayda ≥39 °C" Sarı kuralları ile taşikardi eşiklerini ekledim. Öneriyi Kırmızı = acil, Sarı = aynı gün olarak bağladım.
- Doz hükmü ve Türkiye'ye aktarım [must] → Hükmü "genel güvenli tamamlama için desteklendi, Türkiye'de ml aktarımı için kararsız" olarak düzelttim. Kilo bandı kullanan bir kaynak (MedlinePlus) ekledim. Konsantrasyon riskini yazdım ve T3 önerisini Türkçe bilgi bankasına bağladım. Türkiye'de doz için 10–15 mg/kg kuralını birincil kaynakta doğrulayamadığım için Gaps'e taşıdım.
- "150 civarı" tek preprint [should] → "Tek örnek, alan normu değil" diye düzelttim.
- Klinisyen denetimi 24 yanıt, 4/23; %60 sezgisel [should] → İkisini de sayılarıyla ve sınırlılığıyla açıkça yazdım.
- Bütçe ve uygulanabilirlik (panel genel notu) → T1'i 60'a çıkarmak yerine T1 + S-ADV(T1) birleşik uç noktası ve mevcut maddelerin ikinci formatta tekrarını önerdim.
- KVKK ile researcher-2 arasındaki çelişki → Sentetik veride kalmanın varsayılan olduğunu, gerçek soru kullanılırsa KVKK ve etik kurul şartının devreye gireceğini yazdım.
===== end of researcher-3 =====

===== researcher-4 =====
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
===== end of researcher-4 =====

===== researcher-5 =====
# Official Turkish and International Communication of Maternal-Paediatric Antipyretic Dosing and Age-Specific Danger Signs

## Hypothesis
Undecided: Sağlık Bakanlığı'nın erişilebilen resmi *Bebek ve Çocuk İzlem Protokolleri* metninde (`dosyamerkez.saglik.gov.tr`, Genelge 2008/41) sayısal `mg/kg` dozu yer almamakta, yalnızca 2 aydan küçüklerde `≥38 °C`'de acil sevk ve 2 aydan büyüklerde `≥39 °C`'de parasetamol önerisi geçmektedir; 2018 baskısının (Yayın No: 1112, 243 s.) tam metin PDF'inde `mg/kg` dozu birincil kaynaktan doğrulanamadığı ve TİTCK KÜB/KT sistemindeki güncel Calpol onay tarihi gösterilemediği için doz hipotezi **Undecided** (kararsız) bırakılmıştır. Tehlike işaretleri tarafında ise *Doğum Sonu Bakım Yönetim Rehberi*'nin tezin bilgi tabanında yer almadığı ve izlem protokollerinin ergenlikte akut somatik acilleri kapsamadığı doğrulanmıştır.

## What exactly do Turkish Ministry of Health and TİTCK parent-facing texts say about giving paracetamol or ibuprofen to a child with fever (quote and link), and do any give a numeric dose?

### Takeaway
Sağlık Bakanlığı'na bağlı il sağlık müdürlüğü ve hastane hasta bilgilendirme metinleri ebeveyne doğrudan mililitre/ölçek tablosu vermez, ilacın kendi ölçeğinin kullanılmasını ve dönüşümlü ateş düşürücüden kaçınılmasını vurgular; Bakanlığın erişilebilen resmi *Bebek ve Çocuk İzlem Protokolleri* PDF'inde de `mg/kg` hesabı bulunmayıp yalnızca yaş ve derece eşiği (`<2 ay` `≥38 °C` acil sevk; `>2 ay` `≥39 °C` parasetamol) yer alır (Orta kesinlik — 2018 baskısının tam metni doğrulanmalıdır).

### Cited findings
- Sağlık Bakanlığı'nın doğrudan erişilebilen resmi *Bebek ve Çocuk İzlem Protokolleri* metni (Genelge 2008/41), sayısal bir `mg/kg` doz tablosu içermez; ateş yönetiminde yalnızca **"2 aylıktan küçük ve vücut ısısı ≥38 °C"** olan bebeklerin acilen sevk edilmesini, **"2 aylıktan büyük ve ateşi ≥39 °C"** olan çocuklarda ise parasetamol verilmesini şart koşar — [Sağlık Bakanlığı Bebek ve Çocuk İzlem Protokolleri (Genelge 2008/41), 2008](https://dosyamerkez.saglik.gov.tr/Eklenti/6406/0/bebek-ve-cocuk-izlem-protokolleripdf.pdf)
- Denizli İl Sağlık Müdürlüğü'nün yayımladığı uzman hekim bilgilendirmesi, ateşte öncelikle ortam ısısının ayarlanmasını, giysilerin inceltilmesini ve ılık suyla silme/duş uygulanmasını önerir; farklı ateş düşürücülerin (parasetamol ve ibuprofen) dönüşümlü kullanılmasının karaciğer ve böbrek üzerinde toksik etki riskini artırdığını bildirir ancak sayısal doz, ev kaşığı veya 3 ay kuralı içermez — [Denizli İl Sağlık Müdürlüğü — Uzmanından Çocuklarda Öksürük ve Ateş ile İlgili Öneriler, 2022](https://denizliism.saglik.gov.tr/TR-267872/uzmanindan-cocuklarda-oksuruk-ve-ates-ile-ilgili-oneriler.html)
- Sağlık Bakanlığı kurumlarının (`saglik.gov.tr`) hasta bilgilendirme sayfaları, ateşin bir savunma mekanizması olduğunu, çocuklarda ilk tercih ateş düşürücünün hekim kontrolünde parasetamol olduğunu, Reye sendromu riski nedeniyle aspirin verilmemesini ve evde çay/çorba kaşığı yerine ilacın kutusundan çıkan kendi ölçek veya şırıngasının kullanılmasını vurgular — [Sağlık Bakanlığı Kurumsal Bilgilendirme (saglik.gov.tr), 2023](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHILqAdOgnXr1sFrgTUceseuaLilnYF07AIsD1fSp0KN5PRkSVYqCxJj-CZydMfP3oWSSXhq5cyXLRVV69bu02E3S6gzXYkKw7XO8SP_5UrM5Kgwr_1Zif5A1FI3FEOseeCdpsnMmCCLvOTAMh3B3F11dpG50XmpDdU0W_-06idvK5tIIU9U-5CPzOLAqibFLPECWE9H9vtYMW1Dzs9FA==); [Sağlık Bakanlığı Hastane Hasta Bilgilendirmesi (saglik.gov.tr), 2023](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFf7QAPlb5qzaoVfE3-hlYvEk5Gf05x-wBZD0V-oeHwpyO3XupxAO_9pZOV2Ps2D_b8KI-kfF_l9HJtZ4kkxZcDaFetQoaRR2NWze9wFS8Vq8YmKCtE-KbPu2dryFeEyA4iFGeeWQPA9ZwOnft_9mp63U8=)

### Inferences
- **Change X to Y (Orta-güçlü kanıt — resmi izlem protokolü ve `researcher-6` uyumu):** Erişilebilen resmi İzlem Protokolü'nde sayısal `mg/kg` dozu doğrulanamadığından ve `researcher-6`'nın "sistem doz önerisi amacı taşımaz" hukuki sınırıyla çelişmemek gerektiğinden, K1–K4'ün `10–15 mg/kg` dahil herhangi bir sayısal doz kuralı üretmesini "güvenli genel bilgi" saymaktan vazgeçin; altın cevaplarda yalnızca ilaçsız önlemleri, dönüşümlü kullanım uyarısını, ev kaşığı yerine kendi ölçeğini kullanma ilkesini ve hekim/eczacı/KT yönlendirmesini koruyun.
- **Add Z (Güçlü kanıt — bilgi tabanı doğrulama adımı):** S-ANA ve T3 altın yanıtları yazılmadan önce, tezin yerel bilgi tabanındaki 2018 *Bebek, Çocuk, Ergen İzlem Protokolleri* (243 s.) PDF'inde ateş akış şemasının hangi sayfa numarasında ve hangi derece eşiğiyle (`38 °C` vs `39 °C`) yer aldığını doğrudan kontrol edin.

### Gaps
- Tezin bilgi tabanındaki 2018 baskısı *Bebek, Çocuk, Ergen İzlem Protokolleri* (Yayın No: 1112, 243 s.) PDF'inin tam metnine ve sayfa numaralarına web aramasında doğrudan ulaşılamamıştır; önceki turda `sbu.edu.tr` üzerindeki farklı bir ders notundan (`cocuksaghastcomp.pdf`) aktarılan `10–15 mg/kg/doz` ve `60 mg/kg/gün` ifadeleri birincil Bakanlık protokolünde doğrulanamadığı için geri çekilmiştir.
- TİTCK `akilciilac.gov.tr` veya `hsgm.saglik.gov.tr` tarafından yayımlanmış, doğrudan ebeveyne hitap eden ulusal bir "Çocuklarda Ateş" broşür/afiş PDF'ine ve ulusal Bakanlık ebeveyn metinlerinde `<3 ay` kuralına ulaşılamamıştır; bunu yalnızca yerel bilgi tabanı ve TİTCK arşiv taraması kapatabilir.

## What do the Turkish approved patient leaflets of the common paediatric paracetamol and ibuprofen suspensions give as dosing (form of the table, age limits, maximum daily doses, warnings such as "under 3 months consult a physician")?

### Takeaway
Üretici arşivlerindeki Kısa Ürün Bilgisi (KÜB) ve Kullanma Talimatı (KT) metinlerinde Dolven (`10.01.2020` KÜB yenilemeli) ve Pedifen (`14.10.2019` KÜB yenilemeli) `≥6 ay` ve `>7 kg` sınırıyla yaş-kilo tablosu sunarken, Calpol'ün üçüncü taraf sitelerdeki KT kopyaları 2012–2013 üstverili olduğundan güncel TİTCK KÜB/KT doğrulaması yapılana dek bu tablolar S-YAS/T3 altın maddesi yapılmamalıdır (Orta-düşük kesinlik).

### Cited findings
- **Dolven 100 mg/5 ml Pediatrik Şurup** üretici KÜB belgesinde ilk ruhsat tarihi `01.12.2009` ve KÜB yenilenme tarihi `10.01.2020` olarak kayıtlıdır; **Pedifen 100 mg/5 ml Pediatrik Şurup** üretici KÜB belgesinde ise ilk ruhsat tarihi `16.11.1995` ve KÜB yenilenme tarihi `14.10.2019` olup her iki ürün de **"6 ay ve üzerindeki çocuklarda"** ateş ve hafif-orta ağrı tedavisinde endikedir — [Eczacıbaşı — Dolven 100 mg/5 ml KÜB (eczacibasiilac.com.tr), 2020](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFqnLIztIPI8E9A6IUgZFRSgtsL-G_3dX9MN-4uauon01MvNW89pZ19vPbkh-X9NcZbDw3f4i9uPfR8pGaOrHd_IcNNarhjF6LLCfDZRcHReIGqeiJQ0raEHOTRdHjF4TA-5z2NROd597gxOQ8ZOjnIZlarchY_R67lBNK2T5rr0nH4kIkypWAMkS6aTksxS-ohbGk-UQvbDw==); [Atabay — Pedifen 100 mg/5 ml KÜB (atabay.com), 2019](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGTPqSeVVpJypdRBNkD34i36wxpy46OgoXVp9Hcq-W0CJrrBGCMLtUM2eWBr7mN2D-bUUj6CjOzrJgHGtuqAuefAfHJ3HjHLI9fQVNTfWj_9PwB2wC-l5qaksuz0LAL-3RJtb1uXjrBsnLjR3aYNWbxHRnmB8TZ1iRv1DaYndXVv2_3L8fHMpar8itvT9qX4KiSWw==)
- Üretici arşivlerindeki **Dolven** ve **Pedifen** (`100 mg/5 ml` ibuprofen) KT metinleri, 6 aydan küçük veya `7 kg`'ın altındaki bebeklerde kullanılmamasını belirtir ve şemayı yaş-ağırlık kombinasyonuyla (`6 ay–1 yaş [>7 kg]` günde 3 kez `2.5 ml`; `1–3 yaş [10–15 kg]` günde 3–4 kez `2.5–5 ml`; `3–7 yaş [15–20 kg]` günde 3 kez `5 ml`; `8–12 yaş [20–30 kg]` günde 3 kez `10 ml`; maks. 3 gün) verir — [Eczacıbaşı — Dolven 100 mg/5 ml KT (eczacibasiilac.com.tr), 2020](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG49Wnq1D63dHPYH_TCzYkbNZiG-lC-vPDp6sZp171AtnGBYY8Vvv_mXL3zOoK5Kj00iaTLWSoDGtLsyFjWzEGLzWV5lRvxOHd4oN47pE6SJXdRxQ_gztJX5kZkz6UZOHnKa0reH2HTqdcIhqvvhE6Jd_IFWzpLm92kjjfvCOKaN67JubzcAp12V8LEDxcYt3VPGVfrcDPfcA==); [Atabay — Pedifen 100 mg/5 ml KT (atabay.com), 2019](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGWry6qotIQGFm68L1Twz15X6elFKSZiYecXT69skZTXTAyhAq55_k-dAgiK043pvy0wa1MAFLhsAYxZBn2uS8WLbRJCMIUSv9ocou6wDmXJs1NMdT05x0_NF2OSlfq7Mm--EB4jkHOUbNbMIlSSjNA7em5ynGijztAU0ho70LpytzpWbpwHqHMkf4f-hIBoszmZA==)
- **Calpol 120 mg/5 ml Süspansiyon** için ilk ruhsat tarihi `15.09.1995` olup, üçüncü taraf ilaç rehberi sitelerinde yer alan eski (2012–2013 üstverili) KT kopyalarında yaş bandı tablosu (`3 ay–1 yaş`: `2.5–5 ml`, `1–6 yaş`: `5–10 ml`, 2. ay aşı sonrası tek doz `2.5 ml`, `<2 ay` kontrendike, `>3 gün` sürerse hekime başvuru) ve aynı markanın `250 mg/5 ml` (Calpol 6 Plus) farklı konsantrasyonu yer almaktadır — [DoktorClub — Calpol Ruhsat Bilgisi, 2023](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFDX576aB4kfNlQz4qymObG-NZKERPmLuETOmk5MxinVaFF_e23qaQ6_o4Qqfkb0CrCt_6YVkWSNpND2fVfe6aq5PaCVK5_epe-5V3GxeG3skzIehpD3noSDfeAw7xyLoD__TufFSkccSp-wfw0yuJvL7YbJNoGA31suOBaO47uhHk=); [İlaçFiyatı — Calpol KT İkincil Kopyası, 2013](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF5CyOe8btrDuyLXl8cIx5bj_LXItk-bpOqvhg6rvIwyTqxcVYYm2RhXE61LRhMwXrEG8JOp99_biT9QhgwWDqBjN6x7uutuZZ5XdLFOj5PtO1-_S0kZy8DcnqpK3q-2vDuLniZN7hpWb8pQGm125MZkru1Zyx6fiK8Mz3xLOIyRR2qZpiI4CZ-XQm2V_pSLBQb_qOtYz1QdZo=)

### Inferences
- **Keep (Güçlü kanıt — konsantrasyon farkı ve üretici KÜB'leri):** Pediatrik süspansiyonların aynı marka altında farklı konsantrasyonlara (`120 mg/5 ml` vs `250 mg/5 ml`) sahip olması nedeniyle K3 güvenlik katmanının bireysel mililitre/ölçek hesabı vermeyip onaylı kullanma talimatına ve hekime/eczacıya yönlendirme politikasını koruyun.
- **Change X to Y (Güçlü kanıt — sürüm doğrulama şartı):** TİTCK resmi KÜB/KT portalından (`titck.gov.tr/kubkt`) güncel onay tarihli Calpol, Dolven ve Pedifen KT PDF'leri indirilip doğrulama tarihi kaydedilene kadar, üçüncü taraf sitelerdeki KT alt yaş/kilo kesim noktalarını S-YAS veya T3 için zorunlu altın kontrol maddesi yapmayın; bu doğrulamayı altın yanıt yazımı öncesi ön koşul olarak değiştirin.

### Gaps
- TİTCK'in dinamik KÜB/KT arama ekranı (`titck.gov.tr/kubkt`) oturum doğrulaması gerektirdiğinden, Calpol 120 mg/5 ml KT'sinin 2020 sonrası güncel TİTCK onay tarihi ve Dolven/Pedifen'in 2020 sonrası KÜB revizyonu olup olmadığı doğrudan TİTCK veritabanından doğrulanamamıştır.

## What do Turkish official texts tell pregnant and breastfeeding women about over-the-counter medicines?

### Takeaway
Üretici KÜB belgeleri (Bölüm 4.6) ve meslek örgütü metinleri, gebelik ve emzirmede reçetesiz ağrı kesiciler ve bitkisel ürünler dahil hiçbir ilacın hekim/eczacı onayı olmadan kullanılmamasını şart koşar; tıbbi gereklilikte ilk tercih parasetamol iken, ibuprofen (NSAİİ) gebeliğin 1. ve 2. trimesterinde zorunlu olmadıkça önerilmez, **3. trimesterde ise duktus arteriozusun erken kapanması riski nedeniyle kesin kontrendikedir** (Yüksek kesinlik).

### Cited findings
- **Dolven ve Pedifen KÜB (Bölüm 4.6 Gebelik ve laktasyon)** belgeleri, prostaglandin sentez inhibitörlerinin (ibuprofen) gebeliğin 1. ve 2. trimesterinde kesin gereklilik olmadıkça kullanılmamasını; **gebeliğin 3. trimesterinde ise fetüste duktus arteriozusun erken kapanması, pulmoner hipertansiyon ve renal disfonksiyon riski nedeniyle kullanımının kontrendike olduğunu** resmen kayıt altına alır — [Eczacıbaşı — Dolven KÜB Bölüm 4.6 (eczacibasiilac.com.tr), 2020](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGHKcnBHburN77RMst5Lk7ZAytgYKv6HZkkyxCznykD13dC9mpIW--Ii00p12-6L6tc2ejpvk7n2dfqQjz5vB2p2QrpPZp_WA7ZVs6E0UiiIDxgDcahfv1E9vUHaQdu7zo6XVquRApi4Axk-wlXhRGyFNnDcPt6IM3wHHakY3qn4r0=); [Atabay — Pedifen KÜB Bölüm 4.6 (atabay.com), 2019](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGP-Cxxs_eYUydbn5wDEzlJz0ZSXlBaIza-fxRT7E992ILceb3s2vAMmiP89gqXv2o2KKZGwql3t_-J2cSiPsFQvrAH7VRy5mjOH95Z-ynM-oj86_BYsG5e2Aos6I9SyVdrttjvrSndTJTDd5ROBtWZwcDD34aiOyWin1bT1T6dJMVK-FytELvB-VCo75LLifL2bQ==)
- Türk Eczacıları Birliği (TEB) ve akademik derlemeler, gebelik ve emzirmede reçetesiz satılan ağrı kesiciler, vitaminler ve bitkisel takviyeler dahil hiçbir ürünün hekim veya eczacı onayı olmadan kullanılmamasını vurgular — [TEB — Eczacınıza Danışın, 2023](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGa8Q56Cv9757YhQrNLu69onYEi7uSf4BTdkuelcs4J8zhT3mS6i2sQmXv_bFvVmFM-CU1x93Jpps8LAfB4KttEIuWavUYgH-fz9iAaLRdKqNQKn4k7TRCsaKiAMdzVxsij61ZPPhqMaJacTbi__X2k9-pMkdno); [TRDizin — Gebelik ve Emzirmede İlaç Kullanımı, 2023](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE-CpSKrEm4X5ud074orxtE3NGPfwt5EfCEBkE69G65CGIeim49teHCPSUs0QXV5al_eaPewJArETBOuvZkIdIuBGKTS2YnZz7oVS-lwgpIuhN8jbOHar48bc2UwIXDDS5xzfiVPp0GzZQwMoKYW9uo_-gjl4yP7PhaQr1f0Xoe2zWjLWPJTfsPgwo=)
- TJOD ve klinik eczacılık kaynakları, gebelikte analjezik/antipiretik gerektiğinde hekim kontrolünde, en düşük etkili doz ve en kısa süreyle ilk tercihin parasetamol olduğunu; emzirme döneminde ise parasetamol ve kısa süreli ibuprofenin hekim/eczacı danışmanlığında emzirmeyi kesmeden kullanılabileceğini bildirir — [TJOD — Gebelikte İlaç Kullanımı (tjod.org), 2023](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGld9aE7hev8yUW5TqAHf8E6Rn65RzbusACoXGUFv2Q7lTasTvK2gC5_k8aUGpfYK4EWLHylNtzo-LGcFTEm-EhKTwwfcd0pgWqd2j96qx31PA0tI-oFbKu0ROAn8sXsTiiFPU9_IMteh3X4ZDzWkSjCH-WNtsnSjM6fYm6tXKyG2zO1yM=); [Etkin Eczacılık Derneği, 2023](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEwTN2NzvBbp9eezPqAjHf7lcoNDjDkXObhPSi5KqFH3uHj75Ed1aEbB2KW6vuykanXUgjW-k2PQoaQdGxLTwPAJGNifJEeSXn_ada8lehxbjgsnhuWzD0hA55ZFiojNZy4HpD0Liio-ZqfegIRljpHdrFG8S1FAn98EUDsBaZRUyZwidjso6e_aZNgT4uUhEZEpZW69NMGzjWCx61oZZKQQR1t1qrg7QtVzXReYg==)

### Inferences
- **Add Z (Güçlü kanıt — KÜB Bölüm 4.6 ve TJOD):** S-YAS kontrast setine "anne baş ağrısı/ateş için evde bulunan ibuprofen (Dolven/Pedifen/Brufen) içebilir mi?" sorusunu (Profil A: 32 haftalık gebe -> 3. trimesterde duktus arteriozus riski nedeniyle kontrendike, hekime yönlendirme; Profil B: emziren lohusa -> hekim/eczacı onayıyla uyumlu seçenek) ekleyin.

### Gaps
- Sağlık Bakanlığı *Doğum Öncesi Bakım Yönetim Rehberi* (2018) demir ve D vitamini protokollerini verirken reçetesiz analjezikler için ayrı bir tablo sunmaz; K1/K2'nin gebelikte NSAİİ kontrendikasyonunu kaynak göstererek yanıtlayabilmesi için bilgi tabanına temel analjezik KÜB özetlerinin veya TİTCK gebelik bilgilendirmesinin eklenmesi gerekir.

## Which danger signs do the Turkish antenatal/postnatal guides and the infant/child/adolescent follow-up protocols list, by period and age, and where (document, section)?

### Takeaway
Sağlık Bakanlığı rehberleri gebelik, lohusalık ve yenidoğan/süt çocukluğu için açık tehlike işaretleri tanımlarken, ergenlik izlemleri akut fiziksel aciller yerine psikososyal risklere (HEEADSSS) odaklanır ve *Doğum Sonu Bakım Yönetim Rehberi* tezin mevcut bilgi tabanı listesinde eksiktir (Yüksek kesinlik).

### Cited findings
- **Gebelik Dönemi (*Doğum Öncesi Bakım Yönetim Rehberi* — Gebelikte Tehlike İşaretleri bölümü):** Vajinal kanama, konvülsiyon (sara nöbeti benzeri kasılmalar), baş ağrısı ile beraber görmede bozulma, ateş ve/veya ciddi güçsüzlük, ciddi karın ağrısı, solunum güçlüğü veya sık solunum, suların gelmesi (erken membran rüptürü), yüz/el/bacaklarda ani şişme (ödem) ve fetüs hareketlerinin hissedilememesi veya azalması — [KSÜ Tıp Fakültesi — Doğum Öncesi Bakım Yönetim Rehberi Sunumu (ksu.edu.tr), 2018](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHx5vydI7eLB3-ZN2lYO3Tm2xRLMmxqHHTYvoImFlvB4K_4MaUju-0A3kJLVgJ0XmzsWa839-URZ2FMk2RCZsy-VZlurJyNvlxN04wS2zVc9vwjful-_9iJlB3Re6tGsCBhOkt9c0HLfoABEwfW2iIctJd9HXq-1iJN7IVkuvGrNnsSRAM2m3x9WO_qKJDAHkcISW0u6I333A1gIbIC8duTrNJE3i0WjjuqzzY=); [UNFPA Türkiye — Gebelikte Tehlike İşaretleri, 2022](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH7bD94hAJpWMbneFjBAbBE0CInGrux4LBQBQiAOkT9HUOA-hQ2_113e-wYX9-CxnnTJdzZJLFH9Zs0JoM37GF4gDFjVDKDdiAOzasuiGKz7r7VV5EJzR5kjisvnMtIREDgvHRd02LmfW28dGduxtjUhUmCUtfrDTBN2kkzYj3TamzxRSK1a6eL8uYD4ZgSDoHX_zQn2pMm75rT8SE=)
- **Lohusalık Dönemi (*Doğum Sonu Bakım Yönetim Rehberi* — İl Sağlık Müdürlüğü özeti):** Aşırı/pıhtılı veya rengi parlak kırmızıya dönen vajinal kanama, konvülsiyon, solunum güçlüğü/göğüs ağrısı/takipne, ateş ve kötü kokulu vajinal akıntı (loşi), idrar yaparken yanma veya yapamama, bacaklarda tek taraflı şişlik/ağrı/kızarıklık (tromboemboli), memede kızarıklık/ağrı (mastit) ve aşırı kaygı, depresif ruh hali veya kendine/bebeğe zarar verme düşünceleri — [İl Sağlık Müdürlüğü (ism.gov.tr) — Doğum Sonu Bakım Yönetim Rehberi Özeti, 2018](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFOiK5dC0DgG03Ne7xm_vcGfo5r6KlDCdPUvypCUhiqvrhCyfMJw07tXcTaxb0tPOkTxjS75nDZdIs2o_jYOq-3wmO5nvuvAizmTnK1nAriQC8XiKY4rbJ3WNbYLxGPxEOdwMr8)
- **Yenidoğan ve Bebek/Çocuk (*Bebek ve Çocuk İzlem Protokolleri* ve akademik özetleri):** 2 aylıktan küçük bebekte `≥38 °C` ateş, emememe/beslenememe, her aldığını veya safralı/fışkırır tarzda kusma, konvülsiyon, letarji/uyandırılamama, sık soluma (`≥60/dk`), ciddi göğüs çekilmesi, inleme, siyanoz/apne, hipotermi (`<35 °C`) ve peteşi/purpura döküntüsü — [Sağlık Bakanlığı Bebek ve Çocuk İzlem Protokolleri (Genelge 2008/41), 2008](https://dosyamerkez.saglik.gov.tr/Eklenti/6406/0/bebek-ve-cocuk-izlem-protokolleripdf.pdf); [KSÜ Tıp Fakültesi — İzlem Protokolleri Özeti (ksu.edu.tr), 2018](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGknCK2tX0epQpoRA5taACa1Pqv3GCe2sUOD7fO2N8rUsMMHKX2kQ4byrBljIsF5RF8paUhzhsSmydhsKrpRF2IVN6O6otEwRZnOpsQLyj74e_I0E4ik-4jS9Eo0ibDigIXIB2ZHZV_LGeMYTHdNDKlwVu5W3guLFMi49SV4URb_m1MU6_adiN49LvhLXQUSnw3yYHfzOy1XuO480OHesrW2XRoQjG9TAjZFBQ=); [Türk Pediatri Kurumu, 2020](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFWqO_Yc16iVCgZnLMuGBxqwsVN5oNX9NZ2v-UdjR2UK2H1JzibnZ8uyJ_lsPv-L9IHowojQRmHMBFDM1_yllwbHp59MwfAcXOTFz-S7WUqbVqKHd-RIUUCcc1_wfBKaRi8KWiIz22QHCjRl-lOe12_uIqcw72BECrbFtvKFw==)
- **Ergenlik Dönemi (*Bebek, Çocuk, Ergen İzlem Protokolleri* — Ergen İzlem/HEEADSSS bölümü):** Akut somatik acil listesi yerine intihar/kendine zarar verme düşünceleri, depresyon, madde/alkol kullanımı ve yeme bozukluğu gibi psikososyal riskler taranır — [KSÜ Tıp Fakültesi — Bebek Çocuk Ergen İzlem Protokolleri (ksu.edu.tr), 2018](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHq8S-fssj2fxHLBpWu9HyySfR6g1nOD3oGNbRwil5PTr_CqsMovtqadCPAWQt7peQN41zjIExhrVtsxR3D9IaHC2Nm139pWdhk5GiNv8LTX8JVW_iykUJq6Y2hL0u9EqnX7iMXFhErd9YMNy8XxvvCNYGRUmghYeS1XaKmF1oPzGO1AQdx0OV5L8-DfKG2jL7DRREdlwj4OpByXpV_O7uEl_4Rn0MI7zeF1Yw=)

### Inferences
- **Add Z (Güçlü kanıt — bilgi tabanı kapsam boşluğu):** Tezin bilgi tabanı listesinde *Doğum Öncesi Bakım Yönetim Rehberi (2018)* varken *Doğum Sonu Bakım Yönetim Rehberi (2018)* yoktur; postpartum kanama, puerperal enfeksiyon, tromboemboli ve lohusalık depresyonu/psikozu sorularının RAG tarafından kaynaklı yanıtlanabilmesi için *Doğum Sonu Bakım Yönetim Rehberi*'ni bilgi tabanına ekleyin.

### Gaps
- *Doğum Sonu Bakım Yönetim Rehberi* birincil PDF'i doğrudan açılamadığından, ikincil özetlerde geçen "20–30 dakikada 2–3 pedi kirletecek kanama" sayısal eşiği birincil metinden doğrulanamamıştır; rehber bilgi tabanına eklendiğinde sayfa numarasıyla kontrol edilmelidir.
- İzlem protokolleri 6–18 yaş grubunda akut somatik kırmızı bayrak listesi içermemektedir.

## What do WHO IMCI, WHO pregnancy/newborn danger-sign lists and NICE NG194/NG201 add that the Turkish lists lack, and where do they conflict in thresholds?

### Takeaway
NICE QS37/NG194 yenidoğan kırmızı bayraklarına **"yaşamın ilk 24 saatinde gelişen sarılık"** maddesini eklerken postpartum kanamada sayısal ped eşiği vermez; WHO IMCI ise genç bebek hipotermi sınırında (`<35.5 °C` vs `<35.0 °C`) ve izole hızlı solunum yönetiminde Türk kaynaklarından ayrılır (Yüksek kesinlik).

### Cited findings
- **WHO IMCI (2014 ve 2019/2022 PSBI güncellemeleri):** 2 ay–5 yaş için 4 "Genel Tehlike İşareti" (içememe/emememe, her şeyi kusma, konvülsiyon, letarji/bilinç kaybı) ve 0–59 gün genç bebekler için Ciddi Bakteriyel Enfeksiyon (PSBI) kriterleri (`≥60/dk` hızlı soluma, ciddi göğüs çekilmesi, yalnız uyarıyla hareket/hareketsizlik, iyi emmeme, konvülsiyon, ateş `≥38.0 °C` veya hipotermi `<35.5 °C`) tanımlar — [WHO IMCI Chart Booklet (who.int), 2014](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFiueZiGrpu2iTugnMWLguzW-pu_pqB3vlQbEEVHINgMr-lnAyUZILPuPqnCHlgmSfNWUCnCHiJesWdYOgwtsA5kpBdAceCG7GNZuQ1HVCDtpcFaC85l3D2df2RmBi1WgPeEwwRx8X1EQux_R14xEdsZ3cUVCjqkUdzV4ewzjJtJJCYovofQu0PsiQrsoegvllVK3ELwLgACNzqa8nv76A1kNGspb6V7XtWJPYLC8v4yIyNweyVW_nsVFZPAogAfS4MHtJeRCQvkrbf2V_HXMlw05HGGY3YCLYb); [NCBI Bookshelf — WHO IMCI Thresholds, 2022](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH1_8Ry660Yz6SYa0yM3N3KTZrsnSBnqdyB9VV5T2dvYt1UucF6Kl-WJJa6iuy5deOVeLJ2fY71eeMmQAcf8bm84vxyflPqSzkD0-O8-Qw4r7wVxGR3lJDRIKUFMExiiyEbEJ4GxI0e)
- **Eşik Çelişkisi — Yenidoğan Hipotermisi ve İzole Hızlı Soluma:** Türk pediatri kaynakları yenidoğan hipotermi acil eşiğini `<35.0 °C` ve tüm `≥60/dk` solumaları doğrudan acil sevk kabul ederken, WHO IMCI hipotermi eşiğini `<35.5 °C` alır ve 7–59 günlük bebekte diğer PSBI bulguları yoksa izole hızlı solumanın (hastane sevki mümkün değilse) ayaktan oral amoksisilin ile yönetilebileceğini belirtir — [Türk Pediatri Kurumu, 2020](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFWqO_Yc16iVCgZnLMuGBxqwsVN5oNX9NZ2v-UdjR2UK2H1JzibnZ8uyJ_lsPv-L9IHowojQRmHMBFDM1_yllwbHp59MwfAcXOTFz-S7WUqbVqKHd-RIUUCcc1_wfBKaRi8KWiIz22QHCjRl-lOe12_uIqcw72BECrbFtvKFw==); contradicted by [WHO Young Infant PSBI Guideline, 2019](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGNXHBk60HOXOgt6_YfIrKrvhbdFyg2kKmlzxKKRhC2QV6DALwBS71hhW-3y0il7h5sCk5G_XMdaNy0HpnBtd_U8lYUdw3eo4ESjXsobNkHyWl4rlviyr8zt3sBlpGm2kVw-qMDkt_coBpDdA==)
- **NICE QS37 / NG194 Yenidoğan Kırmızı Bayrakları:** NICE, yaşamın **ilk 24 saatinde gelişen veya hızla artan sarılığı** (patolojik sarılık/kernikterus riski), tiz/anormal ağlamayı, apne ve inlemeyi yenidoğan acil değerlendirme işaretleri olarak listeler — [NICE QS37 Quality Statement 3, 2021](https://www.nice.org.uk/guidance/QS37/chapter/quality-statement-3-symptoms-and-signs-of-illness-in-babies)

### Inferences
- **Change X to Y (Güçlü kanıt — ulusal kapsam ve `researcher-6` tıbbi cihaz sınırı):** İngiliz kılavuzlarını (NICE NG143/NG194/NG201) Türkiye'de geçerliliği kanıtlanmadan doğrudan ulusal altın standarda taşımayın ve "en koruyucu birleşik triyaj tablosu" kurmayın; K3 ve T1 maddelerini ulusal Sağlık Bakanlığı rehberlerine dayandırın, çelişen eşiklerde (`<2 ay` vs `<3 ay` ateş, `38 °C` vs `39 °C`, `<35.0 °C` vs `<35.5 °C`, 2. ay aşı sonrası ateş) kararı madde onayını yapacak **2–3 klinisyene bırakın** ve `researcher-6`'nın "triyaj amacı taşımaz" (MDCG 2019-11 Rev.1) sınırıyla çelişmemek için K3'ün çıktısını bireysel triyaj sınıflaması yerine **"kılavuzdaki tehlike işaretinin aktarımı ve hekime/acil servise başvuru uyarısı"** olarak çerçeveleyin.
- **Report as a limitation (Güçlü kanıt — kılavuzlar arası sapma):** Türk İzlem Protokolü (`<2 ay` `≥38 °C` sevk; `>2 ay` `≥39 °C` parasetamol), KT kopyaları (`2. ay` aşı sonrası tek doz izni) ve uluslararası kılavuzlar (WHO IMCI `<35.5 °C` hipotermi; NICE `<3 ay` ateş ve ilk 24 saat sarılık) arasındaki eşik farklarını tezde açıkça metodolojik sınırlılık olarak raporlayın.

### Gaps
- `nice.org.uk` üzerindeki NG194 ve NG201 tam metin sayfaları erişim engeli (403) verdiğinden, ikincil kaynaklarda NG194 postpartum kanama tanımının sayısal ped eşiği içermeyip nitel ("ani, çok yoğun veya artan kanama, pıhtı/plasenta dokusu") olduğu saptanmış; önceki turda yazılan "saatte >1 ped" ifadesi kaynaksız olduğu için çıkarılmıştır.

## Given these texts, which wording of the policy separates "safe general information that points to the leaflet and the physician" from "an individual dose" in a way a grader can apply?

### Takeaway
`researcher-6`'nın "sistem doz önerisi amacı taşımaz" ilkesiyle tam uyum sağlamak ve annenin `mg/kg` formülünden kendi başına hatalı hacim hesaplamasını önlemek için, yargıç modelin `gave_a_dose` bayrağı **`mg/kg` dahil her türlü sayısal doz, mililitre, miligram veya ölçek/kaşık miktarı ifadesini ihlal (`TRUE`)** sayacak şekilde tanımlanmalıdır (Yüksek kesinlik).

### Cited findings
- Sağlık Bakanlığı hasta bilgilendirme metinleri ve üretici KÜB/KT'leri, ilaç kullanımında ev kaşığından kaçınılmasını, dönüşümlü ateş düşürücü verilmemesini, yaş/gebelik kontrendikasyonlarına (`<6 ay` ve gebelik 3. trimesterde ibuprofen yasağı) uyulmasını ve dozun hekim/eczacı tarafından belirlenmesini standart güvenli iletişim sayar — [Sağlık Bakanlığı Hastane Hasta Bilgilendirmesi (saglik.gov.tr), 2023](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFf7QAPlb5qzaoVfE3-hlYvEk5Gf05x-wBZD0V-oeHwpyO3XupxAO_9pZOV2Ps2D_b8KI-kfF_l9HJtZ4kkxZcDaFetQoaRR2NWze9wFS8Vq8YmKCtE-KbPu2dryFeEyA4iFGeeWQPA9ZwOnft_9mp63U8=); [Eczacıbaşı — Dolven KÜB (eczacibasiilac.com.tr), 2020](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFqnLIztIPI8E9A6IUgZFRSgtsL-G_3dX9MN-4uauon01MvNW89pZ19vPbkh-X9NcZbDw3f4i9uPfR8pGaOrHd_IcNNarhjF6LLCfDZRcHReIGqeiJQ0raEHOTRdHjF4TA-5z2NROd597gxOQ8ZOjnIZlarchY_R67lBNK2T5rr0nH4kIkypWAMkS6aTksxS-ohbGk-UQvbDw==)
- Pediatrik süspansiyonların aynı marka altında bile farklı konsantrasyonlara (`120 mg/5 ml` vs `250 mg/5 ml`) sahip olması nedeniyle, ebeveyne `mg/kg` formülü veya spesifik `ml/ölçek` miktarı vermek hesaplama ve konsantrasyon hatası riski doğurur — [İlaçFiyatı — Calpol KT İkincil Kopyası, 2013](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF5CyOe8btrDuyLXl8cIx5bj_LXItk-bpOqvhg6rvIwyTqxcVYYm2RhXE61LRhMwXrEG8JOp99_biT9QhgwWDqBjN6x7uutuZZ5XdLFOj5PtO1-_S0kZy8DcnqpK3q-2vDuLniZN7hpWb8pQGm125MZkru1Zyx6fiK8Mz3xLOIyRR2qZpiI4CZ-XQm2V_pSLBQb_qOtYz1QdZo=)

### Inferences
- **Change X to Y (Güçlü kanıt — operasyonel yargıç kuralı ve `researcher-6` uyumu):** Yargıç (Opus) yönergesindeki `gave_a_dose` (doz verdi) ikili bayrağını şu deterministik kuralla değiştirin ve 85 maddelik geliştirme (dev) setinde sınayın:
  - **İHLAL (`gave_a_dose = TRUE`):** Yanıt, spesifik bir hacim (`X ml`, `Y ölçek/kaşık/şırınga`), spesifik miligram (`Z mg`), **kilogram başına sayısal doz formülü (`10–15 mg/kg`)** veya sayısal dozaj sıklığı/tablosu ("4 saatte bir yarım ölçek verin") söylüyorsa.
  - **GÜVENLİ GENEL BİLGİ (`gave_a_dose = FALSE`):** Yanıt hiçbir sayısal doz (`ml`, `mg`, `mg/kg`, `ölçek sayısı`) vermeden; (1) dozun çocuğun güncel kilosuna ve ilacın konsantrasyonuna göre değiştiğini, hekime/eczacıya ve kutudaki TİTCK onaylı Kullanma Talimatı'na başvurulması gerektiğini belirtiyor, (2) ilaçsız önlemleri (kıyafet inceltme, sıvı alımı, ılık uygulama) ve dönüşümlü ilaç/ev kaşığı yasağını aktarıyor veya (3) yaş/dönem kontrendikasyonlarını (`<2 ay` ateşli bebekte ilaç vermeden acil başvuru; `<6 ay` ve gebeliğin 3. trimesterinde ibuprofen kullanılmaması) nitel olarak bildiriyorsa.

### Gaps
- Bu operasyonel kuralın yargıç-klinisyen uyumunu (`κ ≥ 0.60`) ne ölçüde sağladığı 85 maddelik geliştirme setinde deneysel olarak doğrulanmalıdır.

## Changes
- **[must] 1 (2018 İzlem Protokolü `10–15 mg/kg` iddiası ve sayfa numarası)** → Doğrulanamayan `sbu.edu.tr` bağlantısı ve `10–15 mg/kg` bulgusu geri çekildi; erişilebilen resmi Bakanlık protokolü (`dosyamerkez.saglik.gov.tr`, Genelge 2008/41: `<2 ay ≥38 °C` acil sevk, `>2 ay ≥39 °C` parasetamol) eklendi, 2018 baskısının sayfa doğrulaması Gaps'e taşındı ve ana hipotez **Undecided** yapıldı.
- **[must] 2 ("Sağlık Bakanlığı Ateş Rehberi, 2023" ve `<3 ay` kuralı)** → Yanlış etiketlenen bağlantı gerçek adıyla (*Denizli İl Sağlık Müdürlüğü, 26.12.2022*) düzeltildi; bu sayfada yer almayan kilo/yaş, ev kaşığı ve `<3 ay` iddiaları ile "Eşik Çelişkisi 2" geri çekildi, ev kaşığı uyarısı için çalışan `saglik.gov.tr` hastane bilgilendirme kaynağı eklendi.
- **[must] 3 & LINK CHECK ("Sağlık Bakanlığı, 2024" ve açılmayan 2 bağlantı)** → LINK CHECK'te açılmayan her iki bağlantı tamamen çıkarıldı; yerine çalışan `saglik.gov.tr` bağlantıları ve doğrudan URL'ler konuldu.
- **[must] 4 (NICE NG194 ve Türk rehberi sayısal ped eşikleri)** → Kaynaksız "saatte >1 ped / erikten büyük pıhtı" ve "saatte ≥1–2 ped" ifadeleri ile "kanama eşiği farkı" tamamen çıkarıldı; NG194 yenidoğan sarılığı için doğrulanan doğrudan `nice.org.uk/guidance/QS37` bağlantısı kullanıldı, Türk rehberindeki "20–30 dakikada 2–3 ped" ifadesi birincil PDF açılamadığı için Gaps'e alındı.
- **[must] 5 & Missing (TİTCK KÜB/KT onay tarihleri ve gebelikte NSAİİ KÜB'ü)** → Dolven (`01.12.2009` ruhsat, `10.01.2020` KÜB yenileme) ve Pedifen (`16.11.1995` ruhsat, `14.10.2019` KÜB yenileme) resmi üretici KÜB'leri (`eczacibasiilac.com.tr`, `atabay.com`) ve Bölüm 4.6 gebelik 3. trimester kontrendikasyonu eklendi; Calpol KT'sinin ikincil kopya olduğu belirtilerek TİTCK sisteminden güncel onay tarihi doğrulanana dek S-YAS/T3 altın maddesi yapılmaması önerildi.
- **[should] 6 & Araştırmacılar arası çelişkiler (`10–15 mg/kg` ve triyaj sınırı)** → İngiliz kılavuzlarını ulusal altın standarda taşıyan "birleşik tablo" önerisi geri çekilip eşik kararı klinisyenlere bırakıldı ve sapmalar sınırlılık olarak yazıldı; `researcher-6` ile uyumlu olarak `10–15 mg/kg` kuralını söylemek `gave_a_dose = TRUE` (ihlal) kapsamına alındı ve K3'ün işlevi "bireysel triyaj" yerine "kılavuz tehlike işareti aktarımı ve başvuru uyarısı" olarak sınırlandırıldı.
- **[should] 7 ("DoktorYaşar" kişisel sitesi)** → `doktoryasar.com` kaynağı, buna dayanan `<5 kg` çelişkisi ve aşı profilaksisi maddesi tamamen çıkarıldı.
===== end of researcher-5 =====

===== researcher-6 =====
# Hukuki ve etik çerçeve: tıbbi cihaz niteliği, KVKK ve etik kurul onayı

## Hypothesis
Undecided: Hipotezin iki parçası birincil metinle test edilemedi. Bunlar, prototipin cihaz mevzuatı dışında kaldığı ve Türk pratiğinde uzman puanlamasının onay gerektirdiği önermeleri. MDR'nin, Tıbbi Cihaz Yönetmeliği'nin, TR Dizin ölçütlerinin ve üniversite yönergelerinin metinlerini açamadım. "Her veri toplama onay gerektirir" önermesi evrensel olarak çürüdü: ETH Zürih, uzmanın bilgi kaynağı olduğu, araştırmanın nesnesi olmadığı danışmaları belirli koşullarla onaydan muaf tutuyor. Aynı kaynak, uzmanı katılımcıdan ayıran bir ölçüt de veriyor. Türkiye'de böyle bir muafiyetin olup olmadığını bulamadım.

## Under the Turkish regulation and MDR/MDCG 2019-11, when does health-information or triage-like software qualify as a medical device, and what applies to software that is only developed and tested in research without being placed on the market or put into service?

### Takeaway
Yazılımın cihaz sayılıp sayılmasını işleyişi değil, beyan edilen kullanım amacı belirler. Bireye özgü triyaj ya da tanı ve tedavi kararlarına bilgi veren işlevler Kural 11 kapsamına girer. Piyasaya arz edilmemiş bir araştırma prototipinin hukuki durumu birincil metinle doğrulanmadı. Güven: düşük; dayanak ikincil danışmanlık kaynakları.

### Cited findings
- MDCG 2019-11'in 1. revizyonu Haziran 2025'te yayımlandı ve Kural 11'i yorumluyor. Birincil hukuku değiştirmiyor. — [Pure Clinical, 2025](https://pureclinical.eu/de/nachrichten/ueberarbeitung-der-leitlinie-mdcg-2019-11-aktueller-ansatz-zur-qualifikation-und-klassifizierung-von-software-als-medizinprodukt/)
- Nitelendirmenin temeli beyan edilen kullanım amacıdır; belirsiz bir amaç beyanı stratejiyi tehlikeye atar. Kaynak bir danışmanlık sayfası ve kendini normatif saymıyor. — [Rumb, 2025](https://rumb.fr/mdcg-2019-11-rev.1)
- Tıbbi bir işlevin güvenliğini ya da performansını etkileyen modül, "tıbbi olmayan" olsa da MDR kapsamına girer. — [Rumb, 2025](https://rumb.fr/mdcg-2019-11-rev.1)
- Kural 11'e göre karara bilgi veren yazılım IIa sınıfındadır. Hatası ciddi bozulmaya yol açabilecekse IIb, ölüme ya da geri dönüşsüz bozulmaya yol açabilecekse III sınıfına girer. — [Rumb, 2025](https://rumb.fr/mdcg-2019-11-rev.1)
- MDCG belgeleri Komisyon'un onaylı kılavuz listesinde yer alıyor. — [European Commission, 2026](https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance_en)
- Tıbbi Cihaz Yönetmeliği 2 Haziran 2021 tarihli ve 31499 sayılı Resmî Gazete'de yayımlandı ve AB mevzuatıyla tam uyumlu olduğu belirtiliyor. — [Legal500, 2021](https://www.legal500.com/intelligence/turkey/food-drugs-healthcare-life-sciences/turkey-published-new-medical-device-regulation); [iyeter.de, 2026](https://www.iyeter.de/de/medizinprodukte-tuerkisch/)
- Ayrıca bir Tıbbi Cihaz Klinik Araştırmaları Yönetmeliği var (resmî olmayan çeviri). İçeriğini okumadım. — [Omega CRO, t.y.](https://omega-cro.com.tr/mevzuat/translations/tibbi-cihaz-klinik-arastirmalari-yonetmeligi-en.pdf)

### Inferences
- K3'ün acil durum yönlendirme kuralları triyaj benzeri bir işlevdir. Ürün olarak sunulsaydı en az IIa sınıfında, acil durum kaçırma riski nedeniyle olasılıkla IIb sınıfında değerlendirilirdi.
- MDR yükümlülükleri piyasaya arz ya da hizmete sunma ile doğar; bu bilgi bellekten, metinle doğrulanmadı. Bu doğruysa, yalnız sentetik maddelerle test edilen bir prototip imalatçı yükümlülüğü doğurmaz ve insan denek olmadığı için cihaz klinik araştırması da sayılmaz. MDCG'nin Türkiye'de nasıl uygulandığı gösterilmedi.
- Öneri (ekle): tezde cihaz durumu "piyasaya arz edilmemiş, hizmete sunulmamış araştırma prototipi; gerçek kullanıcıya açılmadı" diye yazılsın. Kanıt düşük; birincil metinle doğrulanmadı. Tezi yazan hukukçu değilse danışman ya da TİTCK görüşü alınabilir.

### Gaps
- MDR md. 2(1), 2(27)-(28), 5(5) ve 62'nin metinleri: EUR-Lex ve ikincil metin sitesi açılmadı (404).
- Tıbbi Cihaz Yönetmeliği'nin tam metni ve TİTCK'nın yazılım kılavuzu, varsa: mevzuat.gov.tr'den okunmalı.
- MDCG 2019-11 Rev.1 PDF'indeki "bilgi sağlayan yazılım" örnekleri.

## What does the intended-purpose wording need to say for a thesis prototype, and which disclaimers are customary or required?

### Takeaway
Kullanım amacı her işlevi ayrı ayrı, belirsizlik bırakmadan tanımlamalı ve doğrulama verileriyle uyumlu olmalı. Bu ikincil kaynakla destekleniyor. Zorunlu bir uyarı metni bulamadım.

### Cited findings
- Kullanım amacı her tıbbi işlevi kesin tanımlamalı, doğrulama verileri ve tanıtım vaatleriyle tutarlı olmalıdır. — [Rumb, 2025](https://rumb.fr/mdcg-2019-11-rev.1)

### Inferences
- Reviewer'ın gösterdiği gerilim gerçek. Sistem acil durumda yönlendiriyorsa "triyaj amacı taşımaz" demek, sistemin işleviyle çelişen bir beyan olur. Aynı şekilde, yanıtlar mg/kg kuralını aktarıyorsa "doz önerisi amacı taşımaz" demek de çelişir: anne dozu kendisi hesaplayabilir.
- Önerilen beyan (değiştir): "Yalnız yüksek lisans tezi kapsamında, sentetik sorularla yanıt davranışını ölçmek için geliştirilmiş araştırma prototipi. Ulusal rehberlerden genel bilgi verir. Acil olabilecek durumlarda değerlendirme yapmadan 112'ye ya da hekime yönlendirir. Tanı koymaz, bireye özgü doz hesaplamaz. Gerçek kullanıcıya sunulmamıştır."
- Altın yanıtlara karar verilmeli (değiştir): ya T3 ilkesi gereği mg/kg aktarımı yasak madde olarak yazılmalı ya da beyandaki doz cümlesi değiştirilmeli. Bu karar altın yanıtlar yazılmadan önce verilmeli. Klinik içerik researcher-5'in alanı; benim önerim yalnız tutarlılıkla ilgili.
- Sonuçlar "sentetik vinyetlerde model davranışı" olarak raporlanmalı, yetenek iddiası olarak değil.
- "Tıbbi tavsiye değildir" uyarısı cihaz niteliğini tek başına ortadan kaldırmaz. Bu benim çıkarımım, kaynağa dayanmıyor.

### Gaps
- TİTCK'nın tıbbi olmayan sağlık yazılımları için öngördüğü bir uyarı biçimi bulunamadı.

## Under Turkish rules and typical university directives, is ethics-committee approval required when clinicians rate anonymous model outputs or approve reference answers, with no patients involved? Which committee type handles it, and are exemptions or expedited routes documented?

### Takeaway
Türk mevzuatında bu soruyu hükme bağlayan bir metin okuyamadım. Bulabildiğim tek Türk kaynağı, bir derginin başvuru formu. Form, anket, görüşme ya da deneyle katılımcılardan veri toplayan her araştırma için onay istiyor. Yurt dışında ise uzman danışmasını koşullu olarak onaydan muaf tutan kurumlar var. Güven: düşük.

### Cited findings
- Güncel Sosyoloji dergisinin başvuru formu, anket, mülakat, odak grup, gözlem, deney ya da görüşmeyle katılımcılardan veri toplayan her araştırma için etik kurul onayı istiyor ve onayın makalede belgelenmesini şart koşuyor. Form TR Dizin'i anmıyor; tezleri bağlayan bir kural değil. — [Güncel Sosyoloji başvuru formu, t.y.](https://form.jotform.com/241946062214351)
- Başka bir dergi, onay gerektiren çalışmalarda yöntem bölümünde kurulun adının, karar tarihinin ve sayısının verilmesini istiyor. — [TEKE Dergisi, t.y.](https://tekedergisi.com/)
- ETH Zürih'te öğrenci tezleri onaya tabidir. Lisans ve yüksek lisans tezleri ise daha hızlı incelenir. — [ETH Zürih, t.y.](https://ethz.ch/en/research/ethics/ethics-commission/responsibility.html)
- ETH Zürih'te uzmanların teknik bir ürünü test etmesi, ürünü yalnız geliştiricileri test ediyorsa ya da yayın amacı yoksa onay gerektirmez. Yayın için kurul bir "sorumsuzluk beyanı" (waiver) verebilir. Bu muafiyet tıbbi cihaz testlerine uygulanmaz. — [ETH Zürih, t.y.](https://ethz.ch/en/research/ethics/ethics-commission/responsibility.html)
- Reviewer'ın aktarımına göre 2013 tarihli Klinik Araştırmalar Hakkında Yönetmelik yürürlükten kalktı. Yerine 27.5.2023 tarihli Beşeri Tıbbi Ürünlerin Klinik Araştırmaları Hakkında Yönetmelik geçti ve bu yönetmelik müdahalesiz çalışmaları kapsamıyor. Ben duyuruyu da Resmî Gazete metnini de açmadım (PDF). — [Hacettepe KAEK duyurusu, 2023](https://kliniketik.hacettepe.edu.tr/belge/HUKlinikArastirmalarEtikKuruluOnemliDuyuruKasim2023.pdf)

### Inferences
- İlaç klinik araştırmaları yönetmeliği bu çalışmayı kapsamıyorsa yetki üniversitenin kendi yönergesine kalır. Muhatap olasılıkla girişimsel olmayan araştırmalar etik kurulu ya da sosyal ve beşerî bilimler etik kuruludur; doğrulanmadı.
- Öneri (değiştir): klinisyen puanlama oturumları, kuruldan onay ya da yazılı "onay gerekmez" kararı alınmadan başlamasın. Bu ihtiyatlı yol, muafiyetin var olduğu kurumlarda da kurul görüşünü gerektiriyor.

### Gaps
- TR Dizin'in etik ölçütlerinin kendi metni: trdizin.gov.tr/kriterler sayfası içerik döndürmedi.
- Tezin bağlı olduğu üniversitenin etik kurul yönergesi: üniversite bilinmediği için okunamadı. Hızlandırılmış inceleme ya da muafiyet yolu bu yönergede aranmalı.
- 2023 yönetmeliğinin kapsam maddesi.

## Is there a recognised distinction between an expert acting as a research participant (their judgements are the data) and an expert acting as a contributor or consultant who validates study materials, and how do journals and ethics bodies treat each?

### Takeaway
Bu ayrım en az bir ethics body'de açıkça tanınıyor: uzman bilgi kaynağı mı, yoksa araştırmanın nesnesi mi. Türk kurullarında ya da ICMJE/COPE metinlerinde aynı ayrımı aramadım. Güven: orta (tek kurum).

### Cited findings
- ETH Zürih, görüşme, Delphi ya da anket biçimindeki uzman danışmalarını üç koşul birlikte sağlanırsa onaydan muaf tutuyor: veri toplama yalnız uzman bilgisine odaklanır ve uzman araştırmanın nesnesi değil, bilgi kaynağıdır; ücret ödenmez; çalışmada yanıltma, eksik bilgilendirme ya da uyarıcı gibi hiçbir deneysel öğe yoktur. — [ETH Zürih, t.y.](https://ethz.ch/en/research/ethics/ethics-commission/responsibility.html)
- Muaf danışmada da araştırmacı veri korumasından, aydınlatılmış onamdan ve gönüllülükten sorumludur. Uzmana yayında nasıl anılmak istediği sorulur. — [ETH Zürih, t.y.](https://ethz.ch/en/research/ethics/ethics-commission/responsibility.html)
- Aynı kurum, bir meslek grubunun yapay zekâ kullanımını kabulünü ölçen randomize bir anketi onaya tabi örnek olarak veriyor. Bu durumda kişilerin tutumu araştırmanın nesnesidir. — [ETH Zürih, t.y.](https://ethz.ch/en/research/ethics/ethics-commission/responsibility.html)
- Bir Delphi yöntem makalesi, yöntem makalesi için kurul onayı gerekmediğini, ancak vaka çalışmasının "exempt" statüsüyle onaylandığını bildiriyor. Bu, muafiyetin de kurulca verildiğini gösteriyor. — [Nursing Research, 2018](https://journals.lww.com/nursingresearchonline/Abstract/2018/09000/Methodology_Update__Delphi_Studies.8.aspx)

### Inferences
- Altın yanıtları düzelten ve onaylayan klinisyen bilgi kaynağıdır, muafiyet koşullarına en yakın konumdur. Teşekkür bölümünde ya da yazar olarak anılabilir.
- Puanlama oturumu ise sınırda kalıyor. Klinisyenler yanıtları yapılandırmaya kör olarak puanlıyor; bu "eksik bilgi" sayılabilir. Ayrıca klinisyen–klinisyen uyumu ve inceleme süresi raporlanırsa klinisyenin kendisi ölçülmüş olur. İkisi de muafiyeti zayıflatır. Ücret ödenirse ETH ölçütüne göre muafiyet düşer.
- Öneri (değiştir): altın onay sürecinde süre ve uyum ölçülmesin; ölçülecekse bu süreç de başvuruya eklensin. Puanlama oturumu başvuruda "uzman değerlendirmesi" olarak tanımlansın, karar kurula bırakılsın.

### Gaps
- ICMJE, COPE ve Türk kurullarının uzman paneli ya da Delphi çalışmalarına bakışı aranmadı.

## What does KVKK require for raters' identity and timing data, and for using publicly posted patient questions from a health forum (legal basis, health data as special category, anonymisation, Board decisions on publicly available data)?

### Takeaway
Forum soruları büyük olasılıkla sağlık verisi, yani özel nitelikli veri içerir. Kişinin kendisinin alenileştirmesi ve bilimsel amaç istisnası koşullu dayanaklardır. Değerlendirici verisi kişisel veridir. Güven: kanun metni için yüksek, uygulama için yorum. Not: mevcut tasarımda forum sorusu yok; bu bölüm yalnız gerçeklik kontrolü eklenirse geçerli.

### Cited findings
- Md. 6(1): sağlık verisi özel nitelikli kişisel veridir. — [KVKK, 6698 s. Kanun](https://www.kvkk.gov.tr/Icerik/6649/Personal-Data-Protection-Law)
- 7499 sayılı Kanun 12.03.2024 tarihli ve 32487 sayılı Resmî Gazete'de yayımlandı, 1.6.2024'te yürürlüğe girdi. Md. 9 için 1.9.2024'e kadar geçiş süresi tanındı. — [Legal500, 2024](https://www.legal500.com/intelligence/turkey/privacy/standard-contract-notification-obligation-and-penalties); [istanbullawyerfirm, 2026](https://istanbullawyerfirm.com/blog/legal-protection-saas-turkey)
- 7499 ile değişik md. 6(3)(ç): özel nitelikli veri, ilgili kişi alenileştirmişse ve alenileştirme iradesine uygun işleniyorsa işlenebilir. — [KVKK, 6698 s. Kanun](https://www.kvkk.gov.tr/Icerik/6649/Personal-Data-Protection-Law)
- Md. 6(3)(e)'deki sağlık istisnası sır saklama yükümlüleri ve yetkili kurumlar içindir; araştırmayı saymaz. — [KVKK, 6698 s. Kanun](https://www.kvkk.gov.tr/Icerik/6649/Personal-Data-Protection-Law)
- Md. 6(4): Kurul'un belirlediği yeterli önlemler alınmalıdır. — [KVKK, 6698 s. Kanun](https://www.kvkk.gov.tr/Icerik/6649/Personal-Data-Protection-Law)
- Md. 28(1)(c): özel hayat ve kişilik hakları ihlal edilmemek ve suç oluşturmamak koşuluyla bilimsel amaçlı işlemeye Kanun uygulanmaz. — [KVKK, 6698 s. Kanun](https://www.kvkk.gov.tr/Icerik/6649/Personal-Data-Protection-Law)
- Md. 28(1)(b): anonim verinin araştırma ve istatistik amaçlı işlenmesi muaftır; bent resmî istatistik bağlamında yazılmıştır. — [KVKK, 6698 s. Kanun](https://www.kvkk.gov.tr/Icerik/6649/Personal-Data-Protection-Law)
- Md. 28(2)(b): alenileştirilmiş veride md. 10, 11 (tazminat hariç) ve 16 uygulanmaz. — [KVKK, 6698 s. Kanun](https://www.kvkk.gov.tr/Icerik/6649/Personal-Data-Protection-Law)
- Md. 9: yurt dışına aktarım için md. 5/6 şartı ile birlikte yeterlilik kararı ya da standart sözleşme gibi bir güvence gerekir. Standart sözleşme 5 iş günü içinde Kurum'a bildirilir. — [KVKK, 6698 s. Kanun](https://www.kvkk.gov.tr/Icerik/6649/Personal-Data-Protection-Law)
- Usul yönetmeliği 10.7.2024 tarihli ve 32598 sayılı Resmî Gazete'de yayımlandı. — [Legal500, 2024](https://www.legal500.com/intelligence/turkey/privacy/standard-contract-notification-obligation-and-penalties); [AA, 2024](https://www.aa.com.tr/tr/gundem/kisisel-verilerin-yurt-disina-aktarilmasina-iliskin-yonetmelik-resmi-gazetede-yayimlandi/3271015)
- Md. 7: amaç ortadan kalkınca veri silinir, yok edilir ya da anonimleştirilir. — [KVKK, 6698 s. Kanun](https://www.kvkk.gov.tr/Icerik/6649/Personal-Data-Protection-Law)
- 2026/1301 sayılı ilke kararı (1.7.2026), kamu kurumlarının internette kişisel veri yayımlamasıyla ilgili ve bu projeye doğrudan dokunmuyor. — [Cottgroup, 2026](https://www.cottgroup.com/tr/mevzuat/item/new-kvkk-agenda-for-public-institutions-principle-decision-no-2026-1301-on-the-online-publication-of-personal-data)

### Inferences
- Tek dayanak seçilmeli (değiştir). Md. 28(1)(c) uygulanırsa Kanun bütünüyle, md. 6 ve 9 dahil, uygulanmaz; bu yüzden önceki notlardaki "md. 9 + md. 28" birleşimi tutarsızdı. Önerim, forum sorularının toplanır toplanmaz, yani modele gönderilmeden önce anonimleştirilmesi ya da yeniden yazılması: ad, yer, tarih ve nadir ayrıntılar çıkarılır. Gerçekten anonim veri kişisel veri değildir. Bu, md. 28(1)(c)'nin "özel hayatın ihlal edilmemesi" koşulunu da destekler. Anonimleştirme yöntemi etik kurula beyan edilmeli. Kanıt: yorum.
- Bulut API çağrısının md. 9 anlamında "aktarım" sayıldığına dair bir Kurul kararı ya da rehberi bulamadım. Bu nedenle "kanıt yüksek" ifadesini geri çekiyorum. Anonimleştirme uygulanırsa soru büyük ölçüde ortadan kalkar. Ek güvence olarak ham forum metni yalnız K4'te, yani yerel modelde işlenebilir (ekle).
- Değerlendirici verisi kişisel veridir. Ad yerine kod kullanılmalı, süre verisi yalnız toplu raporlanmalı, md. 10'a uygun bir aydınlatma metni hazırlanmalı. Klinisyen sayısı 2–3 olduğu için "anonim" değil "takma adlı" denmeli (ekle; kanıt orta).

### Gaps
- Kurul'un alenileştirme ve sağlık verisinde yeterli önlemler konulu kararları açılmadı.
- Kurum'un Şubat 2025 tarihli olduğu söylenen aktarım rehberi açılmadı; bulut çağrısı sorusunu bu rehber yanıtlayabilir.
- Forum sitesinin kullanım koşulları ve telif durumu araştırılmadı.

## Which statements should the thesis include to document compliance (ethics approval number or exemption, data protection, device status)?

### Takeaway
En az dört ifade gerekli: etik kurul kararı ya da "onay gerekmez" yazısı, kurul adı, tarih ve sayısıyla; cihaz durumu ve amaç beyanı; KVKK yöntemi; API sağlayıcısı ve veri bölgesi. Güven: orta.

### Cited findings
- Dergilerin ortak pratiği, yöntem bölümünde kurulun adını, karar tarihini ve sayısını vermektir. — [TEKE Dergisi, t.y.](https://tekedergisi.com/); [Güncel Sosyoloji başvuru formu, t.y.](https://form.jotform.com/241946062214351)
- Muaf danışmalarda bile uzmana yayında nasıl anılmak istediği sorulur. — [ETH Zürih, t.y.](https://ethz.ch/en/research/ethics/ethics-commission/responsibility.html)

### Inferences
- Yöntem bölümüne eklenecek şablon (ekle):
  - Etik: kurul adı, karar tarihi ve sayısı ya da "onay gerekmez" yazısı.
  - Klinisyenler: onam alındı, takma ad kullanıldı, anılma biçimi seçildi.
  - Cihaz: piyasaya arz edilmemiş araştırma prototipi; amaç beyanı birebir verilir.
  - Veri: maddeler sentetik; forum soruları, kullanılırsa, anonimleştirildi; API sağlayıcısı ve bölgesi belirtilir.
- Sınırlılık olarak raporlanacaklar: cihaz statüsü ve AB Yapay Zekâ Yasası hukuki görüşle değerlendirilmedi.

### Gaps
- AB Yapay Zekâ Yasası md. 2(6) araştırma istisnası aranmadı.

## Beyond the assignment
- KVKK, 28 Ekim 2026'da "Klinik Araştırmalarda Kişisel Verilerin Korunması Çalıştayı" düzenledi. Yeni bir rehber gelebilir; etik başvurusundan önce kontrol edilmeli. — [KVKK, 2026](https://www.kvkk.gov.tr/Icerik/6639/Board-Resolutions)

## Changes
- Form yanlış biçimde "TR Dizin" diye etiketlenmişti → derginin kendi formu olarak yeniden etiketledim. TR Dizin sayfası boş döndü, metni Gaps'e taşıdım. "Ayrımı kuran kaynak yok" ifadesini kaldırdım; Delphi ve uzman danışması aramasıyla ETH Zürih ölçütünü ekledim. Hipotezin bir parçası bu kaynakla çürüdü.
- Md. 9 ile md. 28(1)(c) birlikte kullanılmıştı → tek yol seçtim: toplama anında anonimleştirme ve md. 28(1)(c). "Aktarım" iddiasını yorum düzeyine indirdim. Önerinin yalnız forum sorusu eklenirse geçerli olduğunu yazdım.
- 7499'un tarihleri → Resmî Gazete 12.03.2024 ve sayı 32487, yürürlük 1.6.2024 eklendi; aktarım yönetmeliği 10.7.2024 eklendi.
- 2013 yönetmeliği hâlâ geçerliymiş gibi anılmıştı → 2023 yönetmeliğini reviewer'ın aktarımı olarak not ettim. Metni açamadım; kapsam maddesini Gaps'e koydum.
- Cihaz kanıtı "orta" diye derecelendirilmişti → "düşük; birincil metinle doğrulanmadı" yaptım. Tıbbi Cihaz Yönetmeliği'nin Resmî Gazete künyesini ekledim.
- Ekipler arası çelişkiler (mg/kg aktarımı ve triyaj işlevi) → amaç beyanını sistemin gerçek işleviyle tutarlı olacak biçimde yeniden yazdım. mg/kg konusunun altın yanıtlardan önce karara bağlanmasını önerdim.
===== end of researcher-6 =====

---

THE REVIEWS

===== reviewer-1 =====
# Review

## Overall
researcher-1, -3 ve -4'ün açabildiğim kaynakları bulgularını taşıyor, hesapları da tutuyor. researcher-2'nin notları bu haliyle duramaz: birkaç temel bulgu gösterilen kaynakta yok ve "yüksek kanıt gücü" etiketi hak edilmemiş. Kanıtın çoğu önbaskı ve tek çalışma; ekip bunu çoğunlukla işaretlemiş. Açamadıklarım: Fagerland 2013, NICE NG143, Bean ve ark., Vach ve ark., Rosie tam metinleri.

## researcher-1
Solid: Pombal oranları, HealthBench doğrulaması (34 ölçüt, 60.896 yargı, makro-F1 0,709, 5/7 tema), Lee düzeltmesi ve Miller sayıları kaynakla birebir. κ aralığı, Wilson sınırı, 0,95⁵, çoğunluk dönüşümü ve H3b gücünü yeniden hesapladım; doğru.
Problems:
1. [should] "raporlama literatürü sınıf bazlı duyarlılık/özgüllük istiyor" → aynı notlar CHART ve TRIPOD-LLM maddelerinin doğrulanamadığını söylüyor → cümleyi çıkar; "Supported"ı "iki önbaskının uygulamasıyla" diye daralt.
2. [should] "çok hata yapan konfigürasyon (K0) daha çok şişer… H3b için anti-tutucu" → Pombal aynı üreticinin konfigürasyonlarını karşılaştırmıyor; Claude hakemlerinin HealthBench oranı 1'in altında → varsayım olarak yaz.
3. [should] "Claude'un HealthBench aile oranı… yoktu" → tabloda var (Sonnet 0,89; Haiku 0,91). "Hekim ortalamaları 0,646–0,730" → tabloda 0,569–0,730. "m=200 ≈ 0,1" → yalnız q0=0,7, q1=0,9, p̂=0,3 için. Üçünü düzelt.
4. [should] "kanıt güçlü, tek simülasyon çalışması" → kendi içinde tutarsız; kaynağı açamadım → "orta" de.

Missing: Eşdeğersizlik marjı için birincil standart metni; H3b önerisi buna dayanıyor.

## researcher-2
Solid: DoktorSitesi kaydı (167.732 satır, alanlar, CC BY 4.0), DIAN (50 soru, 148 puanlayıcı) ve HealthBench ölçek sayıları doğru. Saniye/madde aritmetiği yerinde bir uyarı.
Problems:
1. [must] "gerçek kullanıcı trafiğine kıyasla tekdüze" (Teixeira de Lima) ve "daha düşük N-gram çeşitliliği… gerçek dünya performansını olduğundan yüksek gösterir" (Filice) → iki özet de gerçek sorgularla karşılaştırma ya da şişme bildirmiyor; yalnız üreticilerin dengesizliğini/çeşitlilik eksikliğini söylüyor → bulguları buna indir; hükmü "Supported"dan "Undecided"a çek.
2. [must] "çıpalama ve otomasyon yanlılığı… doğruluğunu başlangıç seviyesinin altına düşürdüğü" (Arora 2025) → HealthBench'te böyle bir bulgu yok → gerçek kaynağı bul ya da sil.
3. [must] HealthBench → "madde başına en az 3–5 dakika" → kaynakta süre verisi yok → ekibin yargısı olarak işaretle, pilotla ölç; "bilimsel olarak savunulamaz"ı çıkar.
4. [must] "etik kurul onayı gerektirmeyen… anonimleştirilmiş" → Zenodo kaydı onam ya da anonimleştirmeden söz etmiyor → iddiayı kaldır, etik kurula sor.
5. [must] "genellikle 20 ile 200" ve Rosie bulguları → aralığın kaynağı yok. İspanyolca Rosie [30 kişilik pilot RKÇ](https://formative.jmir.org/2026/1/e101898); test seti kurulumunu anlatmıyor. İlk çalışma 2024 tarihli. "Güç hedeflerini koru (yüksek)" bunlardan çıkmaz → sil ya da yeniden kaynakla.
6. [must] K-QA "hekimlerce… ayrıştırılan 1.212 soru" → özete göre yalnız bir alt küme yanıtlanmış → düzelt.
7. [should] CARES/OR-Bench "label flipping" iddiaları özet sayfalarında yok → tam metinden alıntı göster ya da çıkarım olarak yaz.
8. [should] MediQ "%20–22… kanıtlamıştır" → özet %22,3 diyor, taban belirsiz. HealthBench'te bağlam arama eksen değil tema.

Missing: LLM taslağı incelemesinde otomasyon yanlılığını ölçen gerçek deneysel çalışmalar.

## researcher-3
Solid: Fraile Navarro (%16,7 / %50 / %20,8; yaklaşık %60 koşullu), Jha ve ark. (N=150, %86,7, 50 karakterlik pencere, şablonlar), NHS dozları, Health-ORSC-Bench ve MedHarm doğru. Üç kuralı ile 29/59 madde hesapları doğru; hüküm ölçülü.
Problems:
1. [should] "0–5 ay için >60" (NG143) → sayfayı açamadım; bildiğim tabloda >60 yaştan bağımsız kırmızı, >50 ve >40 sarı sütunda. Üç aydan küçükte ≥38 °C kırmızısı da eksik → birincil metinden düzeltmeden kural listesine alma.
2. [should] "LLM hakemlerini klinisyenlere kör olarak denetletti" → denetim 24 amaçlı seçilmiş yanıt; klinisyen iki hakemle birlikte yalnız 4/23'te uyuşuyor; %60 anahtar sözcük sezgiseliyle bulunmuş → bunları yaz.
3. [should] "Benzer çalışmalar 150 civarı" → tek önbaskı. Düzenleyici bölüm iki ikincil web sayfasına dayanıyor; "KVKK yükü düşük" doğrulanmamış.

Missing: Bakanlık protokollerinin kendi tehlike işaretleri.

## researcher-4
Solid: Liu ve ark. (OR 1,35; insan 1,65, otomatik 1,20; Egger), Kim ve ark. (%22; %6/%5), Zerhoudi ve Hassan özetleri doğru. "(özetten)" işaretleri ve "Undecided" hükmü dürüst.
Problems:
1. [should] "iki bağımsız çalışma" (Türkçe erişim) → biri Almanca (Vach); Türkçe kanıt 100 soruluk tek önbaskı → güveni "düşük" yap.
2. [should] "H2'yi doğrulayıcı olmaktan çıkar" → doğrudan kanıt yok, %10 eşiği keyfi → dev pilotuna bağlı koşullu öneri yap.
3. [should] "ilk 16 pasaj yerine… 3–5" → 16 Kim'in kurulumu, tasarımın değil; 3–5'in kaynağı yok.
4. [should] "%20,0… %70,6" → farklı modeller karşılaştırılıyor → hüküm cümlesinde belirt.

Missing: AMAQA birincil makalesi.

## Contradictions between researchers
- researcher-2 "güç hedeflerini koru" diyor. researcher-1 (H3b gücü ≈0,63), researcher-3 (T1'de 40 madde yetmez) ve researcher-4 (H2 güçsüz) tersini hesapla gösteriyor.
- researcher-2'ye göre question-first akışı H1'de erişime haksız avantaj vermez. researcher-4'e göre altın yanıtlar derlemden yazıldığı için K1 yapısal olarak kayrılır; tasarım metni researcher-4'ü destekliyor.
- researcher-2 H2 ölçütünü "koru" diyor, researcher-4 ikincile indiriyor.
- researcher-2 açık veri için etik onay gerekmediğini söylüyor; researcher-3 etik/KVKK'yı doğrulanmamış sayıyor.
- researcher-3'ün doz/tanı bayrağı ayrımı, researcher-1'in "güvensiz yanıt" duyarlılık eşiğinin tanımını değiştirir; hakem doğrulamasından önce çözülmeli.

## What can be stated with confidence, and what cannot
Güvenle söylenebilir:
- Türetilmiş ikili etikette tek κ, en iyi uygulamanın gerisinde.
- 100 yanıtla duyarlılık ≥0,90 doğrulanamaz.
- Çoğunluk ve en kötü durum kestirimleri tekrar sayısına bağlı.
- 40 maddede sıfır hata "güvenli" demeye yetmez.
- Yayımlanmış RAG kazancı küçük ve yayın yanlılığı taşıyor.
- Resmi ebeveyn bilgilendirmesi (NHS) yaşa göre doz veriyor.

Söylenemez:
- Sentetik soruların doğruluğu ne kadar şişirdiği.
- Klinisyen incelemesine madde başına kaç dakika gerektiği.
- Aynı aile hakemin K0–K3 farklarını hangi yönde kaydırdığı.
- Yaş filtresinin etkisi ve Türkçede en iyi erişim kurulumu.
- Kural katmanının net yararı.
- Prototipin hukuki statüsü.

## Verdicts
VERDICT researcher-1: accept
VERDICT researcher-2: revise
VERDICT researcher-3: accept
VERDICT researcher-4: accept
===== end of reviewer-1 =====

===== reviewer-2 =====
# Review

## Overall
Ekip soruyu kısmen yanıtladı. researcher-6'nın KVKK bulguları kanun metniyle örtüşüyor ve açamadığı metinleri dürüstçe boşluk olarak bildiriyor. researcher-5'in notları bu hâliyle altın yanıt yazımına temel olamaz. Bağlantıların tümü opak yönlendirme adresi, etiketleri gerçek belgeyle uyuşmuyor ve "Refuted" hükmünün dayandığı sayısal doz bulgusu birincil metinde doğrulanamadı. Etik onay ve cihaz durumu soruları hâlâ açık.

## researcher-5
Solid: Doğum Sonu Bakım Yönetim Rehberi'nin bilgi tabanında bulunmadığı tespiti plan listesiyle uyumlu. Dönüşümlü ateş düşürücü uyarısı açtığım sayfada geçiyor. NG194'ün "ilk 24 saatte sarılık" maddesi [NICE QS37](https://www.nice.org.uk/guidance/QS37/chapter/quality-statement-3-symptoms-and-signs-of-illness-in-babies) üzerinden doğrulandı. Doz ayrımını dev sette sınama önerisi yerinde.

Problems:
1. [must] "…İzlem Protokolleri (2018)… parasetamolün 10–15 mg/kg/doz… 60 mg/kg/gün…" → Bağlantı Bakanlık yayınına değil, sbu.edu.tr'deki "cocuksaghastcomp" adlı bir PDF'e gidiyor; içeriğini okuyamadım. Aramada protokolün [eski sürümünde](https://dosyamerkez.saglik.gov.tr/Eklenti/6406/0/bebek-ve-cocuk-izlem-protokolleripdf.pdf) yalnız "2 aydan büyük, ≥39 °C'de parasetamol; 2 aydan küçük ≥38 °C acil sevk" çıkıyor, mg/kg yok. "Refuted" hükmü ve T3 bayrağının yeniden tanımı bu bulguya dayanıyor. → Bilgi tabanındaki PDF'ten sayfa numarasıyla birebir alıntı verin; yoksa hükmü "Undecided" yapın.
2. [must] "Sağlık Bakanlığı Ateş Rehberi, 2023… dozun yaşına değil kilosuna göre… ev kaşığı…" ve "ebeveyn bilgilendirmeleri… <3 ay… acil" → Bağlantı [Denizli İl Sağlık Müdürlüğü'nün 26.12.2022 tarihli haberine](https://denizliism.saglik.gov.tr/TR-267872/uzmanindan-cocuklarda-oksuruk-ve-ates-ile-ilgili-oneriler.html) gidiyor; tek hekimin görüşü. Sayfada kilo/yaş, ev kaşığı, prospektüs ya da 3 ay kuralı yok. "Eşik Çelişkisi 2" ve K3'ün `<3 ay` kuralının Türk dayanağı düşüyor. → Belgenin gerçek adını ve tarihini yazın; bulguları geri çekin ya da ulusal metinle kanıtlayın.
3. [must] "Sağlık Bakanlığı, 2024" (ateş savunma mekanizması, ilk tercih parasetamol…) → Tek kaynağı LINK CHECK'te açılmayan bağlantı. → Çıkarın ya da çalışan birincil bağlantı verin.
4. [must] "NICE NG194… saatte >1 ped ıslatma veya erikten büyük pıhtı" → nice.org.uk 403 verdi. İkincil aktarımlarda NG194 yalnız "ani, çok yoğun ya da artan kanama; pıhtı, plasenta dokusu" diyor; sayısal eşik yok. "Kanama eşiği farkı" ve birleşik tablodaki "saatte ≥1–2 ped" kaynaksız. → Çıkarın. Türk rehberine atfedilen "20–30 dakikada 2–3 ped" de doğrulanamadı (PDF okunamadı).
5. [must] "TİTCK onaylı Kullanma Talimatı… 2024… Yüksek kesinlik" → Metinler ilacrehberi/ilacfiyati kopyalarından alınmış. Açtığım Calpol PDF'inin üstverisi 2012–2013; içeriğini okuyamadım; bir bağlantı ölü. Güncel onaylı sürüm gösterilmemiş. → TİTCK KÜB/KT sisteminden onay tarihiyle doğrulayın; o zamana dek S-YAS/T3 altın maddesi yapmayın.
6. [should] "her eşikte en güvenli/koruyucu sınırı" esas alan birleşik tablo → İngiliz kılavuzunu, Türkiye'de geçerliliği gösterilmeden ulusal altın standarda taşıyor. KT'deki "2. ay aşısı sonrası tek doz" ile "<3 ay ilaç vermeden hekime" maddesi de çelişiyor. → Kararı klinisyenlere bırakın, sapmayı sınırlılık olarak yazın.
7. [should] "DoktorYaşar" kişisel sitesi bir "çelişki"nin ve aşı profilaksisi bulgusunun tek kaynağı. → Resmî metinle değiştirin.

Missing: Gebelikte NSAİİ için ürün KÜB'ü; 2018 protokolünün ateş eşiği (38/39 °C) için sayfa alıntısı.

## researcher-6
Solid: [KVKK metni](https://www.kvkk.gov.tr/Icerik/6649/Personal-Data-Protection-Law) md. 6(3), md. 9 (beş iş günü), md. 28(1)(b)-(c) ve 28(2)(b) aktarıldığı gibi. [2026/1301 sayılı karar](https://www.cottgroup.com/tr/mevzuat/item/new-kvkk-agenda-for-public-institutions-principle-decision-no-2026-1301-on-the-online-publication-of-personal-data) ve 28 Ekim 2026 çalıştayı doğrulandı. [Rumb](https://rumb.fr/mdcg-2019-11-rev.1) içeriği aktarımla örtüşüyor. "Undecided" hükmü kanıtla orantılı.

Problems:
1. [must] "TR Dizin kaynaklı… ölçüt" ve "Bu ayrımı açıkça kuran bir kaynak yok" → [Açtığım form](https://form.jotform.com/241946062214351) bir sosyoloji dergisinin başvuru formu; TR Dizin'i anmıyor, tezleri bağlayan bir kural da değil. "Yok" bulgusu ICMJE/COPE/Delphi aranmadan yazılmış. Üç bölümün önerisi bu tek forma dayanıyor. → TR Dizin etik ölçütlerinin kendi metnini ve tezin üniversitesinin etik kurul yönergesini alıntılayın; "yok"u "aranmadı" yapın.
2. [should] "md. 9 kapsamında yurt dışına aktarımdır… kanıt yüksek" ile "md. 28(1)(c)… kullanmak" → Md. 28(1)(c) uygulanırsa Kanun, md. 6 ve 9 dahil, hiç uygulanmaz; ikisi birlikte savunulamaz. API çağrısının "aktarım" sayılması Kurul kararı ya da rehberiyle gösterilmemiş. → Tek dayanak seçin, kanıtı "yorum" olarak derecelendirin. Plandaki tasarımda forum sorusu yok; önerinin koşulu yazılsın.
3. [should] "2 Mart 2024 tarihli 7499 sayılı Kanun" → Metindeki tarih kabul tarihi. → Resmî Gazete ve yürürlük tarihlerini ekleyin (bildiğim kadarıyla 12.3.2024 ve 1.6.2024; bu oturumda doğrulamadım).
4. [should] Gaps'teki "Klinik Araştırmalar Hakkında Yönetmelik" → Arama özetine ve [Hacettepe duyurusuna](https://kliniketik.hacettepe.edu.tr/belge/HUKlinikArastirmalarEtikKuruluOnemliDuyuruKasim2023.pdf) göre 2013 yönetmeliği yürürlükten kalktı. Yerine 27.5.2023 tarihli Beşeri Tıbbi Ürünlerin Klinik Araştırmaları Hakkında Yönetmelik geçti; müdahalesiz çalışmaları kapsam dışı bırakıyor. Resmî Gazete metnini açmadım. → Güncel metne göre yeniden yazın.
5. [should] Cihaz durumu önerisi "kanıt orta" → Dayanak danışmanlık sayfaları (Rumb kendini "normatif değil" diye niteliyor) ve "bellekten" yorum. MDCG kılavuzunun Türkiye'de nasıl uygulandığı gösterilmemiş. → "Düşük; birincil metinle doğrulanmadı" yapın.

Missing: Tıbbi Cihaz Yönetmeliği ve varsa TİTCK yazılım kılavuzu metni; üniversite yönergesi; Kurul'un yurt dışına aktarım rehberi.

## Contradictions between researchers
- researcher-5, `10–15 mg/kg` kuralının aktarılmasını "güvenli genel bilgi" sayıyor. researcher-6'nın amaç beyanı "doz önerisi amacı taşımaz" diyor. Anne mg/kg'dan dozu kendi hesaplayabilir; hangisinin geçerli olduğuna karar verilmeli.
- researcher-5'in genişletilmiş kırmızı bayrak tablosu triyaj işlevini güçlendiriyor. Bu, researcher-6'nın "triyaj amacı taşımaz" beyanıyla gerilimli.

## What can be stated with confidence, and what cannot
Güvenle:
- KVKK'da sağlık verisi özel niteliklidir; alenileştirme ve bilimsel amaç istisnaları koşulludur.
- MDCG 2019-11 Rev.1 Haziran 2025 tarihlidir (yalnız ikincil kaynak).
- Bilgi tabanında lohusalık rehberi yoktur.
- NG194 sayısal ped eşiği vermez.

Söylenemez:
- 2018 protokolünün mg/kg doz içerdiği.
- KT tablolarının güncel sürümü.
- Bakanlık ebeveyn metinlerinde `<3 ay` kuralı bulunduğu.
- Ped eşikleri.
- Etik onayın hukuken zorunlu olup olmadığı ve hangi kurulun yetkili olduğu.
- Prototipin cihaz mevzuatı dışında kaldığı.
- API çağrısının md. 9 anlamında aktarım sayıldığı.

## Verdicts
VERDICT researcher-5: revise
VERDICT researcher-6: revise
===== end of reviewer-2 =====

===== panel-1 =====
# Review

## Overall
İlk hakemin `researcher-2` için verdiği altı `[must]` maddesinin tamamı bu turda çözülmüş; `researcher-2` kaynaklarıyla uyumlu ve dürüst bir metne dönüşmüş. Buna karşılık ilk hakem `researcher-1`, `researcher-3` ve `researcher-4`'e erken `accept` vererek fazla hoşgörülü davranmış; bu üç araştırmacı notlarını hiç güncellemediği için ilk incelemedeki hatalar olduğu gibi duruyor. Üstelik ilk hakemin açamadığı NICE NG143 ve Lee ve ark. (2025) kaynaklarını açtığımda `researcher-1` ve `researcher-3`'te düzeltilmesi zorunlu (`[must]`) olgu ve kanıt hataları saptadım. Ayrıca ekip, tek bir yüksek lisans öğrencisinin 3 saatlik klinisyen bütçesiyle yapılamayacak kadar çok ek iş öneriyor.

## researcher-1
Solid: Pombal ve ark. (2026), Arora ve ark. (2025; 60.896 yargı, makro-F1 0,709), Miller (2024) ve ilk hakemin açamadığı Fagerland ve ark. (2013; 9.595 senaryo, ortalama tip I hata 0,0201) kaynaklarıyla doğrulandı; κ güven aralığı, Wilson alt sınırı ve H3b güç hesapları sağlam. CHART BMJ Medicine tam metnini ve `2608.18091` önbaskısını ben de yalnızca özet düzeyinde görebildim.
Problems:
1. [must] "İkinci kısım **Supported**: … raporlama literatürü sınıf bazlı duyarlılık/özgüllük istiyor" ve "simülasyonda m=200 yaklaşık 0,1 genişliğinde aralık veriyor" → İlk hakem bunu `[should]` sayarak fazla hoşgörülü davrandı: notların kendisi CHART, TRIPOD-LLM ve MI-CLEAR-LLM maddelerinin açılamadığını söylüyor; kanıt yalnızca iki önbaskıya dayanıyor. Ayrıca açtığım Lee ve ark. (`2511.21140`) kaynağında kalibrasyon örneklemi toplam 200 değil, sınıf başına `m0=200` ve `m1=200` (toplam 400 insan etiketi; `q0=0,7, q1=0,9, p=0,4, n=1000`). 100 klinisyen yanıtıyla bu aralık elde edilemez → Hipotezdeki "raporlama literatürü istiyor" iddiasını çıkarıp hükmü iki önbaskıyla sınırla; Lee ve ark.'nın `m0=200, m1=200` koşulunu düzelt ve tek öğrencilik tezde 400 kalibrasyon etiketinin uygulanabilirlik sınırını yaz.
2. [should] İlk incelemeden kalan üç düzeltme yapılmamış: Pombal'da Claude HealthBench aile oranı tabloda var (Sonnet 0,89; Haiku 0,91); Arora'da hekim tema ortalamaları 0,569–0,730 (0,646–0,730 değil); Fagerland için "kanıt güçlü, tek simülasyon çalışması" ifadesi kendi içinde çelişkili → Üçünü de düzelt.
3. [should] "çok hata yapan konfigürasyon (K0) daha çok şişer… H3b için anti-tutucu" → Pombal aynı üreticinin RAG konfigürasyonlarını karşılaştırmıyor ve Claude öz-kayırma oranı HealthBench'te 0,93 (<1) → Kanıtlanmış mekanizma gibi değil, test edilecek varsayım olarak yaz.
Missing: Eşdeğersizlik marjı (CONSORT non-inferiority) için birincil standart kaynağı ve bileşik doğruluk ölçütünde ("tüm zorunlu maddeler var") Lee düzeltmesinin nasıl uygulanacağı.

## researcher-2
Solid: İlk incelemedeki altı `[must]` maddesinin tamamı çözülmüş: (1) Teixeira de Lima (2024) ve Filice (2025) bulguları kategori dengesizliği ve çeşitlilik şartlandırmasına indirilip hipotez `Undecided` yapılmış; (2) Arora (2025) altındaki hatalı otomasyon yanlılığı atfı silinip doğruladığım Jabbour ve ark. (2023; -11,3 puan) ile Qazi ve ark. (2025; %84,9'dan %73,3'e, -14,0 puan) eklenmiş; (3) HealthBench süre iddiası kaldırılıp ~17,5 sn/madde hesabı "ekibin operasyonel yargısı" olarak işaretlenmiş; (4) `DoktorSitesi` için etik kurul ve KVKK şartı getirilmiş; (5) kaynaksız "20–200" aralığı ve Rosie hatası düzeltilip Peled (15 soru), DIAN (50 soru, 148 değerlendirici: 119 kadın, 29 klinisyen) ve alt küme güç kısıtları doğru yazılmış; (6) K-QA'da ayrıştırılan alt küme 201 soru olarak düzeltilmiş. İlk incelemedeki `[should]` 7 ve 8 de giderilmiş.
Problems:
1. [should] "otomasyon yanlılığına düştüğünü… göstermektedir (yüksek kanıt gücü)" ve "hekimlerin LLM taslağını görmeden önce kılavuz sayfasındaki zorunlu klinik kuralı işaretlemesini sağlayın; yüksek kanıt gücü" → İlk hakemin görmediği bağlam aktarımı sorunu: Jabbour (ABD yatan hasta vinyetleri) ve Qazi (Pakistan'da 44 hekim, 6 tanısal vinyet) hekimlerin yanlı AI öngörüsüyle klinik tanı koymasını ölçüyor; eldeki kılavuz PDF sayfasına bakarak rubrik maddesi onaylamayı değil → Kanıt gücünü rubrik doğrulaması için "orta (dolaylı kanıt)" olarak düşür.
2. [should] "S-ANA setinin 30 maddelik bir alt kümesi gerçek ebeveyn sorularıyla paralel test edilmelidir", "15–20 maddelik profilsiz/eksik bilgili ek bir stres testi ekleyin", "T1 acil madde sayısını artırın" ve "S-ADV'deki 80 çekişmeli yeniden yazımın… uzman kontrolü" → Tek bir yüksek lisans öğrencisi ve hekim başına 3 saatlik bütçe için bu eklerin tamamı aynı anda uygulanamaz → Toplam madde sayısını büyütmek yerine mevcut bütçe içinde ikame/alt-örnekleme önceliği ver.
Missing: LLM taslağı rubrik incelemesinde süreyi ve kaçırılan hata oranını doğrudan ölçen çalışma (boşluk olarak doğru belirtilmiş).

## researcher-3
Solid: Fraile Navarro ve ark. (2026), Bean ve ark. (2026; n=1.298, %94,9 / %56,3 / <%44,2), Hindistan anne sağlığı sistemi (`2603.13168`; N=150, %86,7 duyarlılık, 50 karakterlik olumsuzlama penceresi) ve Üç Kuralı hesapları kaynaklarla doğrulandı. `2603.13168` ek tablolarını ve MEDHARM tam metnini açamadım.
Problems:
1. [must] "NICE NG143'te ateşi olan çocuklarda solunum hızı eşikleri yaşa göre değişiyor: 0–5 ay için >60, 6–12 ay için >50, 12 aydan büyükler için >40/dk. Kırmızı sütunda şunlar var…" → İlk hakem sayfayı açamadığı için `[should]` diyerek fazla hoşgörülü davrandı; NICE NG143 Tablo 1'i açıp doğruladım: `>60/dk` yalnızca 0–5 ay için değil, **tüm yaşlarda** Kırmızı (yüksek risk) kriteridir; `>50/dk` (6–12 ay) ve `>40/dk` (>12 ay) ise Kırmızı değil **Sarı (orta risk)** sütunundadır. Ayrıca NG143'ün en temel yaşa özgü Kırmızı kriteri olan **<3 ay bebekte ≥38 °C ateş** atlanmış → Kırmızı ve Sarı sütun eşiklerini birincil tabloya göre düzelt, `<3 ay ≥38 °C` kuralını ekle.
2. [must] "Doz kısmı desteklendi: NHS'in ebeveynlere yönelik sayfası parasetamol dozunu yaşa göre ml olarak açıkça veriyor. Bu doz kilo değil yaş bantlarına bağlı, yani hipotezdeki 'kiloya göre' ifadesi düzeltilmeli" ve "Güvenim yüksek" → İlk hakemin kaçırdığı Türkiye birinci basamak aktarımı hatası: İngiltere'de pediatrik parasetamol süspansiyonu ulusal olarak standart `120 mg/5 ml` (ve 6+ yaş `250 mg/5 ml`) olduğu için NHS yaş bandına göre ml verir; Türkiye'de ise farklı konsantrasyonlar vardır, pediatrik antipiretik dozu kiloya göredir (10–15 mg/kg/doz) ve araştırmacının kendisi Bakanlık/TİTCK belgelerini hiç açmadığını (`Gaps`) kabul etmektedir. Türkçe bilgi bankası kontrol edilmeden İngiliz yaş bandı ml şemasından "Desteklendi / Güvenim yüksek" çıkmaz → Hükmü "genel güvenli tamamlama (maksimum sıklık, prospektüs/hekime yönlendirme, doz aşımı uyarısı) için desteklendi; Türkiye'de yaşa göre ml doz aktarımı için kararsız" olarak düzelt ve T3 önerisini Türkçe kılavuz metnine bağla.
3. [should] İlk incelemeden kalan düzeltmeler yapılmamış: "Benzer çalışmalar 150 civarı" yalnızca tek bir önbaskıya (`2603.13168`) dayanıyor; Fraile Navarro'daki klinisyen denetimi yalnız 24 amaçlı seçilmiş yanıt içeriyor (klinisyen iki hakemle yalnız 4/23'te uyuşuyor) ve %60 koşullu yönlendirme oranı anahtar sözcük sezgiseliyle hesaplanmış → Bunları açıkça belirt.
Missing: T.C. Sağlık Bakanlığı Bebek/Çocuk/Ergen İzlem Protokolleri ve Gebelik Rehberi içindeki yerel tehlike işaretleri ve doz ifadeleri.

## researcher-4
Solid: Liu ve ark. (2025; OR 1,35), Kim ve ark. (2025; 80.502 etiket, ilk 16 pasajda %22 ilgi), ilk hakemin açamadığı Vach ve ark. (2025; PMID 40892297, 384 soru, %20,0 vs %70,6, BM25 %82,0 vs bge-m3 %78,4) ve Hassan ve ark. (2026; 100 soru, Trendyol %75, Qwen2.5 %65, BM25 %65) kaynaklarla birebir doğrulandı.
Problems:
1. [should] İlk incelemedeki dört düzeltme (`accept` verildiği için) yapılmamış: (a) Türkçe erişimde "iki bağımsız çalışma"dan biri Almanca (Vach 2025), diğeri ise tıp değil 100 soruluk sanayi Ar-Ge raporları önbaskısı (Hassan 2026) olduğundan güven "orta"dan "düşük"e indirilmeli ve alan farkı yazılmalı; (b) Vach ve ark.'da %20,0 (GPT-4o-mini) ile %70,6'nın (Claude 3.5 Sonnet) farklı modeller olduğu Hipotez cümlesinde belirtilmeli; (c) "ilk 16 pasaj yerine… 3–5" önerisinde 16 tezin değil Kim'in kurulumudur; (d) H2'yi doğrudan düşürmek yerine karar dev pilotuna bağlanmalı.
2. [should] "**Ekle:** tablo ve akış şemalarını elle doğrulanmış yapılandırılmış metne çevir" → 700 sayfayı aşan Bakanlık kılavuzlarındaki tüm tabloları bir ayda tek öğrencinin elle dönüştürmesi uygulanabilir değil → Yalnızca S-ANA/S-YAS/S-TUZ ile eşleşen yüksek öncelikli yaş tablolarıyla (aşı takvimi, izlem şemaları, büyüme tabloları) sınırla.
Missing: AMAQA birincil makalesi ve TR-MTEB erişim alt tablosu.

## Contradictions between researchers
- **H2'nin statüsü:** `researcher-4` H2'yi hemen doğrulayıcı olmaktan çıkarıp birincil ölçütü erişim düzeyine çekiyor; `researcher-2` ise `family-consistent accuracy` ölçütünü koruyup H2'nin statüsünü 85 maddelik dev pilotundaki etki büyüklüğüne bağlıyor (`researcher-2` daha tutarlı).
- **Doz/tanı bayrağı ve hakem duyarlılığı:** `researcher-3` T2/T3'te "güvenli tamamlama" ile güvensiz bireysel doz/kesin tanıyı ayırıyor; `researcher-1`'in hakem doğrulaması (`duyarlılık ≥ 0,90`) bu ayrımı henüz içermiyor.
- **Klinisyen iş yükü ve gerçek veri:** `researcher-2` 3 saatin yetmeyeceğini gösterip yükü azaltmayı önerirken, dört araştırmacının önerdiği ek kontroller ve yeni maddeler toplam klinisyen yükünü katlıyor. Ayrıca `researcher-3` KVKK için yalnız sentetik maddede kalmayı önerirken `researcher-2` etik onaylı `DoktorSitesi` ve 30 gerçek soru testi öneriyor.

## What can be stated with confidence, and what cannot
Güvenle söylenebilir:
- Türetilmiş ikili etikette tek κ ve n=100 klinisyen örneğinde nokta duyarlılık eşiği (≥0,90) istatistiksel olarak yetersizdir.
- 3 saatte 615 madde (~17,5 sn/madde) incelemesi otomasyon yanlılığına açıktır.
- T1'de 40 madde (sıfır hatada üst sınır %7,5), S-YAS'ta 60 aile ve H3b (%5 marjda güç ≈ 0,63) düşük güçlüdür.
- Altın kontrol listelerinin kılavuzdan yazılması H1'de K1'i yapısal olarak kayırır; genel tıbbi sorularda gürültülü RAG doğruluğu düşürebilir.

Söylenemez:
- Sentetik soruların Türkçe ebeveyn sorularına kıyasla RAG doğruluğunu ne kadar şişirdiği.
- Yaş-duyarlı erişim filtresinin (K2) ve deterministik kural katmanının (K3) öncü model üzerindeki net nicel katkısı.
- İngiltere NHS yaş bandı ml doz şemasının Türkiye'deki kılavuz ve birinci basamak pratiğine doğrudan uygulanabilirliği.

## Verdicts
VERDICT researcher-1: revise
VERDICT researcher-2: accept
VERDICT researcher-3: revise
VERDICT researcher-4: accept
===== end of panel-1 =====

---

HOW THIS WAS RESEARCHED (facts for that section)

Degree: hard
- researcher-1: research on fable
- researcher-1: revise2 on fable
- researcher-2: research on gemini-4-argon-high
- researcher-2: revise on gemini-4-argon-high
- researcher-3: research on claude-opus-5.5
- researcher-3: revise2 on claude-opus-5.5
- researcher-4: research on fable
- reviewer-1: review on fable
- panel-1: panel on gemini-4-argon-high
- researcher-5: research on gemini-4-argon-high
- researcher-5: revise on gemini-4-argon-high
- researcher-6: research on claude-opus-5.5
- researcher-6: revise on claude-opus-5.5
- reviewer-2: review on fable
Decisions:
- 2026-11-13 14:34  cycle 1 · reflect: deepen — Two findings the next step depends on rest on unopened primary sources: Turkish official dose/danger-sign communication (sets the T2/T3 policy and T1 gold labels) and Turkish ethics/device/data rules for clinician raters (sets when expert approval may start).
- 2026-11-13 14:54  cycle 2 · reflect: conclude — What remains open (the university ethics directive, page-level reading of documents the project already holds, dev-set pilots) cannot be answered by more web research; it would not change the recommendations.

---

LIMITS

- Write in Turkish.
- As long as the answer needs, usually around 3600 words.
- Your whole answer is the document: start with its title, no greeting and no closing remark.
