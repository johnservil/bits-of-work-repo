# Author map: results (2026-10-09)

Method: analysis/author_map_method.md. Numbers: analysis/author_map.txt.
Rebuild order (no API cost except the enrichment fetches, which cache):

```bash
python3 -I pipeline/authors_dblp.py match          # ~5 min, local DBLP dump
python3 -I pipeline/authors_dblp.py stats          # ~5 min
python3 -I analysis/author_map.py > analysis/author_map.txt   # first pass: person list
python3 -I pipeline/authors_enrich.py wikidata     # SPARQL, ~1 min
python3 -I pipeline/authors_zbmath.py              # zbMATH API, ~2-3 h uncached
python3 -I pipeline/authors_enrich.py orcid        # ORCID public API, ~25 min uncached
python3 -I pipeline/authors_enrich.py mgp          # Math Genealogy, 10 s crawl delay
python3 -I analysis/career_stage.py > analysis/career_stage.txt
python3 -I analysis/author_map.py > analysis/author_map.txt
python3 -I analysis/classified_scenarios.py > analysis/classified_scenarios.txt
```

Tables in data/authors/: authors.csv (one row per person), authorships.csv,
coauthor_edges.csv, career.csv (PhD year, sector, zbMATH match),
fte_by_year.csv (per class and year: research-FTE, calendar person-years,
cumulative, career-stage split, active people). Built on the labels as of
commit 052bf00 (round 2); rerun after any relabeling. Nothing here is
human-checked yet. Part 2 (classified comparison): analysis/classified_comparison.md.

## Summary

- About 3,240 distinct people have at least one included cryptanalysis item
  (any class); 351 have five or more. Identities come from DBLP person records
  (73% of authorships), unique-name matches (16%), or unresolved strings (11%).
- People-equivalents per year (research-FTE): each person counts as the share
  of their total output (DBLP plus zbMATH, deduplicated) in the class, so two
  half-time people count as one and someone who stops publishing on it drops
  to zero. 2024-26: lattices ~82-91, factoring/FF-DLP ~39-43, syndrome
  decoding ~30-35, ECDLP ~22-25, multivariate ~17-24, isogenies ~10-12.
- Calendar person-years (research-FTE x career-stage research fraction) are
  ~0.74x research-FTE in every class: about 20% of the effort comes from PhD
  students, 25-30% from people within five years of their PhD, ~40% from
  established researchers, the rest from people of unknown stage. 2022-26:
  lattices ~61 person-years/yr, factoring ~30, codes ~22, ECDLP ~16,
  multivariate ~11, isogenies ~8; all six classes ~148.
- Cumulative to 2026 (research-FTE-years / calendar person-years): factoring
  ~1,110 / ~850, lattices ~1,035 / ~760 (MLWE ~585, plain LWE ~455), ECDLP
  ~595 / ~440, codes ~330 / ~250, multivariate ~210 / ~150, isogenies ~115 /
  ~85. Lattices passed ECDLP in 2019 and, at current rates, pass factoring in
  about two years.
- Ratios: lattices/ECDLP ~1.7x cumulatively and ~3.8x per year in 2022-26;
  codes/ECDLP ~0.56x cumulatively and ~1.3x per year now. These match the
  paper-count ratios in phase1_report.md.
- Each included item corresponds to ~1.1-1.5 research-FTE-years in every
  class, an independent check on the PLAN section 8 prior (1-2 PY per paper).
- Communities: a small core in each class (top 10% of people hold ~40% of
  credit; most people have one item); lattice and ECDLP people barely overlap
  (10-14%); ECDLP's neighbor is factoring (42%); the lattice coauthor graph is
  one large component, while ECDLP, factoring and codes are fragmented.
- Robustness: adding zbMATH output lowers totals 2-4% (most for factoring and
  ECDLP), so the 1 pub/yr output floor had already absorbed most of DBLP's
  undercount of mathematicians. Shifting estimated PhD years by +-2 moves
  calendar person-years +-4%. The output floor matters more for absolute size
  (0.5 -> 2.0 pubs/yr moves ECDLP from ~700 to ~450 research-FTE-years) but
  barely moves class ratios. The research fractions (0.45 for established
  academics) are conventional values and the largest remaining lever.
- Not human-checked. Fastest check: the per-class top-25 lists in
  author_map.txt.

## Coverage

- 7,613 person-item authorships on included items (yes, effort categories).
  73% resolve through a matched DBLP record, 16% by unique name match to a
  DBLP person, 11% stay unresolved name strings (almost all on OpenAlex or
  zbMATH-only items, plus ~86 names in Japanese, Korean or Cyrillic script).
- 3,240 distinct people have at least one included item; 2,573 have DBLP or
  zbMATH career data. Tiers: 2,046 with one item, 843 with 2-4, 351 with 5+.
- Career evidence (analysis/career_stage.txt): PhD year from Math Genealogy
  for 305 people, ORCID for 289, estimated for the other ~2,645 (first paper
  + 2 years; measured offset median 2, quartiles 0-4, n=564). ORCID
  employment gives a sector for 921 people (743 academic, 178 not). zbMATH
  profiles matched 685 of the 2,009 people queried (52 by DBLP id, 20 by
  ORCID, 613 by title).

## Headline per class

| Class | People (all) | People (vetted) | 5+ items in class | Research-FTE-years | Calendar person-years | Research-FTE/yr, 2022-26 | Person-years/yr, 2022-26 | Active people, 2024-26 |
|---|---|---|---|---|---|---|---|---|
| ECDLP | 752 | 474 | 54 | ~595 | ~440 | 22 | 16 | 144 |
| Lattices (any) | 1,013 | 769 | 120 | ~1,035 | ~760 | 83 | 61 | 405 |
|   MLWE/structured | 939 | 708 | 100 | ~585 | ~425 | 47 | 34 | 362 |
|   plain LWE | 838 | 636 | 97 | ~455 | ~330 | 36 | 27 | 345 |
| Syndrome decoding | 456 | 348 | 36 | ~330 | ~250 | 29 | 22 | 194 |
| Factoring/FF-DLP | 1,285 | 618 | 82 | ~1,110 | ~850 | 40 | 30 | 216 |
| Isogeny | 159 | 143 | 10 | ~115 | ~85 | 12 | 8 | 63 |
| Multivariate | 214 | 181 | 23 | ~210 | ~150 | 16 | 11 | 74 |

## People-equivalents per year

data/authors/fte_by_year.csv has, for every year 1970-2026 and every class,
research-FTE ("people-equivalents"): each person counts as the share of their
total DBLP output (+-2-year window) that falls in the class, so two people
each spending half their output on a class count as one, and a person who
stops publishing on it drops to zero. People without DBLP records enter via
the per-paper prior, spread over the same window. The full yearly table is in
analysis/author_map.txt.

Right edge (checked 2026-10-09): the input is not thin in recent years (2026
has the most included items of any year, 197). An earlier version dropped
sharply in 2025-26 because of two method artifacts, now fixed: (1) the output
floor assumed a full 5-year window even where only 3-4 years exist; (2) people
whose last DBLP paper was 2025 were treated as having stopped in 2026. The
floor now counts only available years, and anyone active in NOW-1 is carried
to NOW (`--censor=1`, default). 2026 remains noisier (part year, one-sided
window).

## What the map says that paper counts did not

1. The work is done by a small core. In every class the top 10% of people
   hold 35-44% of author-fractional credit, and 50% of credit sits with ~117
   people for ECDLP, ~137 for lattices, ~72 for codes, 28 for isogenies.
   Between 54% (multivariate) and 74% (factoring) of people in a class have exactly one item in it.
2. Research-FTE per item is about 1.1-1.5 FTE-years in every class, close to
   the PLAN section 8 prior of 1-2 person-years per paper. The two estimates
   are independent, which supports using either.
3. Current intensity differs more than cumulative effort. Cumulatively
   lattices have ~1.7x ECDLP's research-FTE-years and codes ~0.56x. In
   2022-26, lattices run at ~3.8x ECDLP's annual FTE and codes ~1.3x; ECDLP
   peaked in 2011-16 (~26 FTE/yr) and is now ~22.
4. Communities barely overlap. Only 10-14% of lattice people have any ECDLP
   item and vice versa; 23% of code people touch lattices and 9% touch ECDLP. ECDLP's real neighbor
   is factoring/FF-DLP (42% of ECDLP people also touch it; 97 people are
   regulars in both). MLWE and plain-LWE people are essentially one
   community (82-91% overlap), so "all lattices" is the right unit for people.
5. Network shape differs. The lattice coauthor graph has one giant
   component (54% of people); ECDLP (18%), factoring (28%) and codes (29%)
   are fragmented into many small groups. That fits a lattice field organized
   around NIST-era collaborations, and older ECDLP/factoring fields made of
   separate national or institutional groups.
6. Vetting changes people counts far more for factoring (1,285 -> 618) and
   ECDLP (752 -> 474) than for lattices (1,013 -> 769): the low-quality long
   tail is mostly one-paper authors in those two classes.

## Caveats

- Output share is not time share; record computations (E) and theses are
  undercounted per paper.
- Name-only resolution (16%) can merge two people with the same full name
  when DBLP has only one of them; unresolved strings (11%) can split one
  person into several. Non-Latin-script names (~86) are not mapped to their
  Latin forms.
- Most PhD years are estimated; research fractions by career stage are
  conventional values, not measurements.
- Non-publishing staff (engineers, students before their first paper) are
  invisible.

## Next steps

1. Human spot-check of the top-25 lists per class in author_map.txt (user).
2. Map non-Latin-script names (Japanese ECDLP/Weil-descent authors, Korean,
   Ukrainian) to their DBLP identities.
3. If the research fractions matter for a conclusion, replace the priors with
   a small survey or with time-use studies of academic staff.
