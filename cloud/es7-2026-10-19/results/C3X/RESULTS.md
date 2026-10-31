# C3X results (H = 1.0 h, Z = d88e0d49)

One cloud VM, 4 cores, 15 GB, no swap (`env.txt`), 2026-10-21 01:20–02:15 UTC. Budget per (node, method): 120 s wall
on all 4 cores. **No SAT. No proof rejection.** 7 runs completed (`records.jsonl`, one line per run, with every subproblem).

## Table

| node | depth | method | closed | certified/unsat/subproblems | wall s | solve s (sum) | check s (sum) | largest sub s | notes |
|---|---|---|---|---|---|---|---|---|---|
| `0s0-1s1_2s1-8s1_6s1-9s0` | 3 | ref | yes | 1/1/1 | 88.2 | 44.3 | 42.9 | 44.3 | splits 0; wall includes checks |
| `0s0-1s1_2s1-8s1_6s1-9s0` | 3 | march4 | no | 0/0/0 | 120.4 | 0 | 0 | 0 | march 120.1 s, 0 cubes |
| `0s0-1s1_2s1-8s1_6s1-9s0` | 3 | split | yes | 45/45/45 | 89.8 | 321.2 | 854.4 | 20.9 |  |
| `0s0-1s1_2s1-8s1_6s1-9s0` | 3 | opt | yes | 4/4/4 | 74.9 | 208.5 | 147.3 | 74.2 | 4 option sets in parallel; closed if any one certified |
| `0s0-1s1_6s0-9s1_5s0-10s1` | 3 | ref | yes | 1/1/1 | 71.7 | 38.2 | 32.8 | 38.2 | splits 0; wall includes checks |
| `0s0-1s1_6s0-9s1_5s0-10s1` | 3 | opt | yes | 4/4/4 | 92.2 | 227.2 | 144.5 | 92.0 | 4 option sets in parallel; closed if any one certified |
| `0s0-1s1_6s0-9s1_5s0-10s1` | 3 | march2 | no | 0/0/0 | 120.4 | 0 | 0 | 0 | march 120.1 s, 0 cubes |
| `0s0-1s1_6s1-10s0_2_7s0-9s0` | 4 | ref | yes | 1/1/1 | 26.3 | 4.6 | 21.1 | 4.6 | splits 0; wall includes checks |

"certified" = both lrat-check (E2 patch) printed `c VERIFIED` and cake_lpr printed the exact line `s VERIFIED UNSAT` on the
subproblem's LRAT proof. "wall s" is the solve window (budget 120 s) except for `ref`, where close_tree.py's own wall time
includes its checks. Check seconds are not wall-clock: from `split` on node 1 they ran one at a time, later 2 at a time.

## Certified vs measured

- **Certified** (every proof accepted by both checkers): all 6 `closed = yes` rows. Node `0s0-1s1_2s1-8s1_6s1-9s0` is
  certified three independent ways (ref: the node itself; split: all 45 children, which are `tree_children` of the node,
  so cover it by the layer-tree soundness argument in `C3-S/soundness.md`; opt: the node itself, 4 times).
  Node `0s0-1s1_6s0-9s1_5s0-10s1` is certified by ref and by opt (4 proofs).
- **Measured only**: the two march rows (march_cu did not finish cubing within 120 s, so nothing was solved); all timing comparisons.
- **Not run** (time): split and march on nodes 2–4; all methods on the depth-4 node `0s0-1s1_6s1-10s0_2_7s0-9s0` (its ref
  run was killed at the stop, no record) and on the one-orbit layer-2 root `0s0-3s0_4`.

## What was learned

1. **The chosen depth-3 nodes were not hard.** I took open two-orbit depth-3 nodes under roots that timed out at 300 s
   (from the C3WAVE1/C3WAVE2 frontier, where most siblings are certified). Both closed at the node itself in 38–44 s of
   CaDiCaL `--sat`. They were open only because no machine had reached them, not because they resist the solver.
   So the method comparison here is on easy nodes; it does not yet answer the question for the true stalls
   (e.g. `0s0-1s1_4`'s depth-4/5 frontier).
2. **march_cu is too slow to cube these node CNFs**: at depth 4 and even depth 2 it produced no cubes in 120 s (168k vars,
   4.15M clauses). This agrees with C3a/shard_plan.md and C3-S "Measurements". Not usable at node level at this budget.
3. **Splitting on the next layer's orbit choice (`split`) costs far more checking**: on node 1 it needed 45 subproblems,
   321 s solve (sum) and 854 s check (sum) versus 44 s solve and 43 s check for one node solve. The largest child took 21 s,
   so splitting first only pays where a node does not close within its cap, which close_tree.py already does adaptively.
4. **New CaDiCaL options** (`--reducetarget=50`, `--reducetier1glue=3 --reducetier2glue=8`, `--bumpreasondepth=2` with `--sat`;
   `--unsat --vivifytier1eff=20`): all four closed both nodes. With 4 solves sharing 4 cores the three `--sat` variants took
   41–47 s, close to the lone `--sat` reference (38–44 s with the cores otherwise idle), i.e. likely somewhat faster per core,
   but one sample per node and different load: not a significant difference. `--unsat` was slowest (74–92 s), consistent with
   the C3-S finding that `--sat` helps.

## Recommendation for the next wave

Keep the current method: `close_tree.py` with caps 300/300/600, `--cadopts=--sat`, `--split-singles`. Evidence: it
closed both nodes in one subproblem with the least total solve + check time (87 s and 71 s); march_cu produced no cubes;
pre-splitting multiplied check cost ~20×; no new option beat `--sat` clearly. A cheap, untested-at-scale option to try in a
portfolio is `--sat --reducetier1glue=3 --reducetier2glue=8` or `--sat --reducetarget=50` (each was fastest on one node under
4-way load). The real stalls (depth 4–5 under one-orbit roots) still need a longer C3X run on those nodes specifically.
