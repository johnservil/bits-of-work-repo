# Claimed polynomial-time quantum attack on ML-KEM (set aside for separate review)

Surfaced 2026-10-09 during Phase 1 classification. By the user's decision these
items are EXCLUDED from all study counts (data/manual_exclusions.json) and are
listed here for the user's separate reading.

Series: Ming-Xing Luo, "Module Lattice Security" (arXiv, 2026, single author, CoRR-only).

| Part | arXiv | Title | Classifier labels |
|---|---|---|---|
| I | not found in DBLP/OpenAlex harvest | (referenced by Part IV) | n/a |
| II | 2604.22900 (https://arxiv.org/abs/2604.22900) | Module Lattice Reduction via Optimal Sign Selection | pass 1 borderline; pass 2 yes/B ("extends CDPR quantum ideal-SVP attack to module lattices") |
| III | 2605.17404 (https://arxiv.org/abs/2605.17404) | Structured CVP Distance on the Log-Unit Lattice | pass 1 borderline; pass 2 yes/C (title only, no abstract) |
| IV | 2605.17412 (https://arxiv.org/abs/2605.17412) | Probabilistic Polynomial Quantum Attack on Module-LWE over 2-Power Cyclotomics | pass 1 no/X "unvetted claim"; not in pass 2 sample |

Claim as stated in the Part IV abstract (paraphrased): combining Parts I-III with
a tower decomposition of the Principal Ideal Problem along the 2-power cyclotomic
tower, the resulting approximation factor is at most 21, below q/2 for
ML-KEM-1024, with success probability at least 0.99.

Context for the reader: this would go far beyond the known CDPR /
Cramer-Ducas-Wesolowski line (which gives subexponential approximation factors
for ideal lattices and does not reach module-LWE parameters). Nothing found in the
harvest responds to it yet.

Other 2025-2026 "post-quantum break" items in the data were already excluded as
unvetted claims (e.g. W7130414132, W7163743137; Zenodo/low-tier outlets).
