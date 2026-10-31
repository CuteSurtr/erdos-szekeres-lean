# C2P3 M41 (LIST C2P3.tsv, shard j=41 of N=50, H=2.5, task commit 4f653319)

## Tools and checks
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 of base.cnf and base.json match the task.
- Cubes P1..P8: byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details in `tools.txt`; machine in `env.txt` (4 cores, 15 GB).

## Units (9, idx ≡ 41 mod 50)
| unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof bytes |
|---|---|---|---|---|---|---|---|---|
| P6_3-8 | P6 | Q | 6000 | certified UNSAT | 2105.81 | 96.2 | 511.8 | 5794060952 |
| P6_2-8-15 | P6 | H | 1800 | certified UNSAT | 549.72 | 64.4 | 350.8 | 3702391119 |
| P6_7-9-12 | P6 | H | 1800 | certified UNSAT | 27.18 | 13.4 | 108.8 | 215119634 |
| P5_1-2-4 | P5 | H | 1800 | certified UNSAT | 25.66 | 13.0 | 110.0 | 214745046 |
| P5_1-7-15 | P5 | H | 1800 | certified UNSAT | 478.70 | 61.3 | 344.7 | 3621629265 |
| P5_2-3-8 | P5 | H | 1800 | certified UNSAT | 231.13 | 52.8 | 301.4 | 3197972815 |
| P5_2-11-12 | P5 | H | 1800 | certified UNSAT | 308.02 | 54.1 | 299.5 | 3261311651 |
| P5_6-10-13 | P5 | H | 1800 (lane cap 1132) | certified UNSAT | 130.21 | 34.8 | 216.8 | 1937179294 |
| P5_7-13 | P5 | Q | 2400 (lane cap 743) | UNKNOWN (timeout) | 733.31 | – | – | – |

Counts:
- Certified 8: P6 Q 1, P6 H 2, P5 H 5.
- Timed out (UNKNOWN) 1: P5 Q 1 (P5_7-13, cap shortened to 743 s by the END limit; it remains open).
- Not reached 0. Errors 0. `"certified": false` 0.

Certified units (8), min / median / max:
- solve: 25.66 / 269.58 / 2105.81 s
- lrat-check: 13.0 / 53.45 / 96.2 s
- cake_lpr: 108.8 / 300.45 / 511.8 s
- proof: 0.215 / 3.23 / 5.79 GB

Largest solver RSS: 4421 MB (P6_3-8). cake_lpr ran with an 8000 MB heap (about 8.2 GB RSS).

No SAT, no proof rejection, no memory problem.
