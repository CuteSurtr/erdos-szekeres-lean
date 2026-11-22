import N66Geo.CapCup

/-!
# N66Geo.End: the end statement

**`n66_bound_55_of_cubes : CubesUnsat132 → RowsValid R0 → OmissionZRow.N66Bound 55`.**

* `CubesUnsat132` (N66Enc/Full.lean): for each of the 132 leaf cubes of the level-14 split tree, the Lean-defined
  relaxation `fullCnf R0 c` is unsatisfiable. It is discharged outside the kernel by the 132 cake_lpr verdicts on
  the certified `trim.cnf` files: `N66Enc.fullUnsat_of_text` (each printed clause is in `fullCnf R0 c`, ENCBLEAN's
  proved DIMACS round trip) and the hash binding M9 (132/132), under trust items E1-E6 (DESIGN.md §1.3).
* `RowsValid R0` (N66Geo/Assembly.lean): every one of the 11,884 used row supports is left partly unoccupied by
  every configuration of the class. Each row is CERTIFIED separately in the N66 record (templates/cores by
  cake_lpr, transport, mirror, cycle orders); it is not formalized here.

Everything else — the clause families, the cube cover, the counter, the lex-leader argument, the mirror, owner
uniqueness, and the geometry (signotope, no 6-cap/6-cup, 5-cap + 5-cup ⇒ convex octagon) — is proved.
-/

namespace N66Geo
open N66Enc

/-- **`N66Bound 55`, Lean-checked modulo `CubesUnsat132` and `RowsValid R0`.** -/
theorem n66_bound_55_of_cubes (h : CubesUnsat132) (hR : RowsValid R0) : OmissionZRow.N66Bound 55 :=
  n66_bound_55_of_capCup55 h hR capCup55_holds

end N66Geo

/-- info: 'N66Geo.n66_bound_55_of_cubes' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms N66Geo.n66_bound_55_of_cubes
