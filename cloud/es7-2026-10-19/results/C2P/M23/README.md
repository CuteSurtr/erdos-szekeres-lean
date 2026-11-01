# C2P / M23 (LIST C2P.tsv, shard 23 of 42, H = 3.0, Z = 01909a07)

Replaces the earlier attempt (TASK at fb2c59af), which stopped at step 1 because the tool build was refused.

**Result: 13 of 53 units certified UNSAT, 1 timed out (UNKNOWN), 39 not reached. No SAT, no proof rejection,
no error, no memory problem.**

## Tools and checks (`tools.txt`)

- `C2P/vendor/build_tools.sh` from the vendored sources (manifest: all 196 files match; nothing cloned or
  downloaded): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
  Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf and base.json both match.
- Cubes: P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Run

One lane (`run.sh`), started 2026-10-31 03:25 UTC (session start 03:22:56, END = 06:07:56 UTC); the lane
stopped at 05:57:59 with 596 s left before END (fewer than 15 min, so no further unit was started).
Records: `out.jsonl`; log tail: `lane.log.tail`.

## Units by case and kind

| case | kind | units | certified | UNKNOWN | errors | not reached |
|---|---|---|---|---|---|---|
| P8 | H | 4 | 4 | 0 | 0 | 0 |
| P8 | Q | 1 | 1 | 0 | 0 | 0 |
| P7 | H | 6 | 6 | 0 | 0 | 0 |
| P7 | Q | 1 | 1 | 0 | 0 | 0 |
| P6 | H | 5 | 1 | 0 | 0 | 4 |
| P6 | Q | 2 | 0 | 1 | 0 | 1 |
| P5 | H | 6 | 0 | 0 | 0 | 6 |
| P5 | Q | 1 | 0 | 0 | 0 | 1 |
| P4 | H | 5 | 0 | 0 | 0 | 5 |
| P4 | Q | 2 | 0 | 0 | 0 | 2 |
| P3 | H | 5 | 0 | 0 | 0 | 5 |
| P3 | Q | 1 | 0 | 0 | 0 | 1 |
| P2 | H | 5 | 0 | 0 | 0 | 5 |
| P2 | Q | 2 | 0 | 0 | 0 | 2 |
| P1 | H | 6 | 0 | 0 | 0 | 6 |
| P1 | Q | 1 | 0 | 0 | 0 | 1 |
| **all** | | **53** | **13** | **1** | **0** | **39** |

Certified units (13), minimum / median / maximum:

- solve: 70.6 / 236.0 / 776.0 s
- lrat-check: 23.8 / 52.0 / 62.4 s
- cake_lpr: 161.0 / 302.9 / 350.1 s (heap [8000] MB)
- proof size: 1.11 / 3.19 / 3.88 GB

Largest solver RSS: 4412 MB (P8_2-10-12).

Per unit (in run order):

| unit | kind | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|
| P8_2-10-12 | H | UNSATISFIABLE (certified) | 355.8 | 54.4 | 313.8 | 3.32 | 4412 |
| P8_2-4-6 | H | UNSATISFIABLE (certified) | 70.6 | 23.8 | 161.0 | 1.11 | 3158 |
| P8_10-11 | Q | UNSATISFIABLE (certified) | 612.4 | 59.9 | 338.1 | 3.67 | 4394 |
| P8_3-9-12 | H | UNSATISFIABLE (certified) | 412.5 | 57.6 | 331.7 | 3.44 | 4398 |
| P8_1-5-6 | H | UNSATISFIABLE (certified) | 73.6 | 24.5 | 164.3 | 1.11 | 3169 |
| P7_2-3-13 | H | UNSATISFIABLE (certified) | 322.1 | 53.8 | 308.2 | 3.27 | 4359 |
| P7_8-10-14 | H | UNSATISFIABLE (certified) | 111.1 | 31.4 | 195.0 | 1.62 | 3423 |
| P7_2-4-13 | H | UNSATISFIABLE (certified) | 309.5 | 53.1 | 311.6 | 3.29 | 4361 |
| P7_3-14-15 | H | UNSATISFIABLE (certified) | 236.0 | 52.0 | 302.9 | 3.19 | 4355 |
| P7_8-11 | Q | UNSATISFIABLE (certified) | 776.0 | 62.4 | 350.1 | 3.88 | 4394 |
| P7_1-15-16 | H | UNSATISFIABLE (certified) | 203.6 | 50.8 | 291.9 | 3.15 | 4392 |
| P7_9-10-15 | H | UNSATISFIABLE (certified) | 184.5 | 49.9 | 287.6 | 3.06 | 4395 |
| P6_9-10-13 | H | UNSATISFIABLE (certified) | 75.3 | 25.3 | 163.2 | 1.13 | 3147 |
| P6_3-11 | Q | UNKNOWN | 1171.0 | – | – | – | 4372 |

Not reached (39): P6_7-8-10, P6_7-11-12, P6_2-3-15, P6_1-14-16, P6_7-16, P5_2-3-7, P5_1-9-15, P5_1-2-16, P5_1-15, P5_1-6-16, P5_1-11-14, P5_8-10-13, P4_1-12, P4_6-11-12, P4_1-8-13, P4_5-6-13, P4_6-9-10, P4_8-12, P4_1-6-12, P3_7-9-13, P3_7-10-13, P3_5-13, P3_1-9-11, P3_1-7-11, P3_4-7-14, P2_9-10, P2_5-7-8, P2_3-4-14, P2_1-3-13, P2_3-6-9, P2_3-15, P2_1-5-7, P1_3-6-9, P1_2-6-12, P1_2-3, P1_3-6-12, P1_2-7-11, P1_2-7-9, P1_5-8-10

Notes:
- P6_3-11 (Q, list cap 2400 s) ran with the lane's reduced cap of 1181 s (time left before END − 600 s) and
  timed out at that cap; it is open, not a failure. No record has `"certified": false` or an `ERROR` status.
- All cake_lpr runs passed with the 8000 MB heap; no retry at 11000 MB was needed.
- Peak solver RSS 4.4 GB, far below the 15 GB of the machine. No SAT_FOUND file appeared.
