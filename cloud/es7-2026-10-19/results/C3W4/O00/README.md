# C3W4 O00: W4_one.tsv shard 0 of 16 (task commit 3fd8a4d8)

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:23 UTC on 2026-10-24, END 16:16:23 UTC. The runner finished all roots at 15:21:18.

## Tools (`tools.txt`)
- C3U tools: worktree of commit 95cafa93 at /opt/c3u, used unmodified.
- CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8 (example prints `s VERIFIED UNSAT`), and lrat-check 2e3b2dc with the E2 patch. In the sanity test, both checkers reject `3 0 0` and accept `3 0 1 2 0`.
- Base CNF from `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6dd6da` (matches).
- Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat`, slice 2.5 h (`runner.sh`). No records were seeded. `compose.py` was not run, as the task says.

## Per root
Depth is the number of layers. The σ level is the number of 3-bit σ splits on the path. Every certified record has both `c VERIFIED` (lrat-check) and `s VERIFIED UNSAT` (cake_lpr).

| root | stratum | status | certified (depth 2, σ2) | certified (depth 3, σ2) | timeouts | solve s | check s | wall |
|---|---|---|---|---|---|---|---|---|
| 0s0-1s1_3 | H6(1,1)/one | closed | 63 | 51 | 9 at cap 1 (by design) + 1 at cap 300 | 14704 | 4415 | 11:33:58–13:22:41 |
| 0s0-3s1_1 | H6(3,1)/one | closed | 64 | 0 | 9 at cap 1 (by design) | 12013 | 2809 | 13:22:41–14:47:13 |
| 0s0-5s0_8 | H6(5,0)/one | closed | 64 | 0 | 9 at cap 1 (by design) | 3641 | 2275 | 14:47:13–15:21:18 |

- Every root has `open_frontier` 0, and no split record has `"children": 0`.
- On 0s0-1s1_3, one 6-bit cube timed out at cap 300: `0s0-1s1_3__2s0-4s1-5s1-6s1-7s1-8s1`. Its layer split gave 51 children, and all 51 were certified at cap 600.
- The slowest certified cube took 279 s to solve.

## Totals (stratum: one)
- 3 of 3 roots closed.
- 242 certified nodes: 191 σ-level-2 cubes and 51 layer-split children.
- 28 timeouts: 27 by design at cap 1, plus 1 at cap 300 that was then split.
- 30,358 solve-seconds and 9,499 check-seconds.

There were no SAT answers, no proof rejections (so `recheck.jsonl` is empty and not committed), no checker killed at END, and no memory problems (at least 9 GB was always available).
