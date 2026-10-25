# C3W6 P06: units of W6.tsv with row ≡ 6 (mod 44), cap 900

Task: `results/C3W6/TASK.md` at c5260b44, with V = P06, LIST = W6.tsv, j = 6, N = 44, H = 4.5.
One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 05:31:51 UTC, END 09:46:51 UTC; all units were done at 07:55 UTC.

**Result: all 94 units certified at cap 900 (lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT` on every one). No timeouts, no split records, no SAT, no proof rejection, no unit that ended early without a certificate, no memory problem.** Each close_tree run ended with `open_frontier 0, unsplittable 0`.

## Tools and base check

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, `TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools`, unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 (c60730422e758ef1cebe7aeddf2dda31c996bf04); cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (example: `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with `results/E2/tools/lrat-check-E2.patch`. Sanity test passed: on {1},{-1}, LRAT `3 0 0` rejected by both, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Details in `tools.txt`.

## Run

3 lanes (`lane0.sh`, `lane1.sh`, `lane2.sh`, started with `setsid nohup`), lane k on the units at positions ≡ k (mod 3) of `units.tsv`; each unit: `close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`. No records seeded. `out.jsonl` holds the records of lane 0, then 1, then 2 (94 lines, one certified record per unit).

Incident: the first launch (05:34:56) had `/opt/bin` missing from PATH, so every close_tree call died within a second with `FileNotFoundError: 'cadical'` before any solver ran (no records written). The lanes were killed and restarted at 05:35:36 with `PATH=/opt/bin:$PATH` (the committed lane scripts include it); the logs of the failed launch are not committed.

## Solve times of the certified units (s)

min 20.3, Q1 92.0, median 211.6, Q3 299.8, p90 350.4, max 382.9. Certified above 300 s: 23 of 94 (none above 383 s).
Check times: min 23.9, median 47.8, max 68.7. Totals: solve 19437 s, check 4407 s. Largest proof 573 MB (deleted after checking).

## Totals per stratum

| stratum | units | certified | timed out | not reached | median solve s | max solve s |
|---|---|---|---|---|---|---|
| H3/two | 76 | 76 | 0 | 0 | 238 | 383 |
| H6(1,1)/one | 2 | 2 | 0 | 0 | 262 | 268 |
| H6(2,1)/one | 4 | 4 | 0 | 0 | 251 | 277 |
| H6(3,1)/one | 2 | 2 | 0 | 0 | 238 | 256 |
| H6(4,0)/one | 1 | 1 | 0 | 0 | 46 | 46 |
| H6(5,0)/one | 3 | 3 | 0 | 0 | 46 | 74 |
| H6(5,1)/one | 4 | 4 | 0 | 0 | 159 | 182 |
| H6(5,1)/two | 2 | 2 | 0 | 0 | 25 | 29 |

## Totals per prior

| prior | units | certified | timed out | not reached | median solve s | max solve s |
|---|---|---|---|---|---|---|
| never_ran | 10 | 10 | 0 | 0 | 188 | 368 |
| presplit | 58 | 58 | 0 | 0 | 159 | 374 |
| timeout300 | 26 | 26 | 0 | 0 | 295 | 383 |

## Per unit

| row | node | stratum | prior | lane | result | solve s | check s |
|---|---|---|---|---|---|---|---|
| 6 | `0s0_1s0-10s0__2s1-3s1-4s0-5s0-6s1-7s0` | H3/two | timeout300 | 0 | certified | 205.9 | 62.7 |
| 50 | `0s0_1s0-2s0__3s1-4s0-5s0-6s1-7s0-8s1` | H3/two | presplit | 1 | certified | 29.0 | 37.8 |
| 94 | `0s0_1s0-2s1__3s0-4s1-5s1-6s0-7s0-8s0` | H3/two | timeout300 | 2 | certified | 262.9 | 53.2 |
| 138 | `0s0_1s0-3s1__2s1-4s0-5s0-6s0-7s1-8s0` | H3/two | timeout300 | 0 | certified | 318.2 | 63.5 |
| 182 | `0s0_1s0-4s1__2s0-3s1-5s1-6s1-7s0-8s1` | H3/two | timeout300 | 1 | certified | 351.8 | 65.4 |
| 226 | `0s0_1s0-5s1__2s1-3s0-4s0-6s1-7s0-8s1` | H3/two | timeout300 | 2 | certified | 345.0 | 64.6 |
| 270 | `0s0_1s0-7s0__2s0-3s1-4s1-5s1-6s0-8s1` | H3/two | timeout300 | 0 | certified | 190.3 | 52.2 |
| 314 | `0s0_1s1-2s0__3s0-4s0-5s1-6s0-7s1-8s1` | H3/two | timeout300 | 1 | certified | 294.9 | 65.2 |
| 358 | `0s0_1s1-2s0__3s1-4s1-5s0-6s1-7s1-8s1` | H3/two | timeout300 | 2 | certified | 296.1 | 60.2 |
| 402 | `0s0_1s1-5s0__2s0-3s1-4s1-6s0-7s1-8s1` | H3/two | timeout300 | 0 | certified | 314.3 | 61.7 |
| 446 | `0s0_1s1-5s1__2s0-3s0-4s1-6s0-7s1-8s1` | H3/two | presplit | 1 | certified | 121.3 | 53.1 |
| 490 | `0s0_1s1-5s1__2s1-3s1-4s0-6s1-7s1-8s1` | H3/two | presplit | 2 | certified | 188.1 | 49.3 |
| 534 | `0s0_1s1-7s1__2s1-3s1-4s0-5s0-6s1-8s1` | H3/two | timeout300 | 0 | certified | 301.1 | 56.8 |
| 578 | `0s0_1s1-8s0__2s0-3s1-4s1-5s1-6s1-7s1` | H3/two | presplit | 1 | certified | 171.0 | 53.2 |
| 622 | `0s0_1s1-8s1__2s1-3s0-4s0-5s1-6s0-7s1` | H3/two | timeout300 | 2 | certified | 295.0 | 47.6 |
| 666 | `0s0_1s1-9s1__2s1-3s0-4s0-5s0-6s0-7s0` | H3/two | never_ran | 0 | certified | 178.9 | 48.1 |
| 710 | `0s0_2s0-3s1__1s0-4s0-5s1-6s1-7s0-8s0` | H3/two | presplit | 1 | certified | 335.1 | 68.7 |
| 754 | `0s0_2s0-3s1__1s1-4s1-5s1-6s0-7s0-8s0` | H3/two | presplit | 2 | certified | 343.1 | 57.8 |
| 798 | `0s0_2s0-4s1__1s1-3s0-5s0-6s1-7s0-8s0` | H3/two | presplit | 0 | certified | 299.4 | 56.1 |
| 842 | `0s0_2s0-5s0__1s0-3s1-4s0-6s0-7s0-8s0` | H3/two | presplit | 1 | certified | 39.5 | 36.2 |
| 886 | `0s0_2s0-5s0__1s1-3s1-4s1-6s1-7s0-8s0` | H3/two | presplit | 2 | certified | 83.8 | 41.5 |
| 930 | `0s0_2s0-5s1__1s1-3s0-4s1-6s1-7s1-8s1` | H3/two | timeout300 | 0 | certified | 374.2 | 57.6 |
| 974 | `0s0_2s0-6s1__1s0-3s1-4s1-5s1-7s0-8s1` | H3/two | timeout300 | 1 | certified | 382.9 | 59.8 |
| 1018 | `0s0_2s0-7s0__1s0-3s0-4s1-5s0-6s0-8s1` | H3/two | presplit | 2 | certified | 106.9 | 40.4 |
| 1062 | `0s0_2s0-7s0__1s1-3s1-4s0-5s1-6s0-8s1` | H3/two | presplit | 0 | certified | 154.1 | 37.9 |
| 1106 | `0s0_2s0-7s1__1s1-3s0-4s0-5s0-6s0-8s1` | H3/two | presplit | 1 | certified | 217.3 | 47.5 |
| 1150 | `0s0_2s0-8s0__1s0-3s1-4s1-5s1-6s1-7s1` | H3/two | presplit | 2 | certified | 94.6 | 36.2 |
| 1194 | `0s0_2s1-3s0__1s0-4s0-5s1-6s1-7s0-8s0` | H3/two | timeout300 | 0 | certified | 314.0 | 50.2 |
| 1238 | `0s0_2s1-3s0__1s1-4s1-5s1-6s0-7s0-8s0` | H3/two | timeout300 | 1 | certified | 319.0 | 54.4 |
| 1282 | `0s0_2s1-3s1__1s1-4s0-5s0-6s1-7s0-8s0` | H3/two | presplit | 2 | certified | 51.3 | 33.8 |
| 1326 | `0s0_2s1-4s0__1s0-3s1-5s0-6s1-7s0-8s1` | H3/two | timeout300 | 0 | certified | 307.3 | 51.3 |
| 1370 | `0s0_2s1-5s0__1s0-3s0-4s0-6s0-7s1-8s0` | H3/two | presplit | 1 | certified | 165.9 | 40.6 |
| 1414 | `0s0_2s1-5s0__1s1-3s0-4s1-6s1-7s1-8s0` | H3/two | presplit | 2 | certified | 373.8 | 51.8 |
| 1458 | `0s0_2s1-6s0__1s0-3s1-4s1-5s0-7s1-8s0` | H3/two | presplit | 0 | certified | 201.5 | 42.2 |
| 1502 | `0s0_2s1-6s1__1s0-3s0-4s0-5s1-7s1-8s0` | H3/two | presplit | 1 | certified | 101.3 | 36.3 |
| 1546 | `0s0_2s1-6s1__1s1-3s1-4s0-5s0-7s1-8s0` | H3/two | presplit | 2 | certified | 92.3 | 34.2 |
| 1590 | `0s0_2s1-7s0__1s1-3s0-4s0-5s1-6s1-8s0` | H3/two | never_ran | 0 | certified | 296.0 | 50.4 |
| 1634 | `0s0_2s1-7s1__1s1-3s0-4s1-5s1-6s0-8s0` | H3/two | never_ran | 1 | certified | 175.8 | 41.5 |
| 1678 | `0s0_2s1-8s1__1s1-3s0-4s0-5s0-6s0-7s1` | H3/two | presplit | 2 | certified | 126.4 | 38.6 |
| 1722 | `0s0_2s1-9s0__1s0-3s0-4s1-5s1-6s0-7s1` | H3/two | presplit | 0 | certified | 76.7 | 49.2 |
| 1766 | `0s0_2s1-9s0__1s1-3s1-4s1-5s0-6s0-7s1` | H3/two | presplit | 1 | certified | 90.2 | 35.3 |
| 1810 | `0s0_3s0-4s1__1s1-2s0-5s0-6s1-7s0-8s1` | H3/two | presplit | 2 | certified | 333.9 | 53.7 |
| 1854 | `0s0_3s0-5s0__1s0-2s1-4s0-6s0-7s0-8s1` | H3/two | presplit | 0 | certified | 34.6 | 23.9 |
| 1898 | `0s0_3s0-5s0__1s1-2s1-4s1-6s1-7s0-8s1` | H3/two | presplit | 1 | certified | 58.0 | 28.9 |
| 1942 | `0s0_3s0-5s1__1s1-2s1-4s0-6s0-7s1-8s1` | H3/two | timeout300 | 2 | certified | 360.9 | 50.6 |
| 1986 | `0s0_3s0-6s0__1s0-2s1-4s1-5s1-7s1-8s1` | H3/two | presplit | 0 | certified | 65.1 | 31.6 |
| 2030 | `0s0_3s0-6s1__1s0-2s0-4s1-5s0-7s1-8s1` | H3/two | timeout300 | 1 | certified | 277.0 | 47.6 |
| 2074 | `0s0_3s0-6s1__1s1-2s1-4s0-5s1-7s1-8s1` | H3/two | never_ran | 2 | certified | 359.6 | 50.8 |
| 2118 | `0s0_3s0-7s0__1s1-2s0-4s0-5s0-6s1-8s1` | H3/two | presplit | 0 | certified | 86.9 | 35.8 |
| 2162 | `0s0_3s0-7s1__1s0-2s0-4s1-5s1-6s1-8s1` | H3/two | presplit | 1 | certified | 293.1 | 52.0 |
| 2206 | `0s0_3s0-7s1__1s1-2s1-4s1-5s0-6s1-8s1` | H3/two | presplit | 2 | certified | 276.2 | 64.5 |
| 2250 | `0s0_3s0-8s0__1s1-2s1-4s1-5s1-6s0-7s1` | H3/two | presplit | 0 | certified | 123.2 | 36.1 |
| 2294 | `0s0_3s1-4s0__1s0-2s0-5s1-6s1-7s1-8s0` | H3/two | timeout300 | 1 | certified | 291.6 | 51.6 |
| 2338 | `0s0_3s1-4s0__1s1-2s1-5s1-6s0-7s1-8s0` | H3/two | never_ran | 2 | certified | 367.8 | 55.6 |
| 2382 | `0s0_3s1-4s1__1s1-2s0-5s0-6s1-7s1-8s0` | H3/two | presplit | 0 | certified | 43.5 | 31.1 |
| 2426 | `0s0_3s1-5s0__1s0-2s1-4s0-6s0-7s1-8s0` | H3/two | presplit | 1 | certified | 269.5 | 47.8 |
| 2470 | `0s0_3s1-5s0__1s1-2s1-4s1-6s1-7s1-8s0` | H3/two | presplit | 2 | certified | 304.9 | 49.0 |
| 2514 | `0s0_3s1-5s1__1s1-2s0-4s1-6s0-7s1-8s0` | H3/two | presplit | 0 | certified | 49.4 | 30.7 |
| 2558 | `0s0_3s1-7s0__1s1-2s0-4s0-5s1-6s0-8s0` | H3/two | never_ran | 1 | certified | 196.2 | 59.6 |
| 2602 | `0s0_3s1-7s1__1s1-2s0-4s1-5s1-6s1-8s0` | H3/two | timeout300 | 2 | certified | 244.8 | 62.6 |
| 2646 | `0s0_3s1-8s0__1s1-2s0-4s0-5s0-6s1-7s1` | H3/two | presplit | 0 | certified | 230.5 | 43.4 |
| 2690 | `0s0_4s0-5s1__1s0-2s0-3s1-6s1-7s1-8s1` | H3/two | presplit | 1 | certified | 289.9 | 61.7 |
| 2734 | `0s0_4s0-5s1__1s1-2s1-3s1-6s0-7s1-8s1` | H3/two | presplit | 2 | certified | 371.8 | 49.2 |
| 2778 | `0s0_4s0-6s1__1s1-2s0-3s0-5s1-7s1-8s1` | H3/two | presplit | 0 | certified | 285.0 | 54.7 |
| 2822 | `0s0_4s0-7s0__1s0-2s1-3s0-5s0-6s1-8s1` | H3/two | presplit | 1 | certified | 58.2 | 44.8 |
| 2866 | `0s0_4s0-7s0__1s1-2s1-3s1-5s1-6s1-8s1` | H3/two | presplit | 2 | certified | 91.2 | 32.6 |
| 2910 | `0s0_4s0-7s1__1s1-2s1-3s0-5s1-6s0-8s0` | H3/two | presplit | 0 | certified | 307.7 | 49.0 |
| 2954 | `0s0_4s1-5s0__1s1-2s0-3s0-6s0-7s0-8s0` | H3/two | never_ran | 1 | certified | 205.9 | 43.8 |
| 2998 | `0s0_4s1-6s0__1s0-2s0-3s0-5s0-7s1-8s1` | H3/two | presplit | 2 | certified | 172.1 | 42.5 |
| 3042 | `0s0_4s1-6s0__1s1-2s0-3s1-5s1-7s1-8s1` | H3/two | presplit | 0 | certified | 327.3 | 50.8 |
| 3086 | `0s0_4s1-6s1__1s0-2s1-3s1-5s0-7s1-8s1` | H3/two | presplit | 1 | certified | 63.2 | 31.3 |
| 3130 | `0s0_4s1-7s0__1s0-2s0-3s0-5s1-6s1-8s1` | H3/two | presplit | 2 | certified | 190.1 | 42.9 |
| 3174 | `0s0_4s1-7s0__1s1-2s1-3s0-5s0-6s1-8s1` | H3/two | presplit | 0 | certified | 349.1 | 51.5 |
| 3218 | `0s0_5s0-6s0__1s0-2s1-3s1-4s1-7s1-8s1` | H3/two | presplit | 1 | certified | 52.0 | 35.8 |
| 3262 | `0s0_5s0-6s1__1s0-2s0-3s1-4s0-7s1-8s1` | H3/two | presplit | 2 | certified | 275.3 | 53.4 |
| 3306 | `0s0_5s0-6s1__1s1-2s1-3s0-4s1-7s1-8s1` | H3/two | presplit | 0 | certified | 357.8 | 56.7 |
| 3350 | `0s0-1s1_4__2s1-3s0-5s0-6s1-7s1-8s1` | H6(1,1)/one | timeout300 | 1 | certified | 267.7 | 44.8 |
| 3394 | `0s0-1s1_5__2s1-3s0-4s1-6s1-7s1-8s0` | H6(1,1)/one | timeout300 | 2 | certified | 257.3 | 47.8 |
| 3438 | `0s0-2s1_4__1s1-3s0-5s1-6s0-7s1-8s0` | H6(2,1)/one | timeout300 | 0 | certified | 244.9 | 42.1 |
| 3482 | `0s0-2s1_5__1s1-3s0-4s0-6s0-7s1-8s1` | H6(2,1)/one | timeout300 | 1 | certified | 258.0 | 61.3 |
| 3526 | `0s0-2s1_6__1s0-3s1-4s0-5s0-7s0-8s1` | H6(2,1)/one | timeout300 | 2 | certified | 165.5 | 47.2 |
| 3570 | `0s0-2s1_6__1s1-3s1-4s1-5s1-7s0-8s1` | H6(2,1)/one | timeout300 | 0 | certified | 276.9 | 45.8 |
| 3614 | `0s0-3s1_5__1s0-2s0-4s0-6s0-7s0-8s1` | H6(3,1)/one | presplit | 1 | certified | 219.0 | 45.0 |
| 3658 | `0s0-3s1_5__1s1-2s0-4s1-6s1-7s0-8s1` | H6(3,1)/one | presplit | 2 | certified | 256.4 | 50.6 |
| 3702 | `0s0-4s0_6__1s0-2s1-3s1-5s0-7s0-8s1` | H6(4,0)/one | presplit | 0 | certified | 45.5 | 29.5 |
| 3746 | `0s0-5s0_6__1s0-2s0-3s0-4s0-7s0-8s0` | H6(5,0)/one | presplit | 1 | certified | 46.0 | 46.7 |
| 3790 | `0s0-5s0_6__1s1-2s0-3s1-4s1-7s0-8s0` | H6(5,0)/one | presplit | 2 | certified | 74.2 | 36.6 |
| 3834 | `0s0-5s0_7__1s0-2s1-3s1-4s0-6s0-8s0` | H6(5,0)/one | presplit | 0 | certified | 41.4 | 30.9 |
| 3878 | `0s0-5s1_1__2s0-3s1-4s0-6s0-7s1-8s0` | H6(5,1)/one | presplit | 1 | certified | 164.2 | 47.7 |
| 3922 | `0s0-5s1_1__2s1-3s1-4s1-6s1-7s1-8s0` | H6(5,1)/one | presplit | 2 | certified | 85.8 | 34.1 |
| 3966 | `0s0-5s1_2__1s1-3s0-4s1-6s0-7s1-8s0` | H6(5,1)/one | presplit | 0 | certified | 182.2 | 44.6 |
| 4010 | `0s0-5s1_6__1s1-2s1-3s0-4s1-7s1-8s1` | H6(5,1)/one | never_ran | 1 | certified | 153.4 | 41.8 |
| 4054 | `0s0-5s1_1s1-10s1__2s1-3s0-4s1-6s0-7s0-8s1` | H6(5,1)/two | never_ran | 2 | certified | 28.8 | 25.6 |
| 4098 | `0s0-5s1_2s1-3s0__1s1-4s1-6s1-7s1-8s0-9s1` | H6(5,1)/two | never_ran | 0 | certified | 20.3 | 33.6 |
