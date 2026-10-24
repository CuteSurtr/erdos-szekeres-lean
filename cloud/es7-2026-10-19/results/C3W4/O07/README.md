# C3W4 / O07: wave 4, list W4_one.tsv, shard 7 of 16

**Result: root `0s0-4s0_7` is closed (all 64 six-bit σ-cubes certified at cap 300). Root `0s0-2s1_6` is partial: all 64 of its six-bit cubes timed out at 300 s and were layer-split into 3,264 children; 236 of those are certified and 3,028 are open. No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:50 UTC, END 16:16:50 UTC (H = 5.0 h minus 15 min).

- Tools: worktree of 95cafa93 at `/opt/c3u`, `results/C3U/tools` used unmodified. compose.py was not run.
- CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8 (the example gives `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch. Sanity check passed: on {1},{-1}, LRAT `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da`. Both match. Details are in `tools.txt`.
- Roots: rows of `W4_one.tsv` with row ≡ 7 (mod 16). That gives rows 7 (`0s0-2s1_6`, H6(2,1)/one, listed as partial) and 23 (`0s0-4s0_7`, H6(4,0)/one, untouched). See `roots.tsv`. Nothing was seeded: both roots started fresh.
- Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat`.

## Per root

Notation: d = number of layers in the node name (roots are d2), s = number of σ bits fixed.

| root | status | certified | timeouts | splits | solve s | check s |
|---|---|---|---|---|---|---|
| 0s0-2s1_6 | **partial** (open frontier 3,028) | d3/s6: 236 | d2/s0 @1: 1; d2/s3 @1: 8; d2/s6 @300: 64 | σ: 1 + 8; layer: 64 (51 children each) | 30,026 | 8,763 |
| 0s0-4s0_7 | **closed** (open frontier 0, no childless node) | d2/s6: 64 | d2/s0 @1: 1; d2/s3 @1: 8 | σ: 1 + 8 | 6,977 | 3,233 |

Solve and check times are summed over nodes, with 3 jobs sharing 4 cores.

- `0s0-4s0_7`: the six-bit cubes took 56–218 s each (mean 109 s).
- `0s0-2s1_6`: every six-bit cube hit the 300 s cap. Its 3,264 depth-3 children are run at cap 600. The 236 that ran were all certified, at 9–123 s each (mean 46 s), and none timed out. At the stop, 2 of the 64 cubes had all 51 children certified and 14 more had some. The remaining children were never attempted. At this rate, finishing the root would take roughly 3,028 × 46 s / 3 ≈ 13 h with 3 jobs.

Stratum totals: H6(2,1)/one has 0 of 1 roots closed (partial). H6(4,0)/one has 1 of 1 closed. Over both roots: 300 certified nodes and 0 rejections. Every certified node has `c VERIFIED` from lrat-check and `s VERIFIED UNSAT` from cake_lpr. No record has cake_lpr `none`, so `recheck.jsonl` is not needed.

## Deviations (they affect time only, not results)

1. `close_tree.py` checks `--hours` only between batches. For `0s0-2s1_6`, the 2.5 h slice ended at 14:05, but the current batch was all 3,264 cap-600 children, so the run would not stop. At 14:20 I killed it by hand to give the next root its slice. My kill also stopped the runner, so `runner2.sh` (the same runner, starting at the second root) ran `0s0-4s0_7`. That root closed at 15:18 with 0.95 h left. `runner3.sh` then resumed `0s0-2s1_6` from its own `out.jsonl` records for the remaining time and was killed at END (`/opt/work/endkill.sh`). Nothing completed was lost: records are written only when a node finishes, and in-flight nodes are simply still open.
2. The first `=== ROOT 0s0-2s1_6` run has no `end` line. The kill and the resume are marked by `=== NOTE` lines in the driver log.

## SAT / rejections / memory

No SAT. No PROOF NOT ACCEPTED. No childless timed-out node. Peak used memory seen was about 9 GB of 15 GB.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `runner2.sh`, `runner3.sh`, `out.jsonl` (all 464 records), `driver.log.tail`.
