# C3W3 / B6: list B_h3pilot.tsv, shard 6 of 10, 1 lane, --jobs 3, slice 0.9 h, budget 3.0 h

**Result: no SAT, no proof rejection, no memory problem. Root `0s0_1s0-7s0` is partial (375 certified depth-4 nodes); roots `0s0_2s0-9s0` and `0s0_3s1-7s0` were not reached.**

## Setup
One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:41:13 UTC, END 07:26:13 UTC (start + 3 h − 15 min), 2026-10-21. Task file at 640a56c2.

- C3-S tools: worktree of 132398c at /opt/c3s, unmodified.
- CaDiCaL 3.0.1, c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (example prints `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 + E2 patch. Sanity check passed: LRAT `3 0 0` on {1},{-1} rejected by both checkers, `3 0 1 2 0` accepted by both (`tools.txt`).
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: rows 6, 16, 26 of `lists/B_h3pilot.tsv` (`roots.tsv`), all `untouched`, stratum H3/two.
- **Seeded records: 0** (no partial roots). `out.jsonl` contains only new records (385 lines).
- One lane (`lane0.sh`), `close_tree.py ... --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`, S = min(0.9, hours to END).

## Per root (depth = number of layers; roots are at depth 2)

| row | root | stratum | status | certified by depth | splits | timeouts | solve s | check s |
|-----|------|---------|--------|--------------------|--------|----------|---------|---------|
| 6 | 0s0_1s0-7s0 | H3/two | partial | d4: 375 | d2: 1 (timeout, 120 children); d3: 8 (pre-split one-orbit, 91 children each) | 1 (root, 300 s) | 17982 | 11199 |
| 16 | 0s0_2s0-9s0 | H3/two | not reached | – | – | – | – | – |
| 26 | 0s0_3s1-7s0 | H3/two | not reached | – | – | – | – | – |

Solve/check times are summed per node (3 jobs on 4 cores, so inflated vs. wall clock).

Root 6 timed out at 300 s and was split into 120 depth-3 children; the 8 one-orbit children were pre-split into 728 depth-4 nodes. 375 of them were certified (all at the 600 s cap, none timed out), covering the subtrees of `_2`, `_3`, `_4`, `_5` and part of `_6`. Still open: the other 353 depth-4 nodes and the 112 two-orbit depth-3 children (never attempted). `close_tree.py` checks its `--hours` deadline only between frontier batches, so the 0.9 h slice did not stop the root: the first batch ran until END, and the lane was then killed (07:26–07:31 UTC). The in-flight nodes at the kill (2 CaDiCaL runs, 1 cake_lpr) wrote no record, so there is no `cake_lpr: none` record to recheck.

## Totals per stratum
H3/two: 3 roots; 0 closed, 1 partial, 2 not reached; 375 certified nodes, 1 timeout, 9 split records.

## compose.py
`compose.txt`: `certified_nodes: 375, class_covered: false, uncovered_frontier_nodes: 304` (expected; one partial root only). It recomputed the CNF sha256 of every certified node.

## SAT / proof rejections / memory
- SAT: none.
- PROOF NOT ACCEPTED: none. Every certified record has `c VERIFIED` (lrat-check) and `s VERIFIED UNSAT` (cake_lpr).
- Memory: no problem (peak about 9 GB used of 15 GB).
