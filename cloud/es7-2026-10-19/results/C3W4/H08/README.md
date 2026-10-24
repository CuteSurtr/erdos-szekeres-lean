# C3W4 / H08: wave 4, list W4_H3.tsv, shard 8 of 30

**Result: root `0s0_1s1-3s0` (H3/two, row 8) is closed: open frontier 0 and no timed-out node without children. Root `0s0_1s1-9s1` (row 38) is partial. Roots `0s0_3s0-4s1` (row 68) and `0s0_5s0-6s0` (row 98) were not reached. No SAT. No proof rejections. No memory problems.**

## Setup

The VM had 4 cores, 15 GB RAM and no swap (`env.txt`). It ran from 11:31:04 UTC on 2026-10-24, with END at 16:16:04 (start + 5 h − 15 min). The task file is `results/C3W4/TASK.md` at commit 3fd8a4d8. The values were V = H08, LIST = W4_H3.tsv, j = 8, N = 30, SLICE = 2.0 and H = 5.0.

- Tools: a worktree of commit 95cafa93 at `/opt/c3u`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8, and lrat-check 2e3b2dc with the E2 patch. The sanity checks passed (`tools.txt`).
- Base CNF from `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`. Both match.
- Roots: rows with row ≡ 8 (mod 30), which gives 4 roots (`roots.tsv`). No records were seeded.
- Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat`, with S = min(2.0, hours left). The runner is `runner.sh`.

## Per root

"d" is the number of layers and "σ" is the number of 3-bit σ levels. Solve and check seconds are summed per node, with 3 jobs sharing 4 cores.

| row | root | status | certified | timeouts | splits | solve s | check s |
|---|---|---|---|---|---|---|---|
| 8 | 0s0_1s1-3s0 | **closed** | d2/σ2: 50 cubes; d3/σ2: 714 (all at cap 600) | 1 at cap 1 (root), 8 at cap 1 (σ1), 14 cubes at cap 300 (σ2) | 9 σ splits (8 children each), 14 layer splits (51 children each) | 29,682 | 18,469 |
| 38 | 0s0_1s1-9s1 | partial (frontier: 59 of 64 cubes not finished) | d2/σ2: 5 | 1 at cap 1 (root), 8 at cap 1 (σ1) | 9 σ splits | 1,155 | 223 |
| 68 | 0s0_3s0-4s1 | not reached | – | – | – | – | – |
| 98 | 0s0_5s0-6s0 | not reached | – | – | – | – | – |

Row 8 took 4.5 h of wall time (11:32:50 to 16:03:34). `close_tree.py` checks its deadline only between BFS levels. The 2 h slice therefore ran out while the level of 714 layer-split children was in progress, and that level ran to the end. All 714 children were certified at cap 600, and the final output was `{"root": "0s0_1s1-3s0", "open_frontier": 0}`. No split record has `"children": 0`.

Row 38 started at 16:03:34 with a 0.208 h slice. Its 64 6-bit cubes form a single BFS level, so they would have run well past END. I stopped the runner at 16:13:43, 2.3 minutes before END, because a wait loop timed out before it reached END. At that point 5 cubes were certified. The other 59 cubes and anything in progress have no records. The killed processes left no checker records, so there are no `cake_lpr: none` records to re-check.

## Totals (stratum H3/two)

769 certified nodes, every one with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`. 1 root closed, 1 partial, 2 not reached. Total solve time was 30,837 s and check time 18,692 s. The largest proof was 515 MB; no proof was kept.

## SAT, rejections, memory

- SAT: none.
- PROOF NOT ACCEPTED: none. `recheck.jsonl` is not needed.
- Memory: no problems. Used memory peaked at about 10 GB of 15 GB.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all 833 records), `driver.log.tail`.
