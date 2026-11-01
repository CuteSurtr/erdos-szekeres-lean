# C3W3 / A3: wave 3, 3-fold class (m = 11, k = 7), list A_s0.tsv shard 3 of 8

**Result: 37 roots. 10 closed, 3 partial, 24 not reached. 589 new certified nodes. No SAT, no proof rejection, no memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:40:09 UTC on 2026-10-21. END = start + 2.0 h − 15 min = 06:25:09 UTC.
Tools (`tools.txt`) are exactly as in C3WAVE2 step 1:
- C3-S tools: worktree of commit 132398c at `/opt/c3s`, used unmodified.
- CaDiCaL 3.0.1 (c6073042). cake_lpr a36874a8: its example prints `s VERIFIED UNSAT`. lrat-check 2e3b2dc with the E2 patch. Sanity check: `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF: `p cnf 168399 4154921`, sha256 `bf0e502e…6dd6da`, which matches.

Roots: the rows of `lists/A_s0.tsv` with row ≡ 3 (mod 8), 37 in all (`roots.tsv`). I ran 3 lanes (`lane0.sh` to `lane2.sh`), and lane k took the roots at 0-based positions ≡ k (mod 3). Each root ran `close_tree.py … --jobs 1 --caps 300,300,600 --cadopts=--sat --split-singles --hours min(0.5, left)`.

`close_tree.py` checks its deadline only between batches, so each lane's first long root ran past its 0.5 h slice. All three lanes were still on such a root at END. At END I killed the lane process groups (runner, driver, solver and checkers). A killed node writes no record, so `out.jsonl` has no `cake_lpr: none` record and nothing needed a re-check.

**Seeded records: 16, all in lane 0.** They are split records only (8 for `0s0-5s0_1s0-10s0` and 8 for `0s0-4s0_3s0-5s1`) from earlier waves. No earlier certified records exist for these two roots. `out.jsonl` holds only the 599 new records: lane 0 first (without the 16 seeded lines), then lane 1, then lane 2.

## Per root (depth = number of layers; roots are at depth 2)

The "splits" column includes the seeded split records. Solve and check times are summed per node.

| row | root | stratum | h6m_kept | list status | status | certified by depth | splits | timeouts | solve s | check s |
|-----|------|---------|----------|-------------|--------|--------------------|--------|----------|---------|---------|
| 3 | 0s0-5s0_1s0-10s0 | H6(5,0)/two | partial | **partial** | d3: 84, d4: 155 | d2: 1, d3: 7 | 0 | 1955 | 4084 |
| 11 | 0s0-2s0_1s0-6s1 | H6(2,0)/two | untouched | **closed** | d2: 1 | – | 0 | 120 | 43 |
| 19 | 0s0-2s0_3s0-7s0 | H6(2,0)/two | untouched | **closed** | d2: 1 | – | 0 | 11 | 26 |
| 27 | 0s0-2s0_3s1-7s1 | H6(2,0)/two | untouched | **not reached** | – | – | 0 | 0 | 0 |
| 35 | 0s0-2s0_4s1-8s1 | H6(2,0)/two | untouched | **closed** | d2: 1 | – | 0 | 48 | 30 |
| 43 | 0s0-2s0_6s0-7s1 | H6(2,0)/two | untouched | **closed** | d2: 1 | – | 0 | 76 | 27 |
| 51 | 0s0-4s0_2s0-6s1 | H6(4,0)/two | untouched | **not reached** | – | – | 0 | 0 | 0 |
| 59 | 0s0-4s0_5s1-9s1 | H6(4,0)/two | untouched | **closed** | d2: 1 | – | 0 | 81 | 29 |
| 67 | 0s0-5s0_1s0-2s0 | H6(5,0)/two | untouched | **closed** | d2: 1 | – | 0 | 17 | 20 |
| 75 | 0s0-5s0_1s0-9s1 | H6(5,0)/two | untouched | **not reached** | – | – | 0 | 0 | 0 |
| 83 | 0s0-5s0_1s1-7s0 | H6(5,0)/two | untouched | **closed** | d2: 1 | – | 0 | 121 | 33 |
| 91 | 0s0-5s0_2s0-3s0 | H6(5,0)/two | untouched | **closed** | d2: 1 | – | 0 | 22 | 20 |
| 99 | 0s0-5s0_2s0-9s0 | H6(5,0)/two | untouched | **not reached** | – | – | 0 | 0 | 0 |
| 107 | 0s0-5s0_2s1-8s1 | H6(5,0)/two | untouched | **closed** | d2: 1 | – | 0 | 148 | 37 |
| 115 | 0s0-5s0_6s0-8s1 | H6(5,0)/two | untouched | **closed** | d2: 1 | – | 0 | 172 | 36 |
| 123 | 0s0-5s0_6s1-9s0 | H6(5,0)/two | untouched | **not reached** | – | – | 0 | 0 | 0 |
| 131 | 0s0-5s0_7s1-9s0 | H6(5,0)/two | untouched | **partial** | d4: 247 | d2: 1, d3: 7 | 1 | 1586 | 3759 |
| 139 | 0s0-4s0_5 | H6(4,0)/one | untouched | **partial** | d3: 93 | d2: 1 | 0 | 3434 | 2221 |
| 147 | 0s0-4s0_3s0-5s1 | H6(4,0)/two | partial | **not reached** | – | d2: 1, d3: 7 | 0 | 0 | 0 |
| 155 | 0s0-2s0_1s1-7s1 | H6(2,0)/two | untouched | **not reached** | – | – | 0 | 0 | 0 |
| 163 | 0s0-2s0_5s1-10s0 | H6(2,0)/two | untouched | **not reached** | – | – | 0 | 0 | 0 |
| 171 | 0s0-2s0_6s1-9s1 | H6(2,0)/two | untouched | **not reached** | – | – | 0 | 0 | 0 |
| 179 | 0s0-2s0_8s0-9s0 | H6(2,0)/two | untouched | **not reached** | – | – | 0 | 0 | 0 |
| 187 | 0s0-4s0_2s0-3s0 | H6(4,0)/two | untouched | **not reached** | – | – | 0 | 0 | 0 |
| 195 | 0s0-4s0_3s1-9s1 | H6(4,0)/two | untouched | **not reached** | – | – | 0 | 0 | 0 |
| 203 | 0s0-4s0_7s1-9s1 | H6(4,0)/two | untouched | **not reached** | – | – | 0 | 0 | 0 |
| 211 | 0s0-4s0_8s1-9s1 | H6(4,0)/two | untouched | **not reached** | – | – | 0 | 0 | 0 |
| 219 | 0s0-5s0_3s0-10s0 | H6(5,0)/two | untouched | **not reached** | – | – | 0 | 0 | 0 |
| 227 | 0s0-5s0_3s0-8s1 | H6(5,0)/two | untouched | **not reached** | – | – | 0 | 0 | 0 |
| 235 | 0s0-5s0_3s1-6s1 | H6(5,0)/two | untouched | **not reached** | – | – | 0 | 0 | 0 |
| 243 | 0s0-5s0_4s0-10s1 | H6(5,0)/two | untouched | **not reached** | – | – | 0 | 0 | 0 |
| 251 | 0s0-5s0_4s0-9s1 | H6(5,0)/two | untouched | **not reached** | – | – | 0 | 0 | 0 |
| 259 | 0s0-5s0_4s1-8s1 | H6(5,0)/two | untouched | **not reached** | – | – | 0 | 0 | 0 |
| 267 | 0s0-5s0_7s1-9s1 | H6(5,0)/two | untouched | **not reached** | – | – | 0 | 0 | 0 |
| 275 | 0s0-5s0_8s1-9s1 | H6(5,0)/two | untouched | **not reached** | – | – | 0 | 0 | 0 |
| 283 | 0s0-3s0_8 | H6(3,0)/one | untouched | **not reached** | – | – | 0 | 0 | 0 |
| 291 | 0s0-5s0_4 | H6(5,0)/one | untouched | **not reached** | – | – | 0 | 0 | 0 |

Closed (10): 0s0-2s0_1s0-6s1, 0s0-2s0_3s0-7s0, 0s0-2s0_4s1-8s1, 0s0-2s0_6s0-7s1, 0s0-4s0_5s1-9s1, 0s0-5s0_1s0-2s0, 0s0-5s0_1s1-7s0, 0s0-5s0_2s0-3s0, 0s0-5s0_2s1-8s1, 0s0-5s0_6s0-8s1. All were certified at the root (depth 2) without a split.

Partial (3), each killed at END:
- 0s0-5s0_1s0-10s0: resumed from the seeded splits.
- 0s0-5s0_7s1-9s0: one depth-3 node timed out at 300 s and was split.
- 0s0-4s0_5: a one-orbit root, pre-split.

Not reached (24): every other root, including 0s0-4s0_3s0-5s1 (list status partial; its seeded splits are unchanged).

## Totals per stratum

| stratum | closed | partial | not reached | certified nodes | timeouts |
|---------|--------|---------|-------------|-----------------|----------|
| H6(5,0)/two | 5 | 2 | 11 | 491 | 1 |
| H6(2,0)/two | 4 | 0 | 5 | 4 | 0 |
| H6(4,0)/two | 1 | 0 | 6 | 1 | 0 |
| H6(4,0)/one | 0 | 1 | 0 | 93 | 0 |
| H6(3,0)/one | 0 | 0 | 1 | 0 | 0 |
| H6(5,0)/one | 0 | 0 | 1 | 0 | 0 |

Total: 589 certified nodes. Every one has lrat-check `c VERIFIED` (E2 patch) and cake_lpr `s VERIFIED UNSAT`. There is 1 timeout (at 300 s). No record has `certified: false`.

## compose.py

`compose.txt`: `{"certified_nodes": 589, "class_covered": false, "uncovered_frontier_nodes": 892, ...}`. As expected, this machine's shard does not cover the class. compose recomputed the CNF sha256 of all 589 certified nodes.

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: peak use was about 9 of 15 GB, with 3 lanes at `--jobs 1`. No problems.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh` to `lane2.sh`, `out.jsonl` (new records only), `driver0.log` to `driver2.log` (last 100 lines of each), `compose.txt`, `README.md`.
