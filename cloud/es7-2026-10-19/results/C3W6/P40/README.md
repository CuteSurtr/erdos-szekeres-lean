# C3W6 P40: W6.tsv shard 40 of 44

Task: `results/C3W6/TASK.md` at c5260b44, with V = P40, LIST = W6.tsv, j = 40, N = 44, H = 4.5.
Start 2026-10-25 05:31:44 UTC, lanes started 05:33:56, END would have been 09:46:44; all three lanes ran through their units and finished early (lane 0 at 07:40:35, lane 2 at 07:45:31, lane 1 at 08:04:11). Nothing was killed at END.

## Tools and base check

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, used unmodified. `compose.py` was not run.
- CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8 (example: `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch. Sanity test passed: `3 0 0` on {1},{-1} is rejected by both checkers, `3 0 1 2 0` is accepted by both.
- Base CNF from `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da`, which matches.
- Full details are in `tools.txt`.

## Result

**All 93 units were certified at cap 900.** None timed out and none went unreached. All 93 records have status UNSATISFIABLE, `lrat_check` `c VERIFIED` and `cake_lpr` `s VERIFIED UNSAT`. There were no split records, so no unit has open children.

- No SAT result, no proof rejection and no `cake_lpr none`. Nothing needed a re-check, so there is no `recheck.jsonl`.
- No memory problems: peak use was about 7 of 15 GB with 3 lanes.
- No unit ended early without a certificate. 15 units finished their solve in under 72 s, and every one of them has a certificate that both checkers accepted.
- The largest LRAT proof was 604 MB. Proofs are not committed.

### Totals per stratum (all certified)

| stratum | units |
|---|---|
| H3/two | 76 |
| H6(1,1)/one | 1 |
| H6(2,1)/one | 4 |
| H6(3,1)/one | 2 |
| H6(4,0)/one | 2 |
| H6(5,0)/one | 3 |
| H6(5,1)/one | 3 |
| H6(5,1)/two | 2 |
| **total** | **93** |

### Totals per prior (all certified)

| prior | units |
|---|---|
| presplit | 54 |
| timeout300 | 29 |
| never_ran | 10 |

### Solve times of the certified units (seconds)

| min | Q1 | median | Q3 | p90 | max |
|---|---|---|---|---|---|
| 24.7 | 99.9 | 226.4 | 331.0 | 389.2 | 463.2 |

25 of the 93 units were certified above 300 s. These would have timed out at the old cap. Total solve time was 20,640 s and total check time was 3,751 s (largest single check 61.8 s).

## Per unit

| row | node | stratum | prior | result | solve s | check s |
|---|---|---|---|---|---|---|
| 40 | `0s0_1s0-2s0__3s0-4s1-5s1-6s0-7s1-8s1` | H3/two | presplit | certified | 24.7 | 38.2 |
| 84 | `0s0_1s0-2s1__3s0-4s0-5s1-6s1-7s1-8s0` | H3/two | timeout300 | certified | 384.6 | 57.4 |
| 128 | `0s0_1s0-2s1__3s1-4s1-5s1-6s0-7s1-8s0` | H3/two | timeout300 | certified | 399.1 | 61.4 |
| 172 | `0s0_1s0-4s1__2s0-3s1-5s0-6s0-7s1-8s1` | H3/two | timeout300 | certified | 348.3 | 50.0 |
| 216 | `0s0_1s0-5s1__2s0-3s1-4s1-6s0-7s1-8s0` | H3/two | timeout300 | certified | 272.0 | 48.3 |
| 260 | `0s0_1s0-7s0__2s0-3s0-4s1-5s0-6s1-8s1` | H3/two | timeout300 | certified | 161.2 | 45.9 |
| 304 | `0s0_1s0-7s1__2s1-3s1-4s1-5s0-6s1-8s0` | H3/two | timeout300 | certified | 222.1 | 48.1 |
| 348 | `0s0_1s1-2s0__3s1-4s0-5s1-6s1-7s0-8s1` | H3/two | timeout300 | certified | 372.1 | 53.0 |
| 392 | `0s0_1s1-5s0__2s0-3s0-4s0-6s1-7s0-8s0` | H3/two | timeout300 | certified | 225.0 | 42.4 |
| 436 | `0s0_1s1-5s1__2s0-3s0-4s0-6s0-7s0-8s1` | H3/two | presplit | certified | 119.3 | 39.5 |
| 480 | `0s0_1s1-5s1__2s1-3s0-4s1-6s1-7s0-8s1` | H3/two | presplit | certified | 230.1 | 40.1 |
| 524 | `0s0_1s1-7s1__2s1-3s0-4s1-5s0-6s0-8s1` | H3/two | timeout300 | certified | 259.5 | 43.4 |
| 568 | `0s0_1s1-8s0__2s0-3s1-4s0-5s1-6s0-7s1` | H3/two | presplit | certified | 98.2 | 37.2 |
| 612 | `0s0_1s1-8s1__2s0-3s1-4s0-5s1-6s0-7s1` | H3/two | timeout300 | certified | 337.4 | 53.0 |
| 656 | `0s0_1s1-9s1__2s0-3s1-4s0-5s1-6s1-7s0` | H3/two | never_ran | certified | 349.2 | 49.8 |
| 700 | `0s0_2s0-3s1__1s0-4s0-5s0-6s0-7s1-8s0` | H3/two | presplit | certified | 250.6 | 48.8 |
| 744 | `0s0_2s0-3s1__1s1-4s0-5s1-6s1-7s1-8s0` | H3/two | presplit | certified | 390.3 | 49.9 |
| 788 | `0s0_2s0-4s1__1s0-3s1-5s1-6s0-7s1-8s0` | H3/two | presplit | certified | 373.3 | 54.6 |
| 832 | `0s0_2s0-5s0__1s0-3s0-4s0-6s1-7s1-8s0` | H3/two | presplit | certified | 57.3 | 34.0 |
| 876 | `0s0_2s0-5s0__1s1-3s1-4s0-6s0-7s1-8s0` | H3/two | presplit | certified | 68.2 | 31.3 |
| 920 | `0s0_2s0-5s1__1s1-3s0-4s0-6s1-7s0-8s1` | H3/two | timeout300 | certified | 347.3 | 47.4 |
| 964 | `0s0_2s0-6s1__1s0-3s1-4s0-5s0-7s1-8s1` | H3/two | timeout300 | certified | 343.6 | 53.6 |
| 1008 | `0s0_2s0-6s1__1s1-3s1-4s1-5s1-7s1-8s1` | H3/two | timeout300 | certified | 302.7 | 40.9 |
| 1052 | `0s0_2s0-7s0__1s1-3s0-4s1-5s0-6s1-8s1` | H3/two | presplit | certified | 160.1 | 43.8 |
| 1096 | `0s0_2s0-7s1__1s0-3s1-4s0-5s1-6s1-8s1` | H3/two | presplit | certified | 271.2 | 43.9 |
| 1140 | `0s0_2s0-8s0__1s0-3s1-4s0-5s1-6s0-7s1` | H3/two | presplit | certified | 118.7 | 34.1 |
| 1184 | `0s0_2s1-3s0__1s0-4s0-5s0-6s0-7s0-8s1` | H3/two | timeout300 | certified | 227.7 | 38.9 |
| 1228 | `0s0_2s1-3s0__1s1-4s0-5s1-6s1-7s1-8s0` | H3/two | timeout300 | certified | 459.4 | 50.4 |
| 1272 | `0s0_2s1-3s1__1s0-4s1-5s1-6s0-7s1-8s0` | H3/two | presplit | certified | 55.8 | 46.3 |
| 1316 | `0s0_2s1-4s0__1s0-3s0-5s1-6s0-7s0-8s1` | H3/two | timeout300 | certified | 262.2 | 38.9 |
| 1360 | `0s0_2s1-4s0__1s1-3s1-5s1-6s0-7s0-8s0` | H3/two | timeout300 | certified | 288.3 | 40.9 |
| 1404 | `0s0_2s1-5s0__1s1-3s0-4s0-6s1-7s0-8s0` | H3/two | presplit | certified | 286.9 | 38.9 |
| 1448 | `0s0_2s1-6s0__1s0-3s1-4s0-5s0-7s0-8s0` | H3/two | presplit | certified | 161.7 | 32.1 |
| 1492 | `0s0_2s1-6s0__1s1-3s1-4s1-5s1-7s0-8s0` | H3/two | presplit | certified | 258.5 | 34.9 |
| 1536 | `0s0_2s1-6s1__1s1-3s0-4s1-5s0-7s0-8s0` | H3/two | presplit | certified | 122.3 | 34.4 |
| 1580 | `0s0_2s1-7s0__1s0-3s1-4s1-5s1-6s0-8s0` | H3/two | never_ran | certified | 175.0 | 45.2 |
| 1624 | `0s0_2s1-7s1__1s1-3s0-4s0-5s0-6s1-8s0` | H3/two | never_ran | certified | 136.5 | 46.1 |
| 1668 | `0s0_2s1-8s1__1s0-3s1-4s0-5s1-6s1-7s1` | H3/two | presplit | certified | 372.3 | 42.1 |
| 1712 | `0s0_2s1-9s0__1s0-3s0-4s0-5s0-6s1-7s1` | H3/two | presplit | certified | 89.7 | 27.2 |
| 1756 | `0s0_2s1-9s0__1s1-3s0-4s1-5s1-6s1-7s1` | H3/two | presplit | certified | 151.5 | 36.9 |
| 1800 | `0s0_3s0-4s1__1s0-2s1-5s1-6s0-7s1-8s1` | H3/two | presplit | certified | 463.2 | 49.8 |
| 1844 | `0s0_3s0-5s0__1s0-2s0-4s0-6s1-7s1-8s1` | H3/two | presplit | certified | 52.0 | 26.9 |
| 1888 | `0s0_3s0-5s0__1s1-2s1-4s0-6s0-7s1-8s1` | H3/two | presplit | certified | 51.2 | 24.6 |
| 1932 | `0s0_3s0-5s1__1s1-2s0-4s1-6s0-7s0-8s1` | H3/two | timeout300 | certified | 452.5 | 50.6 |
| 1976 | `0s0_3s0-6s0__1s0-2s1-4s0-5s1-7s0-8s1` | H3/two | presplit | certified | 56.6 | 38.7 |
| 2020 | `0s0_3s0-6s1__1s0-2s0-4s0-5s0-7s0-8s1` | H3/two | timeout300 | certified | 170.8 | 37.7 |
| 2064 | `0s0_3s0-6s1__1s1-2s0-4s1-5s1-7s0-8s1` | H3/two | timeout300 | certified | 458.7 | 49.2 |
| 2108 | `0s0_3s0-7s0__1s0-2s1-4s1-5s0-6s0-8s1` | H3/two | presplit | certified | 122.3 | 30.8 |
| 2152 | `0s0_3s0-7s1__1s0-2s0-4s0-5s1-6s0-8s1` | H3/two | presplit | certified | 235.7 | 40.7 |
| 2196 | `0s0_3s0-7s1__1s1-2s1-4s0-5s0-6s0-8s1` | H3/two | presplit | certified | 294.5 | 41.2 |
| 2240 | `0s0_3s0-8s0__1s1-2s1-4s0-5s0-6s1-7s1` | H3/two | presplit | certified | 151.8 | 35.4 |
| 2284 | `0s0_3s1-4s0__1s0-2s0-5s0-6s1-7s0-8s0` | H3/two | timeout300 | certified | 226.4 | 37.9 |
| 2328 | `0s0_3s1-4s0__1s1-2s1-5s0-6s0-7s0-8s0` | H3/two | timeout300 | certified | 292.8 | 41.1 |
| 2372 | `0s0_3s1-4s1__1s0-2s1-5s1-6s1-7s0-8s0` | H3/two | presplit | certified | 42.1 | 22.6 |
| 2416 | `0s0_3s1-5s0__1s0-2s0-4s1-6s0-7s0-8s0` | H3/two | presplit | certified | 265.4 | 41.5 |
| 2460 | `0s0_3s1-5s0__1s1-2s1-4s0-6s1-7s0-8s0` | H3/two | presplit | certified | 381.7 | 45.3 |
| 2504 | `0s0_3s1-5s1__1s1-2s0-4s0-6s0-7s0-8s0` | H3/two | presplit | certified | 101.6 | 35.8 |
| 2548 | `0s0_3s1-7s0__1s0-2s1-4s1-5s0-6s1-8s0` | H3/two | never_ran | certified | 324.5 | 38.8 |
| 2592 | `0s0_3s1-7s1__1s0-2s0-4s1-5s1-6s1-8s1` | H3/two | timeout300 | certified | 229.9 | 35.5 |
| 2636 | `0s0_3s1-8s0__1s0-2s1-4s1-5s0-6s0-7s1` | H3/two | presplit | certified | 180.5 | 33.7 |
| 2680 | `0s0_4s0-5s1__1s0-2s0-3s0-6s1-7s0-8s1` | H3/two | presplit | certified | 263.7 | 39.9 |
| 2724 | `0s0_4s0-5s1__1s1-2s1-3s0-6s0-7s0-8s1` | H3/two | presplit | certified | 444.5 | 51.2 |
| 2768 | `0s0_4s0-6s1__1s0-2s1-3s1-5s1-7s0-8s1` | H3/two | presplit | certified | 414.9 | 56.9 |
| 2812 | `0s0_4s0-7s0__1s0-2s0-3s1-5s0-6s0-8s1` | H3/two | presplit | certified | 71.3 | 28.8 |
| 2856 | `0s0_4s0-7s0__1s1-2s1-3s0-5s1-6s0-8s1` | H3/two | presplit | certified | 68.3 | 27.8 |
| 2900 | `0s0_4s0-7s1__1s1-2s0-3s1-5s0-6s1-8s0` | H3/two | presplit | certified | 342.4 | 56.9 |
| 2944 | `0s0_4s1-5s0__1s0-2s1-3s0-6s1-7s1-8s0` | H3/two | never_ran | certified | 357.7 | 44.6 |
| 2988 | `0s0_4s1-5s1__1s1-2s1-3s1-6s0-7s0-8s1` | H3/two | never_ran | certified | 84.7 | 28.0 |
| 3032 | `0s0_4s1-6s0__1s1-2s0-3s0-5s1-7s0-8s1` | H3/two | presplit | certified | 338.5 | 61.8 |
| 3076 | `0s0_4s1-6s1__1s0-2s1-3s0-5s0-7s0-8s1` | H3/two | presplit | certified | 75.9 | 27.7 |
| 3120 | `0s0_4s1-6s1__1s1-2s1-3s1-5s1-7s0-8s1` | H3/two | presplit | certified | 75.7 | 39.7 |
| 3164 | `0s0_4s1-7s0__1s1-2s0-3s1-5s0-6s0-8s1` | H3/two | presplit | certified | 287.6 | 40.7 |
| 3208 | `0s0_5s0-6s0__1s0-2s1-3s0-4s1-7s0-8s1` | H3/two | presplit | certified | 26.4 | 22.4 |
| 3252 | `0s0_5s0-6s1__1s0-2s0-3s0-4s0-7s0-8s1` | H3/two | presplit | certified | 221.3 | 39.1 |
| 3296 | `0s0_5s0-6s1__1s1-2s0-3s1-4s1-7s0-8s1` | H3/two | presplit | certified | 387.5 | 45.1 |
| 3340 | `0s0_5s1-6s0__1s1-2s1-3s1-4s1-7s0-8s1` | H3/two | timeout300 | certified | 402.5 | 43.2 |
| 3384 | `0s0-1s1_5__2s1-3s0-4s0-6s1-7s0-8s0` | H6(1,1)/one | timeout300 | certified | 212.8 | 37.8 |
| 3428 | `0s0-2s1_4__1s1-3s0-5s0-6s0-7s0-8s0` | H6(2,1)/one | timeout300 | certified | 293.4 | 40.8 |
| 3472 | `0s0-2s1_5__1s0-3s1-4s1-6s0-7s0-8s1` | H6(2,1)/one | timeout300 | certified | 263.1 | 39.8 |
| 3516 | `0s0-2s1_6__1s0-3s0-4s0-5s1-7s0-8s1` | H6(2,1)/one | timeout300 | certified | 219.8 | 39.2 |
| 3560 | `0s0-2s1_6__1s1-3s1-4s0-5s0-7s1-8s1` | H6(2,1)/one | timeout300 | certified | 206.0 | 38.2 |
| 3604 | `0s0-3s1_4__1s1-2s1-5s0-6s1-7s1-8s1` | H6(3,1)/one | never_ran | certified | 242.6 | 38.0 |
| 3648 | `0s0-3s1_5__1s1-2s0-4s0-6s0-7s1-8s1` | H6(3,1)/one | presplit | certified | 219.2 | 35.2 |
| 3692 | `0s0-4s0_6__1s0-2s0-3s1-5s1-7s1-8s1` | H6(4,0)/one | presplit | certified | 48.7 | 30.2 |
| 3736 | `0s0-4s0_6__1s1-2s1-3s1-5s0-7s1-8s1` | H6(4,0)/one | presplit | certified | 42.3 | 22.7 |
| 3780 | `0s0-5s0_6__1s1-2s0-3s0-4s0-7s1-8s0` | H6(5,0)/one | presplit | certified | 76.2 | 31.7 |
| 3824 | `0s0-5s0_7__1s0-2s0-3s1-4s1-6s1-8s0` | H6(5,0)/one | presplit | certified | 74.1 | 34.6 |
| 3868 | `0s0-5s0_7__1s1-2s1-3s1-4s0-6s1-8s0` | H6(5,0)/one | presplit | certified | 91.0 | 45.9 |
| 3912 | `0s0-5s1_1__2s1-3s1-4s0-6s1-7s0-8s0` | H6(5,1)/one | presplit | certified | 169.2 | 32.7 |
| 3956 | `0s0-5s1_2__1s1-3s0-4s0-6s0-7s0-8s0` | H6(5,1)/one | presplit | certified | 260.8 | 41.0 |
| 4000 | `0s0-5s1_6__1s1-2s0-3s1-4s1-7s0-8s1` | H6(5,1)/one | never_ran | certified | 208.0 | 34.8 |
| 4044 | `0s0-5s1_1s1-10s1__2s0-3s1-4s1-6s1-7s1-8s1` | H6(5,1)/two | never_ran | certified | 30.7 | 21.1 |
| 4088 | `0s0-5s1_2s1-3s0__1s1-4s1-6s0-7s0-8s1-9s1` | H6(5,1)/two | never_ran | certified | 31.1 | 32.2 |

## Files

- `units.tsv`: the units of this shard.
- `lane0.sh`, `lane1.sh`, `lane2.sh`: the runners.
- `out.jsonl`: all 93 records, lane 0 then 1 then 2.
- `driver{0,1,2}.log.tail`: the last 100 lines of each driver log.
- `tools.txt` and `env.txt`.

