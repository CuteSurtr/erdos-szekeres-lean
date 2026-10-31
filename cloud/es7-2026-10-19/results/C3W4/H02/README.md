# C3W4 / H02: wave 4, W4_H3.tsv shard 2 of 30, σ-cube splitting

**Result: no root closed, 3 partial, 1 reached only at its first σ levels. No SAT. No proof rejection. No memory problem.**
314 nodes certified (lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT` on every one).

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:07 UTC 2026-10-24, END 16:16:07 UTC (start + 5 h − 15 min).
Task file `results/C3W4/TASK.md` at 3fd8a4d8. Details in `tools.txt`.

- Tools: worktree of 95cafa93 at `/opt/c3u`, `results/C3U/tools` used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 c6073042; cake_lpr a36874a8 (example: `s VERIFIED UNSAT`); lrat-check 2e3b2dc with the E2 patch.
  Sanity check: on {1},{-1}, LRAT `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`. Both match.
- Roots: rows 2, 32, 62, 92 of `W4_H3.tsv` (`roots.tsv`). No records were seeded.
- Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat`, slice 2.0 h (`runner.sh`).

### Deviation in how roots were stopped (timing only; results unaffected)

`close_tree.py` checks `--hours` only between batches. A single batch (64 cubes at 300 s, or the layer-split children at 600 s) can run past the slice, so a root would otherwise have used up the whole budget.

I added two watchdogs, both outside the tools:
- `slicedog.sh` stops a root's `close_tree` when its slice runs out.
- `enddog.sh` stops it at END − 40 s.

Both kill the Python processes before the solvers and checkers. A killed node therefore writes no record: no fake timeout and no `cake_lpr: none`. Afterwards I checked `out.jsonl`:
- no UNKNOWN record at cap 300 or 600 that stopped early;
- no UNSAT record that is not certified.

So no node needed a re-check, and there is no `recheck.jsonl`. Nodes that were running when a root was killed have no record; they are still in the open frontier.

Side effect: after `enddog` stopped root 3 at 16:15:30, the runner still had 37 s left, so it started root 4 with a 0.01 h slice. Root 4 then got only its cap-1 records before the END kill at 16:16:16.

## Per root

Depth = number of layers in the node name. σ level = number of 3-bit σ splits on the path. The open frontier is computed from the records as the children of split records minus the certified and split nodes. No split record has `"children": 0`.

| row | root | status | certified (depth 2 σ2 / depth 3 σ2) | timeouts | splits | open frontier | solve s | check s |
|-----|------|--------|------|------|------|------|------|------|
| 2 | 0s0_1s0-3s1 | partial | 38 / 37 | cap 1: 9; cap 300: 26 | σ: 1+8; layer: 26 (1,352 children) | 1,289 | 18,321 | 2,896 |
| 32 | 0s0_1s1-6s1 | partial | 60 / 153 | cap 1: 9; cap 300: 4 | σ: 1+8; layer: 4 (204 children) | 51 | 15,178 | 5,929 |
| 62 | 0s0_2s1-7s1 | partial | 26 / 0 | cap 1: 9; cap 300: 4 | σ: 1+8; layer: 4 (204 children) | 238 | 6,020 | 1,112 |
| 92 | 0s0_4s1-5s0 | partial (only cap-1 levels, started 37 s before END) | 0 / 0 | cap 1: 7 | σ: 1+6 | 50 | 7 | 0 |

- Root 2 (`0s0_1s0-3s1`): all 64 six-bit cubes ran. 38 were certified at ≤ 300 s, 26 timed out and were layer-split. 37 of their 1,352 children were certified at the 600 s cap before the slice ended.
- Root 32 (`0s0_1s1-6s1`): 60 of the 64 cubes were certified and 4 were layer-split. 153 of those 204 children are certified and 51 are left.
- Root 62 (`0s0_2s1-7s1`): 42-minute slice. 26 cubes certified, 4 timed out and were split. Its remaining cubes were still running at END.
- Root 92 (`0s0_4s1-5s0`): only the cap-1 σ levels ran.

Times are summed per node with 3 jobs sharing 4 cores, so they are not wall-clock.

## Totals (stratum H3/two; all 4 roots)

- Certified nodes: 314 (124 at cap 300, 190 at cap 600). Longest solve 299.8 s, largest proof 560 MB, none committed.
- Timeouts: 34 at cap 300 and 34 at cap 1 (the cap-1 ones are by design).
- Solve time 39,529 s; check time 9,936 s.
- SAT: none. Proof rejections: none. Memory: at most about 9 GB used, no OOM, no cake_lpr `none`.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `slicedog.sh`, `enddog.sh`, `out.jsonl` (454 records, resumable), `driver.log.tail`.
