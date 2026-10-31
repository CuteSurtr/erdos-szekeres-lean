# C3WAVE2 / K30: shard 30 of 40, wave 2, 3-fold class (m = 11, k = 7)

**Result: 1 of my 33 roots is closed (`0s0-1s1_6s1-7s0`). The other 32 were not reached. No SAT. No proof rejection. No memory problem.**

## Setup (`env.txt`, `tools.txt`)

One cloud VM, 4 cores, 15 GB RAM, no swap. Started 00:29:35 UTC on 2026-10-21, with H = 1.5 h, so END = 01:44:35.
- C3-S tools: worktree of `132398c` (8dc27c3 before the rewrite) at /opt/c3s, unmodified.
- CaDiCaL 3.0.1 (c60730422e75…); cake_lpr a36874a8 (`make cake_lpr`, example gives `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc with the E2 patch. The patch is a normal diff, so I applied it with `patch` instead of `git apply`.
- Sanity check on {1},{-1}: `3 0 0` is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none -o /opt/work/base.cnf`: `p cnf 168399 4154921`, sha256 `bf0e502e…cdd6da` (matches).
- Roots: the rows of `C3WAVE2/roots.tsv` with idx ≡ 30 (mod 40), 33 roots (`roots.tsv`). Runner: `runner.sh`, `--jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours 0.17`.

## Per root

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_6s1-7s0 | **closed** | d3: 84, d4: 462 | d2: 1 (timeout at 300 s, 91 children); d3: 7 (pre-split one-orbit, 66 children each) | 5057 (d2 UNKNOWN 300 s + d3 + d4) | 7975 |
| 2–33 | (`roots.tsv`) | not reached | – | – | – | – |

**Closed:** 0s0-1s1_6s1-7s0. **Partial:** none. **Not reached:** 0s0-2s0_1s1-3s0 0s0-2s0_4s0-6s0 0s0-2s0_6s0-9s0 0s0-2s1_1s0-6s1 0s0-2s1_3s1-4s1 0s0-2s1_5s0-6s1 0s0-2s1_7s0-9s1 0s0-3s0_1s1-10s1 0s0-3s0_2s1-8s0 0s0-3s0_5s1-10s0 0s0-3s0_8 0s0-3s1_1s1-6s0 0s0-3s1_4s0-5s0 0s0-3s1_5s1-8s1 0s0-3s1_8s1-9s0 0s0-4s0_1s1-9s1 0s0-4s0_3s0-8s1 0s0-4s0_6s0-7s1 0s0-4s1_1 0s0-4s1_2s0-5s1 0s0-4s1_3s1-6s0 0s0-4s1_6s1-7s0 0s0-5s0_1s0-3s1 0s0-5s0_2s0-9s0 0s0-5s0_3s1-9s1 0s0-5s0_7s0-10s0 0s0-5s1_1s0-8s0 0s0-5s1_2s1-4s1 0s0-5s1_4s0-7s1 0s0-5s1_7s1-10s1 0s0_1s1-2s1 0s0_2s1-8s0 

Totals: 546 certified nodes (84 at depth 3 and 462 at depth 4). Every one has `c VERIFIED` (lrat-check with the E2 patch) and `s VERIFIED UNSAT` (cake_lpr). The longest solve took 61.7 s. Solve and check times are summed per node over 3 parallel jobs, so they are not wall-clock time.

## Why only one root

`close_tree.py` checks `--hours` only between batches, where a batch is the whole current frontier. Root 1 timed out at depth 2 after 300 s. Its full child batch of 546 nodes (84 two-orbit depth-3 nodes, plus 462 depth-4 children of the 7 pre-split one-orbit nodes) started before the 10-minute slice ended. That batch ran to completion from 00:32:18 to 01:49:10. By then END had passed, so the runner started no further roots. The tool was used unmodified. A later wave that wants real 10-minute slices needs a deadline check inside the batch.

## compose.py

`compose.txt`: `{"certified_nodes": 546, "class_covered": false, "uncovered_frontier_nodes": 162, ...}`. The class is not covered, as expected. compose recomputed the CNF sha256 of all 546 certified nodes.

## SAT / proof rejections / memory

None. Memory peaked at about 7 GB used of 15 GB.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `compose.txt`, `README.md`.
