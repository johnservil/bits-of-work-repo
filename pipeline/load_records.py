#!/usr/bin/env python3
"""Load and validate records/<class>/*.yaml (flat key: JSON-value format, see records/README.md).
Usage: load_records.py [--check]   prints counts; with --check, lists schema problems."""
import json, glob, os, sys, collections
REQ = ["id", "class", "problem", "instance", "instance_size", "method", "date", "source_url", "verified", "confidence"]
def load(path):
    rec = {}
    for ln, line in enumerate(open(path, encoding="utf-8"), 1):
        line = line.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"): continue
        k, sep, v = line.partition(":")
        if not sep: raise ValueError(f"{path}:{ln}: no key")
        rec[k.strip()] = json.loads(v.strip())
    return rec
def all_records():
    out = []
    for p in sorted(glob.glob("records/*/*.yaml")):
        r = load(p); r["_path"] = p; r["_summary"] = os.path.basename(p).endswith("_summary.yaml") or "summary" in r.get("id", "")
        out.append(r)
    return out
if __name__ == "__main__":
    recs, bad = [], 0
    for p in sorted(glob.glob("records/*/*.yaml")):
        try: r = load(p)
        except Exception as e: print("PARSE", e); bad += 1; continue
        miss = [k for k in REQ if k not in r]
        ver_ok = r.get("verified") is False or (r.get("verified") is True and r.get("verified_by"))
        if "--check" in sys.argv and (miss or not ver_ok or r.get("id") != os.path.basename(p)[:-5]):
            print("SCHEMA", p, "missing", miss, "verified", r.get("verified"), "id", r.get("id")); bad += 1
        recs.append(r)
    c = collections.Counter(os.path.basename(os.path.dirname(r.get("_path", p))) for r in recs)
    print(f"{len(recs)} record files; problems {bad}; by class {dict(collections.Counter(r.get('class') for r in recs))}")
