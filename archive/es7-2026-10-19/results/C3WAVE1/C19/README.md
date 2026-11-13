# C3WAVE1 / C19: machine 19 of 24, wave 1, 3-fold class (m = 11, k = 7)

## Results

- **No SAT.** Every node that finished was UNSAT or timed out.
- **No real proof rejection.** One "PROOF NOT ACCEPTED" was caused by memory, not by the proof (see below).
- **7 of 68 roots closed**: 19, 43, 67, 91, 115, 139, 163. Root 187 (`0s0-1s1_3`) was partly done when time ran out. Roots 211–1627 (60 roots) were not started.
- **340 nodes certified.** Both cake_lpr (`s VERIFIED UNSAT`) and E2-patched lrat-check (`c VERIFIED`) accepted each one.
- `compose.py` (`compose_output.txt`) reports `certified_nodes: 340, class_covered: false, uncovered_frontier_nodes: 933`. Coverage was expected to be false, since this machine holds only 1/24 of the shards.

## What ran where

- **Machine:** one cloud VM with 4 vCPU, 15.7 GB RAM and no swap (`env.txt`). It ran from 07:35 to 11:35 UTC on 2026-10-20, and solving stopped at 11:13 UTC.
- **Tools:** the C3-S/C3a tools at commit `8dc27c3`, run unchanged from a git worktree at `/opt/c3s`. `/opt/work` was writable, so `close_tree.py` needed no diff.
- **Command:** each root was run in index order, each finished before the next started:
  `close_tree.py /opt/work/base.cnf OUT ROOT --jobs J --caps 300,300,600 --cadopts=--sat --split-singles --hours H`
- **Job count:** `--jobs 4` until 07:54, then `--jobs 3` (see the rejection section).
- **Files:**
  - `out.jsonl`: all driver records.
  - `driver.log`: driver output, with root start and end markers.
  - `roots.tsv`: this machine's 68 roots.
  - `summary.md`: per-root and per-depth tables.

### Tool commits (`tools.txt`)

| tool | commit | notes |
|---|---|---|
| cadical | c60730422e758ef1cebe7aeddf2dda31c996bf04 | version 3.0.1 |
| cake_lpr | a36874a8b750b43fe4b385b8ddbf5b033e46a3fa | built with `make cake_lpr`; prints `s VERIFIED UNSAT` on the bundled example |
| drat-trim lrat-check | 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 | with `results/E2/tools/lrat-check-E2.patch` applied |

### Base CNF and roots

- `gen_case.py 11 7 none` gives `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da`, which matches.
- The roots are the nodes with index ≡ 19 (mod 24), taken from the SHARD expression in `close_tree.py`. That gives 68 roots.
- The list is identical to the sorted depth-2 names in `manifest_depth2.tsv` (empty diff). The sha256 of the 1,630 names matches `shard_plan.md` (`5412782c…`).

## Per root

Only roots with records are shown. The other 60 roots are open and were not started.

| idx | root | status | certified by depth | splits | open by depth | solve s | check s |
|---|---|---|---|---|---|---|---|
| 19 | 0s0-1s0_2s1-10s1 | closed | d2: 1 | 0 | – | 97 | 44 |
| 43 | 0s0-1s0_3s0-7s0 | closed | d2: 1 | 0 | – | 7 | 27 |
| 67 | 0s0-1s0_4s0-5s1 | closed | d2: 1 | 0 | – | 80 | 47 |
| 91 | 0s0-1s0_5s0-6s0 | closed | d2: 1 | 0 | – | 5 | 22 |
| 115 | 0s0-1s0_6s0-8s1 | closed | d2: 1 | 0 | – | 71 | 45 |
| 139 | 0s0-1s0_8 | closed (all 120 children certified) | d3: 120 | 1 (pre-split) | – | 2,146 | 2,546 |
| 163 | 0s0-1s1_2s0-6s0 | closed | d2: 1 | 0 | – | 137 | 30 |
| 187 | 0s0-1s1_3 | **open** | d3: 112, d4: 102 | 9 (1 pre-split, 8 timeouts) | d4: 626 | 23,555 | 7,232 |

Notes on root 187:

- It was pre-split into 120 children. 112 of them were certified.
- The other 8 are the one-orbit nodes `0s0-1s1_3_{2,4,5,6,7,8,9,10}`. They hit the 300 s cap and were split into 91 children each, 728 in total.
- 102 of those 728 were certified. The other 626 were not reached or were cut off at the stop.

Solve and check times are summed over every solver run under the root, including runs that timed out. They are wall-clock seconds while 3 or 4 jobs shared the 4 cores.

## Per depth, all 68 roots

| depth | certified | split | open |
|---|---|---|---|
| 2 | 6 | 2 | 60 (not started) |
| 3 | 232 | 8 | 0 |
| 4 | 102 | 0 | 626 (all under root 187) |

- **Totals:** 349 solver runs: 341 UNSAT and 8 UNKNOWN at the cap. Solve time was 26,098 s and check time was 9,993 s.

## SAT, proof rejections and incidents

- **SAT:** none.
- **Proof rejection (memory, not real):** at 07:54 the driver printed `PROOF NOT ACCEPTED 0s0-1s0_8_2s1-10s1`. lrat-check gave `c VERIFIED`, but cake_lpr printed nothing.
  - `dmesg` shows that the memory cgroup's OOM killer killed three cake_lpr processes, each with about 4.19 GB resident. Four ran at once with `--jobs 4`.
  - I re-ran that node's solve and both checks alone. The CNF sha256 was the same (`ac3eb2f6…`), lrat-check gave `c VERIFIED`, and cake_lpr gave `s VERIFIED UNSAT` with a peak RSS of 4.2 GB. See `logs/recheck_0s0-1s0_8_2s1-10s1.txt`.
  - I resumed with `--jobs 3`. The driver re-solved the node and certified it. `out.jsonl` keeps both records, and only the second has `certified: true`. There were no further OOM kills.
  - As the task allows, the run used only 3 of the 4 cores after the change, to give cake_lpr room.
- **Lost output handles:** at 08:22 a `git pull --rebase` replaced `out.jsonl` and `driver.log` in the worktree. The running driver kept writing to the deleted inodes.
  - I recovered both files intact from `/proc/<pid>/fd`. The committed copy was an exact prefix of the recovered one.
  - The driver was restarted at 08:48, and the 3 in-flight nodes were re-run. Since then the live output is kept in `/opt/work` and copied here before each commit.
- **Driver behaviour:** on "PROOF NOT ACCEPTED" or "SAT FOUND", `close_tree.py` returns from inside the `ProcessPoolExecutor` block. It then keeps solving the queued frontier without recording anything. I killed it by hand.
