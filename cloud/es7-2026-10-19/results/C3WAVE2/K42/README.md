# C3WAVE2 / K42: roots idx 899 down to 800 (3-fold class, m = 11, k = 7)

**Result: 1 root closed (`0s0-4s1_5s1-9s1`), 2 partial (`0s0-4s1_6`, `0s0-4s1_5s1-9s0`), 97 not reached
(idx 896 down to 800). No SAT. No proof rejection. No memory problem.** 172 certified nodes in all.

## Setup (`tools.txt`, `env.txt`)

4 cores, 15 GB RAM, no swap. Start 01:21:13 UTC on 2026-10-21, H = 1.0 h, END = 02:06:13.
- C3-S tools: worktree of 132398c at /opt/c3s, unmodified.
- CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8 (`make cake_lpr`; its example prints `s VERIFIED UNSAT`),
  drat-trim lrat-check 2e3b2dc with `results/E2/tools/lrat-check-E2.patch`. Sanity check: on {1},{-1}, LRAT `3 0 0`
  is rejected by both checkers (`c NOT VERIFIED`; cake_lpr no `s VERIFIED UNSAT`), `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da` (matches).
- Roots: `roots.tsv`, rows of `C3WAVE2/roots.tsv` with idx 899 down to 800, decreasing (100 roots).
- Runner `runner.sh`: `close_tree.py … --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`,
  S = min(0.17, hours left before END).

## Per root (depth = number of layers; roots are at depth 2)

| idx | root | status | certified by depth | splits | solve s | check s |
|-----|------|--------|--------------------|--------|---------|---------|
| 899 | 0s0-4s1_6 | partial | d3: 5 | d2: 1 (pre-split, 120 children); d3: 8 (timeout at 300 s, 91 children each) | 2766 | 158 |
| 898 | 0s0-4s1_5s1-9s1 | **closed** | d2: 1 | 0 | 144 | 45 |
| 897 | 0s0-4s1_5s1-9s0 | partial | d4: 166 | d2: 1 (timeout at 300 s, 91 children); d3: 7 (pre-split, one-orbit) | 1154 | 2436 |
| 896–800 | (`roots.tsv`) | not reached | – | – | – | – |

Totals: 172 certified nodes, each with `c VERIFIED` (lrat-check) and `s VERIFIED UNSAT` (cake_lpr);
9 UNKNOWN records at 300 s (all split). Solve and check times are summed per node, not wall clock.

Closed: `0s0-4s1_5s1-9s1`. Partial: `0s0-4s1_6`, `0s0-4s1_5s1-9s0` (their records stay in `out.jsonl`
for resumption; their unattempted nodes are re-derived by `close_tree.py` on resume).

## compose.py (`compose.txt`)

`{"certified_nodes": 172, "class_covered": false, "uncovered_frontier_nodes": 395, …}`; as expected, not covered.
compose recomputed the CNF sha256 of all 172 certified nodes.

## Incidents (affect time only, not results)

1. ~01:40 the session's VM was restarted (uptime 0 at 01:44); the runner and all solver processes were killed
   during root 1 (`0s0-4s1_6`, started 01:26:54, its slice would have ended 01:37). /opt/work survived, all
   flushed records are intact. Since root 1 had had its slice, I restarted the runner at 01:44:15 with `SKIP=1`
   (the only change to `runner.sh`: it skips the first SKIP roots), starting with root 2 (`driver.log` RESTART line).
   The unfinished depth-3 batch of root 1 (107 of the 120 pre-split children) was not attempted.
2. `close_tree.py` checks `--hours` only between level batches, so root 3's depth-4 batch ran past its slice
   and past END. At 02:11:16 I stopped the driver by hand to leave time for this write-up (STOPPED line in `driver.log`);
   the nodes of that batch without a record are left for a later wave.
3. While building, a stray `lrat-check.c` was created by a mis-directed `patch` in the checkout; it was deleted before
   any commit, and lrat-check was then built cleanly in /opt/drat-trim.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl`, `driver.log` (last 200 lines), `compose.txt`.
