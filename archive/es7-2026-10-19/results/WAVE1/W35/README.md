# WAVE1 / W35: mirror sub-case (ii), "cases" entry (66 hull cases)

The run went on one cloud VM (4 cores, 15 GB, Linux 6.18; see env.txt). It started at 07:00 UTC 2026-10-20, and no new solver call started after 10:28 UTC.

## Result
**13 of 66 cases are closed, 1 is partly done, and 52 were not started. No case gave SAT.** The closed cases are U7_L6, U_L2-3, U_L2-6, U_L2-10, U_L2-13, U3-4_L, U3-7_L, U3-10_L, U3-13_L, U_L4-5, U4-7_L, U_L4-8 and U4-10_L. U4-12_L is the partial case: 64 of its 116 top cubes are closed and 52 are open.
Each case was closed with cake_lpr (`s VERIFIED UNSAT` on every leaf), and `results/Mii-S/scripts/covercheck.py` reports `s COVERED` for the case's `leaves.icnf`.
No UNSAT failed cake_lpr (0 `UNSAT_UNCHECKED`). drat-trim lrat-check was not used.

## Tools (tools.txt)
- CaDiCaL c60730422e758ef1cebe7aeddf2dda31c996bf04 (3.0.1).
- march_cu from CnC 705b60c6. It was built with the Makefile flags plus -fcommon.
- cake_lpr a36874a8, built with `make cake_lpr`. The bundled example prints `s VERIFIED UNSAT`.

## sha256 checks
- Regenerated base `m33k7int.sub.cnf` = 69c1dc8f…932d: OK.
- `verify/ii_wave1.json` = 6df36dab…c72e: OK.
- All 66 case CNFs built with `hullsplit.py case` match the entry and cases.jsonl: 0 mismatches (case_sha256_check.txt).
- Each case's `leaves.jsonl` also records its case sha256 in the top or whole record.

## Method (scripts/close_march_w35.py; the original close_march.py is copied unchanged next to it)
- **Order.** Cases ran in the listed order. A single pool of 4 workers ran them, prioritized by case index; later cases only took cores the earlier ones left idle.
- **Whole case.** Each case first got `cadical --lrat -t 60` on the whole case. An UNSAT counted only after cake_lpr verified it. Such a case is recorded as `"whole": true` with its case sha256, and its `leaves.icnf` is `a 0`. U_L4-5 and U_L4-8 closed this way.
- **Otherwise, close_march.** The rest went through the close_march recipe:
  - `march_cu -d 7` top cubes, saved as `top.icnf` with its sha256 in the top record;
  - `cadical -t 300` with cake_lpr on every UNSAT;
  - `march_cu -d 6` splits on timeout, with the children listed in the SPLIT record.
- **Resuming.** State is rebuilt from `leaves.jsonl` + `top.icnf`, and a cube with no final record is queued again. To continue, run the same command with a later `--deadline`.
- **Files.** `leaves.icnf` holds the verified leaves only. `open.icnf` holds the cubes that are still open (`a 0` = whole case).
- **Incident.** About 10 minutes into the run, a `git pull --rebase` replaced the tracked `leaves.jsonl` files under the running driver. The records were recovered from the driver's open file descriptors before it was stopped. The driver then restarted with its state outside the repository, and the state is copied in before each commit. No record was lost; solver calls that were running when it stopped (a few minutes of CPU) were redone.

## Per case (summary.jsonl)
| case | status | whole 60 s | top cubes (refuted) | splits | cake_lpr-verified leaves | open cubes | covercheck | CPU s |
|---|---|---|---|---|---|---|---|---|
| U7_L6 | CLOSED | TIMEOUT | 108 (12) | 0 | 108 | 0 | s COVERED 108 | 1087 |
| U_L2-3 | CLOSED | TIMEOUT | 128 (0) | 6 | 500 | 0 | s COVERED 500 | 15178 |
| U_L2-6 | CLOSED | TIMEOUT | 127 (1) | 4 | 367 | 0 | s COVERED 367 | 8177 |
| U_L2-10 | CLOSED | TIMEOUT | 122 (4) | 0 | 122 | 0 | s COVERED 122 | 2254 |
| U_L2-13 | CLOSED | TIMEOUT | 128 (0) | 0 | 128 | 0 | s COVERED 128 | 2020 |
| U3-4_L | CLOSED | TIMEOUT | 128 (0) | 3 | 306 | 0 | s COVERED 306 | 9000 |
| U3-7_L | CLOSED | TIMEOUT | 119 (7) | 0 | 119 | 0 | s COVERED 119 | 2793 |
| U3-10_L | CLOSED | TIMEOUT | 128 (0) | 0 | 128 | 0 | s COVERED 128 | 2189 |
| U3-13_L | CLOSED | TIMEOUT | 128 (0) | 0 | 128 | 0 | s COVERED 128 | 2065 |
| U_L4-5 | CLOSED | UNSAT | None (None) | 0 | 0 | 0 | s COVERED 1 | 60 |
| U4-7_L | CLOSED | TIMEOUT | 128 (0) | 0 | 128 | 0 | s COVERED 128 | 1405 |
| U_L4-8 | CLOSED | UNSAT | None (None) | 0 | 0 | 0 | s COVERED 1 | 47 |
| U4-10_L | CLOSED | TIMEOUT | 104 (22) | 0 | 104 | 0 | s COVERED 104 | 1380 |
| U4-12_L | OPEN | TIMEOUT | 116 (10) | 0 | 64 | 52 | s NOT COVERED 64 | 996 |

Not started (52): U4-14_L, U_L4-15, U5-7_L, U_L5-8, U5-10_L, U5-12_L, U5-14_L, U5-16_L, U6-9_L, U6-14_L, U3_L4, U3_L8, U3_L12, U3_L16, U4_L7, U4_L12, U4_L16, U5_L7, U5_L13, U6_L5, U6_L10, U6_L16, U7_L8, U7_L12, U8_L2, U8_L10, U8_L15, U9_L8, U9_L15, U10_L5, U10_L11, U10_L15, U11_L5, U11_L10, U11_L15, U12_L6, U12_L16, U13_L6, U13_L10, U14_L7, U14_L11, U15_L7, U16_L2, U16_L8, U9_L5, U_L2-15, U9_L11, U8_L9, U8_L14, U16_L4, U3-16_L, U9_L10

CLOSED 13, OPEN 1, NOT_STARTED 52, SAT 0, total CPU s 48651

CPU s is the sum over the case's records of solve, check, split and march wall time (each runs single-threaded).

## Open work
- U4-12_L: `U4-12_L/open.icnf` lists 52 cubes. Together with `leaves.icnf` they cover the case (`s COVERED 116`).
- 52 cases were not started; each has `open.icnf` = `a 0`.
- The pace here was about 1,000 to 15,000 CPU s per case (U_L2-3: 15.2k s; most 6-gon cases: 1.4k to 2.8k s). The whole entry is therefore well above its 10.1 core-hour estimate.
