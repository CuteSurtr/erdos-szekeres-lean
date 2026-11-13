# C3W5 M06: W5_two.tsv shard 6 of 10

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 16:12:24 UTC on 2026-10-24, END 18:57:24 UTC
(start + 3 h − 15 min). Task file `results/C3W5/TASK.md` at 265d8921; V = M06, LIST = W5_two.tsv, j = 6, N = 10,
SLICE = 1.0, H = 3.0.

## Tools (`tools.txt`)

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, `TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools`, unmodified
- CaDiCaL c6073042 (3.0.1); cake_lpr a36874a8 (bundled example: `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc
  with `results/E2/tools/lrat-check-E2.patch`. Sanity check on {1},{-1}: LRAT `3 0 0` is rejected by both checkers,
  and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…cdd6da` (matches)
- `compose.py` was not run, as the task says.

## Run

The roots are the rows of `W5_two.tsv` with row ≡ 6 (mod 10), giving 8 roots (`roots.tsv`). None of them was reached in C3W4,
so **0 records were seeded** (48 C3W4 out/recheck files scanned), and `out.jsonl` holds only new records (53 lines).
Runner (`runner.sh`, `setsid nohup`): `close_tree.py … --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 300,300,600
--cadopts=--sat --split-singles --hours S` per root, with S = 1.0. It started at 16:15:26 and finished all 8 roots at 17:37:27.

## Per root

Depth means the number of layers (all nodes here are at depth 2). σ level 0 is the root itself; σ level 1 is the 8 cubes on 3 σ bits.

| row | root | stratum | status | certified (depth 2) | timeouts | σ split | solve s | check s |
|-----|------|---------|--------|---------------------|----------|---------|---------|---------|
| 6 | 0s0-5s1_6s0-7s0 | H6(5,1)/two | **closed** | σ0: 1 | 0 | – | 36 | 43 |
| 16 | 0s0-4s1_1s1-2s0 | H6(4,1)/two | **closed** | σ1: 8 | 1 (root, 300 s) | bits [3,5,6], 8 cubes | 1733 | 369 |
| 26 | 0s0-5s0_1s1-2s0 | H6(5,0)/two | **closed** | σ1: 8 | 1 (root) | bits [3,4,6], 8 cubes | 1070 | 332 |
| 36 | 0s0-5s1_1s1-7s1 | H6(5,1)/two | **closed** | σ1: 8 | 1 (root) | bits [2,3,4], 8 cubes | 1112 | 296 |
| 46 | 0s0-4s1_7s0-8s1 | H6(4,1)/two | **closed** | σ1: 8 | 1 (root) | bits [1,2,3], 8 cubes | 1953 | 370 |
| 56 | 0s0-5s1_1s1-10s0 | H6(5,1)/two | **closed** | σ0: 1 | 0 | – | 44 | 29 |
| 66 | 0s0-5s1_7s0-8s1 | H6(5,1)/two | **closed** | σ1: 8 | 1 (root) | bits [1,2,3], 8 cubes | 1838 | 341 |
| 76 | 0s0-5s1_6s1-10s1 | H6(5,1)/two | **closed** | σ0: 1 | 0 | – | 228 | 37 |

For every root, close_tree reported `open_frontier 0, unsplittable 0`. There is no split record with 0 children, and
no σ cube timed out, so no layer split was needed. Solve and check seconds are summed per node, not wall clock (3 jobs share 4 cores).

## Totals per stratum

| stratum | roots | closed | certified nodes | timeouts | solve s | check s |
|---------|-------|--------|-----------------|----------|---------|---------|
| H6(5,1)/two | 5 | 5 | 19 | 2 | 3258 | 746 |
| H6(4,1)/two | 2 | 2 | 16 | 2 | 3686 | 739 |
| H6(5,0)/two | 1 | 1 | 8 | 1 | 1070 | 332 |
| all | 8 | 8 | 43 | 5 | 8014 | 1817 |

## Incidents

- No SAT answer, no `PROOF NOT ACCEPTED`, and no certified-looking record with cake_lpr `none`. Every certified record has
  `c VERIFIED` and `s VERIFIED UNSAT`, so no re-check was needed and there is no `recheck.jsonl`.
- No memory problem: peak use seen was about 5 GB of 15 GB.
- Pushes needed retries because of concurrent pushers (one 403 RPC failure, then success). The fallback branch was never used.
