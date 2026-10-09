# Seed notes: Unique Games Conjecture and 2-to-1 Games Conjecture

Compiled 2026-10-09. Size estimates are my own rough judgement, not measured.
Identifiers were checked against Crossref, DataCite (arXiv DOIs), arXiv abs pages and the
Theory of Computing site; see seeds_calibration.jsonl.

## A. Unique Games Conjecture (UGC)

- Start: Khot, STOC 2002 (CCC 2002 version), building on Feige-Lovasz (STOC 1992) unique
  two-prover systems. Roughly 2005-2008 is when it became a mainstream program
  (Khot-Vishnoi 2005, Trevisan 2005, Charikar-Makarychev-Makarychev 2006).
- Line 1, algorithms (2005 to ~2013): polynomial SDP/spectral algorithms (Trevisan, Gupta-Talwar,
  CMM, Chlamtac-Makarychev-Makarychev), easy special cases (expanders: AKKSTV 2008, Kolla,
  Makarychev-Makarychev, semi-random), then subexponential algorithms
  (Arora-Barak-Steurer 2010, Barak-Raghavendra-Steurer, Guruswami-Sinop via SoS/Lasserre).
- Line 2, Small-Set Expansion (SSE): Raghavendra-Steurer 2010 reduce UGC to SSE; this drives
  higher-order Cheeger and spectral work (Louis et al., Lee-Oveis Gharan-Trevisan) and SoS
  hypercontractivity (Barak et al. 2012).
- Line 3, integrality gaps and candidate hard instances (Khot-Vishnoi, Raghavendra-Steurer,
  Khot-Saket, Barak et al. short code, Khot-Moshkovitz 2016). Also NP-hardness at weaker
  parameters (O'Donnell-Wright 2012).
- Line 4, the 2-to-2 Games theorem (2016-2018): Khot-Minzer-Safra 2017 (Grassmann graph
  reduction), DKKMS 2018 (non-expanding sets), Khot-Minzer-Safra FOCS 2018 / Annals 2023
  (pseudorandom sets in the Grassmann graph have near-perfect expansion). Parallel SSE
  analogues in shortcode and Johnson graphs (Barak-Kothari-Steurer, KMMS).
- Line 5, recent structural work (2020-2025): HDX and globally hypercontractive graphs
  (Bafna-Barak-Kothari-Schramm, Bafna-Hopkins-Kaufman-Lovett, Bafna-Minzer; Keevash-Lifshitz-
  Long-Minzer global hypercontractivity). Braverman-Khot-Minzer "Rich 2-to-1 Games" is
  equivalent to UGC and gives a reformulation of the open problem.
- Community: algorithmic-attack core of perhaps 50-100 active researchers over 20 years
  (Khot, Steurer, Barak, Raghavendra, Makarychev brothers, Kolla, Minzer, Safra, Kindler,
  Dinur, Kothari, Bafna). The literature that merely uses UGC as an assumption is much larger
  (order 1,000 papers) and is deliberately excluded; papers that attack the conjecture itself
  are on the order of a few hundred.
- Surveys listing the literature:
  - Khot, "On the Unique Games Conjecture (Invited Survey)", CCC 2010: https://doi.org/10.1109/CCC.2010.19
  - Trevisan, "On Khot's Unique Games Conjecture", Bull. AMS 2012: https://doi.org/10.1090/S0273-0979-2011-01361-1
  - Khot, ICM 2010 survey: https://doi.org/10.1142/9789814324359_0163
  - Barak-Steurer, "Sum-of-squares proofs and the quest toward optimal algorithms" (ICM 2014): https://arxiv.org/abs/1404.5236
  - Khot, "On the proof of the 2-to-2 Games Conjecture": https://doi.org/10.4310/CDM.2019.v2019.n1.a2
  - Harsha-Charikar DIMACS tutorial notes: https://arxiv.org/abs/1002.3864
  - Quanta coverage of the 2-to-2 theorem: https://www.quantamagazine.org/computer-scientists-close-in-on-unique-games-conjecture-proof-20180424/
  - Quanta coverage of the October 2026 AI-proof announcement (seen only as a search hit, not read): https://quantamagazine.org/as-ai-closed-in-on-unique-games-proof-researchers-raced-to-beat-the-machines-20261007

## B. 2-to-1 Games Conjecture (and d-to-1 family)

- Start: Khot 2002 (the same CCC/STOC 2002 work that introduced UGC states the d-to-1
  conjectures). Used as a hardness source for vertex cover, coloring and hypergraph coloring
  (Khot-Regev, Dinur-Mossel-Regev, O'Donnell-Wu); those consumer papers are excluded.
- The conjecture has two versions, with perfect completeness (the harder, stronger statement)
  and with imperfect (almost-perfect) completeness. Almost-perfect-completeness hardness is the
  DKKMS result (STOC 2018, ToC 2025); it rests on the Grassmann expansion theorem, which is
  the same machinery as the 2-to-2 theorem.
- Pre-2016 progress was algorithmic or partial: subexponential algorithms for d-to-1 games
  (Steurer 2010; Arora-Barak-Steurer), and NP-hardness of 2-to-1 label cover at some points
  (Austrin-O'Donnell-Wright, Austrin-O'Donnell-Tan 2012).
- The 2016-2018 breakthrough was Khot-Minzer-Safra and DKKMS, then Khot-Minzer-Safra 2018.
  Structural tools that feed it: global hypercontractivity (Keevash-Lifshitz-Long-Minzer),
  hypercontractivity on the symmetric group, invariance for slices, the Bonami lemma for
  linear maps (Ellis-Kindler-Lifshitz 2023), HDX agreement tests (Dinur-Kaufman,
  Bafna-Minzer, Kaufman-Minzer), and the low-rank Grassmann encoding (Golowich FOCS 2023).
- 2026: Fei-Minzer-Wang, arXiv 2610.12378 (listed 2026-10-08), proves the 4-to-1 Games
  Conjecture with perfect completeness, building on DKKMS and Golowich. Its abstract says the
  prior best result was DKKMS's almost-perfect-completeness 2-to-1 hardness. The perfect
  completeness 2-to-1 problem is not claimed there.
- Community: much smaller than UGC, effectively one tightly knit group (Khot, Minzer, Safra,
  Kindler, Dinur, Lifshitz, Braverman and students), a few dozen people, with perhaps 30-60
  directly relevant papers. Most of the 2-to-1 seeds therefore overlap the 2-to-2 / UGC seeds;
  the overlap is deliberate and the records are duplicated under each problem.
- Surveys and lineage sources:
  - Fei-Minzer-Wang 2026, Section 1.1 and reference list: https://arxiv.org/abs/2610.12378
  - DKKMS, Towards a proof of the 2-to-1 games conjecture (Theory of Computing 21(11), 2025): https://theoryofcomputing.org/articles/v021a011
  - Minzer, "On Monotonicity Testing and the 2-to-2 Games Conjecture" (ACM Books 2022): https://doi.org/10.1145/3568031
  - Khot, "On the proof of the 2-to-2 Games Conjecture" (survey): https://doi.org/10.4310/CDM.2019.v2019.n1.a2
  - Khot, ICM 2010 and CCC 2010 surveys (see section A).
