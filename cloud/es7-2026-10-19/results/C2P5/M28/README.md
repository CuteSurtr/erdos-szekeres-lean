# C2P5 M28: list C2P5A.tsv, shard j = 28 of N = 37, H = 4.5 (TASK commit 81cb025f)

## Tools and checks (`tools.txt`)
- Ran `C2P/vendor/build_tools.sh`, which built from the vendored sources only (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Nothing was cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf `b0061e90...d8ff1` and of base.json `2476fafff...2b48`, both as expected.
- Cubes P1..P8 from `C2C34/l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Run
One lane (`run.sh`), started 2026-10-31 19:11:21Z, END 1793489181 (23:26:21Z). The lane finished all its units at 20:50:09Z.

## Units: 10 total, all 10 certified
| case | kind | units | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|---|
| P4 | H | 10 | 10 | 0 | 0 | 0 |

Every record is UNSATISFIABLE, with `c VERIFIED` from lrat-check and `s VERIFIED UNSAT` from cake_lpr.

Certified units, min / median / max:
- solve: 25.4 / 239.6 / 480.3 s
- lrat-check: 12.8 / 55.0 / 61.1 s
- cake_lpr: 115.6 / 313.5 / 348.4 s
- proof size: 0.21 / 3.23 / 3.66 GB

## Other
- Largest solver RSS: 4418 MB (P4_2-6-11).
- No SAT, no proof rejection, no ERROR status and no memory problem.
