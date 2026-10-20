import MirrorEncoding.Gen
import V2L.Defs
import V2L.Facts

/-!
# The CNFs of the certificates of the hull-pair split

`F = Mir.interiorCnf 33 7` (`m33k7int.sub.cnf`). These are the Lean terms whose DIMACS text
`lake exe v2l_data` writes; `V2L.Main` states the certificates about the same terms
(`rootCnf_eq`, `upCnf_eq`, `caseCnf_eq`, all `rfl`).
-/

namespace V2L

open Mir

/-- `cover.py cnf F root`: `F` and the 121 blocking clauses `¬UP(U)`. -/
def rootCnf : List (List Int) := interiorCnf 33 7 ++ upCubes.map negClause

/-- `cover.py cnf F up:U`: `F`, the units of `UP(U)`, and the blocking clauses `¬cube(U, L)`
of the cases with upper chain `U`. -/
def upCnf (p : List Nat × List Int) : List (List Int) :=
  withUnits (interiorCnf 33 7) p.2 ++ (casesOf p.1).map negClause

/-- `hullsplit.py case F U L`: `F` and the units of `cube(U, L)`. -/
def caseCnf (c : List Int) : List (List Int) := withUnits (interiorCnf 33 7) c

end V2L
