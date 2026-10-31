# C3WAVE1 / C13: machine 13 of 24, wave 1, 3-fold class (m = 11, k = 7)

## What ran where
- One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`), 08:51–12:28 UTC on 2026-10-20.
- C3-S/C3a tools: worktree of commit `8dc27c3` at `/opt/c3s`. Not modified (`/opt/work` was writable, so no diff).
- Tools (`tools.txt`): CaDiCaL 3.0.1 `c6073042`; cake_lpr `a36874a8` (`make cake_lpr`; the bundled example prints
  `s VERIFIED UNSAT`); drat-trim lrat-check `2e3b2dc` with `lrat-check-E2.patch`. Sanity check: the unjustified-empty-clause
  LRAT is rejected by both checkers, and a valid one is accepted by both.
- Base CNF: `gen_case.py 11 7 none`, `p cnf 168399 4154921`, sha256
  `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: the SHARD-mode expression of `close_tree.py`, i ≡ 13 (mod 24), gives **68 roots** (`roots.tsv`). The 1,630-name
  list hash is `5412782c…` and is identical, in the same order, to `manifest_depth2.tsv`.
- Driver: `run.sh` runs the roots one at a time, in order, with
  `close_tree.py base.cnf out.jsonl ROOT --jobs J --caps 300,300,600 --cadopts=--sat --split-singles --hours H`.
  All records are in one file, `out.jsonl`. It was stopped by kill at 12:26 UTC (time budget).
- Helper copies: `run.sh`, `commit.sh`, `summ.py` (the tables below), `recheck.py` (re-runs one node alone).

## Results
- **No SAT.** Every record is UNSAT or UNKNOWN, and no model was produced.
- **No real proof rejection.** One `PROOF NOT ACCEPTED`, on node `0s0-1s0_6_2` at 08:58. The cause was memory: lrat-check
  said `c VERIFIED`, cake_lpr printed nothing, and dmesg shows the cgroup OOM-killer killing cake_lpr. With 4 jobs, 4 cake_lpr
  processes at about 4.2 GB RSS each exceed the memory limit. Re-run alone (`recheck.jsonl`), the same 156,939,954-byte
  proof was accepted by both checkers (`s VERIFIED UNSAT`). That record was added to `out.jsonl`. The rest of the run used
  `--jobs 3`, with no further OOM kills.
- Roots started: 12 of 68. **Fully closed: 11.** Open: 1 (`0s0-1s1_6s1-9s0`, interrupted at the deadline). Not started: 56.
- 1,020 solve records: 1,018 UNSAT, all certified; 2 UNKNOWN (two depth-2 roots hit the 300 s cap and were split).
  1,017 distinct certified nodes. Totals: solve 10,217 s, check 17,099 s. The largest proof was 345 MB.
  Checking costs more than solving here: most nodes are small (3–30 s solves), and each cake_lpr run has a fixed cost of
  about 20 s to load the 4.15 M-clause CNF.
- `compose.py` (`compose.txt`): `certified_nodes 1017, class_covered false, uncovered_frontier_nodes 442`.

### Per root (only the 12 started roots; the other 56 were not started)
| root | status | certified by depth | split by depth | open by depth | solve/check s |
|---|---|---|---|---|---|
| 0s0-1s0_2s0-7s1 | CLOSED | d2:1 | - | - | 38/42 |
| 0s0-1s0_3s0-4s0 | CLOSED | d2:1 | - | - | 4/22 |
| 0s0-1s0_3s1-9s0 | CLOSED | d2:1 | - | - | 14/31 |
| 0s0-1s0_4s1-8s1 | CLOSED | d2:1 | - | - | 13/25 |
| 0s0-1s0_6 | CLOSED | d3:120 | d2:1 (pre-split) | - | 2354/2485 |
| 0s0-1s0_7s1-10s0 | CLOSED | d2:1 | - | - | 79/27 |
| 0s0-1s1_2s0-3s0 | CLOSED | d2:1 | - | - | 26/21 |
| 0s0-1s1_2s1-7s0 | CLOSED | d2:1 | - | - | 248/39 |
| 0s0-1s1_3s1-4s1 | CLOSED | d2:1 | - | - | 37/24 |
| 0s0-1s1_4s1-10s0 | CLOSED | d2:1 | - | - | 72/27 |
| 0s0-1s1_5s1-10s1 | CLOSED | d3:84 d4:462 | d2:1 d3:7 (pre-split) | - | 4683/8770 |
| 0s0-1s1_6s1-9s0 | open | d4:342 | d2:1 d3:7 (pre-split) | d3:84 d4:120 | 2651/5586 |

The time for `0s0-1s0_6` includes both solves of `0s0-1s0_6_2` (the OOM run and the re-check). The open nodes of
`0s0-1s1_6s1-9s0` were never attempted; none timed out. On resume, the driver picks up from `out.jsonl`.

### Per depth, over all roots
| depth | certified | split | open |
|---|---|---|---|
| 2 | 9 | 3 | 0 |
| 3 | 204 | 14 | 84 |
| 4 | 804 | 0 | 120 |

(Of the 17 splits, 15 were `--split-singles` pre-splits and 2 followed a 300 s timeout. 56 roots, all at depth 2, were not started.)

## Incidents
1. The OOM at `--jobs 4` (above). The 4-job driver also kept running its already-queued futures after it returned, without
   recording them. It was killed, and none of that work is counted.
2. **Lost records, re-done.** The first commit made after the restart (09:11) used `git pull --rebase --autostash` in the
   primary checkout. That rewrote `out.jsonl` while the driver had it open, so its appends from 09:11 to 09:38 (root
   `0s0-1s0_6`, 119 certified children) went to an unlinked inode. Their summary lines are still in `driver.log`. At 09:42
   the driver was killed and `0s0-1s0_6` was re-run in full (09:43–10:09). All records now in `out.jsonl` come from that
   re-run. From then on, every commit was made from a separate clone (`/opt/push`, `commit.sh`) that copies this directory
   in, so git never touches the live files.
3. Some pushes hit "cannot lock ref" races with other machines. The retry loop pushed them all to `es7-cloud`.
