# C3W6 / P42: shard 42 of 44 of W6.tsv, one pass at cap 900

**Result: all 93 units certified (both checkers). 0 timed out at 900 s, 0 not reached. No SAT, no proof rejection, no memory problem, no unit that ended early without a certificate.**

## Setup

- Task: `results/C3W6/TASK.md` at c5260b44, V = P42, LIST = W6.tsv, j = 42, N = 44, H = 4.5.
- Tools: worktree of cad4e050 at /opt/c3u2, TOOLS = `results/C3U2/tools`, unmodified. CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04, cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (example prints `s VERIFIED UNSAT`), lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with the E2 patch (sanity: `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both). Details in `tools.txt`.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Machine: 4 cores, 15 GB, no swap (`env.txt`). Start 05:31:26 UTC, lanes started 05:34:59, END 09:46:26. Lanes finished at 08:31:24 (lane 0), 08:46:42 (lane 2) and 08:59:25 (lane 1), before END; nothing was killed.
- 93 units (rows ≡ 42 mod 44, `units.tsv`), 3 lanes (`lane0.sh`..`lane2.sh`, positions ≡ k mod 3), each unit `close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`. No records seeded. `compose.py` not run. `watchdog.sh` was there to kill the lane process groups at END; it was not needed.
- `out.jsonl`: 93 records (lane 0, 1, 2), all `UNSATISFIABLE` with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`; no split records (no unit timed out). No `recheck.jsonl` (no re-check was needed).

## Totals

| stratum | units | certified | timed out at 900 | not reached |
|---|---|---|---|---|
| H3/two | 75 | 75 | 0 | 0 |
| H6(1,1)/one | 2 | 2 | 0 | 0 |
| H6(2,1)/one | 4 | 4 | 0 | 0 |
| H6(3,1)/one | 2 | 2 | 0 | 0 |
| H6(4,0)/one | 2 | 2 | 0 | 0 |
| H6(5,0)/one | 3 | 3 | 0 | 0 |
| H6(5,1)/one | 3 | 3 | 0 | 0 |
| H6(5,1)/two | 2 | 2 | 0 | 0 |
| **all** | 93 | 93 | 0 | 0 |

| prior | units | certified | timed out at 900 | not reached | median solve s | max solve s |
|---|---|---|---|---|---|---|
| never_ran | 10 | 10 | 0 | 0 | 335.4 | 464.3 |
| presplit | 55 | 55 | 0 | 0 | 207.6 | 691.6 |
| timeout300 | 28 | 28 | 0 | 0 | 422.2 | 722.2 |

Solve times of the 93 certified units: min 29.0 s, Q1 120.0, median 331.7, Q3 445.6, p90 546.3, max 722.2 s. **53 of 93 were certified above 300 s** (none above 900). 9 units were certified in under 72 s (that is a certificate, not an early end). Sum of solve times 29283 s, sum of check times 4817 s (3 lanes sharing 4 cores, so per-node times are somewhat inflated).

## Per unit

| pos | row | node | stratum | prior | result | solve s | check s |
|---|---|---|---|---|---|---|---|
| 0 | 42 | `0s0_1s0-2s0__3s0-4s1-5s1-6s1-7s0-8s1` | H3/two | presplit | certified | 36.7 | 48.4 |
| 1 | 86 | `0s0_1s0-2s1__3s0-4s1-5s0-6s0-7s0-8s0` | H3/two | timeout300 | certified | 357.8 | 67.3 |
| 2 | 130 | `0s0_1s0-2s1__3s1-4s1-5s1-6s1-7s0-8s0` | H3/two | timeout300 | certified | 426.1 | 62.4 |
| 3 | 174 | `0s0_1s0-4s1__2s0-3s1-5s0-6s1-7s0-8s1` | H3/two | timeout300 | certified | 433.0 | 71.1 |
| 4 | 218 | `0s0_1s0-5s1__2s0-3s1-4s1-6s1-7s0-8s0` | H3/two | timeout300 | certified | 419.6 | 70.3 |
| 5 | 262 | `0s0_1s0-7s0__2s0-3s0-4s1-5s1-6s0-8s1` | H3/two | timeout300 | certified | 285.8 | 68.9 |
| 6 | 306 | `0s0_1s0-7s1__2s1-3s1-4s1-5s1-6s0-8s0` | H3/two | timeout300 | certified | 387.8 | 73.7 |
| 7 | 350 | `0s0_1s1-2s0__3s1-4s0-5s1-6s1-7s1-8s1` | H3/two | timeout300 | certified | 536.5 | 69.5 |
| 8 | 394 | `0s0_1s1-5s0__2s0-3s0-4s0-6s1-7s1-8s0` | H3/two | timeout300 | certified | 308.7 | 65.6 |
| 9 | 438 | `0s0_1s1-5s1__2s0-3s0-4s0-6s0-7s1-8s1` | H3/two | presplit | certified | 195.0 | 55.7 |
| 10 | 482 | `0s0_1s1-5s1__2s1-3s0-4s1-6s1-7s1-8s1` | H3/two | presplit | certified | 265.3 | 55.2 |
| 11 | 526 | `0s0_1s1-7s1__2s1-3s0-4s1-5s0-6s1-8s1` | H3/two | timeout300 | certified | 578.9 | 80.0 |
| 12 | 570 | `0s0_1s1-8s0__2s0-3s1-4s0-5s1-6s1-7s1` | H3/two | presplit | certified | 176.7 | 62.4 |
| 13 | 614 | `0s0_1s1-8s1__2s0-3s1-4s0-5s1-6s1-7s1` | H3/two | timeout300 | certified | 548.7 | 64.6 |
| 14 | 658 | `0s0_1s1-9s1__2s0-3s1-4s1-5s0-6s0-7s0` | H3/two | never_ran | certified | 410.0 | 58.2 |
| 15 | 702 | `0s0_2s0-3s1__1s0-4s0-5s0-6s1-7s0-8s0` | H3/two | presplit | certified | 327.0 | 59.4 |
| 16 | 746 | `0s0_2s0-3s1__1s1-4s1-5s0-6s0-7s0-8s0` | H3/two | presplit | certified | 445.5 | 76.6 |
| 17 | 790 | `0s0_2s0-4s1__1s0-3s1-5s1-6s1-7s0-8s0` | H3/two | presplit | certified | 527.2 | 70.2 |
| 18 | 834 | `0s0_2s0-5s0__1s0-3s0-4s1-6s0-7s0-8s0` | H3/two | presplit | certified | 60.4 | 44.4 |
| 19 | 878 | `0s0_2s0-5s0__1s1-3s1-4s0-6s1-7s0-8s0` | H3/two | presplit | certified | 93.7 | 38.8 |
| 20 | 922 | `0s0_2s0-5s1__1s1-3s0-4s0-6s1-7s1-8s1` | H3/two | timeout300 | certified | 531.6 | 65.7 |
| 21 | 966 | `0s0_2s0-6s1__1s0-3s1-4s0-5s1-7s0-8s1` | H3/two | timeout300 | certified | 445.6 | 65.2 |
| 22 | 1010 | `0s0_2s0-7s0__1s0-3s0-4s0-5s0-6s0-8s1` | H3/two | presplit | certified | 138.5 | 44.3 |
| 23 | 1054 | `0s0_2s0-7s0__1s1-3s0-4s1-5s1-6s0-8s1` | H3/two | presplit | certified | 227.5 | 52.4 |
| 24 | 1098 | `0s0_2s0-7s1__1s0-3s1-4s1-5s0-6s0-8s1` | H3/two | presplit | certified | 411.3 | 53.4 |
| 25 | 1142 | `0s0_2s0-8s0__1s0-3s1-4s0-5s1-6s1-7s1` | H3/two | presplit | certified | 140.0 | 37.6 |
| 26 | 1186 | `0s0_2s1-3s0__1s0-4s0-5s0-6s1-7s0-8s0` | H3/two | timeout300 | certified | 378.4 | 56.5 |
| 27 | 1230 | `0s0_2s1-3s0__1s1-4s1-5s0-6s0-7s0-8s0` | H3/two | timeout300 | certified | 433.7 | 65.8 |
| 28 | 1274 | `0s0_2s1-3s1__1s0-4s1-5s1-6s1-7s0-8s0` | H3/two | presplit | certified | 79.3 | 36.2 |
| 29 | 1318 | `0s0_2s1-4s0__1s0-3s0-5s1-6s0-7s1-8s1` | H3/two | timeout300 | certified | 437.0 | 54.9 |
| 30 | 1362 | `0s0_2s1-4s0__1s1-3s1-5s1-6s0-7s1-8s0` | H3/two | timeout300 | certified | 569.5 | 61.9 |
| 31 | 1406 | `0s0_2s1-5s0__1s1-3s0-4s0-6s1-7s1-8s0` | H3/two | presplit | certified | 454.8 | 55.5 |
| 32 | 1450 | `0s0_2s1-6s0__1s0-3s1-4s0-5s0-7s1-8s0` | H3/two | presplit | certified | 285.2 | 45.8 |
| 33 | 1494 | `0s0_2s1-6s0__1s1-3s1-4s1-5s1-7s1-8s0` | H3/two | presplit | certified | 474.9 | 56.6 |
| 34 | 1538 | `0s0_2s1-6s1__1s1-3s0-4s1-5s0-7s1-8s0` | H3/two | presplit | certified | 155.4 | 40.1 |
| 35 | 1582 | `0s0_2s1-7s0__1s0-3s1-4s1-5s1-6s1-8s0` | H3/two | never_ran | certified | 459.5 | 67.0 |
| 36 | 1626 | `0s0_2s1-7s1__1s1-3s0-4s0-5s1-6s0-8s0` | H3/two | never_ran | certified | 248.0 | 41.1 |
| 37 | 1670 | `0s0_2s1-8s1__1s0-3s1-4s1-5s0-6s0-7s1` | H3/two | presplit | certified | 495.2 | 54.4 |
| 38 | 1714 | `0s0_2s1-9s0__1s0-3s0-4s0-5s1-6s0-7s1` | H3/two | presplit | certified | 103.8 | 31.7 |
| 39 | 1758 | `0s0_2s1-9s0__1s1-3s1-4s0-5s0-6s0-7s1` | H3/two | presplit | certified | 148.0 | 38.2 |
| 40 | 1802 | `0s0_3s0-4s1__1s0-2s1-5s1-6s1-7s0-8s1` | H3/two | presplit | certified | 656.0 | 63.9 |
| 41 | 1846 | `0s0_3s0-5s0__1s0-2s0-4s1-6s0-7s0-8s1` | H3/two | presplit | certified | 29.0 | 28.3 |
| 42 | 1890 | `0s0_3s0-5s0__1s1-2s1-4s0-6s1-7s0-8s1` | H3/two | presplit | certified | 88.4 | 38.3 |
| 43 | 1934 | `0s0_3s0-5s1__1s1-2s0-4s1-6s0-7s1-8s1` | H3/two | timeout300 | certified | 672.8 | 71.1 |
| 44 | 1978 | `0s0_3s0-6s0__1s0-2s1-4s0-5s1-7s1-8s1` | H3/two | presplit | certified | 101.6 | 35.5 |
| 45 | 2022 | `0s0_3s0-6s1__1s0-2s0-4s0-5s0-7s1-8s1` | H3/two | timeout300 | certified | 315.9 | 50.4 |
| 46 | 2066 | `0s0_3s0-6s1__1s1-2s0-4s1-5s1-7s1-8s1` | H3/two | timeout300 | certified | 722.2 | 67.2 |
| 47 | 2110 | `0s0_3s0-7s0__1s0-2s1-4s1-5s0-6s1-8s1` | H3/two | presplit | certified | 120.0 | 37.4 |
| 48 | 2154 | `0s0_3s0-7s1__1s0-2s0-4s0-5s1-6s1-8s1` | H3/two | presplit | certified | 360.9 | 56.2 |
| 49 | 2198 | `0s0_3s0-7s1__1s1-2s1-4s0-5s0-6s1-8s1` | H3/two | presplit | certified | 509.7 | 54.0 |
| 50 | 2242 | `0s0_3s0-8s0__1s1-2s1-4s0-5s1-6s0-7s1` | H3/two | presplit | certified | 251.4 | 43.5 |
| 51 | 2286 | `0s0_3s1-4s0__1s0-2s0-5s0-6s1-7s1-8s0` | H3/two | timeout300 | certified | 424.9 | 53.8 |
| 52 | 2330 | `0s0_3s1-4s0__1s1-2s1-5s0-6s0-7s1-8s0` | H3/two | timeout300 | certified | 560.0 | 56.4 |
| 53 | 2374 | `0s0_3s1-4s1__1s0-2s1-5s1-6s1-7s1-8s0` | H3/two | presplit | certified | 66.0 | 35.4 |
| 54 | 2418 | `0s0_3s1-5s0__1s0-2s0-4s1-6s0-7s1-8s0` | H3/two | presplit | certified | 413.7 | 50.4 |
| 55 | 2462 | `0s0_3s1-5s0__1s1-2s1-4s0-6s1-7s1-8s0` | H3/two | presplit | certified | 578.2 | 53.2 |
| 56 | 2506 | `0s0_3s1-5s1__1s1-2s0-4s0-6s0-7s1-8s0` | H3/two | presplit | certified | 92.0 | 33.2 |
| 57 | 2550 | `0s0_3s1-7s0__1s0-2s1-4s1-5s1-6s0-8s0` | H3/two | never_ran | certified | 411.0 | 53.5 |
| 58 | 2594 | `0s0_3s1-7s1__1s0-2s1-4s1-5s0-6s1-8s0` | H3/two | timeout300 | certified | 246.1 | 46.4 |
| 59 | 2638 | `0s0_3s1-8s0__1s0-2s1-4s1-5s0-6s1-7s1` | H3/two | presplit | certified | 341.3 | 72.2 |
| 60 | 2682 | `0s0_4s0-5s1__1s0-2s0-3s0-6s1-7s1-8s1` | H3/two | presplit | certified | 302.3 | 46.5 |
| 61 | 2726 | `0s0_4s0-5s1__1s1-2s1-3s0-6s0-7s1-8s1` | H3/two | presplit | certified | 691.6 | 89.2 |
| 62 | 2770 | `0s0_4s0-6s1__1s0-2s1-3s1-5s1-7s1-8s1` | H3/two | presplit | certified | 482.7 | 53.1 |
| 63 | 2814 | `0s0_4s0-7s0__1s0-2s0-3s1-5s0-6s1-8s1` | H3/two | presplit | certified | 74.6 | 33.7 |
| 64 | 2858 | `0s0_4s0-7s0__1s1-2s1-3s0-5s1-6s1-8s1` | H3/two | presplit | certified | 90.0 | 31.3 |
| 65 | 2902 | `0s0_4s0-7s1__1s1-2s0-3s1-5s1-6s0-8s0` | H3/two | presplit | certified | 509.2 | 53.3 |
| 66 | 2946 | `0s0_4s1-5s0__1s0-2s1-3s1-6s0-7s0-8s0` | H3/two | never_ran | certified | 464.3 | 55.1 |
| 67 | 2990 | `0s0_4s1-5s1__1s1-2s1-3s1-6s0-7s1-8s1` | H3/two | never_ran | certified | 72.9 | 36.8 |
| 68 | 3034 | `0s0_4s1-6s0__1s1-2s0-3s0-5s1-7s1-8s1` | H3/two | presplit | certified | 503.0 | 56.7 |
| 69 | 3078 | `0s0_4s1-6s1__1s0-2s1-3s0-5s0-7s1-8s1` | H3/two | presplit | certified | 107.3 | 36.2 |
| 70 | 3122 | `0s0_4s1-6s1__1s1-2s1-3s1-5s1-7s1-8s1` | H3/two | presplit | certified | 94.1 | 52.6 |
| 71 | 3166 | `0s0_4s1-7s0__1s1-2s0-3s1-5s0-6s1-8s1` | H3/two | presplit | certified | 507.1 | 58.3 |
| 72 | 3210 | `0s0_5s0-6s0__1s0-2s1-3s0-4s1-7s1-8s1` | H3/two | presplit | certified | 56.0 | 50.4 |
| 73 | 3254 | `0s0_5s0-6s1__1s0-2s0-3s0-4s0-7s1-8s1` | H3/two | presplit | certified | 264.6 | 42.4 |
| 74 | 3298 | `0s0_5s0-6s1__1s1-2s0-3s1-4s1-7s1-8s1` | H3/two | presplit | certified | 615.6 | 61.3 |
| 75 | 3342 | `0s0-1s1_4__2s0-3s1-5s1-6s0-7s0-8s0` | H6(1,1)/one | timeout300 | certified | 354.2 | 46.8 |
| 76 | 3386 | `0s0-1s1_5__2s1-3s0-4s0-6s1-7s1-8s0` | H6(1,1)/one | timeout300 | certified | 356.8 | 54.3 |
| 77 | 3430 | `0s0-2s1_4__1s1-3s0-5s0-6s0-7s1-8s0` | H6(2,1)/one | timeout300 | certified | 363.5 | 51.5 |
| 78 | 3474 | `0s0-2s1_5__1s0-3s1-4s1-6s0-7s1-8s1` | H6(2,1)/one | timeout300 | certified | 313.1 | 43.7 |
| 79 | 3518 | `0s0-2s1_6__1s0-3s0-4s0-5s1-7s1-8s1` | H6(2,1)/one | timeout300 | certified | 200.2 | 39.4 |
| 80 | 3562 | `0s0-2s1_6__1s1-3s1-4s0-5s1-7s0-8s1` | H6(2,1)/one | timeout300 | certified | 379.1 | 49.0 |
| 81 | 3606 | `0s0-3s1_4__1s1-2s1-5s1-6s0-7s0-8s1` | H6(3,1)/one | never_ran | certified | 339.2 | 47.1 |
| 82 | 3650 | `0s0-3s1_5__1s1-2s0-4s0-6s1-7s0-8s1` | H6(3,1)/one | presplit | certified | 385.8 | 53.0 |
| 83 | 3694 | `0s0-4s0_6__1s0-2s1-3s0-5s0-7s0-8s1` | H6(4,0)/one | presplit | certified | 49.4 | 29.4 |
| 84 | 3738 | `0s0-4s0_6__1s1-2s1-3s1-5s1-7s0-8s1` | H6(4,0)/one | presplit | certified | 105.2 | 39.6 |
| 85 | 3782 | `0s0-5s0_6__1s1-2s0-3s0-4s1-7s0-8s0` | H6(5,0)/one | presplit | certified | 79.2 | 37.3 |
| 86 | 3826 | `0s0-5s0_7__1s0-2s1-3s0-4s0-6s0-8s0` | H6(5,0)/one | presplit | certified | 62.0 | 34.6 |
| 87 | 3870 | `0s0-5s0_7__1s1-2s1-3s1-4s1-6s0-8s0` | H6(5,0)/one | presplit | certified | 108.6 | 34.5 |
| 88 | 3914 | `0s0-5s1_1__2s1-3s1-4s0-6s1-7s1-8s0` | H6(5,1)/one | presplit | certified | 207.6 | 40.7 |
| 89 | 3958 | `0s0-5s1_2__1s1-3s0-4s0-6s0-7s1-8s0` | H6(5,1)/one | presplit | certified | 328.6 | 59.7 |
| 90 | 4002 | `0s0-5s1_6__1s1-2s0-3s1-4s1-7s1-8s1` | H6(5,1)/one | never_ran | certified | 331.7 | 49.6 |
| 91 | 4046 | `0s0-5s1_1s1-10s1__2s1-3s0-4s0-6s0-7s0-8s1` | H6(5,1)/two | never_ran | certified | 33.1 | 29.4 |
| 92 | 4090 | `0s0-5s1_2s1-3s0__1s1-4s1-6s0-7s1-8s0-9s1` | H6(5,1)/two | never_ran | certified | 51.8 | 33.6 |

## SAT / rejections / incidents

- SAT: none.
- PROOF NOT ACCEPTED / cake_lpr `none`: none.
- Memory: peak about 8 GB used of 15 GB; no problem.
- Units that ended in under 72 s without a certificate: none.
- The first `git pull --rebase` got an HTTP 403 once; the retry worked. All pushes went to es7-cloud.
