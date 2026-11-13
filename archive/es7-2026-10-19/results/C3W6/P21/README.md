# C3W6 P21: W6.tsv shard 21 of 44, cap 900

Task `results/C3W6/TASK.md` at c5260b44 with V = P21, LIST = W6.tsv, j = 21, N = 44, H = 4.5. Start 2026-10-25 05:31:29 UTC, END 09:46:29 UTC; lanes started 05:33:48 UTC, and all three finished their units by 08:53:08 UTC, before END.

## Tools and base check

- C3U2 tools: worktree of cad4e050 (`results/C3U2/tools`, unmodified). `compose.py` was not run.
- CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (example: `s VERIFIED UNSAT`), lrat-check 2e3b2dc + E2 patch. Sanity check: LRAT `3 0 0` on {1},{-1} rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da`, matches.
- Details in `tools.txt`. No records were seeded.

## Result

**All 93 units certified at cap 900** (cadical UNSAT, with `c VERIFIED` from lrat-check and `s VERIFIED UNSAT` from cake_lpr). None timed out, so no split records were written. Every unit was reached, and every close_tree run ended with `open_frontier: 0`. There was no SAT, no proof rejection, no checker that came back `none`, and no memory problem (peak use about 6 of 15 GB). No unit ended early without a certificate. The 12 units that solved in under 72 s were all certified. `recheck.jsonl` was not needed.

Solve time of the 93 certified units: min 18.6 s, Q1 117.3, median 336.0, Q3 486.2, p90 567.6, max 691.9 s. **53 of 93 were certified above 300 s.** Total solve 29559 s, total check 4648 s.

### Per stratum

| stratum | units | certified | timed out | not reached | median solve s | max solve s | >300 s |
|---|---|---|---|---|---|---|---|
| H3/two | 76 | 76 | 0 | 0 | 367 | 692 | 45 |
| H6(1,1)/one | 2 | 2 | 0 | 0 | 311 | 317 | 2 |
| H6(2,1)/one | 3 | 3 | 0 | 0 | 321 | 352 | 3 |
| H6(3,1)/one | 3 | 3 | 0 | 0 | 341 | 357 | 3 |
| H6(4,0)/one | 1 | 1 | 0 | 0 | 86 | 86 | 0 |
| H6(5,0)/one | 3 | 3 | 0 | 0 | 64 | 70 | 0 |
| H6(5,1)/one | 3 | 3 | 0 | 0 | 249 | 286 | 0 |
| H6(5,1)/two | 2 | 2 | 0 | 0 | 39 | 47 | 0 |

### Per prior

| prior | units | certified | timed out | not reached | median solve s | max solve s | >300 s |
|---|---|---|---|---|---|---|---|
| presplit | 58 | 58 | 0 | 0 | 212 | 596 | 23 |
| timeout300 | 26 | 26 | 0 | 0 | 454 | 651 | 25 |
| never_ran | 9 | 9 | 0 | 0 | 388 | 692 | 5 |

## Per unit

| row | node | stratum | prior | lane | result | solve s | check s |
|---|---|---|---|---|---|---|---|
| 21 | `0s0_1s0-2s0__3s0-4s0-5s1-6s0-7s0-8s0` | H3/two | presplit | 0 | certified | 57.2 | 56.4 |
| 65 | `0s0_1s0-2s0__3s1-4s1-5s0-6s1-7s0-8s0` | H3/two | presplit | 1 | certified | 55.6 | 53.6 |
| 109 | `0s0_1s0-2s1__3s1-4s0-5s0-6s1-7s1-8s1` | H3/two | timeout300 | 2 | certified | 450.9 | 69.6 |
| 153 | `0s0_1s0-3s1__2s1-4s1-5s0-6s1-7s0-8s0` | H3/two | timeout300 | 0 | certified | 483.0 | 67.4 |
| 197 | `0s0_1s0-4s1__2s1-3s0-5s1-6s1-7s0-8s1` | H3/two | timeout300 | 1 | certified | 514.5 | 78.1 |
| 241 | `0s0_1s0-5s1__2s1-3s1-4s0-6s1-7s1-8s1` | H3/two | timeout300 | 2 | certified | 457.0 | 65.5 |
| 285 | `0s0_1s0-7s0__2s1-3s0-4s1-5s1-6s0-8s1` | H3/two | timeout300 | 0 | certified | 239.1 | 55.9 |
| 329 | `0s0_1s1-2s0__3s0-4s1-5s1-6s0-7s1-8s0` | H3/two | timeout300 | 1 | certified | 428.5 | 62.0 |
| 373 | `0s0_1s1-4s0__2s0-3s1-5s1-6s1-7s1-8s0` | H3/two | timeout300 | 2 | certified | 532.6 | 66.0 |
| 417 | `0s0_1s1-5s0__2s1-3s0-4s1-6s1-7s0-8s1` | H3/two | timeout300 | 0 | certified | 366.1 | 61.3 |
| 461 | `0s0_1s1-5s1__2s0-3s1-4s1-6s0-7s1-8s0` | H3/two | presplit | 1 | certified | 245.9 | 54.9 |
| 505 | `0s0_1s1-7s1__2s0-3s1-4s0-5s1-6s0-8s0` | H3/two | timeout300 | 2 | certified | 372.2 | 63.2 |
| 549 | `0s0_1s1-8s0__2s0-3s0-4s0-5s0-6s1-7s0` | H3/two | presplit | 0 | certified | 120.4 | 49.2 |
| 593 | `0s0_1s1-8s0__2s1-3s0-4s1-5s1-6s1-7s0` | H3/two | presplit | 1 | certified | 153.6 | 45.6 |
| 637 | `0s0_1s1-8s1__2s1-3s1-4s0-5s1-6s1-7s0` | H3/two | timeout300 | 2 | certified | 562.3 | 60.5 |
| 681 | `0s0_1s1-9s1__2s1-3s0-4s1-5s1-6s1-7s1` | H3/two | never_ran | 0 | certified | 691.9 | 70.4 |
| 725 | `0s0_2s0-3s1__1s0-4s1-5s1-6s0-7s1-8s1` | H3/two | presplit | 1 | certified | 487.5 | 61.1 |
| 769 | `0s0_2s0-4s1__1s0-3s0-5s0-6s1-7s1-8s1` | H3/two | presplit | 2 | certified | 377.3 | 55.7 |
| 813 | `0s0_2s0-4s1__1s1-3s1-5s0-6s0-7s1-8s1` | H3/two | presplit | 0 | certified | 545.5 | 60.6 |
| 857 | `0s0_2s0-5s0__1s0-3s1-4s1-6s1-7s1-8s1` | H3/two | presplit | 1 | certified | 100.5 | 41.5 |
| 901 | `0s0_2s0-5s1__1s0-3s1-4s0-6s0-7s1-8s0` | H3/two | timeout300 | 2 | certified | 485.0 | 61.0 |
| 945 | `0s0_2s0-5s1__1s1-3s1-4s1-6s1-7s1-8s0` | H3/two | timeout300 | 0 | certified | 482.6 | 54.7 |
| 989 | `0s0_2s0-6s1__1s1-3s0-4s1-5s1-7s0-8s0` | H3/two | timeout300 | 1 | certified | 355.2 | 51.6 |
| 1033 | `0s0_2s0-7s0__1s0-3s1-4s1-5s0-6s0-8s0` | H3/two | presplit | 2 | certified | 145.6 | 38.9 |
| 1077 | `0s0_2s0-7s1__1s0-3s0-4s0-5s1-6s0-8s0` | H3/two | presplit | 0 | certified | 208.8 | 45.1 |
| 1121 | `0s0_2s0-7s1__1s1-3s1-4s0-5s0-6s0-8s0` | H3/two | presplit | 1 | certified | 338.6 | 50.6 |
| 1165 | `0s0_2s0-8s0__1s1-3s0-4s1-5s1-6s1-7s0` | H3/two | presplit | 2 | certified | 277.7 | 47.8 |
| 1209 | `0s0_2s1-3s0__1s0-4s1-5s1-6s0-7s1-8s1` | H3/two | timeout300 | 0 | certified | 534.8 | 60.2 |
| 1253 | `0s0_2s1-3s1__1s0-4s0-5s0-6s1-7s1-8s1` | H3/two | presplit | 1 | certified | 94.8 | 39.3 |
| 1297 | `0s0_2s1-3s1__1s1-4s1-5s0-6s0-7s1-8s1` | H3/two | presplit | 2 | certified | 81.1 | 58.8 |
| 1341 | `0s0_2s1-4s0__1s1-3s0-5s0-6s1-7s0-8s1` | H3/two | timeout300 | 0 | certified | 651.0 | 61.6 |
| 1385 | `0s0_2s1-5s0__1s0-3s1-4s0-6s0-7s0-8s1` | H3/two | presplit | 1 | certified | 320.3 | 66.6 |
| 1429 | `0s0_2s1-5s0__1s1-3s1-4s1-6s1-7s0-8s1` | H3/two | presplit | 2 | certified | 576.7 | 61.3 |
| 1473 | `0s0_2s1-6s0__1s1-3s0-4s1-5s0-7s0-8s1` | H3/two | presplit | 0 | certified | 528.8 | 59.7 |
| 1517 | `0s0_2s1-6s1__1s0-3s1-4s0-5s1-7s0-8s1` | H3/two | presplit | 1 | certified | 336.0 | 49.9 |
| 1561 | `0s0_2s1-7s0__1s0-3s0-4s0-5s0-6s0-8s1` | H3/two | never_ran | 2 | certified | 192.9 | 41.6 |
| 1605 | `0s0_2s1-7s0__1s1-3s1-4s0-5s1-6s0-8s1` | H3/two | never_ran | 0 | certified | 285.8 | 43.0 |
| 1649 | `0s0_2s1-7s1__1s1-3s1-4s1-5s0-6s1-8s1` | H3/two | never_ran | 1 | certified | 495.1 | 57.9 |
| 1693 | `0s0_2s1-8s1__1s1-3s1-4s0-5s0-6s0-7s0` | H3/two | presplit | 2 | certified | 277.7 | 44.8 |
| 1737 | `0s0_2s1-9s0__1s0-3s1-4s1-5s1-6s0-7s0` | H3/two | presplit | 0 | certified | 113.0 | 36.3 |
| 1781 | `0s0_3s0-4s1__1s0-2s0-5s1-6s0-7s0-8s0` | H3/two | presplit | 1 | certified | 411.9 | 55.1 |
| 1825 | `0s0_3s0-4s1__1s1-2s1-5s0-6s1-7s0-8s0` | H3/two | presplit | 2 | certified | 556.6 | 59.5 |
| 1869 | `0s0_3s0-5s0__1s1-2s0-4s0-6s0-7s0-8s0` | H3/two | presplit | 0 | certified | 46.7 | 24.6 |
| 1913 | `0s0_3s0-5s1__1s0-2s1-4s0-6s1-7s1-8s0` | H3/two | timeout300 | 1 | certified | 613.6 | 59.8 |
| 1957 | `0s0_3s0-6s0__1s0-2s0-4s0-5s0-7s1-8s0` | H3/two | presplit | 2 | certified | 67.0 | 38.6 |
| 2001 | `0s0_3s0-6s0__1s1-2s0-4s1-5s1-7s1-8s0` | H3/two | presplit | 0 | certified | 81.1 | 32.3 |
| 2045 | `0s0_3s0-6s1__1s0-2s1-4s1-5s0-7s1-8s0` | H3/two | timeout300 | 1 | certified | 602.1 | 58.4 |
| 2089 | `0s0_3s0-7s0__1s0-2s0-4s0-5s1-6s1-8s0` | H3/two | presplit | 2 | certified | 73.2 | 32.8 |
| 2133 | `0s0_3s0-7s0__1s1-2s1-4s0-5s0-6s1-8s0` | H3/two | presplit | 0 | certified | 196.3 | 42.2 |
| 2177 | `0s0_3s0-7s1__1s0-2s1-4s1-5s1-6s1-8s0` | H3/two | presplit | 1 | certified | 556.6 | 71.6 |
| 2221 | `0s0_3s0-8s0__1s1-2s0-4s0-5s0-6s0-7s0` | H3/two | presplit | 2 | certified | 176.6 | 38.2 |
| 2265 | `0s0_3s0-8s1__1s1-2s0-4s1-5s0-6s0-7s1` | H3/two | timeout300 | 0 | certified | 359.0 | 49.0 |
| 2309 | `0s0_3s1-4s0__1s0-2s1-5s1-6s1-7s0-8s1` | H3/two | timeout300 | 1 | certified | 607.4 | 57.7 |
| 2353 | `0s0_3s1-4s1__1s0-2s0-5s1-6s0-7s0-8s1` | H3/two | presplit | 2 | certified | 97.9 | 34.5 |
| 2397 | `0s0_3s1-4s1__1s1-2s1-5s0-6s1-7s0-8s1` | H3/two | presplit | 0 | certified | 76.0 | 38.3 |
| 2441 | `0s0_3s1-5s0__1s1-2s0-4s0-6s0-7s0-8s1` | H3/two | presplit | 1 | certified | 367.7 | 72.0 |
| 2485 | `0s0_3s1-5s1__1s0-2s0-4s1-6s1-7s0-8s1` | H3/two | presplit | 2 | certified | 145.7 | 37.4 |
| 2529 | `0s0_3s1-5s1__1s1-2s1-4s1-6s0-7s0-8s1` | H3/two | presplit | 0 | certified | 114.2 | 33.2 |
| 2573 | `0s0_3s1-7s0__1s1-2s1-4s0-5s0-6s1-8s1` | H3/two | never_ran | 1 | certified | 492.0 | 52.0 |
| 2617 | `0s0_3s1-8s0__1s0-2s0-4s0-5s1-6s1-7s0` | H3/two | presplit | 2 | certified | 169.2 | 37.4 |
| 2661 | `0s0_3s1-8s0__1s1-2s1-4s0-5s0-6s1-7s0` | H3/two | presplit | 0 | certified | 341.2 | 46.1 |
| 2705 | `0s0_4s0-5s1__1s0-2s1-3s1-6s1-7s1-8s0` | H3/two | presplit | 1 | certified | 596.3 | 54.0 |
| 2749 | `0s0_4s0-6s1__1s0-2s0-3s1-5s0-7s1-8s0` | H3/two | presplit | 2 | certified | 448.4 | 70.6 |
| 2793 | `0s0_4s0-6s1__1s1-2s1-3s0-5s1-7s1-8s0` | H3/two | presplit | 0 | certified | 508.8 | 55.6 |
| 2837 | `0s0_4s0-7s0__1s1-2s0-3s0-5s0-6s1-8s0` | H3/two | presplit | 1 | certified | 50.5 | 24.8 |
| 2881 | `0s0_4s0-7s1__1s0-2s1-3s0-5s1-6s1-8s1` | H3/two | presplit | 2 | certified | 580.1 | 60.4 |
| 2925 | `0s0_4s1-5s0__1s0-2s0-3s0-6s0-7s1-8s1` | H3/two | never_ran | 0 | certified | 387.7 | 48.8 |
| 2969 | `0s0_4s1-5s0__1s1-2s0-3s1-6s1-7s1-8s1` | H3/two | never_ran | 1 | certified | 493.9 | 51.0 |
| 3013 | `0s0_4s1-6s0__1s0-2s1-3s0-5s0-7s1-8s0` | H3/two | presplit | 2 | certified | 454.8 | 51.4 |
| 3057 | `0s0_4s1-6s0__1s1-2s1-3s1-5s1-7s1-8s0` | H3/two | presplit | 0 | certified | 456.0 | 52.0 |
| 3101 | `0s0_4s1-6s1__1s1-2s0-3s1-5s0-7s1-8s0` | H3/two | presplit | 1 | certified | 102.4 | 34.3 |
| 3145 | `0s0_4s1-7s0__1s0-2s1-3s0-5s1-6s1-8s0` | H3/two | presplit | 2 | certified | 440.9 | 53.3 |
| 3189 | `0s0_5s0-6s0__1s0-2s0-3s0-4s0-7s1-8s0` | H3/two | presplit | 0 | certified | 18.6 | 17.7 |
| 3233 | `0s0_5s0-6s0__1s1-2s0-3s1-4s1-7s1-8s0` | H3/two | presplit | 1 | certified | 47.4 | 25.7 |
| 3277 | `0s0_5s0-6s1__1s0-2s1-3s1-4s0-7s1-8s0` | H3/two | presplit | 2 | certified | 571.2 | 55.1 |
| 3321 | `0s0_5s1-6s0__1s1-2s0-3s1-4s0-7s0-8s1` | H3/two | timeout300 | 0 | certified | 491.9 | 52.8 |
| 3365 | `0s0-1s1_5__2s0-3s0-4s1-6s0-7s0-8s1` | H6(1,1)/one | timeout300 | 1 | certified | 316.9 | 44.9 |
| 3409 | `0s0-1s1_5__2s1-3s1-4s1-6s1-7s0-8s1` | H6(1,1)/one | timeout300 | 2 | certified | 304.5 | 46.5 |
| 3453 | `0s0-2s1_4__1s1-3s1-5s1-6s1-7s0-8s0` | H6(2,1)/one | timeout300 | 0 | certified | 319.9 | 44.3 |
| 3497 | `0s0-2s1_5__1s1-3s1-4s0-6s0-7s1-8s0` | H6(2,1)/one | timeout300 | 1 | certified | 352.5 | 48.2 |
| 3541 | `0s0-2s1_6__1s1-3s0-4s0-5s0-7s0-8s0` | H6(2,1)/one | timeout300 | 2 | certified | 321.2 | 45.6 |
| 3585 | `0s0-3s1_4__1s1-2s0-5s0-6s0-7s0-8s1` | H6(3,1)/one | timeout300 | 0 | certified | 314.5 | 47.2 |
| 3629 | `0s0-3s1_5__1s0-2s1-4s0-6s0-7s0-8s0` | H6(3,1)/one | presplit | 1 | certified | 357.2 | 71.2 |
| 3673 | `0s0-3s1_5__1s1-2s1-4s1-6s1-7s0-8s0` | H6(3,1)/one | presplit | 2 | certified | 341.1 | 58.5 |
| 3717 | `0s0-4s0_6__1s1-2s0-3s1-5s0-7s0-8s0` | H6(4,0)/one | presplit | 0 | certified | 86.2 | 33.7 |
| 3761 | `0s0-5s0_6__1s0-2s0-3s1-4s1-7s1-8s1` | H6(5,0)/one | presplit | 1 | certified | 59.2 | 33.4 |
| 3805 | `0s0-5s0_6__1s1-2s1-3s1-4s0-7s1-8s1` | H6(5,0)/one | presplit | 2 | certified | 63.6 | 32.5 |
| 3849 | `0s0-5s0_7__1s1-2s0-3s0-4s1-6s1-8s1` | H6(5,0)/one | presplit | 0 | certified | 69.8 | 38.9 |
| 3893 | `0s0-5s1_1__2s1-3s0-4s0-6s0-7s0-8s1` | H6(5,1)/one | presplit | 1 | certified | 285.9 | 48.4 |
| 3937 | `0s0-5s1_2__1s0-3s0-4s1-6s1-7s0-8s1` | H6(5,1)/one | presplit | 2 | certified | 215.8 | 43.5 |
| 3981 | `0s0-5s1_2__1s1-3s1-4s1-6s0-7s0-8s1` | H6(5,1)/one | presplit | 0 | certified | 248.6 | 43.0 |
| 4025 | `0s0-5s1_1s1-10s1__2s0-3s0-4s1-6s1-7s0-8s0` | H6(5,1)/two | never_ran | 1 | certified | 31.2 | 30.7 |
| 4069 | `0s0-5s1_1s1-10s1__2s1-3s1-4s1-6s0-7s0-8s0` | H6(5,1)/two | never_ran | 2 | certified | 47.4 | 30.1 |

Files: `units.tsv`, `lane0.sh`–`lane2.sh`, `out.jsonl` (93 records: lane 0, then 1, then 2), `driver{0,1,2}.log.tail`, `tools.txt`, `env.txt`.
