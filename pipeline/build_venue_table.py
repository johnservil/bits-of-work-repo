#!/usr/bin/env python3
"""Resolve where each counted item was published, from every venue source we hold.

Run from the repo root:  python3 -I pipeline/build_venue_table.py

Inputs (all optional except the export and the registry; missing sources are skipped):
  data/export/combined_included.csv         counted rows (include = yes, category A-F/H)
  data/venues/venue_registry.tsv            venue identification (name, kind, refereed, DBLP streams, regex)
  data/venues/dblp_matches.jsonl            DBLP records with the same title (match_dblp_versions.py)
  data/venues/dblp_search.jsonl             looser offline DBLP search for still-unresolved items (search_dblp_local.py)
  data/raw/crossref/works.jsonl             Crossref metadata per DOI (fetch_crossref.py)
  data/raw/openalex_locations/works.jsonl   OpenAlex locations per work (fetch_openalex_locations.py)
  data/raw/openalex_title_search/hits.jsonl OpenAlex title search for unresolved items
  data/raw/eprint_pages/pubinfo.jsonl       ePrint "Publication info" (fetch_eprint_pubinfo.py)
  data/venues/openalex_source_overrides.tsv  OpenAlex sources with unreliable venue attribution
  data/venues/fuzzy_checks.csv              verdicts on retitled DBLP matches (id, dblp_key, verdict =
                                            same|different, note)
  data/venues/manual_venues.csv             hand/agent-checked resolutions (id, pub_venue, pub_type,
                                            pub_year, pub_doi, vid, refereed, confidence, evidence); wins
Outputs:
  data/venues/published_venues.csv   one row per counted item (read by build_bibliography.py)
  data/venues/venue_flags.csv        items needing attention (DOI/title mismatch, year conflicts,
                                     possible duplicates, unparsed ePrint publication info)
  analysis/venue_resolution.md       coverage summary by source, id type and class
Evidence order: manual > DBLP record itself > DBLP same-title record with author overlap >
Crossref (item DOI) > zbMATH venue > OpenAlex published location > ePrint publication info >
the export's own venue string. Stdlib only.
"""
import csv, json, re, unicodedata, collections, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V = ROOT / 'data/venues'
EFFORT = set('ABCDEFH')
EPRINT = re.compile(r'^\d{4}/\d+$')
CLASSES = [('Lattices', ['w_MLWE_structured', 'w_LWE_plain']), ('ECDLP', ['w_ECDLP']),
           ('Syndrome decoding', ['w_SD_code']), ('Factoring/FF-DLP', ['w_Factoring_FFDLP']),
           ('Isogenies', ['w_Isogeny']), ('Multivariate', ['w_Multivariate'])]
PREPRINT_STREAMS = {'journals/corr', 'journals/iacr', 'journals/eccc'}


def jl(p):
    p = ROOT / p
    return [json.loads(l) for l in open(p) if l.strip()] if p.exists() else []


def norm(s):
    s = unicodedata.normalize('NFKD', s or '')
    s = re.sub(r'\$[^$]*\$', lambda m: re.sub(r'\\[a-zA-Z]+|[{}^_\\]', '', m[0]), s)
    return re.sub(r'[^a-z0-9]', '', re.sub(r'<[^>]+>', '', s).lower())


def lastnames(names):
    out = set()
    for a in names:
        a = re.sub(r'\s+\d{4}$', '', a.strip())
        if ',' in a:
            a = a.split(',')[0]
        else:
            a = a.split()[-1] if a.split() else ''
        a = norm(a)
        if len(a) > 1:
            out.add(a)
    return out


def tsim(a, b):
    """Crude title similarity: share of character trigrams of the shorter normalized title."""
    a, b = norm(a), norm(b)
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    ga = {a[i:i + 3] for i in range(len(a) - 2)}
    gb = {b[i:i + 3] for i in range(len(b) - 2)}
    return len(ga & gb) / max(1, min(len(ga), len(gb)))


# ---------------------------------------------------------------- registry
REG, BY_STREAM = [], {}
for line in open(V / 'venue_registry.tsv'):
    if line.startswith('#') or line.startswith('vid\t') or not line.strip():
        continue
    f = (line.rstrip('\n').split('\t') + [''] * 7)[:7]
    r = dict(zip(['vid', 'refereed', 'kind', 'name', 'core', 'dblp', 'regex'], [x.strip() for x in f]))
    r['rx'] = re.compile(r['regex'], re.I) if r['regex'] else None
    REG.append(r)
    for s in filter(None, (x.strip() for x in r['dblp'].split(','))):
        BY_STREAM[s] = r


def reg_by_name(*names):
    for n in names:
        if not n:
            continue
        for r in REG:
            if r['rx'] and r['rx'].search(n):
                return r
    return None


def stream(key):
    return '/'.join(key.split('/')[:2])


# ---------------------------------------------------------------- candidate builders
def cand(src, conf, venue_name, kind, year, doi='', reg=None, detail='', refereed=None):
    return {'src': src, 'conf': conf, 'raw': venue_name or '', 'kind': kind, 'year': year, 'doi': doi or '',
            'reg': reg, 'detail': detail,
            'refereed': refereed if refereed is not None else (reg['refereed'] if reg else '')}


def kind_of_dblp(rec_kind, key):
    if rec_kind in ('phdthesis', 'mastersthesis'):
        return 'thesis'
    if rec_kind == 'book':
        return 'book'
    if rec_kind == 'incollection':
        return 'chapter'
    return 'journal' if key.startswith('journals/') else 'conference' if key.startswith('conf/') else 'other'


def from_dblp(m, src, conf, detail):
    s = stream(m['key'])
    reg = BY_STREAM.get(s)
    k = kind_of_dblp(m['kind'], m['key'])
    if reg and reg['kind'] in ('preprint', 'report'):
        k = reg['kind']
    ref = reg['refereed'] if reg else ('thesis' if k == 'thesis' else
                                       'no' if s in PREPRINT_STREAMS or m.get('publtype') == 'informal' else 'likely')
    return cand(src, conf, m['venue'], k, m['year'], m.get('doi', ''), reg, detail or 'dblp ' + m['key'], ref)


CR_KIND = {'journal-article': 'journal', 'proceedings-article': 'conference', 'book-chapter': 'chapter',
           'posted-content': 'preprint', 'dissertation': 'thesis', 'report': 'report', 'book': 'book',
           'monograph': 'book', 'edited-book': 'book', 'reference-entry': 'chapter'}
SERIES = re.compile(r'^(Lecture Notes in|Communications in Computer and Information Science|Advances in Intelligent|'
                    r'Springer|Smart Innovation|Studies in|Mathematics for Industry|Information Security and Cryptography$)', re.I)


def from_crossref(cr, conf):
    names = [n for n in cr.get('containers') or [cr.get('container', '')] if n]
    proc = [n for n in names if not SERIES.match(n)] or names
    k = CR_KIND.get(cr.get('type'), 'other')
    reg = reg_by_name(*(proc + [cr.get('event', '')]))
    if k == 'chapter' and names and SERIES.match(names[0]):
        k = 'conference'  # LNCS-type proceedings chapters
    ref = reg['refereed'] if reg else ('no' if k in ('preprint', 'report') else 'thesis' if k == 'thesis' else 'likely')
    name = proc[0] if proc else ''
    if not name and k == 'book':
        name = f"Book ({cr.get('publisher') or 'publisher unknown'})"
    if not name and k == 'thesis':
        name = 'Dissertation' + (f" ({cr['publisher']})" if cr.get('publisher') else '')
    return cand('crossref', conf, name, k, cr.get('year'), cr['doi'], reg,
                'crossref ' + cr['doi'], ref)


OA_OVERRIDE = {}
if (V / 'openalex_source_overrides.tsv').exists():
    for line in open(V / 'openalex_source_overrides.tsv'):
        f = line.rstrip('\n').split('\t')
        if line.startswith('#') or f[0] == 'source_id' or len(f) < 2:
            continue
        OA_OVERRIDE[f[0]] = f[1]

OA_KIND = {'journal': 'journal', 'conference': 'conference', 'book series': 'conference', 'ebook platform': 'chapter',
           'repository': 'preprint'}


def from_openalex(w, conf):
    out = []
    for l in [w['primary']] + w['locations']:
        if not l.get('source'):
            continue
        act = OA_OVERRIDE.get(l['source_id'])
        if act == 'ignore':
            continue
        if act in ('thesis', 'report'):
            out.append(cand('openalex', 0.5, f"{l['source']} (OpenAlex attribution unreliable)", act, w['year'], w['doi'],
                            None, f"openalex {w['id']} {l['source_id']} override", 'no' if act == 'report' else 'thesis'))
            continue
        k = OA_KIND.get(l['source_type'], 'other')
        reg = reg_by_name(l['source'])
        if reg:
            k = reg['kind'] if reg['kind'] in ('preprint', 'report') else k
        ref = reg['refereed'] if reg else ('no' if k == 'preprint' else 'likely')
        out.append(cand('openalex', conf, l['source'], k, w['year'], w['doi'], reg,
                        f"openalex {w['id']} {l['source_id']}", ref))
    return out


SUBMITTED = re.compile(r'submitted|under (review|submission)|in submission', re.I)
NOPUB = re.compile(r'unknown where it was published|unknown status|^preprint\.?( minor revision\.?| major revision\.?)?$|^$|'
                   r'^published elsewhere\.\s*(-|none\.?|no\.?|n/a\.?)?$|(never|not) (been )?published|to be submitted', re.I)
VENUEISH = re.compile(r'journal|conference|symposium|proceedings|workshop|trans(actions|\.)|lecture notes|lncs|festschrift|'
                      r'\b[A-Z][A-Za-z-]{2,}[ \'’-]?(19|20)?\d\d\b|math|appear|presented|doi', re.I)


def from_pubinfo(p):
    t = p.get('pubinfo', '')
    if NOPUB.search(t.strip()) or SUBMITTED.search(t):
        return None, t
    body = re.sub(r'^(Published elsewhere\.|Preprint\.)\s*(Minor revision\.|Major revision\.)?\s*', '', t, flags=re.I)
    reg = reg_by_name(body)
    yr = re.findall(r'(?<!\d)(19[789]\d|20[0-3]\d)(?!\d)', body)
    conf = 0.85 if re.search(r'IACR publication|Published by the IACR', t) else 0.75
    if 'to appear' in t.lower() or 'accepted' in t.lower() or 'presented' in t.lower():
        conf -= 0.05
    if reg and reg['kind'] in ('preprint', 'report'):
        return None, t
    if not reg:
        # authors' free text naming a venue we have not registered: keep it, flagged, as 'likely'
        if not VENUEISH.search(body) or re.search(r'RSA, NFS|^[a-z ,]+$', body):
            return None, t
        name = re.sub(r'^(This (paper )?(is|appears in) (a |an |the )?(full |extended )?(version of )?)', '', body, flags=re.I)
        return cand('eprint-pubinfo', 0.7, name.strip(' .')[:160], 'other', int(yr[0]) if yr else None, p.get('doi', ''),
                    None, 'eprint pubinfo (unregistered venue): ' + body[:120], 'likely'), t
    k = reg['kind'] if reg['kind'] in ('conference', 'journal', 'workshop') else 'other'
    return cand('eprint-pubinfo', conf, body[:200], k, int(yr[0]) if yr else None, p.get('doi', ''), reg,
                'eprint pubinfo: ' + body[:120]), t


def from_export(row, conf):
    v = row['venue'].strip()
    if not v or EPRINT.match(row['id']):
        return None
    reg = reg_by_name(v)
    k = reg['kind'] if reg else 'other'
    return cand('export-venue', conf, v, k, int(row['year']) if row['year'].isdigit() else None, row['doi'], reg,
                'export venue string', reg['refereed'] if reg else '')


# ---------------------------------------------------------------- display name for the bibliography
def display(c):
    reg, y = c['reg'], c['year']
    if reg and reg['kind'] in ('conference', 'workshop'):
        return f"{reg['name']} {y}" if y else reg['name']
    if reg:
        return reg['name']
    return c['raw']


def pub_type(c):
    k = c['kind']
    if k in ('conference', 'workshop'):
        return 'conference'
    return {'journal': 'journal', 'thesis': 'thesis', 'book': 'book', 'chapter': 'chapter',
            'preprint': 'preprint', 'report': 'report'}.get(k, 'other')


# ---------------------------------------------------------------- main
def main():
    rows = [r for r in csv.DictReader(open(ROOT / 'data/export/combined_included.csv'))
            if r['include'] == 'yes' and r['category'] in EFFORT]
    dblpm = {d['id']: d['matches'] for d in jl('data/venues/dblp_matches.jsonl')}
    cross = {d['doi'].lower(): d for d in jl('data/raw/crossref/works.jsonl') if d.get('status') == 200}
    oalex = {d['id']: d for d in jl('data/raw/openalex_locations/works.jsonl')}
    pubinfo = {d['id']: d for d in jl('data/raw/eprint_pages/pubinfo.jsonl') if d.get('status') == 200}
    dsearch = {d['id']: d['hits'] for d in jl('data/venues/dblp_search.jsonl')}
    oasearch = {d['id']: d['hits'] for d in jl('data/raw/openalex_title_search/hits.jsonl')}
    counted_ids = {r['id'] for r in rows}
    oa_owner = collections.defaultdict(list)
    fuzzy_checks = collections.defaultdict(dict)  # id -> {dblp key: same|different}
    if (V / 'fuzzy_checks.csv').exists():
        for r in csv.DictReader(open(V / 'fuzzy_checks.csv')):
            fuzzy_checks[r['id']][r['dblp_key']] = r['verdict']
    manual = {}
    if (V / 'manual_venues.csv').exists():
        manual = {r['id']: r for r in csv.DictReader(open(V / 'manual_venues.csv'))}

    out, flags = [], []
    dblp_owner = collections.defaultdict(list)  # DBLP key -> counted ids whose title matched it
    stats = collections.Counter()
    for row in rows:
        i = row['id']
        idtype = 'eprint' if EPRINT.match(i) else i.split(':')[0] if ':' in i else 'openalex'
        if i.startswith('dblp:'):
            idtype = 'dblp:' + i[5:].split('/')[0]
        fz_verdict = fuzzy_checks.get(i, {})
        authors = lastnames(row['authors'].split(';'))
        year = int(row['year']) if row['year'].isdigit() else None
        cands, notes = [], []

        # DBLP record itself
        if i.startswith('dblp:'):
            key = i[5:]
            self_m = next((m for m in dblpm.get(i, []) if m['key'] == key), None)
            m = self_m or {'key': key, 'kind': {'conf': 'inproceedings', 'journals': 'article', 'phd': 'phdthesis',
                                                'books': 'book', 'series': 'incollection'}.get(key.split('/')[0], 'article'),
                           'venue': row['venue'], 'year': year, 'doi': row['doi'], 'publtype': ''}
            cands.append(from_dblp(m, 'dblp-self', 1.0, 'dblp ' + key))
            dblp_owner[key].append((i, 'self'))
        # DBLP same-title records with author overlap
        for m in dblpm.get(i, []):
            if i.startswith('dblp:') and m['key'] == i[5:]:
                continue
            if m.get('fuzzy'):  # retitled version: same authors, similar title (Dice on trigrams)
                if stream(m['key']) in PREPRINT_STREAMS:
                    continue
                if m['key'] in fz_verdict:  # checked by hand/agent: data/venues/fuzzy_checks.csv
                    if fz_verdict[m['key']] != 'same':
                        continue
                    conf = 0.85  # agent/hand-checked 'same'; not certain
                else:
                    conf = 0.85 if m['sim'] >= 0.85 else 0.65 if m['sim'] >= 0.6 else 0.5
                c = from_dblp(m, 'dblp-fuzzy', conf, f"dblp {m['key']} (retitled? sim {m['sim']}: {m['title'][:80]})")
                c['fuzzy'] = m
                cands.append(c)
                if conf >= 0.85:
                    dblp_owner[m['key']].append((i, f"retitled sim {m['sim']}"))
                continue
            shared = authors & lastnames(m['authors'])
            if authors and m['authors'] and not shared:
                notes.append(f"title-only dblp match rejected (no shared author): {m['key']}")
                continue
            if year and m['year'] and not (year - 3 <= m['year'] <= year + 8):
                notes.append(f"dblp match outside year window: {m['key']} ({m['year']})")
                continue
            dblp_owner[m['key']].append((i, 'title'))
            cands.append(from_dblp(m, 'dblp-title', 0.95 if shared else 0.85, ''))
        # looser DBLP search hits (search_dblp_local.py), for items the dump pass did not resolve
        seen_keys = {m['key'] for m in dblpm.get(i, [])} | ({i[5:]} if i.startswith('dblp:') else set())
        for h in dsearch.get(i, []):
            if h['key'] in seen_keys or not h['key'] or h['sim'] < 0.6:
                continue
            shared = authors & lastnames(h['authors'])
            if (authors and h['authors'] and not shared) or (not authors and h['sim'] < 0.9):
                continue
            if not authors and row['authors'].strip():
                continue  # authors exist but in a non-Latin script: no author check possible, so no loose match
            if year and h['year'] and not (year - 3 <= h['year'] <= year + 8):
                continue
            if h['key'] in fz_verdict and fz_verdict[h['key']] != 'same':
                continue
            conf = 0.85 if h['key'] in fz_verdict else 0.9 if h['sim'] >= 0.9 else 0.6
            m = dict(h, kind={'informal': 'article'}.get(h['kind'], h['kind']), publtype='informal' if h['kind'] == 'informal' else '')
            c = from_dblp(m, 'dblp-search', conf, f"dblp {h['key']} (search; sim {h['sim']}: {h['title'][:80]})")
            c['fuzzy'] = h
            cands.append(c)
            seen_keys.add(h['key'])
            if conf >= 0.85:
                dblp_owner[h['key']].append((i, f"search sim {h['sim']}"))
        # Crossref for the item's DOI
        cr = cross.get(row['doi'].lower()) if row['doi'] else None
        if cr:
            sim = tsim(cr.get('title', ''), row['title'])
            if sim < 0.5 and cr.get('title'):
                flags.append({'id': i, 'flag': 'doi-title-mismatch', 'detail':
                              f"DOI {row['doi']} is titled {cr.get('title', '')[:100]!r} in Crossref ({cr.get('container', '')})"})
            else:
                cands.append(from_crossref(cr, 0.95))
        # zbMATH venue
        if i.startswith('zb:') and row['venue'].strip():
            reg = reg_by_name(row['venue'])
            cands.append(cand('zbmath', 0.9, row['venue'].strip(), reg['kind'] if reg else 'journal', year, row['doi'],
                              reg, 'zbmath ' + i[3:], reg['refereed'] if reg else 'likely'))
        # OpenAlex locations
        if i in oalex:
            w = oalex[i]
            if tsim(w.get('title') or '', row['title']) >= 0.5:
                cands += from_openalex(w, 0.8)
        # OpenAlex title search (fetch_openalex_title_search.py): separate published works
        for h in oasearch.get(i, []):
            if h['oa_id'] == i or tsim(h['title'], row['title']) < 0.85:
                continue
            shared = authors & lastnames(h['authors'])
            if authors and h['authors'] and not shared:
                continue
            if year and h['year'] and not (year - 3 <= h['year'] <= year + 8):
                continue
            if h['oa_id'] in counted_ids:
                oa_owner[h['oa_id']].append(i)
            hc = from_openalex({'id': h['oa_id'], 'year': h['year'], 'doi': h['doi'], 'primary': h['primary'],
                                'locations': h['locations']}, 0.8)
            for c in hc:
                c['src'] = 'openalex-search'
            cands += hc
        # ePrint publication info (a DOI given there is looked up in Crossref)
        pdoi = pubinfo.get(i, {}).get('doi', '').lower()
        if pdoi and pdoi in cross:
            cands.append(dict(from_crossref(cross[pdoi], 0.9), src='crossref-eprint-doi'))
        if i in pubinfo:
            c, raw = from_pubinfo(pubinfo[i])
            if c:
                cands.append(c)
            elif raw and not NOPUB.search(raw.strip()):
                flags.append({'id': i, 'flag': 'eprint-pubinfo-unparsed', 'detail': raw[:240]})
        # export venue string (fallback)
        c = from_export(row, 0.6)
        if c and not cands:
            cands.append(c)
        # manual
        if i in manual:
            mrow = manual[i]
            reg = next((r for r in REG if r['vid'] == mrow.get('vid')), None) or reg_by_name(mrow.get('pub_venue', ''))
            cm = cand('manual', float(mrow.get('confidence') or 1), mrow['pub_venue'], mrow.get('pub_type') or
                      (reg['kind'] if reg else 'other'), int(mrow['pub_year']) if mrow.get('pub_year', '').isdigit() else None,
                      mrow.get('pub_doi', ''), reg, mrow.get('evidence', 'manual'), mrow.get('refereed') or
                      (reg['refereed'] if reg else ''))
            cm['display'] = mrow['pub_venue']
            cands.insert(0, cm)

        # choose: refereed published versions first (earliest year, then confidence), else best non-refereed
        refd = [c for c in cands if c['refereed'] in ('yes', 'likely', 'thesis') and c['kind'] not in ('preprint', 'report')]
        if any(c['src'] == 'manual' for c in cands):
            best = cands[0]
        elif refd:
            # group by venue identity; confidence of a venue = max over its sources (+ agreement bonus)
            groups = collections.OrderedDict()
            for c in refd:
                vkey = c['reg']['vid'] if c['reg'] else norm(c['raw'])[:40]
                groups.setdefault(vkey, []).append(c)
            ranked = []
            for vkey, cs in groups.items():
                top = max(cs, key=lambda c: c['conf'])
                srcs = {c['src'] for c in cs}
                conf = min(1.0, top['conf'] + 0.03 * (len(srcs) - 1))
                yr = min((c['year'] for c in cs if c['year']), default=None)
                kind_rank = {'thesis': 2}.get(top['kind'], 0)  # a thesis only if nothing else
                named = [c for c in cs if c['raw'] or c['reg']]
                top = max(named or cs, key=lambda c: c['conf'])  # prefer a source that names the venue
                if not (top['raw'] or top['reg']):
                    kind_rank += 1
                ranked.append((kind_rank, -conf if conf < 0.9 else -0.9, yr or 9999, vkey, top, conf, srcs, yr))
            ranked.sort(key=lambda t: t[:4])
            _, _, _, _, best, conf, srcs, yr = ranked[0]
            best = dict(best, conf=conf, year=yr or best['year'], agree=sorted(srcs))
            others = [t[4] for t in ranked[1:]]
        else:
            best = max(cands, key=lambda c: c['conf']) if cands else None
            others = []
        if best is None and idtype == 'eprint' and i in pubinfo:
            # ePrint item: DBLP and the ePrint page were both checked and name no published version
            out.append({'id': i, 'idtype': idtype, 'pub_venue': '', 'pub_type': 'preprint', 'pub_year': '',
                        'pub_doi': '', 'confidence': '', 'evidence': 'ePrint only: no published version in DBLP '
                        'or ePrint publication info' + (' (dblp-checked)' if dblpm else ''), 'vid': 'eprint',
                        'refereed': 'no', 'venue_kind': 'preprint', 'core2023': '', 'other_versions': '',
                        'n_sources': 0, 'notes': '; '.join(notes)[:300]})
            continue
        if best is None and i in oalex and oalex[i].get('type') == 'dissertation':
            best = cand('openalex', 0.7, 'Dissertation (institution not recorded)', 'thesis', year, '', None,
                        f'openalex {i} type dissertation, no host', 'thesis')
        if best is None:
            stats['unresolved'] += 1
            out.append({'id': i, 'idtype': idtype, 'pub_venue': '', 'pub_type': '', 'pub_year': '', 'pub_doi': '',
                        'confidence': '', 'evidence': 'no venue source', 'vid': '', 'refereed': 'unknown',
                        'venue_kind': '', 'core2023': '', 'other_versions': '', 'n_sources': 0, 'notes': '; '.join(notes)})
            continue
        if i in oalex and oalex[i].get('type') == 'dissertation' and best['kind'] in ('preprint', 'report', 'other') \
                and best['src'] in ('openalex', 'export-venue'):
            # a dissertation held in a repository: OpenAlex's work type says thesis
            best = dict(best, kind='thesis', refereed='thesis', detail=best['detail'] + ' [OpenAlex type: dissertation]')
        refereed = best['refereed'] or 'unknown'
        if best['kind'] in ('preprint', 'report'):
            refereed = 'no'
        if best['conf'] < 0.7 and refereed in ('yes', 'likely'):
            refereed = 'unverified'  # only a weak (e.g. fuzzy-title) candidate; needs checking
        pv = html.unescape(best.get('display') or display(best))
        if re.fullmatch(r'(?i)lecture notes in computer science|springer ebooks|lncs', pv.strip()):
            flags.append({'id': i, 'flag': 'series-only-venue', 'detail': f'only the series name is known ({best["detail"][:80]})'})
        out.append({
            'id': i, 'idtype': idtype, 'pub_venue': pv, 'pub_type': pub_type(best),
            'pub_year': best['year'] or '', 'pub_doi': best['doi'] if not EPRINT.match(i) or best['src'] != 'eprint-pubinfo' else best['doi'],
            'confidence': f"{best['conf']:.2f}", 'evidence': best['detail'] + (' [+' + ','.join(best.get('agree', [])) + ']'
                                                                         if len(best.get('agree', [])) > 1 else ''),
            'vid': best['reg']['vid'] if best['reg'] else '', 'refereed': refereed,
            'venue_kind': best['kind'], 'core2023': best['reg']['core'] if best['reg'] else '',
            'other_versions': ' | '.join(sorted({display(c) + (f' ({c["year"]})' if c['year'] else '') for c in others}))[:300],
            'n_sources': len({c['src'] for c in cands}), 'notes': '; '.join(notes)[:300]})
        stats['resolved'] += 1
        # year conflicts: some source dates the work 2+ years BEFORE the counted year (a later published
        # version of an earlier preprint is normal and not flagged)
        if best.get('fuzzy') and best['conf'] < 0.85:
            m = best['fuzzy']
            flags.append({'id': i, 'flag': 'fuzzy-dblp-match' if best['src'] == 'dblp-fuzzy' else 'weak-dblp-search-match', 'detail':
                          f"sim {m['sim']}: {row['title'][:90]!r} vs {m['title'][:90]!r} [{m['key']}]"})
        early = min((c for c in cands if c['year'] and c['conf'] >= 0.85), key=lambda c: c['year'], default=None)
        if year and early and early['year'] <= year - 2:
            flags.append({'id': i, 'flag': 'year-earlier-than-counted', 'detail':
                          f"counted year {year}; {display(early)} gives {early['year']} ({early['detail'][:80]})"})

    for key, hits in dblp_owner.items():
        ids = sorted({h[0] for h in hits})
        if len(ids) > 1:
            how = ', '.join(f'{a} ({b})' for a, b in sorted(set(hits)))
            flags.append({'id': ' + '.join(ids), 'flag': 'possible-duplicate',
                          'detail': f'all match DBLP record {key}: {how}'})

    for oa, ids in oa_owner.items():
        flags.append({'id': ' + '.join(sorted(set(ids) | {oa})), 'flag': 'possible-duplicate',
                      'detail': f'OpenAlex title search for the first item returns counted work {oa}'})
    cols = ['id', 'idtype', 'pub_venue', 'pub_type', 'pub_year', 'pub_doi', 'confidence', 'evidence', 'vid',
            'refereed', 'venue_kind', 'core2023', 'other_versions', 'n_sources', 'notes']
    with open(V / 'published_venues.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(out)
    with open(V / 'venue_flags.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['flag', 'id', 'detail'])
        w.writeheader()
        w.writerows(sorted(flags, key=lambda x: (x['flag'], x['id'])))
    report(rows, out, flags)


def report(rows, out, flags):
    byid = {o['id']: o for o in out}
    L = ['# Venue resolution for counted items', '',
         'Generated by `pipeline/build_venue_table.py`; identification only (no reputation judgment).', '',
         f'Counted items: {len(rows)}. Flags: ' + ', '.join(f'{k} {v}' for k, v in
                                                           collections.Counter(f["flag"] for f in flags).most_common()) + '.', '']

    def tab(title, keyf):
        L.append(f'## {title}\n')
        groups = collections.defaultdict(collections.Counter)
        for r in rows:
            o = byid[r['id']]
            groups[keyf(r, o)][o['refereed']] += 1
        cats = ['yes', 'likely', 'unverified', 'thesis', 'no', 'unknown']
        L.append('| | n | ' + ' | '.join(cats) + ' |')
        L.append('|---|---:|' + '---:|' * len(cats))
        for g in sorted(groups):
            c = groups[g]
            L.append(f'| {g} | {sum(c.values())} | ' + ' | '.join(str(c[k]) for k in cats) + ' |')
        L.append('')

    L.append('Columns: refereed = venue registered as peer-reviewed; likely = peer-reviewed by source type but venue '
             'not in the registry; unverified = only a weak candidate (e.g. fuzzy title match); thesis; no = preprint/report '
             'only (for ePrint: no published version found in DBLP or the ePrint page); unknown = no usable venue source.\n')
    tab('By id type', lambda r, o: o['idtype'])
    tab('By evidence source', lambda r, o: o['evidence'].split(' ')[0] if o['evidence'] else '-')
    L.append('## By class (fractional weights)\n')
    cats = ['yes', 'likely', 'unverified', 'thesis', 'no', 'unknown']
    L.append('| class | weighted n | ' + ' | '.join(cats) + ' |')
    L.append('|---|---:|' + '---:|' * len(cats))
    for label, ws in CLASSES:
        c = collections.Counter()
        for r in rows:
            w = sum(float(r[x] or 0) for x in ws)
            if w:
                c[byid[r['id']]['refereed']] += w
        L.append(f'| {label} | {sum(c.values()):.1f} | ' + ' | '.join(f'{c[k]:.1f}' for k in cats) + ' |')
    L.append('')
    unreg = collections.Counter(o['pub_venue'] for o in out if o['refereed'] == 'likely')
    L.append('## Most common refereed-by-type venues not in the registry\n')
    for v, n in unreg.most_common(40):
        L.append(f'- {n} {v}')
    (ROOT / 'analysis/venue_resolution.md').write_text('\n'.join(L) + '\n')
    print('\n'.join(L[:60]))


if __name__ == '__main__':
    main()
