# C3W6 P35

Task `results/C3W6/TASK.md` at c5260b44, with V = P35, LIST = W6.tsv, j = 35, N = 44, H = 4.5.
Start 05:31:54 UTC on 2026-10-25, END 09:46:54 UTC. The three lanes started at 05:35:26 UTC and all finished
before END (lane 2 at 08:38:39, lane 0 at 08:42:20, lane 1 at 09:12:52), so nothing was killed.

## Tools

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8 (bundled example: `s VERIFIED UNSAT`), and drat-trim lrat-check 2e3b2dc with the E2 patch.
  Sanity check on the CNF {1},{-1}: LRAT `3 0 0` was rejected by both checkers, and `3 0 1 2 0` was accepted by both.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da`, which matches.
- Details are in `tools.txt`.

## Result

**93 of 93 units certified at cap 900** (both checkers accepted every one). There were no timeouts, no split records and no units left unreached.
No SAT, no rejected proofs, no `none` checker results, no rechecks (so there is no `recheck.jsonl`), and no memory problems:
peak used memory was about 6 GB of 15 GB. No unit ended early without a certificate. 11 units solved in under 72 s, and all 11 are certified UNSAT.

`out.jsonl` has 93 records (lane 0, then 1, then 2), one solve record per unit.

### Totals per stratum

| stratum | units | certified |
|---|---|---|
| H3/two | 76 | 76 |
| H6(1,1)/one | 1 | 1 |
| H6(2,1)/one | 4 | 4 |
| H6(3,1)/one | 2 | 2 |
| H6(4,0)/one | 2 | 2 |
| H6(5,0)/one | 3 | 3 |
| H6(5,1)/one | 3 | 3 |
| H6(5,1)/two | 2 | 2 |

### Totals per prior

| prior | units | certified |
|---|---|---|
| presplit | 55 | 55 |
| timeout300 | 28 | 28 |
| never_ran | 10 | 10 |

### Solve times of the certified units (CaDiCaL, s)

Min 17.8, Q1 120.7, median 335.4, Q3 478.2, p90 614.0, max 821.8 (n = 93, total 30,293 s).
51 of the 93 units were certified above 300 s. Check times were at most 80.1 s (total 4,706 s).

## Per unit

| row | node | stratum | prior | lane | result | solve s | check s |
|---|---|---|---|---|---|---|---|
| 35 | `0s0_1s0-2s0__3s0-4s1-5s0-6s1-7s1-8s0` | H3/two | presplit | 0 | certified | 43.7 | 46.8 |
| 79 | `0s0_1s0-2s1__3s0-4s0-5s1-6s0-7s0-8s1` | H3/two | timeout300 | 1 | certified | 455.1 | 73.8 |
| 123 | `0s0_1s0-2s1__3s1-4s1-5s0-6s1-7s0-8s1` | H3/two | timeout300 | 2 | certified | 640.7 | 68.2 |
| 167 | `0s0_1s0-4s1__2s0-3s0-5s1-6s0-7s1-8s1` | H3/two | timeout300 | 0 | certified | 491.8 | 77.4 |
| 211 | `0s0_1s0-4s1__2s1-3s1-5s1-6s0-7s1-8s1` | H3/two | timeout300 | 1 | certified | 693.3 | 78.5 |
| 255 | `0s0_1s0-7s0__2s0-3s0-4s0-5s1-6s0-8s1` | H3/two | timeout300 | 2 | certified | 255.1 | 64.2 |
| 299 | `0s0_1s0-7s1__2s1-3s1-4s0-5s1-6s0-8s1` | H3/two | timeout300 | 0 | certified | 364.1 | 57.7 |
| 343 | `0s0_1s1-2s0__3s1-4s0-5s1-6s0-7s0-8s0` | H3/two | timeout300 | 1 | certified | 501.7 | 71.8 |
| 387 | `0s0_1s1-4s0__2s1-3s1-5s1-6s0-7s1-8s0` | H3/two | timeout300 | 2 | certified | 608.4 | 78.2 |
| 431 | `0s0_1s1-5s0__2s1-3s1-4s1-6s1-7s0-8s0` | H3/two | timeout300 | 0 | certified | 475.7 | 77.5 |
| 475 | `0s0_1s1-5s1__2s1-3s0-4s1-6s0-7s0-8s0` | H3/two | presplit | 1 | certified | 376.7 | 48.8 |
| 519 | `0s0_1s1-7s1__2s1-3s0-4s0-5s1-6s0-8s0` | H3/two | timeout300 | 2 | certified | 480.7 | 66.6 |
| 563 | `0s0_1s1-8s0__2s0-3s1-4s0-5s0-6s0-7s0` | H3/two | presplit | 0 | certified | 89.2 | 50.7 |
| 607 | `0s0_1s1-8s0__2s1-3s1-4s1-5s1-6s0-7s0` | H3/two | presplit | 1 | certified | 120.8 | 44.4 |
| 651 | `0s0_1s1-9s1__2s0-3s0-4s1-5s1-6s0-7s0` | H3/two | never_ran | 2 | certified | 403.9 | 45.5 |
| 695 | `0s0_1s1-9s1__2s1-3s1-4s1-5s1-6s0-7s1` | H3/two | never_ran | 0 | certified | 821.8 | 75.8 |
| 739 | `0s0_2s0-3s1__1s1-4s0-5s1-6s0-7s0-8s1` | H3/two | presplit | 1 | certified | 598.9 | 68.6 |
| 783 | `0s0_2s0-4s1__1s0-3s1-5s0-6s1-7s0-8s1` | H3/two | presplit | 2 | certified | 560.8 | 64.5 |
| 827 | `0s0_2s0-5s0__1s0-3s0-4s0-6s0-7s0-8s1` | H3/two | presplit | 0 | certified | 76.3 | 44.0 |
| 871 | `0s0_2s0-5s0__1s1-3s0-4s1-6s1-7s0-8s1` | H3/two | presplit | 1 | certified | 96.6 | 41.7 |
| 915 | `0s0_2s0-5s1__1s1-3s0-4s0-6s0-7s0-8s0` | H3/two | timeout300 | 2 | certified | 336.2 | 54.7 |
| 959 | `0s0_2s0-6s1__1s0-3s0-4s1-5s1-7s1-8s0` | H3/two | timeout300 | 0 | certified | 512.7 | 67.5 |
| 1003 | `0s0_2s0-6s1__1s1-3s1-4s1-5s0-7s1-8s0` | H3/two | timeout300 | 1 | certified | 549.4 | 67.3 |
| 1047 | `0s0_2s0-7s0__1s1-3s0-4s0-5s1-6s1-8s0` | H3/two | presplit | 2 | certified | 242.8 | 48.8 |
| 1091 | `0s0_2s0-7s1__1s0-3s1-4s0-5s0-6s1-8s0` | H3/two | presplit | 0 | certified | 335.4 | 55.5 |
| 1135 | `0s0_2s0-7s1__1s1-3s1-4s1-5s1-6s1-8s0` | H3/two | presplit | 1 | certified | 547.6 | 80.1 |
| 1179 | `0s0_2s0-8s0__1s1-3s1-4s1-5s1-6s0-7s0` | H3/two | presplit | 2 | certified | 281.4 | 56.9 |
| 1223 | `0s0_2s1-3s0__1s1-4s0-5s1-6s0-7s0-8s1` | H3/two | timeout300 | 0 | certified | 661.0 | 65.0 |
| 1267 | `0s0_2s1-3s1__1s0-4s1-5s0-6s1-7s0-8s1` | H3/two | presplit | 1 | certified | 87.5 | 37.3 |
| 1311 | `0s0_2s1-4s0__1s0-3s0-5s0-6s0-7s1-8s1` | H3/two | timeout300 | 2 | certified | 363.2 | 55.5 |
| 1355 | `0s0_2s1-4s0__1s1-3s1-5s0-6s0-7s1-8s1` | H3/two | timeout300 | 0 | certified | 580.2 | 69.0 |
| 1399 | `0s0_2s1-5s0__1s0-3s1-4s1-6s1-7s1-8s1` | H3/two | presplit | 1 | certified | 363.3 | 53.3 |
| 1443 | `0s0_2s1-6s0__1s0-3s0-4s1-5s0-7s1-8s1` | H3/two | presplit | 2 | certified | 271.1 | 43.6 |
| 1487 | `0s0_2s1-6s0__1s1-3s1-4s0-5s1-7s1-8s1` | H3/two | presplit | 0 | certified | 462.4 | 74.1 |
| 1531 | `0s0_2s1-6s1__1s1-3s0-4s0-5s0-7s1-8s1` | H3/two | presplit | 1 | certified | 137.1 | 41.6 |
| 1575 | `0s0_2s1-7s0__1s0-3s1-4s0-5s1-6s1-8s1` | H3/two | never_ran | 2 | certified | 275.0 | 48.4 |
| 1619 | `0s0_2s1-7s1__1s0-3s1-4s1-5s1-6s0-8s1` | H3/two | timeout300 | 0 | certified | 461.4 | 54.2 |
| 1663 | `0s0_2s1-8s1__1s0-3s1-4s0-5s0-6s1-7s0` | H3/two | presplit | 1 | certified | 354.5 | 47.4 |
| 1707 | `0s0_2s1-8s1__1s1-3s1-4s1-5s1-6s1-7s0` | H3/two | presplit | 2 | certified | 617.7 | 64.0 |
| 1751 | `0s0_2s1-9s0__1s1-3s0-4s1-5s0-6s1-7s0` | H3/two | presplit | 0 | certified | 148.2 | 61.3 |
| 1795 | `0s0_3s0-4s1__1s0-2s1-5s0-6s1-7s1-8s0` | H3/two | presplit | 1 | certified | 673.2 | 63.0 |
| 1839 | `0s0_3s0-5s0__1s0-2s0-4s0-6s0-7s1-8s0` | H3/two | presplit | 2 | certified | 30.3 | 23.1 |
| 1883 | `0s0_3s0-5s0__1s1-2s0-4s1-6s1-7s1-8s0` | H3/two | presplit | 0 | certified | 71.7 | 29.9 |
| 1927 | `0s0_3s0-5s1__1s1-2s0-4s0-6s1-7s0-8s0` | H3/two | timeout300 | 1 | certified | 466.5 | 49.2 |
| 1971 | `0s0_3s0-6s0__1s0-2s1-4s0-5s0-7s0-8s0` | H3/two | presplit | 2 | certified | 82.2 | 40.1 |
| 2015 | `0s0_3s0-6s0__1s1-2s1-4s1-5s1-7s0-8s0` | H3/two | presplit | 0 | certified | 120.6 | 37.0 |
| 2059 | `0s0_3s0-6s1__1s1-2s0-4s1-5s0-7s0-8s0` | H3/two | timeout300 | 1 | certified | 530.3 | 59.0 |
| 2103 | `0s0_3s0-7s0__1s0-2s1-4s0-5s1-6s0-8s0` | H3/two | presplit | 2 | certified | 131.7 | 37.2 |
| 2147 | `0s0_3s0-7s1__1s0-2s0-4s0-5s0-6s0-8s0` | H3/two | presplit | 0 | certified | 224.9 | 38.5 |
| 2191 | `0s0_3s0-7s1__1s1-2s0-4s1-5s1-6s0-8s0` | H3/two | presplit | 1 | certified | 545.6 | 53.2 |
| 2235 | `0s0_3s0-8s0__1s1-2s0-4s1-5s1-6s1-7s0` | H3/two | presplit | 2 | certified | 127.4 | 37.8 |
| 2279 | `0s0_3s0-8s1__1s1-2s1-4s1-5s1-6s1-7s0` | H3/two | timeout300 | 0 | certified | 460.0 | 50.9 |
| 2323 | `0s0_3s1-4s0__1s1-2s0-5s1-6s0-7s1-8s1` | H3/two | timeout300 | 1 | certified | 692.6 | 61.0 |
| 2367 | `0s0_3s1-4s1__1s0-2s1-5s0-6s1-7s1-8s1` | H3/two | presplit | 2 | certified | 69.5 | 33.9 |
| 2411 | `0s0_3s1-5s0__1s0-2s0-4s0-6s0-7s1-8s1` | H3/two | presplit | 0 | certified | 353.8 | 54.2 |
| 2455 | `0s0_3s1-5s0__1s1-2s0-4s1-6s1-7s1-8s1` | H3/two | presplit | 1 | certified | 620.4 | 62.0 |
| 2499 | `0s0_3s1-5s1__1s0-2s1-4s1-6s0-7s1-8s1` | H3/two | presplit | 2 | certified | 91.7 | 34.3 |
| 2543 | `0s0_3s1-7s0__1s0-2s0-4s0-5s1-6s0-8s1` | H3/two | never_ran | 0 | certified | 226.3 | 43.5 |
| 2587 | `0s0_3s1-7s1__1s0-2s0-4s1-5s0-6s1-8s0` | H3/two | timeout300 | 1 | certified | 342.2 | 46.3 |
| 2631 | `0s0_3s1-8s0__1s0-2s1-4s0-5s1-6s0-7s0` | H3/two | presplit | 2 | certified | 204.1 | 43.1 |
| 2675 | `0s0_4s0-5s1__1s0-2s0-3s0-6s0-7s0-8s0` | H3/two | presplit | 0 | certified | 271.9 | 41.4 |
| 2719 | `0s0_4s0-5s1__1s1-2s0-3s1-6s1-7s0-8s0` | H3/two | presplit | 1 | certified | 580.1 | 56.4 |
| 2763 | `0s0_4s0-6s1__1s0-2s1-3s1-5s0-7s0-8s0` | H3/two | presplit | 2 | certified | 453.2 | 56.1 |
| 2807 | `0s0_4s0-7s0__1s0-2s0-3s0-5s1-6s0-8s0` | H3/two | presplit | 0 | certified | 40.0 | 27.5 |
| 2851 | `0s0_4s0-7s0__1s1-2s1-3s0-5s0-6s0-8s0` | H3/two | presplit | 1 | certified | 82.1 | 34.6 |
| 2895 | `0s0_4s0-7s1__1s1-2s0-3s0-5s1-6s0-8s1` | H3/two | presplit | 2 | certified | 680.8 | 64.1 |
| 2939 | `0s0_4s1-5s0__1s0-2s1-3s0-6s0-7s0-8s1` | H3/two | never_ran | 0 | certified | 471.6 | 53.0 |
| 2983 | `0s0_4s1-5s0__1s1-2s1-3s1-6s1-7s0-8s1` | H3/two | never_ran | 1 | certified | 474.8 | 51.4 |
| 3027 | `0s0_4s1-6s0__1s1-2s0-3s0-5s0-7s0-8s0` | H3/two | presplit | 2 | certified | 315.0 | 46.0 |
| 3071 | `0s0_4s1-6s1__1s0-2s0-3s1-5s1-7s0-8s0` | H3/two | presplit | 0 | certified | 105.7 | 36.4 |
| 3115 | `0s0_4s1-6s1__1s1-2s1-3s1-5s0-7s0-8s0` | H3/two | presplit | 1 | certified | 135.1 | 34.9 |
| 3159 | `0s0_4s1-7s0__1s1-2s0-3s0-5s1-6s0-8s0` | H3/two | presplit | 2 | certified | 356.7 | 50.4 |
| 3203 | `0s0_5s0-6s0__1s0-2s1-3s0-4s0-7s0-8s0` | H3/two | presplit | 0 | certified | 17.8 | 18.7 |
| 3247 | `0s0_5s0-6s0__1s1-2s1-3s1-4s1-7s0-8s0` | H3/two | presplit | 1 | certified | 111.4 | 34.2 |
| 3291 | `0s0_5s0-6s1__1s1-2s0-3s1-4s0-7s0-8s0` | H3/two | presplit | 2 | certified | 461.9 | 53.1 |
| 3335 | `0s0_5s1-6s0__1s1-2s1-3s1-4s0-7s0-8s0` | H3/two | timeout300 | 0 | certified | 508.4 | 51.4 |
| 3379 | `0s0-1s1_5__2s0-3s1-4s1-6s1-7s1-8s1` | H6(1,1)/one | timeout300 | 1 | certified | 260.6 | 43.0 |
| 3423 | `0s0-2s1_3__1s1-4s1-5s1-6s0-7s0-8s1` | H6(2,1)/one | timeout300 | 2 | certified | 386.0 | 45.6 |
| 3467 | `0s0-2s1_5__1s0-3s0-4s1-6s1-7s0-8s0` | H6(2,1)/one | timeout300 | 0 | certified | 327.3 | 46.1 |
| 3511 | `0s0-2s1_6__1s0-3s0-4s0-5s0-7s0-8s0` | H6(2,1)/one | timeout300 | 1 | certified | 334.1 | 46.0 |
| 3555 | `0s0-2s1_6__1s1-3s0-4s1-5s1-7s1-8s0` | H6(2,1)/one | timeout300 | 2 | certified | 348.0 | 48.4 |
| 3599 | `0s0-3s1_4__1s1-2s1-5s0-6s0-7s1-8s0` | H6(3,1)/one | never_ran | 0 | certified | 351.0 | 69.8 |
| 3643 | `0s0-3s1_5__1s0-2s1-4s1-6s1-7s1-8s0` | H6(3,1)/one | presplit | 1 | certified | 287.0 | 45.2 |
| 3687 | `0s0-4s0_6__1s0-2s0-3s1-5s0-7s1-8s0` | H6(4,0)/one | presplit | 2 | certified | 47.2 | 41.3 |
| 3731 | `0s0-4s0_6__1s1-2s1-3s0-5s1-7s1-8s0` | H6(4,0)/one | presplit | 0 | certified | 77.7 | 40.4 |
| 3775 | `0s0-5s0_6__1s0-2s1-3s1-4s1-7s0-8s1` | H6(5,0)/one | presplit | 1 | certified | 89.7 | 34.4 |
| 3819 | `0s0-5s0_7__1s0-2s0-3s1-4s0-6s0-8s1` | H6(5,0)/one | presplit | 2 | certified | 52.1 | 27.5 |
| 3863 | `0s0-5s0_7__1s1-2s1-3s0-4s1-6s0-8s1` | H6(5,0)/one | presplit | 0 | certified | 68.3 | 29.5 |
| 3907 | `0s0-5s1_1__2s1-3s0-4s1-6s1-7s1-8s1` | H6(5,1)/one | presplit | 1 | certified | 181.7 | 46.5 |
| 3951 | `0s0-5s1_2__1s0-3s1-4s1-6s0-7s1-8s1` | H6(5,1)/one | presplit | 2 | certified | 188.3 | 38.5 |
| 3995 | `0s0-5s1_6__1s1-2s0-3s1-4s0-7s0-8s0` | H6(5,1)/one | never_ran | 0 | certified | 322.0 | 44.5 |
| 4039 | `0s0-5s1_1s1-10s1__2s0-3s1-4s1-6s0-7s1-8s0` | H6(5,1)/two | never_ran | 1 | certified | 56.9 | 36.8 |
| 4083 | `0s0-5s1_2s1-3s0__1s1-4s0-6s0-7s1-8s1-9s0` | H6(5,1)/two | never_ran | 2 | certified | 40.5 | 25.8 |
