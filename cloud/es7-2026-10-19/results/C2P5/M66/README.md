# C2P5 M66: list C2P5B.tsv, shard j = 16 of N = 50, budget H = 5.25 h, TASK at 81cb025f

Machine: 4 cores, 15 GB RAM (`env.txt`). Start 2026-10-31 15:10:31 UTC; lane started 15:12 UTC with END = 1793477431
(20:10:31 UTC, start + 5.25 h − 15 min, `run.sh`). The lane finished all of its units at 19:43:42 UTC.

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (nothing cloned or downloaded). The manifest
  matched all 196 files. The sources are CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc) with the E2 patch.
- Sanity checks gave the expected results. Both checkers reject the bad LRAT and accept the good one, and the cake_lpr
  example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; the sha256 of base.cnf (b0061e90…) and of base.json (2476faff…) match.
- Cubes: P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`: idx ≡ 16 mod 50 of C2P5B.tsv, 19 units)
**All 19 certified UNSAT.** No units timed out, none were left unreached, and there were no errors.

| case | kind | units | certified | timed out | not reached | other |
|---|---|---|---|---|---|---|
| P2 | Q | 1 | 1 | 0 | 0 | 0 |
| P2 | H | 6 | 6 | 0 | 0 | 0 |
| P1 | Q | 1 | 1 | 0 | 0 | 0 |
| P1 | H | 5 | 5 | 0 | 0 | 0 |
| P3 | Q | 1 | 1 | 0 | 0 | 0 |
| P3 | H | 5 | 5 | 0 | 0 | 0 |

Per unit:

| unit | kind | status | cap s | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|
| P2_3-13 | Q | UNSATISFIABLE (certified) | 8000 | 1893.02 | 91.8 | 517.9 | 5.47 | 4511.95 |
| P1_2-13 | Q | UNSATISFIABLE (certified) | 8000 | 2125.15 | 101.0 | 547.4 | 5.7 | 4432.16 |
| P2_1-3-8 | H | UNSATISFIABLE (certified) | 2400 | 322.42 | 63.7 | 334.2 | 3.37 | 4424.54 |
| P2_1-7-10 | H | UNSATISFIABLE (certified) | 2400 | 304.53 | 60.4 | 343.5 | 3.35 | 4402.04 |
| P2_3-6-15 | H | UNSATISFIABLE (certified) | 2400 | 431.22 | 64.7 | 348.2 | 3.55 | 4410.72 |
| P2_3-13-14 | H | UNSATISFIABLE (certified) | 2400 | 285.37 | 58.5 | 324.9 | 3.36 | 4374.46 |
| P2_4-9-11 | H | UNSATISFIABLE (certified) | 2400 | 72.88 | 28.1 | 170.4 | 1.16 | 3179.36 |
| P2_5-9-12 | H | UNSATISFIABLE (certified) | 2400 | 74.61 | 26.3 | 160.2 | 1.11 | 3163.18 |
| P1_2-4-5 | H | UNSATISFIABLE (certified) | 2400 | 72.09 | 26.6 | 171.7 | 1.19 | 3167.96 |
| P1_2-9-10 | H | UNSATISFIABLE (certified) | 2400 | 220.6 | 56.0 | 316.0 | 3.13 | 4395.48 |
| P1_3-6-14 | H | UNSATISFIABLE (certified) | 2400 | 330.29 | 60.0 | 333.1 | 3.36 | 4367.96 |
| P1_4-7-8 | H | UNSATISFIABLE (certified) | 2400 | 29.55 | 15.3 | 106.1 | 0.22 | 2648.24 |
| P1_6-7-9 | H | UNSATISFIABLE (certified) | 2400 | 27.19 | 13.6 | 111.1 | 0.22 | 2646.4 |
| P3_5-12 | Q | UNSATISFIABLE (certified) | 6470 | 1929.39 | 95.9 | 525.9 | 5.43 | 4414.43 |
| P3_1-5-13 | H | UNSATISFIABLE (certified) | 2400 | 480.33 | 68.0 | 360.4 | 3.65 | 4417.93 |
| P3_1-11-12 | H | UNSATISFIABLE (certified) | 2400 | 272.87 | 55.2 | 313.7 | 3.26 | 4371.03 |
| P3_4-7-16 | H | UNSATISFIABLE (certified) | 2315 | 422.33 | 66.0 | 367.6 | 3.59 | 4382.12 |
| P3_5-7-11 | H | UNSATISFIABLE (certified) | 1446 | 25.2 | 15.5 | 108.6 | 0.22 | 2648.84 |
| P3_6-9-12 | H | UNSATISFIABLE (certified) | 1295 | 78.0 | 28.9 | 175.5 | 1.16 | 3156.97 |

Certified Q (3), min / median / max: solve s 1893.0 / 1929.4 / 2125.2; lrat-check s 91.8 / 95.9 / 101.0; cake_lpr s 517.9 / 525.9 / 547.4; proof GB 5.4 / 5.5 / 5.7

Certified H (16), min / median / max: solve s 25.2 / 246.7 / 480.3; lrat-check s 13.6 / 55.6 / 68.0; cake_lpr s 106.1 / 314.9 / 367.6; proof GB 0.2 / 3.2 / 3.7

Certified all (19), min / median / max: solve s 25.2 / 285.4 / 2125.2; lrat-check s 13.6 / 58.5 / 101.0; cake_lpr s 106.1 / 324.9 / 547.4; proof GB 0.2 / 3.3 / 5.7

Largest solver RSS: 4512 MB

Notes:
- There was no SAT (`/opt/work/SAT_FOUND` never appeared), and neither checker rejected a proof.
- There were no memory problems. Peak RSS was about 8.2 GB, for cake_lpr with an 8000 MB heap, and at most 4.5 GB for CaDiCaL.
- P3_5-12 ran with a cap of 6470 s instead of 8000 s, because lane.py shortened it to fit END. It solved in 1929 s.
- P3_4-7-16 ran with a cap of 2315 s, also shortened to fit END.
- Each proof was deleted after both checks.
