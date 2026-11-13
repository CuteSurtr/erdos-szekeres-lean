# C3WAVE2 / K04: shard 4 of 40, wave 2, 3-fold class (m = 11, k = 7)

**Result: 0 of my 34 roots closed, 1 partial (`0s0-1s1_3s1-6s0`, 478 certified nodes, 68 depth-4 nodes open),
33 not reached. No SAT. No proof rejection.** The time went to one root: `close_tree.py` checks its
`--hours` deadline only between batches (one batch = the whole current frontier), so the 10-minute
slice did not stop root 1, and a VM reboot cost about 7 minutes.

## What ran where

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`), 00:21:47 to 01:51:47 UTC on 2026-10-21 (H = 1.5 h;
runner END 01:36:47). Tools as in `C3WAVE1/C00/README.md` (`tools.txt`):

- C3-S tools: worktree of `132398c` (8dc27c3 before the author rewrite) at `/opt/c3s`, unmodified; live files in `/opt/work`.
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04.
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`); the bundled example prints `s VERIFIED UNSAT`.
- drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 + `results/E2/tools/lrat-check-E2.patch`
  (normal diff, applied with `patch`). Sanity: on {1},{-1}, LRAT `3 0 0` is rejected by both checkers
  (lrat-check `c NOT VERIFIED`, cake_lpr "Checking failed"), `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none -o /opt/work/base.cnf`: `p cnf 168399 4154921`, sha256
  `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: rows of `C3WAVE2/roots.tsv` with idx ≡ 4 (mod 40): 34 roots (`roots.tsv`).
- Runner (`runner.sh`): per root `close_tree.py ... --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`, S = min(0.17, hours left before END).

## Per root (depth = number of layers; roots are at depth 2)

| # | root | status | certified by depth | splits | open | solve s | check s |
|---|------|--------|--------------------|--------|------|---------|---------|
| 1 | 0s0-1s1_3s1-6s0 | **partial** | d3: 84, d4: 394 | d2: 1 (UNKNOWN at 300 s → 91 children); d3: 7 (one-orbit, pre-split, 66 children each) | d4: 68 | 4931 | 7709 |
| 2–34 | (`roots.tsv`, idx 44 … 1324) | not reached | – | – | – | – | – |

Root 1: the root itself timed out at 300 s and was split into 91 depth-3 children: 84 two-orbit
children, all certified (300 s cap), and 7 one-orbit children (`_2`, `_4`, `_5`, `_7`, `_8`, `_9`, `_10`),
each pre-split into 66 depth-4 nodes (462). Of those, 394 were certified (600 s cap; all well under it) and
68 were still running or queued when the run was stopped. No depth-3 or depth-4 node timed out.
Solve and check times are summed per node (3 jobs on 4 cores, so not wall-clock).

Closed roots: none. Partial roots: `0s0-1s1_3s1-6s0`.

## Totals

487 records in `out.jsonl`: 478 UNSAT with `c VERIFIED` (lrat-check, E2 patch) and `s VERIFIED UNSAT`
(cake_lpr), 1 UNKNOWN (the root at 300 s), 8 split records. `summary.jsonl` (from `summary.py`) has the
per-root breakdown.

## compose.py

`compose.txt`: `{"certified_nodes": 478, "class_covered": false, "uncovered_frontier_nodes": 230, ...}`.
As expected, the class is not covered. compose recomputed the CNF sha256 of all 478 certified nodes.

## SAT / proof rejections / memory

- **SAT: none.**
- **PROOF NOT ACCEPTED: none.**
- **Memory:** used memory peaked around 8 GB of 15 GB with 3 jobs; no checker failure.

## Incidents (affect time only, not results)

1. **Slice not enforced.** `close_tree.py` checks the deadline only before a batch, and a batch is the whole
   frontier, so root 1 ran far past its 10-minute slice (00:24 to the stop). The tool was used unmodified, as required.
   A later wave may want a deadline check inside the batch loop, or a per-root wall-clock kill.
2. **VM reboot at about 00:53–01:00 UTC.** The machine rebooted (uptime 0 at 01:00), killing the runner during
   root 1. `out.jsonl` was intact (all 288 lines valid JSON). The runner was restarted at 01:00:37 and resumed from
   `out.jsonl` (marked `=== RESTART` in `driver.log`); the restarted call got a new 0.17 h slice.
3. **Stopped by hand at 01:39 UTC** (past END, batch still running; marked `=== STOPPED` in `driver.log`).
   The nodes in flight were lost; their records are absent, so a later wave resumes them from `out.jsonl`.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines),
`summary.py`, `summary.jsonl`, `compose.txt`.
