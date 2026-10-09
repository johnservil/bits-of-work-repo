# The HAWK case: a historical-effort normalization example

Updated v0.2, 2026-10-09. The adopted comparison uses assumed 1x/10x/100x
productivity multipliers; see [the method](ai_effort_comparison_scoping.md).
HAWK supplies a separately labeled worked example, not a measured exchange rate.
All AI-side figures and their sources are in
data/ai_effort/ai_results.yaml (entries added 2026-10-09). Human-side labels:
data/ai_effort/calib/hawk/labeled_final.jsonl (rubric
pipeline/rubric_calibration.md; two-pass, kappa 0.78 on include, 0/25
audited exclusions flipped). Estimate: data/ai_effort/calib/hawk/estimate.txt.

## The event

| date | result | who | effort disclosed |
|---|---|---|---|
| 2024 (DCC) | HAWK key recovery -> exact SVP in dim n+1 (Z-LIP block reduction) | Ducas (human) | none |
| 2025-05 | automorphism knowledge halves the LIP rank (no public automorphism found) | van Gent, Pulles (human) | none |
| 2026-07-17 | draft: SVP in dim 3n/4 via adjoint lattice reduction | GPT-5.6 + Codex, Luo's group | "minimal technical guidance"; no figures |
| 2026-07-28 | SVP in dim n/2+1 via the Galois involution; HAWK-256 key recovered end to end | Claude Mythos Preview, Anthropic (Straznickas, Weis) | ~60 h, ~$100k API, one non-expert researcher doing project management |
| 2026-07-29 | HAWK withdrawn from NIST round 3 (secondary reports) | HAWK team | |
| 2026-07-30 | ePrint 2026/1560: SVP in dim 3m/8+1 = 3n/4+1, trace-zero approach | Mureau, Pellet-Mary (human) | none |
| 2026-09-24 | ePrint 2026/2198: rank-4 extension; names the three origins | Luo, Jiang, Pan (human, "with the help of GPT" for parts) | none |

The publications describe three contemporaneous approaches, two AI-derived.
Publication dates do not establish discovery durations or independence:
[Anthropic's account](https://www.anthropic.com/research/discovering-cryptographic-weaknesses)
says it shared its attack with the HAWK team in June. The table records public
draft/disclosure dates, not the dates on which each group found its result.

## Human effort before the event (measurement 1)

Snowball from 27 pre-cutoff ePrint seeds (posted on or before 2026-06-30):
20 resolved in OpenAlex, 213 backward references, 250 forward citers, 7
seeds added from ePrint directly; 316 candidates after de-duplication.

| | items | weighted papers | person-years (median, 5-95%) | USD at $250k/PY |
|---|---|---|---|---|
| include = yes (A, C, F, H; G excluded) | 27 | 23.6 | 35.4 [33.2, 37.6] | $8.9M |
| plus borderline at half weight | 49 | 25.6 | 38.4 [36.2, 40.6] | $9.6M |

Five G items (reductions, e.g. HAWK -> nrdPIP) are reported but not counted,
per PLAN.md §8. The interval reflects only the per-paper priors (A/C/F/H
1-2 PY, uniform); it does not include coverage error (OpenAlex abstracts are
missing for 58% of items; forward citers capped at 400 per seed) or prior
misspecification. The previously suggested 20-80 PY ($5M-$20M) outer range is
an illustrative sensitivity range, not a measured uncertainty interval. Shared
uncertainty in effort per paper should move all paper estimates together;
independent per-paper sampling understates that source of uncertainty.

The estimate includes older general LIP work as well as HAWK-specific papers;
it is not a measurement of hours spent directly attacking HAWK since submission.

What the human figure includes: all public work on LIP/Z^n-LIP/module-LIP
attacks and HAWK key recovery, most of which did not produce the July 2026
result but established the tools it used (Ducas's block reduction, van
Gent-Pulles descent, the automorphism viewpoint). What it excludes: the HAWK
design team's own security analysis, side-channel work, the two 2026 solving
groups' own time, and any non-public effort.

## HAWK-normalized historical effort (assumed transfer)

Define one HAWK-equivalent historical-effort unit as 35.4 estimated PY
(yes-only), or 38.4 PY (with borderline), and assign it the reported ~$100k
AI discovery budget. This gives about $2,825 or $2,604 per historical PY:

    D_X_HAWK = $100,000 * H_X_papers / H_HAWK_papers

For a hypothetical 100 PY estimated on the same paper-based method, the
normalization yields about $282k or $260k. A shared multiplicative effort prior
cancels in the ratio, but coverage, attribution and category differences remain.
Use consistent inclusion rules on both sides; do not silently substitute
author-map research-FTE-years for H_X_papers.

This assumes the ratio of accumulated human literature effort to AI breakthrough
cost transfers across problems. It is approximately a 90-96x dollar ratio at
$250k/PY, similar in scale to the adopted 100x scenario. It does not validate
that multiplier: the AI used prior human work as input, so the two expenditures
purchased different outputs. It does not price reproduction of that literature
or an equivalent amount of scrutiny.

## Marginal comparison (human effort unknown)

Mureau-Pellet-Mary's actual effort is undisclosed. The earlier 0.3-1 PY range
was hypothetical; it does not establish near-parity in dollars or faster AI
discovery. At the study's cost convention, $100k equals 0.4 PY before supervision
and other costs. This is a break-even threshold only. The outputs also differ:
3n/4+1 for the human result versus n/2+1 for Anthropic's result.

Anthropic describes ~$100k as the full HAWK discovery process. The boundary of
included earlier failures is unknown; the disclosure should not be described as
pricing only one successful session. Active human hours and HAWK token counts
are not disclosed. AES session accounting does not establish HAWK's accounting.
The marginal and cumulative comparisons do not bound a common exchange rate.

## Measurement 3 (deferred): controlled rediscovery

The user chose the assumption-based comparison on 2026-10-09. No further
experiments are needed for it. The [protocol](pilot_hawk_protocol.md), packet,
and run log remain as historical artifacts: all six attempts were interrupted,
with no completed mathematical evaluations. A negative recall probe detected no
contamination but did not establish a clean training history.
