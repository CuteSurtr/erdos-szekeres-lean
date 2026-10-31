# C2P / M19 (LIST C2P.tsv, shard 19 of 42, H = 3.0, Z = 01909a07)

Restart of the earlier M19 attempt (at fb2c59af), which stopped at step 1; its files were replaced.

**Result: 12 of 53 units run: 11 certified UNSAT, 1 timed out (UNKNOWN), 41 not reached. No SAT, no proof
rejection, no error, no memory problem.**

## Tools and checks ()
- Built with `C2P/vendor/build_tools.sh` from the vendored sources (manifest: all 196 files match; nothing
  cloned or downloaded): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, both sha256 match. All 8 cube files byte-identical.

## Lane
One lane (`run.sh`), start 03:23:14Z (epoch 1793416994), END 06:08:14Z. It ran 03:35:37Z–05:58:18Z and stopped
with 595 s left (less than 15 min before END), so no further unit was started.

Timed out: P7_2-13 (idx 481, Q), solve capped at 1493 s (cap reduced by END − 10 min), status UNKNOWN.
Not reached (41): all units from idx 523 on (P6, P5, P4, P3, P2, P1; see `units.tsv`).

| case | kind | units | certified | timed out | not reached | other |
|---|---|---|---|---|---|---|
| P1 | H | 6 | 0 | 0 | 6 | 0 |
| P1 | Q | 1 | 0 | 0 | 1 | 0 |
| P2 | H | 5 | 0 | 0 | 5 | 0 |
| P2 | Q | 1 | 0 | 0 | 1 | 0 |
| P3 | H | 6 | 0 | 0 | 6 | 0 |
| P3 | Q | 1 | 0 | 0 | 1 | 0 |
| P4 | H | 6 | 0 | 0 | 6 | 0 |
| P4 | Q | 1 | 0 | 0 | 1 | 0 |
| P5 | H | 5 | 0 | 0 | 5 | 0 |
| P5 | Q | 2 | 0 | 0 | 2 | 0 |
| P6 | H | 6 | 0 | 0 | 6 | 0 |
| P6 | Q | 1 | 0 | 0 | 1 | 0 |
| P7 | H | 5 | 5 | 0 | 0 | 0 |
| P7 | Q | 2 | 1 | 1 | 0 | 0 |
| P8 | H | 4 | 4 | 0 | 0 | 0 |
| P8 | Q | 1 | 1 | 0 | 0 | 0 |
| all | | 53 | 11 | 1 | 41 | 0 |

Certified units, min / median / max:
- solve s: 61.7 / 271.6 / 832.9
- lrat-check s: 20.8 / 48.6 / 58.3
- cake_lpr s: 143.9 / 278.6 / 330.8
- proof GB: 1.11 / 3.31 / 4.12
- cake_lpr heap: 8000 MB

Largest solver RSS: 4429 MB.

Per unit:

| idx | unit | kind | status | solve s | proof GB | lrat-check s | cake_lpr s | certified |
|---|---|---|---|---|---|---|---|---|
| 19 | P8_1-13-15 | H | UNSATISFIABLE | 211.49 | 3.20 | 44.9 | 270.6 | True |
| 61 | P8_3-12-14 | H | UNSATISFIABLE | 271.61 | 3.29 | 46.8 | 274.3 | True |
| 103 | P8_1-9-16 | H | UNSATISFIABLE | 355.27 | 3.51 | 49.4 | 289.5 | True |
| 145 | P8_11-14 | Q | UNSATISFIABLE | 832.9 | 4.12 | 58.3 | 330.8 | True |
| 187 | P8_3-5-10 | H | UNSATISFIABLE | 250.23 | 3.31 | 49.3 | 284.9 | True |
| 229 | P7_2-9-11 | H | UNSATISFIABLE | 301.76 | 3.34 | 48.6 | 278.6 | True |
| 271 | P7_10-12 | Q | UNSATISFIABLE | 558.06 | 3.70 | 54.2 | 301.4 | True |
| 313 | P7_8-12-13 | H | UNSATISFIABLE | 96.34 | 1.76 | 29.5 | 184.2 | True |
| 355 | P7_1-10-15 | H | UNSATISFIABLE | 355.44 | 3.44 | 49.3 | 284.9 | True |
| 397 | P7_1-3-5 | H | UNSATISFIABLE | 61.68 | 1.11 | 20.8 | 143.9 | True |
| 439 | P7_3-11-12 | H | UNSATISFIABLE | 249.22 | 3.26 | 45.4 | 277.2 | True |
| 481 | P7_2-13 | Q | UNKNOWN | 1481.56 | - | - | - | None |
