# Handoff status (updated 2026-10-09; Phase 1 incl. round 2 complete; records normalized)

Python 3 stdlib only; run scripts with `python3 -I` from the repo root. Raw pulls
live under data/raw/ (gitignored, re-harvestable). Committed and NOT to be
regenerated: data/eprint.jsonl, data/candidates*.jsonl, data/labeled_*.jsonl,
data/labels/, data/phase1/ (pools, batches, labels, labeled_*.jsonl, token
ledger), records/, data/export/.

Read analysis/phase1_report.md first: it has the counts, ratios, recall
findings and the decision list.

## Standing decisions (user, 2026-10-08)

- OpenAlex API key in ~/.openalex_key (never print or commit it); keyed budget
  10,000 credits/day. Search = 10 credits/page, filter page = 1, singleton = 0.
- Classification budget: original ~10M spent (round 1: 10.92M); user then
  approved round 2 (v2 screen + 10% tier-B sample; actual 2.64M). Total 13.57M
  (ledger data/phase1/token_ledger.tsv). Further classification needs approval.
- The 2026 'Module Lattice Security' (Luo) poly-time ML-KEM claim series is
  excluded from this project (data/manual_exclusions.json); user reviews it separately.
- Git: commit locally at checkpoints, do not push.
- Records: every records/*.yaml stays `verified: false` until a human checks it.

## Done

- Phase 0 (ePrint pilot): analysis/phase0_report.md.
- Phase 1 acquisition: DBLP dump (375,911 kept), OpenAlex phrases (14,195),
  OpenAlex DOI enrichment (39,207 DOIs), OpenAlex snowball round 1 (811 seeds;
  5,071 backward + 16,216 forward), zbMATH (7,498). arXiv blocked (429/503).
- Merge/screen/tier (pipeline/merge_sources.py): 9,245 tier A (classified),
  8,353 tier B (not classified). Coverage: analysis/phase1_coverage.txt.
- Two-pass classification of tier A + 207-item ePrint isogeny supplement:
  data/phase1/labeled_final.jsonl. Kappa 0.87, category agreement 0.92, FN 1.1%
  (analysis/phase1_agreement.txt). Rubric now v0.3.4.
- Combined counts: analysis/phase1_counts.py -> analysis/phase1_counts.txt
  (+ _with_borderline). Export: data/export/combined_included.csv (3,841 rows).
- Records track: 338 files in records/<class>/ + HoF CSVs; summary
  analysis/records_frontier.md; loader pipeline/load_records.py.
- Recall benchmark: analysis/recall_benchmark.md (+ recall_unlabeled_refs.tsv).
  v2 screen dry run: analysis/screen_v2_impact.txt, candidates staged in
  data/phase1/screen_v2_candidates.jsonl (1,840 items, unclassified).

## Round 2 (done 2026-10-09)

- data/phase1/round2/: v2-screen pool (1,840) + seeded 10% tier-B sample (835),
  two-pass labels -> data/phase1/round2/labeled_final.jsonl (kappa 0.89,
  analysis/round2_agreement.txt). Included in analysis/phase1_counts.py
  (incl. a tier-B x10 extrapolated view) and data/export/combined_included.csv.
- Recall vs. seed reference lists now ~96-100% per class (analysis/recall_benchmark.md).
- User verified records: RSA-260, RSA-896, 2^1277-1, and the seven 2026 TII
  McEliece solves (provisional); see verified_by lines.


## AI-effort comparison track (2026-10-09, scenario method adopted)

Current decision (user, 2026-10-09): use assumed 1x/10x/100x economic productivity
at $250k per research-year, D = $250k * H / s. These are sensitivity scenarios,
not an empirical exchange rate. HAWK-normalized historical effort is a separate
worked example. Rediscovery experiments are deferred and not needed for this
comparison; no additional classification, outreach, or paid collection is needed.

Earlier decisions retained for provenance: calibration problems = Epoch Erdős
set, 2-to-1 Games, UGC; cheap models for extraction/seeds/pass 1; original
rediscovery pilot approved; commit AND push this track (user request 2026-10-09).

Read: analysis/ai_effort_comparison_scoping.md (adopted method, current class
budgets, reference-price token conversion), analysis/ai_effort_calibration_report.md
(supporting evidence), analysis/ai_effort_hawk_case.md (normalization example),
analysis/calib_exchange_table.md (per-problem literature estimates/disclosures).
Class budgets use the 2026 *_fte_cumulative fields in data/authors/fte_by_year.csv;
recompute them when the author map changes. No real reference token-price mix has
been selected; the $10/million example in the method is hypothetical.

- AI-side disclosures with sources: data/ai_effort/ai_results.yaml (15 entries);
  per-attempt Erdős rows data/ai_effort/erdos_problems.csv; raw text under
  data/raw/ai_effort/ (gitignored; MANIFEST.md there).
- Human side per problem: data/ai_effort/calib/<problem>/ (pool, screen_labels,
  labels_p1, labels_p2, labeled_final.jsonl, estimate.txt). Tooling:
  pipeline/rubric_calibration.md, make_calib_pool.py, build_calib_pools.py,
  make_screened_batches.py, calib_two_pass.py, calib_estimate.py,
  analysis/calib_exchange_table.py. OpenAlex snowball dir: data/raw/openalex_calib/
  (resumable; seeds_all.jsonl holds HAWK + Erdős-unique + TCS seeds).
- Done: HAWK (38 PY), UGC (86 PY), 2-to-1 (20 PY), 22 Erdős problems; all
  two-pass with 10% exclusion audits; table regenerated.
- Rediscovery pilot: DEFERRED by the current scenario-method decision. Earlier
  model safeguards interrupted all 6 attempts (Fable and Opus), with no completed
  mathematical evaluations. analysis/pilot_hawk_protocol.md preserves the log;
  packet and held-out set remain in data/ai_effort/pilot_hawk/. No decision on
  rerunning the pilot is needed for the adopted comparison.
- Token cost of this track: see data/phase1/token_ledger.tsv rows tagged ai_effort
  (~4.0M subagent tokens).
- Still blocked: ePrint PDFs (Cloudflare) for 2026/1593, 1560, 1377, 2266; the
  Anthropic-hosted copy of 1593 was fetched and text-extracted with Ghostscript.
- Not done (optional): remaining 49 Erdős problems (pools built but not
  screened: data/ai_effort/calib was rebuilt for the 22-problem subset only);
  asking Mureau/Pellet-Mary and the Luo group for their own effort figures.

## Selected attack bounds and events (2026-10-09, revised)

- Eight source-linked tracks in data/attack_history/: five selected numerical
  histories and three qualitative event histories. All human-verification flags
  remain false; primary-source checking and methodological review used agents.
- Corrected the Both-May coefficient/rate scope, lattice oracle comparisons and
  dates, early MQ coverage and guarantees, finite-field target/units, and SIDH
  interpretation. Removed invented compute and security-stability metrics.
- analysis/attack_stability.py builds the report and JSON/CSV exports. The site,
  detailed methodology and paper share those outputs. paper/attack_history.tex
  explains selection, indices, corrections and incompatible guarantees.
- Regression checks cover invalidated claims, absent numerical models,
  independently computed inverse envelopes, RSA's exact L exponent, and source
  eligibility. Remaining scientific limitations: incomplete selected history,
  asymptotic-to-finite-size distortion, different guarantees and unverified proofs.

## Waiting on the human

1. (Done 2026-10-09) Records normalization adopted: analysis/normalization_method.md
   (method + rationale), analysis/normalization.json (factors, targets),
   analysis/normalization_sources.json (sourced constants; see its "unresolved"),
   analysis/records_normalize.py -> analysis/records_normalized.md.
2. Optional: snowball round 2; targeted tier-B pass over the three productive
   signatures (~2,100 items, ~2.5M tokens).
3. Human label spot-checks: analysis/review_sheet.md (Phase 0) and a Phase 1
   sample sheet (to be generated).

## Can proceed without the human (next session)

- Retry arXiv (`python3 -I pipeline/fetch_arxiv.py data/raw/arxiv`) on another
  day; arXiv rate-limited this IP for hours.
- Thesis proxy: harvest HAL/theses.fr/DART-Europe (PLAN §5) - DBLP has only
  ~12-21 included theses per class.
- Records: derive GPU-years/core-years where "N devices x D days" is stated
  (currently only 89 of 326 records have stated core-years).

## Raw re-harvest (new machine)

```bash
mkdir -p data/raw/zbmath data/raw/openalex data/raw/dblp data/raw/arxiv
python3 -I pipeline/fetch_zbmath.py data/raw/zbmath
curl -L -A "literature-search-pilot/0.1" -o data/raw/dblp/dblp.dtd https://dblp.org/xml/dblp.dtd
curl -L -C - -A "literature-search-pilot/0.1 (mailto:matthewdgreen@gmail.com)" -o data/raw/dblp/dblp.xml.gz https://dblp.org/xml/dblp.xml.gz
python3 -I pipeline/parse_dblp.py data/raw/dblp/dblp.xml.gz data/raw/dblp/dblp_candidates.jsonl
python3 -I pipeline/fetch_openalex.py phrases data/raw/openalex
python3 -I pipeline/merge_sources.py          # writes enrich_dois.txt and seeds files
cat data/raw/openalex/seeds.jsonl data/raw/openalex/seeds_unresolved.jsonl > data/raw/openalex/seeds_all.jsonl
pipeline/run_openalex_chain.sh                # dois -> resolve -> backward -> forward (one OpenAlex harvester at a time)
python3 -I pipeline/merge_sources.py
```

## Author map + classified comparison (separate track, 2026-10-09)

Person-level map of public cryptanalysts per class: research-FTE and calendar
person-years per year and cumulative, career stage (ORCID / Math Genealogy /
Wikidata), zbMATH output counts, and a Part 2 scenario comparison with
classified Five Eyes headcount. Read: analysis/author_map.md (summary and
rebuild commands), analysis/author_map_method.md, analysis/classified_comparison.md,
notes/classified_headcount_evidence.md. Tables: data/authors/. Raw enrichment
caches (ORCID, MGP, zbMATH, Wikidata) are in data/raw/enrich/ (gitignored).

Open: human check of the top-25 lists per class (user); non-Latin-script name
mapping; arguing the classified-scenario parameters
(analysis/classified_scenarios.json) with people who know the agencies.

## Working white paper (2026-10-09)

The intended synthesis is a LaTeX white paper. First working draft:
[paper/whitepaper.tex](paper/whitepaper.tex), bibliography in paper/references.bib;
compiled output at output/pdf/cryptanalytic-effort-whitepaper.pdf. Build with
`make -C paper` (local Python stdlib + latexmk, no paid runs).

Coverage: literature search and class counts; author-output and paper-based effort
proxies; nominal person-hours using 2,000 h/research-year with a separate
career-adjusted view; human literature effort around selected math problems;
OpenAI/Anthropic disclosures; forward budget scenarios and inverse assumed
human-year equivalents. Token-only figures retain explicit price assumptions.
The draft does not identify those equivalents with actual human lab labor.

Tables and figure inputs are regenerated by paper/generate_tables.py; source
hashes and constants are in paper/generated/manifest.json. Review the prose when
inputs change. Before circulation: human label checks, temporal/AI-involvement
audit of the problem literature, person-hour definitions, disclosure boundaries,
and validation status of cited math results. Rediscovery remains deferred.

## Website methodology review (2026-10-09)

Updated docs/ without changing the visual stylesheet or baseline author-year
series. Publication shares are explicitly allocation proxies that may
substantially overestimate working time; career adjustment remains an assumed
sensitivity. Website fixes include the main-view corpus count, source-subset
labels, removal of cross-estimator HAWK calibration, successful-run cost
averages, flagged AI-assisted literature, and qualified frontier comparisons.
`python3 -I pipeline/build_site_data.py` regenerates the site data;
`make -C paper` now also copies the PDF into docs/assets/.

A bounded scope audit is in analysis/scope_audit/bounded_review.json. The
rubric excludes leakage extraction but deliberately includes mathematical
hint models and shared solver machinery. The audit flags a HAWK/LIP scope
mismatch and several attribution questions for later review; it does not
relabel the corpus or imply that all keyword matches are errors. Missing
leakage flags prevent a comprehensive no-leakage comparison.

Pending model audit: author_map.py's `num_any` denominator guard takes the
maximum class weight per item rather than the sum across disjoint classes.
This does not guarantee a total allocation <=1 in all edge cases; actual
publication counts and the rate floor can mask it. Quantify before changing
published totals. Exact reruns require the ignored raw DBLP match/profile
inputs, which are absent in this checkout. The current website retains the
existing exports with explicit uncertainty rather than presenting an
unvalidated numerical correction.
