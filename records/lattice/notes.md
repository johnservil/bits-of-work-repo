# Lattice computational-records track: notes

Built 2026-10-08/09 by an agent. Every record has `verified: false`. Fields follow
`records/README.md`. Raw pages were read with curl/WebFetch (read-only). They were
parsed with throwaway stdlib scripts in `_scratch/`, which was deleted afterwards as
instructed. To keep raw pulls, re-fetch them into `data/raw/latticechallenge/` (see
"Re-pull" below).

## Contents (169 YAML files + 5 CSVs)

| group | files | selection rule | source |
|---|---|---|---|
| `svpc_*` TU Darmstadt SVP Challenge | 41 | 36 max-dimension progression entries, plus every entry with dim >= 186 (187, 188, 192), the CPU-only Zhao-Ding-Yang 183 (9.1 core-years stated), and the AH-BKZ 163 (seed paper 2026/1876) | svp-challenge/halloffame.php |
| `ideal_svp_*` Ideal Lattice Challenge, SVP HoF | 21 | 19 progression entries, plus AH-BKZ 164 (2026/1876) and an 8x Titan X GPU Gauss-sieve entry at dim 130 (2016) | ideallattice-challenge/svphalloffame.php |
| `ideal_apxsvp_*` Ideal Lattice Challenge, approx-SVP HoF | 18 | progression entries | ideallattice-challenge/alphasvphalloffame.php |
| `latchal_*` original Lattice Challenge (Buchmann-Lindner-Rückert-Schneider) | 21 | progression by submission id (ids 1-72 have no date) | halloffame.php + details.php?id=N |
| `lwechal_*` TU Darmstadt LWE Challenge | 45 | every solved (n, alpha) cell. Each cell is solved once, so every entry is a cell record; 43/45 were on the solved-region Pareto frontier when solved | lwe_challenge/details.php?n=..&alpha=.. |
| `ntru_si_*` Security Innovation NTRU Challenge | 8 | full progression N=107..173 (2015) and N=181 (2023) | Wayback copies of the SI "Solved Challenges" page and answers PDF; Mårtensson 2016 thesis; ePrint 2023/582 |
| paper-only solves | 10 | seed-list items with a concrete instance (see disposition below) | ePrint abstract pages |
| `*_hof_summary.yaml` | 5 | one per hall of fame (SVP, LWE, ideal SVP, ideal approx-SVP, Lattice Challenge). These have extra `summary_*` keys beyond the README schema and a leading `#` comment | |
| CSVs | 5 | `svp_challenge_hof.csv` (1010 rows), `lwe_challenge_hof.csv` (45), `ideal_lattice_svp_hof.csv` (100), `ideal_lattice_approxsvp_hof.csv` (236), `lattice_challenge_hof.csv` (238) | full HoF tables; one e-mail address redacted |

## Key facts

- **The SVP Challenge is approx-SVP.** An entry needs norm < 1.05·GH(L) (the formula is in an HTML comment on index.php) on Goldstein-Mayer random lattices, or a shorter vector in a dimension that is already solved. It is not proven exact SVP, so all `svpc_*` files use `problem: "approx-SVP"`. The HoF has 1010 entries over 149 distinct dimensions (2010-05-11 to 2026-10-08). Top entry: dim 210, Ding & Zhao, bgj3-gpu, dated 2026-01-01 (printed "2026-01-1"), 56.05 d preprocessing + 22.31 d sieve/lift; GPU count not stated on the HoF. Dim 200 (2025-03-04): 8x RTX 4090, about 31 d.
- Progression of the record: 112 (Chen-Nguyen 2010), 120 (Kuo-Schneider, GPU/EC2 2011), 126 (Chen-Nguyen 2013), 150 (Kashiwabara-Teruya, ~394 d of clusters, 2017), 155 (G6K CPU, 2018), 180 (Ducas-Stevens-van Woerden, 4x RTX 2080 Ti, 51.6 d, 2021-02), 186 (L. Wang-B. Wang, 4x A100, 2023-07), 190 (Y. Sun-S. Chang, 7x RTX 4090(D), ~4 months, 2024-07), 200 (Zhao-Ding, 2025-03), 210 (Ding-Zhao, 2026-01). In 2026 so far: Bai et al. 187 and 192 (8x RTX 4090; not max-dimension records) and K. Matsuoka BGJ-Sieve-GPU entries at dims 160 and 164 (not recorded as files).
- **LWE challenge.** 45 cells solved. Largest n = 100 at alpha 0.005 (J. Ding, 2026-08-10, 419.7 RTX-4090-days). Largest alpha = 0.050 at n = 40 (J. Ding, 2026-07-21; the HoF says 152 RTX-4090-days, but an erratum on another entry corrects this to 85). From the toy file format: m = n^2 samples, q prime near n^2, sigma = alpha·q. The page banner says some instances were "bugged/unbreakable" and are being regenerated; the solved cells are not affected as far as the page says.
- **Original Lattice Challenge.** Top dim 1100 (Yao Sun, 2024-08-08). The early Gama-Nguyen entries (500-725) are dated "2008-12", an upper bound from a 2008-12-02 Wayback capture. The Chen-Nguyen dim 750 entry (id 63) is dated "2011-07", an upper bound. No resource data is published for this challenge.
- **Ideal SVP HoF.** Top dim 180 (Lin Wang et al., 2024-07-16, 8x RTX 3090, ~24 d). `structure_exploited` comes from the HoF "Using Ideal Structure" column. **Ideal approx-SVP HoF**: top dim 796 (Zhao-Ding-Yang 2024, CPU-only, 1.68 core-years). The approx threshold formula is only an image and was not transcribed.
- **NTRU (Security Innovation).** #1-2 (N=107, 113) were solved by "Nick H." (only a first name and initial are given). #3-7 (N=131..173) were solved by Ducas and Nguyen: N=163 took ~41 core-days and N=173 ~290 core-days, on 2.53 GHz cores, using BKZ 2.0 + BDD pruned enumeration. All seven were already solved in the 2015-09-11 Wayback capture, so they are dated "2015-09" (upper bound). N=181 was solved by Kirshanova-May-Nowakowski, ePrint 2023/582, in ~20 core-years. No later NTRU challenge solve was found.

## Seed list (`_eprint_seed_lattice.txt`) disposition

| ePrint | disposition |
|---|---|
| 2013/388 | linked as paper on `ideal_svp_d128_20130411_ishiguro` (~30,000 CPU-h) |
| 2013/470 | NOT written: multivariate (HLY) scheme broken via an easy-LWE reduction (~1 and ~3 days). Belongs in comparator/multivariate |
| 2014/880 | `ideal_svp_d128_2014_bos_naehrig_vandepol` (re-solve, <9 d on 1024 cores) |
| 2015/041 | `svp_d96_2015_mariano_laarhoven_bischof` |
| 2015/176 | `lwe_n350_2015_laine_lauter` (weak large-q regime) |
| 2015/552 | `lwe_n128_binary_2015_kirchner_fouque` |
| 2018/044 | linked on `svpc_d134`..`svpc_d150` Kashiwabara-Teruya entries |
| 2018/741 | `lwe_galbraith_binary_256x400_2017_may_herold` |
| 2018/966 | `mrlwe_bdd16384_2018_bootland_castryck_vercauteren` |
| 2019/089 | linked on `svpc_d153`, `svpc_d155`, and the 2018-2019 G6K LWE cells |
| 2020/230 | `mintru_smallest_2020_lee_wallet` |
| 2020/539 | NOT written: small-secret variants of Darmstadt LWE instances; the abstract gives no concrete solve/resource figures |
| 2021/141 | linked on `svpc_d157`..`svpc_d180`. 2022 LWE cells by the same team are linked with an "assumed" note |
| 2022/239 | linked on `ideal_apxsvp_d656_20210831_zhao`. Discrepancy: the abstract says 380 thread-hours, the HoF says 1400 core-hours |
| 2023/582 | `ntru_si_n181_2023_kirshanova_may_nowakowski`, `ntru_hps171_2023_kirshanova_may_nowakowski` |
| 2024/1229 | `kyber_sparse_kappa2_2024_wenger_et_al` (sparse-secret toy Kyber, 28-36 h) |
| 2024/366 | NOT written: Partial-Vandermonde knapsack (ideal-SIS variant, a 2^-19 weak-key fraction, ~30 h / ~17 h). Not an encryption assumption class in the taxonomy |
| 2024/443 | `lwe_sparse_binary_n1024_2024_nolte_et_al` (compute null; the abstract has no timings) |
| 2024/739 | linked on `svpc_d183_20240504_zhao` (CPU 30 d, 9.1 core-years) |
| 2026/1593 | NOT written: HAWK-256 key recovery "in a few hours on a single server". HAWK is a signature/LIP scheme, not encryption. Could be added if signatures are in scope |
| 2026/1876 | `svpc_d163_20260315_hashimoto`, `ideal_svp_d164_20260316_hashimoto` (per-dimension norm records, not max-dimension) |
| 2026/366 | NOT written: claims "several new records" on the Wenger et al. S&P'25 sparse-LWE benchmark, 17-114x faster than KKN+26. The abstract has no instance/resource numbers. Needs the PDF |

Also checked but not written:
- 2020/707 (Albrecht-Bai-Fouque-Kirchner-Stehlé-Wen): asymptotic enumeration result with simulations only, no record computation.
- 2022/468 and 2022/1343 (Wang/Xia et al.): speedups on LWE cells. 2022/1343 is linked on the cells it names.
- 2016/146 (Aono-Wang-Hayashi-Takagi progressive BKZ): linked on the ideal approx 500-652 entries.
- 2025/1990 (Pulles-Vié GPU primal hybrid on the WSM+25 sparse benchmark): no numbers in the abstract.
- 2026/177 (Oracle-MLWE neighbourhood attack): non-standard assumption.
- No "TII lattice challenge" was found; TII ran McEliece challenges only.

## Conventions and caveats

- `reported_core_years` is filled only when the source states CPU/core time (core-hours/8766, core-days/365.25). Cluster "N cores x D days" figures are left in `raw_compute`/`wall_time_days`, not multiplied out. `gpu_years` is filled only for stated GPU-days (the Ding LWE entries). `wall_time_days` sometimes sums the stated phases; such files say so in `notes`.
- HoF free-text resource notes are self-reported by contestants and unreviewed. Some are ambiguous: "total time" vs wall, threads vs cores, seconds without a unit.
- `instance_size`: lattice/challenge dimension for SVP-type entries; secret dimension n for LWE; ring degree N for NTRU (lattice dimension 2N).
- Paper links marked "assumed" or "unconfirmed" in notes were inferred from same team/software/date, not stated on the HoF.
- ePrint PDFs returned 403 to automated fetch, so paper-derived fields come from abstracts only. The arXiv HTML of 2408.00882 was used for the 2024/1229 hardware.
- Confidence: 0.85 for HoF entries with a resource statement, 0.75 without, 0.6-0.8 for Wayback/thesis-derived NTRU entries, 0.5-0.75 for abstract-only paper records.

## Re-pull (for data/raw)

- `https://www.latticechallenge.org/svp-challenge/halloffame.php` (mixed UTF-8/cp1252; resource notes are in `<tr title=...>`)
- `.../ideallattice-challenge/svphalloffame.php`, `.../ideallattice-challenge/alphasvphalloffame.php`
- `.../halloffame.php`, `.../details.php?id=1..236`
- `.../lwe_challenge/halloffame.php`, `.../lwe_challenge/details.php?n=N&alpha=A`
- Wayback: `20160310143833` (SI solved-challenges.html), `20151229220714` (SI answers PDF), `20081202135127` (latticechallenge.org root)
