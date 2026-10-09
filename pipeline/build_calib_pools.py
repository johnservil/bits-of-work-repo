#!/usr/bin/env python3
"""Build pools + pass-1 batches for every calibration problem present in a seed file.

Usage: build_calib_pools.py SEEDS.jsonl SNOWDIR OUTROOT [erdos_db.jsonl] [only=P1,P2,...] [fwd_max_cited]
Writes OUTROOT/<problem>/statement.txt, pool.jsonl, batches/. Erdős statements come from erdos_db.jsonl.
"""
import json, os, sys, subprocess
SEEDS, SNOW, OUT = sys.argv[1:4]
DB = sys.argv[4] if len(sys.argv) > 4 else None
ONLY = set(sys.argv[5].split(",")) if len(sys.argv) > 5 else None
FWD_MAX = sys.argv[6] if len(sys.argv) > 6 else "1000000000"
stmts = {}
if DB:
    for l in open(DB):
        r = json.loads(l); stmts[f"erdos-{r['problem_number']}"] = (r.get("statement") or "")[:600]
fixed = {
 "UGC": "The Unique Games Conjecture (Khot 2002): work that proves, disproves, or makes progress on it (algorithms for unique games, the 2-to-2 Games line, small-set expansion, structural results used in those proofs). Papers that merely assume UGC are include=no.",
 "2to1": "The 2-to-1 Games Conjecture (with or without perfect completeness): proofs of special cases, reductions, structural results used to attack it, and the 2026 resolution lineage. Papers that merely assume it are include=no.",
}
probs = sorted({p for s in map(json.loads, open(SEEDS)) for p in ([s.get("problem")] + (s.get("problems") or [])) if p})
for P in probs:
    if ONLY and P not in ONLY: continue
    d = os.path.join(OUT, P.replace("/", "_")); os.makedirs(d, exist_ok=True)
    st = fixed.get(P) or (f"Erdős problem {P.split('-',1)[1]} (erdosproblems.com): " + stmts.get(P, "")) if P.startswith("erdos-") else fixed.get(P, "")
    open(os.path.join(d, "statement.txt"), "w").write(st + "\n")
    subprocess.run([sys.executable, "-I", "pipeline/make_calib_pool.py", P, SNOW, SEEDS, d, os.path.join(d, "statement.txt"), "40", FWD_MAX], check=True)
