# C3W6 P16: shard 16 of 44 of W6.tsv

One cloud VM with 4 cores, 15 GB RAM and no swap (`env.txt`). Ran from 05:31:35 to 09:46:35 UTC on 2026-10-25 (END = start + 4.5 h − 15 min). Task: `results/C3W6/TASK.md` at c5260b44, with V = P16, LIST = W6.tsv, j = 16, N = 44, H = 4.5.

## Tools and base CNF (`tools.txt`)

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 c60730422e75; cake_lpr a36874a8b750 (its example gives `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc0ecf9 with the E2 patch. Sanity check passed: on {1},{-1}, LRAT `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF from `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 bf0e502e…dd6da, which matches.

## Run

- 94 units: the rows of W6.tsv with row ≡ 16 (mod 44), listed in `units.tsv`. Nothing was seeded.
- 3 lanes (`lane0.sh` to `lane2.sh`, each started with `setsid nohup`). Lane k took unit positions ≡ k (mod 3). Each unit ran `close_tree.py … U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`.
- At END the three lane process groups were killed. Each lane was then partway through a solve, so 3 units have no record. They count as not reached.
- `out.jsonl` holds the records of lane 0, then lane 1, then lane 2. The `driver{k}.log.tail` files hold the last 100 lines of each driver log.

## Outcome

- **No SAT. No proof rejected.** All 52 UNSAT records were accepted by both lrat-check (`c VERIFIED`) and cake_lpr (`s VERIFIED UNSAT`). No record has cake_lpr `none`, so no re-check was needed and there is no `recheck.jsonl`.
- No unit ended early (under 72 s without a certificate). No unsplittable node. No memory problem: at most 6 GB was in use.
- 94 units: **52 certified**, **16 timed out at 900 s**, 3 killed at END, 23 not reached. The unreached units include all 18 H6 units, which come last in the list.
- Each of the 16 timeouts got its layer split written (51 children each). The children were left unsolved, as intended, so they are open.
- Certified solve times: n=52, min 53.6, Q1 213.1, median 582.8, Q3 783.9, p90 869.8, max 899.6; certified above 300 s: 32.
- 26272 s solve and 3674 s check in total over the certified units.

## Totals per stratum and per prior

| group | certified | timeout900 | killed at END | not reached | other |
|---|---|---|---|---|---|
| prior never_ran | 3 | 1 | 1 | 2 | 0 |
| prior presplit | 33 | 10 | 2 | 14 | 0 |
| prior timeout300 | 16 | 5 | 0 | 7 | 0 |
| stratum H3/two | 52 | 16 | 3 | 5 | 0 |
| stratum H6(1,1)/one | 0 | 0 | 0 | 2 | 0 |
| stratum H6(2,1)/one | 0 | 0 | 0 | 3 | 0 |
| stratum H6(3,1)/one | 0 | 0 | 0 | 3 | 0 |
| stratum H6(4,0)/one | 0 | 0 | 0 | 1 | 0 |
| stratum H6(5,0)/one | 0 | 0 | 0 | 3 | 0 |
| stratum H6(5,1)/one | 0 | 0 | 0 | 3 | 0 |
| stratum H6(5,1)/two | 0 | 0 | 0 | 3 | 0 |

## Per unit

| row | node | stratum | prior | result | detail |
|---|---|---|---|---|---|
| 16 | 0s0_1s0-2s0__3s0-4s0-5s0-6s0-7s1-8s1 | H3/two | presplit | certified | 53.6 s solve, 61.5 s check |
| 60 | 0s0_1s0-2s0__3s1-4s0-5s1-6s1-7s1-8s1 | H3/two | presplit | certified | 54.8 s solve, 69.0 s check |
| 104 | 0s0_1s0-2s1__3s1-4s0-5s0-6s0-7s1-8s0 | H3/two | timeout300 | certified | 733.4 s solve, 87.7 s check |
| 148 | 0s0_1s0-3s1__2s1-4s0-5s1-6s1-7s0-8s0 | H3/two | timeout300 | certified | 895.5 s solve, 99.0 s check |
| 192 | 0s0_1s0-4s1__2s1-3s0-5s1-6s0-7s0-8s0 | H3/two | timeout300 | certified | 727.5 s solve, 90.5 s check |
| 236 | 0s0_1s0-5s1__2s1-3s1-4s0-6s0-7s1-8s0 | H3/two | timeout300 | certified | 899.6 s solve, 105.2 s check |
| 280 | 0s0_1s0-7s0__2s1-3s0-4s1-5s0-6s0-8s0 | H3/two | timeout300 | certified | 310.1 s solve, 69.2 s check |
| 324 | 0s0_1s1-2s0__3s0-4s1-5s0-6s1-7s0-8s1 | H3/two | timeout300 | certified | 887.6 s solve, 97.1 s check |
| 368 | 0s0_1s1-4s0__2s0-3s1-5s1-6s0-7s0-8s1 | H3/two | timeout300 | certified | 860.7 s solve, 81.8 s check |
| 412 | 0s0_1s1-5s0__2s1-3s0-4s1-6s0-7s0-8s0 | H3/two | timeout300 | certified | 536.6 s solve, 72.1 s check |
| 456 | 0s0_1s1-5s1__2s0-3s1-4s0-6s1-7s0-8s1 | H3/two | presplit | certified | 281.4 s solve, 60.2 s check |
| 500 | 0s0_1s1-7s1__2s0-3s0-4s0-5s1-6s1-8s0 | H3/two | timeout300 | certified | 611.3 s solve, 71.6 s check |
| 544 | 0s0_1s1-7s1__2s1-3s1-4s1-5s1-6s0-8s1 | H3/two | timeout300 | certified | 857.0 s solve, 86.9 s check |
| 588 | 0s0_1s1-8s0__2s1-3s0-4s1-5s0-6s0-7s1 | H3/two | presplit | certified | 176.1 s solve, 59.6 s check |
| 632 | 0s0_1s1-8s1__2s1-3s1-4s0-5s0-6s0-7s1 | H3/two | timeout300 | certified | 869.8 s solve, 87.1 s check |
| 676 | 0s0_1s1-9s1__2s1-3s0-4s1-5s0-6s1-7s0 | H3/two | never_ran | certified | 831.9 s solve, 93.6 s check |
| 720 | 0s0_2s0-3s1__1s0-4s1-5s0-6s1-7s1-8s0 | H3/two | presplit | timeout900 | 900.2 s; split: 51 children (open) |
| 764 | 0s0_2s0-4s1__1s0-3s0-5s0-6s0-7s1-8s0 | H3/two | presplit | certified | 762.1 s solve, 98.4 s check |
| 808 | 0s0_2s0-4s1__1s1-3s0-5s1-6s1-7s1-8s0 | H3/two | presplit | timeout900 | 900.1 s; split: 51 children (open) |
| 852 | 0s0_2s0-5s0__1s0-3s1-4s1-6s0-7s1-8s0 | H3/two | presplit | certified | 133.6 s solve, 57.8 s check |
| 896 | 0s0_2s0-5s1__1s0-3s0-4s1-6s1-7s0-8s1 | H3/two | timeout300 | certified | 894.7 s solve, 88.0 s check |
| 940 | 0s0_2s0-5s1__1s1-3s1-4s1-6s0-7s0-8s1 | H3/two | timeout300 | timeout900 | 900.2 s; split: 51 children (open) |
| 984 | 0s0_2s0-6s1__1s1-3s0-4s0-5s1-7s1-8s1 | H3/two | timeout300 | certified | 882.1 s solve, 86.9 s check |
| 1028 | 0s0_2s0-7s0__1s0-3s1-4s0-5s0-6s1-8s1 | H3/two | presplit | certified | 262.2 s solve, 57.8 s check |
| 1072 | 0s0_2s0-7s0__1s1-3s1-4s1-5s1-6s1-8s1 | H3/two | presplit | certified | 252.9 s solve, 59.1 s check |
| 1116 | 0s0_2s0-7s1__1s1-3s0-4s1-5s0-6s1-8s1 | H3/two | presplit | certified | 582.8 s solve, 70.8 s check |
| 1160 | 0s0_2s0-8s0__1s1-3s0-4s1-5s0-6s0-7s1 | H3/two | presplit | certified | 444.2 s solve, 69.1 s check |
| 1204 | 0s0_2s1-3s0__1s0-4s1-5s0-6s1-7s1-8s0 | H3/two | timeout300 | timeout900 | 900.2 s; split: 51 children (open) |
| 1248 | 0s0_2s1-3s1__1s0-4s0-5s0-6s0-7s1-8s0 | H3/two | presplit | certified | 161.6 s solve, 56.8 s check |
| 1292 | 0s0_2s1-3s1__1s1-4s0-5s1-6s1-7s1-8s0 | H3/two | presplit | certified | 124.4 s solve, 52.4 s check |
| 1336 | 0s0_2s1-4s0__1s0-3s1-5s1-6s1-7s1-8s1 | H3/two | timeout300 | certified | 783.9 s solve, 82.3 s check |
| 1380 | 0s0_2s1-5s0__1s0-3s0-4s1-6s1-7s0-8s0 | H3/two | presplit | certified | 812.9 s solve, 77.4 s check |
| 1424 | 0s0_2s1-5s0__1s1-3s1-4s1-6s0-7s0-8s0 | H3/two | presplit | timeout900 | 900.3 s; split: 51 children (open) |
| 1468 | 0s0_2s1-6s0__1s1-3s0-4s0-5s1-7s0-8s0 | H3/two | presplit | certified | 704.9 s solve, 73.6 s check |
| 1512 | 0s0_2s1-6s1__1s0-3s1-4s0-5s0-7s0-8s0 | H3/two | presplit | certified | 286.8 s solve, 62.6 s check |
| 1556 | 0s0_2s1-6s1__1s1-3s1-4s1-5s1-7s0-8s0 | H3/two | presplit | certified | 632.0 s solve, 67.7 s check |
| 1600 | 0s0_2s1-7s0__1s1-3s1-4s0-5s0-6s0-8s0 | H3/two | never_ran | certified | 394.0 s solve, 63.1 s check |
| 1644 | 0s0_2s1-7s1__1s1-3s1-4s0-5s1-6s1-8s0 | H3/two | never_ran | certified | 796.6 s solve, 89.6 s check |
| 1688 | 0s0_2s1-8s1__1s1-3s0-4s1-5s0-6s1-7s1 | H3/two | presplit | timeout900 | 900.2 s; split: 51 children (open) |
| 1732 | 0s0_2s1-9s0__1s0-3s1-4s0-5s1-6s1-7s1 | H3/two | presplit | certified | 349.8 s solve, 57.7 s check |
| 1776 | 0s0_3s0-4s1__1s0-2s0-5s0-6s0-7s1-8s1 | H3/two | presplit | certified | 679.8 s solve, 83.0 s check |
| 1820 | 0s0_3s0-4s1__1s1-2s0-5s1-6s1-7s1-8s1 | H3/two | presplit | timeout900 | 900.1 s; split: 51 children (open) |
| 1864 | 0s0_3s0-5s0__1s0-2s1-4s1-6s0-7s1-8s1 | H3/two | presplit | certified | 101.9 s solve, 38.8 s check |
| 1908 | 0s0_3s0-5s1__1s0-2s0-4s1-6s1-7s1-8s1 | H3/two | timeout300 | certified | 826.4 s solve, 77.8 s check |
| 1952 | 0s0_3s0-5s1__1s1-2s1-4s1-6s1-7s0-8s1 | H3/two | timeout300 | timeout900 | 900.2 s; split: 51 children (open) |
| 1996 | 0s0_3s0-6s0__1s1-2s0-4s1-5s0-7s0-8s1 | H3/two | presplit | certified | 136.4 s solve, 47.8 s check |
| 2040 | 0s0_3s0-6s1__1s0-2s1-4s0-5s1-7s0-8s1 | H3/two | timeout300 | timeout900 | 900.2 s; split: 51 children (open) |
| 2084 | 0s0_3s0-7s0__1s0-2s0-4s0-5s0-6s0-8s1 | H3/two | presplit | certified | 169.4 s solve, 56.1 s check |
| 2128 | 0s0_3s0-7s0__1s1-2s0-4s1-5s1-6s0-8s1 | H3/two | presplit | certified | 194.2 s solve, 52.8 s check |
| 2172 | 0s0_3s0-7s1__1s0-2s1-4s1-5s0-6s0-8s1 | H3/two | presplit | timeout900 | 900.2 s; split: 51 children (open) |
| 2216 | 0s0_3s0-8s0__1s0-2s1-4s1-5s0-6s1-7s1 | H3/two | presplit | certified | 277.4 s solve, 53.9 s check |
| 2260 | 0s0_3s0-8s1__1s0-2s1-4s1-5s0-6s1-7s1 | H3/two | timeout300 | certified | 706.1 s solve, 85.8 s check |
| 2304 | 0s0_3s1-4s0__1s0-2s1-5s1-6s0-7s0-8s0 | H3/two | timeout300 | timeout900 | 900.3 s; split: 51 children (open) |
| 2348 | 0s0_3s1-4s1__1s0-2s0-5s0-6s1-7s0-8s0 | H3/two | presplit | certified | 141.4 s solve, 45.0 s check |
| 2392 | 0s0_3s1-4s1__1s1-2s1-5s0-6s0-7s0-8s0 | H3/two | presplit | certified | 213.1 s solve, 48.2 s check |
| 2436 | 0s0_3s1-5s0__1s0-2s1-4s1-6s1-7s0-8s0 | H3/two | presplit | timeout900 | 900.2 s; split: 51 children (open) |
| 2480 | 0s0_3s1-5s1__1s0-2s0-4s1-6s0-7s0-8s0 | H3/two | presplit | certified | 243.0 s solve, 58.0 s check |
| 2524 | 0s0_3s1-5s1__1s1-2s1-4s0-6s1-7s0-8s0 | H3/two | presplit | certified | 183.5 s solve, 48.8 s check |
| 2568 | 0s0_3s1-7s0__1s1-2s0-4s1-5s1-6s1-8s0 | H3/two | never_ran | timeout900 | 900.1 s; split: 51 children (open) |
| 2612 | 0s0_3s1-8s0__1s0-2s0-4s0-5s0-6s0-7s1 | H3/two | presplit | certified | 423.1 s solve, 56.5 s check |
| 2656 | 0s0_3s1-8s0__1s1-2s0-4s1-5s1-6s0-7s1 | H3/two | presplit | certified | 591.1 s solve, 78.9 s check |
| 2700 | 0s0_4s0-5s1__1s0-2s1-3s1-6s0-7s0-8s1 | H3/two | presplit | timeout900 | 900.2 s; split: 51 children (open) |
| 2744 | 0s0_4s0-6s1__1s0-2s0-3s0-5s1-7s0-8s1 | H3/two | presplit | certified | 701.2 s solve, 68.5 s check |
| 2788 | 0s0_4s0-6s1__1s1-2s1-3s0-5s0-7s0-8s1 | H3/two | presplit | certified | 869.1 s solve, 88.4 s check |
| 2832 | 0s0_4s0-7s0__1s0-2s1-3s1-5s1-6s0-8s1 | H3/two | presplit | certified | 190.2 s solve, 51.7 s check |
| 2876 | 0s0_4s0-7s1__1s0-2s1-3s0-5s0-6s1-8s0 | H3/two | presplit | certified | 776.5 s solve, 70.9 s check |
| 2920 | 0s0_4s0-7s1__1s1-2s1-3s1-5s1-6s1-8s0 | H3/two | presplit | timeout900 | 900.1 s; split: 51 children (open) |
| 2964 | 0s0_4s1-5s0__1s1-2s0-3s1-6s0-7s1-8s0 | H3/two | never_ran | killed at END | solve killed at END, no record |
| 3008 | 0s0_4s1-6s0__1s0-2s0-3s1-5s1-7s0-8s1 | H3/two | presplit | killed at END | solve killed at END, no record |
| 3052 | 0s0_4s1-6s0__1s1-2s1-3s1-5s0-7s0-8s1 | H3/two | presplit | timeout900 | 900.2 s; split: 51 children (open) |
| 3096 | 0s0_4s1-6s1__1s1-2s0-3s0-5s1-7s0-8s1 | H3/two | presplit | not reached |  |
| 3140 | 0s0_4s1-7s0__1s0-2s1-3s0-5s0-6s0-8s1 | H3/two | presplit | not reached |  |
| 3184 | 0s0_4s1-7s0__1s1-2s1-3s1-5s1-6s0-8s1 | H3/two | presplit | killed at END | solve killed at END, no record |
| 3228 | 0s0_5s0-6s0__1s1-2s0-3s1-4s0-7s0-8s1 | H3/two | presplit | not reached |  |
| 3272 | 0s0_5s0-6s1__1s0-2s1-3s0-4s1-7s0-8s1 | H3/two | presplit | not reached |  |
| 3316 | 0s0_5s1-6s0__1s0-2s1-3s1-4s1-7s0-8s1 | H3/two | timeout300 | not reached |  |
| 3360 | 0s0-1s1_5__2s0-3s0-4s0-6s1-7s0-8s0 | H6(1,1)/one | timeout300 | not reached |  |
| 3404 | 0s0-1s1_5__2s1-3s1-4s1-6s0-7s0-8s0 | H6(1,1)/one | timeout300 | not reached |  |
| 3448 | 0s0-2s1_4__1s1-3s1-5s0-6s1-7s0-8s0 | H6(2,1)/one | timeout300 | not reached |  |
| 3492 | 0s0-2s1_5__1s1-3s0-4s1-6s1-7s0-8s1 | H6(2,1)/one | timeout300 | not reached |  |
| 3536 | 0s0-2s1_6__1s0-3s1-4s1-5s0-7s1-8s1 | H6(2,1)/one | timeout300 | not reached |  |
| 3580 | 0s0-3s1_4__1s0-2s1-5s0-6s1-7s1-8s1 | H6(3,1)/one | timeout300 | not reached |  |
| 3624 | 0s0-3s1_5__1s0-2s0-4s1-6s0-7s1-8s1 | H6(3,1)/one | presplit | not reached |  |
| 3668 | 0s0-3s1_5__1s1-2s1-4s0-6s1-7s1-8s1 | H6(3,1)/one | presplit | not reached |  |
| 3712 | 0s0-4s0_6__1s1-2s0-3s0-5s0-7s1-8s1 | H6(4,0)/one | presplit | not reached |  |
| 3756 | 0s0-5s0_6__1s0-2s0-3s1-4s0-7s1-8s0 | H6(5,0)/one | presplit | not reached |  |
| 3800 | 0s0-5s0_6__1s1-2s1-3s0-4s1-7s1-8s0 | H6(5,0)/one | presplit | not reached |  |
| 3844 | 0s0-5s0_7__1s1-2s0-3s0-4s0-6s1-8s0 | H6(5,0)/one | presplit | not reached |  |
| 3888 | 0s0-5s1_1__2s0-3s1-4s1-6s1-7s0-8s0 | H6(5,1)/one | presplit | not reached |  |
| 3932 | 0s0-5s1_2__1s0-3s0-4s1-6s0-7s0-8s0 | H6(5,1)/one | presplit | not reached |  |
| 3976 | 0s0-5s1_2__1s1-3s1-4s0-6s1-7s0-8s0 | H6(5,1)/one | presplit | not reached |  |
| 4020 | 0s0-5s1_1s1-10s1__2s0-3s0-4s0-6s1-7s1-8s1 | H6(5,1)/two | never_ran | not reached |  |
| 4064 | 0s0-5s1_1s1-10s1__2s1-3s1-4s0-6s0-7s1-8s1 | H6(5,1)/two | never_ran | not reached |  |
| 4108 | 0s0-5s1_7s0-9s1__1s1-2s1-3s1 | H6(5,1)/two | presplit | not reached |  |
