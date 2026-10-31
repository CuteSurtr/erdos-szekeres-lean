# W16 (wave 1, mirror sub-case (ii)): U6_L shard 1 of 2 — CLOSED

Entry in `verify/ii_wave1.json`: `{"kind": "shard", "case": "U6_L", "shard": 1, "nshards": 2, "vm": "W16"}`.

## Where it ran
One cloud container (`env.txt`): Linux x86_64, 4 cores, 15 GB RAM. Tools in `/opt/w16/bin`, commits in
`tools.txt` (CaDiCaL c6073042, march_cu at CnC 705b60c6 built with -fcommon, cake_lpr a36874a8;
the cake_lpr example prints `s VERIFIED UNSAT`). Run: 2026-10-20 07:01–09:19 UTC, `--jobs 4`.

## sha256 checks (`checks.md`)
| file | sha256 | |
|---|---|---|
| m33k7int.sub.cnf (regenerated) | 69c1dc8f…ffff932d | match |
| verify/ii_wave1.json | 6df36dab…e901c72e | match |
| U6_L.cnf (`hullsplit.py case BASE 6 ""`) | 8196f2aef46cc55cd21ba4f3d546d838a47b9e3f4e42d7bc5d4487b759871f14 | match |
| top.icnf (`march_cu U6_L.cnf -d 7`) | 6ca82ad4c8db1cc6f3174d10c1ef2f3b726440e90b3ec752fc89ce92e9c5fe63 | 128 cubes, 0 refuted |

U6_L.cnf hash equals the entry and cases.jsonl.
The shard of U6_L running on the other machine must record the same top.icnf sha256.

## Method
`close_march_w16.py` is a copy of `results/Mii-S/scripts/close_march.py` with: `--top` (fixed top-cube
file) and `--shard/--nshards` (0-based line index i, i mod 2 == 1: 64 cubes), resume from
`leaves.jsonl` (SPLIT records store their children), per-record CPU time (wait4), and `leaves.icnf`
restricted to cake_lpr `s VERIFIED UNSAT`. Leaf: `cadical --lrat --binary=false -t 300`, then
cake_lpr on CNF+units and proof (deleted after the check); timeout → `march_cu -d 6` split.

## Result: U6_L shard 1/2 closed
- 972 leaves, all `UNSAT` with cake_lpr `s VERIFIED UNSAT`; 15 splits (5 at depth 7, 6 at 13, 3 at 19, 1 at 25); 0 open (`open.icnf` empty); no SAT, no errors.
- Leaf depths: 7:59, 13:314, 19:381, 23:8, 24:13, 25:133, 31:64.
- Every leaf extends one of the 64 shard-1 top cubes. `covercheck.py U6_L/leaves.icnf + (the 64 shard-0 top cubes)` → `s COVERED 1036` (`U6_L/covercheck.txt`), so the leaves cover exactly this shard's part.
- CPU: 8.28 core-h recorded (CaDiCaL wall 6.54 h, cake_lpr wall 0.99 h, plus march splits); 23.15 GB of LRAT checked in total; max leaf solve 281 s, max check 25 s. The top march_cu run took 182 s.
- `leaves.icnf` sha256 `62c0111cea17c80cf49f2553c9be2102ac6d64dfb62f014fc29fca69eb5bdb80`.

## Incident
The first launch (07:01) wrote `leaves.jsonl` inside the git tree; `git pull --rebase --autostash` replaced
that file, so the process kept writing to an unlinked inode. At 07:12 the 15 records written so far
(14 verified leaves, 1 split) were copied from `/proc/<pid>/fd/3`, the run was killed and restarted
from them with the live output in `/opt/w16/U6_L` (copied into this directory at each commit). Four
cubes in flight at the kill were redone; their ~7.5 CPU-min are not in the totals. No record was lost.
