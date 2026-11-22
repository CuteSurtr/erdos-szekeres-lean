import N66R15Geo.Final
import RowGeo.Blocks
import N66Geo.End
import BalancedBudgetsZZsN

/-!
# Co-import check (not part of the chain; compiled without -o)

This dir's end module imported together with res118-rowblocks (`RowGeo.*`, `RowEnc.*`), n66enc (`N66Geo.*`,
`N66Enc.*`) and the 302 composition (`BalancedBudgetsZZsN`, comp-audit's olean): no module or constant clash. The
level-15 bounds fill the `N66Bound` slots of Res118's text theorem (55) and of `composition_302_n54` (54).
-/

open ErdosSzekeres ErdosSzekeres.Omission

#check @N66R15.n66_bound_54
#check @N66R15.n66_bound_55
#check @RowGeo.residual_bound_118_of_texts
#check @N66Geo.n66_bound_55_of_cubes
#check @OmissionBalancedZZsN.composition_302_n54

/-- `ResidualBound 118` from Res118's row-block texts and slices, with `N66Bound 55` from the level-15 verdicts. -/
theorem coimport_res118
    (hc : N66R15Enc.CubesUnsat105R) (hr : N66R15Geo.RowCertsUnsat)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (s33_18 : Res118.ResSliceExcludes [] 33 18)
    (s34_18 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 34 18)
    (s34_19 : Res118.ResSliceExcludes Res118.rowsP 34 19)
    (s35_18 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 35 18)
    (s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    Partition.ResidualBound 118 :=
  RowGeo.residual_bound_118_of_texts (N66R15.n66_bound_55 hc hr) hP hQ hU hA s33_18 s34_18 s34_19 s35_18 s35_19 s35_20

/-- ES(8) ≤ 302 from the budget-69 trees, `ResidualBound 118` and `N66Bound 54` from the level-15 verdicts. -/
theorem coimport_302 (hc : N66R15Enc.CubesUnsat105R) (hr : N66R15Geo.RowCertsUnsat)
    (trees : OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 69) (hR : Partition.ResidualBound 118) :
    ForcesConvexNGon 302 8 :=
  OmissionBalancedZZsN.composition_302_n54 trees (N66R15.n66_bound_54 hc hr) hR

#print axioms coimport_res118
#print axioms coimport_302
