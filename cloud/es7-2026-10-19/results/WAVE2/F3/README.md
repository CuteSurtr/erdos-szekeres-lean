# WAVE2 F3: case U3_L, part 2 of 3 (frontier positions p mod 3 = 2, reversed)

**Status: share not closed.** 1428 of the 1433 share cubes are closed (1289 by my verified leaves,
139 skipped as closed elsewhere). 4 cubes were split but are only partly closed, and 1 was never
started. `U3_L/open.icnf` lists 713 open cubes.

- No SAT result. No cake_lpr rejection: all 1337 UNSAT answers printed `s VERIFIED UNSAT`, and
  there are no UNSAT_UNCHECKED records.
- Run: 10:26:46 to 13:04:23 UTC, 4 jobs, timeout 300 s, split depth 6, `--hours 2.637`. The driver
  stopped at its deadline with `open 713`.

## Numbers
| | |
|---|---|
| share (top.icnf = share.icnf) | 1433 cubes (frontier.icnf positions p%3==2, last first) |
| verified leaves (`U3_L/leaves.icnf`) | 1337 |
| skipped, closed elsewhere (`U3_L/skip.icnf`, SKIP records) | 139 |
| splits (march_cu -d 6, 64 subs each, 0 refuted) | 12 (4 top cubes, 8 of their depth-19 children) |
| open (`U3_L/open.icnf`) | 713 (1 cube of length 13, 200 of length 19, 512 of length 25) |
| top cubes: fully closed / skipped / partly done / untouched | 1289 / 139 / 4 / 1 |
| solve time (CaDiCaL wall, summed) | 29,287 s |
| check time (cake_lpr wall, summed) | 5,494 s |
| split time (march_cu, summed) | 2,874 s |

The 4 partly done top cubes are hard. Each of them timed out at 300 s, and so did 8 of their
children, which forced a second split. Their remaining sub-cubes are all in `open.icnf`.

## Method
- Tools (`tools.txt`): CaDiCaL 3.0.1 c6073042, march_cu CnC 705b60c6 (-fcommon), cake_lpr a36874a8.
  The bundled cake_lpr example prints `s VERIFIED UNSAT`. F sha256 69c1dc8f...932d and
  U3_L.cnf sha256 7ab00d97...f823 both match.
- `frontier.icnf` is copied from WAVE2/F2 (file sha256 7675944a...6eb06, 4299 cubes).
  `frontier_F2.json` is F2's metadata. My share was checked as disjoint from F2's: the p%3==1
  reversed list equals F2's share.icnf.
- Driver `close_march.py` is a byte-for-byte copy of F2's. See `driver.diff` for checks (a) to (e).
- Skip list: `mkskip.sh`, which runs F1's `mkskip.py` over WAVE1/W25/U3_L and the other WAVE2
  U3_L leaves.jsonl files. It was refreshed at start and about every 30 min. A cube is skipped
  only if a verified leaf with the same case_sha256 is a subset of it, or if it was split and
  every child is closed. Skipped cubes do not appear in my leaves.icnf: their cover comes from
  the other sources.
- `leaves.jsonl` starts with {"case": "U3_L", "case_sha256": ...}. Each UNSAT leaf record carries
  its cake_lpr line. Each SPLIT record carries its subs.
