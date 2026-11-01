# C2P3 M43

V = M43, LIST = C2P3.tsv, j = 43, N = 50, H = 2.5, Z = 4f653319. Start 2026-10-31 09:42:45 UTC (1793439765), END 11:57:45 UTC (1793447865). Machine: 4 cores, 15 GB RAM, no swap (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: built from the vendored `tools-src.tar.xz` (manifest: all 196 files match). CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch. Nothing was cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one. The cake_lpr example prints `s VERIFIED UNSAT`.
- Base: `p cnf 838032 16653336`. sha256 base.cnf b0061e90…8ff1 and base.json 2476faff…2b48, both as expected.
- Cubes: P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (9: idx ≡ 43 mod 50)
| unit | case | kind | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|
| P6_7-10 | P6 | Q | certified UNSAT | 718.95 | 62.3 | 362.1 | 3.79 | 4401 |
| P6_2-9-13 | P6 | H | certified UNSAT | 499.82 | 59.5 | 339.1 | 3.57 | 4369 |
| P6_7-9-14 | P6 | H | certified UNSAT | 116.56 | 30.1 | 194.0 | 1.60 | 3406 |
| P5_1-2-7 | P5 | H | certified UNSAT | 246.18 | 49.4 | 292.3 | 3.21 | 4402 |
| P5_1-8 | P5 | Q | UNKNOWN (timeout, cap 2400) | 2375.31 | – | – | – | 4415 |
| P5_2-3-10 | P5 | H | certified UNSAT | 359.72 | 56.7 | 316.8 | 3.32 | 4360 |
| P5_2-11-14 | P5 | H | certified UNSAT | 324.22 | 53.0 | 312.2 | 3.33 | 4388 |
| P5_6-10-15 | P5 | H | certified UNSAT (cap reduced to 474 by the END rule) | 335.05 | 53.7 | 323.2 | 3.34 | 4359 |
| P5_7-14 | P5 | Q | not reached (lane stopped at 11:51:53 with 351 s left) | – | – | – | – | – |

Counts by case and kind:
- P6: Q 1 certified; H 2 certified.
- P5: H 4 certified; Q 1 timed out (P5_1-8) and 1 not reached (P5_7-14).
- Total: 7 certified, 1 UNKNOWN, 1 not reached, 0 errors.

For the 7 certified units (min / median / max):
- solve: 116.56 / 335.05 / 718.95 s
- lrat-check: 30.1 / 53.7 / 62.3 s
- cake_lpr: 194.0 / 316.8 / 362.1 s
- proof size: 1.60 / 3.33 / 3.79 GB

Every certified record has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`. The proofs were deleted after checking.

## Other
- The largest solver RSS was 4415 MB (P5_1-8). There were no memory problems.
- There was no SAT and no proof rejection, and no records with `certified: false` or ERROR.
- Files: `out.jsonl`, `lane.log.tail`, `units.tsv`, `run.sh`, `tools.txt`, `env.txt`.
