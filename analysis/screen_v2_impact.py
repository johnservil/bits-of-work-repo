#!/usr/bin/env python3
"""Dry run of a v2 keyword screen motivated by analysis/recall_benchmark.md:
count items in the merged harvest (and ePrint) that v2 patterns would newly
screen in. Changes nothing in the pipeline; writes analysis/screen_v2_impact.txt
and data/phase1/screen_v2_candidates.jsonl (for classification if approved).

v2 additions target classic titles without our v1 keywords (Prange, Stern, MMT,
LLL, Kannan, Fincke-Pohst, Arora-Ge, Shoup/Nechaev bounds, Pollard 1978, Cheon)
and keep 'discrete log'-only titles (v1 dropped them as too weak).
"""
import json, re, collections, glob, os
def norm(t): return re.sub(r"[^a-z0-9]+", "", (t or "").lower())[:60]
V2 = {
 "code": [r"information sets?\b", r"decod\w* (of )?(random|general|arbitrary|binary)? ?linear (block )?codes",
          r"codewords? of (small|low|minimum) weight|(small|low|minimum)[- ]weight (code ?words?|words)", r"statistical decoding",
          r"generalized birthday", r"nearest neighbou?rs?.{0,40}decod|decod.{0,40}nearest neighbou?r"],
 "lattice": [r"short(est)? (lattice )?vectors?|vectors? of short length", r"gauss ?sieve|lattice points?\b", r"integer programming",
             r"basis reduction|reduced bas[ie]s|block(wise)? (korkine|reduction|lattice)", r"(learning|learn) (in|with) (the )?presence of errors",
             r"closest vector|nearest (lattice|vector) point", r"factoring polynomials with rational coefficients",
             r"convolution modular lattice|dimension reduction.{0,40}lattice", r"\blattice algorithms?\b"],
 "ecdlp": [r"discrete logarithm|discrete log\b", r"index computation", r"\brho method|\bpollard\b", r"(generic|black[- ]box) (group|algorithm)s?",
           r"auxiliary inputs?", r"diffie[- ]hellman problem", r"multiple discrete", r"collisions? of random walks"],
 "comparator": [r"block (wiedemann|lanczos)", r"factori[sz]ation (algorithm|method)s?|factoring (integers|algorithm|method)",
                r"\bsieve\b.{0,40}(factor|number)|(factor|number).{0,40}\bsieve\b", r"class groups?.{0,30}(comput|algorithm)"],
}
V2C = {k: [re.compile(p, re.I | re.S) for p in v] for k, v in V2.items()}
src = open("pipeline/candidates.py").read().split("counts = collections.Counter()")[0]
ns = {}; exec(src, ns); PC = ns["PC"]; CTX = re.compile(r"crypt|attack|secur|cipher|\bkeys?\b|signature|\bkem\b|post[- ]quantum|factor|lattice|decod", re.I)

def v1hits(text):
    h = {c: [lab for rx, lab in pats if rx.search(text)] for c, pats in PC.items()}
    h = {c: v for c, v in h.items() if v}
    if h.get("ecdlp") == ["dlog generic"] and len(h) == 1: h = {}
    return h

have = set()
for p in ["data/labeled_final.jsonl", "data/phase1/labeled_final.jsonl", "data/candidates_phase1.jsonl"]:
    for l in open(p): have.add(norm(json.loads(l)["title"]))

# merged universe: reuse the Phase 1 merged pull by scanning raw sources (titles + abstracts)
recs = {}
def add(t, ab, rid, src, venue, year, authors, doi=""):
    k = norm(t)
    if len(k) < 10 or k in have: return
    r = recs.setdefault(k, {"id": rid, "title": t, "abstract": "", "sources": set(), "venue": venue, "year": year, "authors": authors, "doi": doi})
    r["sources"].add(src)
    if len(ab or "") > len(r["abstract"]): r["abstract"] = ab
for l in open("data/raw/dblp/dblp_candidates.jsonl"):
    w = json.loads(l)
    if (w.get("venue") or "").startswith("IACR Cryptol. ePrint"): continue
    add(w["title"], "", "dblp:" + w["key"], "dblp", w.get("venue"), w.get("year"), w.get("authors", []), w.get("doi", ""))
for p in glob.glob("data/raw/openalex/*.jsonl") + glob.glob("data/raw/zbmath/*.jsonl"):
    if os.path.basename(p).startswith("seeds"): continue
    for l in open(p, encoding="utf-8"):
        try: w = json.loads(l)
        except json.JSONDecodeError: continue
        if not w.get("title"): continue
        rid = w.get("openalex_id") or ("zb:" + str(w.get("zbmath_id")))
        add(w["title"], w.get("abstract", ""), rid, "openalex" if "openalex_id" in w else "zbmath", w.get("venue"), w.get("year"), w.get("authors", []), w.get("doi", ""))
for l in open("data/eprint.jsonl"):
    r = json.loads(l); add(r["title"], r["abstract"], r["eprint_id"], "eprint", "IACR ePrint", r["year"], r["authors"])

out, cnt, by_era = [], collections.Counter(), collections.Counter()
for k, r in recs.items():
    text = r["title"] + " \n " + r["abstract"]
    if v1hits(text): continue  # v1 would already have screened it (then it is in 'have' or was tier B)
    h = {c: [p.pattern[:30] for p in pats if p.search(text)] for c, pats in V2C.items()}
    h = {c: v for c, v in h.items() if v}
    if not h: continue
    ctx = bool(CTX.search(text + " " + (r.get("venue") or ""))) or r["sources"] == {"eprint"}
    r = dict(r); r["sources"] = sorted(r["sources"]); r["kw_hits"] = h; r["v2_ctx"] = ctx
    out.append(r); cnt[(tuple(sorted(h)), ctx)] += 1
    y = int(str(r.get("year") or 0)[:4]) if str(r.get("year") or "")[:4].isdigit() else 0
    by_era["pre-2006" if y < 2006 else "2006+"] += 1
with open("data/phase1/screen_v2_candidates.jsonl", "w") as f:
    for r in out: f.write(json.dumps(r, ensure_ascii=False) + "\n")
lines = [f"v2 screen would add {len(out)} items not screened by v1 ({sum(1 for r in out if r['v2_ctx'])} with crypto/lattice/decoding context)",
         f"by era: {dict(by_era)}", f"by source: {dict(collections.Counter('|'.join(r['sources']) for r in out))}", "by class set and context:"]
for (cls, ctx), n in cnt.most_common(): lines.append(f"  {'+'.join(cls):30s} ctx={ctx}: {n}")
open("analysis/screen_v2_impact.txt", "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
