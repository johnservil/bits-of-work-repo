#!/usr/bin/env python3
"""Version weights: count each piece of work once, and journal extensions at 1/3.

Run from the repo root:  python3 -I pipeline/build_version_weights.py
Input:  data/venues/duplicate_checks.csv (groups of export ids judged to be versions of
        one work; columns group, ids "a + b + ...", verdict, relation, note) and
        data/export/combined_included.csv (which items are counted, their years).
Output: data/dedup/version_weights.csv  id, weight, role, kept_id, group, relation, note
        Ids not listed have weight 1.

Rules (user decision 2026-10-10):
  - Only groups with verdict "same-work" are used; "different" groups are left alone.
  - Preprint and repository versions (ePrint, arXiv, HAL, tech reports, duplicate database
    records, thesis translations) are the same work as the published version: the group
    counts once. The counted member with the earliest year keeps weight 1 (ties: a published
    version, then the first listed); the other counted members get weight 0.
  - A journal version that extends a conference paper counts 1/3 (assumed new material),
    the conference work 1. This applies only when the extension is certain: relation
    "conf+journal" and a note that does not call the match borderline. Uncertain
    extensions are left at full weight and reported.
  - Members that are not counted (borderline or non-effort categories) are ignored, so an
    item is never discounted against a version that was not counted anyway.
These weights multiply the class weights of each item wherever papers are counted.
"""
from pathlib import Path
import csv, re, collections

ROOT = Path(__file__).resolve().parent.parent
EFFORT = set('ABCDEFH')
EXTENSION_WEIGHT = 1 / 3
EPRINT = re.compile(r'^\d{4}/\d+$')


def kind(i, pubtype):
    if EPRINT.match(i) or i.startswith(('dblp:journals/corr/', 'dblp:journals/iacr/')):
        return 'preprint'
    if i.startswith('dblp:conf/'):
        return 'conference'
    if i.startswith('dblp:journals/'):
        return 'journal'
    if i.startswith('dblp:phd/'):
        return 'thesis'
    return pubtype.get(i) or 'other'


def main():
    rows = {r['id']: r for r in csv.DictReader((ROOT / 'data/export/combined_included.csv').open())}
    counted = {i for i, r in rows.items() if r['include'] == 'yes' and r['category'] in EFFORT}
    pv = ROOT / 'data/venues/published_venues.csv'
    pubtype = {r['id']: r['pub_type'] for r in csv.DictReader(pv.open())} if pv.exists() else {}
    year = lambda i: int(rows[i]['year']) if rows.get(i, {}).get('year', '').isdigit() else 9999

    out, uncertain, summary = [], [], collections.Counter()
    for g in csv.DictReader((ROOT / 'data/venues/duplicate_checks.csv').open()):
        if g['verdict'] != 'same-work':
            continue
        ids = [x.strip() for x in g['ids'].split('+') if x.strip()]
        members = [i for i in ids if i in counted]
        if len(members) < 2:
            summary['groups with fewer than two counted members'] += 1
            continue
        kinds = {i: kind(i, pubtype) for i in members}
        extension = g['relation'] == 'conf+journal'
        if extension and 'borderline' in g['note'].lower():
            uncertain.append(g)
            summary['uncertain extensions left at full weight'] += 1
            continue
        journals = [i for i in members if extension and kinds[i] == 'journal']
        base = [i for i in members if i not in journals]
        if extension and not base:          # nothing but journal records: treat as plain duplicates
            base, journals = members, []

        def rank(i):
            return (year(i), kinds[i] == 'preprint', ids.index(i))
        kept = min(base, key=rank)
        for i in base:
            role = 'kept' if i == kept else 'merged'
            out.append((i, 1.0 if i == kept else 0.0, role, kept, g))
            summary[role] += 1
        for i in journals:
            out.append((i, EXTENSION_WEIGHT, 'extension', kept, g))
            summary['extension'] += 1

    d = ROOT / 'data/dedup'
    d.mkdir(exist_ok=True)
    with (d / 'version_weights.csv').open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['id', 'weight', 'role', 'kept_id', 'group', 'relation', 'note'])
        for i, wt, role, kept, g in sorted(out, key=lambda t: (int(t[4]['group']), t[2] != 'kept', t[0])):
            w.writerow([i, f'{wt:.6g}', role, kept, g['group'], g['relation'], g['note']])
    print(f'wrote data/dedup/version_weights.csv: {len(out)} ids; ' + ', '.join(f'{k} {v}' for k, v in summary.items()))
    for g in uncertain:
        print(f'  uncertain (full weight kept): group {g["group"]}: {g["ids"]} | {g["note"]}')


if __name__ == '__main__':
    main()
