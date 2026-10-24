# C3WAVE2 / K40: roots idx 1348 down to 1000 (decreasing), 3-fold class (m = 11, k = 7)

**Result: 1 of my 349 roots was started and it is partial; 0 closed. Roots 2 to 349 were not reached.
No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 00:57:18 UTC, END = 01:54:18 UTC
(start + 1.2 h − 15 min), runner stopped by hand at 02:02 UTC (end of the time budget).

- C3-S tools: worktree of 132398c (8dc27c3 before the author rewrite) at /opt/c3s, unmodified.
- CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8 (`make cake_lpr`; example prints `s VERIFIED UNSAT`),
  drat-trim lrat-check 2e3b2dc + `results/E2/tools/lrat-check-E2.patch`. Sanity check on {1},{-1}:
  LRAT `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both (`tools.txt`).
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…0cdd6da` (matches).
- Roots: rows of `C3WAVE2/roots.tsv` with idx 1348 down to 1000, in decreasing idx order: 349 roots (`roots.tsv`).
- Runner (`runner.sh`): the TASK.md runner, `close_tree.py … --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`, S = min(0.17, hours left).

## Per root

| # | idx | root | status | certified by depth | splits | solve s | check s |
|---|-----|------|--------|--------------------|--------|---------|---------|
| 1 | 1348 | 0s0_5s1-6s0 | **partial** | d4: 101 | d2: 1 (timeout at 300 s, 120 children); d3: 8 (pre-split, 91 children each) | 7369 | 2968 |
| 2–349 | 1347…1000 | (`roots.tsv`) | not reached | – | – | – | – |

Root 1 timed out at 300 s and was split into 120 depth-3 children: 8 one-orbit children were pre-split
into 728 depth-4 nodes, and 112 two-orbit depth-3 nodes stayed. That makes one batch of 840 nodes.
`close_tree.py` checks its `--hours` deadline only between batches, so the 10-minute slice could not end
the batch. The root ran from 00:59:52 until I stopped it at 02:02. In that time, all 91 children of
`0s0_5s1-6s0_1` and 10 of the 91 children of `0s0_5s1-6s0_2` were certified (101 depth-4 nodes, all UNSAT at
under 300 s, all with `c VERIFIED` and `s VERIFIED UNSAT`). Still open: the other 627 depth-4 nodes and all 112
depth-3 nodes. The records are in `out.jsonl` and can be resumed. Solve and check times are summed per node, not wall time.

Totals: 101 certified nodes (all at depth 4), 1 UNKNOWN (the root at depth 2), 9 split records.

## compose.py

`compose.txt`: `{"certified_nodes": 101, "class_covered": false, "uncovered_frontier_nodes": 308, …}`.
As expected, the class is not covered. compose recomputed the CNF sha256 of all 101 certified nodes.

## SAT / proof rejections / memory

None. No SAT FOUND, no PROOF NOT ACCEPTED, no out-of-memory.

## Note for later waves

The roots near the end of `roots.tsv` (the `0s0_…` ones, 263 units) may be much harder than the
`0s0-…` ones. With a 300 s cap on the root, a timeout makes a batch of hundreds of nodes, and the
deadline does not stop it. A per-root slice only works if the deadline is checked inside the batch.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl`, `driver.log` (last 200 lines), `compose.txt`, `README.md`.
