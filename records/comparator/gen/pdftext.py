import re, sys, zlib
data = open(sys.argv[1], 'rb').read()
out = []
for m in re.finditer(rb'stream\r?\n(.*?)\r?\nendstream', data, re.S):
    s = m.group(1)
    try:
        d = zlib.decompress(s)
    except Exception:
        try: d = zlib.decompressobj().decompress(s)
        except Exception: continue
    # extract text from TJ/Tj
    parts = []
    for t in re.finditer(rb'\[(.*?)\]\s*TJ|\((.*?)(?<!\\)\)\s*Tj|(T\*|Td|TD|ET)', d, re.S):
        if t.group(1) is not None:
            arr = t.group(1)
            seg = b''
            for x in re.finditer(rb'\((.*?)(?<!\\)\)|(-?\d+\.?\d*)', arr, re.S):
                if x.group(1) is not None: seg += x.group(1)
                elif x.group(2) and float(x.group(2)) < -200: seg += b' '
            parts.append(seg)
        elif t.group(2) is not None:
            parts.append(t.group(2))
        else:
            parts.append(b'\n' if t.group(3) in (b'ET', b'T*') else b' ')
    if parts:
        out.append(b''.join(parts))
txt = b'\n'.join(out).decode('latin-1')
txt = txt.replace('\\(', '(').replace('\\)', ')')
sys.stdout.write(txt)
