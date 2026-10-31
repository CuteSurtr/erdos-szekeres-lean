# C2P5 M67: list C2P5B.tsv, shard j = 17 of N = 50, H = 5.25 (TASK.md commit 81cb025f)

## Tools and checks

- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch. Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF `SYMZ/zcnf.py rot 17 7 --m 2 --hull`: header `p cnf 838032 16653336`, sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…b48`, both as expected.
- Cubes P1..P8 from `C2C34/l2cubes.py`: all byte-identical to `C2P/cubes/P{a}_cubes.txt`. Details in `tools.txt`.
- One lane, `run.sh`; start 2026-10-31 15:10:36 UTC, END 1793477436 (20:10:36 UTC).

## Units (19)

| idx | unit | case | kind | cap | result | solve s | lrat-check s | cake_lpr s | proof | RSS MB |
|---|---|---|---|---|---|---|---|---|---|---|
| 17 | P2_3-14 | P2 | Q | 8000 | certified | 1956.82 | 91.4 | 511.8 | 5.76 GB | 4396.97 |
| 67 | P1_2-14 | P1 | Q | 8000 | certified | 2065.47 | 91.1 | 509.5 | 5.95 GB | 4508.15 |
| 117 | P2_1-3-9 | P2 | H | 2400 | certified | 386.31 | 54.7 | 314.7 | 3.48 GB | 4382.83 |
| 167 | P2_1-7-11 | P2 | H | 2400 | certified | 413.8 | 56.0 | 326.2 | 3.49 GB | 4402.72 |
| 217 | P2_3-6-16 | P2 | H | 2400 | certified | 359.18 | 53.4 | 318.0 | 3.55 GB | 4429.82 |
| 267 | P2_3-13-15 | P2 | H | 2400 | certified | 305.09 | 54.4 | 328.3 | 3.45 GB | 4379.92 |
| 317 | P2_4-9-12 | P2 | H | 2400 | certified | 215.85 | 50.1 | 297.0 | 3.13 GB | 4356.71 |
| 367 | P2_5-9-13 | P2 | H | 2400 | certified | 223.46 | 52.6 | 319.4 | 3.08 GB | 4368.36 |
| 417 | P1_2-4-6 | P1 | H | 2400 | certified | 27.93 | 13.2 | 108.2 | 0.22 GB | 2670.92 |
| 467 | P1_2-9-11 | P1 | H | 2400 | certified | 236.13 | 50.5 | 309.8 | 3.24 GB | 4367.46 |
| 517 | P1_3-6-15 | P1 | H | 2400 | certified | 365.66 | 57.2 | 336.3 | 3.42 GB | 4423.2 |
| 567 | P1_4-7-9 | P1 | H | 2400 | certified | 29.87 | 14.9 | 112.6 | 0.22 GB | 2675.19 |
| 617 | P1_6-7-10 | P1 | H | 2400 | certified | 27.47 | 14.7 | 108.5 | 0.22 GB | 2646.16 |
| 667 | P3_5-13 | P3 | Q | 5879 | certified | 2358.37 | 88.2 | 530.0 | 6.01 GB | 4367.28 |
| 717 | P3_1-5-14 | P3 | H | 2400 | certified | 447.34 | 56.3 | 321.7 | 3.69 GB | 4412.05 |
| 767 | P3_1-11-13 | P3 | H | 2036 | certified | 253.33 | 48.7 | 289.4 | 3.30 GB | 4361.1 |
| 817 | P3_4-8-9 | P3 | H | 1435 | certified | 25.0 | 12.2 | 97.9 | 0.22 GB | 2648.23 |
| 867 | P3_5-7-12 | P3 | H | 1298 | certified | 64.67 | 22.9 | 145.6 | 1.11 GB | 3169.28 |
| 917 | P3_6-9-13 | P3 | H | 1061 | certified | 100.42 | 29.3 | 181.3 | 1.65 GB | 3401.48 |

## Counts by case and kind

| case | kind | certified | timed out | not reached | errors |
|---|---|---|---|---|---|
| P1 | H | 5 | 0 | 0 | 0 |
| P1 | Q | 1 | 0 | 0 | 0 |
| P2 | H | 6 | 0 | 0 | 0 |
| P2 | Q | 1 | 0 | 0 | 0 |
| P3 | H | 5 | 0 | 0 | 0 |
| P3 | Q | 1 | 0 | 0 | 0 |

Total: 19 certified.

## Certified units: min / median / max

- solve s: 25.0 / 253.33 / 2358.37
- lrat-check s: 12.2 / 52.6 / 91.4
- cake_lpr s: 97.9 / 314.7 / 530.0
- proof size: 0.22 GB / 3.30 GB / 6.01 GB
- kind Q (3): solve 1956.82 / 2065.47 / 2358.37 s; lrat-check 88.2 / 91.1 / 91.4 s; cake_lpr 509.5 / 511.8 / 530.0 s; proof 5.76 GB / 5.95 GB / 6.01 GB
- kind H (16): solve 25.0 / 229.80 / 447.34 s; lrat-check 12.2 / 50.3 / 57.2 s; cake_lpr 97.9 / 303.4 / 336.3 s; proof 0.22 GB / 3.18 GB / 3.69 GB

Largest solver RSS: 4508 MB (P1_2-14).

## SAT, proof rejections, memory

- SAT: none.
- Certified false or ERROR records: none.
- Memory: no problem; the largest RSS is well under the 15 GB of the machine.
