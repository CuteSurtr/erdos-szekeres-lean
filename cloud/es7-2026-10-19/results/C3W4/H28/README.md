# C3W4 / H28: wave 4, list W4_H3.tsv, shard 28 of 30

**Result: all 3 of my roots are closed. Open frontier 0 on each, no split record with `"children": 0`.
192 nodes certified, each by both checkers. No SAT, no proof rejection, no memory problem.**

Values: V = H28, LIST = W4_H3.tsv, j = 28, N = 30, SLICE = 2.0, H = 5.0, Z = 3fd8a4d8.

## Setup (`tools.txt`, `env.txt`)

- One cloud VM: 4 cores, 15 GB RAM, no swap. Start 11:31:16 UTC, END 16:16:16 UTC (start + 5 h − 15 min).
- Tools: git worktree of commit 95cafa93 at `/opt/c3u`, used unmodified. `compose.py` was not run, as the task says.
- CaDiCaL c6073042 (3.0.1). cake_lpr a36874a8: its example gives `s VERIFIED UNSAT`. lrat-check 2e3b2dc with the E2 patch.
  Sanity test: on {1},{-1}, LRAT `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF from `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`. Both match.
- Roots: rows 28, 58 and 88 of `lists/W4_H3.tsv` (`roots.tsv`). All three were untouched, and nothing was seeded.
- Runner (`runner.sh`, one runner started with setsid nohup): `close_tree.py /opt/work/base.cnf /opt/work/out.jsonl R --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours S`, S = min(2.0, hours left).

## Per root

Each root followed the expected path. The root timed out at cap 1 and was σ-split into 8 cubes. Each of those 8 timed out at cap 1 and was σ-split into 8 cubes. That gives 64 cubes on 6 σ bits, all at layer depth 2, σ level 2, 269 units, cap 300. Every one of the 64 was certified at cap 300, so no cube reached the cap-600 layer split.

| row | root | stratum | status | certified (depth 2, σ level 2) | timeouts | splits (σ) | solve s | check s | cube solve s min–max | wall |
|-----|------|---------|--------|------|------|------|------|------|------|------|
| 28 | 0s0_1s1-4s1 | H3/two | **closed** | 64 | 9 (cap 1) | 9 (8 children each) | 9645 | 2728 | 88–285 | 11:34:09–12:45:45 |
| 58 | 0s0_2s1-5s1 | H3/two | **closed** | 64 | 9 (cap 1) | 9 (8 children each) | 9576 | 2746 | 99–298 | 12:45:45–13:55:55 |
| 88 | 0s0_4s0-6s0 | H3/two | **closed** | 64 | 9 (cap 1) | 9 (8 children each) | 3693 | 2041 | 19–125 | 13:55:55–14:29:20 |

Solve and check seconds are sums over the nodes, with 3 jobs on 4 cores, so they are not wall-clock time. The slowest cube took 297.8 s, which is close to the 300 s cap (`0s0_2s1-5s1__1s0-3s1-4s1-6s0-7s0-8s0`).

## Totals by stratum

| stratum | roots | closed | partial | not reached | certified | timeouts | solve s | check s |
|---------|-------|--------|---------|-------------|-----------|----------|---------|---------|
| H3/two | 3 | 3 | 0 | 0 | 192 | 27 (all at cap 1, all σ-split) | 22914 | 7514 |

`out.jsonl` has 246 records: 192 certified, 27 cap-1 UNKNOWN and 27 σ-split records. All 192 certified records have lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.

## SAT / rejections / incidents

- SAT: none.
- PROOF NOT ACCEPTED: none. No cake_lpr `none`, and `recheck.jsonl` was not needed.
- Memory: no problem. At most about 6 GB was in use.
- The runner finished all roots at 14:29:20 UTC, well before END. Nothing was killed.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl`, `driver.log.tail`, `README.md`.
