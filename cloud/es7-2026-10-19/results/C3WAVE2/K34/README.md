# C3WAVE2 K34: shard 34 of 40 (idx ≡ 34 mod 40), 1.5 h

Start 00:31:18 UTC, END (start + 1.5 h − 15 min) 01:46:18 UTC. Machine: 4 cores, 15 GB RAM (env.txt).

## Tools and base CNF (tools.txt)
- C3-S tools: worktree of 132398c (8dc27c3 before the author rewrite) at /opt/c3s, unmodified.
- CaDiCaL 3.0.1 c6073042; cake_lpr a36874a8 (example: `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc + lrat-check-E2.patch. Sanity check passed: `3 0 0` on {1},{-1} rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 bf0e502e…cdd6da (matches).

## Run
runner.sh, run as described in TASK.md (10-minute slice, `--jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles`). There are 33 roots. 5 were reached before END.
No SAT, no proof rejection and no memory problem (peak about 5 GB used of 15 GB). Every certified node has cake_lpr `s VERIFIED UNSAT` and lrat-check `c VERIFIED`.

Slice overrun: close_tree.py checks its `--hours` deadline only between tree levels, so it cannot stop partway through a level. Root 5 (0s0-2s1_1s0-9s0) hit its 300 s cap at depth 2, was split into 91 children (7 of them pre-split into 66 each), and its level ran from 00:36:40 until END. At 01:46:30 I stopped the runner and its in-flight jobs. Every finished record is in out.jsonl. The 3 nodes that were in flight have no record, so a later wave will re-run them.

## Per root
| root | status | certified (by depth) | splits | solve s | check s |
|---|---|---|---|---|---|
| 0s0-1s1_7s0-10s0 | closed | 1 (d2) | 0 | 23 | 31 |
| 0s0-2s0_1s1-5s1 | closed | 1 (d2) | 0 | 18 | 29 |
| 0s0-2s0_4s0-8s1 | closed | 1 (d2) | 0 | 54 | 32 |
| 0s0-2s0_6s1-7s1 | closed | 1 (d2) | 0 | 6 | 18 |
| 0s0-2s1_1s0-9s0 | partial (3 open: _8s0-10s1, _8s1-10s0, _8s1-10s1) | 543 (d3: 81, d4: 462) | 8 (root UNKNOWN at 300 s + 7 pre-splits) | 4129 | 7654 |

Not reached (28): 0s0-2s1_3s1-6s1, 0s0-2s1_5s0-8s1, 0s0-2s1_7s1-8s1, 0s0-3s0_1s1-4s1, 0s0-3s0_4, 0s0-3s0_5s1-7s0, 0s0-3s0_8s0-9s1, 0s0-3s1_1s1-8s0, 0s0-3s1_4s0-7s0, 0s0-3s1_6s0-10s0, 0s0-3s1_9s0-10s1, 0s0-4s0_2s0-3s0, 0s0-4s0_3s1-10s1, 0s0-4s0_6s0-9s1, 0s0-4s1_1s0-2s0, 0s0-4s1_2s0-7s1, 0s0-4s1_3s1-8s0, 0s0-4s1_6s1-9s0, 0s0-5s0_1s0-6s1, 0s0-5s0_2s1-3s0, 0s0-5s0_4s0-6s0, 0s0-5s0_7s0-9s0, 0s0-5s1_1s1-10s0, 0s0-5s1_2s1-7s1, 0s0-5s1_4s0-9s1, 0s0-5s1_7s1-9s1, 0s0_1s1-4s1, 0s0_3s0-4s0.

Closed (4): 0s0-1s1_7s0-10s0, 0s0-2s0_1s1-5s1, 0s0-2s0_4s0-8s1, 0s0-2s0_6s1-7s1. Partial (1): 0s0-2s1_1s0-9s0.

## Totals
547 certified nodes, 8 splits, 4230 s of solve time and 7763 s of check time (cake_lpr + lrat-check). compose.py: 547 certified nodes, class_covered false (as expected).
