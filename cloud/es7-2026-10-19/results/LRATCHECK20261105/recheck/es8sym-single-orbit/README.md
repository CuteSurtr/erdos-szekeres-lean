# es8sym-single-orbit: cake_lpr re-check of the single-orbit cluster bounds (5 Nov 2026, 13:21 KST)

Record: `cloud/es7-2026-10-19/results/ES8SYM/sets3/single_orbit_bounds/` (`single_orbit_sat.log` lines 4 and 8,
`c6c5_notes.md` claims C3 and C4). Claims: the one-orbit tiny-cluster relaxation is UNSAT for m = 6, K = 8, n = 10
(cluster size <= 9, so <= 54 points) and for m = 5, K = 8, n = 11. The record's proofs were accepted by lrat-check only.

Generator: `clsat_full.py` (copied here as `clsat_full.py.used`, SHA-256 8c3331e0...; the record lists no hash for it),
called as `python3 -I clsat_full.py.used m 8 n X.cnf` (no fix file). The generator output lines (vars, clauses,
composition clauses) equal the log's lines 3 and 7.
Solver: `cadical --lrat --binary=false -q` (CaDiCaL 2.1.3). Checker: `cake_lpr --CML_HEAP_SIZE=12000`; verdict =
`grep -x 's VERIFIED UNSAT'`. Negative control: `../cake_control/`. Sequential, one core.

| instance | CNF header | CNF SHA-256 (recorded prefix) | match | CaDiCaL | cake_lpr |
|---|---|---|---|---|---|
| m6K8n10 | p cnf 2570 23611 | 4ef7a9a108f0b14f | yes | UNSATISFIABLE | s VERIFIED UNSAT |
| m5K8n11 | p cnf 2983 20247 | f723a3c5cc0a2753 | yes | UNSATISFIABLE | s VERIFIED UNSAT |

2/2 hash matches, 2/2 UNSAT, 2/2 cake_lpr VERIFIED. The new LRAT proofs (92,486 and 88,437 bytes) differ from the
record's (95,148 and 88,751 bytes; CaDiCaL version differs), as expected. Not re-checked: the SAT sides (n = 9 for
m = 6, n = 10 for m = 5) and the faithfulness tests, which were not part of this task.

Files per instance X: X.cnf, X.gen.log, X.lrat, X.solver.out, X.solve.time, X.cake.log, X.cake.time, X.hashes.txt.
