# C2P5 M65: list C2P5B.tsv, shard j = 15 of N = 50, H = 5.25 h (task commit 81cb025f)

## Tools and checks (`tools.txt`)
- Tools built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check with the E2 patch (2e3b2dc).
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf (b0061e90…) and base.json (2476faff…) match.
- Cubes P1..P8 from `C2C34/l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, 19 rows with idx ≡ 15 mod 50)
Lane started 15:27:11Z, END 20:27:11Z (`run.sh`); the lane finished all units at 19:56:54Z.

| case | kind | units | certified | timed out | not reached | errors |
|---|---|---|---|---|---|---|
| P2 | Q | 1 | 1 | 0 | 0 | 0 |
| P2 | H | 6 | 6 | 0 | 0 | 0 |
| P1 | Q | 1 | 1 | 0 | 0 | 0 |
| P1 | H | 5 | 5 | 0 | 0 | 0 |
| P3 | Q | 1 | 1 | 0 | 0 | 0 |
| P3 | H | 5 | 5 | 0 | 0 | 0 |
| **total** | | **19** | **19** | **0** | **0** | **0** |

Every unit is UNSATISFIABLE, and both lrat-check (`c VERIFIED`) and cake_lpr (`s VERIFIED UNSAT`) accepted every proof. The certified units are P2_3-12, P1_2-12 and P3_5-11 (Q), and P2_1-3-7, P2_1-7-9, P2_3-6-14, P2_3-12-15, P2_4-9-10, P2_5-9-11, P1_2-3-16, P1_2-8-16, P1_3-6-13, P1_4-6-14, P1_6-7-8, P3_1-5-12, P3_1-10-16, P3_4-7-15, P3_5-7-10 and P3_6-9-11 (H).

Certified units (min / median / max):

| | solve s | lrat-check s | cake_lpr s | proof GB |
|---|---|---|---|---|
| Q (3) | 1699.9 / 1721.7 / 1833.4 | 84.0 / 86.9 / 87.2 | 443.6 / 480.2 / 509.6 | 5.16 / 5.21 / 5.36 |
| H (16) | 19.9 / 292.7 / 460.3 | 13.3 / 58.0 / 63.6 | 102.2 / 326.4 / 360.0 | 0.22 / 3.34 / 3.67 |
| all (19) | 19.9 / 363.2 / 1833.4 | 13.3 / 59.2 / 87.2 | 102.2 / 330.1 / 509.6 | 0.22 / 3.47 / 5.36 |

Per-unit numbers are in `out.jsonl`.

## Memory and anomalies
- The largest solver RSS was 4438.7 MB (P2_1-3-7). There were no memory problems on 15 GB.
- There was no SAT, no proof rejection and no ERROR status.
