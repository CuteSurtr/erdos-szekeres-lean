# C3W4 / O01: wave 4, list W4_one.tsv, shard 1 of 16

**Result: no SAT, no proof rejection, no memory problem. 526 nodes certified. Root 1 (`0s0-1s1_4`) and root 2 (`0s0-3s1_4`) are partial. Root 3 (`0s0-5s1_1`) was not reached.**

## Setup

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:10 UTC, END 16:16:10 UTC (start + 5 h − 15 min), 2026-10-24. Task: `results/C3W4/TASK.md` at 3fd8a4d8.

- Tools: worktree of 95cafa93 at `/opt/c3u`, `results/C3U/tools` used unmodified. CaDiCaL 3.0.1 c6073042. cake_lpr a36874a8 (example prints `s VERIFIED UNSAT`). lrat-check 2e3b2dc with the E2 patch. Sanity check passed: `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both (`tools.txt`).
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).
- Roots: the rows of `W4_one.tsv` with row ≡ 1 (mod 16), giving rows 1, 17 and 33 (`roots.tsv`). Nothing was seeded: every root started fresh.
- Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat`, slice 2.5 h (`runner.sh`).
- `compose.py` was not run, as the task says.

## Per root

Depth means layers, so the roots are at d2. "σn" means n σ bits are fixed.

| row | root | stratum | status | certified | timeouts | splits | open frontier | solve s | check s |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0s0-1s1_4 | H6(1,1)/one | **partial** | d2/σ6: 41; d3/σ6: 466 | σ0 and σ3 at cap 1: 1 + 8; d2/σ6 at 300 s: 23 | σ: 1 + 8 (8 children each); layer: 23 (1,173 children) | ≈707 d3/σ6 layer children not attempted | 26,590 | 11,751 |
| 17 | 0s0-3s1_4 | H6(3,1)/one | **partial** | d2/σ6: 19 | cap 1: 1 + 8; d2/σ6 at 300 s: 20 | σ: 1 + 8; layer: 20 (1,028 children) | 25 6-bit cubes and 1,028 layer children not attempted (≈1,045 counted by the script) | 11,043 | 770 |
| 33 | 0s0-5s1_1 | H6(5,1)/one | not reached | – | – | – | – | – | – |

- No split record has `"children": 0`, so there is no childless timed-out node.
- Every timed-out node was split. All the open nodes are children that were never attempted.
- The solve and check seconds are summed per node over 3 parallel jobs.
- Of the 64 6-bit cubes of each root, root 1 certified 41 and 23 timed out at 300 s (64% certified). Root 2 certified 19 and 20 timed out, and 25 were not attempted (49% of those attempted were certified).

Totals per stratum: H6(1,1)/one 507 certified; H6(3,1)/one 19 certified; H6(5,1)/one 0 (not reached). All 526 certified records have lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`. There are no `none` records and no re-checks (`recheck.jsonl` is absent).

## Deviation: the slice was enforced by killing the process

`close_tree.py` checks `--hours` only between frontier levels. Each level runs as a single batch, and a level can take hours. Root 1 started at 11:33 with `--hours 2.5`, but at 15:08, more than an hour past its slice, it was still in its layer-split level with about 709 of 1,173 children left (about 3 more hours). I killed that `close_tree.py` process tree by hand at 15:08:49. The runner then started root 2 with S = 1.123 h. Root 2 would have overrun END in the same way, so a watchdog (`watchdog.sh`) killed it at END (16:16:10). The watchdog's log line was overwritten because the runner held `driver.log` open without append mode. One orphaned cadical (a 6-bit cube of root 2) kept running after the kill, and I killed it at about 16:17. The nodes that were running when a process was killed have no record, and those killed in a check have no `none` record either. They are simply unattempted. Records already written are not affected.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `watchdog.sh`, `out.jsonl` (all records, resumable), `driver.log.tail`.
