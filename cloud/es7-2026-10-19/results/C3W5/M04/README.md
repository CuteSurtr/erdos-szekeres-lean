# C3W5 / M04: W5_two.tsv shard 4 of 10 (rows ≡ 4 mod 10), slice 1.0 h, budget 3.0 h

**Result: all 8 roots closed (open frontier 0, no childless timed-out node, no unsplittable node). No SAT. No proof rejection. No memory problem.**

Task: `results/C3W5/TASK.md` at 265d8921. Start 16:11:42 UTC 2026-10-24, END 18:56:42 UTC; runner 16:14:16 to 17:18:39 UTC (finished all roots early).

## Tools and base CNF (`tools.txt`)

- Tools: worktree of cad4e050 (`results/C3U2/tools`), unmodified. `compose.py` not run.
- CaDiCaL 3.0.1 c60730422e; cake_lpr a36874a8 (example: `s VERIFIED UNSAT`); lrat-check 2e3b2dc + E2 patch (sanity: `3 0 0` rejected by both, `3 0 1 2 0` accepted by both).
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da` (matches).
- Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 300,300,600 --cadopts=--sat --split-singles --hours 1.0`.
- Seeding: 0 records (none of the 8 roots appears in `results/C3W4/*/out.jsonl`; no `recheck*.jsonl` exist). `out.jsonl` therefore holds only new records (44 lines).

## Per root

Depth = number of layers (roots at depth 2); σ = number of σ-splits on the path.

| row | root | stratum | status | certified (depth, σ level) | timeouts (300 s) | σ split | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| 4 | 0s0-5s1_2s1-6s0 | H6(5,1)/two | **closed** | d2 σ1: 8 | 1 (root) | root on bits [1,3,4], 8 children | 1309 | 347 |
| 14 | 0s0-4s0_2s0-7s0 | H6(4,0)/two | **closed** | d2 σ0: 1 | 0 | – | 104 | 42 |
| 24 | 0s0-4s1_7s0-8s0 | H6(4,1)/two | **closed** | d2 σ0: 1 | 0 | – | 37 | 39 |
| 34 | 0s0-5s1_1s0-9s0 | H6(5,1)/two | **closed** | d2 σ1: 8 | 1 (root) | root on bits [2,3,4], 8 children | 1050 | 299 |
| 44 | 0s0-5s1_7s0-8s0 | H6(5,1)/two | **closed** | d2 σ0: 1 | 0 | – | 41 | 38 |
| 54 | 0s0-5s1_1s0-3s1 | H6(5,1)/two | **closed** | d2 σ1: 8 | 1 (root) | root on bits [2,4,6], 8 children | 1335 | 324 |
| 64 | 0s0-5s1_6s0-9s1 | H6(5,1)/two | **closed** | d2 σ1: 8 | 1 (root) | root on bits [1,2,3], 8 children | 1506 | 335 |
| 74 | 0s0-5s1_2s1-8s0 | H6(5,1)/two | **closed** | d2 σ0: 1 | 0 | – | 295 | 41 |

Solve/check seconds are summed per node (3 jobs on 4 cores), including the 300 s timed-out root attempts.

## Totals per stratum

| stratum | roots | closed | certified nodes |
|---|---|---|---|
| H6(5,1)/two | 6 | 6 | 34 |
| H6(4,0)/two | 1 | 1 | 1 |
| H6(4,1)/two | 1 | 1 | 1 |
| total | 8 | 8 | 36 |

All 36 UNSAT records: lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`. close_tree reported `open_frontier 0, unsplittable 0` for every root. No `"children": 0` split record.

## SAT / rejections / memory

None. No SATISFIABLE result, no PROOF NOT ACCEPTED, no cake_lpr `none`, so no `recheck.jsonl`. Peak memory use observed about 3 GB of 15 GB.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl`, `driver.log.tail`, `README.md`.
