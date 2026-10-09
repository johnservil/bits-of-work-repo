# Part 2: classified versus public cryptanalytic effort (first pass)

Numbers: analysis/classified_scenarios.txt (regenerate with
`python3 -I analysis/classified_scenarios.py > analysis/classified_scenarios.txt`).
Parameters and their sources: analysis/classified_scenarios.json. Evidence log
with URLs and reliability tags: notes/classified_headcount_evidence.md.

## What can and cannot be known

No intelligence agency has published a mathematician or cryptanalyst
headcount, and nothing public splits classified effort by assumption class.
The commonly quoted "NSA employs ~1,000 mathematicians" has no traceable
primary source; "~600" comes from an anonymous 1999 account. What exists:

- Leaked budget (FY2013 Congressional Budget Justification, verified in the
  document text): "Cryptologic Math & IDA Research" $146M / $129M / $119M
  (FY2011-13); Cryptanalysis & Exploitation Services ~$1.0B (FY2013, mostly
  hardware, IT and exploitation); one project ("Analysis of Target Systems",
  which includes public-key systems) with 240 civilian FTE on $39M (FY2011);
  Consolidated Cryptologic Program 34,901 personnel, 21,575 of them NSA.
- Flows and organization: NSA hires ~30-50 mathematicians a year (NSA ~2003;
  AMS 2013); the Research Directorate's math department is 100-200 people
  (journalist, 2022); IDA's two Communications Research centers have >70 PhD
  mathematicians and computer scientists (IDA, undated), on an NSA contract of
  ~$71M a year (GAO).
- UK: Heilbronn Institute, >30 fellows and >45 members each half-time on
  GCHQ-directed research (~20-25 FTE); GCHQ ~7,100 staff.
- Lead-time anecdotes: differential cryptanalysis (~16-18 years ahead), public-
  key encryption at GCHQ (~3-4 years), the Soliloquy structured-lattice attack
  at CESG (2010-13, ~2-5 years before comparable public work). These are
  declassified cases, so they are a biased sample.

## Model

Classified public-key cryptanalysis effort, in full-time staff, is

    (Five Eyes mathematical cryptology research staff) x (share on public-key
    assumption cryptanalysis) x (allocation across classes).

Staff is built bottom-up from four components (NSA in-house research, IDA
C&C, UK, other Five Eyes) with low / mid / high values; the leaked budget line
gives an independent cross-check (~300-490 FTE for NSA math research plus IDA
at $300-400k loaded cost per FTE, which sits inside the bottom-up range). The
public-key share (10% / 20% / 35%) is the least constrained input: NSA's
mathematics postings list cryptanalysis as one of about eight areas, and
public-key assumption work competes with symmetric cryptanalysis,
implementation and protocol work, signals and data science, quantum
computing, and design and assurance of the agencies' own systems.

Three allocation scenarios split the classified public-key effort across
classes: "operational" (effort follows deployed targets: RSA, DH, ECC),
"transition" (effort follows the agencies' own migration to ML-KEM/ML-DSA
under CNSA 2.0), and "mirror public" (same mix as the public literature).

Public effort is the author-map calendar person-years (research-FTE times the
career-stage research fraction), averaged over 2022-26. Classified staff are
counted as full-time, so the two sides are in the same unit.

Out of scope: non-Five-Eyes states (China, Russia, France, Israel and others
have SIGINT workforces of thousands, but no cryptanalyst counts exist), and
exploitation work that does not touch the underlying assumption.

## Results (2022-26; analysis/classified_scenarios.txt)

Public effort on the six classes is ~200 research-FTE per year, or ~148
calendar person-years: lattices ~61, factoring/FF-DLP ~30, codes ~22, ECDLP
~16, multivariate ~11, isogenies ~8.

Classified side:

| | Low | Mid | High |
|---|---|---|---|
| Five Eyes mathematical cryptology research staff | 260 | 630 | 1,380 |
| Share on public-key assumption cryptanalysis | 10% | 20% | 35% |
| Classified public-key cryptanalysis (FTE) | ~26 | ~126 | ~483 |
| Ratio to public (~148 person-years/yr) | 0.18x | 0.85x | 3.3x |

The budget line alone (~300-490 FTE for NSA mathematical research plus IDA,
FY2011-13) lands between the low and mid staff totals before the UK and the
other partners are added, so the mid value is not generous.

Per class (mid headcount and share; ratio = classified / public):

| Class | Public person-yrs/yr | Operational | Transition | Mirror public |
|---|---|---|---|---|
| ECDLP | 16 | 2.8x | 1.6x | 0.9x |
| Lattices | 61 | 0.3x | 1.0x | 0.9x |
| Syndrome decoding | 22 | 0.3x | 0.5x | 0.9x |
| Factoring / FF-DLP | 30 | 1.7x | 0.6x | 0.9x |
| Isogeny | 8 | 0.3x | 0.5x | 0.9x |
| Multivariate | 11 | 0.3x | 0.4x | 0.9x |

Low-to-high ranges are a factor of ~18 wide around each cell (for example,
ECDLP under the operational scenario: 0.6x to 10.6x).

## Reading

1. Today's classified Five Eyes effort on public-key assumptions is plausibly
   the same order of magnitude as public effort: between about a fifth and
   about three times as large, centrally about equal. It is not plausibly 10x
   or 100x larger in staff terms, unless the public-key share or the staff
   totals are far above anything the evidence suggests.
2. Where classified effort goes matters more than how large it is. If the
   agencies chase deployed targets, classified ECDLP and factoring effort
   exceeds public effort (2.8x and 1.7x at mid values, up to ~10x and ~6x at
   high values), and combined scrutiny of ECDLP is ~4x the public figure. If they concentrate on
   assuring their own ML-KEM/ML-DSA transition, classified lattice effort is
   about equal to public, and combined lattice scrutiny doubles.
3. The asymmetry noted in PLAN section 8 survives: classified effort is most
   likely to be large where public effort is smallest (ECDLP, ~16
   person-years/yr) and is least likely to change the picture for lattices,
   where public effort is already large. At mid values lattices keep the
   largest combined scrutiny per year in the transition and mirror scenarios
   and tie factoring in the operational one (~80 person-years/yr each); at
   high operational values factoring pulls well ahead.
4. Cumulatively, the classified ECDLP/factoring history is longer (decades of
   operational incentive since the 1970s-80s) while classified lattice work is
   documented only from 2007 (Soliloquy). A cumulative comparison would widen
   the classical-vs-lattice gap on the classified side; this model does not
   attempt it because there is no staffing time series.
5. Quality is not headcount. Agency staff are selected, full-time, and work
   with compute budgets (Cryptanalytic IT Systems ~$247M in FY2013) and
   classified context. The lead-time anecdotes (DES ~16-18 years, public key
   ~3-4, Soliloquy ~2-5) suggest per-person productivity may be higher, but
   they are a selected sample.

## Caveats

- Every classified input is a judgement range built on journalist estimates,
  a 2003-era hiring figure, a 2011-13 leaked budget and undated institutional
  pages. Treat the result as an order-of-magnitude bracket.
- Non-Five-Eyes effort (China, Russia, France, Israel, others) is excluded
  for lack of any cryptanalyst count; it could plausibly match or exceed the
  Five Eyes total, which would raise every ratio.
- The public side counts only work that reached the literature; industry
  red-teams and unpublished academic work are invisible on both sides.

## Next steps

1. Argue the parameters in analysis/classified_scenarios.json (public-key
   share and allocation shares especially) with people who have worked
   inside or alongside these agencies.
2. Retrieve the documents not yet opened (ISC 2023-25 GCHQ annex, ASD 2024-25
   workforce table, the Schatz NAP transcript, Johnson's NSA history volumes).
3. Add a cumulative scenario once a defensible classified staffing time
   series exists.
