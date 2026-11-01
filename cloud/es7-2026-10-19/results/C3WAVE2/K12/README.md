# C3WAVE2 / K12: shard 12 of 40, 3-fold class (m = 11, k = 7)

**Result: 1 of my 34 roots closed, 1 partial, 32 not reached. No SAT. No proof rejection. No memory problem.**
536 nodes certified, every one with lrat-check `c VERIFIED` (E2 patch) and cake_lpr `s VERIFIED UNSAT`.

## Setup (`tools.txt`, `env.txt`)

One cloud VM, 4 cores, 15 GB RAM, no swap. Start 00:23:14 UTC on 2026-10-21, budget 1.5 h; runner END 01:38:14.

- C3-S tools: worktree of `132398c` (formerly 8dc27c3) at /opt/c3s, unmodified.
- CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8 (`make cake_lpr`; its example prints `s VERIFIED UNSAT`),
  drat-trim lrat-check 2e3b2dc with `lrat-check-E2.patch` (a normal diff, applied with `patch`).
  Sanity check on {1},{-1}: `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF: `gen_case.py 11 7 none -o /opt/work/base.cnf` (this version of the script needs `-o`):
  `p cnf 168399 4154921`, sha256 `bf0e502e…d6da`, matches.
- Roots: rows of `C3WAVE2/roots.tsv` with idx ≡ 12 (mod 40): 34 roots (`roots.tsv`).
- `runner.sh`: the given `close_tree.py … --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`,
  with S = min(0.17, hours left before END).

## Per root (roots are at depth 2)

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_4s1-6s1 | **closed** | d2: 1 | 0 | 28 | 32 |
| 2 | 0s0-1s1_9s1-10s0 | partial | d3: 73, d4: 462 | d2: 1 (UNKNOWN at 300 s); d3: 7 (pre-split, one-orbit) | 4607 | 7742 |
| 3–34 | (`roots.tsv`) | not reached | – | – | – | – |

Solve and check times are summed per node (3 jobs on 4 cores), not wall-clock.

Root 2: the root timed out at 300 s and was split into 91 depth-3 children. The 7 one-orbit children
(`…_2` to `…_8`) were pre-split into 66 depth-4 children each, and all 462 are certified. Of the
84 two-orbit depth-3 children, 73 are certified and 11 were never finished (they were in flight or queued when I stopped):
`…_6s0-7s1, _6s1-7s0, _6s1-7s1, _6s0-8s0, _6s0-8s1, _6s1-8s0, _6s1-8s1, _7s0-8s0, _7s0-8s1, _7s1-8s0, _7s1-8s1`
(prefix `0s0-1s1_9s1-10s0`). A later wave can resume from `out.jsonl`.

Totals: 536 certified nodes (d2: 1, d3: 73, d4: 462), 1 UNKNOWN record (root 2 at 300 s), 8 split records.

## Why only two roots: the slice is not enforced

`close_tree.py` checks `--hours` only between levels of the tree: it submits a whole level as one batch
and waits for all of it. So root 2's 10-minute slice (started 00:26:47) did not stop the run; its depth-3/4
batch of 553 nodes ran until I stopped it by hand at about 01:40 (wall-time budget; the runner's END had passed
and it would have started no further root). I kept the command exactly as given. Records are written per node, so nothing
finished was lost; only the in-flight nodes were killed. For the rest of the wave: with these tools, a root
that is not closed at depth 2 overruns its slice by a whole level, and this runner reaches few roots.

## SAT / rejections / memory

- SAT: none. Proof rejections: none (536/536 accepted by both checkers). Memory: peak about 5 GB used of 15; no problem.

## compose.py

`compose.txt`: `{"certified_nodes": 536, "class_covered": false, "uncovered_frontier_nodes": 172, ...}`, as expected
(this machine holds 1/40 of the roots); it recomputed the CNF sha256 of all 536 certified nodes.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `compose.txt`.
