# C2P5 M76: LIST C2P5B.tsv, shard j=26 of N=50, H=5.25 (TASK at 81cb025f)

Start 2026-10-31 15:10:27Z (epoch 1793459427); lane END 1793477427 (20:10:27Z). Machine: 4 cores, 15 GB RAM (`env.txt`).

## Tools and checks

- `C2P/vendor/build_tools.sh` from the vendored sources: manifest 196/196 files match; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Nothing cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…f2b48`, both as expected.
- Cubes P1..P8 from `C2C34/l2cubes.py`: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details in `tools.txt`; the lane command is in `run.sh`.

## Units (19)

| case | kind | certified | timed out | not reached | error |
|---|---|---|---|---|---|
| P1 | H | 5 | 0 | 0 | 0 |
| P1 | Q | 1 | 0 | 0 | 0 |
| P2 | H | 6 | 0 | 0 | 0 |
| P2 | Q | 1 | 0 | 0 | 0 |
| P3 | H | 5 | 0 | 0 | 0 |
| P3 | Q | 1 | 0 | 0 | 0 |
| all | | 19 | 0 | 0 | 0 |

Other outcomes: none.

| idx | unit | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB | certified |
|---|---|---|---|---|---|---|---|---|---|---|
| 26 | P2_4-11 | Q | 8000 | UNSATISFIABLE | 1626.07 | 90.9 | 449.9 | 4.88 | 4379.7 | True |
| 76 | P1_3-10 | Q | 8000 | UNSATISFIABLE | 1383.25 | 76.5 | 434.6 | 4.65 | 4439.3 | True |
| 126 | P2_1-4-6 | H | 2400 | UNSATISFIABLE | 237.34 | 58.2 | 337.6 | 3.22 | 4404.65 | True |
| 176 | P2_3-4-8 | H | 2400 | UNSATISFIABLE | 86.45 | 27.5 | 178.1 | 1.17 | 3116.71 | True |
| 226 | P2_3-7-16 | H | 2400 | UNSATISFIABLE | 440.73 | 63.0 | 369.8 | 3.61 | 4440.79 | True |
| 276 | P2_4-5-13 | H | 2400 | UNSATISFIABLE | 260.8 | 55.2 | 314.2 | 3.25 | 4409.65 | True |
| 326 | P2_4-11-13 | H | 2400 | UNSATISFIABLE | 244.1 | 54.6 | 328.7 | 3.21 | 4375.37 | True |
| 376 | P2_6-7-9 | H | 2400 | UNSATISFIABLE | 28.77 | 14.3 | 118.3 | 0.22 | 2663.11 | True |
| 426 | P1_2-4-15 | H | 2400 | UNSATISFIABLE | 328.04 | 59.3 | 343.7 | 3.47 | 4429.24 | True |
| 476 | P1_2-10-14 | H | 2400 | UNSATISFIABLE | 405.74 | 60.9 | 355.6 | 3.55 | 4376.34 | True |
| 526 | P1_3-8-9 | H | 2400 | UNSATISFIABLE | 27.79 | 13.7 | 115.2 | 0.22 | 2679.88 | True |
| 576 | P1_4-8-12 | H | 2400 | UNSATISFIABLE | 208.03 | 54.0 | 316.3 | 3.17 | 4383.97 | True |
| 626 | P1_6-9-12 | H | 2400 | UNSATISFIABLE | 78.04 | 25.9 | 172.8 | 1.11 | 3123.62 | True |
| 676 | P3_6-13 | Q | 7227 | UNSATISFIABLE | 2188.81 | 89.6 | 486.9 | 5.57 | 4359.77 | True |
| 726 | P3_1-6-13 | H | 2400 | UNSATISFIABLE | 540.93 | 66.7 | 370.5 | 3.72 | 4381.88 | True |
| 776 | P3_1-13-15 | H | 2400 | UNSATISFIABLE | 239.42 | 54.9 | 331.6 | 3.23 | 4393.76 | True |
| 826 | P3_4-9-11 | H | 2400 | UNSATISFIABLE | 93.13 | 25.9 | 170.5 | 1.15 | 3180.53 | True |
| 876 | P3_5-8-14 | H | 2400 | UNSATISFIABLE | 298.6 | 54.7 | 315.7 | 3.21 | 4402.97 | True |
| 926 | P3_7-8-9 | H | 1827 | UNSATISFIABLE | 26.82 | 14.5 | 115.3 | 0.22 | 2646.74 | True |

## Certified units: min / median / max

- kind H (16): solve s 26.8 / 238.4 / 540.9; lrat-check s 13.7 / 54.7 / 66.7; cake_lpr s 115.2 / 316.0 / 370.5; proof GB 0.2 / 3.2 / 3.7
- kind Q (3): solve s 1383.2 / 1626.1 / 2188.8; lrat-check s 76.5 / 89.6 / 90.9; cake_lpr s 434.6 / 449.9 / 486.9; proof GB 4.6 / 4.9 / 5.6
- all (19): solve s 26.8 / 244.1 / 2188.8; lrat-check s 13.7 / 54.9 / 90.9; cake_lpr s 115.2 / 328.7 / 486.9; proof GB 0.2 / 3.2 / 5.6

## Resources

Largest solver RSS: 4441 MB (of 15 GB). Free disk stayed at or above about 22 GB (the largest proof was 5.57 GB).

## SAT, proof rejections, memory

- SAT: none.
- Proof rejections (certified false): none.
- Errors: none.
- Memory problems: none.
