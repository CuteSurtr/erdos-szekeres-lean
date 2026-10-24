# WAVE2 F4: case U4_L, part 0 of 2

**Status: share NOT closed.** 236 cubes are still open (`U4_L/open.icnf`). They are all sub-cubes of
2 of the 621 share cubes. No SAT result. No cake_lpr rejection.

## Run
- Started 10:28 UTC and the driver stopped at 13:04 UTC, on 4 cores (`env.txt`).
- Tools and their commits are in `tools.txt`. F.cnf and the U4_L case CNF sha256 match
  (case sha ab728682…f991).
- Driver: `close_march.py` is F5's driver, unchanged in code. The checks (per-job mkdtemp, atomic
  leaves/open writes, `case`/`case_sha256` in the first leaves.jsonl record, BUG-1) are in
  `driver.diff`.
- Options: `--timeout 300 --split-depth 6 --jobs 4`.
- Manager: `manage.sh` was adapted from F5. It ran `drop.py` before the start and every 30 min
  against `results/WAVE1/W29/U4_L` and `results/WAVE2/*/U4_L`. The log is `U4_L/manager.log`.

## Share
- `U4_L/frontier.icnf` is F5's 1,242-cube frontier, byte-identical to it (sha 01e111eb…).
- `U4_L/share.icnf` = `U4_L/top.icnf` holds the positions p with p mod 2 = 0, in reverse order:
  621 cubes, disjoint from F5's share.
- At 10:30 UTC, 304 share cubes were dropped as already closed by W29 verified leaves
  (`U4_L/dropped.jsonl`). The checks at 11:00, 11:31, 12:01, 12:31, 13:01 and the final one at
  13:05 dropped nothing more.
- `U4_L/queue.icnf` lists the 317 cubes given to the driver (driver top_sha256 ff65d655…).

## Results (`U4_L/leaves.jsonl`, `U4_L/leaves.icnf`, `U4_L/open.icnf`)
| Item | Count |
|---|---|
| Verified leaves (cake_lpr `s VERIFIED UNSAT`) | 1,152 |
| UNSAT_UNCHECKED | 0 |
| SAT | 0 |
| Splits (march_cu -d 6, 64 sub-cubes each, 0 refuted) | 17 |
| Open cubes | 236 |

Accounting over the 621 share cubes:
- 315 are fully covered by F4 leaves;
- 304 were dropped (closed in W29);
- 2 are partly open, with 236 open sub-cubes. Both are deep split trees, whose
  splits are at cube lengths 13, 19 and 25.

| Time | Seconds |
|---|---|
| CaDiCaL wall | 28,574 |
| cake_lpr wall | 4,363 |
| march_cu split wall | 3,681 |
| child CPU total | 143,492 |

All are summed over jobs.

`open.icnf` is the frontier still to close. Its cubes are full cubes over F's variables (share
cube + split literals).
