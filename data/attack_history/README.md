# Selected algorithmic bounds and attack events

This track records a sourced, deliberately incomplete history of algorithmic
bounds. It does not estimate the probability of a future break or reconstruct
historical security ratings. Source checking by an agent is not human
verification; no agent sets verified: true.

## Two different kinds of evidence

**Index tracks** evaluate selected leading-term formulas at a reference size,
with lower-order factors omitted. The first view shows that index over time;
the second independently inverts each available formula and takes the largest
size needed to give an index of 128. These are model-equivalent sizes, not
security parameter recommendations. A single algorithm need not win both views.

The reference size does not imply comparable cryptographic security across
tracks. The lattice track is an SVP oracle, not a full ML-KEM attack. The
decoding track maximizes the full-distance exponent over rates separately for
each algorithm, rather than holding a particular code fixed. The MQ track
states its algebraic and randomization assumptions explicitly.

**Event tracks** describe finite-field reassessments and SIDH breaks without
putting unlike estimates on a numerical curve. Polynomial, quasi-polynomial,
and subexponential complexities are distinct. Without a parameterized cost
model, inverse size is *not estimated*, never "no finite size." Concrete times
or security estimates retain the instance, units, source, and qualifications.

## Eligibility, dates and corrections

A numerical milestone must have series: true, status: supported, a classical
model, a supported numerical formula, and a source URL. There is no "practical"
Boolean filter: asymptotic bounds can be informative despite prohibitive memory
or lower-order costs. We do not claim an exhaustive best-known envelope.

The year/date fields date the first public version of the **quoted analysis**,
when established from its source. The optional algorithm_year records an older
algorithm. Corrected claims remain context with series: false; adding a larger
corrected exponent alongside an obsolete smaller exponent cannot repair a
running minimum. A later corrected analysis is not silently backdated. This
is a history of currently supported published analyses, not contemporaneous
beliefs. Conference/preprint distinctions and unresolved dates belong in notes.
Same-year curve points show the lowest selected year-end index; the full ledger
retains intermediate results. No "years stable" or exponent-change count is
calculated.

## Schema

Problem fields: key, label, cls, role, display_kind (index or events), problem,
size_unit, size_name, reference (index tracks), from_year, notes, milestones.

Milestone fields: year, date, name, authors, ref, source_url, model, series,
status (supported, corrected, or context), cost, assumptions, notes, optional
algorithm_year, event, context_formula or complexity_description, and verified: false.
Supplementary URLs, track-level assumptions and dating_note preserve source-version
uncertainty and supporting analyses in the rendered ledger. Sources must
be inspected primary papers, author-hosted versions, or official publications.
Formula coefficients are not confidence scores. Scope exclusions and guarantee
differences must be described in prose.

Supported numerical cost forms (all omit lower-order factors):

| Type | Parameters | Index at size s |
|---|---|---|
| sqrt_group | k | s/2 + log2(k), group order 2^s |
| power | exp | exp × s, N = 2^s |
| linear | c | c × s |
| nlogn | c | c × s × log2(s) |
| L | a, c | c × (s ln2)^a × ln(s ln2)^(1−a) / ln2 |

Non-numerical milestones use cost: null and an event, context_formula or complexity_description.
Their absence from the numerical envelope is not absence of scientific progress.

## Build and audit

Run the following from the repository root:

    python3 -I analysis/attack_stability.py
    python3 -I pipeline/build_site_data.py
    make -C paper
    python3 -B -m unittest discover -s analysis -p 'test_attack_stability.py'

The generator validates provenance and eligibility, and writes the report and
record-level JSON/CSV under data/export/. The paper generator records hashes
of the history inputs and renders its summary from the same export.
