#!/usr/bin/env python3
"""Fetch OpenAlex locations (every host of a work, with source metadata) for counted items.

Run from the repo root:  python3 -I pipeline/fetch_openalex_locations.py [ids.txt] [out.jsonl]

Default input: OpenAlex-only counted rows (id = W...) of data/export/combined_included.csv.
An optional ids.txt (one OpenAlex W id per line) replaces that list.
Output (default data/raw/openalex_locations/works.jsonl), resumable, one line per work:
  {"id", "doi", "title", "year", "type", "primary": loc, "locations": [loc...]}
  loc = {"source_id", "source", "source_type", "issn_l", "host", "is_core", "is_in_doaj",
         "version", "is_published", "landing"}
Batched filter=openalex_id (50 per page, 1 credit/page). Uses ~/.openalex_key if present
(never printed). Stdlib only.
"""
import csv, json, os, sys, time, urllib.request, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDS = Path(sys.argv[1]) if len(sys.argv) > 1 else None
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / 'data/raw/openalex_locations/works.jsonl'
MAILTO = 'matthewdgreen@gmail.com'
UA = {'User-Agent': f'literature-search-pilot/0.2 (mailto:{MAILTO})'}
FIELDS = 'id,doi,title,publication_year,type,primary_location,locations'


def key():
    try:
        return open(os.path.expanduser('~/.openalex_key')).read().strip() or None
    except OSError:
        return None


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


def loc(l):
    s = (l or {}).get('source') or {}
    return {'source_id': (s.get('id') or '').rsplit('/', 1)[-1], 'source': s.get('display_name') or '',
            'source_type': s.get('type') or '', 'issn_l': s.get('issn_l') or '',
            'host': s.get('host_organization_name') or '', 'is_core': s.get('is_core'),
            'is_in_doaj': s.get('is_in_doaj'), 'version': (l or {}).get('version'),
            'is_published': (l or {}).get('is_published'), 'landing': (l or {}).get('landing_page_url')}


def main():
    if IDS:
        ids = [l.strip() for l in open(IDS) if l.strip()]
    else:
        ids = [r['id'] for r in csv.DictReader(open(ROOT / 'data/export/combined_included.csv'))
               if r['include'] == 'yes' and r['category'] in set('ABCDEFH') and r['id'].startswith('W')]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    done = {json.loads(l)['id'] for l in open(OUT)} if OUT.exists() else set()
    todo = sorted(set(ids) - done)
    print(f'{len(done)} done, {len(todo)} to fetch', file=sys.stderr)
    with open(OUT, 'a') as out:
        for i in range(0, len(todo), 50):
            chunk = todo[i:i + 50]
            j = get(f'https://api.openalex.org/works?filter=openalex_id:{"|".join(chunk)}&select={FIELDS}&per-page=50')
            for w in j.get('results', []):
                out.write(json.dumps({
                    'id': w['id'].rsplit('/', 1)[-1], 'doi': (w.get('doi') or '').replace('https://doi.org/', ''),
                    'title': w.get('title'), 'year': w.get('publication_year'), 'type': w.get('type'),
                    'primary': loc(w.get('primary_location')),
                    'locations': [loc(l) for l in w.get('locations') or []]}, ensure_ascii=False) + '\n')
            out.flush()
            time.sleep(0.3)


if __name__ == '__main__':
    main()
