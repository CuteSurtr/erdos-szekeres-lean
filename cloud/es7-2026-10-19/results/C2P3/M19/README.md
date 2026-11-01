# C2P3 M19 (LIST = C2P3.tsv, j = 19, N = 50, H = 2.5, task commit 4f653319)

## Tools and checks
- `C2P/vendor/build_tools.sh`: vendored sources (manifest: all 196 files match), CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example `s VERIFIED UNSAT`. Nothing was cloned or downloaded.
- Base CNF: header `p cnf 838032 16653336`, sha256 base.cnf `b0061e90…d8ff1`, base.json `2476faff…2b48` (both match).
- Cubes P1..P8 from `l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details in `tools.txt`; machine in `env.txt` (4 cores, 15 GB).

## Run
Lane started 09:45:59Z with END = 1793447866 (11:57:46Z = start 09:42:46Z + 2.5 h − 15 min); see `run.sh`. It stopped at 11:49:05Z with 520 s left (below the 15-minute start minimum).

## Units (10 assigned)
- Certified: **5** (P6 Q: 1, P6 H: 3, P5 H: 1).
- Timed out (UNKNOWN): 0.
- Errors / `certified: false`: 0.
- Not reached: **5**, all P5 H: P5_1-11-13, P5_2-8-11, P5_6-7-15, P5_7-8-15, P5_9-11-12.

| unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB | certified |
|---|---|---|---|---|---|---|---|---|---|---|
| P6_2-11 | P6 | Q | 6000 | UNSATISFIABLE | 4260.67 | 100.1 | 616.4 | 7.31 | 4412 | True |
| P6_1-12-13 | P6 | H | 1800 | UNSATISFIABLE | 305.07 | 47.4 | 296.4 | 3.26 | 4359 | True |
| P6_3-8-11 | P6 | H | 1603 | UNSATISFIABLE | 413.08 | 46.7 | 291.8 | 3.41 | 4366 | True |
| P6_8-10-12 | P6 | H | 840 | UNSATISFIABLE | 25.22 | 11.0 | 109.6 | 0.22 | 2646 | True |
| P5_1-4-9 | P5 | H | 692 | UNSATISFIABLE | 411.23 | 47.0 | 301.8 | 3.37 | 4364 | True |

Certified units, min / median / max: solve 25.2 / 411.2 / 4260.7 s; lrat-check 11.0 / 47.0 / 100.1 s; cake_lpr 109.6 / 296.4 / 616.4 s; proof 0.2 / 3.4 / 7.3 GB.

The caps below the list values (1603, 840, 692) come from lane.py limiting each solve to the time left minus the 10-minute check reserve. Every unit solved well within its cap.

## Largest solver RSS
4412 MB (P6_2-11). No memory problems. Peak disk use was about 19 GB of 39 GB, during the 7.3 GB proof of P6_2-11.

## SAT / rejections
No SAT, no proof rejection, no errors.
