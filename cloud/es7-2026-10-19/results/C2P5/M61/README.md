# C2P5 M61: list C2P5B.tsv, shard j = 11 of N = 50, H = 5.25 (TASK commit 81cb025f)

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources (no clone or download): manifest all 196 files match; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch).
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf and base.json match the expected values.
- Cubes: P1..P8 from `C2C34/l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (14 = rows with idx ≡ 11 mod 50)
Lane started 15:13Z with END 20:10:24Z (start 15:10:24Z + 5.25 h − 15 min); it finished all units at 17:38:49Z.

| | certified | timed out (UNKNOWN) | not reached | errors / uncertified |
|---|---|---|---|---|
| P2 Q | 1 | 0 | 0 | 0 |
| P1 Q | 2 | 0 | 0 | 0 |
| P1 H | 5 | 0 | 0 | 0 |
| P3 Q | 1 | 0 | 0 | 0 |
| P3 H | 5 | 0 | 0 | 0 |
| **total** | **14** | **0** | **0** | **0** |

All 14 units are UNSATISFIABLE, and lrat-check (`c VERIFIED`) and cake_lpr (`s VERIFIED UNSAT`) both accepted each proof.

Certified units, min / median / max:

| kind | n | solve s | lrat-check s | cake_lpr s | proof GB |
|---|---|---|---|---|---|
| Q | 4 | 387.52 / 612.21 / 981.74 | 51.6 / 57.5 / 68.5 | 293.8 / 330.55 / 384.2 | 3.32 / 3.75 / 4.19 |
| H | 10 | 18.09 / 221.37 / 347.49 | 11.7 / 48.65 / 55.2 | 106.4 / 281 / 315.4 | 0.21 / 3.145 / 3.40 |
| all | 14 | 18.09 / 262.85 / 981.74 | 11.7 / 49.6 / 68.5 | 106.4 / 298.5 / 384.2 | 0.21 / 3.305 / 4.19 |

| unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof GB | solver RSS MB | certified |
|---|---|---|---|---|---|---|---|---|---|---|
| P2_3-8 | P2 | Q | 8000 | UNSATISFIABLE | 780.05 | 60.5 | 357.7 | 4.04 | 4388 | true |
| P1_2-8 | P1 | Q | 8000 | UNSATISFIABLE | 981.74 | 68.5 | 384.2 | 4.19 | 4381 | true |
| P1_8-10 | P1 | Q | 8000 | UNSATISFIABLE | 387.52 | 51.6 | 293.8 | 3.32 | 4378 | true |
| P1_2-3-12 | P1 | H | 2400 | UNSATISFIABLE | 269.8 | 49.5 | 309.2 | 3.35 | 4412 | true |
| P1_2-8-12 | P1 | H | 2400 | UNSATISFIABLE | 347.49 | 55.2 | 315.4 | 3.40 | 4398 | true |
| P1_3-6-9 | P1 | H | 2400 | UNSATISFIABLE | 28.07 | 14.3 | 114.4 | 0.22 | 2651 | true |
| P1_4-6-10 | P1 | H | 2400 | UNSATISFIABLE | 23.63 | 12.7 | 116.5 | 0.22 | 2648 | true |
| P1_5-9-13 | P1 | H | 2400 | UNSATISFIABLE | 189.54 | 49.0 | 275.7 | 3.07 | 4321 | true |
| P3_5-7 | P3 | Q | 8000 | UNSATISFIABLE | 444.37 | 54.5 | 303.4 | 3.46 | 4372 | true |
| P3_1-5-8 | P3 | H | 2400 | UNSATISFIABLE | 255.89 | 49.8 | 306.0 | 3.34 | 4403 | true |
| P3_1-10-12 | P3 | H | 2400 | UNSATISFIABLE | 279.31 | 49.7 | 303.2 | 3.29 | 4365 | true |
| P3_4-7-11 | P3 | H | 2400 | UNSATISFIABLE | 87.7 | 24.7 | 167.8 | 1.23 | 3184 | true |
| P3_5-6-14 | P3 | H | 2400 | UNSATISFIABLE | 253.2 | 48.3 | 286.3 | 3.22 | 4396 | true |
| P3_6-8-12 | P3 | H | 2400 | UNSATISFIABLE | 18.09 | 11.7 | 106.4 | 0.21 | 2376 | true |

## Resources and anomalies
- Largest solver RSS: 4412 MB (P1_2-3-12); cake_lpr ran with an 8000 MB heap. No memory problem.
- No SAT, no proof rejection, no ERROR or uncertified record.
- Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (14 records), `lane.log.tail`.
