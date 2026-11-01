# C3WAVE1 / C21: machine 21 of 24, wave 1, 3-fold class (m = 11, k = 7)

Nothing here is a theorem. A node counts as closed only when cake_lpr printed
`s VERIFIED UNSAT` on its LRAT proof and lrat-check (E2 patch) printed `c VERIFIED`.

## Summary

- 68 roots (the depth-2 nodes with index ≡ 21 mod 24). They were taken one at a time, in order.
  **Roots 0–10 (11 roots) are fully closed. Root 11 (`0s0-1s1_7s0-9s1`) was cut off by the
  time limit: 296 nodes certified, 250 still open. Roots 12–67 (56) were not started.**
- 1,397 certified nodes: 9 at depth 2, 168 at depth 3, 1,220 at depth 4. `compose.py`
  recomputed every node's CNF sha256 from the base CNF and accepted all 1,397 as certified
  nodes. It reports `class_covered: false`, as expected.
- **No SAT.** **No real proof rejection.** In one case cake_lpr printed nothing while 4
  checkers ran at once (memory); that node passed when checked alone (details below).

## What ran where

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`), 2026-10-20 07:35–11:15 UTC. Solving
ran from 07:38 to 11:12. The driver ran with `--jobs 4` until 08:03 and with `--jobs 3` after
that (see "Proof rejection").

Tools (`tools.txt`):
- C3-S / C3a tools: worktree of commit `8dc27c3` at `/opt/c3s`, **unmodified**. `/opt/work`
  was writable, so no path change was needed.
- cadical: CaDiCaL 3.0.1, `c60730422e758ef1cebe7aeddf2dda31c996bf04`
- cake_lpr: `a36874a8b750b43fe4b385b8ddbf5b033e46a3fa`, `make cake_lpr`. The bundled example
  printed `s VERIFIED UNSAT`.
- lrat-check: drat-trim `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` with
  `results/E2/tools/lrat-check-E2.patch`

Base CNF: `gen_case.py 11 7 none` gives `p cnf 168399 4154921`, sha256
`bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches the expected value).

Roots: `roots.tsv`, computed with the same expression `close_tree.py` uses in SHARD mode.
It agrees with `manifest_depth2.tsv` (1,630 depth-2 nodes; 68 have index ≡ 21 mod 24).

Command, one root at a time (via `/opt/work/runner.sh`; H = the time left until 11:12, and the
driver was killed at 11:12):
`python3 close_tree.py /opt/work/base.cnf out.jsonl ROOT --jobs 4|3 --caps 300,300,600 --cadopts=--sat --split-singles --hours H`

## Per root

"splits" counts the root split plus pre-split single-orbit nodes. Solve and check times are
wall seconds per node, summed (3–4 nodes ran in parallel).

| # | root | status | certified by depth | splits | open leaves | solve s | check s |
|---|---|---|---|---|---|---|---|
| 0 | `0s0-1s0_2s1-3s1` | closed | d2:1 | 0 | 0 | 9 | 28 |
| 1 | `0s0-1s0_3s0-8s0` | closed | d2:1 | 0 | 0 | 14 | 28 |
| 2 | `0s0-1s0_4s0-6s1` | closed | d2:1 | 0 | 0 | 67 | 37 |
| 3 | `0s0-1s0_5s0-7s0` | closed | d2:1 | 0 | 0 | 4 | 19 |
| 4 | `0s0-1s0_6s0-9s1` | closed | d2:1 | 0 | 0 | 58 | 36 |
| 5 | `0s0-1s0_8s0-10s1` | closed | d2:1 | 0 | 0 | 77 | 42 |
| 6 | `0s0-1s1_2s0-7s0` | closed | d2:1 | 0 | 0 | 239 | 52 |
| 7 | `0s0-1s1_3s0-10s1` | closed | d2:1 | 0 | 0 | 64 | 38 |
| 8 | `0s0-1s1_3s1-8s1` | closed | d3:84, d4:462 | 8 | 0 | 4462 | 8520 |
| 9 | `0s0-1s1_4s1-8s0` | closed | d3:84, d4:462 | 8 | 0 | 4549 | 8384 |
| 10 | `0s0-1s1_5s1-9s1` | closed | d2:1 | 0 | 0 | 184 | 35 |
| 11 | `0s0-1s1_7s0-9s1` | **open** | d4:296 | 8 | 250 (84 at d3, 166 at d4) | 1969 | 4189 |
| 12–67 | see `summary.md` | not started | – | – | – | – | – |

Root 8's solve time includes the 300 s timeout at depth 2. The depth-3 nodes under 8 and 9 all
closed within their 300 s cap and the depth-4 nodes within 600 s. Below each split root, 7
single-orbit depth-3 nodes were pre-split, each into 66 depth-4 children.

## Per depth, over all roots touched (0–11)

| depth | certified | split | open |
|---|---|---|---|
| 2 | 9 | 3 (roots 8, 9, 11; 300 s timeouts) | 0 |
| 3 | 168 | 21 (pre-split single-orbit nodes, not solved) | 84 (under root 11, not yet tried) |
| 4 | 1,220 | 0 | 166 (under root 11, queued) |

No node at depth 3 or 4 timed out. Every node that was tried closed.

## SAT

None.

## Proof rejection

One (`root_reject1.log`), and it is not a real rejection. Node `0s0-1s1_3s1-8s1_2_5` (depth 4)
was UNSAT in 7.8 s. lrat-check printed `c VERIFIED`, but cake_lpr printed nothing
(`"cake_lpr": "none"`). That was while 4 nodes, and so up to 4 cake_lpr processes with
`CML_HEAP_SIZE=12000`, shared 15 GB. The driver stopped on "PROOF NOT ACCEPTED". I re-ran that
node alone with the driver's own `solve()`: UNSAT in 8.8 s, `c VERIFIED` and
`s VERIFIED UNSAT` (check 21.8 s), the same CNF sha256 `9a909747…`. That record is in
`out.jsonl` with `"recheck_alone": true`. I resumed with `--jobs 3`, as the task says, and
there were no more failures. The failed record is kept in `out.jsonl`, and `compose.py` uses
only the certified one.

## Incident (no data lost in the end)

At first the live `out.jsonl` and `run.log` sat inside the git checkout. The
`git pull --rebase --autostash` before each push replaced those files under the running driver,
so root 5's record went to a deleted inode. I recovered the runner log from `/proc`
(`run1.log`), stopped everything at 07:56, and moved the live files to `/opt/work`, copying them
in only to commit. Root 5 was then solved again (records in `out.jsonl`, `run2.log`). The node
in progress at 07:56 (root 8's first attempt) was restarted.

## Files

- `env.txt`, `tools.txt`, `roots.tsv`
- `out.jsonl`: every record from the driver (resumable; reuse it to continue from root 11)
- `run1.log` (07:38–07:54, recovered), `run2.log` (07:56–08:03), `run3.log` (08:03–11:12): the
  runner and driver output
- `compose.txt`: `compose.py` output (1,397 certified nodes, `class_covered: false`, 423
  uncovered frontier nodes)
- `summary.md`, `summarize.py`: per-root and per-depth tables (a node is covered if it is
  certified, or split with every child covered)
