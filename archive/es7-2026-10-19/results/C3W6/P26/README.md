# C3W6 P26: W6.tsv shard 26 of 44 (task `results/C3W6/TASK.md` at c5260b44)

All 93 units were certified at cap 900. None timed out, no unit went unreached, nothing was split. No SAT, no proof rejections, no memory problems, and no unit ended early.

## Setup

- Tools: C3U2 tools at cad4e050 (worktree /opt/c3u2, unmodified), CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (its example gives `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch. Sanity test on {1},{-1}: LRAT `3 0 0` was rejected by both checkers and `3 0 1 2 0` was accepted by both. Details are in `tools.txt`.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches).
- Machine: 4 cores, 15 GB (`env.txt`). Start 05:31:48 UTC, END 09:46:48 UTC. All lanes finished their units by 07:50:44 UTC, so no unit was killed at END.
- Units: the rows of `lists/W6.tsv` with row ≡ 26 (mod 44), 93 units (`units.tsv`). There were no seeded records. 3 lanes (`lane0.sh`–`lane2.sh`) ran with `close_tree.py … --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`.
- `out.jsonl` holds 93 records (lane 0, then 1, then 2), one solve record per unit. Every record has `certified: true`, lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`. Every unit's close_tree printed `open_frontier 0, unsplittable 0`. No split records were written, and there is no `recheck.jsonl`.

## Totals

| stratum | prior | units | certified | timed out at 900 | not reached |
|---|---|---|---|---|---|
| H3/two | never_ran | 7 | 7 | 0 | 0 |
| H3/two | presplit | 50 | 50 | 0 | 0 |
| H3/two | timeout300 | 19 | 19 | 0 | 0 |
| H6(1,1)/one | timeout300 | 1 | 1 | 0 | 0 |
| H6(2,1)/one | timeout300 | 4 | 4 | 0 | 0 |
| H6(3,1)/one | never_ran | 1 | 1 | 0 | 0 |
| H6(3,1)/one | presplit | 1 | 1 | 0 | 0 |
| H6(4,0)/one | presplit | 2 | 2 | 0 | 0 |
| H6(5,0)/one | presplit | 3 | 3 | 0 | 0 |
| H6(5,1)/one | presplit | 3 | 3 | 0 | 0 |
| H6(5,1)/two | never_ran | 2 | 2 | 0 | 0 |
| **total** | | **93** | **93** | **0** | **0** |

Solve times of the 93 certified units: min 22.7 s, Q1 84.2 s, median 217.7 s, Q3 314.7 s, p90 362.9 s, max 516.2 s. 26 units were certified above 300 s. Check times ran from 22.1 to 75.9 s. Total solve time was 19,573 s and total check time 4,321 s.

## Per unit

| row | node | stratum | prior | lane | result | solve s | check s |
|---|---|---|---|---|---|---|---|
| 26 | `0s0_1s0-2s0__3s0-4s0-5s1-6s1-7s0-8s1` | H3/two | presplit | 0 | certified | 22.7 | 37.4 |
| 70 | `0s0_1s0-2s0__3s1-4s1-5s1-6s0-7s0-8s1` | H3/two | presplit | 1 | certified | 34.7 | 40.1 |
| 114 | `0s0_1s0-2s1__3s1-4s0-5s1-6s1-7s0-8s0` | H3/two | timeout300 | 2 | certified | 294.3 | 61.7 |
| 158 | `0s0_1s0-3s1__2s1-4s1-5s1-6s0-7s1-8s1` | H3/two | timeout300 | 0 | certified | 347.9 | 68.1 |
| 202 | `0s0_1s0-4s1__2s1-3s1-5s0-6s0-7s1-8s0` | H3/two | timeout300 | 1 | certified | 330.9 | 63.8 |
| 246 | `0s0_1s0-5s1__2s1-3s1-4s1-6s1-7s0-8s0` | H3/two | timeout300 | 2 | certified | 278.6 | 50.6 |
| 290 | `0s0_1s0-7s0__2s1-3s1-4s0-5s0-6s1-8s0` | H3/two | timeout300 | 0 | certified | 119.1 | 46.0 |
| 334 | `0s0_1s1-2s0__3s0-4s1-5s1-6s1-7s1-8s1` | H3/two | timeout300 | 1 | certified | 322.1 | 57.2 |
| 378 | `0s0_1s1-4s0__2s1-3s0-5s1-6s1-7s1-8s0` | H3/two | timeout300 | 2 | certified | 281.7 | 58.4 |
| 422 | `0s0_1s1-5s0__2s1-3s1-4s0-6s0-7s1-8s0` | H3/two | timeout300 | 0 | certified | 298.3 | 52.4 |
| 466 | `0s0_1s1-5s1__2s0-3s1-4s1-6s1-7s1-8s1` | H3/two | presplit | 1 | certified | 161.7 | 39.9 |
| 510 | `0s0_1s1-7s1__2s0-3s1-4s1-5s0-6s0-8s1` | H3/two | timeout300 | 2 | certified | 232.3 | 48.9 |
| 554 | `0s0_1s1-8s0__2s0-3s0-4s0-5s1-6s1-7s1` | H3/two | presplit | 0 | certified | 143.6 | 55.8 |
| 598 | `0s0_1s1-8s0__2s1-3s1-4s0-5s0-6s1-7s1` | H3/two | presplit | 1 | certified | 83.6 | 38.3 |
| 642 | `0s0_1s1-8s1__2s1-3s1-4s1-5s0-6s1-7s1` | H3/two | timeout300 | 2 | certified | 339.7 | 53.8 |
| 686 | `0s0_1s1-9s1__2s1-3s1-4s0-5s1-6s0-7s0` | H3/two | never_ran | 0 | certified | 316.3 | 51.3 |
| 730 | `0s0_2s0-3s1__1s1-4s0-5s0-6s0-7s0-8s0` | H3/two | presplit | 1 | certified | 217.7 | 48.5 |
| 774 | `0s0_2s0-4s1__1s0-3s0-5s1-6s1-7s0-8s0` | H3/two | presplit | 2 | certified | 280.2 | 50.4 |
| 818 | `0s0_2s0-4s1__1s1-3s1-5s1-6s0-7s0-8s0` | H3/two | presplit | 0 | certified | 361.0 | 50.6 |
| 862 | `0s0_2s0-5s0__1s1-3s0-4s0-6s1-7s0-8s0` | H3/two | presplit | 1 | certified | 81.9 | 51.2 |
| 906 | `0s0_2s0-5s1__1s0-3s1-4s0-6s1-7s1-8s1` | H3/two | timeout300 | 2 | certified | 324.3 | 48.4 |
| 950 | `0s0_2s0-6s1__1s0-3s0-4s0-5s1-7s0-8s0` | H3/two | timeout300 | 0 | certified | 177.7 | 43.8 |
| 994 | `0s0_2s0-6s1__1s1-3s1-4s0-5s0-7s0-8s1` | H3/two | timeout300 | 1 | certified | 297.9 | 57.3 |
| 1038 | `0s0_2s0-7s0__1s0-3s1-4s1-5s1-6s0-8s1` | H3/two | presplit | 2 | certified | 82.2 | 34.0 |
| 1082 | `0s0_2s0-7s1__1s0-3s0-4s1-5s0-6s0-8s1` | H3/two | presplit | 0 | certified | 210.7 | 42.2 |
| 1126 | `0s0_2s0-7s1__1s1-3s1-4s0-5s1-6s0-8s1` | H3/two | presplit | 1 | certified | 260.4 | 44.8 |
| 1170 | `0s0_2s0-8s0__1s1-3s1-4s0-5s0-6s1-7s1` | H3/two | presplit | 2 | certified | 176.9 | 39.5 |
| 1214 | `0s0_2s1-3s0__1s1-4s0-5s0-6s0-7s0-8s0` | H3/two | timeout300 | 0 | certified | 216.0 | 42.0 |
| 1258 | `0s0_2s1-3s1__1s0-4s0-5s1-6s1-7s0-8s0` | H3/two | presplit | 1 | certified | 55.0 | 31.8 |
| 1302 | `0s0_2s1-3s1__1s1-4s1-5s1-6s0-7s0-8s0` | H3/two | presplit | 2 | certified | 40.4 | 41.2 |
| 1346 | `0s0_2s1-4s0__1s1-3s0-5s1-6s0-7s1-8s0` | H3/two | timeout300 | 0 | certified | 313.5 | 49.4 |
| 1390 | `0s0_2s1-5s0__1s0-3s1-4s0-6s1-7s1-8s0` | H3/two | presplit | 1 | certified | 243.3 | 43.6 |
| 1434 | `0s0_2s1-6s0__1s0-3s0-4s0-5s0-7s1-8s0` | H3/two | presplit | 2 | certified | 147.7 | 39.0 |
| 1478 | `0s0_2s1-6s0__1s1-3s0-4s1-5s1-7s1-8s0` | H3/two | presplit | 0 | certified | 335.6 | 49.8 |
| 1522 | `0s0_2s1-6s1__1s0-3s1-4s1-5s0-7s1-8s0` | H3/two | presplit | 1 | certified | 158.0 | 38.3 |
| 1566 | `0s0_2s1-7s0__1s0-3s0-4s0-5s1-6s1-8s0` | H3/two | never_ran | 2 | certified | 229.6 | 42.1 |
| 1610 | `0s0_2s1-7s0__1s1-3s1-4s1-5s0-6s1-8s0` | H3/two | never_ran | 0 | certified | 225.7 | 44.2 |
| 1654 | `0s0_2s1-8s1__1s0-3s0-4s0-5s1-6s1-7s1` | H3/two | presplit | 1 | certified | 256.1 | 43.5 |
| 1698 | `0s0_2s1-8s1__1s1-3s1-4s0-5s1-6s0-7s1` | H3/two | presplit | 2 | certified | 305.3 | 45.0 |
| 1742 | `0s0_2s1-9s0__1s1-3s0-4s0-5s0-6s0-7s1` | H3/two | presplit | 0 | certified | 120.7 | 40.5 |
| 1786 | `0s0_3s0-4s1__1s0-2s0-5s1-6s1-7s0-8s1` | H3/two | presplit | 1 | certified | 322.6 | 58.1 |
| 1830 | `0s0_3s0-4s1__1s1-2s1-5s1-6s0-7s0-8s1` | H3/two | presplit | 2 | certified | 399.5 | 60.0 |
| 1874 | `0s0_3s0-5s0__1s1-2s0-4s0-6s1-7s0-8s1` | H3/two | presplit | 0 | certified | 31.0 | 23.2 |
| 1918 | `0s0_3s0-5s1__1s0-2s1-4s1-6s0-7s1-8s1` | H3/two | timeout300 | 1 | certified | 383.7 | 53.6 |
| 1962 | `0s0_3s0-6s0__1s0-2s0-4s0-5s1-7s1-8s1` | H3/two | presplit | 2 | certified | 68.5 | 31.5 |
| 2006 | `0s0_3s0-6s0__1s1-2s1-4s0-5s0-7s1-8s1` | H3/two | presplit | 0 | certified | 121.0 | 58.4 |
| 2050 | `0s0_3s0-6s1__1s0-2s1-4s1-5s1-7s1-8s1` | H3/two | timeout300 | 1 | certified | 320.6 | 53.1 |
| 2094 | `0s0_3s0-7s0__1s0-2s0-4s1-5s0-6s1-8s1` | H3/two | presplit | 2 | certified | 60.6 | 47.0 |
| 2138 | `0s0_3s0-7s0__1s1-2s1-4s0-5s1-6s1-8s1` | H3/two | presplit | 0 | certified | 127.2 | 48.6 |
| 2182 | `0s0_3s0-7s1__1s1-2s0-4s0-5s0-6s1-8s1` | H3/two | presplit | 1 | certified | 315.8 | 52.7 |
| 2226 | `0s0_3s0-8s0__1s1-2s0-4s0-5s1-6s0-7s1` | H3/two | presplit | 2 | certified | 122.6 | 35.7 |
| 2270 | `0s0_3s0-8s1__1s1-2s1-4s0-5s1-6s0-7s0` | H3/two | never_ran | 0 | certified | 261.8 | 63.0 |
| 2314 | `0s0_3s1-4s0__1s1-2s0-5s0-6s0-7s1-8s0` | H3/two | timeout300 | 1 | certified | 293.1 | 46.4 |
| 2358 | `0s0_3s1-4s1__1s0-2s0-5s1-6s1-7s1-8s0` | H3/two | presplit | 2 | certified | 91.7 | 38.2 |
| 2402 | `0s0_3s1-4s1__1s1-2s1-5s1-6s0-7s1-8s0` | H3/two | presplit | 0 | certified | 55.4 | 37.8 |
| 2446 | `0s0_3s1-5s0__1s1-2s0-4s0-6s1-7s1-8s0` | H3/two | presplit | 1 | certified | 386.1 | 60.2 |
| 2490 | `0s0_3s1-5s1__1s0-2s1-4s0-6s0-7s1-8s0` | H3/two | presplit | 2 | certified | 72.8 | 30.5 |
| 2534 | `0s0_3s1-5s1__1s1-2s1-4s1-6s1-7s1-8s0` | H3/two | presplit | 0 | certified | 54.7 | 33.9 |
| 2578 | `0s0_3s1-7s0__1s1-2s1-4s1-5s0-6s0-8s0` | H3/two | never_ran | 1 | certified | 282.4 | 52.1 |
| 2622 | `0s0_3s1-8s0__1s0-2s0-4s1-5s0-6s1-7s1` | H3/two | presplit | 2 | certified | 152.5 | 38.8 |
| 2666 | `0s0_3s1-8s0__1s1-2s1-4s0-5s1-6s1-7s1` | H3/two | presplit | 0 | certified | 362.3 | 51.8 |
| 2710 | `0s0_4s0-5s1__1s1-2s0-3s0-6s0-7s1-8s1` | H3/two | presplit | 1 | certified | 332.4 | 58.8 |
| 2754 | `0s0_4s0-6s1__1s0-2s0-3s1-5s1-7s1-8s1` | H3/two | presplit | 2 | certified | 303.3 | 71.0 |
| 2798 | `0s0_4s0-6s1__1s1-2s1-3s1-5s0-7s1-8s1` | H3/two | presplit | 0 | certified | 516.2 | 75.9 |
| 2842 | `0s0_4s0-7s0__1s1-2s0-3s0-5s1-6s1-8s1` | H3/two | presplit | 1 | certified | 65.1 | 42.9 |
| 2886 | `0s0_4s0-7s1__1s0-2s1-3s1-5s1-6s0-8s0` | H3/two | presplit | 2 | certified | 491.0 | 74.2 |
| 2930 | `0s0_4s1-5s0__1s0-2s0-3s1-6s0-7s0-8s0` | H3/two | never_ran | 0 | certified | 278.2 | 48.9 |
| 2974 | `0s0_4s1-5s0__1s1-2s1-3s0-6s1-7s0-8s0` | H3/two | never_ran | 1 | certified | 429.0 | 57.3 |
| 3018 | `0s0_4s1-6s0__1s0-2s1-3s0-5s1-7s1-8s1` | H3/two | presplit | 2 | certified | 369.8 | 54.6 |
| 3062 | `0s0_4s1-6s1__1s0-2s0-3s0-5s0-7s1-8s1` | H3/two | presplit | 0 | certified | 104.4 | 44.4 |
| 3106 | `0s0_4s1-6s1__1s1-2s0-3s1-5s1-7s1-8s1` | H3/two | presplit | 1 | certified | 67.8 | 39.8 |
| 3150 | `0s0_4s1-7s0__1s0-2s1-3s1-5s0-6s1-8s1` | H3/two | presplit | 2 | certified | 377.4 | 56.9 |
| 3194 | `0s0_5s0-6s0__1s0-2s0-3s0-4s1-7s1-8s1` | H3/two | presplit | 0 | certified | 42.2 | 26.5 |
| 3238 | `0s0_5s0-6s0__1s1-2s1-3s0-4s0-7s1-8s1` | H3/two | presplit | 1 | certified | 31.3 | 22.1 |
| 3282 | `0s0_5s0-6s1__1s0-2s1-3s1-4s1-7s1-8s1` | H3/two | presplit | 2 | certified | 362.9 | 50.3 |
| 3326 | `0s0_5s1-6s0__1s1-2s0-3s1-4s1-7s1-8s0` | H3/two | timeout300 | 0 | certified | 451.1 | 52.2 |
| 3370 | `0s0-1s1_5__2s0-3s0-4s1-6s1-7s1-8s0` | H6(1,1)/one | timeout300 | 1 | certified | 181.1 | 39.4 |
| 3414 | `0s0-2s1_3__1s1-4s0-5s1-6s0-7s0-8s1` | H6(2,1)/one | timeout300 | 2 | certified | 274.6 | 59.7 |
| 3458 | `0s0-2s1_5__1s0-3s0-4s0-6s0-7s1-8s0` | H6(2,1)/one | timeout300 | 0 | certified | 157.6 | 39.2 |
| 3502 | `0s0-2s1_5__1s1-3s1-4s0-6s1-7s1-8s1` | H6(2,1)/one | timeout300 | 1 | certified | 204.5 | 39.1 |
| 3546 | `0s0-2s1_6__1s1-3s0-4s0-5s1-7s0-8s1` | H6(2,1)/one | timeout300 | 2 | certified | 230.2 | 44.9 |
| 3590 | `0s0-3s1_4__1s1-2s0-5s1-6s0-7s0-8s1` | H6(3,1)/one | never_ran | 0 | certified | 257.4 | 46.1 |
| 3634 | `0s0-3s1_5__1s0-2s1-4s0-6s1-7s0-8s1` | H6(3,1)/one | presplit | 1 | certified | 263.7 | 58.4 |
| 3678 | `0s0-4s0_6__1s0-2s0-3s0-5s0-7s0-8s1` | H6(4,0)/one | presplit | 2 | certified | 27.4 | 24.0 |
| 3722 | `0s0-4s0_6__1s1-2s0-3s1-5s1-7s0-8s1` | H6(4,0)/one | presplit | 0 | certified | 57.1 | 31.9 |
| 3766 | `0s0-5s0_6__1s0-2s1-3s0-4s1-7s0-8s0` | H6(5,0)/one | presplit | 1 | certified | 62.5 | 34.3 |
| 3810 | `0s0-5s0_7__1s0-2s0-3s0-4s0-6s0-8s0` | H6(5,0)/one | presplit | 2 | certified | 42.7 | 37.4 |
| 3854 | `0s0-5s0_7__1s1-2s0-3s1-4s1-6s0-8s0` | H6(5,0)/one | presplit | 0 | certified | 84.8 | 39.0 |
| 3898 | `0s0-5s1_1__2s1-3s0-4s0-6s1-7s1-8s0` | H6(5,1)/one | presplit | 1 | certified | 177.4 | 45.5 |
| 3942 | `0s0-5s1_2__1s0-3s1-4s0-6s0-7s1-8s0` | H6(5,1)/one | presplit | 2 | certified | 135.5 | 41.4 |
| 3986 | `0s0-5s1_2__1s1-3s1-4s1-6s1-7s1-8s0` | H6(5,1)/one | presplit | 0 | certified | 118.8 | 37.4 |
| 4030 | `0s0-5s1_1s1-10s1__2s0-3s1-4s0-6s0-7s0-8s1` | H6(5,1)/two | never_ran | 1 | certified | 25.3 | 35.8 |
| 4074 | `0s0-5s1_1s1-10s1__2s1-3s1-4s1-6s1-7s0-8s1` | H6(5,1)/two | never_ran | 2 | certified | 39.0 | 32.5 |
