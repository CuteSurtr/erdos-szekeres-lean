# C3WAVE2 / K06: shard 6 of 40 (rerun)

**Result: root 1 of 34 (`0s0-1s1_4s0-10s0`) is partial. 542 nodes are certified and only 4 depth-3 nodes are still open. Roots 2–34 were not reached. No SAT, no proof rejection, no memory problem.**

An earlier K06 session (commits 75e2b11d, baf9db5b) could not build the solver or the checkers. This session built them and replaces that README.

## Setup (`tools.txt`, `env.txt`)

- One cloud VM: 4 cores, 15 GB RAM, no swap. Start 00:50:29 UTC on 2026-10-21. END = start + 1.5 h − 15 min = 02:05:29.
- C3-S tools: a worktree of 132398c (8dc27c3 before the rewrite) at /opt/c3s, used unmodified.
- CaDiCaL 3.0.1, commit c6073042.
- cake_lpr a36874a8 (`make cake_lpr`). Its example prints `s VERIFIED UNSAT`.
- drat-trim lrat-check 2e3b2dc with the E2 patch. Sanity check: `3 0 0` is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none` gives `p cnf 168399 4154921`, sha256 `bf0e502e…0cdd6da`, which **matches**.
- Roots: idx ≡ 6 (mod 40) gives 34 roots (`roots.tsv`). The runner (`runner.sh`) is the TASK.md loop with `--jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours min(0.17, left)`.

## Per root

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_4s0-10s0 | **partial** | d3: 80, d4: 462 | d2: 1 (UNKNOWN at 300 s, 91 children); d3: 7 (pre-split single-orbit, 66 children each) | 4546 | 8413 |
| 2–34 | (`roots.tsv`) | not reached | – | – | – | – |

The open nodes of root 1 are 4 depth-3 nodes that were never finished: `0s0-1s1_4s0-10s0_8s0-9s0`, `_8s0-9s1`, `_8s1-9s0` and `_8s1-9s1`. All 462 depth-4 children of the 7 pre-split nodes (`_2`, `_3`, `_5`, `_6`, `_7`, `_8`, `_9`) are certified, so a resume needs only those 4 nodes.

Solve and check times are summed per node, not measured as wall clock.

Closed roots: none. Partial roots: `0s0-1s1_4s0-10s0`.

## Why only one root

`close_tree.py` checks `--hours` only between layers. The 10-minute slice ran out while the root was being solved at depth 2. The root returned UNKNOWN at 300 s, and its 91 children, after pre-splitting, gave a layer of 546 nodes. The driver runs a whole layer before it checks the deadline again, so that one layer took the rest of the budget. At 02:08 I stopped the driver by hand. Every finished record had already been flushed to `out.jsonl`, and `driver.log.tail` ends with the `KILLED` line.

## Totals and checks

- Certified: 542 nodes. Every one has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.
- `compose.txt`: `certified_nodes 542, class_covered false`. compose recomputed the CNF sha256 of every certified node. The class was not expected to be covered.
- SAT: none. PROOF NOT ACCEPTED: none. Memory: peak use was about 9 of 15 GB, with no failures.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log.tail`, `compose.txt`.
