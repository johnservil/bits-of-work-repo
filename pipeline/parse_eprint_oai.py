#!/usr/bin/env python3
"""Parse harvested OAI-PMH pages into data/eprint.jsonl (one record per line)."""
import glob, json, os, sys, html
import xml.etree.ElementTree as ET

RAW = sys.argv[1] if len(sys.argv) > 1 else "data/raw/eprint"
OUT = sys.argv[2] if len(sys.argv) > 2 else "data/eprint.jsonl"
NS = {"oai": "http://www.openarchives.org/OAI/2.0/",
      "dc": "http://purl.org/dc/elements/1.1/",
      "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/"}

seen = set(); n = 0; deleted = 0
with open(OUT, "w") as out:
    for path in sorted(glob.glob(os.path.join(RAW, "page_*.xml"))):
        root = ET.parse(path).getroot()
        for rec in root.iter("{%s}record" % NS["oai"]):
            hdr = rec.find("oai:header", NS)
            if hdr.get("status") == "deleted":
                deleted += 1; continue
            ident = hdr.findtext("oai:identifier", "", NS)
            eid = ident.split("oai:eprint.iacr.org:")[-1]  # e.g. 2026/2382
            if eid in seen: continue
            seen.add(eid)
            dc = rec.find("oai:metadata/oai_dc:dc", NS)
            if dc is None: continue
            def all_(tag): return [html.unescape((e.text or "").strip()) for e in dc.findall("dc:" + tag, NS)]
            dates = all_("date")
            year = int(eid.split("/")[0])
            row = {
                "eprint_id": eid,
                "year": year,
                "title": " ".join((all_("title") or [""])[0].split()),
                "authors": all_("creator"),
                "author_count": len(all_("creator")),
                "category": (all_("subject") or [""])[0],
                "abstract": " ".join((all_("description") or [""])[0].split()),
                "date_first": min(dates) if dates else None,
                "date_last": max(dates) if dates else None,
                "url": f"https://eprint.iacr.org/{eid}",
            }
            out.write(json.dumps(row, ensure_ascii=False) + "\n"); n += 1
print(f"wrote {n} records ({deleted} deleted stubs skipped) to {OUT}")
