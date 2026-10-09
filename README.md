# literature-search

Estimating public cryptanalytic effort across standardized public-key
encryption assumptions (ECDLP, module/ring LWE, plain LWE, syndrome decoding)
from the literature, with computational records as a hard-unit measure.

- [Working LaTeX white paper](paper/whitepaper.tex): results, person-hours, and AI research comparisons; [build instructions](paper/README.md).
- SUMMARY.md: current findings and state, in one page.
- PLAN.md: methodology.
- [AI-equivalent budget scenarios](analysis/ai_effort_comparison_scoping.md):
  assumed 1x/10x/100x productivity, class budgets, and HAWK normalization.
- STATUS.md: current state and resume commands.
- analysis/phase0_report.md: Phase 0 (ePrint pilot) results.
- pipeline/: harvesters (ePrint OAI-PMH, OpenAlex, zbMATH, DBLP), keyword
  screen, classification rubric and batching, merge scripts.
- data/: harvested metadata, candidates, labels, exports.

The public website is in `docs/`. Regenerate its figures with
`python3 -I pipeline/build_site_data.py`; `make -C paper` also refreshes the
PDF linked from the site. The site preserves publication-share estimates as
proxies and prominently flags possible overestimation of working time and
scope/attribution errors. The bounded scope review is recorded in
`analysis/scope_audit/bounded_review.json`; it does not reclassify the corpus.
