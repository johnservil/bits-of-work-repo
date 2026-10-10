# TODO: fix identity splitting and pooling in the author map

Status: open, assigned 2026-10-10 to the machine that has the DBLP dump.
Do not push or publish without checking with the user (see "Publishing" below).
Related: notes/TODO_fte_dedup.md needs the same author-map rebuild. Do both in one
session if you can, but keep their effects separable (see step 6).

## Why

The researcher explorer (docs/people.html, built 2026-10-10) shows individual people,
which exposed two identity errors in the author map (`analysis/author_map.py`, using
`pipeline/authors_dblp.py`). The FTE estimates have the same errors; they are small in
aggregate (about 2% of authorships), but they matter for named individuals.

1. **Split identities.** The author map normalizes names with `full_norm()` in
   `pipeline/authors_dblp.py`. Author strings that differ from a DBLP person only in
   (a) Unicode dashes (U+2010-2014, U+2212: `Jean‐Charles Faugère`, `Jean–Pierre Tillich`,
   `Francisco Rodríguez‐Henríquez`), (b) "Last, First" order (`Lange, Tanja`,
   `Pomerance, Carl`, `Silverman, Robert D.`, `Montgomery, Peter L.`), or (c) a DBLP homonym
   number kept in the string (`Yuntao Wang 0002`) never match, and become separate
   `name:` identities. `full_norm` drops non-ASCII characters after NFKD, so a Unicode
   hyphen disappears instead of becoming a space.
2. **Pooled identities (DBLP disambiguation pages).** When DBLP has split a name into numbered
   people (`Lei Hu 0003`, pid `09/6501-3`), the unnumbered profile (`Lei Hu`, pid `09/6501`)
   is a disambiguation page: papers by anyone with that name that DBLP has not assigned yet.
   The author map treats it as one person. The DBLP dump marks these person records with
   `<note type="disambiguation">`, but the `stats` pass in `authors_dblp.py` reads only
   affiliation notes, so the information is dropped. Very large unnumbered profiles of common
   Chinese names (Li Xu 495 DBLP papers, Yu Li 760, Zheng Wang 723, Li Yang 757) are probably
   the same thing; check what the dump says about them.

Name-only matching (`exact`, `fuzzy_crypto` in `resolve()` in author_map.py) is less of a
problem than it looks: `stats` collects every DBLP person whose normalized name equals an
unmatched author string, numbered homonyms included, so an `exact` match is unique across
DBLP. It can still land on a disambiguation page or an unsplit catch-all profile, which
step 3 handles.

### Interim workaround now in place (replace it)

`pipeline/build_people_data.py` (the explorer's data builder) patches both problems at the
display layer only:

- `merge_split_names()` merges 165 `name:` identities into DBLP persons when dashes, name
  order or a homonym number are the only difference and exactly one DBLP person fits;
- `ambiguous_ids()` withholds 12 identities from being named on the page, by heuristic:
  (a) an unnumbered DBLP profile whose name also appears with a number (Yixin Shen, Lei Hu,
  Xiaoyun Wang, Jun Xu, Yanlin Chen), (b) an unnumbered profile of a common Chinese name with
  more than 400 DBLP publications (Li Xu, Yu Li, Zheng Wang, Li Yang), (c) an unmatched
  Chinese name string (e.g. Yuntao Wang, Chao Wang).

The user reviewed the named researchers on 2026-10-10. Everyone looked plausible except the
possible ambiguities in Chinese names, which is what (2) is about.

## What to do

1. Inputs: as in notes/TODO_fte_dedup.md step 1 (DBLP dump `data/raw/dblp/dblp.xml.gz` +
   `dblp.dtd`, zbMATH cache `data/raw/enrich/zbmath/`; do **not** rerun
   `analysis/career_stage.py` without the ORCID/MGP/Wikidata caches). Do not query the
   dblp.org website or API: as of 2026-10-10 it sits behind a bot check and returns 429. The
   dump has everything needed.

2. Normalization (split identities). In `pipeline/authors_dblp.py`, map Unicode dashes to
   `-` before NFKD in both `full_norm()` and `name_key()`. `name_key()` also takes the last
   token as the surname, so `Lange, Tanja` gets the key `tanja|l`; reorder "Last, First"
   before keying. Both functions call `strip_homonym()`, so `Yuntao Wang 0002` currently
   normalizes to the ambiguous `yuntao wang`. In `resolve()`
   in `analysis/author_map.py`, also try the "Last, First" reordering (one comma, both parts
   non-empty) and a trailing four-digit homonym number. A string with a homonym number names
   a DBLP person exactly: look it up directly. `spelling_variants()` in build_people_data.py
   is a working reference. `authors_dblp.py match` builds the `exact` and `fuzzy_keys` sets
   from these normalized forms, so rerun `match` and `stats` after the change.

3. Disambiguation pages (pooled identities).
   - In the `stats` pass, record `<note type="disambiguation">` on person records
     (e.g. `person[p]["disambiguation"] = True`) and carry it into `authors.csv` as a column.
   - In `author_map.py`, an authorship that resolves to a disambiguation page should not count
     as that "person". Try to reassign it to one numbered homonym (same base name), e.g. the
     only one with co-authors in common with the item's other authors on other DBLP papers,
     or the only one active in crypto venues around that year. Otherwise mark it ambiguous:
     it still counts in class totals and FTE (use the per-paper prior, as for unresolved
     strings), but the person column says it is ambiguous (e.g. `name:ambiguous:<base name>`
     plus a flag), so the explorer never names it.
   - Report how many authorships were reassigned and how many stayed ambiguous, per class.
   - Check the >400-publication unnumbered profiles listed above: are they flagged as
     disambiguation pages in the dump? If not, leave them and report them to the user.

4. Unmatched Chinese name strings. Identity by spelling alone is weak for common Chinese
   names. Keep them in totals, but give `authors.csv` an `ambiguous` flag for unmatched
   strings with a common Chinese surname (the surname list is `SURNAMES` in
   build_people_data.py), so the explorer can keep withholding them.

5. Explorer builder. Once `authors.csv` carries the flags, simplify
   `pipeline/build_people_data.py`: drop `merge_split_names()` (the author map does it now;
   confirm the merge count falls to about zero first) and make `ambiguous_ids()` read the new
   column, keeping the Chinese-string rule only if step 4 did not cover it. Keep the
   per-profile "matched by name only" count (`nm`). Update the caveat in docs/people.html,
   which quotes the rules and uses `data-ambiguous` for the withheld count.

6. Rebuild and isolate effects. Rebuild order as in notes/TODO_fte_dedup.md step 2. If you
   also do the FTE dedup task, build the author map three times on the same inputs: committed
   code without version weights, with version weights, then with this task's identity
   changes, so each effect can be reported on its own. Compare the 2026 `*_fte_cumulative`
   columns of `data/authors/fte_by_year.csv` and the number of distinct people. Expect
   class totals to move by a few percent at most and class ratios hardly at all.

7. Verify against the known cases. After the rebuild, each of these should be one identity
   (or withheld as ambiguous where stated):
   - Jean-Charles Faugère, Jean-Pierre Tillich, Francisco Rodríguez-Henríquez (dash variants);
   - Tanja Lange 0001, Carl Pomerance, Robert D. Silverman, Peter L. Montgomery, Arne
     Winterhof, Antoine Joux, Pierrick Gaudry (reversed-order variants);
   - Yuntao Wang 0002 (string with a homonym number);
   - Yixin Shen / Yixin Shen 0001, Lei Hu / Lei Hu 0003, Xiaoyun Wang / Xiaoyun Wang 0001,
     Jun Xu / Jun Xu 0022, Yanlin Chen / Yanlin Chen 0001: papers on the unnumbered profile
     either reassigned to a numbered person or marked ambiguous, never shown as a named person.
   Then `python3 -I pipeline/build_people_data.py` should print a merge count near 0 and no
   warnings, and the explorer's top-25 lists per field should be unchanged apart from these
   people. Run the explorer locally (`python3 -m http.server -d docs`, open people.html) and
   check a few profiles.

8. Regenerate everything downstream of `data/authors/` as listed in
   notes/TODO_fte_dedup.md step 5, plus `python3 -I pipeline/build_people_data.py`. Update
   `analysis/author_map.md` (Coverage section: resolution shares, distinct people) and the
   people counts quoted on the site (`grep -n "3,240\|7,613" docs/*.html`).

## Publishing

Same as notes/TODO_fte_dedup.md "Publishing": report the before/after numbers to the user and
push only after approval. The private repo's `main` is what bitsofwork.org serves, and the
public mirror is updated with `pipeline/export_public.py`.
