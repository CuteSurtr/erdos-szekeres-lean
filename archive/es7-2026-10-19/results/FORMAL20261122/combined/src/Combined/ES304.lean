import Combined.Residual
import E304Z.Final

/-!
# combined (22 Nov 2026, part 1): ES(8) ≤ 304 with every Lean-checked piece plugged in

`E304Z.Final.forces_304_of_n66_res : N66Bound 55 → ResidualBound 118 → ForcesConvexNGon 304 8` (FV304: the
budget-67 tree is the Lean theorem `E304Z.Final.excludes_67`; closing import audit in fv304-audit) with
`Combined.residual_bound_118`. Same remaining hypotheses as `FV4A.forces_304_of_slices_rows_n66` minus the four
`BlockValid` (now from row-text verdicts) and the slices s33_18, s34_18, s35_18, s34_19 (now Lean theorems).
-/

namespace Combined

/-- **ES(8) ≤ 304**, Lean-checked modulo `N66Bound 55`, the row-text verdicts of the four blocks and the slices
s35_19, s35_20. -/
theorem es304 (n66 : OmissionZRow.N66Bound 55)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 304 8 :=
  E304Z.Final.forces_304_of_n66_res n66 (residual_bound_118 n66 hP hQ hU hA s35_19 s35_20)

end Combined

/-- info: 'Combined.es304' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms Combined.es304

set_option format.width 10000
#eval IO.println "=== CHECK"
#check Combined.es304
#check E304Z.Final.excludes_67
#eval IO.println "=== MODULES"
open Lean in
#eval show CoreM Unit from do
  for m in (← getEnv).header.moduleNames do
    IO.println s!"module {m}"
#eval IO.println "=== END"
