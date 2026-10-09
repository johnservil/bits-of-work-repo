import re, html, sys, json
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.rows=[]; s.row=None; s.cell=None; s.href=None; s.heads=[]; s.inth=False
    def handle_starttag(s,tag,a):
        a=dict(a)
        if tag=='tr': s.row=[]; s.href=None
        elif tag in('td','th') and s.row is not None: s.cell=''; s.inth=(tag=='th')
        elif tag=='a' and s.cell is not None and 'record' in a.get('href',''): s.href=a['href']
    def handle_endtag(s,tag):
        if tag in('td','th') and s.cell is not None:
            s.row.append(re.sub(r'\s+',' ',s.cell).strip()); s.cell=None
        elif tag=='tr' and s.row is not None:
            if s.row: s.rows.append((s.row,s.href))
            s.row=None
    def handle_data(s,d):
        if s.cell is not None: s.cell+=d
for f in sys.argv[1:]:
    p=P(); p.feed(open(f).read())
    for r,h in p.rows: print(json.dumps([f,r,h]))
