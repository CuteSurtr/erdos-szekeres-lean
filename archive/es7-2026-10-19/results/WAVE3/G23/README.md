# WAVE3 G23: open cubes of U7_L

Task `results/WAVE3/tasks/G23.json` (commit 40e11ae): U7_L, 143 open cubes (128 of length 19, 3 of 24, 12 of 25),
the frontier left by WAVE1 W26.

## Result

| case | cubes given | verified leaves | splits | open | every given cube covered | closed |
|---|---|---|---|---|---|---|
| U7_L | 143 | 206 | 1 | 0 | yes (0 of 143 uncovered) | yes |

- No SAT result. No cake_lpr rejection: all 206 leaves printed `s VERIFIED UNSAT`, with no heap retries.
- 142 given cubes were closed directly. One length-25 cube hit the 300 s cap and was split by march_cu
  (split depth 6) into 64 sub-cubes (0 refuted), all of which were closed.
- Time: driver ran 11:21:28 to 11:47:09 UTC (26 min wall, 4 jobs). Summed per-job wall: solve 3012 s,
  cake_lpr check 924 s, march split 339 s. Longest successful solve 133.8 s. (The `cpu_s` field in leaves.jsonl
  uses process-wide `os.times()` children and so also counts concurrent jobs; it overstates per-cube CPU.)
- Cover: for every given cube T, `leaves.icnf` restricted to T covers T (covercheck.py algorithm, strict
  ` 0\n` line parsing). W26's `U7_L/leaves.icnf` (665) + this `leaves.icnf` (206) cover the whole case U7_L
  (`s COVERED`, 871 cubes).

## Files (`U7_L/`)
- `top.icnf`: the 143 given cubes in task-file order (sha256 b27f5c30325a69cdd53f4caa11516b1d314afdeca50d63a53dcc50b8300d3401).
- `leaves.icnf`: 206 verified leaves, full cubes over F's variables (sha256 cc957d7a326176285b281c09d736ef5576e11cf219d051633988acb33a7a2c70).
- `leaves.jsonl`: first record `{"case": "U7_L", "case_sha256": "d320d668…11d3cb"}`; one record per solved or split cube.
- `open.icnf`: empty.

## Method
- Environment `env.txt`, tools `tools.txt` (CaDiCaL 3.0.1 c6073042, march_cu CnC 705b60c6 with -fcommon,
  cake_lpr a36874a8; bundled example `s VERIFIED UNSAT`).
- F regenerated with gen_etv.py + mirgen.py, sha256 69c1dc8f…ff932d (matches). Case CNF
  `hullsplit.py case F.cnf 7 "" U7_L.cnf`, sha256 d320d668e526b71e8362bbd87462b8ec7b40f677d09359ed515b4dd97f11d3cb (matches cases.jsonl).
- Driver `close_march.py` = byte copy of WAVE2/F2/close_march.py; checks in `driver.diff`.
  Run: `close_march.py U7_L.cnf OUT --top U7_L.top.icnf --name U7_L --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.7`,
  OUT outside the git checkout, copied into `U7_L/` for each commit.
