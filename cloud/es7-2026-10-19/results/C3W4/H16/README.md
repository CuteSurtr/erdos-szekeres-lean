# C3W4 / H16: wave 4, list W4_H3.tsv, shard 16 of 30

**Result: 1 of my 3 roots is closed (`0s0_2s0-6s0`). The other 2 are partial. No SAT, no proof rejection, no memory problem.**

## Setup

- One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:03 UTC on 2026-10-24, END 16:16:03 UTC (start + 5 h − 15 min). Task `results/C3W4/TASK.md` at 3fd8a4d8.
- Tools (`tools.txt`): C3U tools from a worktree of 95cafa93 at `/opt/c3u`, used unmodified. CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (the example gives `s VERIFIED UNSAT`), and lrat-check 2e3b2dc with the E2 patch. In the sanity check, `3 0 0` on {1},{-1} is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`. It matches.
- Roots: the rows of `W4_H3.tsv` with row ≡ 16 (mod 30). These are rows 16, 46 and 76 (`roots.tsv`), all in stratum H3/two, and none were seeded.
- Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat`, slice 2.0 h. `compose.py` was not run, as the task says.

## Runner incident (affects time only, not results)

`close_tree.py` checks `--hours` only between rounds. On root 1 the round of layer children (2,907 nodes at cap 600) started just before the slice ended, so `runner.sh` would have run past the slice and spent the rest of the budget on root 1.

At 13:41:33 (8 min after the slice end at 13:33:14) I stopped `runner.sh` and that round. The close_tree processes were killed first, then the solvers and checkers, so no partial record was written. No record has cake_lpr `none`.

`runner2.sh` (same command) then ran roots 2 and 3. It kills each root's run at the end of its slice and at END, in the same order. Root 3 was cut this way at END (16:16:12).

## Per root

Notation: L*n* = node with *n* layers (the roots have 2), σ*s* = number of 3-bit σ splits on the path (σ2 = the 6-bit cubes). The cap-1 timeouts are the root and its 8 σ1 cubes, which time out at once by design.

| row | root | status | certified (by depth / σ level) | timeouts | splits | open frontier | solve s | check s |
|-----|------|--------|-------------------------------|----------|--------|---------------|---------|---------|
| 16 | 0s0_1s0-4s1 | **partial** | L2/σ2: 7, L3/σ2: 55 (cap 600) | cap 1: 9, cap 300: 57 | σ: 9, layer: 57 (2,907 children) | 2,852 | 20,532 | 1,881 |
| 46 | 0s0_2s0-6s0 | **closed** | L2/σ2: 64 (all 64 cubes at cap 300) | cap 1: 9 | σ: 9 | 0 | 7,397 | 2,325 |
| 76 | 0s0_3s0-8s1 | **partial** | L2/σ2: 36 | cap 1: 9, cap 300: 24 | σ: 9, layer: 24 | 1,228 (4 σ2 cubes cut at END + 1,224 layer children) | 16,167 | 1,454 |

- Root 16: 57 of 64 cubes timed out at 300 s. All 55 of their layer children that ran were certified at cap 600, with none timing out.
- Root 46: closed in 55 min (13:41:46 to 14:36:48).
- Root 76: ran for 1.65 h until END.
- No split record has `"children": 0`. The open frontiers above were recomputed from `out.jsonl` with the tool's expansion.
- Solve and check seconds are summed per node over 3 parallel jobs, so they are not wall-clock time.

## Totals (stratum H3/two, the only one here)

1 closed, 2 partial, 0 not reached. 162 certified nodes in all (`c VERIFIED` and `s VERIFIED UNSAT` on every one), 108 split records and 4,080 open frontier nodes. Solve 44,096 s, check 5,660 s. 378 records in `out.jsonl`.

## SAT / rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none, and no certified-looking record with cake_lpr `none` (so there is no `recheck.jsonl`).
- Memory: at most about 6 GB used of 15 GB, no problem.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh` (until 13:41), `runner2.sh` (from 13:41), `out.jsonl` (all records), `driver.log.tail`, `README.md`.
