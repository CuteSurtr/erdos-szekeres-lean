# C2P5 M29 — LIST C2P5A.tsv, shard j = 29 of N = 37, H = 4.5 (TASK commit 81cb025f)

Start 2026-10-31 19:25:48Z (epoch 1793474748), END 1793490048. The lane finished every unit by 21:15:55Z.

## Tools and checks (`tools.txt`)
- CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc + E2 patch) were built by
  `C2P/vendor/build_tools.sh` from the vendored `vendor/tools-src.tar.xz`. All 196 manifest files matched, and
  nothing was cloned or downloaded.
- The sanity checks passed: both checkers reject the bad LRAT and accept the good one, and the cake_lpr example
  prints `s VERIFIED UNSAT`.
- The base CNF has header `p cnf 838032 16653336`, and the sha256 of base.cnf and base.json match the expected values.
- The cubes P1..P8 from `C2C34/l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (10 rows of C2P5A.tsv with idx ≡ 29 mod 37; all P4, kind H, cap 2400 s)
| case/kind | units | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|
| P4 H | 10 | 10 | 0 | 0 | 0 |

All ten records have status UNSATISFIABLE, lrat-check `c VERIFIED`, cake_lpr `s VERIFIED UNSAT` and certified true:
P4_1-2-5, P4_1-3-6, P4_1-5-15, P4_1-7-16, P4_1-9-12, P4_1-11-15, P4_2-6-12, P4_5-8-13, P4_6-8-15, P4_8-10-11.

Statistics over the 10 certified units (min / median / max):
- solve: 20.97 / 302.8 / 580.02 s
- lrat-check: 12.5 / 45.6 / 50.0 s
- cake_lpr: 112.8 / 294.9 / 346.3 s
- proof size: 0.215 / 3.26 / 3.61 GB (215266133 / 3261416889 / 3607313329 bytes)

The largest solver RSS was 4424 MB (P4_1-3-6).

There were no SAT answers, no proof rejections, no errors and no memory problems.
