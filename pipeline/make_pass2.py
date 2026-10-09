#!/usr/bin/env python3
"""Build pass-2 review batches: all pass-1 yes/borderline items plus a random
sample of pass-1 'no' items (to estimate false-negative rate). Pass-2 items
carry the pass-1 label so the reviewer can agree or override.

Usage: make_pass2.py data/labeled_pass1.jsonl data/batches_pass2 [no_sample_frac] [batch_size] [abstract_cap]
(Phase 0 used cap 2200; Phase 1 uses 1500 for the token budget.)
"""
import json, os, sys, random
IN, OUTDIR = sys.argv[1], sys.argv[2]
FRAC = float(sys.argv[3]) if len(sys.argv) > 3 else 0.10
SIZE = int(sys.argv[4]) if len(sys.argv) > 4 else 60
CAP = int(sys.argv[5]) if len(sys.argv) > 5 else 2200
random.seed(20261008)
os.makedirs(OUTDIR, exist_ok=True)
rows = [json.loads(l) for l in open(IN)]
keep = [r for r in rows if r["label"]["include"] in ("yes", "borderline")]
nos = [r for r in rows if r["label"]["include"] == "no"]
samp = random.sample(nos, int(len(nos) * FRAC))
for r in samp: r["_audit_no"] = True
items = keep + samp
random.shuffle(items)  # mix so reviewer doesn't anchor on runs
manifest = {"n_yes_border": len(keep), "n_no_sampled": len(samp), "n_no_total": len(nos),
            "audit_ids": [r.get("id") or r["eprint_id"] for r in samp]}
json.dump(manifest, open(os.path.join(OUTDIR, "manifest.json"), "w"), indent=1)
for i in range(0, len(items), SIZE):
    with open(os.path.join(OUTDIR, f"batch_{i//SIZE:04d}.txt"), "w") as f:
        for r in items[i:i+SIZE]:
            L = r["label"]; ab = r.get("abstract") or "(no abstract available; judge from title and venue)"
            if len(ab) > CAP: ab = ab[:CAP] + " [...]"
            f.write(f"### {r.get('id') or r['eprint_id']}\nTITLE: {r['title']}\nAUTHORS: {'; '.join(r['authors'][:8])}\n"
                    f"YEAR: {r.get('year')}  " + (f"CATEGORY: {r['category']}" if 'category' in r else f"VENUE: {(r.get('venue') or '')[:80]}") + "\n"
                    f"PASS1: include={L['include']} cat={L['category']} tags={json.dumps(L.get('problem_tags'))} layer={L.get('layer')} regime={L.get('regime')} record={L.get('is_record')} reason={L.get('reason')}\n"
                    f"ABSTRACT: {ab}\n\n")
print(f"pass2: {len(keep)} yes/borderline + {len(samp)} sampled no (of {len(nos)}) -> {(len(items)+SIZE-1)//SIZE} batches")
