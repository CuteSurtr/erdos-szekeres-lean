# AUDIT2 A2 (encoding) working notes

Start 00:33 UTC 2026-10-21, budget 1.75 h (report by ~02:08).

- 00:35 Regenerated both CNFs from the Python scripts at branch head (gen_etv.py, mirgen.py last changed at 3a04d94):
  - m33k7int.sub.cnf (F) sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d, `p cnf 47002 515121` -- matches.
  - hm33k7.sub.cnf sha256 bfbc2d6096e4099ba751130d421eca9da18b72559991103cc2d4b4bc0d92757d, `p cnf 47002 535454` -- matches.
- Lean 4.24.0 release zip fetched; `lake build mir_dimacs MirrorEncoding.Sound MirrorEncoding.Audit` in H3 running (Mathlib from source).
- Read Definitions.lean (GeneralPosition, ConvexPosition = ConvexIndependent, HasConvexNGon), orient, reflLine (a + 2((p-a).u)u - (p-a), correct reflection for unit u), MirrorSet, MirSym, AxisInterior, HullForm, Gen.lean, Sound.lean (hull/interior satisfiable, y-flip via compl), Targets.lean (case split on c in convexHull(S.erase c)).
- Grep forbidden tokens (sorry/admit/native_decide/axiom/implemented_by/extern) over ErdosSzekeres/, H/ETVEncoding, H3/MirrorEncoding: none in code (only `unsafe evalTerm` in ErdosSzekeres/Omission/CoupledLrat.lean, a meta helper; to check it is not imported).
- Every recorded F sha256 in Mii-S, WAVE1-4, V3* is 69c1dc8f...; V1-* record bfbc2d60....
- 01:00 Reproduced case CNF sha256 for U_L2 (1d26b947...) and U3_L (7ab00d97...) = F + case cube units (hullsplit.py case), as recorded in Mii-S/cases.jsonl/probes.jsonl.
- Import closure of V2L (557 local modules across ErdosSzekeres, H, H3, V1-L, V2-L): no sorry/admit/native_decide/axiom/implemented_by/extern/unsafe/opaque in code (CoupledLrat with `unsafe` is not in the closure).
- V2L/V1L state everything over `Mir.interiorCnf 33 7` / `Mir.hullCnf 33 7` directly (rootCnf_eq, upCnf_eq, caseCnf_eq are rfl).
- Own fresh checker `xcheck.py`: 400 random mirror-symmetric integer 33-sets with interior axis point (139 with x-ties, 213 y-flipped): all 163,443 orientation-only clauses of F hold (logs/xcheck.log). Mutant without y-flip: 21/40 sets violate (the unit X(1,2,3)) -> the test discriminates (logs/xcheck_mutants.log).
