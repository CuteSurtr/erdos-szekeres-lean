# C3W4 O10: W4_one.tsv, shard 10 of 16

Task: `results/C3W4/TASK.md` at 3fd8a4d8, with V = O10, LIST = W4_one.tsv, j = 10, N = 16, SLICE = 2.5, H = 5.0.
Ran on one cloud VM (4 cores, 15 GB RAM, no swap; `env.txt`). Start 11:31:17 UTC, END 16:16:17 UTC (2026-10-24).

## Tools and base CNF (`tools.txt`)
- C3U tools: worktree of 95cafa93 at `/opt/c3u`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (example: `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch.
  Sanity check passed: LRAT `3 0 0` on {1},{-1} rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da`, matches.

## Run
One runner (`runner.sh`), `close_tree.py ... --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours S`, S = min(2.5, hours left).
No records were seeded: both roots started fresh. Roots (`roots.tsv`): rows 10 and 26 of W4_one.tsv.

close_tree only checks `--hours` between rounds, so root 0s0-4s1_5 kept going past its 2.5 h slice (14:32) in its
last round (the 918 layer-split children of 18 cubes). I killed it at END (16:16:17). Killed checkers and solvers
write no record, so there are no `cake_lpr: none` records and nothing needed re-checking. Because of the kill,
the driver log has no `open_frontier` line for this root; I computed the open frontier from `out.jsonl` with the
same expand logic close_tree uses.

## Per root
Depth = number of layers (roots are at depth 2); σ level = number of 3-bit σ splits on the path.

| root | stratum | status | certified (depth, σ level) | timeouts | solve s | check s |
|---|---|---|---|---|---|---|
| 0s0-3s0_6 (row 10) | H6(3,0)/one | **closed** (open frontier 0, no childless split) | 64 at (2, 2) | 9 at cap 1 (root and 8 first-level cubes, by design) | 2,889 | 2,113 |
| 0s0-4s1_5 (row 26) | H6(4,1)/one | **partial**, open frontier 241 | 46 at (2, 2); 677 at (3, 2) | 9 at cap 1 (by design); 18 of the 64 6-bit cubes at cap 300; none at cap 600 | 28,748 | 15,977 |

0s0-3s0_6 closed in 29 minutes: all 64 6-bit cubes certified at cap 300 (solve 19–95 s, mean 45 s).

0s0-4s1_5: 46 of the 64 6-bit cubes certified at cap 300 (solve 203–290 s, close to the cap). The other 18 timed out
and were layer-split into 51 children each (918 children, cap 600). 677 children are certified (solve 3–60 s, mean 17 s),
none timed out. Per cube: 13 of the 18 are fully closed, cube `1s1-2s1-3s0-6s0-7s0-8s1` has 14 of 51 children certified, and
4 cubes (`1s1-2s1-3s0-6s0-7s1-8s1`, `1s1-2s1-3s0-6s1-7s0-8s1`, `1s1-2s1-3s0-6s1-7s1-8s1`, `1s1-2s1-3s1-6s0-7s0-8s0`)
were not reached. So 59 of 64 cubes are closed; the open frontier is 37 + 4 × 51 = 241 unattempted depth-3 nodes,
which look easy (no layer-split child came close to the 600 s cap).

## Totals (stratum one, both roots)
- 787 certified nodes (64 + 723); every one has `lrat_check: c VERIFIED` and `cake_lpr: s VERIFIED UNSAT`.
- 36 timeouts: 18 by design at cap 1, 18 at cap 300; 0 at cap 600.
- 27 split records (9 σ splits from cap-1 timeouts per root, 18 layer splits), none with `"children": 0`.
- Solve 31,637 s, check 18,090 s.

## Problems
- No SAT answer, no proof rejection, no `cake_lpr: none` record, no childless timed-out node.
- No memory problem: used memory peaked around 9 GB of 15 GB (largest proof 455 MB).

## Files
`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all 859 records, none seeded), `driver.log.tail`.
