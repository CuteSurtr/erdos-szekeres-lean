# C3W6 P34

Task `results/C3W6/TASK.md` at c5260b44 with V = P34, LIST = W6.tsv, j = 34, N = 44, H = 4.5.
Start 2026-10-25 05:31:49 UTC, END 09:46:49 UTC (start + 4.5 h − 15 min). All three lanes finished before END
(lane 2 at 08:00:05, lane 0 at 08:01:09, lane 1 at 08:33:31 UTC).

## Tools and base check (`tools.txt`)

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, `TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools`, unmodified; `compose.py` not run.
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (example: `s VERIFIED UNSAT`);
  lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with `results/E2/tools/lrat-check-E2.patch`. Sanity test on {1},{-1}:
  `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).

## Run

93 units: the rows of `lists/W6.tsv` with row ≡ 34 (mod 44) (`units.tsv`), no seeding. 3 lanes (`lane0.sh`, `lane1.sh`, `lane2.sh`,
lane k = positions ≡ k mod 3, 31 units each). Each unit ran
`close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`.
`out.jsonl` holds the 93 records (lane 0, 1, 2); `driver{k}.log.tail` are the last 100 lines of the driver logs.

## Result

**All 93 units certified** at cap 900 (one solve each, `open_frontier` 0 for every unit): every record has `status` UNSATISFIABLE,
`lrat_check` `c VERIFIED` and `cake_lpr` `s VERIFIED UNSAT`. No unit timed out, so there are no split records; none was left unreached.

- SAT: none. Proof rejections: none (no `recheck.jsonl`). cake_lpr `none`: none. Memory problems: none (at most ~5 GB used of 15 GB).
- Units that ended early: none without a certificate. Six units were solved in under 72 s (10.7–56 s) and all six were certified, so they did not end early.

Totals per stratum (all certified): H3/two 76; H6(1,1)/one 1; H6(2,1)/one 4; H6(3,1)/one 2; H6(4,0)/one 2; H6(5,0)/one 3; H6(5,1)/one 3; H6(5,1)/two 2.

Totals per prior (all certified): timeout300 28; never_ran 9; presplit 55; layer_leaf 1.

Solve-time distribution over the 93 certified units (s): min 10.7, Q1 101.1, median 286.6, Q3 374.8, p90 448.6, max 547.3.
43 of 93 were certified above 300 s (all under 900). Total solve 23,394 s, total check 4,639 s.

## Per unit

| row | node | stratum | prior | result | solve s | check s |
|---|---|---|---|---|---|---|
| 34 | `0s0_1s0-2s0__3s0-4s1-5s0-6s1-7s0-8s1` | H3/two | presplit | certified | 27.2 | 40.9 |
| 78 | `0s0_1s0-2s1__3s0-4s0-5s1-6s0-7s0-8s0` | H3/two | timeout300 | certified | 289.7 | 63.8 |
| 122 | `0s0_1s0-2s1__3s1-4s1-5s0-6s1-7s0-8s0` | H3/two | timeout300 | certified | 328.0 | 62.4 |
| 166 | `0s0_1s0-4s1__2s0-3s0-5s1-6s0-7s1-8s0` | H3/two | timeout300 | certified | 286.6 | 64.7 |
| 210 | `0s0_1s0-4s1__2s1-3s1-5s1-6s0-7s1-8s0` | H3/two | timeout300 | certified | 459.6 | 71.7 |
| 254 | `0s0_1s0-7s0__2s0-3s0-4s0-5s0-6s1-8s1` | H3/two | timeout300 | certified | 175.4 | 58.5 |
| 298 | `0s0_1s0-7s0__2s1-3s1-4s1-5s1-6s0-8s1` | H3/two | timeout300 | certified | 159.0 | 58.7 |
| 342 | `0s0_1s1-2s0__3s1-4s0-5s0-6s1-7s1-8s1` | H3/two | timeout300 | certified | 450.1 | 70.7 |
| 386 | `0s0_1s1-4s0__2s1-3s1-5s1-6s0-7s0-8s1` | H3/two | timeout300 | certified | 396.6 | 73.9 |
| 430 | `0s0_1s1-5s0__2s1-3s1-4s1-6s0-7s1-8s1` | H3/two | timeout300 | certified | 370.5 | 64.0 |
| 474 | `0s0_1s1-5s1__2s1-3s0-4s0-6s1-7s1-8s1` | H3/two | presplit | certified | 134.4 | 48.4 |
| 518 | `0s0_1s1-7s1__2s1-3s0-4s0-5s0-6s1-8s1` | H3/two | timeout300 | certified | 324.4 | 57.8 |
| 562 | `0s0_1s1-8s0__2s0-3s0-4s1-5s1-6s1-7s1` | H3/two | presplit | certified | 192.4 | 58.2 |
| 606 | `0s0_1s1-8s0__2s1-3s1-4s1-5s0-6s1-7s1` | H3/two | presplit | certified | 109.2 | 50.2 |
| 650 | `0s0_1s1-9s1__2s0-3s0-4s1-5s0-6s1-7s1` | H3/two | never_ran | certified | 377.5 | 60.5 |
| 694 | `0s0_1s1-9s1__2s1-3s1-4s1-5s1-6s0-7s0` | H3/two | never_ran | certified | 436.9 | 61.1 |
| 738 | `0s0_2s0-3s1__1s1-4s0-5s1-6s0-7s0-8s0` | H3/two | presplit | certified | 357.9 | 67.3 |
| 782 | `0s0_2s0-4s1__1s0-3s1-5s0-6s1-7s0-8s0` | H3/two | presplit | certified | 431.3 | 60.2 |
| 826 | `0s0_2s0-5s0__1s0-3s0-4s0-6s0-7s0-8s0` | H3/two | presplit | certified | 52.9 | 54.2 |
| 870 | `0s0_2s0-5s0__1s1-3s0-4s1-6s1-7s0-8s0` | H3/two | presplit | certified | 79.9 | 43.9 |
| 914 | `0s0_2s0-5s1__1s0-3s1-4s1-6s1-7s1-8s1` | H3/two | timeout300 | certified | 351.1 | 57.4 |
| 958 | `0s0_2s0-6s1__1s0-3s0-4s1-5s1-7s0-8s1` | H3/two | timeout300 | certified | 354.2 | 53.6 |
| 1002 | `0s0_2s0-6s1__1s1-3s1-4s1-5s0-7s0-8s1` | H3/two | timeout300 | certified | 470.0 | 71.4 |
| 1046 | `0s0_2s0-7s0__1s1-3s0-4s0-5s1-6s0-8s1` | H3/two | presplit | certified | 187.2 | 48.2 |
| 1090 | `0s0_2s0-7s1__1s0-3s1-4s0-5s0-6s0-8s1` | H3/two | presplit | certified | 296.0 | 59.4 |
| 1134 | `0s0_2s0-7s1__1s1-3s1-4s1-5s1-6s0-8s1` | H3/two | presplit | certified | 391.7 | 58.9 |
| 1178 | `0s0_2s0-8s0__1s1-3s1-4s1-5s0-6s1-7s1` | H3/two | presplit | certified | 156.3 | 40.7 |
| 1222 | `0s0_2s1-3s0__1s1-4s0-5s1-6s0-7s0-8s0` | H3/two | timeout300 | certified | 356.3 | 56.4 |
| 1266 | `0s0_2s1-3s1__1s0-4s1-5s0-6s1-7s0-8s0` | H3/two | presplit | certified | 50.5 | 29.2 |
| 1310 | `0s0_2s1-4s0_9s1-10s0__1s0-3s1-5s0-6s0-7s0-8s1` | H3/two | layer_leaf | certified | 10.7 | 34.6 |
| 1354 | `0s0_2s1-4s0__1s1-3s1-5s0-6s0-7s1-8s0` | H3/two | timeout300 | certified | 407.3 | 69.2 |
| 1398 | `0s0_2s1-5s0__1s0-3s1-4s1-6s1-7s1-8s0` | H3/two | presplit | certified | 358.8 | 53.0 |
| 1442 | `0s0_2s1-6s0__1s0-3s0-4s1-5s0-7s1-8s0` | H3/two | presplit | certified | 215.0 | 46.0 |
| 1486 | `0s0_2s1-6s0__1s1-3s1-4s0-5s1-7s1-8s0` | H3/two | presplit | certified | 250.6 | 51.4 |
| 1530 | `0s0_2s1-6s1__1s1-3s0-4s0-5s0-7s1-8s0` | H3/two | presplit | certified | 109.9 | 36.6 |
| 1574 | `0s0_2s1-7s0__1s0-3s1-4s0-5s1-6s1-8s0` | H3/two | never_ran | certified | 235.2 | 45.0 |
| 1618 | `0s0_2s1-7s1__1s0-3s1-4s1-5s1-6s0-8s0` | H3/two | timeout300 | certified | 355.0 | 63.3 |
| 1662 | `0s0_2s1-8s1__1s0-3s1-4s0-5s0-6s0-7s1` | H3/two | presplit | certified | 284.7 | 47.3 |
| 1706 | `0s0_2s1-8s1__1s1-3s1-4s1-5s1-6s0-7s1` | H3/two | presplit | certified | 472.2 | 56.4 |
| 1750 | `0s0_2s1-9s0__1s1-3s0-4s1-5s0-6s0-7s1` | H3/two | presplit | certified | 135.2 | 38.8 |
| 1794 | `0s0_3s0-4s1__1s0-2s1-5s0-6s1-7s0-8s1` | H3/two | presplit | certified | 496.9 | 66.2 |
| 1838 | `0s0_3s0-5s0__1s0-2s0-4s0-6s0-7s0-8s1` | H3/two | presplit | certified | 18.8 | 19.1 |
| 1882 | `0s0_3s0-5s0__1s1-2s0-4s1-6s1-7s0-8s1` | H3/two | presplit | certified | 49.0 | 26.5 |
| 1926 | `0s0_3s0-5s1__1s1-2s0-4s0-6s0-7s1-8s1` | H3/two | timeout300 | certified | 397.8 | 64.2 |
| 1970 | `0s0_3s0-6s0__1s0-2s0-4s1-5s1-7s1-8s1` | H3/two | presplit | certified | 61.4 | 43.6 |
| 2014 | `0s0_3s0-6s0__1s1-2s1-4s1-5s0-7s1-8s1` | H3/two | presplit | certified | 111.0 | 55.3 |
| 2058 | `0s0_3s0-6s1__1s1-2s0-4s0-5s1-7s1-8s1` | H3/two | timeout300 | certified | 446.3 | 57.1 |
| 2102 | `0s0_3s0-7s0__1s0-2s1-4s0-5s0-6s1-8s1` | H3/two | presplit | certified | 148.5 | 39.9 |
| 2146 | `0s0_3s0-7s0__1s1-2s1-4s1-5s1-6s1-8s1` | H3/two | presplit | certified | 142.8 | 39.5 |
| 2190 | `0s0_3s0-7s1__1s1-2s0-4s1-5s0-6s1-8s1` | H3/two | presplit | certified | 481.6 | 60.5 |
| 2234 | `0s0_3s0-8s0__1s1-2s0-4s1-5s1-6s0-7s1` | H3/two | presplit | certified | 120.3 | 41.3 |
| 2278 | `0s0_3s0-8s1__1s1-2s1-4s1-5s1-6s0-7s1` | H3/two | timeout300 | certified | 319.4 | 55.6 |
| 2322 | `0s0_3s1-4s0__1s1-2s0-5s1-6s0-7s1-8s0` | H3/two | timeout300 | certified | 547.3 | 68.3 |
| 2366 | `0s0_3s1-4s1__1s0-2s1-5s0-6s1-7s1-8s0` | H3/two | presplit | certified | 61.9 | 35.5 |
| 2410 | `0s0_3s1-5s0__1s0-2s0-4s0-6s0-7s1-8s0` | H3/two | presplit | certified | 237.7 | 47.7 |
| 2454 | `0s0_3s1-5s0__1s1-2s0-4s1-6s1-7s1-8s0` | H3/two | presplit | certified | 434.1 | 55.2 |
| 2498 | `0s0_3s1-5s1__1s0-2s1-4s1-6s0-7s1-8s0` | H3/two | presplit | certified | 70.5 | 35.4 |
| 2542 | `0s0_3s1-6s0__1s1-2s1-4s1-5s1-7s0-8s1` | H3/two | timeout300 | certified | 504.3 | 58.7 |
| 2586 | `0s0_3s1-7s1__1s0-2s0-4s0-5s1-6s1-8s0` | H3/two | timeout300 | certified | 289.6 | 50.1 |
| 2630 | `0s0_3s1-8s0__1s0-2s1-4s0-5s0-6s1-7s1` | H3/two | presplit | certified | 323.6 | 44.5 |
| 2674 | `0s0_3s1-8s0__1s1-2s1-4s1-5s1-6s1-7s1` | H3/two | presplit | certified | 316.5 | 42.8 |
| 2718 | `0s0_4s0-5s1__1s1-2s0-3s1-6s0-7s1-8s1` | H3/two | presplit | certified | 476.4 | 61.3 |
| 2762 | `0s0_4s0-6s1__1s0-2s1-3s0-5s1-7s1-8s1` | H3/two | presplit | certified | 375.5 | 51.6 |
| 2806 | `0s0_4s0-7s0__1s0-2s0-3s0-5s0-6s1-8s1` | H3/two | presplit | certified | 55.0 | 34.0 |
| 2850 | `0s0_4s0-7s0__1s1-2s0-3s1-5s1-6s1-8s1` | H3/two | presplit | certified | 89.5 | 41.2 |
| 2894 | `0s0_4s0-7s1__1s1-2s0-3s0-5s1-6s0-8s0` | H3/two | presplit | certified | 317.4 | 49.0 |
| 2938 | `0s0_4s1-5s0__1s0-2s1-3s0-6s0-7s0-8s0` | H3/two | never_ran | certified | 345.2 | 65.2 |
| 2982 | `0s0_4s1-5s0__1s1-2s1-3s1-6s1-7s0-8s0` | H3/two | never_ran | certified | 445.8 | 57.0 |
| 3026 | `0s0_4s1-6s0__1s0-2s1-3s1-5s1-7s1-8s1` | H3/two | presplit | certified | 410.0 | 55.2 |
| 3070 | `0s0_4s1-6s1__1s0-2s0-3s1-5s0-7s1-8s1` | H3/two | presplit | certified | 76.4 | 33.0 |
| 3114 | `0s0_4s1-6s1__1s1-2s1-3s0-5s1-7s1-8s1` | H3/two | presplit | certified | 75.1 | 36.6 |
| 3158 | `0s0_4s1-7s0__1s1-2s0-3s0-5s0-6s1-8s1` | H3/two | presplit | certified | 385.4 | 58.7 |
| 3202 | `0s0_5s0-6s0__1s0-2s0-3s1-4s1-7s1-8s1` | H3/two | presplit | certified | 56.0 | 30.9 |
| 3246 | `0s0_5s0-6s0__1s1-2s1-3s1-4s0-7s1-8s1` | H3/two | presplit | certified | 41.2 | 24.3 |
| 3290 | `0s0_5s0-6s1__1s1-2s0-3s0-4s1-7s1-8s1` | H3/two | presplit | certified | 374.1 | 56.0 |
| 3334 | `0s0_5s1-6s0__1s1-2s1-3s0-4s1-7s1-8s1` | H3/two | timeout300 | certified | 386.6 | 55.3 |
| 3378 | `0s0-1s1_5__2s0-3s1-4s1-6s1-7s1-8s0` | H6(1,1)/one | timeout300 | certified | 332.3 | 51.0 |
| 3422 | `0s0-2s1_3__1s1-4s1-5s1-6s0-7s0-8s0` | H6(2,1)/one | timeout300 | certified | 335.0 | 47.7 |
| 3466 | `0s0-2s1_5__1s0-3s0-4s1-6s0-7s1-8s1` | H6(2,1)/one | timeout300 | certified | 209.3 | 46.2 |
| 3510 | `0s0-2s1_5__1s1-3s1-4s1-6s1-7s1-8s1` | H6(2,1)/one | timeout300 | certified | 301.1 | 51.6 |
| 3554 | `0s0-2s1_6__1s1-3s0-4s1-5s1-7s0-8s1` | H6(2,1)/one | timeout300 | certified | 273.0 | 51.5 |
| 3598 | `0s0-3s1_4__1s1-2s1-5s0-6s0-7s0-8s1` | H6(3,1)/one | never_ran | certified | 307.7 | 47.6 |
| 3642 | `0s0-3s1_5__1s0-2s1-4s1-6s1-7s0-8s1` | H6(3,1)/one | presplit | certified | 356.8 | 51.5 |
| 3686 | `0s0-4s0_6__1s0-2s0-3s1-5s0-7s0-8s1` | H6(4,0)/one | presplit | certified | 31.4 | 23.8 |
| 3730 | `0s0-4s0_6__1s1-2s1-3s0-5s1-7s0-8s1` | H6(4,0)/one | presplit | certified | 75.2 | 43.2 |
| 3774 | `0s0-5s0_6__1s0-2s1-3s1-4s1-7s0-8s0` | H6(5,0)/one | presplit | certified | 86.3 | 36.1 |
| 3818 | `0s0-5s0_7__1s0-2s0-3s1-4s0-6s0-8s0` | H6(5,0)/one | presplit | certified | 49.9 | 35.8 |
| 3862 | `0s0-5s0_7__1s1-2s1-3s0-4s1-6s0-8s0` | H6(5,0)/one | presplit | certified | 92.9 | 33.6 |
| 3906 | `0s0-5s1_1__2s1-3s0-4s1-6s1-7s1-8s0` | H6(5,1)/one | presplit | certified | 144.5 | 44.8 |
| 3950 | `0s0-5s1_2__1s0-3s1-4s1-6s0-7s1-8s0` | H6(5,1)/one | presplit | certified | 138.1 | 44.9 |
| 3994 | `0s0-5s1_6__1s1-2s0-3s0-4s1-7s1-8s1` | H6(5,1)/one | never_ran | certified | 201.5 | 42.2 |
| 4038 | `0s0-5s1_1s1-10s1__2s0-3s1-4s1-6s0-7s0-8s1` | H6(5,1)/two | never_ran | certified | 47.7 | 33.0 |
| 4082 | `0s0-5s1_2s1-3s0__1s1-4s0-6s0-7s1-8s0-9s1` | H6(5,1)/two | never_ran | certified | 35.0 | 30.2 |
