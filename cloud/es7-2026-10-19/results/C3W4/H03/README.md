# C3W4 H03: wave 4, list W4_H3.tsv, shard 3 of 30

Task `results/C3W4/TASK.md` at 3fd8a4d8, V = H03, j = 3, N = 30, SLICE = 2.0 h, H = 5.0 h.
One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:26 UTC, END 16:16:26 + the README.

## Tools and base CNF (`tools.txt`)
- C3U tools: worktree of 95cafa93 at /opt/c3u, unmodified. No `compose.py` was run.
- CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (example: `s VERIFIED UNSAT`), lrat-check 2e3b2dc + E2 patch;
  sanity check passed (`3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both).
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da` (matches).
- Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat`, no seeded records.

## Per root (stratum H3/two for all four)
Depth = number of layers (roots at depth 2); σ level 2 = the 64 cubes on 6 σ bits. The cap-1 timeouts
(root + 8 first-level σ nodes = 9 per root) are the designed pass-through, not real timeouts.

| row | root | status | certified (depth 2, σ2) | certified (depth 3, σ2) | cap-300 timeouts (→ layer split) | solve s | check s |
|---|---|---|---|---|---|---|---|
| 3 | 0s0_1s0-4s0 | **closed** (open_frontier 0) | 64 | 0 | 0 | 4963 | 2304 |
| 33 | 0s0_1s1-7s0 | **closed** (open_frontier 0) | 60 | 204 | 4 | 15641 | 6950 |
| 63 | 0s0_2s1-8s0 | **closed** (open_frontier 0) | 63 | 51 | 1 | 11791 | 3487 |
| 93 | 0s0_4s1-5s1 | **partial** (stopped at END, 9 of 64 σ cubes not finished) | 55 | 0 | 0 | 4055 | 1781 |

Wall time: root 3 42 min, root 33 2 h 09 min, root 63 1 h 27 min, root 93 ~34 min until stopped.
All split records have 8 children (no `"children": 0` record). Every UNSATISFIABLE record is certified
(lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`); no record with cake_lpr `none`.
Root 93 was stopped by hand after END while close_tree was still finishing in-flight jobs; the killed
jobs left no record, so its unfinished cubes are simply absent (open).

## Totals (stratum H3/two)
3 closed, 1 partial, 0 not reached; 497 certified nodes; 5 cap-300 timeouts, all layer-split and closed;
solve 36450 s, check 14522 s.

## Problems
No SAT, no proof rejection, no memory problem (peak ~9 GB used of 15).
