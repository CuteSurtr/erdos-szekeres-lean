# C2P5 M33

Fifth wave, machine M33: LIST = `C2P5A.tsv`, shard j = 33 of N = 37 (rows with idx ≡ 33 mod 37), H = 4.5, TASK commit 81cb025f.
Started 2026-10-31 19:25:48Z. END was 23:40:48Z, but the lane finished all its units at 21:06:01Z.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built everything from the vendored sources only, and all 196 manifest files matched: CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), and lrat-check (2e3b2dc) with the E2 patch. Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: `zcnf.py rot 17 7 --m 2 --hull` gave header `p cnf 838032 16653336`. The sha256 of base.cnf and of base.json both match the expected values.
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, 10 units, all case P4, kind H, cap 2400 s)
| case/kind | units | certified | timed out (UNKNOWN) | not reached | errors |
|---|---|---|---|---|---|
| P4 / H | 10 | 10 | 0 | 0 | 0 |

| unit | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB | certified |
|---|---|---|---|---|---|---|---|
| P4_1-2-9 | UNSATISFIABLE | 340.15 | 54.4 | 315.3 | 3.29 | 4400 | True |
| P4_1-5-8 | UNSATISFIABLE | 321.92 | 55.5 | 318.3 | 3.35 | 4371 | True |
| P4_1-6-9 | UNSATISFIABLE | 393.37 | 56.6 | 332.7 | 3.40 | 4397 | True |
| P4_1-8-14 | UNSATISFIABLE | 536.71 | 62.0 | 358.0 | 3.73 | 4362 | True |
| P4_1-10-13 | UNSATISFIABLE | 293.87 | 55.7 | 317.9 | 3.31 | 4366 | True |
| P4_1-12-15 | UNSATISFIABLE | 244.73 | 53.2 | 307.1 | 3.27 | 4364 | True |
| P4_2-7-9 | UNSATISFIABLE | 242.04 | 52.2 | 306.4 | 3.24 | 4375 | True |
| P4_5-9-10 | UNSATISFIABLE | 76.78 | 25.9 | 165.3 | 1.13 | 3067 | True |
| P4_6-9-13 | UNSATISFIABLE | 114.96 | 33.3 | 206.0 | 1.65 | 3409 | True |
| P4_9-10-11 | UNSATISFIABLE | 25.03 | 13.4 | 115.8 | 0.22 | 2645 | True |

Certified 10/10.
- solve s: min 25.03, median 269.30, max 536.71
- lrat-check s: min 13.40, median 53.80, max 62.00
- cake_lpr s: min 115.80, median 311.20, max 358.00
- proof GB: min 0.22, median 3.28, max 3.73
- largest solver RSS: 4400 MB
non-certified/errors: []

All proofs were deleted after checking, and `out.jsonl` keeps their sha256 values.
- No SAT result.
- No proof was rejected: every unit reports `c VERIFIED` and `s VERIFIED UNSAT`.
- No record has `certified: false` or an `ERROR` status.
- No memory problem: peak solver RSS was 4.4 GB on a 15 GB machine.
