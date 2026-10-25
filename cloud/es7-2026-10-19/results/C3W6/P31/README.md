# C3W6 P31: shard 31 of 44 of W6.tsv, 93 σ-cubes at cap 900

All 93 units were certified (CaDiCaL UNSAT, then both lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`). No unit timed out, none was left unreached, there was no SAT answer, no proof was rejected, nothing needed a re-check, and there were no memory problems (the most used in the `free` samples was 6 of 15 GB). The out file holds 93 solve records and no split records. compose.py was not run.

## Setup

- Task: `results/C3W6/TASK.md` at c5260b44. V = P31, LIST = W6.tsv, j = 31, N = 44, H = 4.5.
- Tools: C3U2 tools from the worktree of cad4e050 (cad4e050d778aa37c9ea23afcbe704c94db3e890), used unmodified. CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (its example gives `s VERIFIED UNSAT`), and lrat-check 2e3b2dc with the E2 patch. Sanity test: `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both. Details are in `tools.txt`.
- Base CNF: `gen_case.py 11 7 none` gives `p cnf 168399 4154921`, with sha256 `bf0e502e…0dd6da` (matches).
- Units: the rows with row ≡ 31 (mod 44), 93 units in `units.tsv`. Nothing was seeded. There were 3 lanes (`lane0.sh` to `lane2.sh`), each with `--jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`. `killer.sh` was the END guard; it was not needed and was stopped after the lanes finished.
- Times: start 05:31:34 UTC, END 09:46:34 UTC. Lanes 0, 2 and 1 finished at 08:23, 08:30 and 08:42 UTC.

## Totals

Total solve time 7.45 h and check time 1.27 h.

| stratum | units | certified |
|---|---|---|
| H3/two | 76 | 76 |
| H6(1,1)/one | 1 | 1 |
| H6(2,1)/one | 4 | 4 |
| H6(3,1)/one | 2 | 2 |
| H6(4,0)/one | 2 | 2 |
| H6(5,0)/one | 3 | 3 |
| H6(5,1)/one | 3 | 3 |
| H6(5,1)/two | 2 | 2 |

| prior | units | certified |
|---|---|---|
| never_ran | 11 | 11 |
| presplit | 57 | 57 |
| timeout300 | 25 | 25 |

Solve times of the certified units (s): min 34.3, Q1 98.4, median 318.8, Q3 433.4, p90 520.7, max 628.0. 50 of 93 were certified above 300 s (so they would have timed out at the earlier cap of 300), and none took more than 628.0 s. 14 units finished in under 72 s, all with a certificate, so no unit ended early without one.

## Per unit

| row | node | stratum | prior | lane | result | solve s | check s |
|---|---|---|---|---|---|---|---|
| 31 | `0s0_1s0-2s0__3s0-4s1-5s0-6s0-7s1-8s0` | H3/two | presplit | 0 | certified | 44.1 | 44.7 |
| 75 | `0s0_1s0-2s0__3s1-4s1-5s1-6s1-7s1-8s0` | H3/two | presplit | 1 | certified | 71.4 | 43.9 |
| 119 | `0s0_1s0-2s1__3s1-4s1-5s0-6s0-7s0-8s1` | H3/two | timeout300 | 2 | certified | 446.1 | 73.8 |
| 163 | `0s0_1s0-4s1__2s0-3s0-5s0-6s1-7s1-8s0` | H3/two | timeout300 | 0 | certified | 357.7 | 75.2 |
| 207 | `0s0_1s0-4s1__2s1-3s1-5s0-6s1-7s1-8s1` | H3/two | timeout300 | 1 | certified | 446.9 | 63.2 |
| 251 | `0s0_1s0-6s1__2s1-3s1-4s1-5s1-7s1-8s0` | H3/two | timeout300 | 2 | certified | 444.4 | 68.9 |
| 295 | `0s0_1s0-7s0__2s1-3s1-4s1-5s0-6s0-8s0` | H3/two | timeout300 | 0 | certified | 204.0 | 49.8 |
| 339 | `0s0_1s1-2s0__3s1-4s0-5s0-6s1-7s0-8s0` | H3/two | timeout300 | 1 | certified | 425.5 | 62.6 |
| 383 | `0s0_1s1-4s0__2s1-3s1-5s0-6s1-7s0-8s1` | H3/two | timeout300 | 2 | certified | 482.2 | 61.0 |
| 427 | `0s0_1s1-5s0__2s1-3s1-4s1-6s0-7s0-8s0` | H3/two | timeout300 | 0 | certified | 389.0 | 64.1 |
| 471 | `0s0_1s1-5s1__2s1-3s0-4s0-6s1-7s0-8s0` | H3/two | presplit | 1 | certified | 150.1 | 47.2 |
| 515 | `0s0_1s1-7s1__2s0-3s1-4s1-5s1-6s1-8s0` | H3/two | timeout300 | 2 | certified | 616.2 | 58.6 |
| 559 | `0s0_1s1-8s0__2s0-3s0-4s1-5s1-6s0-7s0` | H3/two | presplit | 0 | certified | 98.4 | 43.8 |
| 603 | `0s0_1s1-8s0__2s1-3s1-4s1-5s0-6s0-7s0` | H3/two | presplit | 1 | certified | 81.5 | 38.4 |
| 647 | `0s0_1s1-9s1__2s0-3s0-4s0-5s1-6s1-7s1` | H3/two | never_ran | 2 | certified | 442.5 | 51.3 |
| 691 | `0s0_1s1-9s1__2s1-3s1-4s1-5s0-6s0-7s1` | H3/two | never_ran | 0 | certified | 486.0 | 62.0 |
| 735 | `0s0_2s0-3s1__1s1-4s0-5s0-6s1-7s0-8s1` | H3/two | presplit | 1 | certified | 575.3 | 66.0 |
| 779 | `0s0_2s0-4s1__1s0-3s1-5s0-6s0-7s0-8s1` | H3/two | presplit | 2 | certified | 383.4 | 52.8 |
| 823 | `0s0_2s0-4s1__1s1-3s1-5s1-6s1-7s0-8s1` | H3/two | presplit | 0 | certified | 586.7 | 59.3 |
| 867 | `0s0_2s0-5s0__1s1-3s0-4s1-6s0-7s0-8s1` | H3/two | presplit | 1 | certified | 93.0 | 38.8 |
| 911 | `0s0_2s0-5s1__1s0-3s1-4s1-6s1-7s0-8s0` | H3/two | timeout300 | 2 | certified | 473.6 | 79.0 |
| 955 | `0s0_2s0-6s1__1s0-3s0-4s1-5s0-7s1-8s0` | H3/two | timeout300 | 0 | certified | 400.5 | 55.6 |
| 999 | `0s0_2s0-6s1__1s1-3s1-4s0-5s1-7s1-8s0` | H3/two | timeout300 | 1 | certified | 397.4 | 54.5 |
| 1043 | `0s0_2s0-7s0__1s1-3s0-4s0-5s0-6s1-8s0` | H3/two | presplit | 2 | certified | 188.2 | 64.8 |
| 1087 | `0s0_2s0-7s1__1s0-3s0-4s1-5s1-6s1-8s0` | H3/two | presplit | 0 | certified | 305.3 | 48.9 |
| 1131 | `0s0_2s0-7s1__1s1-3s1-4s1-5s0-6s1-8s0` | H3/two | presplit | 1 | certified | 328.4 | 64.2 |
| 1175 | `0s0_2s0-8s0__1s1-3s1-4s1-5s0-6s0-7s0` | H3/two | presplit | 2 | certified | 199.4 | 45.9 |
| 1219 | `0s0_2s1-3s0__1s1-4s0-5s0-6s1-7s0-8s1` | H3/two | timeout300 | 0 | certified | 529.5 | 56.6 |
| 1263 | `0s0_2s1-3s1__1s0-4s1-5s0-6s0-7s0-8s1` | H3/two | presplit | 1 | certified | 80.3 | 57.1 |
| 1307 | `0s0_2s1-3s1__1s1-4s1-5s1-6s1-7s0-8s1` | H3/two | presplit | 2 | certified | 74.3 | 39.6 |
| 1351 | `0s0_2s1-4s0__1s1-3s0-5s1-6s1-7s1-8s1` | H3/two | timeout300 | 0 | certified | 565.1 | 73.5 |
| 1395 | `0s0_2s1-5s0__1s0-3s1-4s1-6s0-7s1-8s1` | H3/two | presplit | 1 | certified | 458.1 | 59.9 |
| 1439 | `0s0_2s1-6s0__1s0-3s0-4s0-5s1-7s1-8s1` | H3/two | presplit | 2 | certified | 323.2 | 42.8 |
| 1483 | `0s0_2s1-6s0__1s1-3s1-4s0-5s0-7s1-8s1` | H3/two | presplit | 0 | certified | 355.1 | 46.2 |
| 1527 | `0s0_2s1-6s1__1s0-3s1-4s1-5s1-7s1-8s1` | H3/two | presplit | 1 | certified | 318.1 | 44.9 |
| 1571 | `0s0_2s1-7s0__1s0-3s1-4s0-5s0-6s1-8s1` | H3/two | never_ran | 2 | certified | 189.8 | 42.4 |
| 1615 | `0s0_2s1-7s0__1s1-3s1-4s1-5s1-6s1-8s1` | H3/two | never_ran | 0 | certified | 318.8 | 51.6 |
| 1659 | `0s0_2s1-8s1__1s0-3s0-4s1-5s1-6s1-7s0` | H3/two | presplit | 1 | certified | 433.4 | 54.5 |
| 1703 | `0s0_2s1-8s1__1s1-3s1-4s1-5s0-6s1-7s0` | H3/two | presplit | 2 | certified | 466.8 | 68.7 |
| 1747 | `0s0_2s1-9s0__1s1-3s0-4s0-5s1-6s1-7s0` | H3/two | presplit | 0 | certified | 138.2 | 40.0 |
| 1791 | `0s0_3s0-4s1__1s0-2s1-5s0-6s0-7s1-8s0` | H3/two | presplit | 1 | certified | 423.4 | 58.7 |
| 1835 | `0s0_3s0-4s1__1s1-2s1-5s1-6s1-7s1-8s0` | H3/two | presplit | 2 | certified | 516.8 | 55.9 |
| 1879 | `0s0_3s0-5s0__1s1-2s0-4s1-6s0-7s1-8s0` | H3/two | presplit | 0 | certified | 54.2 | 29.5 |
| 1923 | `0s0_3s0-5s1__1s1-2s0-4s0-6s0-7s0-8s0` | H3/two | timeout300 | 1 | certified | 368.7 | 51.8 |
| 1967 | `0s0_3s0-6s0__1s0-2s0-4s1-5s1-7s0-8s0` | H3/two | presplit | 2 | certified | 45.5 | 25.0 |
| 2011 | `0s0_3s0-6s0__1s1-2s1-4s1-5s0-7s0-8s0` | H3/two | presplit | 0 | certified | 119.5 | 36.7 |
| 2055 | `0s0_3s0-6s1__1s1-2s0-4s0-5s1-7s0-8s0` | H3/two | timeout300 | 1 | certified | 412.1 | 47.1 |
| 2099 | `0s0_3s0-7s0__1s0-2s1-4s0-5s0-6s0-8s0` | H3/two | presplit | 2 | certified | 112.3 | 34.6 |
| 2143 | `0s0_3s0-7s0__1s1-2s1-4s1-5s1-6s0-8s0` | H3/two | presplit | 0 | certified | 147.1 | 34.9 |
| 2187 | `0s0_3s0-7s1__1s1-2s0-4s1-5s0-6s0-8s0` | H3/two | presplit | 1 | certified | 427.9 | 62.3 |
| 2231 | `0s0_3s0-8s0__1s1-2s0-4s1-5s0-6s1-7s0` | H3/two | presplit | 2 | certified | 166.8 | 37.2 |
| 2275 | `0s0_3s0-8s1__1s1-2s1-4s1-5s0-6s0-7s1` | H3/two | timeout300 | 0 | certified | 373.6 | 61.9 |
| 2319 | `0s0_3s1-4s0__1s1-2s0-5s0-6s1-7s1-8s1` | H3/two | timeout300 | 1 | certified | 580.6 | 56.8 |
| 2363 | `0s0_3s1-4s1__1s0-2s1-5s0-6s0-7s1-8s1` | H3/two | presplit | 2 | certified | 80.2 | 31.6 |
| 2407 | `0s0_3s1-4s1__1s1-2s1-5s1-6s1-7s1-8s1` | H3/two | presplit | 0 | certified | 63.9 | 25.7 |
| 2451 | `0s0_3s1-5s0__1s1-2s0-4s1-6s0-7s1-8s1` | H3/two | presplit | 1 | certified | 628.0 | 81.1 |
| 2495 | `0s0_3s1-5s1__1s0-2s1-4s0-6s1-7s1-8s1` | H3/two | presplit | 2 | certified | 81.8 | 31.0 |
| 2539 | `0s0_3s1-6s0__1s1-2s1-4s0-5s1-7s1-8s1` | H3/two | timeout300 | 0 | certified | 523.7 | 61.2 |
| 2583 | `0s0_3s1-7s0__1s1-2s1-4s1-5s1-6s0-8s1` | H3/two | never_ran | 1 | certified | 458.0 | 49.9 |
| 2627 | `0s0_3s1-8s0__1s0-2s1-4s0-5s0-6s0-7s0` | H3/two | presplit | 2 | certified | 183.7 | 40.8 |
| 2671 | `0s0_3s1-8s0__1s1-2s1-4s1-5s1-6s0-7s0` | H3/two | presplit | 0 | certified | 223.4 | 53.1 |
| 2715 | `0s0_4s0-5s1__1s1-2s0-3s1-6s0-7s0-8s0` | H3/two | presplit | 1 | certified | 390.7 | 54.5 |
| 2759 | `0s0_4s0-6s1__1s0-2s1-3s0-5s1-7s0-8s0` | H3/two | presplit | 2 | certified | 360.2 | 46.8 |
| 2803 | `0s0_4s0-7s0__1s0-2s0-3s0-5s0-6s0-8s0` | H3/two | presplit | 0 | certified | 40.4 | 24.2 |
| 2847 | `0s0_4s0-7s0__1s1-2s0-3s1-5s1-6s0-8s0` | H3/two | presplit | 1 | certified | 82.1 | 35.9 |
| 2891 | `0s0_4s0-7s1__1s1-2s0-3s0-5s0-6s0-8s1` | H3/two | presplit | 2 | certified | 334.0 | 47.5 |
| 2935 | `0s0_4s1-5s0__1s0-2s0-3s1-6s1-7s0-8s1` | H3/two | never_ran | 0 | certified | 443.9 | 56.2 |
| 2979 | `0s0_4s1-5s0__1s1-2s1-3s1-6s0-7s0-8s1` | H3/two | never_ran | 1 | certified | 521.7 | 58.6 |
| 3023 | `0s0_4s1-6s0__1s0-2s1-3s1-5s1-7s0-8s0` | H3/two | presplit | 2 | certified | 524.3 | 60.6 |
| 3067 | `0s0_4s1-6s1__1s0-2s0-3s1-5s0-7s0-8s0` | H3/two | presplit | 0 | certified | 94.2 | 32.2 |
| 3111 | `0s0_4s1-6s1__1s1-2s1-3s0-5s1-7s0-8s0` | H3/two | presplit | 1 | certified | 127.8 | 37.5 |
| 3155 | `0s0_4s1-7s0__1s1-2s0-3s0-5s0-6s0-8s0` | H3/two | presplit | 2 | certified | 266.4 | 46.4 |
| 3199 | `0s0_5s0-6s0__1s0-2s0-3s1-4s1-7s0-8s0` | H3/two | presplit | 0 | certified | 34.3 | 23.3 |
| 3243 | `0s0_5s0-6s0__1s1-2s1-3s1-4s0-7s0-8s0` | H3/two | presplit | 1 | certified | 42.2 | 24.8 |
| 3287 | `0s0_5s0-6s1__1s1-2s0-3s0-4s1-7s0-8s0` | H3/two | presplit | 2 | certified | 428.8 | 50.7 |
| 3331 | `0s0_5s1-6s0__1s1-2s1-3s0-4s1-7s0-8s0` | H3/two | timeout300 | 0 | certified | 488.8 | 56.3 |
| 3375 | `0s0-1s1_5__2s0-3s1-4s1-6s0-7s1-8s1` | H6(1,1)/one | timeout300 | 1 | certified | 263.6 | 45.6 |
| 3419 | `0s0-2s1_3__1s1-4s1-5s0-6s0-7s0-8s1` | H6(2,1)/one | timeout300 | 2 | certified | 358.4 | 49.3 |
| 3463 | `0s0-2s1_5__1s0-3s0-4s0-6s1-7s1-8s1` | H6(2,1)/one | timeout300 | 0 | certified | 250.2 | 43.2 |
| 3507 | `0s0-2s1_5__1s1-3s1-4s1-6s1-7s0-8s0` | H6(2,1)/one | timeout300 | 1 | certified | 343.6 | 47.8 |
| 3551 | `0s0-2s1_6__1s1-3s0-4s1-5s0-7s1-8s0` | H6(2,1)/one | timeout300 | 2 | certified | 300.2 | 44.2 |
| 3595 | `0s0-3s1_4__1s1-2s0-5s1-6s1-7s1-8s0` | H6(3,1)/one | never_ran | 0 | certified | 396.6 | 77.4 |
| 3639 | `0s0-3s1_5__1s0-2s1-4s1-6s0-7s1-8s0` | H6(3,1)/one | presplit | 1 | certified | 320.3 | 45.4 |
| 3683 | `0s0-4s0_6__1s0-2s0-3s0-5s1-7s1-8s0` | H6(4,0)/one | presplit | 2 | certified | 61.2 | 48.8 |
| 3727 | `0s0-4s0_6__1s1-2s1-3s0-5s0-7s1-8s0` | H6(4,0)/one | presplit | 0 | certified | 67.9 | 35.7 |
| 3771 | `0s0-5s0_6__1s0-2s1-3s1-4s0-7s0-8s1` | H6(5,0)/one | presplit | 1 | certified | 64.7 | 33.6 |
| 3815 | `0s0-5s0_7__1s0-2s0-3s0-4s1-6s0-8s1` | H6(5,0)/one | presplit | 2 | certified | 45.5 | 32.5 |
| 3859 | `0s0-5s0_7__1s1-2s1-3s0-4s0-6s0-8s1` | H6(5,0)/one | presplit | 0 | certified | 85.4 | 44.5 |
| 3903 | `0s0-5s1_1__2s1-3s0-4s1-6s0-7s1-8s1` | H6(5,1)/one | presplit | 1 | certified | 166.0 | 38.4 |
| 3947 | `0s0-5s1_2__1s0-3s1-4s0-6s1-7s1-8s1` | H6(5,1)/one | presplit | 2 | certified | 204.0 | 41.1 |
| 3991 | `0s0-5s1_6__1s1-2s0-3s0-4s1-7s0-8s0` | H6(5,1)/one | never_ran | 0 | certified | 266.2 | 48.8 |
| 4035 | `0s0-5s1_1s1-10s1__2s0-3s1-4s0-6s1-7s1-8s0` | H6(5,1)/two | never_ran | 1 | certified | 56.9 | 32.6 |
| 4079 | `0s0-5s1_2s1-3s0__1s1-4s0-6s0-7s0-8s1-9s0` | H6(5,1)/two | never_ran | 2 | certified | 43.9 | 30.5 |
