# C2P / M13 (LIST C2P.tsv, shard 13 of 42, H = 3.0, Z = 01909a07)

Restart of M13; the earlier attempt (at fb2c59af) stopped at step 1 and its files were replaced.

**Result: 8 units certified, 2 timed out (UNKNOWN), 43 not reached, no errors. No SAT, no proof rejection, no memory problem.**

## Tools and checks (`tools.txt`)

- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (nothing cloned or downloaded): manifest all 196
  files match; CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity: cake_lpr example `s VERIFIED UNSAT`; both checkers reject the bad LRAT and accept the good one.
- Base CNF: header `p cnf 838032 16653336`, sha256 of base.cnf and base.json both match.
- Cubes: P1..P8 all byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Lane: one lane (`run.sh`), started 03:26:15Z, END 06:08:36Z; it stopped at 05:58:39Z with 596 s left (< 15 min).

## Units (53: P1 6, P2–P7 7 each, P8 5; 43 H, 10 Q, no cover)

| case | kind | units | certified | UNKNOWN | not reached | error/uncertified | SAT |
|---|---|---|---|---|---|---|---|
| P8 | H | 4 | 4 | 0 | 0 | 0 | 0 |
| P8 | Q | 1 | 0 | 1 | 0 | 0 | 0 |
| P7 | H | 6 | 4 | 0 | 2 | 0 | 0 |
| P7 | Q | 1 | 0 | 1 | 0 | 0 | 0 |
| P6 | H | 5 | 0 | 0 | 5 | 0 | 0 |
| P6 | Q | 2 | 0 | 0 | 2 | 0 | 0 |
| P5 | H | 6 | 0 | 0 | 6 | 0 | 0 |
| P5 | Q | 1 | 0 | 0 | 1 | 0 | 0 |
| P4 | H | 5 | 0 | 0 | 5 | 0 | 0 |
| P4 | Q | 2 | 0 | 0 | 2 | 0 | 0 |
| P3 | H | 6 | 0 | 0 | 6 | 0 | 0 |
| P3 | Q | 1 | 0 | 0 | 1 | 0 | 0 |
| P2 | H | 6 | 0 | 0 | 6 | 0 | 0 |
| P2 | Q | 1 | 0 | 0 | 1 | 0 | 0 |
| P1 | H | 5 | 0 | 0 | 5 | 0 | 0 |
| P1 | Q | 1 | 0 | 0 | 1 | 0 | 0 |
| all | | 53 | 8 | 2 | 43 | 0 | 0 |

Certified units (8), min / median / max:
- solve s: 236.9 / 359.9 / 586.8
- lrat-check s: 47.0 / 55.7 / 68.7
- cake_lpr s: 278.5 / 319.6 / 391.1
- proof size GB: 3.22 / 3.38 / 3.75
- cake_lpr heap MB used: 8000

Largest solver RSS: 4403 MB (P8_1-4-15).

Per unit:

| unit | kind | status | cap s | solve s | proof GB | lrat-check s | cake_lpr s | certified |
|---|---|---|---|---|---|---|---|---|
| P8_1-4-15 | H | UNSATISFIABLE | 1800 | 236.89 | 3.22 | 47.0 | 278.5 | True |
| P8_1-5-14 | H | UNSATISFIABLE | 1800 | 397.61 | 3.48 | 68.7 | 391.1 | True |
| P8_4-10 | Q | UNKNOWN | 2400 | 2380.08 | - | - | - | - |
| P8_4-12-13 | H | UNSATISFIABLE | 1800 | 307.34 | 3.27 | 54.4 | 307.1 | True |
| P8_3-11-14 | H | UNSATISFIABLE | 1800 | 370.87 | 3.38 | 55.8 | 325.5 | True |
| P7_3-11-14 | H | UNSATISFIABLE | 1800 | 361.23 | 3.39 | 55.4 | 319.5 | True |
| P7_2-10-11 | H | UNSATISFIABLE | 1800 | 299.69 | 3.26 | 55.6 | 309.6 | True |
| P7_3-8-14 | H | UNSATISFIABLE | 1800 | 586.79 | 3.75 | 61.4 | 350.8 | True |
| P7_1-10-14 | H | UNSATISFIABLE | 1405 | 358.51 | 3.40 | 57.2 | 319.7 | True |
| P7_9-13 | Q | UNKNOWN | 658 | 652.33 | - | - | - | - |

Uncertified/error records: none

Notes:
- P8_4-10 (Q) timed out at its full 2400 s cap.
- P7_9-13 (Q) was started with the cap shortened by the lane to 658 s (END − 10 min reserve) and timed out; it was not
  tried at its full 2400 s cap, so it should be counted as not finished rather than as hard.
- Not reached (43): every unit after P7_9-13 in `units.tsv` order (P7_1-12-15 onward).
- Solver RSS was 4.36–4.40 GB for every unit; cake_lpr ran with an 8000 MB heap (≈8.2 GB RSS) and never needed the
  11000 MB retry. No OOM or memory problem.
- No SAT_FOUND, no `"certified": false` record, no ERROR status.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (one record per unit), `lane.log.tail`.
