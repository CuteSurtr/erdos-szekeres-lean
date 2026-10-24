# C3W4 / O13: wave 4, list W4_one.tsv, shard 13 of 16

**Result: both of my roots are closed (open frontier 0, no childless timed-out node). No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-24 11:31:20 UTC, END (start + 5.0 h − 15 min) 16:16:20 UTC; the runner finished both roots at 14:37:54 UTC. Task file commit 3fd8a4d8.

- Tools: worktree of commit 95cafa93 at `/opt/c3u`, `TOOLS = /opt/c3u/cloud/es7-2026-10-19/results/C3U/tools`, used unmodified.
- CaDiCaL 3.0.1 (c60730422e758ef1cebe7aeddf2dda31c996bf04); cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`, its example prints `s VERIFIED UNSAT`); lrat-check from drat-trim 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with `results/E2/tools/lrat-check-E2.patch`. Sanity check on {1},{-1}: LRAT `3 0 0` is rejected by both checkers, and `3 0 1 2 0` is accepted by both (`tools.txt`).
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: the rows of `W4_one.tsv` with row ≡ 13 (mod 16): rows 13 and 29 (`roots.tsv`). Both started fresh; nothing was seeded.
- One runner (`runner.sh`): `close_tree.py /opt/work/base.cnf /opt/work/out.jsonl R --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours S`, with S = min(2.5, hours left).
- `compose.py` was not run, as the task says.

## Per root

Depth is the number of layers (roots are at depth 2). σ level is the number of 3-bit σ splits on the path. Solve and check seconds are summed per node, so they are not wall-clock time.

| row | root | stratum | status | certified (depth, σ level) | timeouts | splits | solve s | check s | wall |
|-----|------|---------|--------|----------------------------|----------|--------|---------|---------|------|
| 13 | 0s0-4s1_6 | H6(4,1)/one | **closed** | d2 σ2: 61; d3 σ2: 153 (total 214) | cap 1: root + 8 σ1 nodes; cap 300: 3 σ2 cubes | 9 σ splits (8 children each); 3 layer splits of the timed-out σ2 cubes (51 children each) | 17,497 | 6,061 | 11:34–13:46 |
| 29 | 0s0-5s0_2 | H6(5,0)/one | **closed** | d2 σ2: 64 | cap 1: root + 8 σ1 nodes | 9 σ splits (8 children each) | 6,725 | 2,282 | 13:46–14:38 |

- On `0s0-4s1_6`, 61 of the 64 six-bit cubes were certified at cap 300. The other 3 (`__1s1-2s0-3s0-5s0-7s0-8s1`, `__1s1-2s1-3s0-5s0-7s0-8s0` and `__1s1-2s1-3s1-5s1-7s1-8s0`) timed out and were layer-split. All 153 of their depth-3 children were certified at cap 600.
- On `0s0-5s0_2`, all 64 six-bit cubes were certified at cap 300. The longest solve took 172 s.
- The timed-out nodes all have children. There is no split record with `"children": 0`.

## Totals (stratum: one-orbit, H6(4,1) and H6(5,0))

- Roots: 2 closed, 0 partial, 0 not reached.
- Certified nodes: 278. Every one has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.
- Split records: 21 (18 σ, 3 layer). UNKNOWN records: 21 (18 at cap 1, by design, and 3 at cap 300).
- Solve 24,222 s; check 8,343 s.

## SAT / proof rejections / memory

- SAT: none.
- `PROOF NOT ACCEPTED`: none. No certified-looking record has cake_lpr `none`, and no checker was killed. Because of that, `recheck.jsonl` is empty and not committed.
- Memory: with 3 jobs, at most about 9 GB was used of 15 GB. There was no out-of-memory event.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all 320 records), `driver.log.tail` (the last 100 lines of the driver log).
