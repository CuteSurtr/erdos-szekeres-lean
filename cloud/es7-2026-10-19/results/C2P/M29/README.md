# C2P M29 (LIST = C2P.tsv, j = 29, N = 42, H = 3.0, Z = 01909a07)

Restart of the earlier attempt that stopped at step 1 (the files from that attempt were replaced). Start 2026-10-31 03:22:44 UTC; lane END 06:07:44 UTC; the lane finished at 05:57:59 UTC (584 s left, too few for the next unit).

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check from drat-trim 2e3b2dc with the E2 patch. Nothing was cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, and both sha256 values match (base.cnf `b0061e90…`, base.json `2476faff…`).
- Cubes P1..P8: all 8 are byte-identical to `C2P/cubes/`.

## Units (`units.tsv`: 53 = 41 H + 12 Q, no cover)
| | certified | UNKNOWN | errors | not reached |
|---|---|---|---|---|
| P8 (3 H, 2 Q) | 3 H, 2 Q | 0 | 0 | 0 |
| P7 (5 H, 2 Q) | 5 H, 1 Q | 0 | 0 | 1 Q |
| P1 (6 H, 1 Q) | 0 | 0 | 0 | 6 H, 1 Q |
| P2 (6 H, 1 Q) | 0 | 0 | 0 | 6 H, 1 Q |
| P3 (5 H, 2 Q) | 0 | 0 | 0 | 5 H, 2 Q |
| P4 (5 H, 1 Q) | 0 | 0 | 0 | 5 H, 1 Q |
| P5 (5 H, 2 Q) | 0 | 0 | 0 | 5 H, 2 Q |
| P6 (6 H, 1 Q) | 0 | 0 | 0 | 6 H, 1 Q |
| **total** | **11** (8 H, 3 Q) | 0 | 0 | 42 (33 H, 9 Q) |

Certified: P8_9-10-15, P8_11-13, P8_3-4-16, P8_4-9-12, P8_3-15, P7_3-12-14, P7_1-16, P7_3-11-16, P7_1-10-12, P7_2-9-15, P7_2-12-16. Each was UNSATISFIABLE, with `c VERIFIED` from lrat-check and `s VERIFIED UNSAT` from cake_lpr.

Not reached: P7_2-15 P6_3-7-14 P6_3-7-16 P6_7-14-15 P6_1-16 P6_1-2-12 P6_2-7-9 P6_9-10-14 P5_9-13 P5_2-11-15 P5_1-9-13 P5_7-11-12 P5_2-10-13 P5_7-10 P5_6-7-13 P4_5-11-13 P4_6-9-13 P4_6-15 P4_6-10-15 P4_5-10-12 P4_8-9-12 P3_4-6 P3_1-8-14 P3_1-5-6 P3_5-10-14 P3_6-7-8 P3_5-8 P3_1-2-4 P2_5-9-11 P2_3-6-14 P2_4-10 P2_1-7-11 P2_1-4-10 P2_6-9-11 P2_3-8-9 P1_2-11-14 P1_5-6-7 P1_3-9-12 P1_3-7-14 P1_6-12 P1_4-6-12 P1_2-3-13 

For the certified units (min / median / max):
- solve: 78.2 / 343.6 / 1501.2 s. The H units took 78–422 s; the Q units took 539, 1050 and 1501 s.
- lrat-check: 22.7 / 47.9 / 72.3 s
- cake_lpr: 148.3 / 282.3 / 407.5 s
- proof size: 1.21 / 3.41 / 5.26 GB. The proofs were deleted after checking.

The largest solver RSS was 4471 MB (P8_11-13), well under the 15 GB of RAM.

## SAT, rejection, memory
No SAT, no proof rejection, no errors and no memory problem.
