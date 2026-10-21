# C3WAVE2 / K05: shard 5 of 40, wave 2, 3-fold class (m = 11, k = 7)

**Result: 6 of my 34 roots are closed, 1 is partial, 27 were not reached. No SAT. No proof rejection.**
469 nodes certified, every one with lrat-check (E2 patch) `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 00:21:41 UTC on 2026-10-21, budget 1.5 h,
END = 01:36:41 UTC. Details in `tools.txt`:

- C3-S tools: worktree of commit `132398c` (= `8dc27c3` before the author rewrite) at `/opt/c3s`, unmodified.
- CaDiCaL 3.0.1, c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa
  (`make cake_lpr`, example prints `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
  with `results/E2/tools/lrat-check-E2.patch`. Sanity check on CNF {1},{-1}: LRAT `3 0 0` rejected by both
  (lrat-check `c NOT VERIFIED`, cake_lpr `c Checking failed`), `3 0 1 2 0` accepted by both.
- Base CNF: `gen_case.py 11 7 none` (this tool version needs `-o /opt/work/base.cnf`):
  `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: rows of `C3WAVE2/roots.tsv` with idx ≡ 5 (mod 40): 34 roots (`roots.tsv`).
- `runner.sh`, per root: `close_tree.py base.cnf out.jsonl R --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`,
  S = min(0.17, hours left before END).

## Per root (depth = number of layers; roots are at depth 2)

| # | idx | root | status | certified by depth | splits | solve s | check s |
|---|-----|------|--------|--------------------|--------|---------|---------|
| 1 | 5 | 0s0-1s1_3s1-7s1 | **closed** | d2: 1 | 0 | 239 | 47 |
| 2 | 45 | 0s0-1s1_8s0-9s0 | **closed** | d2: 1 | 0 | 33 | 40 |
| 3 | 85 | 0s0-2s0_3s0-4s1 | **closed** | d2: 1 | 0 | 114 | 42 |
| 4 | 125 | 0s0-2s0_4s1-9s0 | **closed** | d2: 1 | 0 | 53 | 38 |
| 5 | 165 | 0s0-2s0_7s1-10s1 | **closed** | d2: 1 | 0 | 9 | 20 |
| 6 | 205 | 0s0-2s1_1s1-6s1 | **closed** | d2: 1 | 0 | 268 | 48 |
| 7 | 245 | 0s0-2s1_4s0-5s1 | partial | d3: 1, d4: 462 | d2: 1 (timeout at 600 s); d3: 7 (pre-split, one-orbit) | 3139 | 6413 |
| 8–34 | | (`roots.tsv`) | not reached | – | – | – | – |

Root 7 (`0s0-2s1_4s0-5s1`) timed out at its 600 s cap and was split into 91 depth-3 children. The 7 one-orbit
children (`_1`, `_3`, `_6`, `_7`, `_8`, `_9`, `_10`) were pre-split into 7 × 66 = 462 depth-4 nodes, and **all
462 were certified**, so those 7 subtrees are closed. Of the 84 two-orbit depth-3 children, 1 was certified and
83 are open (never finished; 3 were running at the stop). The resume frontier is these 83 depth-3 nodes.

Solve and check times are summed per node, not wall-clock (3 jobs on 4 cores).

## The 10-minute slice is not enforced inside a batch

`close_tree.py` checks `--hours` only between batches: it submits the whole frontier at once and waits for all of
it. Root 7's depth-3 batch (553 nodes) started at about 00:50 and was still running at END, so this root used
57 minutes instead of 10, and roots 8–34 were never started. At 01:37:21 (40 s after END) I stopped
`close_tree.py` by hand (the runner then exited) and killed the 3 orphaned CaDiCaL runs. Every finished
node had already been written to `out.jsonl`; only the 3 running nodes were lost, and they are open in
the frontier. A later wave can resume from `out.jsonl`. For later waves, a per-batch deadline or smaller
batches would keep the slice.

## Totals

| depth | certified | split | open |
|-------|-----------|-------|------|
| 2 | 6 | 1 (timeout) | 27 roots not reached |
| 3 | 1 | 7 (pre-split) | 83 |
| 4 | 462 | 0 | 0 |

469 certified nodes; 478 records in `out.jsonl` (469 UNSAT certified, 1 UNKNOWN at 600 s, 8 split records).

## compose.py

`compose.txt`: `{"certified_nodes": 469, "class_covered": false, "uncovered_frontier_nodes": 543, ...}`. As
expected, the class is not covered (this machine holds 1/40 of the roots). compose recomputed the CNF sha256 of
all 469 certified nodes from the base CNF and the node names.

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: no problem (about 9 GB used at peak with 3 jobs).

Closed roots: `0s0-1s1_3s1-7s1`, `0s0-1s1_8s0-9s0`, `0s0-2s0_3s0-4s1`, `0s0-2s0_4s1-9s0`, `0s0-2s0_7s1-10s1`, `0s0-2s1_1s1-6s1`.
Partial: `0s0-2s1_4s0-5s1`. Not reached: the other 27 rows of `roots.tsv`.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines),
`compose.txt`, this README.
