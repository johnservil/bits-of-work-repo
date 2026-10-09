#!/usr/bin/env python3
"""Merge pass-2 labels over pass-1, compute agreement stats and audit FN rate.

Output: data/labeled_final.jsonl where label = pass-2 label when available,
else pass-1 label; each row keeps both under label_pass1 / label_pass2.
"""
import json, glob, sys, collections
P1, LABDIR, MANIFEST, OUT = sys.argv[1:5]
rows = {(json.loads(l).get("id") or json.loads(l)["eprint_id"]): json.loads(l) for l in open(P1)}
man = json.load(open(MANIFEST)); audit = set(man["audit_ids"])
p2 = {}; bad = 0
for p in sorted(glob.glob(LABDIR + "/*.jsonl")):
    for line in open(p):
        line = line.strip()
        if not line.startswith("{"): continue
        try: o = json.loads(line)
        except json.JSONDecodeError: bad += 1; continue
        oid = o.get("id") or o.get("eprint_id")
        if oid in rows: p2[oid] = o
        else: bad += 1
print(f"pass-2 labels: {len(p2)}; malformed/unknown: {bad}")

# agreement on include (3-way) and category, computed by us (not trusting 'agree' field)
inc_pairs = collections.Counter(); cat_agree = 0; n = 0
fn_audit = 0; audit_seen = 0
for eid, o in p2.items():
    a = rows[eid]["label"]; n += 1
    inc_pairs[(a["include"], o["include"])] += 1
    if a["category"] == o["category"]: cat_agree += 1
    if eid in audit:
        audit_seen += 1
        if o["include"] in ("yes", "borderline"): fn_audit += 1
print("include transitions pass1->pass2:")
for (x, y), c in sorted(inc_pairs.items(), key=lambda t: -t[1]): print(f"   {x:10s} -> {y:10s} {c}")
print(f"category agreement: {cat_agree}/{n} = {cat_agree/n:.2f}")
# Cohen's kappa on binary include (yes/borderline vs no)
def b(x): return x in ("yes", "borderline")
tot = n; po = sum(c for (x, y), c in inc_pairs.items() if b(x) == b(y)) / tot
p1y = sum(c for (x, y), c in inc_pairs.items() if b(x)) / tot
p2y = sum(c for (x, y), c in inc_pairs.items() if b(y)) / tot
pe = p1y * p2y + (1 - p1y) * (1 - p2y)
print(f"binary include kappa: {((po - pe) / (1 - pe)) if pe < 1 else float('nan'):.2f} (observed agreement {po:.2f})")
if audit_seen:
    rate = fn_audit / audit_seen
    print(f"audit of pass-1 'no': {fn_audit}/{audit_seen} flipped to yes/borderline -> est. FN rate {rate:.3f}, "
          f"implies ~{rate * man['n_no_total']:.0f} missed items among {man['n_no_total']} excluded")

with open(OUT, "w") as f:
    for eid, r in sorted(rows.items()):
        r = dict(r); r["label_pass1"] = r.pop("label")
        r["label_pass2"] = p2.get(eid)
        r["label"] = r["label_pass2"] or r["label_pass1"]
        r["label_source"] = "pass2" if eid in p2 else "pass1"
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote", OUT)
