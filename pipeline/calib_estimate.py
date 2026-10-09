#!/usr/bin/env python3
"""Person-year and dollar estimate for one calibration problem from merged labels.

Usage: calib_estimate.py LABELS.jsonl [cost_per_py=250000] [draws=20000] [seed=1]
LABELS.jsonl: one object per item with fields include, category, weight (rubric_calibration.md).
Priors (PLAN.md §8, total person-years per paper across authors, uniform over the range):
  A,C,F,H: 1-2   D: 0.5-1.5   E: 2-10   S: 0.5-1   G: side category, reported but not counted.
Borderline items are counted at half weight in a second ("with borderline") view.
Deterministic stdlib Monte Carlo; prints median and 5-95% range.
"""
import json, sys, random, collections
PRI = {"A": (1, 2), "C": (1, 2), "F": (1, 2), "H": (1, 2), "D": (0.5, 1.5), "E": (2, 10), "S": (0.5, 1)}
path = sys.argv[1]; COST = float(sys.argv[2]) if len(sys.argv) > 2 else 250000
N = int(sys.argv[3]) if len(sys.argv) > 3 else 20000; random.seed(int(sys.argv[4]) if len(sys.argv) > 4 else 1)
rows = [json.loads(l) for l in open(path)]
def items(view):
    out = []
    for r in rows:
        lab = r.get("label") or r
        inc, cat, w = lab.get("include"), lab.get("category"), float(lab.get("weight") or 0)
        if cat not in PRI: continue
        if inc == "yes": out.append((cat, w))
        elif inc == "borderline" and view == "with_borderline": out.append((cat, 0.5 * w))
    return out
def pct(xs, p): xs = sorted(xs); return xs[min(len(xs) - 1, int(p * len(xs)))]
cnt = collections.Counter((r.get("label") or r).get("include") for r in rows)
cats = collections.Counter((r.get("label") or r).get("category") for r in rows if (r.get("label") or r).get("include") == "yes")
print(f"items {len(rows)}  include: {dict(cnt)}  yes-categories: {dict(cats)}")
print(f"G (hardness/reduction, not counted): {cats.get('G', 0)}")
for view in ("yes_only", "with_borderline"):
    it = items(view); draws = []
    for _ in range(N):
        draws.append(sum(w * random.uniform(*PRI[c]) for c, w in it))
    med, lo, hi = pct(draws, .5), pct(draws, .05), pct(draws, .95)
    print(f"{view:16s} n={len(it):4d} weighted={sum(w for _, w in it):7.1f}  PY median {med:7.1f} [{lo:.1f}, {hi:.1f}]  "
          f"USD median {med*COST/1e6:6.2f}M [{lo*COST/1e6:.2f}M, {hi*COST/1e6:.2f}M]")
