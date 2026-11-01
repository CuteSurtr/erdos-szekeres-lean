# C3W5 M02: shard 2 of 10 of W5_two.tsv

Task `results/C3W5/TASK.md` at 265d8921, with V = M02, LIST = W5_two.tsv, j = 2, N = 10, SLICE = 1.0 h, H = 3.0 h.
One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 16:11:31 UTC, END 19:09:31 UTC; the runner finished all roots at 17:07:53 UTC.

## Tools and base CNF

- C3U2 tools from a worktree of cad4e050 at `/opt/c3u2`, used unmodified. `compose.py` not run.
- CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8 (bundled example prints `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch.
  Sanity check passed: on {1},{-1} the LRAT `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches).
- Details are in `tools.txt`.

## Run

Options: `--sigma-split 3 --sigma-levels 2 --caps 300,300,600 --cadopts=--sat --split-singles`, `--jobs 3`, `--hours 1.0` per root (`runner.sh`).
Seeding: no records of `results/C3W4/*/out.jsonl` matched these roots, and there are no `recheck*.jsonl` files, so 0 records were seeded. `out.jsonl` has all 44 records of this run.

## Per root

Every root is **closed**: open frontier 0, no unsplittable node, no split record with `"children": 0`. Every certified node was accepted by both checkers (`c VERIFIED` and `s VERIFIED UNSAT`).

| row | root | stratum | status | certified (σ level 0 / 1) | timeouts | solve s | check s | wall |
|---|---|---|---|---|---|---|---|---|
| 2 | 0s0-3s1_5s1-7s0 | H6(3,1)/two | closed | 0 / 8 | 1 (root) | 1423.5 | 259.8 | 13.6 min |
| 12 | 0s0-3s1_5s1-8s0 | H6(3,1)/two | closed | 0 / 8 | 1 (root) | 1207.6 | 229.6 | 12.7 min |
| 22 | 0s0-4s1_5s1-8s1 | H6(4,1)/two | closed | 1 / 0 | 0 | 32.7 | 24.2 | 1.0 min |
| 32 | 0s0-5s1_1s0-2s0 | H6(5,1)/two | closed | 1 / 0 | 0 | 8.9 | 19.8 | 0.5 min |
| 42 | 0s0-5s1_6s0-7s1 | H6(5,1)/two | closed | 0 / 8 | 1 (root) | 1251.2 | 251.1 | 12.5 min |
| 52 | 0s0-5s0_6s1-8s1 | H6(5,0)/two | closed | 1 / 0 | 0 | 17.9 | 17.8 | 0.6 min |
| 62 | 0s0-5s1_2s1-7s1 | H6(5,1)/two | closed | 1 / 0 | 0 | 166.9 | 30.2 | 3.3 min |
| 72 | 0s0-5s1_2s0-7s1 | H6(5,1)/two | closed | 0 / 8 | 1 (root) | 863.0 | 219.9 | 10.0 min |

All nodes are at layer depth 2 (the roots). Where the root timed out at 300 s, it was split once on 3 σ bits, and all 8 cubes were certified at cap 300. No layer split was needed. Solve-second totals include the 300 s root timeouts.

## Totals per stratum

| stratum | roots | closed | certified | timeouts | solve s | check s |
|---|---|---|---|---|---|---|
| H6(3,1)/two | 2 | 2 | 16 | 2 | 2631.1 | 489.4 |
| H6(4,1)/two | 1 | 1 | 1 | 0 | 32.7 | 24.2 |
| H6(5,1)/two | 4 | 4 | 18 | 2 | 2290.0 | 521.0 |
| H6(5,0)/two | 1 | 1 | 1 | 0 | 17.9 | 17.8 |
| all | 8 | 8 | 36 | 4 | 4971.7 | 1052.4 |

## Incidents

No SAT, no proof rejection, no checker killed at END (so no re-checks and no `recheck.jsonl`), and no memory problem (at most about 6 GB used).
