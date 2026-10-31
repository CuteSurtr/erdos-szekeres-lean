# C3W6 P30: shard 30 of 44 of W6.tsv, cap 900, 3 lanes

Task: `results/C3W6/TASK.md` at c5260b44, with V = P30, LIST = W6.tsv, j = 30, N = 44, H = 4.5.
Started at 2026-10-25 05:31:20 UTC, with END at 09:46:20 UTC. The lanes began at 05:35:00 and the last unit finished at 08:10:20. The machine has 4 cores, 15 GB RAM and no swap (`env.txt`).

**Result: all 93 units were certified at cap 900.** Both checkers accepted every proof (lrat-check printed `c VERIFIED` and cake_lpr printed `s VERIFIED UNSAT`). There was no SAT, no proof rejection, no timeout, no split record and no unsplittable node. No checker was killed, so there is no `none`. No unit ended early without a certificate, and there was no memory problem: at most 3 solves ran at once, and the largest proof was 565 MB, written to /opt/work and deleted. `recheck.jsonl` was not needed. `compose.py` was not run.

## Tools (`tools.txt`)

- C3U2 tools: worktree of cad4e050 at /opt/c3u2, used unmodified.
- CaDiCaL 3.0.1 at c6073042.
- cake_lpr at a36874a8. Its example prints `s VERIFIED UNSAT`.
- drat-trim lrat-check at 2e3b2dc, with the E2 patch applied.
- Sanity check: on the CNF {1},{-1}, both checkers reject the LRAT `3 0 0` and both accept `3 0 1 2 0`.
- Base CNF: `gen_case.py 11 7 none` gives header `p cnf 168399 4154921` and sha256 `bf0e502e…6da`, which matches.

## Run

- Units: the rows of W6.tsv with row ≡ 30 (mod 44), written to `units.tsv`. There are 93 units, all six-bit σ-cubes. No records were seeded.
- Lanes: lane k ran positions ≡ k (mod 3), using `lane0.sh`–`lane2.sh`. Each lane ran 31 units with `close_tree.py … U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`.
- `out.jsonl` holds lane 0's records, then lane 1's, then lane 2's: 93 solve records, one per unit, each with `"cap": 900`.

## Solve times of the certified units (s)

All 93 units: min 30.9, Q1 98.6, median 259.8, Q3 340.0, p90 408.4, max 499.2.
37 of the 93 were certified above 300 s, the old cap. Total solve time was 6.07 h and total check time 1.13 h; the longest check took 69.6 s.

| stratum | units | certified | median solve | max | > 300 s |
|---|---|---|---|---|---|
| H3/two | 76 | 76 | 281.0 | 499.2 | 36 |
| H6(1,1)/one | 1 | 1 | 325.1 | 325.1 | 1 |
| H6(2,1)/one | 4 | 4 | 244.7 | 271.4 | 0 |
| H6(3,1)/one | 2 | 2 | 219.8 | 235.4 | 0 |
| H6(4,0)/one | 2 | 2 | 39.5 | 39.9 | 0 |
| H6(5,0)/one | 3 | 3 | 56.7 | 70.5 | 0 |
| H6(5,1)/one | 3 | 3 | 181.2 | 237.8 | 0 |
| H6(5,1)/two | 2 | 2 | 37.2 | 40.0 | 0 |

| prior | units | certified | median solve | max | > 300 s |
|---|---|---|---|---|---|
| never_ran | 9 | 9 | 258.2 | 440.2 | 4 |
| presplit | 57 | 57 | 142.9 | 448.1 | 16 |
| timeout300 | 27 | 27 | 328.5 | 499.2 | 17 |

All 27 `timeout300` units closed at cap 900, and 17 of them needed more than 300 s.

## Per unit

| row | lane | node | stratum | prior | result | solve s | check s |
|---|---|---|---|---|---|---|---|
| 30 | 0 | `0s0_1s0-2s0__3s0-4s1-5s0-6s0-7s0-8s1` | H3/two | presplit | certified | 30.9 | 35.7 |
| 74 | 1 | `0s0_1s0-2s0__3s1-4s1-5s1-6s1-7s0-8s1` | H3/two | presplit | certified | 49.1 | 36.3 |
| 118 | 2 | `0s0_1s0-2s1__3s1-4s1-5s0-6s0-7s0-8s0` | H3/two | timeout300 | certified | 270.7 | 60.2 |
| 162 | 0 | `0s0_1s0-4s1__2s0-3s0-5s0-6s1-7s0-8s1` | H3/two | timeout300 | certified | 272.9 | 55.7 |
| 206 | 1 | `0s0_1s0-4s1__2s1-3s1-5s0-6s1-7s1-8s0` | H3/two | timeout300 | certified | 336.4 | 59.2 |
| 250 | 2 | `0s0_1s0-6s1__2s1-3s1-4s1-5s1-7s0-8s1` | H3/two | timeout300 | certified | 348.7 | 61.1 |
| 294 | 0 | `0s0_1s0-7s0__2s1-3s1-4s0-5s1-6s1-8s1` | H3/two | timeout300 | certified | 137.1 | 47.7 |
| 338 | 1 | `0s0_1s1-2s0__3s1-4s0-5s0-6s0-7s1-8s1` | H3/two | timeout300 | certified | 334.7 | 59.3 |
| 382 | 2 | `0s0_1s1-4s0__2s1-3s1-5s0-6s1-7s0-8s0` | H3/two | timeout300 | certified | 328.5 | 52.9 |
| 426 | 0 | `0s0_1s1-5s0__2s1-3s1-4s0-6s1-7s1-8s0` | H3/two | timeout300 | certified | 301.1 | 55.7 |
| 470 | 1 | `0s0_1s1-5s1__2s1-3s0-4s0-6s0-7s1-8s1` | H3/two | presplit | certified | 142.9 | 46.7 |
| 514 | 2 | `0s0_1s1-7s1__2s0-3s1-4s1-5s1-6s0-8s1` | H3/two | timeout300 | certified | 385.7 | 56.9 |
| 558 | 0 | `0s0_1s1-8s0__2s0-3s0-4s1-5s0-6s1-7s1` | H3/two | presplit | certified | 121.9 | 30.9 |
| 602 | 1 | `0s0_1s1-8s0__2s1-3s1-4s0-5s1-6s1-7s1` | H3/two | presplit | certified | 137.8 | 46.7 |
| 646 | 2 | `0s0_1s1-8s1__2s1-3s1-4s1-5s1-6s1-7s1` | H3/two | timeout300 | certified | 398.6 | 56.1 |
| 690 | 0 | `0s0_1s1-9s1__2s1-3s1-4s1-5s0-6s0-7s0` | H3/two | never_ran | certified | 340.0 | 58.3 |
| 734 | 1 | `0s0_2s0-3s1__1s1-4s0-5s0-6s1-7s0-8s0` | H3/two | presplit | certified | 321.5 | 53.5 |
| 778 | 2 | `0s0_2s0-4s1__1s0-3s1-5s0-6s0-7s0-8s0` | H3/two | presplit | certified | 253.6 | 45.5 |
| 822 | 0 | `0s0_2s0-4s1__1s1-3s1-5s1-6s1-7s0-8s0` | H3/two | presplit | certified | 284.6 | 50.3 |
| 866 | 1 | `0s0_2s0-5s0__1s1-3s0-4s1-6s0-7s0-8s0` | H3/two | presplit | certified | 64.9 | 38.6 |
| 910 | 2 | `0s0_2s0-5s1__1s0-3s1-4s1-6s0-7s1-8s1` | H3/two | timeout300 | certified | 410.5 | 56.6 |
| 954 | 0 | `0s0_2s0-6s1__1s0-3s0-4s1-5s0-7s0-8s1` | H3/two | timeout300 | certified | 277.4 | 49.3 |
| 998 | 1 | `0s0_2s0-6s1__1s1-3s1-4s0-5s1-7s0-8s1` | H3/two | timeout300 | certified | 300.4 | 53.7 |
| 1042 | 2 | `0s0_2s0-7s0__1s1-3s0-4s0-5s0-6s0-8s1` | H3/two | presplit | certified | 186.7 | 42.9 |
| 1086 | 0 | `0s0_2s0-7s1__1s0-3s0-4s1-5s1-6s0-8s1` | H3/two | presplit | certified | 277.3 | 48.4 |
| 1130 | 1 | `0s0_2s0-7s1__1s1-3s1-4s1-5s0-6s0-8s1` | H3/two | presplit | certified | 369.7 | 56.7 |
| 1174 | 2 | `0s0_2s0-8s0__1s1-3s1-4s0-5s1-6s1-7s1` | H3/two | presplit | certified | 121.5 | 38.2 |
| 1218 | 0 | `0s0_2s1-3s0__1s1-4s0-5s0-6s1-7s0-8s0` | H3/two | timeout300 | certified | 341.3 | 54.6 |
| 1262 | 1 | `0s0_2s1-3s1__1s0-4s1-5s0-6s0-7s0-8s0` | H3/two | presplit | certified | 49.9 | 30.9 |
| 1306 | 2 | `0s0_2s1-3s1__1s1-4s1-5s1-6s1-7s0-8s0` | H3/two | presplit | certified | 45.3 | 30.9 |
| 1350 | 0 | `0s0_2s1-4s0__1s1-3s0-5s1-6s1-7s1-8s0` | H3/two | timeout300 | certified | 414.3 | 54.8 |
| 1394 | 1 | `0s0_2s1-5s0__1s0-3s1-4s1-6s0-7s1-8s0` | H3/two | presplit | certified | 396.9 | 61.4 |
| 1438 | 2 | `0s0_2s1-6s0__1s0-3s0-4s0-5s1-7s1-8s0` | H3/two | presplit | certified | 254.9 | 42.7 |
| 1482 | 0 | `0s0_2s1-6s0__1s1-3s1-4s0-5s0-7s1-8s0` | H3/two | presplit | certified | 266.2 | 45.6 |
| 1526 | 1 | `0s0_2s1-6s1__1s0-3s1-4s1-5s1-7s1-8s0` | H3/two | presplit | certified | 294.0 | 44.5 |
| 1570 | 2 | `0s0_2s1-7s0__1s0-3s1-4s0-5s0-6s1-8s0` | H3/two | timeout300 | certified | 160.6 | 38.9 |
| 1614 | 0 | `0s0_2s1-7s0__1s1-3s1-4s1-5s1-6s1-8s0` | H3/two | never_ran | certified | 258.2 | 43.0 |
| 1658 | 1 | `0s0_2s1-8s1__1s0-3s0-4s1-5s1-6s0-7s1` | H3/two | presplit | certified | 325.4 | 62.0 |
| 1702 | 2 | `0s0_2s1-8s1__1s1-3s1-4s1-5s0-6s0-7s1` | H3/two | presplit | certified | 319.0 | 41.3 |
| 1746 | 0 | `0s0_2s1-9s0__1s1-3s0-4s0-5s1-6s0-7s1` | H3/two | presplit | certified | 124.1 | 47.9 |
| 1790 | 1 | `0s0_3s0-4s1__1s0-2s1-5s0-6s0-7s0-8s1` | H3/two | presplit | certified | 325.8 | 41.9 |
| 1834 | 2 | `0s0_3s0-4s1__1s1-2s1-5s1-6s1-7s0-8s1` | H3/two | presplit | certified | 448.1 | 53.2 |
| 1878 | 0 | `0s0_3s0-5s0__1s1-2s0-4s1-6s0-7s0-8s1` | H3/two | presplit | certified | 36.0 | 21.5 |
| 1922 | 1 | `0s0_3s0-5s1__1s0-2s1-4s1-6s1-7s1-8s1` | H3/two | timeout300 | certified | 338.4 | 47.0 |
| 1966 | 2 | `0s0_3s0-6s0__1s0-2s0-4s1-5s0-7s1-8s1` | H3/two | presplit | certified | 60.3 | 31.5 |
| 2010 | 0 | `0s0_3s0-6s0__1s1-2s1-4s0-5s1-7s1-8s1` | H3/two | presplit | certified | 96.6 | 33.4 |
| 2054 | 1 | `0s0_3s0-6s1__1s1-2s0-4s0-5s0-7s1-8s1` | H3/two | timeout300 | certified | 363.1 | 48.2 |
| 2098 | 2 | `0s0_3s0-7s0__1s0-2s0-4s1-5s1-6s1-8s1` | H3/two | presplit | certified | 83.5 | 29.2 |
| 2142 | 0 | `0s0_3s0-7s0__1s1-2s1-4s1-5s0-6s1-8s1` | H3/two | presplit | certified | 100.6 | 34.3 |
| 2186 | 1 | `0s0_3s0-7s1__1s1-2s0-4s0-5s1-6s1-8s1` | H3/two | presplit | certified | 400.9 | 69.6 |
| 2230 | 2 | `0s0_3s0-8s0__1s1-2s0-4s1-5s0-6s0-7s1` | H3/two | presplit | certified | 117.2 | 32.7 |
| 2274 | 0 | `0s0_3s0-8s1__1s1-2s1-4s1-5s0-6s0-7s0` | H3/two | timeout300 | certified | 267.1 | 39.1 |
| 2318 | 1 | `0s0_3s1-4s0__1s1-2s0-5s0-6s1-7s1-8s0` | H3/two | timeout300 | certified | 462.1 | 49.6 |
| 2362 | 2 | `0s0_3s1-4s1__1s0-2s1-5s0-6s0-7s1-8s0` | H3/two | presplit | certified | 62.8 | 29.7 |
| 2406 | 0 | `0s0_3s1-4s1__1s1-2s1-5s1-6s1-7s1-8s0` | H3/two | presplit | certified | 52.1 | 24.8 |
| 2450 | 1 | `0s0_3s1-5s0__1s1-2s0-4s1-6s0-7s1-8s0` | H3/two | presplit | certified | 421.4 | 47.9 |
| 2494 | 2 | `0s0_3s1-5s1__1s0-2s1-4s0-6s1-7s1-8s0` | H3/two | presplit | certified | 73.8 | 28.7 |
| 2538 | 0 | `0s0_3s1-6s0__1s1-2s1-4s0-5s1-7s1-8s0` | H3/two | timeout300 | certified | 499.2 | 52.4 |
| 2582 | 1 | `0s0_3s1-7s0__1s1-2s1-4s1-5s1-6s0-8s0` | H3/two | never_ran | certified | 329.8 | 43.0 |
| 2626 | 2 | `0s0_3s1-8s0__1s0-2s0-4s1-5s1-6s1-7s1` | H3/two | presplit | certified | 230.9 | 35.7 |
| 2670 | 0 | `0s0_3s1-8s0__1s1-2s1-4s1-5s0-6s1-7s1` | H3/two | presplit | certified | 340.0 | 46.6 |
| 2714 | 1 | `0s0_4s0-5s1__1s1-2s0-3s0-6s1-7s1-8s1` | H3/two | presplit | certified | 405.2 | 48.0 |
| 2758 | 2 | `0s0_4s0-6s1__1s0-2s1-3s0-5s0-7s1-8s1` | H3/two | presplit | certified | 394.9 | 50.9 |
| 2802 | 0 | `0s0_4s0-6s1__1s1-2s1-3s1-5s1-7s1-8s1` | H3/two | presplit | certified | 365.0 | 65.6 |
| 2846 | 1 | `0s0_4s0-7s0__1s1-2s0-3s1-5s0-6s1-8s1` | H3/two | presplit | certified | 72.1 | 31.5 |
| 2890 | 2 | `0s0_4s0-7s1__1s1-2s0-3s0-5s0-6s0-8s0` | H3/two | presplit | certified | 254.6 | 42.5 |
| 2934 | 0 | `0s0_4s1-5s0__1s0-2s0-3s1-6s1-7s0-8s0` | H3/two | never_ran | certified | 440.2 | 48.6 |
| 2978 | 1 | `0s0_4s1-5s0__1s1-2s1-3s1-6s0-7s0-8s0` | H3/two | never_ran | certified | 419.6 | 49.5 |
| 3022 | 2 | `0s0_4s1-6s0__1s0-2s1-3s1-5s0-7s1-8s1` | H3/two | presplit | certified | 390.6 | 44.5 |
| 3066 | 0 | `0s0_4s1-6s1__1s0-2s0-3s0-5s1-7s1-8s1` | H3/two | presplit | certified | 101.4 | 29.1 |
| 3110 | 1 | `0s0_4s1-6s1__1s1-2s1-3s0-5s0-7s1-8s1` | H3/two | presplit | certified | 78.0 | 45.5 |
| 3154 | 2 | `0s0_4s1-7s0__1s0-2s1-3s1-5s1-6s1-8s1` | H3/two | presplit | certified | 342.7 | 42.0 |
| 3198 | 0 | `0s0_5s0-6s0__1s0-2s0-3s1-4s0-7s1-8s1` | H3/two | presplit | certified | 31.9 | 18.4 |
| 3242 | 1 | `0s0_5s0-6s0__1s1-2s1-3s0-4s1-7s1-8s1` | H3/two | presplit | certified | 50.6 | 34.4 |
| 3286 | 2 | `0s0_5s0-6s1__1s1-2s0-3s0-4s0-7s1-8s1` | H3/two | presplit | certified | 316.3 | 47.4 |
| 3330 | 0 | `0s0_5s1-6s0__1s1-2s1-3s0-4s0-7s1-8s1` | H3/two | timeout300 | certified | 419.3 | 61.3 |
| 3374 | 1 | `0s0-1s1_5__2s0-3s1-4s1-6s0-7s1-8s0` | H6(1,1)/one | timeout300 | certified | 325.1 | 55.2 |
| 3418 | 2 | `0s0-2s1_3__1s1-4s1-5s0-6s0-7s0-8s0` | H6(2,1)/one | timeout300 | certified | 271.4 | 53.5 |
| 3462 | 0 | `0s0-2s1_5__1s0-3s0-4s0-6s1-7s1-8s0` | H6(2,1)/one | timeout300 | certified | 259.8 | 36.8 |
| 3506 | 1 | `0s0-2s1_5__1s1-3s1-4s1-6s0-7s1-8s1` | H6(2,1)/one | timeout300 | certified | 229.6 | 41.0 |
| 3550 | 2 | `0s0-2s1_6__1s1-3s0-4s1-5s0-7s0-8s1` | H6(2,1)/one | timeout300 | certified | 189.5 | 52.5 |
| 3594 | 0 | `0s0-3s1_4__1s1-2s0-5s1-6s1-7s0-8s1` | H6(3,1)/one | never_ran | certified | 204.1 | 36.7 |
| 3638 | 1 | `0s0-3s1_5__1s0-2s1-4s1-6s0-7s0-8s1` | H6(3,1)/one | presplit | certified | 235.4 | 35.4 |
| 3682 | 2 | `0s0-4s0_6__1s0-2s0-3s0-5s1-7s0-8s1` | H6(4,0)/one | presplit | certified | 39.9 | 26.6 |
| 3726 | 0 | `0s0-4s0_6__1s1-2s1-3s0-5s0-7s0-8s1` | H6(4,0)/one | presplit | certified | 39.0 | 26.2 |
| 3770 | 1 | `0s0-5s0_6__1s0-2s1-3s1-4s0-7s0-8s0` | H6(5,0)/one | presplit | certified | 70.5 | 33.4 |
| 3814 | 2 | `0s0-5s0_7__1s0-2s0-3s0-4s1-6s0-8s0` | H6(5,0)/one | presplit | certified | 48.5 | 30.0 |
| 3858 | 0 | `0s0-5s0_7__1s1-2s1-3s0-4s0-6s0-8s0` | H6(5,0)/one | presplit | certified | 56.7 | 30.5 |
| 3902 | 1 | `0s0-5s1_1__2s1-3s0-4s1-6s0-7s1-8s0` | H6(5,1)/one | presplit | certified | 152.0 | 37.2 |
| 3946 | 2 | `0s0-5s1_2__1s0-3s1-4s0-6s1-7s1-8s0` | H6(5,1)/one | presplit | certified | 181.2 | 38.6 |
| 3990 | 0 | `0s0-5s1_6__1s1-2s0-3s0-4s0-7s1-8s1` | H6(5,1)/one | never_ran | certified | 237.8 | 39.5 |
| 4034 | 1 | `0s0-5s1_1s1-10s1__2s0-3s1-4s0-6s1-7s0-8s1` | H6(5,1)/two | never_ran | certified | 40.0 | 27.5 |
| 4078 | 2 | `0s0-5s1_2s1-3s0__1s1-4s0-6s0-7s0-8s0-9s1` | H6(5,1)/two | never_ran | certified | 34.4 | 22.4 |
