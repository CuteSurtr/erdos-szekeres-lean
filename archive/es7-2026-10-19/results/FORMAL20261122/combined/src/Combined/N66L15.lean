import Combined.ES303
import Combined.ES302
import N66R15Geo.Final

/-!
# combined part 2 (22-23 Nov 2026): `ResidualBound 118`, ES(8) ≤ 303 and ES(8) ≤ 302 with N66 from level 15

`N66R15.n66_bound_55` and `N66R15.n66_bound_54` (n66-l15-rows; reviewed in its `review/VERIFY_n66-l15-rows.md`)
fill the `N66Bound` slots of part 1's `Combined.residual_bound_118`, `Combined.es303` and `Combined.es302`.

Remaining hypotheses, and nothing else:
* the cake_lpr verdict props `N66R15Enc.CubesUnsat105R` (105 level-15 cube verdicts), `N66R15Geo.RowCertsUnsat`
  (629 row-certificate verdicts: 628 full CNFs plus the trimmed sub-CNF of template 208) and
  `RowGeo.RowsTextUnsat rowsP/Q/U/A` (2,025 row-text verdicts), all under trust items E1-E6;
* the slices s35_19 and s35_20 (not yet Lean-checked);
* the trees not in Lean: `ExcludesHoleBudgetZZsF 68` (303) and `ExcludesHoleBudgetZZsN 16 69` (302).
-/

namespace Combined

/-- **`ResidualBound 118`**, Lean-checked modulo the N66 level-15 verdicts, the row-text verdicts of the four blocks
and the slices s35_19, s35_20. -/
theorem residual_bound_118_l15 (cubes : N66R15Enc.CubesUnsat105R) (certs : N66R15Geo.RowCertsUnsat)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.Omission.Partition.ResidualBound 118 :=
  residual_bound_118 (N66R15.n66_bound_55 cubes certs) hP hQ hU hA s35_19 s35_20

/-- **ES(8) ≤ 303**, Lean-checked modulo the budget-68 tree statement, the N66 level-15 verdicts, the row-text
verdicts of the four blocks and the slices s35_19, s35_20. -/
theorem es303_l15 (tree68 : OmissionBalancedZZsF.ExcludesHoleBudgetZZsF 68)
    (cubes : N66R15Enc.CubesUnsat105R) (certs : N66R15Geo.RowCertsUnsat)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 303 8 :=
  es303 tree68 (N66R15.n66_bound_55 cubes certs) hP hQ hU hA s35_19 s35_20

/-- **ES(8) ≤ 302**, Lean-checked modulo the budget-69 tree statement (no evidence yet: not a bound claim), the N66
level-15 verdicts (here giving `N66Bound 54`), the row-text verdicts of the four blocks and the slices s35_19,
s35_20. -/
theorem es302_l15 (tree69 : OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 69)
    (cubes : N66R15Enc.CubesUnsat105R) (certs : N66R15Geo.RowCertsUnsat)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 302 8 :=
  es302 tree69 (N66R15.n66_bound_54 cubes certs) hP hQ hU hA s35_19 s35_20

end Combined

/-- info: 'Combined.residual_bound_118_l15' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms Combined.residual_bound_118_l15
/-- info: 'Combined.es303_l15' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms Combined.es303_l15
/-- info: 'Combined.es302_l15' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms Combined.es302_l15

set_option format.width 10000
#eval IO.println "=== CHECK"
#check Combined.residual_bound_118_l15
#check Combined.es303_l15
#check Combined.es302_l15
#print N66R15Enc.CubesUnsat105R
#print N66R15Geo.RowCertsUnsat
#check @N66R15.n66_bound_54
#check @N66R15.n66_bound_55

-- Mechanical statement check (fails the compile otherwise): hypothesis count, and no binder mentions `N66Bound`.
open Lean Meta in
#eval show MetaM Unit from do
  for (n, k) in [(``Combined.residual_bound_118_l15, 8), (``Combined.es303_l15, 9), (``Combined.es302_l15, 9)] do
    let ci ← getConstInfo n
    forallTelescope ci.type fun xs body => do
      unless xs.size == k do throwError "{n}: {xs.size} hypotheses, expected {k}"
      for x in xs do
        if (← inferType x).getUsedConstants.contains ``OmissionZRow.N66Bound then
          throwError "{n}: a hypothesis mentions OmissionZRow.N66Bound"
      IO.println s!"STMT {n}: {xs.size} hypotheses, none mentions N66Bound; conclusion {← ppExpr body}"

#eval IO.println "=== MODULES"
open Lean in
#eval show CoreM Unit from do
  for m in (← getEnv).header.moduleNames do
    IO.println s!"module {m}"
#eval IO.println "=== END"
