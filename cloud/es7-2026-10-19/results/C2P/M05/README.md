# C2P M05 (LIST = C2P.tsv, j = 5, N = 42, H = 3.0, Z = 01909a07)

Start 2026-10-31 03:23:06 UTC (epoch 1793416986); END = 1793426886 (06:08:06 UTC). One lane, `run.sh`.
This replaces an earlier attempt (at fb2c59af) that stopped at step 1 without building the tools.

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match):
  CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check from drat-trim 2e3b2dc with the E2 patch. Nothing cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf (`b0061e90…`) and base.json (`2476fafff…`) match.
- Cubes P1..P8: all 8 byte-identical to `C2P/cubes/` (560 lines each).

## Units (`units.tsv`, `out.jsonl`)
54 units (idx ≡ 5 mod 42): 44 H, 10 Q, no cover.

| case | units (H/Q) | certified | timed out (UNKNOWN) | not reached |
|---|---|---|---|---|
| P8 | 6 H | 6 H | 0 | 0 |
| P7 | 5 H + 1 Q | 5 H + 1 Q | 0 | 0 |
| P6 | 5 H + 2 Q | 0 | 1 Q (P6_9-13) | 5 H + 1 Q |
| P5 | 6 H + 1 Q | 0 | 0 | 6 H + 1 Q |
| P4 | 6 H + 1 Q | 0 | 0 | 6 H + 1 Q |
| P3 | 5 H + 2 Q | 0 | 0 | 5 H + 2 Q |
| P2 | 6 H + 1 Q | 0 | 0 | 6 H + 1 Q |
| P1 | 5 H + 2 Q | 0 | 0 | 5 H + 2 Q |
| **total** | 44 H + 10 Q | **12** (11 H + 1 Q) | **1** (Q) | **41** (33 H + 8 Q) |

Errors: none. All 12 certified records have lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT` (heap 8000 MB).

P6_9-13 (Q, list cap 2400 s) ran with a cap of only 773 s, shortened by the time left before END, and stopped at
766.6 s with UNKNOWN. It is not a genuine timeout at its list cap.

Certified units (min / median / max):
- solve: 24.2 / 304.3 / 824.4 s (the Q unit P7_2-3 is the max; H units 24.2–516.8 s)
- lrat-check: 10.7 / 44.8 / 52.2 s
- cake_lpr: 111.1 / 284.8 / 327.4 s
- proof size: 0.22 / 3.26 / 3.91 GB (215 191 854 / 3 263 189 028 / 3 914 441 159 bytes)

## Memory, SAT, rejections
- Largest solver RSS: 4403 MB (P7_2-4-15). No memory problem; cake_lpr never needed the 11000 MB retry.
- No SAT, no proof rejection.
