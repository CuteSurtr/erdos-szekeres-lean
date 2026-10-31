# C3W3 / B0: list B_h3pilot.tsv, shard 0 of 10, one lane

**Result: no root closed. Root 1 (`0s0_1`) is partial; roots 2 and 3 were not reached. No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:41:13 UTC, END 07:26:13 UTC (start + 3 h − 15 min) on 2026-10-21.
TASK.md at 640a56c2, with V = B0, LIST = B_h3pilot.tsv, j = 0, N = 10, LANES = 1, JOBS = 3, SLICE = 0.9, H = 3.0.

- C3-S tools: worktree of 132398c at /opt/c3s, unmodified.
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04.
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`); its example prints `s VERIFIED UNSAT`.
- lrat-check from drat-trim 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with `results/E2/tools/lrat-check-E2.patch`. Sanity check on {1},{-1}: `3 0 0` is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da`. It matches.
- Roots: rows 0, 10 and 20 of `B_h3pilot.tsv` (`roots.tsv`). All three are `untouched`, so **0 records were seeded**, and `out.jsonl` holds only new records.
- One lane (`lane0.sh`): `close_tree.py ... --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`, S = min(0.9, hours left).

## Per root

| # | root | stratum | status | certified by depth | timeouts | splits | solve s | check s |
|---|------|---------|--------|--------------------|----------|--------|---------|---------|
| 1 | 0s0_1 | H3/one | **partial** | none | d3: 96 (all at 300 s) | d2: 1 (pre-split, 153 children); d3: 96 (after a timeout); d4: 609 (pre-split) | 28811 | 0 |
| 2 | 0s0_1s1-6s0 | H3/two | not reached | – | – | – | – | – |
| 3 | 0s0_2s1-8s0 | H3/two | not reached | – | – | – | – | – |

Root 1 started at 04:43:47. Its 0.9 h slice ended at 05:37:47, but `close_tree.py` checks its deadline only between frontier waves. The first wave is the 153 depth-3 children, and at 300 s each with 3 jobs that wave takes about 4.3 h. So the root ran until END, and I killed it at 07:26:15. By then 96 of the 153 depth-3 children had been tried. Every one of them hit the 300 s cap (UNKNOWN) and was split, and the one-orbit children of those splits were pre-split (609 records at depth 4). No depth-4 or deeper node was attempted. The 57 untried depth-3 children and all depth-4/5 children are still open. The records in `out.jsonl` can be used to resume this root.

The three CaDiCaL runs I killed at END wrote no records, and no checker was running at that moment, so no node has `cake_lpr: none`. Solve time is summed per node (3 jobs on 4 cores). No proof was checked, because nothing came back UNSAT.

## Totals per stratum

| stratum | roots | closed | partial | not reached | certified nodes | timeouts |
|---------|-------|--------|---------|-------------|-----------------|----------|
| H3/one | 1 | 0 | 1 | 0 | 0 | 96 |
| H3/two | 2 | 0 | 0 | 2 | 0 | 0 |

## compose.py

`compose.txt`: `certified_nodes: 0, class_covered: false`. This was expected.

## SAT / proof rejection / memory

- SAT: none. No SATISFIABLE result.
- PROOF NOT ACCEPTED: none.
- Memory: no problem. About 2 GB was used, out of 15 GB.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`, `out.jsonl` (all records, new only), `driver0.log` (last 100 lines), `compose.txt`.
