# Phase 1 report: multi-source acquisition, classification, records

Date: 2026-10-09 (updated after the user-approved round 2). Builds on
analysis/phase0_report.md (ePrint pilot). Every number below is reproducible
from committed files via the scripts named. No classifier output has been
human-verified yet; 10 records have been checked by the user (section 4).

## 1. What was done

1. Harvests (raw pulls in data/raw/, not committed):
   - DBLP full dump (8.7M records) parsed with keyword title screen + crypto
     venue allowlist + all PhD theses: 375,911 kept.
   - OpenAlex: 50 phrase queries (14,195 works); abstracts for 39,207 core-venue
     DBLP DOIs (~19k had one); snowball from 811 ePrint seeds resolved to
     OpenAlex: 5,071 backward references, 16,216 forward citers (cap 400/seed).
   - zbMATH: 46 queries, 7,498 rows.
   - arXiv: blocked by the export API (429/503 for 2+ hours); skipped. OpenAlex
     indexes arXiv, so the loss is the arXiv-only remainder.
2. Merge and dedupe (pipeline/merge_sources.py): 356,673 merged items;
   19,266 keyword-screened; 1,875 already covered by ePrint candidates.
3. Tiering (calibrated on Phase 0 per-signature inclusion yields): tier A =
   9,245 (incl. the 207-item ePrint isogeny supplement); tier B = 8,353.
4. Round 1, two-pass classification of tier A (pipeline/classify_prompt.md,
   rubric v0.3.4): 9,254 items; pass 2 on all yes/borderline + 10% audit of no.
   Kappa 0.87, category agreement 0.92, est. FN rate 1.1%
   (analysis/phase1_agreement.txt).
5. Round 2 (user-approved 2026-10-09), same two-pass method:
   - v2 keyword screen (analysis/screen_v2_impact.py): 1,840 items that v1
     missed (classic titles without v1 keywords; "discrete log"-only titles).
   - Seeded 10% random sample of tier B: 835 items.
   - Kappa 0.89, category agreement 0.90, est. FN rate 0.5%
     (analysis/round2_agreement.txt).
6. Cost (data/phase1/token_ledger.tsv): round 1 10.92M, round 2 2.64M;
   classification total 13.57M subagent tokens (+1.03M for the records track).
7. Records track (records/, analysis/records_frontier.md): 338 record files
   (ECDLP 33, lattice 169, code 102, comparator 34) plus hall-of-fame CSVs.
8. Recall benchmark against 12 seed papers' reference lists
   (analysis/recall_benchmark.md).
9. Manual exclusion (user decision): the 2026 "Module Lattice Security" arXiv
   series claiming a poly-time quantum attack on ML-KEM is excluded from all
   counts (data/manual_exclusions.json; notes/mlkem_polytime_claims.md).

## 2. Combined counts (ePrint + Phase 1 rounds 1-2, include = yes, categories A-F,H)

Source: analysis/phase1_counts.txt (also _with_borderline.txt). Fractional
attribution per pipeline/attribution.json; "all lattices" = MLWE + plain LWE union.
Tier-B sample items enter at weight 1 here (they are real papers); the
extrapolated view below weights them x10.

| Class | Fractional | Touch | Distinct authors | pre-2006 | 2006-2016 | 2017-2026 |
|---|---|---|---|---|---|---|
| ECDLP | 465.2 | 555 | 801 | 97.3 | 197.6 | 170.2 |
| All lattices | 840.0 | 862 | 1,071 | 55.0 | 225.1 | 559.9 |
|   of which MLWE/structured | 477.4 | 803 | 988 | 32.5 | 133.2 | 311.6 |
|   of which plain LWE | 362.6 | 678 | 881 | 22.4 | 91.8 | 248.3 |
| Syndrome decoding | 289.5 | 325 | 473 | 24.7 | 80.1 | 184.7 |
| Factoring / FF-DLP (comparator) | 849.1 | 940 | 1,351 | 212.5 | 343.0 | 293.7 |
| Isogeny (comparator) | 80.4 | 83 | 168 | 0.0 | 2.2 | 78.2 |
| Multivariate (comparator) | 174.7 | 190 | 224 | 13.0 | 67.7 | 94.0 |

Relative to the ePrint-only pilot, multi-source coverage raised ECDLP 4.3x
(108.8 -> 465.2), pre-2006 ECDLP 9x (10.6 -> 97.3), lattices 2.6x, codes 2.6x.
Round 2 mostly added generic-DLP and factoring classics (factoring/FF-DLP
+30%; generic DLP items are split 50/50 ECDLP/FF-DLP) and LLL-era lattice work.

### Ratios to ECDLP, by view (robustness)

Each cell: fractional / touch / distinct authors; era columns use fractional counts.

| View | Lattices / ECDLP | SD / ECDLP | Factoring / ECDLP | Lattices/ECDLP by era (pre06, 06-16, 17-26) | SD/ECDLP by era |
|---|---|---|---|---|---|
| ePrint only | 2.91 / 2.47 / 1.75 | 1.01 / 0.97 / 0.87 | 1.61 | 0.19, 1.50, 5.48 | 0.00, 0.48, 1.99 |
| Combined, all sources | 1.81 / 1.55 / 1.34 | 0.62 / 0.59 / 0.59 | 1.83 | 0.57, 1.14, 3.29 | 0.25, 0.41, 1.09 |
| Combined, vetted (ePrint + DBLP-indexed) | 2.28 / 1.93 / 1.60 | 0.78 / 0.73 / 0.73 | 1.54 | 0.65, 1.35, 4.45 | 0.24, 0.44, 1.53 |
| Combined, confidence >= 0.6 | 1.87 / 1.61 / 1.38 | 0.64 / 0.60 / 0.60 | 1.71 | 0.56, 1.14, 3.56 | 0.23, 0.42, 1.15 |
| Vetted + confidence >= 0.6 | 2.30 / 1.96 / 1.60 | 0.78 / 0.74 / 0.71 | 1.48 | 0.65, 1.34, 4.56 | 0.20, 0.44, 1.56 |
| All sources + tier-B extrapolation | 2.00 / 1.72 / 1.34 | 0.64 / 0.61 / 0.59 | 1.87 | 0.66, 1.26, 3.66 | 0.25, 0.39, 1.16 |
| Vetted + tier-B extrapolation | 2.58 / 2.17 / 1.60 | 0.83 / 0.78 / 0.73 | 1.60 | 0.81, 1.56, 4.93 | 0.24, 0.44, 1.68 |

Provisional reading (before human validation of labels):

1. Cumulatively, structured + plain lattices have received roughly 1.3-2.6x the
   visible effort of ECDLP, depending on unit (distinct authors give the low
   end, fractional paper counts the high end) and on source vetting. The lead
   is a post-2016 phenomenon: 3.3-4.9x in 2017-2026; ECDLP led before 2006
   (lattices 0.57-0.81x).
2. Syndrome decoding has received roughly 0.6-0.8x the cumulative visible
   effort of ECDLP, again concentrated after 2017 (1.1-1.7x in that era).
3. The ePrint-only view overstated both PQ leads because ePrint misses older
   ECDLP work.
4. The vetted view (drops OpenAlex/zbMATH-only items, where predatory and
   unreviewed outlets concentrate) raises lattice and code ratios: ECDLP and
   factoring attract a long tail of low-quality papers that the classifier, by
   design, does not exclude on quality. Report both views.
5. Tier B (unclassified generic-pattern items) is estimated to hide ~13% more
   lattice papers (mostly LLL-variant and SVP/CVP algorithm papers), ~2% more
   ECDLP and ~5% more codes: it nudges the lattice ratio up, not the ordering.
   Estimate rests on 37 sample includes, so treat it as rough.

## 3. Recall

- Classifier recall relative to the candidate pool: ~99% (FN rate 1.1% round 1,
  0.5% round 2).
- Pool recall vs. seed reference lists (analysis/recall_benchmark.md): after
  round 2, of 429 references across 12 seed papers, 421 were harvested, 329
  screened in, 327 labeled and 295 labeled include; manual review of the 102 still
  unlabeled (analysis/recall_unlabeled_refs.tsv) finds ~6 in-scope misses
  (Wiener-Zuccherato 1999; two hyperelliptic decomposition-attack papers;
  the small-secret LWE dual/hybrid paper; MATZOV's 2022 report, which no
  source harvested; one FF-DLP paper). Per-class pool recall is now ~96-100%
  (was 82-89% before the v2 screen).
- Tier B: 10% sample yield 26 yes + 11 borderline of 835 (3.1% yes), from
  lattice reduction (8/136), SVP/CVP (6/57), factoring/NFS (5/21); zero yield
  from quasi-cyclic codes (193), multivariate (79), "decoding problem" (65),
  quantum-lattice, rank-metric and quantum-ISD signatures. A targeted pass over
  only the three productive signatures (~2,100 items, est. ~2.5M tokens) would
  replace the extrapolation with labels; not recommended unless the lattice
  sub-count matters at the ~10% level.

## 4. Records track (summary; details in analysis/records_frontier.md)

User-verified (2026-10-09): RSA-260, RSA-896, 2^1277-1 (Sept 2026 GPU-NFS)
and the seven 2026 TII McEliece solves (accepted provisionally). All other
records are agent-transcribed and unverified. Highlights:
- ECDLP: Certicom challenges through ECC2-109 (2004); secp112r1 on PS3 (2009);
  sect113r2 and a 117.35-bit binary-curve subgroup on FPGAs (2016); BN114 (2017);
  Bitcoin puzzle kangaroo solves #110/#115 (256 V100s), #120-#130 and #135
  (2026-07-28, ~200 GPUs x 5 months by the solver's own account). ECC2K-130
  was never completed.
- Lattices: SVP challenge top dimension 210 (2026-01, GPU sieving); LWE
  challenge largest n=100 at alpha 0.005 (2026-08); 1,010 SVP HoF entries.
- Codes: decodingchallenge.org Goppa track max n=1409 (2023), QC track n=4098
  (2026-09-30, 24 GH200 GPUs); 2026 TII McEliece structural key recoveries.
- Comparators: RSA-250 (~2,700 core-years), DLP-240, and the 2026 GPU-NFS
  records above.
- Normalization adopted (analysis/normalization_method.md; output
  analysis/records_normalized.md). Frontier gaps in log2 work: ECDLP 69 bits
  to P-256; lattices 60-75 bits per sieve call to ML-KEM-512 (121-152 to
  ML-KEM-768); Classic McEliece ~79 bits (mceliece348864, site scale); HQC-128
  ~61 bits (Prange approximation); RSA-2048 ~35 bits. Compute totals over
  record-setting solves are ranges in 2020 core-year equivalents; Bitcoin
  puzzles reported separately.

### How to read the frontier gap

The gap is how much more work it would take to break the deployed parameters
than the largest instance of the same problem that anyone has publicly solved,
written in bits: a gap of g bits means 2^g times more work. Both endpoints are
estimated with the same cost model. Only common size-independent multiplicative
factors cancel; size-dependent costs and omitted terms remain. See the RSA check
in analysis/normalization_method.md for the 35.02-bit leading-GNFS calculation.

Example (ECDLP): the largest public generic solve is a 117-bit curve subgroup
(2016), about 2^58.5 group operations (~6.5 months on up to 576 FPGAs).
Breaking P-256 with the same best-known method (Pollard rho) takes about
2^127.8 operations. The gap is 69 bits: P-256 needs 2^69 (about 6 x 10^20)
times the work of that record.

- It is not a security level. P-256's security level is ~128 bits; the gap is
  the distance between demonstrated public capability and the target, so it
  combines how hard the target is with how far the public has pushed.
- It compares modeled work ratios, with different practical uncertainties.
  ML-KEM-512 (60-75 bits per sieve call) and P-256 (69 bits of group-operation
  work) have similarly sized numerical gaps. RSA-2048's ~35-bit gap is a
  leading-GNFS extrapolation (~35 billion times the work), not a calibrated
  runtime or dollar estimate. Memory and parallelism differ across problems.
- It is the quantity to track over time. The ECDLP frontier has barely moved
  since 2016; the lattice frontier went from SVP-challenge dimension 180 (2021)
  to 210 (2026); factoring jumped in September 2026 with GPU NFS. How fast a
  gap shrinks says how quickly public capability approaches the target.
- It assumes today's best known algorithms. A new idea can collapse a gap
  abruptly (the 2022 SIKE break). Lattice gaps are per sieve call (the full
  attack on ML-KEM-512 adds ~9 bits); the HQC gap uses a cruder cost model and
  is approximate.

## 5. Rubric changes during Phase 1 (v0.3 -> v0.3.4)

Added in response to classifier-reported conflicts, all in pipeline/rubric.md:
CSIDH scope (v0.3.1), hyperelliptic/low-genus Jacobian DLP under ecdlp
(v0.3.2), "unvetted claim" exclusion (v0.3.3), lattice-reduction algorithms
incl. LLL variants are yes/A (v0.3.4). Pass 2 saw v0.3.4 for every
yes/borderline item.

Open rubric gaps reviewers kept raising (labels inconsistent on these; small
counts):
- Hidden-number-problem / ECDSA nonce-leakage lattice attacks.
- Lee-metric and other non-Hamming, non-rank decoding problems (no tag).
- Structural attacks on non-Goppa McEliece variants (tagged sd_goppa).
- DLP on non-standard platforms (class groups of number fields, matrix and
  semigroup DLP): mostly no/borderline with tag other.
- Weak-model DL lower bounds (polynomial/Boolean interpolation of the DL):
  split between yes/F and borderline.
- Low-quality but non-sensational papers (toy factoring heuristics): kept as
  yes at low confidence; handled analytically via vetted/confidence views.
- Duplicate records not caught by title dedupe (same work in two languages).

## 6. Known limitations

- No human validation of labels yet (Phase 0 review sheet still unfilled).
- Abstract caps: pass 1 saw <=1,000 chars (round-1 batches >=0010 and all of
  round 2), pass 2 <=1,500.
- arXiv-only items missing; DBLP thesis coverage is sparse (~12-21 included
  theses per class), so the thesis proxy (PLAN §8 proxy 2) needs a dedicated
  HAL/theses.fr/DART-Europe pass.
- OpenAlex sometimes attaches the wrong abstract to a record.

## 7. Open decisions

1. (Done 2026-10-09) Records normalization adopted.
2. Snowball round 2 (seeds = Phase 1 includes): optional; recall vs. seed
   lists is now ~96-100%, so expected yield is small.
3. Targeted tier-B pass (section 3): optional.
4. Human spot-checks of labels (Phase 0 sheet; a Phase 1 sample sheet can be
   generated).
