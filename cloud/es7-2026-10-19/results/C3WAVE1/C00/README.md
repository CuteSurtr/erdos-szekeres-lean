# C3WAVE1 / C00: machine 0 of 24, wave 1, 3-fold class (m = 11, k = 7)

**Result: 9 of my 68 roots are fully closed. Root 10 (`0s0-1s1_4`) is open, and roots 11–68 were
not started. No SAT. No real proof rejection.** One "PROOF NOT ACCEPTED" was caused by memory;
both checkers accept that node when it is checked alone (see below).

## What ran where

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`), 07:54 to 11:29 UTC on 2026-10-20.
Tools are from a worktree of commit `8dc27c3` at `/opt/c3s`, used unmodified. `/opt/work` was writable,
so there is no diff. A wrapper (`runner.sh`) ran `close_tree.py` once per root, in order:
`close_tree.py /opt/work/base.cnf out.jsonl ROOT --jobs J --caps 300,300,600 --cadopts=--sat --split-singles --hours H`,
where H is the time left until 11:33. J was 4 at first and 3 after the memory incident.

- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`); the bundled example prints `s VERIFIED UNSAT`
- drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985, with `results/E2/tools/lrat-check-E2.patch` applied.
  Sanity check: on the CNF {1},{-1}, the LRAT `3 0 0` (an unjustified empty clause) is rejected by both checkers,
  and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256
  `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: the SHARD-mode expression of `close_tree.py` main, with index ≡ 0 (mod 24), gives 68 roots
  (`roots.tsv`). Its 1,630 depth-2 names are the depth-2 set of `manifest_depth2.tsv`, and their
  name-list sha256 `5412782c…` matches `shard_plan.md`.

## Per root (depth = number of layers; roots are at depth 2)

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s0_10 | **closed** | d3: 120 | d2: 1 (pre-split) | 1869 | 2082 |
| 2 | 0s0-1s0_2s1-5s0 | **closed** | d2: 1 | 0 | 103 | 23 |
| 3 | 0s0-1s0_3s0-9s1 | **closed** | d2: 1 | 0 | 16 | 15 |
| 4 | 0s0-1s0_4s0-8s0 | **closed** | d2: 1 | 0 | 10 | 14 |
| 5 | 0s0-1s0_5s0-8s1 | **closed** | d2: 1 | 0 | 75 | 21 |
| 6 | 0s0-1s0_6s1-7s0 | **closed** | d2: 1 | 0 | 121 | 28 |
| 7 | 0s0-1s0_8s1-10s0 | **closed** | d2: 1 | 0 | 99 | 25 |
| 8 | 0s0-1s1_2s0-8s1 | **closed** | d2: 1 | 0 | 104 | 24 |
| 9 | 0s0-1s1_3s0-5s0 | **closed** | d2: 1 | 0 | 39 | 20 |
| 10 | 0s0-1s1_4 | open | d3: 101, d4: 59 | d2: 1 (pre-split); d3: 19 (timeout at 300 s); d4: 66 (pre-split) | 23826 | 4593 |
| 11–68 | (`roots.tsv`) | not started | – | – | – | – |

Solve and check times are summed per node. They are not wall-clock: with 3–4 jobs sharing the
4 cores, each per-node time is inflated.

Root 10 (`0s0-1s1_4`: one-orbit layer {4}) is pre-split into 120 depth-3 children: 101 were certified at the
300 s cap and 19 timed out and were split. Their children (and the pre-split one-orbit ones below)
give 1,454 depth-4 and 2,970 depth-5 nodes. At the stop, 59 depth-4 nodes were certified (all at
under 600 s) and 1,329 depth-4 and 2,970 depth-5 nodes were still open (never attempted).

## Per depth, over all roots

| depth | certified | split | open |
|-------|-----------|-------|------|
| 2 | 8 | 2 (both pre-split) | 58 roots not started |
| 3 | 221 | 19 (timeouts) | 0 |
| 4 | 59 | 66 (pre-split) | 1,329 |
| 5 | 0 | 0 | 2,970 |

Total: 288 certified nodes, all with `c VERIFIED` (lrat-check, E2 patch) and `s VERIFIED UNSAT`
(cake_lpr). Record counts in `out.jsonl`: at depth 3, 222 UNSAT (221 certified in the batch and 1 below) and 19 UNKNOWN at 300 s; at depth 4, 59 UNSAT at 600 s.

## compose.py

`python3 tools/compose.py /opt/work/base.cnf out.jsonl` (`compose.txt`):
`{"certified_nodes": 288, "class_covered": false, "uncovered_frontier_nodes": 355, ...}`.
As expected, the class is not covered: this machine holds only 1/24 of the shards. compose recomputed the CNF
sha256 of all 288 certified nodes from the base CNF and the node names.

## SAT / proof rejections

- **SAT: none.** No SATISFIABLE result at any node.
- **One "PROOF NOT ACCEPTED", caused by memory, not a real rejection.** Node `0s0-1s0_10_2s1-9s1` (with `--jobs 4`):
  lrat-check `c VERIFIED`, but cake_lpr printed nothing (`"none"`). Four cake_lpr runs with
  CML_HEAP_SIZE=12000 were running at once on 15 GB. When the node was re-run alone (`recheck.jsonl`), the CNF sha256 was the same
  (`4f3be36f…`), the proof was the same size (121,081,802 bytes), and lrat-check printed `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`. That record was added to
  `out.jsonl`, and the driver resumed with `--jobs 3`. There was no further rejection.

## Incidents (affect time only, not results)

1. 07:56 to 08:08: the first driver run wrote `out.jsonl`/`driver.log` inside the git checkout. A
   `git pull --rebase` right after the launch replaced those files, so the driver kept writing to deleted inodes.
   I took this for a hang and stopped the run (`driver_run0_lost.log`); its records are lost. From then on, live
   files were kept in `/opt/work` and copied in before each commit.
2. To find the cause, I ran a copy of `close_tree.py` with only a `try/except traceback` added around
   `fu.result()` on root 1. Its 31 certified records (same `solve()`, both checkers) seeded `out.jsonl`
   (the first 32 lines).
3. When the driver stops on PROOF NOT ACCEPTED, `return` inside the `ProcessPoolExecutor` block waits for the
   rest of the queued batch and throws those results away. I killed that run by hand. Workaround: kill the driver and resume.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log`,
`driver_run0_lost.log`, `recheck.jsonl`, `summary.jsonl` (per-root breakdown), `compose.txt`.
