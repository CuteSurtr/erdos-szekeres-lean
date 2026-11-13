# C3W7 Q25: nine-bit σ-cubes of the H3/one roots at cap 900 (shard 25 of 36 of W7.tsv)

Task: `results/C3W7/TASK.md` at 39bb1bac, with V = Q25, LIST = W7.tsv, j = 25, N = 36, H = 4.5.
One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 10:46:09 UTC, lanes started 10:48:33, END 15:01:09 UTC (2026-10-25).

## Tools (`tools.txt`)

- C3U2 tools at cad4e050 (worktree `/opt/c3u2`), used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 c6073042; cake_lpr a36874a8 (the example prints `s VERIFIED UNSAT`); lrat-check 2e3b2dc with the E2 patch. Sanity check: LRAT `3 0 0` on {1},{-1} is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da`, which matches.

## Run

- 53 units (rows ≡ 25 mod 36 of `W7.tsv`, in `units.tsv`). No records were seeded.
- 3 lanes (`lane0.sh`–`lane2.sh` → `lane.sh`), each running `close_tree.py … U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`.
- Lane 2 finished its 18 units at 14:56. Lanes 0 and 1 were killed at END (whole process groups) while they were solving their last unit, so those two units left no record and count as not reached.
- **Result: 28 certified, 23 timed out at 900 s, 2 not reached.**
- Each timed-out unit has its layer-split record (`"split": true, "children": 45`). Its children are unsolved and in `open_frontier`, as the task intends.
- No SAT. No proof rejection: every UNSAT record has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`, so no re-check was needed and there is no `recheck.jsonl`.
- No checker was killed at END and no cake_lpr result is `none`.
- No memory problem: about 2 GB used with 3 jobs, and no OOM.
- No unit ended early: every non-certified solve ran the full 900 s.
- Total solve time 41,586 s and total check time 2,836 s (70.7–120.9 s per certified unit).

## Solve times of certified units

28 certified: min 412.2 s, q1 666.6, median 748.0, q3 834.9, p90 883.1, max 899.5. All 28 were certified above 300 s. 23 of the 51 units that ran timed out at 900 s.

## Per unit

| pos | lane | row | unit | status | solve s | check s |
|---|---|---|---|---|---|---|
| 0 | 0 | 25 | `0s0_1__2s0-3s0-4s0-5s0-6s1-7s1-8s0-9s0-10s1` | certified | 663.6 | 104.3 |
| 1 | 1 | 61 | `0s0_1__2s0-3s0-4s0-5s1-6s1-7s1-8s1-9s0-10s1` | certified | 667.6 | 104.9 |
| 2 | 2 | 97 | `0s0_1__2s0-3s0-4s1-5s1-6s0-7s0-8s0-9s0-10s1` | certified | 726.6 | 99.4 |
| 3 | 0 | 133 | `0s0_1__2s0-3s1-4s0-5s0-6s0-7s0-8s1-9s0-10s1` | certified | 815.9 | 120.9 |
| 4 | 1 | 169 | `0s0_1__2s0-3s1-4s0-5s1-6s0-7s1-8s0-9s0-10s1` | certified | 817.4 | 120.6 |
| 5 | 2 | 205 | `0s0_1__2s0-3s1-4s1-5s0-6s0-7s1-8s1-9s0-10s1` | timed out at 900 | 900.1 |  |
| 6 | 0 | 241 | `0s0_1__2s0-3s1-4s1-5s1-6s1-7s0-8s0-9s0-10s1` | timed out at 900 | 900.1 |  |
| 7 | 1 | 277 | `0s0_1__2s1-3s0-4s0-5s0-6s1-7s0-8s1-9s0-10s1` | certified | 840.1 | 108.5 |
| 8 | 2 | 313 | `0s0_1__2s1-3s0-4s0-5s1-6s1-7s1-8s0-9s0-10s1` | timed out at 900 | 900.1 |  |
| 9 | 0 | 349 | `0s0_1__2s1-3s0-4s1-5s0-6s1-7s1-8s1-9s0-10s1` | timed out at 900 | 900.1 |  |
| 10 | 1 | 385 | `0s0_1__2s1-3s1-4s0-5s0-6s0-7s0-8s0-9s0-10s1` | certified | 614.8 | 99.1 |
| 11 | 2 | 421 | `0s0_1__2s1-3s1-4s0-5s1-6s0-7s0-8s1-9s0-10s1` | certified | 899.5 | 119.7 |
| 12 | 0 | 457 | `0s0_1__2s1-3s1-4s1-5s0-6s0-7s1-8s0-9s0-10s1` | timed out at 900 | 900.1 |  |
| 13 | 1 | 493 | `0s0_1__2s1-3s1-4s1-5s1-6s0-7s1-8s1-9s0-10s1` | certified | 833.2 | 107.0 |
| 14 | 2 | 529 | `0s0_2__1s0-3s0-4s0-5s0-6s1-7s0-8s0-9s0-10s1` | certified | 646.1 | 89.4 |
| 15 | 0 | 565 | `0s0_2__1s0-3s0-4s0-5s1-6s1-7s0-8s1-9s0-10s1` | certified | 883.0 | 106.7 |
| 16 | 1 | 601 | `0s0_2__1s0-3s0-4s1-5s0-6s1-7s1-8s0-9s0-10s1` | certified | 845.4 | 109.2 |
| 17 | 2 | 637 | `0s0_2__1s0-3s0-4s1-5s1-6s1-7s1-8s1-9s0-10s1` | certified | 817.6 | 111.3 |
| 18 | 0 | 673 | `0s0_2__1s0-3s1-4s0-5s1-6s0-7s0-8s0-9s0-10s1` | certified | 694.8 | 95.9 |
| 19 | 1 | 709 | `0s0_2__1s0-3s1-4s1-5s0-6s0-7s0-8s1-9s0-10s1` | timed out at 900 | 900.1 |  |
| 20 | 2 | 745 | `0s0_2__1s0-3s1-4s1-5s1-6s0-7s1-8s0-9s0-10s1` | timed out at 900 | 900.1 |  |
| 21 | 0 | 781 | `0s0_2__1s1-3s0-4s0-5s0-6s0-7s1-8s1-9s0-10s1` | certified | 824.7 | 105.3 |
| 22 | 1 | 817 | `0s0_2__1s1-3s0-4s0-5s1-6s1-7s0-8s0-9s0-10s1` | certified | 878.4 | 120.2 |
| 23 | 2 | 853 | `0s0_2__1s1-3s0-4s1-5s0-6s1-7s0-8s1-9s0-10s1` | certified | 883.5 | 104.0 |
| 24 | 0 | 889 | `0s0_2__1s1-3s0-4s1-5s1-6s1-7s1-8s0-9s0-10s1` | timed out at 900 | 900.1 |  |
| 25 | 1 | 925 | `0s0_2__1s1-3s1-4s0-5s0-6s1-7s1-8s1-9s0-10s1` | timed out at 900 | 900.1 |  |
| 26 | 2 | 961 | `0s0_2__1s1-3s1-4s1-5s0-6s0-7s0-8s0-9s0-10s1` | certified | 750.9 | 101.8 |
| 27 | 0 | 997 | `0s0_2__1s1-3s1-4s1-5s1-6s0-7s0-8s1-9s0-10s1` | timed out at 900 | 900.1 |  |
| 28 | 1 | 1033 | `0s0_3__1s0-2s0-4s0-5s0-6s0-7s1-8s0-9s0-10s1` | certified | 634.5 | 91.4 |
| 29 | 2 | 1069 | `0s0_3__1s0-2s0-4s0-5s1-6s0-7s1-8s1-9s0-10s1` | certified | 770.5 | 92.2 |
| 30 | 0 | 1105 | `0s0_3__1s0-2s0-4s1-5s0-6s1-7s0-8s0-9s0-10s1` | certified | 745.2 | 105.2 |
| 31 | 1 | 1141 | `0s0_3__1s0-2s0-4s1-5s1-6s1-7s0-8s1-9s0-10s1` | timed out at 900 | 900.1 |  |
| 32 | 2 | 1177 | `0s0_3__1s0-2s1-4s0-5s0-6s1-7s1-8s0-9s0-10s1` | timed out at 900 | 900.1 |  |
| 33 | 0 | 1213 | `0s0_3__1s0-2s1-4s0-5s1-6s1-7s1-8s1-9s0-10s1` | timed out at 900 | 900.1 |  |
| 34 | 1 | 1249 | `0s0_3__1s0-2s1-4s1-5s1-6s0-7s0-8s0-9s0-10s1` | timed out at 900 | 900.1 |  |
| 35 | 2 | 1285 | `0s0_3__1s1-2s0-4s0-5s0-6s0-7s0-8s1-9s0-10s1` | certified | 612.0 | 91.7 |
| 36 | 0 | 1321 | `0s0_3__1s1-2s0-4s0-5s1-6s0-7s1-8s0-9s0-10s1` | timed out at 900 | 900.1 |  |
| 37 | 1 | 1357 | `0s0_3__1s1-2s0-4s1-5s0-6s0-7s1-8s1-9s0-10s1` | timed out at 900 | 900.1 |  |
| 38 | 2 | 1393 | `0s0_3__1s1-2s0-4s1-5s1-6s1-7s0-8s0-9s0-10s1` | timed out at 900 | 900.1 |  |
| 39 | 0 | 1429 | `0s0_3__1s1-2s1-4s0-5s0-6s1-7s0-8s1-9s0-10s1` | timed out at 900 | 900.1 |  |
| 40 | 1 | 1465 | `0s0_3__1s1-2s1-4s0-5s1-6s1-7s1-8s0-9s0-10s1` | timed out at 900 | 900.1 |  |
| 41 | 2 | 1501 | `0s0_3__1s1-2s1-4s1-5s0-6s1-7s1-8s1-9s0-10s1` | timed out at 900 | 900.1 |  |
| 42 | 0 | 1537 | `0s0_4__1s0-2s0-3s0-5s0-6s0-7s0-8s0-9s0-10s1` | certified | 412.2 | 70.7 |
| 43 | 1 | 1573 | `0s0_4__1s0-2s0-3s0-5s1-6s0-7s0-8s1-9s0-10s1` | certified | 558.3 | 78.0 |
| 44 | 2 | 1609 | `0s0_4__1s0-2s0-3s1-5s0-6s0-7s1-8s0-9s0-10s1` | certified | 703.1 | 87.7 |
| 45 | 0 | 1645 | `0s0_4__1s0-2s0-3s1-5s1-6s0-7s1-8s1-9s0-10s1` | certified | 886.7 | 99.1 |
| 46 | 1 | 1681 | `0s0_4__1s0-2s1-3s0-5s0-6s1-7s0-8s0-9s0-10s1` | certified | 716.6 | 96.6 |
| 47 | 2 | 1717 | `0s0_4__1s0-2s1-3s0-5s1-6s1-7s0-8s1-9s0-10s1` | timed out at 900 | 900.1 |  |
| 48 | 0 | 1753 | `0s0_4__1s0-2s1-3s1-5s0-6s1-7s1-8s0-9s0-10s1` | timed out at 900 | 900.1 |  |
| 49 | 1 | 1789 | `0s0_4__1s0-2s1-3s1-5s1-6s1-7s1-8s1-9s0-10s1` | timed out at 900 | 900.2 |  |
| 50 | 2 | 1825 | `0s0_4__1s1-2s0-3s0-5s1-6s0-7s0-8s0-9s0-10s1` | certified | 741.3 | 94.8 |
| 51 | 0 | 1861 | `0s0_4__1s1-2s0-3s1-5s0-6s0-7s0-8s1-9s0-10s1` | not reached |  |  |
| 52 | 1 | 1897 | `0s0_4__1s1-2s0-3s1-5s1-6s0-7s1-8s0-9s0-10s1` | not reached |  |  |


## Totals per root

| root | units | certified | timed out | not reached | all certified |
|---|---|---|---|---|---|
| `0s0_1` | 14 | 9 | 5 | 0 | no |
| `0s0_2` | 14 | 9 | 5 | 0 | no |
| `0s0_3` | 14 | 4 | 10 | 0 | no |
| `0s0_4` | 11 | 6 | 3 | 2 | no |

## Totals per parent six-bit cube

Each parent has exactly one unit on this machine. The parents whose units here were all certified (28) are: 0s0_1__2s0-3s0-4s0-5s0-6s1-7s1, 0s0_1__2s0-3s0-4s0-5s1-6s1-7s1, 0s0_1__2s0-3s0-4s1-5s1-6s0-7s0, 0s0_1__2s0-3s1-4s0-5s0-6s0-7s0, 0s0_1__2s0-3s1-4s0-5s1-6s0-7s1, 0s0_1__2s1-3s0-4s0-5s0-6s1-7s0, 0s0_1__2s1-3s1-4s0-5s0-6s0-7s0, 0s0_1__2s1-3s1-4s0-5s1-6s0-7s0, 0s0_1__2s1-3s1-4s1-5s1-6s0-7s1, 0s0_2__1s0-3s0-4s0-5s0-6s1-7s0, 0s0_2__1s0-3s0-4s0-5s1-6s1-7s0, 0s0_2__1s0-3s0-4s1-5s0-6s1-7s1, 0s0_2__1s0-3s0-4s1-5s1-6s1-7s1, 0s0_2__1s0-3s1-4s0-5s1-6s0-7s0, 0s0_2__1s1-3s0-4s0-5s0-6s0-7s1, 0s0_2__1s1-3s0-4s0-5s1-6s1-7s0, 0s0_2__1s1-3s0-4s1-5s0-6s1-7s0, 0s0_2__1s1-3s1-4s1-5s0-6s0-7s0, 0s0_3__1s0-2s0-4s0-5s0-6s0-7s1, 0s0_3__1s0-2s0-4s0-5s1-6s0-7s1, 0s0_3__1s0-2s0-4s1-5s0-6s1-7s0, 0s0_3__1s1-2s0-4s0-5s0-6s0-7s0, 0s0_4__1s0-2s0-3s0-5s0-6s0-7s0, 0s0_4__1s0-2s0-3s0-5s1-6s0-7s0, 0s0_4__1s0-2s0-3s1-5s0-6s0-7s1, 0s0_4__1s0-2s0-3s1-5s1-6s0-7s1, 0s0_4__1s0-2s1-3s0-5s0-6s1-7s0, 0s0_4__1s1-2s0-3s0-5s1-6s0-7s0.

| parent six-bit cube | units | certified | timed out | not reached | all certified |
|---|---|---|---|---|---|
| `0s0_1__2s0-3s0-4s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 | yes |
| `0s0_1__2s0-3s0-4s0-5s1-6s1-7s1` | 1 | 1 | 0 | 0 | yes |
| `0s0_1__2s0-3s0-4s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_1__2s0-3s1-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_1__2s0-3s1-4s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 | yes |
| `0s0_1__2s0-3s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | no |
| `0s0_1__2s0-3s1-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | no |
| `0s0_1__2s1-3s0-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_1__2s1-3s0-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | no |
| `0s0_1__2s1-3s0-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | no |
| `0s0_1__2s1-3s1-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_1__2s1-3s1-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_1__2s1-3s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | no |
| `0s0_1__2s1-3s1-4s1-5s1-6s0-7s1` | 1 | 1 | 0 | 0 | yes |
| `0s0_2__1s0-3s0-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_2__1s0-3s0-4s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_2__1s0-3s0-4s1-5s0-6s1-7s1` | 1 | 1 | 0 | 0 | yes |
| `0s0_2__1s0-3s0-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 | yes |
| `0s0_2__1s0-3s1-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_2__1s0-3s1-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 | no |
| `0s0_2__1s0-3s1-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | no |
| `0s0_2__1s1-3s0-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 | yes |
| `0s0_2__1s1-3s0-4s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_2__1s1-3s0-4s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_2__1s1-3s0-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | no |
| `0s0_2__1s1-3s1-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | no |
| `0s0_2__1s1-3s1-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_2__1s1-3s1-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | no |
| `0s0_3__1s0-2s0-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 | yes |
| `0s0_3__1s0-2s0-4s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 | yes |
| `0s0_3__1s0-2s0-4s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_3__1s0-2s0-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | no |
| `0s0_3__1s0-2s1-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | no |
| `0s0_3__1s0-2s1-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | no |
| `0s0_3__1s0-2s1-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | no |
| `0s0_3__1s1-2s0-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_3__1s1-2s0-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | no |
| `0s0_3__1s1-2s0-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | no |
| `0s0_3__1s1-2s0-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | no |
| `0s0_3__1s1-2s1-4s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | no |
| `0s0_3__1s1-2s1-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | no |
| `0s0_3__1s1-2s1-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | no |
| `0s0_4__1s0-2s0-3s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_4__1s0-2s0-3s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_4__1s0-2s0-3s1-5s0-6s0-7s1` | 1 | 1 | 0 | 0 | yes |
| `0s0_4__1s0-2s0-3s1-5s1-6s0-7s1` | 1 | 1 | 0 | 0 | yes |
| `0s0_4__1s0-2s1-3s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_4__1s0-2s1-3s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | no |
| `0s0_4__1s0-2s1-3s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | no |
| `0s0_4__1s0-2s1-3s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | no |
| `0s0_4__1s1-2s0-3s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_4__1s1-2s0-3s1-5s0-6s0-7s0` | 1 | 0 | 0 | 1 | no |
| `0s0_4__1s1-2s0-3s1-5s1-6s0-7s1` | 1 | 0 | 0 | 1 | no |

