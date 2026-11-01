# C3W4 / H26: wave 4, list W4_H3.tsv, shard 26 of 30

**Result: all 3 of my roots are closed (open frontier 0, no childless timed-out node). No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:14 UTC on 2026-10-24, H = 5.0 h, END 16:16:14 UTC; the runner finished all roots at 13:20:39.
Task file `results/C3W4/TASK.md` at 3fd8a4d8.

- Tools: worktree of commit 95cafa93 at `/opt/c3u`, `TOOLS=/opt/c3u/cloud/es7-2026-10-19/results/C3U/tools`, unmodified. No `compose.py` was run.
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (example prints `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with `results/E2/tools/lrat-check-E2.patch`. Sanity check on {1},{-1}: LRAT `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both (`tools.txt`).
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: rows of `W4_H3.tsv` with row ≡ 26 (mod 30): rows 26, 56, 86 (`roots.tsv`), all stratum H3/two, status untouched. No records seeded.
- Runner (`runner.sh`): `close_tree.py /opt/work/base.cnf /opt/work/out.jsonl R --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours S`, S = min(2.0, hours left before END).

## Per root

Each root timed out at cap 1 (as intended), was σ-split on bits [2,4,5] into 8 nodes, each of which timed out at cap 1 and was σ-split on bits [6,7,8], giving 64 cubes on 6 σ bits. Every cube was certified at cap 300 (max solve 128.8 s); none needed the layer split. All nodes are at layer depth 2 (the root's depth).

| row | root | status | certified (σ level 2, 6 bits) | timeouts (cap 1: root + 8 σ1 nodes) | splits | solve s | check s | wall |
|-----|------|--------|------|------|------|------|------|------|
| 26 | 0s0_1s1-3s1 | **closed** | 64 | 9 | 9 σ splits (8 children each) | 5312 | 2282 | 11:34–12:17 |
| 56 | 0s0_2s1-4s1 | **closed** | 64 | 9 | 9 | 5203 | 2033 | 12:17–12:58 |
| 86 | 0s0_4s0-5s0 | **closed** | 64 | 9 | 9 | 2246 | 1538 | 12:58–13:20 |

Solve and check seconds are summed per node (3 jobs on 4 cores, so per-node times are inflated).

## Totals (stratum H3/two)

3 roots closed, 0 partial, 0 not reached. 192 certified nodes (all `c VERIFIED` from lrat-check and `s VERIFIED UNSAT` from cake_lpr), 27 timeouts at cap 1, 27 split records (none with `"children": 0`), solve 12,760 s, check 5,853 s. `out.jsonl` has 246 records.

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none; no record with cake_lpr `none`, so no `recheck.jsonl`.
- Memory: no problem (peak about 9 GB used of 15 GB).

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, for the fixed composer), `driver.log.tail`.
