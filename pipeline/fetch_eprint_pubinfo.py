#!/usr/bin/env python3
"""Fetch the 'Publication info' (and DOI, if any) from ePrint abstract pages.

Run from the repo root:  python3 -I pipeline/fetch_eprint_pubinfo.py [out.jsonl]

Input: the ePrint ids among the counted rows of data/export/combined_included.csv.
Output (default data/raw/eprint_pages/pubinfo.jsonl), one line per id, resumable:
  {"id", "status", "pubinfo", "doi", "category", "fetched"}
Only these fields are kept (the page also lists contact e-mails; those are not stored).
One request per ~4 s; on HTTP 429 it waits (60 s, then longer) and retries. Stdlib only.
"""
import csv, json, re, sys, time, html, urllib.request, urllib.error, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'data/raw/eprint_pages/pubinfo.jsonl'
UA = 'literature-search-pilot/0.1 (mailto:matthewdgreen@gmail.com)'
EPRINT = re.compile(r'^\d{4}/\d+$')
FIELD = re.compile(r'<dt>\s*(.*?)\s*</dt>\s*<dd[^>]*>(.*?)</dd>', re.S)


def text(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


def ids():
    for r in csv.DictReader(open(ROOT / 'data/export/combined_included.csv')):
        if r['include'] == 'yes' and r['category'] in set('ABCDEFH') and EPRINT.match(r['id']):
            yield r['id']


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if OUT.exists():
        done = {json.loads(l)['id'] for l in open(OUT) if l.strip()}
    todo = [i for i in ids() if i not in done]
    print(f'{len(done)} done, {len(todo)} to fetch', file=sys.stderr)
    with open(OUT, 'a') as out:
        for n, i in enumerate(todo):
            rec = {'id': i, 'status': None, 'pubinfo': '', 'doi': '', 'category': '',
                   'fetched': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')}
            try:
                for wait in (60, 180, 600, None):
                    try:
                        req = urllib.request.Request(f'https://eprint.iacr.org/{i}', headers={'User-Agent': UA})
                        with urllib.request.urlopen(req, timeout=30) as resp:
                            rec['status'] = resp.status
                            page = resp.read().decode('utf-8', 'replace')
                        break
                    except urllib.error.HTTPError as e:
                        if e.code != 429 or wait is None:
                            raise
                        print(f'429 at {i}; waiting {wait}s', file=sys.stderr)
                        time.sleep(wait)
                f = {text(k).lower(): v for k, v in FIELD.findall(page)}
                rec['pubinfo'] = text(f.get('publication info', ''))
                rec['category'] = text(f.get('category', ''))
                m = re.search(r'(10\.\d{4,9}/[^\s"<>]+)', f.get('doi', '') + ' ' + f.get('publication info', ''))
                rec['doi'] = m[1].rstrip('.') if m else ''
            except Exception as e:  # keep going; failed ids are retried on the next run
                rec['status'] = f'error: {e}'
                if '403' in str(e) or '429' in str(e):
                    print(f'stopping at {i}: {e}', file=sys.stderr)
                    break
                continue
            out.write(json.dumps(rec) + '\n')
            out.flush()
            if n % 100 == 0:
                print(n, i, rec['pubinfo'][:80], file=sys.stderr)
            time.sleep(4)


if __name__ == '__main__':
    main()
