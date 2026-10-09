# Summary (2026-10-09)

Bibliometric estimate of public cryptanalytic effort against the assumptions
behind standardized public-key encryption (ECDLP, structured and plain lattices,
syndrome decoding; factoring/FF-DLP, isogenies, multivariate as comparators).
Methodology: PLAN.md. Handoff and exact state: STATUS.md. Nothing here has been
human-validated except where noted; treat numbers as provisional.

## What exists

- [Working LaTeX white paper](paper/whitepaper.tex), with generated tables, a
  bibliography, and a compiled PDF; see [build and review notes](paper/README.md).
  It combines the literature results, nominal person-hours, and assumed
  human-year equivalents of recent OpenAI/Anthropic research budgets.

- Literature corpus: full IACR ePrint (27k records), DBLP (8.7M records),
  OpenAlex (phrase search, DOI enrichment, one citation-snowball round), zbMATH.
  arXiv was blocked and is covered only through OpenAlex.
- Classification: ~16.5k candidates labeled by a two-pass subagent classifier
  against pipeline/rubric.md (v0.3.4); agreement between passes kappa
  0.84-0.89, estimated false-negative rate 0.5-1.1%. 4,349 included items in
  data/export/combined_included.csv. Classification cost 13.6M subagent tokens
  (data/phase1/token_ledger.tsv).
- Recall: ~96-100% per class against the reference lists of 12 seed papers
  (analysis/recall_benchmark.md).
- Computational records: 338 record files (records/), 10 verified by the user;
  normalized frontier and compute totals (analysis/records_normalized.md,
  method and rationale in analysis/normalization_method.md).

## Findings (provisional)

Visible effort, combined sources, fractional paper counts (analysis/phase1_report.md §2):

| Class | Papers | pre-2006 | 2006-2016 | 2017-2026 |
|---|---|---|---|---|
| ECDLP | 465 | 97 | 198 | 170 |
| All lattices | 840 | 55 | 225 | 560 |
| Syndrome decoding | 290 | 25 | 80 | 185 |
| Factoring / FF-DLP | 849 | 213 | 343 | 294 |

- Lattices have received roughly 1.3-2.6x the cumulative visible effort of
  ECDLP (low end: distinct authors; high end: vetted-venue paper counts), all of
  it since 2016 (3.3-4.9x in 2017-2026); ECDLP led before 2006.
- Syndrome decoding has received roughly 0.6-0.8x the cumulative effort of
  ECDLP, but has exceeded it since 2017 (1.1-1.7x).
- The ePrint-only pilot overstated both post-quantum leads; older ECDLP and
  factoring work lives in DBLP/zbMATH, not ePrint.

Frontier gaps (how much more work than the largest public solve, in bits; see
analysis/normalization_method.md §6 for how to read this):

| Target | Gap |
|---|---|
| P-256 (vs. 117-bit generic ECDLP solve, 2016) | 69 bits |
| ML-KEM-512 / 768 (vs. SVP-challenge sieving dim 171, 2026) | 60-75 / 121-152 bits per sieve call |
| mceliece348864 (vs. Goppa n=1409, 2023) | ~79 bits |
| HQC-128 (vs. QC n=4098, 2026) | ~61 bits (approximate) |
| RSA-2048 (vs. RSA-896, 2026) | ~35 bits (leading GNFS heuristic; ~35 billion x) |

These are model-based work ratios, not equally calibrated practical distances.
RSA's figure is 116.88 - 81.86 = 35.02 in the leading GNFS model; NIST's 112-bit
security category is a separate convention. Memory, parallelism and omitted
terms can change the practical ratios. Bitcoin-puzzle compute (interval ECDLP,
non-academic) is reported separately and exceeds all academic ECDLP record compute.

## Set aside

- A 2026 arXiv series claiming a polynomial-time quantum attack on ML-KEM
  ("Module Lattice Security", Luo) is excluded from all counts by user decision
  and listed for separate review in notes/mlkem_polytime_claims.md.

## Other tracks in this repository

Built in parallel sessions; see their own documents:
- Author map and research-FTE model: analysis/author_map.md,
  analysis/author_map_method.md, data/authors/.
- AI-equivalent budget scenarios (adopted 2026-10-09):
  [method and class budgets](analysis/ai_effort_comparison_scoping.md).
  Assume 1x/10x/100x economic productivity at $250k per research-year:
  equivalent inference budgets are $250k/$25k/$2.5k per human research-year.
  These are sensitivity scenarios, not measured exchange rates or attack-cost
  predictions. At 10x, the current author-map research-FTE estimates map to
  about $25.9M for all lattices, $14.8M for ECDLP, and $8.3M for syndrome decoding.
  HAWK-normalized historical effort is a separate worked example; rediscovery
  is deferred. Supporting evidence: analysis/ai_effort_calibration_report.md,
  analysis/ai_effort_hawk_case.md, data/ai_effort/.

## Open items

- Human spot-checks of classifier labels (analysis/review_sheet.md for Phase 0;
  a Phase 1 sheet is still to be generated) and of the unverified records.
- Optional: second snowball round; targeted pass over the productive tier-B
  signatures; dedicated thesis harvest (HAL/theses.fr/DART-Europe) for the
  thesis effort proxy; retry arXiv.
- Effort-estimation phase (PLAN §8: person-year priors, funding proxy, scenario
  multipliers for classified effort).
