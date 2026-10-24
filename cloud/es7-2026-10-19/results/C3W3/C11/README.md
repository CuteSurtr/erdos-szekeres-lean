# C3W3 C11

Task `results/C3W3/TASK.md` (commit 640a56c2) with V = C11, LIST = C_s1two.tsv, j = 11, N = 18, LANES = 1, JOBS = 3, SLICE = 2.0 h, H = 6.0 h.
One cloud VM, 4 cores, 15 GB RAM (`env.txt`). Start 04:43:31 UTC, END 10:28:31 UTC.

## Tools and base CNF (`tools.txt`)
- C3-S tools: worktree of 132398c at /opt/c3s, unmodified.
- CaDiCaL 3.0.1 c6073042; cake_lpr a36874a8 (example prints `s VERIFIED UNSAT`); lrat-check 2e3b2dc + E2 patch, sanity check passed (`3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both).
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 bf0e502e…6da (matches).

## Roots and seeding
33 roots (rows ≡ 11 mod 18, `roots.tsv`), one lane (`lane0.sh`). Seeded 645 records into lane 0
(0s0-1s1_4s1-7s0: 521, 0s0-1s1_8s0-9s1: 124); `out.jsonl` holds only the 2,193 new records.

## Per root (certified counts are new records only; depth = number of layers, roots at depth 2)

| # | root | stratum | list status | status | certified by depth (new) | timeouts | splits | solve s | check s |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0s0-1s1_4s1-7s0 | H6(1,1)/two | partial | closed | d3: 33 | 0 | 0 | 1081 | 916 |
| 2 | 0s0-2s1_1s0-10s1 | H6(2,1)/two | untouched | closed | d2: 1 | 0 | 0 | 57 | 31 |
| 3 | 0s0-2s1_3s1-6s1 | H6(2,1)/two | untouched | closed | d2: 1 | 0 | 0 | 32 | 29 |
| 4 | 0s0-2s1_4s1-8s1 | H6(2,1)/two | untouched | closed | d2: 1 | 0 | 0 | 183 | 43 |
| 5 | 0s0-3s1_1s0-4s0 | H6(3,1)/two | untouched | closed | d2: 1 | 0 | 0 | 25 | 29 |
| 6 | 0s0-3s1_1s1-7s0 | H6(3,1)/two | untouched | closed | d2: 1 | 0 | 0 | 230 | 43 |
| 7 | 0s0-3s1_4s1-10s1 | H6(3,1)/two | untouched | closed | d3: 84, d4: 462 | 1 | 8 | 5740 | 9268 |
| 8 | 0s0-3s1_5s0-9s1 | H6(3,1)/two | untouched | closed | d3: 84, d4: 462 | 1 | 8 | 4891 | 9209 |
| 9 | 0s0-4s1_1s0-2s1 | H6(4,1)/two | untouched | closed | d3: 84, d4: 462 | 1 | 8 | 5654 | 9189 |
| 10 | 0s0-4s1_1s1-5s1 | H6(4,1)/two | untouched | closed | d2: 1 | 0 | 0 | 63 | 24 |
| 11 | 0s0-4s1_2s0-8s1 | H6(4,1)/two | untouched | closed | d2: 1 | 0 | 0 | 295 | 46 |
| 12 | 0s0-4s1_5s1-8s0 | H6(4,1)/two | untouched | partial | d3: 17, d4: 462 | 1 | 8 | 3384 | 7469 |
| 13 | 0s0-5s1_1s0-2s0 | H6(5,1)/two | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 14 | 0s0-5s1_1s1-3s0 | H6(5,1)/two | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 15 | 0s0-5s1_2s0-7s1 | H6(5,1)/two | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 16 | 0s0-5s1_6s0-7s0 | H6(5,1)/two | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 17 | 0s0-5s1_7s1-8s1 | H6(5,1)/two | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 18 | 0s0-1s1_8s0-9s1 | H6(1,1)/two | partial | not reached | - | 0 | 0 | 0 | 0 |
| 19 | 0s0-2s1_1s1-7s0 | H6(2,1)/two | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 20 | 0s0-2s1_6s0-8s0 | H6(2,1)/two | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 21 | 0s0-2s1_7s1-8s1 | H6(2,1)/two | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 22 | 0s0-3s1_2s0-4s0 | H6(3,1)/two | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 23 | 0s0-3s1_2s1-7s0 | H6(3,1)/two | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 24 | 0s0-3s1_6s1-8s0 | H6(3,1)/two | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 25 | 0s0-3s1_8s0-9s1 | H6(3,1)/two | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 26 | 0s0-4s1_2s1-6s0 | H6(4,1)/two | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 27 | 0s0-4s1_3s0-9s0 | H6(4,1)/two | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 28 | 0s0-4s1_6s1-10s1 | H6(4,1)/two | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 29 | 0s0-4s1_8s1-9s1 | H6(4,1)/two | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 30 | 0s0-5s1_3s0-7s1 | H6(5,1)/two | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 31 | 0s0-5s1_4s0-10s1 | H6(5,1)/two | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 32 | 0s0-5s1_4s1-9s1 | H6(5,1)/two | untouched | not reached | - | 0 | 0 | 0 | 0 |
| 33 | 0s0-5s1_9s1-10s1 | H6(5,1)/two | untouched | not reached | - | 0 | 0 | 0 | 0 |

| stratum | closed | partial | not reached | certified (new) | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|
| H6(1,1)/two | 1 | 0 | 1 | 33 | 0 | 1081 | 916 |
| H6(2,1)/two | 3 | 0 | 3 | 3 | 0 | 273 | 103 |
| H6(3,1)/two | 4 | 0 | 4 | 1094 | 2 | 10886 | 18549 |
| H6(4,1)/two | 3 | 1 | 4 | 1027 | 2 | 9396 | 16726 |
| H6(5,1)/two | 0 | 0 | 9 | 0 | 0 | 0 | 0 |


Timeouts are the 300 s root-level UNKNOWN results (each then split). Splits include pre-splits. Solve and check times are summed per node (3 jobs on 4 cores), not wall clock.

## Summary
- 11 roots closed (every leaf certified): 0s0-1s1_4s1-7s0 (resumed partial), 0s0-2s1_1s0-10s1, 0s0-2s1_3s1-6s1, 0s0-2s1_4s1-8s1, 0s0-3s1_1s0-4s0, 0s0-3s1_1s1-7s0, 0s0-3s1_4s1-10s1, 0s0-3s1_5s0-9s1, 0s0-4s1_1s0-2s1, 0s0-4s1_1s1-5s1, 0s0-4s1_2s0-8s1.
- 1 partial: 0s0-4s1_5s1-8s0 (its records are in `out.jsonl` for resumption).
- 21 not reached (including partial 0s0-1s1_8s0-9s1).
- 2,157 new certified nodes, every one with cake_lpr `s VERIFIED UNSAT` and lrat-check accepting. No SAT, no `PROOF NOT ACCEPTED`, no memory problem (peak about 9 GB used).
- close_tree.py did not stop at the end of its last slice (10:28); I killed the runner and its solvers/checkers at about 10:40. Nodes in flight then have no record; no record has `cake_lpr: none`, so no re-check was needed (no `recheck.jsonl`).
- `compose.txt`: output of `compose.py base.cnf out.jsonl` (class not expected to be covered).
