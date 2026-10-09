#!/usr/bin/env python3
"""Records normalization (PLAN §7 steps 2-4), per user decisions of 2026-10-09:
- frontier metric = native instance size and log2(ops); core-year equivalents only
  for totals, always as [low, high] ranges (analysis/normalization.json);
- totals over record-setting solves only; Bitcoin-puzzle compute reported separately.

Outputs: analysis/records_normalized.md, data/export/records_normalized.csv.
Every derived figure carries a 'how' tag so it can be audited.
"""
import sys, re, json, math, csv, collections
sys.path.insert(0, "pipeline")
from load_records import all_records
CFG = json.load(open("analysis/normalization.json"))

def num(x):
    try: return float(x)
    except (TypeError, ValueError): return None
def year(r):
    m = re.match(r"(\d{4})", str(r.get("date") or "")); return int(m.group(1)) if m else None
def era_factor(y):
    tab = {int(k): v for k, v in CFG["cpu_core_year_by_era"].items() if k[0].isdigit()}
    ks = [k for k in sorted(tab) if y is not None and k <= y]
    return tab[ks[-1]] if ks else tab[min(tab)]
def is_btc(r): return "bitcoin" in str(r.get("challenge") or "").lower() or r["id"].startswith("btc-")
def workload(r):
    return {"ecdlp": "ecdlp", "lattice": "lattice", "code": "code"}.get(r["class"], "factoring" if r.get("problem") in ("factoring", "FF-DLP") else "other")

GPU = re.compile(r"(\d+)\s*(?:x|×|\*)?\s*(?:nvidia\s*)?(?:geforce\s*)?(rtx|gtx|titan|tesla|a100|v100|h100|gh200|gpu)", re.I)
GPU2 = re.compile(r"(\d+)\s+(?:\w+\s+){0,3}gpus?\b", re.I)
CORES = re.compile(r"(\d[\d,]*)\s*(?:cpu\s*)?(?:cores|threads)\b", re.I)
PS3 = re.compile(r"(\d+)\s*(?:sony\s*)?(?:playstation\s*3|ps3)s?", re.I)
FPGA = re.compile(r"(\d+)\s+(?:\w+[- ]?){0,3}fpgas?", re.I)
MIPS = re.compile(r"([\d,\.]+)\s*mips[- ]years?", re.I)
CPUH = re.compile(r"cpu time\s*([\d,\.]+)\s*h|([\d,\.]+)\s*(?:cpu|core)[- ]hours", re.I)

def core_years(r):
    """Return (low, high, how) in 2020 core-year equivalents, or (None, None, reason)."""
    y = year(r); lo_e, hi_e = era_factor(y)
    cy = num(r.get("reported_core_years"))
    if cy: return cy * lo_e, cy * hi_e, f"stated core-years x era({y})"
    gy = num(r.get("gpu_years"))
    wl = workload(r)
    if gy:
        f = CFG["device_year"].get(f"gpu:{wl}", CFG["device_year"]["gpu:other"]); return gy * f[0], gy * f[1], f"stated GPU-years x gpu:{wl}"
    text = " ".join(str(r.get(k) or "") for k in ("raw_compute", "hardware", "notes"))
    m = MIPS.search(text)
    if m:
        v = float(m.group(1).replace(",", "")); f = CFG["mips_year"]; return v * f[0], v * f[1], "MIPS-years"
    m = CPUH.search(text)
    if m:
        v = float((m.group(1) or m.group(2)).replace(",", "")) / 8766; return v * lo_e, v * hi_e, f"stated CPU-hours x era({y})"
    days = num(r.get("wall_time_days"))
    if days:
        for rx, kind in ((GPU, "gpu"), (GPU2, "gpu"), (PS3, "ps3"), (FPGA, "fpga"), (CORES, "core")):
            m = rx.search(text)
            if not m: continue
            n = float(m.group(1).replace(",", "")); dy = n * days / 365.25
            if kind == "core": return dy * lo_e, dy * hi_e, f"{int(n)} cores x {days:.3g} d x era({y})"
            f = CFG["device_year"].get(f"{kind}:{wl}") or CFG["device_year"]["gpu:other"]
            return dy * f[0], dy * f[1], f"{int(n)} {kind} x {days:.3g} d x {kind}:{wl}"
        if days < 2 and not any(rx.search(text) for rx in (GPU, GPU2, PS3, FPGA, CORES)):
            return days / 365.25 * lo_e, days / 365.25 * hi_e, f"single machine assumed, {days:.3g} d"
    return None, None, "no usable compute statement"

def group_key(r):
    sub = ""
    m = re.match(r"lwechal_n\d+_(a\d+)", r["id"])
    if m: sub = m.group(1)
    if r["id"].startswith("dc_low_weight"): sub = r["id"]  # every low-weight progression entry is its own record
    return (r["class"], r.get("problem"), str(r.get("challenge") or "paper"), bool(r.get("structure_exploited")), sub)

recs = [r for r in all_records() if not r["_summary"]]
groups = collections.defaultdict(list)
for r in recs: groups[group_key(r)].append(r)
record_setting = set()
for k, g in groups.items():
    best = None
    for r in sorted(g, key=lambda r: str(r.get("date") or "")):
        s = num(r.get("instance_size"))
        if s is not None and (best is None or s > best): best = s; record_setting.add(r["id"])

HOF_NOTES = {}
try:
    for h in csv.DictReader(open("records/lattice/svp_challenge_hof.csv")):
        HOF_NOTES[(h["dimension"], h["date"])] = h.get("algorithm_notes") or ""
except OSError: pass
def sieve_dim(r):
    text = " ".join(str(r.get(k) or "") for k in ("notes", "raw_compute", "method"))
    if r["id"].startswith("svpc_"):
        d = str(int(num(r.get("instance_size")) or 0)); text += " " + HOF_NOTES.get((d, str(r.get("date"))), "")
    m = re.search(r"max(?:imum)?\s+sieving\s+(?:dimension|rank|dim)\s*(?:was|of|=|:)?\s*(\d{2,3})", text, re.I)
    if m: return int(m.group(1)), "reported max sieving dimension"
    d = num(r.get("instance_size"))
    if d and r.get("problem") in ("approx-SVP", "SVP", "Ideal-SVP"): return int(round(d - d / math.log(d))), "dimension - d/ln d (estimated dims-for-free)"
    return None, ""

rows = []
for r in recs:
    lo, hi, how = core_years(r)
    sd, sd_how = sieve_dim(r) if r["class"] == "lattice" else (None, "")
    rows.append({"id": r["id"], "class": r["class"], "problem": r.get("problem"), "date": r.get("date"), "instance": r.get("instance"),
                 "instance_size": r.get("instance_size"), "unit": r.get("instance_size_unit"), "log2_ops_reported": r.get("log2_ops"),
                 "sieve_dim": sd, "sieve_dim_how": sd_how, "structure_exploited": bool(r.get("structure_exploited")),
                 "record_setting": r["id"] in record_setting, "bitcoin_puzzle": is_btc(r), "verified": r.get("verified"),
                 "core_years_low": lo, "core_years_high": hi, "core_years_how": how})

# empirical lattice slope: log2(core-years, geometric mid) vs sieving dimension, record-setting SVP-challenge solves since 2018
pts = [(x["sieve_dim"], math.log2(math.sqrt(x["core_years_low"] * x["core_years_high"]))) for x in rows
       if x["class"] == "lattice" and x["record_setting"] and x["sieve_dim"] and x["core_years_low"] and str(x["date"])[:4] >= "2018"
       and x["id"].startswith("svpc_")]
fit = None
if len(pts) >= 4:
    mx = sum(p[0] for p in pts) / len(pts); my = sum(p[1] for p in pts) / len(pts)
    sxx = sum((p[0] - mx) ** 2 for p in pts); sxy = sum((p[0] - mx) * (p[1] - my) for p in pts)
    if sxx > 0:
        b = sxy / sxx; res = [p[1] - (my + b * (p[0] - mx)) for p in pts]
        se = math.sqrt(sum(e * e for e in res) / max(1, len(pts) - 2) / sxx)
        fit = (b, se, len(pts))
slope_hi = CFG["lattice_model"]["slope_high"]  # sourced (DSvW 2021); our own fit is reported but not used
slope_lo = CFG["lattice_model"]["slope_low"]

def ecdlp_log2(bits): return bits / 2 + math.log2(math.sqrt(math.pi) / 2)
def lnfs_log2(bits):
    """Log2 of the leading GNFS L-expression, not measured operations or NIST strength."""
    lnN = bits * math.log(2); return (64 / 9) ** (1 / 3) * lnN ** (1 / 3) * math.log(lnN) ** (2 / 3) / math.log(2)

out = ["# Normalized computational records", "",
       "Generated by analysis/records_normalize.py from records/ and analysis/normalization.json.",
       "Decisions (user 2026-10-09): frontier in native units and log2(ops); compute totals in 2020 core-year",
       "equivalents as [low, high] ranges; totals over record-setting solves only; Bitcoin-puzzle compute separate.",
       "Values from records not verified by a human are provisional (10 of 338 verified).", ""]

out += ["## Frontier vs deployed targets", ""]
def best(cls, pred=lambda x: True, key="instance_size"):
    c = [x for x in rows if x["class"] == cls and x["record_setting"] and not x["bitcoin_puzzle"] and pred(x) and num(x[key]) is not None]
    return max(c, key=lambda x: num(x[key])) if c else None
e = best("ecdlp", lambda x: x["problem"] == "ECDLP" and not x["structure_exploited"])
eb = max((x for x in rows if x["bitcoin_puzzle"] and "kangaroo" in str(x["instance"]).lower() + str(x.get("problem")).lower() or (x["bitcoin_puzzle"] and x["problem"] == "interval-ECDLP" and num(x["instance_size"]) and num(x["instance_size"]) > 100)), key=lambda x: num(x["instance_size"]) or 0, default=None)
L = best("lattice", lambda x: x["id"].startswith("svpc_") and x["sieve_dim"], key="sieve_dim")  # TU Darmstadt SVP challenge only
f = best("comparator", lambda x: x["problem"] == "factoring" and not x["structure_exploited"] and "snfs" not in x["id"])
out += ["| Class | Largest public generic solve | Native size | log2 cost / model index | Target | Target native | Gap |", "|---|---|---|---|---|---|---|"]
if e:
    for t in CFG["targets"]["ECDLP"]:
        out.append(f"| ECDLP | {e['id']} ({e['date']}) | {num(e['instance_size']):.1f} bits | {ecdlp_log2(num(e['instance_size'])):.1f} | {t['name']} | {t['native']} bits (2^{t['log2_ops']}) | {t['log2_ops'] - ecdlp_log2(num(e['instance_size'])):.1f} bits of work |")
if eb:
    out.append(f"| ECDLP (non-academic, interval) | {eb['id']} ({eb['date']}) | {num(eb['instance_size']):.0f}-bit interval | ~{num(eb['instance_size'])/2+1:.0f} (kangaroo ~2*sqrt) | P-256 | 256 bits | {127.8 - (num(eb['instance_size'])/2+1):.0f} bits; interval DLP, not full ECDLP |")
if L:
    for t in CFG["targets"]["lattice"]:
        d = t["native"] - L["sieve_dim"]
        out.append(f"| Lattices | {L['id']} ({L['date']}) | sieving dim {L['sieve_dim']} ({L['sieve_dim_how']}) | {slope_lo * L['sieve_dim']:.0f} (core-SVP convention) | {t['name']} (beta {t['beta']}; core-SVP 2^{t['log2_core_svp']}, gates 2^{t['log2_gates']}) | sieving dim {t['native']} | {d} dims: {slope_lo * d:.0f}-{slope_hi * d:.0f} bits per sieve call |")
codes = [x for x in rows if x["class"] == "code" and x["record_setting"] and x["log2_ops_reported"] is not None and x["problem"] in ("SD-Goppa", "SD", "SD-QC")]
for prob in ("SD-Goppa", "SD-QC", "SD"):
    c = [x for x in codes if x["problem"] == prob and "dc_" in x["id"]]
    if c and prob in ("SD-Goppa", "SD-QC"):
        x = max(c, key=lambda x: num(x["log2_ops_reported"]))
        tg = next(t for t in CFG["targets"]["code"] if t["track"] == prob)
        if prob == "SD-Goppa":
            px = tg["site_scale_proxy"]; gap = px["log2"] - num(x["log2_ops_reported"])
            out.append(f"| Codes (Goppa/McEliece) | {x['id']} ({x['date']}) | n={x['instance_size']} | {num(x['log2_ops_reported']):.0f} (decodingchallenge: n x Dumer workfactor) | {tg['name']} (advanced ISD 2^{tg['log2_advanced_isd']['constant_memory']}-2^{tg['log2_advanced_isd']['sqrt_memory']}) | n={tg['native']} | {gap:.0f} bits on the site's own scale (proxy instance n={px['n']}) |")
        else:
            gap = tg["prange_log2"] - tg["qc_discount_bits"] - tg["frontier_prange_log2"]
            out.append(f"| Codes (QC/HQC) | {x['id']} ({x['date']}) | n={x['instance_size']} | {num(x['log2_ops_reported']):.0f} (decodingchallenge) / {tg['frontier_prange_log2']} (Prange) | {tg['name']} (advanced ISD 2^{tg['log2_advanced_isd']['constant_memory']}) | n={tg['native']} | ~{gap:.0f} bits (Prange iterations both ends, QC discount {tg['qc_discount_bits']}; approximate) |")
if f:
    t = CFG["targets"]["comparator"][0]
    target_bits = num(t["native"])
    record_index = lnfs_log2(num(f["instance_size"]))
    target_index = lnfs_log2(target_bits)
    gap = target_index - record_index
    out.append(f"| Factoring | {f['id']} ({f['date']}) | {num(f['instance_size']):.0f} bits | {record_index:.2f} (leading GNFS index, not measured ops) | {t['name']} (NIST strength {t['log2_ops']}-bit; separate convention) | {target_bits:.0f} bits; GNFS index {target_index:.2f} | ~{gap:.2f} bits (~{2 ** gap:.2g}x work); leading-term heuristic |")
out += ["", f"Lattice slope range: low {slope_lo} (asymptotic); high {slope_hi:.3f} " +
        "(Ducas-Stevens-van Woerden 2021 GPU sieving fit)" + (f"; our own fit over {fit[2]} record-setting SVP-challenge solves since 2018 gave {fit[0]:.3f} +- {fit[1]:.3f} and is not used (confounded by hardware/algorithm progress)" if fit else "") + ". Gaps are per sieve call; the full primal attack adds roughly 2^9 for ML-KEM-512 (spec). See analysis/normalization_method.md.",
        "The SVP challenge is approx-SVP (norm <= 1.05 GH); its record is used via the solver-reported maximum sieving dimension.",
        "Only a common size-independent multiplicative cost factor cancels in a same-model gap. Size-dependent costs, exponent coefficients, and omitted lower-order terms do not.",
        "RSA: the leading GNFS expression gives log2 L(2^896) = 81.86 and log2 L(2^2048) = 116.88, hence a 35.02-bit gap (about 35 billion times the work). These indices are not calibrated operation counts. NIST's 112-bit RSA-2048 strength is not subtracted from 81.86. Memory, communication, parameter selection and hardware efficiency can change the practical ratio; this is not a runtime or dollar forecast. See the RSA check in analysis/normalization_method.md.", ""]

out += ["## Compute totals over record-setting solves (2020 core-year equivalents, low-high)", "",
        "| Class | record-setting solves | with compute | total low | total high | largest single solve (high) |", "|---|---|---|---|---|---|"]
for cls in ["ecdlp", "lattice", "code", "comparator"]:
    c = [x for x in rows if x["class"] == cls and x["record_setting"] and not x["bitcoin_puzzle"]]
    w = [x for x in c if x["core_years_low"] is not None]
    big = max(w, key=lambda x: x["core_years_high"], default=None)
    out.append(f"| {cls} | {len(c)} | {len(w)} | {sum(x['core_years_low'] for x in w):,.0f} | {sum(x['core_years_high'] for x in w):,.0f} | "
               + (f"{big['id']} {big['core_years_high']:,.0f}" if big else "") + " |")
b = [x for x in rows if x["bitcoin_puzzle"]]; bw = [x for x in b if x["core_years_low"] is not None]
out += ["", f"Bitcoin puzzle (reported separately, non-academic, interval ECDLP / brute force): {len(b)} solves, {len(bw)} with usable compute, "
        f"{sum(x['core_years_low'] for x in bw):,.0f}-{sum(x['core_years_high'] for x in bw):,.0f} core-year equivalents (most solvers publish no compute; lower bound).", ""]
out += ["## Record-setting solves with derived compute", "", "| id | date | size | core-years low-high | how |", "|---|---|---|---|---|"]
for x in sorted([x for x in rows if x["record_setting"]], key=lambda x: (x["class"], str(x["date"]))):
    cy = f"{x['core_years_low']:,.3g}-{x['core_years_high']:,.3g}" if x["core_years_low"] is not None else "-"
    out.append(f"| {x['id']} | {x['date']} | {x['instance_size']} {x['unit'] or ''} | {cy} | {x['core_years_how']} |")
open("analysis/records_normalized.md", "w").write("\n".join(out) + "\n")
with open("data/export/records_normalized.csv", "w", newline="") as fh:
    wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); wr.writeheader(); wr.writerows(rows)
print("\n".join(out[:40]))
