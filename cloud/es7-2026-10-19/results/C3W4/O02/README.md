# C3W4 / O02: W4_one.tsv, shard 2 of 16, σ-cube splitting

**Result: no root closed. Root `0s0-1s1_5` is partial (open frontier 2,836), and roots `0s0-3s1_5` and `0s0-5s1_2` were not reached. No SAT. No proof rejection. No memory problem.**

Task: `results/C3W4/TASK.md` at 3fd8a4d8. Values: V = O02, LIST = W4_one.tsv, j = 2, N = 16, SLICE = 2.5, H = 5.0.

## Setup (`tools.txt`, `env.txt`)

- One cloud VM: 4 cores, 15 GB RAM, no swap. Start 11:31:27 UTC, END 16:16:27 UTC (2026-10-24).
- Tools: worktree of 95cafa93 at `/opt/c3u`, used unmodified. CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8 (its example prints `s VERIFIED UNSAT`), and lrat-check 2e3b2dc with the E2 patch applied using patch(1). Sanity check on {1},{-1}: both checkers reject `3 0 0` and both accept `3 0 1 2 0`.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`. Both match.
- Roots: rows 2, 18 and 34 of `W4_one.tsv` (`roots.tsv`). No records were seeded.
- Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat`, with no `--split-singles` (`runner.sh`).
- `compose.py` was not run, as the task requires.

## Per root

| row | root | stratum | status | certified (depth, σ bits) | timeouts | solve s | check s |
|-----|------|---------|--------|---------------------------|----------|---------|---------|
| 2 | 0s0-1s1_5 | H6(1,1)/one | **partial**: open frontier 2,836, no childless timed-out node | 428 at depth 3 (layer split), σ level 2 (6 bits), all at cap 600 | 73: root (cap 1), 8 σ-level-1 cubes (cap 1), all 64 6-bit cubes (cap 300) | 34,428 (15,208 on certified nodes, 19,220 on timeouts) | 14,943 |
| 18 | 0s0-3s1_5 | H6(3,1)/one | not reached | – | – | – | – |
| 34 | 0s0-5s1_2 | H6(5,1)/one | not reached | – | – | – | – |

Root `0s0-1s1_5` took the intended route. The root and its 8 3-bit cubes (bits 2,3,4) timed out at cap 1. That gave 64 cubes on 6 σ bits (2,3,4,6,7,8). **None of the 64 was certified at cap 300**, unlike the C3SIG2 pilots, where every 6-bit cube that ran was certified. Each of the 64 then got a layer split into 51 children, which makes 3,264 depth-3 nodes at cap 600.

At END, 428 of those children were certified. They took 10–113 s each, and none timed out. That accounts for 8 of the 64 cubes closed in full (all eight with σ prefix `2s0-3s1-4s0`), plus 20 of 51 children of cube `2s0-3s0-4s1-6s0-7s0-8s0`. The other 55 cubes are untouched.

The 8 closed cubes:
`2s0-3s1-4s0-6s{0,1}-7s{0,1}-8s{0,1}`, so the whole σ prefix `2s0-3s1-4s0` is closed.

At the current rate of about 2.5 certified children per minute with 3 jobs, the remaining 2,836 children would take roughly 19 hours on a machine like this one.

## Totals per stratum

| stratum | roots | closed | partial | not reached | certified nodes |
|---------|-------|--------|---------|-------------|-----------------|
| H6(1,1)/one | 1 | 0 | 1 | 0 | 428 |
| H6(3,1)/one | 1 | 0 | 0 | 1 | 0 |
| H6(5,1)/one | 1 | 0 | 0 | 1 | 0 |

## SAT, proof rejections, memory, incidents

- **SAT: none.**
- **No `PROOF NOT ACCEPTED`.** All 428 UNSAT records have both `c VERIFIED` (lrat-check E2) and `s VERIFIED UNSAT` (cake_lpr). No record has `none`, so no re-check was needed, and there is no `recheck.jsonl`.
- **No memory problem.** Peak use was about 9 GB of 15 GB.
- **The slice was overrun.** `close_tree.py` checks `--hours` only between frontier batches, so the 3,264-node layer batch of root 1 ran past its 2.5 h slice until END, as in C3W3. At END (16:16:32) a watcher killed the runner's whole process group (`=== KILLED at END` in the log). A killed node writes no record, so the nodes in flight stay open.
- **Setup note.** `git apply` refused the E2 patch, which is a normal diff, so it was applied with patch(1) as in earlier waves. The build was checked before any run: the source diff is the single E2 line, and the sanity check passed.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all 574 records: 428 certified, 73 UNKNOWN, 73 split records with 9 σ and 64 layer splits), `driver.log.tail`.
