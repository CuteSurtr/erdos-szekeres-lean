# C3W4 O09: W4_one.tsv shard 9 of 16

Task: `results/C3W4/TASK.md` at 3fd8a4d8 with V = O09, LIST = W4_one.tsv, j = 9, N = 16, SLICE = 2.5 h, H = 5.0 h.
One cloud VM (4 cores, 15 GB RAM, no swap; `env.txt`). Started at 11:31:16 UTC on 2026-10-24, with END at 16:16:16 UTC. The runner finished at 14:03:53 UTC, with all roots done.

## Tools and base CNF (`tools.txt`)

- C3U tools: a worktree of commit 95cafa93 at `/opt/c3u`, unmodified. `compose.py` was not run (per the task).
- CaDiCaL 3.0.1 c60730422e75, cake_lpr a36874a8 (its example gives `s VERIFIED UNSAT`), and drat-trim lrat-check 2e3b2dc with the E2 patch. In the sanity test, `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base: `gen_case.py 11 7 none` gives `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches). Every solve record has this `base_sha256`.
- Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat`, with no seeding. `close_tree` ran inside `timeout` until END, but the timeout never fired.

## Per root

Depth means the number of layers, and σ means the number of σ bits in the cube.

| row | root | stratum | status | certified | timeouts | splits | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| 9 | 0s0-3s0_4 | H6(3,0)/one | **closed** (open frontier 0, no childless timeout) | 64 at depth 2, σ6 | 9: root (cap 1) and 8 σ3 cubes (cap 1) | 9 σ splits | 2040.0 | 1779.7 |
| 25 | 0s0-4s1_2 | H6(4,1)/one | **closed** (open frontier 0, no childless timeout) | 214: 61 at depth 2, σ6 and 153 at depth 3, σ6 (cap 600) | 12: root, 8 σ3 cubes (cap 1), 3 σ6 cubes (cap 300) | 9 σ splits and 3 layer splits (51 children each) | 16623.5 | 6115.2 |

- Root 0s0-3s0_4 took 21.7 min of wall time, and its 6-bit cubes took 15–45 s each.
- Root 0s0-4s1_2 took 2 h 8 min. Its 6-bit cubes took about 130–300 s each, and three of them timed out at 300 s. Those three were layer-split, and all 153 of their children were certified.
- The three timed-out 6-bit cubes were:
  - `0s0-4s1_2__1s1-3s0-5s0-6s0-7s0-8s1`
  - `0s0-4s1_2__1s1-3s0-5s1-6s0-7s1-8s0`
  - `0s0-4s1_2__1s1-3s0-5s1-6s1-7s0-8s0`

## Totals (stratum: one)

- 2 of 2 roots closed, with 278 certified nodes. Every one has `lrat_check` "c VERIFIED" and `cake_lpr` "s VERIFIED UNSAT".
- There were 21 timeouts, all split, and no split record has `"children": 0`.
- Solve time was 18663.5 s and check time was 7894.9 s. The longest certified solve took 299.7 s and the longest check 59.3 s.
- There was no SAT, no proof rejection, no checker killed at END (so `recheck.jsonl` is not needed), and no memory problem (at most about 6 GB used, with no OOM in dmesg).
