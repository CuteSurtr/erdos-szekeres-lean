# C2P5 M79: LIST C2P5B.tsv, shard j = 29 of N = 50, H = 5.25 (TASK.md at 81cb025f)

**All 19 units certified UNSAT** (lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT` on every proof). No SAT, no timeouts (UNKNOWN), no unit left unreached, no errors, no proof rejections, no memory problems.

## Tools and checks (details in `tools.txt`)
- `C2P/vendor/build_tools.sh`: all 196 vendored files match MANIFEST.sha256; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch) built from `vendor/tools-src.tar.xz`, nothing downloaded. cake_lpr example `s VERIFIED UNSAT`; sanity: both checkers reject the bad LRAT and accept the good one.
- Base CNF `SYMZ/zcnf.py rot 17 7 --m 2 --hull`: header `p cnf 838032 16653336`, sha256 of base.cnf and base.json as expected.
- Cubes: `l2cubes.py` for P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Lane: `run.sh` (start 15:10 UTC, END epoch 1793477421); the lane finished all units at 19:03:41 UTC, well before END.

## Units by case and kind
| case | kind | certified | other |
|---|---|---|---|
| P1 | H | 5 | 0 |
| P1 | Q | 1 | 0 |
| P2 | H | 6 | 0 |
| P2 | Q | 1 | 0 |
| P3 | H | 5 | 0 |
| P3 | Q | 1 | 0 |

Certified 19 of 19 records; statuses: {'UNSATISFIABLE': 19}

| quantity (certified units) | min / median / max |
|---|---|
| solve s | 21.9 / 254.1 / 2241.3 |
| lrat-check s | 13.5 / 55.1 / 101.4 |
| cake_lpr s | 110.3 / 319.5 / 576.4 |
| proof GB | 0.22 / 3.25 / 5.86 |

Largest solver RSS: 4410 MB (P3_1-14-16).

| unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P2_4-14 | P2 | Q | 8000 | UNSATISFIABLE certified | 2241.29 | 101.4 | 576.4 | 5.86 | 4375 |
| P1_3-13 | P1 | Q | 8000 | UNSATISFIABLE certified | 1838.04 | 88.1 | 509.6 | 5.33 | 4392 |
| P2_1-4-9 | P2 | H | 2400 | UNSATISFIABLE certified | 455.95 | 67.6 | 370.2 | 3.48 | 4372 |
| P2_3-4-11 | P2 | H | 2400 | UNSATISFIABLE certified | 226.72 | 57.7 | 319.5 | 3.18 | 4365 |
| P2_3-8-11 | P2 | H | 2400 | UNSATISFIABLE certified | 254.14 | 55.1 | 328.2 | 3.32 | 4359 |
| P2_4-6-7 | P2 | H | 2400 | UNSATISFIABLE certified | 28.96 | 14.1 | 112.4 | 0.22 | 2652 |
| P2_4-12-14 | P2 | H | 2400 | UNSATISFIABLE certified | 288.61 | 57.8 | 327.8 | 3.32 | 4360 |
| P2_6-7-12 | P2 | H | 2400 | UNSATISFIABLE certified | 21.92 | 14.0 | 112.8 | 0.22 | 2645 |
| P1_2-5-7 | P1 | H | 2400 | UNSATISFIABLE certified | 28.76 | 15.3 | 114.3 | 0.22 | 2670 |
| P1_2-11-13 | P1 | H | 2400 | UNSATISFIABLE certified | 295.26 | 61.3 | 337.1 | 3.39 | 4381 |
| P1_3-8-12 | P1 | H | 2400 | UNSATISFIABLE certified | 265.9 | 54.9 | 309.5 | 3.25 | 4374 |
| P1_4-9-10 | P1 | H | 2400 | UNSATISFIABLE certified | 27.87 | 14.7 | 110.3 | 0.23 | 2645 |
| P1_7-8-10 | P1 | H | 2400 | UNSATISFIABLE certified | 23.94 | 13.5 | 111.0 | 0.22 | 2676 |
| P3_7-9 | P3 | Q | 6817 | UNSATISFIABLE certified | 443.52 | 59.9 | 321.5 | 3.41 | 4370 |
| P3_1-6-16 | P3 | H | 2400 | UNSATISFIABLE certified | 367.68 | 59.8 | 346.8 | 3.56 | 4385 |
| P3_1-14-16 | P3 | H | 2400 | UNSATISFIABLE certified | 219.03 | 52.0 | 315.0 | 3.25 | 4410 |
| P3_4-9-14 | P3 | H | 2400 | UNSATISFIABLE certified | 447.76 | 60.9 | 359.3 | 3.51 | 4374 |
| P3_5-9-11 | P3 | H | 2400 | UNSATISFIABLE certified | 29.78 | 14.0 | 113.1 | 0.22 | 2648 |
| P3_7-8-12 | P3 | H | 2400 | UNSATISFIABLE certified | 30.52 | 16.3 | 110.4 | 0.22 | 2648 |

Note: P3_7-9 ran with cap 6817 s (lane capping the solve so 10 minutes remain for checks before END); it was solved in 444 s.
