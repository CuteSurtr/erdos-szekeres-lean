# C3WAVE2 / K07: shard 7 of 40, 3-fold class (m = 11, k = 7)

**Result: 5 of my 34 roots are closed and 3 are partial. Roots 10–34 were not reached. No SAT, no proof rejection, no memory problem.**
The VM restarted once during the run (01:20 UTC) and killed the runner. I resumed it by hand (see Incidents).

## Setup (`env.txt`, `tools.txt`)

One cloud VM, 4 cores, 15 GB RAM, no swap. Run from 00:23:11 to 01:41 UTC on 2026-10-21 (budget 1.5 h, END = 01:38:11).
- C3-S tools: worktree of `132398c` (= 8dc27c3 before the rewrite) at /opt/c3s, unmodified. Live files are in /opt/work.
- CaDiCaL 3.0.1 `c6073042`. cake_lpr `a36874a8`; its example prints `s VERIFIED UNSAT`. lrat-check `2e3b2dc` with the E2 patch.
  Sanity check: `3 0 0` on {1},{-1} was rejected by both checkers, and `3 0 1 2 0` was accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).
- Roots: idx ≡ 7 (mod 40) of `C3WAVE2/roots.tsv`, 34 roots (`roots.tsv`).
- `runner.sh`: `close_tree.py … --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours min(0.17, left)`.
  `runner2.sh` is the same script with a start row (`FROM`), used for the resume.

## Per root (depth = number of layers; roots are at depth 2)

| # | idx | root | status | certified by depth | splits | solve s | check s |
|---|-----|------|--------|--------------------|--------|---------|---------|
| 1 | 7 | 0s0-1s1_4s0-8s0 | **closed** | d2: 1 | 0 | 135 | 49 |
| 2 | 47 | 0s0-1s1_8s1-10s1 | **closed** | d2: 1 | 0 | 32 | 35 |
| 3 | 87 | 0s0-2s0_3s0-5s1 | **closed** | d2: 1 | 0 | 85 | 46 |
| 4 | 127 | 0s0-2s0_5 | **closed** | d3: 120 | d2: 1 (pre-split, 120) | 3069 | 2641 |
| 5 | 167 | 0s0-2s0_7s1-8s1 | **closed** | d2: 1 | 0 | 7 | 17 |
| 6 | 207 | 0s0-2s1_1s1-7s1 | partial | d4: 96 | d2: 1 (timeout at 300 s, 91 children); d3: 7 (pre-split, 66 each) | 861 | 1361 |
| 7 | 247 | 0s0-2s1_4s0-6s1 | partial | d4: 127 | d2: 1 (timeout at 300 s, 91 children); d3: 7 (pre-split, 66 each) | 926 | 1851 |
| 8 | 287 | 0s0-2s1_6 | partial (only pre-split) | – | d2: 1 (pre-split, 120) | 0 | 0 |
| 9–34 | | (`roots.tsv`) | not reached | – | – | – | – |

Roots 6 and 7 each have 546 leaves: 84 single depth-3 children and 7 × 66 depth-4 children. Root 6 has 96 certified and 450 open. Root 7 has 127 certified and 419 open.
Root 8 holds only its pre-split record, with 120 open children (see Incidents). Solve and check times are per-node sums, not wall-clock.
Root 4 overran its slice: it ran 00:32 to 01:04, because the driver checks `--hours` only between batches.

**Totals:** 367 records in `out.jsonl`: 347 UNSAT, all certified (`c VERIFIED` and `s VERIFIED UNSAT`); 2 UNKNOWN at 300 s (the roots of 6 and 7); 18 split records.
`compose.txt`: `certified_nodes 347, class_covered false`, as expected. compose recomputed the CNF sha256 of every certified node.

Closed: 0s0-1s1_4s0-8s0, 0s0-1s1_8s1-10s1, 0s0-2s0_3s0-5s1, 0s0-2s0_5, 0s0-2s0_7s1-8s1.
Partial: 0s0-2s1_1s1-7s1, 0s0-2s1_4s0-6s1, 0s0-2s1_6.

## SAT / rejections / memory

No SAT. No `PROOF NOT ACCEPTED`. No memory problem (about 2 GB used with 3 jobs).

## Incidents (affect time only, not results)

1. About 01:17–01:20 UTC: the VM restarted (kernel build changed) and killed the runner during root 6. Root 6 had already used 16 minutes, more than its slice.
   /opt/work survived. I resumed with `runner2.sh`. Its first start used the wrong row (root 8, `0s0-2s1_6`), and I killed it after 36 s. That run wrote only root 8's pre-split record.
   I then restarted at root 7, `0s0-2s1_4s0-6s1`, at 01:21:42.
2. At 01:41 I stopped root 7 by hand so that the last 12 minutes were left for this report. Any proof that was in flight then was not recorded. All finished records are in `out.jsonl`, so the work can be resumed.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `runner2.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `compose.txt`.
