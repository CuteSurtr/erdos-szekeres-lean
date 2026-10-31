# C3W3 / A2: wave 3, list A_s0, shard 2 of 8, 3-fold class (m = 11, k = 7)

**Result: 17 of my 37 roots were closed, 2 are partial, and 18 were not reached. No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:40:04 UTC on 2026-10-21, H = 2.0 h, END = 06:25:04.
Values: V = A2, LIST = A_s0.tsv, j = 2, N = 8, LANES = 3, JOBS = 1, SLICE = 0.5, Z = 640a56c2.

- C3-S tools: worktree of commit 132398c at /opt/c3s, used unmodified.
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04.
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`). The bundled example prints `s VERIFIED UNSAT`.
- drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with `results/E2/tools/lrat-check-E2.patch`. Sanity check on the CNF {1},{-1}: the LRAT `3 0 0` is rejected by both checkers (lrat-check `c NOT VERIFIED`; cake_lpr `pivot must be non-zero`), and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: rows of `lists/A_s0.tsv` with row ≡ 2 (mod 8), which gives 37 roots (`roots.tsv`). Lane k ran the roots at positions ≡ k (mod 3) (`lane0.sh` to `lane2.sh`), with `close_tree.py ... --jobs 1 --caps 300,300,600 --cadopts=--sat --split-singles --hours min(0.5, hours left)`.

## Seeded records

Only one of my roots had list status `partial`: `0s0-4s0_1s1-2s0` (lane 0). I seeded lane 0's out file with **57 records** (49 certified and 8 split), all from `C3S0/S0/out.jsonl`. None came from the C3WAVE1 or C3WAVE2 files. `out.jsonl` holds only the 334 new records (lane 0, then lane 1, then lane 2), without the seeded ones.

## Per root

"Closed" means that every leaf of the root's tree (seeded + new records) is certified. Depth = number of layers, so the roots are at depth 2. Solve and check times are per-node sums over the new records.

| row | root | stratum | status | certified (new) by depth | timeouts | splits | solve s | check s |
|-----|------|---------|--------|--------------------------|----------|--------|---------|---------|
| 2 | 0s0-4s0_1s1-2s0 | H6(4,0)/two | partial | d3: 84, d4: 183 | 0 | 0 | 1954 | 4069 |
| 10 | 0s0-2s0_1s0-6s0 | H6(2,0)/two | **closed** | d2: 1 | 0 | 0 | 63 | 34 |
| 18 | 0s0-2s0_3s0-6s0 | H6(2,0)/two | **closed** | d2: 1 | 0 | 0 | 8 | 22 |
| 34 | 0s0-2s0_4s1-7s1 | H6(2,0)/two | **closed** | d2: 1 | 0 | 0 | 19 | 23 |
| 42 | 0s0-2s0_5s1-7s0 | H6(2,0)/two | **closed** | d2: 1 | 0 | 0 | 125 | 33 |
| 58 | 0s0-4s0_5s1-7s1 | H6(4,0)/two | **closed** | d2: 1 | 0 | 0 | 20 | 28 |
| 66 | 0s0-5s0_1s0-10s1 | H6(5,0)/two | **closed** | d2: 1 | 0 | 0 | 38 | 18 |
| 82 | 0s0-5s0_1s1-6s1 | H6(5,0)/two | **closed** | d2: 1 | 0 | 0 | 89 | 23 |
| 90 | 0s0-5s0_2s0-10s1 | H6(5,0)/two | **closed** | d2: 1 | 0 | 0 | 39 | 28 |
| 106 | 0s0-5s0_2s1-8s0 | H6(5,0)/two | **closed** | d2: 1 | 0 | 0 | 88 | 30 |
| 114 | 0s0-5s0_6s0-8s0 | H6(5,0)/two | **closed** | d2: 1 | 0 | 0 | 10 | 15 |
| 130 | 0s0-5s0_7s1-8s1 | H6(5,0)/two | **closed** | d2: 1 | 0 | 0 | 18 | 18 |
| 138 | 0s0-4s0_2 | H6(4,0)/one | partial | d3: 45 | 2 (d3, 300 s) | 3 (1 pre-split + 2 after timeouts) | 4453 | 1274 |
| 154 | 0s0-2s0_1s0-9s1 | H6(2,0)/two | **closed** | d2: 1 | 0 | 0 | 31 | 23 |
| 178 | 0s0-2s0_8s0-10s1 | H6(2,0)/two | **closed** | d2: 1 | 0 | 0 | 113 | 30 |
| 202 | 0s0-4s0_7s1-9s0 | H6(4,0)/two | **closed** | d2: 1 | 0 | 0 | 258 | 34 |
| 226 | 0s0-5s0_3s0-8s0 | H6(5,0)/two | **closed** | d2: 1 | 0 | 0 | 108 | 24 |
| 250 | 0s0-5s0_4s0-9s0 | H6(5,0)/two | **closed** | d2: 1 | 0 | 0 | 105 | 30 |
| 274 | 0s0-5s0_8s1-9s0 | H6(5,0)/two | **closed** | d2: 1 | 0 | 0 | 288 | 32 |

Not reached (18): rows 26, 50, 74, 98, 122, 146, 162, 170, 186, 194, 210, 218, 234, 242, 258, 266, 282, 290 (`roots.tsv`). All of them are in lanes 0 and 2, which spent the whole run on their partial roots. Lane 1 finished all 12 of its roots by 05:09 and then sat idle.

## Totals per stratum

| stratum | roots | closed | partial | not reached | certified (new) | timeouts | solve s | check s |
|---------|-------|--------|---------|-------------|-----------------|----------|---------|---------|
| H6(2,0)/two | 9 | 6 | 0 | 3 | 6 | 0 | 359 | 165 |
| H6(4,0)/two | 7 | 2 | 1 | 4 | 269 | 0 | 2232 | 4131 |
| H6(5,0)/two | 17 | 9 | 0 | 8 | 9 | 0 | 783 | 218 |
| H6(4,0)/one | 1 | 0 | 1 | 0 | 45 | 2 | 4453 | 1274 |
| H6(5,0)/one | 2 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| H6(3,0)/one | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| **total** | 37 | 17 | 2 | 18 | 329 | 2 | 8027 | 5788 |

All 329 new certified records have lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.

## Notes

- **The 0.5 h slice was overrun.** `close_tree.py` checks `--hours` only between frontier levels, so a level that has already started runs to completion. With `--jobs 1`, roots 2 and 138 each kept their lane until END: about 1 h 42 min and 1 h 36 min instead of 30 min. That is why 18 roots were not reached.
- At END I killed both remaining lanes. Each was in CaDiCaL: `0s0-4s0_1s1-2s0_7_3s1-8s0` (600 s cap) and `0s0-4s0_2_3s1-7s1` (300 s cap). No checker was running, so there are no `cake_lpr: none` records and no rechecks were needed. The killed nodes have no records, so a later wave will attempt them again.
- SAT: none. PROOF NOT ACCEPTED: none. Memory: no problems; at most about 6 GB was in use.

## compose.py

`compose.txt`: `certified_nodes: 329, class_covered: false, uncovered_frontier_nodes: 802`. The class is not expected to be covered by one shard. compose recomputed the CNF sha256 of every certified node.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh` to `lane2.sh`, `out.jsonl` (new records only), `driver0.log` to `driver2.log` (last 100 lines), `summary.jsonl` (per-root breakdown), `compose.txt`.
