#!/usr/bin/env python3
"""Two-pass bookkeeping for one calibration problem directory.

Usage: calib_two_pass.py p1merge DIR      -> DIR/labeled_pass1.jsonl from pool_screened.jsonl (or pool.jsonl) + labels_p1/
       calib_two_pass.py p2batches DIR    -> DIR/batches_p2/ (make_pass2.py, 10% audit, problem header prepended)
       calib_two_pass.py final DIR        -> DIR/labeled_final.jsonl via merge_pass2.py, then calib_estimate.py -> DIR/estimate.txt
"""
import json, glob, os, sys, subprocess
cmd, D = sys.argv[1], sys.argv[2].rstrip("/")
PY = sys.executable
if cmd == "p1merge":
    src = os.path.join(D, "pool_screened.jsonl") if os.path.exists(os.path.join(D, "pool_screened.jsonl")) else os.path.join(D, "pool.jsonl")
    pool = {json.loads(l)["id"]: json.loads(l) for l in open(src)}
    n = 0
    for p in sorted(glob.glob(os.path.join(D, "labels_p1", "*.jsonl"))):
        for l in open(p):
            l = l.strip()
            if not l.startswith("{"): continue
            try: o = json.loads(l)
            except json.JSONDecodeError: continue
            r = pool.get(o["id"])
            if r: r["label"] = o; r["label_pass1"] = o; n += 1
    with open(os.path.join(D, "labeled_pass1.jsonl"), "w") as f:
        for r in pool.values():
            if "label" in r: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{os.path.basename(D)}: {n} labeled of {len(pool)}")
elif cmd == "p2batches":
    out = os.path.join(D, "batches_p2")
    subprocess.run([PY, "-I", "pipeline/make_pass2.py", os.path.join(D, "labeled_pass1.jsonl"), out, "0.10", "40", "1500"], check=True)
    head = f"PROBLEM: {os.path.basename(D)}\n" + open(os.path.join(D, "statement.txt")).read().strip() + "\n\n"
    for b in glob.glob(os.path.join(out, "batch_*.txt")):
        s = open(b).read()
        if not s.startswith("PROBLEM:"): open(b, "w").write(head + s)
elif cmd == "final":
    subprocess.run([PY, "-I", "pipeline/merge_pass2.py", os.path.join(D, "labeled_pass1.jsonl"), os.path.join(D, "labels_p2"),
                    os.path.join(D, "batches_p2", "manifest.json"), os.path.join(D, "labeled_final.jsonl")], check=True)
    # de-duplicate conference/journal/arXiv versions by normalized title (keep the first by id)
    import re
    fin = os.path.join(D, "labeled_final.jsonl"); seen = {}; kept = []
    for l in open(fin):
        r = json.loads(l); k = re.sub(r"[^a-z0-9]+", "", (r.get("title") or "").lower())[:60]
        if k and k in seen: continue
        if k: seen[k] = 1
        kept.append(r)
    open(fin, "w").write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kept))
    print(f"dedup by title: kept {len(kept)}")
    with open(os.path.join(D, "estimate.txt"), "w") as f:
        subprocess.run([PY, "-I", "pipeline/calib_estimate.py", os.path.join(D, "labeled_final.jsonl"), "250000"], stdout=f, check=True)
    print(open(os.path.join(D, "estimate.txt")).read())
