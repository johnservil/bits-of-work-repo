"""Hand-transcribed code-based records outside the decodingchallenge progression."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import write, cy_from_days, cy_from_hours

EP = 'https://eprint.iacr.org/'
HEROX = 'https://www.herox.com/TIIMcElieceChallenges/leaderboard'
TIISITE = 'https://crowdchallenge.tii.ae/mceliece-challenges/index.php'
TIIREPO = 'https://github.com/ElenaKirshanova/tii_decoding_challenge'
PARAMS = 'https://raw.githubusercontent.com/ElenaKirshanova/tii_decoding_challenge/main/key_rec_instances'
SAAR = 'https://github.com/mjosaarinen/tii-solved'
HEMM = 'https://github.com/tobhem/key-recovery-mceliece-tii-solutions'
CMNOTE = 'https://classic.mceliece.org/mceliece-610-20260623.pdf'
TIICONF = ('TII/HeroX confirmation: none found; HeroX leaderboard (static since the May 2024 close) still lists '
           'every Track 1B label above 83 as "Available to Solve". Keys are publicly checkable against the official public keys.')
LABEL = ('TII label = round(bitcomplexity) from the organizers\' key_rec_instances file (a brute-force/support-splitting '
         'estimate, disputed by Bernstein 2023 and the 2026 papers); labels are not security levels.')

recs = []

recs.append(dict(
    id='blp2008_mceliece_1024_50', problem='SD-Goppa',
    instance='original McEliece 1978 parameters (n=1024, k=524, t=50) challenge ciphertext',
    instance_size=1024, method='improved Stern ISD (Bernstein-Lange-Peters 2008)', structure_exploited=False,
    hardware='several dozen computers: TU/e C4 and SANdpit clusters, CWI, Loria, DCU/ICHEC, NTU, UIC',
    raw_compute='decrypted a challenge ciphertext in 8000 core-days', reported_core_years=cy_from_days(8000),
    date='2008-10', solvers=['Daniel J. Bernstein', 'Tanja Lange', 'Christiane Peters'], academic=True,
    extrapolation='paper proposes new McEliece/Niederreiter parameters for standard security levels accounting for the improved attack',
    paper='2008/318', source_url='https://www.hyperelliptic.org/tanja/press/mceliece.html',
    other_urls=[EP + '2008/318', 'https://isd.mceliece.org/1347.html'], confidence=0.85,
    notes='Announced at PQCrypto 2008 (Cincinnati, Oct 2008); press release 2008-10-20. Paper abstract estimate: 1400 days on one 2.4 GHz Core 2 Quad or 7 days on 200 CPUs. "A lucky computer in Ireland" found it. instance_size/k/t from the classical McEliece parameters (n=1024,t=50 confirmed by isd.mceliece.org/1347.html; k=524 standard value, not read on the source page).'))

recs.append(dict(
    id='ekm2017_lpn_k243', problem='LPN', instance='LPN k=243, tau=1/8', instance_size=243, instance_size_unit='dim',
    method='Well-Pooled Gauss / ISD-based LPN solver with low memory (Esser-Kuebler-May)', structure_exploited=False,
    hardware='64 threads', raw_compute='15 days on 64 threads', wall_time_days=15.0, date='2017-02',
    solvers=['Andre Esser', 'Robert Kuebler', 'Alexander May'], academic=True,
    extrapolation='k=512, tau=1/8: ~97-bit classical / ~70-bit quantum with limited memory; tau=1/sqrt(k): 80-bit classical for k>=2048',
    paper='2017/078', source_url=EP + '2017/078', confidence=0.8,
    notes='CRYPTO 2017. Method name "Well-Pooled Gauss" is from memory of the paper, not the abstract (abstract: Gaussian elimination extended with ISD techniques, optionally BKW hybrid). 64 threads x 15 days ~ 2.6 thread-years (derived).'))

recs.append(dict(
    id='ws2021_lpn_codedbkw', problem='LPN', instance='largest LPN parameters reported to date (exact k, tau unconfirmed)',
    instance_size=None, instance_size_unit='dim', method='memory-constrained Coded-BKW', structure_exploited=False,
    raw_compute='2^39 bits of memory (abstract); unconfirmed: n=150, tau=0.25 in < 5 h on 80 cores per a secondary citation',
    date='2021-07', solvers=['Thom Wiggers', 'Simona Samardjiska'], academic=True, paper='2021/962',
    source_url=EP + '2021/962', other_urls=['https://github.com/thomwiggers/lpn'], confidence=0.3,
    notes='ISIT 2021. PDF blocked (Cloudflare); instance and time come only from a search-engine summary of a later paper citing [WS21] - treat as unconfirmed.'))

recs.append(dict(
    id='tii_1b_mora_2024', problem='SD-Goppa',
    instance='TII McEliece Track 1B key recovery, best = TII-68 (n=53, k=41, t=2, m=6); also 22-66',
    instance_size=53, method='algebraic: matrix code of quadratic relations (Couvreur-Mora-Tillich 2023 / Mora 2023), Pfaffian modeling; FGOPT degree-2 hybrid for some',
    structure_exploited=True, hardware='Intel Xeon E7-4850 v3',
    raw_compute='per-instance runtimes 3 s to 2 d 6 h (TII-66: 2 d 6 h); TII-68 runtime not listed', date='2024-05',
    solvers=['Rocco Mora'], academic=True, challenge='TII McEliece', source_url=HEROX,
    other_urls=['https://tii.ae/news/tii-mceliece-encryption-challenges-winners-announced', PARAMS], confidence=0.7,
    notes='Solved before the 2024-05-08 deadline (exact dates not shown). Mora won the Track 1A (theory) prize. ' + LABEL))

recs.append(dict(
    id='tii_1b_panny_83_2024', problem='SD-Goppa', instance='TII McEliece Track 1B TII-83 (n=253, k=213, t=5, m=8)',
    instance_size=253, log2_ops=None,
    method='brute-force private-key enumeration with optimized support-splitting algorithm, using key equivalences',
    structure_exploited=False, hardware='various servers with AMD and Ampere CPUs',
    raw_compute='1471:04:51:00 single-core time (HeroX); ~1470 core-days, ~7700 key candidates per core-second (paper)',
    reported_core_years=cy_from_days(1471.2), date='2024-05', solvers=['Lorenz Panny'], academic=True,
    challenge='TII McEliece', paper='2025/632', source_url=HEROX,
    other_urls=[EP + '2025/632', 'https://tii.ae/news/tii-mceliece-encryption-challenges-winners-announced', PARAMS],
    confidence=0.85,
    notes='Track 1B prize winner (announced 2024-05-30). Paper: naive a-priori estimate 2^91 bit operations. Generic key search, no algebraic structural attack. ' + LABEL))

recs.append(dict(
    id='tii_2a_timerr_2024', problem='SD-Goppa', instance='TII McEliece Track 2A message recovery, ~60-bit instance (parameters not read)',
    instance_size=None, method='optimized Stern ISD (BLP software)', structure_exploited=False,
    date='2024-05', solvers=['Run Timerr'], academic=None, challenge='TII McEliece',
    source_url='https://tii.ae/news/tii-mceliece-encryption-challenges-winners-announced', other_urls=[HEROX],
    confidence=0.5,
    notes='Track 2A winner (US$2,000) for ~60-bit estimated complexity; Track 2B (80-90 bit) unbroken. Name as given by TII (possibly a pseudonym); compute not stated; the 2A leaderboard tab was not in the static page.'))

recs.append(dict(
    id='tii_blt2026_upto210', problem='SD-Goppa',
    instance='TII Track 1B key recovery up to TII-210 (n=491, k=428, t=7, m=9); per 2026/1232 the BLT26 set was labels 83, 89, 119, 166, 210',
    instance_size=491, method='Pfaffian modeling of quadratic-relations code + shortening + square search (polynomial-time for very high-rate Goppa)',
    structure_exploited=True, date='2026-03-03', solvers=['Magali Bardet', 'Axel Lemoine', 'Jean-Pierre Tillich'], academic=True,
    challenge='TII McEliece', extrapolation='breaks the CFS signature scheme (very high-rate Goppa); not applicable at Classic McEliece rates',
    paper='2026/430', source_url=EP + '2026/430', other_urls=[CMNOTE, 'https://link.springer.com/chapter/10.1007/978-3-032-35398-6_13', PARAMS],
    confidence=0.55,
    notes='CRYPTO 2026. Compute not read (PDF blocked). Instance list inferred from 2026/1232 as quoted in the Classic McEliece team note; one search summary instead listed 89, 125, 166, 210 - conflict unresolved. ' + LABEL + ' ' + TIICONF))

recs.append(dict(
    id='tii_brlt2026_248', problem='SD-Goppa', instance='TII Track 1B TII-248 (n=482, k=419, t=7, m=9)', instance_size=482,
    method='algebraic modeling for rank-2 matrices in the quadratic-relations code (degree 5), then key reconstruction',
    structure_exploited=True, raw_compute='64000 seconds, >700 GB memory (core count unspecified)', wall_time_days=64000/86400,
    date='2026-06-10', solvers=['Pierre Briaud', 'Axel Lemoine', 'Hugues Randriambololona', 'Jean-Pierre Tillich'], academic=True,
    challenge='TII McEliece',
    extrapolation='conjectured subexponential in the security level; at best ~2^454 for NIST level-1 Classic McEliece parameters (abstract)',
    paper='2026/1232', source_url=CMNOTE, other_urls=[EP + '2026/1232', PARAMS], confidence=0.65,
    notes='Also re-verified TII-83, 89, 119, 166, 210. Figures quoted from 2026/1232 by the Classic McEliece team note (2026-06-23), which notes 2008 ISD software decrypts ciphertexts at (482,7) in 0.17 s on one core, ~30 million times cheaper. ' + LABEL + ' ' + TIICONF))

recs.append(dict(
    id='brlt2026_cfs_m16_r9', problem='SD-Goppa', instance='CFS signature key, binary Goppa m=16, r=9 (claimed 74.9-bit security per LS12)',
    instance_size=None, method='algebraic rank-2 modeling of quadratic-relations code (Briaud-Lemoine-Randriambololona-Tillich)',
    structure_exploited=True, raw_compute='14 hours, 24 GB RAM', wall_time_days=14/24, date='2026-06-10',
    solvers=['Pierre Briaud', 'Axel Lemoine', 'Hugues Randriambololona', 'Jean-Pierre Tillich'], academic=True,
    paper='2026/1232', source_url=EP + '2026/1232', confidence=0.7,
    notes='Not a challenge entry; key generated by the authors. n presumably 2^16 = 65536 (full-length CFS) but not read; instance_size left null.'))

recs.append(dict(
    id='tii_hemmert2026_hov', problem='SD-Goppa',
    instance='TII Track 1B: 32 instances, labels 83-248; largest label TII-248 (n=482, k=419, t=7, m=9); max t=9 (labels 189, 209, 223)',
    instance_size=482, method='higher-order vanishing (HOV) key recovery (Hemmert; distinguisher Hemmert-Wiemers CRYPTO 2026)',
    structure_exploited=True, hardware='2x AMD EPYC 9745 (2x128 cores)',
    raw_compute='TII-248: 17 h 18 min, 0.5 GB; TII-83: 13 min, 1.7 GB (paper Table 1 as quoted by Saarinen)',
    wall_time_days=(17*60+18)/1440, date='2026-06-29', solvers=['Tobias Hemmert'], academic=True, challenge='TII McEliece',
    extrapolation='conjectured to apply to Classic McEliece at roughly the HOV distinguisher cost, still far above target security',
    paper='2026/1339', source_url=HEMM, other_urls=[EP + '2026/1339', SAAR, PARAMS], confidence=0.75,
    notes='Hemmert reportedly at BSI (search summary). Labels solved (from repo file list, committed 2026-06-29): 83,84,85,86,89,90,91,92,93,94,96,100,105,110,113,119,125,134,160,164,166,171,178,189,200,209,210,212,220,223,244,248. Timings are second-hand (Saarinen README). ' + LABEL + ' ' + TIICONF))

recs.append(dict(
    id='tii_saarinen2026_hover_252', problem='SD-Goppa',
    instance='TII Track 1B TII-252 (n=1008, k=898, t=11, m=10); new: 129, 213, 240, 246, 252',
    instance_size=1008, method='HOVER (higher-order vanishing endomorphism recovery), extension of Hemmert HOV',
    structure_exploited=True, hardware='12-core laptop (AMD Ryzen AI 9 HX 370); 28-vCPU server for TII-129/213',
    raw_compute='TII-252: 6 min 15 s wall, 2.7 GiB; TII-213: 6 h 45 min, 144 GiB; TII-129: 4 h 30 min, 80 GiB',
    wall_time_days=374.8/86400, date='2026-07', solvers=['Markku-Juhani O. Saarinen'], academic=True, challenge='TII McEliece',
    extrapolation='author: analysis does not indicate HOVER threatens Classic McEliece parameters in present form',
    paper='2026/1778', source_url=SAAR, other_urls=[EP + '2026/1778', PARAMS], confidence=0.8,
    notes='Keys obtained late July 2026 (repo init 2026-07-21; laptop rerun log dated 2026-07-21); paper received 2026-08-22. Paper says main shortcut was found with an LLM. Also reproduced Hemmert keys for 83 and 248 ~30-75x faster. ' + LABEL + ' ' + TIICONF))

recs.append(dict(
    id='tii_weis2026_253', problem='SD-Goppa', instance='TII Track 1B TII-253 (n=214, k=142, t=9, m=8)', instance_size=214,
    method='GIJS hold-out distinguisher extended to key recovery (single-run variant), sparse kernel computations',
    structure_exploited=True, raw_compute='two sparse kernel computations, ~700 core-hours each, on one server',
    reported_core_years=cy_from_hours(1400), date='2026-08-18', solvers=['Stephen A. Weis'], academic=True,
    challenge='TII McEliece',
    extrapolation='a GIJS run costs 2^89-2^98 bit ops for Classic McEliece (2^107-2^117 with sqrt memory cost); not practical',
    paper='2026/1984', source_url='https://postquantum.com/security-pqc/classic-mceliece-key-recovery-bsi/',
    other_urls=[EP + '2026/1984', 'https://github.com/sweis/mceliece-challenges', EP + '2026/1630', SAAR], confidence=0.65,
    notes='Weis is at Anthropic (industry research lab, named ePrint paper -> academic=true). Solution committed 2026-08-18 (Saarinen cites 2026-08-19). 700 core-hours figure from secondary sources (postquantum.com article; search snippet of the PDF); PDF not read. Vedenev 2026/1747 also recovered TII-253 shortly after. ' + LABEL + ' ' + TIICONF))

recs.append(dict(
    id='tii_vedenev2026_173_249_253', problem='SD-Goppa',
    instance='TII Track 1B TII-173 (n=96, k=40, t=8, m=7), TII-249 (n=235, k=107, t=16, m=8), TII-253 (n=214, t=9, m=8)',
    instance_size=235, method='GIJS hold-out distinguisher extended to key recovery (tangent-plane/minor-code + Sidelnikov-Shestakov, or quadratic-form ratio)',
    structure_exploited=True, date='2026-08-20', solvers=['Kirill Vedenev'], academic=True, challenge='TII McEliece',
    extrapolation='author: whole key recovery ~ one distinguisher run, 2^89.9-2^98.6 bit ops for Classic McEliece; Apon 2026/1810 argues held-position equations are dependent, giving >2^1500 for mceliece8192128',
    paper='2026/1747', source_url=EP + '2026/1747', other_urls=[EP + '2026/1810', PARAMS], confidence=0.55,
    notes='Abstract says 173 and 249 had not been solved before (253 already solved by Weis). Compute not read (PDF blocked); no key repository located, so the 173/249 keys are unverified by us. TII-249 has t=16, the largest Goppa degree among claimed TII solves. 2026/1810 is a lower-bound argument against the asymptotic/Classic McEliece cost, not a dispute of these toy solves. ' + LABEL + ' ' + TIICONF))

recs.append(dict(
    id='tii_saarinen2026_254', problem='SD-Goppa', instance='TII Track 1B TII-254 (n=223, k=127, t=12, m=8)', instance_size=223,
    method='Two-Anchor Holdout/Hermite: two 121-dim relation kernels (block Wiedemann on GPU), pair core, F_2^8 projective-line geometry, completion search',
    structure_exploited=True, hardware='NVIDIA GH200 GPUs on CSC Roihu (up to 8 GPUs for reconstruction)',
    raw_compute='two Krylov sequences 27.2 GPU-hours (13.6 h each on one GH200), excluding GPU reconstruction and CPU work; ~16 h wall, 128 GiB',
    gpu_years=cy_from_hours(27.2), wall_time_days=16/24, date='2026-09-08', solvers=['Markku-Juhani O. Saarinen'], academic=True,
    challenge='TII McEliece', paper='2026/1986', source_url=EP + '2026/1986',
    other_urls=['https://github.com/mjosaarinen/tii254-artifact', SAAR, PARAMS], confidence=0.8,
    notes='Self-described hardest solved TII challenge (label 254); recovered an equivalent degree-12 Goppa key, checked with official check_solution_track2.sage per repo. gpu_years covers only the Krylov phase (lower bound). TII-255 (n=249, t=24, m=8) remains unsolved per the repo. ' + LABEL + ' ' + TIICONF))

recs.append(dict(
    id='tii_keyrec_summary', problem='SD-Goppa',
    instance='TII McEliece Track 1B key recovery summary: 2024 best TII-83 (generic) / TII-68 (algebraic); 2026 best TII-254; TII-255 open',
    instance_size=223, method='structural key recovery (2026)', structure_exploited=True, date='2026-09-08',
    solvers=['Markku-Juhani O. Saarinen'], academic=True, challenge='TII McEliece', source_url=SAAR,
    other_urls=[HEROX, TIISITE, TIIREPO, PARAMS, CMNOTE], confidence=0.7,
    notes='SUMMARY FILE - exclude from record counts. Challenge ran 2023-05-09 to 2024-05-08 (winners 2024-05-30); 206 public keys, labels 22-255. 2026 sequence: BLT (Mar, <=210), Briaud et al. (Jun 10, 248), Hemmert (Jun 29, 32 labels to 248), Saarinen HOVER (Jul, 252), Weis (Aug 18, 253), Vedenev (Aug 20, 173/249/253), Saarinen (Sep 8, 254). All structural; no generic ISD. Track 1B instances have artificially small t (t=2-24, rates up to ~0.9) - not scaled Classic McEliece parameters (Bernstein 2023; Classic McEliece team note 2026-06-23). ' + TIICONF))

recs.append(dict(
    id='cb2013_rm_mceliece_65536', problem='SD', instance='McEliece with binary Reed-Muller codes RM(r,m), n=65536', instance_size=65536,
    method='structural key recovery for RM-code McEliece, O(n^d + n^4 log n), d=gcd(r,m-1)', structure_exploited=True,
    hardware='personal computer', raw_compute='less than 7 hours on a PC', wall_time_days=7/24, date='2013-05',
    solvers=['I. V. Chizhov', 'M. A. Borodin'], academic=True, paper='2013/287', source_url=EP + '2013/287', confidence=0.7,
    notes='Not Goppa codes: breaks the RM-code variant (Sidelnikov-type) of McEliece; r,m for the n=65536 demo not stated in abstract.'))

recs.append(dict(
    id='fopdt2014_qd_qm_mceliece', problem='SD-Goppa', instance='compact (quasi-dyadic / quasi-monoidic) McEliece and CFS parameters from the literature',
    instance_size=None, method='folding to small code + improved FOPT algebraic key recovery with structural elimination',
    structure_exploited=True, raw_compute='most CFS QD/QM parameters in a few seconds; hardest < 2 hours; some encryption parameters out of reach',
    date='2014-03', solvers=['Jean-Charles Faugere', 'Ayoub Otmani', 'Ludovic Perret', 'Frederic de Portzamparc', 'Jean-Pierre Tillich'], academic=True,
    paper='2014/210', source_url=EP + '2014/210', confidence=0.6,
    notes='Multiple proposed parameter sets / "cryptographic challenges" for QD/QM encryption broken; individual instances and hardware not read (PDF blocked).'))

recs.append(dict(
    id='bdhv2025_qasd_f4oleage', problem='LPN', instance='QA-SD (quasi-Abelian syndrome decoding) PCG parameters incl. F4OLEage (Asiacrypt 2024)',
    instance_size=None, method='sparse multivariate interpolation (incl. compressed-sensing convex optimization)', structure_exploited=True,
    raw_compute='distinguishes F4OLEage PCG output with 60% advantage in a few hours', date='2025-05',
    solvers=['Charles Bouillaguet', 'Claire Delaplace', 'Mickael Hamdad', 'Damien Vergnaud'], academic=True,
    paper='2025/892', source_url=EP + '2025/892', confidence=0.6,
    notes='Ring-LPN-like assumption (QA-SD) for PCGs, not a PKE assumption; also breaks parameters of Bombar et al. Crypto 2023 and Li et al. Eurocrypt 2025. Problem label LPN used for lack of a QA-SD category.'))

for r in recs:
    write(r)
print(len(recs))
