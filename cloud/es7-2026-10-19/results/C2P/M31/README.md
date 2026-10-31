# C2P / M31 (LIST C2P.tsv, shard 31 of 42, H = 3.0, Z = 01909a07)

Restart of an earlier attempt that stopped at step 1; its files were replaced.

**Result: 7 units certified, 1 timed out, 45 not reached. No SAT, no proof rejection, no error, no memory problem.**

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from `vendor/tools-src.tar.xz` only (manifest: all 196 files match):
  CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Nothing cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF header `p cnf 838032 16653336`; sha256 of base.cnf and base.json match.
- Cubes P1..P8: byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).
- Commits: env `26d136d1`; tools/units/run.sh `def9e9cb`+1; progress commits after that.

## Lane
Started 03:26Z (session start 03:23:24Z = 1793417004), END = 1793426904 (06:08:24Z); `run.sh`.
The lane stopped at 05:55:21Z with 782 s left (< 15 min, no new unit).

## Units (53: 46 H, 7 Q, no cover)
| | certified | UNKNOWN (timeout) | not reached | errors |
|---|---|---|---|---|
| P8 | 5 (4 H, 1 Q) | 0 | 0 | 0 |
| P7 | 2 (2 H) | 1 (Q: P7_1-5, cap 2400 s) | 4 (3 H, 1 Q) | 0 |
| P6 | 0 | 0 | 7 (6 H, 1 Q) | 0 |
| P5 | 0 | 0 | 7 (6 H, 1 Q) | 0 |
| P4 | 0 | 0 | 6 (5 H, 1 Q) | 0 |
| P3 | 0 | 0 | 7 (6 H, 1 Q) | 0 |
| P2 | 0 | 0 | 7 (5 H, 2 Q) | 0 |
| P1 | 0 | 0 | 7 (6 H, 1 Q) | 0 |
| total | 7 (6 H, 1 Q) | 1 (Q) | 45 (39 H, 6 Q) | 0 |

Certified (both lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`, heap 8000 MB for all):
P8_2-11-16, P8_2-4-15, P8_1-3-14, P8_1-13 (Q), P8_3-10-16, P7_9-12-14, P7_2-13-14.

| certified (7) | min | median | max |
|---|---|---|---|
| solve s | 94.1 | 255.0 | 2319.5 (P8_1-13, Q) |
| lrat-check s | 25.3 | 43.1 | 74.5 |
| cake_lpr s | 173.5 | 278.6 | 452.0 |
| proof size | 1.58 GB | 3.22 GB | 5.73 GB |

H units alone: solve 94–525 s. Timed out: P7_1-5 (Q) at its 2400 s cap (2378 s CPU) — open.
Not reached: units.tsv rows from P7_3-11-13 (idx 367) to the end.

## Other
- Largest solver RSS: 4433 MB (P8_1-13). Memory peaked around 8 GB used of 15 GB (cake_lpr heap); no OOM.
- No SAT_FOUND; no `"certified": false`; no ERROR status.
