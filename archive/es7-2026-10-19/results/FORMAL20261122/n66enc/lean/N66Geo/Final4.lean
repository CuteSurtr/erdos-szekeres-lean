import N66Geo.Pos

/-!
# N66Geo.Final4: three named hypotheses left

Proved since `Gaps3`: 4.3 `holds_pos` (Pos.lean). **`n66_bound_55_of_gaps4` is Lean-checked modulo
`CubesUnsat132`, `RowsValid R0` and the three fields of `Gaps4`.**
-/

namespace N66Geo
open ErdosSzekeres ErdosSzekeres.Omission N66Enc

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

/-- **`N66Bound 55`, Lean-checked modulo `CubesUnsat132`, `RowsValid R0` and `Gaps4`.** -/
theorem n66_bound_55_of_gaps4 (h : CubesUnsat132) (hR : RowsValid R0) (g : Gaps4) :
    OmissionZRow.N66Bound 55 :=
  n66_bound_55_of_gaps3 h hR (gaps3_of_gaps4 g)

end N66Geo

#print axioms N66Geo.n66_bound_55_of_gaps4
