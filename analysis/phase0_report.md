# Phase 0 pilot report: ePrint-only classification

Date: 2026-10-08. Inputs and outputs are all under this directory; every
number below is reproducible from `data/labeled_final.jsonl` via
`analysis/pilot_counts.py`.

## 1. What was done

1. Harvested the full Cryptology ePrint Archive through its OAI-PMH endpoint
   (`pipeline/fetch_eprint_oai.py`): 28,087 identifiers, 27,249 live records
   after dropping withdrawn stubs. Fields: id, title, authors, ePrint
   category, abstract, dates.
2. High-recall keyword screen (`pipeline/candidates.py`): 4,542 candidates
   (lattice 2,896; code 756; ECDLP 670; comparators 667; overlaps allowed).
   Landmark-paper probe found every tested landmark present on ePrint.
3. Pass 1: Sonnet-class subagents labeled all 4,542 candidates against
   `pipeline/rubric.md` (include / category A-H,S,X / problem tags with
   weights / layer / regime / record / quantum / confidence / reason).
4. Pass 2: Opus-class subagents independently re-labeled every pass-1
   yes/borderline item (1,295) plus a random 10% audit of pass-1 exclusions
   (324 of 3,247), seeing the pass-1 label only as a suggestion.
5. Merge, agreement statistics, attribution to headline classes under the
   policy in `pipeline/attribution.json`, counts, exports.

## 2. Classifier quality

| Statistic | Value |
|---|---|
| Pass-1 vs pass-2 binary include (yes+borderline vs no) | observed agreement 0.94, Cohen's kappa 0.84 |
| Pass-1 vs pass-2 category agreement | 0.90 |
| Audit of pass-1 exclusions | 1 of 324 flipped (est. false-negative rate 0.3%, ~10 missed items in 3,247) |
| Borderline instability | of 373 pass-1 borderline: 190 stayed, 90 to no, 83 to yes |

The exclusion side is reliable. The unstable region is the borderline set,
which is where the rubric needs tightening (section 5). A 176-item human
spot-check sheet, prioritising pass-1/pass-2 disagreements, is at
`analysis/review_sheet.md`.

## 3. Pilot counts (ePrint only, include = yes, categories A-F and H)

Fractional attribution; "touch" counts a paper once per class it touches.

| Class | Fractional | Touch | Distinct authors | pre-2006 | 2006-2016 | 2017-2026 |
|---|---|---|---|---|---|---|
| ECDLP | 108.8 | 130 | 248 | 10.6 | 56.3 | 41.9 |
| MLWE / structured lattices | 177.7 | 300 | 402 | 1.5 | 51.4 | 124.8 |
| LWE plain | 145.8 | 257 | 373 | 0.4 | 35.1 | 110.2 |
| All lattices (union) | 323.5 | — | 446 | — | — | — |
| Syndrome decoding | 112.8 | 130 | 222 | 0.0 | 27.6 | 85.2 |
| Factoring / FF-DLP (comparator) | 170.7 | 190 | 306 | 7.0 | 94.4 | 69.3 |
| Isogeny (comparator) | 35.0 | 35 | 82 | 0 | 0 | 35.0 |
| Multivariate (comparator) | 90.4 | 97 | 140 | 4.0 | 25.7 | 60.7 |

Counting borderline items as included raises every class by 15-30% without
changing the ordering (`analysis/pilot_final_with_borderline.txt`).

Category mix (touch counts): ECDLP A:61 B:20 C:19 D:13 E:7 F:9 H:1;
structured lattices A:151 B:31 C:53 D:48 E:5 F:5 H:7; plain LWE A:165 B:25
C:7 D:46 E:4 F:5 H:5; syndrome decoding A:65 B:9 C:39 D:9 E:4 F:2 H:2;
factoring/FF-DLP A:84 B:10 C:53 D:10 E:20 F:12 H:1.

Layer-2 items (analysis aimed at deployed parameter sets): ECDLP 25,
structured lattices 71, plain LWE 59, syndrome decoding 44, factoring 16.

Quantum items: ECDLP 22, lattices 35, syndrome decoding 10, factoring 12.

Lattice parameter regime (pass-2 tag): pqc 55, fhe 29, both 44, n/a 214.
About a tenth of lattice attack papers are FHE-regime only and should be
down-weighted for ML-KEM relevance.

## 4. Observations

1. **ePrint badly undercounts ECDLP and factoring history.** ePrint starts
   in 1996 and only became the default venue around 2004-2005. The
   formative ECDLP cryptanalysis (MOV 1993, Semaev/Smart/Satoh-Araki 1998,
   GHS 2000-2002, parallel rho, Certicom challenge solves 1997-2004) and the
   NFS lineage are mostly absent. The pre-2006 ECDLP count of 10.6 is a
   floor, not an estimate. DBLP, zbMATH and the Handbook/Galbraith-Gaudry
   reference lists are mandatory for Phase 1, and matter most for exactly
   the class the study is trying to compare against.
2. **MLWE and plain LWE are one workforce.** Author-set Jaccard between the
   two lattice classes is 0.74; between ECDLP and factoring 0.21; every
   other pair is 0.11 or below. The MLWE-vs-LWE split is an attribution
   artefact of the 50/50 rule for generic lattice machinery. Recommend the
   headline report "all lattices" with a sub-line for the handful of
   plain-LWE-specific results (BKW, Arora-Ge, Frodo parameter work).
3. **Syndrome decoding is a separate, smaller community.** 222 distinct
   authors, low overlap with everyone else, and three quarters of its
   output is post-2017. Its structural (C) share is high (39 of 130),
   driven by Goppa/QC key-recovery work.
4. **The ECDLP curve is front-loaded.** Over half of the ePrint-visible
   ECDLP attack work sits in 2006-2016 (the summation-polynomial / Weil
   descent push). 2017-2026 is thinner and partly quantum resource
   estimates. This is the "mature negative consensus" effect anticipated
   in PLAN.md section 9 and must be shown per era.
5. **Records (category E) are dominated by factoring/FF-DLP** (20 on
   ePrint alone) versus 7 for ECDLP, roughly 5-10 for lattices and 4 for
   decoding before 2026. The ECC2K-130 paper (2009/541) is a cost estimate;
   the challenge was never completed, and pass 2 relabeled it D.
6. **A 2026 McEliece key-recovery episode is visible in the data.** Six
   2026 ePrint items target "TII McEliece challenges" with structural
   Goppa key recovery (2026/1232, 1339, 1747, 1778, 1984, 1986, 430), and
   one (2026/1810) is a lower-bound rebuttal of 2026/1747. This is after
   the assistant's training data; it needs human reading before anything
   is concluded from it, but it is exactly the kind of event the records
   track should capture (instance sizes, compute, claimed extrapolation).
7. **Withdrawn or refuted attacks cluster in lattices.** The H list has
   seven lattice entries (Eldar-Hallgren 2021 and its LLL note, "RLWE over
   two-to-power cyclotomics is not hard" 2021, Schnorr's SVP factoring
   2021, the dual-sieve question 2023, Chen 2024, a 2025 quantum-lattice
   rebuttal, HAWK 2026) against one each for ECDLP and factoring. Read
   as evidence that claimed lattice attacks are scrutinised fast, and as a
   count of serious attempts that did not pan out.
8. **Isogeny comparator recall is poor** (nothing before 2017, though
   2016-era SIDH cryptanalysis exists). The keyword patterns were too
   narrow. Low priority since it is a comparator, but fix in Phase 1.

## 5. Rubric and pipeline revisions for Phase 1

- Leakage / side-information attacks ("LWE with hints", "Leaky McEliece",
  NTRU with hints): pass 2 was inconsistent. Rule: include (category D or
  C, flag `leakage`) when the paper models hints abstractly on the problem
  instance; exclude when the contribution is extracting leakage from an
  implementation.
- Add explicit out-of-scope examples: permuted kernel, code equivalence
  (LESS), hidden subset sum, lattice isomorphism (HAWK), group-action
  problems. Several were labeled yes in pass 1.
- Add tag `rsa_variant` for Coppersmith-style attacks on structured RSA
  (small CRT exponents, partial key exposure). They are now counted as
  factoring C and inflate the comparator; they should be separable.
- Record the pass-2 `regime` tag for all lattice items (not just the
  reviewed set) and exclude `fhe`-only items from ML-KEM-relevant counts.
- Attribution: report "all lattices" as the headline and drop the 50/50
  split from headline tables (keep it in the sensitivity analysis).
- Operational: subagents sharing one scratchpad overwrote each other's
  helper scripts; give each reviewer a private subdirectory. Output files
  were verified against batch headers and are intact.
- Cost: pass 1 used about 4.4M subagent tokens for 4,542 items, pass 2
  about 2.0M for 1,619 items. Phase 1 candidate pools from DBLP, arXiv,
  OpenAlex and zbMATH will overlap ePrint heavily; dedupe before
  classifying and only classify new items.

## 6. Deliverables

- `data/eprint.jsonl`: full ePrint metadata, 27,249 records.
- `data/candidates.jsonl`: 4,542 screened candidates with keyword hits.
- `data/labeled_final.jsonl`: all candidates with pass-1 and pass-2 labels.
- `data/export/eprint_included.csv`: 1,203 included (yes + borderline) rows.
- `analysis/pilot_final_report.txt`, `analysis/pilot_final_with_borderline.txt`:
  counts, per-year table, records list, H list.
- `analysis/review_sheet.md`: 176-item human spot-check sheet.
- `pipeline/`: harvester, parser, screen, rubric, batchers, mergers.

## 7. Phase 0 exit criteria

| Criterion (PLAN.md section 6.2) | Status |
|---|---|
| Precision > 0.9 on included set | Not yet measured against a human; pass-1/pass-2 kappa 0.84 suggests it is near but the borderline band needs the spot-check |
| Recall > 0.85 | Audit implies ~99.7% recall relative to the candidate pool; recall of the pool itself vs seed reference lists not yet measured (Phase 2 snowballing) |
| Rubric revised | Revisions listed in section 5, not yet applied |

Phase 0 is complete pending the human spot-check of `review_sheet.md`.
