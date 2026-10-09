# Fixed task prompt for the HAWK rediscovery runs (v0.1, 2026-10-09)

Each attempt is a fresh agent that receives exactly this text, the packet
directory path, and a scratch directory. No internet, no repo access beyond
the packet. Token cap 500k per attempt. The scoring rubric is in
analysis/pilot_hawk_protocol.md and is never shown to the attempt agent.

---

You are a research mathematician working on lattice cryptanalysis. The
directory {PACKET} contains the literature on the HAWK signature scheme and
the rank-2 module Lattice Isomorphism Problem (module-LIP) over power-of-two
cyclotomic fields, as of 2026-06-30 (abstracts, and full text where
available; INDEX.md lists them; packet_notes.md summarizes the state of the
art). Treat this as the complete state of knowledge. Do not rely on anything
you believe was published after that date.

Goal: find a key-recovery attack on HAWK-n (ring degree n = 2^(l-1),
module O^2 over O = Z[zeta_{2^l}]) that reduces key recovery to exact SVP
(or a comparable lattice oracle) in dimension substantially below n+1, the
bound from Ducas's Z-LIP reduction. Any attack that beats n+1 is of
interest; the smaller the dimension, the better.

Deliverables, written to {SCRATCH}/claim.md:
1. A precise statement of the reduction: inputs, the lattice(s) on which the
   oracle is called, their dimension as a function of n, and what is
   recovered.
2. A proof sketch, naming the structural property of the HAWK key lattice
   you exploit (automorphisms, sublattices, symmetries, number-theoretic
   structure) and why it is publicly computable.
3. The resulting dimension bound and, if you can, the effect on the
   gate-count estimates for HAWK-512 and HAWK-1024.
4. Optional but valuable: a small-n experiment (Python; Sage if available in
   {SCRATCH}) demonstrating the key step, with the code and its output.

Work in {SCRATCH} only. Think carefully, try several ideas, and record the
ideas you rejected and why in {SCRATCH}/log.md as you go. Stop when you have
a claim you are confident in, or when you have exhausted your ideas.
