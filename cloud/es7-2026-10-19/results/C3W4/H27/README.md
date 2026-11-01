# C3W4 / H27: W4_H3.tsv shard 27 of 30, σ-cube splitting

**Result: no SAT, no proof rejection, no memory problem. Root 1 (`0s0_1s1-4s0`) is partial with 714 certified nodes;
roots 2 and 3 were not reached.** Nothing here was composed (per TASK.md, no `compose.py` was run).

## Setup

One VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:22 UTC on 2026-10-24, END 16:16:22 UTC (start + 5 h − 15 min).
Task file `results/C3W4/TASK.md` at 3fd8a4d8; V = H27, LIST = W4_H3.tsv, j = 27, N = 30, SLICE = 2.0, H = 5.0.

- Tools: worktree of 95cafa93 at `/opt/c3u`, `results/C3U/tools` used unmodified.
- CaDiCaL 3.0.1 c60730422e75, cake_lpr a36874a8 (example: `s VERIFIED UNSAT`), lrat-check 2e3b2dc + E2 patch.
  Sanity check: on {1},{-1}, `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both (`tools.txt`).
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`, which matches.
- Roots (`roots.tsv`): rows 27, 57 and 87, all with stratum H3/two and status untouched. Nothing was seeded.
- Runner (`runner.sh`): `close_tree.py … --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours S`.

## Per root

| row | root | status | certified (level: cap) | timeouts | solve s | check s |
|-----|------|--------|------------------------|----------|---------|---------|
| 27 | 0s0_1s1-4s0 | **partial**: open frontier 1,200 | 6-bit σ cubes (300 s): 27 of 64; layer children of the timed-out cubes (600 s): 687 | 37 of 64 cubes at 300 s, then layer-split (51 children each); 0 at 600 s | 31,330 | 19,120 |
| 57 | 0s0_2s1-5s0 | not reached | – | – | – | – |
| 87 | 0s0_4s0-5s1 | not reached | – | – | – | – |

Node structure of root 27, as expected for this list: the root and its 8 three-bit cubes timed out at cap 1 and were σ-split, giving 64 six-bit cubes at 300 s.
The 37 cubes that timed out were each layer-split into 51 children, giving a batch of 1,887 children at cap 600. Of these, 687 were certified, every one inside 600 s
(the 600-s cap was never hit). One more was running when it was killed at END (see below), and 1,199 were never attempted.
Every one of the 714 UNSAT records has `lrat_check: c VERIFIED` and `cake_lpr: s VERIFIED UNSAT`. Solve and check seconds are summed per node, not wall clock.

Totals for stratum H3/two (the only stratum here): 714 certified, 46 split records (9 σ, 37 layer from timeouts, plus the one artifact below), 1 of 3 roots touched, 0 closed.

## Why roots 2 and 3 were not reached

`close_tree.py` checks `--hours` only between levels. It submits a whole level as one batch and waits for all of it.
The 2.0-h slice of root 27 ran out at 13:34, during the batch of 1,887 layer children. With 3 jobs that batch needs about 7–8 h (about 40 nodes per 10 min),
so root 27 ran until END. I followed the tools unmodified and did not interrupt it. At END I killed the driver and its solvers by hand.

## Kill artifact at END (not a real timeout)

The last two lines of `out.jsonl` both concern node `0s0_1s1-4s0_5s1-7s1__2s1-3s0-5s1-6s0-7s1-8s0`, and both are artifacts of that kill.
The first is an UNKNOWN record at cap 600 with `solve_s` 2.3: CaDiCaL was killed, it did not time out. The second is a layer-split record with `"children": 32` that the dying driver wrote.
None of those 32 children was attempted, so the node is **open**; treat it as unattempted.
A cake_lpr run killed at END (on `…_3s0-10s1__2s1-3s0-5s1-6s0-7s1-8s0`) left no record, so there is no `none` record to re-check, and there is no `recheck.jsonl`.
No record has `"children": 0`.

## SAT / rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none. No cake_lpr `none` among the records.
- Memory: peak use was about 9 GB of 15 GB, with no OOM.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (808 records, all new), `driver.log.tail`, `README.md`.
