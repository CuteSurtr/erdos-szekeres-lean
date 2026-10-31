# C2P M02: shard j = 2 of N = 42 of C2P.tsv

The TASK.md used is the one at fb2c59af. One cloud VM with 4 cores, 15 GB RAM and no swap (`env.txt`). The run started at 02:48:45 UTC on 2026-10-31, with H = 3.5 h, so END = 1793426625 (06:03:45 UTC).
There was one lane (`run.sh`). It ran from 02:51:22 to 05:56:21 UTC and stopped by itself when only 443 s were left before END.

## Tools and checks (`tools.txt`)
- CaDiCaL 3.0.1 at c60730422e75, cake_lpr at a36874a8b750 (`make cake_lpr`), and drat-trim lrat-check at 2e3b2dc0ecf9 with the E2 patch. The patch is in normal-diff format, so it was applied with `patch`, because `git apply` rejects it.
- Sanity checks pass. The cake_lpr example prints `s VERIFIED UNSAT`. Both checkers reject the LRAT `3 0 0` on {1},{-1} and both accept `3 0 1 2 0`.
- Base CNF: `p cnf 838032 16653336`. The sha256 of base.cnf and of base.json both match.
- Cubes: P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`: 54 units, no cover units in this shard)
| case | kind | units | certified | timed out (UNKNOWN) | not reached | errors |
|------|------|-------|-----------|---------------------|-------------|--------|
| P8 | Q | 3 | 3 | 0 | 0 | 0 |
| P8 | H | 3 | 3 | 0 | 0 | 0 |
| P7 | Q | 1 | 1 | 0 | 0 | 0 |
| P7 | H | 6 | 6 | 0 | 0 | 0 |
| P6 | Q | 1 | 0 | 0 | 1 | 0 |
| P6 | H | 5 | 3 | 0 | 2 | 0 |
| P5 | Q / H | 2 / 5 | 0 | 0 | 7 | 0 |
| P4 | Q / H | 1 / 6 | 0 | 0 | 7 | 0 |
| P3 | Q / H | 2 / 5 | 0 | 0 | 7 | 0 |
| P2 | Q / H | 1 / 6 | 0 | 0 | 7 | 0 |
| P1 | Q / H | 1 / 6 | 0 | 0 | 7 | 0 |
| **total** | | **54** | **16** | **0** | **38** | **0** |

All 16 records are `UNSATISFIABLE` with `"certified": true`: lrat-check printed `c VERIFIED` and cake_lpr printed `s VERIFIED UNSAT`, on the 8000 MB heap every time.
Certified units, in order: P8_2-14, P8_2-16, P8_10-12, P8_1-9-13, P8_1-2-9, P8_10-11-13, P7_3-8-13, P7_3-8, P7_8-10-13, P7_2-4-16, P7_1-9-13, P7_1-8-12, P7_1-8-9, P6_7-8-9, P6_1-8-9, P6_2-12-16.
Not reached, starting from the next unit in list order: P6_1-14 (Q), P6_1-8-16, P6_2-3-7, and every unit of P5 through P1.

Certified units (16):
| quantity | min | median | max | total |
|----------|-----|--------|-----|-------|
| solve s | 16.9 | 267.8 | 1681.7 (P7_3-8, Q) | 6827 |
| lrat-check s | 8.8 | 38.4 | 65.6 | 588 |
| cake_lpr s | 78.8 | 231.9 | 368.6 | 3580 |
| proof size | 0.21 GB | 3.45 GB | 6.21 GB | 51.7 GB |

The Q units were the slowest: they took 549–1682 s to solve, against 17–399 s for the H units.

## Memory, SAT, rejections
- The largest solver RSS was 4420 MB (P7_1-8-9). Free memory never ran short.
- No SAT result, no proof rejection, no error and no timeout.
