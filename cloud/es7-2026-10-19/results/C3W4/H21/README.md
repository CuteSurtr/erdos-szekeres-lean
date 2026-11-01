# C3W4 / H21: wave 4, list W4_H3.tsv, shard 21 of 30 (SLICE 2.0 h, H 5.0 h, task at 3fd8a4d8)

**Result: 2 of 3 roots closed (`0s0_1s0-8s1`, `0s0_2s0-9s0`). Root `0s0_3s1-6s0` is partial with 347 open nodes. No SAT. No proof rejections. No memory problems.**

## Setup

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:06 UTC, END 16:16:06 UTC (start + 5 h − 15 min). The run was stopped at 16:18:45.

- Tools: worktree of 95cafa93 at /opt/c3u, `results/C3U/tools` used unmodified. No `compose.py` was run.
- CaDiCaL 3.0.1 c60730422e75; cake_lpr a36874a8b750 (its example gives `s VERIFIED UNSAT`); lrat-check 2e3b2dc0ecf9 with the E2 patch. Sanity check: `3 0 0` on {1},{-1} is rejected by both checkers, and `3 0 1 2 0` is accepted by both (`tools.txt`).
- Base CNF from `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`, which matches.
- Roots are rows 21, 51 and 81 of W4_H3.tsv (`roots.tsv`), all `H3/two` and untouched. Nothing was seeded.
- `runner.sh`: `close_tree.py … --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours S`, with S = min(2.0, hours left).

## Per root

Depth counts layers (roots are at depth 2). σ level is the number of σ bits fixed. Solve and check seconds are summed per node over 3 parallel jobs, so they are not wall time.

| root | status | certified (depth/σ bits) | timeouts | splits | solve s | check s | wall |
|------|--------|--------------------------|----------|--------|---------|---------|------|
| 0s0_1s0-8s1 | **closed** (open frontier 0, no childless split) | d2/σ6: 64 | root (cap 1) 1, σ3 (cap 1) 8 | σ: 1 + 8 | 6983 | 2402 | 11:32–12:26 |
| 0s0_2s0-9s0 | **closed** (open frontier 0, no childless split) | d2/σ6: 64 | root 1, σ3 8 | σ: 1 + 8 | 8236 | 2489 | 12:26–13:27 |
| 0s0_3s1-6s0 | **partial**, open frontier 347 | d2/σ6: 51, d3/σ6: 316 | root 1, σ3 8, σ6 at 300 s: 13 | σ: 1 + 8; layer: 13 (51 children each) | 21099 | 9345 | 13:27–16:18 (killed at END) |

The cap-1 timeouts at the root and at σ level 3 are intended: those nodes go straight to the next split. On the first two roots every 6-bit cube was certified at under 300 s (the slowest took 184 s). On root 3, 13 of the 64 cubes timed out at 300 s and were layer-split. Each split gave 51 depth-3 children at cap 600. The slowest certified child took 57 s.

Layer splits of root 3 (children / certified / open):

| σ6 cube | children | certified | open |
|---|---|---|---|
| `__1s0-2s1-4s1-5s0-7s1-8s0` | 51 | 51 | 0 |
| `__1s0-2s1-4s1-5s1-7s0-8s0` | 51 | 51 | 0 |
| `__1s0-2s1-4s1-5s1-7s0-8s1` | 51 | 51 | 0 |
| `__1s0-2s1-4s1-5s1-7s1-8s0` | 51 | 51 | 0 |
| `__1s1-2s0-4s0-5s1-7s0-8s1` | 51 | 51 | 0 |
| `__1s1-2s0-4s1-5s1-7s0-8s0` | 51 | 51 | 0 |
| `__1s1-2s0-4s1-5s1-7s0-8s1` | 51 | 10 | 41 |
| `__1s1-2s1-4s0-5s1-7s0-8s1` | 51 | 0 | 51 |
| `__1s1-2s1-4s0-5s1-7s1-8s0` | 51 | 0 | 51 |
| `__1s1-2s1-4s0-5s1-7s1-8s1` | 51 | 0 | 51 |
| `__1s1-2s1-4s1-5s0-7s1-8s0` | 51 | 0 | 51 |
| `__1s1-2s1-4s1-5s0-7s1-8s1` | 51 | 0 | 51 |
| `__1s1-2s1-4s1-5s1-7s0-8s1` | 51 | 0 | 51 |

The 347 open nodes (41 + 6 × 51) are depth-3 children that were never finished. They are not childless timeouts. The batch passed the slice deadline (15:27) because `close_tree.py` only checks the deadline between batches, and it was killed at END. The nodes still running at that time had written no records, so there is no `cake_lpr: none` record and nothing to re-check. No split record has `"children": 0`.

## Totals (stratum H3/two, 3 roots)

- 2 closed, 1 partial, 0 not reached.
- 575 records: 495 certified (every one has `c VERIFIED` and `s VERIFIED UNSAT`), 40 timeouts, 40 split records (27 σ, 13 layer).
- Solve 36,318 s and check 14,236 s (summed per node).

## SAT / rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none. There are no uncertified UNSAT records and no `cake_lpr: none` records; no `recheck.jsonl` was needed.
- Memory: with 3 jobs, used memory peaked at about 9 GB of 15 GB. There were no failures.
