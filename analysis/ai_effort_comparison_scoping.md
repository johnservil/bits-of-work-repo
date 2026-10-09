# Comparing human cryptanalytic effort with AI inference budgets

Adopted method, v0.2, 2026-10-09. The user chose an approximate scenario
comparison rather than further rediscovery experiments. This supersedes the
v0.1 proposal to estimate an empirical exchange rate from matched results.
The existing literature estimates and AI disclosures remain supporting evidence
in [the calibration report](ai_effort_calibration_report.md).

## 1. Claim and scope

> We do not estimate an empirical exchange rate between human and AI research.
> We express historical cryptanalytic effort as equivalent inference budgets
> under stated productivity assumptions. These figures describe budget scale;
> they do not predict discovery of an attack.

The comparison is conditional on AI access to the existing literature. It does
not measure how much AI scrutiny has actually occurred, establish that an AI
could reproduce the community's work, or quantify confidence in a cryptosystem.
Accumulated scrutiny includes negative and incremental work as well as advances.
Transferring productivity on individual successes to that mixture is an explicit
assumption, not a result of the HAWK case.

## 2. Adopted productivity scenarios

Let H_X be estimated human research-years for class X, c = $250,000 per
research-year, and s the assumed economic productivity multiplier for the
inference-budget comparison. Assume comparable research effort can be supplied
at s times the human productivity per dollar, given the existing literature.

    D_X(s) = c * H_X / s

| Assumed multiplier s | Inference-budget equivalent per human research-year |
|---|---:|
| 1x | $250,000 |
| 10x | $25,000 |
| 100x | $2,500 |

These are sensitivity scenarios, not confidence bounds or empirically estimated
percentiles. None is the preferred point estimate; multipliers outside this
range remain possible. The same s across classes is an additional simplifying
assumption. Class rankings are therefore inherited from H_X, not evidence about
relative AI capability. Class-specific multipliers may be varied separately.

D_X is an inference-budget equivalent. It excludes separately billed tool
compute, human supervision and verification, and model training. It is not a
measured all-in cost of AI-assisted research. An all-in comparison would add
those costs explicitly and would need its own productivity assumption. Historical
human research compute also remains separate, as in PLAN section 8.

## 3. Human inputs and current class budgets

For class-wide scenarios use the research-FTE cumulative columns in the 2026 row
of [data/authors/fte_by_year.csv](../data/authors/fte_by_year.csv), as present on
2026-10-09. Method: [author_map_method.md](author_map_method.md). These combine
publication-output shares with per-paper priors for unresolved people. They are
proxies, not observed hours, and 2026 is a partial year. The $250k convention is
applied per research-FTE-year here, not per career-adjusted calendar person-year.

| Class | Research-FTE-years H_X | 1x budget | 10x budget | 100x budget |
|---|---:|---:|---:|---:|
| ECDLP | 593.8 | $148.45M | $14.85M | $1.48M |
| All lattices | 1,036.4 | $259.10M | $25.91M | $2.59M |
| MLWE / structured lattices | 583.6 | $145.90M | $14.59M | $1.46M |
| Plain LWE | 452.8 | $113.20M | $11.32M | $1.13M |
| Syndrome decoding | 331.4 | $82.85M | $8.29M | $0.83M |
| Factoring / FF-DLP | 1,111.1 | $277.78M | $27.78M | $2.78M |
| Isogenies | 116.6 | $29.15M | $2.92M | $0.29M |
| Multivariate | 210.2 | $52.55M | $5.26M | $0.53M |

The decimal places make the arithmetic traceable; they do not express precision
in the effort estimates. MLWE and plain LWE are components of all lattices:
do not add them again to that total. Budgets describe public effort at the
assumption-class level, not exclusively scrutiny of deployed parameter sets.
Classified-effort scenarios remain a separate axis.

Recompute this table from the named CSV row and D_X whenever the author map
changes. Keep human-effort uncertainty separate from the choice of s: if H_X
changes by a factor k, every budget changes by k. The paper-based HAWK estimate
below uses a different estimator and must not silently replace these inputs.

## 4. HAWK-normalized historical effort: a worked example

The [HAWK case](ai_effort_hawk_case.md) estimates 35.4 PY of historical literature
effort (yes-only), or 38.4 PY including borderline work. Anthropic reports about
$100,000 for its HAWK discovery process. Define, as a separate normalization:

    D_X_HAWK = $100,000 * H_X_papers / H_HAWK_papers

The implied rate is about $2,825 per PY (35.4-PY denominator), or $2,604 per PY
(38.4-PY denominator). For example, a hypothetical 100 PY of literature effort
computed on the same basis maps to about $282,000 or $260,000 respectively.
This is approximately the scale of the 100x scenario, not evidence for that
scenario's probability.

The transfer assumption is that the ratio of accumulated human literature
effort to AI breakthrough cost is comparable across problems. The expenditures
buy different outputs: prior human work supplies knowledge used by the AI.
Call this quantity **HAWK-normalized historical effort**, not measured labor
replacement or predicted attack cost.

Use the same paper categories, weights, inclusion rule and effort priors in
both H_X_papers and H_HAWK_papers. A shared multiplicative papers-to-years factor
then cancels; differences in category mix, coverage and attribution do not.
Do not divide the author-map research-FTE totals in section 3 by the paper-based
HAWK denominator without explicitly introducing a cross-estimator assumption.

The previously proposed human breakthrough effort of 0.3-1 PY was hypothetical,
not measured. At $250k/PY, $100k corresponds to 0.4 PY before other costs; this is
a break-even threshold, not a finding of human/AI cost parity. The marginal and
cumulative comparisons have different accounting boundaries and do not bound a
common statistical parameter.

## 5. Reference-price token equivalents

Keep disclosed tokens and costs in their original units. To translate a scenario
budget into tokens, fix a reference model/version, a dated price schedule, and
fractions f_in, f_cache, f_out summing to one. With prices per million tokens:

    p_mix = f_in * p_in + f_cache * p_cache + f_out * p_out
    T_reference = 1,000,000 * D_X / p_mix

T_reference counts total input (uncached and cached) plus output tokens under
that reference mix. Include billed reasoning tokens in output where the pricing
schedule does so. Account separately for additional billing categories if used.
An output-only equivalent can instead set f_out = 1, but must be labeled as such
and must not be compared with total-token counts without conversion.

For arithmetic illustration only, a hypothetical p_mix = $10 per million tokens
would make the 1x / 10x / 100x budgets per human research-year equivalent to
25 billion / 2.5 billion / 250 million reference tokens. This is not a quoted
model price or an estimate of actual token consumption. No real reference model
or price mix has been selected; dollar scenarios are the primary output.
HAWK's dollar disclosure does not identify its token count. Elapsed research
hours also do not determine tokens or aggregate agent-hours.

## 6. Evidence and optional future work

Existing evidence is retained in [ai_effort_calibration_report.md](ai_effort_calibration_report.md),
[ai_effort_hawk_case.md](ai_effort_hawk_case.md), and
[data/ai_effort/ai_results.yaml](../data/ai_effort/ai_results.yaml).
The numerical ratios between literature estimates and disclosed successful
results are descriptive; incomplete failure accounting and unequal starting
knowledge prevent treating them as empirical productivity estimates.

The [rediscovery pilot](pilot_hawk_protocol.md) is deferred. Its six interrupted
attempts produced no completed mathematical evaluations. No further experiments,
classification runs, author outreach, or paid collection are required for this
scenario comparison. Human effort interviews and well-controlled experiments
could inform a later study, but would still leave cross-task transfer uncertain.

The useful next checks are consistency of effort definitions, sensitivity to
human-effort priors and s, and whether any substantive conclusion survives these
assumptions. A ratio of a disclosed AI budget to D_X is a conditional budget
comparison, not the fraction of historical scrutiny that AI has reproduced.
