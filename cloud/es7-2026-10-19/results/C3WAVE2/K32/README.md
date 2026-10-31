# C3WAVE2 / K32: shard 32 of 40, wave 2, 3-fold class (m = 11, k = 7)

**Result: 0 of my 33 roots closed. Root 1 (`0s0-1s1_6s1-8s0`) is partial, with 416 certified nodes. Roots 2–33 were
not reached. No SAT. No proof rejections. No memory problems.** The worker process was restarted twice during the run, and both restarts killed the driver. The run was resumed after the first restart. The second restart came right at END, so the run was not resumed.

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 00:29:29 UTC 2026-10-21. END = 01:44:29 UTC (start + 1.5 h − 15 min).
Tools (`tools.txt`): a worktree of commit `132398c` at `/opt/c3s`, used unmodified. CaDiCaL 3.0.1 (c6073042). cake_lpr a36874a8, whose example prints
`s VERIFIED UNSAT`. lrat-check at drat-trim 2e3b2dc with the E2 patch. The sanity check passed: `3 0 0` was rejected by both checkers and `3 0 1 2 0` was accepted by both.
Base CNF `gen_case.py 11 7 none -o …`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da`, which matches.
Roots: the rows of `C3WAVE2/roots.tsv` with idx ≡ 32 (mod 40), 33 roots (`roots.tsv`). Runner: `runner.sh` (`--jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours min(0.17, left)`).

## Per root

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_6s1-8s0 | **partial** | d3: 84, d4: 332 | d2: 1 (timeout at 300 s → 91 children); d3: 7 (pre-split one-orbit, 66 children each) | 4888 | 6939 |
| 2–33 | (`roots.tsv`) | not reached | – | – | – | – |

The root timed out at 300 s and was split into 91 depth-3 children: 84 two-orbit children and 7 one-orbit children. The one-orbit children (`_2,_3,_4,_5,_7,_9,_10`) were pre-split into
462 depth-4 nodes. All 84 depth-3 nodes are certified. 332 of the 462 depth-4 nodes are certified, and the other 130 are open (never attempted, or killed while in flight).
None timed out. Solve and check times are summed per node and are not wall-clock.

**The 10-minute slice did not bound the root.** `close_tree.py` checks `--hours` only between layers. After the split, the
84 + 462 children form a single batch, so the slice ran until the driver was killed: about 70 minutes of compute in total. A later wave can resume this root from
`out.jsonl` (all records are kept).

Totals: 425 records. 416 nodes are certified, each with `c VERIFIED` (lrat-check E2) and `s VERIFIED UNSAT` (cake_lpr). 1 node was UNKNOWN at 300 s (the root), with 1 split and 7 pre-splits.

## compose.py

`compose.txt`: `{"certified_nodes": 416, "class_covered": false, "uncovered_frontier_nodes": 292, ...}`. As expected, the class is not covered.
compose.py recomputed the CNF sha256 of all 416 certified nodes from the base CNF.

## SAT / proof rejections / incidents

- SAT: none. PROOF NOT ACCEPTED: none. Memory: peak use was about 9 of 15 GB with 3 jobs, and there were no checker failures.
- Incident 1, about 00:58 UTC: the session's worker process restarted, and all processes, including the `setsid` driver, were killed. 200 records had been written by then, and all were valid JSON.
  The driver was resumed at 00:59:05 on the same `out.jsonl` (`driver_run1.log` is the log up to that point).
  In-flight nodes were lost and re-solved. There are no duplicate certified records.
- Incident 2, between 01:43:10 and 01:43:26 UTC: a second restart killed the driver. END (01:44:29) had been reached, so it was not restarted (`driver_run2.log`).
  These incidents affected time only, not results.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines),
`driver_run1.log`, `driver_run2.log`, `compose.txt`.
