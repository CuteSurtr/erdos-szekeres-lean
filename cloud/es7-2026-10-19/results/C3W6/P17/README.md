# C3W6 / P17: shard 17 of 44 of W6.tsv, cap 900, one machine

**Result: all 93 units certified at the first attempt (cap 900). Both checkers accepted every one (lrat-check `c VERIFIED`, cake_lpr `s VERIFIED UNSAT`). No timeouts, no split records, no SAT, no proof rejection, no memory problem, and no unit ended early without a certificate.**

## Setup

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 05:31:53 UTC on 2026-10-25, END 09:46:53 UTC (start + 4.5 h − 15 min). The lanes ran 05:34:54–07:41:39 UTC and all three finished before END.

- Task `results/C3W6/TASK.md` at c5260b44. Tools: worktree of cad4e050 at `/opt/c3u2`, `results/C3U2/tools`, unmodified (`tools.txt`)
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (example: `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 + E2 patch. Sanity test: LRAT `3 0 0` on {1},{-1} is rejected by both checkers, and `3 0 1 2 0` is accepted by both
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches)
- Units: the rows of `lists/W6.tsv` with row ≡ 17 (mod 44): 93 units (`units.tsv`), no seeding. 3 lanes (`lane0.sh`–`lane2.sh`) with 31 units each, run as `close_tree.py ... U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`
- `compose.py` was not run. `out.jsonl` = lane 0, then 1, then 2 (93 records, all certified). There is no `recheck.jsonl` because no re-check was needed

## Totals

| stratum | prior | units | certified | timed out at 900 | not reached | solve s (sum) | max solve s |
|---|---|---|---|---|---|---|---|
| H3/two | never_ran | 5 | 5 | 0 | 0 | 1559 | 466.1 |
| H3/two | presplit | 49 | 49 | 0 | 0 | 8255 | 379.5 |
| H3/two | timeout300 | 22 | 22 | 0 | 0 | 6099 | 364.7 |
| H6(1,1)/one | timeout300 | 2 | 2 | 0 | 0 | 382 | 191.0 |
| H6(2,1)/one | timeout300 | 3 | 3 | 0 | 0 | 594 | 226.8 |
| H6(3,1)/one | presplit | 2 | 2 | 0 | 0 | 382 | 220.5 |
| H6(3,1)/one | timeout300 | 1 | 1 | 0 | 0 | 213 | 213.0 |
| H6(4,0)/one | presplit | 1 | 1 | 0 | 0 | 48 | 48.4 |
| H6(5,0)/one | presplit | 3 | 3 | 0 | 0 | 117 | 42.8 |
| H6(5,1)/one | presplit | 3 | 3 | 0 | 0 | 374 | 145.6 |
| H6(5,1)/two | never_ran | 2 | 2 | 0 | 0 | 42 | 31.7 |
| **total** | | **93** | **93** | **0** | **0** | **18065** | **466.1** |

By stratum: H3/two 76/76, one-orbit H6 15/15, two-orbit H6 2/2. By prior: presplit 58/58, timeout300 28/28, never_ran 7/7.

Solve times of the certified units: min 10.8 s, Q1 66.6, median 210.6, Q3 288.4, p90 334.1, max 466.1. 20 units were certified above 300 s. Check time: 3997 s in total, at most 63.6 s per unit. The largest proof was 658 MB (deleted after checking). Times are per node, with 3 lanes sharing 4 cores.

Some units certified in under 72 s; the early-end check concerns only uncertified results, so these are not anomalies.

## Per unit

| row | node | stratum | prior | lane | result | solve s | check s |
|---|---|---|---|---|---|---|---|
| 17 | `0s0_1s0-2s0__3s0-4s0-5s0-6s1-7s0-8s0` | H3/two | presplit | 0 | certified | 39.2 | 44.2 |
| 61 | `0s0_1s0-2s0__3s1-4s1-5s0-6s0-7s0-8s0` | H3/two | presplit | 1 | certified | 40.9 | 46.8 |
| 105 | `0s0_1s0-2s1__3s1-4s0-5s0-6s0-7s1-8s1` | H3/two | timeout300 | 2 | certified | 259.5 | 57.5 |
| 149 | `0s0_1s0-3s1__2s1-4s0-5s1-6s1-7s0-8s1` | H3/two | timeout300 | 0 | certified | 364.7 | 55.6 |
| 193 | `0s0_1s0-4s1__2s1-3s0-5s1-6s0-7s0-8s1` | H3/two | timeout300 | 1 | certified | 305.9 | 63.6 |
| 237 | `0s0_1s0-5s1__2s1-3s1-4s0-6s0-7s1-8s1` | H3/two | timeout300 | 2 | certified | 316.8 | 56.6 |
| 281 | `0s0_1s0-7s0__2s1-3s0-4s1-5s0-6s0-8s1` | H3/two | timeout300 | 0 | certified | 151.4 | 52.8 |
| 325 | `0s0_1s1-2s0__3s0-4s1-5s0-6s1-7s1-8s0` | H3/two | timeout300 | 1 | certified | 292.6 | 55.7 |
| 369 | `0s0_1s1-4s0__2s0-3s1-5s1-6s0-7s1-8s0` | H3/two | timeout300 | 2 | certified | 264.7 | 51.4 |
| 413 | `0s0_1s1-5s0__2s1-3s0-4s1-6s0-7s0-8s1` | H3/two | timeout300 | 0 | certified | 270.7 | 59.9 |
| 457 | `0s0_1s1-5s1__2s0-3s1-4s0-6s1-7s1-8s0` | H3/two | presplit | 1 | certified | 94.0 | 42.8 |
| 501 | `0s0_1s1-7s1__2s0-3s0-4s0-5s1-6s1-8s1` | H3/two | timeout300 | 2 | certified | 184.7 | 43.9 |
| 545 | `0s0_1s1-7s1__2s1-3s1-4s1-5s1-6s1-8s0` | H3/two | timeout300 | 0 | certified | 337.7 | 54.4 |
| 589 | `0s0_1s1-8s0__2s1-3s0-4s1-5s0-6s1-7s0` | H3/two | presplit | 1 | certified | 62.1 | 35.6 |
| 633 | `0s0_1s1-8s1__2s1-3s1-4s0-5s0-6s1-7s0` | H3/two | timeout300 | 2 | certified | 237.3 | 45.9 |
| 677 | `0s0_1s1-9s1__2s1-3s0-4s1-5s0-6s1-7s1` | H3/two | never_ran | 0 | certified | 386.5 | 56.2 |
| 721 | `0s0_2s0-3s1__1s0-4s1-5s0-6s1-7s1-8s1` | H3/two | presplit | 1 | certified | 257.9 | 51.5 |
| 765 | `0s0_2s0-4s1__1s0-3s0-5s0-6s0-7s1-8s1` | H3/two | presplit | 2 | certified | 220.1 | 51.3 |
| 809 | `0s0_2s0-4s1__1s1-3s0-5s1-6s1-7s1-8s1` | H3/two | presplit | 0 | certified | 324.7 | 62.2 |
| 853 | `0s0_2s0-5s0__1s0-3s1-4s1-6s0-7s1-8s1` | H3/two | presplit | 1 | certified | 41.4 | 44.3 |
| 897 | `0s0_2s0-5s1__1s0-3s0-4s1-6s1-7s1-8s0` | H3/two | timeout300 | 2 | certified | 267.4 | 52.4 |
| 941 | `0s0_2s0-5s1__1s1-3s1-4s1-6s0-7s1-8s0` | H3/two | timeout300 | 0 | certified | 303.8 | 44.4 |
| 985 | `0s0_2s0-6s1__1s1-3s0-4s1-5s0-7s0-8s0` | H3/two | timeout300 | 1 | certified | 186.4 | 44.0 |
| 1029 | `0s0_2s0-7s0__1s0-3s1-4s0-5s1-6s0-8s0` | H3/two | presplit | 2 | certified | 80.6 | 36.7 |
| 1073 | `0s0_2s0-7s1__1s0-3s0-4s0-5s0-6s0-8s0` | H3/two | presplit | 0 | certified | 107.3 | 32.1 |
| 1117 | `0s0_2s0-7s1__1s1-3s0-4s1-5s1-6s0-8s0` | H3/two | presplit | 1 | certified | 183.4 | 46.6 |
| 1161 | `0s0_2s0-8s0__1s1-3s0-4s1-5s0-6s1-7s0` | H3/two | presplit | 2 | certified | 157.3 | 51.1 |
| 1205 | `0s0_2s1-3s0__1s0-4s1-5s0-6s1-7s1-8s1` | H3/two | timeout300 | 0 | certified | 331.9 | 50.5 |
| 1249 | `0s0_2s1-3s1__1s0-4s0-5s0-6s0-7s1-8s1` | H3/two | presplit | 1 | certified | 61.6 | 35.4 |
| 1293 | `0s0_2s1-3s1__1s1-4s0-5s1-6s1-7s1-8s1` | H3/two | presplit | 2 | certified | 45.3 | 29.3 |
| 1337 | `0s0_2s1-4s0__1s1-3s0-5s0-6s0-7s0-8s1` | H3/two | timeout300 | 0 | certified | 234.5 | 42.5 |
| 1381 | `0s0_2s1-5s0__1s0-3s0-4s1-6s1-7s0-8s1` | H3/two | presplit | 1 | certified | 248.8 | 47.6 |
| 1425 | `0s0_2s1-5s0__1s1-3s1-4s1-6s0-7s0-8s1` | H3/two | presplit | 2 | certified | 263.3 | 41.3 |
| 1469 | `0s0_2s1-6s0__1s1-3s0-4s0-5s1-7s0-8s1` | H3/two | presplit | 0 | certified | 293.9 | 46.3 |
| 1513 | `0s0_2s1-6s1__1s0-3s1-4s0-5s0-7s0-8s1` | H3/two | presplit | 1 | certified | 93.7 | 43.7 |
| 1557 | `0s0_2s1-6s1__1s1-3s1-4s1-5s1-7s0-8s1` | H3/two | presplit | 2 | certified | 210.6 | 40.5 |
| 1601 | `0s0_2s1-7s0__1s1-3s1-4s0-5s0-6s0-8s1` | H3/two | never_ran | 0 | certified | 152.5 | 34.0 |
| 1645 | `0s0_2s1-7s1__1s1-3s1-4s0-5s1-6s1-8s1` | H3/two | never_ran | 1 | certified | 225.2 | 40.7 |
| 1689 | `0s0_2s1-8s1__1s1-3s0-4s1-5s1-6s0-7s0` | H3/two | presplit | 2 | certified | 247.1 | 42.0 |
| 1733 | `0s0_2s1-9s0__1s0-3s1-4s1-5s0-6s0-7s0` | H3/two | presplit | 0 | certified | 45.8 | 30.7 |
| 1777 | `0s0_3s0-4s1__1s0-2s0-5s0-6s1-7s0-8s0` | H3/two | presplit | 1 | certified | 188.8 | 39.1 |
| 1821 | `0s0_3s0-4s1__1s1-2s1-5s0-6s0-7s0-8s0` | H3/two | presplit | 2 | certified | 269.4 | 41.2 |
| 1865 | `0s0_3s0-5s0__1s0-2s1-4s1-6s1-7s0-8s0` | H3/two | presplit | 0 | certified | 41.6 | 27.0 |
| 1909 | `0s0_3s0-5s1__1s0-2s1-4s0-6s0-7s1-8s0` | H3/two | timeout300 | 1 | certified | 258.1 | 46.1 |
| 1953 | `0s0_3s0-5s1__1s1-2s1-4s1-6s1-7s1-8s0` | H3/two | timeout300 | 2 | certified | 316.7 | 58.4 |
| 1997 | `0s0_3s0-6s0__1s1-2s0-4s1-5s0-7s1-8s0` | H3/two | presplit | 0 | certified | 47.0 | 28.2 |
| 2041 | `0s0_3s0-6s1__1s0-2s1-4s0-5s1-7s1-8s0` | H3/two | timeout300 | 1 | certified | 308.0 | 46.9 |
| 2085 | `0s0_3s0-7s0__1s0-2s0-4s0-5s0-6s1-8s0` | H3/two | presplit | 2 | certified | 52.1 | 31.2 |
| 2129 | `0s0_3s0-7s0__1s1-2s0-4s1-5s1-6s1-8s0` | H3/two | presplit | 0 | certified | 56.8 | 38.1 |
| 2173 | `0s0_3s0-7s1__1s0-2s1-4s1-5s0-6s1-8s0` | H3/two | presplit | 1 | certified | 266.8 | 42.2 |
| 2217 | `0s0_3s0-8s0__1s0-2s1-4s1-5s1-6s0-7s0` | H3/two | presplit | 2 | certified | 102.7 | 40.6 |
| 2261 | `0s0_3s0-8s1__1s0-2s1-4s1-5s1-6s0-7s0` | H3/two | timeout300 | 0 | certified | 254.7 | 45.7 |
| 2305 | `0s0_3s1-4s0__1s0-2s1-5s1-6s0-7s0-8s1` | H3/two | timeout300 | 1 | certified | 316.2 | 49.6 |
| 2349 | `0s0_3s1-4s1__1s0-2s0-5s0-6s1-7s0-8s1` | H3/two | presplit | 2 | certified | 53.1 | 29.5 |
| 2393 | `0s0_3s1-4s1__1s1-2s1-5s0-6s0-7s0-8s1` | H3/two | presplit | 0 | certified | 60.2 | 29.2 |
| 2437 | `0s0_3s1-5s0__1s0-2s1-4s1-6s1-7s0-8s1` | H3/two | presplit | 1 | certified | 379.5 | 49.7 |
| 2481 | `0s0_3s1-5s1__1s0-2s0-4s1-6s0-7s0-8s1` | H3/two | presplit | 2 | certified | 68.4 | 31.4 |
| 2525 | `0s0_3s1-5s1__1s1-2s1-4s0-6s1-7s0-8s1` | H3/two | presplit | 0 | certified | 55.2 | 26.5 |
| 2569 | `0s0_3s1-7s0__1s1-2s0-4s1-5s1-6s1-8s1` | H3/two | never_ran | 1 | certified | 328.7 | 44.6 |
| 2613 | `0s0_3s1-8s0__1s0-2s0-4s0-5s0-6s1-7s0` | H3/two | presplit | 2 | certified | 92.9 | 30.4 |
| 2657 | `0s0_3s1-8s0__1s1-2s0-4s1-5s1-6s1-7s0` | H3/two | presplit | 0 | certified | 161.7 | 37.4 |
| 2701 | `0s0_4s0-5s1__1s0-2s1-3s1-6s0-7s1-8s0` | H3/two | presplit | 1 | certified | 376.6 | 52.7 |
| 2745 | `0s0_4s0-6s1__1s0-2s0-3s0-5s1-7s1-8s0` | H3/two | presplit | 2 | certified | 274.5 | 42.7 |
| 2789 | `0s0_4s0-6s1__1s1-2s1-3s0-5s0-7s1-8s0` | H3/two | presplit | 0 | certified | 338.7 | 48.6 |
| 2833 | `0s0_4s0-7s0__1s0-2s1-3s1-5s1-6s1-8s0` | H3/two | presplit | 1 | certified | 64.8 | 32.2 |
| 2877 | `0s0_4s0-7s1__1s0-2s1-3s0-5s0-6s1-8s1` | H3/two | presplit | 2 | certified | 284.2 | 45.8 |
| 2921 | `0s0_4s0-7s1__1s1-2s1-3s1-5s1-6s1-8s1` | H3/two | presplit | 0 | certified | 252.7 | 52.5 |
| 2965 | `0s0_4s1-5s0__1s1-2s0-3s1-6s0-7s1-8s1` | H3/two | never_ran | 1 | certified | 466.1 | 56.2 |
| 3009 | `0s0_4s1-6s0__1s0-2s0-3s1-5s1-7s1-8s0` | H3/two | presplit | 2 | certified | 330.0 | 60.3 |
| 3053 | `0s0_4s1-6s0__1s1-2s1-3s1-5s0-7s1-8s0` | H3/two | presplit | 0 | certified | 369.0 | 50.7 |
| 3097 | `0s0_4s1-6s1__1s1-2s0-3s0-5s1-7s1-8s0` | H3/two | presplit | 1 | certified | 62.1 | 30.8 |
| 3141 | `0s0_4s1-7s0__1s0-2s1-3s0-5s0-6s1-8s0` | H3/two | presplit | 2 | certified | 245.0 | 44.1 |
| 3185 | `0s0_4s1-7s0__1s1-2s1-3s1-5s1-6s1-8s0` | H3/two | presplit | 0 | certified | 324.4 | 45.4 |
| 3229 | `0s0_5s0-6s0__1s1-2s0-3s1-4s0-7s1-8s0` | H3/two | presplit | 1 | certified | 21.8 | 31.9 |
| 3273 | `0s0_5s0-6s1__1s0-2s1-3s0-4s1-7s1-8s0` | H3/two | presplit | 2 | certified | 295.7 | 46.4 |
| 3317 | `0s0_5s1-6s0__1s0-2s1-3s1-4s1-7s1-8s0` | H3/two | timeout300 | 0 | certified | 335.5 | 55.0 |
| 3361 | `0s0-1s1_5__2s0-3s0-4s0-6s1-7s0-8s1` | H6(1,1)/one | timeout300 | 1 | certified | 191.0 | 45.0 |
| 3405 | `0s0-1s1_5__2s1-3s1-4s1-6s0-7s0-8s1` | H6(1,1)/one | timeout300 | 2 | certified | 190.8 | 38.2 |
| 3449 | `0s0-2s1_4__1s1-3s1-5s0-6s1-7s0-8s1` | H6(2,1)/one | timeout300 | 0 | certified | 180.8 | 39.7 |
| 3493 | `0s0-2s1_5__1s1-3s0-4s1-6s1-7s1-8s0` | H6(2,1)/one | timeout300 | 1 | certified | 226.8 | 40.0 |
| 3537 | `0s0-2s1_6__1s0-3s1-4s1-5s1-7s0-8s0` | H6(2,1)/one | timeout300 | 2 | certified | 186.0 | 37.6 |
| 3581 | `0s0-3s1_4__1s0-2s1-5s1-6s0-7s0-8s1` | H6(3,1)/one | timeout300 | 0 | certified | 213.0 | 42.2 |
| 3625 | `0s0-3s1_5__1s0-2s0-4s1-6s1-7s0-8s0` | H6(3,1)/one | presplit | 1 | certified | 161.6 | 41.5 |
| 3669 | `0s0-3s1_5__1s1-2s1-4s1-6s0-7s0-8s0` | H6(3,1)/one | presplit | 2 | certified | 220.5 | 47.0 |
| 3713 | `0s0-4s0_6__1s1-2s0-3s0-5s1-7s0-8s0` | H6(4,0)/one | presplit | 0 | certified | 48.4 | 31.0 |
| 3757 | `0s0-5s0_6__1s0-2s0-3s1-4s0-7s1-8s1` | H6(5,0)/one | presplit | 1 | certified | 35.5 | 32.6 |
| 3801 | `0s0-5s0_6__1s1-2s1-3s0-4s1-7s1-8s1` | H6(5,0)/one | presplit | 2 | certified | 42.8 | 27.7 |
| 3845 | `0s0-5s0_7__1s1-2s0-3s0-4s0-6s1-8s1` | H6(5,0)/one | presplit | 0 | certified | 38.9 | 31.4 |
| 3889 | `0s0-5s1_1__2s0-3s1-4s1-6s1-7s0-8s1` | H6(5,1)/one | presplit | 1 | certified | 116.3 | 33.2 |
| 3933 | `0s0-5s1_2__1s0-3s0-4s1-6s0-7s0-8s1` | H6(5,1)/one | presplit | 2 | certified | 145.6 | 41.8 |
| 3977 | `0s0-5s1_2__1s1-3s1-4s0-6s1-7s0-8s1` | H6(5,1)/one | presplit | 0 | certified | 111.7 | 36.6 |
| 4021 | `0s0-5s1_1s1-10s1__2s0-3s0-4s1-6s0-7s0-8s0` | H6(5,1)/two | never_ran | 1 | certified | 10.8 | 26.4 |
| 4065 | `0s0-5s1_1s1-10s1__2s1-3s1-4s0-6s1-7s0-8s0` | H6(5,1)/two | never_ran | 2 | certified | 31.7 | 32.9 |
