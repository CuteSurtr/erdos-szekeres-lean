# C3W3 C12

Wave 3 of the 3-fold class (m = 11, k = 7), following `results/C3W3/TASK.md` at 640a56c2 with V = C12, LIST = C_s1two.tsv, j = 12, N = 18, LANES = 1, JOBS = 3, SLICE = 2.0 h, H = 6.0 h. The machine had 4 cores and 15 GB RAM (`env.txt`). Start 04:43:01 UTC, END 10:28:01 UTC.

## Tools and base CNF
- C3-S tools: commit 132398c (132398cdc801ee5df204eda8567b72abdbfc4341), worktree at /opt/c3s, unmodified
- CaDiCaL c60730422e758ef1cebe7aeddf2dda31c996bf04 (3.0.1)
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa; its example gives `s VERIFIED UNSAT`
- lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with the E2 patch applied. Sanity check: `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- base CNF: `p cnf 168399 4154921`, sha256 bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da (matches)

Details are in `tools.txt`.

## Run
There were 32 roots (`roots.tsv`, rows ≡ 12 mod 18) and one lane (`lane0.sh`, `--jobs 3`, 2.0 h slices). The lane reached 7 of the 32 roots: 6 are closed and 1 is partial. At END the lane's process group was killed while it was working on root 0s0-3s1_4s1-5s0. Nodes that were still running at that moment wrote no record, so no record has `cake_lpr: none` and none needed a re-check.

Seeded records: 776 lines at the start of /opt/work/out0.jsonl. They are not in `out.jsonl`.
- 230 for 0s0-1s1_5s0-6s1 (222 certified, 8 split), from C3WAVE1/C05/out.jsonl
- 546 for 0s0-1s1_9s0-10s1 (538 certified, 8 split), from C3WAVE2/K11/out.jsonl. This root was not reached, so these records were never used.

New records: 2139 lines in `out.jsonl`, made of 2103 certified nodes, 4 timeouts and 32 split records. Every UNSAT node was accepted by both cake_lpr (`s VERIFIED UNSAT`) and lrat-check.

No SAT. No proof rejection. No memory problem: peak use was about 9.5 GB of 15 GB, and there were no OOM kills.

Root 0s0-1s1_5s0-6s1 is "closed" because its tree is complete when the seeded records are combined with the new ones. Depth means the number of layers in the node name. Timeouts are nodes that reached the CaDiCaL cap (status UNKNOWN) and were then split. Times are the sums of the solve_s and check_s values of the new records.

## Per root
| row | root | stratum | status | certified by depth | splits | timeouts | solve h | check h |
|---|---|---|---|---|---|---|---|---|
| 12 | 0s0-1s1_5s0-6s1 | H6(1,1)/two | closed | d3: 84, d4: 240 | 0 | 0 | 1.13 | 1.62 |
| 30 | 0s0-2s1_1s0-4s0 | H6(2,1)/two | closed | d2: 1 | 0 | 0 | 0.01 | 0.01 |
| 48 | 0s0-2s1_3s1-7s1 | H6(2,1)/two | closed | d2: 1 | 0 | 0 | 0.05 | 0.01 |
| 66 | 0s0-2s1_4s1-9s1 | H6(2,1)/two | closed | d3: 84, d4: 462 | 8 | 1 | 1.35 | 2.52 |
| 84 | 0s0-3s1_1s0-4s1 | H6(3,1)/two | closed | d3: 84, d4: 462 | 8 | 1 | 1.74 | 2.71 |
| 102 | 0s0-3s1_1s1-7s1 | H6(3,1)/two | closed | d3: 84, d4: 462 | 8 | 1 | 1.49 | 2.58 |
| 120 | 0s0-3s1_4s1-5s0 | H6(3,1)/two | partial | d4: 139 | 8 | 1 | 0.29 | 0.59 |
| 138 | 0s0-3s1_5s1-6s0 | H6(3,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 156 | 0s0-4s1_1s0-3s0 | H6(4,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 174 | 0s0-4s1_1s1-6s0 | H6(4,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 192 | 0s0-4s1_2s0-9s0 | H6(4,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 210 | 0s0-4s1_5s1-8s1 | H6(4,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 228 | 0s0-5s1_1s0-2s1 | H6(5,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 246 | 0s0-5s1_1s1-3s1 | H6(5,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 264 | 0s0-5s1_2s0-8s0 | H6(5,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 282 | 0s0-5s1_6s0-7s1 | H6(5,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 300 | 0s0-5s1_7s1-9s1 | H6(5,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 318 | 0s0-1s1_9s0-10s1 | H6(1,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 336 | 0s0-2s1_1s1-8s0 | H6(2,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 354 | 0s0-2s1_6s0-8s1 | H6(2,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 372 | 0s0-2s1_7s1-9s0 | H6(2,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 390 | 0s0-3s1_2s0-4s1 | H6(3,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 408 | 0s0-3s1_2s1-7s1 | H6(3,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 426 | 0s0-3s1_6s1-9s0 | H6(3,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 444 | 0s0-3s1_8s1-10s0 | H6(3,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 462 | 0s0-4s1_2s1-6s1 | H6(4,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 480 | 0s0-4s1_3s0-9s1 | H6(4,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 498 | 0s0-4s1_6s1-9s0 | H6(4,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 516 | 0s0-4s1_9s0-10s0 | H6(4,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 534 | 0s0-5s1_3s0-8s0 | H6(5,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 552 | 0s0-5s1_4s0-6s0 | H6(5,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 570 | 0s0-5s1_6s1-10s0 | H6(5,1)/two | not reached | - | 0 | 0 | 0.00 | 0.00 |

## Totals per stratum

| stratum | closed | partial | not reached | certified | splits | timeouts | solve h | check h |
|---|---|---|---|---|---|---|---|---|
| H6(1,1)/two | 1 | 0 | 1 | 324 | 0 | 0 | 1.13 | 1.62 |
| H6(2,1)/two | 3 | 0 | 3 | 548 | 8 | 1 | 1.40 | 2.54 |
| H6(3,1)/two | 2 | 1 | 5 | 1231 | 24 | 3 | 3.52 | 5.88 |
| H6(4,1)/two | 0 | 0 | 8 | 0 | 0 | 0 | 0.00 | 0.00 |
| H6(5,1)/two | 0 | 0 | 8 | 0 | 0 | 0 | 0.00 | 0.00 |

statuses of new solve records: {'UNSATISFIABLE': 2103, 'UNKNOWN': 4}
cake_lpr values: {'s VERIFIED UNSAT': 2103}

Closed roots: 0s0-1s1_5s0-6s1, 0s0-2s1_1s0-4s0, 0s0-2s1_3s1-7s1, 0s0-2s1_4s1-9s1, 0s0-3s1_1s0-4s1, 0s0-3s1_1s1-7s1.
Partial root: 0s0-3s1_4s1-5s0 (its 8 presplit children, 139 certified depth-4 nodes; resume from `out.jsonl`).
Not reached: the other 25 roots, starting with 0s0-3s1_5s1-6s0.

`compose.txt` lists 2103 certified nodes (it recomputed the sha256 of every node's CNF). The class is not covered, which is expected.
