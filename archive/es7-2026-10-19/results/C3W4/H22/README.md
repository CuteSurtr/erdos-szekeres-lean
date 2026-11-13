# C3W4 / H22: wave 4, 3-fold class, σ-cube splitting (list W4_H3.tsv, shard 22 of 30)

**Result: 2 of my 3 roots closed (`0s0_1s0-9s0`, `0s0_2s0-9s1`); `0s0_3s1-7s0` is partial (21 of 64 six-bit cubes certified, 43 open). No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:20 UTC 2026-10-24, END 16:16:20 UTC (start + 5 h − 15 min).
Task: `results/C3W4/TASK.md` at 3fd8a4d8 with V = H22, LIST = W4_H3.tsv, j = 22, N = 30, SLICE = 2.0, H = 5.0.

- Tools: worktree of commit 95cafa93 at `/opt/c3u`, `TOOLS=/opt/c3u/cloud/es7-2026-10-19/results/C3U/tools`, unmodified. `compose.py` was not run (as the task says).
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`);
  lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with the E2 patch. Sanity check on CNF {1},{-1}: LRAT `3 0 0` rejected by both
  checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: rows 22, 52, 82 of `lists/W4_H3.tsv` (`roots.tsv`), all stratum H3/two, status untouched. No records seeded.
- One runner (`runner.sh`): `close_tree.py /opt/work/base.cnf /opt/work/out.jsonl R --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours S`, S = min(2.0, hours left before END).

## Per root

Node depth = number of layers (roots are at depth 2); σ level = number of 3-bit σ-splits on the path (level 2 = 6-bit cubes).

| row | root | status | certified (depth, σ level, cap) | timeouts | splits | solve s | check s |
|-----|------|--------|-------------------------------|----------|--------|---------|---------|
| 22 | 0s0_1s0-9s0 | **closed** (open_frontier 0) | d2 σ2 cap 300: 54; d3 σ2 cap 600: 510 (total 564) | cap 1: 1 root + 8 σ1; cap 300: 10 six-bit cubes | σ: 9 (8 children each); layer: 10 (51 children each) | 19753 | 14434 |
| 52 | 0s0_2s0-9s1 | **closed** (open_frontier 0) | d2 σ2 cap 300: 64 | cap 1: 1 root + 8 σ1 | σ: 9 (8 children each) | 8218 | 2499 |
| 82 | 0s0_3s1-7s0 | partial (killed at END during the 6-bit level; 43 of its 64 cubes open) | d2 σ2 cap 300: 21 | cap 1: 1 root + 8 σ1 | σ: 9 (8 children each) | 3919 | 954 |

Root 22 ran 11:33–14:46 (close_tree checks `--hours` only between levels, so the 510-node layer level ran past the 2 h slice), root 52 14:46–15:47, root 82 15:47–16:16.
Solve and check seconds are summed per node (3 jobs on 4 cores; not wall-clock). The cap-1 timeouts are the intended immediate σ-splits.

Notes: in root 22, all 10 six-bit cubes that timed out at 300 s were layer-split and all 510 children were certified at cap 600 (most in under 20 s).
In root 52 every one of the 64 six-bit cubes was certified at cap 300. No split record has `"children": 0`.

## Totals (stratum H3/two)

649 certified nodes (every one with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`), 2 roots closed, 1 partial, 0 not reached.
Timeouts: 27 at cap 1 (intended), 10 at cap 300, 0 at cap 600. Solve 31890 s, check 17887 s.

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none; no record with cake_lpr `none`; no UNSAT record that is not certified. Nodes whose solver or checker was killed at END left no record (they stay open), so there was nothing to re-check; no `recheck.jsonl`.
- Memory: none (lowest observed available memory about 4 GB).
- The END kill: `pkill -f runner.sh` also ended my own shell, so the close_tree pool workers were killed by PID a moment later (16:16–16:19); no records were written after END.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records), `driver.log.tail` (last 100 lines of the driver log).
