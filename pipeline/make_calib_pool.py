#!/usr/bin/env python3
"""Build a candidate pool and classifier batches for one calibration problem.

Usage: make_calib_pool.py PROBLEM SNOWDIR SEEDS.jsonl OUTDIR [statement_file] [batch_size] [fwd_max_cited]
  PROBLEM     label used in the rubric (UGC, 2to1, HAWK_moduleLIP, erdos-<N>)
  SNOWDIR     dir with snow_seeds.jsonl, snow_backward.jsonl, snow_forward.jsonl (fetch_openalex.py)
  SEEDS       the seed file given to `resolve` (unresolved seeds are added from it directly)
  OUTDIR      writes OUTDIR/pool.jsonl and OUTDIR/batches/batch_NNNN.txt
Only items whose cites_seed / seed_id belong to this PROBLEM's seeds are included, so one
snowball directory can serve several problems.
"""
import json, os, sys, re
P, SNOW, SEEDS, OUT = sys.argv[1:5]
STMT = open(sys.argv[5]).read().strip() if len(sys.argv) > 5 and os.path.exists(sys.argv[5]) else ""
SIZE = int(sys.argv[6]) if len(sys.argv) > 6 else 40
FWD_MAX = int(sys.argv[7]) if len(sys.argv) > 7 else 10**9  # drop forward citers of seeds cited more than this (survey-paper noise)
seeds = [json.loads(l) for l in open(SEEDS)]
mine = {s["seed_id"] for s in seeds if s.get("problem") == P or P in (s.get("problems") or [])}
def rd(fn):
    p = os.path.join(SNOW, fn)
    return [json.loads(l) for l in open(p)] if os.path.exists(p) else []
seedrows = [w for w in rd("snow_seeds.jsonl") if w.get("seed_id") in mine]
seed_oa = {w["openalex_id"] for w in seedrows}
fwd_ok = {w["openalex_id"] for w in seedrows if int(w.get("cited_by_count") or 0) <= FWD_MAX}
refs = set(x for w in seedrows for x in w.get("referenced_works", []))
pool = {}
def norm(t): return re.sub(r"[^a-z0-9]+", "", (t or "").lower())[:60]
def add(w, src):
    key = w.get("openalex_id") or norm(w.get("title"))
    if not key: return
    if key in pool: pool[key]["sources"].append(src); return
    r = {"id": w.get("openalex_id") or f"seed:{w.get('seed_id')}", "title": w.get("title") or "", "authors": w.get("authors") or [],
         "year": w.get("year"), "venue": w.get("venue") or "", "abstract": w.get("abstract") or "", "doi": w.get("doi") or "",
         "kw_hits": {}, "sources": [src], "problem": P}
    pool[key] = r
for w in seedrows: add(w, "seed")
for w in rd("snow_backward.jsonl"):
    if w["openalex_id"] in refs: add(w, "backward")
for w in rd("snow_forward.jsonl"):
    if w.get("cites_seed") in fwd_ok: add(w, "forward")
done = json.load(open(os.path.join(SNOW, "resolve_done.json"))) if os.path.exists(os.path.join(SNOW, "resolve_done.json")) else {}
for s in seeds:
    if s["seed_id"] in mine and not done.get(s["seed_id"]):
        add({"seed_id": s["seed_id"], "title": s["title"], "authors": s.get("authors", []), "year": s.get("year"), "venue": "ePrint/arXiv (unresolved in OpenAlex)", "abstract": s.get("abstract", "")}, "seed_unresolved")
rows = sorted(pool.values(), key=lambda r: r["id"])
os.makedirs(os.path.join(OUT, "batches"), exist_ok=True)
with open(os.path.join(OUT, "pool.jsonl"), "w") as f:
    for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")
for i in range(0, len(rows), SIZE):
    with open(os.path.join(OUT, "batches", f"batch_{i//SIZE:04d}.txt"), "w") as f:
        f.write(f"PROBLEM: {P}\n{STMT}\n\n" if STMT else f"PROBLEM: {P}\n\n")
        for r in rows[i:i+SIZE]:
            ab = r["abstract"] or "(no abstract available; judge from title and venue)"
            if len(ab) > 1500: ab = ab[:1500] + " [...]"
            f.write(f"### {r['id']}\nTITLE: {r['title']}\nAUTHORS: {'; '.join(r['authors'][:8])}\nYEAR: {r['year']}  VENUE: {r['venue'][:80]}  SRC: {','.join(sorted(set(r['sources'])))}\nABSTRACT: {ab}\n\n")
print(f"{P}: {len(rows)} items ({sum(1 for r in rows if r['abstract'])} with abstract) -> {(len(rows)+SIZE-1)//SIZE} batches in {OUT}/batches")
