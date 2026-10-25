# C3W6 P33: shard 33 of 44 of W6.tsv, 3 lanes, cap 900

Task `results/C3W6/TASK.md` at c5260b44 (V = P33, LIST = W6.tsv, j = 33, N = 44, H = 4.5). Start 05:31:46 UTC, lanes 05:34:34–07:57:15 UTC, END would have been 09:46:46 UTC.

## Tools and base check

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, used unmodified; `compose.py` not run
- CaDiCaL c60730422e758ef1cebe7aeddf2dda31c996bf04 (3.0.1); cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (example: `s VERIFIED UNSAT`); lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 + E2 patch
- Checker sanity test passed: `3 0 0` rejected by both, `3 0 1 2 0` accepted by both
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches). Details in `tools.txt`.

## Result

All 93 units **certified** at cap 900 (both checkers: `c VERIFIED` / `s VERIFIED UNSAT`). Nothing timed out, no split records, every unit reached. No SAT, no proof rejection, no `none` checker result, no memory problem (available memory at least 7 GB of 15 GB in every ~10-minute sample), and no unit ended early without a certificate. `recheck.jsonl` was not needed.

## Totals per stratum and prior

| stratum | prior | units | certified | timed out | not reached |
|---|---|---|---|---|---|
| H3/two | never_ran | 6 | 6 | 0 | 0 |
| H3/two | presplit | 48 | 48 | 0 | 0 |
| H3/two | timeout300 | 22 | 22 | 0 | 0 |
| H6(1,1)/one | timeout300 | 1 | 1 | 0 | 0 |
| H6(2,1)/one | timeout300 | 4 | 4 | 0 | 0 |
| H6(3,1)/one | never_ran | 1 | 1 | 0 | 0 |
| H6(3,1)/one | presplit | 1 | 1 | 0 | 0 |
| H6(4,0)/one | presplit | 2 | 2 | 0 | 0 |
| H6(5,0)/one | presplit | 3 | 3 | 0 | 0 |
| H6(5,1)/one | never_ran | 1 | 1 | 0 | 0 |
| H6(5,1)/one | presplit | 2 | 2 | 0 | 0 |
| H6(5,1)/two | never_ran | 2 | 2 | 0 | 0 |
| **all** | | 93 | 93 | 0 | 0 |

## Solve times of the certified units (s)

min 16.8, Q1 83.0, median 235.0, Q3 304.0, p90 379.3, max 441.1; 27 certified above 300 s. Total solve 19257 s, check 4318 s (3 lanes on 4 cores, so per-unit times are somewhat inflated).

## Per unit

| row | node | stratum | prior | lane | result | solve s | check s |
|---|---|---|---|---|---|---|---|
| 33 | `0s0_1s0-2s0__3s0-4s1-5s0-6s1-7s0-8s0` | H3/two | presplit | 0 | certified | 44.0 | 46.5 |
| 77 | `0s0_1s0-2s1__3s0-4s0-5s0-6s1-7s1-8s1` | H3/two | timeout300 | 1 | certified | 300.7 | 65.8 |
| 121 | `0s0_1s0-2s1__3s1-4s1-5s0-6s0-7s1-8s1` | H3/two | timeout300 | 2 | certified | 355.6 | 51.2 |
| 165 | `0s0_1s0-4s1__2s0-3s0-5s1-6s0-7s0-8s1` | H3/two | timeout300 | 0 | certified | 277.7 | 71.2 |
| 209 | `0s0_1s0-4s1__2s1-3s1-5s1-6s0-7s0-8s1` | H3/two | timeout300 | 1 | certified | 357.9 | 65.2 |
| 253 | `0s0_1s0-7s0__2s0-3s0-4s0-5s0-6s1-8s0` | H3/two | timeout300 | 2 | certified | 115.8 | 53.2 |
| 297 | `0s0_1s0-7s0__2s1-3s1-4s1-5s0-6s1-8s1` | H3/two | timeout300 | 0 | certified | 107.5 | 51.6 |
| 341 | `0s0_1s1-2s0__3s1-4s0-5s0-6s1-7s1-8s0` | H3/two | timeout300 | 1 | certified | 321.3 | 67.3 |
| 385 | `0s0_1s1-4s0__2s1-3s1-5s1-6s0-7s0-8s0` | H3/two | timeout300 | 2 | certified | 280.8 | 62.5 |
| 429 | `0s0_1s1-5s0__2s1-3s1-4s1-6s0-7s1-8s0` | H3/two | timeout300 | 0 | certified | 278.1 | 67.2 |
| 473 | `0s0_1s1-5s1__2s1-3s0-4s0-6s1-7s1-8s0` | H3/two | presplit | 1 | certified | 109.0 | 45.0 |
| 517 | `0s0_1s1-7s1__2s1-3s0-4s0-5s0-6s1-8s0` | H3/two | timeout300 | 2 | certified | 231.0 | 58.0 |
| 561 | `0s0_1s1-8s0__2s0-3s0-4s1-5s1-6s1-7s0` | H3/two | presplit | 0 | certified | 93.7 | 47.1 |
| 605 | `0s0_1s1-8s0__2s1-3s1-4s1-5s0-6s1-7s0` | H3/two | presplit | 1 | certified | 67.3 | 42.6 |
| 649 | `0s0_1s1-9s1__2s0-3s0-4s1-5s0-6s1-7s0` | H3/two | never_ran | 2 | certified | 280.3 | 54.5 |
| 693 | `0s0_1s1-9s1__2s1-3s1-4s1-5s0-6s1-7s1` | H3/two | never_ran | 0 | certified | 404.4 | 74.0 |
| 737 | `0s0_2s0-3s1__1s1-4s0-5s0-6s1-7s1-8s1` | H3/two | presplit | 1 | certified | 382.6 | 72.7 |
| 781 | `0s0_2s0-4s1__1s0-3s1-5s0-6s0-7s1-8s1` | H3/two | presplit | 2 | certified | 384.3 | 61.9 |
| 825 | `0s0_2s0-4s1__1s1-3s1-5s1-6s1-7s1-8s1` | H3/two | presplit | 0 | certified | 262.6 | 54.9 |
| 869 | `0s0_2s0-5s0__1s1-3s0-4s1-6s0-7s1-8s1` | H3/two | presplit | 1 | certified | 63.5 | 51.4 |
| 913 | `0s0_2s0-5s1__1s0-3s1-4s1-6s1-7s1-8s0` | H3/two | timeout300 | 2 | certified | 399.7 | 67.9 |
| 957 | `0s0_2s0-6s1__1s0-3s0-4s1-5s1-7s0-8s0` | H3/two | timeout300 | 0 | certified | 235.0 | 44.9 |
| 1001 | `0s0_2s0-6s1__1s1-3s1-4s1-5s0-7s0-8s0` | H3/two | timeout300 | 1 | certified | 271.4 | 49.2 |
| 1045 | `0s0_2s0-7s0__1s1-3s0-4s0-5s1-6s0-8s0` | H3/two | presplit | 2 | certified | 117.1 | 46.1 |
| 1089 | `0s0_2s0-7s1__1s0-3s1-4s0-5s0-6s0-8s0` | H3/two | presplit | 0 | certified | 213.1 | 41.7 |
| 1133 | `0s0_2s0-7s1__1s1-3s1-4s1-5s1-6s0-8s0` | H3/two | presplit | 1 | certified | 238.4 | 53.5 |
| 1177 | `0s0_2s0-8s0__1s1-3s1-4s1-5s0-6s1-7s0` | H3/two | presplit | 2 | certified | 170.9 | 55.9 |
| 1221 | `0s0_2s1-3s0__1s1-4s0-5s0-6s1-7s1-8s1` | H3/two | timeout300 | 0 | certified | 348.6 | 55.5 |
| 1265 | `0s0_2s1-3s1__1s0-4s1-5s0-6s0-7s1-8s1` | H3/two | presplit | 1 | certified | 66.1 | 33.8 |
| 1309 | `0s0_2s1-3s1__1s1-4s1-5s1-6s1-7s1-8s1` | H3/two | presplit | 2 | certified | 53.0 | 35.0 |
| 1353 | `0s0_2s1-4s0__1s1-3s1-5s0-6s0-7s0-8s1` | H3/two | timeout300 | 0 | certified | 361.3 | 49.4 |
| 1397 | `0s0_2s1-5s0__1s0-3s1-4s1-6s1-7s0-8s1` | H3/two | presplit | 1 | certified | 318.9 | 48.5 |
| 1441 | `0s0_2s1-6s0__1s0-3s0-4s1-5s0-7s0-8s1` | H3/two | presplit | 2 | certified | 192.5 | 40.9 |
| 1485 | `0s0_2s1-6s0__1s1-3s1-4s0-5s1-7s0-8s1` | H3/two | presplit | 0 | certified | 298.4 | 49.9 |
| 1529 | `0s0_2s1-6s1__1s1-3s0-4s0-5s0-7s0-8s1` | H3/two | presplit | 1 | certified | 120.6 | 40.9 |
| 1573 | `0s0_2s1-7s0__1s0-3s1-4s0-5s1-6s0-8s1` | H3/two | never_ran | 2 | certified | 133.5 | 37.6 |
| 1617 | `0s0_2s1-7s1__1s0-3s1-4s1-5s0-6s1-8s1` | H3/two | timeout300 | 0 | certified | 304.0 | 51.3 |
| 1661 | `0s0_2s1-8s1__1s0-3s1-4s0-5s0-6s0-7s0` | H3/two | presplit | 1 | certified | 162.6 | 37.2 |
| 1705 | `0s0_2s1-8s1__1s1-3s1-4s1-5s1-6s0-7s0` | H3/two | presplit | 2 | certified | 250.8 | 44.9 |
| 1749 | `0s0_2s1-9s0__1s1-3s0-4s1-5s0-6s0-7s0` | H3/two | presplit | 0 | certified | 83.0 | 35.7 |
| 1793 | `0s0_3s0-4s1__1s0-2s1-5s0-6s1-7s0-8s0` | H3/two | presplit | 1 | certified | 309.8 | 48.0 |
| 1837 | `0s0_3s0-5s0__1s0-2s0-4s0-6s0-7s0-8s0` | H3/two | presplit | 2 | certified | 16.8 | 20.0 |
| 1881 | `0s0_3s0-5s0__1s1-2s0-4s1-6s1-7s0-8s0` | H3/two | presplit | 0 | certified | 36.3 | 22.6 |
| 1925 | `0s0_3s0-5s1__1s1-2s0-4s0-6s0-7s1-8s0` | H3/two | timeout300 | 1 | certified | 315.0 | 49.3 |
| 1969 | `0s0_3s0-6s0__1s0-2s0-4s1-5s1-7s1-8s0` | H3/two | presplit | 2 | certified | 44.5 | 31.7 |
| 2013 | `0s0_3s0-6s0__1s1-2s1-4s1-5s0-7s1-8s0` | H3/two | presplit | 0 | certified | 85.7 | 33.9 |
| 2057 | `0s0_3s0-6s1__1s1-2s0-4s0-5s1-7s1-8s0` | H3/two | timeout300 | 1 | certified | 332.6 | 51.9 |
| 2101 | `0s0_3s0-7s0__1s0-2s1-4s0-5s0-6s1-8s0` | H3/two | presplit | 2 | certified | 84.7 | 35.9 |
| 2145 | `0s0_3s0-7s0__1s1-2s1-4s1-5s1-6s1-8s0` | H3/two | presplit | 0 | certified | 93.2 | 35.7 |
| 2189 | `0s0_3s0-7s1__1s1-2s0-4s1-5s0-6s1-8s0` | H3/two | presplit | 1 | certified | 320.5 | 46.5 |
| 2233 | `0s0_3s0-8s0__1s1-2s0-4s1-5s1-6s0-7s0` | H3/two | presplit | 2 | certified | 93.9 | 32.7 |
| 2277 | `0s0_3s0-8s1__1s1-2s1-4s1-5s1-6s0-7s0` | H3/two | timeout300 | 0 | certified | 236.6 | 43.2 |
| 2321 | `0s0_3s1-4s0__1s1-2s0-5s1-6s0-7s0-8s1` | H3/two | timeout300 | 1 | certified | 366.1 | 55.9 |
| 2365 | `0s0_3s1-4s1__1s0-2s1-5s0-6s1-7s0-8s1` | H3/two | presplit | 2 | certified | 44.2 | 28.2 |
| 2409 | `0s0_3s1-5s0__1s0-2s0-4s0-6s0-7s0-8s1` | H3/two | presplit | 0 | certified | 194.6 | 41.9 |
| 2453 | `0s0_3s1-5s0__1s1-2s0-4s1-6s1-7s0-8s1` | H3/two | presplit | 1 | certified | 420.2 | 58.7 |
| 2497 | `0s0_3s1-5s1__1s0-2s1-4s1-6s0-7s0-8s1` | H3/two | presplit | 2 | certified | 64.1 | 47.7 |
| 2541 | `0s0_3s1-6s0__1s1-2s1-4s1-5s0-7s1-8s1` | H3/two | timeout300 | 0 | certified | 343.6 | 49.1 |
| 2585 | `0s0_3s1-7s0__1s1-2s1-4s1-5s1-6s1-8s1` | H3/two | never_ran | 1 | certified | 249.1 | 41.9 |
| 2629 | `0s0_3s1-8s0__1s0-2s1-4s0-5s0-6s1-7s0` | H3/two | presplit | 2 | certified | 154.5 | 53.2 |
| 2673 | `0s0_3s1-8s0__1s1-2s1-4s1-5s1-6s1-7s0` | H3/two | presplit | 0 | certified | 176.0 | 42.1 |
| 2717 | `0s0_4s0-5s1__1s1-2s0-3s1-6s0-7s1-8s0` | H3/two | presplit | 1 | certified | 416.4 | 54.9 |
| 2761 | `0s0_4s0-6s1__1s0-2s1-3s0-5s1-7s1-8s0` | H3/two | presplit | 2 | certified | 356.1 | 55.4 |
| 2805 | `0s0_4s0-7s0__1s0-2s0-3s0-5s0-6s1-8s0` | H3/two | presplit | 0 | certified | 26.5 | 26.3 |
| 2849 | `0s0_4s0-7s0__1s1-2s0-3s1-5s1-6s1-8s0` | H3/two | presplit | 1 | certified | 58.6 | 31.3 |
| 2893 | `0s0_4s0-7s1__1s1-2s0-3s0-5s0-6s1-8s1` | H3/two | presplit | 2 | certified | 298.5 | 48.6 |
| 2937 | `0s0_4s1-5s0__1s0-2s0-3s1-6s1-7s1-8s1` | H3/two | never_ran | 0 | certified | 281.0 | 46.5 |
| 2981 | `0s0_4s1-5s0__1s1-2s1-3s1-6s0-7s1-8s1` | H3/two | never_ran | 1 | certified | 405.9 | 51.6 |
| 3025 | `0s0_4s1-6s0__1s0-2s1-3s1-5s1-7s1-8s0` | H3/two | presplit | 2 | certified | 412.1 | 59.1 |
| 3069 | `0s0_4s1-6s1__1s0-2s0-3s1-5s0-7s1-8s0` | H3/two | presplit | 0 | certified | 65.2 | 48.3 |
| 3113 | `0s0_4s1-6s1__1s1-2s1-3s0-5s1-7s1-8s0` | H3/two | presplit | 1 | certified | 65.6 | 34.4 |
| 3157 | `0s0_4s1-7s0__1s1-2s0-3s0-5s0-6s1-8s0` | H3/two | presplit | 2 | certified | 303.2 | 50.4 |
| 3201 | `0s0_5s0-6s0__1s0-2s0-3s1-4s1-7s1-8s0` | H3/two | presplit | 0 | certified | 26.4 | 24.7 |
| 3245 | `0s0_5s0-6s0__1s1-2s1-3s1-4s0-7s1-8s0` | H3/two | presplit | 1 | certified | 35.2 | 24.4 |
| 3289 | `0s0_5s0-6s1__1s1-2s0-3s0-4s1-7s1-8s0` | H3/two | presplit | 2 | certified | 402.2 | 54.0 |
| 3333 | `0s0_5s1-6s0__1s1-2s1-3s0-4s1-7s1-8s0` | H3/two | timeout300 | 0 | certified | 441.1 | 55.9 |
| 3377 | `0s0-1s1_5__2s0-3s1-4s1-6s1-7s0-8s1` | H6(1,1)/one | timeout300 | 1 | certified | 243.0 | 51.7 |
| 3421 | `0s0-2s1_3__1s1-4s1-5s0-6s0-7s1-8s1` | H6(2,1)/one | timeout300 | 2 | certified | 265.3 | 46.1 |
| 3465 | `0s0-2s1_5__1s0-3s0-4s1-6s0-7s1-8s0` | H6(2,1)/one | timeout300 | 0 | certified | 238.5 | 45.2 |
| 3509 | `0s0-2s1_5__1s1-3s1-4s1-6s1-7s1-8s0` | H6(2,1)/one | timeout300 | 1 | certified | 238.4 | 45.7 |
| 3553 | `0s0-2s1_6__1s1-3s0-4s1-5s1-7s0-8s0` | H6(2,1)/one | timeout300 | 2 | certified | 302.2 | 46.8 |
| 3597 | `0s0-3s1_4__1s1-2s1-5s0-6s0-7s0-8s0` | H6(3,1)/one | never_ran | 0 | certified | 283.5 | 61.5 |
| 3641 | `0s0-3s1_5__1s0-2s1-4s1-6s1-7s0-8s0` | H6(3,1)/one | presplit | 1 | certified | 266.0 | 46.7 |
| 3685 | `0s0-4s0_6__1s0-2s0-3s1-5s0-7s0-8s0` | H6(4,0)/one | presplit | 2 | certified | 44.8 | 31.3 |
| 3729 | `0s0-4s0_6__1s1-2s1-3s0-5s1-7s0-8s0` | H6(4,0)/one | presplit | 0 | certified | 67.7 | 39.4 |
| 3773 | `0s0-5s0_6__1s0-2s1-3s1-4s0-7s1-8s1` | H6(5,0)/one | presplit | 1 | certified | 47.0 | 31.2 |
| 3817 | `0s0-5s0_7__1s0-2s0-3s0-4s1-6s1-8s1` | H6(5,0)/one | presplit | 2 | certified | 55.2 | 38.8 |
| 3861 | `0s0-5s0_7__1s1-2s1-3s0-4s0-6s1-8s1` | H6(5,0)/one | presplit | 0 | certified | 68.5 | 36.9 |
| 3905 | `0s0-5s1_1__2s1-3s0-4s1-6s1-7s0-8s1` | H6(5,1)/one | presplit | 1 | certified | 156.3 | 42.4 |
| 3949 | `0s0-5s1_2__1s0-3s1-4s1-6s0-7s0-8s1` | H6(5,1)/one | presplit | 2 | certified | 138.5 | 37.9 |
| 3993 | `0s0-5s1_6__1s1-2s0-3s0-4s1-7s1-8s0` | H6(5,1)/one | never_ran | 0 | certified | 146.9 | 38.6 |
| 4037 | `0s0-5s1_1s1-10s1__2s0-3s1-4s1-6s0-7s0-8s0` | H6(5,1)/two | never_ran | 1 | certified | 25.7 | 27.2 |
| 4081 | `0s0-5s1_2s1-3s0__1s1-4s0-6s0-7s1-8s0-9s0` | H6(5,1)/two | never_ran | 2 | certified | 36.9 | 30.7 |

Files: `out.jsonl` (lane 0, 1, 2 records), `units.tsv`, `lane0-2.sh`, `driver0-2.log.tail`, `tools.txt`, `env.txt`.
