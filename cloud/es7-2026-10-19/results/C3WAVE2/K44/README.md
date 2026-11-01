# C3WAVE2 / K44: roots idx 699 down to 600, 3-fold class (m = 11, k = 7)

**Result: 18 roots closed, all certified at depth 2 with no splits. Root 19 (`0s0-4s0_2s0-7s1`) was interrupted with no records, and roots 20 to 100 were not reached. No SAT, no proof rejection, no memory problem. No roots were skipped.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 01:21:20 UTC on 2026-10-21, H = 1.0 h, END = 02:06:20 UTC. TASK.md at 852bee7.

- C3-S tools: worktree of `132398c` at /opt/c3s, unmodified.
- CaDiCaL 3.0.1 `c6073042`; cake_lpr `a36874a8` (`make cake_lpr`, its example prints `s VERIFIED UNSAT`); drat-trim lrat-check `2e3b2dc` with the E2 patch. In the sanity check, `3 0 0` on {1},{-1} is rejected by both checkers and `3 0 1 2 0` is accepted by both (`tools.txt`).
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da` (matches).
- Roots: rows of `C3WAVE2/roots.tsv` with idx 699 down to 600, in decreasing order (`roots.tsv`, 100 roots). Before each root the runner ran `git pull --rebase --autostash` and checked every `K*/out.jsonl` for a record of the root or of a descendant. **Skipped roots: none** (no root reached here was already in another machine's out.jsonl).
- Runner (`runner.sh`): `close_tree.py base.cnf out.jsonl R --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`, with S = min(0.17, hours left before END).

## Per root

| # | root | status | certified by depth | splits | solve s | check s |
|---|---|---|---|---|---|---|
| 1 | 0s0-4s0_2s1-9s1 | closed | d2: 1 | 0 | 175 | 50 |
| 2 | 0s0-4s0_2s1-9s0 | closed | d2: 1 | 0 | 14 | 29 |
| 3 | 0s0-4s0_2s1-8s1 | closed | d2: 1 | 0 | 142 | 49 |
| 4 | 0s0-4s0_2s1-8s0 | closed | d2: 1 | 0 | 67 | 39 |
| 5 | 0s0-4s0_2s1-7s1 | closed | d2: 1 | 0 | 66 | 38 |
| 6 | 0s0-4s0_2s1-7s0 | closed | d2: 1 | 0 | 89 | 43 |
| 7 | 0s0-4s0_2s1-6s1 | closed | d2: 1 | 0 | 16 | 33 |
| 8 | 0s0-4s0_2s1-6s0 | closed | d2: 1 | 0 | 96 | 41 |
| 9 | 0s0-4s0_2s1-5s1 | closed | d2: 1 | 0 | 13 | 31 |
| 10 | 0s0-4s0_2s1-5s0 | closed | d2: 1 | 0 | 120 | 46 |
| 11 | 0s0-4s0_2s1-3s1 | closed | d2: 1 | 0 | 14 | 31 |
| 12 | 0s0-4s0_2s1-3s0 | closed | d2: 1 | 0 | 244 | 59 |
| 13 | 0s0-4s0_2s1-10s1 | closed | d2: 1 | 0 | 147 | 43 |
| 14 | 0s0-4s0_2s1-10s0 | closed | d2: 1 | 0 | 16 | 31 |
| 15 | 0s0-4s0_2s0-9s1 | closed | d2: 1 | 0 | 25 | 32 |
| 16 | 0s0-4s0_2s0-9s0 | closed | d2: 1 | 0 | 180 | 47 |
| 17 | 0s0-4s0_2s0-8s1 | closed | d2: 1 | 0 | 70 | 37 |
| 18 | 0s0-4s0_2s0-8s0 | closed | d2: 1 | 0 | 88 | 39 |
| 19 | 0s0-4s0_2s0-7s1 | partial | 0 | 0 | 0 | 0 |

| 20–100 | (idx 680 down to 600, `roots.tsv`) | not reached | – | – | – | – |

Solve and check times are summed per node. They are not wall-clock: 3 jobs share 4 cores.

**Closed (18):** 0s0-4s0_2s1-9s1, 0s0-4s0_2s1-9s0, 0s0-4s0_2s1-8s1, 0s0-4s0_2s1-8s0, 0s0-4s0_2s1-7s1, 0s0-4s0_2s1-7s0, 0s0-4s0_2s1-6s1, 0s0-4s0_2s1-6s0, 0s0-4s0_2s1-5s1, 0s0-4s0_2s1-5s0, 0s0-4s0_2s1-3s1, 0s0-4s0_2s1-3s0, 0s0-4s0_2s1-10s1, 0s0-4s0_2s1-10s0, 0s0-4s0_2s0-9s1, 0s0-4s0_2s0-9s0, 0s0-4s0_2s0-8s1, 0s0-4s0_2s0-8s0.

**Partial (1):** 0s0-4s0_2s0-7s1. Its slice started at 02:02:25 with 0.066 h. About a minute later the container restarted: the kernel changed and every process was killed, the runner included. The root has no records in `out.jsonl`, so a later wave should treat it as not started.

## Totals

18 certified nodes, all at depth 2 and all with `c VERIFIED` (lrat-check, E2 patch) and `s VERIFIED UNSAT` (cake_lpr). Each was solved at the 300 s cap, with a maximum of 244 s. The summed solve time is 1,581 s and the summed check time 719 s. No splits and no UNKNOWN records.

`compose.txt`: `certified_nodes: 18, class_covered: false`, as expected. compose recomputed the CNF sha256 of all 18 certified nodes.

## SAT / proof rejections / memory

None. There was no `SAT FOUND` and no `PROOF NOT ACCEPTED` in the driver log, and no memory problem.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `compose.txt`.
