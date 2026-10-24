# C3W3 / B5: wave 3, 3-fold class (m = 11, k = 7), list B_h3pilot.tsv, shard 5 of 10

**Result: all 3 roots were started and all 3 are partial (none closed). 375 nodes were certified. There was no SAT,
no proof rejection and no memory problem.** No seeded records: all 3 roots were `untouched`.

Values: V = B5, LIST = B_h3pilot.tsv, j = 5, N = 10, LANES = 1, JOBS = 3, SLICE = 0.9, H = 3.0, Z = 640a56c2.

## What ran where

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:41:36 UTC on 2026-10-21, END 07:26:36 (start + 3 h − 15 min).

- C3-S tools: worktree of `132398c` at `/opt/c3s`, used unmodified.
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04.
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`). Its example prints `s VERIFIED UNSAT`.
- drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985, with `results/E2/tools/lrat-check-E2.patch` applied.
  Sanity check on {1},{-1}: both checkers reject `3 0 0` and both accept `3 0 1 2 0`.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).

Details are in `tools.txt`.

## Roots

`roots.tsv` holds rows 5, 15 and 25 of `B_h3pilot.tsv`, all stratum H3/two and status untouched. Seeded records: **0**.
`out.jsonl` therefore contains only new records.

## Deviation: slice enforcement (`watchdog.sh`)

`close_tree.py` checks `--hours` only between whole frontier waves. It submits the full frontier at once, and here
each root's frontier is 840 nodes: 120 depth-3 children, of which 8 one-orbit children are presplit into 91 depth-4
nodes each, giving 112 + 728. A slice of 0.9 h therefore never stopped a root. Root 1 was still running at 06:12,
34 minutes past its slice, and roots 2 and 3 would never have been reached.

At 06:13 I started `watchdog.sh`, a wrapper that leaves the tools unchanged. It kills the current root's
`close_tree.py` process tree once that root has run S hours (+30 s). `lane0.sh` then moves on to the next root.
Records already written stay in `out.jsonl`. Up to 3 in-flight nodes per kill were dropped without a record, so no
`cake_lpr: none` records exist and no recheck was needed. Actual run times:

- root 1: 04:44:24 to 06:13:03 (1.48 h, overran S = 0.9 before the watchdog existed)
- root 2: 06:13:03 to 07:07:42 (S = 0.9)
- root 3: 07:07:42 to 07:27:14 (S = 0.315, i.e. up to END)

## Per root (depth = number of layers; roots are at depth 2)

| # | root | stratum | status | certified by depth | timeouts | splits | open frontier | solve s | check s |
|---|------|---------|--------|--------------------|----------|--------|---------------|---------|---------|
| 1 | 0s0_1s0-6s0 | H3/two | partial | d4: 231 | d2: 1 (300 s) | d2: 1 (timeout → 120); d3: 8 presplit (→ 91 each) | 609 | 9073 | 6058 |
| 2 | 0s0_2s0-8s1 | H3/two | partial | d4: 94 | d2: 1 (300 s) | same shape | 746 | 6082 | 2772 |
| 3 | 0s0_3s1-6s1 | H3/two | partial | d4: 50 | d2: 1 (300 s) | same shape | 790 | 1744 | 1095 |

The open frontier is 840 minus the certified count. It is the remaining depth-4 children of the presplit one-orbit
nodes, plus all 112 two-orbit depth-3 children, none of which were attempted. Solve and check times are summed per
node, not wall clock (3 jobs on 4 cores). No depth-4 node timed out at its 600 s cap.

## Totals per stratum

| stratum | roots | closed | partial | not reached | certified | timeouts | solve s | check s |
|---------|-------|--------|---------|-------------|-----------|----------|---------|---------|
| H3/two | 3 | 0 | 3 | 0 | 375 | 3 (the roots, at 300 s) | 16899 | 9925 |

## Checks

- All 375 UNSAT records carry lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`. 0 records have `certified: false`.
- SAT: none. PROOF NOT ACCEPTED: none. Memory: no problem (peak about 9 GB used of 15).
- `compose.txt`: `certified_nodes: 375, class_covered: false, uncovered_frontier_nodes: 632`. Coverage was not
  expected, because this is 3 roots of the class. compose recomputed the CNF sha256 of every certified node.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`, `watchdog.sh`, `out.jsonl` (all new records, resumable),
`driver0.log` (last 100 lines), `summary.jsonl` (per-root counts; depth there = number of layers), `compose.txt`.
