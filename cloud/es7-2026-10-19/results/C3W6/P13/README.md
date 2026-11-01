# C3W6 P13: shard 13 of 44 of W6.tsv (94 six-bit σ-cubes), cap 900

Task: `results/C3W6/TASK.md` at c5260b44, with V = P13, LIST = W6.tsv, j = 13, N = 44, H = 4.5.

**All 94 units were certified (UNSAT, accepted by lrat-check and cake_lpr). None timed out at 900 s and none went unreached. There were no SAT answers, no proof rejections, no memory problems and no early ends.** No split records were written, so the open frontier is 0 for every unit and `recheck.jsonl` was not needed.

- Tools (see `tools.txt`): C3U2 tools at cad4e050, unmodified; CaDiCaL 3.0.1 c6073042; cake_lpr a36874a8; lrat-check 2e3b2dc + E2 patch (sanity test passed: `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both). The base CNF header is `p cnf 168399 4154921` and its sha256 `bf0e502e…dd6da` matches.
- Run: 3 lanes (`lane0.sh` … `lane2.sh`), `--jobs 1`, `--sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`, with no seeding. Started 05:31:47 UTC; END was set to 09:46:47 UTC. The lanes ran out of units at 07:38, 07:46 and 07:51 UTC, before END, so nothing was killed.
- 18 units solved in under 72 s. Each of them is certified; the task's under-72 s report applies only to solves that end without a certificate, and there were none.
- `compose.py` was not run. `out.jsonl` holds 94 solve records: lane 0, then lane 1, then lane 2.

## Per unit

| pos | row | node | stratum | prior | result | solve s | check s |
|---|---|---|---|---|---|---|---|
| 0 | 13 | `0s0_1s0-2s0__3s0-4s0-5s0-6s0-7s0-8s0` | H3/two | presplit | certified | 39.9 | 43.9 |
| 1 | 57 | `0s0_1s0-2s0__3s1-4s0-5s1-6s1-7s0-8s0` | H3/two | presplit | certified | 27.3 | 35.4 |
| 2 | 101 | `0s0_1s0-2s1__3s0-4s1-5s1-6s1-7s1-8s1` | H3/two | timeout300 | certified | 285.7 | 61.4 |
| 3 | 145 | `0s0_1s0-3s1__2s1-4s0-5s1-6s0-7s0-8s1` | H3/two | timeout300 | certified | 360.2 | 66.6 |
| 4 | 189 | `0s0_1s0-4s1__2s1-3s0-5s0-6s1-7s0-8s1` | H3/two | timeout300 | certified | 290.2 | 62.2 |
| 5 | 233 | `0s0_1s0-5s1__2s1-3s0-4s1-6s1-7s1-8s1` | H3/two | timeout300 | certified | 260.7 | 56.5 |
| 6 | 277 | `0s0_1s0-7s0__2s1-3s0-4s0-5s1-6s0-8s1` | H3/two | timeout300 | certified | 148.7 | 44.2 |
| 7 | 321 | `0s0_1s1-2s0__3s0-4s1-5s0-6s0-7s1-8s0` | H3/two | timeout300 | certified | 307.5 | 59.9 |
| 8 | 365 | `0s0_1s1-2s0__3s1-4s1-5s1-6s1-7s1-8s0` | H3/two | timeout300 | certified | 300.3 | 52.4 |
| 9 | 409 | `0s0_1s1-5s0__2s1-3s0-4s0-6s0-7s1-8s1` | H3/two | timeout300 | certified | 192.7 | 51.4 |
| 10 | 453 | `0s0_1s1-5s1__2s0-3s1-4s0-6s0-7s1-8s0` | H3/two | presplit | certified | 90.6 | 46.0 |
| 11 | 497 | `0s0_1s1-5s1__2s1-3s1-4s1-6s1-7s1-8s0` | H3/two | presplit | certified | 179.1 | 47.2 |
| 12 | 541 | `0s0_1s1-7s1__2s1-3s1-4s1-5s0-6s1-8s0` | H3/two | timeout300 | certified | 339.3 | 62.1 |
| 13 | 585 | `0s0_1s1-8s0__2s1-3s0-4s0-5s1-6s1-7s0` | H3/two | presplit | certified | 76.6 | 42.5 |
| 14 | 629 | `0s0_1s1-8s1__2s1-3s0-4s1-5s1-6s0-7s1` | H3/two | timeout300 | certified | 326.0 | 55.8 |
| 15 | 673 | `0s0_1s1-9s1__2s1-3s0-4s0-5s1-6s1-7s1` | H3/two | never_ran | certified | 353.1 | 55.8 |
| 16 | 717 | `0s0_2s0-3s1__1s0-4s1-5s0-6s0-7s1-8s1` | H3/two | presplit | certified | 312.1 | 59.2 |
| 17 | 761 | `0s0_2s0-3s1__1s1-4s1-5s1-6s1-7s1-8s1` | H3/two | presplit | certified | 235.6 | 46.7 |
| 18 | 805 | `0s0_2s0-4s1__1s1-3s0-5s1-6s0-7s1-8s1` | H3/two | presplit | certified | 353.9 | 59.6 |
| 19 | 849 | `0s0_2s0-5s0__1s0-3s1-4s0-6s1-7s1-8s1` | H3/two | presplit | certified | 67.6 | 43.3 |
| 20 | 893 | `0s0_2s0-5s1__1s0-3s0-4s1-6s0-7s1-8s0` | H3/two | timeout300 | certified | 234.5 | 60.3 |
| 21 | 937 | `0s0_2s0-5s1__1s1-3s1-4s0-6s1-7s1-8s0` | H3/two | timeout300 | certified | 349.8 | 60.2 |
| 22 | 981 | `0s0_2s0-6s1__1s1-3s0-4s0-5s1-7s0-8s0` | H3/two | timeout300 | certified | 206.0 | 55.1 |
| 23 | 1025 | `0s0_2s0-7s0__1s0-3s1-4s0-5s0-6s0-8s0` | H3/two | presplit | certified | 74.2 | 52.3 |
| 24 | 1069 | `0s0_2s0-7s0__1s1-3s1-4s1-5s1-6s0-8s0` | H3/two | presplit | certified | 95.6 | 37.5 |
| 25 | 1113 | `0s0_2s0-7s1__1s1-3s0-4s1-5s0-6s0-8s0` | H3/two | presplit | certified | 172.8 | 45.1 |
| 26 | 1157 | `0s0_2s0-8s0__1s1-3s0-4s0-5s1-6s1-7s0` | H3/two | presplit | certified | 170.1 | 48.8 |
| 27 | 1201 | `0s0_2s1-3s0__1s0-4s1-5s0-6s0-7s1-8s1` | H3/two | timeout300 | certified | 282.3 | 46.3 |
| 28 | 1245 | `0s0_2s1-3s0__1s1-4s1-5s1-6s1-7s1-8s1` | H3/two | timeout300 | certified | 255.0 | 50.9 |
| 29 | 1289 | `0s0_2s1-3s1__1s1-4s0-5s1-6s0-7s1-8s1` | H3/two | presplit | certified | 47.0 | 31.6 |
| 30 | 1333 | `0s0_2s1-4s0__1s0-3s1-5s1-6s1-7s0-8s0` | H3/two | timeout300 | certified | 310.1 | 47.2 |
| 31 | 1377 | `0s0_2s1-5s0__1s0-3s0-4s1-6s0-7s0-8s1` | H3/two | presplit | certified | 233.5 | 50.8 |
| 32 | 1421 | `0s0_2s1-5s0__1s1-3s1-4s0-6s1-7s0-8s1` | H3/two | presplit | certified | 345.5 | 63.7 |
| 33 | 1465 | `0s0_2s1-6s0__1s1-3s0-4s0-5s0-7s0-8s1` | H3/two | presplit | certified | 229.0 | 46.3 |
| 34 | 1509 | `0s0_2s1-6s1__1s0-3s0-4s1-5s1-7s0-8s1` | H3/two | presplit | certified | 168.0 | 40.7 |
| 35 | 1553 | `0s0_2s1-6s1__1s1-3s1-4s1-5s0-7s0-8s1` | H3/two | presplit | certified | 164.2 | 36.7 |
| 36 | 1597 | `0s0_2s1-7s0__1s1-3s0-4s1-5s1-6s0-8s1` | H3/two | never_ran | certified | 217.6 | 43.0 |
| 37 | 1641 | `0s0_2s1-7s1__1s1-3s1-4s0-5s0-6s1-8s1` | H3/two | never_ran | certified | 159.4 | 43.5 |
| 38 | 1685 | `0s0_2s1-8s1__1s1-3s0-4s1-5s0-6s0-7s0` | H3/two | presplit | certified | 150.4 | 39.6 |
| 39 | 1729 | `0s0_2s1-9s0__1s0-3s1-4s0-5s1-6s0-7s0` | H3/two | presplit | certified | 50.3 | 31.9 |
| 40 | 1773 | `0s0_3s0-4s1__1s0-2s0-5s0-6s0-7s0-8s0` | H3/two | presplit | certified | 155.3 | 39.3 |
| 41 | 1817 | `0s0_3s0-4s1__1s1-2s0-5s1-6s1-7s0-8s0` | H3/two | presplit | certified | 331.6 | 51.1 |
| 42 | 1861 | `0s0_3s0-5s0__1s0-2s1-4s1-6s0-7s0-8s0` | H3/two | presplit | certified | 39.8 | 28.2 |
| 43 | 1905 | `0s0_3s0-5s1__1s0-2s0-4s1-6s1-7s0-8s0` | H3/two | timeout300 | certified | 250.1 | 50.3 |
| 44 | 1949 | `0s0_3s0-5s1__1s1-2s1-4s1-6s0-7s1-8s0` | H3/two | timeout300 | certified | 345.0 | 49.4 |
| 45 | 1993 | `0s0_3s0-6s0__1s1-2s0-4s0-5s1-7s1-8s0` | H3/two | presplit | certified | 50.2 | 28.0 |
| 46 | 2037 | `0s0_3s0-6s1__1s0-2s1-4s0-5s0-7s1-8s0` | H3/two | timeout300 | certified | 302.6 | 47.2 |
| 47 | 2081 | `0s0_3s0-6s1__1s1-2s1-4s1-5s1-7s1-8s0` | H3/two | never_ran | certified | 334.2 | 47.8 |
| 48 | 2125 | `0s0_3s0-7s0__1s1-2s0-4s1-5s0-6s1-8s0` | H3/two | presplit | certified | 63.8 | 30.8 |
| 49 | 2169 | `0s0_3s0-7s1__1s0-2s1-4s0-5s1-6s1-8s0` | H3/two | presplit | certified | 224.4 | 45.9 |
| 50 | 2213 | `0s0_3s0-8s0__1s0-2s1-4s1-5s0-6s0-7s0` | H3/two | presplit | certified | 108.6 | 50.1 |
| 51 | 2257 | `0s0_3s0-8s1__1s0-2s1-4s1-5s0-6s0-7s0` | H3/two | timeout300 | certified | 237.7 | 44.7 |
| 52 | 2301 | `0s0_3s1-4s0__1s0-2s1-5s0-6s1-7s0-8s1` | H3/two | timeout300 | certified | 325.9 | 53.5 |
| 53 | 2345 | `0s0_3s1-4s1__1s0-2s0-5s0-6s0-7s0-8s1` | H3/two | presplit | certified | 66.4 | 29.6 |
| 54 | 2389 | `0s0_3s1-4s1__1s1-2s0-5s1-6s1-7s0-8s1` | H3/two | presplit | certified | 46.8 | 30.7 |
| 55 | 2433 | `0s0_3s1-5s0__1s0-2s1-4s1-6s0-7s0-8s1` | H3/two | presplit | certified | 348.3 | 48.6 |
| 56 | 2477 | `0s0_3s1-5s1__1s0-2s0-4s0-6s1-7s0-8s1` | H3/two | presplit | certified | 106.3 | 31.7 |
| 57 | 2521 | `0s0_3s1-5s1__1s1-2s1-4s0-6s0-7s0-8s1` | H3/two | presplit | certified | 72.2 | 37.0 |
| 58 | 2565 | `0s0_3s1-7s0__1s1-2s0-4s1-5s0-6s1-8s1` | H3/two | never_ran | certified | 228.7 | 40.6 |
| 59 | 2609 | `0s0_3s1-7s1__1s1-2s1-4s1-5s1-6s1-8s0` | H3/two | timeout300 | certified | 225.8 | 43.8 |
| 60 | 2653 | `0s0_3s1-8s0__1s1-2s0-4s1-5s0-6s1-7s0` | H3/two | presplit | certified | 147.1 | 45.3 |
| 61 | 2697 | `0s0_4s0-5s1__1s0-2s1-3s0-6s1-7s1-8s0` | H3/two | presplit | certified | 367.1 | 50.5 |
| 62 | 2741 | `0s0_4s0-6s1__1s0-2s0-3s0-5s0-7s1-8s0` | H3/two | presplit | certified | 198.2 | 40.7 |
| 63 | 2785 | `0s0_4s0-6s1__1s1-2s0-3s1-5s1-7s1-8s0` | H3/two | presplit | certified | 425.7 | 58.8 |
| 64 | 2829 | `0s0_4s0-7s0__1s0-2s1-3s1-5s0-6s1-8s0` | H3/two | presplit | certified | 67.4 | 32.3 |
| 65 | 2873 | `0s0_4s0-7s1__1s0-2s0-3s1-5s1-6s1-8s1` | H3/two | presplit | certified | 305.9 | 50.0 |
| 66 | 2917 | `0s0_4s0-7s1__1s1-2s1-3s1-5s0-6s1-8s1` | H3/two | presplit | certified | 323.4 | 51.2 |
| 67 | 2961 | `0s0_4s1-5s0__1s1-2s0-3s0-6s1-7s1-8s1` | H3/two | never_ran | certified | 314.3 | 48.4 |
| 68 | 3005 | `0s0_4s1-6s0__1s0-2s0-3s1-5s0-7s1-8s0` | H3/two | presplit | certified | 307.2 | 46.9 |
| 69 | 3049 | `0s0_4s1-6s0__1s1-2s1-3s0-5s1-7s1-8s0` | H3/two | presplit | certified | 402.2 | 53.5 |
| 70 | 3093 | `0s0_4s1-6s1__1s1-2s0-3s0-5s0-7s1-8s0` | H3/two | presplit | certified | 65.4 | 27.8 |
| 71 | 3137 | `0s0_4s1-7s0__1s0-2s0-3s1-5s1-6s1-8s0` | H3/two | presplit | certified | 303.9 | 50.7 |
| 72 | 3181 | `0s0_4s1-7s0__1s1-2s1-3s1-5s0-6s1-8s0` | H3/two | presplit | certified | 358.9 | 50.0 |
| 73 | 3225 | `0s0_5s0-6s0__1s1-2s0-3s0-4s1-7s1-8s0` | H3/two | presplit | certified | 22.4 | 37.2 |
| 74 | 3269 | `0s0_5s0-6s1__1s0-2s1-3s0-4s0-7s1-8s0` | H3/two | presplit | certified | 289.1 | 47.6 |
| 75 | 3313 | `0s0_5s0-6s1__1s1-2s1-3s1-4s1-7s1-8s0` | H3/two | presplit | certified | 337.5 | 48.9 |
| 76 | 3357 | `0s0-1s1_5__2s0-3s0-4s0-6s0-7s0-8s1` | H6(1,1)/one | timeout300 | certified | 213.3 | 38.8 |
| 77 | 3401 | `0s0-1s1_5__2s1-3s1-4s0-6s1-7s0-8s1` | H6(1,1)/one | timeout300 | certified | 151.1 | 37.4 |
| 78 | 3445 | `0s0-2s1_4__1s1-3s1-5s0-6s0-7s0-8s1` | H6(2,1)/one | timeout300 | certified | 241.4 | 48.9 |
| 79 | 3489 | `0s0-2s1_5__1s1-3s0-4s1-6s0-7s1-8s0` | H6(2,1)/one | timeout300 | certified | 245.2 | 43.8 |
| 80 | 3533 | `0s0-2s1_6__1s0-3s1-4s1-5s0-7s0-8s0` | H6(2,1)/one | timeout300 | certified | 172.2 | 37.9 |
| 81 | 3577 | `0s0-3s1_4__1s0-2s1-5s0-6s1-7s0-8s0` | H6(3,1)/one | timeout300 | certified | 220.4 | 43.3 |
| 82 | 3621 | `0s0-3s1_5__1s0-2s0-4s1-6s0-7s0-8s0` | H6(3,1)/one | presplit | certified | 176.9 | 39.0 |
| 83 | 3665 | `0s0-3s1_5__1s1-2s1-4s0-6s1-7s0-8s0` | H6(3,1)/one | presplit | certified | 218.4 | 47.5 |
| 84 | 3709 | `0s0-4s0_6__1s1-2s0-3s0-5s0-7s0-8s0` | H6(4,0)/one | presplit | certified | 62.0 | 32.0 |
| 85 | 3753 | `0s0-5s0_6__1s0-2s0-3s0-4s1-7s1-8s1` | H6(5,0)/one | presplit | certified | 40.6 | 45.6 |
| 86 | 3797 | `0s0-5s0_6__1s1-2s1-3s0-4s0-7s1-8s1` | H6(5,0)/one | presplit | certified | 55.2 | 31.2 |
| 87 | 3841 | `0s0-5s0_7__1s0-2s1-3s1-4s1-6s1-8s1` | H6(5,0)/one | presplit | certified | 47.9 | 32.1 |
| 88 | 3885 | `0s0-5s1_1__2s0-3s1-4s1-6s0-7s0-8s1` | H6(5,1)/one | presplit | certified | 126.4 | 36.9 |
| 89 | 3929 | `0s0-5s1_2__1s0-3s0-4s0-6s1-7s0-8s1` | H6(5,1)/one | presplit | certified | 148.7 | 39.9 |
| 90 | 3973 | `0s0-5s1_2__1s1-3s1-4s0-6s0-7s0-8s1` | H6(5,1)/one | presplit | certified | 182.8 | 39.9 |
| 91 | 4017 | `0s0-5s1_6__1s1-2s1-3s1-4s1-7s1-8s0` | H6(5,1)/one | never_ran | certified | 182.4 | 38.7 |
| 92 | 4061 | `0s0-5s1_1s1-10s1__2s1-3s1-4s0-6s0-7s0-8s0` | H6(5,1)/two | never_ran | certified | 30.3 | 28.1 |
| 93 | 4105 | `0s0-5s1_7s0-9s1__1s1-2s0-3s0` | H6(5,1)/two | presplit | certified | 180.2 | 35.4 |

## Totals per stratum

| stratum | units | certified | timed out | not reached | solve s (sum) |
|---|---|---|---|---|---|
| H3/two | 76 | 76 | 0 | 0 | 16562 |
| H6(1,1)/one | 2 | 2 | 0 | 0 | 364 |
| H6(2,1)/one | 3 | 3 | 0 | 0 | 659 |
| H6(3,1)/one | 3 | 3 | 0 | 0 | 616 |
| H6(4,0)/one | 1 | 1 | 0 | 0 | 62 |
| H6(5,0)/one | 3 | 3 | 0 | 0 | 144 |
| H6(5,1)/one | 4 | 4 | 0 | 0 | 640 |
| H6(5,1)/two | 2 | 2 | 0 | 0 | 210 |

## Totals per prior

| prior | units | certified | timed out | not reached | solve s (sum) |
|---|---|---|---|---|---|
| never_ran | 8 | 8 | 0 | 0 | 1820 |
| presplit | 58 | 58 | 0 | 0 | 10057 |
| timeout300 | 28 | 28 | 0 | 0 | 7380 |

## Solve times of the certified units (94)

solve s: min 22.4, q1 106.9, median 215.4, q3 305.4, p90 345.4, max 425.7; above 300 s: 27; total 19257 s
check s: min 27.8, median 46.0, max 66.6; total 4248 s
units with solve under 72 s: 18, all certified
max proof size: 0.57 GB (deleted, not committed)
