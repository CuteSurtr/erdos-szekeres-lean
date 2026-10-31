# C2P5 M71

Task `results/C2P5/TASK.md` (commit 81cb025f), V = M71, LIST = C2P5B.tsv, j = 21, N = 50, H = 5.25.
Start 2026-10-31 15:09:30 UTC (epoch 1793459370), END = 1793477370 (20:09:30 UTC). The lane finished all units at 18:17:42 UTC.

## Tools and checks (`tools.txt`)

- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Nothing was cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf and base.json match the expected values.
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (19, all certified)

| case | kind | outcome | units |
|---|---|---|---|
| P1 | H | certified | 5 |
| P1 | Q | certified | 1 |
| P2 | H | certified | 6 |
| P2 | Q | certified | 1 |
| P3 | H | certified | 5 |
| P3 | Q | certified | 1 |

Certified units, min / median / max:

- solve: 23.51 / 268.33 / 528.81 s
- lrat-check: 12.9 / 53.9 / 63.2 s
- cake_lpr: 109.4 / 314.0 / 350.5 s
- proof size: 0.22 GB / 3.23 GB / 3.67 GB

Largest solver RSS: 4440 MB (P3_1-6-8).

| unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB | certified |
|---|---|---|---|---|---|---|---|---|---|---|
| P2_4-6 | P2 | Q | 8000 | UNSATISFIABLE | 414.91 | 59.6 | 316.8 | 3.31 | 4369 | True |
| P1_3-5 | P1 | Q | 8000 | UNSATISFIABLE | 385.05 | 52.8 | 301.8 | 3.32 | 4378 | True |
| P2_1-3-13 | P2 | H | 2400 | UNSATISFIABLE | 425.4 | 57.1 | 320.9 | 3.59 | 4427 | True |
| P2_1-8-11 | P2 | H | 2400 | UNSATISFIABLE | 314.05 | 54.3 | 337.8 | 3.34 | 4359 | True |
| P2_3-7-11 | P2 | H | 2400 | UNSATISFIABLE | 244.33 | 57.2 | 314.0 | 3.23 | 4353 | True |
| P2_4-5-8 | P2 | H | 2400 | UNSATISFIABLE | 25.46 | 12.9 | 114.7 | 0.22 | 2653 | True |
| P2_4-10-11 | P2 | H | 2400 | UNSATISFIABLE | 76.12 | 26.6 | 170.6 | 1.11 | 3160 | True |
| P2_5-10-13 | P2 | H | 2400 | UNSATISFIABLE | 237.21 | 56.1 | 318.1 | 3.17 | 4361 | True |
| P1_2-4-10 | P1 | H | 2400 | UNSATISFIABLE | 212.77 | 50.4 | 305.3 | 3.14 | 4364 | True |
| P1_2-9-15 | P1 | H | 2400 | UNSATISFIABLE | 528.81 | 63.2 | 349.1 | 3.67 | 4430 | True |
| P1_3-7-11 | P1 | H | 2400 | UNSATISFIABLE | 226.07 | 53.3 | 315.8 | 3.14 | 4330 | True |
| P1_4-7-13 | P1 | H | 2400 | UNSATISFIABLE | 278.03 | 54.4 | 319.7 | 3.25 | 4411 | True |
| P1_6-8-10 | P1 | H | 2400 | UNSATISFIABLE | 25.33 | 14.0 | 122.6 | 0.22 | 2648 | True |
| P3_6-8 | P3 | Q | 8000 | UNSATISFIABLE | 498.92 | 62.0 | 350.5 | 3.43 | 4376 | True |
| P3_1-6-8 | P3 | H | 2400 | UNSATISFIABLE | 274.01 | 53.5 | 308.0 | 3.25 | 4440 | True |
| P3_1-12-13 | P3 | H | 2400 | UNSATISFIABLE | 268.33 | 53.9 | 331.3 | 3.22 | 4405 | True |
| P3_4-8-13 | P3 | H | 2400 | UNSATISFIABLE | 361.36 | 56.5 | 311.9 | 3.32 | 4416 | True |
| P3_5-8-9 | P3 | H | 2400 | UNSATISFIABLE | 23.51 | 12.9 | 109.4 | 0.22 | 2650 | True |
| P3_6-10-13 | P3 | H | 2400 | UNSATISFIABLE | 95.26 | 25.6 | 171.4 | 1.22 | 3223 | True |

Non-certified / error / rejected: none

Totals: 19 certified, 0 timed out (UNKNOWN), 0 not reached, 0 errors.

No SAT, no proof rejection (every proof: lrat-check `c VERIFIED`, cake_lpr `s VERIFIED UNSAT`), no memory problem (max solver RSS 4.4 GB of 15 GB).
