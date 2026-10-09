import re,html,sys,json,os
keys=['Length','Challenge provider','Weight','Vector','Authors','Algorithm','Hardware','Runtime','Claimed runtime','Comments','Date']
out=[]
for f in sorted(os.listdir('rec')):
    s=open('rec/'+f).read()
    t=re.sub(r'<script.*?</script>','',s,flags=re.S)
    i=t.find('</nav>'); t=t[i:] if i>0 else t
    t=re.sub(r'<(br|/p|/tr|/li|/h\d|/td|/th|/dt|/dd|/div)[^>]*>','\n',t)
    t=re.sub(r'<[^>]+>',' ',t); t=html.unescape(t)
    lines=[l.strip() for l in t.split('\n') if l.strip()]
    d={'file':f}; cur=None
    for l in lines:
        if l in keys: cur=l; d[cur]=''; continue
        if l.startswith('Details on record'): d['record']=l.split()[-1]; continue
        if cur and cur!='Vector': d[cur]=(d[cur]+' '+l).strip()
    d.pop('Vector',None)
    out.append(d)
for d in out: print(json.dumps(d,ensure_ascii=False))
