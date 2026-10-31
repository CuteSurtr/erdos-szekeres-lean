# C3WAVE2 / K37: shard 37 of 40, wave 2, 3-fold class (m = 11, k = 7)

**Result: 4 of my 33 roots are closed. Root 5 (`0s0-2s1_1s1-10s1`) is partial, and roots 6–33 were not reached. No SAT. No proof rejection. No memory problem.**

## Setup (`tools.txt`, `env.txt`)

One cloud VM, 4 cores, 15 GB RAM, no swap. Start 00:31:20 UTC on 2026-10-21, budget 1.5 h, END = 01:46:20 UTC.

- C3-S tools: worktree of commit `132398c` (8dc27c3 before the author rewrite) at `/opt/c3s`, unmodified.
- CaDiCaL 3.0.1 (c6073042); cake_lpr a36874a8 (`make cake_lpr`, example prints `s VERIFIED UNSAT`);
  drat-trim lrat-check 2e3b2dc + `results/E2/tools/lrat-check-E2.patch`. Sanity check: on {1},{-1}, `3 0 0`
  is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…cdd6da` (matches).
- Roots: rows of `C3WAVE2/roots.tsv` with idx ≡ 37 (mod 40): 33 roots (`roots.tsv`).
- `runner.sh`: per root, `close_tree.py ... --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours min(0.17, left)`.

## Per root (roots are at depth 2)

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_7s0-9s0 | **closed** | d2: 1 | 0 | 30 | 39 |
| 2 | 0s0-2s0_1s1-7s0 | **closed** | d2: 1 | 0 | 49 | 36 |
| 3 | 0s0-2s0_4s1-10s0 | **closed** | d2: 1 | 0 | 16 | 30 |
| 4 | 0s0-2s0_6s1-9s0 | **closed** | d2: 1 | 0 | 104 | 45 |
| 5 | 0s0-2s1_1s1-10s1 | partial | d3: 21, d4: 462 | d2: 1 (UNKNOWN at 300 s, 91 children); d3: 7 (one-orbit pre-split, 66 children each) | 3844 | 7523 |
| 6–33 | (`roots.tsv`) | not reached | – | – | – | – |

Solve and check times are summed per node, not wall clock (3 jobs share 4 cores).

Root 5: the root timed out at the 300 s cap and was split into 91 depth-3 children. The 7 one-orbit
children (`_3` … `_9`) were pre-split into 7 × 66 = 462 depth-4 nodes, all certified. Of the other 84
depth-3 children, 21 were certified when I stopped the driver at END; 63 have no record (open, still in
the in-flight level). The driver checks `--hours` only between levels, so this level ran past the 10-minute
slice from 00:39 until END, where I killed the runner and its solver processes by hand (01:47 UTC). The killed
in-flight nodes left no records; `out.jsonl` is resumable.

## Totals

487 certified nodes (d2: 4, d3: 21, d4: 462), every one with lrat-check `c VERIFIED` and cake_lpr
`s VERIFIED UNSAT`. Records: 487 UNSAT, 1 UNKNOWN (root 5 at 300 s), 8 split records.

`compose.py` (`compose.txt`): `certified_nodes: 487, class_covered: false, uncovered_frontier_nodes: 525`, as
expected for one shard; it recomputed the CNF sha256 of all 487 certified nodes.

## SAT / rejections / memory

No SAT FOUND, no PROOF NOT ACCEPTED, no memory problem (about 6 GB used at peak observation).

Closed roots: 0s0-1s1_7s0-9s0, 0s0-2s0_1s1-7s0, 0s0-2s0_4s1-10s0, 0s0-2s0_6s1-9s0.
Partial: 0s0-2s1_1s1-10s1.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl`, `driver.log` (last 200 lines), `compose.txt`, `README.md`.
