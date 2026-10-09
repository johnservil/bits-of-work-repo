#!/usr/bin/env python3
"""Recall benchmark (PLAN.md §6.3): for seed surveys/key papers per class, fetch
their reference lists from OpenAlex and check how many references our pipeline
(a) harvested at all, (b) keyword-screened into a candidate pool, (c) labeled
include=yes/borderline. Writes analysis/recall_benchmark.md and a TSV of
references we never labeled (for manual relevance review).

Cost: one title search per seed (10 credits) the first time (cached in
data/raw/openalex/recall_seeds.json), then free singleton GETs.
"""
import json, re, os, sys, csv, collections, urllib.parse
sys.path.insert(0, "pipeline")
import fetch_openalex as oa

SEEDS = [
 ("ecdlp", "Recent progress on the elliptic curve discrete logarithm problem"),
 ("ecdlp", "Solving a 112-bit prime elliptic curve discrete logarithm problem on game consoles using sloppy reduction"),
 ("ecdlp", "Breaking ECC2K-130"),
 ("lattice", "Estimate all the {LWE, NTRU} schemes!"),
 ("lattice", "Does the dual-sieve attack on learning with errors even work?"),
 ("lattice", "Advanced lattice sieving on GPUs, with tensor cores"),
 ("lattice", "The general sieve kernel and new records in lattice reduction"),
 ("code", "A survey on code-based cryptography"),
 ("code", "Syndrome Decoding Estimator"),
 ("code", "McEliece needs a break - solving McEliece-1284 and quasi-cyclic-2918 with modern ISD"),
 ("comparator", "Comparing the difficulty of factorization and discrete logarithm: a 240-digit experiment"),
 ("comparator", "An efficient key recovery attack on SIDH"),
]
def norm(t): return re.sub(r"[^a-z0-9]+", "", (t or "").lower())[:60]

# what we have
labeled = {}   # norm title -> include
for l in open("data/labeled_final.jsonl"):
    r = json.loads(l); labeled[norm(r["title"])] = r["label"]["include"]
for p_ in ["data/phase1/labeled_final.jsonl", "data/phase1/round2/labeled_final.jsonl"]:
    for l in open(p_):
        r = json.loads(l); labeled[norm(r["title"])] = r["label"]["include"]
pool = {norm(json.loads(l)["title"]) for l in open("data/candidates_phase1.jsonl")}
pool |= {norm(json.loads(l)["title"]) for l in open("data/candidates.jsonl")}
pool |= {norm(json.loads(l)["title"]) for l in open("data/phase1/round2/pool_pass1.jsonl")}
harvested = set()
for l in open("data/eprint.jsonl"): harvested.add(norm(json.loads(l)["title"]))
for p in ["data/raw/dblp/dblp_candidates.jsonl"] + [os.path.join(d, f) for d in ["data/raw/openalex", "data/raw/zbmath"] for f in os.listdir(d) if f.endswith(".jsonl")]:
    if os.path.basename(p).startswith("seeds"): continue
    for l in open(p, encoding="utf-8"):
        try: harvested.add(norm(json.loads(l).get("title")))
        except json.JSONDecodeError: pass

cache_p = "data/raw/openalex/recall_seeds.json"
cache = json.load(open(cache_p)) if os.path.exists(cache_p) else {}
for cls, t in SEEDS:
    if t in cache: continue
    q = re.sub(r"\s+", " ", re.sub(r"[^A-Za-z0-9 ]+", " ", t)).strip()
    j = oa.get(f"{oa.BASE}?filter=title.search:{urllib.parse.quote(q)}&select=id,title,publication_year,referenced_works_count&per-page=10", cost=10)
    best = None
    for w in (j or {}).get("results", []):
        if norm(w["title"]) == norm(t) and (best is None or (w.get("referenced_works_count") or 0) > (best.get("referenced_works_count") or 0)): best = w
    cache[t] = best["id"].rsplit("/", 1)[-1] if best else None
    json.dump(cache, open(cache_p, "w"), indent=1)

out = ["# Recall benchmark against seed reference lists", "",
       "References of each seed paper (OpenAlex referenced_works) checked against our data by normalized title.",
       "harvested = present in any raw pull; pool = keyword-screened candidate; labeled = classified; incl = yes/borderline.", "",
       "| class | seed | refs | harvested | pool | labeled | incl |", "|---|---|---|---|---|---|---|"]
missing = []
tot = collections.Counter()
for cls, t in SEEDS:
    sid = cache.get(t)
    if not sid: out.append(f"| {cls} | {t[:60]} | not found in OpenAlex | | | | |"); continue
    seed = oa.single(sid)
    refs = [oa.single(x) for x in (seed or {}).get("referenced_works", [])]
    refs = [r for r in refs if r and r.get("title")]
    c = collections.Counter()
    for r in refs:
        k = norm(r["title"]); c["refs"] += 1
        c["harvested"] += k in harvested; c["pool"] += k in pool; c["labeled"] += k in labeled
        c["incl"] += labeled.get(k) in ("yes", "borderline")
        if k not in labeled: missing.append((cls, t[:40], r.get("year"), r["title"], r.get("venue") or "", k in harvested))
    for k2, v in c.items(): tot[(cls, k2)] += v
    out.append(f"| {cls} | {t[:60]} | {c['refs']} | {c['harvested']} | {c['pool']} | {c['labeled']} | {c['incl']} |")
out += ["", "## Per class", "", "| class | refs | harvested | pool | labeled | incl |", "|---|---|---|---|---|---|"]
for cls in ["ecdlp", "lattice", "code", "comparator"]:
    out.append(f"| {cls} | " + " | ".join(str(tot[(cls, k)]) for k in ["refs", "harvested", "pool", "labeled", "incl"]) + " |")
out += ["", f"{len(missing)} references were never labeled; see analysis/recall_unlabeled_refs.tsv for manual review."]
open("analysis/recall_benchmark.md", "w").write("\n".join(out) + "\n")
with open("analysis/recall_unlabeled_refs.tsv", "w", newline="") as f:
    w = csv.writer(f, delimiter="\t"); w.writerow(["class", "seed", "year", "title", "venue", "harvested_but_not_screened"])
    for m in sorted(missing): w.writerow(m)
print("\n".join(out))
