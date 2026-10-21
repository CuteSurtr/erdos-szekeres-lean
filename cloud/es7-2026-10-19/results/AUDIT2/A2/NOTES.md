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
- 00:56 H3 built from source here (Lean 4.24.0, Mathlib v4.24.0 f897ebcf; `Build completed successfully (1561 jobs)`, 21 min, includes MirrorEncoding.Audit's #guard_msgs). `lake exe mir_dimacs interior 33 7` and `hull 33 7` written here: sha256 69c1dc8f... and bfbc2d60..., `cmp`-identical to the Python files (logs/cnf_sha256.txt). Structural scan of both files: every line ends in 0, no inner 0, no empty clause, max var 47002 = header.
- #print axioms (own file Ax.lean, logs/print_axioms_H3.log): mirrorExclusionLine_of_unsat, _of_cubes, hasConvexNGon_of_unsat_hull, interiorTieBreak_holds, hullCnf_satisfiable, interiorCnf_satisfiable: [propext, Classical.choice, Quot.sound]. MirrorExclusionLine and DimacsSat printed: standard.
- Own hull-frame checker hcheck.py: 240 random mirror 33-sets with axis point a hull vertex (115 bottom, y-flipped): all 183,776 orientation-only clauses of hm33k7.sub.cnf hold. Mutant (descending u): exactly the 496 hull units fail on every set.
- V2-L/V1-L build (V2L.FinalTree, V2L.Audit) running.
