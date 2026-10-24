# C3W4 H01: W4_H3.tsv, shard 1 of 30, slice 2.0 h, budget 5 h

Task: `results/C3W4/TASK.md` at 3fd8a4d8. One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:08 UTC, END 16:16:08 UTC (2026-10-24).

## Tools and base check (`tools.txt`)
- C3U tools: worktree of 95cafa93 at /opt/c3u, unmodified. `compose.py` was not run, as the task says.
- CaDiCaL 3.0.1 c60730422e, cake_lpr a36874a8 (bundled example: `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch. Sanity test passed: `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 bf0e502e…6da (matches).

## Run
`runner.sh` ran `close_tree.py … R --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours S` once per root, with S = min(2.0, h left). Nothing was seeded. close_tree checks its deadline only between frontier levels, so root 0s0_1s1-6s0 ran its last (layer) level past its 2 h slice and ended at 16:04. Root 0s0_2s1-7s0 then started with 0.195 h. I killed it at END (16:16:11) while its 6-bit cube level was still running.

## Per root (stratum H3/two for all)
| row | root | status | certified (depth, σ level) | timeouts | splits (σ / layer) | solve s | check s |
|---|---|---|---|---|---|---|---|
| 1 | 0s0_1s0-10s1 | **closed** (open_frontier 0, no childless split) | 64 at (2, σ2) | 9 (cap 1 only) | 9 / 0 | 6661 | 2229 |
| 31 | 0s0_1s1-6s0 | **closed** (open_frontier 0, no childless split) | 53 at (2, σ2), 561 at (3, σ2) | 20 (9 at cap 1, 11 6-bit cubes at 300 s) | 9 / 11 (51 children each) | 25042 | 13899 |
| 61 | 0s0_2s1-7s0 | **partial** (killed at END) | 7 at (2, σ2) | 12 (9 at cap 1, 3 cubes at 300 s) | 9 / 3 (51 children each) | 1858 | 284 |
| 91 | 0s0_4s0-7s1 | not reached | – | – | – | – | – |

Root 0s0_2s1-7s0 open frontier: 53 of its 64 6-bit cubes have no record, 153 layer children of the 3 timed-out cubes are unsolved, and cube `__1s0-3s0-4s1-5s1-6s1-8s1` is in `recheck.jsonl` (see below). Its records stay valid for a later composition.

Totals (stratum H3/two): 2 closed, 1 partial, 1 not reached; 685 certified nodes; 41 timeouts (27 by design at cap 1); solve 33561 s, check 16412 s.

## Incidents
- SAT: none.
- Proof rejections: none. One node, `0s0_2s1-7s0__1s0-3s0-4s1-5s1-6s1-8s1`, got UNSAT with lrat-check `c VERIFIED`, but cake_lpr was killed at END, so cake_lpr is `none` and the node is not certified. Its `--jobs 1` re-check is reported below.
- Memory: no problem (at least 3 GB free throughout, no OOM).
- No `"children": 0` split records.
