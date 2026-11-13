# WAVE2 F1: case U3_L, part 0 of 3

**Result: the share is NOT closed.** 264 cubes are still open. There was no SAT result and no cake_lpr rejection.

## Share
- Source: `U3_L/frontier.icnf`, an exact copy of `results/WAVE2/F2/U3_L/frontier.icnf` (sha256 7675944a…6eb06). It has 4,299 cubes, taken from W25 at commit 4ff95e3.
- My share is positions p with p mod 3 = 0, in reverse order: 1,433 cubes (`U3_L/share.icnf`, identical to `U3_L/top.icnf`).
- Case CNF: `hullsplit.py case F 3 ""`, sha256 7ab00d97…f823, which equals cnf_sha256 in cases.jsonl. F has sha256 69c1dc8f…932d.

## Numbers (run 10:05:50–12:44 UTC, 4 jobs, `--timeout 300 --split-depth 6 --hours 2.6`)
| item | count |
|---|---|
| verified leaves (`leaves.icnf`; each has the cake_lpr line `s VERIFIED UNSAT`) | **1282** |
| share cubes skipped as closed elsewhere (`skip.icnf`, SKIP records) | **139** |
| cubes split (march_cu -d 6, 64 sub-cubes each, 0 refuted) | 4 |
| open (`open.icnf`) | **264**: 8 top-level share cubes never started, plus all 256 sub-cubes of the 4 splits |
| SAT | 0 |
| cake_lpr rejections (UNSAT_UNCHECKED) | 0 |
| TIMEOUT records | 0 |
| total CaDiCaL wall time | 30,018 s |
| total cake_lpr wall time | 5,498 s |
| total march_cu split time | 818 s |

Accounting check: every share cube is in skip, in leaves, in open, or a SPLIT whose children are all leaves or open
(1433 − 139 − 4 + 256 = 1282 + 264). The 1,282 + 264 = 1,546 cubes match that count.
At the end I re-ran mkskip on `open.icnf` against W25 (530 verified), F2 (1,299) and F3 (1,186). None of the 264 open cubes is closed elsewhere.

## Skip mechanism
`mkskip.py` (F1) builds `U3_L/skip.icnf`, and the driver's `--skip` reads it. A cube is skipped if a source records it,
or a subset of it, as UNSAT with cake_lpr `s VERIFIED UNSAT`, or if a source records it as SPLIT and all its children are closed
by the same rule, recursively. The sources are `WAVE1/W25/U3_L/leaves.jsonl` and `WAVE2/{F2,F3,...}/U3_L/leaves.jsonl`.
A source whose case_sha256 differs is refused. Other helpers' SKIP records are never used. The list was refreshed before the start (74)
and at every 30-minute sync (139 from 10:36 on). Skipped cubes are not in `leaves.icnf`; they are closed only by the other helpers' leaves.

## Files
- `env.txt`, `tools.txt` (tool commits; the march_cu flags are the same as F2's), `driver.diff` (the checks I made on F2's driver; the driver is unchanged),
  `close_march.py`, `mkskip.py`
- `U3_L/`: `frontier.icnf` and `frontier.json` (copied from F2), `share.icnf`, `top.icnf`, `skip.icnf`, `leaves.icnf`, `leaves.jsonl`, `open.icnf`

To continue, resume with the same command (the driver rebuilds the frontier from leaves.jsonl), or hand `open.icnf` to another helper.
