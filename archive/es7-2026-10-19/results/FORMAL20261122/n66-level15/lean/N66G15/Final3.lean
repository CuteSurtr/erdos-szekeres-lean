import N66G15.Quad

/-!
# N66G15.Final3: the end-to-end statement with four named hypotheses left

Proved since `Gaps2`: 4.4 `holds_thresh`, 4.8 `holds_ceue` (Families), 4.5-4.7 `holds_triple` (Triple),
4.9-4.10 `holds_quad` (Quad). **`n66_bound_54_of_gaps3` is Lean-checked modulo `CubesUnsat105`, `RowsValid R0_15`
and the four fields of `Gaps3`.**
-/

namespace N66G15
open ErdosSzekeres ErdosSzekeres.Omission N66E15

/-- The facts not yet formalized. -/
structure Gaps3 : Prop where
  /-- G3: a 5-cap and a 5-cup with common endpoints form a convex octagon. -/
  capCup55 : ∀ n (c : Configuration n), ¬ HasConvexNGon 8 (Finset.univ.image c.point) →
    ∀ p u u' q, q < n → SEPath c.cup false p u q 5 → SEPath c.cup true p u' q 5 → False
  /-- G4: the mirror image is in the class and its occupancy is the τ-image. -/
  mirror : ∀ n (c : Configuration n), InClass c → ∃ c' : Configuration n, InClass c' ∧
    ∀ s, n66Occ c'.cup n s ↔ n66Occ c.cup n (tau s)
  /-- 4.1-4.2: empty and domain clauses (state separation, Lemma R). -/
  pair : ∀ M : Model, M.Holds (pairClauses ())
  /-- 4.3: positive clauses (six-order test, plain domains). -/
  pos : ∀ M : Model, M.Holds (posClauses ())

theorem gaps2_of_gaps3 (g : Gaps3) : Gaps2 where
  capCup55 := g.capCup55
  mirror := g.mirror
  pair := g.pair
  pos := g.pos
  thresh := holds_thresh
  triple := holds_triple
  ceue := holds_ceue
  quad := holds_quad

/-- **`N66Bound 54`, Lean-checked modulo `CubesUnsat105`, `RowsValid R0_15` and `Gaps3`.** -/
theorem n66_bound_54_of_gaps3 (h : CubesUnsat105) (hR : RowsValid R0_15) (g : Gaps3) :
    OmissionZRow.N66Bound 54 :=
  n66_bound_54_of_gaps2 h hR (gaps2_of_gaps3 g)

end N66G15

#print axioms N66G15.n66_bound_54_of_gaps3
