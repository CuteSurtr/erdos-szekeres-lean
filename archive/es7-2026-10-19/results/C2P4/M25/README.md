# C2P4 M25

Shard j = 25 of N = 50 of `lists/C2P4.tsv`, budget H = 2.5 h, task commit a46b478d. One lane, started 13:04:03Z on
2026-10-31, END = 1793459804 (15:16:44Z); the lane stopped at 15:08:32Z (491 s left, no unit startable).

## Tools and checks
- `vendor/build_tools.sh` built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, E2 patch) from
  the vendored sources; manifest: all 196 files match. Sanity: the bad LRAT is rejected by both checkers, the good one
  accepted by both; the cake_lpr example prints `s VERIFIED UNSAT`. Nothing was cloned or downloaded.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf and base.json match the expected values.
- Cubes P1..P8 from `l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details in `tools.txt`; machine in `env.txt` (4 cores, 15 GB).

## Units (19 in `units.tsv`)

| | certified | timed out (UNKNOWN) | not reached | errors |
|---|---|---|---|---|
| P5 Q | 1 (P5_2-14) | 0 | 0 | 0 |
| P5 H | 4 (P5_1-11-13, P5_2-10-11, P5_6-9-16, P5_7-11-15) | 0 | 0 | 0 |
| P6 H | 1 (P6_3-10-12) | 0 | 0 | 0 |
| P4 Q | 1 (P4_1-14, cap cut to 1911 s by END, solved in 1447 s) | 0 | 0 | 0 |
| P4 H | 0 | 0 | 6 | 0 |
| P3 Q | 0 | 0 | 1 | 0 |
| P3 H | 0 | 0 | 5 | 0 |
| **total** | **7** | **0** | **12** | **0** |

Not reached: P4_1-2-9, P4_1-8-9, P4_2-5-14, P4_5-7-14, P4_6-8-11, P4_9-10-11, P3_7-12, P3_1-7-10, P3_4-5-7,
P3_4-10-11, P3_5-9-14, P3_7-9-11.

Certified units (all UNSAT, lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`, heap 8000 MB):

| unit | kind | solve s | lrat-check s | cake_lpr s | proof bytes |
|---|---|---|---|---|---|
| P5_2-14 | Q | 1567.6 | 80.6 | 440.5 | 5102707808 |
| P6_3-10-12 | H | 304.5 | 52.7 | 309.8 | 3291838962 |
| P5_1-11-13 | H | 241.2 | 51.9 | 301.4 | 3217888985 |
| P5_2-10-11 | H | 278.0 | 54.8 | 316.5 | 3249001441 |
| P5_6-9-16 | H | 389.5 | 56.2 | 325.3 | 3440593572 |
| P5_7-11-15 | H | 240.8 | 52.2 | 303.7 | 3201059997 |
| P4_1-14 | Q | 1446.7 | 83.5 | 465.7 | 4997634510 |

min / median / max: solve 240.8 / 304.5 / 1567.6 s; lrat-check 51.9 / 54.8 / 83.5 s; cake_lpr 301.4 / 316.5 / 465.7 s;
proof 3.20 / 3.29 / 5.10 GB (all proofs deleted after checking).

## Resources and problems
- Largest solver RSS: 4405 MB (P5_1-11-13). cake_lpr peaked at about 8.2 GB RSS; no memory problem.
- No SAT, no proof rejection, no ERROR record, no timeout.
- Pushes: one early progress commit went to the fallback branch `es7-fallback-c2p4-m25` during push contention; all
  later pushes went to `es7-cloud`.
