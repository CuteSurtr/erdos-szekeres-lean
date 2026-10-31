# C3WAVE1 / C12: machine 12 of 24, wave 1, 3-fold class (33 points, m = 11, k = 7)

Nothing here is a theorem. A node counts as closed only if cake_lpr printed `s VERIFIED UNSAT`
on its LRAT proof. The driver also required lrat-check (E2 patch) to print `c VERIFIED`.

## Summary

- **Roots: 68** (depth-2 nodes with index ≡ 12 mod 24). **19 fully closed, 1 partly done (468), 48 not started.**
- **1,197 certified nodes** (compose.py agrees). No SAT. No real proof rejection: one cake_lpr
  failure was a memory problem, and the node passed both checkers when re-run alone.
- `compose.py`: `class_covered: false`, 732 uncovered frontier nodes. This was expected.

## What ran where

- One cloud VM: 4 vCPU, 15 GB RAM, no swap (`env.txt`). Run from 07:38 to 11:11 UTC, 2026-10-20.
- Tools (`tools.txt`):
  - C3-S/C3a tools: worktree at `8dc27c3` in `/opt/c3s`, unmodified. `/opt/work` was writable, so there is no diff.
  - CaDiCaL 3.0.1 `c6073042`
  - cake_lpr `a36874a8`. The bundled example printed `s VERIFIED UNSAT`.
  - drat-trim lrat-check `2e3b2dc` plus `lrat-check-E2.patch`
- Base CNF: `gen_case.py 11 7 none`, `p cnf 168399 4154921`, sha256
  `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: computed with the SHARD-mode expression from `close_tree.py`. 1,630 depth-2 names,
  list sha256 `5412782c…`, identical to `manifest_depth2.tsv`. The list is in `roots.txt`.
- Command per root, run one root at a time in order (`driver.log`):
  `close_tree.py base.cnf out.jsonl ROOT --jobs J --caps 300,300,600 --cadopts=--sat --split-singles --hours H`.
  J was 4 until about 07:55 UTC and 3 after that (see the incident below). A watchdog stopped the
  driver at the end of the time budget, in the middle of root 468.

## Incidents

1. **PROOF NOT ACCEPTED, node `0s0-1s1_3s1-4s0_2_5`** at about 07:55, with `--jobs 4`.
   lrat-check printed `c VERIFIED` but cake_lpr printed nothing (recorded as `none`).
   Re-run alone, both checkers accepted: `c VERIFIED` and `s VERIFIED UNSAT`, same CNF sha256
   (`recheck_0s0-1s1_3s1-4s0_2_5.md`). Cause: memory. Four cake_lpr processes each start with
   CML_HEAP_SIZE=12000 on a 15 GB machine. I resumed with `--jobs 3`, and the driver then
   re-solved and certified the node itself. There were no more rejections at `--jobs 3`.
   The stale record (`certified: false`) is still in `out.jsonl`.
2. **Bookkeeping, not a result.** `git pull --rebase --autostash` rewrote `out.jsonl` and `driver.log`
   while the driver was writing to them. The driver went on appending to the deleted inode.
   At about 08:45 I stopped the driver and recovered the full file from its open descriptor
   (`/proc/PID/fd`): 194 records, of which the 80 visible ones were an exact prefix.
   I then resumed with the live files in `/opt/work`, copied here before each commit.
   Only in-flight solver runs were lost, and resume re-solved them.

## Per root

`summary.md` has the full table (from `summarize.py out.jsonl roots.txt`). Solve and check times
are per-node wall times summed over nodes, with 3–4 running at once.

| idx | root | status | certified by depth | splits by depth | solve s | check s |
|---|---|---|---|---|---|---|
| 12 | 0s0-1s0_2s0-7s0 | CLOSED | d2:1 | - | 18 | 24 |
| 36 | 0s0-1s0_3s0-10s1 | CLOSED | d2:1 | - | 12 | 32 |
| 60 | 0s0-1s0_3s1-8s1 | CLOSED | d2:1 | - | 55 | 43 |
| 84 | 0s0-1s0_4s1-8s0 | CLOSED | d2:1 | - | 67 | 42 |
| 108 | 0s0-1s0_5s1-9s1 | CLOSED | d2:1 | - | 13 | 31 |
| 132 | 0s0-1s0_7s0-9s1 | CLOSED | d2:1 | - | 74 | 44 |
| 156 | 0s0-1s1_2s0-10s1 | CLOSED | d2:1 | - | 64 | 43 |
| 180 | 0s0-1s1_2s1-6s1 | CLOSED | d2:1 | - | 134 | 47 |
| 204 | 0s0-1s1_3s1-4s0 | CLOSED | d3:84, d4:462 | d2:1, d3:7 | 6537 | 9809 |
| 228 | 0s0-1s1_4s0-9s1 | CLOSED | d3:84, d4:462 | d2:1, d3:7 | 3983 | 8497 |
| 252 | 0s0-1s1_5s1-10s0 | CLOSED | d2:1 | - | 206 | 32 |
| 276 | 0s0-1s1_6s1-8s1 | CLOSED | d2:1 | - | 35 | 23 |
| 300 | 0s0-1s1_8s1-9s1 | CLOSED | d2:1 | - | 32 | 23 |
| 324 | 0s0-2s0_1s1-10s0 | CLOSED | d2:1 | - | 11 | 14 |
| 348 | 0s0-2s0_3s0-6s1 | CLOSED | d2:1 | - | 100 | 32 |
| 372 | 0s0-2s0_4s0-5s0 | CLOSED | d2:1 | - | 5 | 13 |
| 396 | 0s0-2s0_5s0-10s1 | CLOSED | d2:1 | - | 55 | 27 |
| 420 | 0s0-2s0_6s0-8s0 | CLOSED | d2:1 | - | 8 | 13 |
| 444 | 0s0-2s0_7s1-9s1 | CLOSED | d2:1 | - | 6 | 14 |
| 468 | 0s0-2s1_1s0-5s1 | open (in progress) | d4:88 | d2:1, d3:7 | 685 | 1316 |
| 492 … 1620 (48 roots) | see `roots.txt` | not started | - | - | 0 | 0 |

In roots 204, 228 and 468, the root itself timed out at 300 s and was split. Its seven
one-orbit layer-3 children (`…_2` … `…_10` style) were pre-split by `--split-singles`. Each
depth-3 two-orbit child closed directly, and each depth-4 child below a single layer closed directly.
None of these nodes needed a second solve.

Totals: solve 12,101 s and check 20,120 s, summed over nodes.

## Per depth, over all roots

| depth | certified | split | still open (untried) |
|---|---|---|---|
| 2 | 17 | 3 | 48 (roots not started) |
| 3 | 168 | 21 | 84 (below root 468) |
| 4 | 1,012 | 0 | 374 (below root 468) |

No node was tried and then left open: every cap timeout was split.

## compose.py

`compose.txt`: `{"certified_nodes": 1197, "class_covered": false, "uncovered_frontier_nodes": 732, ...}`

## Files

| file | contents |
|---|---|
| `env.txt` | machine description |
| `tools.txt` | tool commits |
| `roots.txt` | this machine's 68 roots |
| `out.jsonl` | driver records (resumable input for `close_tree.py`) |
| `driver.log` | driver output |
| `compose.txt` | compose.py output |
| `summarize.py`, `summary.md` | per-root and per-depth tables |
| `recheck_0s0-1s1_3s1-4s0_2_5.md` | re-check of the rejected node |

No CNF or LRAT files are committed. All of them can be regenerated.
To resume: run `close_tree.py … out.jsonl ROOT --jobs 3 …` for the roots from 468 on.
