# C3W6 P20

Task `results/C3W6/TASK.md` at c5260b44, with V = P20, LIST = W6.tsv, j = 20, N = 44, H = 4.5. Start 2026-10-25 05:31:17 UTC, END 09:46:17 UTC. All lanes finished their units at 07:39 UTC, so nothing was killed at END.

## Tools and base CNF

- C3U2 tools: worktree of cad4e050 at /opt/c3u2, used unmodified; `compose.py` not run.
- CaDiCaL c6073042 (3.0.1); cake_lpr a36874a8 (example prints `s VERIFIED UNSAT`); lrat-check 2e3b2dc with the E2 patch. Sanity test passed: `3 0 0` on {1},{-1} is rejected by both checkers, `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`, which matches.
- Details are in `tools.txt`.

## Run

- Units: the rows of W6.tsv with row ≡ 20 (mod 44), 93 units (`units.tsv`). No records were seeded.
- Three lanes (`lane0.sh` to `lane2.sh`, started with `setsid nohup`). Lane k took units at positions ≡ k (mod 3) and ran `close_tree.py … U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02` on each.
- `out.jsonl` holds the lane 0 records, then lane 1, then lane 2: 93 records, one per unit.

## Result

- **All 93 units were certified at cap 900** on the first solve. Each record has status UNSATISFIABLE, `lrat_check` "c VERIFIED" and `cake_lpr` "s VERIFIED UNSAT".
- No unit timed out and none was left unreached, so no split records were written and every unit's `open_frontier` is 0.
- No SAT, no proof rejection, no `cake_lpr: none` and no memory problem (at most about 6 GB of 15 GB in use). No `recheck.jsonl` was needed.
- No unit ended early without a certificate. The 21 units that solved in under 72 s were all certified.

solve_s over 93 certified units: min 11.7, Q1 76.8, median 188.7, Q3 292.6, p90 340.9, max 454.7; above 300 s: 22; under 72 s: 21 (all certified)
total solve 18280 s, total check 3992 s

| stratum | units | certified | timed out at 900 | not reached | solve s | check s |
|---|---|---|---|---|---|---|
| H3/two | 76 | 76 | 0 | 0 | 15969 | 3328 |
| H6(1,1)/one | 2 | 2 | 0 | 0 | 356 | 78 |
| H6(2,1)/one | 3 | 3 | 0 | 0 | 610 | 137 |
| H6(3,1)/one | 3 | 3 | 0 | 0 | 538 | 127 |
| H6(4,0)/one | 1 | 1 | 0 | 0 | 49 | 45 |
| H6(5,0)/one | 3 | 3 | 0 | 0 | 184 | 96 |
| H6(5,1)/one | 3 | 3 | 0 | 0 | 493 | 120 |
| H6(5,1)/two | 2 | 2 | 0 | 0 | 80 | 60 |

| prior | units | certified | timed out at 900 | not reached | solve s | check s |
|---|---|---|---|---|---|---|
| never_ran | 9 | 9 | 0 | 0 | 1880 | 392 |
| presplit | 58 | 58 | 0 | 0 | 9427 | 2292 |
| timeout300 | 26 | 26 | 0 | 0 | 6973 | 1308 |

| row | unit | stratum | prior | result | solve s | check s |
|---|---|---|---|---|---|---|
| 20 | `0s0_1s0-2s0__3s0-4s0-5s0-6s1-7s1-8s1` | H3/two | presplit | certified | 15.9 | 29.4 |
| 64 | `0s0_1s0-2s0__3s1-4s1-5s0-6s0-7s1-8s1` | H3/two | presplit | certified | 24.5 | 34.8 |
| 108 | `0s0_1s0-2s1__3s1-4s0-5s0-6s1-7s1-8s0` | H3/two | timeout300 | certified | 322.1 | 66.2 |
| 152 | `0s0_1s0-3s1__2s1-4s1-5s0-6s0-7s1-8s1` | H3/two | timeout300 | certified | 343.7 | 68.7 |
| 196 | `0s0_1s0-4s1__2s1-3s0-5s1-6s1-7s0-8s0` | H3/two | timeout300 | certified | 329.7 | 64.4 |
| 240 | `0s0_1s0-5s1__2s1-3s1-4s0-6s1-7s1-8s0` | H3/two | timeout300 | certified | 281.2 | 53.9 |
| 284 | `0s0_1s0-7s0__2s1-3s0-4s1-5s1-6s0-8s0` | H3/two | timeout300 | certified | 100.0 | 43.3 |
| 328 | `0s0_1s1-2s0__3s0-4s1-5s1-6s0-7s0-8s1` | H3/two | timeout300 | certified | 275.5 | 49.2 |
| 372 | `0s0_1s1-4s0__2s0-3s1-5s1-6s1-7s0-8s1` | H3/two | timeout300 | certified | 324.0 | 54.4 |
| 416 | `0s0_1s1-5s0__2s1-3s0-4s1-6s1-7s0-8s0` | H3/two | timeout300 | certified | 208.1 | 46.1 |
| 460 | `0s0_1s1-5s1__2s0-3s1-4s1-6s0-7s0-8s1` | H3/two | presplit | certified | 182.1 | 52.0 |
| 504 | `0s0_1s1-7s1__2s0-3s1-4s0-5s0-6s1-8s1` | H3/two | timeout300 | certified | 236.7 | 58.5 |
| 548 | `0s0_1s1-8s0__2s0-3s0-4s0-5s0-6s0-7s1` | H3/two | presplit | certified | 88.4 | 39.9 |
| 592 | `0s0_1s1-8s0__2s1-3s0-4s1-5s1-6s0-7s1` | H3/two | presplit | certified | 84.9 | 29.7 |
| 636 | `0s0_1s1-8s1__2s1-3s1-4s0-5s1-6s0-7s1` | H3/two | timeout300 | certified | 315.3 | 63.1 |
| 680 | `0s0_1s1-9s1__2s1-3s0-4s1-5s1-6s1-7s0` | H3/two | never_ran | certified | 336.7 | 51.9 |
| 724 | `0s0_2s0-3s1__1s0-4s1-5s1-6s0-7s1-8s0` | H3/two | presplit | certified | 254.4 | 47.7 |
| 768 | `0s0_2s0-4s1__1s0-3s0-5s0-6s1-7s1-8s0` | H3/two | presplit | certified | 240.3 | 64.4 |
| 812 | `0s0_2s0-4s1__1s1-3s1-5s0-6s0-7s1-8s0` | H3/two | presplit | certified | 316.0 | 48.9 |
| 856 | `0s0_2s0-5s0__1s0-3s1-4s1-6s1-7s1-8s0` | H3/two | presplit | certified | 52.3 | 30.7 |
| 900 | `0s0_2s0-5s1__1s0-3s1-4s0-6s0-7s0-8s1` | H3/two | timeout300 | certified | 290.7 | 48.7 |
| 944 | `0s0_2s0-5s1__1s1-3s1-4s1-6s1-7s0-8s1` | H3/two | timeout300 | certified | 381.9 | 49.0 |
| 988 | `0s0_2s0-6s1__1s1-3s0-4s1-5s0-7s1-8s1` | H3/two | timeout300 | certified | 251.4 | 44.4 |
| 1032 | `0s0_2s0-7s0__1s0-3s1-4s0-5s1-6s1-8s1` | H3/two | presplit | certified | 75.3 | 34.6 |
| 1076 | `0s0_2s0-7s1__1s0-3s0-4s0-5s0-6s1-8s1` | H3/two | presplit | certified | 149.0 | 43.8 |
| 1120 | `0s0_2s0-7s1__1s1-3s0-4s1-5s1-6s1-8s1` | H3/two | presplit | certified | 191.7 | 43.5 |
| 1164 | `0s0_2s0-8s0__1s1-3s0-4s1-5s1-6s0-7s1` | H3/two | presplit | certified | 188.7 | 42.3 |
| 1208 | `0s0_2s1-3s0__1s0-4s1-5s1-6s0-7s1-8s0` | H3/two | timeout300 | certified | 313.3 | 53.3 |
| 1252 | `0s0_2s1-3s1__1s0-4s0-5s0-6s1-7s1-8s0` | H3/two | presplit | certified | 51.4 | 31.0 |
| 1296 | `0s0_2s1-3s1__1s1-4s1-5s0-6s0-7s1-8s0` | H3/two | presplit | certified | 47.1 | 26.9 |
| 1340 | `0s0_2s1-4s0__1s1-3s0-5s0-6s1-7s0-8s0` | H3/two | timeout300 | certified | 258.9 | 52.5 |
| 1384 | `0s0_2s1-5s0__1s0-3s1-4s0-6s0-7s0-8s0` | H3/two | presplit | certified | 167.9 | 39.2 |
| 1428 | `0s0_2s1-5s0__1s1-3s1-4s1-6s1-7s0-8s0` | H3/two | presplit | certified | 316.5 | 46.3 |
| 1472 | `0s0_2s1-6s0__1s1-3s0-4s1-5s0-7s0-8s0` | H3/two | presplit | certified | 178.0 | 39.5 |
| 1516 | `0s0_2s1-6s1__1s0-3s1-4s0-5s1-7s0-8s0` | H3/two | presplit | certified | 178.4 | 42.1 |
| 1560 | `0s0_2s1-7s0__1s0-3s0-4s0-5s0-6s0-8s0` | H3/two | never_ran | certified | 101.5 | 33.0 |
| 1604 | `0s0_2s1-7s0__1s1-3s1-4s0-5s1-6s0-8s0` | H3/two | never_ran | certified | 247.7 | 46.5 |
| 1648 | `0s0_2s1-7s1__1s1-3s1-4s1-5s0-6s1-8s0` | H3/two | never_ran | certified | 210.4 | 40.5 |
| 1692 | `0s0_2s1-8s1__1s1-3s0-4s1-5s1-6s1-7s1` | H3/two | presplit | certified | 380.9 | 51.3 |
| 1736 | `0s0_2s1-9s0__1s0-3s1-4s1-5s0-6s1-7s1` | H3/two | presplit | certified | 100.2 | 36.9 |
| 1780 | `0s0_3s0-4s1__1s0-2s0-5s0-6s1-7s1-8s1` | H3/two | presplit | certified | 238.1 | 44.8 |
| 1824 | `0s0_3s0-4s1__1s1-2s1-5s0-6s0-7s1-8s1` | H3/two | presplit | certified | 454.7 | 58.9 |
| 1868 | `0s0_3s0-5s0__1s0-2s1-4s1-6s1-7s1-8s1` | H3/two | presplit | certified | 62.8 | 33.6 |
| 1912 | `0s0_3s0-5s1__1s0-2s1-4s0-6s1-7s0-8s1` | H3/two | timeout300 | certified | 321.8 | 50.1 |
| 1956 | `0s0_3s0-6s0__1s0-2s0-4s0-5s0-7s0-8s1` | H3/two | presplit | certified | 37.9 | 28.2 |
| 2000 | `0s0_3s0-6s0__1s1-2s0-4s1-5s1-7s0-8s1` | H3/two | presplit | certified | 53.8 | 29.5 |
| 2044 | `0s0_3s0-6s1__1s0-2s1-4s1-5s0-7s0-8s1` | H3/two | timeout300 | certified | 332.4 | 47.6 |
| 2088 | `0s0_3s0-7s0__1s0-2s0-4s0-5s1-6s0-8s1` | H3/two | presplit | certified | 62.3 | 28.3 |
| 2132 | `0s0_3s0-7s0__1s1-2s1-4s0-5s0-6s0-8s1` | H3/two | presplit | certified | 139.7 | 40.6 |
| 2176 | `0s0_3s0-7s1__1s0-2s1-4s1-5s1-6s0-8s1` | H3/two | presplit | certified | 409.8 | 61.9 |
| 2220 | `0s0_3s0-8s0__1s0-2s1-4s1-5s1-6s1-7s1` | H3/two | presplit | certified | 79.8 | 29.8 |
| 2264 | `0s0_3s0-8s1__1s0-2s1-4s1-5s1-6s1-7s1` | H3/two | timeout300 | certified | 284.7 | 45.2 |
| 2308 | `0s0_3s1-4s0__1s0-2s1-5s1-6s1-7s0-8s0` | H3/two | timeout300 | certified | 328.8 | 49.0 |
| 2352 | `0s0_3s1-4s1__1s0-2s0-5s1-6s0-7s0-8s0` | H3/two | presplit | certified | 46.9 | 28.3 |
| 2396 | `0s0_3s1-4s1__1s1-2s1-5s0-6s1-7s0-8s0` | H3/two | presplit | certified | 46.7 | 30.1 |
| 2440 | `0s0_3s1-5s0__1s1-2s0-4s0-6s0-7s0-8s0` | H3/two | presplit | certified | 184.9 | 38.4 |
| 2484 | `0s0_3s1-5s1__1s0-2s0-4s1-6s1-7s0-8s0` | H3/two | presplit | certified | 61.0 | 29.3 |
| 2528 | `0s0_3s1-5s1__1s1-2s1-4s1-6s0-7s0-8s0` | H3/two | presplit | certified | 76.4 | 33.7 |
| 2572 | `0s0_3s1-7s0__1s1-2s1-4s0-5s0-6s1-8s0` | H3/two | never_ran | certified | 259.4 | 48.1 |
| 2616 | `0s0_3s1-8s0__1s0-2s0-4s0-5s1-6s0-7s1` | H3/two | presplit | certified | 99.9 | 33.6 |
| 2660 | `0s0_3s1-8s0__1s1-2s1-4s0-5s0-6s0-7s1` | H3/two | presplit | certified | 199.1 | 37.2 |
| 2704 | `0s0_4s0-5s1__1s0-2s1-3s1-6s1-7s0-8s1` | H3/two | presplit | certified | 402.9 | 56.9 |
| 2748 | `0s0_4s0-6s1__1s0-2s0-3s1-5s0-7s0-8s1` | H3/two | presplit | certified | 244.7 | 46.6 |
| 2792 | `0s0_4s0-6s1__1s1-2s1-3s0-5s1-7s0-8s1` | H3/two | presplit | certified | 430.5 | 55.4 |
| 2836 | `0s0_4s0-7s0__1s1-2s0-3s0-5s0-6s0-8s1` | H3/two | presplit | certified | 59.7 | 30.9 |
| 2880 | `0s0_4s0-7s1__1s0-2s1-3s0-5s1-6s1-8s0` | H3/two | presplit | certified | 324.6 | 52.5 |
| 2924 | `0s0_4s1-5s0__1s0-2s0-3s0-6s0-7s1-8s0` | H3/two | never_ran | certified | 196.7 | 57.6 |
| 2968 | `0s0_4s1-5s0__1s1-2s0-3s1-6s1-7s1-8s0` | H3/two | never_ran | certified | 448.4 | 54.2 |
| 3012 | `0s0_4s1-6s0__1s0-2s1-3s0-5s0-7s0-8s1` | H3/two | presplit | certified | 294.5 | 47.2 |
| 3056 | `0s0_4s1-6s0__1s1-2s1-3s1-5s1-7s0-8s1` | H3/two | presplit | certified | 411.7 | 49.6 |
| 3100 | `0s0_4s1-6s1__1s1-2s0-3s1-5s0-7s0-8s1` | H3/two | presplit | certified | 77.1 | 35.3 |
| 3144 | `0s0_4s1-7s0__1s0-2s1-3s0-5s1-6s0-8s1` | H3/two | presplit | certified | 225.8 | 39.8 |
| 3188 | `0s0_5s0-6s0__1s0-2s0-3s0-4s0-7s0-8s1` | H3/two | presplit | certified | 11.7 | 17.5 |
| 3232 | `0s0_5s0-6s0__1s1-2s0-3s1-4s1-7s0-8s1` | H3/two | presplit | certified | 40.6 | 26.2 |
| 3276 | `0s0_5s0-6s1__1s0-2s1-3s1-4s0-7s0-8s1` | H3/two | presplit | certified | 320.4 | 47.6 |
| 3320 | `0s0_5s1-6s0__1s1-2s0-3s1-4s0-7s0-8s0` | H3/two | timeout300 | certified | 286.3 | 41.7 |
| 3364 | `0s0-1s1_5__2s0-3s0-4s1-6s0-7s0-8s0` | H6(1,1)/one | timeout300 | certified | 171.9 | 37.3 |
| 3408 | `0s0-1s1_5__2s1-3s1-4s1-6s1-7s0-8s0` | H6(1,1)/one | timeout300 | certified | 184.2 | 41.2 |
| 3452 | `0s0-2s1_4__1s1-3s1-5s1-6s0-7s1-8s0` | H6(2,1)/one | timeout300 | certified | 218.5 | 41.4 |
| 3496 | `0s0-2s1_5__1s1-3s1-4s0-6s0-7s0-8s1` | H6(2,1)/one | timeout300 | certified | 258.5 | 43.0 |
| 3540 | `0s0-2s1_6__1s0-3s1-4s1-5s1-7s1-8s1` | H6(2,1)/one | timeout300 | certified | 133.0 | 52.7 |
| 3584 | `0s0-3s1_4__1s1-2s0-5s0-6s0-7s0-8s0` | H6(3,1)/one | timeout300 | certified | 220.2 | 42.9 |
| 3628 | `0s0-3s1_5__1s0-2s0-4s1-6s1-7s1-8s1` | H6(3,1)/one | presplit | certified | 153.0 | 38.4 |
| 3672 | `0s0-3s1_5__1s1-2s1-4s1-6s0-7s1-8s1` | H6(3,1)/one | presplit | certified | 165.3 | 46.0 |
| 3716 | `0s0-4s0_6__1s1-2s0-3s0-5s1-7s1-8s1` | H6(4,0)/one | presplit | certified | 48.8 | 45.4 |
| 3760 | `0s0-5s0_6__1s0-2s0-3s1-4s1-7s1-8s0` | H6(5,0)/one | presplit | certified | 58.4 | 33.3 |
| 3804 | `0s0-5s0_6__1s1-2s1-3s1-4s0-7s1-8s0` | H6(5,0)/one | presplit | certified | 56.0 | 30.3 |
| 3848 | `0s0-5s0_7__1s1-2s0-3s0-4s1-6s1-8s0` | H6(5,0)/one | presplit | certified | 69.9 | 32.3 |
| 3892 | `0s0-5s1_1__2s1-3s0-4s0-6s0-7s0-8s0` | H6(5,1)/one | presplit | certified | 160.2 | 39.8 |
| 3936 | `0s0-5s1_2__1s0-3s0-4s1-6s1-7s0-8s0` | H6(5,1)/one | presplit | certified | 167.7 | 40.0 |
| 3980 | `0s0-5s1_2__1s1-3s1-4s1-6s0-7s0-8s0` | H6(5,1)/one | presplit | certified | 165.4 | 40.2 |
| 4024 | `0s0-5s1_1s1-10s1__2s0-3s0-4s1-6s0-7s1-8s1` | H6(5,1)/two | never_ran | certified | 42.6 | 30.1 |
| 4068 | `0s0-5s1_1s1-10s1__2s1-3s1-4s0-6s1-7s1-8s1` | H6(5,1)/two | never_ran | certified | 36.9 | 29.8 |
