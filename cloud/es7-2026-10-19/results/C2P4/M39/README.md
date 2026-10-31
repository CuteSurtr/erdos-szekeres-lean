# C2P4 M39 — LIST C2P4.tsv, shard j=39 of N=50, H=2.5, task commit a46b478d

## Tools and checks
- `C2P/vendor/build_tools.sh` built the tools from the vendored sources only (manifest: all 196 files match). Versions: CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc, with the E2 patch). Sanity checks: both checkers rejected the bad LRAT and accepted the good one, and the cake_lpr example printed `s VERIFIED UNSAT`.
- The base CNF header is `p cnf 838032 16653336`. Both sha256 values match (base.cnf b0061e90…, base.json 2476faff…).
- The cubes P1..P8 are byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Full details are in `tools.txt`.

## Units (19 in `units.tsv`: 13 for P5+P4 listed first, then P3)
| case | kind | units | certified | timed out | not reached | errors |
|---|---|---|---|---|---|---|
| P5 | Q | 1 | 1 | 0 | 0 | 0 |
| P5 | H | 5 | 5 | 0 | 0 | 0 |
| P4 | Q | 1 | 1 | 0 | 0 | 0 |
| P4 | H | 5 | 0 | 0 | 5 | 0 |
| P3 | Q | 1 | 0 | 0 | 1 | 0 |
| P3 | H | 6 | 0 | 0 | 6 | 0 |
| **total** | | 19 | **7** | 0 | 12 | 0 |

Every unit in P5 on this shard is certified (P5_7-11, P5_1-3-15, P5_2-6-14, P5_6-7-10, P5_7-8-9, P5_8-11-14). P4_5-11 is certified too: END had shortened its cap to 3275 s, and it solved in 2486 s.
These 12 units were not reached, because the lane stopped at 15:04:49Z with 702 s left before END: P4_1-5-6, P4_1-9-16, P4_2-7-10, P4_5-9-13, P4_6-10-14, P3_1-15, P3_1-2-10, P3_1-8-10, P3_4-5-15, P3_4-11-14, P3_5-11-13, P3_8-9-11.

| unit | case | kind | status | cap s | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB | certified |
|---|---|---|---|---|---|---|---|---|---|---|
| P5_7-11 | P5 | Q | UNSATISFIABLE | 6000 | 1180.76 | 73.3 | 398.4 | 4.38 | 4380 | True |
| P5_1-3-15 | P5 | H | UNSATISFIABLE | 1800 | 241.14 | 55.8 | 323.6 | 3.18 | 4405 | True |
| P5_2-6-14 | P5 | H | UNSATISFIABLE | 1800 | 590.2 | 69.6 | 379.0 | 3.67 | 4366 | True |
| P5_6-7-10 | P5 | H | UNSATISFIABLE | 1800 | 78.47 | 25.6 | 172.9 | 1.12 | 3159 | True |
| P5_7-8-9 | P5 | H | UNSATISFIABLE | 1800 | 28.48 | 14.0 | 122.6 | 0.22 | 2664 | True |
| P5_8-11-14 | P5 | H | UNSATISFIABLE | 1800 | 30.84 | 14.9 | 122.3 | 0.22 | 2645 | True |
| P4_5-11 | P4 | Q | UNSATISFIABLE | 3275 | 2485.5 | 101.6 | 548.4 | 5.84 | 4380 | True |

Certified units (min / median / max): solve 28.5 / 241.1 / 2485.5 s; lrat-check 14.0 / 55.8 / 101.6 s; cake_lpr 122.3 / 323.6 / 548.4 s; proof 0.22 / 3.18 / 5.84 GB.

The largest solver RSS was 4405 MB (P5_1-3-15).

There was no SAT, no proof rejection, no ERROR record and no memory problem. The lane deleted every proof, and none was committed.
