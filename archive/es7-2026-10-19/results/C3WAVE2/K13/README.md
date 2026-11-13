# C3WAVE2 K13: shard 13 of 40 (budget 1.5 h)

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`), 00:25 to 01:55 UTC on 2026-10-21.

## Tools and base CNF (`tools.txt`)
- C3-S tools: worktree of `132398c` (8dc27c3 before the author rewrite) at /opt/c3s, unmodified.
- CaDiCaL 3.0.1 (c6073042); cake_lpr a36874a8 (example prints `s VERIFIED UNSAT`);
  lrat-check 2e3b2dc + `lrat-check-E2.patch`. Sanity check passed: on {1},{-1}, LRAT `3 0 0` is rejected
  by both checkers, `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da` (matches).
- Roots: rows of `C3WAVE2/roots.tsv` with idx % 40 == 13: 34 roots (`roots.tsv`).
- Runner: `runner.sh` (the K00 runner with this machine's END = start + 1.5 h - 15 min), `--jobs 3 --caps 300,300,600
  --cadopts=--sat --split-singles --hours 0.17` per root.

## Result
Only the first root was reached. `close_tree.py` checks its `--hours` deadline only between waves, and
the depth-3/depth-4 wave of this root ran from 00:27 to past END (01:40), so the runner was
stopped by hand at 01:40 UTC. Results already written to `out.jsonl` are kept; the nodes that were in flight
were not recorded and will be re-solved on resume.

| root | status | certified (depth 3 / depth 4) | splits | solve s | check s |
|---|---|---|---|---|---|
| 0s0-1s1_4s1-7s0 (idx 13) | partial | 51 / 462 | 8 (root + 7 single-orbit pre-splits) | 4,240 | 8,166 |
| other 33 roots | not reached | – | – | – | – |

Details for 0s0-1s1_4s1-7s0: the root itself was UNKNOWN at the 300 s cap and split into 91 children.
7 of them (`_2 _3 _5 _6 _8 _9 _10`) are single-orbit and were pre-split into 66 children each, and all 462 of those
are certified (cap 600 s). Of the other 84 depth-3 children, 51 are certified (cap 300 s) and 33 are still open
(not yet solved). Largest solve 55.4 s, largest check 33.4 s. Every certified node is accepted by both
cake_lpr (`s VERIFIED UNSAT`) and lrat-check.

Totals: 513 certified nodes, 8 splits, 0 SAT, 0 proof rejections, no out-of-memory events (peak about 9 GB used).

Closed roots: none. Partial roots: 0s0-1s1_4s1-7s0. Not reached: the other 33 roots of `roots.tsv`.

`compose.txt`: 513 certified nodes, class not covered (as expected), 195 uncovered frontier nodes.
Files: `out.jsonl` (all records, used to resume), `driver_tail.log` (last 200 driver lines), `compose.txt`.
