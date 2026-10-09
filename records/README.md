# Computational records (PLAN.md §7)

One file per record: `records/<class>/<slug>.yaml`, where class is one of
`ecdlp`, `lattice`, `code`, `comparator`. Each file is flat YAML where every
value is written as a JSON literal (strings double-quoted, lists as `[...]`,
`null` for unknown), one `key: value` per line, so the stdlib can parse it
(`json.loads` on each value). Comment lines start with `#`.

Every record is `verified: false` until a human has checked it against the
source. Agents must never set `verified: true` on their own; it is set only on
the user's explicit statement, with a `verified_by` line saying who and when.

## Fields

| key | meaning |
|---|---|
| id | slug, same as filename stem |
| class | ecdlp / lattice / code / comparator |
| problem | ECDLP, interval-ECDLP, SVP, approx-SVP, LWE, NTRU, Ideal-SVP, SD, SD-Goppa, SD-QC, LPN, factoring, FF-DLP, isogeny, multivariate |
| instance | short description (e.g. "secp112r1", "SVP challenge dim 186", "McEliece-1409 decodingchallenge") |
| instance_size | numeric size in the class's natural unit (bits of group order; lattice dim; code length n) |
| instance_size_unit | "bits" / "dim" / "n" / "digits" |
| log2_ops | log2 expected/actual operations as reported (null if not stated) |
| method | algorithm (Pollard rho, G6K GPU sieve, BJMM/MMT ISD, NFS, kangaroo, ...) |
| structure_exploited | true if the solve used special structure (Koblitz/Frobenius, QC, weak curve, ideal structure), else false |
| hardware | as reported ("200 PS3", "64 Spartan-6 FPGAs", "4x RTX 2080 Ti", "CPU cluster") |
| raw_compute | the authors' own resource statement, verbatim-ish, short ("about 3.5 months on 200 PS3s", "2700 core-years") |
| reported_core_years | number if the source states CPU-core-years (or core-hours converted /8766), else null |
| gpu_years | number if stated, else null |
| wall_time_days | number if stated, else null |
| date | YYYY-MM or YYYY-MM-DD of the solve/announcement |
| solvers | list of names / team |
| academic | true for academic/research-lab work; false for hobbyist/puzzle/industry-anonymous |
| challenge | name of challenge if a challenge entry (Certicom, TU Darmstadt SVP, decodingchallenge.org, RSA, Bitcoin puzzle #N, TII McEliece), else null |
| extrapolation | authors' own extrapolation to deployed parameters, short text, or null |
| paper | ePrint id / DOI / arXiv id, or null |
| source_url | primary URL where the facts were read (required) |
| other_urls | list |
| confidence | 0.0-1.0 that the fields are correct as transcribed |
| verified | false, or true when a human has checked it |
| verified_by | (only when verified) who checked it, when, and how |
| notes | short |

Normalization to 2020 CPU-core-year equivalents is done later in
`analysis/` with documented conversion factors; record files only hold raw
figures.
