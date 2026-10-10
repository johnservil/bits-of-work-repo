#!/usr/bin/env python3
"""OpenAlex title search for counted items that still lack a refereed venue.

Run from the repo root:  python3 -I pipeline/fetch_openalex_title_search.py ids.txt [out.jsonl]

ids.txt: one counted id per line (e.g. rows of data/venues/published_venues.csv with refereed
no/unknown/unverified). OpenAlex often keeps a preprint and its published version as separate
works; this finds the latter. Output (default data/raw/openalex_title_search/hits.jsonl), resumable:
  {"id", "query", "hits": [{"oa_id", "doi", "title", "year", "type", "authors", "primary": loc,
                            "locations": [loc...]}...]}
loc as in fetch_openalex_locations.py. Cost: 10 credits per query (title.search filter).
Uses ~/.openalex_key if present (never printed). Stdlib only.
"""
import csv, json, os, re, sys, time, urllib.request, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDS = Path(sys.argv[1])
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / 'data/raw/openalex_title_search/hits.jsonl'
MAILTO = 'matthewdgreen@gmail.com'
UA = {'User-Agent': f'literature-search-pilot/0.2 (mailto:{MAILTO})'}
FIELDS = 'id,doi,title,publication_year,type,primary_location,locations,authorships'
sys.path.insert(0, str(ROOT / 'pipeline'))
from fetch_openalex_locations import loc, key  # noqa: E402


def get(url):
    k = key()
    full = url + '&mailto=' + MAILTO + (f'&api_key={k}' if k else '')
    for wait in (5, 30, 120, None):
        try:
            with urllib.request.urlopen(urllib.request.Request(full, headers=UA), timeout=60) as r:
                return json.load(r)
        except Exception as e:
            if wait is None:
                raise SystemExit(f'giving up on {url}: {type(e).__name__}')  # url has no key
            time.sleep(wait)


def main():
    rows = {r['id']: r for r in csv.DictReader(open(ROOT / 'data/export/combined_included.csv'))}
    ids = [l.strip() for l in open(IDS) if l.strip() in rows]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    done = {json.loads(l)['id'] for l in open(OUT)} if OUT.exists() else set()
    todo = [i for i in ids if i not in done]
    print(f'{len(done)} done, {len(todo)} to query (~{10 * len(todo)} credits)', file=sys.stderr)
    with open(OUT, 'a') as out:
        for n, i in enumerate(todo):
            t = re.sub(r'\$[^$]*\$', ' ', rows[i]['title'])
            q = ' '.join(re.findall(r'[A-Za-z0-9]+', t)[:20])
            if len(q) < 10:
                continue
            j = get('https://api.openalex.org/works?filter=title.search:' + urllib.parse.quote(q) +
                    f'&select={FIELDS}&per-page=8')
            hits = []
            for w in j.get('results', []):
                hits.append({'oa_id': w['id'].rsplit('/', 1)[-1], 'doi': (w.get('doi') or '').replace('https://doi.org/', ''),
                             'title': w.get('title') or '', 'year': w.get('publication_year'), 'type': w.get('type'),
                             'authors': [(a.get('author') or {}).get('display_name', '') for a in w.get('authorships') or []],
                             'primary': loc(w.get('primary_location')), 'locations': [loc(l) for l in w.get('locations') or []]})
            out.write(json.dumps({'id': i, 'query': q, 'hits': hits}, ensure_ascii=False) + '\n')
            out.flush()
            if n % 50 == 0:
                print(n, i, len(hits), file=sys.stderr)
            time.sleep(0.3)


if __name__ == '__main__':
    main()
