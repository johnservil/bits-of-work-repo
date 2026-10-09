#!/usr/bin/env python3
"""After a title screen, build pass-1 batches (with abstracts) from the kept items only.

Usage: make_screened_batches.py PROBLEM_DIR [batch_size]
Reads PROBLEM_DIR/pool.jsonl, PROBLEM_DIR/screen_labels/*.jsonl, PROBLEM_DIR/statement.txt.
Writes PROBLEM_DIR/pool_screened.jsonl and PROBLEM_DIR/batches/batch_NNNN.txt (replacing earlier batches).
Items with no screen label are kept (fail open).
"""
import json, glob, os, sys, shutil
D = sys.argv[1].rstrip("/"); SIZE = int(sys.argv[2]) if len(sys.argv) > 2 else 40
P = os.path.basename(D); ST = open(os.path.join(D, "statement.txt")).read().strip()
keep = {}
for f in glob.glob(os.path.join(D, "screen_labels", "*.jsonl")):
    for l in open(f):
        l = l.strip()
        if l.startswith("{"):
            try: o = json.loads(l); keep[o["id"]] = bool(o.get("keep", True))
            except json.JSONDecodeError: pass
rows = [json.loads(l) for l in open(os.path.join(D, "pool.jsonl"))]
kept = [r for r in rows if keep.get(r["id"], True)]
with open(os.path.join(D, "pool_screened.jsonl"), "w") as f:
    for r in kept: f.write(json.dumps(r, ensure_ascii=False) + "\n")
bd = os.path.join(D, "batches"); shutil.rmtree(bd, ignore_errors=True); os.makedirs(bd)
for i in range(0, len(kept), SIZE):
    with open(os.path.join(bd, f"batch_{i//SIZE:04d}.txt"), "w") as f:
        f.write(f"PROBLEM: {P}\n{ST}\n\n")
        for r in kept[i:i+SIZE]:
            ab = r.get("abstract") or "(no abstract available; judge from title and venue)"
            if len(ab) > 1500: ab = ab[:1500] + " [...]"
            f.write(f"### {r['id']}\nTITLE: {r['title']}\nAUTHORS: {'; '.join(r.get('authors', [])[:8])}\nYEAR: {r.get('year')}  VENUE: {(r.get('venue') or '')[:80]}  SRC: {','.join(sorted(set(r.get('sources', []))))}\nABSTRACT: {ab}\n\n")
print(f"{P}: {len(rows)} pooled, {len(keep)} screened, {len(kept)} kept -> {(len(kept)+SIZE-1)//SIZE} batches")
