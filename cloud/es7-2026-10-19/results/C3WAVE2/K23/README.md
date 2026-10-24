# C3WAVE2 / K23: shard 23 of 40, wave 2, 3-fold class (m = 11, k = 7)

**Result: 0 of my 34 roots closed. Root 1 (`0s0-1s1_5s1-8s0`) is partial (535 certified nodes, 11 open);
roots 2–34 were not reached. No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`), 00:27 to 01:57 UTC on 2026-10-21 (H = 1.5).
Tools as in `results/C3WAVE1/C00/README.md`, recorded in `tools.txt`:
C3-S tools from a worktree of `132398c` at `/opt/c3s`, unmodified; CaDiCaL 3.0.1 (c6073042);
cake_lpr a36874a8 (`make cake_lpr`, example prints `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc
with `lrat-check-E2.patch` (sanity: `3 0 0` on {1},{-1} rejected by both checkers, `3 0 1 2 0` accepted by both).
Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256
`bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
Roots: rows of `C3WAVE2/roots.tsv` with idx ≡ 23 (mod 40), 34 roots (`roots.tsv`). Runner: `runner.sh`
(END = start + 1.5 h − 15 min = 01:42:33 UTC).

## Per root

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_5s1-8s0 | partial | d3: 73, d4: 462 | d2: 1 (UNKNOWN at 300 s, 91 children); d3: 7 (pre-split, 66 children each) | 4569 | 8154 |
| 2–34 | (`roots.tsv`) | not reached | – | – | – | – |

Solve/check times are summed per node (3 jobs on 4 cores), not wall-clock.

Root 1 timed out at the 300 s cap and was split into 91 depth-3 children; 7 one-orbit children were
pre-split into 7 × 66 = 462 depth-4 nodes, all certified. Of the 84 two-orbit depth-3 children, 73 were
certified and 11 were still running or queued when I stopped the driver. No node timed out below the root.

Note on the slice: `close_tree.py` checks `--hours` only between layers, so the whole depth-3/4 batch
(546 nodes) of root 1 was submitted at once and ran far past its 10-minute slice (00:30 to 01:45).
At 01:44 (after END) I killed the runner and driver so the README fits in the budget; every finished
record is in `out.jsonl`, and the 11 open nodes are resumable from it.

## Totals

544 records; 535 certified nodes, each with `c VERIFIED` (lrat-check, E2 patch) and `s VERIFIED UNSAT`
(cake_lpr); 1 UNKNOWN (the root at 300 s); 8 split records.

## compose.py

`compose.txt`: `{"certified_nodes": 535, "class_covered": false, "uncovered_frontier_nodes": 173, ...}` —
not covered, as expected for 1/40 of the shards. compose recomputed the CNF sha256 of all 535 certified nodes.

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: up to ~9 GB used of 15 GB with 3 jobs; no failure.

## Lists

- Closed roots: none.
- Partial roots: `0s0-1s1_5s1-8s0`.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log`
(last 200 lines), `compose.txt`.
