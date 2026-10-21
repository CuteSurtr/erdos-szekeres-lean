# C3WAVE2 / K18: shard 18 of 40, wave 2, 3-fold class (m = 11, k = 7)

**Result: 0 of my 34 roots closed. Root 1 (`0s0-1s1_5s0-8s1`) is partial: 510 nodes certified, 36 depth-4 nodes still open. Roots 2–34 were not reached. No SAT. No proof rejection. No memory problem.**

## What ran where

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 00:24:58 UTC on 2026-10-21 (epoch 1792542298), budget 1.5 h, runner END 01:39:58.
Tools as in `results/C3WAVE1/C00/README.md` (`tools.txt`):

- C3-S tools: worktree of `132398c` (8dc27c3 before the author rewrite) at `/opt/c3s`, unmodified; `/opt/work` writable.
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04.
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`); the bundled example prints `s VERIFIED UNSAT`.
- drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 + `results/E2/tools/lrat-check-E2.patch`.
  Sanity check: on {1},{-1}, LRAT `3 0 0` is rejected by both (lrat-check `c NOT VERIFIED`, cake_lpr `pivot must be non-zero`), and `3 0 1 2 0` is accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`).
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: rows of `C3WAVE2/roots.tsv` with idx ≡ 18 (mod 40): 34 roots (`roots.tsv`).
- Runner (`runner.sh`): K00's runner with START = 1792542298; `close_tree.py ... --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`, S = min(0.17, hours left).

## Per root (depth = number of layers; roots are at depth 2)

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_5s0-8s1 | partial | d3: 84, d4: 426 | d2: 1 (timeout at 300 s, 91 children); d3: 7 (pre-split, 66 children each) | 4528 | 7767 |
| 2–34 | (`roots.tsv`) | not reached | – | – | – | – |

Root 1 timed out at 300 s at depth 2 and was split into 91 depth-3 children: 84 certified at the 300 s cap, 7 one-orbit children
(`_2`, `_3`, `_4`, `_6`, `_7`, `_9`, `_10`) pre-split into 66 depth-4 children each (462). Six of them (`_2` … `_9`) are fully
certified (66/66); `_10` has 30 of 66 certified, so 36 depth-4 nodes remain open. No node timed out at depth 3 or 4: the
largest depth-4 solve time was 60 s against the 600 s cap. Solve and check times are summed per node (depth 3: 1 296 s / 1 717 s
for the 84; depth 4: 2 932 s / 6 050 s for the 426; plus 300 s for the depth-2 timeout). With 3 jobs on 4 cores they are not wall-clock.

Totals: 510 certified nodes, all with `c VERIFIED` (lrat-check, E2 patch) and `s VERIFIED UNSAT` (cake_lpr); 1 UNKNOWN (the root at 300 s);
519 records in `out.jsonl` (resumable).

## Why only one root

`close_tree.py` checks `--hours` only between batches. The 10-minute slice ran out while root 1's batches (91 depth-3 nodes, then 462
depth-4 nodes, each solved and checked by both checkers) were still running, so the driver did not stop at 0.17 h.
Root 1 took all the budget. At 01:42:37, past the runner's END, I stopped the driver and its workers by hand to keep the last 12 minutes
for this report. Records are written per node, so nothing certified was lost. The node being checked at the kill has no record and is
counted as open. A later wave can resume root 1 from `out.jsonl`.

## Incident (affects time only, not results)

At about 01:01 UTC the VM restarted (uptime 0), which killed the runner during root 1. `/opt` survived: `out.jsonl` was intact
(289 records, all valid JSON), and the tools and base CNF were still in place. The runner was relaunched unchanged at 01:02:07
(marked `=== VM RESTART` in `driver.log`), and `close_tree.py` resumed root 1 from the records. About 12 minutes were lost.

## compose.py

`compose.txt`: `{"certified_nodes": 510, "class_covered": false, "uncovered_frontier_nodes": 198, ...}`. As expected, the class
is not covered. compose recomputed the CNF sha256 of all 510 certified nodes from the base CNF and the node names.

## SAT / proof rejections / memory

- **SAT: none.**
- **PROOF NOT ACCEPTED: none.**
- **Memory: no problem** (about 8 GB used with 3 jobs).

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `compose.txt`.
