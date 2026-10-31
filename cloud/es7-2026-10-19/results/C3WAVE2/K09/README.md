# C3WAVE2 / K09: shard 9 of 40, 3-fold class (m = 11, k = 7)

**Result: 1 of my 34 roots is closed (`0s0-1s1_4s0-9s0`), 1 is partial (`0s0-1s1_9`), and 32 were not reached.
No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 00:23:16 UTC on 2026-10-21, budget 1.5 h, END = 01:38:16.
Tools as in `C3WAVE1/C00` (`tools.txt`): worktree of `132398c` (= 8dc27c3) at `/opt/c3s`, unmodified;
CaDiCaL 3.0.1 (c6073042); cake_lpr a36874a8 (example prints `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc
with the E2 patch (sanity check passed: `3 0 0` rejected by both, `3 0 1 2 0` accepted by both).
Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da` (matches).
Roots: rows of `C3WAVE2/roots.tsv` with idx ≡ 9 (mod 40): 34 roots (`roots.tsv`).
Runner (`runner.sh`): `close_tree.py … --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`,
S = min(0.17, hours left before END).

## Per root

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_4s0-9s0 | **closed** | d2: 1 | 0 | 241 | 48 |
| 2 | 0s0-1s1_9 | partial | d3: 83 | d2: 1 (pre-split, 120 children); d3: 8 (timeout at 300 s, 91 children each) | 9871 | 2495 |
| 3–34 | (`roots.tsv`) | not reached | – | – | – | – |

Root 2 (`0s0-1s1_9`, one-orbit layer {9}) is pre-split into 120 depth-3 children, all submitted as one batch.
`close_tree.py` checks its `--hours` deadline only between batches, so the 10-minute slice did not stop this
batch: it ran from 00:30:17 until I stopped the runner at 01:40:16, at the end of my budget. By then 91 of
the 120 children had records: 83 certified, 8 UNKNOWN at 300 s (split into 728 depth-4 nodes, not attempted).
The other 29 depth-3 children have no record (in flight or not started when the run was stopped); a resume
of this root re-attempts them. Solve and check times are summed per node, not wall-clock.

## Totals

84 certified nodes (1 at depth 2, 83 at depth 3), each with lrat-check `c VERIFIED` and cake_lpr
`s VERIFIED UNSAT`. 8 UNKNOWN (timeouts), 9 split records (1 pre-split). Largest proof 385 MB.
Solve 10,112 s, check 2,543 s in total. Memory peaked at about 6 GB used of 15 GB.

`compose.txt`: `{"certified_nodes": 84, "class_covered": false, "uncovered_frontier_nodes": 198, …}`, as expected;
compose recomputed the CNF sha256 of all 84 certified nodes.

## SAT / proof rejections / memory

None. No SATISFIABLE result, no PROOF NOT ACCEPTED, no checker printing nothing.

Closed: `0s0-1s1_4s0-9s0`. Partial: `0s0-1s1_9`.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `compose.txt`.
