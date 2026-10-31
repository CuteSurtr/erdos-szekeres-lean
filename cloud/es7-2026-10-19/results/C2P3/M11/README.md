# C2P3 M11

Task `results/C2P3/TASK.md` (commit 4f653319), LIST = `C2P3.tsv`, j = 11, N = 50, H = 2.5.
Start 2026-10-31 09:42:47Z, lane END 11:57:47Z (epoch 1793447867); lane done 11:45:24Z (742 s left, below the 15-minute start threshold).
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` from the vendored sources (MANIFEST: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Nothing cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`); cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…b48`, both as expected.
- Cubes P1..P8 from `l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (10: idx ≡ 11 mod 50)

| case | kind | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|
| P7 | Q | 1 (P7_9-14) | 0 | 0 | 0 |
| P6 | H | 3 (P6_1-7-13, P6_3-7-9, P6_7-14-15) | 0 | 0 | 0 |
| P5 | H | 2 (P5_1-3-13, P5_1-10-11) | 0 | 2 (P5_2-7-12, P5_8-12-13) | 0 |
| P5 | Q | 0 | 0 | 2 (P5_6-7, P5_6-16) | 0 |
| total | | 6 | 0 | 4 | 0 |

All 6 records are UNSATISFIABLE with `"certified": true` (lrat-check `c VERIFIED`, cake_lpr `s VERIFIED UNSAT`).

| unit | solve s | lrat-check s | cake_lpr s | proof bytes |
|---|---|---|---|---|
| P7_9-14 (Q, cap 6000) | 2759.73 | 103.0 | 546.6 | 6,791,732,351 |
| P6_1-7-13 | 569.75 | 56.0 | 323.2 | 3,750,685,784 |
| P6_3-7-9 | 232.58 | 47.3 | 309.8 | 3,241,418,955 |
| P6_7-14-15 | 287.09 | 58.3 | 336.7 | 3,159,625,494 |
| P5_1-3-13 | 341.19 | 58.4 | 341.6 | 3,287,294,488 |
| P5_1-10-11 | 356.67 | 59.4 | 331.2 | 3,272,077,110 |

Min / median / max: solve 232.58 / 348.93 / 2759.73 s; lrat-check 47.3 / 58.35 / 103.0 s; cake_lpr 309.8 / 333.95 / 546.6 s; proof 3.16 / 3.28 / 6.79 GB.

Largest solver RSS: 4402 MB (P6_3-7-9). cake_lpr heap 8000 MB.

No SAT, no proof rejection, no error, no memory problem. Disk stayed above 21 GB free.
