# C3W5 / M00: shard 0 of 10 of W5_two.tsv

**Result: all 8 of my roots are closed (open frontier 0, no unsplittable or childless timed-out node). No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 16:11:28 UTC, END 18:56:28 UTC (start + 3 h − 15 min); the runner finished all roots at 17:04:55 UTC.

- Tools: worktree of cad4e050 at `/opt/c3u2`, TOOLS = `results/C3U2/tools`, unmodified. `compose.py` not run.
- CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (example prints `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch. Sanity check: LRAT `3 0 0` on {1},{-1} rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).
- Roots: rows of `C3W5/lists/W5_two.tsv` with row ≡ 0 (mod 10): 8 roots (`roots.tsv`).
- Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`, S = min(1.0, hours left). Runner: `runner.sh`. Details in `tools.txt`.
- Seeding: 1 record, the σ split record of `0s0-5s1_2s0-3s1` (bits [1,4,6], 8 children) from `C3W4/T0/out.jsonl`. No other root had a certified or split record in `C3W4/*/out.jsonl` or `recheck*.jsonl`. `out.jsonl` here holds only the 33 new records (after the seeded line).

## Per root

All nodes are at depth 2 (no layer split was needed). σ level 0 = the root itself, level 1 = a 3-bit σ cube. Solve and check seconds are summed per node (3 jobs on 4 cores).

| row | root | stratum | status | certified (σ level) | timeouts (300 s) | σ splits | solve s | check s |
|-----|------|---------|--------|---------------------|------------------|----------|---------|---------|
| 0 | 0s0-5s1_2s0-3s1 | H6(5,1)/two | **closed** | L1: 8 | 0 (root split seeded) | seeded: bits [1,4,6] | 873 | 342 |
| 10 | 0s0-3s1_4s0-8s0 | H6(3,1)/two | **closed** | L0: 1 | 0 | 0 | 140 | 40 |
| 20 | 0s0-4s1_5s0-7s1 | H6(4,1)/two | **closed** | L1: 8 | 1 (root) | bits [1,2,3] | 1814 | 393 |
| 30 | 0s0-5s0_6s1-8s0 | H6(5,0)/two | **closed** | L0: 1 | 0 | 0 | 249 | 49 |
| 40 | 0s0-5s1_2s1-7s0 | H6(5,1)/two | **closed** | L1: 8 | 1 (root) | bits [1,3,4] | 812 | 284 |
| 50 | 0s0-5s0_2s1-10s1 | H6(5,0)/two | **closed** | L0: 1 | 0 | 0 | 200 | 42 |
| 60 | 0s0-5s1_2s0-7s0 | H6(5,1)/two | **closed** | L0: 1 | 0 | 0 | 137 | 36 |
| 70 | 0s0-5s1_1s1-9s0 | H6(5,1)/two | **closed** | L0: 1 | 0 | 0 | 38 | 32 |

## Totals per stratum

| stratum | roots | closed | certified nodes | timeouts |
|---------|-------|--------|-----------------|----------|
| H6(5,1)/two | 4 | 4 | 18 | 1 |
| H6(5,0)/two | 2 | 2 | 2 | 0 |
| H6(4,1)/two | 1 | 1 | 8 | 1 |
| H6(3,1)/two | 1 | 1 | 1 | 0 |
| all | 8 | 8 | 29 | 2 |

All 29 certified nodes have `lrat_check: c VERIFIED` and `cake_lpr: s VERIFIED UNSAT`. Records: 29 UNSATISFIABLE, 2 UNKNOWN (root timeouts at 300 s), 2 split records.

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none; no record with cake_lpr `none`; no recheck needed.
- Memory: no problem (about 3 GB used with 3 jobs).
- Unsplittable / childless timed-out nodes: none.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (new records only), `driver.log.tail`, `README.md`.
