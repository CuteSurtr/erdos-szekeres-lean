# C2P5 M84: list C2P5B.tsv, shard 34 of 50 (H = 5.25 h, TASK commit 81cb025f)

## Tools and checks
- Tools built by `C2P/vendor/build_tools.sh` from the vendored `vendor/tools-src.tar.xz` (no clones or downloads). The manifest check passed for all 196 files. CaDiCaL is 3.0.1. Commits: c6073042 (CaDiCaL), a36874a8 (cake_lpr), 2e3b2dc (lrat-check with the E2 patch).
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. sha256 b0061e90…d8ff1 (base.cnf) and 2476faff…bf472b48 (base.json), both as expected.
- Cubes P1..P8 are byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Full details are in `tools.txt`.

## Units (14 = rows of C2P5B.tsv with idx ≡ 34 mod 50)
| case | kind | units | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|---|
| P2 | Q | 1 | 1 | 0 | 0 | 0 |
| P2 | H | 6 | 6 | 0 | 0 | 0 |
| P1 | Q | 1 | 1 | 0 | 0 | 0 |
| P1 | H | 4 | 4 | 0 | 0 | 0 |
| P3 | Q | 2 | 2 | 0 | 0 | 0 |
| **all** | | **14** | **14** | 0 | 0 | 0 |

All 14 units are UNSATISFIABLE and certified: lrat-check printed `c VERIFIED` and cake_lpr printed `s VERIFIED UNSAT` for every one.

| unit | case | kind | solve s | lrat-check s | cake_lpr s | proof GB | solver RSS MB |
|---|---|---|---|---|---|---|---|
| P2_5-9 | P2 | Q | 762.4 | 66.6 | 380.2 | 3.74 | 4418 |
| P1_4-7 | P1 | Q | 515.0 | 57.2 | 344.7 | 3.39 | 4413 |
| P2_1-4-14 | P2 | H | 439.1 | 65.0 | 368.9 | 3.51 | 4369 |
| P2_3-4-16 | P2 | H | 344.0 | 63.1 | 344.4 | 3.46 | 4418 |
| P2_3-8-16 | P2 | H | 486.4 | 59.7 | 353.0 | 3.62 | 4419 |
| P2_4-6-12 | P2 | H | 213.4 | 54.8 | 321.9 | 3.13 | 4396 |
| P2_5-6-10 | P2 | H | 28.2 | 15.2 | 124.2 | 0.22 | 2648 |
| P2_6-8-12 | P2 | H | 31.2 | 14.1 | 123.0 | 0.22 | 2646 |
| P1_2-5-12 | P1 | H | 372.3 | 56.5 | 333.8 | 3.38 | 4366 |
| P1_2-12-15 | P1 | H | 339.0 | 58.2 | 344.2 | 3.46 | 4382 |
| P1_3-9-11 | P1 | H | 115.6 | 31.0 | 195.8 | 1.45 | 3412 |
| P1_4-10-11 | P1 | H | 85.5 | 26.6 | 174.7 | 1.13 | 3137 |
| P3_1-2 | P3 | Q | 970.8 | 75.0 | 389.7 | 4.20 | 4380 |
| P3_8-9 | P3 | Q | 452.1 | 61.5 | 341.4 | 3.29 | 4402 |

Minimum / median / maximum over the certified units:
- solve: 28.2 / 358.2 / 970.8 s
- lrat-check: 14.1 / 57.7 / 75.0 s
- cake_lpr: 123.0 / 342.8 / 389.7 s
- proof size: 0.22 / 3.39 / 4.20 GB

The largest solver RSS was 4419 MB (P2_3-8-16). cake_lpr ran with an 8000 MB heap and used about 8.2 GB RSS.

## Problems
None. There was no SAT, no proof rejection, no ERROR status and no memory problem. The lane started at 15:13:42Z, finished all units at 18:03:03Z (well before END = 1793477472) and exited normally.
