# C2P / M33 (LIST C2P.tsv, shard 33 of 42, H = 3.0, Z = 01909a07)

Restart of an earlier attempt (TASK at fb2c59af) that stopped at step 1; its files were replaced.

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match):
  CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 of base.cnf and base.json both match.
- Cubes P1..P8: all byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Lane
Start 03:23:23Z, END 06:08:23Z (start + 3 h − 15 min); `run.sh`. The lane stopped at 05:58:25Z
("stop: 597 s left"). 53 units (42 H, 11 Q, no cover); 10 reached.

| unit | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|
| P8_1-3-10 | H | 1800 | certified | 281.3 | 47.7 | 277.0 | 3.28 | 4393 |
| P8_4-12 | Q | 2400 | UNKNOWN | 2385.8 | | | | 4367 |
| P8_10-11-15 | H | 1800 | certified | 68.5 | 20.9 | 143.8 | 1.12 | 3137 |
| P8_3-10-11 | H | 1800 | certified | 293.9 | 46.4 | 279.4 | 3.32 | 4403 |
| P8_2-9 | Q | 2400 | UNKNOWN | 2387.1 | | | | 4421 |
| P7_1-3-12 | H | 1800 | certified | 269.7 | 45.6 | 274.3 | 3.29 | 4359 |
| P7_1-3-15 | H | 1701* | certified | 194.3 | 47.2 | 281.3 | 3.18 | 4402 |
| P7_1-11-13 | H | 1170* | certified | 231.5 | 46.0 | 270.4 | 3.22 | 4351 |
| P7_2-3-5 | H | 614* | certified | 62.7 | 20.7 | 142.4 | 1.11 | 3170 |
| P7_8-16 | Q | 384* | UNKNOWN | 381.7 | | | | 4382 |

\* cap shortened by lane.py so that 10 minutes remain before END (list caps: 1800 for H, 2400 for P7_8-16).

## Counts by case and kind
- Certified 7: P8 H 3, P7 H 4.
- Timed out (UNKNOWN) 3: P8 Q 2 (full 2400 s cap), P7 Q 1 (P7_8-16, only 384 s because of END; worth re-running with its full cap).
- Not reached 43: P1 6H+1Q, P2 5H+2Q, P3 6H+1Q, P4 4H+2Q, P5 6H+1Q, P6 6H+1Q, P7 2H, P8 none.
- Errors 0; no `"certified": false` record.

Certified units (7), min / median / max: solve 62.7 / 231.5 / 293.9 s; lrat-check 20.7 / 46.0 / 47.7 s;
cake_lpr 142.4 / 274.3 / 281.3 s; proof size 1.11 / 3.22 / 3.32 GB (1110229185 / 3217228403 / 3324024345 bytes).

Largest solver RSS: 4421 MB (P8_2-9). No memory problem (machine has 15 GB).

**No SAT, no proof rejection, no memory problem.**
