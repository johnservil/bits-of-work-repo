# Rediscovery pilot protocol: HAWK key recovery (v0.1, 2026-10-09)

## Current status: deferred (2026-10-09)

The user adopted the [assumption-based 1x/10x/100x budget comparison](ai_effort_comparison_scoping.md).
Further rediscovery runs are not needed for that comparison. The original
design and run log below are retained for provenance, not as an active work plan.
All six attempts were interrupted; none completed a mathematical evaluation.

If revisited, the design needs verified model/version provenance, exact packet
versions, expert checking of successful claims, and a fixed or explicitly modeled
stopping rule. Cold recall probes can detect contamination but cannot establish
its absence; keep any solution-bearing probes separate from solving contexts.
Anthropic reports disclosure to the HAWK team in June, so July publication dates
alone do not establish discovery timing or independence. The goal prompt measures
directed rediscovery, not an unrestricted search for weaknesses. A verify-or-extend
task would measure a different activity. These qualifications supersede stronger
claims in the original design below.

## Why HAWK

Between 2026-07-30 and 2026-09-30 four ePrint papers reduced HAWK-n key
recovery (rank-2 module-LIP over power-of-two cyclotomics) from exact-SVP in
dimension n+1 (Ducas, DCC 2024) to exact-SVP in smaller dimension:

| ePrint | posted | authors | bound | origin per 2026/2198 |
|---|---|---|---|---|
| 2026/1560 | 2026-07-30 | Mureau, Pellet-Mary | 3n/4+1 | human |
| 2026/1593 | 2026-08-03 | Straznickas, Weis | n/2+1 | "Claude-derived" |
| (unlocated) | summer 2026 | ? | 3n/4+1 | "ChatGPT-derived" |
| 2026/2198 | 2026-09-24 | Luo, Jiang, Pan | rank-4 extension | human, cites the above |

Per 2026/2198 the HAWK team withdrew the scheme. Saarinen (2026/2266) calls
this the field's "Lee Sedol moment". Saarinen's 2026/1377 (refuting the
"Guessing Game" attack 2026/1318) also states that AI tools did the rapid
exploration and implementation. So HAWK is not a synthetic target: it is a
matched human/AI event inside mathematical cryptanalysis, with three
independent solutions within about five weeks of each other.

This gives three measurements instead of one:

1. Human effort before the event: the module-LIP/HAWK cryptanalysis
   literature 2021-2026-06, estimated with the standard pipeline
   (data/ai_effort/seeds_hawk.jsonl, 27 pre-cutoff seeds, rubric
   pipeline/rubric_calibration.md, problem HAWK_moduleLIP), plus the
   direct effort of the three solving groups where stated in their papers.
2. AI effort as disclosed by the original AI-derived papers (2026/1593 and
   the ChatGPT-derived one): model, sessions, tokens, cost, human hours.
   Status: PDFs are behind a Cloudflare challenge; full text not yet read.
3. AI effort under our own full accounting: a controlled rediscovery run
   (below), which prices failed attempts, the thing no public figure does.

## Controlled rediscovery run

Model: a strong model with training cutoff before 2026-07-30 (Fable 5.1,
cutoff June 2026; also one run with Opus 5.5 for a cost comparison).

Contamination check (run first, no packet): ask the model cold (a) what is
the best known reduction of HAWK key recovery to SVP and in what dimension,
(b) whether it knows of an attack using the Galois involution zeta -> -zeta
or a trace-zero sublattice. If it names n/2+1, 3n/4+1, or any of the four
papers, the target is contaminated and the run is void.

Packet: data/ai_effort/pilot_hawk/packet/ (ePrint items posted on or
before 2026-06-30, abstracts plus full text where obtainable, HAWK spec).
Held-out answer key: data/ai_effort/pilot_hawk/heldout/ (never shown).

Task prompt (fixed text, recorded in the run log): "Using only the
attached literature, find a reduction from HAWK-n key recovery to exact
SVP in a lattice of dimension substantially below n+1. Give the reduction
precisely, with a proof sketch, and state the resulting dimension. You may
write and run code (Python, stdlib or sage if available) to test ideas on
small n."

Design: K independent attempts (K = 5 to start), each a fresh agent with a
hard token cap (500k tokens), tools: read packet, python. No internet. Each
attempt ends with a written claim. Total pilot budget 3M tokens; stop
early if two attempts reach score 4 or higher.

Scoring (strong model, blind to attempt order, then human spot-check):
0 nothing beyond the packet;
1 identifies that extra automorphisms of the key lattice would reduce the
  problem (already in van Gent-Pulles 2025/928);
2 proposes a concrete publicly computable automorphism or sublattice
  (Galois involution, trace-zero part, symmetric square);
3 shows the auxiliary object is a public lattice of smaller dimension and
  gives its dimension;
4 full chain: recover the automorphism/sublattice by SVP in the smaller
  lattice, then recover the key (Ducas block reduction + van Gent-Pulles
  descent, or equivalent), with correct dimension 3n/4+1 or n/2+1;
5 as 4 with a verified small-n implementation.

Recorded per attempt: tokens in/out, wall-clock, tool calls, final score,
and the first point at which the key idea appears (token index). Exchange
rate inputs: total tokens over all attempts (including failures) and list
price dollars; human side from measurement 1.

## What is not yet done

- Full text of 2026/1593, 2026/1377, 2026/2266, 2026/1560 (Cloudflare
  blocks automated PDF download; arXiv API rate-limited this IP). The
  ePrint HTML abstract pages do load.
- Identity of the "ChatGPT-derived" 3n/4+1 paper.
- Direct effort statements from the human authors (ask them; optional).

## Contamination check result (2026-10-09)

Run with a fresh Fable 5.1 agent, no tools, no context. Answers: best known
attack = generic 2n-dimensional lattice reduction plus the Chevignard et al.
Eurocrypt'25 nrdPIP reduction (no concrete speedup); UNKNOWN for any
Galois-involution or trace-zero reduction to n/2+1 or 3n/4+1; believes HAWK
not withdrawn (knowledge "as of ~late 2025"); UNKNOWN for any AI-produced
HAWK result; latest recalled items are the Eurocrypt 2025 papers. It did not
recall Ducas's n+1 Z-LIP bound (ePrint 2023/447) or van Gent-Pulles 2025/928
either, so the packet supplies those. Original verdict was "target not
contaminated"; corrected interpretation: no contamination detected by this
probe, with the model's actual training exposure unverified.

## Run log (2026-10-09)

- Attempt 1 (Fable 5.1): terminated by the model's safeguards before any
  work was done ("Fable 5.1's safeguards flagged this message", reasoning
  extraction). Not retried with rephrasing; recorded as a model-availability
  limit, not as a failed attempt. The error text suggests changing model.
- Attempt 3 (Fable 5.1): same safeguard termination at the first step.
  Decision: run the pilot on Opus 5.5 only (attempts 4-6). The Fable
  contamination check remains valid as a knowledge probe; Opus's own
  cutoff is assumed at or before Fable's (not separately probed).
- Attempt 6 (Opus 5.5): stopped by a safety classifier partway through its
  first response, before any analysis; no files written. Attempts 2, 4, 5
  were left to finish or stop on their own; none was re-prompted.
- Decision (2026-10-09): measurement 3 (controlled rediscovery with full
  accounting of failed attempts) is BLOCKED in this environment by model
  safeguards on autonomous cryptanalysis of a (withdrawn) NIST candidate.
  No rewording or retry was attempted. Whether and how to proceed is a
  human decision; options are (a) a human-in-the-loop version where the
  model is asked to verify or extend a stated reduction rather than to
  find an attack, (b) a different, non-cryptographic rediscovery target
  (e.g. an Erdős problem from the Epoch set, where the same accounting
  applies), or (c) drop measurement 3 and rely on the disclosed figures.
  This is itself a data point for the study: the AI-side effort that is
  observable publicly comes from labs running their own models without
  these product safeguards.
- Attempt 4 (Opus 5.5): read the key packet papers (2025/928, 2023/447,
  2024/601, spec §5.1-5.3), then was stopped by a safety classifier before
  writing anything. No claim; no files.
- Attempt 5 (Opus 5.5): stopped by a safety classifier while reading
  2025/928; no claim, no files. Counted as interrupted, not as evidence.
- Attempt 2 (Fable 5.1): read the packet index and notes, then was
  terminated by the model's safeguards while opening 2025/928. No claim,
  no files. All six attempts are now accounted for: 0 analyses completed.
