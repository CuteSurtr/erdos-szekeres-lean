# c7upper-calib: cake_lpr re-check of the C7UPPER calibration instances (5 Nov 2026, 13:20 KST)

Record: `cloud/es7-2026-10-19/results/C7UPPER` (README §4 "Calibration", `logs/calib_unsat.log`). Claim: for
(m, K) = (3,4), (4,5), (5,6), (6,7) the C7UPPER encoding is UNSAT one layer past the known maximum. The record's
proofs were accepted by lrat-check only.

Generator: `C7UPPER/gen.py` (copied here as `gen.py.used`, SHA-256 4564e7f0..., equal to `C7UPPER/SHA256SUMS.txt`),
called as `python3 -I gen.py.used m K t X.cnf` (no added unit clauses; the hashes confirm this).
Solver: `cadical --lrat --binary=false -q X.cnf X.lrat` (CaDiCaL 2.1.3, /usr/bin/cadical).
Checker: `cake_lpr --CML_HEAP_SIZE=12000 X.cnf X.lrat > X.cake.log` (~/.local/bin/cake_lpr, SHA-256 c14ff498...);
verdict = `grep -x 's VERIFIED UNSAT' X.cake.log`. Negative control: `../cake_control/` (bogus proof "2 0 0" for a SAT
formula is rejected; no `s VERIFIED UNSAT` line). Run sequentially on one core.

| instance | CNF header | CNF SHA-256 (recorded prefix) | match | CaDiCaL | cake_lpr |
|---|---|---|---|---|---|
| m3K4t2 | p cnf 22 32 | 0b93d14c4ee3d0e0 | yes | UNSATISFIABLE | s VERIFIED UNSAT |
| m4K5t3 | p cnf 300 1172 | 53d649777bb24228 | yes | UNSATISFIABLE | s VERIFIED UNSAT |
| m5K6t4 | p cnf 1507 11550 | 1251ca7696e893ef | yes | UNSATISFIABLE | s VERIFIED UNSAT |
| m6K7t6 | p cnf 10388 154363 | ee15a3f0485b011e | yes | UNSATISFIABLE | s VERIFIED UNSAT |

4/4 hash matches (the log records 16-hex prefixes; full hashes in `results.tsv`), 4/4 UNSAT, 4/4 cake_lpr VERIFIED.
Each run took under 2 s. The LRAT proofs differ from the record's (CaDiCaL 2.1.3 here, 3.0.1 there); that is
expected and irrelevant, since the new proofs are checked. Not re-checked here: the SAT side of the calibration
(`logs/calib_sat.log`), which was not part of this task.

Files per instance X: X.cnf, X.cnf.json (generator metadata), X.gen.log, X.gen.time, X.lrat, X.solver.out,
X.solve.time, X.cake.log, X.cake.time, X.hashes.txt (sha256sum of all of them). `run.log`: the sequential run.
