# C2P3 M07 (LIST = C2P3.tsv, j = 7, N = 50, H = 2.5, Z = 4f653319)

Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-31 09:42:49 UTC (epoch 1793439769), END = 1793447869 (11:57:49 UTC). Lane started 09:45:53Z and ended on its own at 11:51:56Z ("stop: 352 s left").

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built from the vendored `tools-src.tar.xz`: manifest OK (all 196 files match). CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch. Nothing was cloned or downloaded.
- Sanity checks: both checkers reject the bad LRAT and accept the good one. The cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. sha256 matches for base.cnf (b0061e90…) and base.json (2476faff…).
- Cubes: P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, idx ≡ 7 mod 50: 10 units)
| unit | case | kind | cap s | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|
| P7_8-13 | P7 | Q | 6000 | 3073.11 | 108.6 | 574.9 | 6.76 | 4479 |
| P6_1-5-9 | P6 | H | 1800 | 467.76 | 63.6 | 341.0 | 3.46 | 4381 |
| P6_2-14-15 | P6 | H | 1800 | 268.62 | 57.1 | 336.2 | 3.19 | 4356 |
| P6_7-12-14 | P6 | H | 1800 | 208.41 | 56.6 | 311.8 | 3.09 | 4377 |
| P5_1-3-9 | P5 | H | 1363* | 329.82 | 54.8 | 312.5 | 3.30 | 4401 |
| P5_1-9-14 | P5 | H | 654* | 482.01 | 59.8 | 346.2 | 3.60 | 4365 |

\* The lane reduced the cap so that 10 minutes remained before END for the checks.

- **Certified (UNSAT, both checkers accepted): 6.** By case and kind: P7 Q 1, P6 H 3, P5 H 2.
- **Timed out (UNKNOWN): 0.**
- **Not reached: 4**, all P5 H: P5_2-7-8, P5_2-14-16, P5_6-13-15, P5_8-11-12.
- **Errors / `certified: false`: 0.**
- Certified min / median / max: solve 208.4 / 398.8 / 3073.1 s; lrat-check 54.8 / 58.5 / 108.6 s; cake_lpr 311.8 / 338.6 / 574.9 s; proof size 3.09 / 3.38 / 6.76 GB.
- Largest solver RSS: 4479 MB (P7_8-13). cake_lpr ran with an 8000 MB heap.
- No SAT, no proof rejection, no memory problem. All proofs were deleted after the checks, and no CNF or proof file is committed.
