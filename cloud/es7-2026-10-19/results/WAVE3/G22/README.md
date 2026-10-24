# WAVE3 G22: open cubes of U_L5

Task: `results/WAVE3/tasks/G22.json` (U_L5: 274 open cubes: 192 of length 25, 81 of length 19, 1 of length 13).
Tools and commits: `tools.txt`. The driver is `close_march.py`, a byte-identical copy of
`results/WAVE2/F2/close_march.py`; my review is in `driver.diff`.
F.cnf sha256 69c1dc8f…932d and the U_L5 case CNF sha256 84bf54f2…6ff6e (equal to cases.jsonl) were checked.

Run: `close_march.py U_L5.cnf U_L5 --top <the 274 cubes in file order> --name U_L5 --depth 7
--timeout 300 --split-depth 6 --jobs 4 --hours 2.722`, on 4 cores, 10:58 to 13:21 UTC 2026-10-20.

| case | cubes given | verified leaves | open cubes | every given cube covered |
|------|-------------|-----------------|------------|--------------------------|
| U_L5 | 274 | 1142 | 0 | yes |

- **U_L5 is closed.** `open.icnf` is empty. Every leaf in `leaves.icnf` has a `leaves.jsonl` record with
  CaDiCaL exit 20 and cake_lpr output `s VERIFIED UNSAT`.
- Coverage: for each of the 274 given cubes, the leaves restricted to that cube cover it (checked with the
  covercheck.py algorithm per top cube). Every leaf extends exactly one given cube, and no leaf appears twice.
- 14 cubes reached the 300 s cap and were split with march_cu at depth 6 (6 of length 19, 2 of length 25,
  4 of length 31, 2 of length 37). The two length-37 splits gave 57 cubes each (march_cu: "including 5
  refuted"). Those refuted cubes are in the cube file, and the driver solved and verified them like the others.
- No SAT result. No cake_lpr rejection: all 1142 checks printed `s VERIFIED UNSAT`, with no retries.
- Time, summed over jobs: CaDiCaL 24159 s, cake_lpr 4084 s, march_cu splits 4366 s, child CPU 125655 s.
  The slowest leaf solve took 298.1 s; the slowest check took 27.7 s.
