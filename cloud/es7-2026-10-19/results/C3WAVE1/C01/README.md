# C3WAVE1 / C01 — machine 1 of 24, wave 1, 3-fold class (m = 11, k = 7)

Nothing here is a theorem. A node counts as closed only if cake_lpr printed `s VERIFIED UNSAT`
on its LRAT proof (and the E2-patched lrat-check printed `c VERIFIED`; the driver requires both).

## What ran where
- One cloud VM: 4 vCPU, 15 GB RAM, no swap (`env.txt`). Start 07:35 UTC, driver stopped by the
  deadline at 11:15:46 UTC, 2026-10-20.
- C3-S / C3a tools from a worktree of `8dc27c3` (`/opt/c3s`), unmodified. `/opt/work` was
  writable, so the driver's work path was not changed.
- Tools (`tools.txt`): CaDiCaL 3.0.1 `c6073042`; cake_lpr `a36874a8` (`make cake_lpr`; bundled
  example prints `s VERIFIED UNSAT`); drat-trim `2e3b2dc` lrat-check + `results/E2/tools/lrat-check-E2.patch`.
  Control: a SAT formula with a hintless empty clause is rejected by both checkers.
- Base CNF `gen_case.py 11 7 none`: sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: 68 depth-2 nodes with index ≡ 1 (mod 24), from the SHARD-mode expression in
  `close_tree.py` main. The 1,630 names equal the depth-2 rows of `manifest_depth2.tsv` (name-list
  sha256 `5412782c…6b7e` as in shard_plan.md). List: `roots.txt`.
- Command per root, in order, one at a time (`run_roots.sh`):
  `close_tree.py base.cnf out.jsonl ROOT --jobs J --caps 300,300,600 --cadopts=--sat --split-singles --hours H`.
  J = 4 at first, then 3 from 08:00 UTC (memory, see below).

## Deviations and incidents (all recorded in `run.log`, `tools.txt`)
1. **cake_lpr flag change.** At `a36874a8`, cake_lpr no longer reads `CML_HEAP_SIZE`/`CML_STACK_SIZE`
   from the environment, which is how `controls.dual` sets them. So `cake_lpr` on PATH is a wrapper
   (`cake_lpr_wrapper.sh`). Final version: first try with heap 5000 MB in one of two lock slots. If
   that does not print `s VERIFIED UNSAT`, retry with the driver's 12000/2000 MB holding both slots.
   Acceptance is still cake_lpr's own `s VERIFIED UNSAT`. Heap test on a 219 MB proof: 12000 MB →
   11.6 GB RSS; 5000 → 32 s, `s VERIFIED UNSAT`; 3000 → 33 s, `s VERIFIED UNSAT`. The large-heap retry
   was never needed (no `cake_retries.log` entries).
2. **OOM (memory).** With `--jobs 4`, several concurrent cake_lpr checks with 12 GB heaps hit the
   15 GB cgroup limit. 19 cake_lpr processes were OOM-killed between 07:51 and 08:19 UTC
   (`oom_dmesg.txt`). As instructed, I lowered `--jobs` to 3 and resumed. There were no OOM kills after 08:19.
3. **Lost records (git).** Until 08:30, OUT.jsonl and run.log were written inside the git tree.
   `git pull --rebase --autostash` replaces those files, so the running driver went on writing to
   unlinked inodes. That cost root 1's first attempt (07:39–07:53, no records). The records from
   08:05–08:30 were recovered from `/proc/PID/fd` (identical prefix with the committed copy). Since
   then the live files are in `/opt/work` and are copied here at each commit. Of the earlier roots,
   25–97 were solved before the first such rewrite or recovered, and every certified record is in `out.jsonl`.
4. **One "PROOF NOT ACCEPTED", caused by memory and not a real rejection** (`rejection_recheck.md`):
   `0s0-1s0_2_3s0-8s1`, lrat-check `c VERIFIED`, cake_lpr no output. Its cake_lpr was OOM-killed at
   08:18–08:19, while my own heap test ran beside the driver. Re-run alone: same CNF sha256, same
   proof size, `c VERIFIED` + `s VERIFIED UNSAT`. The driver then re-solved and certified it in a
   later record, and only that record counts.
5. The runner prints `ALL DONE` after a deadline break too. Here that line only means "stopped at the deadline".

## Results

**No SAT. No real proof rejection.** Up to the end of root 169, every node solved was UNSAT, and
every one was certified by both checkers.

Per root (only the roots that were reached; roots after 193 in `roots.txt` were not started):

| root (index) | status | certified nodes by depth | splits (incl. pre-splits) | open leaves | solve s | check s |
|---|---|---|---|---|---|---|
| 0s0-1s0_2 (1) | **closed** (all 120 children certified) | d3: 120 | 1 | 0 | 1,424 | 4,105 |
| 0s0-1s0_2s1-5s1 (25) | **closed** (certified) | d2: 1 | 0 | 0 | 10 | 54 |
| 0s0-1s0_3s1-10s0 (49) | **closed** | d2: 1 | 0 | 0 | 11 | 60 |
| 0s0-1s0_4s0-8s1 (73) | **closed** | d2: 1 | 0 | 0 | 54 | 68 |
| 0s0-1s0_5s0-9s0 (97) | **closed** | d2: 1 | 0 | 0 | 14 | 58 |
| 0s0-1s0_6s1-7s1 (121) | **closed** | d2: 1 | 0 | 0 | 5 | 21 |
| 0s0-1s0_8s1-10s1 (145) | **closed** | d2: 1 | 0 | 0 | 6 | 20 |
| 0s0-1s1_2s0-9s0 (169) | **closed** (recursively: d2 timed out at 300 s, all descendants closed) | d3: 84, d4: 462 | 8 | 0 | 4,883 | 11,507 |
| 0s0-1s1_3s0-5s1 (193) | open (stopped at the deadline) | d4: 309 | 8 | 237 (84 at d3, 153 at d4) | 1,949 | 5,902 |
| other 59 roots (217 … 1609) | not started | – | – | – | – | – |

Times are wall seconds per node, summed (3 concurrent jobs; the check time includes waiting for a
cake_lpr slot). Over all records: 984 solver runs, 2 timeouts (the depth-2 nodes 169 and 193),
8,356 s solving, 21,794 s checking, largest proof 254 MB.

Per depth, over all reached roots (nodes in the subtrees of the 9 roots above):

| depth | certified | split | still open |
|---|---|---|---|
| 2 | 6 | 3 | 0 |
| 3 | 204 | 14 | 84 |
| 4 | 771 | 0 | 153 |

Fully closed roots (8 of 68): indices 1, 25, 49, 73, 97, 121, 145, 169. Open: 193 (partly done) and
the 59 roots not started.

`compose.py base.cnf out.jsonl` (`compose.txt`):
```
{"certified_nodes": 981, "class_covered": false, "uncovered_frontier_nodes": 413, ...}
```
As expected, the class is not covered by this shard alone.

## Files
`env.txt`, `tools.txt`, `roots.txt`, `run_roots.sh`, `cake_lpr_wrapper.sh`, `out.jsonl` (all records,
resumable), `run.log`, `summary.md` (from `summarize_c01.py`, run from C3-S/tools), `compose.txt`,
`oom_dmesg.txt`, `rejection_recheck.md`. No CNF or proof files are committed.

To resume: put `out.jsonl` back at `/opt/work/out.jsonl` and run `run_roots.sh`. Root 193 continues
from its frontier.
