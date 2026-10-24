# C3WAVE2 / K16: shard 16 of 40, wave 2, 3-fold class (m = 11, k = 7)

**Result: 0 of my 34 roots closed. Root 1 (`0s0-1s1_5`) is partial; roots 2 to 34 were not reached. No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). The run went from 00:25 to 01:40 UTC on 2026-10-21 (H = 1.5 h, END = start + 75 min).
The tools are as in `results/C3WAVE1/C00/README.md`; details are in `tools.txt`:
- C3-S tools: worktree of `132398c` at `/opt/c3s`, used unmodified.
- CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8 (`make cake_lpr`; the example prints `s VERIFIED UNSAT`), and lrat-check 2e3b2dc with the E2 patch.
  Sanity check: the LRAT `3 0 0` on {1},{-1} is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF from `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da`, which matches.
- Roots: the rows of `C3WAVE2/roots.tsv` with idx ≡ 16 (mod 40), 34 roots (`roots.tsv`). The runner is `runner.sh`, with `--jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`, S = 0.17.

## The slice did not bound the root

`close_tree.py` checks `--hours` only between frontier layers. It submits a whole layer at once and waits for all of it. Root 1, `0s0-1s1_5`, is a single-orbit layer at depth 2, so it is pre-split into 120 depth-3 children, all in one batch. With 3 jobs and a 300 s cap, that batch alone takes about 2 to 3 hours. The 10-minute slice therefore never took effect, and the root used the whole budget. At END (01:40) the driver was still inside this first batch, and I killed it. Each record is written when its node finishes, so `out.jsonl` keeps every finished node and can be resumed. Only the nodes running at the kill were lost, and they will be re-run on resume.
Later waves should note this: a pre-split root with 120 children cannot fit in a 10-minute slice with this driver.

## Per root

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_5 | partial | d3: 68 | d2: 1 (pre-split, 120 children); d3: 8 (timeout at 300 s, 91 children each) | 10558 | 2304 |
| 2–34 | (`roots.tsv`) | not reached | – | – | – | – |

For root 1, depth 3 stands at 68 certified, 8 timed out and split, and 44 not finished. The timed-out nodes are `_2, _3, _4, _6, _7, _8, _9, _10` (single-orbit layers). They give 728 depth-4 children, none attempted. Solve times of the certified nodes run from 27 to 256 s per node. These are summed per node and inflated by 3 jobs sharing 4 cores.

Closed roots: none. Partial roots: `0s0-1s1_5`. Not reached: the other 33 roots in `roots.tsv`.

## Totals

There are 68 certified nodes, all at depth 3. Each has `c VERIFIED` (lrat-check with the E2 patch) and `s VERIFIED UNSAT` (cake_lpr). `out.jsonl` has 85 records: 68 UNSAT, 8 UNKNOWN, and 9 split records (1 pre-split and 8 after timeouts).
`compose.txt`: `certified_nodes: 68`, `class_covered: false`, `uncovered_frontier_nodes: 214`. Not covered, as expected. compose recomputed the CNF sha256 of all 68 certified nodes.

## SAT / rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: peak use was about 2 to 3 GB of 15 GB. No problem.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `compose.txt`.
