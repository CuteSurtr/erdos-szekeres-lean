# C3W6 P18: shard 18 of 44 of W6.tsv, one machine

Task: `results/C3W6/TASK.md` at c5260b44, with V = P18, LIST = W6.tsv, j = 18, N = 44, H = 4.5. One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 05:31:26 UTC, END 09:46:26 UTC; the three lanes started at 05:34:04 and all finished at 07:36 UTC, before END.

## Tools and base CNF

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, TOOLS = `/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 (c60730422e758ef1cebe7aeddf2dda31c996bf04); cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (example prints `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with `results/E2/tools/lrat-check-E2.patch`. Sanity test passed: on {1},{-1}, LRAT `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Details in `tools.txt`. My first launch at 05:33 was missing `/opt/bin` from PATH. Every unit failed within a second (`No such file or directory: 'cadical'`) and no record was written. I deleted those logs and the empty out files and restarted the lanes at 05:34:04 with PATH set (`lane*.sh`).

## Result

**All 93 units are certified at cap 900:** status UNSATISFIABLE, lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT` on every one. Each unit has one record in `out.jsonl` (lane 0, then 1, then 2). No unit timed out, so no split records were written and `open_frontier` is 0 for every unit. There was no SAT, no proof rejection, no checker result `none`, no recheck (so there is no `recheck.jsonl`), no memory problem, and no unit ended early without a certificate (all 23 solves under 72 s are certified).

Solve time of the certified units: min 19.8 s, quartiles 73.4 / 203.2 / 274.8 s, p90 320.1 s, max 384.5 s. 15 were certified above 300 s. Totals: solve 17482 s, check 3794 s. Largest proof 633 MB (no proofs committed).

### Totals per stratum and prior

| stratum | prior | units | certified | timed out at 900 | not reached |
|---|---|---|---|---|---|
| H3/two | never_ran | 6 | 6 | 0 | 0 |
| H3/two | presplit | 48 | 48 | 0 | 0 |
| H3/two | timeout300 | 22 | 22 | 0 | 0 |
| H6(1,1)/one | timeout300 | 2 | 2 | 0 | 0 |
| H6(2,1)/one | timeout300 | 3 | 3 | 0 | 0 |
| H6(3,1)/one | presplit | 2 | 2 | 0 | 0 |
| H6(3,1)/one | timeout300 | 1 | 1 | 0 | 0 |
| H6(4,0)/one | presplit | 1 | 1 | 0 | 0 |
| H6(5,0)/one | presplit | 3 | 3 | 0 | 0 |
| H6(5,1)/one | presplit | 3 | 3 | 0 | 0 |
| H6(5,1)/two | never_ran | 2 | 2 | 0 | 0 |

Per stratum: H3/two 76/76, H6(1,1)/one 2/2, H6(2,1)/one 3/3, H6(3,1)/one 3/3, H6(4,0)/one 1/1, H6(5,0)/one 3/3, H6(5,1)/one 3/3, H6(5,1)/two 2/2 certified.

Per prior: never_ran 8/8, presplit 57/57, timeout300 28/28 certified.

### Per unit

| row | node | stratum | prior | result | solve s | check s |
|---|---|---|---|---|---|---|
| 18 | `0s0_1s0-2s0__3s0-4s0-5s0-6s1-7s0-8s1` | H3/two | presplit | certified | 19.8 | 33.3 |
| 62 | `0s0_1s0-2s0__3s1-4s1-5s0-6s0-7s0-8s1` | H3/two | presplit | certified | 27.9 | 42.1 |
| 106 | `0s0_1s0-2s1__3s1-4s0-5s0-6s1-7s0-8s0` | H3/two | timeout300 | certified | 294.3 | 59.1 |
| 150 | `0s0_1s0-3s1__2s1-4s0-5s1-6s1-7s1-8s1` | H3/two | timeout300 | certified | 384.5 | 62.6 |
| 194 | `0s0_1s0-4s1__2s1-3s0-5s1-6s0-7s1-8s0` | H3/two | timeout300 | certified | 290.1 | 62.3 |
| 238 | `0s0_1s0-5s1__2s1-3s1-4s0-6s1-7s0-8s0` | H3/two | timeout300 | certified | 296.7 | 52.4 |
| 282 | `0s0_1s0-7s0__2s1-3s0-4s1-5s0-6s1-8s0` | H3/two | timeout300 | certified | 121.8 | 46.6 |
| 326 | `0s0_1s1-2s0__3s0-4s1-5s0-6s1-7s1-8s1` | H3/two | timeout300 | certified | 321.8 | 60.0 |
| 370 | `0s0_1s1-4s0__2s0-3s1-5s1-6s0-7s1-8s1` | H3/two | timeout300 | certified | 275.3 | 54.0 |
| 414 | `0s0_1s1-5s0__2s1-3s0-4s1-6s0-7s1-8s0` | H3/two | timeout300 | certified | 221.2 | 46.8 |
| 458 | `0s0_1s1-5s1__2s0-3s1-4s0-6s1-7s1-8s1` | H3/two | presplit | certified | 103.7 | 48.3 |
| 502 | `0s0_1s1-7s1__2s0-3s0-4s1-5s1-6s1-8s1` | H3/two | timeout300 | certified | 222.7 | 46.6 |
| 546 | `0s0_1s1-7s1__2s1-3s1-4s1-5s1-6s1-8s1` | H3/two | timeout300 | certified | 227.3 | 46.0 |
| 590 | `0s0_1s1-8s0__2s1-3s0-4s1-5s0-6s1-7s1` | H3/two | presplit | certified | 92.1 | 39.2 |
| 634 | `0s0_1s1-8s1__2s1-3s1-4s0-5s0-6s1-7s1` | H3/two | timeout300 | certified | 317.7 | 49.6 |
| 678 | `0s0_1s1-9s1__2s1-3s0-4s1-5s1-6s0-7s0` | H3/two | never_ran | certified | 247.9 | 53.8 |
| 722 | `0s0_2s0-3s1__1s0-4s1-5s1-6s0-7s0-8s0` | H3/two | presplit | certified | 274.3 | 53.5 |
| 766 | `0s0_2s0-4s1__1s0-3s0-5s0-6s1-7s0-8s0` | H3/two | presplit | certified | 203.0 | 43.2 |
| 810 | `0s0_2s0-4s1__1s1-3s1-5s0-6s0-7s0-8s0` | H3/two | presplit | certified | 222.1 | 51.2 |
| 854 | `0s0_2s0-5s0__1s0-3s1-4s1-6s1-7s0-8s0` | H3/two | presplit | certified | 44.3 | 35.9 |
| 898 | `0s0_2s0-5s1__1s0-3s0-4s1-6s1-7s1-8s1` | H3/two | timeout300 | certified | 240.8 | 43.7 |
| 942 | `0s0_2s0-5s1__1s1-3s1-4s1-6s0-7s1-8s1` | H3/two | timeout300 | certified | 296.8 | 52.4 |
| 986 | `0s0_2s0-6s1__1s1-3s0-4s1-5s0-7s0-8s1` | H3/two | timeout300 | certified | 219.3 | 47.1 |
| 1030 | `0s0_2s0-7s0__1s0-3s1-4s0-5s1-6s0-8s1` | H3/two | presplit | certified | 99.6 | 39.2 |
| 1074 | `0s0_2s0-7s1__1s0-3s0-4s0-5s0-6s0-8s1` | H3/two | presplit | certified | 143.0 | 38.0 |
| 1118 | `0s0_2s0-7s1__1s1-3s0-4s1-5s1-6s0-8s1` | H3/two | presplit | certified | 218.8 | 41.3 |
| 1162 | `0s0_2s0-8s0__1s1-3s0-4s1-5s0-6s1-7s1` | H3/two | presplit | certified | 170.3 | 36.7 |
| 1206 | `0s0_2s1-3s0__1s0-4s1-5s1-6s0-7s0-8s0` | H3/two | timeout300 | certified | 284.9 | 42.3 |
| 1250 | `0s0_2s1-3s1__1s0-4s0-5s0-6s1-7s0-8s0` | H3/two | presplit | certified | 42.9 | 30.2 |
| 1294 | `0s0_2s1-3s1__1s1-4s1-5s0-6s0-7s0-8s0` | H3/two | presplit | certified | 36.6 | 21.2 |
| 1338 | `0s0_2s1-4s0__1s1-3s0-5s0-6s0-7s1-8s0` | H3/two | timeout300 | certified | 260.7 | 44.9 |
| 1382 | `0s0_2s1-5s0__1s0-3s0-4s1-6s1-7s1-8s0` | H3/two | presplit | certified | 242.9 | 41.5 |
| 1426 | `0s0_2s1-5s0__1s1-3s1-4s1-6s0-7s1-8s0` | H3/two | presplit | certified | 333.4 | 47.9 |
| 1470 | `0s0_2s1-6s0__1s1-3s0-4s0-5s1-7s1-8s0` | H3/two | presplit | certified | 302.7 | 46.6 |
| 1514 | `0s0_2s1-6s1__1s0-3s1-4s0-5s0-7s1-8s0` | H3/two | presplit | certified | 87.7 | 34.1 |
| 1558 | `0s0_2s1-6s1__1s1-3s1-4s1-5s1-7s1-8s0` | H3/two | presplit | certified | 164.8 | 33.3 |
| 1602 | `0s0_2s1-7s0__1s1-3s1-4s0-5s0-6s1-8s0` | H3/two | never_ran | certified | 203.2 | 39.6 |
| 1646 | `0s0_2s1-7s1__1s1-3s1-4s1-5s0-6s0-8s0` | H3/two | never_ran | certified | 174.4 | 34.1 |
| 1690 | `0s0_2s1-8s1__1s1-3s0-4s1-5s1-6s0-7s1` | H3/two | presplit | certified | 260.0 | 39.4 |
| 1734 | `0s0_2s1-9s0__1s0-3s1-4s1-5s0-6s0-7s1` | H3/two | presplit | certified | 60.1 | 28.8 |
| 1778 | `0s0_3s0-4s1__1s0-2s0-5s0-6s1-7s0-8s1` | H3/two | presplit | certified | 229.1 | 52.9 |
| 1822 | `0s0_3s0-4s1__1s1-2s1-5s0-6s0-7s0-8s1` | H3/two | presplit | certified | 306.2 | 44.8 |
| 1866 | `0s0_3s0-5s0__1s0-2s1-4s1-6s1-7s0-8s1` | H3/two | presplit | certified | 30.7 | 19.3 |
| 1910 | `0s0_3s0-5s1__1s0-2s1-4s0-6s0-7s1-8s1` | H3/two | timeout300 | certified | 313.7 | 47.2 |
| 1954 | `0s0_3s0-5s1__1s1-2s1-4s1-6s1-7s1-8s1` | H3/two | timeout300 | certified | 261.1 | 53.9 |
| 1998 | `0s0_3s0-6s0__1s1-2s0-4s1-5s0-7s1-8s1` | H3/two | presplit | certified | 48.1 | 26.2 |
| 2042 | `0s0_3s0-6s1__1s0-2s1-4s0-5s1-7s1-8s1` | H3/two | timeout300 | certified | 259.9 | 46.2 |
| 2086 | `0s0_3s0-7s0__1s0-2s0-4s0-5s0-6s1-8s1` | H3/two | presplit | certified | 56.7 | 26.4 |
| 2130 | `0s0_3s0-7s0__1s1-2s0-4s1-5s1-6s1-8s1` | H3/two | presplit | certified | 63.4 | 32.5 |
| 2174 | `0s0_3s0-7s1__1s0-2s1-4s1-5s0-6s1-8s1` | H3/two | presplit | certified | 313.3 | 45.1 |
| 2218 | `0s0_3s0-8s0__1s0-2s1-4s1-5s1-6s0-7s1` | H3/two | presplit | certified | 80.4 | 31.4 |
| 2262 | `0s0_3s0-8s1__1s0-2s1-4s1-5s1-6s0-7s1` | H3/two | timeout300 | certified | 235.0 | 39.6 |
| 2306 | `0s0_3s1-4s0__1s0-2s1-5s1-6s0-7s1-8s0` | H3/two | timeout300 | certified | 332.1 | 48.4 |
| 2350 | `0s0_3s1-4s1__1s0-2s0-5s0-6s1-7s1-8s0` | H3/two | presplit | certified | 56.1 | 27.1 |
| 2394 | `0s0_3s1-4s1__1s1-2s1-5s0-6s0-7s1-8s0` | H3/two | presplit | certified | 51.8 | 26.5 |
| 2438 | `0s0_3s1-5s0__1s0-2s1-4s1-6s1-7s1-8s0` | H3/two | presplit | certified | 363.7 | 49.2 |
| 2482 | `0s0_3s1-5s1__1s0-2s0-4s1-6s0-7s1-8s0` | H3/two | presplit | certified | 53.7 | 27.7 |
| 2526 | `0s0_3s1-5s1__1s1-2s1-4s0-6s1-7s1-8s0` | H3/two | presplit | certified | 48.8 | 29.6 |
| 2570 | `0s0_3s1-7s0__1s1-2s1-4s0-5s0-6s0-8s0` | H3/two | never_ran | certified | 176.0 | 35.5 |
| 2614 | `0s0_3s1-8s0__1s0-2s0-4s0-5s0-6s1-7s1` | H3/two | presplit | certified | 151.2 | 37.1 |
| 2658 | `0s0_3s1-8s0__1s1-2s0-4s1-5s1-6s1-7s1` | H3/two | presplit | certified | 224.1 | 37.3 |
| 2702 | `0s0_4s0-5s1__1s0-2s1-3s1-6s0-7s1-8s1` | H3/two | presplit | certified | 381.1 | 65.9 |
| 2746 | `0s0_4s0-6s1__1s0-2s0-3s0-5s1-7s1-8s1` | H3/two | presplit | certified | 219.7 | 40.4 |
| 2790 | `0s0_4s0-6s1__1s1-2s1-3s0-5s0-7s1-8s1` | H3/two | presplit | certified | 332.0 | 47.4 |
| 2834 | `0s0_4s0-7s0__1s0-2s1-3s1-5s1-6s1-8s1` | H3/two | presplit | certified | 63.7 | 29.9 |
| 2878 | `0s0_4s0-7s1__1s0-2s1-3s0-5s1-6s0-8s0` | H3/two | presplit | certified | 245.7 | 40.7 |
| 2922 | `0s0_4s1-5s0__1s0-2s0-3s0-6s0-7s0-8s0` | H3/two | never_ran | certified | 138.3 | 33.2 |
| 2966 | `0s0_4s1-5s0__1s1-2s0-3s1-6s1-7s0-8s0` | H3/two | never_ran | certified | 344.8 | 48.2 |
| 3010 | `0s0_4s1-6s0__1s0-2s0-3s1-5s1-7s1-8s1` | H3/two | presplit | certified | 296.1 | 55.9 |
| 3054 | `0s0_4s1-6s0__1s1-2s1-3s1-5s0-7s1-8s1` | H3/two | presplit | certified | 309.0 | 46.8 |
| 3098 | `0s0_4s1-6s1__1s1-2s0-3s0-5s1-7s1-8s1` | H3/two | presplit | certified | 61.7 | 28.7 |
| 3142 | `0s0_4s1-7s0__1s0-2s1-3s0-5s0-6s1-8s1` | H3/two | presplit | certified | 254.8 | 42.3 |
| 3186 | `0s0_4s1-7s0__1s1-2s1-3s1-5s1-6s1-8s1` | H3/two | presplit | certified | 253.5 | 36.8 |
| 3230 | `0s0_5s0-6s0__1s1-2s0-3s1-4s0-7s1-8s1` | H3/two | presplit | certified | 37.1 | 35.1 |
| 3274 | `0s0_5s0-6s1__1s0-2s1-3s0-4s1-7s1-8s1` | H3/two | presplit | certified | 295.1 | 44.5 |
| 3318 | `0s0_5s1-6s0__1s1-2s0-3s0-4s1-7s0-8s1` | H3/two | timeout300 | certified | 321.7 | 46.2 |
| 3362 | `0s0-1s1_5__2s0-3s0-4s0-6s1-7s1-8s0` | H6(1,1)/one | timeout300 | certified | 136.5 | 36.2 |
| 3406 | `0s0-1s1_5__2s1-3s1-4s1-6s0-7s1-8s0` | H6(1,1)/one | timeout300 | certified | 201.7 | 36.6 |
| 3450 | `0s0-2s1_4__1s1-3s1-5s0-6s1-7s1-8s0` | H6(2,1)/one | timeout300 | certified | 233.7 | 38.8 |
| 3494 | `0s0-2s1_5__1s1-3s0-4s1-6s1-7s1-8s1` | H6(2,1)/one | timeout300 | certified | 164.2 | 37.8 |
| 3538 | `0s0-2s1_6__1s0-3s1-4s1-5s1-7s0-8s1` | H6(2,1)/one | timeout300 | certified | 234.2 | 49.7 |
| 3582 | `0s0-3s1_4__1s0-2s1-5s1-6s0-7s1-8s1` | H6(3,1)/one | timeout300 | certified | 203.2 | 36.8 |
| 3626 | `0s0-3s1_5__1s0-2s0-4s1-6s1-7s0-8s1` | H6(3,1)/one | presplit | certified | 198.2 | 37.1 |
| 3670 | `0s0-3s1_5__1s1-2s1-4s1-6s0-7s0-8s1` | H6(3,1)/one | presplit | certified | 190.6 | 45.5 |
| 3714 | `0s0-4s0_6__1s1-2s0-3s0-5s1-7s0-8s1` | H6(4,0)/one | presplit | certified | 41.9 | 25.4 |
| 3758 | `0s0-5s0_6__1s0-2s0-3s1-4s1-7s0-8s0` | H6(5,0)/one | presplit | certified | 64.2 | 29.6 |
| 3802 | `0s0-5s0_6__1s1-2s1-3s1-4s0-7s0-8s0` | H6(5,0)/one | presplit | certified | 62.4 | 29.0 |
| 3846 | `0s0-5s0_7__1s1-2s0-3s0-4s1-6s0-8s0` | H6(5,0)/one | presplit | certified | 66.4 | 29.6 |
| 3890 | `0s0-5s1_1__2s0-3s1-4s1-6s1-7s1-8s0` | H6(5,1)/one | presplit | certified | 110.6 | 43.2 |
| 3934 | `0s0-5s1_2__1s0-3s0-4s1-6s0-7s1-8s0` | H6(5,1)/one | presplit | certified | 114.3 | 34.5 |
| 3978 | `0s0-5s1_2__1s1-3s1-4s0-6s1-7s1-8s0` | H6(5,1)/one | presplit | certified | 143.2 | 37.0 |
| 4022 | `0s0-5s1_1s1-10s1__2s0-3s0-4s1-6s0-7s0-8s1` | H6(5,1)/two | never_ran | certified | 19.8 | 24.3 |
| 4066 | `0s0-5s1_1s1-10s1__2s1-3s1-4s0-6s1-7s0-8s1` | H6(5,1)/two | never_ran | certified | 36.6 | 28.4 |
