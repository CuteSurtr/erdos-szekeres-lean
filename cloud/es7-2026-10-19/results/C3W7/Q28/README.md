# C3W7 / Q28: nine-bit σ-cubes of the H3/one roots at cap 900 (W7.tsv, shard 28 of 36)

**Result: 28 of my 53 nine-bit units certified, 20 timed out at 900 s, 3 were killed at END while solving, and 2 were not reached. No SAT, no proof rejection, no memory problem, and no unit ended early.**

## Setup

- One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 10:46:24 UTC, lanes started 11:01:51, END 15:01:24 (start + 4.5 h − 15 min). Task: `results/C3W7/TASK.md` at 39bb1bac, with V = Q28, LIST = W7.tsv, j = 28, N = 36, H = 4.5.
- Tools (`tools.txt`): C3U2 tools from a worktree of cad4e050 at `/opt/c3u2`, used unmodified. CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (its example prints `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch. The checker sanity test passed: `3 0 0` on {1},{-1} is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da`, which matches.
- Units: the rows of `lists/W7.tsv` with row ≡ 28 (mod 36), 53 units in `units.tsv`, nothing seeded. 3 lanes (`lane.sh`, `lane0..2.sh`); lane k took positions ≡ k (mod 3). Each unit ran `close_tree.py … --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`. `compose.py` was not run.
- `out.jsonl` holds lane 0's records, then lane 1's, then lane 2's: 28 certified UNSAT records, plus 20 UNKNOWN records at 900 s, each followed by its layer-split record (45 children, left unsolved in `open_frontier` as the task intends). There is no `recheck.jsonl`, because no recheck was needed.

## Per unit

| row | unit | lane | result |
|---|---|---|---|
| 28 | `0s0_1__2s0-3s0-4s0-5s0-6s1-7s1-8s1-9s0-10s0` | 0 | certified, solve 868.5 s, check 126.9 s |
| 64 | `0s0_1__2s0-3s0-4s1-5s0-6s0-7s0-8s0-9s0-10s0` | 1 | certified, solve 546.4 s, check 94.8 s |
| 100 | `0s0_1__2s0-3s0-4s1-5s1-6s0-7s0-8s1-9s0-10s0` | 2 | certified, solve 812.6 s, check 119.6 s |
| 136 | `0s0_1__2s0-3s1-4s0-5s0-6s0-7s1-8s0-9s0-10s0` | 0 | certified, solve 658.9 s, check 113.4 s |
| 172 | `0s0_1__2s0-3s1-4s0-5s1-6s0-7s1-8s1-9s0-10s0` | 1 | timed out at 900 (900.1 s) |
| 208 | `0s0_1__2s0-3s1-4s1-5s0-6s1-7s0-8s0-9s0-10s0` | 2 | certified, solve 716.3 s, check 113.8 s |
| 244 | `0s0_1__2s0-3s1-4s1-5s1-6s1-7s0-8s1-9s0-10s0` | 0 | certified, solve 852.0 s, check 134.7 s |
| 280 | `0s0_1__2s1-3s0-4s0-5s0-6s1-7s1-8s0-9s0-10s0` | 1 | certified, solve 829.7 s, check 121.5 s |
| 316 | `0s0_1__2s1-3s0-4s0-5s1-6s1-7s1-8s1-9s0-10s0` | 2 | timed out at 900 (900.1 s) |
| 352 | `0s0_1__2s1-3s0-4s1-5s1-6s0-7s0-8s0-9s0-10s0` | 0 | certified, solve 761.5 s, check 115.7 s |
| 388 | `0s0_1__2s1-3s1-4s0-5s0-6s0-7s0-8s1-9s0-10s0` | 1 | certified, solve 720.5 s, check 99.5 s |
| 424 | `0s0_1__2s1-3s1-4s0-5s1-6s0-7s1-8s0-9s0-10s0` | 2 | certified, solve 835.2 s, check 102.6 s |
| 460 | `0s0_1__2s1-3s1-4s1-5s0-6s0-7s1-8s1-9s0-10s0` | 0 | timed out at 900 (900.2 s) |
| 496 | `0s0_1__2s1-3s1-4s1-5s1-6s1-7s0-8s0-9s0-10s0` | 1 | certified, solve 750.7 s, check 119.9 s |
| 532 | `0s0_2__1s0-3s0-4s0-5s0-6s1-7s0-8s1-9s0-10s0` | 2 | certified, solve 838.3 s, check 112.5 s |
| 568 | `0s0_2__1s0-3s0-4s0-5s1-6s1-7s1-8s0-9s0-10s0` | 0 | timed out at 900 (900.2 s) |
| 604 | `0s0_2__1s0-3s0-4s1-5s0-6s1-7s1-8s1-9s0-10s0` | 1 | timed out at 900 (900.1 s) |
| 640 | `0s0_2__1s0-3s1-4s0-5s0-6s0-7s0-8s0-9s0-10s0` | 2 | certified, solve 520.9 s, check 84.3 s |
| 676 | `0s0_2__1s0-3s1-4s0-5s1-6s0-7s0-8s1-9s0-10s0` | 0 | timed out at 900 (900.1 s) |
| 712 | `0s0_2__1s0-3s1-4s1-5s0-6s0-7s1-8s0-9s0-10s0` | 1 | certified, solve 843.8 s, check 112.3 s |
| 748 | `0s0_2__1s0-3s1-4s1-5s1-6s0-7s1-8s1-9s0-10s0` | 2 | timed out at 900 (900.1 s) |
| 784 | `0s0_2__1s1-3s0-4s0-5s0-6s1-7s0-8s0-9s0-10s0` | 0 | certified, solve 725.9 s, check 103.4 s |
| 820 | `0s0_2__1s1-3s0-4s0-5s1-6s1-7s0-8s1-9s0-10s0` | 1 | timed out at 900 (900.1 s) |
| 856 | `0s0_2__1s1-3s0-4s1-5s0-6s1-7s1-8s0-9s0-10s0` | 2 | timed out at 900 (900.1 s) |
| 892 | `0s0_2__1s1-3s0-4s1-5s1-6s1-7s1-8s1-9s0-10s0` | 0 | timed out at 900 (900.1 s) |
| 928 | `0s0_2__1s1-3s1-4s0-5s1-6s0-7s0-8s0-9s0-10s0` | 1 | certified, solve 813.5 s, check 98.8 s |
| 964 | `0s0_2__1s1-3s1-4s1-5s0-6s0-7s0-8s1-9s0-10s0` | 2 | timed out at 900 (900.1 s) |
| 1000 | `0s0_2__1s1-3s1-4s1-5s1-6s0-7s1-8s0-9s0-10s0` | 0 | certified, solve 841.5 s, check 92.3 s |
| 1036 | `0s0_3__1s0-2s0-4s0-5s0-6s0-7s1-8s1-9s0-10s0` | 1 | certified, solve 708.2 s, check 106.5 s |
| 1072 | `0s0_3__1s0-2s0-4s0-5s1-6s1-7s0-8s0-9s0-10s0` | 2 | certified, solve 818.4 s, check 119.3 s |
| 1108 | `0s0_3__1s0-2s0-4s1-5s0-6s1-7s0-8s1-9s0-10s0` | 0 | certified, solve 832.9 s, check 101.7 s |
| 1144 | `0s0_3__1s0-2s0-4s1-5s1-6s1-7s1-8s0-9s0-10s0` | 1 | certified, solve 887.8 s, check 111.1 s |
| 1180 | `0s0_3__1s0-2s1-4s0-5s0-6s1-7s1-8s1-9s0-10s0` | 2 | timed out at 900 (900.1 s) |
| 1216 | `0s0_3__1s0-2s1-4s1-5s0-6s0-7s0-8s0-9s0-10s0` | 0 | certified, solve 636.3 s, check 91.4 s |
| 1252 | `0s0_3__1s0-2s1-4s1-5s1-6s0-7s0-8s1-9s0-10s0` | 1 | timed out at 900 (900.1 s) |
| 1288 | `0s0_3__1s1-2s0-4s0-5s0-6s0-7s1-8s0-9s0-10s0` | 2 | certified, solve 648.0 s, check 85.4 s |
| 1324 | `0s0_3__1s1-2s0-4s0-5s1-6s0-7s1-8s1-9s0-10s0` | 0 | timed out at 900 (900.1 s) |
| 1360 | `0s0_3__1s1-2s0-4s1-5s0-6s1-7s0-8s0-9s0-10s0` | 1 | certified, solve 733.3 s, check 100.1 s |
| 1396 | `0s0_3__1s1-2s0-4s1-5s1-6s1-7s0-8s1-9s0-10s0` | 2 | certified, solve 873.5 s, check 128.3 s |
| 1432 | `0s0_3__1s1-2s1-4s0-5s0-6s1-7s1-8s0-9s0-10s0` | 0 | timed out at 900 (900.1 s) |
| 1468 | `0s0_3__1s1-2s1-4s0-5s1-6s1-7s1-8s1-9s0-10s0` | 1 | timed out at 900 (900.1 s) |
| 1504 | `0s0_3__1s1-2s1-4s1-5s1-6s0-7s0-8s0-9s0-10s0` | 2 | timed out at 900 (900.1 s) |
| 1540 | `0s0_4__1s0-2s0-3s0-5s0-6s0-7s0-8s1-9s0-10s0` | 0 | certified, solve 483.0 s, check 78.1 s |
| 1576 | `0s0_4__1s0-2s0-3s0-5s1-6s0-7s1-8s0-9s0-10s0` | 1 | certified, solve 671.8 s, check 106.5 s |
| 1612 | `0s0_4__1s0-2s0-3s1-5s0-6s0-7s1-8s1-9s0-10s0` | 2 | certified, solve 795.6 s, check 101.3 s |
| 1648 | `0s0_4__1s0-2s0-3s1-5s1-6s1-7s0-8s0-9s0-10s0` | 0 | timed out at 900 (900.1 s) |
| 1684 | `0s0_4__1s0-2s1-3s0-5s0-6s1-7s0-8s1-9s0-10s0` | 1 | timed out at 900 (900.1 s) |
| 1720 | `0s0_4__1s0-2s1-3s0-5s1-6s1-7s1-8s0-9s0-10s0` | 2 | timed out at 900 (900.1 s) |
| 1756 | `0s0_4__1s0-2s1-3s1-5s0-6s1-7s1-8s1-9s0-10s0` | 0 | killed: started, killed at END (no record) |
| 1792 | `0s0_4__1s1-2s0-3s0-5s0-6s0-7s0-8s0-9s0-10s0` | 1 | killed: started, killed at END (no record) |
| 1828 | `0s0_4__1s1-2s0-3s0-5s1-6s0-7s0-8s1-9s0-10s0` | 2 | killed: started, killed at END (no record) |
| 1864 | `0s0_4__1s1-2s0-3s1-5s0-6s0-7s1-8s0-9s0-10s0` | 0 | notreached: not reached |
| 1900 | `0s0_4__1s1-2s0-3s1-5s1-6s0-7s1-8s1-9s0-10s0` | 1 | notreached: not reached |

"Killed" means the lane was killed at END during the CaDiCaL solve. No record was written, and no checker was killed, so no node has cake_lpr `none`.

## Totals per root and per parent six-bit cube

Stride 36 over the list puts exactly one of each parent's 8 nine-bit cubes on this machine, so each parent row covers one unit.


| root | units | certified | timed out | killed at END | not reached |
|---|---|---|---|---|---|
| `0s0_1` | 14 | 11 | 3 | 0 | 0 |
| `0s0_2` | 14 | 6 | 8 | 0 | 0 |
| `0s0_3` | 14 | 8 | 6 | 0 | 0 |
| `0s0_4` | 11 | 3 | 3 | 3 | 2 |

| parent six-bit cube | units | certified | timed out | killed at END | not reached |
|---|---|---|---|---|---|
| `0s0_1__2s0-3s0-4s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_1__2s0-3s1-4s1-5s1-6s1-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_1__2s1-3s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s1-5s1-6s1-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s1-5s0-6s0-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_2__1s0-3s1-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_2__1s1-3s1-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s1-5s1-6s0-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_3__1s0-2s1-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_3__1s1-2s0-4s1-5s1-6s1-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_3__1s1-2s1-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s0-6s0-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s1-5s0-6s1-7s1` | 1 | 0 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s0-5s0-6s0-7s0` | 1 | 0 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s0-5s1-6s0-7s0` | 1 | 0 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s1-5s0-6s0-7s1` | 1 | 0 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s1-6s0-7s1` | 1 | 0 | 0 | 0 | 1 |

parents all of whose units here were certified: 28
- `0s0_1__2s0-3s0-4s0-5s0-6s1-7s1`
- `0s0_1__2s0-3s0-4s1-5s0-6s0-7s0`
- `0s0_1__2s0-3s0-4s1-5s1-6s0-7s0`
- `0s0_1__2s0-3s1-4s0-5s0-6s0-7s1`
- `0s0_1__2s0-3s1-4s1-5s0-6s1-7s0`
- `0s0_1__2s0-3s1-4s1-5s1-6s1-7s0`
- `0s0_1__2s1-3s0-4s0-5s0-6s1-7s1`
- `0s0_1__2s1-3s0-4s1-5s1-6s0-7s0`
- `0s0_1__2s1-3s1-4s0-5s0-6s0-7s0`
- `0s0_1__2s1-3s1-4s0-5s1-6s0-7s1`
- `0s0_1__2s1-3s1-4s1-5s1-6s1-7s0`
- `0s0_2__1s0-3s0-4s0-5s0-6s1-7s0`
- `0s0_2__1s0-3s1-4s0-5s0-6s0-7s0`
- `0s0_2__1s0-3s1-4s1-5s0-6s0-7s1`
- `0s0_2__1s1-3s0-4s0-5s0-6s1-7s0`
- `0s0_2__1s1-3s1-4s0-5s1-6s0-7s0`
- `0s0_2__1s1-3s1-4s1-5s1-6s0-7s1`
- `0s0_3__1s0-2s0-4s0-5s0-6s0-7s1`
- `0s0_3__1s0-2s0-4s0-5s1-6s1-7s0`
- `0s0_3__1s0-2s0-4s1-5s0-6s1-7s0`
- `0s0_3__1s0-2s0-4s1-5s1-6s1-7s1`
- `0s0_3__1s0-2s1-4s1-5s0-6s0-7s0`
- `0s0_3__1s1-2s0-4s0-5s0-6s0-7s1`
- `0s0_3__1s1-2s0-4s1-5s0-6s1-7s0`
- `0s0_3__1s1-2s0-4s1-5s1-6s1-7s0`
- `0s0_4__1s0-2s0-3s0-5s0-6s0-7s0`
- `0s0_4__1s0-2s0-3s0-5s1-6s0-7s1`
- `0s0_4__1s0-2s0-3s1-5s0-6s0-7s1`

## Solve times of the certified units

- certified n=28: min 483.0, Q1 680.9, median 778.5, Q3 837.5, p90 869.0, max 887.8; above 300 s: 28
- check s: min 78.1, max 134.7, total 2996
- All 28 certified units took more than 300 s. Every unit's solve took at least 483 s, so none ended under 72 s without a certificate.

## SAT / rejections / memory

- SAT: none. PROOF NOT ACCEPTED: none. Every certified record has `c VERIFIED` and `s VERIFIED UNSAT`.
- Memory: peak used memory seen was about 9 GB of 15 GB, with no OOM.
- Not finished at END: killed while solving: `0s0_4__1s0-2s1-3s1-5s0-6s1-7s1-8s1-9s0-10s0`, `0s0_4__1s1-2s0-3s0-5s0-6s0-7s0-8s0-9s0-10s0`, `0s0_4__1s1-2s0-3s0-5s1-6s0-7s0-8s1-9s0-10s0`. Not reached: `0s0_4__1s1-2s0-3s1-5s0-6s0-7s1-8s0-9s0-10s0`, `0s0_4__1s1-2s0-3s1-5s1-6s0-7s1-8s1-9s0-10s0`.
