# C2P3 M04 (LIST = C2P3.tsv, j = 4, N = 50, H = 2.5, Z = 4f653319)

## Tools and checks
- `C2P/vendor/build_tools.sh` built CaDiCaL 3.0.1, cake_lpr and lrat-check (with the E2 patch) from the vendored sources. The manifest check passed for all 196 files.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one, and the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: the header was `p cnf 838032 16653336`, and the sha256 of base.cnf and of base.json both matched the expected values.
- The cubes from `l2cubes.py` for P1..P8 are byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details are in `tools.txt`.

## Run
- One lane (`run.sh`), started 09:44:33Z.
- END was 1793447872 (11:57:52Z). The lane stopped at 11:51:08Z with 403 s left.
- It had already started every unit in the list.

## Units: 10 in the list, 8 certified, 0 timed out, 2 not reached, 0 errors

| case | kind | certified | not reached |
|---|---|---|---|
| P7 | Q | 1 (P7_2-13) | 0 |
| P7 | H | 1 (P7_3-11-13) | 0 |
| P6 | H | 2 (P6_2-12-15, P6_7-11-15) | 0 |
| P5 | H | 4 (P5_1-3-6, P5_1-9-11, P5_2-6-15, P5_2-13-16) | 2 (P5_6-12-15, P5_8-10-13) |

Every certified unit was UNSAT, and both lrat-check and cake_lpr accepted its proof.
- P5_2-6-15 ran with its cap cut to 1253 s and P5_2-13-16 with its cap cut to 400 s, to fit the time left before END. Both finished inside those caps.

### Per unit (seconds and bytes)

| unit | solve | lrat-check | cake_lpr | proof bytes | RSS MB |
|---|---|---|---|---|---|
| P7_2-13 (Q) | 2440.18 | 93.5 | 514.2 | 6156621636 | 4409.61 |
| P7_3-11-13 | 303.79 | 53.0 | 298.8 | 3300435638 | 4397.18 |
| P6_2-12-15 | 276.83 | 49.3 | 294.0 | 3327293179 | 4350.78 |
| P6_7-11-15 | 240.51 | 48.6 | 288.5 | 3177269990 | 4361.54 |
| P5_1-3-6 | 203.30 | 48.7 | 279.6 | 3204454952 | 4367.27 |
| P5_1-9-11 | 276.95 | 49.8 | 289.7 | 3301659244 | 4354.10 |
| P5_2-6-15 | 439.09 | 59.6 | 340.6 | 3620057646 | 4375.45 |
| P5_2-13-16 | 239.52 | 50.4 | 296.8 | 3254834129 | 4375.36 |

Min / median / max over the 8 certified units:
- solve: 203.3 / 276.9 / 2440.2 s
- lrat-check: 48.6 / 50.1 / 93.5 s
- cake_lpr: 279.6 / 295.4 / 514.2 s
- proof size: 3.18 / 3.30 / 6.16 GB

Over the 7 H units only:
- solve: 203.3 / 276.8 / 439.1 s
- proof size: 3.18 / 3.30 / 3.62 GB

## Resources and anomalies
- Largest solver RSS: 4409.61 MB (P7_2-13).
- No SAT, no proof rejection, no ERROR status and no memory problem.
