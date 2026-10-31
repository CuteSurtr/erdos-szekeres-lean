# C2P5 M56: LIST = C2P5B.tsv, shard j = 6 of N = 50, H = 5.25 h (task commit 81cb025f)

Start 2026-10-31 15:09:32 UTC (epoch 1793459372); END = 1793477372 (20:09:32 UTC). The lane finished all units at 18:58:00 UTC.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: all 196 vendored files match `MANIFEST.sha256`. Built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, E2 patch) from those sources. Nothing was cloned or downloaded.
- Sanity checks: the cake_lpr example prints `s VERIFIED UNSAT`. Both checkers reject the bad LRAT and accept the good one.
- Base CNF: header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…) and base.json (2476faff…) both match.
- Cubes P1..P8 from `l2cubes.py`: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (14)
| case | kind | units | certified | timed out | not reached | errors |
|---|---|---|---|---|---|---|
| P2 | Q | 1 | 1 | 0 | 0 | 0 |
| P1 | Q | 2 | 2 | 0 | 0 | 0 |
| P1 | H | 5 | 5 | 0 | 0 | 0 |
| P3 | Q | 1 | 1 | 0 | 0 | 0 |
| P3 | H | 5 | 5 | 0 | 0 | 0 |
| **total** | | **14** | **14** | 0 | 0 | 0 |

Every unit is UNSATISFIABLE and certified: lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.

Certified units (min / median / max):
- solve: 28.65 / 375.5 / 2462.0 s (Q: 455.4 / 1342.8 / 2462.0 s; H: 28.65 / 259.1 / 525.5 s)
- lrat-check: 14.7 / 59.4 / 100.9 s
- cake_lpr: 116.0 / 339.1 / 581.8 s
- proof size: 0.215 / 3.36 / 6.05 GB

| unit | kind | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|
| P2_1-9 | Q | 2192.25 | 90.2 | 516.4 | 5.43 | 4424 |
| P1_2-3 | Q | 455.41 | 63.3 | 360.6 | 3.43 | 4374 |
| P1_7-8 | Q | 493.35 | 62.1 | 337.8 | 3.33 | 4372 |
| P1_2-3-7 | H | 29.04 | 15.0 | 121.5 | 0.22 | 2657 |
| P1_2-7-15 | H | 525.54 | 61.5 | 370.7 | 3.63 | 4419 |
| P1_3-5-13 | H | 282.72 | 56.5 | 310.4 | 3.15 | 4388 |
| P1_4-5-13 | H | 235.54 | 56.8 | 333.9 | 3.20 | 4360 |
| P1_5-8-12 | H | 109.47 | 32.7 | 207.1 | 1.58 | 3326 |
| P3_4-13 | Q | 2462.01 | 100.9 | 581.8 | 6.05 | 4490 |
| P3_1-4-14 | H | 421.40 | 63.2 | 357.5 | 3.56 | 4382 |
| P3_1-9-13 | H | 433.86 | 57.2 | 340.4 | 3.49 | 4369 |
| P3_4-6-15 | H | 329.53 | 63.2 | 344.6 | 3.40 | 4376 |
| P3_5-6-9 | H | 28.65 | 14.7 | 116.0 | 0.22 | 2650 |
| P3_6-7-13 | H | 121.91 | 34.9 | 230.2 | 1.78 | 3455 |

The largest solver RSS was 4490 MB (P3_4-13).

## SAT, rejections, memory
- No SAT answer.
- No proof was rejected, and there were no errors.
- No memory problems: solver RSS stayed at or below 4.5 GB out of 15 GB.
