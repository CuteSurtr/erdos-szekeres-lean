# C3W4 / H05: wave 4, W4_H3.tsv shard 5 of 30

**Result: no SAT, no proof rejection, no memory problem. Root 1 of 4 (`0s0_1s0-7s0`) is partial; roots 2–4 were not reached.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:38 UTC, END (start + 5 h − 15 min) 16:16:38 UTC.

- Tools: worktree of commit 95cafa93 at `/opt/c3u`, `C3U/tools` used unmodified. No `compose.py` was run.
- CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8 (example: `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch. Sanity check passed: on {1},{-1} the LRAT `3 0 0` is rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).
- Roots: rows of `W4_H3.tsv` with row ≡ 5 (mod 30): rows 5, 35, 65, 95 (`roots.tsv`). Nothing seeded.
- Runner (`runner.sh`): `close_tree.py base.cnf out.jsonl R --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours S`, S = min(2.0, hours left before END).
- CaDiCaL was first built by two concurrent `make` runs (my build scripts raced). I rebuilt it from `make clean` before anything ran.

## Per root

| row | root | stratum | status | certified | timeouts | splits | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| 5 | 0s0_1s0-7s0 | H3/two | **partial** | 9 six-bit σ-cubes (σ level 2, cap 300); 447 layer children of timed-out cubes (σ level 2 + 1 layer, cap 600) | root and 8 three-bit cubes at cap 1 (as intended); 55 of 64 six-bit cubes at cap 300 | σ: 1 (root) + 8 (level 1); layer: 55 cubes → 2,805 children | 32,623 | 16,580 |
| 35 | 0s0_1s1-8s0 | H3/two | not reached | – | – | – | – | – |
| 65 | 0s0_2s1-9s0 | H3/two | not reached | – | – | – | – | – |
| 95 | 0s0_4s1-6s1 | H3/two | not reached | – | – | – | – | – |

Root 0s0_1s0-7s0: the 9 certified 6-bit cubes solved in 246–299 s (mean 277). The 447 certified layer children solved in 6–118 s (mean 30), all at cap 600, none timed out. 2,805 − 447 = 2,358 layer children are still open: the run was killed at END before it attempted them (2–3 were in flight and left no record). `open_frontier` was never printed because the run was killed. There is no childless timed-out node: every timeout has a split record with 8, 8 or 51 children.

Solve and check times are summed per node. With 3 jobs sharing 4 cores they are not wall-clock.

Totals (stratum H3/two): 456 certified nodes, all with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`, 64 timeouts, 64 split records, 0 SAT, 0 rejected. No certified record has cake_lpr `none`, so no re-check was needed and there is no `recheck.jsonl`.

## Why only one root

`close_tree.py` checks `--hours` only between generations of the frontier. The 2.0 h slice ran out while the third generation was running: the 2,805 layer children at cap 600, submitted all at once. At the observed rate (447 children in about 2.8 h on 3 jobs) the whole generation needs about 17 h. The runner started no other root, and I stopped the run at END (16:16:38 UTC). All 584 records written up to then are in `out.jsonl` and can be reused when the root is resumed.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (584 records), `driver.log.tail`.
