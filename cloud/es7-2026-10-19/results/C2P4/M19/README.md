# C2P4 M19 (LIST = C2P4.tsv, j = 19, N = 50, H = 2.5, Z = a46b478d)

Start 2026-10-31 13:02:04 UTC (epoch 1793451724), END 1793459824 (15:17:04 UTC). One lane (`run.sh`); it stopped at 15:07:08 with 595 s left before END.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: manifest all 196 files match; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch) built from the vendored sources only. Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`); cake_lpr example `s VERIFIED UNSAT`.
- Base CNF `zcnf.py rot 17 7 --m 2 --hull`: header `p cnf 838032 16653336`, sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…f2b48`, both as expected.
- Cubes P1..P8 from `l2cubes.py`: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (14)
| unit | case | kind | status | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|---|
| P5_1-13 | P5 | Q | certified UNSAT | 1926.73 | 85.0 | 603.8 | 5275703310 | 4376 |
| P6_2-4-7 | P6 | H | certified UNSAT | 205.47 | 50.0 | 282.3 | 3188374232 | 4401 |
| P5_1-9-13 | P5 | H | certified UNSAT | 383.90 | 58.4 | 331.3 | 3439527953 | 4352 |
| P5_2-8-13 | P5 | H | certified UNSAT | 494.33 | 56.1 | 329.1 | 3661699479 | 4366 |
| P5_6-8-16 | P5 | H | certified UNSAT | 339.77 | 54.8 | 331.3 | 3418942069 | 4398 |
| P5_7-10-12 | P5 | H | certified UNSAT | 28.67 | 16.5 | 114.8 | 215976979 | 2661 |
| P4_1-8 | P4 | Q | UNKNOWN (timed out at the END-shortened cap 1562 s, not 6000) | 1545.75 | – | – | – | 4385 |
| P4_10-11, P3_4-14 | P4, P3 | Q | not reached | | | | | |
| P3_1-4-15, P3_1-9-14, P3_4-6-16, P3_5-6-10, P3_6-7-14 | P3 | H | not reached | | | | | |

Counts by case and kind:
- Certified (6): P5 Q 1, P5 H 4, P6 H 1.
- Timed out (1): P4 Q 1 (P4_1-8; cap reduced by the lane to 1562 s because of END, so it did not get its full 6000 s).
- Not reached (7): P4 Q 1 (P4_10-11), P3 Q 1 (P3_4-14), P3 H 5.
- Errors: none.

Certified units (6): solve s min 28.67 / median 361.84 / max 1926.73; lrat-check s 16.5 / 55.45 / 85.0; cake_lpr s 114.8 / 330.2 / 603.8; proof bytes 215976979 / 3429235011 / 5275703310.

Largest solver RSS: 4401 MB (P6_2-4-7); the machine (15 GB, 4 cores) had no memory problem.

No SAT, no proof rejection, no `certified: false` record, no ERROR status, no memory problem.
