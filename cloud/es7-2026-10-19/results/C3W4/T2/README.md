# C3W4 / T2: wave 4, list W4_two.tsv, shard 2 of 4

**Result: 20 of my 43 roots closed, 1 partial (`0s0-4s1_6s1-8s0`, 3 σ-cubes open), 22 not reached. No SAT. No proof rejection. No memory problem.**

## Setup
- One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-24 11:31:29 UTC; END = start + 4 h − 15 min = 15:16:29 UTC. Task: `results/C3W4/TASK.md` at 3fd8a4d8.
- Tools (`tools.txt`): C3U tools from a worktree of 95cafa93 at /opt/c3u, unmodified. CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8 (bundled example gives `s VERIFIED UNSAT`), and lrat-check 2e3b2dc with the E2 patch. Sanity check: `3 0 0` on {1},{-1} is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF from `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).
- Roots: rows of W4_two.tsv with row ≡ 2 (mod 4), 43 roots (`roots.tsv`). No records were seeded: every root started fresh.
- Options: `close_tree.py … --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 300,300,600 --cadopts=--sat --split-singles --hours min(1.0, left)`. Runner: `runner.sh`.
- compose.py was not run, as the task says.

## Per root
Depth is the number of layers. σ level s is the number of 3-bit σ splits above the node. Solve and check seconds are summed per node, not wall clock (3 jobs on 4 cores).

| row | root | stratum | status | certified (depth/σ level) | timeouts | splits | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| 2 | 0s0-3s1_1s1-5s0 | H6(3,1)/two | closed | d2/s1: 8 | 1 | sigma 1 | 1405 | 339 |
| 6 | 0s0-3s1_6s0-7s1 | H6(3,1)/two | closed | d2/s1: 8 | 1 | sigma 1 | 2054 | 367 |
| 10 | 0s0-4s0_1s1-2s0 | H6(4,0)/two | closed | d2/s1: 8 | 1 | sigma 1 | 880 | 339 |
| 14 | 0s0-4s1_5s1-8s0 | H6(4,1)/two | closed | d2/s1: 8 | 1 | sigma 1 | 1446 | 310 |
| 18 | 0s0-5s0_1s0-4s1 | H6(5,0)/two | closed | d2/s1: 8 | 1 | sigma 1 | 856 | 294 |
| 22 | 0s0-5s0_2s0-3s1 | H6(5,0)/two | closed | d2/s1: 8 | 1 | sigma 1 | 1026 | 322 |
| 26 | 0s0-2s0_3s1-4s0 | H6(2,0)/two | closed | d2/s0: 1 | 0 | - | 135 | 35 |
| 30 | 0s0-2s0_3s1-8s0 | H6(2,0)/two | closed | d2/s0: 1 | 0 | - | 60 | 31 |
| 34 | 0s0-3s1_4s1-6s0 | H6(3,1)/two | closed | d2/s1: 8 | 1 | sigma 1 | 1788 | 356 |
| 38 | 0s0-3s1_5s0-7s1 | H6(3,1)/two | closed | d2/s1: 7, d2/s2: 8 | 2 | sigma 2 | 2352 | 564 |
| 42 | 0s0-3s1_6s0-8s1 | H6(3,1)/two | closed | d2/s1: 8 | 1 | sigma 1 | 1982 | 348 |
| 46 | 0s0-4s0_2s0-5s1 | H6(4,0)/two | closed | d2/s1: 8 | 1 | sigma 1 | 952 | 282 |
| 50 | 0s0-4s0_2s0-7s1 | H6(4,0)/two | closed | d2/s0: 1 | 0 | - | 175 | 34 |
| 54 | 0s0-4s1_1s0-7s1 | H6(4,1)/two | closed | d2/s1: 8 | 1 | sigma 1 | 783 | 272 |
| 58 | 0s0-4s1_1s1-2s1 | H6(4,1)/two | closed | d2/s0: 1 | 0 | - | 37 | 23 |
| 62 | 0s0-4s1_2s0-10s0 | H6(4,1)/two | closed | d2/s1: 8 | 1 | sigma 1 | 1079 | 288 |
| 66 | 0s0-4s1_2s0-6s0 | H6(4,1)/two | closed | d2/s0: 1 | 0 | - | 35 | 22 |
| 70 | 0s0-4s1_5s0-10s0 | H6(4,1)/two | closed | d2/s0: 1 | 0 | - | 237 | 37 |
| 74 | 0s0-4s1_5s0-8s1 | H6(4,1)/two | closed | d2/s1: 8 | 1 | sigma 1 | 1500 | 319 |
| 78 | 0s0-4s1_5s1-6s1 | H6(4,1)/two | closed | d2/s0: 1 | 0 | - | 38 | 23 |
| 82 | 0s0-4s1_6s0-8s1 | H6(4,1)/two | closed | d2/s1: 8 | 1 | sigma 1 | 1959 | 381 |
| 86 | 0s0-4s1_6s1-8s0 | H6(4,1)/two | partial (open frontier 3) | d2/s1: 5 | 1 | sigma 1 | 1040 | 204 |
| 90 | 0s0-4s1_7s0-8s1 | H6(4,1)/two | not reached | - | 0 | - | - | - |
| 94 | 0s0-5s0_1s0-9s1 | H6(5,0)/two | not reached | - | 0 | - | - | - |
| 98 | 0s0-5s0_2s0-6s0 | H6(5,0)/two | not reached | - | 0 | - | - | - |
| 102 | 0s0-5s0_2s0-8s1 | H6(5,0)/two | not reached | - | 0 | - | - | - |
| 106 | 0s0-5s0_2s1-10s1 | H6(5,0)/two | not reached | - | 0 | - | - | - |
| 110 | 0s0-5s0_6s1-10s0 | H6(5,0)/two | not reached | - | 0 | - | - | - |
| 114 | 0s0-5s0_6s1-8s1 | H6(5,0)/two | not reached | - | 0 | - | - | - |
| 118 | 0s0-5s0_7s0-8s1 | H6(5,0)/two | not reached | - | 0 | - | - | - |
| 122 | 0s0-5s1_1s0-3s1 | H6(5,1)/two | not reached | - | 0 | - | - | - |
| 126 | 0s0-5s1_1s0-7s0 | H6(5,1)/two | not reached | - | 0 | - | - | - |
| 130 | 0s0-5s1_1s1-10s0 | H6(5,1)/two | not reached | - | 0 | - | - | - |
| 134 | 0s0-5s1_1s1-3s0 | H6(5,1)/two | not reached | - | 0 | - | - | - |
| 138 | 0s0-5s1_1s1-8s1 | H6(5,1)/two | not reached | - | 0 | - | - | - |
| 142 | 0s0-5s1_2s0-10s1 | H6(5,1)/two | not reached | - | 0 | - | - | - |
| 146 | 0s0-5s1_2s0-7s0 | H6(5,1)/two | not reached | - | 0 | - | - | - |
| 150 | 0s0-5s1_2s1-10s1 | H6(5,1)/two | not reached | - | 0 | - | - | - |
| 154 | 0s0-5s1_2s1-7s1 | H6(5,1)/two | not reached | - | 0 | - | - | - |
| 158 | 0s0-5s1_6s0-10s0 | H6(5,1)/two | not reached | - | 0 | - | - | - |
| 162 | 0s0-5s1_6s0-9s1 | H6(5,1)/two | not reached | - | 0 | - | - | - |
| 166 | 0s0-5s1_6s1-8s1 | H6(5,1)/two | not reached | - | 0 | - | - | - |
| 170 | 0s0-5s1_7s0-8s1 | H6(5,1)/two | not reached | - | 0 | - | - | - |
Every closed root has `open_frontier` 0 in the driver log and no split record with `"children": 0` (there are none in the whole file). Row 38 needed a second σ level: 1 of its 8 first-level cubes timed out and was σ-split again, and all 8 second-level cubes were certified. No layer split was needed anywhere.

**Partial:** `0s0-4s1_6s1-8s0` (row 86). Its slice started at 15:09:31 with 0.116 h left. The root timed out at 300 s and was σ-split on bits [1,2,3]. Five cubes were certified (`1s0-2s0-3s0`, `1s0-2s0-3s1`, `1s0-2s1-3s0`, `1s1-2s0-3s0`, `1s0-2s1-3s1`). close_tree finishes a batch it has already submitted, even after its deadline, so I stopped it at about 15:22 to leave time for the README. Three cubes are still open: `1s1-2s0-3s1`, `1s1-2s1-3s0` and `1s1-2s1-3s1`. Their solves were killed before they wrote any record, so no checker was cut off and nothing needs a re-check.

**Not reached:** rows 90–170 of `roots.tsv`: 22 roots, 13 of them in stratum H6(5,1).

## Totals per stratum
| stratum | roots | closed | partial | not reached | certified | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| H6(3,1)/two | 5 | 5 | 0 | 0 | 47 | 6 | 9581 | 1973 |
| H6(4,0)/two | 3 | 3 | 0 | 0 | 17 | 2 | 2007 | 654 |
| H6(4,1)/two | 11 | 9 | 1 | 1 | 49 | 6 | 8154 | 1879 |
| H6(5,0)/two | 9 | 2 | 0 | 7 | 16 | 2 | 1882 | 616 |
| H6(2,0)/two | 2 | 2 | 0 | 0 | 2 | 0 | 195 | 65 |
| H6(5,1)/two | 13 | 0 | 0 | 13 | 0 | 0 | 0 | 0 |

out.jsonl holds 163 records: 120 certified nodes (each with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`), 16 timeouts at 300 s and 16 σ-split records. None has cake_lpr `none`.

## SAT / rejections / memory
- SAT: none.
- PROOF NOT ACCEPTED: none, so no `recheck.jsonl`.
- Memory: peak use about 9 GB of 15 GB, with no failure.
- Incident: at the stop, my `pkill -f close_tree.py` also matched and killed my own waiting shell. close_tree kept running about 2 more minutes, which is how it certified a fifth cube, and was then killed by PID. This affected timing only.

## Files
`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl`, `driver.log.tail`, `README.md`.
