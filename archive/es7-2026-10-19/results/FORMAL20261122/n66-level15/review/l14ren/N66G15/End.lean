import N66G15.CapCup

/-!
# N66G15.End: the end statement

**`n66_bound_54_of_cubes : CubesUnsat105 → RowsValid R0_15 → OmissionZRow.N66Bound 54`.**

* `CubesUnsat105` (N66E15/Full.lean): for each of the 132 leaf cubes of the level-14 split tree, the Lean-defined
  relaxation `fullCnf R0_15 c` is unsatisfiable. It is discharged outside the kernel by the 132 cake_lpr verdicts on
  the certified `trim.cnf` files: `N66E15.fullUnsat_of_text` (each printed clause is in `fullCnf R0_15 c`, ENCBLEAN's
  proved DIMACS round trip) and the hash binding M9 (132/132), under trust items E1-E6 (DESIGN.md §1.3).
* `RowsValid R0_15` (N66G15/Assembly.lean): every one of the 11,884 used row supports is left partly unoccupied by
  every configuration of the class. Each row is CERTIFIED separately in the N66 record (templates/cores by
  cake_lpr, transport, mirror, cycle orders); it is not formalized here.

Everything else — the clause families, the cube cover, the counter, the lex-leader argument, the mirror, owner
uniqueness, and the geometry (signotope, no 6-cap/6-cup, 5-cap + 5-cup ⇒ convex octagon) — is proved.
-/

namespace N66G15
open N66E15

/-- **`N66Bound 54`, Lean-checked modulo `CubesUnsat105` and `RowsValid R0_15`.** -/
theorem n66_bound_54_of_cubes (h : CubesUnsat105) (hR : RowsValid R0_15) : OmissionZRow.N66Bound 54 :=
  n66_bound_54_of_capCup55 h hR capCup55_holds

end N66G15

/-- info: 'N66G15.n66_bound_54_of_cubes' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms N66G15.n66_bound_54_of_cubes
