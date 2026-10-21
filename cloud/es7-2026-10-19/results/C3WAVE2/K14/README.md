# C3WAVE2 / K14: shard 14 of 40, wave 2, 3-fold class (m = 11, k = 7)

**Result: 13 of my 34 roots are closed, root 14 (`0s0-3s1_2s1-10s1`) is partial, and roots 15–34 were not reached. No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Started 00:24:55 UTC on 2026-10-21, budget 1.5 h, END = start + 75 min = 01:39:55.
Tools as in `results/C3WAVE1/C00/README.md`, details in `tools.txt`:

- C3-S tools: worktree of `132398c` (= 8dc27c3 before the author rewrite) at `/opt/c3s`, unmodified.
- CaDiCaL 3.0.1 (c6073042); cake_lpr a36874a8 (`make cake_lpr`), its example prints `s VERIFIED UNSAT`;
  drat-trim lrat-check 2e3b2dc + `lrat-check-E2.patch`. Sanity: on {1},{-1}, `3 0 0` is rejected by both
  (`c NOT VERIFIED`; cake_lpr "pivot must be non-zero"), `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…0cdd6da` (matches).
- Roots: rows of `C3WAVE2/roots.tsv` with idx ≡ 14 (mod 40): 34 roots (`roots.tsv`). Runner: `runner.sh` (10-minute slice per root, `--jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles`).

## Per root

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_4s1-9s0 | **closed** | d2: 1 | 0 | 172 | 43 |
| 2 | 0s0-2s0_10 | **closed** | d3: 120 | d2: 1 (pre-split) | 2240 | 2456 |
| 3 | 0s0-2s0_3s1-10s0 | **closed** | d2: 1 | 0 | 10 | 17 |
| 4 | 0s0-2s0_5s0-9s0 | **closed** | d2: 1 | 0 | 22 | 23 |
| 5 | 0s0-2s0_8s1-10s1 | **closed** | d2: 1 | 0 | 7 | 18 |
| 6 | 0s0-2s1_3s0-10s1 | **closed** | d2: 1 | 0 | 61 | 33 |
| 7 | 0s0-2s1_4s1-10s0 | **closed** | d2: 1 | 0 | 56 | 32 |
| 8 | 0s0-2s1_6s0-9s0 | **closed** | d2: 1 | 0 | 31 | 29 |
| 9 | 0s0-3s0_1s0-10s1 | **closed** | d2: 1 | 0 | 17 | 24 |
| 10 | 0s0-3s0_2s0-7s0 | **closed** | d2: 1 | 0 | 67 | 37 |
| 11 | 0s0-3s0_4s1-7s1 | **closed** | d2: 1 | 0 | 17 | 26 |
| 12 | 0s0-3s0_6s1-8s1 | **closed** | d2: 1 | 0 | 10 | 24 |
| 13 | 0s0-3s1_1s0-6s0 | **closed** | d2: 1 | 0 | 127 | 37 |
| 14 | 0s0-3s1_2s1-10s1 | partial | d4: 250 | d2: 1 (UNKNOWN at 300 s → 91 children); d3: 7 one-orbit pre-split (66 children each) | 1744 | 3790 |
| 15–34 | (`roots.tsv`) | not reached | – | – | – | – |

Solve/check times are per-node sums (3 jobs on 4 cores), not wall clock.

Root 14: the root timed out at the 300 s cap and was split into 91 depth-3 children; the 7 one-orbit ones were pre-split into 462 depth-4 nodes. At the stop, 250 of those depth-4 nodes were certified; 212 depth-4 nodes and the 84 other depth-3 children are open (not yet attempted). Its records stay in `out.jsonl` for a later wave to resume.

Note on the slice: `close_tree.py` checks `--hours` only between batches, so a slice can overrun. Root 2 ran 26 min and root 14 ran from 01:08:57 past END. At 01:43:33 I killed the runner and the driver by hand to keep the final 12 minutes; the in-flight batch of root 14 (a few depth-4 nodes) is lost and will be redone on resume. Nothing recorded is affected.

## Totals

- 382 certified nodes (d2: 12, d3: 120, d4: 250), every one with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.
- `compose.txt`: `certified_nodes 382, class_covered false` (expected: 1/40 of the survey), CNF sha256 of every certified node recomputed from the base CNF.
- SAT: none. PROOF NOT ACCEPTED: none. Memory: no incident (peak about 8 GB used of 15).

**Closed (13):** 0s0-1s1_4s1-9s0, 0s0-2s0_10, 0s0-2s0_3s1-10s0, 0s0-2s0_5s0-9s0, 0s0-2s0_8s1-10s1, 0s0-2s1_3s0-10s1, 0s0-2s1_4s1-10s0, 0s0-2s1_6s0-9s0, 0s0-3s0_1s0-10s1, 0s0-3s0_2s0-7s0, 0s0-3s0_4s1-7s1, 0s0-3s0_6s1-8s1, 0s0-3s1_1s0-6s0.
**Partial (1):** 0s0-3s1_2s1-10s1.
**Not reached (20):** roots 15–34 of `roots.tsv`.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `compose.txt`.
