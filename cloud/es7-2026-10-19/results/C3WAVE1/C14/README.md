# C3WAVE1 / C14: machine 14 of 24, wave 1, 3-fold class (m = 11, k = 7)

Status: **8 of 68 roots fully closed, 1 partly worked (open), 59 not started.** No SAT.
One proof was rejected under memory pressure; the same proof passed both checkers when re-run alone.

## What ran where
- One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Ran from 08:51 to 12:28 UTC on 2026-10-20.
- C3-S/C3a tools: worktree of commit `8dc27c3` at `/opt/c3s`, unchanged. `/opt/work` was writable, so the driver was not modified.
- cadical 3.0.1 `c60730422e758ef1cebe7aeddf2dda31c996bf04`. cake_lpr `a36874a8b750b43fe4b385b8ddbf5b033e46a3fa` (`make cake_lpr`; the bundled example prints `s VERIFIED UNSAT`). drat-trim lrat-check `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` with the E2 patch. In the sanity test, both checkers reject an unjustified empty clause and accept a justified one. Details are in `tools.txt`.
- Base CNF: `gen_case.py 11 7 none`, `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: the indices ≡ 14 (mod 24) from the driver's SHARD expression, 68 roots (`roots.tsv`). The 1,630-name list hash `5412782c…` matches `shard_plan.md`, and the set equals the depth-2 set in `manifest_depth2.tsv`.
- Command per root, in order, each root finished before the next: `close_tree.py base.cnf OUT ROOT --jobs J --caps 300,300,600 --cadopts=--sat --split-singles --hours H`, with H = the time left until 12:28 UTC. A wrapper (`run.sh`) drove it. One OUT file was used for all roots (`out.jsonl`).

## Incidents (none affect any certified record)
1. **Proof rejected under memory pressure (09:07).** Node `0s0-1s1_2s0-3s1_4_8`: lrat-check printed `c VERIFIED`, but cake_lpr printed nothing. At the time, 4 cake_lpr processes with `CML_HEAP_SIZE=12000` were running on 15 GB. The same node was re-run alone: same CNF sha256, same proof size of 19,799,625 bytes, `c VERIFIED` and `s VERIFIED UNSAT` (`recheck.jsonl`). That record was appended to `out.jsonl` (it carries a `"recheck"` field). The run then resumed with **--jobs 3** and had no further rejections. **No real proof rejection occurred.**
2. **Driver behaviour on a rejection.** On `PROOF NOT ACCEPTED`, `close_tree.py` returns from `main()`, but the `ProcessPoolExecutor` context then waits for the whole queued batch, and those results are discarded. I killed it by hand. The v3 wrapper kills the pool itself, re-checks the node alone, and resumes.
3. **Files unlinked by `git pull --rebase`.** `driver.log` and later `out.jsonl` lived in the git tree. Each rebase replaced them with new inodes, so the running processes kept writing to deleted files. Both were recovered in full from `/proc/<pid>/fd` (`driver_run0_reconstructed.log`, plus 179 records at 10:01), and the run was restarted (wrapper v3) with every live file in `/opt/work`, copied into this directory on each commit. The restart lost at most a few minutes of in-flight solves. Those nodes were simply re-solved.

## Per root (closed = certified, or every child closed, recursively)
Solve and check times are summed wall seconds per process. The 3–4 processes in parallel share the 4 cores.

| idx | root | status | certified by depth | splits | solve s | check s |
|---|---|---|---|---|---|---|
| 14 | 0s0-1s0_2s0-8s0 | closed | {2: 1} | 0 | 39 | 41 |
| 38 | 0s0-1s0_3s0-4s1 | closed | {2: 1} | 0 | 76 | 42 |
| 62 | 0s0-1s0_3s1-9s1 | closed | {2: 1} | 0 | 77 | 28 |
| 86 | 0s0-1s0_4s1-9s0 | closed | {2: 1} | 0 | 57 | 47 |
| 110 | 0s0-1s0_6s0-10s0 | closed | {2: 1} | 0 | 26 | 45 |
| 134 | 0s0-1s0_7s1-10s1 | closed | {2: 1} | 0 | 6 | 24 |
| 158 | 0s0-1s1_2s0-3s1 | closed | {3: 84, 4: 462} | 8 | 6050 | 9302 |
| 182 | 0s0-1s1_2s1-7s1 | closed | {3: 84, 4: 462} | 8 | 4791 | 9101 |
| 206 | 0s0-1s1_3s1-5s0 | open | {4: 115} | 8 | 1006 | 1824 |


The other 59 roots (indices 230, 254, …, 1622; see `summary.md`) were **not started**.

## Per depth over all 68 roots

| depth | certified | split | open (in started roots) | open (roots not started) |
|---|---|---|---|---|
| 2 | 6 | 3 | 0 | 59 |
| 3 | 168 | 21 | 84 | 0 |
| 4 | 1039 | 0 | 347 | 0 |

"Open" means not decided. At depth 3/4 under root 206 it means not yet attempted, or killed at the 12:28 cutoff. Every split node in the closed roots has all its children certified.

## compose.py
`python3 tools/compose.py /opt/work/base.cnf out.jsonl` (`compose.txt`): `certified_nodes: 1213`, `class_covered: false`, `uncovered_frontier_nodes: 412`. As expected, this shard alone does not cover the class. The 1,213 certified nodes all passed compose's recomputation of the CNF sha256 and the dual-checker filter.

## SAT
None. No `SATISFIABLE` record.

## Files
`env.txt`, `tools.txt`, `roots.tsv`, `out.jsonl` (all records), `recheck.jsonl`, `driver.log` (v2/v3 runner log), `driver_run0_reconstructed.log`, `cur_root.log` (last root's driver output), `run.sh`, `recheck.py`, `summary.md`, `compose.txt`.
