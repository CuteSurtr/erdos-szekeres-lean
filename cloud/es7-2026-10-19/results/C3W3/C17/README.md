# C3W3 C17: C_s1two.tsv, shard 17 of 18

Values: V = C17, LIST = C_s1two.tsv, j = 17, N = 18, LANES = 1, JOBS = 3, SLICE = 2.0 h, H = 6.0 h, Z = 640a56c2.
Start 04:43:25 UTC (1792557805), END 10:28:25 UTC. Machine: 4 cores, 15 GB RAM (env.txt).

## Tools and base CNF
- C3-S tools: worktree of 132398c at /opt/c3s, used unmodified.
- CaDiCaL c60730422e758ef1cebe7aeddf2dda31c996bf04 (3.0.1); cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (example prints `s VERIFIED UNSAT`); lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with the E2 patch. Sanity check passed: `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF from `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da (matches).

## Run
32 roots (rows ≡ 17 mod 18), one lane (`lane0.sh`) with `--jobs 3`. 11 roots were reached: 10 closed and 1 partial (0s0-4s1_5s0-6s1, stopped at END). The other 21 were not reached.
Seeded records: 1362 in lane 0 (0s0-2s1_1s0-9s0: 551, 0s0-1s1_5s0-9s1: 553, 0s0-3s1_2s1-10s1: 258). Of the three partial roots, only 0s0-2s1_1s0-9s0 was reached, and it closed after 3 new records.
`out.jsonl` holds only the 2201 new records: 2165 certified, each with both `c VERIFIED` and `s VERIFIED UNSAT`, plus 4 timeouts at the 300 s cap, which were split. The other records are split markers.
At END I killed the in-flight solver and checker processes of 0s0-4s1_5s0-6s1. Those nodes wrote no records, so no record has `cake_lpr: none` and nothing needed re-checking.
**No SAT, no proof rejection, no memory problem.** Peak use was about 9 GB of 15 GB, with no OOM kills.
`compose.txt`: 2165 certified nodes with their CNF sha256 recomputed. The class is not covered (expected).

## Per root
(Certified nodes are counted by depth = the number of layers. Times are summed over jobs.)

| row | root | stratum | list status | status | certified | by depth | timeouts | splits | solve h | check h | seeded |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 17 | 0s0-2s1_1s0-9s0 | H6(2,1)/two | partial | closed | 3 | d3:3 | 0 | 0 | 0.02 | 0.03 | 551 |
| 35 | 0s0-2s1_3s0-4s0 | H6(2,1)/two | untouched | closed | 1 | d2:1 | 0 | 0 | 0.01 | 0.01 | 0 |
| 53 | 0s0-2s1_4s0-6s0 | H6(2,1)/two | untouched | closed | 1 | d2:1 | 0 | 0 | 0.01 | 0.01 | 0 |
| 71 | 0s0-2s1_5s0-8s0 | H6(2,1)/two | untouched | closed | 1 | d2:1 | 0 | 0 | 0.01 | 0.01 | 0 |
| 89 | 0s0-3s1_1s0-8s0 | H6(3,1)/two | untouched | closed | 546 | d3:84 d4:462 | 1 | 8 | 1.20 | 2.43 | 0 |
| 107 | 0s0-3s1_4s0-10s0 | H6(3,1)/two | untouched | closed | 546 | d3:84 d4:462 | 1 | 8 | 1.21 | 2.40 | 0 |
| 125 | 0s0-3s1_4s1-7s1 | H6(3,1)/two | untouched | closed | 1 | d2:1 | 0 | 0 | 0.01 | 0.01 | 0 |
| 143 | 0s0-3s1_5s1-8s1 | H6(3,1)/two | untouched | closed | 1 | d2:1 | 0 | 0 | 0.01 | 0.01 | 0 |
| 161 | 0s0-4s1_1s0-7s0 | H6(4,1)/two | untouched | closed | 1 | d2:1 | 0 | 0 | 0.08 | 0.01 | 0 |
| 179 | 0s0-4s1_1s1-8s1 | H6(4,1)/two | untouched | closed | 546 | d3:84 d4:462 | 1 | 8 | 1.77 | 2.67 | 0 |
| 197 | 0s0-4s1_5s0-6s1 | H6(4,1)/two | untouched | partial | 518 | d3:56 d4:462 | 1 | 8 | 1.44 | 2.49 | 0 |
| 215 | 0s0-4s1_6s0-9s0 | H6(4,1)/two | untouched | not reached | 0 | - | 0 | 0 | 0.00 | 0.00 | 0 |
| 233 | 0s0-5s1_1s0-6s0 | H6(5,1)/two | untouched | not reached | 0 | - | 0 | 0 | 0.00 | 0.00 | 0 |
| 251 | 0s0-5s1_1s1-7s1 | H6(5,1)/two | untouched | not reached | 0 | - | 0 | 0 | 0.00 | 0.00 | 0 |
| 269 | 0s0-5s1_2s1-10s1 | H6(5,1)/two | untouched | not reached | 0 | - | 0 | 0 | 0.00 | 0.00 | 0 |
| 287 | 0s0-5s1_6s1-10s1 | H6(5,1)/two | untouched | not reached | 0 | - | 0 | 0 | 0.00 | 0.00 | 0 |
| 305 | 0s0-1s1_5s0-9s1 | H6(1,1)/two | partial | not reached | 0 | - | 0 | 0 | 0.00 | 0.00 | 553 |
| 323 | 0s0-3s1_2s1-10s1 | H6(3,1)/two | partial | not reached | 0 | - | 0 | 0 | 0.00 | 0.00 | 258 |
| 341 | 0s0-2s1_4s0-10s0 | H6(2,1)/two | untouched | not reached | 0 | - | 0 | 0 | 0.00 | 0.00 | 0 |
| 359 | 0s0-2s1_6s1-8s1 | H6(2,1)/two | untouched | not reached | 0 | - | 0 | 0 | 0.00 | 0.00 | 0 |
| 377 | 0s0-2s1_8s0-9s1 | H6(2,1)/two | untouched | not reached | 0 | - | 0 | 0 | 0.00 | 0.00 | 0 |
| 395 | 0s0-3s1_2s0-7s0 | H6(3,1)/two | untouched | not reached | 0 | - | 0 | 0 | 0.00 | 0.00 | 0 |
| 413 | 0s0-3s1_4s1-10s0 | H6(3,1)/two | untouched | not reached | 0 | - | 0 | 0 | 0.00 | 0.00 | 0 |
| 431 | 0s0-3s1_7s0-8s1 | H6(3,1)/two | untouched | not reached | 0 | - | 0 | 0 | 0.00 | 0.00 | 0 |
| 449 | 0s0-3s1_9s0-10s1 | H6(3,1)/two | untouched | not reached | 0 | - | 0 | 0 | 0.00 | 0.00 | 0 |
| 467 | 0s0-4s1_2s1-9s0 | H6(4,1)/two | untouched | not reached | 0 | - | 0 | 0 | 0.00 | 0.00 | 0 |
| 485 | 0s0-4s1_3s1-6s0 | H6(4,1)/two | untouched | not reached | 0 | - | 0 | 0 | 0.00 | 0.00 | 0 |
| 503 | 0s0-4s1_7s1-10s0 | H6(4,1)/two | untouched | not reached | 0 | - | 0 | 0 | 0.00 | 0.00 | 0 |
| 521 | 0s0-5s1_2s0-4s0 | H6(5,1)/two | untouched | not reached | 0 | - | 0 | 0 | 0.00 | 0.00 | 0 |
| 539 | 0s0-5s1_3s1-10s1 | H6(5,1)/two | untouched | not reached | 0 | - | 0 | 0 | 0.00 | 0.00 | 0 |
| 557 | 0s0-5s1_4s0-8s1 | H6(5,1)/two | untouched | not reached | 0 | - | 0 | 0 | 0.00 | 0.00 | 0 |
| 575 | 0s0-5s1_7s1-9s0 | H6(5,1)/two | untouched | not reached | 0 | - | 0 | 0 | 0.00 | 0.00 | 0 |

Totals per stratum:

| stratum | roots | closed | partial | not reached | certified | timeouts | solve h | check h |
|---|---|---|---|---|---|---|---|---|
| H6(2,1)/two | 7 | 4 | 0 | 3 | 6 | 0 | 0.05 | 0.06 |
| H6(3,1)/two | 9 | 4 | 0 | 5 | 1094 | 2 | 2.43 | 4.85 |
| H6(4,1)/two | 7 | 2 | 1 | 4 | 1065 | 2 | 3.29 | 5.17 |
| H6(5,1)/two | 8 | 0 | 0 | 8 | 0 | 0 | 0.00 | 0.00 |
| H6(1,1)/two | 1 | 0 | 0 | 1 | 0 | 0 | 0.00 | 0.00 |

ALL: records 2201 certified 2165 rejected 0 SAT 0
closed: 0s0-2s1_1s0-9s0 0s0-2s1_3s0-4s0 0s0-2s1_4s0-6s0 0s0-2s1_5s0-8s0 0s0-3s1_1s0-8s0 0s0-3s1_4s0-10s0 0s0-3s1_4s1-7s1 0s0-3s1_5s1-8s1 0s0-4s1_1s0-7s0 0s0-4s1_1s1-8s1
partial: 0s0-4s1_5s0-6s1
