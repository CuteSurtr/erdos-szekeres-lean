# C3W4 / H11: wave 4, W4_H3.tsv shard 11 of 30

**Result: no SAT and no proof rejection. Root 1 (`0s0_5s1-6s0`) is partial: 37 of its 64 σ-cubes are closed,
and 1,363 depth-3 nodes are still open. Roots 2 and 3 were not reached.** All 701 certified nodes were accepted by both checkers.

Values: V = H11, LIST = W4_H3.tsv, j = 11, N = 30, SLICE = 2.0, H = 5.0, task commit 3fd8a4d8.
Start 11:31:28 UTC, END 16:16:28 UTC on 2026-10-24. One VM with 4 cores, 15 GB RAM and no swap (`env.txt`).

## Tools and base check (`tools.txt`)

- C3U tools: a worktree of commit 95cafa93 at `/opt/c3u`, used unmodified. `compose.py` was not run, as the task says.
- CaDiCaL 3.0.1 c60730422e75. cake_lpr a36874a8 (its bundled example prints `s VERIFIED UNSAT`). drat-trim lrat-check 2e3b2dc0 with the E2 patch.
  Sanity check on {1},{-1}: `3 0 0` is rejected by both checkers; `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches).
- Roots: rows of W4_H3.tsv with row ≡ 11 (mod 30), which gives rows 11, 41 and 71 (`roots.tsv`). All were started fresh, with no seeded records.
- Runner (`runner.sh`): `close_tree.py … --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours S`.

## Per root

| row | root | stratum | status | certified (depth, σ bits) | timeouts | solve s | check s |
|-----|------|---------|--------|---------------------------|----------|---------|---------|
| 11 | 0s0_5s1-6s0 | H3/two | **partial** (open frontier 1,363) | d2/σ6: 24; d3/σ6: 677 | d2/σ0: 1 (cap 1), d2/σ3: 8 (cap 1), d2/σ6: 40 (cap 300) | 31,525 | 18,275 |
| 41 | 0s0_2s0-3s1 | H3/two | not reached | – | – | – | – |
| 71 | 0s0_3s0-6s0 | H3/two | not reached | – | – | – | – |

Tree of root 11: the root and its 8 three-bit cubes timed out at cap 1 as intended. Each was σ-split, which gives 64 six-bit cubes.
At cap 300, 24 cubes were certified (solve 179–297 s) and 40 timed out. Each timeout got the layer split into 51 depth-3 children,
2,040 in total, at cap 600. Of those, 677 were certified, all in at most 72 s; there were no depth-3 timeouts.
That closes 13 of the 40 timed-out cubes completely. One cube has 14 of 51 children closed, and 26 cubes have no children attempted.
So 37 of 64 cubes are closed. The open frontier is 1,363 unattempted depth-3 nodes.
No split record has `"children": 0`.

Solve and check seconds are summed per node. With 3 jobs on 4 cores they are not wall-clock time.

Totals for stratum H3/two: 3 roots, 0 closed, 1 partial, 2 not reached; 701 certified nodes; 49 timeouts (all split).

## Stop at END

`close_tree.py` checks its `--hours` deadline only between waves. The root's slice ended at 13:34, but it was then inside
the 2,040-node depth-3 wave, which was still running at END. At 16:16 UTC I killed the runner and its solver and checker
processes (marked in `driver.log.tail`), so no `open_frontier` line was printed. The frontier above is computed from `out.jsonl`.
Killed jobs write no record, so no record has cake_lpr `none` and none needed a re-check (there is no `recheck.jsonl`).

## SAT / rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none. Every UNSAT record has `c VERIFIED` and `s VERIFIED UNSAT`.
- Memory: peak use was about 12 of 15 GB with 3 jobs. There was no failure.
