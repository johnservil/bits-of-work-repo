#!/usr/bin/env python3
"""Split candidates into classifier batches (plain-text, abstract-trimmed).

Works for Phase 0 rows (eprint_id, category) and Phase 1 rows (id, venue, sources).
Usage: make_batches.py CANDIDATES.jsonl OUTDIR [batch_size] [abstract_cap] [first_batch]
Phase 0 used cap 1800; Phase 1 pass 1 uses 1000 from batch 0010 on (token budget).
first_batch: only (re)write batches with index >= this (others are left untouched).
"""
import json, os, sys
IN = sys.argv[1]; OUTDIR = sys.argv[2]; SIZE = int(sys.argv[3]) if len(sys.argv) > 3 else 60
CAP = int(sys.argv[4]) if len(sys.argv) > 4 else 1800
FIRST = int(sys.argv[5]) if len(sys.argv) > 5 else 0
os.makedirs(OUTDIR, exist_ok=True)
def rid(r): return r.get("id") or r["eprint_id"]
rows = [json.loads(l) for l in open(IN)]
rows.sort(key=rid)
for i in range(0, len(rows), SIZE):
    if i // SIZE < FIRST: continue
    with open(os.path.join(OUTDIR, f"batch_{i//SIZE:04d}.txt"), "w") as f:
        for r in rows[i:i+SIZE]:
            ab = r.get("abstract") or "(no abstract available; judge from title and venue)"
            if len(ab) > CAP: ab = ab[:CAP] + " [...]"
            where = f"CATEGORY: {r['category']}" if "category" in r else f"VENUE: {(r.get('venue') or '')[:80]}"
            f.write(f"### {rid(r)}\nTITLE: {r['title']}\nAUTHORS: {'; '.join(r.get('authors', [])[:8])}\n"
                    f"YEAR: {r.get('year')}  {where}  KW: {','.join(sorted(set(sum(r['kw_hits'].values(), []))))[:200]}\n"
                    f"ABSTRACT: {ab}\n\n")
print(f"{len(rows)} items -> {(len(rows)+SIZE-1)//SIZE} batches in {OUTDIR}")
