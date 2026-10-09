import re,html,sys
for f in sys.argv[1:]:
    s=open(f).read()
    t=re.search(r'<title>(.*?)</title>',s,re.S)
    m=re.search(r'<h5[^>]*>\s*Abstract\s*</h5>(.*?)</p>',s,re.S)
    a=re.search(r'name="citation_author" content="([^"]*)"',s)
    au=re.findall(r'name="citation_author" content="([^"]*)"',s)
    d=re.findall(r'(History|Last revised|Submitted)[^<]*</[^>]+>\s*<[^>]+>([^<]*)',s)
    hist=re.search(r'<h5[^>]*>\s*History\s*</h5>(.*?)</dl>',s,re.S)
    ab=re.sub(r'<[^>]+>','',m.group(1)) if m else 'NO ABSTRACT'
    print('=====',f, html.unescape(t.group(1)).strip() if t else '')
    print('AUTHORS:',', '.join(au))
    if hist: print('HIST:',re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',hist.group(1)))[:300])
    print(re.sub(r'\s+',' ',html.unescape(ab)).strip())
