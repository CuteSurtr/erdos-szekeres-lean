# C2P2 M11: list C2P2.tsv, shard j = 11 of N = 42, H = 2.5 h (TASK at d266d2c3)

## Tools and checks
- `build_tools.sh` built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch) from the vendored sources. All 196 manifest hashes matched.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one, and the cake_lpr example printed `s VERIFIED UNSAT` (`tools.txt`).
- Base CNF: header `p cnf 838032 16653336`, and both sha256 values (base.cnf `b0061e90…`, base.json `2476faff…`) were as expected.
- Cubes: `l2cubes.py` output for P1..P8 was byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Run
- One lane (`run.sh`), started 06:49Z, with END = 1793437326 (09:02:06Z).
- The lane stopped at 08:48:54Z with 791 s left before END, which is less than the 15 minutes it needs to start a unit.

## Units (8 assigned)
| unit | case | kind | status | solve s | lrat-check s | cake_lpr s | proof bytes | solver RSS MB |
|---|---|---|---|---|---|---|---|---|
| P8_3-12 | P8 | Q | certified | 4998.1 | 109.2 | 634.1 | 7,863,024,115 | 4372 |
| P6_1-2-16 | P6 | H | certified | 233.0 | 42.9 | 282.7 | 3,224,323,902 | 4349 |
| P6_1-8-11 | P6 | H | certified | 418.4 | 46.0 | 303.0 | 3,411,394,781 | 4362 |

- Certified, 3: P8 Q 1 (P8_3-12), P6 H 2.
  - Solve s: min 233.0, median 418.4, max 4998.1.
  - lrat-check s: min 42.9, median 46.0, max 109.2.
  - cake_lpr s: min 282.7, median 303.0, max 634.1.
  - Proof size: min 3.22 GB, median 3.41 GB, max 7.86 GB.
- Timed out (UNKNOWN): 0.
- Not reached, 5: P6_2-3 (P6 Q), and P6_2-9-16, P6_3-8-13, P6_7-11-16, P6_9-11-12 (P6 H).
- Errors or `certified: false`: none.

## Other
- Largest solver RSS: 4372 MB. cake_lpr used about 8.2 GB RSS with an 8000 MB heap.
- No memory problems.
- No SAT answer, and no proof was rejected.
