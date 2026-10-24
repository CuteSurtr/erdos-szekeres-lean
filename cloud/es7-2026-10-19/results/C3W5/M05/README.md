# C3W5 M05: W5_two.tsv shard 5 of 10

Task: `results/C3W5/TASK.md` at 265d8921, with V = M05, LIST = W5_two.tsv, j = 5, N = 10, SLICE = 1.0 h, H = 3.0 h.
One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 16:12:23 UTC, END 18:57:23 UTC (2026-10-24); the runner finished all roots at 17:01:12 UTC.

## Tools and base CNF (`tools.txt`)

- Tools: worktree of cad4e050 at `/opt/c3u2`, `results/C3U2/tools`, unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8 (example prints `s VERIFIED UNSAT`); lrat-check 2e3b2dc0 with the E2 patch. Sanity check passed: LRAT `3 0 0` on {1},{-1} rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…0cdd6da` (matches).

## Roots and seeding

Rows of `W5_two.tsv` with row ≡ 5 (mod 10): 8 roots (`roots.tsv`), all "not reached in C3W4". Seeded records from `C3W4/*/out.jsonl` and `C3W4/*/recheck*.jsonl`: **0** (none of the 8 roots has records there; no recheck files exist). So `out.jsonl` holds all 35 records written by this run.

Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 300,300,600 --cadopts=--sat --split-singles --hours 1.0` (`runner.sh`).

## Per root

Depth is the number of layers (roots are depth 2; σ children stay at depth 2). "σ1" is the first σ level.

| row | root | stratum | status | certified | timeouts | splits | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| 5 | 0s0-5s1_2s1-9s0 | H6(5,1)/two | **closed** | d2 σ0: 1 | 0 | 0 | 45.2 | 42.7 |
| 15 | 0s0-4s1_1s0-6s1 | H6(4,1)/two | **closed** | d2 σ1: 8 | 1 (root, 300 s) | root σ-split, 8 children | 1105.6 | 345.9 |
| 25 | 0s0-5s0_1s0-9s0 | H6(5,0)/two | **closed** | d2 σ1: 8 | 1 (root, 300 s) | root σ-split, 8 children | 932.8 | 329.1 |
| 35 | 0s0-5s1_1s1-2s1 | H6(5,1)/two | **closed** | d2 σ0: 1 | 0 | 0 | 39.6 | 35.7 |
| 45 | 0s0-5s1_7s1-8s1 | H6(5,1)/two | **closed** | d2 σ0: 1 | 0 | 0 | 42.2 | 43.7 |
| 55 | 0s0-5s1_1s0-7s0 | H6(5,1)/two | **closed** | d2 σ0: 1 | 0 | 0 | 288.4 | 53.0 |
| 65 | 0s0-5s1_6s1-8s1 | H6(5,1)/two | **closed** | d2 σ0: 1 | 0 | 0 | 41.1 | 40.7 |
| 75 | 0s0-5s1_6s0-10s1 | H6(5,1)/two | **closed** | d2 σ1: 8 | 1 (root, 300 s) | root σ-split, 8 children | 1041.4 | 322.4 |

Every root ended with `open_frontier 0` and `unsplittable 0`; there is no split record with `children: 0`. No root was left partial or not reached.

## Totals per stratum

| stratum | roots | closed | certified nodes | timeouts | solve s | check s |
|---|---|---|---|---|---|---|
| H6(5,1)/two | 6 | 6 | 13 | 1 | 1497.9 | 538.2 |
| H6(4,1)/two | 1 | 1 | 8 | 1 | 1105.6 | 345.9 |
| H6(5,0)/two | 1 | 1 | 8 | 1 | 932.8 | 329.1 |
| all | 8 | 8 | 29 | 3 | 3536.3 | 1213.2 |

All 29 certified records have `lrat_check: c VERIFIED` and `cake_lpr: s VERIFIED UNSAT`.

## Incidents

No SAT answer, no `PROOF NOT ACCEPTED`, no cake_lpr `none`, no re-checks (`recheck.jsonl` not needed), no memory problem (peak about 6 GB used of 15). The only deviation from a literal copy of a command: the E2 patch is in normal `diff` format, so it was applied with `patch` rather than `git apply` (same resulting line in `lrat-check.c`).
