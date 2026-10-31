# C2P / M41 (LIST C2P.tsv, shard j = 41 of N = 42, H = 3.0, Z = 01909a07)

Restart of the earlier M41 attempt (TASK at fb2c59af), which had stopped at step 1; its files were replaced.

## Tools and checks (`tools.txt`)
- `vendor/build_tools.sh` from the vendored sources: manifest 196/196 files match; CaDiCaL c6073042 (3.0.1),
  cake_lpr a36874a8, lrat-check 2e3b2dc + E2 patch. Nothing cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 of base.cnf and base.json both match.
- Cubes P1..P8: byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Lane (`run.sh`)
START 03:23:14Z (1793416994), END 06:08:14Z (1793426894). Lane started 03:26:29Z, stopped 05:53:50Z
("863 s left", below the 900 s start threshold).

## Units (53: 43 H, 10 Q, no cover)
| case | units | certified | UNKNOWN | errors | not reached |
|---|---|---|---|---|---|
| P8 | 5 H | 5 H | 0 | 0 | 0 |
| P7 | 5 H + 2 Q | 5 H + 2 Q | 0 | 0 | 0 |
| P1 | 6 H + 1 Q | 0 | 0 | 0 | 6 H + 1 Q |
| P2 | 5 H + 2 Q | 0 | 0 | 0 | 5 H + 2 Q |
| P3 | 6 H + 1 Q | 0 | 0 | 0 | 6 H + 1 Q |
| P4 | 6 H + 1 Q | 0 | 0 | 0 | 6 H + 1 Q |
| P5 | 5 H + 2 Q | 0 | 0 | 0 | 5 H + 2 Q |
| P6 | 5 H + 1 Q | 0 | 0 | 0 | 5 H + 1 Q |
| **total** | 53 | **12** (10 H, 2 Q) | 0 | 0 | 41 (33 H, 8 Q) |

All 12 run units were UNSAT and certified by both lrat-check (`c VERIFIED`) and cake_lpr (`s VERIFIED UNSAT`,
heap 8000 MB, no retry needed).

Certified units (min / median / max):
- solve: 71.5 / 261.1 / 1677.6 s (all 12); H: 71.5 / 258.2 / 318.5 s; Q: P7_8-9 602.1 s, P7_3-15 1677.6 s
- lrat-check: 24.3 / 52.3 / 82.3 s
- cake_lpr: 160.1 / 302.7 / 458.2 s
- proof size: 1.11 / 3.23 / 5.24 GB (deleted after checking; sizes and sha256 in `out.jsonl`)

Largest solver RSS: 4411 MB (P7_2-4-9). cake_lpr peaked around 8.2 GB RSS; free memory never ran out.

No SAT, no proof rejection, no ERROR, no timeout, no memory problem.
