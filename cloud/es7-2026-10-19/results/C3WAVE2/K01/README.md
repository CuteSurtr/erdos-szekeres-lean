# C3WAVE2 / K01: shard 1 of 40, 3-fold class (m = 11, k = 7)

**Result: 6 of my 34 roots are closed. Root 7 (`0s0-2s1_4`) is partial, and roots 8–34 were not reached.
No SAT, no proof rejection, no memory problem.** 126 nodes certified, each by both lrat-check (E2 patch) and cake_lpr (`s VERIFIED UNSAT`).

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 00:22:27 UTC on 2026-10-21, budget 1.5 h, runner END = 01:37:27.
- C3-S tools: worktree of `132398c` (= `8dc27c3` before the rewrite) at `/opt/c3s`, used unmodified.
- CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8 (bundled example: `s VERIFIED UNSAT`), drat-trim lrat-check 2e3b2dc with
  `E2/tools/lrat-check-E2.patch`. Sanity check on {1},{-1}: LRAT `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both (`tools.txt`).
- Base CNF `gen_case.py 11 7 none -o /opt/work/base.cnf` (the current script requires `-o`): `p cnf 168399 4154921`,
  sha256 `bf0e502e…6da` (**matches**).
- Roots: the 34 rows of `C3WAVE2/roots.tsv` with idx ≡ 1 (mod 40) (`roots.tsv`). The runner (`runner.sh`) calls
  `close_tree.py … R --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S` with S = min(0.17, hours left to END).

## Per root (roots are at depth 2)

| # | root | status | certified by depth | splits | solve s | check s | wall |
|---|------|--------|--------------------|--------|---------|---------|------|
| 1 | 0s0-1s1_2s1-5s1 | **closed** | d2: 1 | 0 | 67 | 55 | 00:25:29–00:27:33 |
| 2 | 0s0-1s1_7s1-8s1 | **closed** | d2: 1 | 0 | 69 | 51 | 00:27:34–00:29:35 |
| 3 | 0s0-2s0_3 | **closed** | d3: 120 | d2: 1 (pre-split, 120 children) | 4916 | 3587 | 00:29:35–01:17:23 |
| 4 | 0s0-2s0_4s1-7s0 | **closed** | d2: 1 | 0 | 276 | 56 | 01:17:23–01:22:56 |
| 5 | 0s0-2s0_7s0-8s1 | **closed** | d2: 1 | 0 | 255 | 53 | 01:22:56–01:28:05 |
| 6 | 0s0-2s1_1s1-4s1 | **closed** | d2: 1 | 0 | 104 | 47 | 01:28:05–01:30:38 |
| 7 | 0s0-2s1_4 | partial | d3: 1 (`0s0-2s1_4_1s0-3s0`) | d2: 1 (pre-split, 120 children); d3: 6 timeouts at 300 s (`_1`, `_3`, `_5`, `_6`, `_7`, `_8`), each split into 91 | 1842 | 41 | 01:30:38–01:42 (stopped by hand) |
| 8–34 | (`roots.tsv`) | not reached | – | – | – | – | – |

Solve and check times are summed per node (3 jobs share 4 cores, so they are not wall-clock times).
Totals: 126 certified nodes (5 at d2, 121 at d3), 6 UNKNOWN (300 s cap), 0 SAT, 0 rejected; solve 7529 s, check 3890 s.

Closed: 0s0-1s1_2s1-5s1, 0s0-1s1_7s1-8s1, 0s0-2s0_3, 0s0-2s0_4s1-7s0, 0s0-2s0_7s0-8s1, 0s0-2s1_1s1-4s1.
Partial: 0s0-2s1_4 (113 depth-3 children never attempted, 546 depth-4 children of the 6 timeouts never attempted; all records are in `out.jsonl`, so it can be resumed).

## The slice is soft

`close_tree.py` checks `--hours` only between frontier layers (`while frontier and time.time() < deadline`), and it submits the
whole layer at once. So a pre-split one-orbit root runs its full depth-3 layer of 120 children whatever S is. Root 3
(`0s0-2s0_3`) took 48 min of wall time instead of 10. Root 7 (`0s0-2s1_4`, also a one-orbit {4} root) began at 01:30:38 with S = 0.114.
Its layer of 120 children at a 300 s cap would have run far past the budget, so at 01:42 I stopped the runner, the driver and
the solver and checker processes by hand. The records already written are intact (all 140 lines of `out.jsonl` parse as JSON). The nodes in flight
(`0s0-2s1_4_9`, `_10`, `_1s0-3s1`) have no record. The tools stayed unmodified.

## compose.py

`compose.txt`: `{"certified_nodes": 126, "class_covered": false, "uncovered_frontier_nodes": 579, …}`. As expected, the class is
not covered. compose recomputed the CNF sha256 of all 126 certified nodes.

## SAT / proof rejections / memory

None. Peak use was about 8 GB of the 15 GB.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `compose.txt`.
