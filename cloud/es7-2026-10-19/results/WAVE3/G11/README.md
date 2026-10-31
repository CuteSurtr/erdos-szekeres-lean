# WAVE3 G11: open cubes of case U_L15

Branch `es7-cloud`, task file `results/WAVE3/tasks/G11.json` (commit 9a26cc2). Environment in `env.txt`:
4 cores, 15 GB. Tools and their commits are in `tools.txt`: CaDiCaL 3.0.1 c6073042, march_cu CnC 705b60c6
built with `-fcommon`, cake_lpr a36874a8. The bundled example gives `s VERIFIED UNSAT`.

- F was regenerated with gen_etv.py + mirgen.py. Its sha256 is 69c1dc8f…ffff932d, as expected.
- The case CNF `hullsplit.py case F "" "15"` has sha256 226600f0…f2d8bc, which equals cases.jsonl.
- The driver is `close_march.py`, copied unchanged from WAVE2/F2. `driver.diff` records the review:
  - (a) every solve and march job runs in its own `mkdtemp` directory;
  - (b) leaves.icnf and open.icnf are written to a temporary file and renamed into place;
  - (c) the first record of leaves.jsonl holds `case` and `case_sha256`;
  - a leaf counts only on the exact line `s VERIFIED UNSAT`.
- Run: `--name U_L15 --top <the 64 task cubes, in file order> --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.711`.
  `U_L15/top.icnf` is that top file (sha256 13a114d7…24cd).

| case | cubes given | verified leaves | cubes still open | every given cube covered | splits | SAT | cake_lpr rejections |
|---|---|---|---|---|---|---|---|
| U_L15 | 64 | 64 | 0 | yes: CLOSED | 0 | 0 | 0 |

Every one of the 64 given cubes was solved directly by CaDiCaL within the 300 s cap, so nothing had to be split.
Each proof was checked by cake_lpr with `s VERIFIED UNSAT`. leaves.icnf is exactly the given set of 64 cubes,
and every line ends in ` 0`.

Times:
- 10.0 min of wall time (10:58–11:08 UTC);
- solve 1730 s in total (max 119.6 s per cube);
- cake_lpr check 410 s in total.

The `cpu_s` field in leaves.jsonl comes from process-wide `os.times()` of the children. Because 4 jobs ran
at once, it over-counts and is not a per-cube CPU time.

Files in `U_L15/`: `leaves.icnf`, `leaves.jsonl`, `open.icnf` (empty), `top.icnf`, `driver.log`.
