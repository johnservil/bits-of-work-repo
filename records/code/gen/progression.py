import json,re
recs={}
for l in open('recs.jsonl'):
    d=json.loads(l); recs[d['file'].replace('.html','')]=d
hof={}
for l in open('hof_rows.jsonl'):
    f,r,h=json.loads(l)
    if not h: continue
    t=f[4:-5]
    hof.setdefault(t,[]).append((r,h))
out={}
for t,rows in hof.items():
    items=[]
    for r,h in rows:
        key=h.replace('/','_')
        d=recs[key]
        if t=='low-weight':
            w=int(r[0]); n=1280; date=r[4]; auth=r[1]; alg=r[3]
        else:
            n=int(r[0]); w=int(r[1]); auth=r[2]; alg=r[3]; date=r[4]
        items.append(dict(track=t,n=n,w=w,authors=auth,alg=alg,date=date,rec=h,recid=int(h.split('/')[-1]),
            provider=d.get('Challenge provider'),length_field=d.get('Length'),hardware=d.get('Hardware'),
            runtime=d.get('Runtime') or d.get('Claimed runtime'),comments=d.get('Comments')))
    items.sort(key=lambda x:(x['date'],x['recid']))
    prog=[]; best=None
    for it in items:
        better = (best is None) or (it['w']<best if t=='low-weight' else it['n']>best)
        if better:
            best = it['w'] if t=='low-weight' else it['n']
            if prog and prog[-1]['authors']==it['authors'] and prog[-1]['date']==it['date']:
                prog[-1]=it
            else: prog.append(it)
    out[t]={'all':items,'prog':prog}
json.dump(out,open('dc.json','w'),ensure_ascii=False,indent=0)
for t in out:
    print('==',t,len(out[t]['all']),len(out[t]['prog']))
    for p in out[t]['prog']: print(' ',p['n'],p['w'],p['date'],p['authors'][:40],'|',p['alg'][:30],'|',p['hardware'][:40],'|',p['runtime'][:50])
