# C3W5 / M09: W5_two.tsv shard 9 of 10, 3-fold class, σ-cube mop-up

**Result: all 7 of my roots are closed (open frontier 0, no unsplittable / childless timed-out node). No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 16:11:59 UTC, END 18:56:59 UTC (3 h − 15 min); the runner finished all roots at 17:05:26 UTC.

- Tools: worktree of `cad4e050` at `/opt/c3u2`, TOOLS = `results/C3U2/tools`, used unmodified; `compose.py` not run.
- CaDiCaL 3.0.1 `c60730422e758ef1cebe7aeddf2dda31c996bf04`; cake_lpr `a36874a8` (example: `s VERIFIED UNSAT`); lrat-check `2e3b2dc` + E2 patch. Sanity: LRAT `3 0 0` on {1},{-1} rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…cdd6da` (matches). Details in `tools.txt`.
- Roots: rows of `lists/W5_two.tsv` with row ≡ 9 (mod 10): 7 roots (`roots.tsv`), all "not reached in C3W4".
- Seeding: **0 records** (no C3W4 out/recheck record has node R, R_… or R__… for any of these roots), so `out.jsonl` holds only new records (47 lines).
- Runner `runner.sh`: `close_tree.py … --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`, S = min(1.0, hours left).

## Per root

σ1 = 3-bit cube, σ2 = 6-bit cube; no layer split was needed. Solve/check seconds are summed per node (3 jobs on 4 cores).

| row | root | stratum | status | certified | timeouts (cap 300) | solve s | check s |
|-----|------|---------|--------|-----------|--------------------|---------|---------|
| 9 | 0s0-5s1_7s1-8s0 | H6(5,1)/two | **closed** | σ1: 5, σ2: 24 | root 1, σ1 3 | 3235 | 1047 |
| 19 | 0s0-4s1_2s0-8s0 | H6(4,1)/two | **closed** | σ1: 8 | root 1 | 819 | 302 |
| 29 | 0s0-5s0_6s0-9s1 | H6(5,0)/two | **closed** | root: 1 | – | 198 | 40 |
| 39 | 0s0-5s1_2s1-10s0 | H6(5,1)/two | **closed** | root: 1 | – | 45 | 31 |
| 49 | 0s0-5s0_2s0-8s1 | H6(5,0)/two | **closed** | root: 1 | – | 124 | 32 |
| 59 | 0s0-5s1_2s0-10s1 | H6(5,1)/two | **closed** | root: 1 | – | 77 | 35 |
| 69 | 0s0-5s1_1s1-3s1 | H6(5,1)/two | **closed** | root: 1 | – | 55 | 30 |

## Totals per stratum

| stratum | roots | closed | certified nodes | timeouts |
|---------|-------|--------|-----------------|----------|
| H6(5,1)/two | 4 | 4 | 32 | 4 |
| H6(4,1)/two | 1 | 1 | 8 | 1 |
| H6(5,0)/two | 2 | 2 | 2 | 0 |
| **all** | 7 | 7 | 42 | 5 |

All 42 UNSAT records carry `lrat_check: c VERIFIED` and `cake_lpr: s VERIFIED UNSAT` (`certified: true`). All 5 timeouts were split (4 splits of 8 children); no split record has 0 children.

## SAT / rejections / memory

- SAT: none. PROOF NOT ACCEPTED: none; no cake_lpr `none`, so no `recheck.jsonl`.
- Memory: peak about 12 GB used of 15 GB during root 9 (three proofs checked at once); no failure.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl`, `driver.log.tail`, `README.md`.
