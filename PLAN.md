# Estimating public cryptanalytic effort across standardized PKE assumptions

Working plan, v0.2 (2026-10-08)

Status: Phase 0 pilot executed on ePrint on 2026-10-08; see
`analysis/phase0_report.md` for counts, classifier agreement, and the rubric
revisions to apply before Phase 1.

## 1. Goal

Produce a defensible, reproducible comparison of how much public cryptanalytic
effort has been spent on each assumption class underlying standardized
public-key encryption / key agreement, expressed as (a) a classified
bibliography, (b) a table of computational records with normalized compute,
and (c) an order-of-magnitude effort estimate per class with explicit
uncertainty. The output should be strong enough to support a claim of the form
"class X has received roughly N times the public scrutiny of class Y, and the
largest public computation against X is 2^k operations versus 2^j against Y."

Non-goals: ranking the *security* of the assumptions; estimating classified
effort with any precision (we bound it, see §8).

## 2. Scope

### 2.1 Assumption classes (primary)

| Class | Standardized instantiation | Problem variants to fold in |
|---|---|---|
| ECDLP | ECDH (SP 800-56A), ECDSA/EdDSA (FIPS 186-5), ECIES, X25519/X448 | EC-CDH, EC-DDH, gap-DH, static-DH / oracle-assisted DLP, interval DLP, DLP on Koblitz/binary/pairing-friendly curves, Weil descent targets |
| MLWE (and RLWE) | ML-KEM (FIPS 203); NTRU-family in deployed products (sntrup761 in OpenSSH, NTRU-HRSS) | MSIS/RSIS only insofar as the attack is shared (ML-DSA, Falcon); ideal-SVP, NTRU problem, decisional vs search |
| plain LWE | FrodoKEM (ISO track; BSI/ANSSI recommendations) | LWR, BDD/uSVP formulations, LPN as a boundary case |
| Syndrome decoding | HQC (NIST selection, March 2025; quasi-cyclic SD); Classic McEliece (ISO track; binary Goppa SD); BIKE (QC-MDPC, not selected) | Generic SD over F_2 and F_q, QC-SD, low-weight codeword finding, Goppa-code distinguishing, MDPC decoding-failure attacks (scheme-level, tag separately) |

### 2.2 Comparator / calibration classes (secondary, cheaper pass)

- Factoring and finite-field DLP (RSA, FF-DH). The best-documented class
  anywhere; gives a ceiling for "mature" and a well-measured compute history
  (RSA-250, DLP-240). Also where index calculus ideas originate before being
  tried on curves.
- Isogenies (SIDH/SIKE) and multivariate (Rainbow). Both received serious
  multi-year scrutiny and then broke. They provide base rates: how much visible
  effort preceded the break, and what the paper-count curve looked like before
  it. Light pass only: counts and timeline, no full tagging.

Including comparators is what turns raw counts into something interpretable.

### 2.3 Boundaries (what is *not* counted)

- Side-channel, fault, and implementation attacks (not about the assumption).
- Constructions that *use* the assumption (the bulk of the lattice literature).
- Protocol-level or scheme-level attacks that do not bear on the underlying
  problem (e.g. KEM misuse, invalid-curve attacks). Decoding-failure /
  reaction attacks on QC-MDPC and HQC are a borderline case; tag them as
  "scheme-level" and report them separately rather than drop them.
- Pure worst-case/average-case reduction theory. Keep it, but in its own
  category ("hardness theory"), since it is confidence-building rather than
  cryptanalytic effort. Decide later whether it enters the effort estimate.

### 2.4 Time windows

Start dates differ and this must be visible in every chart:
ECDLP 1985 (Miller/Koblitz; generic-group DLP results earlier),
lattice reduction 1982 (LLL; knapsack cryptanalysis is lattice cryptanalysis),
LWE 2005, RLWE 2010, MLWE 2011-12, syndrome decoding 1962 (Prange) /
McEliece 1978. Report both cumulative totals and per-era totals (pre-2016 vs
NIST-competition era) because the competition massively distorts the recent
counts for lattices and codes.

## 3. Taxonomy of a "relevant paper"

Every included item gets one primary category and any number of assumption
tags plus a technique-layer tag (§4).

| Category | Definition | Examples |
|---|---|---|
| A. Algorithm (classical) | New or improved algorithm for the problem, incl. asymptotic improvements | Pollard rho variants, Semaev/Gaudry/Diem index calculus, BKZ 2.0, sieving (GaussSieve, BDGL16, G6K), dual attacks, BKW, Arora-Ge, Stern/Dumer/MMT/BJMM/May-Ozerov ISD, Both-May |
| B. Algorithm (quantum) | Quantum algorithms or resource estimates targeting the problem | Shor-on-EC resource estimates (Roetteler 2017, Häner 2020, Gidney), quantum sieving, quantum ISD, Eisenträger-Hallgren-Kitaev-Song unit group, Cramer-Ducas-Peikert-Regev, Chen 2024 (retracted) |
| C. Structural | Results exploiting or ruling out structure: Weil descent, anomalous/MOV curves, ideal-lattice structure, QC/Goppa structure, distinguishers | GHS, Smart/SSSA, Frey-Rück, Campbell-Groves-Shepherd "Soliloquy", Biasse-Song, FGOPT high-rate Goppa distinguisher, DOOM |
| D. Concrete cost / parameter estimation | Cost models, estimators, "how big must n be" | Lattice Estimator lineage (Albrecht-Player-Scott 2015 onward), MATZOV 2022, Ducas-Pulles 2023, CryptographicEstimators, Bernstein-Lange "non-uniform cracks", Hamdaoui-Sendrier |
| E. Computational record | Solves a concrete instance and reports compute | Certicom challenges, secp112r1 (Bos et al.), FPGA 113/117-bit solves, SVP/LWE/Ideal/NTRU challenge records, decodingchallenge.org records, Bernstein-Lange-Peters 2008 |
| F. Negative / generic-model results | Lower bounds, impossibility, "no index calculus on these curves" | Shoup generic-group bound, Nechaev, limits on summation-polynomial approaches |
| G. Hardness theory | Reductions among variants, worst-case/average-case | Regev 2005, LPR 2010, Langlois-Stehlé, Alekhnovich, Peikert-Regev-Stephens-Davidowitz |
| H. Failed / retracted attacks | Public claims later withdrawn | Chen 2024 quantum LWE; various claimed ECDLP index-calculus speedups |
| S. Survey / thesis | Used for snowballing; theses also enter the effort model | Galbraith-Gaudry 2016, Peikert 2016, Weger-Gassner-Rosenthal, PhD theses |

Categories A-F and H are "cryptanalytic effort." G is reported alongside.
Category H deserves its own count: a withdrawn attack is still evidence that
capable people tried.

## 4. Attribution model (the hard part)

Most attack papers are not about one assumption. A sieving paper applies to
MLWE, LWE, NTRU, MSIS and the SVP challenge alike; an ISD paper applies to
HQC, McEliece and BIKE; an index-calculus paper might target FF-DLP with
curves as a secondary target. Use a three-layer scheme and fractional
attribution:

- Layer 0, generic machinery: lattice reduction / sieving / enumeration;
  ISD and its sieving analogues; generic-group algorithms (rho, kangaroo,
  BSGS); index calculus / NFS. Attributed to every class that the technique
  is the best known attack on, with weights set per class at the pilot
  stage (e.g. a BKZ paper: MLWE 0.4, LWE 0.4, MSIS/NTRU 0.2).
- Layer 1, assumption-specific: structured-lattice attacks (ideal/module
  structure), Goppa / QC structure, EC-specific index calculus, Weil descent.
  Attributed fully to the class.
- Layer 2, scheme-specific: parameter-set analyses of Kyber-512, HQC-128,
  mceliece348864, FrodoKEM-640, P-256/secp256k1. Attributed fully and also
  flagged so we can report "effort aimed at the deployed parameters."

Report results under at least two attribution rules (fractional and
"count once per class touched") to show the ranking is robust to the choice.
If the ranking flips between rules, that is a finding, not a bug.

## 5. Data sources

| Source | Why | Access |
|---|---|---|
| DBLP | Complete coverage of crypto venues (CRYPTO, EUROCRYPT, ASIACRYPT, PKC, TCC, CHES, PQCrypto, SAC, ANTS, JoC, DCC, Math. Comp.) | Full XML dump or publication-search API; venue-filtered pull |
| IACR ePrint | Where attacks appear first; many never reach a venue; full text available | Per-year listings + search; bulk metadata/abstract scrape with rate limiting; PDFs for category D/E extraction |
| arXiv | cs.CR, cs.IT (coding), math.NT (ECDLP, index calculus), quant-ph (resource estimates), cs.DS (lattice algorithms) | API |
| OpenAlex | Citation graph for snowballing, abstracts, free | API, bulk |
| Semantic Scholar | References/citations endpoints, SPECTER embeddings for classifier features, citation counts as an attention proxy | API with free key |
| zbMATH Open | Math-side coverage (number theory, lattice algorithms) that DBLP misses | Free API |
| HAL / theses.fr, DART-Europe, ProQuest | PhD theses (INRIA Caramba/COSMIQ/LFANT, ENS Lyon, TU/e, Bochum/CASA, Royal Holloway, Waterloo) | Search + manual |
| NIST pqc-forum archive; NIST IR 8240 / 8309 / 8413 / 8545 | Attack discussion that never became papers; NIST's own per-candidate summaries | Google Groups export; PDFs |
| Challenge sites | Ground truth for records: Certicom ECC challenge, TU Darmstadt SVP / LWE / Ideal-lattice challenges, Security Innovation NTRU challenge, decodingchallenge.org, RSA factoring challenge | Hall-of-fame pages (archive.org for Certicom and NTRU) |
| Non-academic compute | Bitcoin "puzzle" transactions (interval ECDLP on secp256k1 by kangaroo where the public key is exposed; brute force + hash otherwise), Large Bitcoin Collider, pool efforts | Forum threads (bitcointalk), GitHub (JeanLucPons Kangaroo, BitCrack), privatekeys.pw |
| Software | Effort proxy and reference list source: fplll, G6K (+GPU), lattice-estimator, CryptographicEstimators, CADO-NFS, ISD implementations | GitHub (commit history, contributor counts) |
| Funding databases | Person-year proxy: NSF award search, EU CORDIS (PQCRYPTO, PROMETHEUS, SAFEcrypto), ERC, ANR, DFG (CASA), NWO | Public search |

Google Scholar is used only for manual recall checks (no API; scraping is
unreliable and ToS-hostile).

## 6. Search methodology

### 6.1 Candidate pool (high recall)

Boolean queries per class over DBLP + ePrint + arXiv + OpenAlex, deliberately
broad. Expected pool: tens of thousands of records, most irrelevant. Starter
query stems (to be refined in the pilot):

- ECDLP: "elliptic curve discrete logarithm", "ECDLP", "Pollard rho" AND
  curve, "summation polynomial", "Weil descent", "index calculus" AND
  (elliptic OR curve), "Koblitz curve" AND (attack OR solve), "anomalous
  curve", "MOV", "generic group" AND (lower bound OR discrete log),
  "kangaroo", "interval discrete log".
- Lattices: "learning with errors" AND (attack OR cryptanalysis OR estimate
  OR solving OR dual OR primal OR BKW), "module-LWE", "ring-LWE" AND
  (attack OR structure OR ideal), "BKZ", "lattice sieving", "lattice
  enumeration", "shortest vector" AND (algorithm OR record OR challenge),
  "NTRU" AND (attack OR cryptanalysis OR hybrid), "ideal lattice" AND
  (quantum OR attack OR unit), "Kyber" AND (attack OR security estimate),
  "SVP challenge", "LWE challenge".
- Codes: "information set decoding", "syndrome decoding" AND (algorithm OR
  attack OR complexity OR estimate), "McEliece" AND (attack OR cryptanalysis
  OR distinguisher OR structural), "Goppa code" AND distinguish, "quasi-cyclic"
  AND (attack OR decoding OR DOOM), "MDPC" AND (attack OR failure OR reaction),
  "HQC" AND (attack OR security), "low weight codeword", "decoding challenge".
- Cross-cutting: "quantum resource estimate" AND (elliptic OR lattice OR
  decoding), "post-quantum" AND cryptanalysis.

Deduplicate across sources on DOI, then on normalized title + first author +
year (ePrint vs venue versions are merged into one item with both links;
keep earliest date as the effort date).

### 6.2 Classification (precision)

1. Title + abstract pass with an LLM classifier against the §3 rubric,
   emitting: include/exclude, category, assumption tags, layer, and a one-line
   justification. Run two independent passes (different prompts or models)
   and route disagreements to manual review.
2. Manual validation on a stratified random sample (~300 items, stratified by
   class and source). Measure precision and recall against hand labels;
   target >0.9 precision and >0.85 recall before proceeding. Record Cohen's
   kappa between the two automated passes.
3. Full-text pass only for categories D and E (structured extraction, §7) and
   for anything the abstract pass flagged as uncertain.

### 6.3 Snowballing (recall)

Seed sets, which also serve as a recall benchmark (fraction of each seed
list's references that the pipeline recovered on its own):

- ECDLP: Galbraith-Gaudry 2016 (DCC) survey; Handbook of Elliptic and
  Hyperelliptic Curve Cryptography attack chapters; SafeCurves bibliography;
  Certicom challenge write-ups; Bos et al. secp112r1 paper; Joux,
  Algorithmic Cryptanalysis.
- Lattices: lattice-estimator reference list; Peikert 2016; "Estimate all
  the {LWE,NTRU} schemes!"; NIST IR 8413 §Kyber/Saber/NTRU/Frodo security
  sections; ML-KEM and FrodoKEM specification security chapters; G6K and
  MATZOV reference lists; Ducas-Pulles 2023.
- Codes: CryptographicEstimators (SDFq, SD) reference list; Sendrier 2017
  "Code-based cryptography: state of the art"; Weger-Gassner-Rosenthal;
  Classic McEliece, HQC, BIKE spec security chapters; decodingchallenge.org
  record write-ups; Esser's and Zweydinger's theses.
- Comparators: NFS literature via CADO-NFS and Boudot et al. 2020; SIKE break
  (Castryck-Decru, Maino-Martindale, Robert) citation neighborhoods;
  Beullens 2022 for Rainbow.

Iterate forward (citations) and backward (references) from every included
item, re-classify new candidates, stop when a round adds under ~2% new
included items. Expect two to three rounds.

### 6.4 Database schema (SQLite + CSV export)

`papers`: id, title, authors (list), author_count, year, first_appearance_date,
venue, venue_tier, eprint_id, doi, arxiv_id, url, abstract, category,
assumption_tags (with fractional weights), layer, targets_deployed_params
(bool), is_thesis, citation_count (date-stamped), source_of_discovery
(query / snowball seed), classifier_confidence, manual_reviewed (bool), notes.

`authors`: name, affiliations by year, group (hand-curated for the ~200 most
prolific), country.

`records`: paper_id, problem (ECDLP / SVP / LWE / SD / NTRU / factoring /
FF-DLP / interval-ECDLP), instance_description, instance_size (bits, dim,
n/k/w), log2_expected_ops, method, structure_exploited (bool), hardware (CPU
model / GPU model / FPGA), core_count, wall_time, reported_core_hours,
normalized_core_years_2020 (with conversion factor used), energy_estimate
(optional), date, extrapolated_cost_to_deployed_params (log2, as reported by
the authors), source_url.

`software`, `theses`, `grants`: proxies for §8.

## 7. Computational records track

This gets its own workstream because it is the only place where effort is
measured in hard units.

1. Enumerate records per class from challenge hall-of-fames, the E-category
   papers, and non-academic sources. Known anchors to verify and extend
   (dates and figures from memory; confirm every one):
   - ECDLP: Certicom ECC2K-108 (2000), ECCp-109 (2002), ECC2-109 (2004);
     secp112r1 on PS3 cluster (Bos-Kaihara-Kleinjung-Lenstra-Montgomery,
     2009); 113-bit Koblitz and binary curves on FPGAs (Wenger-Wolfger 2014/15);
     117.35-bit binary curve on FPGAs (Bernstein-Engels-Lange-Niederhagen-
     Paar-Schwabe-Zimmermann 2016); 114-bit BN curve (Kusaka et al. 2017);
     ECC2K-130 effort (Bailey et al. 2009; check whether ever completed).
     Bitcoin puzzle: kangaroo solves of exposed-pubkey puzzles (#105-#130
     range, 2020-2025) and brute-force solves up to roughly #66-#69
     (2024-2025); these are 2^60-2^66-scale real computations and dwarf the
     academic ECDLP record compute.
   - Lattices: SVP challenge dim 180+ (Ducas-Stevens-van Woerden 2021,
     GPU sieving) and later entries; LWE challenge top entries; Ideal
     lattice challenge; NTRU challenge solves (2014-2016); any record from
     the Albrecht-Bai-Fouque-Kirchner-Stehlé-Wen enumeration work (2020).
   - Codes: Bernstein-Lange-Peters 2008 (original McEliece parameters);
     decodingchallenge.org Goppa/McEliece track (Esser-May-Zweydinger 2022
     "McEliece needs a break" and successors by Narisada et al., Esser-
     Zweydinger); SD and QC tracks; large-weight track.
   - Comparators: RSA-240/DLP-240 (2019), RSA-250 (2020), GF(2^n) DLP
     records (Granger et al.), SIKE break compute (minutes on a laptop; the
     point is the contrast).
2. Extract the record fields in §6.4 from each paper, including hardware
   generation, so compute can be normalized. Pick one normalization unit
   (proposal: "2020 CPU-core-year equivalents") and document each conversion
   factor (GPU-year, FPGA-year, PS3-year, 2008 Core 2 year). Report raw
   numbers alongside, since the conversions are crude.
3. Build the "frontier" plot per class: log2(expected ops) of the largest
   public solve vs date, with the deployed parameter target drawn as a
   horizontal line. The gap between frontier and target, and the frontier's
   slope, are the two headline numbers. Note where records exploit structure
   (Koblitz, QC) versus generic parameters.
4. Sum compute per class across all records and challenge submissions
   (challenge sites list every submission, not just the top), plus
   non-academic compute, with academic/non-academic split.
5. Record the authors' own extrapolations to deployed parameters, since
   those are the numbers the standards bodies actually relied on.

Adopted normalization (2026-10-09; full rationale in
analysis/normalization_method.md): the frontier is measured in log2(ops) on
each problem's own cost model (lattices: delta in sieving dimension/BKZ
blocksize, converted with a slope range from 0.292 to a practical exponent);
compute totals use 2020 core-year equivalents as low/high ranges over
record-setting solves only (not every hall-of-fame entry); Bitcoin-puzzle
compute is reported separately from ECDLP. This supersedes the "every
submission" wording of step 4 and the single-unit default in §11.

### 7.6 Selected attack bounds and events (revised 2026-10-09)

A supplementary sourced history separates algorithmic progress from literature
attention and attack execution. Eight tracks in data/attack_history/ comprise
five numerical indices (generic ECDLP, selected heuristic SVP sieve bounds,
worst-over-rate full-distance binary decoding, factoring, and Boolean MQ) and
three qualitative event histories (small-characteristic DLP, pairing-field
reassessments, and SIDH). This is an explicitly selected, incomplete history,
not a reconstruction of the best attack known at every date.

analysis/attack_stability.py evaluates supported classical leading formulas at
declared reference sizes. A second view independently inverts each formula and
takes the largest size giving index 128; neither view supplies calibrated
security bits or recommended parameters. There is no practicality filter.
Guarantees, memory, algebraic assumptions and source-version dates are recorded.
Corrected invalid claims cannot enter the running minimum. Missing numerical
models never imply infinite required sizes or zero security.

The former bits-lost, exponent-change-count and years-stable metrics are removed.
A flat curve can omit subexponential gains, implementation improvements, new
proofs and changes in the full attack. The SVP index is an oracle model, not an
ML-KEM attack; decoding maximizes over rates separately for each algorithm.
Output: analysis/attack_stability.md, data/export/attack_history.{json,csv}, the
website's attack-history section and detailed methodology, and the white paper's
selected-attack-methods section. Regression checks enforce these distinctions.
Sources have been checked by agents; independent human verification is pending.

## 8. Effort estimation methodology

The honest output is a log-scale range per class, not a point estimate.
Build it from several independent proxies and show them side by side; the
estimate is credible only where the proxies agree.

Proxy 1, weighted paper counts. Convert items to person-year equivalents
(PYE) with per-category priors, e.g. A/C/F: 1-2 PY per paper total across
authors; D: 0.5-1.5; E: 2-10 plus compute; B: 1-2; H: 0.5-1; S (survey): 0.5.
Apply fractional attribution (§4). Sample the priors (Monte Carlo over the
ranges) to get a distribution per class rather than a number.

Proxy 2, theses. A PhD thesis whose primary topic is attacking the class
counts as 3-5 PY. This is the most reliable single unit of focused effort
and it undercounts less than paper counts do (one thesis, many papers).

Proxy 3, distinct people and groups. Number of distinct authors, distinct
groups, and distinct countries contributing A-F work, per class and per
era. Diversity of scrutiny arguably matters more than volume; report it on
its own, not folded into PYE.

Proxy 4, funding. Sum identifiable grant money for projects whose stated
aim includes cryptanalysis of the class (CORDIS, NSF, ERC, ANR, DFG), convert
at a stated cost per researcher-year. Coarse, but independent of publication
behavior.

Proxy 5, compute (§7). Reported separately in core-years; do not convert to
person-years.

Proxy 6, attention. Citation counts of A-F items and pqc-forum thread
volume. This measures interest rather than effort; use it to sanity-check,
not to estimate.

Cross-checks:
- Compare paper-count-based PYE against thesis-based PYE; a ratio far from
  the expected papers-per-thesis (~3-5) flags a counting problem.
- Comparator classes: the ratio for factoring vs ECDLP should look plausible
  to anyone in the field; the pre-break curves for SIKE and Rainbow give a
  base rate for "how much visible effort preceded a break."
- Expert recall check: send the per-class bibliographies to one or two
  people per class and ask what is missing.

Classified effort. Cannot be measured; can be bounded and discussed. Public
effort is a lower bound. Evidence that non-public effort exists and sometimes
surfaces: Campbell-Groves-Shepherd "Soliloquy" (CESG, 2014) on a lattice
scheme; NSA's 2015 CNSA announcement and later statements; the historical
record on DES differential cryptanalysis and on RSA/DLP interest in SIGINT
agencies. Present the final estimates under scenario multipliers (e.g. 1x,
3x, 10x public effort) and state which conclusions survive which scenarios.
Note the asymmetry: the classified ECDLP/factoring effort is almost certainly
larger in absolute terms (decades of operational incentive), while the
lattice/code effort is more recent and its size is less inferable.

### 8.1 AI-equivalent inference budgets (adopted 2026-10-09)

Use explicit productivity scenarios rather than estimating an empirical
human-to-AI exchange rate. For estimated human research-years H, assume an
economic productivity multiplier s in {1, 10, 100} and report
D = $250,000 * H / s. The equivalent inference budgets per research-year are
$250k, $25k and $2.5k. These are sensitivity scenarios, not confidence bounds,
and no scenario is a preferred point estimate.

The class table uses the 2026 cumulative research-FTE columns of
data/authors/fte_by_year.csv. Keep that definition separate from career-adjusted
calendar person-years and per-paper PYE. Human-effort uncertainty and the
productivity assumption are separate axes. A common s preserves class rankings
by construction; it does not establish relative AI capability across classes.

The assumption is conditional on access to the existing literature and extends
to the mixture of negative, incremental and successful research. The budgets
describe scale, not expected attack cost, attack probability, or actual AI scrutiny.
Human supervision, tool compute, verification and training are outside the
inference allowance and must be separately accounted for in all-in comparisons.

Full method, class table, HAWK-normalized historical-effort example, and
reference-price token conversion: analysis/ai_effort_comparison_scoping.md.
HAWK normalization requires the same paper-based estimator on both sides and
is an assumed transfer, not an empirical calibration. Rediscovery experiments
are deferred; they are not a prerequisite for this comparison.

## 9. Known confounders (must be addressed in the write-up)

- Progress vs scrutiny. ECDLP has few recent attack papers partly because
  the field concluded (after the 2004-2015 index-calculus push) that generic
  attacks are optimal on prime-field curves. Low recent counts reflect a
  mature negative consensus, not neglect. Separate the per-era counts and
  the F-category (negative results) so this is visible.
- Competition inflation. 2017-2024 lattice and code counts are inflated by
  NIST-competition incentives and by the sheer size of the lattice
  community. Normalize per era and per deployed-parameter target (layer 2).
- FHE spill-over. Many LWE "attack" or "estimate" papers are motivated by
  FHE parameter choices with small secrets and huge moduli that are
  irrelevant to ML-KEM. Tag parameter regimes.
- Shared machinery. Handled by §4; always report under two attribution
  rules.
- Venue drift. ePrint-only items are not lower quality in cryptanalysis
  (many of the most important attacks were ePrint-first). Do not weight by
  venue in the headline estimate; report venue mix separately.
- Age of the field and tooling. A 1995 ECDLP paper and a 2023 sieving paper
  are different units of labor. Do not inflate; just show per-era.
- Non-academic effort. Bitcoin-puzzle compute is enormous but is generic
  kangaroo/brute force; it tells us about generic-attack engineering, not
  about structural weaknesses. Keep it in the compute table with a flag.

## 10. Phases and deliverables

The final synthesis is a working white paper in LaTeX: paper/whitepaper.tex,
with references, reproducible tables, and a compiled PDF. It covers the search,
human person-time estimates, historical effort around selected mathematical
problems, and assumed human-year equivalents of OpenAI/Anthropic AI budgets.
The inverse scenario conversion is H_equiv = s * D / $250k; nominal hours use
2,000 h/research-year, with the career-adjusted alternative shown separately.
These are conventions and scenario equivalents, not observed labor. First draft
and build instructions: paper/README.md. Rediscovery is not a prerequisite.


Phase 0, scoping and pilot (first). Finalize §3 rubric and §4 weights.
Run the full pipeline on ePrint only, all four primary classes, to calibrate
the classifier, measure precision/recall on a hand-labeled sample, and get
first per-class counts. Deliverable: pilot counts, labeled sample, revised
rubric.

Phase 1, acquisition. Pull DBLP (venue-filtered), arXiv, OpenAlex, zbMATH;
deduplicate; build the candidate pool. Deliverable: `papers` table populated
with candidates.

Phase 2, classification and snowballing. Two-pass classification, manual
validation, two to three snowball rounds from the §6.3 seeds, recall
benchmark against seed reference lists. Deliverable: included-set
bibliographies per class (BibTeX + CSV), recall/precision report.

Phase 3, records track (§7). Can run in parallel with Phase 2 since the
record set is small (expect under 100 items). Deliverable: `records` table,
frontier plots, normalized compute totals.

Phase 4, proxies and estimate (§8). Theses, authors/groups, funding,
Monte Carlo over priors, scenario analysis for classified effort.
Deliverable: estimate tables with ranges, sensitivity analysis.

Phase 5, write-up and external check. Report with figures; send
bibliographies to per-class experts for recall; revise.

Repository layout proposal:

```
literature-search/
  PLAN.md
  data/raw/        # per-source pulls, untouched
  data/db.sqlite   # working database
  data/export/     # BibTeX, CSV per class
  pipeline/        # fetch_*.py, dedup.py, classify.py, snowball.py
  records/         # one YAML per computational record, hand-verified
  analysis/        # notebooks: counts, frontier plots, estimates
  report/
```

## 11. Open decisions

- Whether hardness theory (G) enters the PYE estimate at all. Default: no,
  reported alongside.
- Whether NTRU gets its own column or is folded into MLWE. Default: own tag,
  folded into the structured-lattice total for headline numbers.
- Whether to include hash-based or other signature-only assumptions.
  Default: no (scope is encryption/KEM), but MSIS enters via shared
  lattice machinery at layer 0.
- Normalization unit for compute. Default: 2020 CPU-core-year equivalents,
  with raw figures always shown.
- How far to pursue funding data (Proxy 4). Default: EU + NSF + ERC only.
