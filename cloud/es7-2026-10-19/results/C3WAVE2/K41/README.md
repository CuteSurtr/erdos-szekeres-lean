# C3WAVE2 / K41: 3-fold class (m = 11, k = 7), roots idx 999 down to 900

**Result: 3 of my 100 roots are closed and 1 is partial. The other 96 were not reached. No SAT, no proof rejection, no memory problem.**

## Setup

One cloud VM with 4 cores, 15 GB RAM and no swap (`env.txt`). Start 01:21:08 UTC on 2026-10-21, H = 1.0 h, END = start + 45 min = 02:06:08.
The tools are as in `C3WAVE1/C00/README.md` (`tools.txt`):
- C3-S tools from a worktree of 132398c (8dc27c3 before the rewrite) at /opt/c3s, unmodified
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa; its example prints `s VERIFIED UNSAT`
- lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with the E2 patch. Sanity check: `3 0 0` on {1},{-1} is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches).

Roots are the rows of `C3WAVE2/roots.tsv` with idx 999 down to 900, in decreasing idx order (`roots.tsv`, 100 roots). This was set by the prompt in place of the residue class.
The runner is `runner.sh`: the K00 runner with my END and S = min(0.17, hours left), `--jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles`.

## Per root (depth = number of layers; roots are at depth 2)

| idx | root | status | certified by depth | splits | solve s | check s |
|-----|------|--------|--------------------|--------|---------|---------|
| 999 | 0s0-5s0_2s1-6s1 | **closed** | d2: 1 | 0 | 16 | 32 |
| 998 | 0s0-5s0_2s1-6s0 | **closed** | d2: 1 | 0 | 160 | 44 |
| 997 | 0s0-5s0_2s1-4s1 | **closed** | d2: 1 | 0 | 19 | 32 |
| 996 | 0s0-5s0_2s1-4s0 | partial | d4: 314 | d2: 1 (UNKNOWN at 300 s, 91 children); d3: 7 (pre-split, 66 each) | 1822 | 4644 |
| 995–900 | (96 roots, `roots.tsv`) | not reached | – | – | – | – |

Solve and check times are summed per node. They are not wall-clock time.

Root 996 (`0s0-5s0_2s1-4s0`) hit the 300 s cap at the root (01:28:30 to 01:33:30) and was split into 91 depth-3 children. Seven of them have a one-orbit layer (`_1`, `_3`, `_6`, `_7`, `_8`, `_9`, `_10`) and were pre-split into 66 depth-4 children each, which gives a frontier of 84 depth-3 + 462 depth-4 = 546 nodes. close_tree.py only checks its deadline between layers, so this layer kept running past the 10-minute slice and END. Of the 546 nodes, 314 depth-4 nodes were certified (each solved in at most 8.7 s). The remaining 232 (84 depth-3 and 148 depth-4) have no record yet. At 02:08:31 I stopped the runner by hand because the time budget was used up. The nodes in flight at that point were killed and left no records. `out.jsonl` can be resumed.

## Totals

326 records: 317 UNSAT, all certified (`c VERIFIED` from lrat-check E2 and `s VERIFIED UNSAT` from cake_lpr), 1 UNKNOWN (root 996 at 300 s), and 8 split records.
There was no SAT, no PROOF NOT ACCEPTED, and no memory problem (about 1 GB used).

`compose.txt` (`compose.py /opt/work/base.cnf out.jsonl`): `certified_nodes: 317, class_covered: false, uncovered_frontier_nodes: 261`. The class is not covered, as expected. compose recomputed the CNF sha256 of every certified node.

**Closed:** 0s0-5s0_2s1-6s1, 0s0-5s0_2s1-6s0, 0s0-5s0_2s1-4s1.
**Partial:** 0s0-5s0_2s1-4s0.
**Not reached:** 0s0-5s0_2s1-3s1 0s0-5s0_2s1-3s0 0s0-5s0_2s1-10s1 0s0-5s0_2s1-10s0 0s0-5s0_2s0-9s1 0s0-5s0_2s0-9s0 0s0-5s0_2s0-8s1 0s0-5s0_2s0-8s0 0s0-5s0_2s0-7s1 0s0-5s0_2s0-7s0 0s0-5s0_2s0-6s1 0s0-5s0_2s0-6s0 0s0-5s0_2s0-4s1 0s0-5s0_2s0-4s0 0s0-5s0_2s0-3s1 0s0-5s0_2s0-3s0 0s0-5s0_2s0-10s1 0s0-5s0_2s0-10s0 0s0-5s0_2 0s0-5s0_1s1-9s1 0s0-5s0_1s1-9s0 0s0-5s0_1s1-8s1 0s0-5s0_1s1-8s0 0s0-5s0_1s1-7s1 0s0-5s0_1s1-7s0 0s0-5s0_1s1-6s1 0s0-5s0_1s1-6s0 0s0-5s0_1s1-4s1 0s0-5s0_1s1-4s0 0s0-5s0_1s1-3s1 0s0-5s0_1s1-3s0 0s0-5s0_1s1-2s1 0s0-5s0_1s1-2s0 0s0-5s0_1s1-10s1 0s0-5s0_1s1-10s0 0s0-5s0_1s0-9s1 0s0-5s0_1s0-9s0 0s0-5s0_1s0-8s1 0s0-5s0_1s0-8s0 0s0-5s0_1s0-7s1 0s0-5s0_1s0-7s0 0s0-5s0_1s0-6s1 0s0-5s0_1s0-6s0 0s0-5s0_1s0-4s1 0s0-5s0_1s0-4s0 0s0-5s0_1s0-3s1 0s0-5s0_1s0-3s0 0s0-5s0_1s0-2s1 0s0-5s0_1s0-2s0 0s0-5s0_1s0-10s1 0s0-5s0_1s0-10s0 0s0-5s0_10 0s0-5s0_1 0s0-4s1_9s1-10s1 0s0-4s1_9s1-10s0 0s0-4s1_9s0-10s1 0s0-4s1_9s0-10s0 0s0-4s1_9 0s0-4s1_8s1-9s1 0s0-4s1_8s1-9s0 0s0-4s1_8s1-10s1 0s0-4s1_8s1-10s0 0s0-4s1_8s0-9s1 0s0-4s1_8s0-9s0 0s0-4s1_8s0-10s1 0s0-4s1_8s0-10s0 0s0-4s1_8 0s0-4s1_7s1-9s1 0s0-4s1_7s1-9s0 0s0-4s1_7s1-8s1 0s0-4s1_7s1-8s0 0s0-4s1_7s1-10s1 0s0-4s1_7s1-10s0 0s0-4s1_7s0-9s1 0s0-4s1_7s0-9s0 0s0-4s1_7s0-8s1 0s0-4s1_7s0-8s0 0s0-4s1_7s0-10s1 0s0-4s1_7s0-10s0 0s0-4s1_7 0s0-4s1_6s1-9s1 0s0-4s1_6s1-9s0 0s0-4s1_6s1-8s1 0s0-4s1_6s1-8s0 0s0-4s1_6s1-7s1 0s0-4s1_6s1-7s0 0s0-4s1_6s1-10s1 0s0-4s1_6s1-10s0 0s0-4s1_6s0-9s1 0s0-4s1_6s0-9s0 0s0-4s1_6s0-8s1 0s0-4s1_6s0-8s0 0s0-4s1_6s0-7s1 0s0-4s1_6s0-7s0 0s0-4s1_6s0-10s1 0s0-4s1_6s0-10s0 

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `compose.txt`.
