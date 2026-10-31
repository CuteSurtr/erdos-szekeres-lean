# C3W4 / O04: W4_one.tsv shard 4 of 16, σ-cube splitting

**Result: all 3 of my roots are closed (open frontier 0, no childless timed-out node). No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:10 UTC 2026-10-24, END 16:16:10 UTC; the runner finished at 14:54:21 UTC.

- Tools: worktree of commit 95cafa93 (`95cafa9307faef75cc584c08d44727b43c89c0bf`) at `/opt/c3u`, `results/C3U/tools` used unmodified.
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (example prints `s VERIFIED UNSAT`); lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with the E2 patch. Sanity check passed: LRAT `3 0 0` on {1},{-1} rejected by both checkers, `3 0 1 2 0` accepted by both (`tools.txt`).
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).
- Roots: rows of `W4_one.tsv` with row ≡ 4 (mod 16): rows 4, 20, 36 (`roots.tsv`). Nothing was seeded; every root started fresh.
- Runner (`runner.sh`): `close_tree.py /opt/work/base.cnf /opt/work/out.jsonl R --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours min(2.5, left)`.
- `compose.py` was not run, as the task requires.

## Per root

Each root: the root and its 8 first-level σ nodes timed out at cap 1 s (9 timeouts, 9 split records, each with 8 children). That gives 64 cubes on 6 σ bits (σ level 2, layer depth 2). All 64 were certified at cap 300 s, so no cube needed the layer split (no cap-600 records).

| row | root | stratum | status | certified (depth 2, σ level 2) | timeouts (cap 1) | max cube solve s | solve s | check s | wall |
|---|---|---|---|---|---|---|---|---|---|
| 4 | 0s0-2s0_1 | H6(2,0)/one | **closed** | 64 | 9 | 127 | 3,127 | 2,111 | 11:32–12:03 |
| 20 | 0s0-3s1_7 | H6(3,1)/one | **closed** | 64 | 9 | 276 | 13,179 | 3,101 | 12:03–13:35 |
| 36 | 0s0-5s1_7 | H6(5,1)/one | **closed** | 64 | 9 | 243 | 11,081 | 2,825 | 13:35–14:54 |

Solve and check seconds are summed over nodes (3 jobs share 4 cores, so they are not wall-clock). Every certified record has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.

## Totals per stratum

| stratum | roots | closed | certified cubes | timeouts | solve s | check s |
|---|---|---|---|---|---|---|
| H6(2,0)/one | 1 | 1 | 64 | 9 | 3,127 | 2,111 |
| H6(3,1)/one | 1 | 1 | 64 | 9 | 13,179 | 3,101 |
| H6(5,1)/one | 1 | 1 | 64 | 9 | 11,081 | 2,825 |
| all | 3 | 3 | 192 | 27 | 27,387 | 8,037 |

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none. No certified-looking record has cake_lpr `none`, and no checker was killed. There is no `recheck.jsonl`.
- Memory: peak about 9 GB used of 15 GB; no problem.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (246 records), `driver.log.tail`, `README.md`.
