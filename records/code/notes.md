# Code-based records track: notes (harvest 2026-10-08/09)

All files follow `records/README.md`. Every record has `verified: false`. Raw
pulls and generator scripts are in `_scratch/` (`progression.py`, `gen_dc.py`,
`gen_manual.py`, `common.py`). To regenerate, run from the repo root:
`python3 -I records/code/_scratch/progression.py` (run it inside `_scratch/`), then
`python3 -I records/code/_scratch/gen_dc.py` and `.../gen_manual.py`.

## Inventory

- `dc_<track>_n<N>.yaml` / `dc_low_weight_w<W>.yaml`: 79 decodingchallenge.org
  record-progression entries (SD 19, Goppa 16, QC 19, large-weight 10,
  low-weight 15).
- `dc_<track>_summary.yaml` (5): one summary per track. Each is marked
  "SUMMARY FILE" in its notes and duplicates the latest progression record, so
  leave these out of counts.
- `dc_<track>_hof.csv` (5): the full hall of fame per track, with 62/28/28/25/21
  rows and per-record hardware, runtime, comments and site complexity.
- 18 hand-transcribed records: BLP 2008, two LPN records, nine TII challenge
  records plus `tii_keyrec_summary` (also a SUMMARY FILE), the CFS m=16 key, and
  three structural breaks of proposed parameters (RM-McEliece 2013, QD/QM 2014,
  QA-SD PCG 2025).

## decodingchallenge.org conventions

- Source: the hall-of-fame page of each track plus every `/<track>/record/<id>`
  page (164 pages fetched). The hall of fame lists the first ten solvers per
  instance.
- Progression rule: sort entries by date and keep each one that raised the
  track's max n (for low-weight, each one that lowered the weight). Entries by
  the same solver on the same day are merged into the best one, so a batch such
  as Lequesne's ten Prange solves on 2019-07-22 becomes a single record.
- `log2_ops` for dc records is the site's own per-instance tooltip ("indication
  of complexity"). It is not a figure from the solver. For QC the tooltip is
  keyed by w. Low-weight has no tooltip, so its `log2_ops` is null.
- `reported_core_years` is filled only when the page gives CPU or core time
  ("CPU days", "core-days", "CPU time"). These are converted at /365.25 for days
  and /8766 for hours. "CPU days" may mean hardware threads.
- `wall_time_days` comes from the "Runtime" field when that field does not say
  CPU time. Many runtimes do not say whether they are wall or CPU time.
- Problem labels: the Goppa track is `SD-Goppa`, but its instances are random
  parity-check matrices with McEliece-like rate and weight, not actual Goppa
  codes. Large-weight is ternary SD. Low-weight (codeword finding, n=1280) is
  labeled `SD` because README has no LWC category.
- `structure_exploited: true` only for QC entries that use DOOM or ring folding.
- Two recent entries to note: QC n=4098 by Saarinen on 2026-09-30 (24 GH200, 24.5
  GPU-hours, no paper found), and an SD n=520 entry by Lucien Pech on 2026-10-03.
  The n=520 entry is not a progression record.
- Goppa n=1347 (Bernstein, 2023) was enriched from isd.mceliece.org/1347.html.
  The source gives 2^41.7 iterations at about 2.3M cycles each. My own derived
  estimate of about 115 core-years is in the notes field only.

## TII McEliece challenges: what was actually solved

- The challenge ran from 2023-05-09 to 2024-05-08, with winners announced
  2024-05-30. Track 1B is key recovery: 206 public keys with labels 22-255. A label
  is round(bitcomplexity) from `key_rec_instances`. I mapped labels to (n,k,t,m)
  by checking matrix dimensions in the public key files, and the 2026 papers'
  stated parameters match: TII-254 = (223,127,12,8), TII-253 = (214,142,9,8).
- Labels are not security levels. The instances have artificially small t (2-24)
  and rates up to ~0.9. Bernstein disputed this in May/June 2023, and the Classic
  McEliece team note of 2026-06-23 shows 2008 ISD decrypts at (482,7) in 0.17 s.
- Results by 2024: the best generic result was TII-83 by Panny (support-splitting
  brute force, about 1471 core-days). The best algebraic result was TII-68 by
  Mora. The Track 2A message-recovery winner reached about 60 bits with BLP Stern
  ISD. Track 2B was unbroken.
- 2026 results are all structural key recovery, with no generic ISD:
  - BLT 2026/430, March: up to 210.
  - Briaud et al. 2026/1232, June 10: TII-248 in 64000 s with >700 GB. They also
    broke a CFS key in 14 h.
  - Hemmert 2026/1339, June 29: 32 labels from 83 to 248, keys on GitHub.
  - Saarinen HOVER 2026/1778, July: 129, 213, 240, 246, 252 in minutes to hours.
  - Weis 2026/1984, Aug 18: 253, about 2x700 core-hours (secondary sources).
  - Vedenev 2026/1747, Aug 20: 173, 249 and 253. No keys located.
  - Saarinen 2026/1986, Sep 8: 254, with ≥27.2 GH200 GPU-hours.
  - TII-255 (n=249, t=24) is unsolved as far as found.
- Organizer confirmation: none found. The HeroX leaderboard has not changed since
  the 2024 close and still shows every label above 83 as "Available to Solve".
  The verification that exists is public: Hemmert and Saarinen publish keys and
  verifiers, and Saarinen's keys pass the official `check_solution_track2.sage`
  according to his repo (I did not run it).
- 2026/1810 (Apon) argues a lower bound against the cost of Vedenev's method for
  Classic McEliece parameters (>2^1500 for mceliece8192128). It does not dispute
  the toy TII solves, so it has no record file.
- Context only, not records: GIJS 2026/1630 (quasipolynomial distinguisher),
  Saarinen 2026/1786 (cost model), and the BSI advisory of 2026-10-01 against new
  Classic McEliece deployments (postquantum.com, 2026-10-02).

## Uncertainty and gaps

- ePrint PDFs are behind a Cloudflare challenge, which I did not bypass. Details
  beyond the abstracts therefore come from author GitHub repos, the Classic
  McEliece team note, decodingchallenge pages, or search-engine summaries. The
  last of these are marked "unconfirmed" with lower confidence. Affected fields:
  - EMZ22 CPU-years (5 / 22): snippet only.
  - Narisada 1409 hardware.
  - Hemmert per-instance timings: quoted from Saarinen.
  - Weis 700 core-hours.
  - WS21 LPN instance: confidence 0.3.
  - BLT instance list: conflicting.
- BLP 2008: the 8000 core-days figure is from Lange's press page. k=524 is the
  standard parameter and was not read on the page.
- `academic`: null where affiliation is unknown (Tinarelli, Chae/Jeong, Meyer,
  Bossard, Usatyuk, Run Timerr). Industry research labs (KDDI Research,
  Anthropic) are set to true.
- Not covered: rank-metric records (none found incidentally) and further LPN
  records (Bogos-Tramer-Vaudenay 2016, Dissection-BKW 2018). In the Goppa
  track, no solve beyond n=1409 exists as of 2026-10-08.
- `2022/1329` (QC-3138), `2024/393` (Goppa-1409, QC 3366-3846, LW 204-210),
  `2021/1634` and `2020/869` are attached as `paper` on the corresponding dc records
  rather than as separate files, to avoid double counting.
