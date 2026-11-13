# C3W4 O15: W4_one.tsv shard 15 of 16

Task: `results/C3W4/TASK.md` at 3fd8a4d8 with V = O15, LIST = W4_one.tsv, j = 15, N = 16, SLICE = 2.5, H = 5.0.
Start 2026-10-24 16:04:11 UTC, END 20:49:11 UTC. Machine: 4 cores, 15 GB RAM (`env.txt`).

## Tools and base CNF (`tools.txt`)
- C3U tools: worktree of 95cafa9307faef75cc584c08d44727b43c89c0bf, used unmodified; `compose.py` not run, as the task says.
- CaDiCaL c60730422e758ef1cebe7aeddf2dda31c996bf04 (3.0.1); cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (its example gives `s VERIFIED UNSAT`); lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with the E2 patch. Sanity check passed: `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF from `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat`, nothing seeded.

## Roots (`roots.tsv`)
| row | root | stratum | result |
|---|---|---|---|
| 15 | 0s0-2s1_5 | H6(2,1)/one | **partial**: open frontier 2805 (not counting the 3 jobs killed at END) |
| 31 | 0s0-5s0_7 | H6(5,0)/one | **not reached** |

Root 0s0-2s1_5, all records in `out.jsonl` (605 lines):
- Root at cap 1: timed out. Split into 8 cubes on 3 σ bits, each timed out at cap 1 and was split into 8 more. That gives 64 cubes on 6 σ bits.
- **All 64 six-bit cubes timed out at cap 300** (0 certified). Each one got the layer split into 51 children, 3264 children in all.
- Layer children (depth 1, 6 σ bits) at cap 600: **459 certified**, 0 timeouts, 2805 not yet run.
- Certified nodes by depth and σ level: depth 0 / 6 σ bits: 0; depth 1 / 6 σ bits: 459.
- Timeouts: 1 (root, cap 1) + 8 (3 σ bits, cap 1) + 64 (6 σ bits, cap 300) = 73. None of the 73 split records has `children: 0`.
- Solve time 34,139 s in total (19,200 s of it is the 64 timed-out cubes at 300 s each). Check time 15,343 s.

Totals for stratum H6(·,·)/one on this shard: 1 root partial, 1 not reached, 0 closed; 459 certified nodes.

## Notes
- No SAT. No proof rejection: all 459 UNSAT records have lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`, and there is no record with cake_lpr `none`, so `recheck.jsonl` is empty and not committed. No memory problem: at most about 9 GB of 15 GB used.
- Time limits: `close_tree.py` only checks `--hours` between frontier levels. So once the 3264-child level had been submitted, it ran past the 2.5 h slice (which ended at 18:37), and root 31 never started. At END (20:49:16) I killed the runner's process group, which held 2 cadical runs and 1 cake_lpr run. They left no records, so no `none` records exist and nothing needed re-checking.
- On this root the 6-bit σ cubes did not finish at 300 s, unlike the C3SIG2 pilots. The 51-way layer split of each cube does close quickly: about 10–90 s solving and about 30 s checking per child. About 2805 children × ~105 s / 3 jobs ≈ 27 more hours would be needed to finish it at this rate.
