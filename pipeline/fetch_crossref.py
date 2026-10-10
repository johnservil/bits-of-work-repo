#!/usr/bin/env python3
"""Look up Crossref metadata for every DOI among the counted rows.

Run from the repo root:  python3 -I pipeline/fetch_crossref.py [out.jsonl]

Input: data/export/combined_included.csv (counted rows with a DOI), plus any DOIs listed
in data/raw/eprint_pages/pubinfo.jsonl.
Output (default data/raw/crossref/works.jsonl), resumable, one line per DOI:
  {"doi", "status", "type", "container", "short_container", "event", "publisher",
   "issn", "isbn", "year", "title"}
Uses the Crossref polite pool (mailto in the User-Agent). Stdlib only.
"""
import csv, json, sys, time, urllib.request, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'data/raw/crossref/works.jsonl'
UA = 'literature-search-pilot/0.1 (mailto:matthewdgreen@gmail.com)'


def dois():
    seen = set()
    for r in csv.DictReader(open(ROOT / 'data/export/combined_included.csv')):
        if r['include'] == 'yes' and r['category'] in set('ABCDEFH') and r['doi']:
            seen.add(r['doi'].lower())
    p = ROOT / 'data/raw/eprint_pages/pubinfo.jsonl'
    if p.exists():
        seen |= {json.loads(l)['doi'].lower() for l in open(p) if json.loads(l).get('doi')}
    return sorted(seen)


def first(x):
    return x[0] if isinstance(x, list) and x else (x or '')


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    done = {json.loads(l)['doi'] for l in open(OUT)} if OUT.exists() else set()
    todo = [d for d in dois() if d not in done]
    print(f'{len(done)} done, {len(todo)} to fetch', file=sys.stderr)
    with open(OUT, 'a') as out:
        for n, d in enumerate(todo):
            rec = {'doi': d}
            try:
                url = 'https://api.crossref.org/works/' + urllib.parse.quote(d, safe='/')
                with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=30) as resp:
                    m = json.load(resp)['message']
                rec.update(status=200, type=m.get('type', ''), container=first(m.get('container-title')),
                           containers=m.get('container-title') or [],
                           short_container=first(m.get('short-container-title')),
                           event=(m.get('event') or {}).get('name', ''), publisher=m.get('publisher', ''),
                           issn=m.get('ISSN') or [], isbn=m.get('ISBN') or [],
                           year=((m.get('issued') or {}).get('date-parts') or [[None]])[0][0],
                           title=first(m.get('title')))
            except urllib.error.HTTPError as e:
                rec['status'] = e.code
                if e.code == 429:
                    print('rate limited; stopping', file=sys.stderr)
                    break
            except Exception as e:
                print(d, e, file=sys.stderr)
                continue
            out.write(json.dumps(rec) + '\n')
            out.flush()
            if n % 200 == 0:
                print(n, d, rec.get('container', ''), file=sys.stderr)
            time.sleep(0.15)


if __name__ == '__main__':
    main()
