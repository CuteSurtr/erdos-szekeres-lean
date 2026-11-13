# C3W3 / B3: wave 3, list B_h3pilot.tsv, shard 3 of 10, 1 lane

**Result: 0 of my 3 roots closed. Root 1 (`0s0_1s0-3s1`) is partial with 245 certified depth-4 nodes. Roots 2 and 3 were not reached. No SAT, no proof rejection, no memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:40:58 UTC on 2026-10-21, H = 3.0 h, END = start + 3 h − 15 min = 07:25:58 UTC.
Task: `results/C3W3/TASK.md` at 640a56c2, with V = B3, LIST = B_h3pilot.tsv, j = 3, N = 10, LANES = 1, JOBS = 3, SLICE = 0.9.

- C3-S tools: worktree of 132398c at /opt/c3s, unmodified.
- CaDiCaL 3.0.1 at c6073042; cake_lpr a36874a8 (its example gives `s VERIFIED UNSAT`); lrat-check 2e3b2dc with the E2 patch.
  Sanity check: `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both (`tools.txt`).
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da`, which matches.
- Roots: the rows of B_h3pilot.tsv with row ≡ 3 (mod 10): rows 3, 13 and 23 (`roots.tsv`). All three are `untouched`, so I seeded **0 records**.
  `out.jsonl` therefore holds only new records (255 lines).
- One lane (`lane0.sh`): `close_tree.py … --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`, with S = min(0.9, hours left).

## Per root

| row | root | stratum | status | certified by depth | splits | timeouts | solve s | check s |
|-----|------|---------|--------|--------------------|--------|----------|---------|---------|
| 3 | 0s0_1s0-3s1 | H3/two | **partial** | d4: 245 | d2: 1 (timeout at 300 s); d3: 8 (pre-split, 91 children each) | 1 (d2, 300 s) | 19086 | 7353 |
| 13 | 0s0_2s0-4s0 | H3/two | not reached | – | – | – | – | – |
| 23 | 0s0_3s1-4s0 | H3/two | not reached | – | – | – | – | – |

The solve and check times are summed per node, not wall-clock: 3 jobs shared 4 cores.

Root `0s0_1s0-3s1` timed out at 300 s and was split into 8 single-orbit depth-3 children (layers 2, 4, 5, 6, 7, 8, 9 and 10). Each was pre-split into 91 depth-4 nodes, 728 in all. Of these, 245 are certified, all at the 600 s cap and with no depth-4 timeouts. The slowest solve took 280 s.
- `_2`: 91/91 certified; `_4`: 91/91 certified; `_5`: 63/91 certified; `_6` to `_10`: not started.
- So 483 depth-4 nodes are still open. A later wave can resume from `out.jsonl`, which holds the certified and split records.

The 0.9 h slice ran out at 05:48, but `close_tree.py` checks its deadline only between batches. The whole 728-node frontier was a single batch, so the root used the rest of the budget. At END I killed the runner, its process group and the remaining solver and checker processes. The jobs still running then left no records: none was written, so there are no `cake_lpr: none` records to re-check.

## Totals per stratum

| stratum | roots | closed | partial | not reached | certified nodes | timeouts |
|---------|-------|--------|---------|-------------|-----------------|----------|
| H3/two | 3 | 0 | 1 | 2 | 245 (all depth 4) | 1 |

## compose.py

`compose.txt`: `certified_nodes: 245`, `class_covered: false`. That is expected for one shard of one list. compose recomputed the CNF sha256 of every certified node.

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none. Every UNSAT record has `c VERIFIED` (lrat-check) and `s VERIFIED UNSAT` (cake_lpr).
- Memory: no problem. Usage peaked around 7 GB of 15 GB.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`, `out.jsonl` (new records only; 0 seeded), `driver0.log` (last 100 lines), `compose.txt`, `README.md`.
