# C3W4 / H19: wave 4, list W4_H3.tsv, shard 19 of 30

**Result: no SAT and no proof rejections. Root 1 (`0s0_1s0-6s1`) is partial: 766 nodes certified and 98 open at END. Roots 2 and 3 were not reached.**

## Setup

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Ran 11:31:12 to 16:16:29 UTC on 2026-10-24 (H = 5 h, END = start + 5 h − 15 min). Task file commit 3fd8a4d8.

- Tools: a worktree of commit 95cafa93 at `/opt/c3u`, `results/C3U/tools` used unmodified. No `compose.py` was run.
- CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (its example prints `s VERIFIED UNSAT`), and lrat-check 2e3b2dc with the E2 patch. In the sanity check, both checkers reject `3 0 0` and accept `3 0 1 2 0` (`tools.txt`).
- Base CNF from `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6dd6da`, which matches.
- Roots: rows 19, 49 and 79 of `W4_H3.tsv` (`roots.tsv`, all `H3/two`, untouched). Nothing was seeded.
- Runner (`runner.sh`): `close_tree.py … --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours S` with S = min(2.0, hours left).

## Per root

| row | root | status | certified | timeouts | splits | solve s | check s |
|-----|------|--------|-----------|----------|--------|---------|---------|
| 19 | 0s0_1s0-6s1 | **partial** (98 open) | σ level 2 (6 bits), depth 2: 48; depth 3 (layer split under a 6-bit cube): 718 | root and 8 3-bit cubes at cap 1 (by design); 16 of 64 6-bit cubes at 300 s; none at 600 s | 9 σ (root and 8 3-bit cubes), 16 layer (51 children each, 816 in all) | 31,416 | 18,394 |
| 49 | 0s0_2s0-7s1 | not reached | – | – | – | – | – |
| 79 | 0s0_3s1-5s0 | not reached | – | – | – | – | – |

Details for root 1:
- **6-bit cubes certified directly at cap 300:** 48 of 64, with 11,324 s of solving and 2,246 s of checking.
- **Cubes that timed out:** the other 16 used 4,802 s. Each was layer-split into 51 children at cap 600.
- **Layer-split cubes:** 14 of the 16 are fully closed (51 of 51 children certified). Two are open:
  - `…__2s1-3s1-4s1-5s1-7s0-8s1`: 4 of 51 children certified.
  - `…__2s1-3s1-4s1-5s1-7s1-8s0`: 0 of 51 certified.
- **Open frontier:** 98 nodes, all children of those two cubes at depth 3.
- **No childless split record** (`"children": 0`).

**Why the root ran past its 2 h slice:** `close_tree.py` checks its deadline only between batches. The 816-node layer batch began at about 13:30 and was still running at END. At END I killed the runner, close_tree and the solver and checker processes. Three nodes were in flight (two cadical runs and one cake_lpr). They wrote no record, so no record has cake_lpr `none`, and they stay in the open count. `close_tree` printed no final `open_frontier` line because it was killed; the 98 above is counted from `out.jsonl`.

## Totals for stratum H3/two (this machine)

- **Nodes:** 766 certified and 25 UNKNOWN. Every certified node has `c VERIFIED` and `s VERIFIED UNSAT`.
- **Time:** 31,416 s solving and 18,394 s checking, summed per node (not wall clock; 3 jobs on 4 cores).
- **Proofs:** the largest is 452 MB. Proofs are not committed.
- **Roots:** 0 closed, 1 partial, 2 not reached.

## SAT, rejections, memory

- **SAT:** none.
- **PROOF NOT ACCEPTED:** none, so there is no `recheck.jsonl`.
- **Memory:** no problems. At least about 5 GB was always available.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all 816 records, resumable), `driver.log.tail`.
