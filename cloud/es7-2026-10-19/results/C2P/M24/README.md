# C2P / M24 (LIST C2P.tsv, shard 24 of 42, H = 3.0, Z = 01909a07)

Restart of the earlier M24 attempt (fb2c59af), which had stopped at step 1; its files were replaced.

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match):
  CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check from drat-trim 2e3b2dc with the E2 patch.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 of base.cnf and base.json match.
- Cubes P1..P8: all 8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (53: 43 H, 10 Q, no cover)
Lane started 03:25Z, END 06:08:15Z (start 03:23:15Z + 3 h − 15 min); lane finished at 06:03Z ("stop: 281 s left").

| | certified | UNKNOWN (timed out) | not reached | errors |
|---|---|---|---|---|
| P8 | 4 H + 1 Q | 0 | 0 | 0 |
| P7 | 2 H | 1 Q (P7_3-13, solve 2379.8 s at cap 2400) | 3 H + 1 Q | 0 |
| P1 | 0 | 0 | 6 H + 1 Q | 0 |
| P2 | 0 | 0 | 6 H + 1 Q | 0 |
| P3 | 0 | 0 | 5 H + 1 Q | 0 |
| P4 | 0 | 0 | 6 H + 1 Q | 0 |
| P5 | 0 | 0 | 5 H + 2 Q | 0 |
| P6 | 0 | 0 | 6 H + 1 Q | 0 |
| **total** | **7** (6 H, 1 Q) | **1** (Q) | **45** (37 H, 8 Q) | **0** |

Certified: P8_2-10-14, P8_3-14-16, P8_4-10-15, P8_2-6 (Q), P8_1-4-13, P7_1-12-14, P7_2-4-12.
Every certified record has `lrat-check: c VERIFIED` and `cake_lpr: s VERIFIED UNSAT`.

Certified units (min / median / max):
- solve: 232.0 / 354.2 / 1996.4 s (the Q unit P8_2-6 is the maximum)
- lrat-check: 51.7 / 55.5 / 85.9 s
- cake_lpr: 296.9 / 310.3 / 461.8 s
- proof size: 3.21 / 3.40 / 5.70 GB (3213600159 / 3402343553 / 5701211635 bytes)

Largest solver RSS: 4421 MB (P8_4-10-15). No memory problem.

No SAT, no proof rejection, no record with `certified: false`, no ERROR status.
