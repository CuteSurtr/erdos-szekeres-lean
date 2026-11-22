import N66Enc.Alloc
import N66Enc.Cover
import N66Enc.Rows

/-!
# N66Enc.Full: the theorem's CNF (Std-only, never evaluated)

`fullCnf R c` is the complete level-14 relaxation for cube `c` and row supports `R` (DESIGN.md §1.2): the eager
stream, mono66's complete F6 + F8 (`quadStream`), the fixed units, the units of `c`, one clause per row of `R`, the
counter and the lex-leader clauses, numbered by `num`. Every certified `trim.cnf` is (by `N66Enc.Print` and the
hash binding) a sub-list of `fullCnf R0 c` for its leaf `c`.
-/

namespace N66Enc

/-- The structured relaxation. -/
noncomputable def fullS (R : List (List (Fin 70))) (c : Cube) : List (List SLit) :=
  eagerStream () ++ quadStream ++ fixedUnits ++ c.map cubeUnit ++ R.map rowClause ++ cardClauses ++ sbClauses

/-- **The level-14 relaxation for cube `c`** (DIMACS numbers of the generator). -/
noncomputable def fullCnf (R : List (List (Fin 70))) (c : Cube) : List (List Int) := (fullS R c).map toDimacs

/-- **The 132 verdicts, as one proposition** (through the printer and the hash binding, DESIGN.md §1.1). -/
def CubesUnsat132 : Prop := ∀ c ∈ leaves132, ¬ EncB.DimacsSatisfiable (fullCnf R0 c)

end N66Enc
