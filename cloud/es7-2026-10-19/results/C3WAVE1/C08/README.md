# C3WAVE1 / C08: machine 8 of 24, wave 1, 3-fold class (m = 11, k = 7)

## Summary

- **12 of 68 roots fully closed** (every certified or recursively all children certified): 10 directly
  at depth 2, plus `0s0-1s1_3s0-9s0` and `0s0-1s1_4s0-7s1`, each closed by 546 certified nodes at depths 3–4.
  Root 13 (`0s0-1s1_8s0-9s1`) was partly closed (116 depth-4 nodes) when time ran out; 55 roots were not started.
- **1,218 certified nodes** in total (`compose.py` agrees: `certified_nodes 1218`).
  Every one has `s VERIFIED UNSAT` from cake_lpr and `c VERIFIED` from lrat-check with the E2 patch.
- **No SAT.**
- **No real proof rejection.** One `PROOF NOT ACCEPTED` (`0s0-1s1_3s0-9s0_2_5`, 08:44) came from a memory-cgroup OOM kill of
  cake_lpr with 4 parallel jobs. Re-run alone, both checkers accept it (`recheck_0s0-1s1_3s0-9s0_2_5.txt`). The driver was
  resumed with `--jobs 3`, and later re-solved and certified that node itself.
- `compose.py`: `class_covered: false`, as expected (`compose.txt`).

## What ran where

One cloud VM: Linux 6.18, 4 cores, 15 GB RAM, no swap (`env.txt`). Setup started 08:16 UTC, the driver ran 08:19–11:52 UTC
and was stopped by a watchdog at the time limit (records are written as nodes finish).
`--jobs 4` until 08:45, `--jobs 3` after the OOM.

Tools (`tools.txt`):
- C3-S / C3a tools: worktree of `8dc27c3` at `/opt/c3s`, unmodified (`/opt/work` was writable);
- CaDiCaL 3.0.1, `c60730422e758ef1cebe7aeddf2dda31c996bf04`;
- cake_lpr `a36874a8b750b43fe4b385b8ddbf5b033e46a3fa` (`make cake_lpr`; the bundled example prints `s VERIFIED UNSAT`);
- drat-trim lrat-check `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` + `results/E2/tools/lrat-check-E2.patch`. Sanity check:
  an unjustified empty clause is rejected by both checkers, and a correct proof is accepted by both.

Base CNF: `gen_case.py 11 7 none`, `p cnf 168399 4154921`, sha256
`bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).

Roots: the SHARD-mode expression of `close_tree.py` main with i % 24 == 8 gives 68 roots. The list agrees with
`manifest_depth2.tsv` (1,630 depth-2 nodes, name-list sha256 `5412782c…` as in `shard_plan.md`). See `roots.txt` (index, node).
Roots were run one at a time, in order, by `run.sh`:
`close_tree.py base.cnf out.jsonl ROOT --jobs J --caps 300,300,600 --cadopts=--sat --split-singles --hours H`.

### Incident: lost records in part 1 (fixed)
In part 1, `out.jsonl` and `driver.log` sat in the git work tree. `git pull --rebase --autostash` replaced them, so the
driver went on writing to unlinked files. Both were recovered from `/proc/PID/fd` (`driver_part1.log`), and the driver was
restarted with its outputs in `/opt/work`, copied into this directory at each commit. One root's full record was lost:
root 8, `0s0-1s0_2s0-5s0`, certified at 08:19 (summary line in `driver_part1.log`). It was re-run (08:46) and is
certified again in `out.jsonl`. Every record in `out.jsonl` comes from the driver.

## Per root (roots that were started)

Certified nodes by depth (depth = number of layers), splits (including pre-splits of single-orbit layers), open
(unsolved frontier) nodes, and wall seconds of solve and check summed over the root's records (`summary.md`).

| idx | root | status | certified by depth | splits | open | solve s | check s |
| 8 | `0s0-1s0_2s0-5s0` | closed | d2: 1 | 0 | 0 | 6 | 12 |
| 32 | `0s0-1s0_2s1-9s0` | closed | d2: 1 | 0 | 0 | 13 | 31 |
| 56 | `0s0-1s0_3s1-6s1` | closed | d2: 1 | 0 | 0 | 14 | 29 |
| 80 | `0s0-1s0_4s1-6s0` | closed | d2: 1 | 0 | 0 | 127 | 41 |
| 104 | `0s0-1s0_5s1-7s1` | closed | d2: 1 | 0 | 0 | 6 | 17 |
| 128 | `0s0-1s0_7s0-10s1` | closed | d2: 1 | 0 | 0 | 83 | 39 |
| 152 | `0s0-1s0_9s1-10s1` | closed | d2: 1 | 0 | 0 | 6 | 21 |
| 176 | `0s0-1s1_2s1-4s1` | closed | d2: 1 | 0 | 0 | 32 | 33 |
| 200 | `0s0-1s1_3s0-9s0` | closed | d3: 84, d4: 462 | 8 | 0 | 5262 | 8025 |
| 224 | `0s0-1s1_4s0-7s1` | closed | d3: 84, d4: 462 | 8 | 0 | 6380 | 8426 |
| 248 | `0s0-1s1_5s0-8s0` | closed | d2: 1 | 0 | 0 | 45 | 22 |
| 272 | `0s0-1s1_6s1-10s1` | closed | d2: 1 | 0 | 0 | 245 | 30 |
| 296 | `0s0-1s1_8s0-9s1` | open | d4: 116 | 8 | 430 | 1166 | 1699 |
| depth | certified | split | open |
| 2 | 10 | 3 | 0 |
| 3 | 168 | 21 | 84 |
| 4 | 1040 | 0 | 346 |

Not started (time ran out), 55 roots: `0s0-2s0_1s0-8s0`, `0s0-2s0_3s0-4s1`, `0s0-2s0_3s1-9s1`, `0s0-2s0_4s1-9s0`, `0s0-2s0_6s0-10s0`, `0s0-2s0_7s1-10s1`, `0s0-2s1_1s0-3s1`, `0s0-2s1_1s1-7s1`, `0s0-2s1_3s1-5s0`, `0s0-2s1_4s1-10s1`, `0s0-2s1_5s1-6s0`, `0s0-2s1_6s1-9s1`, `0s0-2s1_9s0-10s0`, `0s0-3s0_1s1-2s0`, `0s0-3s0_2s0-7s1`, `0s0-3s0_4s0-6s0`, `0s0-3s0_5s0-6s1`, `0s0-3s0_6s0-9s0`, `0s0-3s0_8s0-10s0`, `0s0-3s1_1s0-6s1`, `0s0-3s1_2s0-10s0`, `0s0-3s1_2s1-8s0`, `0s0-3s1_4s1-7s1`, `0s0-3s1_5s1-9s0`, `0s0-3s1_7s0-9s0`, `0s0-4s0_1s0-10s0`, `0s0-4s0_1s1-6s0`, `0s0-4s0_2s1-10s1`, `0s0-4s0_3s0-9s0`, `0s0-4s0_5s0-9s1`, `0s0-4s0_6s1-8s0`, `0s0-4s0_8s1-9s0`, `0s0-4s1_1s0-9s1`, `0s0-4s1_2s0-6s0`, `0s0-4s1_3s0-10s1`, `0s0-4s1_5s0-10s0`, `0s0-4s1_6s0-7s1`, `0s0-4s1_7s1-9s0`, `0s0-5s0_1s0-4s0`, `0s0-5s0_1s1-9s0`, `0s0-5s0_2s1-6s1`, `0s0-5s0_3s1-6s0`, `0s0-5s0_4s1-7s1`, `0s0-5s0_7s0-10s1`, `0s0-5s0_9s1-10s1`, `0s0-5s1_1s1-3s1`, `0s0-5s1_2s0-9s0`, `0s0-5s1_3s0-7s1`, `0s0-5s1_4s0-8s0`, `0s0-5s1_6s1-10s1`, `0s0-5s1_8s0-9s1`, `0s0_1s0-7s1`, `0s0_2s0-3s1`, `0s0_2s1-8s1`, `0s0_4s0-5s1`.

| depth | certified | split | open |
|---|---|---|---|
| 2 | 10 | 3 | 0 |
| 3 | 168 | 21 | 84 |
| 4 | 1040 | 0 | 346 |

closed roots: 12 of 68
UNSAT records not certified (driver PROOF NOT ACCEPTED): ['0s0-1s1_3s0-9s0_2_5'] ; of these never certified later: []
total solve s (all records): 13384 check s: 18426

Total over all records: solve 13,384 s, check 18,426 s. Checking (lrat-check + cake_lpr) costs about 1.4× solve here,
because most nodes are small (3–30 s solve) and both checkers parse the 4.15 M-clause CNF.

## Files

- `out.jsonl`: driver records (resumable; the same file was used for all roots);
- `driver.log`, `driver_part1.log`: driver output;
- `roots.txt`, `roots_done.txt`;
- `run.sh`, `watchdog.sh`, `commit.sh`: the loop, the time-limit stop and the commit helper;
- `recheck_0s0-1s1_3s0-9s0_2_5.txt`: the OOM re-check;
- `compose.txt`: `compose.py` output;
- `summary.md`, `summarize_c08.py`: per-root and per-depth tables, including roots not started.
