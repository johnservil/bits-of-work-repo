import re,html,sys
for f in sys.argv[1:]:
    s=open(f).read()
    t=re.sub(r'<script.*?</script>','',s,flags=re.S)
    i=t.find('</nav>'); t=t[i:] if i>0 else t
    t=re.sub(r'<(br|/p|/tr|/li|/h\d)[^>]*>','\n',t)
    t=re.sub(r'<[^>]+>',' ',t); t=html.unescape(t); t=re.sub(r'[ \t]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
    print('=====',f); print(t.strip()[:3000])
