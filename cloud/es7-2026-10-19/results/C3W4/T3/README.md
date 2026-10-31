# C3W4 T3: W4_two.tsv shard 3 of 4, σ-cube splitting

Task `results/C3W4/TASK.md` at 3fd8a4d8, V = T3, LIST = W4_two.tsv, j = 3, N = 4, SLICE = 1.0 h, H = 4.0 h.
One VM, 4 cores, 15 GB RAM (`env.txt`). Start 11:31:13 UTC 2026-10-24, END 15:16:13 UTC; the last root's
in-flight cubes finished at 15:21:42.

## Tools and base check (`tools.txt`)

- C3U tools: worktree of 95cafa93 at /opt/c3u, used unmodified. No `compose.py` was run.
- CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (example prints `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch.
  Sanity check passed: `3 0 0` on {1},{-1} is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 bf0e502e…dd6da (matches).

## Run

43 roots (rows ≡ 3 mod 4), none seeded. Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 300,300,600 --cadopts=--sat --split-singles`, one runner (`runner.sh`).
Every root either closed directly at 300 s or timed out and was σ-split once on 3 bits into 8 cubes, all certified at the first σ level.
No second σ level and no layer split was needed. All nodes sit at depth 2 (the root's layers). The σ column below counts certified nodes per σ level (σ0 = the root itself).

**31 closed, 0 partial, 12 not reached.** No SAT, no proof rejection, no `cake_lpr: none` record (so no `recheck.jsonl`), no split record with `"children": 0`, and no memory problem (no OOM kills; peak use was about 11 of 15 GB).
All 136 UNSAT records have cake_lpr `s VERIFIED UNSAT` and lrat-check accepting.

## Per root

| row | root | stratum | status | certified (depth:σ-level → n) | timeouts | childless timed-out | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| 3 | 0s0-3s1_1s1-9s1 | H6(3,1)/two | closed | 8 (σ1:8) | 1 | 0 | 1728 | 398 |
| 7 | 0s0-3s1_6s1-7s0 | H6(3,1)/two | closed | 8 (σ1:8) | 1 | 0 | 1928 | 424 |
| 11 | 0s0-4s1_1s1-3s0 | H6(4,1)/two | closed | 8 (σ1:8) | 1 | 0 | 1554 | 376 |
| 15 | 0s0-5s0_1s0-10s0 | H6(5,0)/two | closed | 8 (σ1:8) | 1 | 0 | 1000 | 372 |
| 19 | 0s0-5s0_1s0-6s1 | H6(5,0)/two | closed | 8 (σ1:8) | 1 | 0 | 740 | 300 |
| 23 | 0s0-5s0_2s0-6s1 | H6(5,0)/two | closed | 8 (σ1:8) | 1 | 0 | 852 | 332 |
| 27 | 0s0-2s0_3s1-5s0 | H6(2,0)/two | closed | 1 (σ0:1) | 0 | 0 | 106 | 35 |
| 31 | 0s0-2s0_3s1-8s1 | H6(2,0)/two | closed | 1 (σ0:1) | 0 | 0 | 109 | 38 |
| 35 | 0s0-3s1_4s1-7s0 | H6(3,1)/two | closed | 8 (σ1:8) | 1 | 0 | 1405 | 367 |
| 39 | 0s0-3s1_5s0-8s0 | H6(3,1)/two | closed | 1 (σ0:1) | 0 | 0 | 36 | 27 |
| 43 | 0s0-3s1_6s1-7s1 | H6(3,1)/two | closed | 1 (σ0:1) | 0 | 0 | 39 | 35 |
| 47 | 0s0-4s0_2s0-6s0 | H6(4,0)/two | closed | 1 (σ0:1) | 0 | 0 | 24 | 26 |
| 51 | 0s0-4s0_5s0-10s0 | H6(4,0)/two | closed | 1 (σ0:1) | 0 | 0 | 87 | 34 |
| 55 | 0s0-4s1_1s0-9s1 | H6(4,1)/two | closed | 1 (σ0:1) | 0 | 0 | 68 | 34 |
| 59 | 0s0-4s1_1s1-6s0 | H6(4,1)/two | closed | 8 (σ1:8) | 1 | 0 | 1023 | 334 |
| 63 | 0s0-4s1_2s0-10s1 | H6(4,1)/two | closed | 1 (σ0:1) | 0 | 0 | 60 | 28 |
| 67 | 0s0-4s1_2s0-6s1 | H6(4,1)/two | closed | 8 (σ1:8) | 1 | 0 | 1570 | 402 |
| 71 | 0s0-4s1_5s0-6s0 | H6(4,1)/two | closed | 1 (σ0:1) | 0 | 0 | 41 | 32 |
| 75 | 0s0-4s1_5s0-9s0 | H6(4,1)/two | closed | 1 (σ0:1) | 0 | 0 | 150 | 36 |
| 79 | 0s0-4s1_5s1-7s0 | H6(4,1)/two | closed | 8 (σ1:8) | 1 | 0 | 1656 | 366 |
| 83 | 0s0-4s1_6s0-9s0 | H6(4,1)/two | closed | 1 (σ0:1) | 0 | 0 | 36 | 35 |
| 87 | 0s0-4s1_6s1-8s1 | H6(4,1)/two | closed | 1 (σ0:1) | 0 | 0 | 38 | 32 |
| 91 | 0s0-5s0_1s0-8s0 | H6(5,0)/two | closed | 8 (σ1:8) | 1 | 0 | 762 | 322 |
| 95 | 0s0-5s0_1s1-10s0 | H6(5,0)/two | closed | 1 (σ0:1) | 0 | 0 | 26 | 30 |
| 99 | 0s0-5s0_2s0-7s0 | H6(5,0)/two | closed | 1 (σ0:1) | 0 | 0 | 106 | 36 |
| 103 | 0s0-5s0_2s0-9s0 | H6(5,0)/two | closed | 8 (σ1:8) | 1 | 0 | 770 | 308 |
| 107 | 0s0-5s0_6s0-7s1 | H6(5,0)/two | closed | 8 (σ1:8) | 1 | 0 | 745 | 303 |
| 111 | 0s0-5s0_6s1-7s0 | H6(5,0)/two | closed | 1 (σ0:1) | 0 | 0 | 271 | 48 |
| 115 | 0s0-5s0_6s1-9s0 | H6(5,0)/two | closed | 1 (σ0:1) | 0 | 0 | 252 | 45 |
| 119 | 0s0-5s1_1s0-10s0 | H6(5,1)/two | closed | 8 (σ1:8) | 1 | 0 | 1028 | 333 |
| 123 | 0s0-5s1_1s0-4s1 | H6(5,1)/two | closed | 8 (σ1:8) | 1 | 0 | 1077 | 322 |
| 127 | 0s0-5s1_1s0-8s0 | H6(5,1)/two | not reached | | | | | |
| 131 | 0s0-5s1_1s1-10s1 | H6(5,1)/two | not reached | | | | | |
| 135 | 0s0-5s1_1s1-3s1 | H6(5,1)/two | not reached | | | | | |
| 139 | 0s0-5s1_1s1-9s0 | H6(5,1)/two | not reached | | | | | |
| 143 | 0s0-5s1_2s0-3s0 | H6(5,1)/two | not reached | | | | | |
| 147 | 0s0-5s1_2s0-7s1 | H6(5,1)/two | not reached | | | | | |
| 151 | 0s0-5s1_2s1-3s0 | H6(5,1)/two | not reached | | | | | |
| 155 | 0s0-5s1_2s1-8s0 | H6(5,1)/two | not reached | | | | | |
| 159 | 0s0-5s1_6s0-10s1 | H6(5,1)/two | not reached | | | | | |
| 163 | 0s0-5s1_6s1-10s1 | H6(5,1)/two | not reached | | | | | |
| 167 | 0s0-5s1_6s1-9s0 | H6(5,1)/two | not reached | | | | | |
| 171 | 0s0-5s1_7s0-9s1 | H6(5,1)/two | not reached | | | | | |

| stratum | closed | partial | not reached | certified | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|
| H6(2,0)/two | 2 | 0 | 0 | 2 | 0 | 215 | 73 |
| H6(3,1)/two | 5 | 0 | 0 | 26 | 3 | 5136 | 1250 |
| H6(4,0)/two | 2 | 0 | 0 | 2 | 0 | 111 | 60 |
| H6(4,1)/two | 10 | 0 | 0 | 38 | 4 | 6197 | 1675 |
| H6(5,0)/two | 10 | 0 | 0 | 52 | 6 | 5522 | 2097 |
| H6(5,1)/two | 2 | 0 | 12 | 16 | 2 | 2105 | 655 |


Records: 166 in out.jsonl: 136 certified, 15 timeouts at 300 s (one per σ-split root), 15 σ-split records with 8 children each.
