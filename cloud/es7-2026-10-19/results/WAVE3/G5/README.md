# WAVE3 / G5: open cubes of U15_L

Branch `es7-cloud`, task file `results/WAVE3/tasks/G5.json` (commit 9a26cc2). Environment in `env.txt`
(4 cores, 15 GB). Tools in `tools.txt`: CaDiCaL 3.0.1 (c6073042), march_cu (CnC 705b60c6, `-fcommon`),
cake_lpr (a36874a8; bundled example prints `s VERIFIED UNSAT`).

F regenerated with gen_etv.py + mirgen.py: sha256 69c1dc8f…ffff932d (matches). Case CNF of U15_L from
hullsplit.py (U = 15, L empty): sha256 3f479f9f…a5adc8e (matches cases.jsonl).

Driver: `close_march.py` is `results/WAVE2/F2/close_march.py` unchanged. `driver.diff` records the checks
(fresh mkdtemp directory per job, atomic leaves/open writes, case + case_sha256 in the first record,
leaf counted only on `s VERIFIED UNSAT`). Run as
`close_march.py U15_L.cnf U15_L --name U15_L --top <64 given cubes> --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.725`,
10:58–11:27 UTC.

## Results

| case | cubes given | verified leaves | splits | cubes still open | every given cube covered |
|---|---|---|---|---|---|
| U15_L | 64 | 177 | 2 (63 + 52 sub-cubes; 62 + 63 + 52 = 177) | 0 | yes |

- **U15_L: closed.** The 64 given cubes are 64 of the 128 top cubes of `results/WAVE1/W29/U15_L/top.icnf`
  (copied as `U15_L/top.icnf`, in the task file's order). 62 closed directly; 2 hit the 300 s cap and were
  split by march_cu -d 6; all their sub-cubes closed.
- Solve time 3999 s (CaDiCaL, summed over jobs), check time 763 s (cake_lpr), split time 632 s (march_cu);
  wall time about 29 minutes on 4 cores.
- No SAT result. No cake_lpr rejection: every one of the 177 UNSAT answers printed `s VERIFIED UNSAT`.
- Cover: `cover_g5.py` (own checker, rejects lines not ending in ` 0`) confirms that the 177 leaves in
  `U15_L/leaves.icnf` cover all 64 given cubes (`s COVERED`); each leaf has a VERIFIED record in
  `leaves.jsonl`. `U15_L/open.icnf` is empty.
