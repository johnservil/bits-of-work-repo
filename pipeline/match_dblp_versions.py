#!/usr/bin/env python3
"""Find every DBLP record whose title matches a counted item (to locate published versions).

Run from the repo root:
  python3 -I pipeline/match_dblp_versions.py DBLP_XML_GZ DBLP_DTD [out.jsonl]

Input: counted rows of data/export/combined_included.csv (include = yes, category A-F/H).
Output (default data/venues/dblp_matches.jsonl), one line per counted item that has at
least one DBLP record with the same normalized title:
  {"id", "matches": [{"key", "kind", "venue", "year", "doi", "authors"}...]}
Titles are normalized by dropping TeX, punctuation, case and whitespace. Whether a match is
really the same paper (author overlap, year) is decided later by build_venue_table.py.
A second, fuzzy pass catches retitled versions: a DBLP record sharing at least min(2, #authors)
author last names with an item, dated within [year-3, year+8], and with character-trigram
Dice title similarity >= 0.5 is written as {"fuzzy": true, "sim": ...} in the same list.
Stdlib only.
"""
import csv, gzip, json, re, sys, unicodedata
from pathlib import Path
from xml.etree.ElementTree import XMLParser

ROOT = Path(__file__).resolve().parent.parent
SRC, DTD = sys.argv[1], sys.argv[2]
OUT = Path(sys.argv[3]) if len(sys.argv) > 3 else ROOT / 'data/venues/dblp_matches.jsonl'
KINDS = {'article', 'inproceedings', 'incollection', 'phdthesis', 'mastersthesis', 'book', 'proceedings'}


def norm_title(t):
    t = unicodedata.normalize('NFKD', t)
    t = re.sub(r'\$[^$]*\$', lambda m: re.sub(r'\\[a-zA-Z]+|[{}^_\\]', '', m[0]), t)
    t = re.sub(r'<[^>]+>', '', t)
    return re.sub(r'[^a-z0-9]', '', t.lower())


def lastname(a):
    a = re.sub(r'\s+\d{4}$', '', a.strip())
    a = a.split(',')[0] if ',' in a else (a.split() or [''])[-1]
    return re.sub(r'[^a-z]', '', unicodedata.normalize('NFKD', a).lower())


def grams(t):
    return {t[i:i + 3] for i in range(len(t) - 2)}


want, items, by_last = {}, {}, {}
for r in csv.DictReader(open(ROOT / 'data/export/combined_included.csv')):
    if r['include'] == 'yes' and r['category'] in set('ABCDEFH'):
        k = norm_title(r['title'])
        if len(k) >= 12:
            want.setdefault(k, []).append(r['id'])
        ln = {x for x in (lastname(a) for a in r['authors'].split(';')) if len(x) > 1}
        if ln and len(k) >= 12:
            items[r['id']] = (ln, int(r['year']) if r['year'].isdigit() else None, grams(k), k)
            for x in ln:
                by_last.setdefault(x, set()).add(r['id'])
print(f'{sum(map(len, want.values()))} items, {len(want)} distinct titles', file=sys.stderr)

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
            k = norm_title(c['title'])
            rec = None
            if k in want:
                rec = {x: c[x] for x in ('key', 'kind', 'venue', 'year', 'doi', 'authors', 'publtype')}
                for i in want[k]:
                    found.setdefault(i, []).append(rec)
            ln = {lastname(a) for a in c['authors']}
            hits = {}
            for x in ln:
                for i in by_last.get(x, ()):
                    hits[i] = hits.get(i, 0) + 1
            for i, n in hits.items():
                iln, iy, ig, ik = items[i]
                if n < min(2, len(iln)) or ik == k or (iy and c['year'] and not iy - 3 <= c['year'] <= iy + 8):
                    continue
                g = grams(k)
                sim = 2 * len(ig & g) / max(1, len(ig) + len(g))  # Dice on character trigrams
                if sim >= 0.5:
                    r2 = {x: c[x] for x in ('key', 'kind', 'venue', 'year', 'doi', 'authors', 'publtype')}
                    r2.update(fuzzy=True, sim=round(sim, 3), title=c['title'])
                    found.setdefault(i, []).append(r2)
            self.cur = None
            if self.n % 1000000 == 0:
                print(f'  {self.n} records, {len(found)} items matched', file=sys.stderr, flush=True)
        self.text = ''

    def close(self):
        return self.n


ENT = {m[1]: chr(int(m[2])) for m in re.finditer(r'<!ENTITY\s+(\w+)\s+"&#(\d+);"\s*>', open(DTD, encoding='latin-1').read())}
target = Target()
parser = XMLParser(target=target, encoding='ISO-8859-1')
parser.entity.update(ENT)
with gzip.open(SRC, 'rb') as f:
    while chunk := f.read(1 << 20):
        parser.feed(chunk)
parser.close()
OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, 'w') as out:
    for i in sorted(found):
        out.write(json.dumps({'id': i, 'matches': found[i]}, ensure_ascii=False) + '\n')
print(f'parsed {target.n} records; {len(found)} items matched', file=sys.stderr)
