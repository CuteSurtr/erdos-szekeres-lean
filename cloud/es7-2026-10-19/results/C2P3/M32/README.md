# C2P3 M32

Task `results/C2P3/TASK.md` at 4f653319, LIST = C2P3.tsv, j = 32, N = 50, H = 2.5.
Machine: 4 cores, 15 GB RAM (`env.txt`). Start 09:42:53Z (epoch 1793439773), END 1793447873 (12:11:13Z).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: manifest check passed (all 196 files match). It built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, E2 patch) from the vendored sources. Nothing was cloned or downloaded.
- Sanity: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…) and of base.json (2476faff…) both match.
- Cubes P1..P8: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, idx ≡ 32 mod 50): 10 units
| case | kind | certified | timed out | not reached | errors |
|---|---|---|---|---|---|
| P6 | Q | 2 (P6_2-4, P6_9-12) | 0 | 0 | 0 |
| P6 | H | 3 (P6_2-7-12, P6_7-8-10, P6_9-10-14) | 0 | 0 | 0 |
| P5 | Q | 1 (P5_1-14) | 0 | 0 | 0 |
| P5 | H | 2 (P5_1-6-16, P5_2-9-16) | 0 | 2 (P5_6-9-11, P5_7-10-15) | 0 |
| **total** | | **8** | **0** | **2** | **0** |

All 8 records are UNSATISFIABLE with `"certified": true` (lrat-check `c VERIFIED`, cake_lpr `s VERIFIED UNSAT`).
- P5_2-9-16 ran with its cap cut to 1036 s by the time limit and finished in 407 s.
- The lane stopped at 11:43:55Z with 837 s left before END, which was under its 15-minute floor for starting a unit. The last two units were therefore not reached.

| unit | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|
| P6_2-4 (Q, cap 6000) | 815.4 | 59.1 | 339.8 | 4.09 | 4370 |
| P6_9-12 (Q, cap 4800) | 681.1 | 58.0 | 327.9 | 3.82 | 4397 |
| P6_2-7-12 (H) | 524.5 | 55.8 | 318.1 | 3.67 | 4371 |
| P6_7-8-10 (H) | 23.7 | 12.2 | 109.0 | 0.21 | 2650 |
| P6_9-10-14 (H) | 104.8 | 31.2 | 190.5 | 1.77 | 3467 |
| P5_1-6-16 (H) | 355.2 | 54.1 | 316.1 | 3.51 | 4378 |
| P5_1-14 (Q, cap 2400) | 1393.8 | 73.0 | 431.3 | 4.83 | 4383 |
| P5_2-9-16 (H) | 407.3 | 58.1 | 320.5 | 3.55 | 4378 |

Across the 8 certified units:

| | min | median | max |
|---|---|---|---|
| solve s | 23.7 | 465.9 | 1393.8 |
| lrat-check s | 12.2 | 56.9 | 73.0 |
| cake_lpr s | 109.0 | 319.3 | 431.3 |
| proof bytes | 0.21 GB | 3.61 GB | 4.83 GB |

Largest solver RSS: 4397 MB (P6_9-12). cake_lpr used an 8000 MB heap.

No SAT, no proof rejection, no memory problem and no errors.
