# C2P3 M36 (LIST = C2P3.tsv, j = 36, N = 50, H = 2.5, task commit 4f653319)

## Tools and checks
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 of base.cnf and base.json match the expected values.
- Cubes P1..P8: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details in `tools.txt`.

## Units (10 assigned, idx ≡ 36 mod 50)

| unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P6_2-13 | P6 | Q | 6000 | UNSAT, certified | 2442.96 | 97.5 | 505.2 | 5971270409 | 4378 |
| P6_10-13 | P6 | Q | 4800 (lane cap 4321) | UNSAT, certified | 694.77 | 59.6 | 344.3 | 3817481091 | 4353 |
| P6_2-8-9 | P6 | H | 1800 | UNSAT, certified | 312.81 | 52.2 | 308.3 | 3268351401 | 4359 |
| P6_7-8-14 | P6 | H | 1800 | UNSAT, certified | 109.93 | 29.6 | 190.2 | 1572779959 | 3404 |
| P6_9-12-13 | P6 | H | 1800 | UNSAT, certified | 28.21 | 12.3 | 105.1 | 216433951 | 2671 |
| P5_1-7-10 | P5 | H | 1800 | UNSAT, certified | 379.55 | 54.8 | 343.3 | 3420425864 | 4368 |
| P5_1-15-16 | P5 | H | 1800 (lane cap 1249) | UNSAT, certified | 216.59 | 49.7 | 291.2 | 3150061164 | 4396 |
| P5_2-10-13 | P5 | H | 1800 (lane cap 683) | UNSAT, certified | 357.11 | 52.7 | 327.8 | 3415292246 | 4459 |
| P5_6-9-15 | P5 | H | 1800 | not reached | | | | | |
| P5_7-11-14 | P5 | H | 1800 | not reached | | | | | |

Counts:
- Certified 8: P6 Q 2, P6 H 3, P5 H 3.
- Timed out (UNKNOWN): 0.
- Not reached 2: P5 H 2 (P5_6-9-15, P5_7-11-14); the lane stopped at 11:48:43Z with 534 s left before END.
- Errors / `certified: false`: 0.

Certified (min / median / max):
- solve: 28.21 / 334.96 / 2442.96 s
- lrat-check: 12.3 / 52.45 / 97.5 s
- cake_lpr: 105.1 / 318.05 / 505.2 s
- proof: 0.22 / 3.34 / 5.97 GB

Largest solver RSS: 4459 MB (P5_2-10-13). No SAT, no proof rejection, no memory or disk problem (free disk never below 22 GB).
