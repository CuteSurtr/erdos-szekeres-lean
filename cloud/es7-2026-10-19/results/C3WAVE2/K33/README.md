# C3WAVE2 / K33: shard 33 of 40, wave 2, 3-fold class (m = 11, k = 7)

**Result: 5 of my 33 roots are closed. Root 6 (`0s0-2s1_3s1-6s0`) is partial; roots 7–33 were not reached.
No SAT, no proof rejection, no memory problem.** 504 nodes certified in total.

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Started 00:29:32 UTC on 2026-10-21 with H = 1.5 h, so END = 01:44:32.
Tools (`tools.txt`), as in `results/C3WAVE1/C00/README.md`:
- C3-S tools: worktree of `132398c` at `/opt/c3s`, used unmodified (live files in `/opt/work`).
- CaDiCaL 3.0.1 (c60730422e758ef1cebe7aeddf2dda31c996bf04); cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa
  (`make cake_lpr`, the example prints `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
  with `lrat-check-E2.patch` applied (it is a normal diff, so it was applied with `patch`, not `git apply`).
  Sanity check: on {1},{-1}, LRAT `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF: `gen_case.py 11 7 none -o /opt/work/base.cnf` (the script requires `-o`): `p cnf 168399 4154921`,
  sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: the 33 rows of `results/C3WAVE2/roots.tsv` with idx ≡ 33 (mod 40) (`roots.tsv`).
- `runner.sh`: one `close_tree.py ... --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S` per root,
  where S = min(0.17, hours left before END).

## Per root (roots are at depth 2)

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_6s1-9s1 | **closed** | d2: 1 | 0 | 33 | 38 |
| 2 | 0s0-2s0_1s1-5s0 | **closed** | d2: 1 | 0 | 70 | 40 |
| 3 | 0s0-2s0_4s0-8s0 | **closed** | d2: 1 | 0 | 10 | 22 |
| 4 | 0s0-2s0_6s1-7s0 | **closed** | d2: 1 | 0 | 98 | 42 |
| 5 | 0s0-2s1_1s0-8s1 | **closed** | d2: 1 | 0 | 78 | 39 |
| 6 | 0s0-2s1_3s1-6s0 | partial | d3: 37, d4: 462 | d2: 1 (UNKNOWN at 300 s, 91 children); d3: 7 one-orbit pre-split (66 children each) | 3691 | 7279 |
| 7–33 | (`roots.tsv`, from 0s0-2s1_5s0-8s0) | not reached | – | – | – | – |

Root 6: the 300 s attempt on the root timed out, and the root was split into 91 depth-3 children. 7 of them (one-orbit
layers 1, 4, 5, 7, 8, 9 and 10) were pre-split into 66 depth-4 children each. All 462 of those depth-4 nodes and 37 of the
84 two-orbit depth-3 nodes were certified. At the stop, 47 depth-3 nodes had not finished. None of them had a result yet,
so none had been split. All are resumable from `out.jsonl`.

The times are summed per node, not wall-clock; with 3 jobs sharing 4 cores, each node's time is inflated.

## Totals

- 504 certified nodes (5 at d2, 37 at d3, 462 at d4), every one with lrat-check `c VERIFIED` (E2 patch) and cake_lpr
  `s VERIFIED UNSAT`. `out.jsonl`: 504 UNSAT records, 1 UNKNOWN (root 6 at 300 s), 8 split records.
- `compose.txt`: `certified_nodes: 504, class_covered: false, uncovered_frontier_nodes: 508`. The class is not covered,
  as expected. compose recomputed the CNF sha256 of all 504 certified nodes.

## SAT / proof rejections / memory

- SAT: none. PROOF NOT ACCEPTED: none. Memory: at least 5 GB stayed available throughout (3 jobs).

## Incident (affects time only)

`close_tree.py` checks its `--hours` deadline only between whole frontier batches. Root 6's first batch held 546 nodes,
so its 10-minute slice (started 00:39:45) ran until END. At 01:44:38 I stopped the runner and the remaining solver
processes by hand (`=== KILLED` line in `driver.log`). The last record in `out.jsonl` is complete; the nodes that were
running at that moment have no record and will simply be run again on resume. Because of this, roots 7–33 were not
reached. A later wave may want a per-node deadline check (or a smaller slice for roots that split).

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines),
`compose.txt`.
