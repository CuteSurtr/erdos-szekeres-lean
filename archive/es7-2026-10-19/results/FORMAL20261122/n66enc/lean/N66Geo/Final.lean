import N66Geo.Small

/-!
# N66Geo.Final: the end-to-end statement with the proved fields removed from `Gaps`

`Gaps2` is `Gaps` without L6 (`lexChoice`), L7 (`holes_le`) and 4.11 (`holds_fixed`), which are proved, and with
`eager` split into its five families (`holds_eager_of_parts`). `n66_bound_55_of_gaps2` is therefore
**Lean-checked modulo `CubesUnsat132`, `RowsValid R0` and the eight fields of `Gaps2`.**
-/

namespace N66Geo
open ErdosSzekeres ErdosSzekeres.Omission N66Enc

/-- The facts not yet formalized after L6, L7 and 4.11. -/
structure Gaps2 : Prop where
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
  /-- 4.4: threshold monotonicity. -/
  thresh : ∀ M : Model, M.Holds (threshClauses ())
  /-- 4.5-4.7: transitivity, growth with ceilings, chain starts. -/
  triple : ∀ M : Model, M.Holds (tripleClauses ())
  /-- 4.8: CE/UE links and exclusion. -/
  ceue : ∀ M : Model, M.Holds (ceueClauses ())
  /-- 4.9-4.10: chain steps and signotope packets. -/
  quad : ∀ M : Model, M.Holds quadStream

theorem gaps_of_gaps2 (g : Gaps2) : Gaps where
  capCup55 := g.capCup55
  mirror := g.mirror
  lexChoice := lexChoice
  holes := holes_le
  fixed := holds_fixed
  eager := fun M => holds_eager_of_parts (g.pair M) (g.pos M) (g.thresh M) (g.triple M) (g.ceue M)
  quad := g.quad

/-- **`N66Bound 55`, Lean-checked modulo `CubesUnsat132`, `RowsValid R0` and `Gaps2`.** -/
theorem n66_bound_55_of_gaps2 (h : CubesUnsat132) (hR : RowsValid R0) (g : Gaps2) :
    OmissionZRow.N66Bound 55 :=
  n66_bound_55_of_gaps h hR (gaps_of_gaps2 g)

end N66Geo

#print axioms N66Geo.n66_bound_55_of_gaps2
