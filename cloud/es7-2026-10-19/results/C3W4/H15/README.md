# C3W4 / H15: wave 4, W4_H3.tsv shard 15 of 30 (one machine)

**Result: 1 of my 3 roots closed (`0s0_1s0-3s0`). `0s0_2s0-5s1` is partial (open frontier 2,906). `0s0_3s0-8s0` was not reached. No SAT, no proof rejection, no memory problem.**

Task: `results/C3W4/TASK.md` at 3fd8a4d8, with V = H15, LIST = W4_H3.tsv, j = 15, N = 30, SLICE = 2.0, H = 5.0.

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:27 UTC, END 16:16:27 UTC.
- Tools: worktree of 95cafa93 at `/opt/c3u`, `C3U/tools` used unmodified. CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (example prints `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch. Sanity check passed: `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both (`tools.txt`).
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).
- Roots: rows 15, 45, 75 of `W4_H3.tsv` (all H3/two, untouched), `roots.tsv`. No seeded records.
- `runner.sh`: `close_tree.py ... --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours S`, S = 2.0.
- `compose.py` was not run, as the task says.

## Per root

Depth = number of layers, σ = σ level (number of 3-bit σ splits in the cube). Solve and check seconds are summed per node. They are not wall-clock time, because 3 jobs share 4 cores.

| root | status | certified (depth/σ) | timeouts | splits | solve s | check s |
|------|--------|---------------------|----------|--------|---------|---------|
| 0s0_1s0-3s0 | **closed** (open frontier 0, no childless split), 11:35–12:15 | d2/σ2: 64 | d2/σ0 cap 1: 1; d2/σ1 cap 1: 8 | σ: 1 + 8 | 4,387 | 2,649 |
| 0s0_2s0-5s1 | partial (open frontier 2,906 at d3/σ2) | d2/σ2: 1; d3/σ2: 307 | d2/σ0 cap 1: 1; d2/σ1 cap 1: 8; **d2/σ2 cap 300: 63 of 64** | σ: 1 + 8; layer: 63 (51 children each, 3,213 in total) | 31,222 | 11,743 |
| 0s0_3s0-8s0 | not reached | – | – | – | – | – |

Root 1: all 64 of its 6-bit cubes were certified at cap 300. Root 2: only 1 of its 64 6-bit cubes was certified at 300 s; 63 timed out and got the layer split. Of the 3,213 depth-3 children at cap 600, 307 were certified with no timeout (max solve 163 s), and 2,906 were still unattempted when the run was stopped. No split record has `"children": 0`.

Totals (stratum H3/two): 372 certified nodes, every one with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`; 81 timeouts (18 at cap 1, as intended, and 63 at cap 300, all on root 2); 534 records in `out.jsonl`.

## Incident: the slice does not bound a generation

`close_tree.py` checks `--hours` only before it submits a new generation. Root 2's third generation (3,213 nodes at cap 600) was submitted at about 14:10, before its 2-hour slice ran out (14:15), and would have taken many more hours. So the slice did not stop it, and root 3 was never started. At END (16:16:27) I killed the runner, and at 16:21 I killed close_tree and the running solvers and checkers (2 cake_lpr, 1 cadical). Killed nodes left no record; they are part of the open frontier. No record has cake_lpr `none`, so there was nothing to re-check (no `recheck.jsonl`).

## SAT / rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: used memory peaked at about 7 GB of 16 GB; no problem.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all 534 records), `driver.log.tail`.
