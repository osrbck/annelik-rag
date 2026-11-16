# Survey (orchestrator's map, not research)

Seven searches on 2026-11-13. Nothing here goes into the final document unless a researcher
finds and cites it.

## Where the field starts

- LLM-as-judge bias: "Self-Preference Bias in LLM-as-a-Judge" (arXiv 2410.21819); a counter-line
  arguing self-preference largely reflects real quality or evaluator uncertainty ("Do LLM
  Evaluators Prefer Themselves for a Reason?", a Findings of EMNLP 2026 paper).
- Rubric-based health evaluation: HealthBench (arXiv 2505.08775): physician-written per-item
  rubric criteria, model grader validated against physicians (macro F1 on consensus criteria).
- Medical RAG: MIRAGE / MedRAG (arXiv 2402.13178); a late-2025 expert evaluation
  "Rethinking Retrieval-Augmented Generation for Medicine" (arXiv 2511.06738) that questions RAG's benefit.
- Synthetic benchmarks: "Can we Evaluate RAGs with Synthetic Data?" (arXiv 2508.11758):
  synthetic sets rank retriever variants well, generator variants poorly.
- Triage safety: a Nature Medicine study of a consumer health assistant (51.6% emergency
  under-triage), follow-ups arguing the result depends on evaluation format; AcuityBench, CARE-BENCH.
- Domain neighbours: DIAN pregnancy RAG chatbot (Frontiers in AI 2025); a maternal-health RAG chatbot
  for India (arXiv 2603.13168) with synthetic data + LLM judge + experts.
- Turkish: TR-MTEB (Findings of EMNLP 2025) for embeddings; Pubmed-RAG-TR; TurkishMedLLM preprint.

## Competing answers

- Same-family judge: harmful bias vs. artefact of quality/uncertainty; unclear for checklist
  grading against a reference (most studies are pairwise or free scoring).
- RAG in medicine: clear gains (MedRAG) vs. little or negative gain for strong models (2025 expert study).
- Triage failures: model limitation vs. artefact of forced-choice evaluation format.

## Gaps seen

- No guideline-grounded evaluation found for parents' paediatric questions; nothing in Turkish for
  maternal/child health.
- Little on over-refusal as a measured cost of safety layers in health assistants.
- Little on realism of LLM-written lay questions versus real caregivers' questions.
- Deterministic (rule-based) safety layers on top of LLMs: evidence not seen in the survey.

## Terms

"Under-triage / over-triage" (field) = missed emergency / needless escalation (project's
"kaçırılan acil", "aşırı ret" partly overlaps over-triage but also covers refusals).
"Rubric criteria" (HealthBench) = the project's "zorunlu/yasak öğeler" (required/forbidden items).
"Contrast sets" = the project's S-YAS "families".
