#!/usr/bin/env python3
"""Merge classifier JSONL outputs, validate against the candidate list, report gaps."""
import json, glob, sys, collections
CAND = sys.argv[1]; LABDIR = sys.argv[2]; OUT = sys.argv[3]
cands = {(json.loads(l).get("id") or json.loads(l)["eprint_id"]): json.loads(l) for l in open(CAND)}
labels = {}; bad = 0
for p in sorted(glob.glob(LABDIR + "/*.jsonl")):
    for ln, line in enumerate(open(p)):
        line = line.strip()
        if not line or not line.startswith("{"): continue
        try: o = json.loads(line)
        except json.JSONDecodeError: bad += 1; continue
        eid = o.get("id") or o.get("eprint_id")
        if eid not in cands: bad += 1; continue
        labels[eid] = o
missing = sorted(set(cands) - set(labels))
print(f"labeled {len(labels)}/{len(cands)}; malformed/unknown {bad}; missing {len(missing)}")
if missing: open(LABDIR + "/MISSING.txt", "w").write("\n".join(missing)); print("missing ids written to", LABDIR + "/MISSING.txt")
with open(OUT, "w") as f:
    for eid, o in sorted(labels.items()):
        row = dict(cands[eid]); row["label"] = o; f.write(json.dumps(row, ensure_ascii=False) + "\n")
c = collections.Counter((o.get("include"), o.get("category")) for o in labels.values())
print("include/category:", sorted(c.items(), key=lambda x: -x[1])[:20])
