# C3WAVE1 / C04: machine 4 of 24, wave 1 of the 3-fold class

Nothing here is a theorem. A node counts as closed only if cake_lpr printed `s VERIFIED UNSAT`
(and the E2-patched lrat-check `c VERIFIED`) on its LRAT proof.

## What ran where
- One cloud VM: 4 cores, 15 GB RAM (memcg limit 14.3 GB), no swap (`env.txt`). Run 07:35–11:12 UTC on 2026-10-20.
- C3-S/C3a tools: git worktree of `8dc27c3` at `/opt/c3s`, unmodified (`/opt/work` was writable).
- Tools built from source (`tools.txt`): CaDiCaL 3.0.1 `c6073042`; cake_lpr `a36874a8` (bundled example prints
  `s VERIFIED UNSAT`); drat-trim lrat-check `2e3b2dc` + `E2/tools/lrat-check-E2.patch`.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256
  `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: 68 depth-2 nodes with index ≡ 4 (mod 24) (`roots.txt`). Taken from the SHARD expression in `close_tree.py`;
  they agree with `manifest_depth2.tsv` (full list sha256 `5412782c…`, which matches).
- Roots were run one at a time, in order (`close_tree.py BASE out.jsonl ROOT --jobs J --caps 300,300,600
  --cadopts=--sat --split-singles --hours H`), with J = 4 until 08:06 and J = 3 after it (see the proof rejection below). A
  wrapper killed the driver at 11:12 (`run.log`).

## Data-loss incident and reconstruction (read this)
My periodic committer ran `git pull --rebase --autostash` in the repository checkout, which rewrote
`out.jsonl` while the driver still held it open in append mode. After each rewrite, the driver's appends went to an
unlinked file until the next root started. **`out.jsonl` keeps only 373 records (353 certified).**
The driver's stdout (`run.log`) keeps one line per finished node: node, status, solve_s and the certified flag.
The driver prints that line only after it writes the full record, and `certified: true` there means `dual()` returned
lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`. `reconstruct_from_runlog.py` rebuilds the missing records from
`run.log` into **`out_reconstructed.jsonl` (848 certified, each marked `reconstructed_from_run_log`)**. It recomputes
each CNF sha256 from base + units with compose.py's `node_sha`. The proof checker strings and check times in those
records are inferred, not logged, and they cannot be re-checked without re-running: the CNFs and proofs were deleted
as designed. To audit them independently, re-run those nodes. Check times below cover only the records that survived.
(Fix for other machines: keep OUT.jsonl outside the git checkout and copy it in before committing.)

## compose.py
- `compose.py base.cnf out.jsonl` (surviving records only): `certified_nodes 353, class_covered false` (`compose.txt`).
- `compose.py base.cnf out.jsonl out_reconstructed.jsonl`: `certified_nodes 1201, class_covered false,
  uncovered_frontier_nodes 323`; all sha256 matched (`compose_merged.txt`).

## Per root (merged records; `summary_merged.json`; surviving records only: `summary.json`)
| idx | root | state | certified by depth | splits | solve s | check s (surviving) |
|---|---|---|---|---|---|---|
| 4 | 0s0-1s0_2s0-3s0 | closed | d2: 1 | 0 | 5 | 26 |
| 28 | 0s0-1s0_2s1-7s0 | closed | d2: 1 | 0 | 60 | 40 |
| 52 | 0s0-1s0_3s1-4s1 | closed | d2: 1 | 0 | 11 | 35 |
| 76 | 0s0-1s0_4s1-10s0 | closed | d2: 1 | 0 | 11 | 28 |
| 100 | 0s0-1s0_5s1-10s1 | closed | d2: 1 | 0 | 22 | 31 |
| 124 | 0s0-1s0_6s1-9s0 | closed | d2: 1 | 0 | 114 | 50 |
| 148 | 0s0-1s0_9 | closed | d3: 120 | 1 (presplit) | 2139 | 2252 |
| 172 | 0s0-1s1_2s1-10s1 | closed | d3: 84, d4: 462 | d2: 1 (timeout), d3: 7 (presplit) | 6816 | 1156 |
| 196 | 0s0-1s1_3s0-7s0 | closed | d2: 1 | 0 | 145 | 30 |
| 220 | 0s0-1s1_4s0-5s1 | **open** (18 depth-3 nodes not finished at the deadline) | d3: 66, d4: 462 | d2: 1 (timeout), d3: 7 (presplit) | 5813 | 2051 |
| 244… | the other 58 roots (0s0-1s1_5s0-6s0 onward) | not started | | | | |

Solve times include re-runs. 0s0-1s0_9_4s0-6s1 was solved twice, and 0s0-1s0_9 was partly re-run after the OOM stop.
Wall-clock times were measured with 3–4 processes on 4 cores.

Fully closed roots (certified, or every child closed, recursively): 9 of 68. They are 0s0-1s0_2s0-3s0, 0s0-1s0_2s1-7s0,
0s0-1s0_3s1-4s1, 0s0-1s0_4s1-10s0, 0s0-1s0_5s1-10s1, 0s0-1s0_6s1-9s0, 0s0-1s0_9, 0s0-1s1_2s1-10s1 and 0s0-1s1_3s0-7s0.
On the surviving records alone, 8 are closed (0s0-1s1_2s1-10s1 needs reconstructed records).

## Per depth, over all roots (merged)
| depth | certified | split | still open |
|---|---|---|---|
| 2 | 7 | 3 | 0 (plus 58 roots not started) |
| 3 | 270 | 14 | 18 |
| 4 | 924 | 0 | 0 |

## SAT / proof rejections
- **No SAT** answer.
- **One "PROOF NOT ACCEPTED"**, for 0s0-1s0_9_4s0-6s1 at 07:58 with jobs 4: lrat-check said `c VERIFIED` and cake_lpr's output was `none`.
  Cause: the kernel memcg OOM killer killed cake_lpr (dmesg). Run alone, the node gave the same CNF sha256 and the same UNSAT result,
  lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT` (`recheck_0s0-1s0_9_4s0-6s1.txt`). The run resumed with jobs 3 and
  certified the node again. There was no real rejection.
- Two 300 s timeouts (the depth-2 roots 0s0-1s1_2s1-10s1 and 0s0-1s1_4s0-5s1); both were split.
