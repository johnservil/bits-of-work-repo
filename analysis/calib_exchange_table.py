#!/usr/bin/env python3
"""Join per-problem human effort estimates (data/ai_effort/calib/*/labeled_final.jsonl) with
AI-side per-attempt costs (data/ai_effort/erdos_problems.csv) into one table.

Usage: python3 -I analysis/calib_exchange_table.py > analysis/calib_exchange_table.md
Human PY uses the same priors as pipeline/calib_estimate.py (A/C/F/H 1-2, D 0.5-1.5, E 2-10, S 0.5-1; G excluded);
the point estimate is the midpoint sum, the range is the prior-range sum. USD at $250k/PY.
AI side: successful-attempt dollars/hours as disclosed (Epoch, Nexus); blank where undisclosed.
"""
import json, glob, os, csv, collections
PRI = {"A": (1, 2), "C": (1, 2), "F": (1, 2), "H": (1, 2), "D": (0.5, 1.5), "E": (2, 10), "S": (0.5, 1)}
COST = 250000
ai = collections.defaultdict(lambda: {"attempts": 0, "successes": 0, "usd": 0.0, "usd_n": 0, "hours": 0.0, "hours_n": 0, "models": set()})
for r in csv.DictReader(open("data/ai_effort/erdos_problems.csv")):
    pn = r["problem_number"].split(".")[0]
    a = ai[pn]; a["attempts"] += 1; a["models"].add(r["model"])
    ok = r["outcome"].strip().lower() in ("resolved", "solved", "proved", "disproved", "success")
    if ok: a["successes"] += 1
    if r.get("cost_usd", "").strip():
        try: a["usd"] += float(r["cost_usd"]); a["usd_n"] += 1
        except ValueError: pass
    if r.get("hours", "").strip():
        try: a["hours"] += float(r["hours"]); a["hours_n"] += 1
        except ValueError: pass
rows = []
for d in sorted(glob.glob("data/ai_effort/calib/*/labeled_final.jsonl")):
    P = os.path.basename(os.path.dirname(d)); items = [json.loads(l) for l in open(d)]
    lo = hi = 0.0; n_yes = n_b = 0; solved_by = []
    for r in items:
        L = r.get("label") or r; c = L.get("category"); w = float(L.get("weight") or 0)
        if L.get("include") == "yes": n_yes += 1
        elif L.get("include") == "borderline": n_b += 1; w *= 0.5
        else: continue
        if c in PRI: lo += w * PRI[c][0]; hi += w * PRI[c][1]
        if L.get("solves"): solved_by.append(("AI " if L.get("ai_assisted") else "") + (r.get("title") or "")[:50] + f" ({r.get('year')})")
    mid = (lo + hi) / 2
    pn = P.split("-", 1)[1] if P.startswith("erdos-") else None; a = ai.get(pn) if pn else None
    rows.append((P, len(items), n_yes, n_b, mid, lo, hi, mid * COST / 1e6, a, solved_by))
print("| problem | pool | yes | border | human PY (range) | human USD | AI attempts (succ.) | AI USD on priced attempts | AI hours | solved by |")
print("|---|---|---|---|---|---|---|---|---|---|")
for P, n, y, b, mid, lo, hi, usd, a, sb in rows:
    ai_s = f"{a['attempts']} ({a['successes']})" if a else ""
    ai_u = f"${a['usd']:,.0f} over {a['usd_n']}" if a and a["usd_n"] else ""
    ai_h = f"{a['hours']:.0f} over {a['hours_n']}" if a and a["hours_n"] else ""
    print(f"| {P} | {n} | {y} | {b} | {mid:.1f} ({lo:.1f}-{hi:.1f}) | ${usd:.2f}M | {ai_s} | {ai_u} | {ai_h} | {'; '.join(sb)[:120]} |")
