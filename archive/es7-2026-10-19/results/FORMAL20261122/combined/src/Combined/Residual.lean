import RowGeo.Blocks
import RS.Final3318
import RS.Final3418
import RS.Final3518
import RS.Final3419

/-!
# combined (22 Nov 2026, part 1): `ResidualBound 118` with every Lean-checked piece plugged in

* the four row blocks from their per-row verdicts on the printed texts (`RowGeo.residual_bound_118_of_texts`,
  res118-rowblocks; it applies `Res118.residual_bound_118_of_slices`);
* the slices s33_18, s34_18, s35_18 and s34_19 as the compact-checker theorems `RS.s33_18`, `RS.s34_18`,
  `RS.s35_18`, `RS.s34_19` (res-slices-fv).

Remaining hypotheses: `N66Bound 55`, the four `RowsTextUnsat` (2,025 cake_lpr verdicts on the bytes `rowprint`
writes, trust items E1-E6), and the slices s35_19 (Lean check running in res-slices-fv) and s35_20.
-/

namespace Combined

/-- **`ResidualBound 118`**, Lean-checked modulo `N66Bound 55`, the row-text verdicts of the four blocks and the
slices s35_19, s35_20. -/
theorem residual_bound_118 (n66 : OmissionZRow.N66Bound 55)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.Omission.Partition.ResidualBound 118 :=
  RowGeo.residual_bound_118_of_texts n66 hP hQ hU hA RS.s33_18 RS.s34_18 RS.s34_19 RS.s35_18 s35_19 s35_20

end Combined

/-- info: 'Combined.residual_bound_118' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms Combined.residual_bound_118

set_option format.width 10000
#eval IO.println "=== CHECK"
#check Combined.residual_bound_118
#eval IO.println "=== MODULES"
open Lean in
#eval show CoreM Unit from do
  for m in (← getEnv).header.moduleNames do
    IO.println s!"module {m}"
#eval IO.println "=== END"
