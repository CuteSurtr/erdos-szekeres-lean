# C3W4 / H12: wave 4, W4_H3.tsv shard 12 of 30, σ-cube splitting

**Result: 1 of 3 roots closed (`0s0_2s0-4s0`, all 64 6-bit σ cubes certified). The other 2 are partial. No SAT, no proof rejection, no memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:40 UTC, END 16:16:40 UTC (start + 5.0 h − 15 min), 2026-10-24. Task: `results/C3W4/TASK.md` at 3fd8a4d8.

- Tools: worktree of 95cafa93 at `/opt/c3u`, `results/C3U/tools` used unmodified. CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (example prints `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch. Sanity check: `3 0 0` on {1},{-1} is rejected by both checkers and `3 0 1 2 0` is accepted by both (`tools.txt`).
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).
- Roots: rows 12, 42 and 72 of `W4_H3.tsv` (`roots.tsv`). No records were seeded.
- Runner (`runner.sh`): `close_tree.py base out R --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours S`, with S = min(2.0, hours left before END).
- No `compose.py` was run, as the task says.

### Deviation: slice watchdog

`close_tree.py` checks its `--hours` deadline only before it starts a frontier wave. A whole wave is always submitted and waited for. On root `0s0_1`, the wave after the 64 timed-out cubes has 4,608 layer children at cap 600, about 10 days of work for 3 jobs. Without a limit, that root would have kept the machine for the whole budget and past END.

I added `watchdog.sh`, which runs outside the tools. It kills a close_tree run and its workers (SIGKILL) once the run's elapsed time is longer than its `--hours`. Records are flushed one node at a time, so a kill loses only the nodes in flight, and those stay open. A killed in-flight checker writes no record, so there is no `cake_lpr: none` record.

- The watchdog stopped root `0s0_1` at 13:50:10 (its slice ended at 13:35:45; the watchdog was started at 13:50). That kill's log line was lost, because the runner writes `driver.log` without append; `watchdog.log` records it by hand.
- It stopped root `0s0_3s0-6s1` at END (16:16:47).

### Open frontiers

The open frontiers of the two killed runs were recomputed afterwards with the same command and `--hours 0` on a copy of `out.jsonl`. The copy was unchanged afterwards.

## Per root

Depth = number of layers (roots are at depth 2); σ level = number of 3-bit σ splits on the path. Solve and check seconds are summed per node over 3 concurrent jobs.

| row | root | stratum | status | certified (depth/σ level) | timeouts | splits | open frontier | solve s | check s |
|-----|------|---------|--------|---------------------------|----------|--------|---------------|---------|---------|
| 12 | 0s0_1 | H3/one | **partial** | 0 | cap 1: 1 (d2/σ0) + 8 (d2/σ1); cap 300: 64 of 64 (d2/σ2); cap 600: 6 (d3/σ2) | σ: 9; layer: 64 cubes → 72 children each, 6 d3 nodes → 60 each | 4,962 | 22,823 | 0 |
| 42 | 0s0_2s0-4s0 | H3/two | **closed** | 64 (d2/σ2) | cap 1: 1 + 8 (by design) | σ: 9 | 0 | 6,801 | 3,349 |
| 72 | 0s0_3s0-6s1 | H3/two | **partial** | 0 | cap 1: 1 + 8; cap 300: 51 of 64 (d2/σ2), 13 cubes not attempted | σ: 9; layer: 51 cubes → 51 children each | 2,614 | 15,317 | 0 |

- `0s0_2s0-4s0`: all 64 cubes were certified at cap 300, in 62–~200 s each. The root closed in 58 minutes.
- `0s0_1`: every 6-bit cube timed out at 300 s. The 6 layer children that ran (depth 3, cap 600) also timed out, and each was split into 60.
- `0s0_3s0-6s1`: every attempted cube timed out at 300 s.
- No split record has `"children": 0`.

## Totals per stratum

| stratum | roots | closed | partial | certified nodes | solve s | check s |
|---------|-------|--------|---------|-----------------|---------|---------|
| H3/one | 1 | 0 | 1 | 0 | 22,823 | 0 |
| H3/two | 2 | 1 | 1 | 64 | 22,118 | 3,349 |

All 64 certified nodes have lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.

## SAT, rejections, memory

- SAT: none.
- PROOF NOT ACCEPTED: none. No record has `cake_lpr: none`, so there is no `recheck.jsonl`.
- Memory: at most about 6 GB used out of 15 GB. No problems.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `watchdog.sh`, `watchdog.log`, `out.jsonl` (all 360 records; resumable), `driver.log.tail`, `README.md`.
