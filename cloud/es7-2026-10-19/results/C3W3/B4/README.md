# C3W3 / B4: wave 3, list B_h3pilot.tsv, shard 4 of 10

**Result: root 1 of 3 (`0s0_1s0-4s0`) is partial (755 certified nodes, 85 depth-3 nodes still open); roots 2 and 3 were not reached. No SAT. No proof rejection. No memory problem.**

Task: `results/C3W3/TASK.md` at 640a56c2, with V = B4, LIST = B_h3pilot.tsv, j = 4, N = 10, LANES = 1, JOBS = 3, SLICE = 0.9, H = 3.0.

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:41:24 UTC on 2026-10-21, END 07:26:24 UTC.

- C3-S tools: worktree of commit 132398c at `/opt/c3s`, used unmodified.
- CaDiCaL 3.0.1, c60730422e758ef1cebe7aeddf2dda31c996bf04.
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`); its example prints `s VERIFIED UNSAT`.
- lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with `results/E2/tools/lrat-check-E2.patch` (applied with patch(1)). Sanity check: on {1},{-1}, `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: rows of `lists/B_h3pilot.tsv` with row ≡ 4 (mod 10), giving 3 roots (`roots.tsv`). All are `untouched`, so **0 records were seeded**, and `out.jsonl` holds only new records.
- One lane (`lane0.sh`) running `close_tree.py ... --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`, with S = min(0.9, hours left).

## Per root (depth = number of layers; roots are at depth 2)

| row | root | stratum | status | certified by depth | splits | timeouts | solve s | check s |
|-----|------|---------|--------|--------------------|--------|----------|---------|---------|
| 4 | 0s0_1s0-4s0 | H3/two | **partial** | d3: 27, d4: 728 | d2: 1 (timeout, 120 children); d3: 8 (pre-split, 91 children each) | 1 (the root, 300 s) | 13292 | 15130 |
| 14 | 0s0_2s0-4s1 | H3/two | not reached | – | – | – | – | – |
| 24 | 0s0_3s1-6s0 | H3/two | not reached | – | – | – | – | – |

Solve and check times are summed per node, so they are not wall-clock. With 3 jobs on 4 cores, each per-node time is inflated.

Root `0s0_1s0-4s0` timed out at 300 s and was split into 120 depth-3 children: 8 one-orbit children (`_2`, `_3`, `_5` … `_10`) and 112 two-orbit children. The 8 one-orbit children were pre-split into 8 × 91 = 728 depth-4 nodes. **All 728 were certified**, so those 8 subtrees are closed. Of the 112 two-orbit depth-3 nodes, 27 were certified (the largest solve took 112 s, all under the 300 s cap) and 85 are still open.

The root ran as a single frontier wave from 04:43 until END. `close_tree.py` checks its `--hours` deadline only between waves, so the 0.9 h slice did not stop it. At END I killed the lane's process group, including two cake_lpr runs and one lrat-check run that were in progress. Those nodes have no record, and no `cake_lpr: none` record was written, so no re-check was needed. A later wave resumes the root from `out.jsonl` (its certified and split records).

## Totals per stratum

| stratum | roots | closed | partial | not reached | certified nodes | timeouts |
|---------|-------|--------|---------|-------------|-----------------|----------|
| H3/two | 3 | 0 | 1 | 2 | 755 | 1 |

Every one of the 755 certified records has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`. The largest proof was 305 MB; proofs were not committed.

## compose.py

`compose.txt`: `certified_nodes: 755, class_covered: false, uncovered_frontier_nodes: 194`. This is expected, since this machine holds one shard of one list.

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: no problem. About 6 GB in use with 3 jobs.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`, `out.jsonl` (new records only; 0 seeded), `driver0.log` (last 100 lines), `compose.txt`.
