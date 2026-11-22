import Combined.Residual

/-!
combined negative control (must be REJECTED): the slice theorems are not interchangeable. The same term as
`Combined.residual_bound_118`, with the budget-34 slice `RS.s34_18` passed where Res118 needs the budget-35 slice
`s35_18`. Lean must reject the argument (type mismatch 34 vs 35), so no olean is written and lean_rc is 1.
-/

example (n66 : OmissionZRow.N66Bound 55)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.Omission.Partition.ResidualBound 118 :=
  RowGeo.residual_bound_118_of_texts n66 hP hQ hU hA RS.s33_18 RS.s34_18 RS.s34_19 RS.s34_18 s35_19 s35_20
