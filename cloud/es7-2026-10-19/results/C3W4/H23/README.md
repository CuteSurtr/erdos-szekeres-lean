# C3W4 / H23: wave 4, W4_H3.tsv shard 23 of 30, 3-fold class (m = 11, k = 7)

**Result: 1 of my 3 roots closed (`0s0_1s1-10s0`), 2 partial. No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:26 UTC, END 16:16:26 UTC (start + 5 h − 15 min), 2026-10-24.

- Tools: worktree of commit 95cafa93 at `/opt/c3u`, `results/C3U/tools` used unmodified.
- CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8 (bundled example: `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch.
  Sanity check passed: LRAT `3 0 0` on {1},{-1} is rejected by both checkers, and `3 0 1 2 0` is accepted by both (`tools.txt`).
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).
- Roots: rows of `W4_H3.tsv` with row ≡ 23 (mod 30), i.e. rows 23, 53 and 83, all `H3/two`, all untouched. No records were seeded.
- Runner (`runner.sh`): `close_tree.py … --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours S`, with S = min(2.0, hours left).
  `compose.py` was not run, as the task says.

## Per root

Depth is the number of layers; "σ bits" is the size of the σ-cube. Solve and check seconds are summed per node, so they are not wall time (3 jobs on 4 cores).

| row | root | status | certified | timeouts | splits | solve s | check s | wall |
|-----|------|--------|-----------|----------|--------|---------|---------|------|
| 23 | 0s0_1s1-10s0 | **closed** (open frontier 0, no childless split) | 64 (depth 2, 6 σ bits, cap 300) | root and 8 3-bit cubes at cap 1 (intended) | 9 σ splits | 6111 | 2720 | 11:34–12:25 |
| 53 | 0s0_2s1-3s0 | partial | 54 (depth 3, 6 σ bits, cap 600) | cap 1: root + 8; **cap 300: all 64 6-bit cubes** | 9 σ, 64 layer (3,264 children) | 20767 | 1602 | 12:25–14:34 |
| 83 | 0s0_3s1-7s1 | partial | 39 (depth 2, 6 σ bits, cap 300) + 4 (depth 3, 6 σ bits, cap 600) | cap 1: root + 8; cap 300: 25 of 64 6-bit cubes | 9 σ, 25 layer (1,275 children) | 16086 | 1855 | 14:34–16:16 |

Open frontier at the stop (layer children not yet certified): about 3,210 for row 53 and 1,271 for row 83. These records can be resumed. No split record has `"children": 0`.

Total for the `H3/two` stratum (my only stratum): 161 certified nodes, all with `c VERIFIED` and `s VERIFIED UNSAT`. Of the 192 6-bit cubes, 103 were certified at cap 300 and 89 timed out and were layer-split. That is 0 of 64 on row 53, 39 of 64 on row 83 and 64 of 64 on row 23. Layer children at cap 600 run fast, averaging about 30 s solve.

## Slice enforcement (operator action; `operator.log`)

`close_tree.py` checks `--hours` only between levels. On row 53, the level of 3,264 layer children at cap 600 started after the 2.0 h slice, and it would have run far past END.
At 14:34:01 (2 h 9 min into the slice) I killed that close_tree and its workers so that row 83 could get its slice. The runner then started row 83 with S = 1.707 h.
At END I killed the runner and every solver and checker. Nodes in flight at a kill leave no record, so no `cake_lpr: none` record exists and nothing needed a re-check (`recheck.jsonl` is absent).

## SAT / rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none. There are 0 records with `cake_lpr` `none`, and 0 UNSAT records that are not certified.
- Memory: peak about 9 GB used of 15. No problem.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (393 records), `driver.log.tail`, `operator.log`, `summary.txt`.
