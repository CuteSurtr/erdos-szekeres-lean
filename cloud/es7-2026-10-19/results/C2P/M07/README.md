# C2P / M07 (LIST C2P.tsv, shard j = 7 of N = 42, H = 3.0, Z = 01909a07)

**Result: 12 of 54 units certified UNSAT; 0 timed out, 0 errors, 42 not reached (out of time). No SAT.**

Start 2026-10-31T03:23:09Z, END 06:08:09Z. Lane ran 03:26:03Z–05:53:24Z and stopped with 884 s left (< 900 s).
This replaces an earlier M07 attempt (TASK at fb2c59af) that stopped at step 1.

## Tools and checks (`tools.txt`)
- `vendor/build_tools.sh` from the vendored sources only (nothing cloned or downloaded): manifest, all 196 files match.
  CaDiCaL c6073042 (`--version` 3.0.1), cake_lpr a36874a8, lrat-check from drat-trim 2e3b2dc with the E2 patch.
- Sanity: cake_lpr example `s VERIFIED UNSAT`; bad LRAT rejected by both (lrat-check `c FAILED: empty clause without
  a RUP conflict`, cake_lpr `pivot must be non-zero`); good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`).
- Base CNF: header `p cnf 838032 16653336`, sha256 of base.cnf and base.json both match.
- Cubes P1..P8: all 8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, 54 rows: 44 H, 10 Q, no cover)
| case | certified | UNKNOWN | error | not reached |
|---|---|---|---|---|
| P8 | 6 (5 H, 1 Q) | 0 | 0 | 0 |
| P7 | 6 (5 H, 1 Q) | 0 | 0 | 0 |
| P6 | 0 | 0 | 0 | 7 (6 H, 1 Q) |
| P5 | 0 | 0 | 0 | 7 (5 H, 2 Q) |
| P4 | 0 | 0 | 0 | 7 (6 H, 1 Q) |
| P3 | 0 | 0 | 0 | 7 (5 H, 2 Q) |
| P2 | 0 | 0 | 0 | 7 (6 H, 1 Q) |
| P1 | 0 | 0 | 0 | 7 (6 H, 1 Q) |
| total | 12 (10 H, 2 Q) | 0 | 0 | 42 (34 H, 8 Q) |

Certified (both checkers accepted; all cake_lpr runs at heap 8000 MB), min / median / max:
- solve: 23.3 / 320.1 / 764.2 s (the Q units were the two slowest: P8_9-11 654 s, P7_3-4 764 s)
- lrat-check: 13.0 / 53.6 / 61.6 s
- cake_lpr: 111.8 / 308.1 / 346.9 s
- proof size: 0.22 / 3.34 / 3.97 GB (221,983,683 / 3,340,693,658.5 / 3,974,208,854 bytes)

Largest solver RSS: 4457 MB (P7_2-11-13).

No SAT, no proof rejection, no `certified: false` record, no ERROR, no memory problem.
