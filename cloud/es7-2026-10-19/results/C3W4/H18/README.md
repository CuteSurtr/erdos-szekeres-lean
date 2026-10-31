# C3W4 H18: W4_H3.tsv shard 18 of 30

Task `results/C3W4/TASK.md` (3fd8a4d8), V = H18, LIST = W4_H3.tsv, j = 18, N = 30, SLICE = 2.0 h, H = 5.0 h.
One VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:25 UTC, END 16:16:25 UTC (2026-10-24).

## Tools and base CNF
- Worktree of 95cafa93 at /opt/c3u, TOOLS = `/opt/c3u/cloud/es7-2026-10-19/results/C3U/tools`, unmodified.
- CaDiCaL c6073042 (3.0.1); cake_lpr a36874a8 (example: `s VERIFIED UNSAT`); lrat-check 2e3b2dc with the E2 patch.
  Sanity check passed: `3 0 0` on {1},{-1} rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF (`gen_case.py 11 7 none -o ...`; this tool version needs `-o`): `p cnf 168399 4154921`,
  sha256 `bf0e502e...6cdd6da` (matches). Details in `tools.txt`.
- Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat`, no seeding. No compose.py run.

## Per root (stratum H3/two for all three)
| row | root | status | certified (depth 2 / depth 3, all at σ level 2) | timeouts | open frontier | solve s | check s |
|---|---|---|---|---|---|---|---|
| 18 | 0s0_1s0-5s1 | partial | 16 / 733 (749) | 9 at cap 1 (root + 8 first-level σ nodes), 48 of 64 six-bit cubes at cap 300, none at cap 600 | 1,715 (never solved) | 32,800 | 17,142 |
| 48 | 0s0_2s0-7s0 | not reached | – | – | – | – | – |
| 78 | 0s0_3s1-4s1 | not reached | – | – | – | – | – |

Root 0s0_1s0-5s1 went root → 8 σ nodes → 64 six-bit cubes (9 σ splits). 16 of the 64 cubes were certified at
cap 300 (about 200–300 s each); the other 48 timed out and got the layer split (48 layer splits, 2,464 depth-3
children). Of these, 733 were certified at cap 600 (typically 5–60 s each) and none timed out; 1,715 were not yet
solved at END. No split record has `"children": 0`.

close_tree checks its `--hours` deadline only between frontier waves, so the 2-hour slice of the first root ran on in
its layer-split wave until END; the runner's process group was then terminated at 16:16:30 (no `open_frontier`
line was printed for this root; the frontier above is recomputed from `out.jsonl` with the hullcase child
functions). Killed jobs wrote no records, so there is no record with cake_lpr `none` and no `recheck.jsonl`.

Totals (stratum H3/two): 0 closed, 1 partial, 2 not reached; 749 certified nodes, 57 timeouts, 32,800 s solve,
17,142 s check.

No SAT answer, no proof rejection (every UNSAT record has `c VERIFIED` and `s VERIFIED UNSAT`), no memory problem
(available memory stayed at or above about 3 GB; no OOM kills).

Files: `out.jsonl` (863 records), `driver.log.tail`, `roots.tsv`, `runner.sh`, `tools.txt`, `env.txt`.
