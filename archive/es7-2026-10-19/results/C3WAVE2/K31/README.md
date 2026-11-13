# C3WAVE2 / K31: shard 31 of 40, wave 2, 3-fold class (m = 11, k = 7)

**Result: 5 of my 33 roots are closed and 1 is partial. The other 27 were not reached. No SAT, no proof rejection, no memory problem.**
The VM restarted at about 01:41 UTC. That killed the runner while it was working on root 6, three minutes before its END time (01:44), so I did not restart it.

## Setup

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start time 00:29:27 UTC on 2026-10-21. H = 1.5 h, and the runner's END was 01:44:27.
Tools are listed in `tools.txt`, as C3WAVE1/C00 describes them:

- C3-S tools: worktree of commit `132398c` (`8dc27c3` before the author rewrite) at `/opt/c3s`, used unmodified.
- CaDiCaL 3.0.1, commit c6073042.
- cake_lpr a36874a8. Its example prints `s VERIFIED UNSAT`.
- drat-trim lrat-check 2e3b2dc with the E2 patch. Sanity check: `3 0 0` on {1},{-1} is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF from `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da` (matches).
- Roots: the rows of `C3WAVE2/roots.tsv` with idx ≡ 31 (mod 40), 33 roots in all (`roots.tsv`).
- Runner: `runner.sh`. For each root it runs `close_tree.py ... --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours min(0.17, left)`.

## Per root (depth = number of layers; roots are at depth 2)

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_6s1-7s1 | **closed** | d2: 1 | 0 | 30 | 33 |
| 2 | 0s0-2s0_1s1-3s1 | **closed** | d2: 1 | 0 | 10 | 24 |
| 3 | 0s0-2s0_4s0-6s1 | **closed** | d2: 1 | 0 | 66 | 39 |
| 4 | 0s0-2s0_6s0-9s1 | **closed** | d2: 1 | 0 | 61 | 38 |
| 5 | 0s0-2s1_1s0-7s0 | **closed** | d2: 1 | 0 | 257 | 50 |
| 6 | 0s0-2s1_3s1-5s0 | partial | d3: 35, d4: 462 | d2: 1 (timeout at 300 s); d3: 7 (pre-split) | 3448 | 6872 |
| 7–33 | (`roots.tsv`) | not reached | – | – | – | – |

Solve and check times are summed per node. They are not wall-clock time: 3 jobs shared the 4 cores.

Root 6 (`0s0-2s1_3s1-5s0`) timed out at depth 2 after 300 s and was split. Seven of its depth-3 children were one-orbit nodes and were pre-split. That gave a single batch of 546 nodes at depth 3 and depth 4. `close_tree.py` checks `--hours` only between batches, so the 10-minute slice did not stop the run, and the root ran from 00:41 until the VM restarted. At the restart, 497 nodes were certified (35 at depth 3, 462 at depth 4). 49 depth-3 nodes are still open. None of them was split, and none has an UNKNOWN record. The records are in `out.jsonl`, so a later wave can resume the root.

Totals: 502 certified nodes. Every one has both `c VERIFIED` (lrat-check with the E2 patch) and `s VERIFIED UNSAT` (cake_lpr). There is 1 UNKNOWN (the root-6 node at depth 2) and 8 split records. Per-root details are in `summary.jsonl`.

## compose.py

`compose.txt`: `{"certified_nodes": 502, "class_covered": false, "uncovered_frontier_nodes": 510, ...}`. This is as expected, because the shard does not cover the class. compose recomputed the CNF sha256 of all 502 certified nodes.

## SAT / proof rejection / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: no problem. At most about 5 GB of the 15 GB was in use.
- Incident: the VM/worker restarted at about 01:41 to 01:43 UTC. The nodes that were in flight then are lost, and they are simply still open. Every record had already been flushed to `out.jsonl`, and every line parses.

Closed roots: 0s0-1s1_6s1-7s1, 0s0-2s0_1s1-3s1, 0s0-2s0_4s0-6s1, 0s0-2s0_6s0-9s1, 0s0-2s1_1s0-7s0.
Partial root: 0s0-2s1_3s1-5s0.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `summary.jsonl`, `compose.txt`.
