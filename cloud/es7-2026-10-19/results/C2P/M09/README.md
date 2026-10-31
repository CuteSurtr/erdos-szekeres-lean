# C2P / M09 (LIST C2P.tsv, shard j = 9 of N = 42, H = 3.0, Z = 01909a07)

Restart of the earlier M09 attempt that stopped at step 1 (its files were replaced). Start 03:23:15Z,
END 06:08:15Z (epoch 1793426895); the lane stopped itself at 05:58:19Z with 595 s left.

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match):
  CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (drat-trim 2e3b2dc + E2 patch). Nothing downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 of base.cnf and base.json both match.
- Cubes P1..P8: byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (54: 44 H, 10 Q, no cover)
| case | certified | UNKNOWN (timed out) | not reached |
|---|---|---|---|
| P8 | 6 (5 H, 1 Q) | 0 | 0 |
| P7 | 5 (4 H, 1 Q) | 1 Q (P7_3-10) | 0 |
| P1–P4, P6 | 0 | 0 | 7 each (6 H, 1 Q) |
| P5 | 0 | 0 | 7 (5 H, 2 Q) |
| **total** | **11** (9 H, 2 Q) | **1** (Q) | **42** (35 H, 7 Q) |

- P7_3-10 (Q): UNKNOWN after 1724 s at its reduced cap of 1735 s (cap shortened by END). Open.
- Not reached: every P1–P6 unit (in units.tsv order, after P8 and P7).
- Errors: none. `"certified": false`: none.

Certified units (min / median / max):
- solve: 22.6 / 278.1 / 1424.8 s (the slowest was P7_2-14, Q)
- lrat-check: 11.7 / 46.7 / 72.3 s
- cake_lpr: 99.8 / 275.4 / 395.7 s
- proof size: 0.21 / 3.27 / 5.10 GB (deleted after checking)

## Resources and outcomes
- Largest solver RSS: 4416 MB (P8_2-5-9). No memory problem.
- No SAT. No proof rejection.
