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

## researcher-1
Persona: A leading measurement scientist of NLP evaluation, known for work on the validity and reliability of automatic and LLM-based graders and for insisting that a metric is validated against human judgement before it carries a claim.
Angle: Whether the scoring and inference chain is sound: checklist-based LLM judging by a same-family stronger model, the validation design (who labels, how many, which agreement statistics and thresholds), the rule "all required items present" as the correctness criterion, three repeats with majority/worst-case aggregation without temperature control, and the statistics (exact McNemar, Holm, a 5-point non-inferiority margin, bootstrap, the power figures). Include the reporting standards a thesis of this kind is expected to follow.
Not yours: how the questions and gold answers are produced (researcher-2); triage, red flags and guardrails (researcher-3); whether RAG helps and retrieval technology (researcher-4).
Sources: ACL Anthology and arXiv on LLM-as-judge bias and meta-evaluation (self-preference, family bias, rubric or reference-guided grading); HealthBench and its meta-evaluation; reporting guidelines for LLM studies in health (TRIPOD-LLM, CHART, MI-CLEAR-LLM and similar on EQUATOR); statistics literature on agreement (kappa paradoxes, Gwet AC1, Krippendorff alpha, sample size for kappa), paired binary tests and non-inferiority margins; vendor documentation on determinism.
Hypothesis: Same-family bias is measurable in pairwise and free-scoring settings but small in reference-guided checklist grading, so it does not threaten the K0–K3 paired comparisons, while it does threaten K4 vs K3; refuted if studies show family bias persists under rubric grading or interacts with answer style (e.g. citation-bearing RAG answers) in a way that differs between configurations. Second: a single κ ≥ 0.70 on a binary derived label is a weaker validation than item-level agreement with prevalence-robust statistics; refuted if the literature treats binary κ at this sample size as standard and sufficient.
Questions:
- What is the measured size of same-family or self-preference bias when the judge grades against explicit rubric items or a reference, as opposed to pairwise preference, and does it differ by answer style?
- How do the strongest health benchmarks validate a model grader (unit of agreement, statistic, sample size, who the humans are), and how does this design compare?
- Is a single non-clinician rater (the researcher) an accepted reference for judge validation, and what do reporting standards require about raters and blinding?
- Is "all required items present and no critical error" a defensible primary correctness criterion compared with partial-credit rubric scores, and what does each choice do to power and to ceiling/floor effects?
- With no temperature or seed control, are three repeats with majority and worst-case aggregation adequate, and how should run-to-run variance be reported?
- Are exact McNemar with Holm, a 5-point non-inferiority margin on over-refusal and percentile bootstrap intervals appropriate here, and what do standards say a non-inferiority margin must be justified by?

## researcher-2
Persona: A leading scholar of benchmark and test construction for language technology in health, known for showing how the way items are written determines what a benchmark can and cannot claim.
Angle: Whether the test sets can carry the thesis's claims: stems written by a single LLM rather than drawn from real mothers; gold checklists drafted by an LLM from guideline PDFs and then approved by clinicians in a short review; "question first, then look for the answer in the guideline" versus generating questions from passages; contrast pairs and adversarial rewrites as constructs; item counts, dev/test separation and contamination. Include how comparable published systems for pregnancy, infant and child health built and validated their evaluation sets, and what real-question sources exist in Turkish or could be used to check realism.
Not yours: how answers are graded and the statistics (researcher-1); the clinical content of red flags and the safety layer (researcher-3); whether RAG improves accuracy and retrieval technology (researcher-4).
Sources: arXiv and ACL Anthology on synthetic evaluation data and its validity for RAG; contrast sets and adversarial/perturbation test literature; consumer health question corpora (e.g. real-user question datasets, health-line and forum corpora) and Turkish equivalents; JMIR, npj Digital Medicine, Frontiers, BMJ-family papers on maternal, breastfeeding and paediatric chatbots; psychometrics and annotation literature on expert review of machine-drafted reference answers (automation or anchoring bias).
Hypothesis: LLM-written lay questions are cleaner, more answerable and more uniform than real caregivers' questions, which inflates accuracy for every configuration and can distort generator comparisons; and clinicians who approve machine-drafted gold items at under a minute per item anchor on the draft and miss errors. Refuted if studies show LLM-written consumer health questions match real ones on the properties that drive system performance, or that expert review of drafted references reaches the same quality as expert authoring.
Questions:
- What is known about how synthetic or LLM-written evaluation questions differ from real users' questions, and about which comparisons (retriever vs generator) stay valid on synthetic sets?
- Which sources of real Turkish (or translatable) mothers' and parents' questions exist and could be used, within ethics, to seed items or to run a realism check?
- What do studies say about expert validation of LLM-drafted reference answers or rubrics (error rates missed, anchoring, time needed per item), and what review designs reduce the risk?
- How did published maternal and child health assistants construct their test questions and references, with what sample sizes and expert involvement?
- Are contrast pairs with an all-members-correct criterion, and adversarial rewrites inheriting the parent's label, used and validated elsewhere, and what pitfalls are reported?
- Does a single-turn, profile-prefixed format hide failures that multi-turn or missing-information formats reveal, and how do others report this limit?

## researcher-3
Persona: A leading clinical safety researcher of digital triage and consumer health AI, with a paediatric and maternal emergency background, known for measuring under-triage in symptom checkers and for strictness about what a safety claim needs.
Angle: Whether the safety design and its measurement hold: a "no diagnosis, no dose, emergency referral first" policy; red-flag lists by age and pregnancy period and which authoritative sources they should come from; a deterministic rule-based layer around an LLM versus model-based or hybrid guardrails; how under-triage, over-triage and over-refusal are measured in the field; whether 40 emergency items and worst-of-three aggregation support any safety statement; the legal and ethical frame in Türkiye and the EU for a research prototype giving health information (medical-device software qualification, data protection, ethics review for expert raters).
Not yours: judge validity and statistics in general (researcher-1); how ordinary questions and gold answers are built (researcher-2); retrieval accuracy and whether RAG helps (researcher-4).
Sources: Nature Medicine, BMJ, JAMA-network, Lancet Digital Health and npj Digital Medicine on LLM and symptom-checker triage; triage benchmarks (acuity and red-flag recognition); WHO IMCI and danger-sign material, NICE traffic-light and antenatal/postnatal red-flag guidance, Turkish Ministry of Health protocols; guardrail literature and vendor documentation; MDCG guidance on software as a medical device, the Turkish medical device regulation, KVKK, and research-ethics rules for studies with professionals as raters.
Hypothesis: Current frontier models already refer most explicit emergencies, so a keyword/rule layer adds little on clearly worded items and mainly raises over-triage, while its real value (and the benchmark's blind spot) lies in atypically worded and multi-symptom presentations; and a dose-refusal policy is stricter than what guideline-based parent information gives (e.g. weight-based antipyretic dosing), so it may count helpful answers as unsafe. Refuted if evidence shows rule layers materially cut under-triage for strong models without raising over-triage, or that authoritative lay-facing sources withhold dosing.
Questions:
- What under-triage and over-triage rates are reported for current LLM assistants on maternal, neonatal and paediatric presentations, and how much do they depend on evaluation format?
- Which authoritative, age-stratified red-flag sources should a list for pregnancy, newborn, infant, child and adolescent be built from, and what do they include that generic lists miss?
- What evidence exists for deterministic guardrails versus model-based safety classifiers in health assistants (benefit, failure modes, over-blocking)?
- Is "never give a dose, never name a diagnosis" consistent with how national and international parent-facing guidance communicates, and how do evaluations treat safe partial answers?
- What can and cannot be claimed about emergency safety from 40 items with zero or few failures, and what sample sizes or designs do safety evaluations use?
- What do Turkish and EU rules require of a thesis prototype of this kind (device qualification, disclaimers, data protection, ethics approval when clinicians only rate texts)?

## researcher-4
Persona: A leading information-retrieval researcher who specialises in retrieval-augmented generation for morphologically rich, lower-resource languages, known for careful negative results; here cast as the advocate of the strongest case against the thesis's expected outcomes.
Angle: The strongest evidence-based case that the planned comparisons will not show what is expected, and what technical choices decide it: whether RAG still improves answer accuracy for current frontier models in medicine or mostly adds noise; ceiling effects when the bare model already knows guideline content, and how national-guideline-specific or recently changed facts alter that; whether metadata (age) filtering beats simply giving the age to the model; retrieval quality in Turkish (embedding and re-ranking models, hybrid lexical search, tokenisation and morphology); extracting and chunking long guideline PDFs with tables and flowcharts; and which local open models answer health questions in Turkish acceptably when quantised.
Not yours: how answers are graded (researcher-1); how questions and gold answers are produced (researcher-2); triage and safety layers (researcher-3).
Sources: arXiv, ACL Anthology, SIGIR/ECIR and medical informatics journals on medical RAG (benefit and harm studies, expert evaluations), retrieval robustness and context noise; TR-MTEB, MTEB/MMTEB leaderboards and papers for Turkish retrieval; Turkish RAG and Turkish medical QA datasets; document-parsing and chunking studies for guidelines; metadata-filtered and self-query retrieval studies; evaluations of open-weight and quantised models in Turkish.
Hypothesis: On ordinary guideline questions a 2026 frontier small model is already near ceiling, so K1 − K0 will be well under the 15 points the design can detect, except on Türkiye-specific and recently changed facts; and since every configuration is told the age, age-filtered retrieval adds only a few points over plain RAG, far below the 25 points detectable on 60 families. Refuted if recent studies show double-digit accuracy gains from RAG for frontier models on guideline-specific questions in non-English settings, or large gains from metadata-filtered retrieval over plain dense retrieval on age- or population-conditioned questions.
Questions:
- What do 2024–2026 studies report for RAG versus no-RAG accuracy with strong models in medicine, where does RAG hurt, and what explains the differences (question type, corpus, retrieval quality)?
- How large are effects for local-guideline-specific or recently updated facts, and is there evidence from non-English or national-guideline settings?
- What is the evidence for metadata or population filtering in retrieval versus leaving conditioning to the generator, and how are such gains measured?
- Which embedding, re-ranking and hybrid setups perform best for Turkish retrieval on current benchmarks, and what Turkish-specific pitfalls are documented?
- What is recommended for parsing and chunking long clinical guideline PDFs with tables, flowcharts and two-page spreads, and how much does this move answer accuracy?
- Which open-weight models, at which quantisation, are documented to handle Turkish health or general question answering well enough for a local configuration, and what quality drop is reported?

## reviewer-1
Persona: A professor who wrote the standard textbook on evaluation methodology for clinical AI and has examined theses in the field for decades; strict about claims that outrun their evidence, about preprints presented as settled, and about recommendations that do not follow from the cited source.

## panel-1
Persona: A professor of maternal and child health informatics who wrote the standard reference on validating digital health tools; strict about clinical safety claims, about whether a cited study's population and setting transfer to Turkish primary care, and about feasibility for a single master's student.

## writer-1
Persona: A professor who has supervised and examined applied theses in health informatics for decades; strict about telling the candidate exactly what to change, in order of importance, with the evidence and its strength beside each change, and about saying plainly what remains uncertain.
