# C3W6 / P00: shard 0 of 44 of `lists/W6.tsv`, cap 900, 3 lanes

**Result: all 94 of my units were certified at cap 900 (both checkers). None timed out, so there are no split records and nothing is left open. No SAT, no proof rejection, no memory problem, and no unit ended early without a certificate.**

## Setup

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 05:31:50 UTC, END 09:46:50 UTC (H = 4.5 h minus 15 min). All lanes had finished by 08:52:20 UTC, so nothing was killed at END. Task: `results/C3W6/TASK.md` at c5260b44.

- Tools: worktree of cad4e050 at `/opt/c3u2`, `C3U2/tools` used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 c60730422e75, cake_lpr a36874a8 (its example prints `s VERIFIED UNSAT`), lrat-check 2e3b2dc0 + E2 patch. Sanity test: `3 0 0` on {1},{-1} is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da`, which matches. Every record has this `base_sha256`.
- Units: rows of `W6.tsv` with row ≡ 0 (mod 44), so 94 units (`units.tsv`). Lane k ran positions ≡ k (mod 3): 32/31/31 units. Each lane ran `close_tree.py … U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`, with no seeding (`lane*.sh`, `tools.txt`).

## Totals per stratum and prior

| stratum | prior | units | certified | timed out at 900 | not reached | median solve s | max solve s |
|---|---|---|---|---|---|---|---|
| H3/two | never_ran | 7 | 7 | 0 | 0 | 459 | 530 |
| H3/two | presplit | 47 | 47 | 0 | 0 | 237 | 638 |
| H3/two | timeout300 | 22 | 22 | 0 | 0 | 413 | 588 |
| H6(1,1)/one | timeout300 | 2 | 2 | 0 | 0 | 368 | 414 |
| H6(2,1)/one | timeout300 | 4 | 4 | 0 | 0 | 308 | 329 |
| H6(3,1)/one | never_ran | 1 | 1 | 0 | 0 | 373 | 373 |
| H6(3,1)/one | presplit | 1 | 1 | 0 | 0 | 411 | 411 |
| H6(4,0)/one | presplit | 2 | 2 | 0 | 0 | 57 | 77 |
| H6(5,0)/one | presplit | 3 | 3 | 0 | 0 | 105 | 142 |
| H6(5,1)/one | never_ran | 1 | 1 | 0 | 0 | 300 | 300 |
| H6(5,1)/one | presplit | 2 | 2 | 0 | 0 | 223 | 312 |
| H6(5,1)/two | never_ran | 2 | 2 | 0 | 0 | 36 | 41 |
| **total** | | **94** | **94** | **0** | **0** | 329 | 638 |

By prior: timeout300 28/28 certified, presplit 55/55, never_ran 11/11.

## Solve times of the certified units (wall seconds, 3 lanes on 4 cores)

min 24.2, Q1 135.3, median 329.2, Q3 425.8, p90 476.0, max 638.1. **54 of 94 units were certified above 300 s**, and one above 600 s. Total solve time is 27,989 s and total check time is 4,355 s (check per unit: min 22.4, median 46.2, max 77.2). The largest proof was 589 MB. Seven solves took under 72 s, and all seven were certified.

## SAT / rejections / incidents

- SAT: none. No `SAT FOUND` and no model files.
- `PROOF NOT ACCEPTED`: none. No records with cake_lpr `none`, so there is no `recheck.jsonl`.
- Memory: free memory never dropped below about 5 GB (spot checks). No OOM.
- Timeouts, split records and unsplittable nodes: none.

## Per unit

| pos | row | node | stratum | prior | result | solve s | check s |
|---|---|---|---|---|---|---|---|
| 0 | 0 | `0s0_1s0-10s0__2s1-3s0-4s1-5s0-6s1-7s1` | H3/two | timeout300 | certified | 254.7 | 61.7 |
| 1 | 44 | `0s0_1s0-2s0__3s0-4s1-5s1-6s1-7s1-8s1` | H3/two | presplit | certified | 24.2 | 35.8 |
| 2 | 88 | `0s0_1s0-2s1__3s0-4s1-5s0-6s0-7s1-8s0` | H3/two | timeout300 | certified | 475.1 | 74.8 |
| 3 | 132 | `0s0_1s0-2s1__3s1-4s1-5s1-6s1-7s1-8s0` | H3/two | timeout300 | certified | 435.1 | 60.6 |
| 4 | 176 | `0s0_1s0-4s1__2s0-3s1-5s0-6s1-7s1-8s1` | H3/two | timeout300 | certified | 455.6 | 69.0 |
| 5 | 220 | `0s0_1s0-5s1__2s0-3s1-4s1-6s1-7s1-8s0` | H3/two | timeout300 | certified | 363.4 | 62.6 |
| 6 | 264 | `0s0_1s0-7s0__2s0-3s0-4s1-5s1-6s1-8s1` | H3/two | timeout300 | certified | 192.6 | 51.7 |
| 7 | 308 | `0s0_1s0-7s1__2s1-3s1-4s1-5s1-6s1-8s0` | H3/two | timeout300 | certified | 304.9 | 55.3 |
| 8 | 352 | `0s0_1s1-2s0__3s1-4s1-5s0-6s0-7s0-8s1` | H3/two | timeout300 | certified | 415.5 | 60.1 |
| 9 | 396 | `0s0_1s1-5s0__2s0-3s0-4s1-6s1-7s0-8s1` | H3/two | timeout300 | certified | 362.8 | 63.1 |
| 10 | 440 | `0s0_1s1-5s1__2s0-3s0-4s0-6s1-7s0-8s1` | H3/two | presplit | certified | 130.7 | 43.3 |
| 11 | 484 | `0s0_1s1-5s1__2s1-3s1-4s0-6s0-7s0-8s1` | H3/two | presplit | certified | 357.6 | 65.0 |
| 12 | 528 | `0s0_1s1-7s1__2s1-3s0-4s1-5s1-6s0-8s1` | H3/two | timeout300 | certified | 440.4 | 57.3 |
| 13 | 572 | `0s0_1s1-8s0__2s0-3s1-4s1-5s0-6s0-7s1` | H3/two | presplit | certified | 131.6 | 47.9 |
| 14 | 616 | `0s0_1s1-8s1__2s0-3s1-4s1-5s0-6s1-7s0` | H3/two | timeout300 | certified | 410.0 | 69.1 |
| 15 | 660 | `0s0_1s1-9s1__2s0-3s1-4s1-5s0-6s1-7s0` | H3/two | never_ran | certified | 492.6 | 59.7 |
| 16 | 704 | `0s0_2s0-3s1__1s0-4s0-5s0-6s1-7s1-8s0` | H3/two | presplit | certified | 387.0 | 62.9 |
| 17 | 748 | `0s0_2s0-3s1__1s1-4s1-5s0-6s0-7s1-8s0` | H3/two | presplit | certified | 465.7 | 55.7 |
| 18 | 792 | `0s0_2s0-4s1__1s0-3s1-5s1-6s1-7s1-8s0` | H3/two | presplit | certified | 521.8 | 58.5 |
| 19 | 836 | `0s0_2s0-5s0__1s0-3s0-4s1-6s0-7s1-8s0` | H3/two | presplit | certified | 51.1 | 43.1 |
| 20 | 880 | `0s0_2s0-5s0__1s1-3s1-4s0-6s1-7s1-8s0` | H3/two | presplit | certified | 98.0 | 39.4 |
| 21 | 924 | `0s0_2s0-5s1__1s1-3s0-4s1-6s0-7s0-8s1` | H3/two | timeout300 | certified | 405.7 | 47.9 |
| 22 | 968 | `0s0_2s0-6s1__1s0-3s1-4s0-5s1-7s1-8s1` | H3/two | timeout300 | certified | 420.7 | 55.4 |
| 23 | 1012 | `0s0_2s0-7s0__1s0-3s0-4s0-5s0-6s1-8s1` | H3/two | presplit | certified | 129.6 | 39.6 |
| 24 | 1056 | `0s0_2s0-7s0__1s1-3s0-4s1-5s1-6s1-8s1` | H3/two | presplit | certified | 165.2 | 40.2 |
| 25 | 1100 | `0s0_2s0-7s1__1s0-3s1-4s1-5s0-6s1-8s1` | H3/two | presplit | certified | 389.5 | 60.1 |
| 26 | 1144 | `0s0_2s0-8s0__1s0-3s1-4s1-5s0-6s0-7s1` | H3/two | presplit | certified | 176.9 | 41.0 |
| 27 | 1188 | `0s0_2s1-3s0__1s0-4s0-5s0-6s1-7s1-8s0` | H3/two | timeout300 | certified | 385.2 | 50.5 |
| 28 | 1232 | `0s0_2s1-3s0__1s1-4s1-5s0-6s0-7s1-8s0` | H3/two | timeout300 | certified | 475.7 | 56.5 |
| 29 | 1276 | `0s0_2s1-3s1__1s0-4s1-5s1-6s1-7s1-8s0` | H3/two | presplit | certified | 87.6 | 35.5 |
| 30 | 1320 | `0s0_2s1-4s0__1s0-3s0-5s1-6s1-7s0-8s1` | H3/two | timeout300 | certified | 430.5 | 49.6 |
| 31 | 1364 | `0s0_2s1-4s0__1s1-3s1-5s1-6s1-7s0-8s0` | H3/two | timeout300 | certified | 468.3 | 50.2 |
| 32 | 1408 | `0s0_2s1-5s0__1s1-3s0-4s1-6s0-7s0-8s0` | H3/two | presplit | certified | 440.2 | 48.6 |
| 33 | 1452 | `0s0_2s1-6s0__1s0-3s1-4s0-5s1-7s0-8s0` | H3/two | presplit | certified | 301.5 | 42.4 |
| 34 | 1496 | `0s0_2s1-6s1__1s0-3s0-4s0-5s0-7s0-8s0` | H3/two | presplit | certified | 152.5 | 49.4 |
| 35 | 1540 | `0s0_2s1-6s1__1s1-3s0-4s1-5s1-7s0-8s0` | H3/two | presplit | certified | 316.3 | 43.8 |
| 36 | 1584 | `0s0_2s1-7s0__1s1-3s0-4s0-5s0-6s0-8s0` | H3/two | never_ran | certified | 209.5 | 36.3 |
| 37 | 1628 | `0s0_2s1-7s1__1s1-3s0-4s0-5s1-6s1-8s0` | H3/two | never_ran | certified | 351.1 | 46.6 |
| 38 | 1672 | `0s0_2s1-8s1__1s0-3s1-4s1-5s0-6s1-7s1` | H3/two | presplit | certified | 552.0 | 52.7 |
| 39 | 1716 | `0s0_2s1-9s0__1s0-3s0-4s0-5s1-6s1-7s1` | H3/two | presplit | certified | 137.9 | 31.3 |
| 40 | 1760 | `0s0_2s1-9s0__1s1-3s1-4s0-5s0-6s1-7s1` | H3/two | presplit | certified | 166.7 | 35.0 |
| 41 | 1804 | `0s0_3s0-4s1__1s0-2s1-5s1-6s1-7s1-8s1` | H3/two | presplit | certified | 395.1 | 47.2 |
| 42 | 1848 | `0s0_3s0-5s0__1s0-2s0-4s1-6s0-7s1-8s1` | H3/two | presplit | certified | 31.6 | 23.0 |
| 43 | 1892 | `0s0_3s0-5s0__1s1-2s1-4s0-6s1-7s1-8s1` | H3/two | presplit | certified | 109.0 | 32.1 |
| 44 | 1936 | `0s0_3s0-5s1__1s1-2s0-4s1-6s1-7s0-8s1` | H3/two | timeout300 | certified | 588.3 | 55.1 |
| 45 | 1980 | `0s0_3s0-6s0__1s0-2s1-4s1-5s0-7s0-8s1` | H3/two | presplit | certified | 77.0 | 28.1 |
| 46 | 2024 | `0s0_3s0-6s1__1s0-2s0-4s0-5s1-7s0-8s1` | H3/two | timeout300 | certified | 345.5 | 46.1 |
| 47 | 2068 | `0s0_3s0-6s1__1s1-2s1-4s0-5s0-7s0-8s1` | H3/two | timeout300 | certified | 466.6 | 47.3 |
| 48 | 2112 | `0s0_3s0-7s0__1s0-2s1-4s1-5s1-6s0-8s1` | H3/two | presplit | certified | 120.0 | 32.0 |
| 49 | 2156 | `0s0_3s0-7s1__1s0-2s0-4s1-5s0-6s0-8s1` | H3/two | presplit | certified | 350.2 | 45.8 |
| 50 | 2200 | `0s0_3s0-7s1__1s1-2s1-4s0-5s1-6s0-8s1` | H3/two | presplit | certified | 469.2 | 47.8 |
| 51 | 2244 | `0s0_3s0-8s0__1s1-2s1-4s0-5s1-6s1-7s1` | H3/two | presplit | certified | 161.5 | 34.5 |
| 52 | 2288 | `0s0_3s1-4s0__1s0-2s0-5s1-6s0-7s0-8s0` | H3/two | timeout300 | certified | 375.2 | 64.6 |
| 53 | 2332 | `0s0_3s1-4s0__1s1-2s1-5s0-6s1-7s0-8s0` | H3/two | never_ran | certified | 502.2 | 48.6 |
| 54 | 2376 | `0s0_3s1-4s1__1s1-2s0-5s0-6s0-7s0-8s0` | H3/two | presplit | certified | 93.6 | 31.6 |
| 55 | 2420 | `0s0_3s1-5s0__1s0-2s0-4s1-6s1-7s0-8s0` | H3/two | presplit | certified | 388.1 | 44.6 |
| 56 | 2464 | `0s0_3s1-5s0__1s1-2s1-4s1-6s0-7s0-8s0` | H3/two | presplit | certified | 446.7 | 46.3 |
| 57 | 2508 | `0s0_3s1-5s1__1s1-2s0-4s0-6s1-7s0-8s0` | H3/two | presplit | certified | 95.7 | 30.8 |
| 58 | 2552 | `0s0_3s1-7s0__1s0-2s1-4s1-5s1-6s1-8s0` | H3/two | never_ran | certified | 458.7 | 49.1 |
| 59 | 2596 | `0s0_3s1-7s1__1s0-2s1-4s1-5s1-6s0-8s1` | H3/two | timeout300 | certified | 289.6 | 38.6 |
| 60 | 2640 | `0s0_3s1-8s0__1s0-2s1-4s1-5s1-6s0-7s1` | H3/two | presplit | certified | 329.7 | 61.8 |
| 61 | 2684 | `0s0_4s0-5s1__1s0-2s0-3s1-6s0-7s0-8s1` | H3/two | presplit | certified | 420.6 | 49.0 |
| 62 | 2728 | `0s0_4s0-5s1__1s1-2s1-3s0-6s1-7s0-8s1` | H3/two | presplit | certified | 638.1 | 62.9 |
| 63 | 2772 | `0s0_4s0-6s1__1s1-2s0-3s0-5s0-7s0-8s1` | H3/two | presplit | certified | 356.4 | 41.2 |
| 64 | 2816 | `0s0_4s0-7s0__1s0-2s0-3s1-5s1-6s0-8s1` | H3/two | presplit | certified | 74.0 | 29.2 |
| 65 | 2860 | `0s0_4s0-7s0__1s1-2s1-3s1-5s0-6s0-8s1` | H3/two | presplit | certified | 237.0 | 40.4 |
| 66 | 2904 | `0s0_4s0-7s1__1s1-2s0-3s1-5s1-6s1-8s0` | H3/two | presplit | certified | 504.8 | 50.7 |
| 67 | 2948 | `0s0_4s1-5s0__1s0-2s1-3s1-6s0-7s1-8s0` | H3/two | never_ran | certified | 529.9 | 77.2 |
| 68 | 2992 | `0s0_4s1-5s1__1s1-2s1-3s1-6s1-7s0-8s1` | H3/two | never_ran | certified | 72.0 | 31.9 |
| 69 | 3036 | `0s0_4s1-6s0__1s1-2s0-3s1-5s0-7s0-8s1` | H3/two | presplit | certified | 476.1 | 49.3 |
| 70 | 3080 | `0s0_4s1-6s1__1s0-2s1-3s0-5s1-7s0-8s1` | H3/two | presplit | certified | 77.4 | 29.7 |
| 71 | 3124 | `0s0_4s1-7s0__1s0-2s0-3s0-5s0-6s0-8s1` | H3/two | presplit | certified | 198.8 | 37.1 |
| 72 | 3168 | `0s0_4s1-7s0__1s1-2s0-3s1-5s1-6s0-8s1` | H3/two | presplit | certified | 393.3 | 44.4 |
| 73 | 3212 | `0s0_5s0-6s0__1s0-2s1-3s1-4s0-7s0-8s1` | H3/two | presplit | certified | 29.5 | 23.9 |
| 74 | 3256 | `0s0_5s0-6s1__1s0-2s0-3s0-4s1-7s0-8s1` | H3/two | presplit | certified | 427.5 | 52.4 |
| 75 | 3300 | `0s0_5s0-6s1__1s1-2s1-3s0-4s0-7s0-8s1` | H3/two | presplit | certified | 548.2 | 68.1 |
| 76 | 3344 | `0s0-1s1_4__2s0-3s1-5s1-6s0-7s1-8s1` | H6(1,1)/one | timeout300 | certified | 414.0 | 47.6 |
| 77 | 3388 | `0s0-1s1_5__2s1-3s0-4s1-6s0-7s0-8s0` | H6(1,1)/one | timeout300 | certified | 321.7 | 46.1 |
| 78 | 3432 | `0s0-2s1_4__1s1-3s0-5s0-6s1-7s0-8s0` | H6(2,1)/one | timeout300 | certified | 328.8 | 44.8 |
| 79 | 3476 | `0s0-2s1_5__1s0-3s1-4s1-6s1-7s0-8s1` | H6(2,1)/one | timeout300 | certified | 317.7 | 40.6 |
| 80 | 3520 | `0s0-2s1_6__1s0-3s0-4s1-5s0-7s1-8s1` | H6(2,1)/one | timeout300 | certified | 262.0 | 43.3 |
| 81 | 3564 | `0s0-2s1_6__1s1-3s1-4s0-5s1-7s1-8s1` | H6(2,1)/one | timeout300 | certified | 297.5 | 45.6 |
| 82 | 3608 | `0s0-3s1_4__1s1-2s1-5s1-6s0-7s1-8s1` | H6(3,1)/one | never_ran | certified | 372.6 | 63.0 |
| 83 | 3652 | `0s0-3s1_5__1s1-2s0-4s0-6s1-7s1-8s1` | H6(3,1)/one | presplit | certified | 410.7 | 49.5 |
| 84 | 3696 | `0s0-4s0_6__1s0-2s1-3s0-5s0-7s1-8s1` | H6(4,0)/one | presplit | certified | 36.3 | 22.4 |
| 85 | 3740 | `0s0-4s0_6__1s1-2s1-3s1-5s1-7s1-8s1` | H6(4,0)/one | presplit | certified | 77.3 | 32.5 |
| 86 | 3784 | `0s0-5s0_6__1s1-2s0-3s0-4s1-7s1-8s0` | H6(5,0)/one | presplit | certified | 75.8 | 29.1 |
| 87 | 3828 | `0s0-5s0_7__1s0-2s1-3s0-4s0-6s1-8s0` | H6(5,0)/one | presplit | certified | 104.7 | 34.3 |
| 88 | 3872 | `0s0-5s0_7__1s1-2s1-3s1-4s1-6s1-8s0` | H6(5,0)/one | presplit | certified | 141.9 | 34.2 |
| 89 | 3916 | `0s0-5s1_1__2s1-3s1-4s1-6s0-7s0-8s0` | H6(5,1)/one | presplit | certified | 134.5 | 36.2 |
| 90 | 3960 | `0s0-5s1_2__1s1-3s0-4s0-6s1-7s0-8s0` | H6(5,1)/one | presplit | certified | 311.7 | 42.2 |
| 91 | 4004 | `0s0-5s1_6__1s1-2s1-3s0-4s0-7s0-8s1` | H6(5,1)/one | never_ran | certified | 299.7 | 42.2 |
| 92 | 4048 | `0s0-5s1_1s1-10s1__2s1-3s0-4s0-6s0-7s1-8s1` | H6(5,1)/two | never_ran | certified | 40.9 | 23.9 |
| 93 | 4092 | `0s0-5s1_2s1-3s0__1s1-4s1-6s0-7s1-8s1-9s1` | H6(5,1)/two | never_ran | certified | 31.1 | 25.9 |

## Files

`env.txt`, `tools.txt`, `units.tsv`, `lane.sh` + `lane0.sh`–`lane2.sh`, `out.jsonl` (94 records: lane 0, then 1, then 2), `driver{0,1,2}.log.tail`.
