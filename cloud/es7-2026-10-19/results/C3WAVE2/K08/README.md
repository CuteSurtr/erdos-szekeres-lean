# C3WAVE2 / K08: shard 8 of 40, 3-fold class (m = 11, k = 7)

**Result: 0 of my 34 roots closed. Root 1 (`0s0-1s1_4s0-8s1`) is partial: 538 of its 546 leaves are certified and 8 depth-4 nodes are still open. Roots 2–34 were not reached. No SAT. No proof rejections. No memory problems.**

## Setup

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Started 00:23 UTC on 2026-10-21, H = 1.5 h, END = 01:38 UTC. Tools are listed in `tools.txt`:
- C3-S tools: a worktree of `132398c` (8dc27c3 before the rewrite) at `/opt/c3s`, used unmodified.
- CaDiCaL 3.0.1 (`c6073042`), cake_lpr (`a36874a8`; its example prints `s VERIFIED UNSAT`), and drat-trim lrat-check (`2e3b2dc`) with the E2 patch. Sanity check on {1},{-1}: `3 0 0` is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…d6da`. **This matches.**
- Roots: the rows of `C3WAVE2/roots.tsv` with idx ≡ 8 (mod 40), 34 roots (`roots.tsv`).
- `runner.sh` runs `close_tree.py … --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours min(0.17, left)` once per root.

## Per root

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_4s0-8s1 | partial | d3: 84, d4: 454 | d2: 1 (timeout at 300 s → 91 children); d3: 7 (pre-split one-orbit, 66 children each → 462 d4) | 4690 | 7704 |
| 2–34 | (`roots.tsv`) | not reached | – | – | – | – |

Root 1 still has 8 open depth-4 nodes (all under `_10`), which were never finished. Its records are in `out.jsonl`, so a later wave can resume it. Solve and check times are summed over nodes, with 3 jobs sharing 4 cores.

Totals: 547 records, 538 certified nodes (each has `c VERIFIED` and `s VERIFIED UNSAT`), 8 split records, and 1 UNKNOWN (the root at 300 s). `compose.py` (`compose.txt`) reports `certified_nodes: 538`, `class_covered: false`, as expected, and recomputed every certified CNF sha256.

## Why only one root was reached

`close_tree.py` checks `--hours` only between frontier batches. Root 1's 10-minute slice ended during its first big batch, and the batch kept running: the 91 depth-3 nodes, then 462 depth-4 nodes at a 600 s cap. So the slice overran, and the whole budget went to root 1. The tool was used unmodified, as the task requires. A later wave should take this into account: either give each root a cap on wall time from outside the tool, or accept that a slice can last as long as one batch.

## Incidents (these affect time only, not results)

1. At about 00:57 the session's worker process restarted, and this killed the runner in the middle of a batch. The records already written were kept, and the nodes that were in flight were re-solved. At 00:58 I restarted the runner (`=== RESTART` in `driver.log`). Because of this, root 1 got a second slice.
2. At 01:40 (the time budget) I stopped the driver by hand while root 1 was still in a batch (`=== STOPPED` in `driver.log`).

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory problems: none. Peak use was about 5 GB with 3 jobs.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `compose.txt`.
