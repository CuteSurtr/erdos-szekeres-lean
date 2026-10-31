# C3W6 P24: shard 24 of 44 of W6.tsv, cap 900, 3 lanes

Task `results/C3W6/TASK.md` at c5260b44, with V = P24, LIST = W6.tsv, j = 24, N = 44, H = 4.5.
One cloud VM (4 cores, 15 GB, no swap; `env.txt`). Start 05:31:48 UTC, END 09:46:48 UTC. All 3 lanes finished their
units before END (lane 0 at 08:24:42, lane 1 at 08:49:49, lane 2 at 08:52:47), so nothing was killed.

## Result

**All 93 units certified** at cap 900. No timeouts, no split records, no SAT, no proof rejections, no re-checks
(no `recheck.jsonl`), no memory problems, and no unit ended early without a certificate. Each unit has exactly one record
in `out.jsonl` with `UNSATISFIABLE`, lrat-check `c VERIFIED`, cake_lpr `s VERIFIED UNSAT`, `certified: true` and the base
sha256 below. `compose.py` was not run.

## Tools

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, used unmodified
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (example: `s VERIFIED UNSAT`);
  lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 + E2 patch; sanity test passed (`3 0 0` rejected by both, `3 0 1 2 0` accepted by both)
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches)

Details are in `tools.txt`. Each unit was run as
`close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`
(`lane0.sh`, `lane1.sh`, `lane2.sh`).

## Solve times of the certified units (93)

| | min | q1 | median | q3 | p90 | max |
|---|---|---|---|---|---|---|
| solve s | 19.3 | 128.9 | 310.4 | 466.1 | 544.5 | 747.2 |

48 of the 93 units were certified above 300 s. Check times ran from 18.1 s to 81.2 s (median 50.9 s). Totals: 28,818 s of solving and 4,684 s of checking.

## Totals per stratum and prior

| stratum | prior | units | certified | timed out | not reached | solve s | check s |
|---|---|---|---|---|---|---|---|
| H3/two | never_ran | 7 | 7 | 0 | 0 | 3022 | 376 |
| H3/two | presplit | 49 | 49 | 0 | 0 | 12791 | 2312 |
| H3/two | timeout300 | 20 | 20 | 0 | 0 | 8901 | 1264 |
| H6(1,1)/one | timeout300 | 1 | 1 | 0 | 0 | 293 | 45 |
| H6(2,1)/one | timeout300 | 4 | 4 | 0 | 0 | 1581 | 199 |
| H6(3,1)/one | never_ran | 1 | 1 | 0 | 0 | 364 | 58 |
| H6(3,1)/one | presplit | 2 | 2 | 0 | 0 | 574 | 90 |
| H6(4,0)/one | presplit | 1 | 1 | 0 | 0 | 56 | 29 |
| H6(5,0)/one | presplit | 3 | 3 | 0 | 0 | 327 | 120 |
| H6(5,1)/one | presplit | 3 | 3 | 0 | 0 | 827 | 132 |
| H6(5,1)/two | never_ran | 2 | 2 | 0 | 0 | 82 | 57 |
| **total** | | **93** | **93** | **0** | **0** | **28818** | **4684** |

By stratum: H3/two 76 out of 76, one-orbit H6 15 out of 15, two-orbit H6 2 out of 2 (both are 3-bit cubes).

## Per unit

| row | lane | node | stratum | prior | result | solve s | check s |
|---|---|---|---|---|---|---|---|
| 24 | 0 | `0s0_1s0-2s0__3s0-4s0-5s1-6s0-7s1-8s1` | H3/two | presplit | certified | 31.5 | 46.8 |
| 68 | 1 | `0s0_1s0-2s0__3s1-4s1-5s0-6s1-7s1-8s1` | H3/two | presplit | certified | 39.9 | 49.5 |
| 112 | 2 | `0s0_1s0-2s1__3s1-4s0-5s1-6s0-7s1-8s0` | H3/two | timeout300 | certified | 536.1 | 61.8 |
| 156 | 0 | `0s0_1s0-3s1__2s1-4s1-5s1-6s0-7s0-8s1` | H3/two | timeout300 | certified | 547.6 | 71.7 |
| 200 | 1 | `0s0_1s0-4s1__2s1-3s1-5s0-6s0-7s0-8s0` | H3/two | timeout300 | certified | 398.6 | 67.6 |
| 244 | 2 | `0s0_1s0-5s1__2s1-3s1-4s1-6s0-7s1-8s0` | H3/two | timeout300 | certified | 481.7 | 70.1 |
| 288 | 0 | `0s0_1s0-7s0__2s1-3s1-4s0-5s0-6s0-8s0` | H3/two | timeout300 | certified | 194.4 | 55.2 |
| 332 | 1 | `0s0_1s1-2s0__3s0-4s1-5s1-6s1-7s0-8s1` | H3/two | timeout300 | certified | 552.1 | 81.2 |
| 376 | 2 | `0s0_1s1-4s0__2s1-3s0-5s1-6s1-7s0-8s0` | H3/two | timeout300 | certified | 422.2 | 59.1 |
| 420 | 0 | `0s0_1s1-5s0__2s1-3s1-4s0-6s0-7s0-8s0` | H3/two | timeout300 | certified | 294.3 | 62.2 |
| 464 | 1 | `0s0_1s1-5s1__2s0-3s1-4s1-6s1-7s0-8s1` | H3/two | presplit | certified | 298.6 | 55.6 |
| 508 | 2 | `0s0_1s1-7s1__2s0-3s1-4s0-5s1-6s1-8s1` | H3/two | timeout300 | certified | 460.9 | 60.5 |
| 552 | 0 | `0s0_1s1-8s0__2s0-3s0-4s0-5s1-6s0-7s1` | H3/two | presplit | certified | 152.0 | 51.8 |
| 596 | 1 | `0s0_1s1-8s0__2s1-3s1-4s0-5s0-6s0-7s1` | H3/two | presplit | certified | 110.8 | 46.5 |
| 640 | 2 | `0s0_1s1-8s1__2s1-3s1-4s1-5s0-6s0-7s1` | H3/two | timeout300 | certified | 538.1 | 68.4 |
| 684 | 0 | `0s0_1s1-9s1__2s1-3s1-4s0-5s0-6s1-7s0` | H3/two | never_ran | certified | 539.9 | 63.4 |
| 728 | 1 | `0s0_2s0-3s1__1s0-4s1-5s1-6s1-7s1-8s0` | H3/two | presplit | certified | 485.6 | 63.0 |
| 772 | 2 | `0s0_2s0-4s1__1s0-3s0-5s1-6s0-7s1-8s0` | H3/two | presplit | certified | 464.9 | 59.0 |
| 816 | 0 | `0s0_2s0-4s1__1s1-3s1-5s0-6s1-7s1-8s0` | H3/two | presplit | certified | 539.9 | 65.5 |
| 860 | 1 | `0s0_2s0-5s0__1s1-3s0-4s0-6s0-7s1-8s0` | H3/two | presplit | certified | 129.0 | 46.1 |
| 904 | 2 | `0s0_2s0-5s1__1s0-3s1-4s0-6s1-7s0-8s1` | H3/two | timeout300 | certified | 488.1 | 79.3 |
| 948 | 0 | `0s0_2s0-6s1__1s0-3s0-4s0-5s0-7s1-8s0` | H3/two | timeout300 | certified | 254.5 | 52.7 |
| 992 | 1 | `0s0_2s0-6s1__1s1-3s0-4s1-5s1-7s1-8s1` | H3/two | timeout300 | certified | 445.1 | 55.9 |
| 1036 | 2 | `0s0_2s0-7s0__1s0-3s1-4s1-5s0-6s1-8s1` | H3/two | presplit | certified | 121.7 | 32.2 |
| 1080 | 0 | `0s0_2s0-7s1__1s0-3s0-4s0-5s1-6s1-8s1` | H3/two | presplit | certified | 222.2 | 54.3 |
| 1124 | 1 | `0s0_2s0-7s1__1s1-3s1-4s0-5s0-6s1-8s1` | H3/two | presplit | certified | 312.2 | 61.5 |
| 1168 | 2 | `0s0_2s0-8s0__1s1-3s1-4s0-5s0-6s0-7s1` | H3/two | presplit | certified | 228.1 | 41.7 |
| 1212 | 0 | `0s0_2s1-3s0__1s0-4s1-5s1-6s1-7s1-8s0` | H3/two | timeout300 | certified | 349.9 | 49.5 |
| 1256 | 1 | `0s0_2s1-3s1__1s0-4s0-5s1-6s0-7s1-8s0` | H3/two | presplit | certified | 69.8 | 30.3 |
| 1300 | 2 | `0s0_2s1-3s1__1s1-4s1-5s0-6s1-7s1-8s0` | H3/two | presplit | certified | 61.3 | 32.1 |
| 1344 | 0 | `0s0_2s1-4s0__1s1-3s0-5s1-6s0-7s0-8s0` | H3/two | timeout300 | certified | 443.4 | 48.9 |
| 1388 | 1 | `0s0_2s1-5s0__1s0-3s1-4s0-6s1-7s0-8s0` | H3/two | presplit | certified | 362.7 | 46.3 |
| 1432 | 2 | `0s0_2s1-6s0__1s0-3s0-4s0-5s0-7s0-8s0` | H3/two | presplit | certified | 159.1 | 35.9 |
| 1476 | 0 | `0s0_2s1-6s0__1s1-3s0-4s1-5s1-7s0-8s0` | H3/two | presplit | certified | 409.4 | 66.6 |
| 1520 | 1 | `0s0_2s1-6s1__1s0-3s1-4s1-5s0-7s0-8s0` | H3/two | presplit | certified | 255.9 | 41.1 |
| 1564 | 2 | `0s0_2s1-7s0__1s0-3s0-4s0-5s1-6s0-8s0` | H3/two | never_ran | certified | 172.1 | 37.4 |
| 1608 | 0 | `0s0_2s1-7s0__1s1-3s1-4s1-5s0-6s0-8s0` | H3/two | never_ran | certified | 246.6 | 45.1 |
| 1652 | 1 | `0s0_2s1-7s1__1s1-3s1-4s1-5s1-6s1-8s0` | H3/two | never_ran | certified | 475.4 | 50.9 |
| 1696 | 2 | `0s0_2s1-8s1__1s1-3s1-4s0-5s0-6s1-7s1` | H3/two | presplit | certified | 570.1 | 58.4 |
| 1740 | 0 | `0s0_2s1-9s0__1s0-3s1-4s1-5s1-6s1-7s1` | H3/two | presplit | certified | 167.0 | 55.2 |
| 1784 | 1 | `0s0_3s0-4s1__1s0-2s0-5s1-6s0-7s1-8s1` | H3/two | presplit | certified | 468.1 | 55.0 |
| 1828 | 2 | `0s0_3s0-4s1__1s1-2s1-5s0-6s1-7s1-8s1` | H3/two | presplit | certified | 652.1 | 62.4 |
| 1872 | 0 | `0s0_3s0-5s0__1s1-2s0-4s0-6s0-7s1-8s1` | H3/two | presplit | certified | 54.7 | 28.3 |
| 1916 | 1 | `0s0_3s0-5s1__1s0-2s1-4s1-6s0-7s0-8s1` | H3/two | timeout300 | certified | 526.7 | 78.2 |
| 1960 | 2 | `0s0_3s0-6s0__1s0-2s0-4s0-5s1-7s0-8s1` | H3/two | presplit | certified | 49.9 | 28.1 |
| 2004 | 0 | `0s0_3s0-6s0__1s1-2s1-4s0-5s0-7s0-8s1` | H3/two | presplit | certified | 146.6 | 36.8 |
| 2048 | 1 | `0s0_3s0-6s1__1s0-2s1-4s1-5s1-7s0-8s1` | H3/two | timeout300 | certified | 627.2 | 60.3 |
| 2092 | 2 | `0s0_3s0-7s0__1s0-2s0-4s1-5s0-6s0-8s1` | H3/two | presplit | certified | 113.3 | 57.4 |
| 2136 | 0 | `0s0_3s0-7s0__1s1-2s1-4s0-5s1-6s0-8s1` | H3/two | presplit | certified | 225.4 | 40.3 |
| 2180 | 1 | `0s0_3s0-7s1__1s1-2s0-4s0-5s0-6s0-8s1` | H3/two | presplit | certified | 394.0 | 57.5 |
| 2224 | 2 | `0s0_3s0-8s0__1s1-2s0-4s0-5s0-6s1-7s1` | H3/two | presplit | certified | 170.8 | 35.6 |
| 2268 | 0 | `0s0_3s0-8s1__1s1-2s0-4s1-5s1-6s1-7s0` | H3/two | timeout300 | certified | 447.0 | 70.1 |
| 2312 | 1 | `0s0_3s1-4s0__1s1-2s0-5s0-6s0-7s0-8s0` | H3/two | timeout300 | certified | 356.6 | 44.7 |
| 2356 | 2 | `0s0_3s1-4s1__1s0-2s0-5s1-6s1-7s0-8s0` | H3/two | presplit | certified | 77.7 | 30.9 |
| 2400 | 0 | `0s0_3s1-4s1__1s1-2s1-5s1-6s0-7s0-8s0` | H3/two | presplit | certified | 70.3 | 33.2 |
| 2444 | 1 | `0s0_3s1-5s0__1s1-2s0-4s0-6s1-7s0-8s0` | H3/two | presplit | certified | 446.0 | 53.4 |
| 2488 | 2 | `0s0_3s1-5s1__1s0-2s1-4s0-6s0-7s0-8s0` | H3/two | presplit | certified | 125.0 | 32.8 |
| 2532 | 0 | `0s0_3s1-5s1__1s1-2s1-4s1-6s1-7s0-8s0` | H3/two | presplit | certified | 79.1 | 51.2 |
| 2576 | 1 | `0s0_3s1-7s0__1s1-2s1-4s0-5s1-6s1-8s0` | H3/two | never_ran | certified | 522.6 | 57.7 |
| 2620 | 2 | `0s0_3s1-8s0__1s0-2s0-4s1-5s0-6s0-7s1` | H3/two | presplit | certified | 166.6 | 36.6 |
| 2664 | 0 | `0s0_3s1-8s0__1s1-2s1-4s0-5s1-6s0-7s1` | H3/two | presplit | certified | 340.5 | 58.7 |
| 2708 | 1 | `0s0_4s0-5s1__1s1-2s0-3s0-6s0-7s0-8s1` | H3/two | presplit | certified | 421.9 | 53.9 |
| 2752 | 2 | `0s0_4s0-6s1__1s0-2s0-3s1-5s1-7s0-8s1` | H3/two | presplit | certified | 467.3 | 52.5 |
| 2796 | 0 | `0s0_4s0-6s1__1s1-2s1-3s1-5s0-7s0-8s1` | H3/two | presplit | certified | 597.3 | 55.9 |
| 2840 | 1 | `0s0_4s0-7s0__1s1-2s0-3s0-5s1-6s0-8s1` | H3/two | presplit | certified | 79.0 | 36.9 |
| 2884 | 2 | `0s0_4s0-7s1__1s0-2s1-3s1-5s0-6s1-8s0` | H3/two | presplit | certified | 449.4 | 48.8 |
| 2928 | 0 | `0s0_4s1-5s0__1s0-2s0-3s0-6s1-7s1-8s0` | H3/two | never_ran | certified | 360.8 | 48.5 |
| 2972 | 1 | `0s0_4s1-5s0__1s1-2s1-3s0-6s0-7s1-8s0` | H3/two | never_ran | certified | 704.3 | 73.0 |
| 3016 | 2 | `0s0_4s1-6s0__1s0-2s1-3s0-5s1-7s0-8s1` | H3/two | presplit | certified | 564.6 | 59.1 |
| 3060 | 0 | `0s0_4s1-6s1__1s0-2s0-3s0-5s0-7s0-8s1` | H3/two | presplit | certified | 114.4 | 35.7 |
| 3104 | 1 | `0s0_4s1-6s1__1s1-2s0-3s1-5s1-7s0-8s1` | H3/two | presplit | certified | 131.3 | 44.6 |
| 3148 | 2 | `0s0_4s1-7s0__1s0-2s1-3s1-5s0-6s0-8s1` | H3/two | presplit | certified | 403.5 | 62.5 |
| 3192 | 0 | `0s0_5s0-6s0__1s0-2s0-3s0-4s1-7s0-8s1` | H3/two | presplit | certified | 19.3 | 18.1 |
| 3236 | 1 | `0s0_5s0-6s0__1s1-2s1-3s0-4s0-7s0-8s1` | H3/two | presplit | certified | 23.9 | 30.0 |
| 3280 | 2 | `0s0_5s0-6s1__1s0-2s1-3s1-4s1-7s0-8s1` | H3/two | presplit | certified | 747.2 | 76.3 |
| 3324 | 0 | `0s0_5s1-6s0__1s1-2s0-3s1-4s1-7s0-8s0` | H3/two | timeout300 | certified | 536.1 | 66.9 |
| 3368 | 1 | `0s0-1s1_5__2s0-3s0-4s1-6s1-7s0-8s0` | H6(1,1)/one | timeout300 | certified | 293.0 | 44.7 |
| 3412 | 2 | `0s0-2s1_3__1s1-4s0-5s0-6s0-7s0-8s0` | H6(2,1)/one | timeout300 | certified | 425.5 | 53.9 |
| 3456 | 0 | `0s0-2s1_5__1s0-3s0-4s0-6s0-7s0-8s0` | H6(2,1)/one | timeout300 | certified | 341.3 | 44.9 |
| 3500 | 1 | `0s0-2s1_5__1s1-3s1-4s0-6s1-7s0-8s1` | H6(2,1)/one | timeout300 | certified | 341.7 | 48.0 |
| 3544 | 2 | `0s0-2s1_6__1s1-3s0-4s0-5s0-7s1-8s1` | H6(2,1)/one | timeout300 | certified | 472.4 | 52.1 |
| 3588 | 0 | `0s0-3s1_4__1s1-2s0-5s0-6s1-7s1-8s1` | H6(3,1)/one | never_ran | certified | 363.5 | 58.4 |
| 3632 | 1 | `0s0-3s1_5__1s0-2s1-4s0-6s0-7s1-8s1` | H6(3,1)/one | presplit | certified | 268.9 | 46.7 |
| 3676 | 2 | `0s0-3s1_5__1s1-2s1-4s1-6s1-7s1-8s1` | H6(3,1)/one | presplit | certified | 305.5 | 43.7 |
| 3720 | 0 | `0s0-4s0_6__1s1-2s0-3s1-5s0-7s1-8s1` | H6(4,0)/one | presplit | certified | 55.9 | 29.3 |
| 3764 | 1 | `0s0-5s0_6__1s0-2s1-3s0-4s0-7s1-8s0` | H6(5,0)/one | presplit | certified | 103.4 | 46.3 |
| 3808 | 2 | `0s0-5s0_6__1s1-2s1-3s1-4s1-7s1-8s0` | H6(5,0)/one | presplit | certified | 95.1 | 33.9 |
| 3852 | 0 | `0s0-5s0_7__1s1-2s0-3s1-4s0-6s1-8s0` | H6(5,0)/one | presplit | certified | 128.9 | 40.1 |
| 3896 | 1 | `0s0-5s1_1__2s1-3s0-4s0-6s1-7s0-8s0` | H6(5,1)/one | presplit | certified | 310.4 | 48.4 |
| 3940 | 2 | `0s0-5s1_2__1s0-3s1-4s0-6s0-7s0-8s0` | H6(5,1)/one | presplit | certified | 233.5 | 40.8 |
| 3984 | 0 | `0s0-5s1_2__1s1-3s1-4s1-6s1-7s0-8s0` | H6(5,1)/one | presplit | certified | 283.2 | 43.3 |
| 4028 | 1 | `0s0-5s1_1s1-10s1__2s0-3s0-4s1-6s1-7s1-8s1` | H6(5,1)/two | never_ran | certified | 46.8 | 32.4 |
| 4072 | 2 | `0s0-5s1_1s1-10s1__2s1-3s1-4s1-6s0-7s1-8s1` | H6(5,1)/two | never_ran | certified | 35.6 | 24.7 |
