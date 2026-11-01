# C3W3 / A0: list A_s0.tsv, shard 0 of 8, 3-fold class (m = 11, k = 7)

**Result: 17 of my 37 roots closed, 2 partial, 18 not reached. No SAT. No proof rejection. No memory problem.**

## Setup
One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:40:04 UTC 2026-10-21, END 06:25:04 (H = 2.0 h minus 15 min).
3 lanes (`lane0.sh`..`lane2.sh`), each `close_tree.py ... --jobs 1 --caps 300,300,600 --cadopts=--sat --split-singles --hours min(0.5, left)`.
Tools (`tools.txt`): C3-S tools worktree 132398c unmodified; CaDiCaL 3.0.1 c6073042; cake_lpr a36874a8 (example: `s VERIFIED UNSAT`);
lrat-check 2e3b2dc + E2 patch (sanity: `3 0 0` rejected by both, `3 0 1 2 0` accepted by both).
Base CNF `p cnf 168399 4154921`, sha256 `bf0e502e…6dda` (matches).

Roots: rows of `lists/A_s0.tsv` with row ≡ 0 (mod 8): 37 roots (`roots.tsv`). Lane k took positions ≡ k (mod 3).

**Seeded records: 112** (lane 0 only, root `0s0-4s0_1s0-5s1`: 104 certified + 8 split records from C3WAVE1/C3WAVE2/C3S0). They are not in `out.jsonl`; it holds only the 351 new records (350 certified, 1 split).

Note: `close_tree.py` checks its `--hours` deadline only between frontier batches, so with `--jobs 1` the two long roots ran far past their 0.5 h slice (lane 0 from 04:42, lane 2 from 04:53) until I stopped them at END (06:25–06:28). Lane 1 finished all its 12 roots at 05:11 and was then idle. Killed solvers/checkers wrote no records, so no `cake_lpr: none` record exists and no re-check was needed.

## Per root (depth = number of layers; roots at depth 2). Solve/check seconds summed over new records.

| row | root | stratum | status | certified by depth | timeouts | splits | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| 0 | 0s0-4s0_1s0-5s1 | H6(4,0)/two | partial | d3:84 d4:163 | 0 | 0 | 1671 | 4613 |
| 8 | 0s0-2s0_1s0-3s1 | H6(2,0)/two | **closed** | d2:1 | 0 | 0 | 237 | 54 |
| 16 | 0s0-2s0_3s0-4s0 | H6(2,0)/two | **closed** | d2:1 | 0 | 0 | 6 | 27 |
| 24 | 0s0-2s0_3s1-4s0 | H6(2,0)/two | not reached | - | 0 | 0 | 0 | 0 |
| 32 | 0s0-2s0_4s0-9s1 | H6(2,0)/two | **closed** | d2:1 | 0 | 0 | 46 | 38 |
| 40 | 0s0-2s0_5s0-8s1 | H6(2,0)/two | **closed** | d2:1 | 0 | 0 | 89 | 32 |
| 48 | 0s0-4s0_2s0-5s0 | H6(4,0)/two | not reached | - | 0 | 0 | 0 | 0 |
| 56 | 0s0-4s0_5s0-8s1 | H6(4,0)/two | **closed** | d2:1 | 0 | 0 | 122 | 42 |
| 64 | 0s0-4s0_7s0-8s1 | H6(4,0)/two | **closed** | d2:1 | 0 | 0 | 179 | 47 |
| 72 | 0s0-5s0_1s0-8s0 | H6(5,0)/two | not reached | - | 0 | 0 | 0 | 0 |
| 80 | 0s0-5s0_1s1-3s1 | H6(5,0)/two | **closed** | d2:1 | 0 | 0 | 16 | 21 |
| 88 | 0s0-5s0_1s1-9s1 | H6(5,0)/two | **closed** | d2:1 | 0 | 0 | 218 | 39 |
| 96 | 0s0-5s0_2s0-7s1 | H6(5,0)/two | not reached | - | 0 | 0 | 0 | 0 |
| 104 | 0s0-5s0_2s1-7s0 | H6(5,0)/two | **closed** | d2:1 | 0 | 0 | 158 | 40 |
| 112 | 0s0-5s0_6s0-7s0 | H6(5,0)/two | **closed** | d2:1 | 0 | 0 | 10 | 13 |
| 120 | 0s0-5s0_6s1-7s1 | H6(5,0)/two | not reached | - | 0 | 0 | 0 | 0 |
| 128 | 0s0-5s0_7s0-9s1 | H6(5,0)/two | **closed** | d2:1 | 0 | 0 | 188 | 36 |
| 136 | 0s0-3s0_6 | H6(3,0)/one | partial | d3:86 | 0 | 1 | 3354 | 2282 |
| 144 | 0s0-5s0_6 | H6(5,0)/one | not reached | - | 0 | 0 | 0 | 0 |
| 152 | 0s0-2s0_1s0-7s0 | H6(2,0)/two | **closed** | d2:1 | 0 | 0 | 78 | 36 |
| 160 | 0s0-2s0_4s1-9s1 | H6(2,0)/two | not reached | - | 0 | 0 | 0 | 0 |
| 168 | 0s0-2s0_6s0-9s0 | H6(2,0)/two | not reached | - | 0 | 0 | 0 | 0 |
| 176 | 0s0-2s0_7s1-9s0 | H6(2,0)/two | **closed** | d2:1 | 0 | 0 | 127 | 36 |
| 184 | 0s0-2s0_9s1-10s0 | H6(2,0)/two | not reached | - | 0 | 0 | 0 | 0 |
| 192 | 0s0-4s0_3s1-10s0 | H6(4,0)/two | not reached | - | 0 | 0 | 0 | 0 |
| 200 | 0s0-4s0_7s1-10s1 | H6(4,0)/two | **closed** | d2:1 | 0 | 0 | 9 | 20 |
| 208 | 0s0-4s0_8s1-10s0 | H6(4,0)/two | not reached | - | 0 | 0 | 0 | 0 |
| 216 | 0s0-5s0_2s0-4s0 | H6(5,0)/two | not reached | - | 0 | 0 | 0 | 0 |
| 224 | 0s0-5s0_3s0-7s0 | H6(5,0)/two | **closed** | d2:1 | 0 | 0 | 30 | 28 |
| 232 | 0s0-5s0_3s1-4s0 | H6(5,0)/two | not reached | - | 0 | 0 | 0 | 0 |
| 240 | 0s0-5s0_3s1-9s0 | H6(5,0)/two | not reached | - | 0 | 0 | 0 | 0 |
| 248 | 0s0-5s0_4s0-8s0 | H6(5,0)/two | **closed** | d2:1 | 0 | 0 | 37 | 31 |
| 256 | 0s0-5s0_4s1-7s0 | H6(5,0)/two | not reached | - | 0 | 0 | 0 | 0 |
| 264 | 0s0-5s0_7s0-10s1 | H6(5,0)/two | not reached | - | 0 | 0 | 0 | 0 |
| 272 | 0s0-5s0_8s1-10s0 | H6(5,0)/two | **closed** | d2:1 | 0 | 0 | 255 | 38 |
| 280 | 0s0-2s0_8 | H6(2,0)/one | not reached | - | 0 | 0 | 0 | 0 |
| 288 | 0s0-4s0_9 | H6(4,0)/one | not reached | - | 0 | 0 | 0 | 0 |

Root `0s0-4s0_1s0-5s1` (partial, seeded): 247 new certified nodes (d3: 84, d4: 163), on top of the 104 seeded; still open at stop.
Root `0s0-3s0_6` (one-orbit, partial): pre-split into depth-3 children; 86 certified, rest open at stop.

## Totals per stratum
| stratum | roots | closed | partial | not reached | new certified nodes |
|---|---|---|---|---|---|
| H6(2,0)/one | 1 | 0 | 0 | 1 | 0 |
| H6(2,0)/two | 10 | 6 | 0 | 4 | 6 |
| H6(3,0)/one | 1 | 0 | 1 | 0 | 86 |
| H6(4,0)/one | 1 | 0 | 0 | 1 | 0 |
| H6(4,0)/two | 7 | 3 | 1 | 3 | 250 |
| H6(5,0)/one | 1 | 0 | 0 | 1 | 0 |
| H6(5,0)/two | 16 | 8 | 0 | 8 | 8 |

Closed (17): 0s0-2s0_1s0-3s1, 0s0-2s0_3s0-4s0, 0s0-2s0_4s0-9s1, 0s0-2s0_5s0-8s1, 0s0-4s0_5s0-8s1, 0s0-4s0_7s0-8s1, 0s0-5s0_1s1-3s1, 0s0-5s0_1s1-9s1, 0s0-5s0_2s1-7s0, 0s0-5s0_6s0-7s0, 0s0-5s0_7s0-9s1, 0s0-2s0_1s0-7s0, 0s0-2s0_7s1-9s0, 0s0-4s0_7s1-10s1, 0s0-5s0_3s0-7s0, 0s0-5s0_4s0-8s0, 0s0-5s0_8s1-10s0 (each certified at the root, depth 2, at the 300 s cap).
Partial (2): 0s0-4s0_1s0-5s1, 0s0-3s0_6.

## compose.py
`compose.txt`: certified_nodes 350, class_covered false (expected; one shard of one list), uncovered_frontier_nodes 868.

## SAT / proof rejection / memory
- SAT: none. Proof rejection: none (every certified record has `c VERIFIED` and `s VERIFIED UNSAT`). Memory: no problem (peak ~5 GB used).

## Files
`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`–`lane2.sh`, `out.jsonl` (new records only, lane by lane), `driver0.log`–`driver2.log` (last 100 lines), `compose.txt`.
