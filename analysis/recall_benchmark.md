# Recall benchmark against seed reference lists

References of each seed paper (OpenAlex referenced_works) checked against our data by normalized title.
harvested = present in any raw pull; pool = keyword-screened candidate; labeled = classified; incl = yes/borderline.

| class | seed | refs | harvested | pool | labeled | incl |
|---|---|---|---|---|---|---|
| ecdlp | Recent progress on the elliptic curve discrete logarithm pro | 107 | 106 | 87 | 87 | 80 |
| ecdlp | Solving a 112-bit prime elliptic curve discrete logarithm pr | 48 | 45 | 23 | 22 | 19 |
| ecdlp | Breaking ECC2K-130 | 23 | 20 | 10 | 10 | 9 |
| lattice | Estimate all the {LWE, NTRU} schemes! | 48 | 48 | 44 | 43 | 36 |
| lattice | Does the dual-sieve attack on learning with errors even work | 27 | 26 | 19 | 19 | 18 |
| lattice | Advanced lattice sieving on GPUs, with tensor cores | 34 | 34 | 28 | 28 | 26 |
| lattice | The general sieve kernel and new records in lattice reductio | 38 | 38 | 37 | 37 | 36 |
| code | A survey on code-based cryptography | 0 | 0 | 0 | 0 | 0 |
| code | Syndrome Decoding Estimator | 25 | 25 | 23 | 23 | 23 |
| code | McEliece needs a break - solving McEliece-1284 and quasi-cyc | 16 | 16 | 14 | 14 | 14 |
| comparator | Comparing the difficulty of factorization and discrete logar | 33 | 33 | 29 | 29 | 27 |
| comparator | An efficient key recovery attack on SIDH | 30 | 30 | 15 | 15 | 7 |

## Per class

| class | refs | harvested | pool | labeled | incl |
|---|---|---|---|---|---|
| ecdlp | 178 | 171 | 120 | 119 | 108 |
| lattice | 147 | 146 | 128 | 127 | 116 |
| code | 41 | 41 | 37 | 37 | 37 |
| comparator | 63 | 63 | 44 | 44 | 34 |

102 references were never labeled; see analysis/recall_unlabeled_refs.tsv for manual review.
