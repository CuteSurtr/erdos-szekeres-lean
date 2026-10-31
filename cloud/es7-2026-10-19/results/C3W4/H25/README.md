# C3W4 H25: W4_H3.tsv shard 25 of 30

Task: `results/C3W4/TASK.md` at 3fd8a4d8 with V = H25, LIST = W4_H3.tsv, j = 25, N = 30, SLICE = 2.0, H = 5.0.
Start 2026-10-24 16:04:15 UTC, END 20:49:15 UTC (start + 5 h − 15 min). One machine: 4 cores, 15 GB RAM.

## Tools and base check (`tools.txt`)
- C3U tools: worktree of 95cafa93 at /opt/c3u, unmodified. No `compose.py` was run.
- CaDiCaL c6073042 (3.0.1). cake_lpr a36874a8 (its example gives `s VERIFIED UNSAT`). lrat-check 2e3b2dc with the E2 patch. Sanity test passed: `3 0 0` is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF from `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`. Both match.
- Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat`, slice 2.0 h. No seeded records.

## Runner and watchdogs
`runner.sh` is the H24 runner with this machine's start time. close_tree checks `--hours` only between waves. So root 0s0_2s1-4s0 was still in its cap-600 layer-split wave 17 min after its slice ended. I then added the H02 watchdogs, copied unchanged except for END: `slicedog.sh` and `enddog.sh`. They kill the close_tree main process first and then the solvers and checkers, so no record is written for a killed node. slicedog stopped root 2 at 19:03:45. Root 3 then got the remaining 1.758 h. enddog stopped root 3 at 20:48:36 (END − 40 s).

## Per root (`summary.txt`)
| root | stratum | status | certified nodes (depth, σ levels) | timeouts | solve s | check s |
|---|---|---|---|---|---|---|
| 0s0_1s1-2s1 | H3/two | **closed**: open frontier 0, no childless split | 64 at (2, 2): all 64 6-bit cubes, cap 300 | 9 (the cap-1 root and the 8 cap-1 level-1 nodes) | 4865 | 2152 |
| 0s0_2s1-4s0 | H3/two | **partial**: open frontier 2908 | 5 at (2, 2) (cubes); 101 at (3, 2) (layer children of cubes, cap 600) | 68: the 9 cap-1 nodes, plus 59 of 64 cubes at cap 300. No cap-600 timeout | 21394 | 2642 |
| 0s0_4 | H3/one | **partial**: open frontier 4324 | 0 | 69: the 9 cap-1 nodes, plus all 60 cubes that ran (cap 300). 4 cubes not run | 18015 | 0 |

Root 1 ran 16:06:53–16:46:49. Root 2 ran 16:46:49–19:03:45 (killed by slicedog). Root 3 ran 19:03:45–20:48:36 (killed by enddog). Every root was reached.

No split record has `"children": 0`. Root 2's frontier is its 59 layer-split cubes (51 children each) minus the 101 certified children. Root 3's frontier is its 60 layer-split cubes plus the 4 cubes that were not run.

## Totals per stratum
- H3/two: 2 roots, 1 closed and 1 partial. 170 certified nodes. Solve 26259 s, check 4794 s.
- H3/one: 1 root, partial. 0 certified. Solve 18015 s.

## Problems
- SAT: none.
- `PROOF NOT ACCEPTED`: none.
- Certified records with cake_lpr `none`: none. Every certified record has `s VERIFIED UNSAT` and `c VERIFIED`. Nodes killed at the slice end or at END left no record, so nothing needed a re-check and there is no `recheck.jsonl`.
- Memory: no problems. Peak use was about 9 GB of 15 GB.
