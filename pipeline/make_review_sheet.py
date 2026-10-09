#!/usr/bin/env python3
"""Build a human spot-check sheet (markdown) from labeled_final.jsonl.

Stratified: all pass1/pass2 include-disagreements (capped), plus a random
sample of agreed yes / borderline / no per headline class.
Usage: make_review_sheet.py data/labeled_final.jsonl analysis/review_sheet.md [n_per_stratum]
"""
import json, sys, random, collections
IN, OUT = sys.argv[1], sys.argv[2]; N = int(sys.argv[3]) if len(sys.argv) > 3 else 12
random.seed(7)
rows = [json.loads(l) for l in open(IN)]
def inc(l): return l.get("include") if l else None
dis = [r for r in rows if r["label_pass2"] and inc(r["label_pass1"]) != inc(r["label_pass2"])]
agreed = [r for r in rows if r["label_pass2"] and inc(r["label_pass1"]) == inc(r["label_pass2"])]
strata = collections.defaultdict(list)
for r in agreed:
    tags = list((r["label"].get("problem_tags") or {}).keys())
    key = (r["label"]["include"], tags[0] if tags else "none")
    strata[key].append(r)
pick = random.sample(dis, min(len(dis), 4 * N))
for k, v in strata.items(): pick += random.sample(v, min(len(v), max(2, N // 4)))
seen = set(); out = []
for r in pick:
    if r["eprint_id"] in seen: continue
    seen.add(r["eprint_id"]); out.append(r)
with open(OUT, "w") as f:
    f.write(f"# Spot-check sheet ({len(out)} items; {len(dis)} total pass1/pass2 include disagreements)\n\n")
    f.write("Mark each row: OK / WRONG-include / WRONG-category / WRONG-tags, and add a note if useful.\n\n")
    for r in out:
        a, b = r["label_pass1"], r["label_pass2"]
        f.write(f"## {r['eprint_id']} — {r['title']}\n")
        f.write(f"{r['year']} · {', '.join(r['authors'][:5])}{' et al.' if len(r['authors'])>5 else ''} · {r['url']}\n\n")
        f.write(f"- pass1: {a['include']} / {a['category']} / {json.dumps(a.get('problem_tags'))} / L{a.get('layer')} — {a.get('reason')}\n")
        if b: f.write(f"- pass2: {b['include']} / {b['category']} / {json.dumps(b.get('problem_tags'))} / L{b.get('layer')} — {b.get('reason')}{(' — OVERRIDE: ' + b['override_note']) if b.get('override_note') else ''}\n")
        f.write(f"- abstract: {r['abstract'][:600]}{'…' if len(r['abstract'])>600 else ''}\n")
        f.write("- verdict: \n\n")
print(f"review sheet: {len(out)} items -> {OUT}")
