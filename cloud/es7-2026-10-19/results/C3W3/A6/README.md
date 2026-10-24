# C3W3 / A6: wave 3, 3-fold class (m = 11, k = 7), list A_s0.tsv, shard 6 of 8

**Result: 8 of my 36 roots are closed. 3 are partial and 25 were not reached. No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:40:25 UTC, END 06:25:25 UTC (start + 2 h − 15 min), 2026-10-21.
The task file is `results/C3W3/TASK.md` at 640a56c2, with V = A6, LIST = A_s0.tsv, j = 6, N = 8, LANES = 3, JOBS = 1, SLICE = 0.5, H = 2.0.

- C3-S tools: worktree of 132398c at /opt/c3s, used unmodified.
- CaDiCaL 3.0.1, c60730422e758ef1cebe7aeddf2dda31c996bf04
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa; its example prints `s VERIFIED UNSAT`
- lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with the E2 patch. Sanity check: `3 0 0` on {1},{-1} is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`, which matches.

Roots: the 36 rows of `A_s0.tsv` with row ≡ 6 (mod 8) (`roots.tsv`). Lane k ran positions ≡ k (mod 3) (`lane0.sh`–`lane2.sh`), each with `--jobs 1 --caps 300,300,600 --cadopts=--sat --split-singles --hours min(0.5, left)`.

Seeded records: there are **158**, all in lane 0. That is 40 for `0s0-5s0_1s1-3s0` and 118 for `0s0-2s0_9`, taken from the C3WAVE1/C3WAVE2/C3S0 out and recheck files, certified or split. `out.jsonl` holds only the 674 new records: lane 0 without its seeded lines, then lane 1, then lane 2.

Note: `close_tree.py` checks `--hours` only between tree levels, so a slice can overrun by a whole level. Lane 0 spent the full budget on its first root. Lane 2 spent it on its fourth root, and lane 1 on its seventh. At END I killed all three lanes (whole process groups). Records are written only when a node finishes, so there are no `cake_lpr: none` records and nothing needed a re-check.

## Per root (depth = number of layers; roots are at depth 2). Solve and check times are summed per node.

| row | root | stratum | status | certified by depth | timeouts | splits | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| 6 | `0s0-5s0_1s1-3s0` | H6(5,0)/two | partial (was partial) | d3: 84, d4: 190 | 0 | – | 1959 | 4127 |
| 14 | `0s0-2s0_1s1-6s1` | H6(2,0)/two | closed | d2: 1 | 0 | – | 47 | 32 |
| 22 | `0s0-2s0_3s0-8s1` | H6(2,0)/two | closed | d2: 1 | 0 | – | 41 | 32 |
| 30 | `0s0-2s0_4s0-6s0` | H6(2,0)/two | not reached | – | 0 | – | 0 | 0 |
| 38 | `0s0-2s0_5s0-7s0` | H6(2,0)/two | closed | d2: 1 | 0 | – | 5 | 15 |
| 46 | `0s0-4s0_1s1-9s0` | H6(4,0)/two | closed | d2: 1 | 0 | – | 16 | 23 |
| 54 | `0s0-4s0_5s0-10s0` | H6(4,0)/two | not reached | – | 0 | – | 0 | 0 |
| 62 | `0s0-4s0_6s0-9s1` | H6(4,0)/two | closed | d2: 1 | 0 | – | 99 | 32 |
| 70 | `0s0-5s0_1s0-4s0` | H6(5,0)/two | closed | d2: 1 | 0 | – | 24 | 22 |
| 78 | `0s0-5s0_1s1-2s0` | H6(5,0)/two | not reached | – | 0 | – | 0 | 0 |
| 86 | `0s0-5s0_1s1-8s1` | H6(5,0)/two | closed | d2: 1 | 0 | – | 208 | 35 |
| 94 | `0s0-5s0_2s0-6s1` | H6(5,0)/two | partial | d4: 308 | 1 | d2: 1, d3: 7 | 1519 | 4395 |
| 102 | `0s0-5s0_2s1-10s1` | H6(5,0)/two | not reached | – | 0 | – | 0 | 0 |
| 110 | `0s0-5s0_6s0-10s0` | H6(5,0)/two | closed | d2: 1 | 0 | – | 44 | 21 |
| 118 | `0s0-5s0_6s1-10s0` | H6(5,0)/two | not reached | – | 0 | – | 0 | 0 |
| 126 | `0s0-5s0_7s0-8s1` | H6(5,0)/two | not reached | – | 0 | – | 0 | 0 |
| 134 | `0s0-3s0_1` | H6(3,0)/one | partial | d3: 74 | 0 | d2: 1 | 3763 | 1793 |
| 142 | `0s0-5s0_1` | H6(5,0)/one | not reached | – | 0 | – | 0 | 0 |
| 150 | `0s0-2s0_9` | H6(2,0)/one | not reached (was partial) | – | 0 | – | 0 | 0 |
| 158 | `0s0-2s0_4s0-10s1` | H6(2,0)/two | not reached | – | 0 | – | 0 | 0 |
| 166 | `0s0-2s0_5s1-9s1` | H6(2,0)/two | not reached | – | 0 | – | 0 | 0 |
| 174 | `0s0-2s0_7s1-10s0` | H6(2,0)/two | not reached | – | 0 | – | 0 | 0 |
| 182 | `0s0-2s0_8s1-9s1` | H6(2,0)/two | not reached | – | 0 | – | 0 | 0 |
| 190 | `0s0-4s0_3s0-7s1` | H6(4,0)/two | not reached | – | 0 | – | 0 | 0 |
| 198 | `0s0-4s0_7s0-10s0` | H6(4,0)/two | not reached | – | 0 | – | 0 | 0 |
| 206 | `0s0-4s0_8s0-9s0` | H6(4,0)/two | not reached | – | 0 | – | 0 | 0 |
| 214 | `0s0-4s0_9s1-10s0` | H6(4,0)/two | not reached | – | 0 | – | 0 | 0 |
| 222 | `0s0-5s0_3s0-4s1` | H6(5,0)/two | not reached | – | 0 | – | 0 | 0 |
| 230 | `0s0-5s0_3s1-10s0` | H6(5,0)/two | not reached | – | 0 | – | 0 | 0 |
| 238 | `0s0-5s0_3s1-8s0` | H6(5,0)/two | not reached | – | 0 | – | 0 | 0 |
| 246 | `0s0-5s0_4s0-7s0` | H6(5,0)/two | not reached | – | 0 | – | 0 | 0 |
| 254 | `0s0-5s0_4s1-6s0` | H6(5,0)/two | not reached | – | 0 | – | 0 | 0 |
| 262 | `0s0-5s0_6s1-10s1` | H6(5,0)/two | not reached | – | 0 | – | 0 | 0 |
| 270 | `0s0-5s0_8s0-9s0` | H6(5,0)/two | not reached | – | 0 | – | 0 | 0 |
| 278 | `0s0-5s0_9s1-10s0` | H6(5,0)/two | not reached | – | 0 | – | 0 | 0 |
| 286 | `0s0-4s0_3` | H6(4,0)/one | not reached | – | 0 | – | 0 | 0 |

## Totals per stratum

| stratum | roots | closed | partial | not reached | certified nodes | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| H6(5,0)/two | 17 | 3 | 2 | 12 | 585 | 1 | 3754 | 8600 |
| H6(2,0)/two | 8 | 3 | 0 | 5 | 3 | 0 | 93 | 78 |
| H6(4,0)/two | 7 | 2 | 0 | 5 | 2 | 0 | 114 | 55 |
| H6(3,0)/one | 1 | 0 | 1 | 0 | 74 | 0 | 3763 | 1793 |
| H6(5,0)/one | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| H6(2,0)/one | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| H6(4,0)/one | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| total | 36 | 8 | 3 | 25 | 664 | 1 | 7723 | 10526 |

The splits at d2 are a pre-split for `0s0-3s0_1` and a 300 s timeout for `0s0-5s0_2s0-6s1`. The d3 splits of `0s0-5s0_2s0-6s1` are one-orbit pre-splits.
Closed roots: `0s0-2s0_1s1-6s1`, `0s0-2s0_3s0-8s1`, `0s0-2s0_5s0-7s0`, `0s0-4s0_1s1-9s0`, `0s0-4s0_6s0-9s1`, `0s0-5s0_1s0-4s0`, `0s0-5s0_1s1-8s1`, `0s0-5s0_6s0-10s0`.
Partial roots: `0s0-5s0_1s1-3s0`, `0s0-5s0_2s0-6s1`, `0s0-3s0_1`. Their records are in `out.jsonl`, plus the 158 seeded records for `0s0-5s0_1s1-3s0`, so a later wave can resume them. `0s0-2s0_9` was partial before this wave and was not reached here.

## compose.py

`compose.txt`: `certified_nodes: 664, class_covered: false`. This is expected for one shard. compose recomputed the CNF sha256 of every certified node.

## SAT / rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none. Every UNSAT record has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.
- Memory: no problem. At most 3 jobs ran at once, and used memory stayed at or below about 6 GB of 15 GB.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`–`lane2.sh`, `out.jsonl` (new records only), `driver0.log`–`driver2.log` (the last 100 lines of each), `compose.txt`, `README.md`.
