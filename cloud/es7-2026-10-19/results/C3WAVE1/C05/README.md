# C3WAVE1 / C05: machine 5 of 24, wave 1, 3-fold class (m = 11, k = 7)

## What ran where

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Solving ran from 08:19 to 11:52 UTC on 2026-10-20
and was stopped by a deadline watchdog at 11:52. Nodes still running then were discarded and have no record.

- Tools (`tools.txt`), built from source: CaDiCaL 3.0.1 `c6073042`; cake_lpr `a36874a8` (its bundled
  example prints `s VERIFIED UNSAT`); drat-trim lrat-check `2e3b2dc` with `results/E2/tools/lrat-check-E2.patch`.
- C3-S/C3a tools: a git worktree of `8dc27c3` at `/opt/c3s`, unmodified (`/opt/work` was writable, so no diff).
- Base CNF: `gen_case.py 11 7 none`, `p cnf 168399 4154921`, sha256
  `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: the 68 depth-2 nodes with index ≡ 5 (mod 24) (`roots.txt`). They come from the SHARD-mode expression of
  `close_tree.py`. The full list of 1,630 names has sha256 `5412782c…`, and both the full list and this shard
  agree with `manifest_depth2.tsv`.
- Command, run once per root, in order: `close_tree.py base.cnf out.jsonl ROOT --caps 300,300,600 --cadopts=--sat
  --split-singles --hours H`. Roots 1–7 used `--jobs 4`. From root 8 on (08:38) the run used `--jobs 3`; the next
  section says why. `out.jsonl` is the single resumable record file. `run.log` is the driver output.

## Proof rejection (not a real one)

At 08:3x the driver stopped with `PROOF NOT ACCEPTED 0s0-1s1_2s1-3s0_4_6`. lrat-check printed `c VERIFIED`, but
cake_lpr printed nothing. Four jobs were running, and cake_lpr uses a 12 GB heap. The node was then re-run alone:
same CNF sha256, same proof size, and both checkers accepted it (`recheck_0s0-1s1_2s1-3s0_4_6.txt`). The cause was
memory, so the run resumed with `--jobs 3`. The driver later certified this node itself.
**No real proof rejection. No SAT. No model was found.**

## Results

11 of the 68 roots were reached (roots.txt lines 1–11). The last of them, `0s0-1s1_5s0-6s1`, was in progress at the
stop, and the other 57 roots were not started. Of the 11, **10 are fully closed**: certified, or every child closed,
recursively. `0s0-1s1_5s0-6s1` is open.

1,326 solver runs: 1,322 certified UNSAT (both checkers), 3 UNKNOWN at the 300 s cap (the three depth-2 roots that
were split), and the one rejected run above. Total solve time 12,596 s, total check time 21,564 s. Checking cost
more than solving, mostly cake_lpr. Split records: 3 after a timeout, 21 pre-splits of single-orbit layers
(`--split-singles`).

Per root ("splits" counts split records under the root, pre-splits included):

| root | status | certified by depth | splits | solve s | check s | open frontier by depth |
|---|---|---|---|---|---|---|
| `0s0-1s0_2s0-3s1` | closed | {2: 1} | 0 | 89 | 46 | {} |
| `0s0-1s0_2s1-7s1` | closed | {2: 1} | 0 | 77 | 44 | {} |
| `0s0-1s0_3s1-5s0` | closed | {2: 1} | 0 | 80 | 45 | {} |
| `0s0-1s0_4s1-10s1` | closed | {2: 1} | 0 | 48 | 46 | {} |
| `0s0-1s0_5s1-6s0` | closed | {2: 1} | 0 | 96 | 46 | {} |
| `0s0-1s0_6s1-9s1` | closed | {2: 1} | 0 | 6 | 19 | {} |
| `0s0-1s0_9s0-10s0` | closed | {2: 1} | 0 | 6 | 21 | {} |
| `0s0-1s1_2s1-3s0` | closed | {3: 84, 4: 462} | 8 | 5956 | 9300 | {} |
| `0s0-1s1_3s0-7s1` | closed | {3: 84, 4: 462} | 8 | 4628 | 8631 | {} |
| `0s0-1s1_4s0-6s0` | closed | {2: 1} | 0 | 34 | 22 | {} |
| `0s0-1s1_5s0-6s1` | open | {4: 222} | 8 | 1569 | 3325 | {3: 84, 4: 240} |

Per depth over all roots. "Open" counts nodes not yet tried: the frontier of `0s0-1s1_5s0-6s1` at the stop.

| depth | certified | split | open |
|---|---|---|---|
| 2 | 8 | 3 | 0 |
| 3 | 168 | 21 | 84 |
| 4 | 1146 | 0 | 240 |

## compose.py

`python3 tools/compose.py /opt/work/base.cnf out.jsonl` (`compose.txt`) re-derived the CNF sha256 of all 1,322
certified nodes, with no mismatch, and printed:
`{"certified_nodes": 1322, "class_covered": false, "uncovered_frontier_nodes": 433, ...}`.
The class is not covered, as expected for one shard.

## Note on files

At 08:59 a `git pull --rebase` in the live checkout replaced `run.log` under the running driver. From then on all
commits came from a separate clone, and `run.log` was rebuilt from the runner's open file descriptor. Nothing in
`out.jsonl` was lost: it was checked identical after the change.
