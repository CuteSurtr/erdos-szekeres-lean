# C3WAVE2 / K21: shard 21 of 40, wave 2, 3-fold class (m = 11, k = 7)

**Result: root 1 of 34 (`0s0-1s1_5s1-6s0`) is closed. The other 33 roots were not reached. No SAT, no proof rejection, no memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 00:27:37 UTC on 2026-10-21, budget 1.5 h, END = 01:42:37.
The tools are as in `results/C3WAVE1/C00/README.md` (`tools.txt`):
- C3-S tools: a worktree of `132398c` (`8dc27c3` before the rewrite) at /opt/c3s, unmodified.
- CaDiCaL 3.0.1 (c6073042). cake_lpr a36874a8 (`make cake_lpr`); its example prints `s VERIFIED UNSAT`.
- lrat-check 2e3b2dc with the E2 patch. On {1},{-1}, `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches).
- Roots: the rows of `C3WAVE2/roots.tsv` with idx ≡ 21 (mod 40), 34 roots (`roots.tsv`). Runner: `runner.sh` (`--jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`).

## Per root

| # | idx | root | status | certified by depth | splits | solve s | check s |
|---|-----|------|--------|--------------------|--------|---------|---------|
| 1 | 21 | 0s0-1s1_5s1-6s0 | **closed** | d3: 84, d4: 462 | d2: 1 (timed out at 300 s, 91 children); d3: 7 (pre-split one-orbit, 66 children each) | 5465 | 8831 |
| 2–34 | | (`roots.tsv`) | not reached | – | – | – | – |

Solve and check times are summed over the nodes. They are not wall-clock: 3 jobs share 4 cores.
The slowest certified node took 62 s. All 546 certified records have `lrat_check = c VERIFIED` and `cake_lpr = s VERIFIED UNSAT`.

**Why only one root was reached:** `close_tree.py` checks `--hours` only between batches (`while frontier and time.time() < deadline`).
The root itself used up its 300 s cap and came back UNKNOWN, so the second batch held all 546 children (84 two-orbit depth-3 nodes plus 7×66 depth-4 nodes).
It started inside the 10-minute slice, and the driver finished the whole batch before returning, at 01:53:20.
By then END had passed, so the runner started no other root. This affected time only, not the results.

## Totals

547 solve records: 546 certified UNSAT and 1 UNKNOWN (the root at 300 s). There are 8 split records. No SATISFIABLE, no `PROOF NOT ACCEPTED`, and no OOM.

## compose.py

`compose.txt`: `certified_nodes: 546, class_covered: false`. This is expected: compose found only this machine's records. It recomputed the CNF sha256 of all 546 certified nodes.

## Closed / partial

- Closed: `0s0-1s1_5s1-6s0`.
- Partial: none.
- Not reached (idx node): 61 0s0-2s0_1s0-6s0, 101 0s0-2s0_3s1-7s1, 141 0s0-2s0_5s1-8s1, 181 0s0-2s1_10, 221 0s0-2s1_3s0-7s0, 261 0s0-2s1_4s1-7s1, 301 0s0-2s1_6s1-8s1, 341 0s0-3s0_1s0-6s0, 381 0s0-3s0_2s1-10s1, 421 0s0-3s0_5s0-10s1, 461 0s0-3s0_7s0-8s1, 501 0s0-3s1_1s0-9s1, 541 0s0-3s1_2s1-7s0, 581 0s0-3s1_5s0-9s0, 621 0s0-3s1_7s1-9s0, 661 0s0-4s0_1s1-5s0, 701 0s0-4s0_3s0-10s0, 741 0s0-4s0_5s1-7s1, 781 0s0-4s0_8s1-10s0, 821 0s0-4s1_1s1-8s1, 861 0s0-4s1_3s0-7s1, 901 0s0-4s1_6s0-10s1, 941 0s0-4s1_9s1-10s0, 981 0s0-5s0_2s0-3s1, 1021 0s0-5s0_3s1-4s0, 1061 0s0-5s0_6s1-10s0, 1101 0s0-5s1_1s0-2s1, 1141 0s0-5s1_2s0-8s0, 1181 0s0-5s1_3s1-8s1, 1221 0s0-5s1_6s1-9s1, 1261 0s0_1s0-6s1, 1301 0s0_2s1-3s1, 1341 0s0_4s1-5s1.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `compose.txt`.
