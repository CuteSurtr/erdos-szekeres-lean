# C3W3 C9

Task: `results/C3W3/TASK.md` at 640a56c2, with V = C9, LIST = C_s1two.tsv, j = 9, N = 18, LANES = 1, JOBS = 3, SLICE = 2.0, H = 6.0.
Start 2026-10-21 04:43:17 UTC, END 10:28:17 UTC. One lane (`lane0.sh`), `--jobs 3`, slice 2.0 h per root.

## Tools and base CNF
- C3-S tools: worktree of 132398c at /opt/c3s, unmodified.
- CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04.
- cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa. The example prints `s VERIFIED UNSAT`.
- lrat-check from drat-trim 2e3b2dc0ecf938addbd779d42877b6ed69d9a985, with the E2 patch. Sanity check: `3 0 0` on {1},{-1} is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF: `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches).
Details are in `tools.txt`.

## Seeding
634 records were seeded at the start of /opt/work/out0.jsonl: 610 certified and 24 split. They cover the three partial roots:
- 0s0-1s1_4s0-5s1: 156, from C3WAVE1/C04
- 0s0-4s1_5s1-9s0: 174, from C3WAVE2/K42
- 0s0-1s1_7s0-9s1: 304, from C3WAVE1/C21

`out.jsonl` holds only the 2,360 new records, without the seeded lines.

## Results
Out of 33 roots, 9 were closed, 1 is partial and 23 were not reached. A closed root has open_frontier 0 in close_tree, with the seeded records counted for the two partial roots. Depths count the node's layers: the root is d2. A timeout is a node that stayed UNKNOWN at its cap and was then split. Solve and check times are summed over the new records.

| row | root | stratum | prior | status | certified by depth | splits | timeouts | solve h | check h |
|---|---|---|---|---|---|---|---|---|---|
| 9 | 0s0-1s1_4s0-5s1 | H6(1,1)/two | partial | closed | d3: 84, d4: 314 | 0 | 0 | 1.27 | 1.88 |
| 27 | 0s0-4s1_5s1-9s0 | H6(4,1)/two | partial | closed | d3: 84, d4: 296 | 0 | 0 | 0.91 | 1.78 |
| 45 | 0s0-2s1_3s1-4s1 | H6(2,1)/two | untouched | closed | d2: 1 | 0 | 0 | 0.01 | 0.01 |
| 63 | 0s0-2s1_4s1-7s1 | H6(2,1)/two | untouched | closed | d2: 1 | 0 | 0 | 0.01 | 0.01 |
| 81 | 0s0-3s1_1s0-2s0 | H6(3,1)/two | untouched | closed | d2: 1 | 0 | 0 | 0.01 | 0.01 |
| 99 | 0s0-3s1_1s1-6s0 | H6(3,1)/two | untouched | closed | d3: 84, d4: 462 | 8 | 1 | 1.21 | 2.39 |
| 117 | 0s0-3s1_4s0-9s0 | H6(3,1)/two | untouched | closed | d2: 1 | 0 | 0 | 0.06 | 0.01 |
| 135 | 0s0-3s1_5s0-8s1 | H6(3,1)/two | untouched | closed | d3: 84, d4: 462 | 8 | 1 | 1.51 | 2.52 |
| 153 | 0s0-4s1_1s0-10s1 | H6(4,1)/two | untouched | closed | d2: 1 | 0 | 0 | 0.02 | 0.01 |
| 171 | 0s0-4s1_1s1-3s0 | H6(4,1)/two | untouched | partial | d4: 458 | 8 | 1 | 0.77 | 1.86 |
| 189 | 0s0-4s1_2s0-7s1 | H6(4,1)/two | untouched | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 207 | 0s0-4s1_5s1-7s0 | H6(4,1)/two | untouched | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 225 | 0s0-5s1_1s0-10s0 | H6(5,1)/two | untouched | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 243 | 0s0-5s1_1s1-2s0 | H6(5,1)/two | untouched | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 261 | 0s0-5s1_2s0-6s1 | H6(5,1)/two | untouched | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 279 | 0s0-5s1_6s0-10s0 | H6(5,1)/two | untouched | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 297 | 0s0-5s1_7s0-9s1 | H6(5,1)/two | untouched | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 315 | 0s0-1s1_7s0-9s1 | H6(1,1)/two | partial | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 333 | 0s0-2s1_1s1-5s0 | H6(2,1)/two | untouched | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 351 | 0s0-2s1_6s0-10s0 | H6(2,1)/two | untouched | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 369 | 0s0-2s1_7s1-10s1 | H6(2,1)/two | untouched | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 387 | 0s0-3s1_2s0-10s0 | H6(3,1)/two | untouched | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 405 | 0s0-3s1_2s1-5s1 | H6(3,1)/two | untouched | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 423 | 0s0-3s1_6s1-10s0 | H6(3,1)/two | untouched | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 441 | 0s0-3s1_8s0-10s1 | H6(3,1)/two | untouched | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 459 | 0s0-4s1_2s1-5s0 | H6(4,1)/two | untouched | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 477 | 0s0-4s1_3s0-8s0 | H6(4,1)/two | untouched | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 495 | 0s0-4s1_6s0-10s1 | H6(4,1)/two | untouched | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 513 | 0s0-4s1_8s1-10s1 | H6(4,1)/two | untouched | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 531 | 0s0-5s1_3s0-6s1 | H6(5,1)/two | untouched | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 549 | 0s0-5s1_3s1-9s1 | H6(5,1)/two | untouched | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 567 | 0s0-5s1_4s1-8s1 | H6(5,1)/two | untouched | not reached | - | 0 | 0 | 0.00 | 0.00 |
| 585 | 0s0-5s1_9s0-10s1 | H6(5,1)/two | untouched | not reached | - | 0 | 0 | 0.00 | 0.00 |

| stratum | closed | partial | not reached | new certified | timeouts | solve h | check h |
|---|---|---|---|---|---|---|---|
| H6(1,1)/two | 1 | 0 | 1 | 398 | 0 | 1.27 | 1.88 |
| H6(4,1)/two | 2 | 1 | 6 | 839 | 1 | 1.70 | 3.65 |
| H6(2,1)/two | 2 | 0 | 3 | 2 | 0 | 0.02 | 0.01 |
| H6(3,1)/two | 4 | 0 | 4 | 1094 | 2 | 2.79 | 4.92 |
| H6(5,1)/two | 0 | 0 | 9 | 0 | 0 | 0.00 | 0.00 |

new records: 2360; certified 2333; splits 24

Root 0s0-4s1_1s1-3s0 was running at END. I killed its runner at 10:31 UTC, when close_tree had not stopped on its own. Records of killed jobs were never written, so there are no `cake_lpr: none` records to re-check. Partial roots that were not reached keep their earlier records in the waves listed above.

`compose.txt` reports 2333 certified nodes. The class is not covered, as expected.

## Flags
- SAT FOUND: none.
- PROOF NOT ACCEPTED: none.
- Uncertified UNSAT: none.
- Memory: no problems. Peak use was about 11 of 15 GB.
