#!/usr/bin/env python3
"""Looser offline DBLP search for counted items that still lack a refereed venue.

Run from the repo root:
  python3 -I pipeline/search_dblp_local.py DBLP_XML_GZ DBLP_DTD [ids.txt] [out.jsonl]

Default ids: rows of data/venues/published_venues.csv whose refereed is no/unknown/unverified
(run build_venue_table.py first). Looser than match_dblp_versions.py: a DBLP record is a hit if
  - it shares >= 1 author last name with the item and title Dice similarity >= 0.6, or
  - the item has no authors and the DBLP title starts with the item's normalized title
    (>= 25 chars; catches truncated OpenAlex titles) or has Dice >= 0.9.
Output (default data/venues/dblp_search.jsonl), one line per item with hits:
  {"id", "hits": [{"key", "kind", "venue", "year", "doi", "authors", "title", "sim"}...]}
build_venue_table.py applies the author/year/similarity rules and confidence. (The DBLP search
API now sits behind a bot check, so this runs on the dump.) Stdlib only.
"""
import csv, gzip, json, re, sys, unicodedata
from pathlib import Path
from xml.etree.ElementTree import XMLParser

ROOT = Path(__file__).resolve().parent.parent
SRC, DTD = sys.argv[1], sys.argv[2]
IDS = Path(sys.argv[3]) if len(sys.argv) > 3 else None
OUT = Path(sys.argv[4]) if len(sys.argv) > 4 else ROOT / 'data/venues/dblp_search.jsonl'
KINDS = {'article', 'inproceedings', 'incollection', 'phdthesis', 'mastersthesis', 'book'}


def norm(t):
    t = unicodedata.normalize('NFKD', t or '')
    t = re.sub(r'\$[^$]*\$', lambda m: re.sub(r'\\[a-zA-Z]+|[{}^_\\]', '', m[0]), t)
    return re.sub(r'[^a-z0-9]', '', re.sub(r'<[^>]+>', '', t).lower())


def lastname(a):
    a = re.sub(r'\s+\d{4}$', '', a.strip())
    a = a.split(',')[0] if ',' in a else (a.split() or [''])[-1]
    return re.sub(r'[^a-z]', '', unicodedata.normalize('NFKD', a).lower())


def grams(t):
    return {t[i:i + 3] for i in range(len(t) - 2)}


rows = {r['id']: r for r in csv.DictReader(open(ROOT / 'data/export/combined_included.csv'))}
if IDS:
    ids = [l.strip() for l in open(IDS) if l.strip()]
else:
    ids = [o['id'] for o in csv.DictReader(open(ROOT / 'data/venues/published_venues.csv'))
           if o['refereed'] in ('no', 'unknown', 'unverified')]
items, by_last, noauth = {}, {}, {}
for i in ids:
    r = rows[i]
    k = norm(r['title'])
    if len(k) < 12:
        continue
    ln = {x for x in (lastname(a) for a in r['authors'].split(';')) if len(x) > 1}
    items[i] = (ln, grams(k), k)
    for x in ln:
        by_last.setdefault(x, set()).add(i)
    if not ln:
        noauth[i] = k
print(f'{len(items)} items ({len(noauth)} without authors)', file=sys.stderr)
found = {}


class Target:
    def __init__(self):
        self.cur, self.text, self.n = None, '', 0

    def start(self, tag, attrib):
        if tag in KINDS and self.cur is None:
            self.cur = {'kind': tag, 'key': attrib.get('key'), 'authors': [], 'title': '', 'year': None,
                        'venue': '', 'doi': '', 'publtype': attrib.get('publtype', '')}
        self.text = ''

    def data(self, d):
        self.text += d

    def end(self, tag):
        c = self.cur
        if c is None:
            return
        if tag == 'author':
            c['authors'].append(self.text.strip())
        elif tag == 'title':
            c['title'] = re.sub(r'\s+', ' ', self.text).strip().rstrip('.')
        elif tag == 'year':
            c['year'] = int(self.text) if self.text.strip().isdigit() else None
        elif tag in ('journal', 'booktitle', 'school') and not c['venue']:
            c['venue'] = self.text.strip()
        elif tag == 'ee' and 'doi.org/' in self.text and not c['doi']:
            c['doi'] = self.text.strip().split('doi.org/')[-1]
        elif tag == c['kind']:
            self.n += 1
            k = None
            cand = set()
            for a in c['authors']:
                cand |= by_last.get(lastname(a), set())
            for i in cand:
                k = k or norm(c['title'])
                g = grams(k)
                ig = items[i][1]
                sim = 2 * len(ig & g) / max(1, len(ig) + len(g))
                if sim >= 0.6:
                    self.hit(i, c, sim)
            if noauth:
                k = k or norm(c['title'])
                for i, ik in noauth.items():
                    if (len(ik) >= 25 and k.startswith(ik)) or (abs(len(k) - len(ik)) < 20 and k[:20] == ik[:20]):
                        g = grams(k)
                        sim = 2 * len(items[i][1] & g) / max(1, len(items[i][1]) + len(g))
                        self.hit(i, c, max(sim, 0.9 if k.startswith(ik) else sim))
            self.cur = None
            if self.n % 2000000 == 0:
                print(f'  {self.n} records, {len(found)} items with hits', file=sys.stderr, flush=True)
        self.text = ''

    def hit(self, i, c, sim):
        h = {x: c[x] for x in ('key', 'kind', 'venue', 'year', 'doi', 'authors', 'title')}
        h['kind'] = 'informal' if c['publtype'] == 'informal' else c['kind']
        h['sim'] = round(sim, 3)
        found.setdefault(i, []).append(h)

    def close(self):
        return self.n


ENT = {m[1]: chr(int(m[2])) for m in re.finditer(r'<!ENTITY\s+(\w+)\s+"&#(\d+);"\s*>', open(DTD, encoding='latin-1').read())}
t = Target()
p = XMLParser(target=t, encoding='ISO-8859-1')
p.entity.update(ENT)
with gzip.open(SRC, 'rb') as f:
    while chunk := f.read(1 << 20):
        p.feed(chunk)
p.close()
with open(OUT, 'w') as out:
    for i in sorted(found):
        out.write(json.dumps({'id': i, 'hits': found[i]}, ensure_ascii=False) + '\n')
print(f'parsed {t.n}; {len(found)} items with hits', file=sys.stderr)
