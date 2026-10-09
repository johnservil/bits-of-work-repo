# Computational records: normalization method and rationale

Status: adopted 2026-10-09 (user decisions on the options in
analysis/normalization_proposal.md, which is kept as the decision record).
Implementation: analysis/records_normalize.py; configuration and sourced
constants: analysis/normalization.json and analysis/normalization_sources.json.
Output: analysis/records_normalized.md, data/export/records_normalized.csv.

## 1. What the records track has to answer

PLAN.md §7 asks two questions of the computational records: how far is the
largest public solve from the deployed parameters (the frontier gap), and how
much compute has been spent (totals). The 338 records span thirty years of
hardware (1994 MIPS-years, 1997 Alpha "machine-days", PS3s, FPGAs, CPU clusters,
2026 GPUs) and four problem families with different natural size units, and
only about a quarter state CPU core-years. Any single conversion to one unit
would carry multi-x uncertainty and would hide which part of a gap is
algorithmic and which is hardware.

## 2. Decisions

| # | Decision (user, 2026-10-09) | Alternative rejected |
|---|---|---|
| 1 | Frontier is measured in log2(operations) on the problem's own cost model; core-year equivalents are used only for compute totals. | One currency (core-years) for everything. |
| 2 | Hardware conversions are low/high ranges, deliberately coarse. | Point estimates. |
| 3 | Lattices: frontier and targets in sieving dimension / BKZ blocksize beta; the gap is converted to log2(ops) as a slope range from the asymptotic exponent to an empirically observed practical exponent. | A single cost model (lattice-estimator gate counts, or a G6K timing fit) applied to both endpoints. |
| 4 | Totals sum record-setting solves only. | Every hall-of-fame entry (PLAN §7.4 original). |
| 5 | Bitcoin-puzzle compute is reported separately from ECDLP totals. | Folded into ECDLP with a flag (PLAN §9 original). |

## 3. Why

1. log2(ops) as the frontier metric. The question a standards reader asks is
   "how much more work than anything done publicly would an attack on the
   deployed parameters take". That is a ratio of work, which log2(ops)
   expresses directly and which does not depend on what hardware the record
   happened to use. Core-years answer a different question (how much was
   spent) and are kept for that.

2. Ranges. Each hardware conversion (e.g. a 2016 FPGA-year or a 2026 GPU-year
   into 2020 core-years) is uncertain by 2-5x and workload-dependent. Point
   values would imply precision we do not have; ranges propagate the honest
   uncertainty into the totals, and order-of-magnitude conclusions survive them.

3. Lattice cost model: native units plus a slope range.
   - Both endpoints must be measured with the same model, otherwise the gap is
     an artefact of mixing models.
   - Measuring both in sieving dimension (frontier: the solver-reported maximum
     sieving dimension of the record SVP-challenge solve; target: the BKZ
     blocksize beta that the primal attack on ML-KEM needs) makes the gap in
     native units model-free: delta-beta.
   - Converting delta-beta to bits of work needs a per-dimension exponent. The
     low end is the asymptotic BDGL exponent 0.292 (NIST's "core-SVP"
     convention). The high end is 0.367, the practical exponent of the GPU
     sieve used for recent records (Ducas-Stevens-van Woerden 2021, Fig. 7(b),
     fit 2^(0.367n - 37.15) s over sieving dimensions 121-140; their measured
     record FLOP counts at sieving dimensions 127-150 give 0.365). Real sieves
     have overheads that grow with dimension, so the asymptotic figure
     understates practical cost at accessible dimensions. Other published
     practical fits (0.31-0.37 for 2021-2025 CPU/GPU sieves) fall inside or at
     the edge of this range (normalization_sources.json).
   - Endpoints: frontier = the solver-reported maximum sieving dimension of
     the record SVP-challenge solve (171 for dimension 210, 2026); targets =
     the refined-primal sieving dimension beta' from the Kyber round-3
     specification, Table 4 (375 / 586 / 829 for ML-KEM-512 / 768 / 1024;
     FIPS 203 parameters are identical). Comparing sieving dimension with
     sieving dimension (not with the BKZ blocksize beta = 413 / 637 / 894)
     keeps the pairing like-for-like.
   - Rejected: the lattice-estimator's gate counts as the model. They are a
     parameter-selection model; no record solve was measured in gates, so the
     frontier endpoint would have to be re-estimated rather than measured. Kept
     as a cited reference value for the targets only.
   - Rejected: a single G6K/GPU timing fit. Fits are calibrated at dimensions
     ~100-190; extrapolating 200+ dimensions turns a slope error of a few
     hundredths into tens of bits.
   - Rejected: fitting the slope to our own record data. We tried: over the 11
     record-setting SVP-challenge solves since 2018 the fit gives about 0.18
     log2 core-years per dimension, below the asymptotic exponent, because GPU
     and algorithmic progress during 2018-2026 is confounded with dimension.
     The fit measures progress, not cost growth.
   - Caveat: the SVP challenge is approx-SVP (norm <= 1.05 GH), not exact SVP,
     and ML-KEM's primal attack needs BKZ with blocksize beta (many SVP calls),
     not one SVP call; the per-sieve gap is therefore a lower bound on the gap
     in total work, by about 2^9 for ML-KEM-512 per the specification.
   - Reference values (cited, not used as the model): spec gate counts 2^151.5
     (+-2^16) / 2^215.1 / 2^287.3; lattice-estimator default model for
     ML-KEM-512 2^143.8; core-SVP 2^118 / 2^183 / 2^256.

4. Record-setting solves only. Hall-of-fame totals are dominated by many small
   repeat solves (1,010 SVP-challenge entries) whose count reflects how easy a
   leaderboard is to enter, not effort against the deployed problem.
   Record-setting solves measure the push on the frontier and are comparable
   across classes.

5. Bitcoin puzzles separate. They are non-academic, mostly unpublished
   (compute known for 3 of 12 solves), and solve interval-ECDLP (or brute force
   on hash160), not the full ECDLP on a random point. Folding them in would
   make ECDLP totals depend on hobbyist disclosure and on a different problem.
   They are still reported, because they show that generic-attack engineering
   at the 2^65-2^70 scale is routine.

## 4. Per-class frontier conventions

- ECDLP: log2(ops) = log2(sqrt(pi n / 4)) group operations (SafeCurves:
  0.886 sqrt(l) additions; 2^127.8 for P-256 / secp256k1) for a generic rho
  solve of group order n; reported iteration counts override when given.
  Weak-curve and structure-exploiting solves (GHS, Koblitz/Frobenius, BN
  automorphism) are listed but excluded from the generic frontier.
- Lattices: as above (section 3.3).
- Codes: one model on both endpoints.
  - Goppa / Classic McEliece: decodingchallenge.org's own complexity figure
    (length n times Dumer's workfactor, computed with CaWoF) for the record
    instance (n=1409, 2^63) and for the track's instance nearest to
    mceliece348864 (n=3471, 2^142): gap ~79 bits. Advanced-ISD estimates for
    mceliece348864 (Syndrome Decoding Estimator: 2^158.6 with square-root
    memory cost, 2^141 with constant memory cost) are cited for reference.
  - QC / HQC: no published estimator value exists for the record instance, so
    both endpoints use Prange iteration counts (record n=4098: 2^64.7;
    HQC-128: 2^132.4 minus ~7 bits quasi-cyclic discount): gap ~61 bits,
    approximate. HQC-128 advanced-ISD estimate 2^145 (constant memory) cited.
    Prange overstates absolute costs, but the overstatement largely cancels
    in a same-model gap; at the frontier it agrees with the site's figures
    within ~1.3 bits.
- Factoring: the leading L_N[1/3, (64/9)^(1/3)] GNFS expression, with o(1)
  dropped, applied to both endpoints. Its absolute values are cost-model
  indices, not calibrated operation counts. Only a common size-independent
  multiplicative factor cancels; the exponent coefficient and size-dependent
  corrections do not. RSA-2048's 112-bit NIST security strength is a separate
  convention and is not used as an endpoint in this subtraction.

### RSA-896 to RSA-2048 check (2026-10-09)

For a b-bit modulus, set N approximately 2^b and evaluate:

    F(b) = (64/9)^(1/3) * (b ln 2)^(1/3) * [ln(b ln 2)]^(2/3) / ln 2
    estimated work ratio = 2^[F(target_bits) - F(record_bits)]

| Modulus bits b | F(b), leading GNFS index | Gap to 2048 | Work ratio to 2048 |
|---|---:|---:|---:|
| 896 | 81.8596 | 35.0242 bits | 3.49 x 10^10 |
| 1024 | 86.7661 | 30.1177 bits | 1.17 x 10^9 |
| 2048 | 116.8838 | 0 | 1 |

Thus the ~35-bit figure is arithmetically correct under this model. GNFS
scales subexponentially in modulus size; doubling the modulus does not double
its security exponent. A 35-bit gap still means roughly 35 billion times as
much modeled work. Decimal places above document the arithmetic, not predictive
precision.

As a consistency check, the [RSA-260 primary write-up](https://cognition.com/blog/factoring-rsa-260)
gives a roughly billion-fold RSA-1024-to-2048 ratio and a 91.2-billion-fold
RSA-260-to-2048 ratio. Those are the same kind of GNFS extrapolation, not
independent measurements at 2048 bits. The [RSA-896 account](https://saweis.net/posts/rsa-896.html)
reports a GPU implementation advance rather than an asymptotic algorithm change.

The practical ratio is uncertain: the omitted terms, polynomial selection,
sieving/linear-algebra balance, memory, communication and machine efficiency
can vary with size. There is no calibrated error bar here, and no claim that
35.02 is an accurate wall-time or dollar exponent. The [NIST 112-bit category](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf)
is neither F(2048) nor a reason to compute 112 - F(896). Keep security-strength
categories, leading GNFS indices, and measured hardware time distinct.

## 6. How to read the gap

The gap is how much more work it would take to break the deployed parameters
than the largest instance of the same problem that anyone has publicly solved,
written in bits: a gap of g bits means 2^g times more work. Both endpoints are
estimated with the same cost model. A common size-independent multiplicative
factor cancels, but size-dependent effects and omitted terms remain. The ratio
is a model-based work extrapolation, not a measured resource gap.

Example (ECDLP): the largest public generic solve is a 117-bit curve subgroup
(2016), about 2^58.5 group operations (~6.5 months on up to 576 FPGAs).
Breaking P-256 with the same best-known method (Pollard rho) takes about
2^127.8 operations. The gap is 69 bits: P-256 needs 2^69 (about 6 x 10^20)
times the work of that record.

- It is not a security level. P-256's security level is ~128 bits; the gap is
  the distance between demonstrated public capability and the target, so it
  combines how hard the target is with how far the public has pushed.
- It permits a coarse comparison of modeled work ratios across problems.
  ML-KEM-512 (60-75 bits per sieve call) and P-256 (69 bits of group-operation
  work) have gaps of similar numerical size; RSA-2048 has a smaller leading-GNFS
  gap (~35 bits). Different memory, parallelism and model assumptions prevent
  treating these as equally calibrated practical distances or security levels.
- It is the quantity to track over time. The ECDLP frontier has barely moved
  since 2016; the lattice frontier went from SVP-challenge dimension 180 (2021)
  to 210 (2026); factoring jumped in September 2026 with GPU NFS. How fast a
  gap shrinks says how quickly public capability approaches the target.
- It assumes today's best known algorithms. A new idea can collapse a gap
  abruptly (the 2022 SIKE break). Lattice gaps are per sieve call (the full
  attack on ML-KEM-512 adds ~9 bits); the HQC gap uses a cruder cost model and
  is approximate.

## 7. Resulting frontier gaps (analysis/records_normalized.md)

| Class | Public frontier | Target | Gap (log2 work) |
|---|---|---|---|
| ECDLP (generic) | 117.35-bit subgroup, 2016 (2^58.5) | P-256 (2^127.8) | 69.3 |
| ECDLP (Bitcoin puzzle, interval, separate) | 134-bit interval, 2026 | P-256 | ~60 (different problem) |
| Lattices | sieving dim 171, 2026 | ML-KEM-512 / 768 / 1024 (beta' 375 / 586 / 829) | 60-75 / 121-152 / 192-241 per sieve call (+~9 for the full attack on ML-KEM-512) |
| Codes, Goppa | n=1409, 2023 (2^63) | mceliece348864 | ~79 |
| Codes, QC | n=4098, 2026 | HQC-128 | ~61 (Prange approximation) |
| Factoring | RSA-896, 2026 | RSA-2048 | ~35 (~35 billion x; leading GNFS heuristic) |

## 5. Known limitations

- Conversion factors are coarse by design (decision 2).
- Only 10 of 338 records are human-verified; derived compute uses heuristic
  parsing of hardware strings ("how" column records the derivation).
- Lattice gap is per SVP call (see 3.3 caveat).
- Codes: decodingchallenge states no memory-cost model; the QC gap is a
  Prange-based approximation (no estimator run on the record instance).
- Unresolved source items are listed under "unresolved" in
  normalization_sources.json.
