# C3W6 P32: shard 32 of 44 of W6.tsv, cap 900, one pass

Task: `results/C3W6/TASK.md` at c5260b44, with V = P32, LIST = W6.tsv, j = 32, N = 44, H = 4.5.
Machine: 4 cores, 15 GB (`env.txt`). Start 2026-10-25 05:31:51 UTC, lanes started 05:34:00 UTC, END 09:46:51 UTC.
All three lanes finished their units before END (09:06:24, 09:32:05, 09:10:56 UTC); nothing was killed.

## Tools and base check

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, used unmodified. `compose.py` not run.
- CaDiCaL 3.0.1 c6073042; cake_lpr a36874a8 (bundled example: `s VERIFIED UNSAT`); lrat-check 2e3b2dc with the E2 patch.
  Sanity check: LRAT `3 0 0` on {1},{-1} is rejected by both checkers, `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…0cdd6da` (matches).
- Details in `tools.txt`.

## Summary

- 93 units (`units.tsv`), 3 lanes (`lane0.sh` to `lane2.sh`), options `--jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`, no seeded records.
- **92 certified** (lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT` on every one), **1 timed out at 900 s**, 0 not reached.
- The timed-out unit is row 3024, `0s0_4s1-6s0__1s0-2s1-3s1-5s1-7s0-8s1` (H3/two, presplit). close_tree wrote its layer split record (51 children). The children were not solved, as intended, so the unit is open with 51 frontier nodes.
- No SAT, no proof rejection, no checker returning `none`, no rechecks (so there is no `recheck.jsonl`), no memory problem (at least 3 GB free at every check), and no unit ended early without a certificate.
- Solve times of the 92 certified units: min 34.0 s, Q1 149.0, median 361.0, Q3 603.5, p90 649.7, max 690.7 s. 54 were certified above 300 s.
- Check times: 24.2 to 81.8 s. Total solve 34,006 s, total check 4,880 s.
- `out.jsonl` has 94 records: lane 0, then lane 1, then lane 2. That is 93 solve records plus 1 split record.

## Totals

| group | certified | timeout900 | not reached |
|---|---|---|---|
| H3/two | 75 | 1 | 0 |
| H6(1,1)/one | 1 | 0 | 0 |
| H6(2,1)/one | 4 | 0 | 0 |
| H6(3,1)/one | 2 | 0 | 0 |
| H6(4,0)/one | 2 | 0 | 0 |
| H6(5,0)/one | 3 | 0 | 0 |
| H6(5,1)/one | 3 | 0 | 0 |
| H6(5,1)/two | 2 | 0 | 0 |
| prior:never_ran | 10 | 0 | 0 |
| prior:presplit | 56 | 1 | 0 |
| prior:timeout300 | 26 | 0 | 0 |


## Per unit

| row | node | stratum | prior | result | solve s | check s | note |
|---|---|---|---|---|---|---|---|
| 32 | `0s0_1s0-2s0__3s0-4s1-5s0-6s0-7s1-8s1` | H3/two | presplit | certified | 34.0 | 48.3 |  |
| 76 | `0s0_1s0-2s0__3s1-4s1-5s1-6s1-7s1-8s1` | H3/two | presplit | certified | 74.3 | 33.4 |  |
| 120 | `0s0_1s0-2s1__3s1-4s1-5s0-6s0-7s1-8s0` | H3/two | timeout300 | certified | 576.6 | 81.8 |  |
| 164 | `0s0_1s0-4s1__2s0-3s0-5s0-6s1-7s1-8s1` | H3/two | timeout300 | certified | 455.9 | 74.9 |  |
| 208 | `0s0_1s0-4s1__2s1-3s1-5s1-6s0-7s0-8s0` | H3/two | timeout300 | certified | 524.4 | 68.4 |  |
| 252 | `0s0_1s0-7s0__2s0-3s0-4s0-5s0-6s0-8s1` | H3/two | timeout300 | certified | 253.6 | 64.4 |  |
| 296 | `0s0_1s0-7s0__2s1-3s1-4s1-5s0-6s0-8s1` | H3/two | timeout300 | certified | 311.3 | 74.5 |  |
| 340 | `0s0_1s1-2s0__3s1-4s0-5s0-6s1-7s0-8s1` | H3/two | timeout300 | certified | 646.4 | 79.2 |  |
| 384 | `0s0_1s1-4s0__2s1-3s1-5s0-6s1-7s1-8s0` | H3/two | timeout300 | certified | 652.0 | 61.6 |  |
| 428 | `0s0_1s1-5s0__2s1-3s1-4s1-6s0-7s0-8s1` | H3/two | timeout300 | certified | 562.6 | 75.3 |  |
| 472 | `0s0_1s1-5s1__2s1-3s0-4s0-6s1-7s0-8s1` | H3/two | presplit | certified | 224.3 | 60.1 |  |
| 516 | `0s0_1s1-7s1__2s0-3s1-4s1-5s1-6s1-8s1` | H3/two | timeout300 | certified | 599.6 | 66.7 |  |
| 560 | `0s0_1s1-8s0__2s0-3s0-4s1-5s1-6s0-7s1` | H3/two | presplit | certified | 148.1 | 52.3 |  |
| 604 | `0s0_1s1-8s0__2s1-3s1-4s1-5s0-6s0-7s1` | H3/two | presplit | certified | 137.1 | 48.0 |  |
| 648 | `0s0_1s1-9s1__2s0-3s0-4s1-5s0-6s0-7s1` | H3/two | never_ran | certified | 393.4 | 56.6 |  |
| 692 | `0s0_1s1-9s1__2s1-3s1-4s1-5s0-6s1-7s0` | H3/two | never_ran | certified | 680.1 | 65.9 |  |
| 736 | `0s0_2s0-3s1__1s1-4s0-5s0-6s1-7s1-8s0` | H3/two | presplit | certified | 546.0 | 68.1 |  |
| 780 | `0s0_2s0-4s1__1s0-3s1-5s0-6s0-7s1-8s0` | H3/two | presplit | certified | 520.8 | 79.1 |  |
| 824 | `0s0_2s0-4s1__1s1-3s1-5s1-6s1-7s1-8s0` | H3/two | presplit | certified | 611.8 | 66.6 |  |
| 868 | `0s0_2s0-5s0__1s1-3s0-4s1-6s0-7s1-8s0` | H3/two | presplit | certified | 123.5 | 46.7 |  |
| 912 | `0s0_2s0-5s1__1s0-3s1-4s1-6s1-7s0-8s1` | H3/two | timeout300 | certified | 690.7 | 69.8 |  |
| 956 | `0s0_2s0-6s1__1s0-3s0-4s1-5s0-7s1-8s1` | H3/two | timeout300 | certified | 487.4 | 66.7 |  |
| 1000 | `0s0_2s0-6s1__1s1-3s1-4s0-5s1-7s1-8s1` | H3/two | timeout300 | certified | 628.3 | 64.4 |  |
| 1044 | `0s0_2s0-7s0__1s1-3s0-4s0-5s0-6s1-8s1` | H3/two | presplit | certified | 300.3 | 54.9 |  |
| 1088 | `0s0_2s0-7s1__1s0-3s0-4s1-5s1-6s1-8s1` | H3/two | presplit | certified | 357.0 | 52.7 |  |
| 1132 | `0s0_2s0-7s1__1s1-3s1-4s1-5s0-6s1-8s1` | H3/two | presplit | certified | 602.4 | 66.8 |  |
| 1176 | `0s0_2s0-8s0__1s1-3s1-4s1-5s0-6s0-7s1` | H3/two | presplit | certified | 284.9 | 49.4 |  |
| 1220 | `0s0_2s1-3s0__1s1-4s0-5s0-6s1-7s1-8s0` | H3/two | timeout300 | certified | 623.2 | 63.3 |  |
| 1264 | `0s0_2s1-3s1__1s0-4s1-5s0-6s0-7s1-8s0` | H3/two | presplit | certified | 78.8 | 49.2 |  |
| 1308 | `0s0_2s1-3s1__1s1-4s1-5s1-6s1-7s1-8s0` | H3/two | presplit | certified | 81.3 | 33.3 |  |
| 1352 | `0s0_2s1-4s0__1s1-3s1-5s0-6s0-7s0-8s0` | H3/two | timeout300 | certified | 531.1 | 60.4 |  |
| 1396 | `0s0_2s1-5s0__1s0-3s1-4s1-6s1-7s0-8s0` | H3/two | presplit | certified | 648.6 | 76.8 |  |
| 1440 | `0s0_2s1-6s0__1s0-3s0-4s1-5s0-7s0-8s0` | H3/two | presplit | certified | 302.3 | 48.5 |  |
| 1484 | `0s0_2s1-6s0__1s1-3s1-4s0-5s1-7s0-8s0` | H3/two | presplit | certified | 484.5 | 56.8 |  |
| 1528 | `0s0_2s1-6s1__1s1-3s0-4s0-5s0-7s0-8s0` | H3/two | presplit | certified | 230.5 | 42.4 |  |
| 1572 | `0s0_2s1-7s0__1s0-3s1-4s0-5s1-6s0-8s0` | H3/two | never_ran | certified | 282.7 | 45.8 |  |
| 1616 | `0s0_2s1-7s1__1s0-3s1-4s1-5s0-6s1-8s0` | H3/two | timeout300 | certified | 614.4 | 57.6 |  |
| 1660 | `0s0_2s1-8s1__1s0-3s0-4s1-5s1-6s1-7s1` | H3/two | presplit | certified | 605.2 | 57.0 |  |
| 1704 | `0s0_2s1-8s1__1s1-3s1-4s1-5s0-6s1-7s1` | H3/two | presplit | certified | 575.6 | 58.6 |  |
| 1748 | `0s0_2s1-9s0__1s1-3s0-4s0-5s1-6s1-7s1` | H3/two | presplit | certified | 306.2 | 62.3 |  |
| 1792 | `0s0_3s0-4s1__1s0-2s1-5s0-6s0-7s1-8s1` | H3/two | presplit | certified | 650.2 | 63.0 |  |
| 1836 | `0s0_3s0-4s1__1s1-2s1-5s1-6s1-7s1-8s1` | H3/two | presplit | certified | 628.7 | 59.0 |  |
| 1880 | `0s0_3s0-5s0__1s1-2s0-4s1-6s0-7s1-8s1` | H3/two | presplit | certified | 68.9 | 52.6 |  |
| 1924 | `0s0_3s0-5s1__1s1-2s0-4s0-6s0-7s0-8s1` | H3/two | timeout300 | certified | 603.9 | 61.7 |  |
| 1968 | `0s0_3s0-6s0__1s0-2s0-4s1-5s1-7s0-8s1` | H3/two | presplit | certified | 54.6 | 40.6 |  |
| 2012 | `0s0_3s0-6s0__1s1-2s1-4s1-5s0-7s0-8s1` | H3/two | presplit | certified | 155.7 | 39.5 |  |
| 2056 | `0s0_3s0-6s1__1s1-2s0-4s0-5s1-7s0-8s1` | H3/two | timeout300 | certified | 659.5 | 57.4 |  |
| 2100 | `0s0_3s0-7s0__1s0-2s1-4s0-5s0-6s0-8s1` | H3/two | presplit | certified | 258.4 | 45.8 |  |
| 2144 | `0s0_3s0-7s0__1s1-2s1-4s1-5s1-6s0-8s1` | H3/two | presplit | certified | 210.5 | 42.3 |  |
| 2188 | `0s0_3s0-7s1__1s1-2s0-4s1-5s0-6s0-8s1` | H3/two | presplit | certified | 626.4 | 58.1 |  |
| 2232 | `0s0_3s0-8s0__1s1-2s0-4s1-5s0-6s1-7s1` | H3/two | presplit | certified | 151.7 | 36.5 |  |
| 2276 | `0s0_3s0-8s1__1s1-2s1-4s1-5s0-6s1-7s0` | H3/two | timeout300 | certified | 404.3 | 49.5 |  |
| 2320 | `0s0_3s1-4s0__1s1-2s0-5s1-6s0-7s0-8s0` | H3/two | timeout300 | certified | 579.9 | 53.1 |  |
| 2364 | `0s0_3s1-4s1__1s0-2s1-5s0-6s1-7s0-8s0` | H3/two | presplit | certified | 72.1 | 43.5 |  |
| 2408 | `0s0_3s1-5s0__1s0-2s0-4s0-6s0-7s0-8s0` | H3/two | presplit | certified | 298.5 | 47.6 |  |
| 2452 | `0s0_3s1-5s0__1s1-2s0-4s1-6s1-7s0-8s0` | H3/two | presplit | certified | 685.6 | 65.4 |  |
| 2496 | `0s0_3s1-5s1__1s0-2s1-4s1-6s0-7s0-8s0` | H3/two | presplit | certified | 155.2 | 38.7 |  |
| 2540 | `0s0_3s1-6s0__1s1-2s1-4s1-5s0-7s1-8s0` | H3/two | timeout300 | certified | 624.2 | 57.8 |  |
| 2584 | `0s0_3s1-7s0__1s1-2s1-4s1-5s1-6s1-8s0` | H3/two | never_ran | certified | 612.9 | 53.3 |  |
| 2628 | `0s0_3s1-8s0__1s0-2s1-4s0-5s0-6s0-7s1` | H3/two | presplit | certified | 361.4 | 52.7 |  |
| 2672 | `0s0_3s1-8s0__1s1-2s1-4s1-5s1-6s0-7s1` | H3/two | presplit | certified | 402.3 | 48.3 |  |
| 2716 | `0s0_4s0-5s1__1s1-2s0-3s1-6s0-7s0-8s1` | H3/two | presplit | certified | 619.8 | 65.3 |  |
| 2760 | `0s0_4s0-6s1__1s0-2s1-3s0-5s1-7s0-8s1` | H3/two | presplit | certified | 670.6 | 62.2 |  |
| 2804 | `0s0_4s0-7s0__1s0-2s0-3s0-5s0-6s0-8s1` | H3/two | presplit | certified | 89.5 | 35.8 |  |
| 2848 | `0s0_4s0-7s0__1s1-2s0-3s1-5s1-6s0-8s1` | H3/two | presplit | certified | 86.4 | 34.6 |  |
| 2892 | `0s0_4s0-7s1__1s1-2s0-3s0-5s0-6s1-8s0` | H3/two | presplit | certified | 459.5 | 54.7 |  |
| 2936 | `0s0_4s1-5s0__1s0-2s0-3s1-6s1-7s1-8s0` | H3/two | never_ran | certified | 689.4 | 61.5 |  |
| 2980 | `0s0_4s1-5s0__1s1-2s1-3s1-6s0-7s1-8s0` | H3/two | never_ran | certified | 622.4 | 75.6 |  |
| 3024 | `0s0_4s1-6s0__1s0-2s1-3s1-5s1-7s0-8s1` | H3/two | presplit | timeout900 | 900.2 |  | split 51 children |
| 3068 | `0s0_4s1-6s1__1s0-2s0-3s1-5s0-7s0-8s1` | H3/two | presplit | certified | 105.6 | 32.9 |  |
| 3112 | `0s0_4s1-6s1__1s1-2s1-3s0-5s1-7s0-8s1` | H3/two | presplit | certified | 107.1 | 36.6 |  |
| 3156 | `0s0_4s1-7s0__1s1-2s0-3s0-5s0-6s0-8s1` | H3/two | presplit | certified | 434.4 | 50.8 |  |
| 3200 | `0s0_5s0-6s0__1s0-2s0-3s1-4s1-7s0-8s1` | H3/two | presplit | certified | 40.5 | 27.2 |  |
| 3244 | `0s0_5s0-6s0__1s1-2s1-3s1-4s0-7s0-8s1` | H3/two | presplit | certified | 44.3 | 26.3 |  |
| 3288 | `0s0_5s0-6s1__1s1-2s0-3s0-4s1-7s0-8s1` | H3/two | presplit | certified | 562.9 | 58.6 |  |
| 3332 | `0s0_5s1-6s0__1s1-2s1-3s0-4s1-7s0-8s1` | H3/two | timeout300 | certified | 654.0 | 56.4 |  |
| 3376 | `0s0-1s1_5__2s0-3s1-4s1-6s1-7s0-8s0` | H6(1,1)/one | timeout300 | certified | 335.5 | 50.3 |  |
| 3420 | `0s0-2s1_3__1s1-4s1-5s0-6s0-7s1-8s0` | H6(2,1)/one | timeout300 | certified | 387.1 | 52.0 |  |
| 3464 | `0s0-2s1_5__1s0-3s0-4s1-6s0-7s0-8s1` | H6(2,1)/one | timeout300 | certified | 295.6 | 44.0 |  |
| 3508 | `0s0-2s1_5__1s1-3s1-4s1-6s1-7s0-8s1` | H6(2,1)/one | timeout300 | certified | 489.2 | 59.1 |  |
| 3552 | `0s0-2s1_6__1s1-3s0-4s1-5s0-7s1-8s1` | H6(2,1)/one | timeout300 | certified | 409.0 | 55.9 |  |
| 3596 | `0s0-3s1_4__1s1-2s0-5s1-6s1-7s1-8s1` | H6(3,1)/one | never_ran | certified | 342.8 | 49.7 |  |
| 3640 | `0s0-3s1_5__1s0-2s1-4s1-6s0-7s1-8s1` | H6(3,1)/one | presplit | certified | 360.6 | 50.1 |  |
| 3684 | `0s0-4s0_6__1s0-2s0-3s0-5s1-7s1-8s1` | H6(4,0)/one | presplit | certified | 44.4 | 24.2 |  |
| 3728 | `0s0-4s0_6__1s1-2s1-3s0-5s0-7s1-8s1` | H6(4,0)/one | presplit | certified | 52.0 | 28.4 |  |
| 3772 | `0s0-5s0_6__1s0-2s1-3s1-4s0-7s1-8s0` | H6(5,0)/one | presplit | certified | 119.2 | 35.4 |  |
| 3816 | `0s0-5s0_7__1s0-2s0-3s0-4s1-6s1-8s0` | H6(5,0)/one | presplit | certified | 80.9 | 39.7 |  |
| 3860 | `0s0-5s0_7__1s1-2s1-3s0-4s0-6s1-8s0` | H6(5,0)/one | presplit | certified | 112.5 | 37.3 |  |
| 3904 | `0s0-5s1_1__2s1-3s0-4s1-6s1-7s0-8s0` | H6(5,1)/one | presplit | certified | 177.0 | 41.8 |  |
| 3948 | `0s0-5s1_2__1s0-3s1-4s1-6s0-7s0-8s0` | H6(5,1)/one | presplit | certified | 184.8 | 41.3 |  |
| 3992 | `0s0-5s1_6__1s1-2s0-3s0-4s1-7s0-8s1` | H6(5,1)/one | never_ran | certified | 259.5 | 55.6 |  |
| 4036 | `0s0-5s1_1s1-10s1__2s0-3s1-4s0-6s1-7s1-8s1` | H6(5,1)/two | never_ran | certified | 68.1 | 31.6 |  |
| 4080 | `0s0-5s1_2s1-3s0__1s1-4s0-6s0-7s0-8s1-9s1` | H6(5,1)/two | never_ran | certified | 45.4 | 30.2 |  |

