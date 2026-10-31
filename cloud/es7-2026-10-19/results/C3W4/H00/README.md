# C3W4 H00: W4_H3.tsv shard 0 of 30

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`), 11:31:17 to 16:16:25 UTC on 2026-10-24 (END = start + 5 h − 15 min).
Task `results/C3W4/TASK.md` at 3fd8a4d8, with V = H00, LIST = W4_H3.tsv, j = 0, N = 30, SLICE = 2.0, H = 5.0.

## Tools and base check (`tools.txt`)

- C3U tools: worktree of 95cafa93 at `/opt/c3u`, unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8 (example: `s VERIFIED UNSAT`);
  lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 + E2 patch. Sanity check passed: LRAT `3 0 0` on {1},{-1}
  rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).

## Run

`runner.sh`: one runner, `close_tree.py … --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours S`,
S = min(2.0, hours left before END). Roots (`roots.tsv`, rows ≡ 0 mod 30, all fresh, nothing seeded):
0s0_1s0-10s0 (row 0, partial in earlier waves), 0s0_1s1-5s1 (30), 0s0_2s1-6s1 (60), 0s0_4s0-7s0 (90), all stratum H3/two.

The first root used the whole budget. `close_tree.py` checks its deadline only between BFS levels, so after its 2 h
slice ran out (13:33) it kept going through the level it had already submitted: 1,224 layer-split children at cap 600.
I killed the runner and all solver/checker processes at END (16:16:20). Killed jobs wrote no records, so no record has
cake_lpr `none` and nothing needed a recheck (`recheck.jsonl` not created).

## Per root

| root | status | detail |
|---|---|---|
| 0s0_1s0-10s0 | partial, open frontier 640 | see below |
| 0s0_1s1-5s1 | not reached | |
| 0s0_2s1-6s1 | not reached | |
| 0s0_4s0-7s0 | not reached | |

0s0_1s0-10s0 (`out.jsonl`, 690 records, `summary.txt`):
- root (cap 1): timed out, σ-split on 3 bits → 8 children; all 8 (cap 1) timed out, σ-split again → 64 cubes on 6 σ bits.
- 6-bit cubes, cap 300: 40 certified, 24 timed out (solve 17,538 s, check 2,125 s).
- Each of the 24 got a layer split (51 children each, 1,224 total). At cap 600, 584 were run and **all 584 certified**,
  none timed out (solve 14,399 s, check 15,710 s). 640 children were never run: the open frontier.
- Every split record has children > 0 (no childless timed-out node).
- Totals: 624 certified, 33 timeouts (1 + 8 at cap 1, 24 at cap 300), 9 σ splits, 24 layer splits; solve 31,945 s, check 17,834 s.

Totals per stratum: H3/two: 0 closed, 1 partial (640 open), 3 not reached.

## SAT, rejections, memory

No SAT. No proof rejected: every UNSAT answer was accepted by both lrat-check and cake_lpr. No memory problem. Used memory
peaked around 11 of 15 GB, when two or three cake_lpr ran at once (about 4 GB each).
