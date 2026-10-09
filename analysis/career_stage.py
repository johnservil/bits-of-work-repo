#!/usr/bin/env python3
"""Career stage and sector per person, from ORCID, Math Genealogy, Wikidata and
first-publication year. Feeds analysis/author_map.py (calendar person-years).

Inputs: data/authors/authors.csv, data/raw/enrich/{wikidata.jsonl, orcid/, mgp/, zbmath/},
        data/raw/dblp/authors_stats.json
Output: data/authors/career.csv, one row per person:
  phd_year, phd_source     mgp > orcid (education/qualification with a doctoral
                           role) > estimate (first publication year + calibrated
                           offset; first year from DBLP and zbMATH together)
  first_pub                earliest DBLP or zbMATH publication year
  sector_latest            academic / nonacademic / unknown (latest ORCID employment)
  employments              compact ORCID employment history: start-end:sector:role
  zb_code, zb_method       zbMATH author match (pipeline/authors_zbmath.py)
Prints the offset calibration and coverage to stdout.
"""
import csv, json, os, re, sys, glob, hashlib, collections, statistics

DOCTORAL = re.compile(r"ph\.?\s?d|d\.?\s?phil|doctor|doctorat|dr\.?\s?(rer|sc|phil|ing)|promotion|doktor|th[eè]se|dottorato|doutorado|kandidat", re.I)
ACADEMIC = re.compile(r"univers|college|institut|école|ecole|inria|cnrs|academ|polytechn|hochschule|eth |epfl|cwi|centrum wiskunde|max planck|school|kth|ntnu|riken|national laborator|centre national|politecnico|techni(on|sche)|ist austria|weizmann|simons", re.I)


def year(d):
    try: return int(((d or {}).get("year") or {}).get("value"))
    except (TypeError, ValueError): return None


def orcid_entries(path, section):
    d = json.load(open(path)) if os.path.exists(path) else {}
    for g in ((d.get(section) or {}).get("affiliation-group") or []):
        for s in g.get("summaries") or []:
            v = next(iter(s.values()))
            yield {"role": v.get("role-title") or "", "dept": v.get("department-name") or "",
                   "org": ((v.get("organization") or {}).get("name") or ""),
                   "start": year(v.get("start-date")), "end": year(v.get("end-date"))}


def main():
    ppl = [r for r in csv.DictReader(open("data/authors/authors.csv")) if int(r["n_items_yes"]) > 0]
    wd = {d["dblp_pid"]: d for d in map(json.loads, open("data/raw/enrich/wikidata.jsonl"))} if os.path.exists("data/raw/enrich/wikidata.jsonl") else {}
    stats = json.load(open("data/raw/dblp/authors_stats.json"))["stats"]
    rows = []; known = []
    for r in ppl:
        p = r["person"]
        zb = {}
        zf = f"data/raw/enrich/zbmath/{hashlib.md5(p.encode()).hexdigest()[:16]}.json"
        if os.path.exists(zf): zb = json.load(open(zf))
        zext = zb.get("external_ids") or {}
        orcids = {x for x in [r["orcid"], zext.get("orcid")] if x} | set((wd.get(r["dblp_pid"]) or {}).get("orcid", []))
        mgps = {x for x in [r["mgp_id"], zext.get("mgp")] if x} | set((wd.get(r["dblp_pid"]) or {}).get("mgp", []))
        phd, src = None, ""
        for m in sorted(mgps):
            f = f"data/raw/enrich/mgp/{m}.json"
            if not os.path.exists(f): continue
            ys = [d["year"] for d in json.load(open(f)).get("degrees", []) if d.get("year") and DOCTORAL.search(d.get("degree", "") + " Ph.D.")]
            if ys: phd, src = min(ys), "mgp"; break
        emps = []
        for o in sorted(orcids):
            f = f"data/raw/enrich/orcid/{o}.json"
            if not phd:
                ys = [e["end"] for sec in ("educations", "qualifications") for e in orcid_entries(f, sec)
                      if e["end"] and DOCTORAL.search(e["role"] + " " + e["dept"])]
                if ys: phd, src = min(ys), "orcid"
            for e in orcid_entries(f, "employments"):
                emps.append((e["start"] or 0, e["end"] or 0, "academic" if ACADEMIC.search(e["org"]) else "nonacademic", e["role"][:40]))
        firsts = [v[0] for v in (stats.get(p) or {}).get("pubs", {}).values() if 1900 < v[0] <= 2026]
        firsts += [d["year"] for d in zb.get("docs") or [] if d.get("year") and 1900 < d["year"] <= 2026]
        first = min(firsts) if firsts else None
        if not first and r["first_item"]: first = int(r["first_item"])
        if phd and first: known.append(phd - first)
        emps.sort()
        latest = max(emps, key=lambda e: (e[0], e[1] or 9999))[2] if emps else "unknown"
        rows.append({"person": p, "phd_year": phd or "", "phd_source": src, "first_pub": first or "",
                     "sector_latest": latest, "employments": "; ".join(f"{a or ''}-{b or ''}:{s}:{t}" for a, b, s, t in emps),
                     "zb_code": zb.get("code", ""), "zb_method": zb.get("method") or "",
                     "zb_docs": len(zb.get("docs") or [])})
    # Calibrate the PhD offset on people with a known PhD year and a first paper no more than
    # 15 years before it (earlier gaps are usually name collisions or pre-PhD careers elsewhere).
    k = [x for x in known if -15 <= x <= 15]
    off = round(statistics.median(k)) if k else 3
    forced = next((int(x.split("=")[1]) for x in sys.argv if x.startswith("--offset=")), None)
    if forced is not None: off = forced  # sensitivity runs
    for row in rows:
        if not row["phd_year"] and row["first_pub"]:
            row["phd_year"] = int(row["first_pub"]) + off; row["phd_source"] = "estimate"
    with open("data/authors/career.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    c = collections.Counter(r["phd_source"] for r in rows)
    print(f"persons {len(rows)}; PhD year source: {dict(c)}")
    if k:
        q = statistics.quantiles(k, n=4)
        print(f"PhD year - first publication year (n={len(k)}): median {statistics.median(k)}, quartiles {q[0]}..{q[2]}; offset used {off}")
    print("latest sector (ORCID employment):", dict(collections.Counter(r["sector_latest"] for r in rows)))
    print("zbMATH match:", dict(collections.Counter(r["zb_method"] or "none" for r in rows)))


if __name__ == "__main__":
    main()
