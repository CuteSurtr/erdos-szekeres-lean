# C3W6 P36: W6.tsv shard 36 of 44, cap 900

Task: `results/C3W6/TASK.md` at c5260b44, with V = P36, LIST = W6.tsv, j = 36, N = 44, H = 4.5.
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 05:31:48 UTC, END 09:46:48 UTC. Lanes ran 05:34:41 to 08:58:08 UTC, so they finished before END and the watchdog never fired.

## Tools (`tools.txt`)

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, `TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04.
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa: the bundled example gives `s VERIFIED UNSAT`.
- lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with the E2 patch. Sanity test on the CNF {1},{-1}: `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF from `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da`, which matches.

## Run

- Units: the 93 rows of `lists/W6.tsv` with row ≡ 36 (mod 44) (`units.tsv`). No records were seeded.
- 3 lanes (`lane0.sh`, `lane1.sh`, `lane2.sh`) of 31 units each.
- Each unit ran once: `close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`.
- `out.jsonl` holds lane 0, then lane 1, then lane 2: 93 records, one solve record per unit and no split records.

## Result

**All 93 units were certified at cap 900.** Every record has status UNSATISFIABLE, lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.

- No unit timed out and every unit was reached. Open frontier: 0 for every unit.
- No SAT and no proof rejection, so there is no `recheck.jsonl`.
- No checker was killed at END and no memory problem occurred: available memory stayed at 9 GB or more.
- 9 units finished in under 72 s, and all 9 have certificates. No unit ended early without a certificate.

Solve-time distribution of the 93 certified units:

| statistic | seconds |
|---|---|
| min | 20.0 |
| Q1 | 127.9 |
| median | 332.8 |
| Q3 | 443.3 |
| p90 | 564.0 |
| max | 718.7 |

- 49 of the 93 were certified above 300 s, so they would have timed out at the earlier cap of 300.
- Check time per unit: 18.2 s minimum, 50.5 s median, 90.3 s maximum.
- Totals: 28,784 s of solving and 4,602 s of checking.
- Largest proof: 590 MB, deleted after checking.

### Totals per stratum and per prior

| column | value | units | certified | timed out at 900 | not reached | solve s | check s |
|---|---|---|---|---|---|---|---|
| stratum | H3/two | 76 | 76 | 0 | 0 | 25217 | 3850 |
| stratum | H6(1,1)/one | 1 | 1 | 0 | 0 | 373 | 54 |
| stratum | H6(2,1)/one | 4 | 4 | 0 | 0 | 1353 | 211 |
| stratum | H6(3,1)/one | 2 | 2 | 0 | 0 | 605 | 98 |
| stratum | H6(4,0)/one | 2 | 2 | 0 | 0 | 162 | 68 |
| stratum | H6(5,0)/one | 3 | 3 | 0 | 0 | 347 | 112 |
| stratum | H6(5,1)/one | 3 | 3 | 0 | 0 | 625 | 144 |
| stratum | H6(5,1)/two | 2 | 2 | 0 | 0 | 101 | 66 |
| prior | timeout300 | 27 | 27 | 0 | 0 | 11254 | 1574 |
| prior | never_ran | 11 | 11 | 0 | 0 | 3852 | 571 |
| prior | presplit | 55 | 55 | 0 | 0 | 13678 | 2458 |

## Per unit (lane = position mod 3; seconds from out.jsonl)

| row | lane | node | stratum | prior | result | solve s | check s |
|---|---|---|---|---|---|---|---|
| 36 | 0 | `0s0_1s0-2s0__3s0-4s1-5s0-6s1-7s1-8s1` | H3/two | presplit | certified | 31.9 | 45.5 |
| 80 | 1 | `0s0_1s0-2s1__3s0-4s0-5s1-6s0-7s1-8s0` | H3/two | timeout300 | certified | 398.7 | 73.1 |
| 124 | 2 | `0s0_1s0-2s1__3s1-4s1-5s0-6s1-7s1-8s0` | H3/two | timeout300 | certified | 479.6 | 71.6 |
| 168 | 0 | `0s0_1s0-4s1__2s0-3s0-5s1-6s1-7s0-8s0` | H3/two | timeout300 | certified | 474.0 | 64.1 |
| 212 | 1 | `0s0_1s0-4s1__2s1-3s1-5s1-6s1-7s0-8s0` | H3/two | timeout300 | certified | 364.9 | 69.4 |
| 256 | 2 | `0s0_1s0-7s0__2s0-3s0-4s0-5s1-6s1-8s0` | H3/two | timeout300 | certified | 187.1 | 57.9 |
| 300 | 0 | `0s0_1s0-7s1__2s1-3s1-4s0-5s1-6s1-8s0` | H3/two | timeout300 | certified | 257.4 | 60.5 |
| 344 | 1 | `0s0_1s1-2s0__3s1-4s0-5s1-6s0-7s0-8s1` | H3/two | timeout300 | certified | 459.4 | 69.4 |
| 388 | 2 | `0s0_1s1-4s0__2s1-3s1-5s1-6s0-7s1-8s1` | H3/two | timeout300 | certified | 475.1 | 75.1 |
| 432 | 0 | `0s0_1s1-5s0__2s1-3s1-4s1-6s1-7s0-8s1` | H3/two | timeout300 | certified | 438.2 | 75.3 |
| 476 | 1 | `0s0_1s1-5s1__2s1-3s0-4s1-6s0-7s0-8s1` | H3/two | presplit | certified | 310.6 | 65.4 |
| 520 | 2 | `0s0_1s1-7s1__2s1-3s0-4s0-5s1-6s0-8s1` | H3/two | timeout300 | certified | 392.4 | 56.4 |
| 564 | 0 | `0s0_1s1-8s0__2s0-3s1-4s0-5s0-6s0-7s1` | H3/two | presplit | certified | 116.3 | 44.7 |
| 608 | 1 | `0s0_1s1-8s0__2s1-3s1-4s1-5s1-6s0-7s1` | H3/two | presplit | certified | 153.3 | 41.9 |
| 652 | 2 | `0s0_1s1-9s1__2s0-3s0-4s1-5s1-6s0-7s1` | H3/two | never_ran | certified | 421.8 | 57.1 |
| 696 | 0 | `0s0_1s1-9s1__2s1-3s1-4s1-5s1-6s1-7s0` | H3/two | never_ran | certified | 556.2 | 65.7 |
| 740 | 1 | `0s0_2s0-3s1__1s1-4s0-5s1-6s0-7s1-8s0` | H3/two | presplit | certified | 467.7 | 56.1 |
| 784 | 2 | `0s0_2s0-4s1__1s0-3s1-5s0-6s1-7s1-8s0` | H3/two | presplit | certified | 568.1 | 60.1 |
| 828 | 0 | `0s0_2s0-5s0__1s0-3s0-4s0-6s0-7s1-8s0` | H3/two | presplit | certified | 63.4 | 36.7 |
| 872 | 1 | `0s0_2s0-5s0__1s1-3s0-4s1-6s1-7s1-8s0` | H3/two | presplit | certified | 104.3 | 37.4 |
| 916 | 2 | `0s0_2s0-5s1__1s1-3s0-4s0-6s0-7s0-8s1` | H3/two | timeout300 | certified | 432.3 | 52.4 |
| 960 | 0 | `0s0_2s0-6s1__1s0-3s0-4s1-5s1-7s1-8s1` | H3/two | timeout300 | certified | 363.8 | 51.1 |
| 1004 | 1 | `0s0_2s0-6s1__1s1-3s1-4s1-5s0-7s1-8s1` | H3/two | timeout300 | certified | 471.8 | 54.2 |
| 1048 | 2 | `0s0_2s0-7s0__1s1-3s0-4s0-5s1-6s1-8s1` | H3/two | presplit | certified | 252.2 | 45.7 |
| 1092 | 0 | `0s0_2s0-7s1__1s0-3s1-4s0-5s0-6s1-8s1` | H3/two | presplit | certified | 319.5 | 50.6 |
| 1136 | 1 | `0s0_2s0-7s1__1s1-3s1-4s1-5s1-6s1-8s1` | H3/two | presplit | certified | 365.1 | 49.5 |
| 1180 | 2 | `0s0_2s0-8s0__1s1-3s1-4s1-5s1-6s0-7s1` | H3/two | presplit | certified | 190.1 | 41.2 |
| 1224 | 0 | `0s0_2s1-3s0__1s1-4s0-5s1-6s0-7s1-8s0` | H3/two | timeout300 | certified | 482.6 | 53.2 |
| 1268 | 1 | `0s0_2s1-3s1__1s0-4s1-5s0-6s1-7s1-8s0` | H3/two | presplit | certified | 81.0 | 35.6 |
| 1312 | 2 | `0s0_2s1-4s0__1s0-3s0-5s0-6s1-7s0-8s1` | H3/two | timeout300 | certified | 369.9 | 50.5 |
| 1356 | 0 | `0s0_2s1-4s0__1s1-3s1-5s0-6s1-7s0-8s0` | H3/two | timeout300 | certified | 424.0 | 54.2 |
| 1400 | 1 | `0s0_2s1-5s0__1s1-3s0-4s0-6s0-7s0-8s0` | H3/two | presplit | certified | 291.3 | 47.9 |
| 1444 | 2 | `0s0_2s1-6s0__1s0-3s0-4s1-5s1-7s0-8s0` | H3/two | presplit | certified | 425.9 | 53.4 |
| 1488 | 0 | `0s0_2s1-6s0__1s1-3s1-4s1-5s0-7s0-8s0` | H3/two | presplit | certified | 397.6 | 49.0 |
| 1532 | 1 | `0s0_2s1-6s1__1s1-3s0-4s0-5s1-7s0-8s0` | H3/two | presplit | certified | 154.7 | 44.0 |
| 1576 | 2 | `0s0_2s1-7s0__1s0-3s1-4s1-5s0-6s0-8s0` | H3/two | never_ran | certified | 214.5 | 40.1 |
| 1620 | 0 | `0s0_2s1-7s1__1s0-3s1-4s1-5s1-6s1-8s0` | H3/two | never_ran | certified | 479.8 | 52.5 |
| 1664 | 1 | `0s0_2s1-8s1__1s0-3s1-4s0-5s0-6s1-7s1` | H3/two | presplit | certified | 443.3 | 54.9 |
| 1708 | 2 | `0s0_2s1-8s1__1s1-3s1-4s1-5s1-6s1-7s1` | H3/two | presplit | certified | 622.8 | 55.4 |
| 1752 | 0 | `0s0_2s1-9s0__1s1-3s0-4s1-5s0-6s1-7s1` | H3/two | presplit | certified | 176.5 | 42.2 |
| 1796 | 1 | `0s0_3s0-4s1__1s0-2s1-5s0-6s1-7s1-8s1` | H3/two | presplit | certified | 581.8 | 56.4 |
| 1840 | 2 | `0s0_3s0-5s0__1s0-2s0-4s0-6s0-7s1-8s1` | H3/two | presplit | certified | 20.9 | 18.2 |
| 1884 | 0 | `0s0_3s0-5s0__1s1-2s0-4s1-6s1-7s1-8s1` | H3/two | presplit | certified | 73.1 | 30.7 |
| 1928 | 1 | `0s0_3s0-5s1__1s1-2s0-4s0-6s1-7s0-8s1` | H3/two | timeout300 | certified | 584.8 | 59.1 |
| 1972 | 2 | `0s0_3s0-6s0__1s0-2s1-4s0-5s0-7s0-8s1` | H3/two | presplit | certified | 85.8 | 34.8 |
| 2016 | 0 | `0s0_3s0-6s0__1s1-2s1-4s1-5s1-7s0-8s1` | H3/two | presplit | certified | 117.9 | 34.7 |
| 2060 | 1 | `0s0_3s0-6s1__1s1-2s0-4s1-5s0-7s0-8s1` | H3/two | timeout300 | certified | 544.3 | 54.9 |
| 2104 | 2 | `0s0_3s0-7s0__1s0-2s1-4s0-5s1-6s0-8s1` | H3/two | presplit | certified | 144.8 | 37.5 |
| 2148 | 0 | `0s0_3s0-7s1__1s0-2s0-4s0-5s0-6s0-8s1` | H3/two | presplit | certified | 209.8 | 43.9 |
| 2192 | 1 | `0s0_3s0-7s1__1s1-2s0-4s1-5s1-6s0-8s1` | H3/two | presplit | certified | 570.5 | 64.5 |
| 2236 | 2 | `0s0_3s0-8s0__1s1-2s0-4s1-5s1-6s1-7s1` | H3/two | presplit | certified | 110.9 | 33.2 |
| 2280 | 0 | `0s0_3s0-8s1__1s1-2s1-4s1-5s1-6s1-7s1` | H3/two | timeout300 | certified | 387.5 | 42.2 |
| 2324 | 1 | `0s0_3s1-4s0__1s1-2s0-5s1-6s1-7s0-8s0` | H3/two | timeout300 | certified | 606.1 | 60.6 |
| 2368 | 2 | `0s0_3s1-4s1__1s0-2s1-5s1-6s0-7s0-8s0` | H3/two | presplit | certified | 53.5 | 26.2 |
| 2412 | 0 | `0s0_3s1-5s0__1s0-2s0-4s0-6s1-7s0-8s0` | H3/two | presplit | certified | 284.8 | 46.2 |
| 2456 | 1 | `0s0_3s1-5s0__1s1-2s1-4s0-6s0-7s0-8s0` | H3/two | presplit | certified | 390.9 | 51.4 |
| 2500 | 2 | `0s0_3s1-5s1__1s0-2s1-4s1-6s1-7s0-8s0` | H3/two | presplit | certified | 74.2 | 30.8 |
| 2544 | 0 | `0s0_3s1-7s0__1s0-2s0-4s0-5s1-6s1-8s0` | H3/two | never_ran | certified | 405.9 | 57.2 |
| 2588 | 1 | `0s0_3s1-7s1__1s0-2s0-4s1-5s0-6s1-8s1` | H3/two | timeout300 | certified | 257.7 | 41.6 |
| 2632 | 2 | `0s0_3s1-8s0__1s0-2s1-4s0-5s1-6s0-7s1` | H3/two | presplit | certified | 280.8 | 43.9 |
| 2676 | 0 | `0s0_4s0-5s1__1s0-2s0-3s0-6s0-7s0-8s1` | H3/two | presplit | certified | 333.1 | 47.9 |
| 2720 | 1 | `0s0_4s0-5s1__1s1-2s0-3s1-6s1-7s0-8s1` | H3/two | presplit | certified | 718.7 | 71.5 |
| 2764 | 2 | `0s0_4s0-6s1__1s0-2s1-3s1-5s0-7s0-8s1` | H3/two | presplit | certified | 650.7 | 90.3 |
| 2808 | 0 | `0s0_4s0-7s0__1s0-2s0-3s0-5s1-6s0-8s1` | H3/two | presplit | certified | 68.8 | 37.4 |
| 2852 | 1 | `0s0_4s0-7s0__1s1-2s1-3s0-5s0-6s0-8s1` | H3/two | presplit | certified | 127.9 | 38.0 |
| 2896 | 2 | `0s0_4s0-7s1__1s1-2s0-3s0-5s1-6s1-8s0` | H3/two | presplit | certified | 480.7 | 57.9 |
| 2940 | 0 | `0s0_4s1-5s0__1s0-2s1-3s0-6s0-7s1-8s0` | H3/two | never_ran | certified | 460.3 | 55.1 |
| 2984 | 1 | `0s0_4s1-5s0__1s1-2s1-3s1-6s1-7s1-8s0` | H3/two | never_ran | certified | 565.6 | 59.1 |
| 3028 | 2 | `0s0_4s1-6s0__1s1-2s0-3s0-5s0-7s0-8s1` | H3/two | presplit | certified | 392.2 | 53.2 |
| 3072 | 0 | `0s0_4s1-6s1__1s0-2s0-3s1-5s1-7s0-8s1` | H3/two | presplit | certified | 76.5 | 33.1 |
| 3116 | 1 | `0s0_4s1-6s1__1s1-2s1-3s1-5s0-7s0-8s1` | H3/two | presplit | certified | 107.6 | 52.8 |
| 3160 | 2 | `0s0_4s1-7s0__1s1-2s0-3s0-5s1-6s0-8s1` | H3/two | presplit | certified | 387.2 | 47.3 |
| 3204 | 0 | `0s0_5s0-6s0__1s0-2s1-3s0-4s0-7s0-8s1` | H3/two | presplit | certified | 20.0 | 19.4 |
| 3248 | 1 | `0s0_5s0-6s0__1s1-2s1-3s1-4s1-7s0-8s1` | H3/two | presplit | certified | 129.1 | 35.5 |
| 3292 | 2 | `0s0_5s0-6s1__1s1-2s0-3s1-4s0-7s0-8s1` | H3/two | presplit | certified | 557.6 | 60.5 |
| 3336 | 0 | `0s0_5s1-6s0__1s1-2s1-3s1-4s0-7s0-8s1` | H3/two | timeout300 | certified | 676.0 | 61.6 |
| 3380 | 1 | `0s0-1s1_5__2s1-3s0-4s0-6s0-7s0-8s0` | H6(1,1)/one | timeout300 | certified | 373.3 | 54.2 |
| 3424 | 2 | `0s0-2s1_3__1s1-4s1-5s1-6s0-7s1-8s0` | H6(2,1)/one | timeout300 | certified | 403.8 | 62.7 |
| 3468 | 0 | `0s0-2s1_5__1s0-3s0-4s1-6s1-7s0-8s1` | H6(2,1)/one | timeout300 | certified | 254.2 | 46.0 |
| 3512 | 1 | `0s0-2s1_6__1s0-3s0-4s0-5s0-7s0-8s1` | H6(2,1)/one | timeout300 | certified | 332.8 | 53.5 |
| 3556 | 2 | `0s0-2s1_6__1s1-3s0-4s1-5s1-7s1-8s1` | H6(2,1)/one | timeout300 | certified | 362.6 | 48.9 |
| 3600 | 0 | `0s0-3s1_4__1s1-2s1-5s0-6s0-7s1-8s1` | H6(3,1)/one | never_ran | certified | 363.5 | 57.1 |
| 3644 | 1 | `0s0-3s1_5__1s0-2s1-4s1-6s1-7s1-8s1` | H6(3,1)/one | presplit | certified | 241.3 | 40.5 |
| 3688 | 2 | `0s0-4s0_6__1s0-2s0-3s1-5s0-7s1-8s1` | H6(4,0)/one | presplit | certified | 69.2 | 36.9 |
| 3732 | 0 | `0s0-4s0_6__1s1-2s1-3s0-5s1-7s1-8s1` | H6(4,0)/one | presplit | certified | 92.5 | 30.7 |
| 3776 | 1 | `0s0-5s0_6__1s0-2s1-3s1-4s1-7s1-8s0` | H6(5,0)/one | presplit | certified | 109.2 | 38.7 |
| 3820 | 2 | `0s0-5s0_7__1s0-2s0-3s1-4s0-6s1-8s0` | H6(5,0)/one | presplit | certified | 123.2 | 35.7 |
| 3864 | 0 | `0s0-5s0_7__1s1-2s1-3s0-4s1-6s1-8s0` | H6(5,0)/one | presplit | certified | 114.9 | 37.8 |
| 3908 | 1 | `0s0-5s1_1__2s1-3s1-4s0-6s0-7s0-8s0` | H6(5,1)/one | presplit | certified | 153.4 | 41.0 |
| 3952 | 2 | `0s0-5s1_2__1s0-3s1-4s1-6s1-7s0-8s0` | H6(5,1)/one | presplit | certified | 188.4 | 42.0 |
| 3996 | 0 | `0s0-5s1_6__1s1-2s0-3s1-4s0-7s0-8s1` | H6(5,1)/one | never_ran | certified | 282.9 | 60.9 |
| 4040 | 1 | `0s0-5s1_1s1-10s1__2s0-3s1-4s1-6s0-7s1-8s1` | H6(5,1)/two | never_ran | certified | 53.8 | 32.6 |
| 4084 | 2 | `0s0-5s1_2s1-3s0__1s1-4s0-6s0-7s1-8s1-9s1` | H6(5,1)/two | never_ran | certified | 47.6 | 33.1 |
