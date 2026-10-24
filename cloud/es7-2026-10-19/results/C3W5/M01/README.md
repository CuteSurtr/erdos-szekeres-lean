# C3W5 M01: shard 1 of 10 of W5_two.tsv

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Session start 16:12:25 UTC on 2026-10-24, END would have been 18:57:25 UTC (start + 3 h − 15 min); the runner started at 16:15:16 and finished all 8 roots at 17:08:12 UTC. TASK.md commit 265d8921.

## Tools (`tools.txt`)

- C3U2 tools: worktree of commit cad4e050 at `/opt/c3u2`, `TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools`, unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1, c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8 (`make cake_lpr`; its example prints `s VERIFIED UNSAT`); lrat-check drat-trim 2e3b2dc with the E2 patch. Sanity check passed: on {1},{-1}, `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).

## Run

- Roots: rows of `C3W5/lists/W5_two.tsv` with row ≡ 1 (mod 10): 8 roots (`roots.tsv`).
- Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 300,300,600 --cadopts=--sat --split-singles`, slice 1.0 h (`runner.sh`, started with `setsid nohup`).
- Seeding: 6 records, all for root `0s0-4s1_6s1-8s0`, all from `C3W4/T2/out.jsonl`: its σ split record (bits 1,2,3, 8 children) and 5 certified σ cubes. No other C3W4 record matched my roots; there are no `recheck*.jsonl` files in C3W4. `out.jsonl` here holds only the 43 new records (lines 7 onward of the run's out file).

## Per root

Every root's `open_frontier` is 0 with `unsplittable` 0. No split record has 0 children, and no node timed out without children.

| row | root | stratum | status | certified (new) | timeouts | splits | solve s | check s |
|-----|------|---------|--------|-----------------|----------|--------|---------|---------|
| 1 | 0s0-4s1_6s1-8s0 | H6(4,1)/two | **closed** | 3 σ cubes (3 bits); +5 seeded cubes | 0 (new) | seeded root σ split (8) | 584 | 155 |
| 11 | 0s0-3s1_5s0-6s0 | H6(3,1)/two | **closed** | root | 0 | 0 | 33 | 37 |
| 21 | 0s0-4s1_5s1-6s0 | H6(4,1)/two | **closed** | 8 σ cubes (3 bits) | 1 (root, 300 s) | root σ split, 8 | 1564 | 368 |
| 31 | 0s0-5s0_7s0-8s0 | H6(5,0)/two | **closed** | root | 0 | 0 | 9 | 23 |
| 41 | 0s0-5s1_2s1-9s1 | H6(5,1)/two | **closed** | 8 σ cubes (3 bits) | 1 (root, 300 s) | root σ split, 8 | 1175 | 336 |
| 51 | 0s0-5s0_6s1-10s0 | H6(5,0)/two | **closed** | root | 0 | 0 | 144 | 43 |
| 61 | 0s0-5s1_2s1-10s1 | H6(5,1)/two | **closed** | 8 σ cubes (3 bits) | 1 (root, 300 s) | root σ split, 8 | 1391 | 330 |
| 71 | 0s0-5s1_2s0-3s0 | H6(5,1)/two | **closed** | root | 0 | 0 | 24 | 28 |

All σ cubes are at the first σ level, depth 2 (layer depth of the root). Solve and check times are summed per node over the new records only. They are not wall-clock: three jobs shared the 4 cores.

## Totals per stratum

- H6(3,1)/two: 1 root, 1 closed (1 certified node).
- H6(4,1)/two: 2 roots, 2 closed (11 new certified nodes, 1 timeout).
- H6(5,0)/two: 2 roots, 2 closed (2 certified nodes).
- H6(5,1)/two: 3 roots, 3 closed (17 certified nodes, 2 timeouts).
- All: 8 of 8 closed. 31 new certified nodes and 3 new σ split records, 3 timeouts (all at roots that were then σ-split), 4924 solve s, 1320 check s.

No SAT answer, no proof rejection (lrat-check and cake_lpr accepted every UNSAT proof; no checker returned `none`), no memory problem (peak use was about 9 GB of 15).
