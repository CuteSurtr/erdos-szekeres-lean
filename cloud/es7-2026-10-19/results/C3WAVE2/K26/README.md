# C3WAVE2 / K26: shard 26 of 40, 3-fold class (m = 11, k = 7)

**Result: 0 of my 34 roots closed. Root 1 (`0s0-1s1_6s0-10s1`) is partial, with 531 certified nodes and 15 depth-3 children still open. Roots 2–34 were not reached. No SAT. No proof rejection. No memory problem.**

## Setup (`tools.txt`, `env.txt`)

One cloud VM: 4 cores, 15 GB RAM, no swap. Start 00:26:55 UTC on 2026-10-21, END 01:41:55 (start + 1.5 h − 15 min).
- C3-S tools: worktree `/opt/c3s` at 132398c (formerly 8dc27c3), unmodified (0 changes)
- CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8 (`make cake_lpr`; the example prints `s VERIFIED UNSAT`), drat-trim lrat-check 2e3b2dc + E2 patch.
  Sanity check: the LRAT `3 0 0` on {1},{-1} is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none -o /opt/work/base.cnf`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da` (matches)
- Roots: idx ≡ 26 (mod 40) in `results/C3WAVE2/roots.tsv`, 34 roots (`roots.tsv`). `runner.sh` is the K12 runner with my END.

## Per root

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_6s0-10s1 | partial | d3: 69, d4: 462 | d2: 1 (UNKNOWN at 300 s, 91 children); d3: 7 (one-orbit pre-split, 66 children each) | 4949 | 7812 |
| 2–34 | (`roots.tsv`) | not reached | – | – | – | – |

Root 1 hit the 300 s cap and was split into 91 depth-3 children: 84 two-orbit children and 7 one-orbit children. The one-orbit children (`_2`, `_3`, `_4`, `_5`, `_7`, `_8`, `_9`) were pre-split into 462 depth-4 nodes. That gives one batch of 546 nodes. `close_tree.py` checks its `--hours` deadline only between batches, so the 10-minute slice did not stop this batch. It ran from 00:29 to the end of my budget.

At 01:44 I stopped the runner by hand, to leave time for the write-up. By then all 462 depth-4 nodes and 69 of the 84 depth-3 nodes were certified. The 15 depth-3 nodes below have no record yet; a later wave resumes them from `out.jsonl`:
`_5s0-9s1 _5s1-9s0 _5s1-9s1 _7s0-8s0 _7s0-8s1 _7s1-8s0 _7s1-8s1 _7s0-9s0 _7s0-9s1 _7s1-9s0 _7s1-9s1 _8s0-9s0 _8s0-9s1 _8s1-9s0 _8s1-9s1` (each prefixed by `0s0-1s1_6s0-10s1`).

Solve and check times are summed per node, not wall-clock: 3 jobs shared the 4 cores.

## Totals

531 certified nodes. Every one has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`. There is one UNKNOWN record (the root, at 300 s) and 8 split records.
Closed roots: none. Partial roots: `0s0-1s1_6s0-10s1`. Not reached: the other 33.

`compose.txt`: `{"certified_nodes": 531, "class_covered": false, "uncovered_frontier_nodes": 177, ...}`. As expected, the class is not covered. compose recomputed the CNF sha256 of all 531 certified nodes.

## SAT / proof rejection / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: at most about 8 GB used of 15 GB. No problem.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `compose.txt`, `README.md`.
