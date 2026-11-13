# C3W6 P39: shard 39 of 44 of W6.tsv, cap 900

Task: `results/C3W6/TASK.md` at c5260b44, with V = P39, LIST = W6.tsv, j = 39, N = 44, H = 4.5.
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 05:31:43 UTC on 2026-10-25, END 09:46:43 UTC. All lanes finished at 07:58:10 UTC, so END was not needed and no lane was killed.

## Tools and base CNF (`tools.txt`)

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04.
- cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa. Its example prints `s VERIFIED UNSAT`.
- lrat-check from drat-trim 2e3b2dc0ecf938addbd779d42877b6ed69d9a985, with the E2 patch. Sanity test on {1},{-1}: both checkers reject `3 0 0` and both accept `3 0 1 2 0`.
- Base CNF from `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…6da`. Both match the expected values.

## Run

- Units: the 93 rows of W6.tsv with row ≡ 39 (mod 44), listed in `units.tsv`. All 93 are six-bit σ-cubes. No records were seeded.
- Three lanes ran `lane0.sh` to `lane2.sh`. Lane k took the positions ≡ k (mod 3), 31 units per lane. Each lane called `close_tree.py … U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`.
- `out.jsonl` holds lane 0, then lane 1, then lane 2: 93 solve records and no split records.

## Result

- **All 93 units are certified at cap 900.** For every unit, lrat-check printed `c VERIFIED` and cake_lpr printed `s VERIFIED UNSAT`.
- No unit timed out and every unit was reached. No open frontier and no unsplittable node.
- There was no SAT answer and no proof rejection, so `recheck.jsonl` was not needed.
- No memory problem: at most about 5 GB was in use. The largest proof was 582 MB, deleted after checking.
- No unit ended early without a certificate.

Solve times of the 93 certified units, in seconds:

| min | Q1 | median | Q3 | p90 | max |
|---|---|---|---|---|---|
| 24.5 | 98.7 | 222.2 | 308.0 | 388.3 | 456.3 |

27 units were certified above 300 s. Over all units, solving took 19,755 s and checking took 3,833 s.

### Totals per stratum and per prior

| column | value | units | certified | timed out at 900 | not reached | solve s | check s |
|---|---|---|---|---|---|---|---|
| stratum | H3/two | 76 | 76 | 0 | 0 | 17198.7 | 3251.4 |
| stratum | H6(1,1)/one | 1 | 1 | 0 | 0 | 197.9 | 36.2 |
| stratum | H6(2,1)/one | 4 | 4 | 0 | 0 | 993.5 | 152.6 |
| stratum | H6(3,1)/one | 2 | 2 | 0 | 0 | 552.4 | 83.2 |
| stratum | H6(4,0)/one | 2 | 2 | 0 | 0 | 117.9 | 55.9 |
| stratum | H6(5,0)/one | 3 | 3 | 0 | 0 | 161.1 | 98.3 |
| stratum | H6(5,1)/one | 3 | 3 | 0 | 0 | 451.2 | 100.2 |
| stratum | H6(5,1)/two | 2 | 2 | 0 | 0 | 82.3 | 55.6 |
| prior | never_ran | 10 | 10 | 0 | 0 | 1995.6 | 394.1 |
| prior | presplit | 54 | 54 | 0 | 0 | 9229.1 | 2073.9 |
| prior | timeout300 | 29 | 29 | 0 | 0 | 8530.3 | 1365.4 |

### Per unit

| row | lane | node | stratum | prior | result | solve s | check s |
|---|---|---|---|---|---|---|---|
| 39 | 0 | `0s0_1s0-2s0__3s0-4s1-5s1-6s0-7s1-8s0` | H3/two | presplit | certified | 32.5 | 35.5 |
| 83 | 1 | `0s0_1s0-2s1__3s0-4s0-5s1-6s1-7s0-8s1` | H3/two | timeout300 | certified | 372.7 | 62.5 |
| 127 | 2 | `0s0_1s0-2s1__3s1-4s1-5s1-6s0-7s0-8s1` | H3/two | timeout300 | certified | 456.3 | 64.6 |
| 171 | 0 | `0s0_1s0-4s1__2s0-3s1-5s0-6s0-7s0-8s1` | H3/two | timeout300 | certified | 314.6 | 64.5 |
| 215 | 1 | `0s0_1s0-4s1__2s1-3s1-5s1-6s1-7s1-8s1` | H3/two | timeout300 | certified | 282.6 | 41.5 |
| 259 | 2 | `0s0_1s0-7s0__2s0-3s0-4s1-5s0-6s1-8s0` | H3/two | timeout300 | certified | 159.6 | 47.9 |
| 303 | 0 | `0s0_1s0-7s1__2s1-3s1-4s1-5s0-6s0-8s1` | H3/two | timeout300 | certified | 298.4 | 44.9 |
| 347 | 1 | `0s0_1s1-2s0__3s1-4s0-5s1-6s1-7s0-8s0` | H3/two | timeout300 | certified | 311.3 | 54.2 |
| 391 | 2 | `0s0_1s1-5s0__2s0-3s0-4s0-6s0-7s1-8s1` | H3/two | timeout300 | certified | 217.2 | 43.8 |
| 435 | 0 | `0s0_1s1-5s1__2s0-3s0-4s0-6s0-7s0-8s0` | H3/two | presplit | certified | 112.9 | 40.6 |
| 479 | 1 | `0s0_1s1-5s1__2s1-3s0-4s1-6s1-7s0-8s0` | H3/two | presplit | certified | 183.3 | 41.8 |
| 523 | 2 | `0s0_1s1-7s1__2s1-3s0-4s1-5s0-6s0-8s0` | H3/two | timeout300 | certified | 278.4 | 48.1 |
| 567 | 0 | `0s0_1s1-8s0__2s0-3s1-4s0-5s1-6s0-7s0` | H3/two | presplit | certified | 70.4 | 38.2 |
| 611 | 1 | `0s0_1s1-8s1__2s0-3s1-4s0-5s0-6s1-7s1` | H3/two | timeout300 | certified | 301.9 | 48.5 |
| 655 | 2 | `0s0_1s1-9s1__2s0-3s1-4s0-5s1-6s0-7s1` | H3/two | never_ran | certified | 354.3 | 66.8 |
| 699 | 0 | `0s0_2s0-3s1__1s0-4s0-5s0-6s0-7s0-8s1` | H3/two | presplit | certified | 242.6 | 48.1 |
| 743 | 1 | `0s0_2s0-3s1__1s1-4s0-5s1-6s1-7s0-8s1` | H3/two | presplit | certified | 454.8 | 49.9 |
| 787 | 2 | `0s0_2s0-4s1__1s0-3s1-5s1-6s0-7s0-8s1` | H3/two | presplit | certified | 430.8 | 64.0 |
| 831 | 0 | `0s0_2s0-5s0__1s0-3s0-4s0-6s1-7s0-8s1` | H3/two | presplit | certified | 51.8 | 33.5 |
| 875 | 1 | `0s0_2s0-5s0__1s1-3s1-4s0-6s0-7s0-8s1` | H3/two | presplit | certified | 58.4 | 31.5 |
| 919 | 2 | `0s0_2s0-5s1__1s1-3s0-4s0-6s1-7s0-8s0` | H3/two | timeout300 | certified | 309.2 | 56.1 |
| 963 | 0 | `0s0_2s0-6s1__1s0-3s1-4s0-5s0-7s1-8s0` | H3/two | timeout300 | certified | 358.7 | 54.1 |
| 1007 | 1 | `0s0_2s0-6s1__1s1-3s1-4s1-5s1-7s1-8s0` | H3/two | timeout300 | certified | 335.2 | 47.0 |
| 1051 | 2 | `0s0_2s0-7s0__1s1-3s0-4s1-5s0-6s1-8s0` | H3/two | presplit | certified | 143.6 | 34.5 |
| 1095 | 0 | `0s0_2s0-7s1__1s0-3s1-4s0-5s1-6s1-8s0` | H3/two | presplit | certified | 237.7 | 45.3 |
| 1139 | 1 | `0s0_2s0-8s0__1s0-3s1-4s0-5s1-6s0-7s0` | H3/two | presplit | certified | 142.8 | 37.8 |
| 1183 | 2 | `0s0_2s1-3s0__1s0-4s0-5s0-6s0-7s0-8s0` | H3/two | timeout300 | certified | 213.1 | 53.0 |
| 1227 | 0 | `0s0_2s1-3s0__1s1-4s0-5s1-6s1-7s0-8s1` | H3/two | timeout300 | certified | 390.4 | 49.3 |
| 1271 | 1 | `0s0_2s1-3s1__1s0-4s1-5s1-6s0-7s0-8s1` | H3/two | presplit | certified | 67.4 | 31.1 |
| 1315 | 2 | `0s0_2s1-4s0__1s0-3s0-5s1-6s0-7s0-8s0` | H3/two | timeout300 | certified | 249.6 | 40.1 |
| 1359 | 0 | `0s0_2s1-4s0__1s1-3s1-5s0-6s1-7s1-8s1` | H3/two | timeout300 | certified | 396.5 | 53.3 |
| 1403 | 1 | `0s0_2s1-5s0__1s1-3s0-4s0-6s0-7s1-8s1` | H3/two | presplit | certified | 303.4 | 60.9 |
| 1447 | 2 | `0s0_2s1-6s0__1s0-3s0-4s1-5s1-7s1-8s1` | H3/two | presplit | certified | 239.2 | 39.4 |
| 1491 | 0 | `0s0_2s1-6s0__1s1-3s1-4s1-5s0-7s1-8s1` | H3/two | presplit | certified | 242.7 | 39.3 |
| 1535 | 1 | `0s0_2s1-6s1__1s1-3s0-4s0-5s1-7s1-8s1` | H3/two | presplit | certified | 121.3 | 46.5 |
| 1579 | 2 | `0s0_2s1-7s0__1s0-3s1-4s1-5s0-6s1-8s1` | H3/two | never_ran | certified | 151.0 | 35.3 |
| 1623 | 0 | `0s0_2s1-7s1__1s1-3s0-4s0-5s0-6s0-8s1` | H3/two | never_ran | certified | 140.1 | 31.0 |
| 1667 | 1 | `0s0_2s1-8s1__1s0-3s1-4s0-5s1-6s1-7s0` | H3/two | presplit | certified | 352.6 | 45.2 |
| 1711 | 2 | `0s0_2s1-9s0__1s0-3s0-4s0-5s0-6s1-7s0` | H3/two | presplit | certified | 77.9 | 34.5 |
| 1755 | 0 | `0s0_2s1-9s0__1s1-3s0-4s1-5s1-6s1-7s0` | H3/two | presplit | certified | 111.3 | 48.7 |
| 1799 | 1 | `0s0_3s0-4s1__1s0-2s1-5s1-6s0-7s1-8s0` | H3/two | presplit | certified | 423.0 | 60.7 |
| 1843 | 2 | `0s0_3s0-5s0__1s0-2s0-4s0-6s1-7s1-8s0` | H3/two | presplit | certified | 26.7 | 19.3 |
| 1887 | 0 | `0s0_3s0-5s0__1s1-2s1-4s0-6s0-7s1-8s0` | H3/two | presplit | certified | 55.7 | 29.6 |
| 1931 | 1 | `0s0_3s0-5s1__1s1-2s0-4s1-6s0-7s0-8s0` | H3/two | timeout300 | certified | 306.7 | 41.0 |
| 1975 | 2 | `0s0_3s0-6s0__1s0-2s1-4s0-5s1-7s0-8s0` | H3/two | presplit | certified | 51.8 | 26.8 |
| 2019 | 0 | `0s0_3s0-6s1__1s0-2s0-4s0-5s0-7s0-8s0` | H3/two | timeout300 | certified | 166.9 | 45.4 |
| 2063 | 1 | `0s0_3s0-6s1__1s1-2s0-4s1-5s1-7s0-8s0` | H3/two | timeout300 | certified | 366.8 | 45.0 |
| 2107 | 2 | `0s0_3s0-7s0__1s0-2s1-4s1-5s0-6s0-8s0` | H3/two | presplit | certified | 89.2 | 29.1 |
| 2151 | 0 | `0s0_3s0-7s1__1s0-2s0-4s0-5s1-6s0-8s0` | H3/two | presplit | certified | 207.4 | 47.4 |
| 2195 | 1 | `0s0_3s0-7s1__1s1-2s1-4s0-5s0-6s0-8s0` | H3/two | presplit | certified | 228.8 | 37.4 |
| 2239 | 2 | `0s0_3s0-8s0__1s1-2s1-4s0-5s0-6s1-7s0` | H3/two | presplit | certified | 144.3 | 34.0 |
| 2283 | 0 | `0s0_3s1-4s0__1s0-2s0-5s0-6s0-7s1-8s1` | H3/two | timeout300 | certified | 222.2 | 39.2 |
| 2327 | 1 | `0s0_3s1-4s0__1s1-2s0-5s1-6s1-7s1-8s1` | H3/two | timeout300 | certified | 357.8 | 44.8 |
| 2371 | 2 | `0s0_3s1-4s1__1s0-2s1-5s1-6s0-7s1-8s1` | H3/two | presplit | certified | 54.4 | 26.4 |
| 2415 | 0 | `0s0_3s1-5s0__1s0-2s0-4s0-6s1-7s1-8s1` | H3/two | presplit | certified | 238.6 | 57.8 |
| 2459 | 1 | `0s0_3s1-5s0__1s1-2s1-4s0-6s0-7s1-8s1` | H3/two | presplit | certified | 385.2 | 45.1 |
| 2503 | 2 | `0s0_3s1-5s1__1s0-2s1-4s1-6s1-7s1-8s1` | H3/two | presplit | certified | 62.9 | 30.8 |
| 2547 | 0 | `0s0_3s1-7s0__1s0-2s1-4s1-5s0-6s0-8s1` | H3/two | never_ran | certified | 226.0 | 37.8 |
| 2591 | 1 | `0s0_3s1-7s1__1s0-2s0-4s1-5s1-6s1-8s0` | H3/two | timeout300 | certified | 271.6 | 42.7 |
| 2635 | 2 | `0s0_3s1-8s0__1s0-2s1-4s1-5s0-6s0-7s0` | H3/two | presplit | certified | 133.3 | 35.2 |
| 2679 | 0 | `0s0_4s0-5s1__1s0-2s0-3s0-6s1-7s0-8s0` | H3/two | presplit | certified | 232.7 | 39.5 |
| 2723 | 1 | `0s0_4s0-5s1__1s1-2s1-3s0-6s0-7s0-8s0` | H3/two | presplit | certified | 290.4 | 37.5 |
| 2767 | 2 | `0s0_4s0-6s1__1s0-2s1-3s1-5s1-7s0-8s0` | H3/two | presplit | certified | 361.2 | 44.2 |
| 2811 | 0 | `0s0_4s0-7s0__1s0-2s0-3s1-5s0-6s0-8s0` | H3/two | presplit | certified | 54.2 | 27.6 |
| 2855 | 1 | `0s0_4s0-7s0__1s1-2s1-3s0-5s1-6s0-8s0` | H3/two | presplit | certified | 60.5 | 31.3 |
| 2899 | 2 | `0s0_4s0-7s1__1s1-2s0-3s1-5s0-6s0-8s1` | H3/two | presplit | certified | 353.0 | 44.2 |
| 2943 | 0 | `0s0_4s1-5s0__1s0-2s1-3s0-6s1-7s0-8s1` | H3/two | never_ran | certified | 438.6 | 62.7 |
| 2987 | 1 | `0s0_4s1-5s1__1s1-2s1-3s1-6s0-7s0-8s0` | H3/two | never_ran | certified | 108.1 | 29.5 |
| 3031 | 2 | `0s0_4s1-6s0__1s1-2s0-3s0-5s1-7s0-8s0` | H3/two | presplit | certified | 303.9 | 48.1 |
| 3075 | 0 | `0s0_4s1-6s1__1s0-2s1-3s0-5s0-7s0-8s0` | H3/two | presplit | certified | 75.6 | 27.2 |
| 3119 | 1 | `0s0_4s1-6s1__1s1-2s1-3s1-5s1-7s0-8s0` | H3/two | presplit | certified | 114.4 | 29.9 |
| 3163 | 2 | `0s0_4s1-7s0__1s1-2s0-3s1-5s0-6s0-8s0` | H3/two | presplit | certified | 242.3 | 36.9 |
| 3207 | 0 | `0s0_5s0-6s0__1s0-2s1-3s0-4s1-7s0-8s0` | H3/two | presplit | certified | 24.5 | 21.3 |
| 3251 | 1 | `0s0_5s0-6s1__1s0-2s0-3s0-4s0-7s0-8s0` | H3/two | presplit | certified | 156.9 | 32.3 |
| 3295 | 2 | `0s0_5s0-6s1__1s1-2s0-3s1-4s1-7s0-8s0` | H3/two | presplit | certified | 393.4 | 65.8 |
| 3339 | 0 | `0s0_5s1-6s0__1s1-2s1-3s1-4s1-7s0-8s0` | H3/two | timeout300 | certified | 401.2 | 45.1 |
| 3383 | 1 | `0s0-1s1_5__2s1-3s0-4s0-6s0-7s1-8s1` | H6(1,1)/one | timeout300 | certified | 197.9 | 36.2 |
| 3427 | 2 | `0s0-2s1_4__1s0-3s1-5s1-6s1-7s1-8s1` | H6(2,1)/one | timeout300 | certified | 332.1 | 41.2 |
| 3471 | 0 | `0s0-2s1_5__1s0-3s1-4s1-6s0-7s0-8s0` | H6(2,1)/one | timeout300 | certified | 252.3 | 36.6 |
| 3515 | 1 | `0s0-2s1_6__1s0-3s0-4s0-5s1-7s0-8s0` | H6(2,1)/one | timeout300 | certified | 179.6 | 36.4 |
| 3559 | 2 | `0s0-2s1_6__1s1-3s1-4s0-5s0-7s1-8s0` | H6(2,1)/one | timeout300 | certified | 229.5 | 38.4 |
| 3603 | 0 | `0s0-3s1_4__1s1-2s1-5s0-6s1-7s1-8s0` | H6(3,1)/one | never_ran | certified | 291.7 | 42.1 |
| 3647 | 1 | `0s0-3s1_5__1s1-2s0-4s0-6s0-7s1-8s0` | H6(3,1)/one | presplit | certified | 260.7 | 41.1 |
| 3691 | 2 | `0s0-4s0_6__1s0-2s0-3s1-5s1-7s1-8s0` | H6(4,0)/one | presplit | certified | 57.5 | 28.1 |
| 3735 | 0 | `0s0-4s0_6__1s1-2s1-3s1-5s0-7s1-8s0` | H6(4,0)/one | presplit | certified | 60.4 | 27.8 |
| 3779 | 1 | `0s0-5s0_6__1s1-2s0-3s0-4s0-7s0-8s1` | H6(5,0)/one | presplit | certified | 51.1 | 30.2 |
| 3823 | 2 | `0s0-5s0_7__1s0-2s0-3s1-4s1-6s0-8s1` | H6(5,0)/one | presplit | certified | 54.3 | 27.6 |
| 3867 | 0 | `0s0-5s0_7__1s1-2s1-3s1-4s0-6s0-8s1` | H6(5,0)/one | presplit | certified | 55.7 | 40.5 |
| 3911 | 1 | `0s0-5s1_1__2s1-3s1-4s0-6s0-7s1-8s1` | H6(5,1)/one | presplit | certified | 135.7 | 35.7 |
| 3955 | 2 | `0s0-5s1_2__1s0-3s1-4s1-6s1-7s1-8s1` | H6(5,1)/one | presplit | certified | 112.0 | 31.2 |
| 3999 | 0 | `0s0-5s1_6__1s1-2s0-3s1-4s1-7s0-8s0` | H6(5,1)/one | never_ran | certified | 203.5 | 33.3 |
| 4043 | 1 | `0s0-5s1_1s1-10s1__2s0-3s1-4s1-6s1-7s1-8s0` | H6(5,1)/two | never_ran | certified | 40.4 | 30.6 |
| 4087 | 2 | `0s0-5s1_2s1-3s0__1s1-4s1-6s0-7s0-8s1-9s0` | H6(5,1)/two | never_ran | certified | 41.9 | 25.0 |
