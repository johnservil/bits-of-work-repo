#!/usr/bin/env python3
"""Export the combined included set (Phase 0 ePrint + Phase 1) to
data/export/combined_included.csv (yes + borderline), one row per item, with
headline-class attribution (fractional weights) and provenance columns.
Includes the symmetric extension's labels (pipeline/symmetric_labels.py).
"""
import json, csv, os, sys
sys.path.insert(0, "pipeline")
from symmetric_labels import join
EXCL = set(json.load(open('data/manual_exclusions.json'))['items'])
POL = json.load(open("pipeline/attribution.json")); FRAC = POL["fractional"]; CLASSES = POL["classes"]

def study_rows():
    for l in open("data/labeled_final.jsonl"):
        r = json.loads(l); yield r["eprint_id"], "eprint", ["eprint"], r
    for l in open("data/phase1/labeled_final.jsonl"):
        r = json.loads(l); s = r.get("sources", [])
        yield r["id"], ("eprint" if s == ["eprint_supp"] else "phase1"), s, r
    tb = {json.loads(l)["id"] for l in open("data/phase1/round2/pool_tierB_sample.jsonl")}
    for l in open("data/phase1/round2/labeled_final.jsonl"):
        r = json.loads(l); s = r.get("sources", [])
        yield r["id"], ("eprint" if s == ["eprint"] else ("round2_tierB_sample" if r["id"] in tb else "round2_v2")), s, r

def rows():
    study = list(study_rows())
    retagged, extra = join({rid: r for rid, _, _, r in study})
    for rid, phase, srcs, r in study: yield rid, phase, srcs, retagged[rid]
    for r in extra:
        s = r.get("sources", [])
        yield r["id"], ("eprint" if r["round"] == "eprint" else "symmetric_" + r["round"]), s, r

os.makedirs("data/export", exist_ok=True)
cols = ["id", "phase", "sources", "vetted", "year", "include", "category", "problem_tags", "layer", "params", "regime", "leakage",
        "is_record", "quantum", "confidence", "label_source"] + [f"w_{c}" for c in CLASSES] + ["author_count", "authors", "title", "venue", "doi", "reason"]
n = 0
with open("data/export/combined_included.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(cols)
    for rid, phase, srcs, r in rows():
        L = r["label"]
        if rid in EXCL or L.get("include") not in ("yes", "borderline"): continue
        tags = L.get("problem_tags") or {}; tot = sum(tags.values()) or 1.0
        cw = {c: 0.0 for c in CLASSES}
        for t, wt in tags.items():
            for c, x in FRAC.get(t, {}).items(): cw[c] += wt / tot * x
        vetted = phase == "eprint" or "dblp" in srcs or "eprint" in srcs
        w.writerow([rid, phase, "|".join(srcs), vetted, r.get("year"), L.get("include"), L.get("category"), json.dumps(tags),
                    L.get("layer"), "|".join(L.get("params") or []), L.get("regime"), L.get("leakage"), L.get("is_record"), L.get("quantum"),
                    L.get("confidence"), r.get("label_source")] + [round(cw[c], 3) for c in CLASSES] +
                   [len(r.get("authors") or []), "; ".join(r.get("authors") or []), r.get("title"), r.get("venue") or r.get("category", ""),
                    r.get("doi", ""), L.get("reason")])
        n += 1
print(f"wrote {n} rows to data/export/combined_included.csv")
