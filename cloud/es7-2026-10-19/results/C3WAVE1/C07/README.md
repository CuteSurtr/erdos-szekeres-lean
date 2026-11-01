# C3WAVE1 / C07: machine 7 of 24, wave 1, 3-fold class (m = 11, k = 7)

**Result: 11 of my 68 roots are fully closed. 1 root is partly done and 56 were not started.
1,159 nodes certified. No SAT. No real proof rejection.** The class is not covered
(`compose.txt`: `class_covered: false`).

## What ran where
- One cloud VM: 4 cores, 15 GB RAM, no swap, memory cgroup limit 14.3 GB (`env.txt`).
  Ran 2026-10-20 from 07:35 to 11:13 UTC (driver), then this write-up.
- C3-S/C3a tools: git worktree of `8dc27c3` at `/opt/c3s`, unmodified. `/opt/work` was
  writable, so there is no path diff.
- Tool commits (`tools.txt`): CaDiCaL 3.0.1 `c6073042`. cake_lpr `a36874a8` (`make cake_lpr`;
  the bundled example prints `s VERIFIED UNSAT`). drat-trim lrat-check `2e3b2dc` with the E2
  patch.
- **cake_lpr note:** at `a36874a8`, cake_lpr ignores the `CML_HEAP_SIZE`/`CML_STACK_SIZE`
  environment variables; it now takes them as `--CML_HEAP_SIZE=` flags. So the driver's env
  setting (12000/2000) has no effect, and every check ran with the built-in default:
  4096 MB heap and 4096 MB stack. No proof failed for lack of heap.
- Base CNF: `gen_case.py 11 7 none` gives sha256
  `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (match),
  `p cnf 168399 4154921`.
- Roots: 68 depth-2 nodes, index ≡ 7 (mod 24), from the SHARD expression in `close_tree.py`.
  This list is identical to the depth-2 rows of `manifest_depth2.tsv` in sorted order, and the
  1,630-name sha256 `5412782c…` matches. The list is in `roots.txt`.
- Driver: `run.sh`. It runs one `close_tree.py … ROOT --caps 300,300,600 --cadopts=--sat
  --split-singles --hours <left>` per root, in order, with a hard stop at 11:13 UTC.
  `--jobs 4` until 08:01, then `--jobs 3` (see below).

## Incidents
1. **Lost first records (my error).** The first launch wrote `out.jsonl` and `driver.log` inside
   the git work tree. My periodic `git pull --rebase --autostash` rewrote those files, so the
   driver kept writing to unlinked inodes. Root 1's records were lost (`driver_attempt1_lost.log`).
   I stopped the run, moved the live files to `/opt/work/live`, which is copied into this
   directory at each commit, and restarted from scratch at 07:43. Root 1 was re-solved, and
   nothing from the first attempt is used. The same trap applies to any machine whose driver
   writes into the repo while it pulls with rebase.
2. **PROOF NOT ACCEPTED, cause memory, not a real rejection.** At 08:01, on node
   `0s0-1s1_2s1-4s0_3_6`, lrat-check printed `c VERIFIED`, but cake_lpr printed nothing.
   dmesg shows a memory-cgroup OOM kill of cake_lpr (anon-rss 3.8 GB) while 4 jobs ran.
   Re-run alone, the CNF sha256 matched the record, the proof had the same size
   (21,101,284 bytes), and both checkers accepted it (`recheck_0s0-1s1_2s1-4s0_3_6.md`).
   I resumed with `--jobs 3`. The driver then re-solved the node and certified it in
   `out.jsonl`, and that record is the one that counts. The failed record stays in `out.jsonl`
   with `certified: false`, and compose ignores it.
   While restarting I also fixed a `run.sh` bug: its stop check matched the old
   "PROOF NOT ACCEPTED" line in the log tail. It now checks only the current root's output.
   `driver_part1.log` is the log up to that point; `driver.log` is the log after it.
3. With one root at a time, a root that closes at once uses only one core for about 2 min.
   This follows from the "one root at a time" rule.

## Per root (`summary.tsv`; solve and check times are summed per process, in seconds)
| root | status | certified nodes by depth | splits | solve s | check s |
|---|---|---|---|---|---|
| 0s0-1s0_2s0-4s1 | closed | d2: 1 | 0 | 82 | 46 |
| 0s0-1s0_2s1-8s1 | closed | d2: 1 | 0 | 86 | 44 |
| 0s0-1s0_3s1-6s0 | closed | d2: 1 | 0 | 89 | 46 |
| 0s0-1s0_4s1-5s1 | closed | d2: 1 | 0 | 6 | 22 |
| 0s0-1s0_5s1-7s0 | closed | d2: 1 | 0 | 105 | 47 |
| 0s0-1s0_7s0-10s0 | closed | d2: 1 | 0 | 5 | 21 |
| 0s0-1s0_9s1-10s0 | closed | d2: 1 | 0 | 90 | 44 |
| 0s0-1s1_2s1-4s0 | closed (every child closed) | d3: 84, d4: 462 | 8 (1 timeout + 7 presplit) | 5943 | 9195 |
| 0s0-1s1_3s0-8s1 | closed | d2: 1 | 0 | 283 | 39 |
| 0s0-1s1_4s0-7s0 | closed | d2: 1 | 0 | 32 | 20 |
| 0s0-1s1_5s0-7s1 | closed (every child closed) | d3: 84, d4: 462 | 8 (1 timeout + 7 presplit) | 5812 | 9009 |
| 0s0-1s1_6s1-10s0 | **open** (stopped at 11:13) | d4: 58 | 8 (1 timeout + 7 presplit) | 697 | 970 |
| remaining 56 roots (index 12..67 of my list) | not started | – | – | – | – |

Each split root timed out at 300 s and has 91 children. 7 of those children are one-orbit
layers, and each was presplit into 66 nodes. So each split root has 546 depth-3/4 leaves, and
all of them closed at the first try (no further timeouts). The open root has 488 leaves left
(84 at depth 3, 404 at depth 4).

## Per depth over all roots
| depth | certified | split | open |
|---|---|---|---|
| 2 | 9 | 3 | 56 not started |
| 3 | 168 | 21 (presplit) | 84 (all below the open root, not yet run) |
| 4 | 982 | 0 | 404 (all below the open root, not yet run) |

Total: 1,163 solver runs. 1,160 were UNSAT, all certified by both checkers in the end; the one
first rejection is incident 2. 3 timed out (UNKNOWN). No SAT. CPU time: about 3.7 h solving and
5.4 h checking. The largest proof was 372 MB.

## compose.py
`python3 tools/compose.py /opt/work/base.cnf out.jsonl` (`compose.txt`):
`{"certified_nodes": 1159, "class_covered": false, "uncovered_frontier_nodes": 401, …}`.
That is the expected answer for one shard.

## Files
`env.txt`, `tools.txt`, `roots.txt`, `run.sh` (final driver), `out.jsonl` (all records),
`driver.log`, `driver_part1.log`, `driver_attempt1_lost.log`, `recheck_*.md`, `compose.txt`,
`summarize.py` and `summary.tsv` (per-root and per-depth tables; run from the C3-S tools
directory).
No CNF or proof files are committed.
