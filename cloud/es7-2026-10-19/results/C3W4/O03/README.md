# C3W4 O03: W4_one.tsv, shard 3 of 16

Task: `results/C3W4/TASK.md` at 3fd8a4d8, with V = O03, LIST = W4_one.tsv, j = 3, N = 16, SLICE = 2.5 h, H = 5 h.
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:22 UTC on 2026-10-24, END 16:16:22 UTC.

## Tools (`tools.txt`)

- C3U tools: worktree of 95cafa93 at `/opt/c3u`, used unmodified. No `compose.py` was run.
- CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (example: `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch.
  Sanity check: `3 0 0` on {1},{-1} is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF from `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`, which matches.

## Run

There was one runner (`runner.sh`) with `close_tree.py … --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat`. Nothing was seeded, so every root started fresh. Roots are listed in `roots.tsv`, and all three are in stratum `one`.

Depth: each root is at layer depth 2, and a layer split below a 6-bit σ cube gives depth 3. σ level is the number of 3-bit σ splits on the path (0, 1 or 2).

| root | stratum | result | certified (depth, σ level) | timeouts | solve s | check s |
|---|---|---|---|---|---|---|
| 0s0-1s1_6 | H6(1,1)/one | **closed**: open frontier 0, no childless split | 59 at (2, σ2) and 255 at (3, σ2): 314 | 1 root and 8 σ1 nodes at cap 1 (by design); 5 of 64 σ2 cubes at 300 s, each layer-split and fully closed at depth 3 | 18661 | 9414 |
| 0s0-3s1_6 | H6(3,1)/one | **closed**: open frontier 0, no childless split | 64 at (2, σ2): all 64 cubes | only the cap-1 nodes (9) | 12405 | 2800 |
| 0s0-5s1_6 | H6(5,1)/one | **partial**: cut at END | 33 at (2, σ2) | only the cap-1 nodes (9); 31 σ2 cubes have no record | 4922 | 1328 |

Root 0s0-5s1_6 got only 0.615 h because of the time left before END. `close_tree.py` checks its deadline only between generations, so at END (16:16:22) I killed the runner's process group while its 64-cube generation was still running. Its open frontier is the 31 σ2 cubes `0s0-5s1_6__…` that have no record in `out.jsonl`. `close_tree.py` did not get to print `open_frontier` for this root.

The first root's slice also ran past 2.5 h (11:34:49 to 14:13:56), for the same reason: the generation that was running was allowed to finish.

## Totals (stratum `one`)

- 2 roots closed and 1 partial. Every root was reached.
- 411 certified nodes. Each has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`, and no record has cake_lpr `none`.
- 475 records in `out.jsonl`, with no split record that has `"children": 0`.

## Incidents

- No SAT and no proof rejection, so `recheck.jsonl` is empty and not committed.
- No memory problems: at least 6 GB was available throughout.
- Several pushes needed retries because the branch was busy. Every push reached es7-cloud, and the fallback branch was not used.
