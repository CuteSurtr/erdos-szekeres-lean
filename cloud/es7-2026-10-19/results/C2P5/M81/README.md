# C2P5 M81: LIST = C2P5B.tsv, shard j = 31 of N = 50, H = 5.25 h (TASK commit 81cb025f)

**Result: all 19 units were certified UNSAT (lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`). There was no SAT, no timeout, no unit left unreached, no error, no proof rejection and no memory problem.**

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch).
- Sanity checks: both checkers reject the bad LRAT and accept the good one, and the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. Both sha256 values match the expected ones: base.cnf `b0061e90…d8ff1` and base.json `2476faff…bb472b48`.
- Cubes P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Run
- Lane start: 15:24:41 UTC (epoch 1793460281). END = 1793478281 (`run.sh`).
- The first unit started at 15:27:18 and the lane finished at 19:30:16 UTC, well before END.
- Lane cap note: P3_7-11 had a listed cap of 8000 s, but lane.py set its cap to 6877 s so that the checks would finish before END. It solved in 984 s.

## Units (rows with idx ≡ 31 mod 50; 19 in all)

| case | kind | units | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|---|
| P2 | Q | 1 | 1 | 0 | 0 | 0 |
| P2 | H | 6 | 6 | 0 | 0 | 0 |
| P1 | Q | 1 | 1 | 0 | 0 | 0 |
| P1 | H | 5 | 5 | 0 | 0 | 0 |
| P3 | Q | 1 | 1 | 0 | 0 | 0 |
| P3 | H | 5 | 5 | 0 | 0 | 0 |
| **all** | | **19** | **19** | 0 | 0 | 0 |

Certified units, min / median / max:

| kind | n | solve s | lrat-check s | cake_lpr s | proof GB |
|---|---|---|---|---|---|
| Q | 3 | 510.5 / 984.4 / 2539.6 | 48.9 / 56.4 / 85.0 | 324.9 / 388.7 / 546.0 | 3.31 / 3.94 / 5.82 |
| H | 16 | 20.6 / 251.6 / 588.1 | 11.1 / 47.4 / 57.3 | 108.9 / 303.4 / 352.7 | 0.22 / 3.17 / 3.67 |
| all | 19 | 20.6 / 327.4 / 2539.6 | 11.1 / 48.5 / 85.0 | 108.9 / 321.3 / 546.0 | 0.22 / 3.28 / 5.82 |

Per unit, in seconds (solve / lrat-check / cake_lpr) with proof size:
- P2_5-6 Q 510 / 49 / 325, 3.31 GB
- P1_3-15 Q 2540 / 85 / 546, 5.82 GB
- P2_1-4-11 530 / 50 / 343, 3.57 GB
- P2_3-4-13 360 / 51 / 325, 3.37 GB
- P2_3-8-13 504 / 52 / 335, 3.48 GB
- P2_4-6-9 28 / 12 / 114, 0.22 GB
- P2_5-6-7 29 / 12 / 115, 0.22 GB
- P2_6-8-9 29 / 11 / 113, 0.22 GB
- P1_2-5-9 227 / 45 / 298, 3.11 GB
- P1_2-11-15 464 / 57 / 353, 3.53 GB
- P1_3-8-14 557 / 52 / 333, 3.40 GB
- P1_4-9-12 254 / 48 / 302, 3.18 GB
- P1_7-9-10 21 / 12 / 109, 0.24 GB
- P3_7-11 Q 984 / 56 / 389, 3.94 GB
- P3_1-7-9 327 / 49 / 321, 3.28 GB
- P3_4-5-6 89 / 25 / 178, 1.36 GB
- P3_4-9-16 588 / 51 / 337, 3.67 GB
- P3_5-9-13 249 / 46 / 305, 3.17 GB
- P3_7-9-10 29 / 11 / 112, 0.23 GB

## Resources
- Largest solver RSS: 4418 MB (P3_4-9-16). cake_lpr ran with an 8000 MB heap.
- Free disk never fell below about 22 GB.
- No SAT_FOUND. No record had `"certified": false` or an ERROR status.
