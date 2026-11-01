# C2P / M20 (LIST C2P.tsv, shard j = 20 of N = 42, H = 3.0, Z = 01909a07)

Start 2026-10-31 03:22:52 UTC, END 06:07:52 UTC. This run replaces an earlier attempt (TASK at fb2c59af) that
stopped at step 1 because the tool build was refused there.

## Tools and checks (`tools.txt`)
- Built by `C2P/vendor/build_tools.sh` from the vendored sources (manifest: all 196 files match). Nothing was cloned or
  downloaded. Commits: CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check from drat-trim 2e3b2dc with the E2 patch.
- Sanity checks as expected. Both checkers reject the bad LRAT and accept the good one, and the cake_lpr example
  prints `s VERIFIED UNSAT`.
- Base CNF header `p cnf 838032 16653336`. The sha256 of base.cnf and of base.json both match.
- P1..P8 cube files are byte-identical to `C2P/cubes/` (560 lines each).

## Units (`units.tsv`: 53 units, idx ≡ 20 mod 42; 42 H, 11 Q, no cover)
| case | units | certified | timed out (UNKNOWN) | not reached |
|---|---|---|---|---|
| P8 | 5 (3 H, 2 Q) | 4 (3 H: P8_9-13-14, P8_2-10-13, P8_4-10-13; 1 Q: P8_2-13) | 1 Q: P8_3-12 (cap 2400 s) | 0 |
| P7 | 7 (6 H, 1 Q) | 3 H: P7_3-4-11, P7_2-13-16 (cap 1133), P7_1-4-15 (cap 499) | 0 | 4 (3 H, 1 Q) |
| P6 | 7 (5 H, 2 Q) | 0 | 0 | 7 |
| P5 | 7 (6 H, 1 Q) | 0 | 0 | 7 |
| P4 | 7 (6 H, 1 Q) | 0 | 0 | 7 |
| P3 | 7 (6 H, 1 Q) | 0 | 0 | 7 |
| P2 | 6 (5 H, 1 Q) | 0 | 0 | 6 |
| P1 | 7 (5 H, 2 Q) | 0 | 0 | 7 |
| total | 53 (42 H, 11 Q) | **7** (6 H, 1 Q) | **1** (Q) | **45** (36 H, 9 Q) |

There were no errors. Every UNSAT record has `"certified": true`, with lrat-check `c VERIFIED` and cake_lpr
`s VERIFIED UNSAT` on the first try at heap 8000 MB.

For the 7 certified units (min / median / max):
- solve: 141.8 / 310.8 / 2235.4 s (the Q unit P8_2-13 is the 2235 s one; H units are 141.8–438.4 s);
- lrat-check: 38.3 / 55.3 / 92.9 s;
- cake_lpr: 233.7 / 315.9 / 524.9 s;
- proof size: 2.16 / 3.25 / 5.84 GB (2161761377 / 3251052530 / 5840492619 bytes). The proofs were deleted after
  checking; their sha256 values are in `out.jsonl`.

The lane stopped at 06:00:15 UTC with 456 s left before END, which is under the 900 s minimum for starting a unit.
The first unit not reached is P7_2-9 (idx 356).

## Memory, SAT and rejections
- Largest solver RSS: 4462.7 MB (P8_2-10-13). cake_lpr used about 8.2 GB RSS at heap 8000 MB (seen with ps). The
  15 GB machine had no memory problem.
- No SAT. No proof was rejected.
