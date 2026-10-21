# C3W3 A5

Values: V = A5, LIST = A_s0.tsv, j = 5, N = 8 (rows with row % 8 == 5: 36 roots), LANES = 3, JOBS = 1, SLICE = 0.5 h, H = 2.0 h, Z = 640a56c2.
One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:40:08 UTC, END 06:25:08 UTC (start + 2 h − 15 min) on 2026-10-21.

## Tools and base CNF (`tools.txt`)

- C3-S tools: worktree of 132398c at /opt/c3s, unmodified.
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (example prints `s VERIFIED UNSAT`);
  lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 + E2 patch. Sanity check passed: `3 0 0` on {1},{-1} rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches).

## Run

Lanes `lane0.sh`, `lane1.sh`, `lane2.sh` (lane k takes root positions ≡ k mod 3), each `close_tree.py … --jobs 1 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`.
All three lanes were killed at END (06:25 UTC). The nodes in flight at that moment wrote no record, so `out.jsonl` has no record with `cake_lpr: none` and there was nothing to re-check.
`close_tree.py` checks its deadline only between waves, so a root can run past its 0.5 h slice. Lane 0 spent the whole run on root 5 and lane 2 on root 69. Lane 1 closed 7 roots.

Seeded records (step 3): 360, all in lane 0 (0s0-5s0_1s0-4s1: 38, 0s0-5s0_2s1-4s0: 322), from earlier waves' out/recheck files. `out.jsonl` has only the 698 new records (lane by lane, without the seeded lines).

**No SAT, no proof rejection, no memory problem** (peak about 9 GB used of 15). Every UNSAT record (688) has `certified: true` with cake_lpr `s VERIFIED UNSAT`.
`compose.txt`: 688 certified nodes, CNF sha256 recomputed, class not covered (as expected).

Closed (9): 0s0-2s0_1s1-4s0, 0s0-2s0_3s0-8s0, 0s0-2s0_5s0-6s1, 0s0-4s0_1s1-7s0, 0s0-4s0_6s0-8s0, 0s0-5s0_1s1-8s0, 0s0-5s0_2s1-9s1, 0s0-2s0_4, 0s0-2s0_3s1-10s1.
Partial: 0s0-5s0_1s0-4s1 (row 5, resumed), 0s0-5s0_1s0-3s1 (row 69), 0s0-2s0_8s1-9s0 (row 181; started 3 min before END, nothing recorded).
Not reached: 25 roots, including the seeded partial root 0s0-5s0_2s1-4s0 (row 149).

## Per root (new records only; depth = number of layers, roots are at depth 2)

| row | root | stratum | seeded | status | certified (new) by depth | splits | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|---|---|
| 5 | 0s0-5s0_1s0-4s1 | H6(5,0)/two | 38 | partial | d3:84, d4:177 | 0 | 0 | 1807 | 4282 |
| 13 | 0s0-2s0_1s1-4s0 | H6(2,0)/two | 0 | closed | d2:1 | 0 | 0 | 76 | 27 |
| 21 | 0s0-2s0_3s0-8s0 | H6(2,0)/two | 0 | closed | d2:1 | 0 | 0 | 30 | 28 |
| 29 | 0s0-2s0_3s1-8s1 | H6(2,0)/two | 0 | not reached | - | 0 | 0 | 0 | 0 |
| 37 | 0s0-2s0_5s0-6s1 | H6(2,0)/two | 0 | closed | d2:1 | 0 | 0 | 89 | 39 |
| 45 | 0s0-4s0_1s1-7s0 | H6(4,0)/two | 0 | closed | d2:1 | 0 | 0 | 78 | 30 |
| 53 | 0s0-4s0_2s0-7s1 | H6(4,0)/two | 0 | not reached | - | 0 | 0 | 0 | 0 |
| 61 | 0s0-4s0_6s0-8s0 | H6(4,0)/two | 0 | closed | d2:1 | 0 | 0 | 9 | 18 |
| 69 | 0s0-5s0_1s0-3s1 | H6(5,0)/two | 0 | partial | d4:299 | 8 | 1 | 1475 | 4425 |
| 77 | 0s0-5s0_1s1-10s1 | H6(5,0)/two | 0 | not reached | - | 0 | 0 | 0 | 0 |
| 85 | 0s0-5s0_1s1-8s0 | H6(5,0)/two | 0 | closed | d2:1 | 0 | 0 | 24 | 26 |
| 93 | 0s0-5s0_2s0-6s0 | H6(5,0)/two | 0 | not reached | - | 0 | 0 | 0 | 0 |
| 101 | 0s0-5s0_2s1-10s0 | H6(5,0)/two | 0 | not reached | - | 0 | 0 | 0 | 0 |
| 109 | 0s0-5s0_2s1-9s1 | H6(5,0)/two | 0 | closed | d2:1 | 0 | 0 | 199 | 40 |
| 117 | 0s0-5s0_6s0-9s1 | H6(5,0)/two | 0 | not reached | - | 0 | 0 | 0 | 0 |
| 125 | 0s0-5s0_7s0-8s0 | H6(5,0)/two | 0 | not reached | - | 0 | 0 | 0 | 0 |
| 133 | 0s0-2s0_4 | H6(2,0)/one | 0 | closed | d3:120 | 1 | 0 | 2735 | 2481 |
| 141 | 0s0-4s0_7 | H6(4,0)/one | 0 | not reached | - | 0 | 0 | 0 | 0 |
| 149 | 0s0-5s0_2s1-4s0 | H6(5,0)/two | 322 | not reached | - | 0 | 0 | 0 | 0 |
| 157 | 0s0-2s0_3s1-10s1 | H6(2,0)/two | 0 | closed | d2:1 | 0 | 0 | 147 | 39 |
| 165 | 0s0-2s0_5s1-9s0 | H6(2,0)/two | 0 | not reached | - | 0 | 0 | 0 | 0 |
| 173 | 0s0-2s0_7s0-9s0 | H6(2,0)/two | 0 | not reached | - | 0 | 0 | 0 | 0 |
| 181 | 0s0-2s0_8s1-9s0 | H6(2,0)/two | 0 | partial | - | 0 | 0 | 0 | 0 |
| 189 | 0s0-4s0_3s0-10s0 | H6(4,0)/two | 0 | not reached | - | 0 | 0 | 0 | 0 |
| 197 | 0s0-4s0_6s1-9s1 | H6(4,0)/two | 0 | not reached | - | 0 | 0 | 0 | 0 |
| 205 | 0s0-4s0_8s0-10s1 | H6(4,0)/two | 0 | not reached | - | 0 | 0 | 0 | 0 |
| 213 | 0s0-4s0_9s0-10s1 | H6(4,0)/two | 0 | not reached | - | 0 | 0 | 0 | 0 |
| 221 | 0s0-5s0_3s0-4s0 | H6(5,0)/two | 0 | not reached | - | 0 | 0 | 0 | 0 |
| 229 | 0s0-5s0_3s0-9s1 | H6(5,0)/two | 0 | not reached | - | 0 | 0 | 0 | 0 |
| 237 | 0s0-5s0_3s1-7s1 | H6(5,0)/two | 0 | not reached | - | 0 | 0 | 0 | 0 |
| 245 | 0s0-5s0_4s0-6s1 | H6(5,0)/two | 0 | not reached | - | 0 | 0 | 0 | 0 |
| 253 | 0s0-5s0_4s1-10s1 | H6(5,0)/two | 0 | not reached | - | 0 | 0 | 0 | 0 |
| 261 | 0s0-5s0_4s1-9s1 | H6(5,0)/two | 0 | not reached | - | 0 | 0 | 0 | 0 |
| 269 | 0s0-5s0_8s0-10s1 | H6(5,0)/two | 0 | not reached | - | 0 | 0 | 0 | 0 |
| 277 | 0s0-5s0_9s0-10s1 | H6(5,0)/two | 0 | not reached | - | 0 | 0 | 0 | 0 |
| 285 | 0s0-4s0_10 | H6(4,0)/one | 0 | not reached | - | 0 | 0 | 0 | 0 |

| stratum | roots | closed | partial | not reached | certified (new) | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| H6(2,0)/one | 1 | 1 | 0 | 0 | 120 | 0 | 2735 | 2481 |
| H6(2,0)/two | 8 | 4 | 1 | 3 | 4 | 0 | 341 | 132 |
| H6(4,0)/one | 2 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| H6(4,0)/two | 7 | 2 | 0 | 5 | 2 | 0 | 87 | 48 |
| H6(5,0)/two | 18 | 2 | 2 | 14 | 562 | 1 | 3506 | 8773 |
