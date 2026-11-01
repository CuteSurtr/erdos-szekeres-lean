# C2P4 M33: shard 33 of 50 of `lists/C2P4.tsv`

Task: `results/C2P4/TASK.md` at commit a46b478d, with V = M33, LIST = C2P4.tsv, j = 33, N = 50, H = 2.5.
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Lane started 13:04:15Z (epoch 1793451855), END 1793459955 (15:19:15Z); command in `run.sh`.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: all 196 manifest files match; CaDiCaL 3.0.1, cake_lpr and lrat-check (E2 patch) built from the vendored sources only, nothing cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`); cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…b48`, both as expected.
- Cubes P1..P8 from `C2C34/l2cubes.py`: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, 19 units: P5 1 Q + 5 H, P4 1 Q + 5 H, P3 1 Q + 6 H)

| case | kind | units | certified | timed out (UNKNOWN) | not reached | errors |
|---|---|---|---|---|---|---|
| P5 | Q | 1 | 1 (P5_6-14) | 0 | 0 | 0 |
| P5 | H | 5 | 4 (P5_1-2-12, P5_2-6-8, P5_2-13-14, P5_6-12-13) | 0 | 1 (P5_8-10-11) | 0 |
| P4 | Q | 1 | 0 | 0 | 1 | 0 |
| P4 | H | 5 | 0 | 0 | 5 | 0 |
| P3 | Q | 1 | 0 | 0 | 1 | 0 |
| P3 | H | 6 | 0 | 0 | 6 | 0 |
| total | | 19 | 5 | 0 | 14 | 0 |

All 5 records are `UNSATISFIABLE` with `"certified": true` (lrat-check `c VERIFIED`, cake_lpr `s VERIFIED UNSAT` at heap 8000 MB). The lane stopped at 15:11:26Z with 468 s left before END (below the 15-minute start threshold); the first Q unit used 1 h 23 min including checks.

Certified units (min / median / max over all 5; the Q unit is the max in every column):

| | min | median | max |
|---|---|---|---|
| solve s | 228.1 | 276.0 | 4131.6 (P5_6-14, Q) |
| lrat-check s | 52.3 | 53.2 | 136.0 |
| cake_lpr s | 310.9 | 321.0 | 653.8 |
| proof size | 3.02 GB | 3.24 GB | 7.88 GB |

The 4 H units alone: solve 228–335 s, lrat-check 52–54 s, cake_lpr 311–334 s, proofs 3.02–3.28 GB.

Largest solver RSS: 4398 MB (P5_2-6-8). No SAT, no proof rejection, no memory problem, no errors.
