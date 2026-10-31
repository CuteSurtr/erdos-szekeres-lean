# C3WAVE2 / K11: shard 11 of 40, wave 2, 3-fold class (m = 11, k = 7)

**Result: 1 of my 34 roots is closed (`0s0-1s1_4s1-5s1`), 1 is partial (`0s0-1s1_9s0-10s1`, 8 depth-3 nodes
left open), and 32 were not reached. No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 00:23:18 UTC on 2026-10-21, budget 1.5 h,
END = 01:38:18 UTC. Tools (`tools.txt`):

- C3-S tools: worktree of `132398c` (8dc27c3 before the author rewrite) at `/opt/c3s`, unmodified.
- CaDiCaL 3.0.1, c60730422e758ef1cebe7aeddf2dda31c996bf04.
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`); its example prints `s VERIFIED UNSAT`.
- drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 + `results/E2/tools/lrat-check-E2.patch`
  (a normal diff, applied with `patch`). Sanity: on {1},{-1}, LRAT `3 0 0` is rejected by both checkers,
  `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256
  `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: rows of `C3WAVE2/roots.tsv` with idx ≡ 11 (mod 40): 34 roots (`roots.tsv`).
- `runner.sh`: per root, `close_tree.py ... --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`,
  S = min(0.17, hours left before END).

## Per root (roots are at depth 2)

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_4s1-5s1 | **closed** | d2: 1 | 0 | 30 | 33 |
| 2 | 0s0-1s1_9s0-10s1 | partial | d3: 76, d4: 462 | d2: 1 (timeout at 300 s); d3: 7 (pre-split) | 4618 | 7949 |
| 3–34 | (`roots.tsv`) | not reached | – | – | – | – |

Root 2 timed out at 300 s and was split into 91 depth-3 children; 7 single-orbit ones were pre-split into
depth-4 nodes. At the stop, 76 depth-3 and 462 depth-4 nodes were certified (all depth-4 nodes of the
pre-split children are certified), and 8 depth-3 nodes were open (`0s0-1s1_9s0-10s1_6s0-8s0`, `_6s0-8s1`,
`_6s1-8s0`, and 5 more; never finished, no record). No node of this root timed out at depth 3.
Solve and check times are summed per node (3 jobs on 4 cores, so not wall-clock).

**Why only 2 roots:** `close_tree.py` checks `--hours` only between layers, and it submits the whole layer
at once. Root 2's depth-3/4 layer (91 children, ~546 nodes, each solved in ~5 s but checked in ~15 s with
cake_lpr on a ~150 MB proof) took from 00:26 until END, far beyond its 10-minute slice. At 01:40 UTC
(END + 2 min, to keep the README window) I stopped the runner and the driver by hand (`=== STOPPED BY HAND`
in `driver.log`). Every finished node was already written to `out.jsonl`, so the root can be resumed.

## Totals

539 certified nodes (d2: 1, d3: 76, d4: 462), all with lrat-check `c VERIFIED` (E2 patch) and cake_lpr
`s VERIFIED UNSAT`. Records in `out.jsonl`: 539 UNSAT certified, 1 UNKNOWN (root 2 at 300 s), 8 split records.

## compose.py

`compose.txt`: `{"certified_nodes": 539, "class_covered": false, "uncovered_frontier_nodes": 169, ...}`;
not covered, as expected for one shard. compose recomputed the CNF sha256 of all 539 certified nodes.

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: no problem (at most ~8 GB used of 15 GB).

Closed roots: `0s0-1s1_4s1-5s1`. Partial roots: `0s0-1s1_9s0-10s1`.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `compose.txt`.
