# C2P5 M62: LIST = C2P5B.tsv, j = 12, N = 50, H = 5.25 (task commit 81cb025f)

**Outcome: all 19 units were certified UNSAT.** There was no SAT, no timeout, no unit left unreached, no error, no proof rejection and no memory problem.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, E2 patch) from the vendored `tools-src.tar.xz`. The manifest check reported all 196 files matching. No code was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF from `SYMZ/zcnf.py rot 17 7 --m 2 --hull`: header `p cnf 838032 16653336`. Both sha256 values match the expected ones: base.cnf `b0061e90…d8ff1`, base.json `2476faff…2b48`.
- Cubes: `C2C34/l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Run
- One lane, started 15:26:35Z. END is 1793478268 (20:24:28Z); the command is in `run.sh`.
- The lane finished every unit at 19:43:41Z.
- The cap of P3_5-8 was lowered by lane.py to 6291 s because of END, and P3_6-8-13 to 2260 s. Both finished well under their caps.

## Units
| unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB | certified |
|---|---|---|---|---|---|---|---|---|---|---|
| P2_3-9 | P2 | Q | 8000 | UNSATISFIABLE | 1235.9 | 79.1 | 433.2 | 4.35 | 4419.34 | True |
| P1_2-9 | P1 | Q | 8000 | UNSATISFIABLE | 1298.58 | 72.2 | 441.8 | 4.35 | 4386.89 | True |
| P2_1-3-4 | P2 | H | 2400 | UNSATISFIABLE | 283.3 | 56.5 | 339.4 | 3.28 | 4412.81 | True |
| P2_1-6-12 | P2 | H | 2400 | UNSATISFIABLE | 591.39 | 66.3 | 378.0 | 3.68 | 4366.14 | True |
| P2_3-6-11 | P2 | H | 2400 | UNSATISFIABLE | 250.22 | 55.0 | 344.5 | 3.18 | 4398.86 | True |
| P2_3-11-15 | P2 | H | 2400 | UNSATISFIABLE | 513.5 | 63.8 | 362.1 | 3.53 | 4402.72 | True |
| P2_4-8-13 | P2 | H | 2400 | UNSATISFIABLE | 313.98 | 59.7 | 357.9 | 3.25 | 4361.93 | True |
| P2_5-8-13 | P2 | H | 2400 | UNSATISFIABLE | 263.16 | 57.0 | 335.6 | 3.16 | 4391.38 | True |
| P1_2-3-13 | P1 | H | 2400 | UNSATISFIABLE | 344.72 | 59.8 | 338.5 | 3.40 | 4420.67 | True |
| P1_2-8-13 | P1 | H | 2400 | UNSATISFIABLE | 573.35 | 65.2 | 370.8 | 3.64 | 4373.96 | True |
| P1_3-6-10 | P1 | H | 2400 | UNSATISFIABLE | 81.64 | 25.8 | 173.0 | 1.12 | 3127.52 | True |
| P1_4-6-11 | P1 | H | 2400 | UNSATISFIABLE | 121.82 | 39.8 | 212.0 | 1.63 | 3344.31 | True |
| P1_5-10-11 | P1 | H | 2400 | UNSATISFIABLE | 21.92 | 13.9 | 118.9 | 0.22 | 2664.02 | True |
| P3_5-8 | P3 | Q | 6291 | UNSATISFIABLE | 596.77 | 62.2 | 341.8 | 3.59 | 4388.56 | True |
| P3_1-5-9 | P3 | H | 2400 | UNSATISFIABLE | 420.68 | 61.9 | 354.0 | 3.42 | 4405.79 | True |
| P3_1-10-13 | P3 | H | 2400 | UNSATISFIABLE | 312.11 | 60.9 | 342.7 | 3.34 | 4424.02 | True |
| P3_4-7-12 | P3 | H | 2400 | UNSATISFIABLE | 268.83 | 57.1 | 326.8 | 3.21 | 4363.3 | True |
| P3_5-6-15 | P3 | H | 2400 | UNSATISFIABLE | 357.63 | 63.2 | 341.5 | 3.33 | 4352.4 | True |
| P3_6-8-13 | P3 | H | 2260 | UNSATISFIABLE | 137.96 | 38.2 | 232.0 | 1.85 | 3467.13 | True |

**Counts by case and kind** (certified / UNKNOWN / not reached / error):

- P2 Q: 1 units: 1 certified, 0 UNKNOWN, 0 not reached, 0 errors
- P2 H: 6 units: 6 certified, 0 UNKNOWN, 0 not reached, 0 errors
- P1 Q: 1 units: 1 certified, 0 UNKNOWN, 0 not reached, 0 errors
- P1 H: 5 units: 5 certified, 0 UNKNOWN, 0 not reached, 0 errors
- P3 Q: 1 units: 1 certified, 0 UNKNOWN, 0 not reached, 0 errors
- P3 H: 5 units: 5 certified, 0 UNKNOWN, 0 not reached, 0 errors

**Totals:** 19 units, 19 certified, 0 UNKNOWN, 0 not reached, 0 errors.

Certified units, min / median / max:

- solve s: 21.9 / 314.0 / 1298.6
- lrat-check s: 13.9 / 59.8 / 79.1
- cake_lpr s: 118.9 / 341.8 / 441.8
- proof GB: 0.2 / 3.3 / 4.4

Largest solver RSS: 4424.02 MB (P3_1-10-13).
Checker results: all 19 proofs `c VERIFIED` (lrat-check) and `s VERIFIED UNSAT` (cake_lpr), cake heap {8000} MB.

No SAT_FOUND appeared. No record has `certified: false` or an ERROR status. The machine has 15 GB and no swap, and the largest solver RSS was about 4.4 GB.
