# WAVE3 / G9

Task: close the open cubes in `results/WAVE3/tasks/G9.json` (commit 9a26cc2): case U8_L, 64 cubes.

| case | cubes given | verified leaves | cubes still open | every given cube covered | closed |
|------|------------:|----------------:|-----------------:|:------------------------:|:------:|
| U8_L | 64 | 64 | 0 | yes | yes |

- U8_L.cnf from `hullsplit.py case F.cnf 8 "" OUT`: sha256 84d46852…9a9882, which matches cases.jsonl.
  F.cnf sha256 69c1dc8f…f932d matches.
- The 64 cubes (7 literals each) were passed as `--top` in file order (`U8_L/top.icnf`).
  Every one was solved directly by CaDiCaL within the 300 s cap. No split was needed.
  `leaves.icnf` is exactly the 64 given cubes, and `open.icnf` is empty.
- Every leaf has cake_lpr output `s VERIFIED UNSAT`. There were no cake_lpr rejections, no heap
  retries, no SAT results and no timeouts.
- Times: CaDiCaL 3285.1 s total (max 292.3 s per cube), cake_lpr 481.0 s total (max 23.4 s),
  LRAT proofs 3.23 GB in total (deleted, not committed). Wall time 11:20–11:46 UTC on 4 cores.
- Driver: `close_march.py` (copy of WAVE2/F2), reviewed in `driver.diff`. Tools are listed in
  `tools.txt` and the environment in `env.txt`.
