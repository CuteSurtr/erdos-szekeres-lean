# C2P5 M17: LIST = C2P5A.tsv, j = 17, N = 37, H = 4.5 (TASK.md commit 81cb025f)

Start 2026-10-31 18:50Z (epoch 1793472624), END 23:05:24Z (epoch 1793487924). One lane (`run.sh`); it finished all units at 20:53:09Z.

## Tools and checks (details in `tools.txt`)
- `C2P/vendor/build_tools.sh` built everything from the vendored sources (manifest: all 196 files match): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch. Nothing was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one, and the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. Both sha256 values matched (base.cnf `b0061e90…d8ff1`, base.json `2476faff…bb472b48`).
- Cubes P1..P8 from `l2cubes.py`: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (idx ≡ 17 mod 37 of C2P5A.tsv: 6 units)
| | P4 Q | P4 H | P3 H | total |
|---|---|---|---|---|
| certified (UNSAT, both checkers accept) | 1 | 4 | 1 | 6 |
| timed out (UNKNOWN) | 0 | 0 | 0 | 0 |
| not reached | 0 | 0 | 0 | 0 |
| errors / certified false | 0 | 0 | 0 | 0 |

| unit | kind | cap | solve s | lrat-check s | cake_lpr s | proof bytes | solver RSS MB |
|---|---|---|---|---|---|---|---|
| P4_1-12 | Q | 8000 | 2822.2 | 84.2 | 521.0 | 5,800,322,465 | 4383 |
| P4_2-5-10 | H | 2400 | 474.6 | 49.8 | 328.4 | 3,440,988,832 | 4364 |
| P4_2-7-14 | H | 2400 | 659.4 | 55.1 | 344.9 | 3,707,103,005 | 4411 |
| P4_5-9-15 | H | 2400 | 462.4 | 49.6 | 326.2 | 3,444,965,885 | 4412 |
| P4_6-10-13 | H | 2400 | 125.1 | 26.9 | 192.7 | 1,575,845,077 | 3411 |
| P3_4-12-13 | H | 2400 | 276.9 | 47.2 | 284.9 | 3,116,633,650 | 4391 |

Across all 6 certified units (min / median / max):
- solve: 125.1 / 468.5 / 2822.2 s
- lrat-check: 26.9 / 49.7 / 84.2 s
- cake_lpr: 192.7 / 327.3 / 521.0 s (heap 8000 MB every time; no retries)
- proof size: 1.58 / 3.44 / 5.80 GB

Largest solver RSS: 4412 MB (P4_5-9-15).

## Problems
- No SAT. No proof was rejected. No memory or disk problem: free disk never dropped below 22 GB.
