/-!
# Clause-level definitions, free of Mathlib

Kept free of Mathlib so that the `v2l_data` exe builds quickly. `withUnits` is H3's
`Mir.cubeCnf` restated; `V2L.withUnits_eq` proves the two equal by `rfl`.
-/

namespace V2L

/-- The blocking clause of a cube: the disjunction of its negated literals. -/
def negClause (c : List Int) : List Int := c.map fun z => -z

/-- `F` with the literals of `cube` appended as unit clauses (= `Mir.cubeCnf F cube`). -/
def withUnits (F : List (List Int)) (cube : List Int) : List (List Int) :=
  F ++ cube.map fun z => [z]

end V2L
