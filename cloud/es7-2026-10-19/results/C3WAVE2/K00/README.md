# C3WAVE2 / K00: shard 0 of 40, 3-fold class (m = 11, k = 7)

**Result: no root closed. Root 1 (`0s0-1s1_2s1-5s0`) is partial: 505 of its 546 frontier nodes are certified and 41 are open. Roots 2 to 34 were not reached. No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 00:22:14 UTC on 2026-10-21, budget 1.5 h, runner END 01:37:14.
- Tools: worktree of `132398c` at `/opt/c3s`, used unmodified. CaDiCaL 3.0.1 (c6073042). cake_lpr a36874a8 (its example prints `s VERIFIED UNSAT`). lrat-check 2e3b2dc with the E2 patch. On {1},{-1}, both checkers reject `3 0 0` and accept `3 0 1 2 0` (`tools.txt`).
- Base CNF from `gen_case.py 11 7 none` (`-o /opt/work/base.cnf`): `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da`. Both match.
- Roots: rows of `C3WAVE2/roots.tsv` with idx ≡ 0 (mod 40), 34 roots (`roots.tsv`). Runner: `runner.sh`, with `--jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours min(0.17, left)`.

## The 10-minute slice is not enforced inside a batch

`close_tree.py` checks `--hours` only between batches. Each batch is the whole current frontier, so once a batch starts it runs to the end. Root 1 timed out at depth 2 (300 s) and was split into 91 depth-3 children. Seven of them were one-orbit nodes, which were pre-split into 66 depth-4 children each. That gave one batch of 84 + 462 = 546 nodes, which ran from about 00:29 until the end of the budget. I killed the driver at 01:46:18 (start + 1 h 24 min) to leave time for the write-up, and the runner never reached root 2. Later waves should keep this in mind: on a root that needs a split, the slice is really a whole batch.

## Per root

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_2s1-5s0 | partial | d3: 43, d4: 462 | d2: 1 (timeout at 300 s); d3: 7 (pre-split, 66 children each) | 5307 | 8508 |
| 2–34 | (`roots.tsv`) | not reached | – | – | – | – |

Solve and check times are per-node sums (3 jobs on 4 cores), not wall-clock. Root 1 has 41 open depth-3 nodes. They were never finished: the batch was killed, and these nodes have no record in `out.jsonl`, so a resume of `close_tree.py` on this root will run them first.

Totals: 505 certified nodes (`c VERIFIED` and `s VERIFIED UNSAT` for each), 1 UNKNOWN (the root at 300 s), 8 split records.

Closed roots: none. Partial roots: `0s0-1s1_2s1-5s0`.

## compose.py

`compose.txt`: `certified_nodes 505, class_covered false, uncovered_frontier_nodes 203`. This is expected for one shard. compose recomputed the CNF sha256 of all 505 certified nodes.

## SAT / rejections / memory

No SAT. No PROOF NOT ACCEPTED. Peak memory use was about 7 GB of 15 GB.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (resumable), `driver.log` (last 200 lines), `compose.txt`.
