# C3WAVE2 / K28: shard 28 of 40, 3-fold class (m = 11, k = 7)

**Result: 0 of my 34 roots closed. 1 partial: `0s0-1s1_6s0-8s1`, with 489 certified nodes and 57 open leaves. 33 not reached. No SAT. No proof rejection.**

## Setup (`tools.txt`, `env.txt`)

One cloud VM, 4 cores, 15 GB RAM, no swap. Start 00:29:28 UTC on 2026-10-21, END = start + 1.5 h − 15 min = 01:44:28.
- C3-S tools: worktree of `132398c` (8dc27c3 before the rewrite) at /opt/c3s, used unmodified.
- CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8 (example prints `s VERIFIED UNSAT`), and lrat-check 2e3b2dc with the E2 patch. Sanity check: `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da` (matches).
- Roots: rows of `C3WAVE2/roots.tsv` with idx ≡ 28 (mod 40), 34 roots (`roots.tsv`). The runner is `runner.sh`, the same as K00's apart from END.

## Per root

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_6s0-8s1 | **partial** | d3: 69, d4: 420 | d2: 1 (UNKNOWN at 300 s); d3: 7 (pre-split, 66 children each) | 4737 | 7527 |
| 2–34 | (`roots.tsv`) | not reached | – | – | – | – |

Root 1: its 91 depth-3 children are 84 leaves plus 7 single-orbit layers ({2},{3},{4},{5},{7},{9},{10}). Those 7 are pre-split into 462 depth-4 leaves. 69/84 depth-3 and 420/462 depth-4 leaves are certified, which leaves **57 leaves open, all never attempted**. No node timed out below the root: every attempted child was certified, the slowest solve took 67 s, and most took about 5 s. So the root looks closable in about 15 to 20 more minutes. Solve and check times are summed per node, with 3 jobs sharing 4 cores.

Totals: 490 solver records, 489 certified (each `c VERIFIED` and `s VERIFIED UNSAT`), 1 UNKNOWN (the root at 300 s).

## Why only one root

1. **The slice overran.** `close_tree.py` checks `--hours` only between batches. Its first batch is the whole pre-split frontier of the root (546 leaves), so the 10-minute slice (`--hours 0.17`) did not stop the root. It ran from 00:31:54 until I stopped it at END. Other machines with large pre-split roots will see the same thing.
2. **Worker restart.** About 01:20 the session's worker process restarted and killed the runner (log up to then: `driver_run0.log`). `out.jsonl` was intact (every line parses), so I restarted the same runner at 01:22:28 with the same END. It resumed root 1 from its records.
3. At END (01:44:54) the driver was still in that batch, so I killed it (SIGTERM/SIGKILL) to leave time for the wrap-up. Nodes in flight were not recorded and stay open.

## compose.py (`compose.txt`)

`{"certified_nodes": 489, "class_covered": false, "uncovered_frontier_nodes": 219, ...}`. As expected, the class is not covered. compose recomputed the CNF sha256 of all 489 certified nodes.

## SAT / rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: no problems (about 5 GB used with 3 jobs).

Closed roots: none. Partial: `0s0-1s1_6s0-8s1`. Not reached: idx 68, 108, …, 1348 of `roots.tsv` (rows 2–34).

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (resumable), `driver.log` (tail 200, both runs), `driver_run0.log` (the log of the first run, before the restart), `compose.txt`.
