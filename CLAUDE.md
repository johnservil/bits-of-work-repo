# literature-search

Bibliometric study estimating public cryptanalytic effort per standardized
public-key encryption assumption class (ECDLP, MLWE/structured lattices,
plain LWE, syndrome decoding; factoring/FF-DLP, isogenies and multivariate as
comparators). Computational records get a dedicated track.

Read these first, in order:

1. STATUS.md: what is done, what is partial, exact resume commands.
2. PLAN.md: the full methodology (taxonomy, attribution model, sources,
   records track, effort-estimation proxies, confounders).
3. analysis/phase0_report.md: Phase 0 pilot results and rubric lessons.
4. pipeline/rubric.md: the classification rubric (v0.3) used by the
   two-pass subagent classifier.

Conventions: Python 3 stdlib only; run scripts with `python3 -I` from the
repo root; raw pulls go under data/raw/<source>/ and are never edited by
hand; classification runs via subagents (no API key assumed), two passes
(fast model over all candidates, stronger model over included/borderline plus
a 10% audit of exclusions); never run two OpenAlex harvesters concurrently.
