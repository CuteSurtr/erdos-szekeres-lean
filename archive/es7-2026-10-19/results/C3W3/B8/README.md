# C3W3 / B8: wave 3, list B_h3pilot.tsv, shard 8 of 10, one machine

**Result: 0 of my 3 roots closed. Root 1 (`0s0_1s0-9s1`) is partial with 506 certified nodes; roots 2 and 3 were not reached. No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:41:30 UTC on 2026-10-21 (1792557690), H = 3 h, END = 07:26:30 UTC. 1 lane, `--jobs 3`, slice 0.9 h, TASK.md at 640a56c2.

- C3-S tools: worktree of 132398c (132398cdc801…) at `/opt/c3s`, unmodified.
- CaDiCaL 3.0.1 (c60730422e75…); cake_lpr a36874a8 (`make cake_lpr`, example prints `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc with `results/E2/tools/lrat-check-E2.patch`. Sanity check: on {1},{-1}, LRAT `3 0 0` is rejected by both checkers (`c NOT VERIFIED`; cake_lpr "pivot must be non-zero"), `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches). Details in `tools.txt`.
- Roots: rows 8, 18, 28 of `lists/B_h3pilot.tsv` (`roots.tsv`), all stratum H3/two, h6m_kept `na`, status `untouched`.
- Seeded records: **0** (no root was `partial`). `out.jsonl` holds only this run's records.

## Per root (depth = number of layers; roots are at depth 2)

| row | root | stratum | status | certified by depth | timeouts | splits | solve s | check s |
|-----|------|---------|--------|--------------------|----------|--------|---------|---------|
| 8 | 0s0_1s0-9s1 | H3/two | **partial** | d4: 506 | d2: 1 (300 s) | d2: 1 (120 children); d3: 8 pre-split (91 children each) | 16755 | 12390 |
| 18 | 0s0_2s1-3s1 | H3/two | not reached | – | – | – | – | – |
| 28 | 0s0_4s0-6s1 | H3/two | not reached | – | – | – | – | – |

Solve and check times are per-node sums (3 jobs on 4 cores), not wall-clock.

Root 8 timed out at depth 2 (300 s) and was split into 120 depth-3 children: 112 two-orbit children and 8 one-orbit ones (`_2`…`_8`, `_10`), which were pre-split into 91 depth-4 children each. That gave one batch of 112 + 728 = 840 nodes. At the stop, 506 depth-4 nodes were certified (all with `c VERIFIED` and `s VERIFIED UNSAT`, at most 163 s solve against the 600 s cap): every child of `_2`, `_3`, `_4`, `_5` and `_6` (5 × 91 = 455), and 51 of the 91 children of `_7`. The other 40 children of `_7`, all 182 children of `_8` and `_10`, and the 112 depth-3 two-orbit children (334 nodes) have no record and are open; a resume of `close_tree.py` on this root will run them first.

## Totals per stratum

| stratum | roots | closed | partial | not reached | certified nodes | timeouts |
|---------|-------|--------|---------|-------------|-----------------|----------|
| H3/two | 3 | 0 | 1 | 2 | 506 | 1 |

## The slice is not enforced inside a batch

As already noted in the C3WAVE2 READMEs, `close_tree.py` checks `--hours` only before a batch, and a batch is the whole current frontier. Root 8's second batch (840 nodes) started at about 04:49 and was still running at END, well past its 0.9 h slice, so the runner never reached roots 18 and 28. I stopped the driver by hand at 07:30:49 UTC (END 07:26:30; my scripted kill at END stopped only the runner shell; marked `=== STOPPED` in `driver0.log`). The nodes in flight at the kill (one cadical, two cake_lpr runs) wrote no record, so there is no `cake_lpr: none` record and nothing to re-check.

## compose.py

`compose.txt`: `{"certified_nodes": 506, "class_covered": false, "uncovered_frontier_nodes": 263, ...}`. As expected, the class is not covered; compose recomputed the CNF sha256 of all 506 certified nodes.

## SAT / proof rejections / memory

- **SAT: none.**
- **PROOF NOT ACCEPTED: none.** Every UNSATISFIABLE record is certified by both checkers.
- **Memory:** no problem (about 2–3 GB used of 15 GB with 3 jobs).

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`, `out.jsonl` (all 516 new records of lane 0), `driver0.log` (last 100 lines), `compose.txt`.
