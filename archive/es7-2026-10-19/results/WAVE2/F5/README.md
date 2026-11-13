# WAVE2 F5: case U4_L, part 1 of 2 (odd frontier positions)

**Result: my whole share of U4_L is closed.** None of the 621 share cubes is open. Every cube is covered by
931 leaves that cake_lpr verified (`s VERIFIED UNSAT`) plus 5 cubes that W29 had meanwhile closed. There were no SAT
results, no cake_lpr rejections (UNSAT_UNCHECKED), and no timeouts after the deadline.

The case as a whole (U4_L) is **not** closed yet. Taken together, W29, F4 and F5 still leave 111 cubes of the W29
frontier open as of 11:45 UTC. All 111 lie under the even positions (F4's share), and F4 is still running.

| | |
|---|---|
| case | U4_L, case CNF sha256 ab7286828ae500e47de8236b6c6953c8ac9a3e776d71991cca253246090ff991 (rebuilt and matches) |
| F | sha256 69c1dc8f…ffff932d (rebuilt and matches) |
| frontier | 1242 cubes from W29 at commit bbf84c7 (W29/U4_L last updated in a53374a, 09:27). Same sha256 as F4's frontier.icnf (01e111eb…) |
| share | positions p with p mod 2 = 1, in reverse order: 621 cubes (`share.icnf` = `top.icnf`), disjoint from F4's share |
| verified leaves | 931 (`leaves.icnf`), one for each UNSAT record whose cake_lpr line is exactly `s VERIFIED UNSAT` |
| SPLIT records | 5 (march_cu -d 6). Leaves reach a depth of up to 31 literals |
| dropped | 5 cubes, covered by verified leaves in results/WAVE1/W29/U4_L (`dropped.jsonl`) |
| open | 0 (`open.icnf` is empty) |
| solve / check / split time | 16,092 s CaDiCaL, 3,409 s cake_lpr, 1,018 s march_cu (sums of wall times per job, 4 jobs in parallel) |
| wall time | 09:43 to 11:24 UTC |

The `cpu_s` field in leaves.jsonl comes from the W19 driver's `os.times()` children delta. With 4 threads it also
counts the work of the other jobs, so it overstates the CPU time of each job. Do not use it.

## Cover check of the share (`cover_share.py`, `U4_L/cover_share.txt`)
For each share cube S, CaDiCaL shows that the units of S, together with the negations of every leaf and dropped cube
that is comparable with S, are UNSAT. All 621 checks returned UNSAT, so 0 cubes are uncovered. The script also checks
that leaves.icnf equals the set of verified records in leaves.jsonl, with no duplicates and no malformed lines. The
5 dropped cubes rely on W29's leaves. A full cover check of U4_L must therefore take the union of W29 + F4 + F5.

## Files
- `env.txt`, `tools.txt`: environment, and tool commits and build flags (march_cu built with -fcommon; the cake_lpr example verifies).
- `close_march.py`, `driver.diff`: the W19 driver with only (a) a fresh `tempfile.mkdtemp` dir for each solver, checker and
  march job (and SAT copies named after that dir), (b) leaves.icnf and open.icnf written to a .tmp file and then `os.replace`d,
  (c) `"case"` and `"case_sha256"` in the first leaves.jsonl record. I tested it on U8-16_L (depth 2, timeout 2 s, split depth 1):
  7 verified leaves and 0 open.
- `frontier.py`: frontier = created cubes (top cubes, and parent+sub for each SPLIT) minus verified-closed minus split, in Python
  `sorted()` order. W29/U4_L had no open.icnf at 09:27, so I had nothing to compare it with. By 10:31 W29 had written an open.icnf,
  and it equals the frontier recomputed at that commit (665 = 665, no difference).
- `drop.py`, `manage.sh`: a 30-minute checkpoint that commits, pulls, and drops queue cubes already covered by verified leaves
  of W29 or another WAVE2 helper. At 10:13, 5 cubes were dropped. The driver was stopped, its top.icnf in the work dir was replaced
  by the remaining open cubes (`queue.icnf`, 350), and it resumed from leaves.jsonl. The `top_sha256` in leaves.jsonl refers to the
  original 621-cube share. Cubes that were in flight when the driver stopped were solved again after the restart.
- `U4_L/`: `frontier.icnf`, `share.icnf`, `top.icnf`, `queue.icnf`, `leaves.icnf`, `leaves.jsonl`, `open.icnf` (empty), `dropped.jsonl`,
  `open_before_restart.icnf`, `manager.log`.
