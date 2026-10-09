# ECDLP records: agent notes (2026-10-08)

33 record files. All have `verified: false`.

## Conventions used
- `instance_size` is log2 of the prime subgroup order n, rounded to 2 decimals, where n
  was available (Certicom appendix, papers). So ECC2-79 is 78.0 and secp112r1 is 111.78.
  Where only a nominal size was published (BN114, BN116), the nominal size is used.
  For interval-ECDLP it is log2 of the interval width (puzzle #N -> N-1).
- `reported_core_years` is filled only when the source gives a CPU-time figure. That
  includes Certicom "machine-days on a 500 MHz Alpha" (divided by 365.25), the Athlon
  single-core-equivalent years for ECC2-109, and core-days or CPU-hours in papers. Derived
  figures such as GPUs x months or cores x months are in `notes` only.
- `date` is the solve or submission date where known. Otherwise it is the announcement
  date, or the first ePrint version (marked in notes).

## Seed list (records/_eprint_seed_ecdlp.txt) dispositions
- 2014/368, 2015/143, 2016/382: recorded. 2016/382 covers two records: sect113r2 and the
  117.35-bit curve over F_2^127.
- 2016/507 (MNT-170): recorded with problem FF-DLP, because the work is NFS in F_{p^3}.
  Consider moving it to the comparator class.
- 2011/020 (Joux-Vitse F_{p^6}) and 2021/676 (GLS+GHS over F_2^155): recorded, with
  structure_exploited true. The 2021 paper also documents the earlier Velichka-Jacobson-
  Stein solve of the same curve (ePrint 2011/098), which is recorded from that secondary
  table.
- 2001/041 (Jacobson-Menezes-Stein, F_2^155): not recorded. The abstract only says the
  instance "can be solved" with modest resources, and the 2021 paper treats JMS-style
  timings as estimates. I could not confirm a completed solve. Open question.
- 2010/090 (676-bit GF(3^{6n})) and 2012/345 (GF(3^{6*97}), eta_T pairing): not
  recorded. These are pure finite-field DLP records in pairing target groups and belong
  to the comparator FF-DLP track.

## Not completed / skipped
- ECC2K-130 (Bailey et al. 2009, ePrint 2009/541): never completed as far as I can find.
  The expected cost was 2^60.9 iterations, about 2^35.63 DPs. Their estimates were one
  year on 4200 Cell CPUs, or 2 years on 1520 CPUs. The Certicom document (2009-11-10)
  lists it as open, and Zhang's 2019 CAB Forum slides still list all 131-bit challenges as
  open. ecc-challenge.info shows the run as "ongoing" with no completion. One secondary
  source (arXiv 2508.14011) claims it was broken; I treat that as an error.
- Bitcoin puzzles #65-#100 (every 5th; public keys exposed in 2019): solved, but no
  resources are published and they are small. Not recorded.
- Bitcoin puzzle #71: unsolved as of the tracker data I read (deposits through
  2026-09-29). #140 to #160 are unsolved.

## Unconfirmed / weak spots
- ePrint, IACR archive, Springer, HAL and infoscience PDFs were blocked (403, 429 or bot
  wall), so these were not read directly:
  - Wenger-Wolfger 2014 and 2015: iteration totals; the 47-day and 82-day actual runtimes
    come from Wikipedia.
  - Kusaka et al. 2017: 2000 cores and 6 months come from Wikipedia and abstract snippets.
  - Bos et al. IJACT 2012: I used their SHARCS 2009 paper from joppebos.com instead.
- BN116 (Manabe et al. 2023): only the OpenAlex abstract ("success report") was read.
  Resources are unknown.
- Bitcoin puzzle #105 solver and method are unknown. #120, #125 and #130 are attributed
  to RetiredCoder by the agntn/puzzles tracker and his GitHub profile; no compute is
  published. The #135 figure ("about 5 months on 200 GPUs") is his own bitcointalk post
  of 2026-07-28. The GPU model is not stated.
- Solvers of the brute-force puzzles (#64 and #66 to #69) are unnamed, and no compute is
  published.
- Certicom ECCp-79 iteration count: the doc's two tables disagree (1.4e12 vs 1.4e11). I
  used 1.4e12, which matches Sec. 6.1.7.
