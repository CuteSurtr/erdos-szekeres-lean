# C3W6 P29: shard 29 of 44 of W6.tsv, cap 900, one pass

Task: `results/C3W6/TASK.md` at c5260b44. One VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 05:31:52 UTC, END 09:46:52 UTC; at END the three lanes were killed (whole process groups, plus any remaining close_tree/cadical/checker processes).

## Tools and base check

- C3U2 tools: worktree of cad4e050 at /opt/c3u2, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 c60730422e75; cake_lpr a36874a8 (example: `s VERIFIED UNSAT`); lrat-check 2e3b2dc + E2 patch. Sanity check passed: LRAT `3 0 0` on {1},{-1} rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).
- Details in `tools.txt`.

## Units

93 rows of W6.tsv with row ≡ 29 (mod 44) (`units.tsv`), no seeding. 3 lanes (`lane0.sh`–`lane2.sh`), lane k = positions ≡ k (mod 3). Each unit: `close_tree.py ... U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`.

| | units |
|---|---|
| certified (both checkers) | 53 |
| timed out at 900 (layer split record written, 51 children unsolved) | 18 |
| killed at END while running (no record) | 3 |
| not reached | 19 |

`out.jsonl`: 89 records (lane 0, 1, 2): 53 certified solves, 18 UNKNOWN solves at cap 900, 18 split records with 51 children each. Every certified record has `lrat_check: c VERIFIED` and `cake_lpr: s VERIFIED UNSAT`.

Totals per stratum:

| stratum | certified | timed out | killed at END | not reached |
|---|---|---|---|---|
| H3/two | 53 | 18 | 3 | 2 |
| H6(1,1)/one | 0 | 0 | 0 | 1 |
| H6(2,1)/one | 0 | 0 | 0 | 4 |
| H6(3,1)/one | 0 | 0 | 0 | 2 |
| H6(4,0)/one | 0 | 0 | 0 | 2 |
| H6(5,0)/one | 0 | 0 | 0 | 3 |
| H6(5,1)/one | 0 | 0 | 0 | 3 |
| H6(5,1)/two | 0 | 0 | 0 | 2 |

Totals per prior:

| prior | certified | timed out | killed at END | not reached |
|---|---|---|---|---|
| presplit | 38 | 8 | 1 | 10 |
| timeout300 | 11 | 9 | 1 | 5 |
| never_ran | 4 | 1 | 1 | 4 |

Solve time of the 53 certified units: min 48.4 s, quartiles 188.8 / 489.0 / 686.2 s, p90 799.4 s, max 896.8 s; 33 of 53 certified above 300 s.

No SAT, no proof rejection, no memory problem (peak about 5 GB used of 15), no unit ended early without a certificate (the only solve under 72 s, row 3197 at 48.4 s, is certified). No node with cake_lpr `none`, so nothing to re-check; no `recheck.jsonl`.

Killed at END (open, no record): rows 2977 `0s0_4s1-5s0__1s1-2s1-3s0-6s1-7s1-8s1`, 3285 `0s0_5s0-6s1__1s1-2s0-3s0-4s0-7s1-8s0`, 3329 `0s0_5s1-6s0__1s1-2s1-3s0-4s0-7s1-8s0`.

## Per unit

(solve s / check s for certified units)

| row | node | stratum | prior | result |
|---|---|---|---|---|
| 29 | `0s0_1s0-2s0__3s0-4s1-5s0-6s0-7s0-8s0` | H3/two | presplit | certified 91.8/69.1 |
| 73 | `0s0_1s0-2s0__3s1-4s1-5s1-6s1-7s0-8s0` | H3/two | presplit | certified 116.4/74.3 |
| 117 | `0s0_1s0-2s1__3s1-4s0-5s1-6s1-7s1-8s1` | H3/two | timeout300 | certified 825.7/117.4 |
| 161 | `0s0_1s0-4s1__2s0-3s0-5s0-6s0-7s1-8s1` | H3/two | timeout300 | certified 654.0/103.9 |
| 205 | `0s0_1s0-4s1__2s1-3s1-5s0-6s1-7s0-8s1` | H3/two | timeout300 | timed out at 900 |
| 249 | `0s0_1s0-5s1__2s1-3s1-4s1-6s1-7s1-8s1` | H3/two | timeout300 | certified 712.8/87.1 |
| 293 | `0s0_1s0-7s0__2s1-3s1-4s0-5s1-6s0-8s1` | H3/two | timeout300 | certified 427.7/76.3 |
| 337 | `0s0_1s1-2s0__3s1-4s0-5s0-6s0-7s1-8s0` | H3/two | timeout300 | certified 748.5/94.4 |
| 381 | `0s0_1s1-4s0__2s1-3s1-5s0-6s0-7s1-8s1` | H3/two | timeout300 | timed out at 900 |
| 425 | `0s0_1s1-5s0__2s1-3s1-4s0-6s1-7s0-8s1` | H3/two | timeout300 | certified 711.8/81.0 |
| 469 | `0s0_1s1-5s1__2s1-3s0-4s0-6s0-7s1-8s0` | H3/two | presplit | certified 235.0/83.1 |
| 513 | `0s0_1s1-7s1__2s0-3s1-4s1-5s1-6s0-8s0` | H3/two | timeout300 | certified 681.5/90.5 |
| 557 | `0s0_1s1-8s0__2s0-3s0-4s1-5s0-6s1-7s0` | H3/two | presplit | certified 171.8/63.6 |
| 601 | `0s0_1s1-8s0__2s1-3s1-4s0-5s1-6s1-7s0` | H3/two | presplit | certified 193.8/55.6 |
| 645 | `0s0_1s1-8s1__2s1-3s1-4s1-5s1-6s1-7s0` | H3/two | timeout300 | timed out at 900 |
| 689 | `0s0_1s1-9s1__2s1-3s1-4s0-5s1-6s1-7s1` | H3/two | never_ran | timed out at 900 |
| 733 | `0s0_2s0-3s1__1s1-4s0-5s0-6s0-7s1-8s1` | H3/two | presplit | certified 808.6/86.1 |
| 777 | `0s0_2s0-4s1__1s0-3s0-5s1-6s1-7s1-8s1` | H3/two | presplit | certified 799.4/76.4 |
| 821 | `0s0_2s0-4s1__1s1-3s1-5s1-6s0-7s1-8s1` | H3/two | presplit | timed out at 900 |
| 865 | `0s0_2s0-5s0__1s1-3s0-4s0-6s1-7s1-8s1` | H3/two | presplit | certified 351.0/63.6 |
| 909 | `0s0_2s0-5s1__1s0-3s1-4s1-6s0-7s1-8s0` | H3/two | timeout300 | timed out at 900 |
| 953 | `0s0_2s0-6s1__1s0-3s0-4s0-5s1-7s1-8s1` | H3/two | timeout300 | certified 642.0/81.7 |
| 997 | `0s0_2s0-6s1__1s1-3s1-4s0-5s1-7s0-8s0` | H3/two | timeout300 | certified 647.3/73.4 |
| 1041 | `0s0_2s0-7s0__1s1-3s0-4s0-5s0-6s0-8s0` | H3/two | presplit | certified 302.8/61.9 |
| 1085 | `0s0_2s0-7s1__1s0-3s0-4s1-5s1-6s0-8s0` | H3/two | presplit | certified 532.8/67.7 |
| 1129 | `0s0_2s0-7s1__1s1-3s1-4s1-5s0-6s0-8s0` | H3/two | presplit | certified 690.8/70.7 |
| 1173 | `0s0_2s0-8s0__1s1-3s1-4s0-5s1-6s1-7s0` | H3/two | presplit | certified 388.3/70.4 |
| 1217 | `0s0_2s1-3s0__1s1-4s0-5s0-6s0-7s1-8s1` | H3/two | timeout300 | timed out at 900 |
| 1261 | `0s0_2s1-3s1__1s0-4s0-5s1-6s1-7s1-8s1` | H3/two | presplit | certified 183.8/49.3 |
| 1305 | `0s0_2s1-3s1__1s1-4s1-5s1-6s0-7s1-8s1` | H3/two | presplit | certified 129.9/49.9 |
| 1349 | `0s0_2s1-4s0__1s1-3s0-5s1-6s1-7s0-8s1` | H3/two | timeout300 | timed out at 900 |
| 1393 | `0s0_2s1-5s0__1s0-3s1-4s1-6s0-7s0-8s1` | H3/two | presplit | certified 759.1/84.4 |
| 1437 | `0s0_2s1-6s0__1s0-3s0-4s0-5s1-7s0-8s1` | H3/two | presplit | certified 572.9/79.0 |
| 1481 | `0s0_2s1-6s0__1s1-3s1-4s0-5s0-7s0-8s1` | H3/two | presplit | certified 647.9/67.2 |
| 1525 | `0s0_2s1-6s1__1s0-3s1-4s1-5s1-7s0-8s1` | H3/two | presplit | certified 676.6/92.7 |
| 1569 | `0s0_2s1-7s0__1s0-3s1-4s0-5s0-6s0-8s1` | H3/two | timeout300 | certified 214.7/56.1 |
| 1613 | `0s0_2s1-7s0__1s1-3s1-4s1-5s1-6s0-8s1` | H3/two | never_ran | certified 513.9/67.3 |
| 1657 | `0s0_2s1-8s1__1s0-3s0-4s1-5s1-6s0-7s0` | H3/two | presplit | certified 579.4/70.5 |
| 1701 | `0s0_2s1-8s1__1s1-3s1-4s1-5s0-6s0-7s0` | H3/two | presplit | certified 656.6/68.9 |
| 1745 | `0s0_2s1-9s0__1s1-3s0-4s0-5s1-6s0-7s0` | H3/two | presplit | certified 200.4/59.1 |
| 1789 | `0s0_3s0-4s1__1s0-2s1-5s0-6s0-7s0-8s0` | H3/two | presplit | certified 726.9/82.7 |
| 1833 | `0s0_3s0-4s1__1s1-2s1-5s1-6s1-7s0-8s0` | H3/two | presplit | timed out at 900 |
| 1877 | `0s0_3s0-5s0__1s1-2s0-4s1-6s0-7s0-8s0` | H3/two | presplit | certified 89.7/33.8 |
| 1921 | `0s0_3s0-5s1__1s0-2s1-4s1-6s1-7s1-8s0` | H3/two | timeout300 | timed out at 900 |
| 1965 | `0s0_3s0-6s0__1s0-2s0-4s1-5s0-7s1-8s0` | H3/two | presplit | certified 90.9/40.8 |
| 2009 | `0s0_3s0-6s0__1s1-2s1-4s0-5s1-7s1-8s0` | H3/two | presplit | certified 254.7/53.6 |
| 2053 | `0s0_3s0-6s1__1s1-2s0-4s0-5s0-7s1-8s0` | H3/two | timeout300 | certified 822.7/74.6 |
| 2097 | `0s0_3s0-7s0__1s0-2s0-4s1-5s1-6s1-8s0` | H3/two | presplit | certified 125.4/50.6 |
| 2141 | `0s0_3s0-7s0__1s1-2s1-4s1-5s0-6s1-8s0` | H3/two | presplit | certified 285.9/56.2 |
| 2185 | `0s0_3s0-7s1__1s1-2s0-4s0-5s1-6s1-8s0` | H3/two | presplit | certified 677.0/73.3 |
| 2229 | `0s0_3s0-8s0__1s1-2s0-4s1-5s0-6s0-7s0` | H3/two | presplit | certified 304.8/57.4 |
| 2273 | `0s0_3s0-8s1__1s1-2s1-4s0-5s1-6s1-7s1` | H3/two | never_ran | certified 644.1/89.0 |
| 2317 | `0s0_3s1-4s0__1s1-2s0-5s0-6s1-7s0-8s1` | H3/two | timeout300 | timed out at 900 |
| 2361 | `0s0_3s1-4s1__1s0-2s1-5s0-6s0-7s0-8s1` | H3/two | presplit | certified 165.8/45.6 |
| 2405 | `0s0_3s1-4s1__1s1-2s1-5s1-6s1-7s0-8s1` | H3/two | presplit | certified 119.9/39.7 |
| 2449 | `0s0_3s1-5s0__1s1-2s0-4s1-6s0-7s0-8s1` | H3/two | presplit | timed out at 900 |
| 2493 | `0s0_3s1-5s1__1s0-2s1-4s0-6s1-7s0-8s1` | H3/two | presplit | certified 163.3/47.7 |
| 2537 | `0s0_3s1-6s0__1s1-2s1-4s0-5s1-7s0-8s1` | H3/two | timeout300 | timed out at 900 |
| 2581 | `0s0_3s1-7s0__1s1-2s1-4s1-5s0-6s1-8s1` | H3/two | never_ran | certified 896.8/78.6 |
| 2625 | `0s0_3s1-8s0__1s0-2s0-4s1-5s1-6s1-7s0` | H3/two | presplit | certified 356.5/87.3 |
| 2669 | `0s0_3s1-8s0__1s1-2s1-4s1-5s0-6s1-7s0` | H3/two | presplit | certified 489.0/94.9 |
| 2713 | `0s0_4s0-5s1__1s1-2s0-3s0-6s1-7s1-8s0` | H3/two | presplit | timed out at 900 |
| 2757 | `0s0_4s0-6s1__1s0-2s1-3s0-5s0-7s1-8s0` | H3/two | presplit | certified 776.6/80.4 |
| 2801 | `0s0_4s0-6s1__1s1-2s1-3s1-5s1-7s1-8s0` | H3/two | presplit | timed out at 900 |
| 2845 | `0s0_4s0-7s0__1s1-2s0-3s1-5s0-6s1-8s0` | H3/two | presplit | certified 166.6/54.5 |
| 2889 | `0s0_4s0-7s1__1s0-2s1-3s1-5s1-6s1-8s1` | H3/two | presplit | timed out at 900 |
| 2933 | `0s0_4s1-5s0__1s0-2s0-3s1-6s0-7s1-8s1` | H3/two | never_ran | certified 888.0/98.8 |
| 2977 | `0s0_4s1-5s0__1s1-2s1-3s0-6s1-7s1-8s1` | H3/two | never_ran | killed at END |
| 3021 | `0s0_4s1-6s0__1s0-2s1-3s1-5s0-7s1-8s0` | H3/two | presplit | timed out at 900 |
| 3065 | `0s0_4s1-6s1__1s0-2s0-3s0-5s1-7s1-8s0` | H3/two | presplit | certified 241.3/56.6 |
| 3109 | `0s0_4s1-6s1__1s1-2s1-3s0-5s0-7s1-8s0` | H3/two | presplit | not reached |
| 3153 | `0s0_4s1-7s0__1s0-2s1-3s1-5s1-6s1-8s0` | H3/two | presplit | timed out at 900 |
| 3197 | `0s0_5s0-6s0__1s0-2s0-3s1-4s0-7s1-8s0` | H3/two | presplit | certified 48.4/29.5 |
| 3241 | `0s0_5s0-6s0__1s1-2s1-3s0-4s1-7s1-8s0` | H3/two | presplit | not reached |
| 3285 | `0s0_5s0-6s1__1s1-2s0-3s0-4s0-7s1-8s0` | H3/two | presplit | killed at END |
| 3329 | `0s0_5s1-6s0__1s1-2s1-3s0-4s0-7s1-8s0` | H3/two | timeout300 | killed at END |
| 3373 | `0s0-1s1_5__2s0-3s1-4s1-6s0-7s0-8s1` | H6(1,1)/one | timeout300 | not reached |
| 3417 | `0s0-2s1_3__1s1-4s0-5s1-6s1-7s1-8s0` | H6(2,1)/one | timeout300 | not reached |
| 3461 | `0s0-2s1_5__1s0-3s0-4s0-6s1-7s0-8s1` | H6(2,1)/one | timeout300 | not reached |
| 3505 | `0s0-2s1_5__1s1-3s1-4s1-6s0-7s1-8s0` | H6(2,1)/one | timeout300 | not reached |
| 3549 | `0s0-2s1_6__1s1-3s0-4s1-5s0-7s0-8s0` | H6(2,1)/one | timeout300 | not reached |
| 3593 | `0s0-3s1_4__1s1-2s0-5s1-6s1-7s0-8s0` | H6(3,1)/one | never_ran | not reached |
| 3637 | `0s0-3s1_5__1s0-2s1-4s1-6s0-7s0-8s0` | H6(3,1)/one | presplit | not reached |
| 3681 | `0s0-4s0_6__1s0-2s0-3s0-5s1-7s0-8s0` | H6(4,0)/one | presplit | not reached |
| 3725 | `0s0-4s0_6__1s1-2s1-3s0-5s0-7s0-8s0` | H6(4,0)/one | presplit | not reached |
| 3769 | `0s0-5s0_6__1s0-2s1-3s0-4s1-7s1-8s1` | H6(5,0)/one | presplit | not reached |
| 3813 | `0s0-5s0_7__1s0-2s0-3s0-4s0-6s1-8s1` | H6(5,0)/one | presplit | not reached |
| 3857 | `0s0-5s0_7__1s1-2s0-3s1-4s1-6s1-8s1` | H6(5,0)/one | presplit | not reached |
| 3901 | `0s0-5s1_1__2s1-3s0-4s1-6s0-7s0-8s1` | H6(5,1)/one | presplit | not reached |
| 3945 | `0s0-5s1_2__1s0-3s1-4s0-6s1-7s0-8s1` | H6(5,1)/one | presplit | not reached |
| 3989 | `0s0-5s1_6__1s1-2s0-3s0-4s0-7s1-8s0` | H6(5,1)/one | never_ran | not reached |
| 4033 | `0s0-5s1_1s1-10s1__2s0-3s1-4s0-6s1-7s0-8s0` | H6(5,1)/two | never_ran | not reached |
| 4077 | `0s0-5s1_2s1-3s0__1s1-4s0-6s0-7s0-8s0-9s0` | H6(5,1)/two | never_ran | not reached |
