# Records normalization: proposal for discussion (SUPERSEDED)

Superseded 2026-10-09 by analysis/normalization_method.md (user decisions on the questions below). Kept as the decision record.

Status: draft for the user, 2026-10-09. Nothing in analysis/ uses these factors yet.

## The problem

Of 326 non-summary records, 89 state CPU core-years, 12 state GPU-years, ~158
give wall time, and the rest give hardware counts or nothing. Units run from
1994 MIPS-years and 1997 Alpha "machine-days" (Certicom) through PS3s, Spartan-6
and Virtex-6 FPGAs, Opteron/Xeon cores, to 2026 RTX 4090 / GH200 GPUs.

## Recommendation: two measures, never one

1. Primary (frontier plots, PLAN §7.3): problem-intrinsic work, log2 of
   operations, with no hardware conversion.
   - ECDLP: log2(group operations or rho iterations) as reported; else
     0.5*log2(n) + log2(sqrt(pi/2)) for a generic rho solve of group order n.
   - Lattices: log2 cost of the solve under one fixed cost model (proposal:
     practical sieving 2^(0.292 d + 16.4) from the G6K/Ducas et al. fits, with
     classical-core-SVP 0.292d reported alongside); SVP challenge dimension
     maps to d directly.
   - Codes: the decodingchallenge.org per-instance complexity (already in
     log2_ops) or the Syndrome Decoding Estimator figure for the paper's instance.
   - Factoring/FF-DLP: L-notation heuristic cost for the size (stated as such)
     plus the authors' own operation counts where given.
   This makes "gap between frontier and deployed target" a clean number per class.

2. Secondary (compute totals, PLAN §7.4): 2020 CPU-core-year equivalents, as a
   low/high RANGE per record, propagated to class totals as a range. Raw
   figures stay in every table.

## Proposed conversion factors (ranges; the main thing to agree on)

| Unit | 2020 core-year equivalents | Basis / caveat |
|---|---|---|
| 1 CPU core-year, 1995-1999 | 0.03-0.06 | single-thread throughput growth |
| 2000-2004 | 0.08-0.15 | |
| 2005-2009 | 0.25-0.40 | |
| 2010-2014 | 0.5-0.7 | |
| 2015-2019 | 0.8-0.9 | |
| 2020+ | 1 | |
| 1 MIPS-year (RSA-129 era) | ~3e-5 | 3.15e13 instr / ~1e18 instr per 2020 core-year |
| Certicom machine-day (500 MHz Alpha) | 1/30-1/15 core-day, then the 1995-99 row | Certicom's own unit |
| 1 PS3-year (Cell, 6 SPEs), ECC rho | 3-8 | Bos et al. SIMD throughput vs. modern core |
| FPGA device-year | prefer iterations x per-iteration core cost | device throughput is workload-specific |
| 1 GPU-year, lattice sieving (2080Ti-4090-A100, tensor cores) | 100-500 | DSvW 2021 / later GPU-sieve speedups vs. CPU G6K |
| 1 GPU-year, ECDLP kangaroo/rho (V100-4090) | 50-200 | per-device jumps/s vs. per-core |
| 1 GPU-year, ISD (cuBJMM etc.) | 20-100 | |
| 1 GPU-year, NFS (2026 GPU CADO-NFS) | use authors' CPU-equivalent where given (RSA-260: ~7,010 core-years for 13.5 GPU-years -> ~520x) | the authors' own estimate |

## Questions for the user

1. Is log2(ops) acceptable as the primary frontier metric, with core-years only
   for totals?
2. Ranges or point values for the conversion table? (Ranges recommended; the
   honest uncertainty is ~2-5x per conversion.)
3. Lattice cost model for log2(ops): practical G6K-fit sieving, or the
   lattice-estimator's default? (Affects how the SVP-challenge frontier compares
   with ML-KEM's ~2^143 classical gate estimate.)
4. Totals scope: frontier-only records, or every hall-of-fame entry (the SVP
   HoF has 1,010 entries; decodingchallenge has ~160)? PLAN §7.4 says every
   entry; that inflates lattice totals mostly via many small solves.
5. Bitcoin puzzle compute (non-academic, interval ECDLP and brute force): in the
   ECDLP total with a flag (PLAN default), or reported only separately?
   It likely dominates ECDLP compute: #135 alone is ~200 GPUs x 5 months
   (~83 GPU-years, roughly 4,000-17,000 core-years by the factor above).
