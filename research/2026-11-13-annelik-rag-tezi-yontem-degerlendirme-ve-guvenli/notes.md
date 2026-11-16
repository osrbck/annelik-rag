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
