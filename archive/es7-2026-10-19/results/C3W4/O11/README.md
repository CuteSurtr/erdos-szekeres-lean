# C3W4 O11: W4_one.tsv, shard 11 of 16

Task: `results/C3W4/TASK.md` at 3fd8a4d8, with V = O11, LIST = W4_one.tsv, j = 11, N = 16, SLICE = 2.5, H = 5.0.
One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:33 UTC on 2026-10-24, END 16:16:33 UTC. The runner finished at 14:05:07 UTC with both roots closed.

## Tools (`tools.txt`)

- C3U tools from a worktree of 95cafa93 at `/opt/c3u`, used unmodified. `compose.py` was not run, as the task says.
- CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (its example gives `s VERIFIED UNSAT`), and lrat-check 2e3b2dc with the E2 patch. Sanity check: the LRAT `3 0 0` on {1},{-1} is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF from `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).
- Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat`, slice 2.5 h, nothing seeded (`runner.sh`).
- The first launch failed straight away because `cadical` was not on PATH. No records were written. The runner was fixed (`export PATH=/opt/bin:$PATH`) and restarted at 11:35:37.

## Per root

| row | root | stratum | status | certified | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|
| 11 | 0s0-4s0_2 | H6(4,0)/one | closed (open frontier 0, no childless node) | 64: all at σ level 2 (6-bit cubes, depth 2, cap 300) | 9 at cap 1 (the root and its 8 3-bit cubes) | 4609 | 2388 |
| 27 | 0s0-4s1_7 | H6(4,1)/one | closed (open frontier 0, no childless node) | 164: 62 at σ level 2 (6-bit cubes, depth 2, cap 300) and 102 one layer below, after a layer split of 2 timed-out 6-bit cubes (depth 3, cap 600) | 9 at cap 1 and 2 at cap 300 | 14288 | 5010 |

Root 0s0-4s0_2 took 40 min and root 0s0-4s1_7 took 1 h 49 min.
- 6-bit cubes at cap 300: 126 certified. Solve time was 44, 135 and 289 s (min, median, max); check time was at most 57 s.
- Layer children at cap 600: 102 certified. Solve time was 4, 12 and 46 s (min, median, max); check time was at most 44 s.
- The two 6-bit cubes that timed out were `0s0-4s1_7__1s1-2s1-3s0-5s1-6s0-8s1` and `0s0-4s1_7__1s1-2s1-3s1-5s0-6s0-8s0`, with 51 layer children each.

## Totals

- Stratum H6(4,0)/one: 1 root, closed.
- Stratum H6(4,1)/one: 1 root, closed.
- Records: 228 certified, 20 split records, 0 split records with `"children": 0`.
- Every UNSAT record has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.
- No SAT, no proof rejection, no re-check needed (no `recheck.jsonl`), no memory problem (peak about 6 GB used).
- The largest proof was 468 MB. It was not committed.
