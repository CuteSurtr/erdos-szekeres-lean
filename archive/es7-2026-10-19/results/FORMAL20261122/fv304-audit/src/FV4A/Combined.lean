/-
fv304-audit (22 Nov 2026): ES(8) ≤ 304 with the budget-67 tree hypothesis discharged in Lean.

`E304Z.Final.excludes_67 : OmissionBalancedZ.ExcludesHoleBudgetZ 67` (FV304, fv304-20261120/olean: the compact-checker
proof of the budget-67 Z-row tree) is fed into `Res118.forces_304_of_slices` (formalize-20261122/res118, rebuilt in
this directory's olean/ from byte-identical sources). Remaining hypotheses: N66 ≤ 55, the validity of the four
unit-row blocks and the six residual slice exclusions. The commands after the theorem print its statement, axioms,
the definitions in its statement and the module list of the environment (= the import closure of this module).
-/
import E304Z.Final
import Res118.Compose304

set_option Elab.async false

namespace FV4A

/-- **ES(8) ≤ 304, Lean-checked modulo** `N66Bound 55`, the validity of the four unit-row blocks (`BlockValid`) and
the six residual slice exclusions (`ResSliceExcludes`). There is no tree hypothesis: the balanced budget-67 tree is
the Lean theorem `E304Z.Final.excludes_67` (FV304). -/
theorem forces_304_of_slices_rows_n66
    (n66 : OmissionZRow.N66Bound 55)
    (vP : Res118.BlockValid Res118.rowsP) (vQ : Res118.BlockValid Res118.rowsQ)
    (vU : Res118.BlockValid Res118.rowsU) (vA : Res118.BlockValid Res118.rowsA)
    (s33_18 : Res118.ResSliceExcludes [] 33 18)
    (s34_18 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 34 18)
    (s34_19 : Res118.ResSliceExcludes Res118.rowsP 34 19)
    (s35_18 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 35 18)
    (s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 304 8 :=
  Res118.forces_304_of_slices E304Z.Final.excludes_67 n66 vP vQ vU vA s33_18 s34_18 s34_19 s35_18 s35_19 s35_20

end FV4A

set_option format.width 10000
#eval IO.println "=== CHECK"
#check FV4A.forces_304_of_slices_rows_n66
#check Res118.forces_304_of_slices
#check Res118.residual_bound_118_of_slices
#check E304Z.Final.excludes_67
#eval IO.println "=== AXIOMS"
#print axioms FV4A.forces_304_of_slices_rows_n66
#print axioms Res118.forces_304_of_slices
#print axioms Res118.residual_bound_118_of_slices
#eval IO.println "=== DEFS"
#print Res118.BlockValid
#print Res118.ValidUnitRow
#print Res118.ResSliceExcludes
#print Res118.lsupp
#print Res118.F
#print Res118.Lo
#print Res118.InLo
#print Res118.loProfile
#eval IO.println "=== MODULES"
open Lean in
#eval show CoreM Unit from do
  for m in (← getEnv).header.moduleNames do
    IO.println s!"module {m}"
#eval IO.println "=== END"
