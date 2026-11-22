import N66G15.Pos

/-!
# N66G15.Final4: three named hypotheses left

Proved since `Gaps3`: 4.3 `holds_pos` (Pos.lean). **`n66_bound_54_of_gaps4` is Lean-checked modulo
`CubesUnsat105`, `RowsValid R0_15` and the three fields of `Gaps4`.**
-/

namespace N66G15
open ErdosSzekeres ErdosSzekeres.Omission N66E15

structure Gaps4 : Prop where
  /-- G3: a 5-cap and a 5-cup with common endpoints form a convex octagon. -/
  capCup55 : ∀ n (c : Configuration n), ¬ HasConvexNGon 8 (Finset.univ.image c.point) →
    ∀ p u u' q, q < n → SEPath c.cup false p u q 5 → SEPath c.cup true p u' q 5 → False
  /-- G4: the mirror image is in the class and its occupancy is the τ-image. -/
  mirror : ∀ n (c : Configuration n), InClass c → ∃ c' : Configuration n, InClass c' ∧
    ∀ s, n66Occ c'.cup n s ↔ n66Occ c.cup n (tau s)
  /-- 4.1-4.2: empty and domain clauses (state separation, Lemma R). -/
  pair : ∀ M : Model, M.Holds (pairClauses ())

theorem gaps3_of_gaps4 (g : Gaps4) : Gaps3 where
  capCup55 := g.capCup55
  mirror := g.mirror
  pair := g.pair
  pos := holds_pos

/-- **`N66Bound 54`, Lean-checked modulo `CubesUnsat105`, `RowsValid R0_15` and `Gaps4`.** -/
theorem n66_bound_54_of_gaps4 (h : CubesUnsat105) (hR : RowsValid R0_15) (g : Gaps4) :
    OmissionZRow.N66Bound 54 :=
  n66_bound_54_of_gaps3 h hR (gaps3_of_gaps4 g)

end N66G15

#print axioms N66G15.n66_bound_54_of_gaps4
