# TODO: deduplicate the effort (research-FTE) estimates

Status: open, assigned 2026-10-10 to the machine that has the DBLP dump.
Do not push or publish without checking with the user (see "Publishing" below).

## Why

On 2026-10-10 the user decided that each piece of work counts once (commit dd1440c):

- a preprint, repository copy, duplicate database record or thesis translation of a
  counted work gets weight 0 (the earliest counted version keeps weight 1);
- a journal paper that certainly extends a conference paper counts 1/3 (assumed new
  material), the conference paper 1;
- groups judged "different", and the one borderline extension (group 55,
  2025/739 + W7210281815), are left at full weight (group 55 confirmed by the user
  2026-10-10: keep both at full weight).

`pipeline/build_version_weights.py` turns the same-work groups in
`data/venues/duplicate_checks.csv` into `data/dedup/version_weights.csv` (92 ids at 0,
9 at 1/3). `analysis/export_combined.py` now multiplies the `w_*` class weights in
`data/export/combined_included.csv` by these weights (new columns `version_weight`,
`version_of`), and `analysis/phase1_counts.py` applies them too. Paper counts fell 3-5%
per class; ratios did not move. See the commit message of dd1440c for the numbers.

**The author map was not rebuilt**, because its raw inputs were missing on the machine
that made the change. So `data/authors/fte_by_year.csv` and everything derived from it
(research-allocation years, the 1x/10x/100x AI budget scenarios, the classified-effort
comparison, the white paper's labor and budget tables, the site's effort charts) still
count duplicate versions.

## What to do

1. Inputs (all gitignored under `data/raw/`):
   - DBLP dump: `data/raw/dblp/dblp.xml.gz` + `dblp.dtd`. A 2026-10-09 dump exists at
     `~/Documents/literature-search/data/raw/dblp/` on the main Mac; copy or symlink it.
   - zbMATH per-person cache `data/raw/enrich/zbmath/` (needed so mathematicians'
     zbMATH output enters the denominator; without it totals come out ~2-4% higher).
     Re-fetch with `pipeline/authors_zbmath.py` (~2-3 h, resumable) if missing.
   - `data/authors/career.csv` is committed. **Do not rerun `analysis/career_stage.py`**
     unless the ORCID, Math Genealogy and Wikidata caches under `data/raw/enrich/` exist:
     it rebuilds career.csv from those caches and would wipe the career data.

2. Rebuild (from the repo root, after `git pull`):

   ```bash
   python3 -I analysis/export_combined.py            # should reproduce the committed export exactly
   python3 -I pipeline/authors_dblp.py match          # ~5 min
   python3 -I pipeline/authors_dblp.py stats          # ~5 min
   python3 -I analysis/author_map.py > analysis/author_map.txt   # person list for zbMATH
   python3 -I pipeline/authors_zbmath.py              # only if the zbMATH cache is missing
   python3 -I analysis/author_map.py > analysis/author_map.txt
   python3 -I analysis/classified_scenarios.py > analysis/classified_scenarios.txt
   ```

3. Isolate the effect of deduplication. Before trusting the new numbers, build the author
   map twice on the same inputs: once with the committed (version-weighted) export and
   once with version weights disabled (temporarily move `data/dedup/version_weights.csv`
   aside and rerun `analysis/export_combined.py`, then restore it and rerun). Compare the
   2026 `*_fte_cumulative` columns. Otherwise changes in the DBLP dump or the zbMATH cache
   get mixed into the dedup effect.

4. Method question to settle (and report to the user). The FTE model computes, per person
   and year, class-weighted cryptanalysis items divided by the person's total DBLP (+zbMATH)
   output. DBLP usually lists both versions of a duplicated work, so the duplicate also
   sits in the denominator. Applying version weights only to the numerator (what the
   export now does) therefore undercounts slightly. Consider also removing merged records
   (weight 0) and two-thirds of each extension from the person's publication counts, and
   report both variants. Expect a small effect either way.

5. Regenerate everything that reads `data/authors/fte_by_year.csv`, then check text:
   - `python3 -I pipeline/build_site_data.py` (site charts and summary table);
   - `python3 -I paper/generate_tables.py` and `make -C paper` (white paper and both PDF copies);
   - update the hand-written class budget table in `analysis/ai_effort_comparison_scoping.md`
     (section 3) and the FTE totals quoted in `docs/methodology.html`
     (`grep -n "593.8\|1,036.4\|331.4\|1,111.1"` finds them);
   - check `SUMMARY.md`, `docs/index.html` and `paper/whitepaper.tex` for quoted
     allocation years or ratios (e.g. "lattices ~1.7x ECDLP") that moved.

## Publishing

The private repo's `main` is what bitsofwork.org serves. After the user approves:

```bash
git push origin main
python3 -I pipeline/export_public.py ~/Dropbox/src2/bits-of-work-repo   # must report 0 matches, 0 broken links
cd ~/Dropbox/src2/bits-of-work-repo && git add -A && git commit -m "Update public export from private <hash>" && git push origin main
```

Then wait for `gh api repos/matthewdgreen/literature-search/pages/builds/latest --jq .status`
to say `built` and spot-check https://bitsofwork.org/.

## Related open items (not part of this task)

- 32 year discrepancies flagged in `data/venues/venue_flags.csv` (counting-year errors);
  they change counts and need a user decision.
