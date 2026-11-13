# C2P4 M37 (LIST = C2P4.tsv, j = 37, N = 50, H = 2.5, TASK commit a46b478d)

Machine: 4 cores, 15 GB RAM (env.txt). Start 13:02 UTC, lane 13:05:45–15:10:10 UTC, END = 1793459825 (15:17:05 UTC).

## Tools and checks (tools.txt)
- Built by `C2P/vendor/build_tools.sh` from the vendored sources: manifest all 196 files match; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Nothing cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF header `p cnf 838032 16653336`; sha256 base.cnf b0061e90…d8ff1 and base.json 2476faff…f2b48, both as required.
- Cubes P1..P8 from `C2C34/l2cubes.py` byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units
Units: 19; records: 10; certified UNSAT: 10; UNKNOWN: 0; errors/uncertified: 0; not reached: 9.

| case | kind | units | certified | UNKNOWN | error | not reached |
|---|---|---|---|---|---|---|
| P5 | Q | 1 | 1 | 0 | 0 | 0 |
| P5 | H | 5 | 5 | 0 | 0 | 0 |
| P4 | Q | 1 | 1 | 0 | 0 | 0 |
| P4 | H | 5 | 3 | 0 | 0 | 2 |
| P3 | Q | 1 | 0 | 0 | 0 | 1 |
| P3 | H | 6 | 0 | 0 | 0 | 6 |

Per unit:

| unit | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|
| P5_7-9 | Q | 6000 | UNSATISFIABLE certified | 587.52 | 61.2 | 348.1 | 3.57 | 4397.09 |
| P5_1-3-10 | H | 1800 | UNSATISFIABLE certified | 357.96 | 56.9 | 323.5 | 3.37 | 4363.2 |
| P5_2-6-12 | H | 1800 | UNSATISFIABLE certified | 495.4 | 61.2 | 345.6 | 3.60 | 4364.52 |
| P5_6-7-8 | H | 1800 | UNSATISFIABLE certified | 85.78 | 30.0 | 188.2 | 1.35 | 3407.03 |
| P5_6-13-15 | H | 1800 | UNSATISFIABLE certified | 305.68 | 56.8 | 325.9 | 3.30 | 4354.9 |
| P5_8-11-12 | H | 1800 | UNSATISFIABLE certified | 19.98 | 13.5 | 121.7 | 0.22 | 2639.97 |
| P4_5-9 | Q | 3432 | UNSATISFIABLE certified | 916.03 | 66.2 | 375.8 | 4.08 | 4402.5 |
| P4_1-3-9 | H | 1800 | UNSATISFIABLE certified | 324.03 | 54.9 | 311.9 | 3.31 | 4362.68 |
| P4_1-9-14 | H | 1353 | UNSATISFIABLE certified | 489.48 | 60.4 | 350.9 | 3.58 | 4366.49 |
| P4_2-7-8 | H | 439 | UNSATISFIABLE certified | 237.33 | 53.4 | 323.7 | 3.22 | 4411.16 |

Not reached: P4_5-9-11, P4_6-10-12, P3_1-13, P3_1-2-8, P3_1-7-16, P3_4-5-13, P3_4-11-12, P3_5-10-15, P3_7-11-12

Certified units (min / median / max): solve s 20.0 / 341.0 / 916.0; lrat-check s 13.5 / 56.8 / 66.2; cake_lpr s 121.7 / 324.8 / 375.8; proof GB 0.2 / 3.3 / 4.1.

Largest solver RSS: 4411 MB.

The caps of P4_5-9, P4_1-9-14 and P4_2-7-8 were shortened by lane.py to fit END; all three still finished UNSAT and certified.

## Problems
No SAT, no proof rejection, no uncertified or ERROR record, no memory problem (peak solver RSS 4.4 GB of 15 GB).
