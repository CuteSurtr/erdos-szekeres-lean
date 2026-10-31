# C2P4 M28: results

Task `results/C2P4/TASK.md` (commit a46b478d), V = M28, LIST = C2P4.tsv, j = 28, N = 50, H = 2.5. Lane started 13:03:55Z, END 15:18:55Z (1793459935); the lane stopped at 15:14:45Z (249 s left, no unit could be started).

## Tools and checks

- Built by `C2P/vendor/build_tools.sh` from the vendored sources only, nothing downloaded (manifest: all 196 files match): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one; the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf b0061e90… and base.json 2476faff… both match.
- Cubes: P1..P8 from `C2C34/l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details are in `tools.txt`.

## Units (14)

- Certified UNSAT (lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`): 9
- Timed out (UNKNOWN): 0
- Not reached: 5 (P4_2-6-7 H, P4_5-8-9 H, P4_6-8-14 H, P3_1-4 Q, P3_8-10 Q)
- Errors or certified false: 0

| case | kind | units | certified | UNKNOWN | not reached |
|---|---|---|---|---|---|
| P6 | H | 1 | 1 | 0 | 0 |
| P5 | Q | 1 | 1 | 0 | 0 |
| P5 | H | 4 | 4 | 0 | 0 |
| P4 | Q | 1 | 1 | 0 | 0 |
| P4 | H | 5 | 2 | 0 | 3 |
| P3 | Q | 2 | 0 | 0 | 2 |

### Certified units

| unit | kind | cap s | solve s | RSS MB | proof GB | lrat-check s | cake_lpr s |
|---|---|---|---|---|---|---|---|
| P5_6-7 | Q | 6000 | 718.2 | 4414 | 3.55 | 57.3 | 349.5 |
| P6_7-12-13 | H | 1800 | 131.38 | 3399 | 1.78 | 28.9 | 224.9 |
| P5_1-12-16 | H | 1800 | 326.88 | 4353 | 3.25 | 49.3 | 323.2 |
| P5_2-11-16 | H | 1800 | 497.3 | 4414 | 3.44 | 58.5 | 369.2 |
| P5_6-11-12 | H | 1800 | 32.85 | 2645 | 0.22 | 12.1 | 137.9 |
| P5_8-9-10 | H | 1800 | 104.68 | 2943 | 1.16 | 25.8 | 199.3 |
| P4_2-5 | Q | 3789 | 1832.12 | 4425 | 5.03 | 73.3 | 457.1 |
| P4_1-2-12 | H | 1396 | 392.16 | 4378 | 3.30 | 49.6 | 311.6 |
| P4_1-8-12 | H | 629 | 559.24 | 4368 | 3.53 | 56.5 | 346.8 |

Min / median / max over the certified units:

- solve s: 32.9 / 392.2 / 1832.1
- lrat-check s: 12.1 / 49.6 / 73.3
- cake_lpr s: 137.9 / 323.2 / 457.1
- proof GB: 0.22 / 3.30 / 5.03

The caps of P4_2-5 (3789 s), P4_1-2-12 (1396 s) and P4_1-8-12 (629 s) were shortened by lane.py so that the checks could finish before END. All three still finished UNSAT within the shortened cap.

Largest solver RSS: 4425 MB (P4_2-5).

## SAT, rejections, memory

No SAT. No proof was rejected and there were no errors. There were no memory problems (the solver peak was under 5 GB, with 15 GB on the machine). The lowest free disk while a proof was being written was 23 GB.

Files: env.txt, tools.txt, units.tsv, run.sh, out.jsonl, lane.log.tail.
