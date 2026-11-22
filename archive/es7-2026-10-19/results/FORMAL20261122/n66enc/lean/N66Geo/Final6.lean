import N66Geo.MirrorB

/-!
# N66Geo.Final6: one geometric hypothesis left (G3)

Proved since `Gaps5`: G4 `mirror_holds` (MirrorA/MirrorB: negated colors swap the labels, the states transpose to
τ, and the reflection (x, y) ↦ (x, −y) realizes it inside the class). **`n66_bound_55_of_capCup55` is
Lean-checked modulo `CubesUnsat132`, `RowsValid R0` and `CapCup55`.**
-/

namespace N66Geo
open ErdosSzekeres ErdosSzekeres.Omission N66Enc

/-- **G3** (the one remaining geometric fact): in a configuration with no convex octagon, no 5-cap and 5-cup
(paths of consecutive triples of one color) share both endpoints. -/
def CapCup55 : Prop := ∀ n (c : Configuration n), ¬ HasConvexNGon 8 (Finset.univ.image c.point) →
  ∀ p u u' q, q < n → SEPath c.cup false p u q 5 → SEPath c.cup true p u' q 5 → False

/-- **`N66Bound 55`, Lean-checked modulo `CubesUnsat132`, `RowsValid R0` and `CapCup55`.** -/
theorem n66_bound_55_of_capCup55 (h : CubesUnsat132) (hR : RowsValid R0) (g3 : CapCup55) :
    OmissionZRow.N66Bound 55 :=
  n66_bound_55_of_gaps5 h hR ⟨g3, mirror_holds⟩

end N66Geo

#print axioms N66Geo.n66_bound_55_of_capCup55
