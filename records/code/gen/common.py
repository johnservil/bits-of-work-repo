import json, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
KEYS = ['id','class','problem','instance','instance_size','instance_size_unit','log2_ops','method',
        'structure_exploited','hardware','raw_compute','reported_core_years','gpu_years','wall_time_days',
        'date','solvers','academic','challenge','extrapolation','paper','source_url','other_urls',
        'confidence','verified','notes']
DEFAULTS = {'class':'code','log2_ops':None,'structure_exploited':False,'hardware':None,'raw_compute':None,
            'reported_core_years':None,'gpu_years':None,'wall_time_days':None,'academic':None,'challenge':None,
            'extrapolation':None,'paper':None,'other_urls':[],'verified':False,'notes':None,'instance_size_unit':'n'}
def write(rec, header=None):
    r = dict(DEFAULTS); r.update(rec); r['verified'] = False
    for k in r:
        assert k in KEYS, k
    for k in KEYS:
        assert k in r, (r.get('id'), k)
    path = os.path.join(OUT, r['id'] + '.yaml')
    with open(path, 'w') as f:
        f.write('# computational record, code-based class (records/README.md format); agent-transcribed, unverified\n')
        if header: f.write('# ' + header + '\n')
        for k in KEYS:
            f.write('%s: %s\n' % (k, json.dumps(r[k], ensure_ascii=False)))
    return path
def cy_from_days(d): return round(d/365.25, 4)
def cy_from_hours(h): return round(h/8766, 6)
