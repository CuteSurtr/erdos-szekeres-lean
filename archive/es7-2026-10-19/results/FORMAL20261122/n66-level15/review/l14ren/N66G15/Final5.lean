import N66G15.Pair

/-!
# N66G15.Final5: two geometric hypotheses left

Proved since `Gaps4`: 4.1-4.2 `holds_pair` (Pair.lean: state separation in the refined domains, Lemma R).
Every clause family of the relaxation is now proved sound for every `Model` (M2 complete). **`n66_bound_54_of_gaps5`
is Lean-checked modulo `CubesUnsat105`, `RowsValid R0_15` and the two geometric fields of `Gaps5`.**
-/

namespace N66G15
open ErdosSzekeres ErdosSzekeres.Omission N66E15

/-- The two geometric facts not yet formalized. -/
structure Gaps5 : Prop where
  /-- G3: a 5-cap and a 5-cup with common endpoints form a convex octagon. -/
  capCup55 : ∀ n (c : Configuration n), ¬ HasConvexNGon 8 (Finset.univ.image c.point) →
    ∀ p u u' q, q < n → SEPath c.cup false p u q 5 → SEPath c.cup true p u' q 5 → False
  /-- G4: the mirror image is in the class and its occupancy is the τ-image. -/
  mirror : ∀ n (c : Configuration n), InClass c → ∃ c' : Configuration n, InClass c' ∧
    ∀ s, n66Occ c'.cup n s ↔ n66Occ c.cup n (tau s)

theorem gaps4_of_gaps5 (g : Gaps5) : Gaps4 where
  capCup55 := g.capCup55
  mirror := g.mirror
  pair := holds_pair

/-- **`N66Bound 54`, Lean-checked modulo `CubesUnsat105`, `RowsValid R0_15` and `Gaps5` (G3, G4).** -/
theorem n66_bound_54_of_gaps5 (h : CubesUnsat105) (hR : RowsValid R0_15) (g : Gaps5) :
    OmissionZRow.N66Bound 54 :=
  n66_bound_54_of_gaps4 h hR (gaps4_of_gaps5 g)

end N66G15

#print axioms N66G15.n66_bound_54_of_gaps5
