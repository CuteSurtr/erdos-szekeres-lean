# C3WAVE2 / K22: shard 22 of 40, 3-fold class (m = 11, k = 7)

**Result: root 1 of 34 (`0s0-1s1_5s1-7s0`) is closed, with every leaf of its tree certified. Roots 2–34 were not reached. No SAT, no proof rejection, no memory problem.**

## Setup (`tools.txt`, `env.txt`)

One cloud VM: 4 cores, 15 GB RAM, no swap. Start 00:27:48 UTC 2026-10-21; END = start + 1.5 h − 15 min = 01:42:48.
- C3-S tools: worktree of 132398c (8dc27c3 before the rewrite) at /opt/c3s, unmodified.
- CaDiCaL 3.0.1 (c6073042); cake_lpr a36874a8 (example prints `s VERIFIED UNSAT`); lrat-check 2e3b2dc + E2 patch.
  Sanity check: `3 0 0` on {1},{-1} is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da` (matches).
- Roots: idx ≡ 22 (mod 40) of `C3WAVE2/roots.tsv`, 34 roots (`roots.tsv`). Runner: `runner.sh` (same as K15 apart from START).

## Per root

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_5s1-7s0 | **closed** | d3: 84, d4: 462 | d2: 1 (timeout at 300 s, 91 children); d3: 7 (pre-split, 66 children each) | 5471 | 8844 |
| 2–34 | (`roots.tsv`) | not reached | – | – | – | – |

Solve and check times are summed per node. They are not wall-clock: 3 jobs shared 4 cores.

The root timed out at 300 s and was split into 91 depth-3 children. Seven of these are one-orbit layers, pre-split into 7 × 66 = 462 depth-4 nodes. All 84 + 462 = 546 leaves were certified in a single batch: all were UNSAT within their cap, with no timeouts. `close_tree.py` checks the `--hours` deadline only between batches, so this one batch ran from 00:30 to 01:54, well past its 10-minute slice and past END. When it ended, the runner stopped because END had passed. No other root was started.

## Totals

546 certified nodes, each with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`. There is 1 UNKNOWN record (the root at 300 s). Closed roots: `0s0-1s1_5s1-7s0`. Partial roots: none.

## compose.py

`compose.txt`: `certified_nodes: 546, class_covered: false`. Coverage is not expected from one shard. compose recomputed the CNF sha256 of all 546 certified nodes.

## SAT / rejections / memory

No SATISFIABLE result. No PROOF NOT ACCEPTED. Peak memory use was about 8 GB of 15 GB, and there were no checker failures.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `compose.txt`.
