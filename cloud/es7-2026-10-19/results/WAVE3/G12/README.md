# WAVE3 / G12: open cubes of U_L16

Task: `results/WAVE3/tasks/G12.json` (commit 9a26cc2): case U_L16 with 64 open cubes, each of 7 literals.
Environment: `env.txt` (4 cores, 15 GB). Tools: `tools.txt` (CaDiCaL c6073042 3.0.1, march_cu CnC 705b60c6
built with `-fcommon`, cake_lpr a36874a8, whose example prints `s VERIFIED UNSAT`).
F was regenerated with sha256 69c1dc8f…ffff932d. The U_L16 case CNF (hullsplit, U = "", L = "16") has sha256
edd50c27…21b31c9a, which matches cases.jsonl.
Driver: `close_march.py` is a byte-identical copy of `results/WAVE2/F2/close_march.py`. What was checked is
in `driver.diff`: per-job mkdtemp, atomic leaves/open writes, the case record in the first line, and leaves
only on `s VERIFIED UNSAT`.
Command: `close_march.py U_L16.cnf U_L16 --name U_L16 --top <64 given cubes> --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours H`.

## Result

| case | cubes given | verified leaves | open | covered | splits | solve time (sum) | check time (sum) |
|---|---|---|---|---|---|---|---|
| U_L16 | 64 | 64 | 0 | yes: the leaves are exactly the 64 given cubes | 0 | 905.7 s (max 45.2 s per cube) | 301.7 s |

- **U_L16 is closed.** Every given cube was solved directly by CaDiCaL within the 300 s cap, and cake_lpr
  printed `s VERIFIED UNSAT` on its LRAT proof. The set of leaves equals the set of given cubes, and every
  line ends with ` 0`. `open.icnf` is empty.
- There were no SAT results, no cake_lpr rejections and no timeouts.
- One problem with the driver: the first run (10:58–11:19 UTC) exited with `open 1`. Cube
  `-45533 -1014 -962 -1896 993 992 -991` got no record in leaves.jsonl, so its worker thread must have
  failed silently (swallowed exceptions, AUDIT NOTE-1). The cause is unknown. Nothing false was claimed,
  because the cube stayed in open.icnf. Re-running the driver resumed with a frontier of 1, and the cube
  closed in 5.5 s solve plus 3.7 s check. leaves.jsonl therefore has two `resume` records.
