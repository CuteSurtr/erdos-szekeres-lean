# C2P M32 (LIST = C2P.tsv, j = 32, N = 42, H = 3.0, Z = 01909a07)

Start 2026-10-31 03:23 UTC; END = 06:08:27 UTC (epoch 1793426907). The lane ran 03:35–05:58 UTC and stopped by itself (595 s left before END, under the 15-minute floor). This run replaces an earlier attempt (task fb2c59af) that stopped at step 1.

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only. Nothing was cloned or downloaded. The manifest check passed for all 196 files.
  - CaDiCaL c6073042 (`--version` 3.0.1), cake_lpr a36874a8, and lrat-check 2e3b2dc with the E2 patch.
- Sanity checks: both checkers reject the bad LRAT and accept the good one, and the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: the header is `p cnf 838032 16653336`, and the sha256 of both base.cnf and base.json match.
- Cubes P1..P8: all are byte-identical to `C2P/cubes/`.

## Units (`units.tsv`, 53 units: 43 H, 10 Q, no cover)
| case | kind | units | certified | UNKNOWN (timed out) | not reached | errors |
|---|---|---|---|---|---|---|
| P8 | H | 4 | 4 | 0 | 0 | 0 |
| P8 | Q | 1 | 0 | 1 (P8_9-14, 2385 s of cap 2400) | 0 | 0 |
| P7 | H | 6 | 2 | 0 | 4 | 0 |
| P7 | Q | 1 | 0 | 1 (P7_8-13, 1930 s of cap 1942) | 0 | 0 |
| P1 | H / Q | 5 / 2 | 0 | 0 | 5 / 2 | 0 |
| P2 | H / Q | 6 / 1 | 0 | 0 | 6 / 1 | 0 |
| P3 | H / Q | 5 / 2 | 0 | 0 | 5 / 2 | 0 |
| P4 | H / Q | 5 / 1 | 0 | 0 | 5 / 1 | 0 |
| P5 | H / Q | 6 / 1 | 0 | 0 | 6 / 1 | 0 |
| P6 | H / Q | 6 / 1 | 0 | 0 | 6 / 1 | 0 |
| **total** | | 53 | 6 | 2 | 45 | 0 |

The certified units are P8_3-10-13, P8_2-14-16, P8_3-13-16, P8_2-3-15, P7_1-9-15 and P7_1-3-9, all of kind H. For each one, lrat-check printed `c VERIFIED` and cake_lpr printed `s VERIFIED UNSAT`.

The 6 certified units (minimum / median / maximum):
- solve: 216 / 342 / 441 s
- lrat-check: 51.9 / 55.1 / 57.3 s
- cake_lpr: 286 / 312 / 328 s (heap 8000 MB)
- proof size: 3.16 / 3.30 / 3.52 GB (3155921761 / 3301337512 / 3522977359 bytes)

Both Q units reached their caps (UNKNOWN). No unit reported `certified: false` or an `ERROR` status.

## Resources
The largest solver RSS was 4479 MB (P7_8-13).

## SAT, rejection, memory
- No SAT.
- No proof was rejected.
- No memory problem: free memory never fell below about 2 GB.
