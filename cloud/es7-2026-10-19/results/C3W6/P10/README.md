# C3W6 / P10: shard 10 of 44 of `W6.tsv`, cap 900, one machine

**Result: all 94 units certified at cap 900** (both checkers on every one: lrat-check `c VERIFIED`, cake_lpr `s VERIFIED UNSAT`). None timed out, all were reached, and nothing was split. No SAT, no proof rejection, no `none` checker result, no memory problem, and no unit ended early without a certificate.

## Setup

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 05:31:10 UTC on 2026-10-25, END 09:46:10 UTC (H = 4.5). Lanes ran from 05:34:43 and were finished by 08:36:40 (lane 1 at 08:00:40, lane 0 at 08:26:47, lane 2 at 08:36:40), before END, so nothing was killed.

- Tools: worktree of cad4e050 at `/opt/c3u2`, TOOLS = `results/C3U2/tools`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 (c60730422e758ef1cebe7aeddf2dda31c996bf04). cake_lpr a36874a8 (its example gives `s VERIFIED UNSAT`). lrat-check 2e3b2dc with the E2 patch. Sanity test: on {1},{-1}, `3 0 0` was rejected by both checkers and `3 0 1 2 0` was accepted by both.
- Base CNF from `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches).
- Units: the rows of `lists/W6.tsv` with row ≡ 10 (mod 44), giving 94 units (`units.tsv`). 93 are six-bit cubes and one is a 3-bit cube (`0s0-5s1_7s0-9s1__1s0-2s0-3s1`, row 4102). No records were seeded.
- Lanes `lane0.sh`, `lane1.sh` and `lane2.sh` took positions ≡ 0, 1, 2 (mod 3): 32, 31 and 31 units. Each unit ran `close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`.
- Files: `out.jsonl` (94 records, lane 0, then 1, then 2), `driver{k}.log.tail`, `tools.txt`. There is no `recheck.jsonl` because no re-check was needed.

## Totals

| stratum | units | certified | timed out at 900 | not reached |
|---|---|---|---|---|
| H3/two | 76 | 76 | 0 | 0 |
| H6(1,1)/one | 2 | 2 | 0 | 0 |
| H6(2,1)/one | 3 | 3 | 0 | 0 |
| H6(3,1)/one | 3 | 3 | 0 | 0 |
| H6(4,0)/one | 1 | 1 | 0 | 0 |
| H6(5,0)/one | 3 | 3 | 0 | 0 |
| H6(5,1)/one | 4 | 4 | 0 | 0 |
| H6(5,1)/two | 2 | 2 | 0 | 0 |

| prior | units | certified | timed out at 900 | not reached |
|---|---|---|---|---|
| never_ran | 9 | 9 | 0 | 0 |
| presplit | 56 | 56 | 0 | 0 |
| timeout300 | 29 | 29 | 0 | 0 |

Solve time of the 94 certified units: min 29.7, Q1 139.5, median 310.3, Q3 386.4, p90 433.6, max 500.0 s; 51 certified above 300 s; total solve 25701 s, total check 4171 s (check per unit 19.2–68.5 s).

Under 72 s: 12 units, all with a certificate (none ended early without one).

## Per unit

| row | unit | stratum | prior | lane | result | solve s | check s |
|---|---|---|---|---|---|---|---|
| 10 | `0s0_1s0-10s0__2s1-3s1-4s0-5s1-6s1-7s1` | H3/two | timeout300 | 0 | certified | 199.6 | 53.3 |
| 54 | `0s0_1s0-2s0__3s1-4s0-5s1-6s0-7s0-8s1` | H3/two | presplit | 1 | certified | 35.9 | 37.2 |
| 98 | `0s0_1s0-2s1__3s0-4s1-5s1-6s1-7s0-8s0` | H3/two | timeout300 | 2 | certified | 396.9 | 68.5 |
| 142 | `0s0_1s0-3s1__2s1-4s0-5s0-6s1-7s1-8s0` | H3/two | timeout300 | 0 | certified | 416.3 | 65.8 |
| 186 | `0s0_1s0-4s1__2s1-3s0-5s0-6s0-7s1-8s0` | H3/two | timeout300 | 1 | certified | 366.4 | 58.4 |
| 230 | `0s0_1s0-5s1__2s1-3s0-4s1-6s1-7s0-8s0` | H3/two | timeout300 | 2 | certified | 291.8 | 57.7 |
| 274 | `0s0_1s0-7s0__2s1-3s0-4s0-5s0-6s1-8s0` | H3/two | timeout300 | 0 | certified | 140.2 | 44.7 |
| 318 | `0s0_1s1-2s0__3s0-4s0-5s1-6s1-7s1-8s1` | H3/two | timeout300 | 1 | certified | 320.2 | 56.9 |
| 362 | `0s0_1s1-2s0__3s1-4s1-5s1-6s0-7s1-8s1` | H3/two | timeout300 | 2 | certified | 432.6 | 65.4 |
| 406 | `0s0_1s1-5s0__2s0-3s1-4s1-6s1-7s1-8s1` | H3/two | timeout300 | 0 | certified | 327.2 | 52.3 |
| 450 | `0s0_1s1-5s1__2s0-3s0-4s1-6s1-7s1-8s1` | H3/two | presplit | 1 | certified | 140.2 | 43.3 |
| 494 | `0s0_1s1-5s1__2s1-3s1-4s1-6s0-7s1-8s1` | H3/two | presplit | 2 | certified | 327.6 | 44.3 |
| 538 | `0s0_1s1-7s1__2s1-3s1-4s0-5s1-6s1-8s1` | H3/two | timeout300 | 0 | certified | 406.3 | 52.4 |
| 582 | `0s0_1s1-8s0__2s1-3s0-4s0-5s0-6s1-7s1` | H3/two | presplit | 1 | certified | 105.1 | 44.3 |
| 626 | `0s0_1s1-8s1__2s1-3s0-4s1-5s0-6s1-7s0` | H3/two | timeout300 | 2 | certified | 411.0 | 54.2 |
| 670 | `0s0_1s1-9s1__2s1-3s0-4s0-5s1-6s0-7s0` | H3/two | never_ran | 0 | certified | 380.0 | 47.7 |
| 714 | `0s0_2s0-3s1__1s0-4s1-5s0-6s0-7s0-8s0` | H3/two | presplit | 1 | certified | 376.2 | 53.2 |
| 758 | `0s0_2s0-3s1__1s1-4s1-5s1-6s1-7s0-8s0` | H3/two | presplit | 2 | certified | 434.6 | 52.9 |
| 802 | `0s0_2s0-4s1__1s1-3s0-5s1-6s0-7s0-8s0` | H3/two | presplit | 0 | certified | 417.0 | 65.7 |
| 846 | `0s0_2s0-5s0__1s0-3s1-4s0-6s1-7s0-8s0` | H3/two | presplit | 1 | certified | 50.5 | 31.8 |
| 890 | `0s0_2s0-5s1__1s0-3s0-4s0-6s1-7s1-8s1` | H3/two | timeout300 | 2 | certified | 340.6 | 43.7 |
| 934 | `0s0_2s0-5s1__1s1-3s1-4s0-6s0-7s1-8s1` | H3/two | timeout300 | 0 | certified | 465.2 | 49.6 |
| 978 | `0s0_2s0-6s1__1s1-3s0-4s0-5s0-7s0-8s1` | H3/two | timeout300 | 1 | certified | 342.8 | 51.5 |
| 1022 | `0s0_2s0-7s0__1s0-3s0-4s1-5s1-6s0-8s1` | H3/two | presplit | 2 | certified | 124.0 | 50.4 |
| 1066 | `0s0_2s0-7s0__1s1-3s1-4s1-5s0-6s0-8s1` | H3/two | presplit | 0 | certified | 166.7 | 36.0 |
| 1110 | `0s0_2s0-7s1__1s1-3s0-4s0-5s1-6s0-8s1` | H3/two | presplit | 1 | certified | 300.7 | 46.2 |
| 1154 | `0s0_2s0-8s0__1s1-3s0-4s0-5s0-6s1-7s1` | H3/two | presplit | 2 | certified | 207.2 | 36.9 |
| 1198 | `0s0_2s1-3s0__1s0-4s1-5s0-6s0-7s0-8s0` | H3/two | timeout300 | 0 | certified | 341.7 | 57.4 |
| 1242 | `0s0_2s1-3s0__1s1-4s1-5s1-6s1-7s0-8s0` | H3/two | timeout300 | 1 | certified | 440.5 | 48.9 |
| 1286 | `0s0_2s1-3s1__1s1-4s0-5s1-6s0-7s0-8s0` | H3/two | presplit | 2 | certified | 47.4 | 22.2 |
| 1330 | `0s0_2s1-4s0__1s0-3s1-5s1-6s0-7s0-8s1` | H3/two | timeout300 | 0 | certified | 422.1 | 58.9 |
| 1374 | `0s0_2s1-5s0__1s0-3s0-4s0-6s1-7s1-8s0` | H3/two | presplit | 1 | certified | 252.7 | 40.8 |
| 1418 | `0s0_2s1-5s0__1s1-3s1-4s0-6s0-7s1-8s0` | H3/two | presplit | 2 | certified | 451.8 | 52.1 |
| 1462 | `0s0_2s1-6s0__1s0-3s1-4s1-5s1-7s1-8s0` | H3/two | presplit | 0 | certified | 380.1 | 50.1 |
| 1506 | `0s0_2s1-6s1__1s0-3s0-4s1-5s0-7s1-8s0` | H3/two | presplit | 1 | certified | 114.6 | 47.8 |
| 1550 | `0s0_2s1-6s1__1s1-3s1-4s0-5s1-7s1-8s0` | H3/two | presplit | 2 | certified | 176.5 | 40.0 |
| 1594 | `0s0_2s1-7s0__1s1-3s0-4s1-5s0-6s1-8s0` | H3/two | never_ran | 0 | certified | 314.4 | 44.9 |
| 1638 | `0s0_2s1-7s1__1s1-3s1-4s0-5s0-6s0-8s0` | H3/two | never_ran | 1 | certified | 137.5 | 34.3 |
| 1682 | `0s0_2s1-8s1__1s1-3s0-4s0-5s1-6s0-7s1` | H3/two | presplit | 2 | certified | 384.8 | 45.5 |
| 1726 | `0s0_2s1-9s0__1s0-3s1-4s0-5s0-6s0-7s1` | H3/two | presplit | 0 | certified | 83.6 | 30.1 |
| 1770 | `0s0_2s1-9s0__1s1-3s1-4s1-5s1-6s0-7s1` | H3/two | presplit | 1 | certified | 133.7 | 35.2 |
| 1814 | `0s0_3s0-4s1__1s1-2s0-5s1-6s0-7s0-8s1` | H3/two | presplit | 2 | certified | 489.6 | 59.2 |
| 1858 | `0s0_3s0-5s0__1s0-2s1-4s0-6s1-7s0-8s1` | H3/two | presplit | 0 | certified | 39.1 | 19.2 |
| 1902 | `0s0_3s0-5s1__1s0-2s0-4s1-6s0-7s0-8s1` | H3/two | timeout300 | 1 | certified | 306.2 | 43.0 |
| 1946 | `0s0_3s0-5s1__1s1-2s1-4s0-6s1-7s1-8s1` | H3/two | timeout300 | 2 | certified | 497.8 | 55.9 |
| 1990 | `0s0_3s0-6s0__1s1-2s0-4s0-5s0-7s1-8s1` | H3/two | presplit | 0 | certified | 97.4 | 40.9 |
| 2034 | `0s0_3s0-6s1__1s0-2s0-4s1-5s1-7s1-8s1` | H3/two | timeout300 | 1 | certified | 320.3 | 44.8 |
| 2078 | `0s0_3s0-6s1__1s1-2s1-4s1-5s0-7s1-8s1` | H3/two | never_ran | 2 | certified | 500.0 | 53.2 |
| 2122 | `0s0_3s0-7s0__1s1-2s0-4s0-5s1-6s1-8s1` | H3/two | presplit | 0 | certified | 92.8 | 30.4 |
| 2166 | `0s0_3s0-7s1__1s0-2s1-4s0-5s0-6s1-8s1` | H3/two | presplit | 1 | certified | 408.9 | 52.1 |
| 2210 | `0s0_3s0-7s1__1s1-2s1-4s1-5s1-6s1-8s1` | H3/two | presplit | 2 | certified | 372.2 | 41.6 |
| 2254 | `0s0_3s0-8s1__1s0-2s0-4s1-5s1-6s1-7s0` | H3/two | timeout300 | 0 | certified | 375.5 | 47.1 |
| 2298 | `0s0_3s1-4s0__1s0-2s1-5s0-6s0-7s1-8s0` | H3/two | timeout300 | 1 | certified | 372.3 | 48.6 |
| 2342 | `0s0_3s1-4s0__1s1-2s1-5s1-6s1-7s1-8s0` | H3/two | never_ran | 2 | certified | 407.0 | 47.8 |
| 2386 | `0s0_3s1-4s1__1s1-2s0-5s1-6s0-7s1-8s0` | H3/two | presplit | 0 | certified | 63.9 | 26.8 |
| 2430 | `0s0_3s1-5s0__1s0-2s1-4s0-6s1-7s1-8s0` | H3/two | presplit | 1 | certified | 396.8 | 56.8 |
| 2474 | `0s0_3s1-5s1__1s0-2s0-4s0-6s0-7s1-8s0` | H3/two | presplit | 2 | certified | 81.5 | 27.6 |
| 2518 | `0s0_3s1-5s1__1s1-2s0-4s1-6s1-7s1-8s0` | H3/two | presplit | 0 | certified | 69.4 | 29.8 |
| 2562 | `0s0_3s1-7s0__1s1-2s0-4s1-5s0-6s0-8s0` | H3/two | never_ran | 1 | certified | 279.8 | 56.3 |
| 2606 | `0s0_3s1-7s1__1s1-2s1-4s1-5s0-6s1-8s0` | H3/two | timeout300 | 2 | certified | 245.0 | 59.2 |
| 2650 | `0s0_3s1-8s0__1s1-2s0-4s0-5s1-6s1-7s1` | H3/two | presplit | 0 | certified | 360.0 | 48.6 |
| 2694 | `0s0_4s0-5s1__1s0-2s1-3s0-6s0-7s1-8s1` | H3/two | presplit | 1 | certified | 396.4 | 48.6 |
| 2738 | `0s0_4s0-5s1__1s1-2s1-3s1-6s1-7s1-8s1` | H3/two | presplit | 2 | certified | 357.5 | 43.3 |
| 2782 | `0s0_4s0-6s1__1s1-2s0-3s1-5s0-7s1-8s1` | H3/two | presplit | 0 | certified | 452.8 | 53.1 |
| 2826 | `0s0_4s0-7s0__1s0-2s1-3s0-5s1-6s1-8s1` | H3/two | presplit | 1 | certified | 67.9 | 26.9 |
| 2870 | `0s0_4s0-7s1__1s0-2s0-3s1-5s1-6s0-8s0` | H3/two | presplit | 2 | certified | 336.8 | 44.8 |
| 2914 | `0s0_4s0-7s1__1s1-2s1-3s1-5s0-6s0-8s0` | H3/two | presplit | 0 | certified | 346.9 | 47.0 |
| 2958 | `0s0_4s1-5s0__1s1-2s0-3s0-6s1-7s0-8s0` | H3/two | never_ran | 1 | certified | 329.1 | 48.0 |
| 3002 | `0s0_4s1-6s0__1s0-2s0-3s0-5s1-7s1-8s1` | H3/two | presplit | 2 | certified | 260.9 | 38.5 |
| 3046 | `0s0_4s1-6s0__1s1-2s1-3s0-5s0-7s1-8s1` | H3/two | presplit | 0 | certified | 411.9 | 44.7 |
| 3090 | `0s0_4s1-6s1__1s0-2s1-3s1-5s1-7s1-8s1` | H3/two | presplit | 1 | certified | 65.8 | 28.3 |
| 3134 | `0s0_4s1-7s0__1s0-2s0-3s1-5s0-6s1-8s1` | H3/two | presplit | 2 | certified | 324.3 | 48.8 |
| 3178 | `0s0_4s1-7s0__1s1-2s1-3s0-5s1-6s1-8s1` | H3/two | presplit | 0 | certified | 397.6 | 44.7 |
| 3222 | `0s0_5s0-6s0__1s1-2s0-3s0-4s0-7s1-8s1` | H3/two | presplit | 1 | certified | 29.7 | 22.6 |
| 3266 | `0s0_5s0-6s1__1s0-2s0-3s1-4s1-7s1-8s1` | H3/two | presplit | 2 | certified | 377.5 | 50.2 |
| 3310 | `0s0_5s0-6s1__1s1-2s1-3s1-4s0-7s1-8s1` | H3/two | presplit | 0 | certified | 448.7 | 47.1 |
| 3354 | `0s0-1s1_4__2s1-3s1-5s0-6s1-7s1-8s0` | H6(1,1)/one | timeout300 | 1 | certified | 323.2 | 43.2 |
| 3398 | `0s0-1s1_5__2s1-3s1-4s0-6s0-7s1-8s0` | H6(1,1)/one | timeout300 | 2 | certified | 244.8 | 42.7 |
| 3442 | `0s0-2s1_4__1s1-3s0-5s1-6s1-7s1-8s0` | H6(2,1)/one | timeout300 | 0 | certified | 391.1 | 45.9 |
| 3486 | `0s0-2s1_5__1s1-3s0-4s0-6s1-7s1-8s1` | H6(2,1)/one | timeout300 | 1 | certified | 201.0 | 35.7 |
| 3530 | `0s0-2s1_6__1s0-3s1-4s0-5s1-7s0-8s1` | H6(2,1)/one | timeout300 | 2 | certified | 256.4 | 48.7 |
| 3574 | `0s0-3s1_4__1s0-2s0-5s1-6s1-7s1-8s0` | H6(3,1)/one | timeout300 | 0 | certified | 304.8 | 43.9 |
| 3618 | `0s0-3s1_5__1s0-2s0-4s0-6s1-7s0-8s1` | H6(3,1)/one | presplit | 1 | certified | 229.7 | 38.8 |
| 3662 | `0s0-3s1_5__1s1-2s1-4s0-6s0-7s0-8s1` | H6(3,1)/one | presplit | 2 | certified | 305.0 | 41.6 |
| 3706 | `0s0-4s0_6__1s0-2s1-3s1-5s1-7s0-8s1` | H6(4,0)/one | presplit | 0 | certified | 73.1 | 30.1 |
| 3750 | `0s0-5s0_6__1s0-2s0-3s0-4s1-7s0-8s0` | H6(5,0)/one | presplit | 1 | certified | 67.7 | 28.5 |
| 3794 | `0s0-5s0_6__1s1-2s1-3s0-4s0-7s0-8s0` | H6(5,0)/one | presplit | 2 | certified | 68.2 | 32.3 |
| 3838 | `0s0-5s0_7__1s0-2s1-3s1-4s1-6s0-8s0` | H6(5,0)/one | presplit | 0 | certified | 85.2 | 31.8 |
| 3882 | `0s0-5s1_1__2s0-3s1-4s0-6s1-7s1-8s0` | H6(5,1)/one | presplit | 1 | certified | 219.5 | 36.3 |
| 3926 | `0s0-5s1_2__1s0-3s0-4s0-6s0-7s1-8s0` | H6(5,1)/one | presplit | 2 | certified | 244.0 | 37.2 |
| 3970 | `0s0-5s1_2__1s1-3s0-4s1-6s1-7s1-8s0` | H6(5,1)/one | presplit | 0 | certified | 193.7 | 37.0 |
| 4014 | `0s0-5s1_6__1s1-2s1-3s1-4s0-7s1-8s1` | H6(5,1)/one | never_ran | 1 | certified | 257.5 | 39.6 |
| 4058 | `0s0-5s1_1s1-10s1__2s1-3s0-4s1-6s1-7s0-8s1` | H6(5,1)/two | never_ran | 2 | certified | 44.9 | 28.1 |
| 4102 | `0s0-5s1_7s0-9s1__1s0-2s0-3s1` | H6(5,1)/two | presplit | 0 | certified | 207.8 | 31.4 |

Solve and check times are per node. Three lanes shared 4 cores, so they are not single-core times.
