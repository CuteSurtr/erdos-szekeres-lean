# C3W3 / D0: wave 3, list D_s1one.tsv, shard 0 of 25, one lane

**Result: root 0s0-1s1_2 is closed. Root 0s0-1s1_10 is partial, stopped at END while working in its `_9` and `_10` subtrees. No SAT. No proof rejection. No memory problem.**

## Setup
- One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:54:36 UTC (1792558476), END 10:39:36 UTC. Task from `C3W3/TASK.md` at 640a56c2: V = D0, LIST = D_s1one.tsv, j = 0, N = 25, LANES = 1, JOBS = 3, SLICE = 6.0, H = 6.0.
- Tools (`tools.txt`): the C3-S tools come from a worktree of 132398c at /opt/c3s, used unmodified. Also CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8 (its example prints `s VERIFIED UNSAT`), and lrat-check 2e3b2dc with the E2 patch. Sanity check: LRAT `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…0cdd6da` (matches).
- Roots (`roots.tsv`): rows 0 and 25, both stratum H6(1,1)/one and both `partial`. Row 0 has h6m_kept = yes and row 25 has no.
- **Seeded records: 755** at the start of /opt/work/out0.jsonl (0s0-1s1_2: 281, 0s0-1s1_10: 474). These are the certified and split records from C3WAVE1/C3WAVE2 out/recheck and C3S0 out. `out.jsonl` contains only the 920 new records.

## Per root
Depth = number of layers (roots are at depth 2). Times are summed per node and are not wall-clock.

| root | stratum | status | new certified by depth | new splits | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|
| 0s0-1s1_2 | H6(1,1)/one | **closed** (`open_frontier: 0`, 08:47:29) | d4: 568 | 0 | 0 | 25647 | 15359 |
| 0s0-1s1_10 | H6(1,1)/one | partial (stopped at END) | d4: 352 | 0 | 0 | 11967 | 8652 |

Totals for stratum H6(1,1)/one: 1 closed, 1 partial; 920 new certified nodes (all depth 4). Every one has `c VERIFIED` (lrat-check) and `s VERIFIED UNSAT` (cake_lpr). All of them were solved within the 600 s cap.

## Incidents
1. At about 05:38 a restart of the session worker killed the runner. `out0.jsonl` was intact (847 lines, all valid JSON). I restarted `lane0.sh` at 05:40:24 with the same END, and close_tree reused the certified and split records already in the file. Only the in-flight nodes were lost, and they were redone. `driver0_run1.log` is the log before the restart.
2. At END, close_tree was still running its batch (it checks its hours budget only between batches). I killed it by hand at about 10:44 to stay inside the time budget. Killed nodes wrote no records. No record has `cake_lpr: none`, so there was nothing to re-check.

## compose.txt
I ran `compose.py base.cnf out.jsonl` on the new records only. It recomputed the CNF sha256 of all 920 certified nodes: `certified_nodes 920`, `class_covered false`. That is expected, because the records seeded from earlier waves are not in this file.

## Files
`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`, `out.jsonl` (new records only), `driver0.log` (last 100 lines), `driver0_run1.log` (last 100 lines before the restart), `compose.txt`.
