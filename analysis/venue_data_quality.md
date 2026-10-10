# Venue data: sources, coverage and data-quality findings (2026-10-10)

Companion to `analysis/venue_resolution.md` (generated tables). This track answers "where was each
counted paper published?"; it makes no reputation judgment yet.

## What the export's `venue` column was

- 907 ePrint rows: the ePrint *category* ("Public-key cryptography"), not a venue.
- ~300 counted rows blank; many OpenAlex rows named a repository (arXiv, HAL, Zenodo), a series
  ("Lecture notes in computer science"), or a misattributed source (OpenAlex files Japanese NDL/CiNii
  theses under the journal "Medical Entomology and Zoology").

## Sources used, in order of trust

1. DBLP record itself (dblp:* ids).
2. DBLP records with the same normalized title and a shared author (full 2026-10-09 dump; 8.78M records).
3. Retitled DBLP versions (shared authors, trigram Dice >= 0.5): >= 0.85 accepted; lower ones were
   checked by an agent (data/venues/fuzzy_checks.csv: 78 same, 46 different) or stay `unverified`.
4. Crossref for the item's DOI (container and proceedings titles; LNCS chapters resolve to the conference).
5. zbMATH venue string, plus the zbMATH API for proceedings collections.
6. OpenAlex locations (all hosts of the work); OpenAlex title search (78 of 327 queries so far).
7. ePrint "Publication info" from each abstract page (all 907 counted ePrint papers).

Rows use `confidence`; the bibliography applies only rows with confidence >= 0.7.

## Coverage (counted items, n = 2877)

| refereed status | items |
|---|---:|
| registered peer-reviewed venue (`yes`) | 1444 |
| peer-reviewed by source type, venue not in registry (`likely`) | 755 |
| thesis | 121 |
| preprint / report only (`no`) | 490 |
| weak candidate only (`unverified`) | 27 |
| no venue source (`unknown`) | 40 |

(See `analysis/venue_resolution.md` for current numbers; the table above is a snapshot.)
For the 281 ePrint papers marked `no`, neither DBLP nor the ePrint page names a published version.
Some will be retitled versions that the author/title rules missed, so treat that as an upper bound on
"never published".

## Findings that affect counts (not applied; need a decision)

1. **Duplicates.** 99 groups of counted records are verified versions of the same work
   (data/venues/duplicate_checks.csv; 10 more groups were judged different). 102 extra records.
   Relations: ePrint+conference 28, ePrint+journal 19, conference+journal 10, thesis title in two
   languages 8, arXiv+venue 12, two records of one paper 8, other 14.
   PLAN.md says ePrint and venue versions are merged into one item; the title-based merge missed
   retitled ones. Counting each group once lowers class weights by: lattices 3.8%, ECDLP 3.7%,
   syndrome decoding 3.4%, factoring/FF-DLP 2.5%, isogenies 5.0%, multivariate 5.2%.
   This is a lower bound: only pairs that DBLP/OpenAlex could link were found.
   Whether conference + journal versions count once is a policy choice that PLAN.md does not state.
2. **Years.** 32 items have a source dating the work 2+ years before the counted year (flag
   `year-earlier-than-counted` in data/venues/venue_flags.csv). Most are journal versions of earlier
   conference papers or preprints (e.g. Shor, SICOMP 1997, counted 1999); a few look like OpenAlex
   date errors. The bibliography keeps the counted year for grouping.
3. **Wrong DOIs.** 5 `doi-title-mismatch` flags; most are translated titles, one (zb:0796.94006) is a
   wrong DOI.

## Open items

- OpenAlex title search for 249 remaining unresolved non-ePrint items: needs `~/.openalex_key` on this
  Mac (absent) or the free quota after midnight UTC
  (`python3 -I pipeline/fetch_openalex_title_search.py <ids>`).
- 18 fuzzy and 9 weak-search candidates remain unverified (flags in venue_flags.csv).
- Not used: the DBLP search API and SCImago (both now behind bot checks).

## Rebuild

```
python3 -I pipeline/fetch_eprint_pubinfo.py
python3 -I pipeline/fetch_crossref.py
python3 -I pipeline/fetch_openalex_locations.py
python3 -I pipeline/match_dblp_versions.py DBLP.xml.gz dblp.dtd
python3 -I pipeline/build_venue_table.py
python3 -I pipeline/search_dblp_local.py DBLP.xml.gz dblp.dtd
python3 -I pipeline/build_venue_table.py
```
