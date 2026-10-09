# Human and AI effort: scenarios and supporting evidence (v0.2, 2026-10-09)

Status updated 2026-10-09: the adopted comparison is now the
[1x/10x/100x productivity scenario method](ai_effort_comparison_scoping.md).
It uses D_X = $250,000 * H_X / s, with multipliers explicitly assumed rather
than fitted. That document contains the current class budgets, HAWK-normalized
worked example, and reference-price token conversion. Rediscovery is deferred.

This report retains the earlier literature estimates and AI-side disclosures
as supporting evidence, not an empirical calibration of productivity. Per-problem
table: analysis/calib_exchange_table.md (regenerate with
`python3 -I analysis/calib_exchange_table.py`). Sources:
data/ai_effort/ai_results.yaml and data/ai_effort/erdos_problems.csv.
Labels and estimates: data/ai_effort/calib/<problem>/.

## 1. What was measured

Human side, same method for every problem: seed papers (erdosproblems.com
references; curated UGC/2-to-1 lists; pre-cutoff ePrint papers for HAWK),
OpenAlex snowball (backward references, forward citers capped at 400 per
seed, forward citers dropped for seeds cited >200 times in the Erdős runs),
a haiku title screen, sonnet pass 1 and opus pass 2 under
pipeline/rubric_calibration.md, de-duplication of versions, and the PLAN.md §8
priors (A/C/F/H 1-2 PY per paper, D 0.5-1.5, E 2-10, S 0.5-1; G not counted;
borderline at half weight). Problems: HAWK key recovery, 2-to-1 Games, UGC,
and 22 Erdős problems (the 12 with an AI resolution in the Epoch
or AlphaProof Nexus sets, plus 10 unsolved ones sampled at random from the
Epoch benchmark).

AI side: disclosed figures only, with their price basis, from the Epoch
FrontierMath Erdős paper (per successful attempt; failed attempts unpriced
except through the 3% success rate and $300 cap), AlphaProof Nexus (TPU-hours
per run; sweep cost undisclosed), OpenAI's 2026-10-06 release (3 hours of
ChatGPT Pro thinking per accepted result, no per-family figure), and the
Anthropic HAWK post (about 60 hours, about $100k API).

## 2. Supporting case comparisons (not productivity estimates)

| problem class | human effort (PY, $ at $250k) | AI effort as disclosed | dollar ratio human : AI |
|---|---|---|---|
| Erdős problems resolved by GPT-6 Astra in the Epoch set (#1, #74, #126, #548, #571) | median 9.8 PY ($2.4M); range 3-22 PY | $160-$900 per successful attempt; Epoch's expected cost per resolution incl. failures about $10k | 10^3-10^4 per success; ~10^2-10^3 after failures |
| Erdős problems resolved by AlphaProof Nexus (#12, #26, #125, #138, #152, #741, #846) | median 2.9 PY; #138 (van der Waerden numbers) 64 PY | ~27.5 TPU-h (~$60) per run plus "a few hundred dollars" of LLM cost; the 353-problem sweep cost undisclosed | 10^3-10^5 per success |
| Erdős problems not resolved by any model (10 sampled) | median 2.0 PY, mean 4.2 | 5-10 failed attempts each, unpriced | n/a |
| Unique Games Conjecture (OpenAI family 102, claimed, unvetted) | 86 PY ($21M) of direct work on the conjecture, 2002-2026 (81 yes items; 729 of 824 pool items were UGC consumers or unrelated) | release-wide 3 h Pro thinking per result; no per-family figure | not computable from disclosures |
| 2-to-1 Games (human 4-to-1 result vs OpenAI family 105) | 20 PY ($5M) on the conjecture line | release-wide 3 h Pro thinking per result; no per-family figure | not computable from disclosures |
| HAWK key recovery (cumulative literature vs Anthropic run) | 38 PY ($9.6M) incl. borderline; 35 PY yes-only | ~60 h, ~$100k | ~90 |
| HAWK, marginal step (Mureau-Pellet-Mary 3n/4+1 vs Claude n/2+1) | actual human effort undisclosed; former 0.3-1 PY range was hypothetical | ~$100k plus human work; active human hours undisclosed | not computable from disclosures |

The class-wide budget table now lives in
[the adopted method, section 3](ai_effort_comparison_scoping.md#3-human-inputs-and-current-class-budgets)
and uses the 2026 cumulative research-FTE columns of data/authors/fte_by_year.csv.
It supersedes the older headcount totals previously quoted here. Disclosed AI
runs can be set beside those scenarios after aligning price and cost boundaries;
that comparison does not measure an equivalent fraction of scrutiny.

## 3. How to read the evidence

1. Historical literature effort and the cost of a new result are different
   quantities. Their ratio is descriptive and does not establish how much human
   labor an AI replaces. HAWK's approximately 90x cumulative dollar ratio is used
   only in the separately labeled historical-effort normalization.
2. In this selected sample, the 12 AI-resolved Erdős problems have median estimated
   human effort of 4.0 PY and the 10 unresolved ones 2.0 PY. These small, selected
   groups do not establish a general relationship between literature size and
   AI success.
3. Failure accounting is incomplete and varies by source. Anthropic describes
   its ~$100k as the full HAWK discovery process; whether earlier unsuccessful
   campaigns are included is unknown. It should not be relabeled as the cost of
   only one successful session. The AES discussion does not quantify HAWK failures.
   These accounting gaps and human-proxy uncertainty prevent rigorous bounds on
   the productivity advantage.
4. HAWK's human marginal effort is unknown. At the chosen cost convention,
   $100k equals 0.4 PY before supervision and other costs. Near-parity and
   days-versus-months claims cannot be inferred from the publication dates.
5. The adopted 1x/10x/100x multipliers are sensitivity scenarios, not a statistical
   interval inferred from these case comparisons. No scenario is a point estimate.

## 4. Method caveats

- Two-pass agreement is good on HAWK (kappa 0.78) and 2-to-1 (0.76) but poor
  on several Erdős problems (0.05-0.6): the strong model demoted problem
  collections and variant papers that the fast model kept. Erdős estimates
  are therefore less stable; the 10% audit of exclusions flipped nothing
  except on #970 (4 of 6, prime-gap constructions counted as Jacobsthal
  lower bounds), so recall there is understated.
- OpenAlex coverage: 192 of 322 Erdős seed titles and 85 of 87 TCS seeds
  resolved; abstracts missing for about half of all items; forward citers
  capped. Old classic papers resolve badly. Direction of bias: undercount.
- Priors are per paper, not per problem-year; a 1950 note and a 2024 paper
  count the same.
- The monetary rate ($250k) is the user's decision; budgets scale linearly.
- The HAWK Monte Carlo interval samples independent per-paper priors. It does
  not include uncertainty in the shared papers-to-years conversion, coverage or
  attribution. The exchange table's prior-endpoint ranges and those Monte Carlo
  intervals have different meanings; neither is a comprehensive confidence bound.
- Self-evaluation: this study was run with Claude models, and the HAWK AI
  figures come from Anthropic. The Erdős and OpenAI figures are independent
  of that.

## 5. The controlled rediscovery run (deferred)

The user chose the assumption-based comparison on 2026-10-09; further experiments
are not required. Six earlier attempts (three Fable 5.1, three Opus 5.5) were
interrupted by model safeguards, with no completed mathematical evaluations.
See [the archived protocol and run log](pilot_hawk_protocol.md). These interruptions
measure workflow availability, not mathematical failure. The packet and held-out
answer key remain in data/ai_effort/pilot_hawk/ for possible future research.

## 6. UGC and 2-to-1 as a pair

UGC (86 PY) and 2-to-1 (20 PY) overlap: 622 pool items are shared and the
2-to-2 Games line is counted under both. Read them as nested, not additive.
No per-family compute was published, and the claims' validation status matters.
Release-wide thinking hours and subscription prices do not establish per-result
inference costs. These rows remain "not computable" from the disclosures; scenario
budget equivalents can still be calculated from H under the adopted assumptions.

## 7. Token cost of this track

About 4.0M subagent tokens (data/phase1/token_ledger.tsv, stage ai_effort):
haiku screens ~1.2M, sonnet pass 1 and extraction ~1.9M, opus pass 2 ~0.76M,
blocked rediscovery attempts ~0.3M.
