#!/usr/bin/env python3
"""Phase-0 pilot analysis over labeled ePrint candidates.

Usage: pilot_counts.py data/labeled_pass1.jsonl [--borderline]
Prints: per-class totals under fractional and touch attribution, per-era
split, category mix, distinct-author counts, records list.
"""
import json, sys, collections
LAB = sys.argv[1]; INCLUDE_BORDER = "--borderline" in sys.argv
POL = json.load(open("pipeline/attribution.json"))
CLASSES = POL["classes"]; FRAC = POL["fractional"]; EFF = set(POL["effort_categories"])

rows = [json.loads(l) for l in open(LAB)]
def ok(r):
    inc = r["label"].get("include")
    return inc == "yes" or (INCLUDE_BORDER and inc == "borderline")
inc = [r for r in rows if ok(r)]
eff = [r for r in inc if r["label"].get("category") in EFF]
print(f"labeled {len(rows)}; included {len(inc)}; effort categories (A-F,H) {len(eff)}; borderline counted: {INCLUDE_BORDER}\n")

def era(y): return "pre-2006" if y < 2006 else ("2006-2016" if y <= 2016 else "2017-2026")
frac = collections.defaultdict(float); touch = collections.Counter()
frac_era = collections.defaultdict(float); touch_era = collections.Counter()
cat_by_class = collections.defaultdict(collections.Counter)
authors = collections.defaultdict(set); per_year = collections.defaultdict(float)
for r in eff:
    tags = r["label"].get("problem_tags") or {}
    tot = sum(tags.values()) or 1.0
    touched = set()
    for t, w in tags.items():
        for c, cw in FRAC.get(t, {}).items():
            frac[c] += (w / tot) * cw; frac_era[(c, era(r["year"]))] += (w / tot) * cw
            per_year[(c, r["year"])] += (w / tot) * cw
            touched.add(c)
    for c in touched:
        touch[c] += 1; touch_era[(c, era(r["year"]))] += 1
        cat_by_class[c][r["label"]["category"]] += 1
        for a in r["authors"]: authors[c].add(a)

print(f"{'class':18s} {'fractional':>10s} {'touch':>6s} {'authors':>8s}   {'pre-2006':>9s} {'2006-2016':>10s} {'2017-2026':>10s}   categories")
for c in CLASSES:
    cats = " ".join(f"{k}:{v}" for k, v in sorted(cat_by_class[c].items()))
    print(f"{c:18s} {frac[c]:10.1f} {touch[c]:6d} {len(authors[c]):8d}   {frac_era[(c,'pre-2006')]:9.1f} {frac_era[(c,'2006-2016')]:10.1f} {frac_era[(c,'2017-2026')]:10.1f}   {cats}")

print("\nfractional per year (effort categories):")
years = sorted({y for (_, y) in per_year})
print("year  " + " ".join(f"{c[:8]:>8s}" for c in CLASSES))
for y in years:
    print(f"{y}  " + " ".join(f"{per_year[(c,y)]:8.1f}" for c in CLASSES))

print("\nrecords (category E or is_record):")
for r in sorted(inc, key=lambda r: r["year"]):
    L = r["label"]
    if L.get("category") == "E" or L.get("is_record"):
        print(f"  {r['eprint_id']:9s} {','.join(L.get('problem_tags',{}))[:28]:28s} {r['title'][:85]}")

print("\nlayer-2 (deployed-parameter) items per class:")
l2 = collections.Counter()
for r in eff:
    if r["label"].get("layer") == 2:
        for t in r["label"].get("problem_tags", {}):
            for c in FRAC.get(t, {}): l2[c] += 1
print("  ", dict(l2))
print("\nH (withdrawn/refuted attacks):")
for r in inc:
    if r["label"].get("category") == "H": print(f"  {r['eprint_id']:9s} {r['title'][:90]}")
