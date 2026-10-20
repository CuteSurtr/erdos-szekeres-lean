# WAVE3 G4: open cubes of U15_L

Branch `es7-cloud`, paths under `cloud/es7-2026-10-19/`. One 4-core VM (`env.txt`). Tools in
`tools.txt`: CaDiCaL 3.0.1 (c6073042), march_cu (CnC 705b60c6, `-fcommon`), cake_lpr (a36874a8,
bundled example gives `s VERIFIED UNSAT`). F was regenerated with sha256 69c1dc8f…ffff932d.

Driver: `close_march.py` is a byte copy of `results/WAVE2/F2/close_march.py`. What I checked
against W19 (fresh `mkdtemp` per job, atomic `leaves.icnf`/`open.icnf`, `case`/`case_sha256` in
the first record, leaf only on `s VERIFIED UNSAT`) is in `driver.diff`. `--skip` was not used.

## Result

| case | cubes given | verified leaves | cubes still open | every given cube covered |
|---|---|---|---|---|
| U15_L | 64 | 127 | 0 | yes: **closed** |

- U15_L case CNF sha256 3f479f9f…dc8e, equal to cases.jsonl. The 64 cubes from
  `results/WAVE3/tasks/G4.json` (at 9a26cc2) went in as `--top`, in file order (`top.icnf`,
  sha256 64ac1b17…2dbe).
- 63 of the 64 cubes were UNSAT within 300 s. One cube,
  `-9842 -32 987 -1651 -1600 -1618 -552`, timed out. march_cu split it at depth 6 into 64
  sub-cubes (0 refuted), and all 64 were UNSAT within 300 s.
- Each of the 127 leaves has the cake_lpr line `s VERIFIED UNSAT`. There was no SAT result,
  no cake_lpr rejection, and no heap retry.
- Times: CaDiCaL wall 3673 s in total, cake_lpr 652 s, march split 75 s, child CPU 16727 s.
  The driver ran from 10:58:44 to 11:19 UTC, about 21 min of wall time on 4 jobs. The largest
  LRAT proof was 292 MB (not committed).
- Cover check (`cover_given.py`, my own script): it parses `leaves.icnf` strictly (every line
  must be `a … 0`) and requires each leaf to have a verified record in `leaves.jsonl`. For each
  given cube C, it takes the leaves consistent with C, drops C's literals, and has CaDiCaL show
  that the negations of these residual cubes are UNSAT. Output: `U15_L given 64 covered 64
  leaves 127`. As a mutation test, deleting one leaf gives `covered 63`.
