# C2P5 M93: list C2P5B.tsv, shard j = 43 of N = 50, H = 5.25 (TASK commit 81cb025f)

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built from the vendored sources only (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Nothing cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90...d8ff1` and base.json `2476fafff...2b48`, both as expected.
- Cubes P1..P8 from `C2C34/l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Run
One lane (`run.sh`), start 2026-10-31 15:10:40Z, END 1793477440 (20:10:40Z). The lane finished all its units at 19:07:54Z.

## Units: 18 total, all 18 certified
| case | kind | units | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|---|
| P2 | Q | 1 | 1 | 0 | 0 | 0 |
| P2 | H | 6 | 6 | 0 | 0 | 0 |
| P1 | Q | 1 | 1 | 0 | 0 | 0 |
| P1 | H | 4 | 4 | 0 | 0 | 0 |
| P3 | Q | 1 | 1 | 0 | 0 | 0 |
| P3 | H | 5 | 5 | 0 | 0 | 0 |

Every record is UNSATISFIABLE, with `c VERIFIED` from lrat-check and `s VERIFIED UNSAT` from cake_lpr.

Certified units, min / median / max:
- solve: 23.0 / 302.4 / 2014.0 s
- lrat-check: 14.4 / 58.1 / 88.0 s
- cake_lpr: 123.4 / 333.8 / 511.2 s
- proof size: 0.22 / 3.3 / 5.43 GB

The quadrilateral units (cap 8000 s) took: P2_6-10 667 s (proof 3.73 GB), P1_5-7 403 s (3.28 GB), P3_1-12 2014 s (5.43 GB).

## Other
- Largest solver RSS: 4417 MB (P1_2-6-11).
- No SAT, no proof rejection, no ERROR status and no memory problem.
