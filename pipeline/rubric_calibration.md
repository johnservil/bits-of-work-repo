# Calibration rubric (v0.1, 2026-10-09): effort toward a named open problem

Purpose: label papers from a citation snowball around one named mathematical
problem P, so that the same weighted-count method used for the cryptanalysis
classes (pipeline/rubric.md, PLAN.md §8) yields a person-year estimate for the
human effort spent attacking P before an AI system claimed a solution.
You see title, authors, year, venue and abstract. Judge what the paper DOES.

The batch header names the problem P. Problems in this run:
- UGC: the Unique Games Conjecture (Khot 2002), incl. 2-to-2 Games line,
  small-set expansion, subexponential and SoS algorithms for unique games.
- 2to1: the 2-to-1 Games Conjecture, with or without perfect completeness.
- HAWK_moduleLIP: key recovery for HAWK / rank-2 module-LIP, incl. attacks on
  the Lattice Isomorphism Problem (LIP), Z^n-LIP, nrdPIP reductions, and
  automorphism-based dimension reduction.
- erdos-<N>: Erdős problem number N as stated on erdosproblems.com (the
  statement is given in the batch header).

## include (one)

- `yes`: the paper's main contribution is work ON P: a proof or disproof of
  P or of a special case, a partial result, a new algorithm for the problem
  underlying P, a reduction to or from P, a counterexample attempt, a
  barrier/impossibility result for approaches to P, a computational search
  or record on P, or a survey/thesis centred on attacks on P.
- `no`: the paper only ASSUMES P (e.g. UGC-hardness of some other problem),
  only cites P as motivation, constructs schemes on top of the problem
  (HAWK-based signatures, protocols), is about implementation or side
  channels, or is about a different Erdős problem.
- `borderline`: progress on a closely related problem that the community
  treats as an approach to P (e.g. small-set expansion for UGC; Z^n-LIP
  algorithms for HAWK; a weaker variant of the Erdős statement), or unclear
  from the abstract.

## category (one)

- A  algorithm or construction that makes progress on P (new algorithm,
     improved bound, special case solved).
- C  structural result used to attack P (e.g. automorphism of the key
     lattice, expansion of Grassmann graphs, pseudorandom-set structure).
- D  concrete cost or hardness estimate (bit-security of HAWK, concrete
     parameters).
- E  computational result on an instance (record, exhaustive search,
     counterexample found by computer).
- F  negative/barrier result: lower bounds, limits of a method, "this
     approach cannot work".
- G  reduction or equivalence between P and other problems, hardness
     theory, no direct progress.
- H  claimed result on P later withdrawn or refuted.
- S  survey or thesis centred on P.
- X  include = no.

## weight (0-1)

How much of the paper is about P. 1.0 = entirely; 0.5 = P is one of two
main topics; 0.2 = P is one section or an application. Papers with
include=no get weight 0.

## other fields

- `solves`: true only if the paper claims to resolve P itself (not a
  special case). Default false.
- `ai_assisted`: true if the abstract states that AI/LLM tools were used
  for the result (2026 papers). Default false.
- `confidence`: 0-1.
- `reason`: one clause.

## output

One JSON object per item, one line, no other text:
{"id": "...", "include": "yes|no|borderline", "category": "A|C|D|E|F|G|H|S|X",
 "weight": 0.0-1.0, "solves": false, "ai_assisted": false,
 "confidence": 0.0-1.0, "reason": "..."}

## calibration examples

- "Pseudorandom sets in Grassmann graph have near-perfect expansion" (Khot,
  Minzer, Safra 2018), P = UGC: yes, C, weight 1.0 (the key structural
  result of the 2-to-2 Games line).
- "Optimal inapproximability results for MAX-CUT and other 2-variable CSPs"
  (Khot, Kindler, Mossel, O'Donnell), P = UGC: no, X (assumes UGC).
- "Subexponential algorithms for unique games and related problems" (Arora,
  Barak, Steurer), P = UGC: yes, A, weight 1.0.
- "HAWK: Having Automorphisms Weakens Key" (van Gent, Pulles), P =
  HAWK_moduleLIP: yes, C, weight 1.0.
- "Hawk: Module LIP makes Lattice Signatures Fast, Compact and Simple",
  P = HAWK_moduleLIP: borderline, D, weight 0.3 (design paper; its security
  analysis section is the only attack content).
- "Post-Quantum Anonymous Signatures from the Lattice Isomorphism Group
  Action", P = HAWK_moduleLIP: no, X.
