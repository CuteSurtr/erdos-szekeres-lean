# C3W4 O06: W4_one.tsv, shard 6 of 16

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:36 UTC on 2026-10-24, H = 5.0, END = 16:16:36 UTC. The task file is at 3fd8a4d8.

## Tools (`tools.txt`)
- C3U tools: worktree of 95cafa93 at `/opt/c3u`, used unmodified. No `compose.py` was run.
- CaDiCaL 3.0.1 c60730422e; cake_lpr a36874a8 (its example prints `s VERIFIED UNSAT`); lrat-check 2e3b2dc with the E2 patch. Sanity check passed: on {1},{-1}, `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6dd6da` (matches).

## Run
Roots: rows 6 and 22 of `W4_one.tsv` (`roots.tsv`). Nothing was seeded. One runner (`runner.sh`) used `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat` with a 2.5 h slice.

`close_tree.py` checks `--hours` only between BFS waves. The wave of layer-split children (2,193 nodes) started before the slice ended, so root 6 kept running past its 2.5 h slice until the stop. I stopped all processes by hand at 16:11:27–16:12:10 UTC, about 5 minutes before END. That is my mistake: the wait loop timed out early. Solves and checks that were killed wrote no record, so there are no `cake_lpr: none` records and nothing to re-check (`recheck.jsonl` is absent).

## Per root
| row | root | stratum | status |
|---|---|---|---|
| 6 | 0s0-2s1_4 | H6(2,1)/one | **partial**: open frontier 1,485, no childless timed-out node |
| 22 | 0s0-4s0_6 | H6(4,0)/one | not reached |

0s0-2s1_4 in detail:
- The root and its 8 three-bit cubes timed out at cap 1, as intended. 9 σ splits produced 64 cubes on 6 σ bits (bits 1,3,5 at the first level).
- 6-bit cubes (cap 300): **21 certified** and 43 timed out. Of the certified ones, 17 have σ1 = 0 and 4 have σ1 = 1, so the σ1 = 1 half is much harder. Certified solves: median 256 s, max 295 s.
- Each of the 43 timed-out cubes got a layer split with 51 children (cap 600). **708 children were certified** (median solve 15 s, max 62 s; no child timed out).
  - 13 of the 43 split cubes are fully closed.
  - 1 split cube has 45 of 51 children certified.
  - 29 split cubes have no child solved yet. All 29 are in the σ1 = 1 half except 1s0-3s1-5s1-6s1-7s1-8s1.
- Certified nodes: 729 in total, by (layer depth below root, σ level): (0, 2) 21; (1, 2) 708. Each has `lrat_check: c VERIFIED` and `cake_lpr: s VERIFIED UNSAT`.
- Timeouts: 1 at (0, 0) cap 1, 8 at (0, 1) cap 1, and 43 at (0, 2) cap 300.
- Time: 32,408 s of solving in records (including timeouts) and 16,800 s of checking. Certified 6-bit cubes: 5,416 s solve and 1,024 s check. Layer children: 14,078 s solve and 15,776 s check.
- Splits: 9 σ and 43 layer. Every split record has children > 0.

## Totals per stratum
- H6(2,1)/one: 1 root, partial, 729 certified, 52 timeouts, open frontier 1,485.
- H6(4,0)/one: 1 root, not reached.

## Problems
No SAT and no proof rejection. Memory: the largest proof was 414 MB; available memory never fell below about 6 GB at the samples I took, and no process was OOM-killed. No CNF or proof files are committed.
