# AUDIT2 A2 (encoding) working notes

Start 00:33 UTC 2026-10-21, budget 1.75 h (report by ~02:08).

- 00:35 Regenerated both CNFs from the Python scripts at branch head (gen_etv.py, mirgen.py last changed at 3a04d94):
  - m33k7int.sub.cnf (F) sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d, `p cnf 47002 515121` -- matches.
  - hm33k7.sub.cnf sha256 bfbc2d6096e4099ba751130d421eca9da18b72559991103cc2d4b4bc0d92757d, `p cnf 47002 535454` -- matches.
- Lean 4.24.0 release zip fetched; `lake build mir_dimacs MirrorEncoding.Sound MirrorEncoding.Audit` in H3 running (Mathlib from source).
- Read Definitions.lean (GeneralPosition, ConvexPosition = ConvexIndependent, HasConvexNGon), orient, reflLine (a + 2((p-a).u)u - (p-a), correct reflection for unit u), MirrorSet, MirSym, AxisInterior, HullForm, Gen.lean, Sound.lean (hull/interior satisfiable, y-flip via compl), Targets.lean (case split on c in convexHull(S.erase c)).
- Grep forbidden tokens (sorry/admit/native_decide/axiom/implemented_by/extern) over ErdosSzekeres/, H/ETVEncoding, H3/MirrorEncoding: none in code (only `unsafe evalTerm` in ErdosSzekeres/Omission/CoupledLrat.lean, a meta helper; to check it is not imported).
- Every recorded F sha256 in Mii-S, WAVE1-4, V3* is 69c1dc8f...; V1-* record bfbc2d60....
