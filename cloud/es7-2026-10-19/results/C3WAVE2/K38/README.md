# C3WAVE2 / K38: shard 38 of 40, wave 2, 3-fold class (m = 11, k = 7)

**Result: 0 of my 34 roots are closed. Root 1 (`0s0-1s1_7s1-10s0`) is partial: 537 nodes certified, 9 depth-3 nodes still open. Roots 2–34 were not reached. No SAT, no proof rejection, no memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 00:31:20 UTC on 2026-10-21, END (start + 1.5 h − 15 min) 01:46:20 UTC.
The tools are the ones in the C00 README (`tools.txt`):
- C3-S tools: worktree of `132398c` (it was `8dc27c3` before the author rewrite) at /opt/c3s, used unmodified.
- CaDiCaL 3.0.1 (c6073042); cake_lpr a36874a8 (`make cake_lpr`), which prints `s VERIFIED UNSAT` on its example; drat-trim lrat-check 2e3b2dc with the E2 patch. Sanity check on {1},{-1}: both checkers reject `3 0 0` and both accept `3 0 1 2 0`.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da`. This matches the expected value.
- Roots: the rows of `C3WAVE2/roots.tsv` with idx ≡ 38 (mod 40). That gives 34 roots (`roots.tsv`).
- Runner: `runner.sh` gives each root a 10-minute slice: `--jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`.

## What happened

`close_tree.py` checks its `--hours` deadline only between batches, and it runs a whole batch to the end once it starts. Root 1 timed out at the 300 s cap at depth 2 and was split into 91 depth-3 children. Seven of those (`_2 _3 _4 _5 _6 _8 _9`, the one-orbit layers) were pre-split into 66 children each, which put 84 + 462 = 546 nodes in one batch. That batch used the whole budget. At END (01:46:20) it was still running, so I killed the runner and the driver by hand at 01:46:44 (last line of `driver.log`). All finished results were already flushed to `out.jsonl`, so the root can be resumed.

## Per root

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_7s1-10s0 | **partial** | d3: 75 (300 s cap), d4: 462 (600 s cap) | d2: 1 (timeout at 300 s, 91 children); d3: 7 (pre-split, 66 each) | 4554 | 7953 |
| 2–34 | (`roots.tsv`, from `0s0-2s0_1s1-7s1` on) | not reached | – | – | – | – |

Solve and check times are summed per node. They are not wall-clock times, because 3 jobs shared 4 cores. The slowest certified solve took 43.4 s.

Open nodes of root 1 (9, all at depth 3, never attempted):
`0s0-1s1_7s1-10s0_6s1-8s0`, `_6s0-9s0`, `_6s0-9s1`, `_6s1-9s0`, `_6s1-9s1`, `_8s0-9s0`, `_8s0-9s1`, `_8s1-9s0`, `_8s1-9s1` (each with the prefix `0s0-1s1_7s1-10s0`).

Closed roots: none. Partial roots: `0s0-1s1_7s1-10s0`.

## Totals

537 certified nodes. Every one has `c VERIFIED` (lrat-check, E2 patch) and `s VERIFIED UNSAT` (cake_lpr). There is also 1 UNKNOWN record (the root at depth 2, 300 s) and 8 split records.
`compose.txt`: `{"certified_nodes": 537, "class_covered": false, ...}`. The class is not covered, as expected. compose recomputed the CNF sha256 of all 537 certified nodes.

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: no problem. Peak use was about 9 GB of 15 GB.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `compose.txt`, `README.md`.
