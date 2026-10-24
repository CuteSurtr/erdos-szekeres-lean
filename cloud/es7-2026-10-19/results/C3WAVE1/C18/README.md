# C3WAVE1 / C18: machine 18 of 24, wave 1, 3-fold class (m = 11, k = 7)

## What ran where

One cloud VM (`env.txt`): 4 cores, 15 GB RAM (cgroup limit 14.3 GB), no swap.
Started 07:35 UTC on 2026-10-20. The driver was stopped at 11:15 UTC.
The C3-S and C3a tools were run from a git worktree at `8dc27c3` (`/opt/c3s`). `/opt/work` was
writable, so the driver is unchanged. Runner: `run.sh` (one root at a time, in order).

Tools (`tools.txt`):
- cadical: CaDiCaL 3.0.1, c60730422e758ef1cebe7aeddf2dda31c996bf04
- cake_lpr: a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, `make cake_lpr`. The bundled example
  prints `s VERIFIED UNSAT`.
- lrat-check: drat-trim 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with the E2 patch. It rejects
  the trivial bogus empty-clause proof ("c NOT VERIFIED").

Base CNF: `gen_case.py 11 7 none`, `p cnf 168399 4154921`, sha256
`bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da`. This matches the
expected value.

Roots: the 68 depth-2 nodes with index ≡ 18 (mod 24), listed in `roots.txt`. The SHARD
expression in `close_tree.py` gives the same 1,630 names as `manifest_depth2.tsv` (sha256 of
the names `5412782c…`).

Command per root:
`close_tree.py base.cnf out.jsonl ROOT --jobs J --caps 300,300,600 --cadopts=--sat --split-singles --hours H`.
J was 4 at first, then 3 from 07:49 (see below).

## Results: 9 of 68 roots attempted, no SAT, no real proof rejection

`compose.py` output (`compose.txt`): `certified_nodes: 721, class_covered: false`.

| # | root | status | certified nodes by depth | splits | solve s | check s |
|---|------|--------|--------------------------|--------|---------|---------|
| 1 | 0s0-1s0_2s1-10s0 | **closed** | d2: 1 | 0 | 12 | 18 |
| 2 | 0s0-1s0_3s0-6s1 | **closed** | d2: 1 | 0 | 70 | 46 |
| 3 | 0s0-1s0_4s0-5s0 | **closed** | d2: 1 | 0 | 4 | 20 |
| 4 | 0s0-1s0_5s0-10s1 | **closed** | d2: 1 | 0 | 36 | 42 |
| 5 | 0s0-1s0_6s0-8s0 | **closed** | d2: 1 | 0 | 6 | 23 |
| 6 | 0s0-1s0_7s1-9s1 | **closed** | d2: 1 | 0 | 5 | 23 |
| 7 | 0s0-1s1_2s0-5s1 | **closed per driver log; records lost, open for compose** | in out.jsonl: d3: 34 (log: d3: 84, d4: 462) | 8 | ~6,400 (log) | — |
| 8 | 0s0-1s1_2s1-9s1 | **closed** | d3: 84, d4: 462 | 8 | 6,249 | 9,579 |
| 9 | 0s0-1s1_3s1-7s0 | open (stopped at the deadline; 411 nodes not done) | d4: 135 | 8 | 1,088 | 2,090 |

Roots 10–68 were not started.

"Splits" counts the timed-out depth-2 node plus its pre-split single-orbit children
(`--split-singles`). Times are wall-clock per process, with 3–4 processes sharing 4 cores.
Every depth-3 and depth-4 node closed within its cap; nothing below depth 4 was needed.

Per depth, over all roots, as counted from out.jsonl (`summary.txt`, `summarize_c18.py`):

| depth | certified | split | open (untried or lost) |
|-------|-----------|-------|------------------------|
| 2 | 6 | 3 | 0 |
| 3 | 118 | 21 | 134 |
| 4 | 597 | 0 | 789 |

The open nodes are 512 lost records under root 7 and 411 untried nodes under root 9.

Fully closed, and counted by compose: roots 1–6 and 8 (7 roots).

## Problems

1. **PROOF NOT ACCEPTED, 0s0-1s1_2s0-5s1_3_4 (07:48): memory, not a real rejection.**
   cake_lpr was OOM-killed (dmesg) while 4 cake_lpr processes ran at about 4 GB each.
   lrat-check had printed "c VERIFIED". Re-run alone: both checkers accept
   (`rejection_0s0-1s1_2s0-5s1_3_4.md`, `recheck_*.json`). Resumed with --jobs 3. The
   driver later re-certified the node (`run.log`). No other rejection.
2. **Lost records (my error, `records_lost_root7.md`).** The driver wrote out.jsonl inside the
   git working tree, and my periodic `git pull --rebase --autostash` replaced the file under
   the running driver. Root 7's driver printed certified: true for all 546 nodes and
   `open_frontier: 0`. But 512 full records (50 at depth 3, 462 at depth 4) never reached
   out.jsonl, so compose cannot count root 7. **It needs a re-run (about 90 min at --jobs 3).**
   Root 1 was lost the same way and was re-run at 11:17. Fixed at 09:31: commits now go
   through a separate clone. Root 8's records are complete (its file was opened after the
   last rebase).
3. No SAT.

## Files

`out.jsonl` (driver records), `run_part1.log` (07:37–07:49, jobs 4), `run.log` (from 07:49,
jobs 3, driver stdout), `compose.txt`, `summary.txt`, `summarize_c18.py`, `roots.txt`,
`tools.txt`, `run.sh`, `env.txt`, `rejection_*.md`, `recheck_*.json`, `records_lost_root7.md`.
