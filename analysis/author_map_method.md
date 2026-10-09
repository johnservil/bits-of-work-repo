# Author map: method

Goal: a person-level map of public cryptanalysis of the study's assumption
classes, so effort can be expressed in people and research-FTE-years rather
than paper counts, and so the size and overlap of the communities working on
each class can be measured. Part 2 (later) compares this with what is known
about classified headcount.

Interpretation (website review, 2026-10-09): these are publication-based
research-allocation estimates, not measured FTE or working hours. Publication
share can substantially overestimate time share when researchers have other
duties, contribute unequally to papers, or complete projects quickly. The
publication-rate floor reduces sparse-record inflation but cannot validate
the time interpretation. The career-stage alternative lowers the main totals
by roughly a quarter under assumed research fractions; it is a sensitivity
case, not an empirically established correction. Budget scenarios inherit
any overestimate proportionally. The baseline series is retained with these
qualifications, rather than silently replacing it with another unvalidated
estimate.

## Inputs

- Labeled items: data/export/combined_included.csv (yes + borderline, all
  rounds, manual exclusions applied). Headline uses include = yes and effort
  categories A-F, H (same as analysis/phase1_counts.py).
- DBLP dump (data/raw/dblp/dblp.xml.gz), read twice by pipeline/authors_dblp.py.

## Identity resolution (pipeline/authors_dblp.py)

1. `match`: each item is linked to DBLP records by DBLP key, ePrint id (the
   `ee` link on DBLP's ePrint entries), DOI, then normalized title with year
   +-1. The DBLP person-record alias map (secondary name -> primary name) is
   collected in the same pass.
2. Record choice: the record whose author list best overlaps the item's own
   list (surname + first initial), then by match method, then peer-reviewed
   over informal. DBLP's ePrint entries sometimes keep a first-version author
   list, so overlap goes first. Item authors missing from the chosen record
   are resolved individually.
3. Persons are DBLP primary names (homonym-numbered, e.g. "Paul Zimmermann
   0001"), with aliases merged.
4. Authors of items DBLP lacks (mostly OpenAlex/zbMATH-only, the unvetted
   part of the corpus): exact full-name match to a unique DBLP person; else
   surname + initial to a unique person already in the cryptanalysis set;
   else kept as an unresolved string identity `name:<normalized>`.

## Career data (pipeline/authors_dblp.py `stats`)

For every resolved person: all DBLP publications, deduplicated by normalized
title (so an ePrint/CoRR copy and its published version count once), with
first year, whether only an informal version exists, and whether the venue is
a cryptography venue. Plus the DBLP person record: affiliation notes, ORCID,
Math Genealogy id (PhD year source for later).

## Measures (analysis/author_map.py)

Per person and class: touch (items touching the class), fractional items
(sum of class weights), author-fractional credit (class weight / number of
authors), first/last item year, tier (core >= 5 included items, regular 2-4,
occasional 1), DBLP career (pubs, span, crypto-venue share), and
cryptanalysis share (included items / distinct DBLP pubs).

Research-FTE model: for person p, class c, year y,

    share_c(y) = (class-c weight of p's included items in [y-2, y+2])
                 / max(p's distinct DBLP pubs in [y-2, y+2], the included-item total)

The floor (default 1 pub/year, `--rate`) is applied per window year the
person could have published in (from first DBLP year to NOW). A person counts
until their last DBLP year; anyone whose last year is NOW-1 or later is carried
to NOW (`--censor`, default 1) to offset indexing lag.

Summed over persons this is "research-FTE in class c in year y": the number of
full-time-research-equivalent people whose output that year was class-c
cryptanalysis. Summed over years it gives research-FTE-years. Persons with no
DBLP record get the PLAN section 8 per-paper prior (A/B/C/F 1.5 PY, D 1.0, E
6.0, H 0.75 per paper, split over authors) instead; reported separately.

Converting to calendar person-time: research-FTE assumes the person spends all
working time on research. Faculty typically spend 30-50% on research, PhD
students and postdocs 70-100%, industry researchers vary. A single blended
factor of ~0.6 is a reasonable starting point; the person table keeps the
DBLP career fields so the factor can later be set per career stage.

Known biases:
- Output share is not time share: record computations (E) and long
  negative-result projects take more time per paper; prolific authors with
  many short papers get a smaller share per paper.
- DBLP undercounts math-venue output (number theory, coding theory journals),
  which inflates the share for mathematicians; zbMATH author profiles would
  fix this for the math side.
- Unresolved string identities split one person into several when name forms
  differ, and the per-paper prior is used for them.
- Students before their first DBLP paper and engineers who never publish are
  invisible.

Networks: coauthor edges from included items, per class. Reported: connected
components, largest-component share, label-propagation communities of >= 3
("groups"), concentration of credit, and cross-class overlap of person sets.

## zbMATH output counts (pipeline/authors_zbmath.py)

DBLP covers computer-science venues well but misses much of the mathematics
literature, so mathematicians' output shares came out too high (the 1 pub/yr
floor was a crude patch). For people with no DBLP career data or fewer than
1.5 DBLP papers per career year (the group where this matters), the zbMATH
Open author search is queried by name. A zbMATH author is accepted only if
its external ids include the person's DBLP pid or ORCID, or (for at most three
name-compatible candidates) it shares at least one normalized title with the
person's known work. All of the accepted author's zbMATH documents are
fetched and merged with DBLP on the normalized-title hash, so a paper in both
counts once. People without DBLP data whose zbMATH profile matches move from
the per-paper prior to the output-share model. `--no-zbmath` reproduces the
DBLP-only numbers.

## Career stage and calendar person-years (pipeline/authors_enrich.py, analysis/career_stage.py)

Research-FTE says what share of a person's output went to a class; it does
not say how much of their working time was research. To convert it to
calendar person-years, each person-year gets a career stage and a research
fraction.

PhD year, in order of preference:
1. Math Genealogy Project (ids from DBLP person records, Wikidata P549, or
   zbMATH author profiles; fetched at the site's 10 s crawl delay).
2. ORCID education/qualification entries with a doctoral role title (ORCID
   ids from DBLP, Wikidata P496, or zbMATH).
3. Estimate: first publication year (DBLP or zbMATH) plus the median offset
   measured on people with a known PhD year.

Stage in year y: student before the PhD year; early career for the 5 years
after it; established afterwards. Sector (academic / non-academic) comes from
the ORCID employment entry covering y (organization-name heuristic), unknown
otherwise. Research fractions (priors, editable in analysis/author_map.py):
student 0.9, early career 0.85, established academic 0.45, established
non-academic 0.7, established unknown 0.5. Calendar person-years =
research-FTE x research fraction. People on the per-paper prior keep the prior
(already in person-years) and are reported as "unknown stage".

Caveats: ORCID and MGP cover a minority of people, so most PhD years are
estimates (first paper is often 1-2 years before the PhD for CS students and
after it for mathematicians); the fractions are conventional values, not
measurements; non-publishing staff remain invisible.
