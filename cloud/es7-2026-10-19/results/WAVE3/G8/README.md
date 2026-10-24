# WAVE3 / G8: open cubes of case U8_L

Task: `results/WAVE3/tasks/G8.json` (commit 9a26cc2), 64 open cubes of case U8_L (all depth 7).
Environment: `env.txt` (4 cores, 15 GB). Tools: `tools.txt` (CaDiCaL 3.0.1 c6073042, march_cu 705b60c6 with
`-fcommon`, cake_lpr a36874a8; bundled example gives `s VERIFIED UNSAT`). F regenerated, sha256 69c1dc8f…ffff932d;
U8_L case CNF rebuilt with hullsplit.py, sha256 84d46852…09a9882 = cases.jsonl.
Driver: `close_march.py` = verbatim copy of `results/WAVE2/F2/close_march.py`; checks recorded in `driver.diff`.
Run: `--name U8_L --top <the 64 cubes in file order> --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.722`,
started 10:58Z, finished 12:13Z (wall about 1 h 15 min).

| case | cubes given | verified leaves | splits | cubes still open | covered |
|---|---|---|---|---|---|
| U8_L | 64 | 503 | 7 | 0 | yes, CLOSED |

- Every leaf is UNSAT with cake_lpr printing exactly `s VERIFIED UNSAT`; no SAT result, no cake_lpr rejection,
  no timeout left unsplit, no UNSAT_UNCHECKED record.
- Times (sum over jobs): CaDiCaL solve 12,730 s, cake_lpr check 2,180 s, march_cu splits 1,571 s; slowest leaf 227.9 s;
  LRAT proofs 13.2 GB total (not committed).
- Cover check: for each of the 64 given cubes G, the leaves that extend G (with G's literals removed) were checked
  with `results/Haudit/scripts/mycover.py` (CaDiCaL + cake_lpr on the CNF of negated cubes; rejects malformed lines):
  64/64 `s COVERED`, and all 503 leaves extend one of the given cubes.

Files in `U8_L/`: `top.icnf` (the 64 given cubes), `leaves.icnf` (503 full cubes over F's variables),
`leaves.jsonl` (first record has case and case_sha256), `open.icnf` (empty).
