#!/usr/bin/env python3
"""Build docs/assets/people-data.js for the researcher explorer (docs/people.html).

Stdlib only. Run from the repo root:  python3 -I pipeline/build_people_data.py

Who wrote what comes from data/authors/authorships.csv (the author map); class weights, inclusion and
version weights come from the current labels in data/export/combined_included.csv, so a person's paper
credit (class weight x version weight / number of authors) sums to the paper counts on the summary page.

Unmatched name strings that differ from exactly one DBLP person only by Unicode dashes, "Last, First" order or a
kept DBLP homonym number are merged into that person (see merge_split_names). The author map itself does not
do this yet, so its FTE figures still treat them as separate people.

People with fewer than NAMED_MIN counted items are written without a name: they still enter totals,
counts and concentration shares, but the page never ranks or lists them individually. The same applies to
identities on an ambiguous name (see ambiguous_ids): DBLP disambiguation pages, catch-all profiles of very common
Chinese names, and unmatched Chinese name strings, any of which can pool several people.
"""
from pathlib import Path
import csv, json, re, sys, datetime, collections

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'pipeline'))
from authors_dblp import full_norm  # noqa: E402  (the author map's key for unmatched names)
OUT = ROOT / 'docs/assets/people-data.js'
EFFORT_CATS = set('ABCDEFH')     # same inclusion rule as build_site_data.py
Y0, Y1 = 1970, 2026
NAMED_MIN = 3                    # counted items (any class) needed to appear by name
CATCHALL_PUBS = 400              # an unnumbered DBLP profile of a common Chinese name this large likely pools people
NAME_ONLY = {'exact', 'fuzzy_crypto'}   # author-map methods that matched a DBLP person by name string, not by record
# Common pinyin surnames; a romanized name ending in one is treated as a likely Chinese name.
SURNAMES = set('''wang li zhang liu chen yang huang zhao wu zhou xu sun ma zhu hu guo he gao lin luo zheng liang xie
    song tang han feng deng cao peng zeng xiao tian dong pan yuan cai jiang yu du ye cheng wei su lu ding ren shen yao
    jin fu zhong cui tan liao fan wan qian dai qin jia gu xue hou meng long duan lei hao kong shao shi mao chang qiu lai
    jiao wen yin yan xiang bai ni niu kang tao fang qi xing mo ou geng zou hong'''.split())

# Site class keys -> label, export weight columns
CLASSES = [
    ('lattice',   'All lattices',       ['w_MLWE_structured', 'w_LWE_plain']),
    ('ecdlp',     'ECDLP',              ['w_ECDLP']),
    ('code',      'Syndrome decoding',  ['w_SD_code']),
    ('factoring', 'Factoring / FF-DLP', ['w_Factoring_FFDLP']),
    ('isogeny',   'Isogenies',          ['w_Isogeny']),
    ('mq',        'Multivariate',       ['w_Multivariate']),
    ('mlwe',      'MLWE / structured',  ['w_MLWE_structured']),
    ('lwe',       'Plain LWE',          ['w_LWE_plain']),
]


def bib_keys():
    """studyid -> BibTeX key (the bibliography page's <li id>)."""
    keys, key = {}, None
    for line in (ROOT / 'docs/bibliography.bib').open():
        m = re.match(r'@\w+\{([^,]+),', line)
        if m:
            key = m.group(1)
        m = re.match(r'\s*studyid\s*=\s*\{(.*)\},?\s*$', line)
        if m and key:
            keys[m.group(1)] = key
    return keys


def spelling_variants(name):
    """Forms the author map's full_norm misses: Unicode dashes and 'Last, First' order."""
    s = re.sub(r'[\u2010\u2011\u2012\u2013\u2014\u2212]', '-', name)
    if s.count(',') == 1:
        last, first = (x.strip() for x in s.split(','))
        if first and last:
            s = f'{first} {last}'
    return s


def chinese_name(name):
    t = re.sub(r'\s+\d{4}$', '', name).replace('-', ' ').split()
    return len(t) >= 2 and t[-1].lower() in SURNAMES and all(re.fullmatch(r'[A-Za-z]+', x) for x in t)


def ambiguous_ids(authors):
    """Author-map identities whose name may pool several people. Without the DBLP dump's disambiguation notes:
    (a) an unnumbered DBLP profile whose name also appears with a DBLP number (DBLP has split that name, so the
        unnumbered profile is its disambiguation page);
    (b) an unnumbered DBLP profile of a Chinese name with more than CATCHALL_PUBS publications;
    (c) an unmatched Chinese name string (identity by spelling alone)."""
    base = lambda p: full_norm(re.sub(r'^name:', '', re.sub(r'\s+\d{4}$', '', p)))
    numbered = {base(p) for p in authors if re.search(r'\s\d{4}$', p)}
    out = set()
    for p, r in authors.items():
        unnumbered = not re.search(r'\s\d{4}$', p)
        if p.startswith('name:'):
            if chinese_name(r['name']):
                out.add(p)
        elif unnumbered and base(p) and base(p) in numbered:
            out.add(p)
        elif unnumbered and chinese_name(p) and int(r.get('dblp_pubs') or 0) > CATCHALL_PUBS:
            out.add(p)
    return out


def merge_split_names(authors, raw, avoid=frozenset()):
    """unmatched person id -> DBLP person id, when the spellings point to exactly one DBLP person."""
    idx = collections.defaultdict(set)
    for p, r in authors.items():
        if not p.startswith('name:'):
            idx[full_norm(r['name'])].add(p)
    alias = {}
    for p in authors:
        if not p.startswith('name:'):
            continue
        hit = set()
        for form in raw.get(p, ()):
            hit |= {form} if form in authors and not form.startswith('name:') else idx.get(full_norm(spelling_variants(form)), set())
        if len(hit) == 1 and not hit & avoid:
            alias[p] = next(iter(hit))
    return alias


def main():
    labels = {r['id']: r for r in csv.DictReader((ROOT / 'data/export/combined_included.csv').open())}
    authors = {r['person']: r for r in csv.DictReader((ROOT / 'data/authors/authors.csv').open())}
    # unmatched people are keyed by a normalized string; keep the spellings seen in the records
    raw = collections.defaultdict(collections.Counter)
    for L in labels.values():
        for a in L['authors'].split(';'):
            a = re.sub(r'\s+', ' ', a).strip()
            if a:
                raw['name:' + full_norm(a)][a] += 1
    amb = ambiguous_ids(authors)
    alias = merge_split_names(authors, raw, avoid=amb)
    by_item = collections.defaultdict(list)
    name_only = collections.defaultdict(set)   # person -> items matched to them by name string only
    for r in csv.DictReader((ROOT / 'data/authors/authorships.csv').open()):
        p = alias.get(r['person'], r['person'])
        if p not in by_item[r['item_id']]:
            by_item[r['item_id']].append(p)
        if r['resolution'] in NAME_ONLY or r['person'] in alias:
            name_only[p].add(r['item_id'])
    keys = bib_keys()

    papers, pidx, people, item_of = [], {}, [], []
    skipped = collections.Counter()
    for iid, L in labels.items():
        if L['include'] != 'yes' or L['category'] not in EFFORT_CATS:
            continue
        vw = float(L.get('version_weight') or 1)
        if vw <= 0:
            skipped['duplicate version'] += 1
            continue
        if not L['year'] or not (Y0 <= int(L['year']) <= Y1):
            skipped['no chart year'] += 1
            continue
        if iid not in by_item:
            skipped['no author record'] += 1
            continue
        a = []
        for p in by_item[iid]:
            if p not in pidx:
                pidx[p] = len(people)
                people.append(p)
            a.append(pidx[p])
        w = [round(sum(float(L[c] or 0) for c in cols) * vw, 4) for _, _, cols in CLASSES]
        papers.append({'k': keys.get(iid, ''), 't': L['title'], 'y': int(L['year']), 'w': w, 'a': a,
                       **({'q': 1} if L.get('quantum') == 'True' else {})})
        item_of.append(iid)

    n_items = collections.Counter(i for p in papers for i in p['a'])
    counted = collections.defaultdict(set)
    for p, iid in zip(papers, item_of):
        for i in p['a']:
            counted[i].add(iid)
    withheld = 0
    seen = collections.Counter()
    out_people = []
    for i, p in enumerate(people):
        A = authors.get(p, {})
        named = n_items[i] >= NAMED_MIN and p not in amb
        withheld += n_items[i] >= NAMED_MIN and p in amb
        rec = {'n': None}
        if named:
            name = A.get('name') or re.sub(r'^name:', '', p)
            if p.startswith('name:') and raw.get(p):
                name = re.sub(r'\s+\d{4}$', '', spelling_variants(raw[p].most_common(1)[0][0]))
            seen[name] += 1
            rec = {'n': name,
                   'r': 'u' if A.get('resolution') == 'unresolved' else 'd',
                   'pid': A.get('dblp_pid') or None,
                   'af': (A.get('affiliation') or '').split(';')[0].strip() or None}
            if p.startswith('name:'):
                rec['nm'] = n_items[i]
            elif name_only[p] & counted[i]:
                rec['nm'] = len(name_only[p] & counted[i])
        out_people.append(rec)
    dup = {n for n, c in seen.items() if c > 1}
    for rec in out_people:
        if rec['n'] in dup:
            rec['h'] = 1   # homonym: the page shows the DBLP id to tell them apart

    data = {
        'generated': datetime.date.today().isoformat(),
        'y0': Y0, 'y1': Y1, 'named_min': NAMED_MIN, 'ambiguous_withheld': withheld,
        'classes': [{'key': k, 'label': l} for k, l, _ in CLASSES],
        'people': out_people,
        'papers': papers,
        'skipped': dict(skipped),
    }
    OUT.write_text('// Generated by pipeline/build_people_data.py; do not edit.\n'
                   'window.PEOPLE_DATA = ' + json.dumps(data, separators=(',', ':'), ensure_ascii=False) + ';\n')
    print(f'wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size:,} bytes): {len(papers)} papers, '
          f'{len(people)} people ({sum(r["n"] is not None for r in out_people)} named, {withheld} withheld as ambiguous), '
          f'{len(alias)} split names merged; '
          f'skipped {dict(skipped)}')


if __name__ == '__main__':
    main()
