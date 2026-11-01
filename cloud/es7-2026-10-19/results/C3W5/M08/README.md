# C3W5 / M08: shard 8 of 10 of `W5_two.tsv` (3-fold class, σ-cube mop-up)

**Result: 6 of my 8 roots are closed, 1 is partial, 1 was not reached. No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 16:12:35 UTC (2026-10-24), END 18:57:35 UTC
(start + 3 h − 15 min). Task: `results/C3W5/TASK.md` at 265d8921, with V = M08, LIST = W5_two.tsv, j = 8, N = 10, SLICE = 1.0, H = 3.0.

- Tools: worktree of cad4e050 at `/opt/c3u2`, TOOLS = `/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools`, unmodified.
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8 (`make cake_lpr`, example → `s VERIFIED UNSAT`);
  lrat-check 2e3b2dc with the E2 patch. Sanity check passed: LRAT `3 0 0` on {1},{−1} rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches). Details in `tools.txt`.
- Roots: rows ≡ 8 (mod 10) of `W5_two.tsv` (`roots.tsv`).
- Seeding: **0 records**. None of my 8 roots has any record in `C3W4/*/out.jsonl`. There are no `C3W4/*/recheck*.jsonl` files. All 8 were "not reached in C3W4". `out.jsonl` therefore holds only new records (174 lines).
- Runner (`runner.sh`, `setsid nohup`): `close_tree.py base.cnf out.jsonl R --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`, S = min(1.0, hours left before END).
  At END I killed the runner, close_tree and its solvers and checkers by hand. No killed node had written a record. Every UNSAT record in `out.jsonl` has `certified: true`, with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`, so there was nothing to re-check (no `recheck.jsonl`).

## Per root

All roots are depth-2 roots. σ level: s0 = the root, s1 = a 3-bit σ cube, s2 = a 6-bit σ cube. Solve and check seconds are summed per node, and with 3 jobs on 4 cores they are not wall-clock.

| row | root | stratum | status | certified (σ level) | timeouts → σ-split | solve s | check s |
|-----|------|---------|--------|---------------------|--------------------|---------|---------|
| 8 | 0s0-5s1_6s1-9s1 | H6(5,1) | **closed** | s0: 1 | 0 | 90 | 80 |
| 18 | 0s0-4s1_2s0-5s1 | H6(4,1) | **closed** | s2: 64 | s0: 1, s1: 8 | 7153 | 3283 |
| 28 | 0s0-5s0_2s1-10s0 | H6(5,0) | **closed** | s0: 1 | 0 | 41 | 34 |
| 38 | 0s0-5s1_2s0-6s1 | H6(5,1) | **closed** | s1: 7, s2: 8 | s0: 1, s1: 1 | 2873 | 806 |
| 48 | 0s0-5s0_2s0-6s0 | H6(5,0) | **closed** | s0: 1 | 0 | 64 | 38 |
| 58 | 0s0-5s1_1s1-8s1 | H6(5,1) | **closed** | s1: 4, s2: 32 | s0: 1, s1: 4 | 4268 | 1761 |
| 68 | 0s0-5s1_1s1-10s1 | H6(5,1) | partial | s2: 6 | s0: 1, s1: 8 | 2983 | 297 |
| 78 | 0s0-5s1_7s0-9s1 | H6(5,1) | not reached | – | – | – | – |

Each closed root ended with `open_frontier 0` and `unsplittable 0`, and has no split record with `"children": 0`. In the whole run, no σ-level-2 cube timed out, so none was layer-split.

**Partial root 0s0-5s1_1s1-10s1** (started 18:33:28 with a 0.402 h slice and stopped at END): the root and all 8 of its 3-bit cubes timed out at 300 s and were split. Of the 64 resulting 6-bit cubes, 6 are certified and **58 are open** (never finished). It has no timed-out childless nodes (`unsplittable`: none), so the 58 open cubes are the whole open frontier. The run was killed at END, so close_tree printed no final `open_frontier` line for this root.

## Totals per stratum

| stratum | roots | closed | partial | not reached | certified nodes | solve s | check s |
|---------|-------|--------|---------|-------------|-----------------|---------|---------|
| H6(5,1)/two | 5 | 3 | 1 | 1 | 58 | 10214 | 2944 |
| H6(4,1)/two | 1 | 1 | 0 | 0 | 64 | 7153 | 3283 |
| H6(5,0)/two | 2 | 2 | 0 | 0 | 2 | 105 | 72 |
| **total** | 8 | 6 | 1 | 1 | 124 | 17472 | 6299 |

Records: 124 certified, 25 timeouts (UNKNOWN), 25 split records (all with 8 children). The largest proof was 316 MB; no proof files are committed.

## SAT / proof rejections / memory

- **SAT: none.**
- **PROOF NOT ACCEPTED: none.** There are no records with cake_lpr `none`.
- Memory: no problem. About 2 GB was in use with 3 jobs.
- One note: with the 1.0 h slice, close_tree overran by a few minutes because it finishes its running batch first (root 18 ended at 17:23:50, not 17:19:30).

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (new records only, 0 seeded), `driver.log.tail`, `summary.txt` (per-root counts by depth and σ level).
