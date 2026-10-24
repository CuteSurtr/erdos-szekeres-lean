# C3W4 H29: W4_H3.tsv shard 29 of 30, σ-cube split

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-24 11:31:21 UTC, H = 5 h, END 16:16:21 UTC.
Task: `results/C3W4/TASK.md` at 3fd8a4d8, V = H29, LIST = W4_H3.tsv, j = 29, N = 30, SLICE = 2.0.

## Tools and base check (`tools.txt`)

- C3U tools: worktree of 95cafa93 at `/opt/c3u`, unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 c60730422e75; cake_lpr a36874a8 (example: `s VERIFIED UNSAT`); lrat-check 2e3b2dc0 + E2 patch.
  Sanity check passed: `3 0 0` on {1},{-1} rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).
- Roots: rows 29, 59, 89 (`roots.tsv`), all H3/two, untouched. No records were seeded.
- Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat` (`runner.sh`).

## Per root

| row | root | status | certified (depth d, σ level s) | timeouts | solve s | check s |
|-----|------|--------|--------------------------------|----------|---------|---------|
| 29 | 0s0_1s1-5s0 | **partial**, open frontier 2,213 | d2 s2: 9; d3 s2: 592 | d2 s0 at cap 1: 1; d2 s1 at cap 1: 8; d2 s2 at cap 300: 55; none at cap 600 | 33,292 | 16,318 |
| 59 | 0s0_2s1-6s0 | not reached | – | – | – | – |
| 89 | 0s0_4s0-6s1 | not reached | – | – | – | – |

Root 29: the root and its 8 first-level cubes timed out at cap 1 as intended, which gave 64 cubes on 6 σ bits.
Only 9 of the 64 were certified at cap 300. The other **55 timed out**, unlike the C3SIG2 pilots,
where every 6-bit cube that ran was certified. Each of the 55 was layer-split into 51 children, giving 2,805 depth-3 nodes at cap 600.
By END, 592 of them were certified (median solve about 20 s, none timed out) and 2,213 were still open.
No split record has `"children": 0`.

Run note: `close_tree.py` checks its `--hours` deadline only between generations. The 2.0 h slice ran out at 13:34
while the depth-3 generation was queued, so that generation kept running until END, when I stopped the runner's process group
(16:16:35). The jobs running at that moment wrote no records, so they count as open. No checker produced a `none` result.
Rows 59 and 89 were never started.

Solve and check seconds are summed per node, with 3 jobs sharing 4 cores, so they are not wall-clock.

## Totals (stratum H3/two)

1 root partial, 0 closed, 2 not reached. 601 nodes certified: all 601 have cake_lpr `s VERIFIED UNSAT` and lrat-check `c VERIFIED`.
64 timeouts, 64 split records (9 σ splits, 55 layer splits), open frontier 2,213.

No SAT, no proof rejection, no re-checks (so there is no `recheck.jsonl`), no memory problem (at least 6 GB was always available).
