# C3W6 / P07: shard 7 of 44 of W6.tsv, cap 900, one machine

**Result: all 94 units certified at cap 900 (cadical UNSAT, lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT` on every one). No timeout, no split record, no SAT, no proof rejection, no memory problem, no unit ended early without a certificate.** All three lanes ran out of units before END (last unit ended 09:14:37 UTC; END was 09:46:28 UTC).

## Setup

- One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 05:31:28 UTC, lanes started 05:34 UTC.
- Task: `results/C3W6/TASK.md` at c5260b44, with V = P07, LIST = W6.tsv, j = 7, N = 44, H = 4.5.
- Tools (`tools.txt`): C3U2 tools from a worktree of cad4e050 at `/opt/c3u2`, unmodified; CaDiCaL 3.0.1 c6073042; cake_lpr a36874a8 (example prints `s VERIFIED UNSAT`); lrat-check 2e3b2dc with the E2 patch (sanity: `3 0 0` on {1},{-1} rejected by both checkers, `3 0 1 2 0` accepted by both).
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Units: the rows of `lists/W6.tsv` with row ≡ 7 (mod 44): 94 units (`units.tsv`), no seeding. 3 lanes (`lane0.sh`–`lane2.sh`, lane k = positions ≡ k mod 3), each `close_tree.py base.cnf out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`. The lanes were set to stop on `SAT FOUND`; proof rejections would have been re-checked alongside (none occurred, so there is no `recheck.jsonl`).
- `compose.py` was not run.

## Totals

| stratum | units | certified | timed out at 900 | not reached | median solve s | max solve s |
|---|---|---|---|---|---|---|
| H3/two | 76 | 76 | 0 | 0 | 357 | 680 |
| H6(1,1)/one | 2 | 2 | 0 | 0 | 378 | 400 |
| H6(2,1)/one | 4 | 4 | 0 | 0 | 425 | 566 |
| H6(3,1)/one | 2 | 2 | 0 | 0 | 400 | 496 |
| H6(4,0)/one | 1 | 1 | 0 | 0 | 74 | 74 |
| H6(5,0)/one | 3 | 3 | 0 | 0 | 81 | 92 |
| H6(5,1)/one | 4 | 4 | 0 | 0 | 264 | 406 |
| H6(5,1)/two | 2 | 2 | 0 | 0 | 40 | 50 |
| **total** | **94** | **94** | 0 | 0 | 348 | 680 |

| prior | units | certified | median solve s | max solve s |
|---|---|---|---|---|
| presplit | 58 | 58 | 199 | 680 |
| timeout300 | 26 | 26 | 415 | 625 |
| never_ran | 10 | 10 | 383 | 578 |

Solve-time distribution of the 94 certified units (seconds, 3 solves sharing 4 cores): min 19.2, Q1 138.8, median 348.1, Q3 471.1, p90 531.5, max 680.4; 54 units certified above 300 s (4 above 600 s). Total solve 29,806 s, total check 4,795 s (check min 19.3, median 50.2, max 81.2). Largest proof 0.58 GB (deleted after checking; no proof or CNF files are committed). 9 units were solved in under 72 s, all with both certificates (the H6(5,*) and H6(4,0) cubes and a few H3/two cubes).

## Per unit

| row | node | stratum | prior | result | solve s | check s |
|---|---|---|---|---|---|---|
| 7 | `0s0_1s0-10s0__2s1-3s1-4s0-5s0-6s1-7s1` | H3/two | timeout300 | certified | 283.3 | 66.3 |
| 51 | `0s0_1s0-2s0__3s1-4s0-5s0-6s1-7s1-8s0` | H3/two | presplit | certified | 49.1 | 51.9 |
| 95 | `0s0_1s0-2s1__3s0-4s1-5s1-6s0-7s0-8s1` | H3/two | timeout300 | certified | 418.2 | 72.1 |
| 139 | `0s0_1s0-3s1__2s1-4s0-5s0-6s0-7s1-8s1` | H3/two | timeout300 | certified | 522.0 | 74.3 |
| 183 | `0s0_1s0-4s1__2s0-3s1-5s1-6s1-7s1-8s0` | H3/two | timeout300 | certified | 400.7 | 70.4 |
| 227 | `0s0_1s0-5s1__2s1-3s0-4s0-6s1-7s1-8s0` | H3/two | timeout300 | certified | 510.6 | 69.5 |
| 271 | `0s0_1s0-7s0__2s0-3s1-4s1-5s1-6s1-8s0` | H3/two | timeout300 | certified | 174.8 | 54.2 |
| 315 | `0s0_1s1-2s0__3s0-4s0-5s1-6s1-7s0-8s0` | H3/two | timeout300 | certified | 440.3 | 78.6 |
| 359 | `0s0_1s1-2s0__3s1-4s1-5s1-6s0-7s0-8s0` | H3/two | timeout300 | certified | 419.5 | 64.1 |
| 403 | `0s0_1s1-5s0__2s0-3s1-4s1-6s1-7s0-8s0` | H3/two | timeout300 | certified | 408.7 | 67.9 |
| 447 | `0s0_1s1-5s1__2s0-3s0-4s1-6s1-7s0-8s0` | H3/two | presplit | certified | 138.8 | 49.8 |
| 491 | `0s0_1s1-5s1__2s1-3s1-4s1-6s0-7s0-8s0` | H3/two | presplit | certified | 285.5 | 69.9 |
| 535 | `0s0_1s1-7s1__2s1-3s1-4s0-5s1-6s0-8s0` | H3/two | timeout300 | certified | 400.6 | 57.4 |
| 579 | `0s0_1s1-8s0__2s1-3s0-4s0-5s0-6s0-7s0` | H3/two | presplit | certified | 61.2 | 46.5 |
| 623 | `0s0_1s1-8s1__2s1-3s0-4s0-5s1-6s1-7s0` | H3/two | timeout300 | certified | 469.1 | 61.3 |
| 667 | `0s0_1s1-9s1__2s1-3s0-4s0-5s0-6s0-7s1` | H3/two | never_ran | certified | 360.4 | 51.8 |
| 711 | `0s0_2s0-3s1__1s0-4s0-5s1-6s1-7s0-8s1` | H3/two | presplit | certified | 432.5 | 65.7 |
| 755 | `0s0_2s0-3s1__1s1-4s1-5s1-6s0-7s0-8s1` | H3/two | presplit | certified | 603.2 | 81.2 |
| 799 | `0s0_2s0-4s1__1s1-3s0-5s0-6s1-7s0-8s1` | H3/two | presplit | certified | 496.9 | 63.6 |
| 843 | `0s0_2s0-5s0__1s0-3s1-4s0-6s0-7s0-8s1` | H3/two | presplit | certified | 48.4 | 38.1 |
| 887 | `0s0_2s0-5s0__1s1-3s1-4s1-6s1-7s0-8s1` | H3/two | presplit | certified | 101.5 | 40.7 |
| 931 | `0s0_2s0-5s1__1s1-3s1-4s0-6s0-7s0-8s0` | H3/two | timeout300 | certified | 399.3 | 53.9 |
| 975 | `0s0_2s0-6s1__1s0-3s1-4s1-5s1-7s1-8s0` | H3/two | timeout300 | certified | 517.7 | 66.4 |
| 1019 | `0s0_2s0-7s0__1s0-3s0-4s1-5s0-6s1-8s0` | H3/two | presplit | certified | 110.4 | 61.1 |
| 1063 | `0s0_2s0-7s0__1s1-3s1-4s0-5s1-6s1-8s0` | H3/two | presplit | certified | 163.9 | 42.7 |
| 1107 | `0s0_2s0-7s1__1s1-3s0-4s0-5s0-6s1-8s0` | H3/two | presplit | certified | 215.4 | 50.7 |
| 1151 | `0s0_2s0-8s0__1s1-3s0-4s0-5s0-6s0-7s0` | H3/two | presplit | certified | 188.5 | 49.3 |
| 1195 | `0s0_2s1-3s0__1s0-4s0-5s1-6s1-7s0-8s1` | H3/two | timeout300 | certified | 506.7 | 58.6 |
| 1239 | `0s0_2s1-3s0__1s1-4s1-5s1-6s0-7s0-8s1` | H3/two | timeout300 | certified | 545.5 | 64.0 |
| 1283 | `0s0_2s1-3s1__1s1-4s0-5s0-6s1-7s0-8s1` | H3/two | presplit | certified | 95.4 | 45.3 |
| 1327 | `0s0_2s1-4s0__1s0-3s1-5s0-6s1-7s1-8s0` | H3/two | timeout300 | certified | 501.5 | 77.6 |
| 1371 | `0s0_2s1-5s0__1s0-3s0-4s0-6s0-7s1-8s1` | H3/two | presplit | certified | 312.9 | 46.8 |
| 1415 | `0s0_2s1-5s0__1s1-3s0-4s1-6s1-7s1-8s1` | H3/two | presplit | certified | 529.5 | 54.3 |
| 1459 | `0s0_2s1-6s0__1s0-3s1-4s1-5s0-7s1-8s1` | H3/two | presplit | certified | 235.1 | 42.7 |
| 1503 | `0s0_2s1-6s1__1s0-3s0-4s0-5s1-7s1-8s1` | H3/two | presplit | certified | 164.3 | 39.2 |
| 1547 | `0s0_2s1-6s1__1s1-3s1-4s0-5s0-7s1-8s1` | H3/two | presplit | certified | 155.9 | 35.8 |
| 1591 | `0s0_2s1-7s0__1s1-3s0-4s0-5s1-6s1-8s1` | H3/two | never_ran | certified | 434.9 | 51.5 |
| 1635 | `0s0_2s1-7s1__1s1-3s0-4s1-5s1-6s0-8s1` | H3/two | never_ran | certified | 312.5 | 45.3 |
| 1679 | `0s0_2s1-8s1__1s1-3s0-4s0-5s0-6s1-7s0` | H3/two | presplit | certified | 206.9 | 41.1 |
| 1723 | `0s0_2s1-9s0__1s0-3s0-4s1-5s1-6s1-7s0` | H3/two | presplit | certified | 118.6 | 37.6 |
| 1767 | `0s0_2s1-9s0__1s1-3s1-4s1-5s0-6s1-7s0` | H3/two | presplit | certified | 138.8 | 39.5 |
| 1811 | `0s0_3s0-4s1__1s1-2s0-5s0-6s1-7s1-8s0` | H3/two | presplit | certified | 491.3 | 55.7 |
| 1855 | `0s0_3s0-5s0__1s0-2s1-4s0-6s0-7s1-8s0` | H3/two | presplit | certified | 57.2 | 33.2 |
| 1899 | `0s0_3s0-5s0__1s1-2s1-4s1-6s1-7s1-8s0` | H3/two | presplit | certified | 100.7 | 31.7 |
| 1943 | `0s0_3s0-5s1__1s1-2s1-4s0-6s1-7s0-8s0` | H3/two | timeout300 | certified | 625.4 | 58.6 |
| 1987 | `0s0_3s0-6s0__1s1-2s0-4s0-5s0-7s0-8s0` | H3/two | presplit | certified | 84.0 | 35.3 |
| 2031 | `0s0_3s0-6s1__1s0-2s0-4s1-5s1-7s0-8s0` | H3/two | timeout300 | certified | 379.5 | 48.2 |
| 2075 | `0s0_3s0-6s1__1s1-2s1-4s1-5s0-7s0-8s0` | H3/two | never_ran | certified | 429.4 | 49.1 |
| 2119 | `0s0_3s0-7s0__1s1-2s0-4s0-5s1-6s0-8s0` | H3/two | presplit | certified | 110.7 | 37.3 |
| 2163 | `0s0_3s0-7s1__1s0-2s1-4s0-5s0-6s0-8s0` | H3/two | presplit | certified | 322.8 | 44.6 |
| 2207 | `0s0_3s0-7s1__1s1-2s1-4s1-5s1-6s0-8s0` | H3/two | presplit | certified | 406.4 | 49.3 |
| 2251 | `0s0_3s0-8s0__1s1-2s1-4s1-5s1-6s1-7s0` | H3/two | presplit | certified | 177.2 | 40.3 |
| 2295 | `0s0_3s1-4s0__1s0-2s0-5s1-6s1-7s1-8s1` | H3/two | timeout300 | certified | 343.6 | 46.3 |
| 2339 | `0s0_3s1-4s0__1s1-2s1-5s1-6s0-7s1-8s1` | H3/two | never_ran | certified | 578.4 | 55.1 |
| 2383 | `0s0_3s1-4s1__1s1-2s0-5s0-6s1-7s1-8s1` | H3/two | presplit | certified | 82.5 | 32.5 |
| 2427 | `0s0_3s1-5s0__1s0-2s1-4s0-6s0-7s1-8s1` | H3/two | presplit | certified | 504.3 | 73.5 |
| 2471 | `0s0_3s1-5s0__1s1-2s1-4s1-6s1-7s1-8s1` | H3/two | presplit | certified | 536.7 | 52.9 |
| 2515 | `0s0_3s1-5s1__1s1-2s0-4s1-6s0-7s1-8s1` | H3/two | presplit | certified | 92.5 | 33.1 |
| 2559 | `0s0_3s1-7s0__1s1-2s0-4s0-5s1-6s0-8s1` | H3/two | never_ran | certified | 352.7 | 46.5 |
| 2603 | `0s0_3s1-7s1__1s1-2s0-4s1-5s1-6s1-8s1` | H3/two | timeout300 | certified | 398.6 | 52.6 |
| 2647 | `0s0_3s1-8s0__1s1-2s0-4s0-5s1-6s0-7s0` | H3/two | presplit | certified | 191.9 | 37.1 |
| 2691 | `0s0_4s0-5s1__1s0-2s1-3s0-6s0-7s0-8s0` | H3/two | presplit | certified | 335.6 | 46.6 |
| 2735 | `0s0_4s0-5s1__1s1-2s1-3s1-6s1-7s0-8s0` | H3/two | presplit | certified | 680.4 | 67.4 |
| 2779 | `0s0_4s0-6s1__1s1-2s0-3s1-5s0-7s0-8s0` | H3/two | presplit | certified | 477.2 | 51.1 |
| 2823 | `0s0_4s0-7s0__1s0-2s1-3s0-5s1-6s0-8s0` | H3/two | presplit | certified | 52.2 | 30.7 |
| 2867 | `0s0_4s0-7s1__1s0-2s0-3s1-5s0-6s0-8s1` | H3/two | presplit | certified | 458.4 | 57.4 |
| 2911 | `0s0_4s0-7s1__1s1-2s1-3s0-5s1-6s0-8s1` | H3/two | presplit | certified | 652.3 | 67.3 |
| 2955 | `0s0_4s1-5s0__1s1-2s0-3s0-6s0-7s0-8s1` | H3/two | never_ran | certified | 500.4 | 53.9 |
| 2999 | `0s0_4s1-6s0__1s0-2s0-3s0-5s1-7s0-8s0` | H3/two | presplit | certified | 296.9 | 55.6 |
| 3043 | `0s0_4s1-6s0__1s1-2s1-3s0-5s0-7s0-8s0` | H3/two | presplit | certified | 325.3 | 67.2 |
| 3087 | `0s0_4s1-6s1__1s0-2s1-3s1-5s1-7s0-8s0` | H3/two | presplit | certified | 129.2 | 40.7 |
| 3131 | `0s0_4s1-7s0__1s0-2s0-3s1-5s0-6s0-8s0` | H3/two | presplit | certified | 404.6 | 46.7 |
| 3175 | `0s0_4s1-7s0__1s1-2s1-3s0-5s1-6s0-8s0` | H3/two | presplit | certified | 500.5 | 55.0 |
| 3219 | `0s0_5s0-6s0__1s1-2s0-3s0-4s0-7s0-8s0` | H3/two | presplit | certified | 19.2 | 19.3 |
| 3263 | `0s0_5s0-6s1__1s0-2s0-3s1-4s1-7s0-8s0` | H3/two | presplit | certified | 477.9 | 54.9 |
| 3307 | `0s0_5s0-6s1__1s1-2s1-3s1-4s0-7s0-8s0` | H3/two | presplit | certified | 533.5 | 72.7 |
| 3351 | `0s0-1s1_4__2s1-3s0-5s1-6s0-7s0-8s1` | H6(1,1)/one | timeout300 | certified | 356.7 | 47.4 |
| 3395 | `0s0-1s1_5__2s1-3s0-4s1-6s1-7s1-8s1` | H6(1,1)/one | timeout300 | certified | 400.2 | 45.0 |
| 3439 | `0s0-2s1_4__1s1-3s0-5s1-6s0-7s1-8s1` | H6(2,1)/one | timeout300 | certified | 565.8 | 55.2 |
| 3483 | `0s0-2s1_5__1s1-3s0-4s0-6s1-7s0-8s0` | H6(2,1)/one | timeout300 | certified | 378.9 | 46.6 |
| 3527 | `0s0-2s1_6__1s0-3s1-4s0-5s0-7s1-8s0` | H6(2,1)/one | timeout300 | certified | 412.1 | 59.2 |
| 3571 | `0s0-2s1_6__1s1-3s1-4s1-5s1-7s1-8s0` | H6(2,1)/one | timeout300 | certified | 437.9 | 65.5 |
| 3615 | `0s0-3s1_5__1s0-2s0-4s0-6s0-7s1-8s0` | H6(3,1)/one | presplit | certified | 303.9 | 45.8 |
| 3659 | `0s0-3s1_5__1s1-2s0-4s1-6s1-7s1-8s0` | H6(3,1)/one | presplit | certified | 496.2 | 57.8 |
| 3703 | `0s0-4s0_6__1s0-2s1-3s1-5s0-7s1-8s0` | H6(4,0)/one | presplit | certified | 74.2 | 34.3 |
| 3747 | `0s0-5s0_6__1s0-2s0-3s0-4s0-7s0-8s1` | H6(5,0)/one | presplit | certified | 57.9 | 29.6 |
| 3791 | `0s0-5s0_6__1s1-2s0-3s1-4s1-7s0-8s1` | H6(5,0)/one | presplit | certified | 91.8 | 36.4 |
| 3835 | `0s0-5s0_7__1s0-2s1-3s1-4s0-6s0-8s1` | H6(5,0)/one | presplit | certified | 80.9 | 41.3 |
| 3879 | `0s0-5s1_1__2s0-3s1-4s0-6s0-7s1-8s1` | H6(5,1)/one | presplit | certified | 255.8 | 55.2 |
| 3923 | `0s0-5s1_1__2s1-3s1-4s1-6s1-7s1-8s1` | H6(5,1)/one | presplit | certified | 146.3 | 34.8 |
| 3967 | `0s0-5s1_2__1s1-3s0-4s1-6s0-7s1-8s1` | H6(5,1)/one | presplit | certified | 272.2 | 43.7 |
| 4011 | `0s0-5s1_6__1s1-2s1-3s1-4s0-7s0-8s0` | H6(5,1)/one | never_ran | certified | 405.9 | 45.3 |
| 4055 | `0s0-5s1_1s1-10s1__2s1-3s0-4s1-6s0-7s1-8s0` | H6(5,1)/two | never_ran | certified | 49.8 | 27.4 |
| 4099 | `0s0-5s1_2s1-3s0__1s1-4s1-6s1-7s1-8s1-9s0` | H6(5,1)/two | never_ran | certified | 31.0 | 26.4 |

## Files

`env.txt`, `tools.txt`, `units.tsv`, `lane0.sh`–`lane2.sh`, `out.jsonl` (94 records: lane 0, then 1, then 2), `driver0.log.tail`–`driver2.log.tail`.
