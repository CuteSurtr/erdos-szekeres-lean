# C3W3 / B7: wave 3 of the 3-fold class (m = 11, k = 7), list B_h3pilot.tsv, shard 7 of 10

**Result: no SAT, no proof rejection, no memory problem. Root 1 of 3 (`0s0_1s0-8s0`) is partial with 353
certified nodes; roots 2 and 3 were not reached.**

Values: V = B7, LIST = B_h3pilot.tsv, j = 7, N = 10, LANES = 1, JOBS = 3, SLICE = 0.9, H = 3.0, Z = 640a56c2.

## What ran where

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:41:28 UTC on 2026-10-21, END = start + 3 h − 15 min
= 07:26:28 UTC. Details in `tools.txt`:

- C3-S tools: worktree of commit `132398c` at `/opt/c3s`, used unmodified (live files in `/opt/work`).
- CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8 (`make cake_lpr`; its example prints `s VERIFIED UNSAT`),
  drat-trim lrat-check 2e3b2dc with `results/E2/tools/lrat-check-E2.patch` (applied with `patch`).
  Sanity check: on {1},{-1}, the LRAT `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256
  `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: rows of `lists/B_h3pilot.tsv` with row ≡ 7 (mod 10): rows 7, 17, 27 (`roots.tsv`). All three have status
  `untouched`, so **0 records were seeded**; `out.jsonl` holds only new records (363 lines).
- One lane (`lane0.sh`, started with `setsid nohup`), `close_tree.py ... --jobs 3 --caps 300,300,600 --cadopts=--sat
  --split-singles --hours S`, S = min(0.9, hours left before END).

## Per root

| row | root | stratum | status | certified by depth | splits | timeouts | open at stop | solve s | check s |
|-----|------|---------|--------|--------------------|--------|----------|--------------|---------|---------|
| 7 | 0s0_1s0-8s0 | H3/two | **partial** | d4: 353 | d2: 1 (after timeout); d3: 8 (pre-split) | d2: 1 (root, 300 s) | d3: 112, d4: 375 | 18152 | 10277 |
| 17 | 0s0_2s1-3s0 | H3/two | not reached | – | – | – | – | – | – |
| 27 | 0s0_3s1-7s1 | H3/two | not reached | – | – | – | – | – | – |

Solve and check times are summed per node (3 jobs on 4 cores, so not wall-clock).

Root `0s0_1s0-8s0` timed out at 300 s and was split into 120 depth-3 children: 8 single-orbit ones were pre-split
(`--split-singles`) into 728 depth-4 nodes, and 112 two-orbit ones stay at depth 3. That gives one batch of 840 nodes.
`close_tree.py` checks its `--hours` deadline only between batches, so this first batch ran past its 0.9 h slice and
filled the whole budget. Its frontier sort puts the single-orbit (fewer `-`) depth-3 nodes first, so their depth-4
children ran first at the 600 s cap: 353 of the 728 were certified (all UNSAT, max solve 149 s, max proof 354 MB),
375 depth-4 and all 112 depth-3 nodes were not attempted. No node timed out apart from the root.

At END I killed the runner, `close_tree.py` and its three running CaDiCaL jobs (no checker was running, so there is
no `cake_lpr: none` record to re-check). `driver0.log` (last 100 lines) ends with that kill. The root is resumable from
`out.jsonl` (certified and split records).

## Totals per stratum

| stratum | roots | closed | partial | not reached | certified nodes |
|---------|-------|--------|---------|-------------|-----------------|
| H3/two | 3 | 0 | 1 | 2 | 353 |

All 353 certified records have `c VERIFIED` (lrat-check, E2 patch) and `s VERIFIED UNSAT` (cake_lpr).

## compose.py

`compose.txt`: `{"certified_nodes": 353, "class_covered": false, "uncovered_frontier_nodes": 236, ...}`, as
expected for one shard. compose recomputed the CNF sha256 of every certified node.

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: no problem (lowest available about 4 GB, no OOM).

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`, `out.jsonl`, `driver0.log` (last 100 lines), `summary.jsonl`
(per-root breakdown), `compose.txt`.
