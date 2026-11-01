# C3W6 P02: shard j = 2 of N = 44 of W6.tsv (94 units), H = 4.5 h

Task: `results/C3W6/TASK.md` at c5260b44. Start 2026-10-25 05:31:42 UTC; END 09:46:42 UTC. All three lanes finished their units before END (lane 1 at 07:50:51, lane 0 at 07:53:22, lane 2 at 08:01:55 UTC), so nothing was killed.

Tools (details in `tools.txt`): C3U2 tools at cad4e050 (worktree at /opt/c3u2, used unmodified), CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (example → `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch (sanity: `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both). Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da` (matches). No records seeded. `compose.py` not run.

Run: 3 lanes (`lane0.sh`, `lane1.sh`, `lane2.sh`), each `close_tree.py … U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`.

## Result

All **94 of 94 units certified** at cap 900 (lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT` on every record). 0 timed out, 0 not reached, so no split records were written and every unit has `open_frontier` 0. `out.jsonl` holds 94 records (lane 0, then 1, then 2).

- No SAT, no `PROOF NOT ACCEPTED`, no cake_lpr `none`, so no rechecks were needed (no `recheck.jsonl`).
- No memory problem: at most about 2–3 GB used of 15 GB.
- No unit ended early without a certificate. 14 units were solved in under 72 s, and all 14 were certified.

## Totals per stratum

| stratum | certified | timed out | not reached |
|---|---|---|---|
| H3/two | 76 | 0 | 0 |
| H6(1,1)/one | 2 | 0 | 0 |
| H6(2,1)/one | 4 | 0 | 0 |
| H6(3,1)/one | 2 | 0 | 0 |
| H6(4,0)/one | 1 | 0 | 0 |
| H6(4,1)/one | 1 | 0 | 0 |
| H6(5,0)/one | 2 | 0 | 0 |
| H6(5,1)/one | 4 | 0 | 0 |
| H6(5,1)/two | 2 | 0 | 0 |

## Totals per prior

| prior | certified | timed out | not reached |
|---|---|---|---|
| never_ran | 12 | 0 | 0 |
| presplit | 54 | 0 | 0 |
| timeout300 | 28 | 0 | 0 |

## Solve times of the certified units (n = 94)

min 25.9 s, Q1 119.4 s, median 237.5 s, Q3 320.3 s, p90 385.7 s, max 479.2 s. Certified above 300 s: 31. Under 72 s: 14 (all certified). Total solve 21524 s, total check 3842 s.

## Per unit (solve s / check s)

| row | node | stratum | prior | result | solve / check |
|---|---|---|---|---|---|
| 2 | `0s0_1s0-10s0__2s1-3s0-4s1-5s1-6s0-7s1` | H3/two | timeout300 | certified | 222.3 / 55.3 |
| 46 | `0s0_1s0-2s0__3s1-4s0-5s0-6s0-7s0-8s1` | H3/two | presplit | certified | 33.9 / 36.0 |
| 90 | `0s0_1s0-2s1__3s0-4s1-5s0-6s1-7s0-8s0` | H3/two | timeout300 | certified | 355.1 / 66.1 |
| 134 | `0s0_1s0-3s1__2s0-4s1-5s1-6s0-7s0-8s1` | H3/two | timeout300 | certified | 371.3 / 59.6 |
| 178 | `0s0_1s0-4s1__2s0-3s1-5s1-6s0-7s0-8s1` | H3/two | timeout300 | certified | 343.2 / 43.6 |
| 222 | `0s0_1s0-5s1__2s1-3s0-4s0-6s0-7s0-8s1` | H3/two | timeout300 | certified | 281.2 / 41.2 |
| 266 | `0s0_1s0-7s0__2s0-3s1-4s1-5s0-6s0-8s1` | H3/two | timeout300 | certified | 153.1 / 46.3 |
| 310 | `0s0_1s1-2s0__3s0-4s0-5s0-6s1-7s1-8s1` | H3/two | timeout300 | certified | 301.7 / 54.6 |
| 354 | `0s0_1s1-2s0__3s1-4s1-5s0-6s0-7s1-8s1` | H3/two | timeout300 | certified | 417.1 / 53.5 |
| 398 | `0s0_1s1-5s0__2s0-3s0-4s1-6s1-7s1-8s1` | H3/two | timeout300 | certified | 201.6 / 57.4 |
| 442 | `0s0_1s1-5s1__2s0-3s0-4s0-6s1-7s1-8s1` | H3/two | presplit | certified | 120.3 / 41.9 |
| 486 | `0s0_1s1-5s1__2s1-3s1-4s0-6s0-7s1-8s1` | H3/two | presplit | certified | 189.8 / 41.3 |
| 530 | `0s0_1s1-7s1__2s1-3s0-4s1-5s1-6s1-8s1` | H3/two | timeout300 | certified | 433.4 / 52.4 |
| 574 | `0s0_1s1-8s0__2s0-3s1-4s1-5s0-6s1-7s1` | H3/two | presplit | certified | 126.4 / 44.9 |
| 618 | `0s0_1s1-8s1__2s0-3s1-4s1-5s1-6s0-7s0` | H3/two | timeout300 | certified | 321.3 / 47.9 |
| 662 | `0s0_1s1-9s1__2s0-3s1-4s1-5s1-6s0-7s0` | H3/two | never_ran | certified | 360.0 / 48.8 |
| 706 | `0s0_2s0-3s1__1s0-4s0-5s1-6s0-7s0-8s0` | H3/two | presplit | certified | 293.5 / 44.5 |
| 750 | `0s0_2s0-3s1__1s1-4s1-5s0-6s1-7s0-8s0` | H3/two | presplit | certified | 379.7 / 50.3 |
| 794 | `0s0_2s0-4s1__1s1-3s0-5s0-6s0-7s0-8s0` | H3/two | presplit | certified | 232.0 / 40.0 |
| 838 | `0s0_2s0-5s0__1s0-3s0-4s1-6s1-7s0-8s0` | H3/two | presplit | certified | 46.1 / 34.7 |
| 882 | `0s0_2s0-5s0__1s1-3s1-4s1-6s0-7s0-8s0` | H3/two | presplit | certified | 82.8 / 29.7 |
| 926 | `0s0_2s0-5s1__1s1-3s0-4s1-6s0-7s1-8s1` | H3/two | timeout300 | certified | 360.1 / 48.5 |
| 970 | `0s0_2s0-6s1__1s0-3s1-4s1-5s0-7s0-8s1` | H3/two | timeout300 | certified | 353.8 / 55.8 |
| 1014 | `0s0_2s0-7s0__1s0-3s0-4s0-5s1-6s0-8s1` | H3/two | presplit | certified | 107.2 / 33.8 |
| 1058 | `0s0_2s0-7s0__1s1-3s1-4s0-5s0-6s0-8s1` | H3/two | presplit | certified | 154.6 / 34.1 |
| 1102 | `0s0_2s0-7s1__1s0-3s1-4s1-5s1-6s0-8s1` | H3/two | presplit | certified | 391.1 / 48.1 |
| 1146 | `0s0_2s0-8s0__1s0-3s1-4s1-5s0-6s1-7s1` | H3/two | presplit | certified | 119.1 / 31.7 |
| 1190 | `0s0_2s1-3s0__1s0-4s0-5s1-6s0-7s0-8s0` | H3/two | timeout300 | certified | 293.8 / 56.6 |
| 1234 | `0s0_2s1-3s0__1s1-4s1-5s0-6s1-7s0-8s0` | H3/two | timeout300 | certified | 347.1 / 42.4 |
| 1278 | `0s0_2s1-3s1__1s1-4s0-5s0-6s0-7s0-8s0` | H3/two | presplit | certified | 77.2 / 33.5 |
| 1322 | `0s0_2s1-4s0__1s0-3s0-5s1-6s1-7s1-8s1` | H3/two | timeout300 | certified | 270.3 / 39.1 |
| 1366 | `0s0_2s1-4s0__1s1-3s1-5s1-6s1-7s1-8s0` | H3/two | timeout300 | certified | 397.4 / 49.1 |
| 1410 | `0s0_2s1-5s0__1s1-3s0-4s1-6s0-7s1-8s0` | H3/two | presplit | certified | 376.2 / 48.2 |
| 1454 | `0s0_2s1-6s0__1s0-3s1-4s0-5s1-7s1-8s0` | H3/two | presplit | certified | 275.8 / 40.0 |
| 1498 | `0s0_2s1-6s1__1s0-3s0-4s0-5s0-7s1-8s0` | H3/two | presplit | certified | 107.8 / 31.3 |
| 1542 | `0s0_2s1-6s1__1s1-3s0-4s1-5s1-7s1-8s0` | H3/two | presplit | certified | 187.3 / 43.0 |
| 1586 | `0s0_2s1-7s0__1s1-3s0-4s0-5s0-6s1-8s0` | H3/two | never_ran | certified | 238.5 / 42.0 |
| 1630 | `0s0_2s1-7s1__1s1-3s0-4s1-5s0-6s0-8s0` | H3/two | never_ran | certified | 121.8 / 34.9 |
| 1674 | `0s0_2s1-8s1__1s0-3s1-4s1-5s1-6s0-7s1` | H3/two | presplit | certified | 388.3 / 49.6 |
| 1718 | `0s0_2s1-9s0__1s0-3s0-4s1-5s0-6s0-7s1` | H3/two | presplit | certified | 79.7 / 27.1 |
| 1762 | `0s0_2s1-9s0__1s1-3s1-4s0-5s1-6s0-7s1` | H3/two | presplit | certified | 128.0 / 32.9 |
| 1806 | `0s0_3s0-4s1__1s1-2s0-5s0-6s0-7s0-8s1` | H3/two | presplit | certified | 300.8 / 56.2 |
| 1850 | `0s0_3s0-5s0__1s0-2s0-4s1-6s1-7s0-8s1` | H3/two | presplit | certified | 25.9 / 21.8 |
| 1894 | `0s0_3s0-5s0__1s1-2s1-4s1-6s0-7s0-8s1` | H3/two | presplit | certified | 76.5 / 30.6 |
| 1938 | `0s0_3s0-5s1__1s1-2s0-4s1-6s1-7s1-8s1` | H3/two | timeout300 | certified | 409.9 / 45.3 |
| 1982 | `0s0_3s0-6s0__1s0-2s1-4s1-5s0-7s1-8s1` | H3/two | presplit | certified | 87.1 / 46.2 |
| 2026 | `0s0_3s0-6s1__1s0-2s0-4s0-5s1-7s1-8s1` | H3/two | timeout300 | certified | 278.4 / 45.8 |
| 2070 | `0s0_3s0-6s1__1s1-2s1-4s0-5s0-7s1-8s1` | H3/two | never_ran | certified | 452.9 / 46.9 |
| 2114 | `0s0_3s0-7s0__1s0-2s1-4s1-5s1-6s1-8s1` | H3/two | presplit | certified | 79.3 / 29.2 |
| 2158 | `0s0_3s0-7s1__1s0-2s0-4s1-5s0-6s1-8s1` | H3/two | presplit | certified | 283.3 / 39.9 |
| 2202 | `0s0_3s0-7s1__1s1-2s1-4s0-5s1-6s1-8s1` | H3/two | presplit | certified | 233.7 / 41.0 |
| 2246 | `0s0_3s0-8s0__1s1-2s1-4s1-5s0-6s0-7s1` | H3/two | presplit | certified | 195.0 / 38.8 |
| 2290 | `0s0_3s1-4s0__1s0-2s0-5s1-6s0-7s1-8s0` | H3/two | timeout300 | certified | 317.2 / 57.2 |
| 2334 | `0s0_3s1-4s0__1s1-2s1-5s0-6s1-7s1-8s0` | H3/two | never_ran | certified | 479.2 / 50.6 |
| 2378 | `0s0_3s1-4s1__1s1-2s0-5s0-6s0-7s1-8s0` | H3/two | presplit | certified | 58.9 / 25.9 |
| 2422 | `0s0_3s1-5s0__1s0-2s0-4s1-6s1-7s1-8s0` | H3/two | presplit | certified | 322.9 / 40.1 |
| 2466 | `0s0_3s1-5s0__1s1-2s1-4s1-6s0-7s1-8s0` | H3/two | presplit | certified | 306.4 / 41.0 |
| 2510 | `0s0_3s1-5s1__1s1-2s0-4s0-6s1-7s1-8s0` | H3/two | presplit | certified | 65.1 / 27.3 |
| 2554 | `0s0_3s1-7s0__1s1-2s0-4s0-5s0-6s0-8s0` | H3/two | never_ran | certified | 174.0 / 33.4 |
| 2598 | `0s0_3s1-7s1__1s0-2s1-4s1-5s1-6s1-8s1` | H3/two | timeout300 | certified | 208.9 / 36.7 |
| 2642 | `0s0_3s1-8s0__1s0-2s1-4s1-5s1-6s1-7s1` | H3/two | presplit | certified | 276.1 / 38.8 |
| 2686 | `0s0_4s0-5s1__1s0-2s0-3s1-6s0-7s1-8s1` | H3/two | presplit | certified | 376.5 / 46.5 |
| 2730 | `0s0_4s0-5s1__1s1-2s1-3s0-6s1-7s1-8s1` | H3/two | presplit | certified | 419.1 / 46.6 |
| 2774 | `0s0_4s0-6s1__1s1-2s0-3s0-5s0-7s1-8s1` | H3/two | presplit | certified | 314.4 / 45.2 |
| 2818 | `0s0_4s0-7s0__1s0-2s0-3s1-5s1-6s1-8s1` | H3/two | presplit | certified | 66.3 / 26.6 |
| 2862 | `0s0_4s0-7s0__1s1-2s1-3s1-5s0-6s1-8s1` | H3/two | presplit | certified | 99.8 / 28.0 |
| 2906 | `0s0_4s0-7s1__1s1-2s1-3s0-5s0-6s0-8s0` | H3/two | presplit | certified | 315.3 / 42.7 |
| 2950 | `0s0_4s1-5s0__1s0-2s1-3s1-6s1-7s0-8s0` | H3/two | never_ran | certified | 435.7 / 48.9 |
| 2994 | `0s0_4s1-5s1__1s1-2s1-3s1-6s1-7s1-8s1` | H3/two | never_ran | certified | 32.0 / 20.5 |
| 3038 | `0s0_4s1-6s0__1s1-2s0-3s1-5s0-7s1-8s1` | H3/two | presplit | certified | 362.8 / 49.8 |
| 3082 | `0s0_4s1-6s1__1s0-2s1-3s0-5s1-7s1-8s1` | H3/two | presplit | certified | 59.9 / 25.5 |
| 3126 | `0s0_4s1-7s0__1s0-2s0-3s0-5s0-6s1-8s1` | H3/two | presplit | certified | 178.0 / 34.7 |
| 3170 | `0s0_4s1-7s0__1s1-2s0-3s1-5s1-6s1-8s1` | H3/two | presplit | certified | 353.5 / 41.2 |
| 3214 | `0s0_5s0-6s0__1s0-2s1-3s1-4s0-7s1-8s1` | H3/two | presplit | certified | 36.2 / 32.3 |
| 3258 | `0s0_5s0-6s1__1s0-2s0-3s0-4s1-7s1-8s1` | H3/two | presplit | certified | 278.6 / 41.8 |
| 3302 | `0s0_5s0-6s1__1s1-2s1-3s0-4s0-7s1-8s1` | H3/two | presplit | certified | 309.8 / 39.1 |
| 3346 | `0s0-1s1_4__2s1-3s0-5s0-6s0-7s0-8s0` | H6(1,1)/one | timeout300 | certified | 279.4 / 39.5 |
| 3390 | `0s0-1s1_5__2s1-3s0-4s1-6s0-7s1-8s0` | H6(1,1)/one | timeout300 | certified | 222.0 / 46.2 |
| 3434 | `0s0-2s1_4__1s1-3s0-5s0-6s1-7s1-8s0` | H6(2,1)/one | timeout300 | certified | 279.2 / 40.7 |
| 3478 | `0s0-2s1_5__1s0-3s1-4s1-6s1-7s1-8s1` | H6(2,1)/one | timeout300 | certified | 201.5 / 31.1 |
| 3522 | `0s0-2s1_6__1s0-3s0-4s1-5s1-7s0-8s1` | H6(2,1)/one | timeout300 | certified | 146.0 / 49.6 |
| 3566 | `0s0-2s1_6__1s1-3s1-4s1-5s0-7s0-8s1` | H6(2,1)/one | timeout300 | certified | 253.2 / 39.3 |
| 3610 | `0s0-3s1_4__1s1-2s1-5s1-6s1-7s0-8s1` | H6(3,1)/one | never_ran | certified | 236.5 / 41.3 |
| 3654 | `0s0-3s1_5__1s1-2s0-4s1-6s0-7s0-8s1` | H6(3,1)/one | presplit | certified | 291.6 / 44.2 |
| 3698 | `0s0-4s0_6__1s0-2s1-3s0-5s1-7s0-8s1` | H6(4,0)/one | presplit | certified | 65.4 / 30.2 |
| 3742 | `0s0-4s1_5__1s1-2s1-3s0-6s0-7s1-8s1` | H6(4,1)/one | timeout300 | certified | 267.9 / 39.4 |
| 3786 | `0s0-5s0_6__1s1-2s0-3s1-4s0-7s0-8s0` | H6(5,0)/one | presplit | certified | 60.9 / 30.6 |
| 3830 | `0s0-5s0_7__1s0-2s1-3s0-4s1-6s0-8s0` | H6(5,0)/one | presplit | certified | 55.5 / 29.6 |
| 3874 | `0s0-5s1_1__2s0-3s0-4s1-6s1-7s1-8s0` | H6(5,1)/one | presplit | certified | 172.4 / 44.5 |
| 3918 | `0s0-5s1_1__2s1-3s1-4s1-6s0-7s1-8s0` | H6(5,1)/one | presplit | certified | 120.7 / 31.8 |
| 3962 | `0s0-5s1_2__1s1-3s0-4s0-6s1-7s1-8s0` | H6(5,1)/one | presplit | certified | 248.9 / 39.0 |
| 4006 | `0s0-5s1_6__1s1-2s1-3s0-4s0-7s1-8s1` | H6(5,1)/one | never_ran | certified | 231.5 / 38.2 |
| 4050 | `0s0-5s1_1s1-10s1__2s1-3s0-4s0-6s1-7s0-8s1` | H6(5,1)/two | never_ran | certified | 36.4 / 26.5 |
| 4094 | `0s0-5s1_2s1-3s0__1s1-4s1-6s1-7s0-8s0-9s1` | H6(5,1)/two | never_ran | certified | 44.2 / 26.5 |
