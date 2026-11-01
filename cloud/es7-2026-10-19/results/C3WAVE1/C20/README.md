# C3WAVE1 / C20: machine 20 of 24, wave 1, 3-fold class (m = 11, k = 7)

## Result

- **10 of my 68 roots are fully closed.** 6 roots were certified directly at depth 2. 2 were
  closed through all their children, recursively. 1 was split and is partly done. 57 were not started.
- **1,230 nodes certified.** Each was accepted by both cake_lpr (`s VERIFIED UNSAT`) and
  lrat-check with the E2 patch (`c VERIFIED`).
- **No SAT.**
- **No real proof rejection.** The one "PROOF NOT ACCEPTED" was cake_lpr killed by the memory
  limit. The node passed both checkers when re-run alone (details below).
- `compose.py` reports `class_covered: false`, as expected for one shard of 24.

## What ran where

- One cloud VM: 4 cores, 15 GB RAM, memory cgroup limit 14.3 GB, no swap (`env.txt`).
- Run from 07:35 to 11:35 UTC on 2026-10-20. The driver ran from 07:38 to 11:13 UTC; the
  watchdog stopped it at the time budget.
- C3-S and C3a tools: a git worktree of `8dc27c3` at `/opt/c3s`, unmodified. `/opt/work` was
  writable, so no path change was needed.
- Tool commits (`tools.txt`):
  - cadical: CaDiCaL 3.0.1, c60730422e758ef1cebe7aeddf2dda31c996bf04.
  - cake_lpr: a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, `make cake_lpr`. The bundled example
    printed `s VERIFIED UNSAT`.
  - lrat-check: drat-trim 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with
    `results/E2/tools/lrat-check-E2.patch` applied.
- Base CNF: `gen_case.py 11 7 none` gives `p cnf 168399 4154921`, sha256
  `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: the depth-2 nodes with index ≡ 20 (mod 24), 68 nodes, from the SHARD expression in
  `close_tree.py` (`roots.txt`).
  - They are identical to the same selection from `manifest_depth2.tsv`.
  - The sha256 of the manifest's name list matches `5412782c…`.
- How roots were run (`run_roots.sh`):
  - One root at a time, in order:
    `close_tree.py base.cnf out.jsonl ROOT --caps 300,300,600 --cadopts=--sat --split-singles --hours H`,
    with one shared `out.jsonl`.
  - `--jobs 4` until 07:53, then `--jobs 3` (see below).
- Commits: `out.jsonl` was written in this directory and committed from a separate worktree, so
  that `pull --autostash` never replaced the file while the driver had it open.

## Per root (roots that were started)

"open" = nodes in the frontier that were not yet decided (tried or not).

| root | status | certified by depth | split by depth | open by depth | solve s | check s |
|---|---|---|---|---|---|---|
| 0s0-1s0_2s1-3s0 | closed | d2: 1 | - | - | 108 | 41 |
| 0s0-1s0_3s0-7s1 | closed | d2: 1 | - | - | 57 | 43 |
| 0s0-1s0_4s0-6s0 | closed | d2: 1 | - | - | 5 | 22 |
| 0s0-1s0_5s0-6s1 | closed | d2: 1 | - | - | 86 | 46 |
| 0s0-1s0_6s0-9s0 | closed | d2: 1 | - | - | 6 | 22 |
| 0s0-1s0_8s0-10s0 | closed | d2: 1 | - | - | 6 | 24 |
| 0s0-1s1_2s0-6s1 | closed | d3: 84, d4: 462 | d2: 1, d3: 7 | - | 5178 | 9440 |
| 0s0-1s1_3s0-10s0 | closed | d3: 84, d4: 462 | d2: 1, d3: 7 | - | 5616 | 9458 |
| 0s0-1s1_3s1-8s0 | closed | d2: 1 | - | - | 228 | 36 |
| 0s0-1s1_4s1-7s1 | closed | d2: 1 | - | - | 35 | 22 |
| 0s0-1s1_5s1-9s0 | open | d4: 130 | d2: 1, d3: 7 | d3: 84, d4: 332 | 1244 | 2155 |

The 57 roots after `0s0-1s1_5s1-9s0` in `roots.txt` were not started. Per-root wall time:

- roots 1 to 6: about 0.5 to 2.5 min each;
- `0s0-1s1_2s0-6s1`: 80 min;
- `0s0-1s1_3s0-10s0`: 88 min;
- `0s0-1s1_3s1-8s0`: 4.4 min;
- `0s0-1s1_4s1-7s1`: 1 min;
- `0s0-1s1_5s1-9s0`: 23 min so far, still open.

Solve and check times are CPU-time sums over nodes.

## Per depth, over all roots

"open" counts nodes that are not decided, including the 57 roots not started (depth 2) and the
untried children of the open root.

| depth | certified | split | open |
|---|---|---|---|
| 2 | 8 | 3 | 57 |
| 3 | 168 | 21 | 84 |
| 4 | 1054 | 0 | 332 |

- 3 nodes hit the 300 s cap and were split: the three depth-2 roots.
- The 21 depth-3 splits are `--split-singles` presplits of single-orbit layers.

## SAT

None.

## Proof rejection (memory, not real)

At 07:52, `0s0-1s1_2s0-6s1_3_5` was reported "PROOF NOT ACCEPTED" (`cake_lpr: none`).

- dmesg shows a memory-cgroup oom-kill of that cake_lpr process: anon-rss 4.07 GB, with 4 jobs
  running.
- I stopped the driver and re-ran the node alone. The CNF sha256 was the same (`ddba8d04…`).
- CaDiCaL returned UNSAT in 3.2 s, with a 652,929 B proof. lrat-check printed `c VERIFIED` and
  cake_lpr printed `s VERIFIED UNSAT`.
- I resumed with `--jobs 3`. The driver re-solved the node, and it is certified in `out.jsonl`.
- There were no more oom-kills.

## Another incident

The driver's first attempt at root `0s0-1s0_2s1-3s0` (07:38 to 07:41) exited without writing
any record, most likely killed by a stray `pkill` of mine. After the restart at 07:53, that
root was certified in 108 s.

## compose.py

```
{"certified_nodes": 1230, "class_covered": false, "uncovered_frontier_nodes": 395, "uncovered_sample": ["0s0", "0s0-1s0_2", "0s0-1s0_3", "0s0-1s0_4", "0s0-1s0_5", "0s0-1s0_6", "0s0-1s0_7", "0s0-1s0_8", "0s0-1s0_9", "0s0-1s0_10"]}
```

## Files

- `out.jsonl`: all records (resumable).
- `driver.log`: driver output and notes.
- `roots.txt`: the 68 roots with their indices.
- `summary.md`: the full per-root table, from `summarize.py`, run from C3-S/tools of 8dc27c3.
- `compose.txt`: the output of `compose.py`.
- `env.txt`, `tools.txt`, `run_roots.sh`.
