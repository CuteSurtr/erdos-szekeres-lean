# C2P5 M91: list C2P5B.tsv, shard 41 of 50

Task: `results/C2P5/TASK.md` at 81cb025f, with V = M91, LIST = C2P5B.tsv, j = 41, N = 50, H = 5.25.
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-31 15:11:47 UTC, END 20:11:47 UTC; the lane finished all units at 19:12:45 UTC.

## Tools and checks (`tools.txt`)

- Built by `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match):
  CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1`, base.json `2476faff…2b48`, both as expected.
- Cubes: P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units: 18, all certified

| case | kind | units | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|---|
| P2 | Q | 1 | 1 | 0 | 0 | 0 |
| P2 | H | 6 | 6 | 0 | 0 | 0 |
| P1 | Q | 1 | 1 | 0 | 0 | 0 |
| P1 | H | 4 | 4 | 0 | 0 | 0 |
| P3 | Q | 1 | 1 | 0 | 0 | 0 |
| P3 | H | 5 | 5 | 0 | 0 | 0 |
| total | | 18 | 18 | 0 | 0 | 0 |

Every record is UNSATISFIABLE with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.

Certified units (min / median / max):
- solve: 18.6 / 251.3 / 2400.4 s (total 8250 s)
- lrat-check: 13.2 / 54.6 / 99.5 s
- cake_lpr: 112.4 / 314.9 / 539.2 s
- proof size: 0.22 / 3.25 / 5.71 GB

| unit | case | kind | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|
| P2_6-8 | P2 | Q | 432.2 | 60.4 | 320.7 | 3.28 | 4413 |
| P1_4-14 | P1 | Q | 2156.3 | 99.5 | 539.2 | 5.71 | 4438 |
| P2_1-5-11 | P2 | H | 472.3 | 60.3 | 372.4 | 3.56 | 4409 |
| P2_3-5-12 | P2 | H | 279.9 | 55.8 | 334.2 | 3.26 | 4366 |
| P2_3-9-16 | P2 | H | 522.5 | 62.3 | 365.7 | 3.68 | 4383 |
| P2_4-7-11 | P2 | H | 101.5 | 31.6 | 182.7 | 1.26 | 3132 |
| P2_5-7-10 | P2 | H | 25.5 | 13.2 | 122.1 | 0.22 | 2649 |
| P2_6-10-12 | P2 | H | 18.6 | 14.1 | 118.1 | 0.22 | 2359 |
| P1_2-6-9 | P1 | H | 99.1 | 27.7 | 176.3 | 1.25 | 3229 |
| P1_3-4-8 | P1 | H | 25.0 | 14.0 | 116.3 | 0.22 | 2653 |
| P1_3-10-13 | P1 | H | 289.3 | 59.9 | 328.9 | 3.27 | 4370 |
| P1_5-6-8 | P1 | H | 27.1 | 13.6 | 112.4 | 0.22 | 2663 |
| P3_1-10 | P3 | Q | 2400.4 | 90.7 | 504.4 | 5.68 | 4376 |
| P3_1-2-5 | P3 | H | 222.6 | 53.3 | 309.1 | 3.25 | 4370 |
| P3_1-7-13 | P3 | H | 551.8 | 61.0 | 374.9 | 3.68 | 4377 |
| P3_4-5-10 | P3 | H | 75.9 | 26.2 | 169.1 | 1.12 | 3174 |
| P3_4-10-14 | P3 | H | 467.2 | 61.7 | 366.2 | 3.49 | 4390 |
| P3_5-10-12 | P3 | H | 82.6 | 26.4 | 165.6 | 1.12 | 3126 |

Largest solver RSS: 4438 MB (P1_4-14).

## Problems

- No SAT, no proof rejection, no error record, and no memory problem.
- Operational note (see `run.sh`): my first launch at 15:14:32 UTC mistakenly started two lane instances, which raced on
  the same unit files. Both were killed within a minute, before either wrote a record. I then deleted the unit
  files and lane.log, re-checked the base.cnf sha256 and started exactly one lane at 15:15:05 UTC. All 18 records
  come from that single lane.
