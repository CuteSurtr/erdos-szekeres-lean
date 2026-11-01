# C2P5 M34 — LIST C2P5A.tsv, shard j=34 of N=37, H=4.5, TASK commit 81cb025f

Start 2026-10-31 19:25:49Z (epoch 1793474749); END 1793490049 (23:40:49Z). Lane finished all units at 21:22:44Z.

## Tools and checks
- Built by `C2P/vendor/build_tools.sh` from the vendored sources only: CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc + E2 patch. Manifest: all 196 files match.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 for base.cnf and base.json both match.
- Cubes P1..P8: byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details are in `tools.txt`.

## Units (10, all P4 hexagonal, cap 2400 s)
| case | kind | certified | timed out (UNKNOWN) | not reached | errors |
|---|---|---|---|---|---|
| P4 | H | 10 | 0 | 0 | 0 |

Certified (min / median / max):
- solve: 19.54 / 363.87 / 585.94 s
- lrat-check: 13.4 / 56.9 / 65.5 s
- cake_lpr: 118.3 / 334.95 / 363.5 s
- proof size: 0.21 / 3.34 / 3.71 GB

| unit | kind | status | certified | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|
| P4_1-2-11 | H | UNSATISFIABLE | True | 428.4 | 56.4 | 332.1 | 3.36 | 4355 |
| P4_1-5-9 | H | UNSATISFIABLE | True | 431.45 | 57.9 | 351.0 | 3.44 | 4375 |
| P4_1-7-12 | H | UNSATISFIABLE | True | 585.94 | 65.4 | 357.9 | 3.71 | 4368 |
| P4_1-8-15 | H | UNSATISFIABLE | True | 531.05 | 65.5 | 363.5 | 3.64 | 4376 |
| P4_1-10-14 | H | UNSATISFIABLE | True | 389.46 | 58.1 | 339.6 | 3.37 | 4361 |
| P4_1-13-14 | H | UNSATISFIABLE | True | 288.59 | 57.1 | 334.6 | 3.24 | 4400 |
| P4_2-7-10 | H | UNSATISFIABLE | True | 338.28 | 56.7 | 335.3 | 3.32 | 4374 |
| P4_5-9-11 | H | UNSATISFIABLE | True | 31.88 | 15.5 | 124.0 | 0.22 | 2663 |
| P4_6-9-14 | H | UNSATISFIABLE | True | 240.95 | 54.2 | 310.2 | 3.17 | 4373 |
| P4_9-10-12 | H | UNSATISFIABLE | True | 19.54 | 13.4 | 118.3 | 0.21 | 2357 |

Largest solver RSS: 4400 MB (about 4.3 GB).

There were no SAT answers, no proof rejections (every record has `c VERIFIED` and `s VERIFIED UNSAT`), no errors and no memory problems.
