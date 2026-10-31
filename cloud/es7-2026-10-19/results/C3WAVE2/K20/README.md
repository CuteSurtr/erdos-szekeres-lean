# C3WAVE2 / K20: shard 20 of 40 (idx ≡ 20 mod 40), 3-fold class (m = 11, k = 7)

**Result: 0 of my 34 roots closed, 1 partial, 33 not reached. No SAT. No proof rejection. No memory problem.**
Root 1 (`0s0-1s1_5s0-9s1`) has 545 certified nodes and **1 open node**:
`0s0-1s1_5s0-9s1_8s0-10s1` (depth 3). CaDiCaL had already solved it UNSAT and cake_lpr was checking it when the budget ran out.

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Started 00:27:07 UTC on 2026-10-21 with a 1.5 h budget, so END = 01:42:07.
Tools are listed in `tools.txt`, all as in `C3WAVE1/C00/README.md`:
- C3-S tools: a worktree of `132398c` (`8dc27c3` before the rewrite) at `/opt/c3s`, used unmodified.
- CaDiCaL 3.0.1 `c6073042`.
- cake_lpr `a36874a8`. Its example prints `s VERIFIED UNSAT`.
- lrat-check `2e3b2dc` with the E2 patch. Sanity check: `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`, which matches.

The runner (`runner.sh`) is the one from the task: `--jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours min(0.17, left)`.

## Why only one root

`close_tree.py` checks `--hours` only between batches. Root 1 was not solved at the depth-2 cap (300 s, UNKNOWN), so it was split. Its first batch of children then held 545+ nodes, including depth-4 nodes from the pre-split single-orbit children. That one batch ran from 00:29:50 until I stopped it at 01:44:51. That was past END, and I stopped it to leave time for this write-up. The process group was killed. Every finished node had already been written to `out.jsonl`, so the root can be resumed. The one open node lost only its in-progress cake_lpr check.

## Per root

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_5s0-9s1 | partial (1 open node, d3) | d3: 83, d4: 462 | d2: 1 (UNKNOWN at 300 s); d3: 7 (pre-split, single-orbit) | 4169 | 8467 |
| 2–34 | (`roots.tsv`) | not reached | – | – | – | – |

Solve and check times are summed per node. They are not wall-clock time: 3 jobs shared 4 cores.

Totals: 545 certified nodes. Each one has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.

Closed roots: none. Partial roots: `0s0-1s1_5s0-9s1`. Not reached: roots 2–34 of `roots.tsv`.

## compose.py

`compose.txt`: `{"certified_nodes": 545, "class_covered": false, "uncovered_frontier_nodes": 163, ...}`. As expected, the class is not covered. compose recomputed the CNF sha256 of all 545 certified nodes.

## SAT / rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: peak use was about 9 of 15 GB in use. No memory problem.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `compose.txt`.
