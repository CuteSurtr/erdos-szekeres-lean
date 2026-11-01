# C3W6 / P11: shard 11 of 44 of W6.tsv

**Result: all 94 of my units were certified at cap 900 (both checkers). No timeouts, so no split records. No SAT. No proof rejection. No memory problem. No unit ended early without a certificate.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 05:31:50 UTC, END 09:46:50 UTC (start + 4.5 h − 15 min). The lanes started at 05:34:22 and finished all their units by 09:10:38 (lane 1 at 08:48:49, lane 0 at 08:58:04, lane 2 at 09:10:38), so nothing was killed at END.

- Tools: worktree of cad4e050 at `/opt/c3u2`, TOOLS = `results/C3U2/tools`, unmodified. I did not run `compose.py`.
- CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (its example prints `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch. Sanity check: both checkers reject the LRAT `3 0 0` on {1},{-1} and both accept `3 0 1 2 0`.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Units: the rows of `C3W6/lists/W6.tsv` with row ≡ 11 (mod 44), 94 units (`units.tsv`). No seeding.
- 3 lanes (`lane0.sh`, `lane1.sh`, `lane2.sh`, each started with `setsid nohup`). Lane k ran the positions ≡ k (mod 3) with `close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`. `killer.sh` was set to kill the lane process groups at END; it was never needed. Details are in `tools.txt`.
- `out.jsonl` holds lane 0, then lane 1, then lane 2: 94 solve records, all UNSATISFIABLE with `lrat_check: c VERIFIED` and `cake_lpr: s VERIFIED UNSAT`. There is no `recheck.jsonl` because no recheck was needed.

## Solve times of the certified units (s, cap 900, 3 solves in parallel on 4 cores)

min 23.9, Q1 166.4, median 358.4, Q3 479.5, p90 571.0, max 674.5. **54 of 94 were certified above 300 s**, so cap 300 would have timed them out. Check time: median 52.2 s, max 77.4 s. Total solve 31,810 s, total check 4,797 s.

Seven units solved in under 72 s (23.9–69.8 s). All seven have certificates (UNSAT, both checkers), so none of them is a case that the task asks to report.

## Totals per stratum

| stratum | units | certified | timed out at 900 | not reached | solve s | check s |
|---|---|---|---|---|---|---|
| H3/two | 76 | 76 | 0 | 0 | 26252 | 3933 |
| H6(1,1)/one | 2 | 2 | 0 | 0 | 936 | 105 |
| H6(2,1)/one | 3 | 3 | 0 | 0 | 1374 | 165 |
| H6(3,1)/one | 3 | 3 | 0 | 0 | 1259 | 152 |
| H6(4,0)/one | 1 | 1 | 0 | 0 | 105 | 58 |
| H6(5,0)/one | 3 | 3 | 0 | 0 | 249 | 114 |
| H6(5,1)/one | 4 | 4 | 0 | 0 | 1262 | 196 |
| H6(5,1)/two | 2 | 2 | 0 | 0 | 374 | 74 |
| all | 94 | 94 | 0 | 0 | 31810 | 4797 |

## Totals per prior

| prior | units | certified | timed out at 900 | not reached | solve s | check s |
|---|---|---|---|---|---|---|
| never_ran | 9 | 9 | 0 | 0 | 3415 | 459 |
| presplit | 56 | 56 | 0 | 0 | 15747 | 2650 |
| timeout300 | 29 | 29 | 0 | 0 | 12648 | 1688 |

## Per unit

| row | lane | unit | stratum | prior | result | solve s | check s |
|---|---|---|---|---|---|---|---|
| 11 | 0 | `0s0_1s0-10s0__2s1-3s1-4s1-5s0-6s0-7s0` | H3/two | timeout300 | certified | 253.2 | 64.6 |
| 55 | 1 | `0s0_1s0-2s0__3s1-4s0-5s1-6s0-7s1-8s0` | H3/two | presplit | certified | 37.0 | 43.3 |
| 99 | 2 | `0s0_1s0-2s1__3s0-4s1-5s1-6s1-7s0-8s1` | H3/two | timeout300 | certified | 446.9 | 73.5 |
| 143 | 0 | `0s0_1s0-3s1__2s1-4s0-5s0-6s1-7s1-8s1` | H3/two | timeout300 | certified | 487.2 | 76.7 |
| 187 | 1 | `0s0_1s0-4s1__2s1-3s0-5s0-6s0-7s1-8s1` | H3/two | timeout300 | certified | 472.0 | 73.9 |
| 231 | 2 | `0s0_1s0-5s1__2s1-3s0-4s1-6s1-7s0-8s1` | H3/two | timeout300 | certified | 537.5 | 75.1 |
| 275 | 0 | `0s0_1s0-7s0__2s1-3s0-4s0-5s0-6s1-8s1` | H3/two | timeout300 | certified | 262.2 | 64.0 |
| 319 | 1 | `0s0_1s1-2s0__3s0-4s1-5s0-6s0-7s0-8s0` | H3/two | timeout300 | certified | 394.0 | 70.5 |
| 363 | 2 | `0s0_1s1-2s0__3s1-4s1-5s1-6s1-7s0-8s0` | H3/two | timeout300 | certified | 410.2 | 56.1 |
| 407 | 0 | `0s0_1s1-5s0__2s1-3s0-4s0-6s0-7s0-8s1` | H3/two | timeout300 | certified | 277.6 | 60.4 |
| 451 | 1 | `0s0_1s1-5s1__2s0-3s1-4s0-6s0-7s0-8s0` | H3/two | presplit | certified | 165.9 | 51.9 |
| 495 | 2 | `0s0_1s1-5s1__2s1-3s1-4s1-6s1-7s0-8s0` | H3/two | presplit | certified | 323.4 | 57.2 |
| 539 | 0 | `0s0_1s1-7s1__2s1-3s1-4s1-5s0-6s0-8s0` | H3/two | timeout300 | certified | 358.1 | 59.1 |
| 583 | 1 | `0s0_1s1-8s0__2s1-3s0-4s0-5s1-6s0-7s0` | H3/two | presplit | certified | 84.5 | 52.9 |
| 627 | 2 | `0s0_1s1-8s1__2s1-3s0-4s1-5s0-6s1-7s1` | H3/two | timeout300 | certified | 565.0 | 53.8 |
| 671 | 0 | `0s0_1s1-9s1__2s1-3s0-4s0-5s1-6s0-7s1` | H3/two | never_ran | certified | 440.2 | 49.0 |
| 715 | 1 | `0s0_2s0-3s1__1s0-4s1-5s0-6s0-7s0-8s1` | H3/two | presplit | certified | 460.0 | 77.4 |
| 759 | 2 | `0s0_2s0-3s1__1s1-4s1-5s1-6s1-7s0-8s1` | H3/two | presplit | certified | 574.1 | 53.9 |
| 803 | 0 | `0s0_2s0-4s1__1s1-3s0-5s1-6s0-7s0-8s1` | H3/two | presplit | certified | 548.7 | 55.8 |
| 847 | 1 | `0s0_2s0-5s0__1s0-3s1-4s0-6s1-7s0-8s1` | H3/two | presplit | certified | 58.7 | 30.2 |
| 891 | 2 | `0s0_2s0-5s1__1s0-3s0-4s1-6s0-7s0-8s0` | H3/two | timeout300 | certified | 310.3 | 43.9 |
| 935 | 0 | `0s0_2s0-5s1__1s1-3s1-4s0-6s1-7s0-8s0` | H3/two | timeout300 | certified | 549.9 | 55.8 |
| 979 | 1 | `0s0_2s0-6s1__1s1-3s0-4s0-5s0-7s1-8s0` | H3/two | timeout300 | certified | 399.4 | 50.7 |
| 1023 | 2 | `0s0_2s0-7s0__1s0-3s0-4s1-5s1-6s1-8s0` | H3/two | presplit | certified | 108.6 | 34.8 |
| 1067 | 0 | `0s0_2s0-7s0__1s1-3s1-4s1-5s0-6s1-8s0` | H3/two | presplit | certified | 165.4 | 49.6 |
| 1111 | 1 | `0s0_2s0-7s1__1s1-3s0-4s0-5s1-6s1-8s0` | H3/two | presplit | certified | 253.3 | 41.7 |
| 1155 | 2 | `0s0_2s0-8s0__1s1-3s0-4s0-5s1-6s0-7s0` | H3/two | presplit | certified | 249.6 | 41.8 |
| 1199 | 0 | `0s0_2s1-3s0__1s0-4s1-5s0-6s0-7s0-8s1` | H3/two | timeout300 | certified | 421.2 | 49.1 |
| 1243 | 1 | `0s0_2s1-3s0__1s1-4s1-5s1-6s1-7s0-8s1` | H3/two | timeout300 | certified | 618.7 | 61.1 |
| 1287 | 2 | `0s0_2s1-3s1__1s1-4s0-5s1-6s0-7s0-8s1` | H3/two | presplit | certified | 67.4 | 25.6 |
| 1331 | 0 | `0s0_2s1-4s0__1s0-3s1-5s1-6s0-7s1-8s0` | H3/two | timeout300 | certified | 585.3 | 56.3 |
| 1375 | 1 | `0s0_2s1-5s0__1s0-3s0-4s0-6s1-7s1-8s1` | H3/two | presplit | certified | 302.7 | 45.8 |
| 1419 | 2 | `0s0_2s1-5s0__1s1-3s1-4s0-6s0-7s1-8s1` | H3/two | presplit | certified | 624.4 | 59.6 |
| 1463 | 0 | `0s0_2s1-6s0__1s0-3s1-4s1-5s1-7s1-8s1` | H3/two | presplit | certified | 297.6 | 42.7 |
| 1507 | 1 | `0s0_2s1-6s1__1s0-3s0-4s1-5s0-7s1-8s1` | H3/two | presplit | certified | 166.5 | 37.4 |
| 1551 | 2 | `0s0_2s1-6s1__1s1-3s1-4s0-5s1-7s1-8s1` | H3/two | presplit | certified | 233.5 | 45.0 |
| 1595 | 0 | `0s0_2s1-7s0__1s1-3s0-4s1-5s0-6s1-8s1` | H3/two | never_ran | certified | 404.8 | 49.4 |
| 1639 | 1 | `0s0_2s1-7s1__1s1-3s1-4s0-5s0-6s0-8s1` | H3/two | never_ran | certified | 281.7 | 43.0 |
| 1683 | 2 | `0s0_2s1-8s1__1s1-3s0-4s0-5s1-6s1-7s0` | H3/two | presplit | certified | 505.7 | 56.2 |
| 1727 | 0 | `0s0_2s1-9s0__1s0-3s1-4s0-5s0-6s1-7s0` | H3/two | presplit | certified | 87.3 | 31.7 |
| 1771 | 1 | `0s0_2s1-9s0__1s1-3s1-4s1-5s1-6s1-7s0` | H3/two | presplit | certified | 135.9 | 36.3 |
| 1815 | 2 | `0s0_3s0-4s1__1s1-2s0-5s1-6s0-7s1-8s0` | H3/two | presplit | certified | 567.8 | 56.1 |
| 1859 | 0 | `0s0_3s0-5s0__1s0-2s1-4s0-6s1-7s1-8s0` | H3/two | presplit | certified | 65.8 | 31.0 |
| 1903 | 1 | `0s0_3s0-5s1__1s0-2s0-4s1-6s0-7s1-8s0` | H3/two | timeout300 | certified | 533.2 | 55.9 |
| 1947 | 2 | `0s0_3s0-5s1__1s1-2s1-4s1-6s0-7s0-8s0` | H3/two | timeout300 | certified | 422.2 | 52.3 |
| 1991 | 0 | `0s0_3s0-6s0__1s1-2s0-4s0-5s1-7s0-8s0` | H3/two | presplit | certified | 69.8 | 35.8 |
| 2035 | 1 | `0s0_3s0-6s1__1s0-2s1-4s0-5s0-7s0-8s0` | H3/two | timeout300 | certified | 446.7 | 75.1 |
| 2079 | 2 | `0s0_3s0-6s1__1s1-2s1-4s1-5s1-7s0-8s0` | H3/two | never_ran | certified | 452.5 | 69.8 |
| 2123 | 0 | `0s0_3s0-7s0__1s1-2s0-4s1-5s0-6s0-8s0` | H3/two | presplit | certified | 101.1 | 53.5 |
| 2167 | 1 | `0s0_3s0-7s1__1s0-2s1-4s0-5s1-6s0-8s0` | H3/two | presplit | certified | 431.4 | 52.5 |
| 2211 | 2 | `0s0_3s0-8s0__1s0-2s1-4s0-5s1-6s1-7s0` | H3/two | presplit | certified | 196.7 | 40.9 |
| 2255 | 0 | `0s0_3s0-8s1__1s0-2s0-4s1-5s1-6s1-7s1` | H3/two | timeout300 | certified | 324.2 | 44.2 |
| 2299 | 1 | `0s0_3s1-4s0__1s0-2s1-5s0-6s0-7s1-8s1` | H3/two | timeout300 | certified | 483.8 | 49.1 |
| 2343 | 2 | `0s0_3s1-4s0__1s1-2s1-5s1-6s1-7s1-8s1` | H3/two | never_ran | certified | 482.7 | 51.9 |
| 2387 | 0 | `0s0_3s1-4s1__1s1-2s0-5s1-6s0-7s1-8s1` | H3/two | presplit | certified | 76.5 | 44.0 |
| 2431 | 1 | `0s0_3s1-5s0__1s0-2s1-4s0-6s1-7s1-8s1` | H3/two | presplit | certified | 501.0 | 57.2 |
| 2475 | 2 | `0s0_3s1-5s1__1s0-2s0-4s0-6s0-7s1-8s1` | H3/two | presplit | certified | 143.6 | 34.0 |
| 2519 | 0 | `0s0_3s1-5s1__1s1-2s0-4s1-6s1-7s1-8s1` | H3/two | presplit | certified | 95.0 | 32.8 |
| 2563 | 1 | `0s0_3s1-7s0__1s1-2s0-4s1-5s0-6s0-8s1` | H3/two | never_ran | certified | 299.3 | 44.0 |
| 2607 | 2 | `0s0_3s1-7s1__1s1-2s1-4s1-5s0-6s1-8s1` | H3/two | timeout300 | certified | 299.5 | 41.5 |
| 2651 | 0 | `0s0_3s1-8s0__1s1-2s0-4s1-5s0-6s0-7s0` | H3/two | presplit | certified | 179.8 | 38.3 |
| 2695 | 1 | `0s0_4s0-5s1__1s0-2s1-3s0-6s1-7s0-8s0` | H3/two | presplit | certified | 468.6 | 60.5 |
| 2739 | 2 | `0s0_4s0-6s1__1s0-2s0-3s0-5s0-7s0-8s0` | H3/two | presplit | certified | 224.0 | 55.2 |
| 2783 | 0 | `0s0_4s0-6s1__1s1-2s0-3s1-5s1-7s0-8s0` | H3/two | presplit | certified | 497.9 | 55.0 |
| 2827 | 1 | `0s0_4s0-7s0__1s0-2s1-3s1-5s0-6s0-8s0` | H3/two | presplit | certified | 111.6 | 38.6 |
| 2871 | 2 | `0s0_4s0-7s1__1s0-2s0-3s1-5s1-6s0-8s1` | H3/two | presplit | certified | 596.2 | 63.6 |
| 2915 | 0 | `0s0_4s0-7s1__1s1-2s1-3s1-5s0-6s0-8s1` | H3/two | presplit | certified | 616.6 | 58.0 |
| 2959 | 1 | `0s0_4s1-5s0__1s1-2s0-3s0-6s1-7s0-8s1` | H3/two | never_ran | certified | 479.4 | 54.4 |
| 3003 | 2 | `0s0_4s1-6s0__1s0-2s0-3s1-5s0-7s0-8s0` | H3/two | presplit | certified | 413.7 | 50.3 |
| 3047 | 0 | `0s0_4s1-6s0__1s1-2s1-3s0-5s1-7s0-8s0` | H3/two | presplit | certified | 594.0 | 58.8 |
| 3091 | 1 | `0s0_4s1-6s1__1s1-2s0-3s0-5s0-7s0-8s0` | H3/two | presplit | certified | 138.1 | 59.2 |
| 3135 | 2 | `0s0_4s1-7s0__1s0-2s0-3s1-5s1-6s0-8s0` | H3/two | presplit | certified | 458.4 | 53.4 |
| 3179 | 0 | `0s0_4s1-7s0__1s1-2s1-3s1-5s0-6s0-8s0` | H3/two | presplit | certified | 467.0 | 76.2 |
| 3223 | 1 | `0s0_5s0-6s0__1s1-2s0-3s0-4s1-7s0-8s0` | H3/two | presplit | certified | 23.9 | 18.4 |
| 3267 | 2 | `0s0_5s0-6s1__1s0-2s1-3s0-4s0-7s0-8s0` | H3/two | presplit | certified | 389.5 | 50.6 |
| 3311 | 0 | `0s0_5s0-6s1__1s1-2s1-3s1-4s1-7s0-8s0` | H3/two | presplit | certified | 674.5 | 64.2 |
| 3355 | 1 | `0s0-1s1_4__2s1-3s1-5s1-6s0-7s1-8s1` | H6(1,1)/one | timeout300 | certified | 471.8 | 52.9 |
| 3399 | 2 | `0s0-1s1_5__2s1-3s1-4s0-6s0-7s1-8s1` | H6(1,1)/one | timeout300 | certified | 463.8 | 52.1 |
| 3443 | 0 | `0s0-2s1_4__1s1-3s0-5s1-6s1-7s1-8s1` | H6(2,1)/one | timeout300 | certified | 420.3 | 53.0 |
| 3487 | 1 | `0s0-2s1_5__1s1-3s0-4s1-6s0-7s0-8s0` | H6(2,1)/one | timeout300 | certified | 595.0 | 60.3 |
| 3531 | 2 | `0s0-2s1_6__1s0-3s1-4s0-5s1-7s1-8s0` | H6(2,1)/one | timeout300 | certified | 358.6 | 52.1 |
| 3575 | 0 | `0s0-3s1_4__1s0-2s1-5s0-6s0-7s0-8s0` | H6(3,1)/one | timeout300 | certified | 479.9 | 54.8 |
| 3619 | 1 | `0s0-3s1_5__1s0-2s0-4s0-6s1-7s1-8s0` | H6(3,1)/one | presplit | certified | 324.9 | 43.0 |
| 3663 | 2 | `0s0-3s1_5__1s1-2s1-4s0-6s0-7s1-8s0` | H6(3,1)/one | presplit | certified | 454.3 | 53.7 |
| 3707 | 0 | `0s0-4s0_6__1s0-2s1-3s1-5s1-7s1-8s0` | H6(4,0)/one | presplit | certified | 104.8 | 58.3 |
| 3751 | 1 | `0s0-5s0_6__1s0-2s0-3s0-4s1-7s0-8s1` | H6(5,0)/one | presplit | certified | 74.1 | 38.2 |
| 3795 | 2 | `0s0-5s0_6__1s1-2s1-3s0-4s0-7s0-8s1` | H6(5,0)/one | presplit | certified | 94.0 | 37.6 |
| 3839 | 0 | `0s0-5s0_7__1s0-2s1-3s1-4s1-6s0-8s1` | H6(5,0)/one | presplit | certified | 80.9 | 37.8 |
| 3883 | 1 | `0s0-5s1_1__2s0-3s1-4s0-6s1-7s1-8s1` | H6(5,1)/one | presplit | certified | 271.4 | 44.7 |
| 3927 | 2 | `0s0-5s1_2__1s0-3s0-4s0-6s0-7s1-8s1` | H6(5,1)/one | presplit | certified | 283.9 | 45.4 |
| 3971 | 0 | `0s0-5s1_2__1s1-3s0-4s1-6s1-7s1-8s1` | H6(5,1)/one | presplit | certified | 192.8 | 41.0 |
| 4015 | 1 | `0s0-5s1_6__1s1-2s1-3s1-4s1-7s0-8s0` | H6(5,1)/one | never_ran | certified | 513.8 | 64.8 |
| 4059 | 2 | `0s0-5s1_1s1-10s1__2s1-3s0-4s1-6s1-7s1-8s0` | H6(5,1)/two | never_ran | certified | 60.5 | 32.4 |
| 4103 | 0 | `0s0-5s1_7s0-9s1__1s0-2s1-3s0` | H6(5,1)/two | presplit | certified | 313.4 | 41.5 |

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none. No record has cake_lpr `none`, so nothing needed a recheck.
- Memory: no problem (about 2 GB used with 3 solves at once).
- Units that ended early without a certificate: none.

## Files

`env.txt`, `tools.txt`, `units.tsv`, `lane0.sh`, `lane1.sh`, `lane2.sh`, `killer.sh`, `out.jsonl`, `driver0.log.tail`, `driver1.log.tail`, `driver2.log.tail`, `README.md`.
