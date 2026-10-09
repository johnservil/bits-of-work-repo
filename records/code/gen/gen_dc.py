"""Generate decodingchallenge.org progression records, track summaries and HOF CSVs.
Inputs (all fetched 2026-10-08/09 into this scratch dir): dc.json (from progression.py),
tooltips.json (per-instance complexity tooltips on the track pages)."""
import json, csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import write, OUT, cy_from_days, cy_from_hours

HERE = os.path.dirname(os.path.abspath(__file__))
dc = json.load(open(os.path.join(HERE, 'dc.json')))
import re as _re
for _t in dc.values():
    for _p in _t['all'] + _t['prog']:
        if _p.get('provider'): _p['provider'] = _re.sub('[\U0001F1E6-\U0001F1FF]', '', _p['provider']).replace('  ', ' ').strip()
tt = json.load(open(os.path.join(HERE, 'tooltips.json')))
BASE = 'https://decodingchallenge.org/'

TRACK = {
    'syndrome':     dict(slug='sd', problem='SD', label='SD (random binary [n,n/2], w=ceil(1.05 d_GV))'),
    'goppa':        dict(slug='goppa', problem='SD-Goppa', label='Goppa-McEliece setting (random binary, R=0.8, w=ceil(n/(5 ceil(log2 n))))'),
    'q-c':          dict(slug='qc', problem='SD-QC', label='quasi-cyclic setting (BIKE-like, n=w^2+2, R=0.5)'),
    'large-weight': dict(slug='large_weight', problem='SD', label='large-weight ternary SD (F3, R=0.5)'),
    'low-weight':   dict(slug='low_weight', problem='SD', label='low-weight codeword search, fixed n=1280, R=0.5'),
}

# (track, key) -> overrides. key = n (or weight for low-weight). Times as stated on record pages.
D = 1.0
OV = {
 ('goppa',286): dict(wall_time_days=5/86400),
 ('goppa',640): dict(wall_time_days=40/86400, notes_extra='submitter comment: theoretical work factor 2^32 (Dumer p=4, l=8).'),
 ('goppa',695): dict(wall_time_days=12/1440),
 ('goppa',865): dict(wall_time_days=100/1440),
 ('goppa',923): dict(wall_time_days=10/24),
 ('goppa',982): dict(wall_time_days=4/24),
 ('goppa',1041): dict(wall_time_days=108/24),
 ('goppa',1101): dict(wall_time_days=60/24, academic=False, notes_extra='submitter comment "Greetings from Sweden, Scania!" suggests industry hobby project.'),
 ('goppa',1161): dict(wall_time_days=375.8/24),
 ('goppa',1223): dict(wall_time_days=3.0, paper='2021/1634', other_urls=['https://eprint.iacr.org/2021/1634'],
     extrapolation='EMZ22 extrapolate from 1223/1284 records that McEliece round-3 192/256-bit parameters are overestimated by ~20 and ~10 bits.',
     notes_extra='paper reportedly states ~5 CPU-years for this record (search snippet only; PDF blocked by Cloudflare; unconfirmed). BLP later re-solved all three n=1223 provider instances with their 2008 software on 2x EPYC 7742 (lucky runs of 5-250 h wall), see isd.mceliece.org/20220704.txt.'),
 ('goppa',1284): dict(reported_core_years=cy_from_days(8047), paper='2021/1634', other_urls=['https://eprint.iacr.org/2021/1634','https://isd.mceliece.org/1347.html'],
     extrapolation='EMZ22: McEliece round-3 192/256-bit parameter sets ~20/~10 bits below claimed level.',
     notes_extra='"8047 CPU Days" on record page (CPU vs hardware-thread ambiguous); paper ~22 CPU-years (search snippet). Bernstein (isd.mceliece.org/1347.html) says EMZ22 average was 37.47 days on 4x EPYC 7742 vs 31.56 days for the BLP 2008 software.'),
 ('goppa',1347): dict(hardware='Cisco ICS cluster (UCSD), Academia Sinica Fast Crypto Lab, UIC and TU/e machines; solution found on 2x AMD EPYC 7742 node',
     raw_compute='2^41.7 iterations (predicted average 2^41.6); ~2.3M cycles per iteration on the EPYC node',
     solvers=['Daniel J. Bernstein','Tanja Lange','Christiane Peters'], academic=True, paper='2008/318',
     other_urls=['https://isd.mceliece.org/1347.html','https://eprint.iacr.org/2008/318'],
     date='2023-02-24',
     notes_extra='Run by Bernstein using the unmodified PQCrypto 2008 BLP Stern-variant ISD software; credit assigned to BLP. Derived (not stated): 2^41.7 x 2.3e6 cycles ~ 2^62.8 cycles ~ 115 core-years at 2.245 GHz; per-core cycles differ across the clusters used. Announcement page dated 2023-02-26.',
     method='Stern-type ISD (BLP 2008 software, "2+2" case)', confidence=0.85),
 ('goppa',1409): dict(wall_time_days=30/24, paper='2024/393', other_urls=['https://eprint.iacr.org/2024/393','https://github.com/sh-narisada/CU_BJMM'],
     notes_extra='paper title "Solving McEliece-1409 in One Day"; paper presents GPU depth-2 BJMM (cuBJMM) but the record page leaves hardware blank and calls the algorithm "MMT variant" -- hardware for this solve unconfirmed. Paper describes ~70-bit security instance (search snippet).'),
 ('large-weight',20): dict(wall_time_days=1/86400),
 ('large-weight',80): dict(wall_time_days=20/1440),
 ('large-weight',130): dict(reported_core_years=cy_from_hours(110/60)),
 ('large-weight',140): dict(reported_core_years=cy_from_hours(15/60), notes_extra='solved on seed 1 instance.'),
 ('large-weight',150): dict(reported_core_years=cy_from_days(13)),
 ('large-weight',190): dict(wall_time_days=90/24, reported_core_years=cy_from_days(480), paper='2021/1634'),
 ('large-weight',200): dict(wall_time_days=43/24, reported_core_years=cy_from_days(919), paper='2021/1634'),
 ('large-weight',220): dict(wall_time_days=15.8),
 ('large-weight',230): dict(wall_time_days=2.4),
 ('large-weight',240): dict(wall_time_days=1.4),
 ('low-weight',568): dict(wall_time_days=1/1440),
 ('low-weight',233): dict(reported_core_years=cy_from_days(3), notes_extra='stated as "< 3 core days" (upper bound).'),
 ('low-weight',231): dict(reported_core_years=cy_from_days(30)),
 ('low-weight',230): dict(wall_time_days=1/24),
 ('low-weight',224): dict(wall_time_days=34/24),
 ('low-weight',214): dict(wall_time_days=30, method='lattice-based: Kannan embedding + BKZ/SVP', notes_extra='runtime stated only as "Month".'),
 ('low-weight',212): dict(wall_time_days=19, method='lattice-based: BKZ + SVP', notes_extra='"19 day from prev. SVP solut." (incremental from the w=214 run).'),
 ('low-weight',211): dict(wall_time_days=4+19/24+4/1440, paper='2020/869', academic=True,
     notes_extra='MCCL implementation, 40 threads; 2-level Wagner p=3 with Babai lifting on reduced code basis.'),
 ('low-weight',210): dict(wall_time_days=22.7/24, paper='2024/393', notes_extra='expected runtime 7.3 days on the 10 PCs (lucky).'),
 ('low-weight',209): dict(wall_time_days=2.67, paper='2024/393', notes_extra='expected runtime 9.65 days on the 10 PCs.'),
 ('low-weight',204): dict(wall_time_days=62.4, paper='2024/393', notes_extra='expected runtime 440 days on the 10 PCs (lucky).'),
 ('q-c',1158): dict(wall_time_days=12.5/1440),
 ('q-c',1298): dict(wall_time_days=1/24),
 ('q-c',1446): dict(wall_time_days=3/24),
 ('q-c',1602): dict(wall_time_days=90/24),
 ('q-c',1766): dict(reported_core_years=cy_from_hours(1150), notes_extra='"1150 h" marked CPU time.'),
 ('q-c',1938): dict(reported_core_years=cy_from_days(6400)),
 ('q-c',2118): dict(wall_time_days=63/1440, paper='2021/1634'),
 ('q-c',2502): dict(wall_time_days=7.3/24, reported_core_years=cy_from_days(157.3), paper='2021/1634'),
 ('q-c',2918): dict(wall_time_days=80/24, reported_core_years=cy_from_days(1719), paper='2021/1634',
     extrapolation='EMZ22: extrapolations confirm claimed BIKE/HQC bit-security levels.',
     notes_extra='paper: "1700 CPU days" (search snippet), bit-security 58.6 for this instance.'),
 ('q-c',3138): dict(wall_time_days=38.31/24, reported_core_years=cy_from_days(817), paper='2022/1329', other_urls=['https://eprint.iacr.org/2022/1329'],
     extrapolation='EZ23: lowers previous McEliece/BIKE/HQC estimates by up to 6 bits.'),
 ('q-c',3366): dict(wall_time_days=9.27, paper='2024/393', notes_extra='expected runtime 8.4 days on 10 PCs.'),
 ('q-c',3602): dict(wall_time_days=63.5, paper='2024/393', notes_extra='expected runtime 31.9 days on 10 PCs (unlucky).'),
 ('q-c',3846): dict(wall_time_days=66.2, paper='2024/393', notes_extra='expected runtime 138.7 days on 10 PCs (lucky).'),
 ('q-c',4098): dict(wall_time_days=(61+22/60)/1440, gpu_years=cy_from_hours(24.5), academic=True,
     method='"Crinoid" codebase: threefold ring folding, GPU BJMM + DOOM, multi-target QC rotations, full-ring lifting',
     notes_extra='very recent (5 days before harvest); no paper located. Submitter affiliation inferred (Tampere Univ., per his tii-solved repo). Ring folding exploits QC structure.',
     confidence=0.75),
 ('syndrome',30): dict(wall_time_days=10/86400),
 ('syndrome',170): dict(wall_time_days=100/86400),
 ('syndrome',200): dict(wall_time_days=1/24),
 ('syndrome',340): dict(notes_extra='seed 221 instance; runtime "a few hours".'),
 ('syndrome',370): dict(wall_time_days=1/24, notes_extra='p=6, l=19.'),
 ('syndrome',410): dict(wall_time_days=21/24),
 ('syndrome',450): dict(reported_core_years=cy_from_days(39), notes_extra='"39 d" marked CPU time.'),
 ('syndrome',460): dict(wall_time_days=100/1440, gpu_years=cy_from_hours(8), notes_extra='100 min x 5 V100 = 8 GPU-hours.'),
 ('syndrome',470): dict(gpu_years=cy_from_hours(75)),
 ('syndrome',500): dict(gpu_years=cy_from_days(20.3)),
 ('syndrome',510): dict(notes_extra='runtime field "592.9" with no unit.', other_urls=['https://www.jstage.jst.go.jp/article/transfun/advpub/0/advpub_2022CIP0023/_pdf']),
 ('syndrome',530): dict(wall_time_days=301/24, other_urls=['https://www.jstage.jst.go.jp/article/transfun/advpub/0/advpub_2022CIP0023/_pdf']),
 ('syndrome',540): dict(wall_time_days=79.44, other_urls=['https://www.jstage.jst.go.jp/article/transfun/advpub/0/advpub_2022CIP0023/_pdf']),
 ('syndrome',550): dict(wall_time_days=13.03, other_urls=['https://www.jstage.jst.go.jp/article/transfun/advpub/0/advpub_2022CIP0023/_pdf']),
 ('syndrome',570): dict(wall_time_days=45.32, notes_extra='GPU MMT ("Multiparallel MMT", IEICE Trans. 2023) likely but hardware blank on record page.'),
}

ACAD_TRUE = ['Lequesne','Lavauzelle','Loidreau','Vasseur','Narisada','Esser','Zweydinger','Bernstein','Karpman',
             'Udovenko','Samuel Neves','Ducas','Saarinen','Bordes']
ORGANIZERS = ['Lequesne','Lavauzelle','Aragon']

def split_authors(a):
    a = a.replace(' and ', ', ')
    return [x.strip() for x in a.split(',') if x.strip()]

def academic_of(a):
    if any(k in a for k in ACAD_TRUE): return True
    return None

def ops(track, p):
    k = str(p['w'] if track == 'q-c' else p['n'])
    v = tt.get(track, {}).get(k)
    if v and v.startswith('2^') and '/' not in v:
        return float(v[2:])
    return None

def blank(x):
    return None if (x is None or x.strip() in ('', '-')) else x.strip()

written = []
for track, info in TRACK.items():
    prog = dc[track]['prog']
    for p in prog:
        key = p['w'] if track == 'low-weight' else p['n']
        ov = dict(OV.get((track, key), {}))
        extra = ov.pop('notes_extra', None)
        if track == 'low-weight':
            rid = 'dc_low_weight_w%d' % p['w']
            inst = 'decodingchallenge low-weight codeword n=1280, weight %d found' % p['w']
        else:
            rid = 'dc_%s_n%d' % (info['slug'], p['n'])
            inst = 'decodingchallenge %s n=%d w=%d' % (info['slug'].replace('_', '-'), p['n'], p['w'])
        hw = blank(p['hardware']); rt = blank(p['runtime'])
        raw = '; '.join(x for x in [('runtime: ' + rt) if rt else None, ('hardware: ' + hw) if hw else None] if x) or None
        ds = 'QC' in info['problem'] and ('DOOM' in p['alg'] or 'QC rotation' in p['alg'] or 'folding' in p['alg'])
        notes = ['record progression entry (new max n%s at submission date per hall of fame)' % (' / new min weight' if track == 'low-weight' else '')]
        lo = ops(track, p)
        if lo is not None:
            notes.append('log2_ops = site tooltip "indication of complexity" for this instance, not a solver figure')
        if p.get('provider'): notes.append('instance provider: ' + p['provider'])
        if any(o in p['authors'] for o in ORGANIZERS): notes.append('solver is a challenge organizer')
        if ds: notes.append('DOOM/QC structure exploited')
        if track == 'goppa': notes.append('instances are random parity-check matrices with planted error (not actual Goppa codes); McEliece-like rate/weight')
        if track == 'large-weight': notes.append('ternary large-weight SD (Wave-like)')
        if extra: notes.append(extra)
        rec = dict(id=rid, problem=info['problem'], instance=inst,
                   instance_size=p['n'], instance_size_unit='n', log2_ops=lo,
                   method=blank(p['alg']), structure_exploited=bool(ds), hardware=hw, raw_compute=raw,
                   date=p['date'], solvers=split_authors(p['authors']), academic=academic_of(p['authors']),
                   challenge='decodingchallenge.org', source_url=BASE + p['rec'],
                   other_urls=[BASE + track + '/halloffame'], confidence=0.85)
        for k, v in ov.items():
            if k == 'other_urls': rec['other_urls'] = rec['other_urls'] + v
            else: rec[k] = v
        rec['notes'] = '; '.join(notes)
        written.append(write(rec))

    # summary file
    last = prog[-1]
    if track == 'low-weight':
        sid = 'dc_low_weight_summary'; cur = 'best weight %d at n=1280 (GV ~144)' % last['w']
    else:
        sid = 'dc_%s_summary' % info['slug']; cur = 'max n=%d (w=%d)' % (last['n'], last['w'])
    steps = ', '.join(('w%d %s' % (p['w'], p['date'][:7])) if track == 'low-weight' else ('%d %s' % (p['n'], p['date'][:7])) for p in prog)
    rec = dict(id=sid, problem=info['problem'],
               instance='decodingchallenge %s track summary: %s' % (info['label'], cur),
               instance_size=last['n'], log2_ops=ops(track, last), method=blank(last['alg']),
               structure_exploited=bool('QC' in info['problem'] and ('DOOM' in last['alg'] or 'folding' in last['alg'])), hardware=blank(last['hardware']), raw_compute=blank(last['runtime']),
               date=last['date'], solvers=split_authors(last['authors']), academic=academic_of(last['authors']),
               challenge='decodingchallenge.org', source_url=BASE + track + '/halloffame',
               other_urls=[BASE + track, BASE + last['rec']], confidence=0.85,
               notes='SUMMARY FILE - duplicates the latest progression record; exclude from record counts. '
                     'Hall of fame has %d entries (first ten solvers per instance). Progression (n or weight, date): %s. '
                     'Full table: dc_%s_hof.csv. Harvested 2026-10-08.' % (len(dc[track]['all']), steps, info['slug']))
    written.append(write(rec))

    # HOF CSV
    path = os.path.join(OUT, 'dc_%s_hof.csv' % info['slug'])
    with open(path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['track', 'length_n', 'weight', 'authors', 'algorithm', 'date', 'provider_or_seed',
                    'hardware', 'runtime', 'comments', 'site_log2_complexity', 'record_url'])
        for p in sorted(dc[track]['all'], key=lambda x: (x['n'], -x['w'], x['date'])) if track != 'low-weight' else sorted(dc[track]['all'], key=lambda x: x['w']):
            w.writerow([track, p['n'], p['w'], p['authors'], p['alg'], p['date'],
                        p['provider'] or p['length_field'], p['hardware'], p['runtime'],
                        (p['comments'] or '')[:300], ops(track, p), BASE + p['rec']])
    written.append(path)
print(len(written), 'files')
