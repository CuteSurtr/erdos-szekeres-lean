# C3W5 M03: W5_two.tsv shard 3 of 10 (rows ≡ 3 mod 10), 8 roots

Task: `results/C3W5/TASK.md` at 265d8921, V = M03, LIST = W5_two.tsv, j = 3, N = 10, SLICE = 1.0 h, H = 3.0 h.
Start 16:11:36 UTC, END 18:56:36 UTC; runner 16:15:08 to END. Machine: 4 cores, 15 GB (env.txt); peak memory use ~2 GB, no memory problem.

## Tools and base CNF (tools.txt)
- C3U2 tools: worktree of cad4e050, `results/C3U2/tools`, unmodified; compose.py not run.
- CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8 (example: `s VERIFIED UNSAT`), lrat-check 2e3b2dc + E2 patch (sanity: `3 0 0` rejected by both, `3 0 1 2 0` accepted by both).
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 bf0e502e…dd6da: matches.
- Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 300,300,600 --cadopts=--sat --split-singles`.
- Seeding: 0 records. No record in `results/C3W4/*/out.jsonl` or `recheck*.jsonl` has node R, R_* or R__* for any of the 8 roots (all "not reached in C3W4"). So out.jsonl holds all 173 new records.

## Results
No SAT. No PROOF NOT ACCEPTED. Every UNSAT record is certified by both cake_lpr (`s VERIFIED UNSAT`) and lrat-check (`c VERIFIED`), so no recheck was needed and there is no recheck.jsonl. There is no split record with `children: 0`, and close_tree reported `unsplittable: 0` for every root it finished.

Certified counts are by depth (d = layer-split depth below the σ cube) and σ level (s0 = the root itself, s1 = 3-bit cube, s2 = 6-bit cube). Timeouts are UNKNOWN records. Times are the sums of solve_s and check_s.

| row | root | stratum | status | certified | by d/σ | timeouts | splits | solve s | check s | notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 0s0-5s1_2s0-9s0 | H6(5,1)/two | closed | 15 | {'d0/s1': 7, 'd0/s2': 8} | 2 | 2 | 2065 | 848 |    |
| 13 | 0s0-4s0_2s0-5s0 | H6(4,0)/two | closed | 1 | {'d0/s0': 1} | 0 | 0 | 49 | 48 |    |
| 23 | 0s0-4s1_6s1-7s1 | H6(4,1)/two | closed | 1 | {'d0/s0': 1} | 0 | 0 | 87 | 62 |    |
| 33 | 0s0-5s1_1s0-6s1 | H6(5,1)/two | closed | 22 | {'d0/s1': 6, 'd0/s2': 16} | 3 | 3 | 2771 | 1176 |    |
| 43 | 0s0-5s1_6s1-8s0 | H6(5,1)/two | closed | 50 | {'d0/s1': 2, 'd0/s2': 48} | 7 | 7 | 5665 | 2364 |    |
| 53 | 0s0-5s0_7s0-8s1 | H6(5,0)/two | closed | 8 | {'d0/s1': 8} | 1 | 1 | 1189 | 427 |    |
| 63 | 0s0-5s1_6s0-10s0 | H6(5,1)/two | closed | 1 | {'d0/s0': 1} | 0 | 0 | 206 | 47 |    |
| 73 | 0s0-5s1_2s1-3s0 | H6(5,1)/two | partial (cut at END, no final report) | 33 | {'d0/s1': 1, 'd0/s2': 32} | 8 | 8 | 4594 | 1591 |    |

Root 73 `0s0-5s1_2s1-3s0` is **partial**. Its slice was cut at END, and the runner was stopped at 18:57 UTC. At that point close_tree had started three cap-600 cadical jobs past END, and those were killed; no checker was killed and no record has cake_lpr `none`. Of its 8 σ-level-1 cubes, 1 is certified directly and 4 are split with all 8 σ-level-2 children certified. The other 3 (`__1s1-4s0-6s0`, `__1s1-4s1-6s0`, `__1s1-4s1-6s1`) were split (records present) but none of their 24 σ-level-2 children has a record. Those 24 cubes are the open frontier.

## Totals per stratum
- H6(5,1)/two: 5 roots; 4 closed (rows 3, 33, 43, 63), 1 partial (row 73).
- H6(5,0)/two: 1 root, closed (row 53).
- H6(4,1)/two: 1 root, closed (row 23).
- H6(4,0)/two: 1 root, closed (row 13).
- All: 7 closed, 1 partial, 0 not reached; 173 records, 131 certified, 0 SAT.

Closed: 0s0-5s1_2s0-9s0, 0s0-4s0_2s0-5s0, 0s0-4s1_6s1-7s1, 0s0-5s1_1s0-6s1, 0s0-5s1_6s1-8s0, 0s0-5s0_7s0-8s1, 0s0-5s1_6s0-10s0.
Partial: 0s0-5s1_2s1-3s0.
