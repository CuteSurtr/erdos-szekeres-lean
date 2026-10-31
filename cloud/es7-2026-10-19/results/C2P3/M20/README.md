# C2P3 M20 (LIST C2P3.tsv, j = 20, N = 50, H = 2.5, task commit 4f653319)

## Tools and checks
- I built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc with the E2 patch) with `C2P/vendor/build_tools.sh`, using only the vendored `tools-src.tar.xz`. All 196 manifest hashes match, and nothing was downloaded.
- Sanity checks: lrat-check and cake_lpr both reject the bad LRAT and both accept the good one. The cake_lpr example prints `s VERIFIED UNSAT`.
- The base CNF header is `p cnf 838032 16653336`. The sha256 of base.cnf and of base.json match the expected values.
- The cubes P1..P8 are byte-identical to `C2P/cubes/P*_cubes.txt`.
- Details are in `tools.txt`.

## Units (10 assigned; idx ≡ 20 mod 50)
| case | kind | certified | timed out | not reached | errors |
|---|---|---|---|---|---|
| P6 | Q | 1 (P6_3-9) | 0 | 0 | 0 |
| P6 | H | 3 (P6_1-12-14, P6_3-8-12, P6_8-10-13) | 0 | 0 | 0 |
| P5 | H | 3 (P5_1-4-10, P5_1-11-14, P5_2-8-12) | 0 | 2 (P5_6-7-16, P5_9-11-13) | 0 |
| P5 | Q | 0 | 0 | 1 (P5_7-9) | 0 |
| **total** | | **7** | **0** | **3** | **0** |

All 7 records are UNSATISFIABLE with `"certified": true`: lrat-check gave `c VERIFIED` and cake_lpr gave `s VERIFIED UNSAT`. Some caps were cut by END (P5_1-11-14 to 1368 s and P5_2-8-12 to 692 s); both units still finished within the cut cap. The lane stopped at 11:53:08Z with 275 s left before END, so it started no further units.

| unit | case | kind | cap s | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|
| P6_3-9 | P6 | Q | 6000 | 2833.31 | 85.3 | 505.4 | 6.08 | 4379 |
| P6_1-12-14 | P6 | H | 1800 | 269.81 | 46.0 | 292.9 | 3.23 | 4454 |
| P6_3-8-12 | P6 | H | 1800 | 498.08 | 49.3 | 327.4 | 3.51 | 4408 |
| P6_8-10-13 | P6 | H | 1800 | 26.21 | 11.4 | 104.6 | 0.22 | 2646 |
| P5_1-4-10 | P5 | H | 1800 | 499.78 | 51.0 | 329.9 | 3.48 | 4370 |
| P5_1-11-14 | P5 | H | 1368 | 293.27 | 49.7 | 321.2 | 3.24 | 4365 |
| P5_2-8-12 | P5 | H | 692 | 606.56 | 54.1 | 341.0 | 3.60 | 4409 |

Certified units, as minimum / median / maximum:
- solve: 26.21 / 498.08 / 2833.31 s
- lrat-check: 11.4 / 49.7 / 85.3 s
- cake_lpr: 104.6 / 327.4 / 505.4 s
- proof: 0.22 / 3.48 / 6.08 GB

## Resources
- The largest solver RSS was 4454 MB, on a machine with 15 GB.
- There were no memory problems, and peak disk use stayed below the 29 GB free.

## SAT, rejections, errors
None. No unit returned SAT, no proof was rejected, and no record has an ERROR status.
