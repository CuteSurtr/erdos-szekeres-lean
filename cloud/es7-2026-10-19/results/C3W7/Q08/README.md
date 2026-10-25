# C3W7 / Q08: nine-bit σ-cubes of the H3/one roots, shard 8 of 36 of W7.tsv

**Result: of 53 units, 29 were certified, 22 timed out at 900 s, and 2 were not reached. No SAT, no proof rejection, no memory problem, and no unit ended early.** The 2 units that were not reached had started, but they were still solving when the lanes were killed at END.

## Setup

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 10:48:42 UTC, END 15:03:42 UTC (H = 4.5 h, minus 15 min), on 2026-10-25. The task was `results/C3W7/TASK.md` at 39bb1bac, with V = Q08, LIST = W7.tsv, j = 8 and N = 36.

- Tools: a worktree of cad4e050 at `/opt/c3u2`, with TOOLS = `results/C3U2/tools`, used unmodified. `compose.py` was not run.
- CaDiCaL c60730422e758ef1cebe7aeddf2dda31c996bf04 (3.0.1). cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa: its example prints `s VERIFIED UNSAT`. lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with the E2 patch. Sanity test: both checkers reject `3 0 0` and accept `3 0 1 2 0`.
- Base CNF: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da`, which matches. Details are in `tools.txt`.
- Units: the 53 rows of W7.tsv with row ≡ 8 (mod 36) (`units.tsv`). No records were seeded.
- 3 lanes (`lane.sh`, `lane0.sh` to `lane2.sh`). Each lane ran this command once per unit: `close_tree.py base.cnf out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`.
- Lane 2 finished its 17 units at 14:53. Lanes 0 and 1 were killed at END (whole process groups), each in the middle of a unit.

## Outcome

- Certified: 29 nodes. Every one has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`, and none has cake_lpr `none`.
- Timed out at 900 s: 22. Each wrote its layer-split record, as the task intends: 22 split records in `out.jsonl`, with their children left unsolved. The open_frontier lines of these units sum to 990 children, and there are 0 unsplittable nodes.
- `out.jsonl` has 73 records: 51 solve records and 22 split records.
- Summed time over all solve records: 41,178 s solving and 2,668 s checking.
- No `recheck.jsonl`: no PROOF NOT ACCEPTED occurred, and no checker was killed at END.

| row | unit | parent six-bit cube | result | solve s | check s |
|---|---|---|---|---|---|
| 8 | `0s0_1__2s0-3s0-4s0-5s0-6s0-7s1-8s0-9s0-10s0` | `0s0_1__2s0-3s0-4s0-5s0-6s0-7s1` | certified | 494.3 | 85.8 |
| 44 | `0s0_1__2s0-3s0-4s0-5s1-6s0-7s1-8s1-9s0-10s0` | `0s0_1__2s0-3s0-4s0-5s1-6s0-7s1` | certified | 759.4 | 100.1 |
| 80 | `0s0_1__2s0-3s0-4s1-5s0-6s1-7s0-8s0-9s0-10s0` | `0s0_1__2s0-3s0-4s1-5s0-6s1-7s0` | certified | 592.1 | 92.5 |
| 116 | `0s0_1__2s0-3s0-4s1-5s1-6s1-7s0-8s1-9s0-10s0` | `0s0_1__2s0-3s0-4s1-5s1-6s1-7s0` | timed out at 900 | 900.1 | – |
| 152 | `0s0_1__2s0-3s1-4s0-5s0-6s1-7s1-8s0-9s0-10s0` | `0s0_1__2s0-3s1-4s0-5s0-6s1-7s1` | certified | 876.6 | 112.7 |
| 188 | `0s0_1__2s0-3s1-4s0-5s1-6s1-7s1-8s1-9s0-10s0` | `0s0_1__2s0-3s1-4s0-5s1-6s1-7s1` | timed out at 900 | 900.1 | – |
| 224 | `0s0_1__2s0-3s1-4s1-5s1-6s0-7s0-8s0-9s0-10s0` | `0s0_1__2s0-3s1-4s1-5s1-6s0-7s0` | certified | 728.2 | 100.6 |
| 260 | `0s0_1__2s1-3s0-4s0-5s0-6s0-7s0-8s1-9s0-10s0` | `0s0_1__2s1-3s0-4s0-5s0-6s0-7s0` | certified | 624.9 | 87.0 |
| 296 | `0s0_1__2s1-3s0-4s0-5s1-6s0-7s1-8s0-9s0-10s0` | `0s0_1__2s1-3s0-4s0-5s1-6s0-7s1` | certified | 751.2 | 105.3 |
| 332 | `0s0_1__2s1-3s0-4s1-5s0-6s0-7s1-8s1-9s0-10s0` | `0s0_1__2s1-3s0-4s1-5s0-6s0-7s1` | timed out at 900 | 900.1 | – |
| 368 | `0s0_1__2s1-3s0-4s1-5s1-6s1-7s0-8s0-9s0-10s0` | `0s0_1__2s1-3s0-4s1-5s1-6s1-7s0` | certified | 752.8 | 98.5 |
| 404 | `0s0_1__2s1-3s1-4s0-5s0-6s1-7s0-8s1-9s0-10s0` | `0s0_1__2s1-3s1-4s0-5s0-6s1-7s0` | certified | 837.9 | 99.0 |
| 440 | `0s0_1__2s1-3s1-4s0-5s1-6s1-7s1-8s0-9s0-10s0` | `0s0_1__2s1-3s1-4s0-5s1-6s1-7s1` | certified | 764.0 | 98.3 |
| 476 | `0s0_1__2s1-3s1-4s1-5s0-6s1-7s1-8s1-9s0-10s0` | `0s0_1__2s1-3s1-4s1-5s0-6s1-7s1` | certified | 816.9 | 97.8 |
| 512 | `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0-8s0-9s0-10s0` | `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0` | certified | 469.4 | 80.5 |
| 548 | `0s0_2__1s0-3s0-4s0-5s1-6s0-7s0-8s1-9s0-10s0` | `0s0_2__1s0-3s0-4s0-5s1-6s0-7s0` | certified | 833.0 | 99.9 |
| 584 | `0s0_2__1s0-3s0-4s1-5s0-6s0-7s1-8s0-9s0-10s0` | `0s0_2__1s0-3s0-4s1-5s0-6s0-7s1` | certified | 714.8 | 91.9 |
| 620 | `0s0_2__1s0-3s0-4s1-5s1-6s0-7s1-8s1-9s0-10s0` | `0s0_2__1s0-3s0-4s1-5s1-6s0-7s1` | timed out at 900 | 900.1 | – |
| 656 | `0s0_2__1s0-3s1-4s0-5s0-6s1-7s0-8s0-9s0-10s0` | `0s0_2__1s0-3s1-4s0-5s0-6s1-7s0` | certified | 632.4 | 83.7 |
| 692 | `0s0_2__1s0-3s1-4s0-5s1-6s1-7s0-8s1-9s0-10s0` | `0s0_2__1s0-3s1-4s0-5s1-6s1-7s0` | timed out at 900 | 900.1 | – |
| 728 | `0s0_2__1s0-3s1-4s1-5s0-6s1-7s1-8s0-9s0-10s0` | `0s0_2__1s0-3s1-4s1-5s0-6s1-7s1` | timed out at 900 | 900.1 | – |
| 764 | `0s0_2__1s0-3s1-4s1-5s1-6s1-7s1-8s1-9s0-10s0` | `0s0_2__1s0-3s1-4s1-5s1-6s1-7s1` | certified | 841.9 | 102.7 |
| 800 | `0s0_2__1s1-3s0-4s0-5s1-6s0-7s0-8s0-9s0-10s0` | `0s0_2__1s1-3s0-4s0-5s1-6s0-7s0` | certified | 670.1 | 86.2 |
| 836 | `0s0_2__1s1-3s0-4s1-5s0-6s0-7s0-8s1-9s0-10s0` | `0s0_2__1s1-3s0-4s1-5s0-6s0-7s0` | certified | 815.0 | 98.9 |
| 872 | `0s0_2__1s1-3s0-4s1-5s1-6s0-7s1-8s0-9s0-10s0` | `0s0_2__1s1-3s0-4s1-5s1-6s0-7s1` | timed out at 900 | 900.1 | – |
| 908 | `0s0_2__1s1-3s1-4s0-5s0-6s0-7s1-8s1-9s0-10s0` | `0s0_2__1s1-3s1-4s0-5s0-6s0-7s1` | timed out at 900 | 900.1 | – |
| 944 | `0s0_2__1s1-3s1-4s0-5s1-6s1-7s0-8s0-9s0-10s0` | `0s0_2__1s1-3s1-4s0-5s1-6s1-7s0` | certified | 899.4 | 86.0 |
| 980 | `0s0_2__1s1-3s1-4s1-5s0-6s1-7s0-8s1-9s0-10s0` | `0s0_2__1s1-3s1-4s1-5s0-6s1-7s0` | timed out at 900 | 900.0 | – |
| 1016 | `0s0_2__1s1-3s1-4s1-5s1-6s1-7s1-8s0-9s0-10s0` | `0s0_2__1s1-3s1-4s1-5s1-6s1-7s1` | certified | 818.7 | 88.2 |
| 1052 | `0s0_3__1s0-2s0-4s0-5s0-6s1-7s1-8s1-9s0-10s0` | `0s0_3__1s0-2s0-4s0-5s0-6s1-7s1` | timed out at 900 | 900.1 | – |
| 1088 | `0s0_3__1s0-2s0-4s1-5s0-6s0-7s0-8s0-9s0-10s0` | `0s0_3__1s0-2s0-4s1-5s0-6s0-7s0` | certified | 513.1 | 71.3 |
| 1124 | `0s0_3__1s0-2s0-4s1-5s1-6s0-7s0-8s1-9s0-10s0` | `0s0_3__1s0-2s0-4s1-5s1-6s0-7s0` | timed out at 900 | 900.1 | – |
| 1160 | `0s0_3__1s0-2s1-4s0-5s0-6s0-7s1-8s0-9s0-10s0` | `0s0_3__1s0-2s1-4s0-5s0-6s0-7s1` | certified | 701.2 | 82.8 |
| 1196 | `0s0_3__1s0-2s1-4s0-5s1-6s0-7s1-8s1-9s0-10s0` | `0s0_3__1s0-2s1-4s0-5s1-6s0-7s1` | timed out at 900 | 900.1 | – |
| 1232 | `0s0_3__1s0-2s1-4s1-5s0-6s1-7s0-8s0-9s0-10s0` | `0s0_3__1s0-2s1-4s1-5s0-6s1-7s0` | certified | 872.3 | 101.4 |
| 1268 | `0s0_3__1s0-2s1-4s1-5s1-6s1-7s0-8s1-9s0-10s0` | `0s0_3__1s0-2s1-4s1-5s1-6s1-7s0` | timed out at 900 | 900.1 | – |
| 1304 | `0s0_3__1s1-2s0-4s0-5s0-6s1-7s1-8s0-9s0-10s0` | `0s0_3__1s1-2s0-4s0-5s0-6s1-7s1` | timed out at 900 | 900.1 | – |
| 1340 | `0s0_3__1s1-2s0-4s0-5s1-6s1-7s1-8s1-9s0-10s0` | `0s0_3__1s1-2s0-4s0-5s1-6s1-7s1` | timed out at 900 | 900.1 | – |
| 1376 | `0s0_3__1s1-2s0-4s1-5s1-6s0-7s0-8s0-9s0-10s0` | `0s0_3__1s1-2s0-4s1-5s1-6s0-7s0` | certified | 773.5 | 87.9 |
| 1412 | `0s0_3__1s1-2s1-4s0-5s0-6s0-7s0-8s1-9s0-10s0` | `0s0_3__1s1-2s1-4s0-5s0-6s0-7s0` | certified | 823.7 | 93.5 |
| 1448 | `0s0_3__1s1-2s1-4s0-5s1-6s0-7s1-8s0-9s0-10s0` | `0s0_3__1s1-2s1-4s0-5s1-6s0-7s1` | timed out at 900 | 900.1 | – |
| 1484 | `0s0_3__1s1-2s1-4s1-5s0-6s0-7s1-8s1-9s0-10s0` | `0s0_3__1s1-2s1-4s1-5s0-6s0-7s1` | timed out at 900 | 900.1 | – |
| 1520 | `0s0_3__1s1-2s1-4s1-5s1-6s1-7s0-8s0-9s0-10s0` | `0s0_3__1s1-2s1-4s1-5s1-6s1-7s0` | timed out at 900 | 900.1 | – |
| 1556 | `0s0_4__1s0-2s0-3s0-5s0-6s1-7s0-8s1-9s0-10s0` | `0s0_4__1s0-2s0-3s0-5s0-6s1-7s0` | certified | 809.6 | 88.6 |
| 1592 | `0s0_4__1s0-2s0-3s0-5s1-6s1-7s1-8s0-9s0-10s0` | `0s0_4__1s0-2s0-3s0-5s1-6s1-7s1` | certified | 880.1 | 90.4 |
| 1628 | `0s0_4__1s0-2s0-3s1-5s0-6s1-7s1-8s1-9s0-10s0` | `0s0_4__1s0-2s0-3s1-5s0-6s1-7s1` | timed out at 900 | 900.1 | – |
| 1664 | `0s0_4__1s0-2s1-3s0-5s0-6s0-7s0-8s0-9s0-10s0` | `0s0_4__1s0-2s1-3s0-5s0-6s0-7s0` | certified | 584.8 | 75.4 |
| 1700 | `0s0_4__1s0-2s1-3s0-5s1-6s0-7s0-8s1-9s0-10s0` | `0s0_4__1s0-2s1-3s0-5s1-6s0-7s0` | timed out at 900 | 900.2 | – |
| 1736 | `0s0_4__1s0-2s1-3s1-5s0-6s0-7s1-8s0-9s0-10s0` | `0s0_4__1s0-2s1-3s1-5s0-6s0-7s1` | timed out at 900 | 900.1 | – |
| 1772 | `0s0_4__1s0-2s1-3s1-5s1-6s0-7s1-8s1-9s0-10s0` | `0s0_4__1s0-2s1-3s1-5s1-6s0-7s1` | timed out at 900 | 900.1 | – |
| 1808 | `0s0_4__1s1-2s0-3s0-5s0-6s1-7s0-8s0-9s0-10s0` | `0s0_4__1s1-2s0-3s0-5s0-6s1-7s0` | certified | 724.3 | 81.4 |
| 1844 | `0s0_4__1s1-2s0-3s0-5s1-6s1-7s0-8s1-9s0-10s0` | `0s0_4__1s1-2s0-3s0-5s1-6s1-7s0` | not reached (started, killed at END unsolved) | – | – |
| 1880 | `0s0_4__1s1-2s0-3s1-5s0-6s1-7s1-8s0-9s0-10s0` | `0s0_4__1s1-2s0-3s1-5s0-6s1-7s1` | not reached (started, killed at END unsolved) | – | – |

**Per root**

| root | units | certified | timed out | not reached |
|---|---|---|---|---|
| 0s0_1 | 14 | 11 | 3 | 0 |
| 0s0_2 | 15 | 9 | 6 | 0 |
| 0s0_3 | 14 | 5 | 9 | 0 |
| 0s0_4 | 10 | 4 | 4 | 2 |

**Per parent six-bit cube**

| parent | units here | certified | timed out | not reached |
|---|---|---|---|---|
| `0s0_1__2s0-3s0-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s1-4s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s1-4s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s0-4s1-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s1-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s0-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s1-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s1-4s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s0-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s0-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s0-4s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s0-3s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s1-2s0-3s0-5s1-6s1-7s0` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s0-6s1-7s1` | 1 | 0 | 0 | 1 |

Parents all of whose units on this machine were certified (29):
- `0s0_1__2s0-3s0-4s0-5s0-6s0-7s1`
- `0s0_1__2s0-3s0-4s0-5s1-6s0-7s1`
- `0s0_1__2s0-3s0-4s1-5s0-6s1-7s0`
- `0s0_1__2s0-3s1-4s0-5s0-6s1-7s1`
- `0s0_1__2s0-3s1-4s1-5s1-6s0-7s0`
- `0s0_1__2s1-3s0-4s0-5s0-6s0-7s0`
- `0s0_1__2s1-3s0-4s0-5s1-6s0-7s1`
- `0s0_1__2s1-3s0-4s1-5s1-6s1-7s0`
- `0s0_1__2s1-3s1-4s0-5s0-6s1-7s0`
- `0s0_1__2s1-3s1-4s0-5s1-6s1-7s1`
- `0s0_1__2s1-3s1-4s1-5s0-6s1-7s1`
- `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0`
- `0s0_2__1s0-3s0-4s0-5s1-6s0-7s0`
- `0s0_2__1s0-3s0-4s1-5s0-6s0-7s1`
- `0s0_2__1s0-3s1-4s0-5s0-6s1-7s0`
- `0s0_2__1s0-3s1-4s1-5s1-6s1-7s1`
- `0s0_2__1s1-3s0-4s0-5s1-6s0-7s0`
- `0s0_2__1s1-3s0-4s1-5s0-6s0-7s0`
- `0s0_2__1s1-3s1-4s0-5s1-6s1-7s0`
- `0s0_2__1s1-3s1-4s1-5s1-6s1-7s1`
- `0s0_3__1s0-2s0-4s1-5s0-6s0-7s0`
- `0s0_3__1s0-2s1-4s0-5s0-6s0-7s1`
- `0s0_3__1s0-2s1-4s1-5s0-6s1-7s0`
- `0s0_3__1s1-2s0-4s1-5s1-6s0-7s0`
- `0s0_3__1s1-2s1-4s0-5s0-6s0-7s0`
- `0s0_4__1s0-2s0-3s0-5s0-6s1-7s0`
- `0s0_4__1s0-2s0-3s0-5s1-6s1-7s1`
- `0s0_4__1s0-2s1-3s0-5s0-6s0-7s0`
- `0s0_4__1s1-2s0-3s0-5s0-6s1-7s0`

Certified solve times (n=29): min 469.4, Q1 670.1, median 759.4, Q3 823.7, p90 872.3, max 899.4; above 300 s: 29

Totals: {'certified': 29, 'timed out at 900': 22, 'not reached': 2}
