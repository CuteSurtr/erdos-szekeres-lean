# C3W4 / H06: wave 4, W4_H3.tsv shard 6 of 30 (σ-cube splitting)

**Result: 1 of my 4 roots is closed (`0s0_1s0-8s0`). `0s0_1s1-8s1` and `0s0_3` are partial, and `0s0_4s1-7s0` was not reached. No SAT. No proof rejections. No memory problems.**

## Setup

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:15 UTC on 2026-10-24, END 16:16:15 (start + 5 h − 15 min).
- Tools: worktree of commit 95cafa93 at /opt/c3u, `results/C3U/tools` used unmodified. CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
  Sanity checks passed: the cake_lpr example gives `s VERIFIED UNSAT`. On {1},{-1}, `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both. Details in `tools.txt`.
- Base CNF from `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`. Both match.
- Roots: rows of `W4_H3.tsv` with row ≡ 6 (mod 30), giving 4 roots (`roots.tsv`). No seeding.
- One runner (`runner.sh`) with `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat`, slice 2.0 h per root.
- `compose.py` was not run, as the task requires.

## Per root

Depth counts the layers (roots are d2). sK is the number of σ bits fixed: s2 means 6 bits, which is a cube.

| root | stratum | status | certified | timeouts | splits | solve s | check s |
|---|---|---|---|---|---|---|---|
| 0s0_1s0-8s0 | H3/two | **closed** (open frontier 0, no childless split) | d2/s2: 64 (all 64 cubes) | d2/s0 at cap 1: 1; d2/s1 at cap 1: 8 | σ: 1 + 8 | 10917 | 2914 |
| 0s0_1s1-8s1 | H3/two | partial, open frontier 1,833 | d2/s2: 26 cubes; d3/s2: 105 layer children (cap 600) | cap 1: 1 + 8; d2/s2 cubes at cap 300: 38 | σ: 1 + 8; layer: 38 × 51 = 1,938 children | 19965 | 4068 |
| 0s0_3 | H3/one | partial, open frontier 2,833 | 0 | cap 1: 1 + 8; d2/s2 cubes at cap 300: 39 (all that ran) | σ: 1 + 8; layer: 39 × 72 = 2,808 children | 11715 | 0 |
| 0s0_4s1-7s0 | H3/two | not reached | – | – | – | – | – |

Solve and check seconds are summed over nodes, with 3 jobs sharing 4 cores.
- Root `0s0_1s0-8s0` took 11:34 to 12:52. Each cube was certified in 116–222 s.
- Root `0s0_1s1-8s1`: 26 of its 64 cubes were certified in 154–297 s, and 38 timed out at 300 s. Each timed-out cube was layer-split into 51 children. All 105 children attempted were certified, at 5–65 s each.
- Root `0s0_3` (one orbit): every one of the 39 cubes that ran timed out at 300 s, and 25 cubes were never attempted. This does not match the C3SIG2 pilot, where 6-bit cubes were certified in about 100–250 s.
- Totals by stratum: H3/two has 1 closed, 1 partial and 1 not reached, with 195 certified nodes. H3/one has 1 partial root and 0 certified nodes.

## Manual stops (affect time only, not results)

1. `close_tree.py` checks `--hours` only between batches. In root `0s0_1s1-8s1`, one batch held all 1,938 layer children at cap 600, enough for about 7 more hours. At 15:09:38 (2 h 17 min into its 2.0 h slice) I killed that close_tree and its 3 running cadical processes, so the runner went on to `0s0_3` (`manual_stop.txt`). No record is written for a killed node. The root keeps its split records and can be resumed.
2. At END (16:16:15) I killed the runner, close_tree for `0s0_3` and 3 running cadical processes. No checker was running, so no record has `cake_lpr: none` and none needed a re-check.

## SAT / proof rejections / memory

- SAT: none. No SATISFIABLE record and no model files.
- Proof rejections: none. All 195 UNSAT records have `c VERIFIED` and `s VERIFIED UNSAT`, and `recheck.jsonl` was not needed.
- Memory: no problems. The largest proof was 490 MB, and available RAM never fell below about 6 GB.
- No split record has `"children": 0`.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (403 records), `driver.log.tail`, `manual_stop.txt`.
