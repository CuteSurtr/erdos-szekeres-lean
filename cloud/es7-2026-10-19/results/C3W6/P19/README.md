# C3W6 P19: shard 19 of 44 of W6.tsv, cap 900, one machine

Task `results/C3W6/TASK.md` at c5260b44, with V = P19, LIST = W6.tsv, j = 19, N = 44, H = 4.5. 4 cores, 15 GB RAM (`env.txt`).
Start 2026-10-25 05:31:47 UTC, END 09:46:47 UTC. The lanes ran from 05:34:08 and finished all units at 07:39:57, well before END. Nothing was killed at END.

## Tools (`tools.txt`)

- C3U2 tools at cad4e050, unmodified (`/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools`); `compose.py` not run.
- CaDiCaL 3.0.1 c6073042; cake_lpr a36874a8 (example: `s VERIFIED UNSAT`); lrat-check 2e3b2dc with the E2 patch. Sanity test passed: LRAT `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF from `gen_case.py 11 7 none`: header `p cnf 168399 4154921` and sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da`, both as required.

## Run

- 93 units (rows of W6.tsv with row ≡ 19 mod 44, `units.tsv`), no seeding. 3 lanes of 31 units each (`lane0.sh` to `lane2.sh`).
- Each unit ran `close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`.
- `out.jsonl` holds 93 records (lane 0, then 1, then 2), one solve record per unit. There are no split records.
- A detached helper (`/opt/work/daemon.sh`, not committed) did the 25-minute syncs for part of the run. It was started because the agent's shell was blocked for a few minutes; it was never needed to stop the lanes.

## Result

**All 93 units are certified** (UNSAT at cap 900, cake_lpr `s VERIFIED UNSAT` and lrat-check `c VERIFIED`). None timed out at 900 s and none were left unreached.

Also:
- no SAT;
- no rejected proof and no cake_lpr `none`, so no re-checks were needed and there is no `recheck.jsonl`;
- no memory problem;
- no unit ended early without a certificate. 22 units finished in under 72 s, all of them certified.

Solve times of the certified units (93): min 11.1, Q1 75.2, median 205.5, Q3 287.4, p90 329.1, max 480.7; above 300 s: 16; under 72 s: 22; total solve 17921 s; total check 3972 s; max check 72.0.

The 26 units that had timed out at 300 s before all closed here, in 154–355 s (median 270 s).

## Totals

| stratum | units | certified | timed out | not reached |
|---|---|---|---|---|
| H3/two | 76 | 76 | 0 | 0 |
| H6(1,1)/one | 2 | 2 | 0 | 0 |
| H6(2,1)/one | 3 | 3 | 0 | 0 |
| H6(3,1)/one | 3 | 3 | 0 | 0 |
| H6(4,0)/one | 1 | 1 | 0 | 0 |
| H6(5,0)/one | 3 | 3 | 0 | 0 |
| H6(5,1)/one | 3 | 3 | 0 | 0 |
| H6(5,1)/two | 2 | 2 | 0 | 0 |

| prior | units | certified | timed out | not reached |
|---|---|---|---|---|
| presplit | 59 | 59 | 0 | 0 |
| timeout300 | 26 | 26 | 0 | 0 |
| never_ran | 8 | 8 | 0 | 0 |


## Per unit

| row | unit | stratum | prior | lane | result | solve s | check s |
|---|---|---|---|---|---|---|---|
| 19 | `0s0_1s0-2s0__3s0-4s0-5s0-6s1-7s1-8s0` | H3/two | presplit | 0 | certified | 26.8 | 32.4 |
| 63 | `0s0_1s0-2s0__3s1-4s1-5s0-6s0-7s1-8s0` | H3/two | presplit | 1 | certified | 32.4 | 38.3 |
| 107 | `0s0_1s0-2s1__3s1-4s0-5s0-6s1-7s0-8s1` | H3/two | timeout300 | 2 | certified | 291.1 | 64.3 |
| 151 | `0s0_1s0-3s1__2s1-4s1-5s0-6s0-7s0-8s1` | H3/two | timeout300 | 0 | certified | 341.2 | 68.1 |
| 195 | `0s0_1s0-4s1__2s1-3s0-5s1-6s0-7s1-8s1` | H3/two | timeout300 | 1 | certified | 335.1 | 72.0 |
| 239 | `0s0_1s0-5s1__2s1-3s1-4s0-6s1-7s0-8s1` | H3/two | timeout300 | 2 | certified | 268.4 | 63.0 |
| 283 | `0s0_1s0-7s0__2s1-3s0-4s1-5s0-6s1-8s1` | H3/two | timeout300 | 0 | certified | 154.2 | 46.2 |
| 327 | `0s0_1s1-2s0__3s0-4s1-5s1-6s0-7s0-8s0` | H3/two | timeout300 | 1 | certified | 286.9 | 52.2 |
| 371 | `0s0_1s1-4s0__2s0-3s1-5s1-6s1-7s0-8s0` | H3/two | timeout300 | 2 | certified | 270.1 | 44.2 |
| 415 | `0s0_1s1-5s0__2s1-3s0-4s1-6s0-7s1-8s1` | H3/two | timeout300 | 0 | certified | 242.6 | 49.0 |
| 459 | `0s0_1s1-5s1__2s0-3s1-4s1-6s0-7s0-8s0` | H3/two | presplit | 1 | certified | 175.2 | 36.7 |
| 503 | `0s0_1s1-7s1__2s0-3s1-4s0-5s0-6s1-8s0` | H3/two | timeout300 | 2 | certified | 240.9 | 47.5 |
| 547 | `0s0_1s1-8s0__2s0-3s0-4s0-5s0-6s0-7s0` | H3/two | presplit | 0 | certified | 75.9 | 33.3 |
| 591 | `0s0_1s1-8s0__2s1-3s0-4s1-5s1-6s0-7s0` | H3/two | presplit | 1 | certified | 65.4 | 33.5 |
| 635 | `0s0_1s1-8s1__2s1-3s1-4s0-5s1-6s0-7s0` | H3/two | timeout300 | 2 | certified | 314.6 | 47.7 |
| 679 | `0s0_1s1-9s1__2s1-3s0-4s1-5s1-6s0-7s1` | H3/two | never_ran | 0 | certified | 480.7 | 58.7 |
| 723 | `0s0_2s0-3s1__1s0-4s1-5s1-6s0-7s0-8s1` | H3/two | presplit | 1 | certified | 339.2 | 55.5 |
| 767 | `0s0_2s0-4s1__1s0-3s0-5s0-6s1-7s0-8s1` | H3/two | presplit | 2 | certified | 261.7 | 46.2 |
| 811 | `0s0_2s0-4s1__1s1-3s1-5s0-6s0-7s0-8s1` | H3/two | presplit | 0 | certified | 349.1 | 54.4 |
| 855 | `0s0_2s0-5s0__1s0-3s1-4s1-6s1-7s0-8s1` | H3/two | presplit | 1 | certified | 53.8 | 45.8 |
| 899 | `0s0_2s0-5s1__1s0-3s1-4s0-6s0-7s0-8s0` | H3/two | timeout300 | 2 | certified | 215.3 | 41.6 |
| 943 | `0s0_2s0-5s1__1s1-3s1-4s1-6s1-7s0-8s0` | H3/two | timeout300 | 0 | certified | 327.6 | 48.8 |
| 987 | `0s0_2s0-6s1__1s1-3s0-4s1-5s0-7s1-8s0` | H3/two | timeout300 | 1 | certified | 255.9 | 45.8 |
| 1031 | `0s0_2s0-7s0__1s0-3s1-4s0-5s1-6s1-8s0` | H3/two | presplit | 2 | certified | 74.6 | 35.2 |
| 1075 | `0s0_2s0-7s1__1s0-3s0-4s0-5s0-6s1-8s0` | H3/two | presplit | 0 | certified | 131.6 | 37.2 |
| 1119 | `0s0_2s0-7s1__1s1-3s0-4s1-5s1-6s1-8s0` | H3/two | presplit | 1 | certified | 214.7 | 41.1 |
| 1163 | `0s0_2s0-8s0__1s1-3s0-4s1-5s1-6s0-7s0` | H3/two | presplit | 2 | certified | 163.7 | 37.6 |
| 1207 | `0s0_2s1-3s0__1s0-4s1-5s1-6s0-7s0-8s1` | H3/two | timeout300 | 0 | certified | 293.0 | 48.4 |
| 1251 | `0s0_2s1-3s1__1s0-4s0-5s0-6s1-7s0-8s1` | H3/two | presplit | 1 | certified | 61.3 | 28.9 |
| 1295 | `0s0_2s1-3s1__1s1-4s1-5s0-6s0-7s0-8s1` | H3/two | presplit | 2 | certified | 47.4 | 26.3 |
| 1339 | `0s0_2s1-4s0__1s1-3s0-5s0-6s0-7s1-8s1` | H3/two | timeout300 | 0 | certified | 309.7 | 46.7 |
| 1383 | `0s0_2s1-5s0__1s0-3s0-4s1-6s1-7s1-8s1` | H3/two | presplit | 1 | certified | 226.0 | 54.9 |
| 1427 | `0s0_2s1-5s0__1s1-3s1-4s1-6s0-7s1-8s1` | H3/two | presplit | 2 | certified | 426.9 | 53.0 |
| 1471 | `0s0_2s1-6s0__1s1-3s0-4s0-5s1-7s1-8s1` | H3/two | presplit | 0 | certified | 289.8 | 45.2 |
| 1515 | `0s0_2s1-6s1__1s0-3s1-4s0-5s0-7s1-8s1` | H3/two | presplit | 1 | certified | 112.7 | 33.8 |
| 1559 | `0s0_2s1-6s1__1s1-3s1-4s1-5s1-7s1-8s1` | H3/two | presplit | 2 | certified | 182.7 | 37.1 |
| 1603 | `0s0_2s1-7s0__1s1-3s1-4s0-5s0-6s1-8s1` | H3/two | never_ran | 0 | certified | 194.6 | 39.8 |
| 1647 | `0s0_2s1-7s1__1s1-3s1-4s1-5s0-6s0-8s1` | H3/two | never_ran | 1 | certified | 197.6 | 38.1 |
| 1691 | `0s0_2s1-8s1__1s1-3s0-4s1-5s1-6s1-7s0` | H3/two | presplit | 2 | certified | 287.3 | 48.0 |
| 1735 | `0s0_2s1-9s0__1s0-3s1-4s1-5s0-6s1-7s0` | H3/two | presplit | 0 | certified | 57.8 | 29.7 |
| 1779 | `0s0_3s0-4s1__1s0-2s0-5s0-6s1-7s1-8s0` | H3/two | presplit | 1 | certified | 244.9 | 41.2 |
| 1823 | `0s0_3s0-4s1__1s1-2s1-5s0-6s0-7s1-8s0` | H3/two | presplit | 2 | certified | 317.0 | 66.1 |
| 1867 | `0s0_3s0-5s0__1s0-2s1-4s1-6s1-7s1-8s0` | H3/two | presplit | 0 | certified | 41.3 | 28.8 |
| 1911 | `0s0_3s0-5s1__1s0-2s1-4s0-6s1-7s0-8s0` | H3/two | timeout300 | 1 | certified | 276.1 | 46.7 |
| 1955 | `0s0_3s0-6s0__1s0-2s0-4s0-5s0-7s0-8s0` | H3/two | presplit | 2 | certified | 33.0 | 25.5 |
| 1999 | `0s0_3s0-6s0__1s1-2s0-4s1-5s1-7s0-8s0` | H3/two | presplit | 0 | certified | 46.9 | 28.7 |
| 2043 | `0s0_3s0-6s1__1s0-2s1-4s1-5s0-7s0-8s0` | H3/two | timeout300 | 1 | certified | 270.6 | 46.5 |
| 2087 | `0s0_3s0-7s0__1s0-2s0-4s0-5s1-6s0-8s0` | H3/two | presplit | 2 | certified | 45.5 | 29.5 |
| 2131 | `0s0_3s0-7s0__1s1-2s1-4s0-5s0-6s0-8s0` | H3/two | presplit | 0 | certified | 101.6 | 50.2 |
| 2175 | `0s0_3s0-7s1__1s0-2s1-4s1-5s1-6s0-8s0` | H3/two | presplit | 1 | certified | 287.5 | 46.3 |
| 2219 | `0s0_3s0-8s0__1s0-2s1-4s1-5s1-6s1-7s0` | H3/two | presplit | 2 | certified | 96.5 | 30.7 |
| 2263 | `0s0_3s0-8s1__1s0-2s1-4s1-5s1-6s1-7s0` | H3/two | timeout300 | 0 | certified | 274.2 | 59.6 |
| 2307 | `0s0_3s1-4s0__1s0-2s1-5s1-6s0-7s1-8s1` | H3/two | timeout300 | 1 | certified | 354.8 | 50.7 |
| 2351 | `0s0_3s1-4s1__1s0-2s0-5s0-6s1-7s1-8s1` | H3/two | presplit | 2 | certified | 86.5 | 30.1 |
| 2395 | `0s0_3s1-4s1__1s1-2s1-5s0-6s0-7s1-8s1` | H3/two | presplit | 0 | certified | 62.9 | 42.3 |
| 2439 | `0s0_3s1-5s0__1s0-2s1-4s1-6s1-7s1-8s1` | H3/two | presplit | 1 | certified | 297.8 | 41.8 |
| 2483 | `0s0_3s1-5s1__1s0-2s0-4s1-6s0-7s1-8s1` | H3/two | presplit | 2 | certified | 84.4 | 30.4 |
| 2527 | `0s0_3s1-5s1__1s1-2s1-4s0-6s1-7s1-8s1` | H3/two | presplit | 0 | certified | 51.4 | 32.6 |
| 2571 | `0s0_3s1-7s0__1s1-2s1-4s0-5s0-6s0-8s1` | H3/two | never_ran | 1 | certified | 231.0 | 40.7 |
| 2615 | `0s0_3s1-8s0__1s0-2s0-4s0-5s1-6s0-7s0` | H3/two | presplit | 2 | certified | 87.1 | 32.5 |
| 2659 | `0s0_3s1-8s0__1s1-2s1-4s0-5s0-6s0-7s0` | H3/two | presplit | 0 | certified | 180.6 | 50.8 |
| 2703 | `0s0_4s0-5s1__1s0-2s1-3s1-6s1-7s0-8s0` | H3/two | presplit | 1 | certified | 316.6 | 49.1 |
| 2747 | `0s0_4s0-6s1__1s0-2s0-3s1-5s0-7s0-8s0` | H3/two | presplit | 2 | certified | 205.5 | 40.6 |
| 2791 | `0s0_4s0-6s1__1s1-2s1-3s0-5s1-7s0-8s0` | H3/two | presplit | 0 | certified | 310.6 | 47.0 |
| 2835 | `0s0_4s0-7s0__1s1-2s0-3s0-5s0-6s0-8s0` | H3/two | presplit | 1 | certified | 45.2 | 31.3 |
| 2879 | `0s0_4s0-7s1__1s0-2s1-3s0-5s1-6s0-8s1` | H3/two | presplit | 2 | certified | 311.4 | 53.8 |
| 2923 | `0s0_4s1-5s0__1s0-2s0-3s0-6s0-7s0-8s1` | H3/two | never_ran | 0 | certified | 171.4 | 41.6 |
| 2967 | `0s0_4s1-5s0__1s1-2s0-3s1-6s1-7s0-8s1` | H3/two | never_ran | 1 | certified | 468.0 | 56.0 |
| 3011 | `0s0_4s1-6s0__1s0-2s1-3s0-5s0-7s0-8s0` | H3/two | presplit | 2 | certified | 186.6 | 39.5 |
| 3055 | `0s0_4s1-6s0__1s1-2s1-3s1-5s1-7s0-8s0` | H3/two | presplit | 0 | certified | 293.1 | 47.3 |
| 3099 | `0s0_4s1-6s1__1s1-2s0-3s1-5s0-7s0-8s0` | H3/two | presplit | 1 | certified | 118.6 | 31.8 |
| 3143 | `0s0_4s1-7s0__1s0-2s1-3s0-5s1-6s0-8s0` | H3/two | presplit | 2 | certified | 258.4 | 45.8 |
| 3187 | `0s0_5s0-6s0__1s0-2s0-3s0-4s0-7s0-8s0` | H3/two | presplit | 0 | certified | 11.1 | 18.9 |
| 3231 | `0s0_5s0-6s0__1s1-2s0-3s1-4s1-7s0-8s0` | H3/two | presplit | 1 | certified | 36.0 | 20.9 |
| 3275 | `0s0_5s0-6s1__1s0-2s1-3s1-4s0-7s0-8s0` | H3/two | presplit | 2 | certified | 289.5 | 47.5 |
| 3319 | `0s0_5s1-6s0__1s1-2s0-3s0-4s1-7s1-8s1` | H3/two | timeout300 | 0 | certified | 330.1 | 47.4 |
| 3363 | `0s0-1s1_5__2s0-3s0-4s0-6s1-7s1-8s1` | H6(1,1)/one | timeout300 | 1 | certified | 262.8 | 48.4 |
| 3407 | `0s0-1s1_5__2s1-3s1-4s1-6s0-7s1-8s1` | H6(1,1)/one | timeout300 | 2 | certified | 191.1 | 53.9 |
| 3451 | `0s0-2s1_4__1s1-3s1-5s1-6s0-7s0-8s1` | H6(2,1)/one | timeout300 | 0 | certified | 221.2 | 42.5 |
| 3495 | `0s0-2s1_5__1s1-3s1-4s0-6s0-7s0-8s0` | H6(2,1)/one | timeout300 | 1 | certified | 222.6 | 49.7 |
| 3539 | `0s0-2s1_6__1s0-3s1-4s1-5s1-7s1-8s0` | H6(2,1)/one | timeout300 | 2 | certified | 172.8 | 48.7 |
| 3583 | `0s0-3s1_4__1s0-2s1-5s1-6s1-7s1-8s0` | H6(3,1)/one | timeout300 | 0 | certified | 251.1 | 61.6 |
| 3627 | `0s0-3s1_5__1s0-2s0-4s1-6s1-7s1-8s0` | H6(3,1)/one | presplit | 1 | certified | 228.6 | 41.7 |
| 3671 | `0s0-3s1_5__1s1-2s1-4s1-6s0-7s1-8s0` | H6(3,1)/one | presplit | 2 | certified | 218.1 | 40.0 |
| 3715 | `0s0-4s0_6__1s1-2s0-3s0-5s1-7s1-8s0` | H6(4,0)/one | presplit | 0 | certified | 53.7 | 34.7 |
| 3759 | `0s0-5s0_6__1s0-2s0-3s1-4s1-7s0-8s1` | H6(5,0)/one | presplit | 1 | certified | 50.6 | 33.9 |
| 3803 | `0s0-5s0_6__1s1-2s1-3s1-4s0-7s0-8s1` | H6(5,0)/one | presplit | 2 | certified | 56.7 | 34.2 |
| 3847 | `0s0-5s0_7__1s1-2s0-3s0-4s1-6s0-8s1` | H6(5,0)/one | presplit | 0 | certified | 38.7 | 29.7 |
| 3891 | `0s0-5s1_1__2s0-3s1-4s1-6s1-7s1-8s1` | H6(5,1)/one | presplit | 1 | certified | 108.1 | 35.9 |
| 3935 | `0s0-5s1_2__1s0-3s0-4s1-6s0-7s1-8s1` | H6(5,1)/one | presplit | 2 | certified | 96.5 | 36.5 |
| 3979 | `0s0-5s1_2__1s1-3s1-4s0-6s1-7s1-8s1` | H6(5,1)/one | presplit | 0 | certified | 178.6 | 48.0 |
| 4023 | `0s0-5s1_1s1-10s1__2s0-3s0-4s1-6s0-7s1-8s0` | H6(5,1)/two | never_ran | 1 | certified | 19.7 | 26.2 |
| 4067 | `0s0-5s1_1s1-10s1__2s1-3s1-4s0-6s1-7s1-8s0` | H6(5,1)/two | never_ran | 2 | certified | 50.6 | 30.4 |

