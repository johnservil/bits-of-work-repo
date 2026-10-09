#!/usr/bin/env python3
"""Author map, step 3: zbMATH Open author profiles, to complete publication
counts for mathematicians (DBLP misses much math-journal output).

Scope: persons with >= 1 included item (data/authors/authors.csv) who either have
no DBLP career data or publish fewer than MAX_RATE DBLP papers per career year;
for prolific DBLP authors zbMATH changes the output share little. 3 parallel
workers.
  1. zbMATH author search by name (up to 20 candidates).
  2. Accept the candidate whose zbMATH external ids include the person's DBLP
     pid (method zb_dblp), else their ORCID (zb_orcid), else the first
     name-compatible candidate (at most 3 tried) sharing at least one
     normalized title with the person's known work (zb_title): DBLP titles for
     DBLP persons, included-item titles for unresolved name strings.
  3. Fetch all of the accepted author's zbMATH documents: year, title hash
     (same hash as pipeline/authors_dblp.py), document type, MSC codes.

Output (resumable): data/raw/enrich/zbmath/<person-hash>.json
Usage: python3 -I pipeline/authors_zbmath.py
"""
import csv, json, os, re, sys, time, hashlib, urllib.parse
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, "pipeline")
from authors_dblp import norm_title, full_norm, strip_homonym
from authors_enrich import get, persons

OUT = "data/raw/enrich/zbmath"
MAX_RATE = 1.5
WORKERS = 3
API = "https://api.zbmath.org/v1"


def th(title):
    return hashlib.md5(norm_title(title).encode()).hexdigest()[:10]


def title_of(d):
    t = d.get("title")
    return (t.get("title") if isinstance(t, dict) else t) or ""


def search_authors(name):
    body = get(f"{API}/author/_search?" + urllib.parse.urlencode({"search_string": name, "results_per_page": 20}), delay=3)
    return (json.loads(body).get("result") or []) if body else []


def documents(code, cap=2000):
    docs = []
    for page in range(cap // 100):
        body = get(f"{API}/document/_search?" + urllib.parse.urlencode(
            {"search_string": f"ai:{code}", "page": page, "results_per_page": 100}), delay=3)
        res = (json.loads(body).get("result") or []) if body else []
        for d in res:
            y = str(d.get("year") or "")[:4]
            docs.append({"year": int(y) if y.isdigit() else None, "th": th(title_of(d)),
                         "type": (d.get("document_type") or {}).get("code"),
                         "msc": [c.get("code") for c in d.get("msc") or []][:3]})
        if len(res) < 100: break
        time.sleep(0.5)
    return docs


def similar(a, b):
    """Titles match if >= 70% of the shorter title's words (3+ letters) appear in the other."""
    wa = {w for w in re.sub(r"[^a-z0-9 ]", " ", a.lower()).split() if len(w) > 2}
    wb = {w for w in re.sub(r"[^a-z0-9 ]", " ", b.lower()).split() if len(w) > 2}
    return bool(wa and wb) and len(wa & wb) >= 0.7 * min(len(wa), len(wb))


def title_check(code, titles):
    """Cheap verification: does author `code` have a zbMATH document matching one of these titles?"""
    for t in list(titles)[:2]:
        words = [w for w in re.sub(r"[^A-Za-z0-9 ]", " ", t).split() if len(w) > 2][:5]
        if len(words) < 2: continue
        body = get(f"{API}/document/_search?" + urllib.parse.urlencode(
            {"search_string": f"ai:{code} & ti:{' '.join(words)}", "results_per_page": 5}), delay=3)
        res = (json.loads(body).get("result") or []) if body else []
        if any(similar(title_of(d), t) for d in res):
            return True
    return False


def compatible(person_name, cand):
    a = full_norm(person_name).split()
    for sp in cand.get("spellings") or [{"first_name": "", "last_name": cand.get("name", "")}]:
        b = full_norm(f"{sp.get('first_name', '')} {sp.get('last_name', '')}").split()
        if a and b and a[-1] == b[-1] and a[0][0] == b[0][0]: return True
    return False


def in_scope(r):
    if not r.get("dblp_pubs"): return True
    return int(r["dblp_pubs"]) / max(1, int(r["career_years"])) < MAX_RATE


def one(r, stats, item_titles, raw_titles):
    fn = f"{OUT}/{hashlib.md5(r['person'].encode()).hexdigest()[:16]}.json"
    if os.path.exists(fn): return
    name = strip_homonym(r["person"][5:] if r["person"].startswith("name:") else r["person"])
    known = set((stats.get(r["person"]) or {}).get("pubs", {})) | item_titles.get(r["person"], set())
    cands = search_authors(name)
    pick, method, docs = None, None, None
    for c in cands:
        ext = {(e["type"], e["external_id"]) for e in c.get("external_ids") or []}
        if r["dblp_pid"] and ("dblp", r["dblp_pid"]) in ext: pick, method = c, "zb_dblp"; break
        if r["orcid"] and ("orcid", r["orcid"]) in ext: pick, method = c, "zb_orcid"; break
    if not pick:
        tried = 0
        for c in cands:
            if tried >= 3: break
            if not compatible(name, c): continue
            tried += 1
            if title_check(c["code"], raw_titles.get(r["person"], ())): pick, method = c, "zb_title"; break
    rec = {"person": r["person"], "n_candidates": len(cands), "method": method}
    if pick:
        rec.update({"code": pick["code"], "zb_name": pick.get("name"),
                    "external_ids": {e["type"]: e["external_id"] for e in pick.get("external_ids") or []},
                    "main_fields": [(f["field"], f["count"]) for f in pick.get("main_fields") or []],
                    "docs": docs if docs is not None else documents(pick["code"])})
    json.dump(rec, open(fn + ".tmp", "w")); os.replace(fn + ".tmp", fn)
    time.sleep(0.5)


def main():
    os.makedirs(OUT, exist_ok=True)
    stats = json.load(open("data/raw/dblp/authors_stats.json"))["stats"]
    item_titles, raw_titles = {}, {}
    for r in csv.DictReader(open("data/authors/authorships.csv")):
        item_titles.setdefault(r["person"], set()).add(th(r["title"]))
        raw_titles.setdefault(r["person"], []).append(r["title"])
    # Priority: people with >= 2 included items or no DBLP career data; then the one-item DBLP
    # authors in seeded random order (analysis/author_map.py corrects any not yet fetched by the
    # ratio measured on those fetched).
    import random
    ppl = [r for r in persons() if in_scope(r)]
    prio = [r for r in ppl if int(r["n_items_yes"]) >= 2 or not r.get("dblp_pubs")]
    rest = [r for r in ppl if r not in prio]; random.Random(20261009).shuffle(rest)
    ppl = prio + rest
    print(f"{len(ppl)} persons in scope ({len(prio)} priority)", flush=True)
    with ThreadPoolExecutor(WORKERS) as ex:
        for n, _ in enumerate(ex.map(lambda r: one(r, stats, item_titles, raw_titles), ppl)):
            if n % 100 == 0: print(f"  {n}/{len(ppl)}", flush=True)


if __name__ == "__main__":
    main()
