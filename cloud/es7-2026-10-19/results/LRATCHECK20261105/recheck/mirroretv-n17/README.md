# mirroretv-n17: cake_lpr re-check of the 17-point K = 7 instances, N(7,4,7) <= 16 (5 Nov 2026, 13:22 KST)

Record: `cloud/es7-2026-10-19/results/MIRRORETV` (README lines 36 and 124, `sat/README.md`). Claim: no 17 x-sorted
points in general position with no 4-cap and no 7 points in convex position; "certificate accepted by lrat-check only
(four encodings)". The four recorded CNF/LRAT hashes are `ef7d33ce…`/`2b14c13d…` (`sat/enc.py`) and three "not
committed" encodings `8d76eab2…`/`9ea81e17…`, `0ba68e66…`/`e16c2956…`, `28c788f5…`/`9cf38a94…`.

Solver: `cadical --lrat --binary=false -q` (CaDiCaL 2.1.3). Checker: `cake_lpr --CML_HEAP_SIZE=12000`; verdict =
`grep -x 's VERIFIED UNSAT'`. Negative control: `../cake_control/`. Sequential, one core.

| instance | generator (copy here) | CNF header | CNF SHA-256 | recorded | match | CaDiCaL | cake_lpr |
|---|---|---|---|---|---|---|---|
| n17_K7 | `MIRRORETV/sat/enc.py 17 7` (`enc.py.used`, 0aed2c21…, = record) | p cnf 3370 37060 | ef7d33ce…21c1 | full hash | yes | UNSATISFIABLE | s VERIFIED UNSAT |
| encA_n17_K7 | `ES8SYM/mirror/encode.py 17 7 … full` (`encode_mirror46indep.py.used`, a749d3df…, = `ES8SYM/mirror/hashes.txt`) | p cnf 2739 32124 | 8d76eab2…6b16 | 8d76eab2 | yes | UNSATISFIABLE | s VERIFIED UNSAT |
| (third encoding) | not found | – | – | 0ba68e66 | not regenerated | not run | NOT CHECKED |
| (fourth encoding) | not found | – | – | 28c788f5 | not regenerated | not run | NOT CHECKED |

Result: 2 of 4 encodings regenerated with matching hashes, both UNSAT, both cake_lpr VERIFIED. The claim
N(7,4,7) <= 16 at 17 points is therefore cake_lpr-certified through two encodings (`enc.py`, whose soundness argument
is in `MIRRORETV/sat/README.md`, and the mirror46_indep encoder `ES8SYM/mirror/encode.py`).

**Problem: two encodings cannot be regenerated.** The record says they were not committed. `enc.py`'s docstring names
`mirror46_indep/encode.py` and `sat_rmax/enc_rmax.py` as the other encoders. The first is `ES8SYM/mirror/encode.py`
and yields `8d76eab2…` (above). `ES8SYM/mirror/enc_rmax.py` hard-codes K = 8, so it would have to be modified to
produce a K = 7 instance; under the rules it was not modified. `ES7SPLIT/calib/gen_etv.py 17 7 4 7` (a later ETV
encoder, tried as a probe in a scratch directory) gives `2fabc45d…`, not a recorded hash. No file on this machine
contains `0ba68e66` or `28c788f5` outside the MIRRORETV README. Those two instances are reported, not counted.

The new LRAT proofs differ from the recorded ones (CaDiCaL 2.1.3 here, 3.0.1 there), as expected.
`encA_n17_K7.gen.log` is the log of a second, byte-identical regeneration (written to a temporary name, compared with
`cmp`, then deleted). `encA_n17_K7.cnf.vars` is the encoder's variable map.

Files per instance X: X.cnf, X.gen.log, X.lrat, X.solver.out, X.solve.time, X.cake.log, X.cake.time, X.hashes.txt.
