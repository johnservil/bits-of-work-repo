#!/usr/bin/env python3
"""Build sourced histories of selected algorithmic bounds, not security forecasts.

Index tracks omit lower-order terms. Event tracks have no common numerical cost
model and are never assigned fabricated indices or infinite parameter sizes.
Run from any directory: python3 -I analysis/attack_stability.py
"""
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'data/attack_history'
TARGET = 128
END = 2026
ORDER = ['ecdlp', 'svp', 'sd', 'rsa', 'mq', 'ffdlp_small', 'ffdlp_pairing', 'sidh']
NUMERIC_TYPES = {'sqrt_group', 'power', 'linear', 'nlogn', 'L'}


def log2_cost(cost, size):
    """Leading-term index only; unknown/poly/quasipoly models have no number."""
    if not cost or cost['type'] not in NUMERIC_TYPES:
        return None
    t = cost['type']
    if t == 'sqrt_group':
        return size / 2 + math.log2(cost['k'])
    if t == 'power':
        return cost['exp'] * size
    if t == 'linear':
        return cost['c'] * size
    if t == 'nlogn':
        return cost['c'] * size * math.log2(size)
    ln_n = size * math.log(2)
    return cost['c'] * ln_n ** cost['a'] * math.log(ln_n) ** (1 - cost['a']) / math.log(2)


def size_for(cost, bits):
    """Size giving the chosen index, or None for an unspecified cost model.

    None means not estimated. It never means that no finite size can meet a
    work target, and it never implies a polynomial-time or practical break.
    """
    if not cost or cost['type'] not in NUMERIC_TYPES:
        return None
    t = cost['type']
    if t == 'sqrt_group':
        return 2 * (bits - math.log2(cost['k']))
    if t == 'power':
        return bits / cost['exp']
    if t == 'linear':
        return bits / cost['c']
    lo, hi = 4.0, 8.0
    while log2_cost(cost, hi) < bits:
        hi *= 2
        if hi > 1e12:
            raise ValueError('Index inversion exceeds supported range')
    for _ in range(100):
        mid = (lo + hi) / 2
        if log2_cost(cost, mid) < bits:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def in_series(m):
    # A superseded numerical claim cannot win forever via a running minimum.
    return (m.get('series') is True and m.get('status') == 'supported'
            and m.get('model') == 'classical'
            and (m.get('cost') or {}).get('type') in NUMERIC_TYPES
            and bool(m.get('source_url')))


def validate(p):
    if p['display_kind'] not in ('index', 'events'):
        raise ValueError(f"Unknown track type: {p['key']}")
    for m in p['milestones']:
        if not m.get('source_url', '').startswith('https://'):
            raise ValueError(f"Missing source: {p['key']}: {m['name']}")
        if m['year'] > END or str(m['year']) != str(m['date'])[:4]:
            raise ValueError(f"Inconsistent date: {p['key']}: {m['name']}")
        if m.get('series') and not in_series(m):
            raise ValueError(f"Unsupported series entry: {p['key']}: {m['name']}")
        if p['display_kind'] == 'events' and m.get('series'):
            raise ValueError('Event tracks cannot enter the quantitative series')


def analyse(p):
    validate(p)
    ms = sorted(p['milestones'], key=lambda m: (m['year'], m['date']))
    for m in ms:
        m['in_series'] = in_series(m)
    if p['display_kind'] == 'events':
        return {'steps': [], 'size_steps': [], 'metrics': None}
    selected = [m for m in ms if m['in_series']]
    if not selected:
        raise ValueError(f"No selected bounds: {p['key']}")
    ref = p['reference']['size']
    steps, sizes = [], []
    # Minimize reference index and maximize inverse threshold independently:
    # algorithms can cross, so these need not have the same winner.
    for year in sorted({max(m['year'], p['from_year']) for m in selected}):
        known = [m for m in selected if m['year'] <= year]
        best = min(known, key=lambda m: log2_cost(m['cost'], ref))
        size_best = max(known, key=lambda m: size_for(m['cost'], TARGET))
        for output, winner, value, field in (
            (steps, best, log2_cost(best['cost'], ref), 'cost'),
            (sizes, size_best, size_for(size_best['cost'], TARGET), 'size'),
        ):
            if not output or abs(output[-1][field] - value) > 1e-9:
                output.append({'year': year, field: value, 'name': winner['name'],
                               'authors': winner['authors'], 'ref': winner['ref'],
                               'source_url': winner['source_url'],
                               'assumptions': winner.get('assumptions', '')})
    first, last = steps[0], steps[-1]
    return {'steps': steps, 'size_steps': sizes, 'metrics': {
        'first_year': first['year'], 'first_cost': first['cost'],
        'current_cost': last['cost'], 'index_drop': first['cost'] - last['cost'],
        'first_size': sizes[0]['size'], 'current_size': sizes[-1]['size'],
        'last_bound_year': last['year'],
    }}


def formula(c):
    if not c:
        return 'not parameterized'
    t = c['type']
    if t == 'L':
        return f"L[{c['a']:.6g}, {c['c']:.6g}], lower-order terms omitted"
    if t == 'linear':
        return f"2^({c['c']:.6g} n)"
    if t == 'nlogn':
        return f"n^({c['c']:.6g} n)"
    if t == 'power':
        return f"N^{c['exp']:.6g}"
    if t == 'sqrt_group':
        return f"{c['k']:.6g} sqrt(group order)"
    return t + ' (not numerically parameterized)'


def cell(v):
    return str(v).replace('|', r'\|').replace('\n', ' ')


def main():
    probs = [json.loads(f.read_text()) for f in SRC.glob('*.json')]
    probs.sort(key=lambda p: ORDER.index(p['key']))
    exported, csv_rows = [], []
    md = ['# Selected algorithmic bounds and attack events', '',
          'Generated by analysis/attack_stability.py. Source-checked by an agent on 2026-10-09; '
          'not independently verified by a human. This is a selected, incomplete history, not a security forecast.', '',
          '## Method', '',
          'Numerical tracks evaluate selected leading-term formulas at a declared reference size. '
          'They omit polynomial/lower-order factors and do not share a calibrated operation unit across algorithms. '
          'Their differences are changes in an index, not observed security bits lost. '
          'The inverse view finds the size giving index 128, not a recommended cryptographic parameter.', '',
          'Each series uses currently supported analyses, dated when the quoted analysis became public. '
          'Earlier algorithm dates and corrected claims are retained in notes. This is not a reconstruction '
          'of historical beliefs. Series eligibility is explicit and sourced; practicality is not a Boolean filter. '
          'The minimum is taken only over these selected bounds, independently for each view. '
          'No count of exponent changes or security-stability duration is inferred.', '',
          'Lattice indices describe an SVP oracle, not full ML-KEM attacks. Decoding indices maximize '
          'over code rates separately for each algorithm, not a single fixed-rate code. '
          'MQ bounds have explicit algebraic/randomization assumptions. See each track.', '',
          'Qualitative events cover finite-field reassessments and SIDH. A missing/inapplicable numerical model '
          'means not estimated, never infinite size or zero remaining security. No placeholder compute is used.', '',
          '## Index-track summary', '',
          '| Track | Reference size | First selected index | Latest selected index | Index decrease | Latest plotted bound | Size giving index 128, first → latest |',
          '|---|---|---|---|---|---|---|']
    for p in probs:
        result = analyse(p)
        exported.append(p | result)
        if result['metrics']:
            m = result['metrics']
            md.append('| ' + ' | '.join(map(cell, [
                p['label'], p['reference']['label'],
                f"{m['first_year']}: {m['first_cost']:.1f}",
                f"{m['current_cost']:.1f}", f"{m['index_drop']:.1f}",
                m['last_bound_year'],
                f"{m['first_size']:,.1f} → {m['current_size']:,.1f} {p['size_unit']}",
            ])) + ' |')
    for p in exported:
        md += ['', '## ' + p['label'], '', p['problem'], '', p['notes'], '']
        if p.get('assumptions'):
            md += ['Track assumptions: ' + p['assumptions'], '']
        if p['display_kind'] == 'index':
            md += [f"Reference: {p['reference']['label']}. {p['reference']['why']}", '']
        md += ['| Analysis date | Result | Treatment | Formula or event | Assumptions / qualifications | Source |',
               '|---|---|---|---|---|---|']
        for m in sorted(p['milestones'], key=lambda m: (m['year'], m['date'])):
            cost = m.get('cost')
            treatment = 'selected index' if m['in_series'] else m['status']
            description = (m.get('event') or m.get('context_formula')
                           or m.get('complexity_description') or formula(cost))
            source_links = [f"[{m['ref']}]({m['source_url']})"]
            extra_urls = m.get('additional_source_urls', [])
            if m.get('analysis_source_url'):
                extra_urls = extra_urls + [m['analysis_source_url']]
            if m.get('date_source_url'):
                extra_urls = extra_urls + [m['date_source_url']]
            source_links += [f'[Additional analysis {i}]({url})'
                             for i, url in enumerate(extra_urls, 1)]
            notes = ' '.join(filter(None, [m.get('notes'), m.get('dating_note')]))
            md.append('| ' + ' | '.join(map(cell, [
                m['date'], m['name'], treatment, description,
                ' '.join([m.get('assumptions', ''), notes]),
                '; '.join(source_links),
            ])) + ' |')
            numeric = m['in_series'] and p['display_kind'] == 'index'
            csv_rows.append([p['key'], m['date'], m['name'], treatment, description,
                             log2_cost(cost, p['reference']['size']) if numeric else '',
                             size_for(cost, TARGET) if numeric else '',
                             m.get('assumptions', ''), notes, m['source_url'],
                             '; '.join(extra_urls)])
    (ROOT / 'analysis/attack_stability.md').write_text('\n'.join(md) + '\n')
    output = ROOT / 'data/export'
    output.mkdir(exist_ok=True)
    (output / 'attack_history.json').write_text(json.dumps({
        'schema_version': 2, 'reviewed_on': '2026-10-09', 'target_index': TARGET,
        'end_year': END, 'problems': exported,
    }, indent=2, ensure_ascii=False) + '\n')
    with (output / 'attack_history.csv').open('w', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['problem', 'analysis_date', 'result', 'treatment', 'formula_or_event',
                    'reference_index', 'size_for_index_128', 'assumptions', 'notes',
                    'source_url', 'additional_source_urls'])
        w.writerows(csv_rows)
    print(f"Built {len(exported)} sourced tracks; "
          f"{sum(p['display_kind'] == 'index' for p in exported)} numerical, "
          f"{sum(p['display_kind'] == 'events' for p in exported)} qualitative.")


if __name__ == '__main__':
    main()
