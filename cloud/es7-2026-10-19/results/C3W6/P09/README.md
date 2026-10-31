# C3W6 P09: shard 9 of 44 of W6.tsv, 94 σ-cubes solved once at cap 900

Task: `results/C3W6/TASK.md` at c5260b44, with V = P09, LIST = W6.tsv, j = 9, N = 44, H = 4.5. One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`).
Start 05:31:52 UTC on 2026-10-25, END 09:46:52 UTC. Lanes started at 05:34:22 UTC and all finished before END (the last at 09:26:53 UTC), so nothing was killed.

## Tools (`tools.txt`)

- C3U2 tools from a worktree of cad4e050 at `/opt/c3u2`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 (c60730422e75), cake_lpr a36874a8 (bundled example: `s VERIFIED UNSAT`), and drat-trim lrat-check 2e3b2dc with the E2 patch. Sanity check on {1},{-1}: `3 0 0` is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da` (matches). Every record has this `base_sha256`.

## Run

`units.tsv` holds the 94 rows of W6.tsv with row ≡ 9 (mod 44). There are 3 lanes (`lane0.sh`, `lane1.sh`, `lane2.sh`), and lane k takes positions ≡ k (mod 3). Each unit was run as `close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`. No records were seeded.
A detached keeper script pushed progress every 20 minutes and would have killed the lanes at END. `out.jsonl` holds 94 records (lane 0, then 1, then 2), one solve record per unit and no split records.

## Result

**All 94 units are certified at cap 900.** For each one, CaDiCaL returned UNSATISFIABLE, lrat-check printed `c VERIFIED` and cake_lpr printed `s VERIFIED UNSAT`. Every unit's `open_frontier` is 0.
There was no SAT, no proof rejection, no cake_lpr `none`, no timeout and no memory problem (free memory never fell below about 5 GB). Because nothing needed a re-check, there is no `recheck.jsonl`.
Seven units solved in under 72 s, and all seven were certified, so none of them is an early end without a certificate.

Solve times of the 94 certified units: min 21.5 s, Q1 182.5 s, median 387.0 s, Q3 529.7 s, p90 601.4 s, max 774.0 s. **59 of 94 were certified above 300 s.**
In total, solving took 34580 s and checking took 4968 s (17–90 s per unit). Three jobs ran on 4 cores.

| stratum | units | certified | timed out | not reached | median solve s | max solve s | certified > 300 s |
|---|---|---|---|---|---|---|---|
| H3/two | 76 | 76 | 0 | 0 | 469.4 | 774.0 | 50 |
| H6(1,1)/one | 2 | 2 | 0 | 0 | 389.7 | 389.7 | 2 |
| H6(2,1)/one | 3 | 3 | 0 | 0 | 373.2 | 529.7 | 2 |
| H6(3,1)/one | 3 | 3 | 0 | 0 | 344.5 | 414.4 | 3 |
| H6(4,0)/one | 1 | 1 | 0 | 0 | 111.6 | 111.6 | 0 |
| H6(5,0)/one | 3 | 3 | 0 | 0 | 80.9 | 100.8 | 0 |
| H6(5,1)/one | 4 | 4 | 0 | 0 | 327.6 | 391.2 | 2 |
| H6(5,1)/two | 2 | 2 | 0 | 0 | 157.2 | 157.2 | 0 |

| prior | units | certified | timed out | not reached | median solve s | max solve s | certified > 300 s |
|---|---|---|---|---|---|---|---|
| never_ran | 9 | 9 | 0 | 0 | 516.1 | 772.3 | 7 |
| presplit | 57 | 57 | 0 | 0 | 265.4 | 774.0 | 25 |
| timeout300 | 28 | 28 | 0 | 0 | 477.3 | 679.8 | 27 |

## Per unit

| row | node | stratum | prior | result | solve s | check s |
|---|---|---|---|---|---|---|
| 9 | `0s0_1s0-10s0__2s1-3s1-4s0-5s1-6s0-7s1` | H3/two | timeout300 | certified | 326.7 | 71.4 |
| 53 | `0s0_1s0-2s0__3s1-4s0-5s1-6s0-7s0-8s0` | H3/two | presplit | certified | 66.5 | 52.0 |
| 97 | `0s0_1s0-2s1__3s0-4s1-5s1-6s0-7s1-8s1` | H3/two | timeout300 | certified | 543.2 | 76.1 |
| 141 | `0s0_1s0-3s1__2s1-4s0-5s0-6s1-7s0-8s1` | H3/two | timeout300 | certified | 549.8 | 78.1 |
| 185 | `0s0_1s0-4s1__2s1-3s0-5s0-6s0-7s0-8s1` | H3/two | timeout300 | certified | 490.4 | 54.3 |
| 229 | `0s0_1s0-5s1__2s1-3s0-4s1-6s0-7s0-8s1` | H3/two | timeout300 | certified | 414.8 | 70.7 |
| 273 | `0s0_1s0-7s0__2s1-3s0-4s0-5s0-6s0-8s1` | H3/two | timeout300 | certified | 312.8 | 66.5 |
| 317 | `0s0_1s1-2s0__3s0-4s0-5s1-6s1-7s1-8s0` | H3/two | timeout300 | certified | 522.3 | 76.6 |
| 361 | `0s0_1s1-2s0__3s1-4s1-5s1-6s0-7s1-8s0` | H3/two | timeout300 | certified | 469.4 | 68.6 |
| 405 | `0s0_1s1-5s0__2s0-3s1-4s1-6s1-7s1-8s0` | H3/two | timeout300 | certified | 505.4 | 68.1 |
| 449 | `0s0_1s1-5s1__2s0-3s0-4s1-6s1-7s1-8s0` | H3/two | presplit | certified | 187.9 | 54.9 |
| 493 | `0s0_1s1-5s1__2s1-3s1-4s1-6s0-7s1-8s0` | H3/two | presplit | certified | 320.4 | 48.7 |
| 537 | `0s0_1s1-7s1__2s1-3s1-4s0-5s1-6s1-8s0` | H3/two | timeout300 | certified | 679.8 | 66.9 |
| 581 | `0s0_1s1-8s0__2s1-3s0-4s0-5s0-6s1-7s0` | H3/two | presplit | certified | 109.2 | 49.1 |
| 625 | `0s0_1s1-8s1__2s1-3s0-4s1-5s0-6s0-7s1` | H3/two | timeout300 | certified | 477.3 | 66.5 |
| 669 | `0s0_1s1-9s1__2s1-3s0-4s0-5s0-6s1-7s1` | H3/two | never_ran | certified | 566.0 | 63.2 |
| 713 | `0s0_2s0-3s1__1s0-4s0-5s1-6s1-7s1-8s1` | H3/two | presplit | certified | 453.3 | 59.6 |
| 757 | `0s0_2s0-3s1__1s1-4s1-5s1-6s0-7s1-8s1` | H3/two | presplit | certified | 573.2 | 64.8 |
| 801 | `0s0_2s0-4s1__1s1-3s0-5s0-6s1-7s1-8s1` | H3/two | presplit | certified | 601.4 | 73.3 |
| 845 | `0s0_2s0-5s0__1s0-3s1-4s0-6s0-7s1-8s1` | H3/two | presplit | certified | 66.0 | 43.0 |
| 889 | `0s0_2s0-5s0__1s1-3s1-4s1-6s1-7s1-8s1` | H3/two | presplit | certified | 132.0 | 51.8 |
| 933 | `0s0_2s0-5s1__1s1-3s1-4s0-6s0-7s1-8s0` | H3/two | timeout300 | certified | 653.7 | 61.4 |
| 977 | `0s0_2s0-6s1__1s1-3s0-4s0-5s0-7s0-8s0` | H3/two | timeout300 | certified | 320.8 | 57.0 |
| 1021 | `0s0_2s0-7s0__1s0-3s0-4s1-5s1-6s0-8s0` | H3/two | presplit | certified | 129.9 | 45.3 |
| 1065 | `0s0_2s0-7s0__1s1-3s1-4s1-5s0-6s0-8s0` | H3/two | presplit | certified | 201.0 | 38.5 |
| 1109 | `0s0_2s0-7s1__1s1-3s0-4s0-5s1-6s0-8s0` | H3/two | presplit | certified | 280.7 | 56.6 |
| 1153 | `0s0_2s0-8s0__1s1-3s0-4s0-5s0-6s1-7s0` | H3/two | presplit | certified | 262.0 | 56.6 |
| 1197 | `0s0_2s1-3s0__1s0-4s0-5s1-6s1-7s1-8s1` | H3/two | timeout300 | certified | 468.4 | 75.6 |
| 1241 | `0s0_2s1-3s0__1s1-4s1-5s1-6s0-7s1-8s1` | H3/two | timeout300 | certified | 621.0 | 66.2 |
| 1285 | `0s0_2s1-3s1__1s1-4s0-5s0-6s1-7s1-8s1` | H3/two | presplit | certified | 84.5 | 52.8 |
| 1329 | `0s0_2s1-4s0__1s0-3s1-5s1-6s0-7s0-8s0` | H3/two | timeout300 | certified | 522.6 | 51.6 |
| 1373 | `0s0_2s1-5s0__1s0-3s0-4s0-6s1-7s0-8s1` | H3/two | presplit | certified | 359.4 | 46.1 |
| 1417 | `0s0_2s1-5s0__1s1-3s1-4s0-6s0-7s0-8s1` | H3/two | presplit | certified | 527.7 | 60.1 |
| 1461 | `0s0_2s1-6s0__1s0-3s1-4s1-5s1-7s0-8s1` | H3/two | presplit | certified | 496.2 | 53.6 |
| 1505 | `0s0_2s1-6s1__1s0-3s0-4s1-5s0-7s0-8s1` | H3/two | presplit | certified | 182.5 | 36.1 |
| 1549 | `0s0_2s1-6s1__1s1-3s1-4s0-5s1-7s0-8s1` | H3/two | presplit | certified | 275.9 | 43.5 |
| 1593 | `0s0_2s1-7s0__1s1-3s0-4s1-5s0-6s0-8s1` | H3/two | never_ran | certified | 268.6 | 42.4 |
| 1637 | `0s0_2s1-7s1__1s1-3s0-4s1-5s1-6s1-8s1` | H3/two | never_ran | certified | 514.8 | 50.7 |
| 1681 | `0s0_2s1-8s1__1s1-3s0-4s0-5s1-6s0-7s0` | H3/two | presplit | certified | 217.1 | 42.7 |
| 1725 | `0s0_2s1-9s0__1s0-3s1-4s0-5s0-6s0-7s0` | H3/two | presplit | certified | 82.1 | 32.3 |
| 1769 | `0s0_2s1-9s0__1s1-3s1-4s1-5s1-6s0-7s0` | H3/two | presplit | certified | 129.2 | 38.1 |
| 1813 | `0s0_3s0-4s1__1s1-2s0-5s1-6s0-7s0-8s0` | H3/two | presplit | certified | 544.4 | 58.9 |
| 1857 | `0s0_3s0-5s0__1s0-2s1-4s0-6s1-7s0-8s0` | H3/two | presplit | certified | 59.6 | 47.2 |
| 1901 | `0s0_3s0-5s1__1s0-2s0-4s1-6s0-7s0-8s0` | H3/two | timeout300 | certified | 387.0 | 48.8 |
| 1945 | `0s0_3s0-5s1__1s1-2s1-4s0-6s1-7s1-8s0` | H3/two | timeout300 | certified | 573.5 | 60.9 |
| 1989 | `0s0_3s0-6s0__1s1-2s0-4s0-5s0-7s1-8s0` | H3/two | presplit | certified | 87.5 | 30.6 |
| 2033 | `0s0_3s0-6s1__1s0-2s0-4s1-5s1-7s1-8s0` | H3/two | timeout300 | certified | 501.0 | 52.1 |
| 2077 | `0s0_3s0-6s1__1s1-2s1-4s1-5s0-7s1-8s0` | H3/two | never_ran | certified | 571.3 | 52.6 |
| 2121 | `0s0_3s0-7s0__1s1-2s0-4s0-5s1-6s1-8s0` | H3/two | presplit | certified | 99.0 | 34.1 |
| 2165 | `0s0_3s0-7s1__1s0-2s1-4s0-5s0-6s1-8s0` | H3/two | presplit | certified | 481.6 | 59.5 |
| 2209 | `0s0_3s0-7s1__1s1-2s1-4s1-5s1-6s1-8s0` | H3/two | presplit | certified | 478.1 | 52.2 |
| 2253 | `0s0_3s0-8s1__1s0-2s0-4s1-5s1-6s0-7s1` | H3/two | timeout300 | certified | 397.0 | 49.7 |
| 2297 | `0s0_3s1-4s0__1s0-2s1-5s0-6s0-7s0-8s1` | H3/two | timeout300 | certified | 530.1 | 50.9 |
| 2341 | `0s0_3s1-4s0__1s1-2s1-5s1-6s1-7s0-8s1` | H3/two | never_ran | certified | 772.3 | 66.0 |
| 2385 | `0s0_3s1-4s1__1s1-2s0-5s1-6s0-7s0-8s1` | H3/two | presplit | certified | 78.4 | 30.3 |
| 2429 | `0s0_3s1-5s0__1s0-2s1-4s0-6s1-7s0-8s1` | H3/two | presplit | certified | 699.3 | 73.2 |
| 2473 | `0s0_3s1-5s1__1s0-2s0-4s0-6s0-7s0-8s1` | H3/two | presplit | certified | 139.7 | 35.8 |
| 2517 | `0s0_3s1-5s1__1s1-2s0-4s1-6s1-7s0-8s1` | H3/two | presplit | certified | 91.7 | 38.2 |
| 2561 | `0s0_3s1-7s0__1s1-2s0-4s0-5s1-6s1-8s1` | H3/two | never_ran | certified | 516.1 | 55.8 |
| 2605 | `0s0_3s1-7s1__1s1-2s1-4s0-5s1-6s1-8s1` | H3/two | timeout300 | certified | 310.9 | 46.8 |
| 2649 | `0s0_3s1-8s0__1s1-2s0-4s0-5s1-6s1-7s0` | H3/two | presplit | certified | 281.0 | 45.1 |
| 2693 | `0s0_4s0-5s1__1s0-2s1-3s0-6s0-7s1-8s0` | H3/two | presplit | certified | 584.6 | 63.3 |
| 2737 | `0s0_4s0-5s1__1s1-2s1-3s1-6s1-7s1-8s0` | H3/two | presplit | certified | 618.1 | 56.5 |
| 2781 | `0s0_4s0-6s1__1s1-2s0-3s1-5s0-7s1-8s0` | H3/two | presplit | certified | 576.4 | 62.2 |
| 2825 | `0s0_4s0-7s0__1s0-2s1-3s0-5s1-6s1-8s0` | H3/two | presplit | certified | 69.0 | 32.9 |
| 2869 | `0s0_4s0-7s1__1s0-2s0-3s1-5s0-6s1-8s1` | H3/two | presplit | certified | 490.7 | 53.5 |
| 2913 | `0s0_4s0-7s1__1s1-2s1-3s0-5s1-6s1-8s1` | H3/two | presplit | certified | 774.0 | 61.9 |
| 2957 | `0s0_4s1-5s0__1s1-2s0-3s0-6s0-7s1-8s1` | H3/two | never_ran | certified | 547.6 | 53.5 |
| 3001 | `0s0_4s1-6s0__1s0-2s0-3s0-5s1-7s1-8s0` | H3/two | presplit | certified | 394.0 | 47.2 |
| 3045 | `0s0_4s1-6s0__1s1-2s1-3s0-5s0-7s1-8s0` | H3/two | presplit | certified | 520.0 | 52.9 |
| 3089 | `0s0_4s1-6s1__1s0-2s1-3s1-5s1-7s1-8s0` | H3/two | presplit | certified | 80.3 | 33.6 |
| 3133 | `0s0_4s1-7s0__1s0-2s0-3s1-5s0-6s1-8s0` | H3/two | presplit | certified | 530.8 | 67.2 |
| 3177 | `0s0_4s1-7s0__1s1-2s1-3s0-5s1-6s1-8s0` | H3/two | presplit | certified | 666.8 | 90.2 |
| 3221 | `0s0_5s0-6s0__1s1-2s0-3s0-4s0-7s1-8s0` | H3/two | presplit | certified | 21.5 | 17.3 |
| 3265 | `0s0_5s0-6s1__1s0-2s0-3s1-4s1-7s1-8s0` | H3/two | presplit | certified | 584.9 | 61.1 |
| 3309 | `0s0_5s0-6s1__1s1-2s1-3s1-4s0-7s1-8s0` | H3/two | presplit | certified | 712.7 | 63.8 |
| 3353 | `0s0-1s1_4__2s1-3s0-5s1-6s1-7s1-8s1` | H6(1,1)/one | timeout300 | certified | 389.7 | 48.2 |
| 3397 | `0s0-1s1_5__2s1-3s1-4s0-6s0-7s0-8s1` | H6(1,1)/one | timeout300 | certified | 374.1 | 47.9 |
| 3441 | `0s0-2s1_4__1s1-3s0-5s1-6s1-7s0-8s1` | H6(2,1)/one | timeout300 | certified | 529.7 | 64.3 |
| 3485 | `0s0-2s1_5__1s1-3s0-4s0-6s1-7s1-8s0` | H6(2,1)/one | timeout300 | certified | 373.2 | 52.2 |
| 3529 | `0s0-2s1_6__1s0-3s1-4s0-5s1-7s0-8s0` | H6(2,1)/one | timeout300 | certified | 268.1 | 44.3 |
| 3573 | `0s0-3s1_4__1s0-2s0-5s1-6s1-7s0-8s0` | H6(3,1)/one | timeout300 | certified | 343.1 | 44.5 |
| 3617 | `0s0-3s1_5__1s0-2s0-4s0-6s1-7s0-8s0` | H6(3,1)/one | presplit | certified | 344.5 | 60.5 |
| 3661 | `0s0-3s1_5__1s1-2s1-4s0-6s0-7s0-8s0` | H6(3,1)/one | presplit | certified | 414.4 | 56.1 |
| 3705 | `0s0-4s0_6__1s0-2s1-3s1-5s1-7s0-8s0` | H6(4,0)/one | presplit | certified | 111.6 | 38.9 |
| 3749 | `0s0-5s0_6__1s0-2s0-3s0-4s0-7s1-8s1` | H6(5,0)/one | presplit | certified | 65.4 | 36.0 |
| 3793 | `0s0-5s0_6__1s1-2s0-3s1-4s1-7s1-8s1` | H6(5,0)/one | presplit | certified | 80.9 | 54.2 |
| 3837 | `0s0-5s0_7__1s0-2s1-3s1-4s0-6s1-8s1` | H6(5,0)/one | presplit | certified | 100.8 | 35.2 |
| 3881 | `0s0-5s1_1__2s0-3s1-4s0-6s1-7s0-8s1` | H6(5,1)/one | presplit | certified | 265.4 | 46.7 |
| 3925 | `0s0-5s1_2__1s0-3s0-4s0-6s0-7s0-8s1` | H6(5,1)/one | presplit | certified | 260.3 | 43.8 |
| 3969 | `0s0-5s1_2__1s1-3s0-4s1-6s1-7s0-8s1` | H6(5,1)/one | presplit | certified | 327.6 | 45.0 |
| 4013 | `0s0-5s1_6__1s1-2s1-3s1-4s0-7s1-8s0` | H6(5,1)/one | never_ran | certified | 391.2 | 51.6 |
| 4057 | `0s0-5s1_1s1-10s1__2s1-3s0-4s1-6s1-7s0-8s0` | H6(5,1)/two | never_ran | certified | 46.2 | 26.8 |
| 4101 | `0s0-5s1_7s0-9s1__1s0-2s0-3s0` | H6(5,1)/two | presplit | certified | 157.2 | 35.1 |
