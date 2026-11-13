# C3W4 / H20: wave 4, list W4_H3.tsv, shard 20 of 30

**Result: no SAT and no proof rejections. Root 1 (`0s0_1s0-7s1`) is partial: 705 nodes certified, 559 layer children still open. Roots 2 and 3 were not reached.**

## Setup (`env.txt`, `tools.txt`)

One cloud VM with 4 cores, 15 GB RAM and no swap. The run started at 11:31:25 UTC and END was 16:16:25 UTC (5 h − 15 min).
- C3U tools: worktree of 95cafa93 at `/opt/c3u`, used unmodified. `compose.py` was not run, as the task requires.
- CaDiCaL c60730422e758ef1cebe7aeddf2dda31c996bf04 (3.0.1); cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (its example prints `s VERIFIED UNSAT`); lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with the E2 patch. Sanity check: both checkers reject `3 0 0` and accept `3 0 1 2 0`.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).
- Roots: rows of `W4_H3.tsv` with row ≡ 20 (mod 30), 3 roots (`roots.tsv`), all H3/two and untouched. 0 seeded records.
- Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours 2.0` (`runner.sh`).

## Per root

| row | root | status | certified (layers, σ bits) | timeouts | splits | solve s | check s |
|---|---|---|---|---|---|---|---|
| 20 | 0s0_1s0-7s1 | **partial** (559 open) | 40 six-bit cubes at depth 2; 665 layer children (3 layers, 6 bits) at cap 600 | root and 8 three-bit cubes at cap 1 (by design); 24 of 64 six-bit cubes at cap 300 | 1 + 8 σ-splits, 24 layer splits (1,224 children) | 30,959 | 18,831 |
| 50 | 0s0_2s0-8s0 | not reached | – | – | – | – | – |
| 80 | 0s0_3s1-5s1 | not reached | – | – | – | – | – |

Root 1 in detail: 40 of its 64 six-bit cubes were certified at cap 300 (about 175–295 s each). The other 24 timed out and were layer-split into 1,224 children. Of those, 665 were certified (no timeouts at cap 600, typically 7–80 s) and 559 were never attempted. No split record has `"children": 0`. Solve and check seconds are summed per node, with 3 jobs sharing 4 cores.

**Why roots 2 and 3 were not reached:** `close_tree.py` checks `--hours` only between whole waves of the frontier. The 2.0 h slice ran out at 13:33, but the wave of 1,224 layer children had started at about 13:20. That wave would have needed about 3 more hours (around 47 s of solve plus check per node, 3 jobs), so it ran until END. At END (16:16:32) I killed the runner, `close_tree.py` and its solvers by hand. As a result, close_tree printed no final `open_frontier` line. The open count of 559 was reconstructed from `out.jsonl` as 1,224 children minus 665 attempted. Every record that was written is complete. 3 nodes were in flight when killed, and no record was written for them. No checker record has `none`, so nothing needed a re-check.

## Totals per stratum

H3/two: 1 of 3 roots partial, 2 not reached. 771 records: 705 certified (both checkers), 33 UNKNOWN, 33 split, 0 SAT, 0 rejected.

## SAT / proof rejection / memory

None. Peak memory use was about 9 GB of 15 GB. The largest proof was 428 MB, which was deleted along with all CNFs.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all 771 records, resumable), `driver.log.tail`, `README.md`.
