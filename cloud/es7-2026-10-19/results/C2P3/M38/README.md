# C2P3 M38

TASK `results/C2P3/TASK.md` at commit 4f653319, with V = M38, LIST = C2P3.tsv, j = 38, N = 50, H = 2.5.
Machine: 4 cores, 15 GB RAM (`env.txt`). Start 2026-10-31 09:42:39 UTC (epoch 1793439759), END epoch 1793447859 (11:57:39 UTC).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: manifest 196/196 files match; CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch, all built from the vendored sources (nothing downloaded).
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…2b48`, both as required.
- Cubes P1..P8 from `C2C34/l2cubes.py`: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (9 rows with idx ≡ 38 mod 50)

| case | kind | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|
| P6 | Q | 1 (P6_2-15) | 0 | 0 | 0 |
| P6 | H | 3 (P6_2-8-11, P6_7-8-16, P6_10-11-13) | 0 | 0 | 0 |
| P5 | Q | 2 (P5_2-3, P5_6-10) | 0 | 1 (P5_7-12) | 0 |
| P5 | H | 2 (P5_1-7-12, P5_2-10-15) | 0 | 0 | 0 |
| total | | 8 | 0 | 1 | 0 |

All 8 records are UNSATISFIABLE with `"certified": true` (lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`).
P5_6-10 ran with its cap shortened by lane.py to 1294 s and finished in 1028.85 s. P5_7-12 was not started: 418 s were left before END when the lane stopped.

| unit | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|
| P6_2-15 | 1190.71 | 70.3 | 385.6 | 4742276465 | 4373.7 |
| P6_2-8-11 | 382.08 | 51.7 | 310.3 | 3463778090 | 4358.6 |
| P6_7-8-16 | 279.56 | 50.3 | 280.7 | 3268313223 | 4362.3 |
| P6_10-11-13 | 24.22 | 13.4 | 106.6 | 218785952 | 2643.6 |
| P5_1-7-12 | 520.68 | 58.2 | 322.3 | 3735686134 | 4376.6 |
| P5_2-3 | 744.55 | 58.4 | 351.2 | 4029062529 | 4405.8 |
| P5_2-10-15 | 412.77 | 55.6 | 313.6 | 3540666476 | 4369.1 |
| P5_6-10 | 1028.85 | 67.2 | 360.0 | 4342647129 | 4395.3 |

Certified units (min / median / max): solve 24.2 / 466.7 / 1190.7 s; lrat-check 13.4 / 56.9 / 70.3 s; cake_lpr 106.6 / 318.0 / 385.6 s; proof 0.22 / 3.64 / 4.74 GB.

Largest solver RSS: 4405.8 MB (P5_2-3).

No SAT, no proof rejection, no error, no memory problem.
