# C3WAVE2 K19 (shard 19 of 40, H = 1.5 h, task at 852bee7)

Start 2026-10-21 00:25:06 UTC (epoch 1792542306). END (start + 1.5 h - 15 min) = 01:40:06 UTC. Machine: 4 cores, 15 GB, see env.txt.

## Tools and base CNF
- C3-S tools: worktree of 132398c at /opt/c3s, unmodified.
- CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8 (`make cake_lpr`, example prints `s VERIFIED UNSAT`), drat-trim lrat-check 2e3b2dc + lrat-check-E2.patch.
- Sanity: LRAT `3 0 0` on {1},{-1}: lrat-check `c NOT VERIFIED`, cake_lpr `pivot must be non-zero` (both reject). `3 0 1 2 0`: `c VERIFIED` and `s VERIFIED UNSAT`.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 bf0e502e…dd6da (matches).
- Details are in tools.txt.

## Run
runner.sh is the K00 runner with this machine's start time. It used 10-minute slices (`--hours 0.17`), `--jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles`.

Note: close_tree.py checks its deadline only between frontier waves, so a wave that has already been submitted runs to the end. That is why 0s0-3s0_5 took 33.5 min (a presplit wave of 120 depth-3 nodes) and 0s0-3s1_2s1-6s0 ran past END. At 01:41 UTC, after END, I killed the runner and close_tree. That root's finished records stay in out.jsonl, so a later wave can resume it.

No SAT, no PROOF NOT ACCEPTED, no memory problem (peak use about 3-4 GB of 15). Every solved node was accepted by both lrat-check and cake_lpr.

## Per root (34 roots; 13 closed, 1 partial, 20 not reached)
| # | root | status | certified nodes by depth | splits | solve s | check s |
|---|---|---|---|---|---|---|
| 1 | 0s0-1s1_5s0-9s0 | closed | d2: 1 | 0 | 126 | 41 |
| 2 | 0s0-2s0_1s0-4s0 | closed | d2: 1 | 0 | 17 | 30 |
| 3 | 0s0-2s0_3s1-5s1 | closed | d2: 1 | 0 | 11 | 26 |
| 4 | 0s0-2s0_5s1-6s1 | closed | d2: 1 | 0 | 8 | 24 |
| 5 | 0s0-2s0_9s0-10s1 | closed | d2: 1 | 0 | 85 | 41 |
| 6 | 0s0-2s1_3s0-6s0 | closed | d2: 1 | 0 | 35 | 33 |
| 7 | 0s0-2s1_4s1-6s1 | closed | d2: 1 | 0 | 33 | 35 |
| 8 | 0s0-2s1_6s1-7s1 | closed | d2: 1 | 0 | 35 | 34 |
| 9 | 0s0-3s0_1s0-5s0 | closed | d2: 1 | 0 | 23 | 33 |
| 10 | 0s0-3s0_2s0-9s1 | closed | d2: 1 | 0 | 39 | 38 |
| 11 | 0s0-3s0_5 | closed | d3: 120 | 1 | 3375 | 2588 |
| 12 | 0s0-3s0_7s0-10s1 | closed | d2: 1 | 0 | 88 | 30 |
| 13 | 0s0-3s1_1s0-8s1 | closed | d2: 1 | 0 | 72 | 29 |
| 14 | 0s0-3s1_2s1-6s0 | partial | d4: 183 | 8 | 1111 | 2562 |
| 15 | 0s0-3s1_5s0-8s0 | not reached | | | | |
| 16 | 0s0-3s1_7s1-8s0 | not reached | | | | |
| 17 | 0s0-4s0_1s1-3s0 | not reached | | | | |
| 18 | 0s0-4s0_2s1-9s1 | not reached | | | | |
| 19 | 0s0-4s0_5s1-6s1 | not reached | | | | |
| 20 | 0s0-4s0_8s0-9s0 | not reached | | | | |
| 21 | 0s0-4s1_1s1-7s1 | not reached | | | | |
| 22 | 0s0-4s1_3s0-6s1 | not reached | | | | |
| 23 | 0s0-4s1_6 | not reached | | | | |
| 24 | 0s0-4s1_9s0-10s0 | not reached | | | | |
| 25 | 0s0-5s0_2s0-10s1 | not reached | | | | |
| 26 | 0s0-5s0_3s1-10s0 | not reached | | | | |
| 27 | 0s0-5s0_6s0-9s0 | not reached | | | | |
| 28 | 0s0-5s1_1s0-10s1 | not reached | | | | |
| 29 | 0s0-5s1_2s0-7s0 | not reached | | | | |
| 30 | 0s0-5s1_3s1-7s1 | not reached | | | | |
| 31 | 0s0-5s1_6s1-8s1 | not reached | | | | |
| 32 | 0s0_1s0-5s1 | not reached | | | | |
| 33 | 0s0_2s0-9s1 | not reached | | | | |
| 34 | 0s0_4s0-7s1 | not reached | | | | |

Totals: 315 certified nodes, 9 split records, solve 5056 s, check 5544 s (summed over jobs).

Closed roots (13): 0s0-1s1_5s0-9s0, 0s0-2s0_1s0-4s0, 0s0-2s0_3s1-5s1, 0s0-2s0_5s1-6s1, 0s0-2s0_9s0-10s1, 0s0-2s1_3s0-6s0, 0s0-2s1_4s1-6s1, 0s0-2s1_6s1-7s1, 0s0-3s0_1s0-5s0, 0s0-3s0_2s0-9s1, 0s0-3s0_5 (presplit into 120 depth-3 leaves, all certified), 0s0-3s0_7s0-10s1, 0s0-3s1_1s0-8s1.

Partial (1): 0s0-3s1_2s1-6s0. The root timed out at the 300 s cap (UNKNOWN) and split into 91 children. 7 of them are single-orbit and were presplit into 66 each, for a wave of 84 + 462 = 546 nodes. 183 depth-4 nodes were certified before the kill; the rest are open.

Not reached (20): roots 15-34 of roots.tsv.

## compose.py
compose.txt: certified_nodes 315, class_covered false, uncovered_frontier_nodes 860 (expected: this shard covers only a few roots).
