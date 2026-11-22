import Combined.N66L15

/-!
combined part 2 negative control (must be REJECTED): the N66 bounds are bound to their exact number. The term of
`Combined.es302_l15` with `N66R15.n66_bound_55` passed where `Combined.es302` (and so `composition_302_n54`) needs
`N66Bound 54`. Lean must reject the argument (type mismatch 55 vs 54), so no olean is written and lean_rc is 1.
-/

example (tree69 : OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 69)
    (cubes : N66R15Enc.CubesUnsat105R) (certs : N66R15Geo.RowCertsUnsat)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 302 8 :=
  Combined.es302 tree69 (N66R15.n66_bound_55 cubes certs) hP hQ hU hA s35_19 s35_20
