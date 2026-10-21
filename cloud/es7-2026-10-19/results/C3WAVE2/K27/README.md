# C3WAVE2 / K27: shard 27 of 40, wave 2, 3-fold class (m = 11, k = 7)

**Result: 4 of my 34 roots are closed, 1 is partial (`0s0-2s1_1s0-4s1`), 29 were not reached. No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 00:29:30 UTC 2026-10-21, budget 1.5 h, END = 01:44:30.
Tools as in `results/C3WAVE1/C00/README.md` (`tools.txt`):
- C3-S tools: worktree of commit `132398c` at /opt/c3s, unmodified.
- CaDiCaL 3.0.1 (c6073042); cake_lpr a36874a8 (`make cake_lpr`, example prints `s VERIFIED UNSAT`);
  drat-trim lrat-check 2e3b2dc + `lrat-check-E2.patch`. Sanity check: on {1},{-1}, LRAT `3 0 0` rejected by both, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da` (matches).
- Roots: rows of `C3WAVE2/roots.tsv` with idx ≡ 27 (mod 40): 34 roots (`roots.tsv`).
- `runner.sh` (the K00 runner with my start time): `close_tree.py … R --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`, S = min(0.17, hours to END).

## Per root (roots are at depth 2)

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_6s0-7s0 | **closed** | d2: 1 | 0 | 31 | 33 |
| 2 | 0s0-2s0_1s0-9s0 | **closed** | d2: 1 | 0 | 174 | 49 |
| 3 | 0s0-2s0_4s0-10s0 | **closed** | d2: 1 | 0 | 63 | 41 |
| 4 | 0s0-2s0_6s0-7s0 | **closed** | d2: 1 | 0 | 7 | 19 |
| 5 | 0s0-2s1_1s0-4s1 | partial | d3: 32, d4: 462 | d2: 1 (timeout at 300 s, 91 children); d3: 7 (one-orbit pre-split, 66 children each) | 3556 (incl. 300 s UNKNOWN at d2) | 7457 |
| 6–34 | (`roots.tsv`) | not reached | – | – | – | – |

Root 5: of its 91 depth-3 children, 7 one-orbit layers were pre-split into 462 depth-4 nodes, all 462 certified;
of the 84 two-orbit depth-3 children, 32 were certified and 52 were still open (not attempted) when the runner was stopped.
So the remaining frontier of root 5 is 52 depth-3 nodes; its records are in `out.jsonl` for a later wave to resume.

Note on slices: `close_tree.py` checks its `--hours` deadline only between layer batches, so root 5 (started 00:38:35 with a
10-minute slice) kept running its batch until I stopped the runner at END (01:44:30). This used the rest of my budget on root 5,
which is why roots 6–34 were not reached. Solve and check times are summed per node, not wall-clock (3 jobs on 4 cores).

## Totals

498 certified nodes (d2: 4, d3: 32, d4: 462), all with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.
1 UNKNOWN record (root 5 at 300 s, then split). Largest proof 339 MB (not committed). Sum solve 3,532 s, check 7,599 s over certified nodes.

`compose.py` (`compose.txt`): `certified_nodes: 498, class_covered: false` (expected: one shard of 40); it recomputed the CNF sha256 of every certified node.

## SAT / rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: no problem seen (about 1–2 GB used at checks).

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `compose.txt`.
