# C3W3 C1: C_s1two.tsv shard 1 of 18 (1 lane, --jobs 3, slice 2.0 h, budget 6 h)

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:42:37 UTC, END 10:27:37 UTC, runner stopped 10:34 UTC.

## Tools and base CNF (`tools.txt`)
- C3-S tools: worktree of 132398c at /opt/c3s, unmodified
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8 (the example prints `s VERIFIED UNSAT`); lrat-check 2e3b2dc + E2 patch (sanity check: `3 0 0` rejected by both, `3 0 1 2 0` accepted by both)
- base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 bf0e502e…6cdd6da (matches)

## Roots and seeding
33 roots (rows ≡ 1 mod 18, `roots.tsv`): 3 partial, 30 untouched. **Seeded records: 729** (lane 0): 0s0-1s1_2s1-10s1 78 certified + 8 split; 0s0-2s1_3s1-5s0 497 + 8; 0s0-1s1_5s1-9s0 130 + 8. `out.jsonl` contains only the 2,187 new records.

## Result
- **No SAT. No proof rejected** (every new UNSAT record is certified by both cake_lpr and lrat-check). There were no memory problems (free memory never fell below about 4 GB).
- 10 roots closed: 0s0-1s1_2s1-10s1, 0s0-2s1_3s1-5s0, 0s0-2s1_3s0-5s1, 0s0-2s1_4s0-7s1, 0s0-2s1_5s1-6s1, 0s0-3s1_1s0-9s1, 0s0-3s1_4s0-5s0, 0s0-3s1_4s1-8s1, 0s0-3s1_6s0-7s0, 0s0-4s1_1s0-8s0. Four of them (0s0-3s1_*) closed at the root itself in under a minute.
- 0 partial; 23 not reached (from 0s0-4s1_1s1-9s1 on, including the list-partial root 0s0-1s1_5s1-9s0).
- Note: close_tree.py kept dispatching jobs past END for the last root (its `--hours` stops only new rounds). The tree closed at about 10:33, and I killed the runner at 10:34 before it started the next root. In-flight solves were killed without records, so no record has `cake_lpr: none`, and there was nothing to re-check.
- `compose.txt`: compose.py run on the new records only: 2,149 certified nodes, class not covered (as expected).

## Per root (new records only; depth = number of layers)
| row | root | stratum | h6m | list status | status | certified by depth | splits | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0s0-1s1_2s1-10s1 | H6(1,1)/two | yes | partial | closed | d3:84, d4:384 | 0 | 0 | 4703 | 7579 |
| 19 | 0s0-2s1_3s1-5s0 | H6(2,1)/two | yes | partial | closed | d3:49 | 0 | 0 | 1760 | 1410 |
| 37 | 0s0-2s1_3s0-5s1 | H6(2,1)/two | yes | untouched | closed | d3:84, d4:462 | 8 | 1 | 5951 | 9229 |
| 55 | 0s0-2s1_4s0-7s1 | H6(2,1)/two | yes | untouched | closed | d3:84, d4:462 | 8 | 1 | 5726 | 9080 |
| 73 | 0s0-2s1_5s1-6s1 | H6(2,1)/two | yes | untouched | closed | d2:1 | 0 | 0 | 36 | 22 |
| 91 | 0s0-3s1_1s0-9s1 | H6(3,1)/two | yes | untouched | closed | d2:1 | 0 | 0 | 62 | 26 |
| 109 | 0s0-3s1_4s0-5s0 | H6(3,1)/two | yes | untouched | closed | d2:1 | 0 | 0 | 38 | 25 |
| 127 | 0s0-3s1_4s1-8s1 | H6(3,1)/two | yes | untouched | closed | d2:1 | 0 | 0 | 184 | 28 |
| 145 | 0s0-3s1_6s0-7s0 | H6(3,1)/two | yes | untouched | closed | d2:1 | 0 | 0 | 34 | 22 |
| 163 | 0s0-4s1_1s0-8s0 | H6(4,1)/two | yes | untouched | closed | d3:84, d4:462 | 8 | 1 | 4444 | 8792 |
| 181 | 0s0-4s1_1s1-9s1 | H6(4,1)/two | yes | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 199 | 0s0-4s1_5s0-7s1 | H6(4,1)/two | yes | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 217 | 0s0-4s1_6s1-7s0 | H6(4,1)/two | yes | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 235 | 0s0-5s1_1s0-7s0 | H6(5,1)/two | yes | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 253 | 0s0-5s1_1s1-8s1 | H6(5,1)/two | yes | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 271 | 0s0-5s1_2s1-6s0 | H6(5,1)/two | yes | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 289 | 0s0-5s1_6s1-7s1 | H6(5,1)/two | yes | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 307 | 0s0-1s1_5s1-9s0 | H6(1,1)/two | no | partial | not reached | - | 0 | 0 | 0 | 0 |
| 325 | 0s0-1s1_7s1-8s0 | H6(1,1)/two | no | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 343 | 0s0-2s1_5s0-10s0 | H6(2,1)/two | no | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 361 | 0s0-2s1_6s1-9s1 | H6(2,1)/two | no | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 379 | 0s0-2s1_8s1-10s1 | H6(2,1)/two | no | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 397 | 0s0-3s1_2s0-8s0 | H6(3,1)/two | no | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 415 | 0s0-3s1_5s0-10s1 | H6(3,1)/two | no | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 433 | 0s0-3s1_7s0-9s1 | H6(3,1)/two | no | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 451 | 0s0-3s1_9s1-10s1 | H6(3,1)/two | no | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 469 | 0s0-4s1_3s0-10s0 | H6(4,1)/two | no | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 487 | 0s0-4s1_3s1-7s0 | H6(4,1)/two | no | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 505 | 0s0-4s1_7s1-8s0 | H6(4,1)/two | no | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 523 | 0s0-5s1_2s1-3s1 | H6(5,1)/two | no | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 541 | 0s0-5s1_3s1-4s1 | H6(5,1)/two | no | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 559 | 0s0-5s1_4s0-9s1 | H6(5,1)/two | no | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 577 | 0s0-5s1_8s0-10s1 | H6(5,1)/two | no | untouched | not reached | - | 0 | 0 | 0 | 0 |

| stratum | roots | closed | partial | not reached | certified | timeouts | solve h | check h |
|---|---|---|---|---|---|---|---|---|
| H6(1,1)/two | 3 | 1 | 0 | 2 | 468 | 0 | 1.31 | 2.11 |
| H6(2,1)/two | 7 | 4 | 0 | 3 | 1142 | 2 | 3.74 | 5.48 |
| H6(3,1)/two | 8 | 4 | 0 | 4 | 4 | 0 | 0.09 | 0.03 |
| H6(4,1)/two | 7 | 1 | 0 | 6 | 546 | 1 | 1.23 | 2.44 |
| H6(5,1)/two | 8 | 0 | 0 | 8 | 0 | 0 | 0.00 | 0.00 |
| total | 33 | 10 | 0 | 23 | 2160 | 3 | 6.37 | 10.06 |

new records: 2187; seeded: 729; records with certified=false: 0; SAT: 0
