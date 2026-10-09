# Working white paper

Editable source: [whitepaper.tex](whitepaper.tex). Bibliography: [references.bib](references.bib).
Compiled draft: [cryptanalytic-effort-whitepaper.pdf](../output/pdf/cryptanalytic-effort-whitepaper.pdf).

The paper is the project's working synthesis: public cryptanalytic literature,
estimated research-years and person-hours, historical literature effort around
selected mathematical problems, and assumed human-year equivalents of recent
OpenAI/Anthropic AI research budgets. It distinguishes historical human labor,
actual human supervision, and scenario-derived equivalents.

## Build

From the repository root:

```sh
make -C paper
```

Requires Python 3 (standard library only), `latexmk`, and a LaTeX installation
with the packages declared in `whitepaper.tex`. No network, model call, or paid
classification is part of the build. Intermediate files go to
`tmp/pdfs/whitepaper/`; the deliverable goes to `output/pdf/`, with a copy in
`docs/assets/` for the website's PDF link.

The build first regenerates the selected attack-history export.
`generate_tables.py` rebuilds the tables and the cumulative-effort figure data
from existing repository outputs, including the five attack-index rows. `generated/manifest.json` records source
hashes, assumptions, and derived values. Generated `.tex` rows and the figure CSV
are checked-in source companions so the manuscript can also be edited and
compiled without rebuilding the literature pipeline. Regenerate and review prose
when the source data changes. Rounding uses decimal half-up; displayed hours
are calculated before rounding the displayed years.

## Conventions in version 0.2

- Observation date: 2026-10-09; 2026 coverage is incomplete.
- 2,000 hours per research-year is a nominal accounting convention, not observed
  time. The career-adjusted person-time view is shown separately.
- Human cost: $250,000 per research-year. Productivity multipliers: 1x, 10x, 100x.
  Neither those multipliers nor the resulting budgets are confidence bounds.
- Inverse comparison: assumed human-year equivalent = multiplier x AI dollars /
  $250,000. This does not estimate actual human labor by lab employees.
- Token-only valuations use explicitly hypothetical prices; the paper does not
  infer an internal model bill from public output-token counts.
- HAWK normalization remains a separate historical-effort example.
- The attack-history section separates selected asymptotic indices from
  qualitative break events. Its inverses are not security parameter recommendations;
  source records retain assumptions, corrections and date-version uncertainties.
- Mathematical claims are attributed to their sources, not independently verified.

## Before external circulation

Human review should focus on high-impact literature labels, historical cutoffs
and AI involvement in the mathematical-problem samples, the meaning of the
person-hour conventions, the cost boundaries of the AI disclosures, and the
validation status of recent mathematical claims. These are draft-review tasks;
rediscovery experiments remain deferred.

## Draft verification

Version 0.2 compiles to 16 pages, including the selected-attack-methods section
and its primary references. All pages were rendered and visually reviewed.
The final LaTeX log has no undefined references/citations or overfull boxes.
Generated class/year/hour/budget relationships and all bibliography keys were
checked. This validates document construction, not the scientific assumptions or
underlying machine labels.
