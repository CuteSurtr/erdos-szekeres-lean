# C3WAVE2 / K43: idx 799 down to 700 of `C3WAVE2/roots.tsv`, 3-fold class (m = 11, k = 7)

**Result: 0 of my 100 roots closed, 1 partial (`0s0-4s1_1s0-5s1`, idx 799), 99 not reached. 373 nodes certified
(both checkers). No SAT. No proof rejection. No memory problem.**

## Setup (`env.txt`, `tools.txt`)

One cloud VM, 4 cores, 15 GB RAM, no swap. Start 01:28:16 UTC 2026-10-21, budget 1.0 h, END = 02:13:16 UTC.

- C3-S tools: worktree of `132398c` (= 8dc27c3 before the author rewrite) at `/opt/c3s`, unmodified.
- CaDiCaL 3.0.1 (c6073042); cake_lpr a36874a8 (`make cake_lpr`, example prints `s VERIFIED UNSAT`);
  drat-trim lrat-check 2e3b2dc + `E2/tools/lrat-check-E2.patch`. Sanity: on {1},{-1}, LRAT `3 0 0` rejected by
  both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).
- Roots: rows of `C3WAVE2/roots.tsv` with idx 799 down to 700, in decreasing idx order (`roots.tsv`, 100 roots).
- Runner (`runner.sh`): per root, `close_tree.py base.cnf out.jsonl R --jobs 3 --caps 300,300,600 --cadopts=--sat
  --split-singles --hours S`, S = min(0.17, hours left before END).

## Per root (roots are at depth 2)

| idx | root | status | certified by depth | splits | solve s | check s |
|-----|------|--------|--------------------|--------|---------|---------|
| 799 | 0s0-4s1_1s0-5s1 | partial | d4: 373 | d2: 1 (timeout at 300 s, 91 children); d3: 7 (pre-split one-orbit, 66 children each) | 2035 | 5427 |
| 798–700 | (`roots.tsv`) | not reached | – | – | – | – |

Solve and check times are summed per node (3 jobs on 4 cores, so not wall-clock).

Root 799 timed out at 300 s and was split into 91 depth-3 children; the 7 one-orbit children (`_2`, `_3`, `_6`–`_10`)
were pre-split into 462 depth-4 nodes. The driver works through that whole layer before it checks its deadline, so
the 10-minute slice ran over: the layer (84 depth-3 + 462 depth-4 nodes, cap 600 s) was still running at 02:16, when
I stopped the runner by hand to keep the last 12 minutes for this write-up. At the stop, 373 depth-4 nodes were
certified (all UNSAT within a few seconds each); 89 depth-4 and the 84 depth-3 nodes have no record yet. The records
are all in `out.jsonl`, so a later wave can resume the root.

## Totals

| depth | certified | split | open |
|-------|-----------|-------|------|
| 2 | 0 | 1 | 99 roots not reached |
| 3 | 0 | 7 (pre-split) | 84 |
| 4 | 373 | 0 | 89 |

All 373 with `c VERIFIED` (lrat-check, E2 patch) and `s VERIFIED UNSAT` (cake_lpr).

`compose.txt`: `{"certified_nodes": 373, "class_covered": false, "uncovered_frontier_nodes": 270, ...}`; compose
recomputed the CNF sha256 of all 373 certified nodes from the base CNF and the node names. As expected, not covered.

## SAT / proof rejections / memory

None. No SATISFIABLE result, no PROOF NOT ACCEPTED, peak memory use about 8 GB of 15.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines),
`compose.txt`.
