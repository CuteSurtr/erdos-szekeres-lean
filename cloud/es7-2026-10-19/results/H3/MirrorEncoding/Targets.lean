import MirrorEncoding.TieBreak
import MirrorEncoding.Cover

/-!
# The mirror exclusion: statement, reduction, and what is left

`MirrorExclusion` says that every mirror-symmetric set of 33 points in general position
(one point on the axis, 16 mirror pairs; `MirrorSet`) contains a convex 7-gon. It follows
from
* UNSAT of `hullCnf 33 7` (`hm33k7.sub.cnf`, sub-case (i)),
* UNSAT of `interiorCnf 33 7` (`m33k7int.sub.cnf`, sub-case (ii)),
by `mirrorExclusion_of_unsat`. The geometric step of sub-case (ii), `InteriorTieBreak`, is
stated as a proposition and proved in `TieBreak.lean` (`interiorTieBreak`).

`MirrorSet` fixes the axis to be the y-axis. A set symmetric in some other line is the image
of such a set under an isometry, which preserves general position and convex position;
that step is not formalised here.
-/

namespace Mir

open ETV ErdosSzekeres

/-- Sub-case (ii), geometric step: some enumeration of the points gives a mirror-symmetric
signotope with the axis point interior. Proved below (`interiorTieBreak_holds`), by sorting
along the key `x / (1 + ε y)` of the projective map `(x, y) ↦ (x, y) / (1 + ε y)`. -/
def InteriorTieBreak : Prop :=
  ∀ (S : Finset Point) (c : Point) (K : ℕ), 4 ≤ K → GeneralPosition S → MirrorSet S c →
    c ∈ convexHull ℝ (↑(S.erase c) : Set Point) → ¬HasConvexNGon K S →
    ∃ σ : Sig, IsSignotope S.card σ ∧ ¬HasGon σ S.card K ∧ MirSym S.card false σ ∧
      AxisInterior S.card σ

theorem interiorTieBreak_holds : InteriorTieBreak := interiorTieBreak

/-- The mirror-symmetric class at 33 points has no heptagon-free member. -/
def MirrorExclusion : Prop :=
  ∀ (S : Finset Point) (c : Point), GeneralPosition S → S.card = 33 → MirrorSet S c →
    HasConvexNGon 7 S

/-- Sub-case (ii) at the point-set level, from `InteriorTieBreak`. -/
theorem hasConvexNGon_of_unsat_interior (ht : InteriorTieBreak) {S : Finset Point}
    {c : Point} (hunsat : ¬DimacsSatisfiable (interiorCnf 33 7)) (hgp : GeneralPosition S)
    (hcard : S.card = 33) (hM : MirrorSet S c)
    (hin : c ∈ convexHull ℝ (↑(S.erase c) : Set Point)) : HasConvexNGon 7 S := by
  by_contra hno
  obtain ⟨σ, hσ, hg, hS, hI⟩ := ht S c 7 (by norm_num) hgp hM hin hno
  rw [hcard] at hσ hg hS hI
  exact hunsat (interiorCnf_satisfiable (by norm_num) (by norm_num) hσ hg hS hI)

/-- **The reduction**: UNSAT of the two CNFs implies `MirrorExclusion`. -/
theorem mirrorExclusion_of_unsat
    (h1 : ¬DimacsSatisfiable (hullCnf 33 7)) (h2 : ¬DimacsSatisfiable (interiorCnf 33 7)) :
    MirrorExclusion := by
  intro S c hgp hcard hM
  by_cases hin : c ∈ convexHull ℝ (↑(S.erase c) : Set Point)
  · exact hasConvexNGon_of_unsat_interior interiorTieBreak_holds h2 hgp hcard hM hin
  · exact hasConvexNGon_of_unsat_hull h1 hgp hcard hM hin

/-- The same with the two UNSAT facts in cube-and-conquer form: cube lists accepted by
`coverCheck` and a refutation of every cube CNF. -/
theorem mirrorExclusion_of_cubes {C1 C2 : List (List ℤ)}
    (hc1 : coverCheck C1 = true) (hc2 : coverCheck C2 = true)
    (h1 : ∀ c ∈ C1, ¬DimacsSatisfiable (cubeCnf (hullCnf 33 7) c))
    (h2 : ∀ c ∈ C2, ¬DimacsSatisfiable (cubeCnf (interiorCnf 33 7) c)) : MirrorExclusion :=
  mirrorExclusion_of_unsat (not_dimacsSatisfiable_of_coverCheck hc1 h1)
    (not_dimacsSatisfiable_of_coverCheck hc2 h2)

/-! ### One point on the axis -/

/-- A set of odd size in general position that is symmetric in the y-axis has exactly one point
on the axis: the off-axis points come in pairs, and three axis points would be collinear. -/
theorem exists_mirrorSet {S : Finset Point} (hgp : GeneralPosition S)
    (hsym : ∀ q ∈ S, reflX q ∈ S) (hodd : Odd S.card) : ∃ c, MirrorSet S c := by
  classical
  let A := S.filter fun q => q 0 = 0
  let L := S.filter fun q => q 0 < 0
  let R := S.filter fun q => 0 < q 0
  have hsplit : S.card = A.card + L.card + R.card := by
    have h1 := Finset.filter_card_add_filter_neg_card_eq_card (s := S) (fun q : Point => q 0 = 0)
    have h2 := Finset.filter_card_add_filter_neg_card_eq_card
      (s := S.filter fun q : Point => ¬q 0 = 0) (fun q : Point => q 0 < 0)
    rw [Finset.filter_filter, Finset.filter_filter] at h2
    have e1 : (S.filter fun q : Point => ¬q 0 = 0 ∧ q 0 < 0) = L := by
      apply Finset.filter_congr
      intro q _
      constructor
      · exact fun h => h.2
      · exact fun h => ⟨h.ne, h⟩
    have e2 : (S.filter fun q : Point => ¬q 0 = 0 ∧ ¬q 0 < 0) = R := by
      apply Finset.filter_congr
      intro q _
      constructor
      · rintro ⟨h1, h2⟩
        exact lt_of_le_of_ne (not_lt.1 h2) (Ne.symm h1)
      · exact fun h => ⟨h.ne', not_lt.2 h.le⟩
    rw [e1, e2] at h2
    change A.card + _ = S.card at h1
    omega
  have hLR : L.card = R.card := by
    have : L.image reflX = R := by
      ext q
      simp only [L, R, Finset.mem_image, Finset.mem_filter]
      constructor
      · rintro ⟨p, ⟨hp, hp0⟩, rfl⟩
        exact ⟨hsym p hp, by simp; linarith⟩
      · rintro ⟨hq, hq0⟩
        exact ⟨reflX q, ⟨hsym q hq, by simp; linarith⟩, reflX_reflX q⟩
    rw [← this, Finset.card_image_of_injective _ reflX_injective]
  have hAodd : Odd A.card := by
    rw [hsplit, hLR] at hodd
    rcases hodd with ⟨k, hk⟩
    exact ⟨k - R.card, by omega⟩
  have hA2 : A.card ≤ 2 := by
    by_contra h3
    obtain ⟨a, ha, b, hb, d, hd, hab, had, hbd⟩ := Finset.two_lt_card.1 (show 2 < A.card by omega)
    simp only [A, Finset.mem_filter] at ha hb hd
    apply (generalPosition_iff_orient_ne_zero S).1 hgp a ha.1 b hb.1 d hd.1 hab had hbd
    simp only [orient, ha.2, hb.2, hd.2]
    ring
  have hA1 : A.card = 1 := by
    rcases hAodd with ⟨k, hk⟩
    omega
  obtain ⟨c, hc⟩ := Finset.card_eq_one.1 hA1
  have hcA : c ∈ A := by rw [hc]; exact Finset.mem_singleton_self c
  simp only [A, Finset.mem_filter] at hcA
  refine ⟨c, hcA.1, hcA.2, hsym, ?_⟩
  intro q hq hqc hq0
  have : q ∈ A := by simp only [A, Finset.mem_filter]; exact ⟨hq, hq0⟩
  rw [hc, Finset.mem_singleton] at this
  exact hqc this

/-- The mirror class, stated without choosing the axis point: every 33-point set in general
position that is symmetric in the y-axis has a convex 7-gon. -/
def MirrorExclusionY : Prop :=
  ∀ S : Finset Point, GeneralPosition S → S.card = 33 → (∀ q ∈ S, reflX q ∈ S) →
    HasConvexNGon 7 S

theorem mirrorExclusionY_of_mirrorExclusion (h : MirrorExclusion) : MirrorExclusionY := by
  intro S hgp hcard hsym
  obtain ⟨c, hM⟩ := exists_mirrorSet hgp hsym (by rw [hcard]; decide)
  exact h S c hgp hcard hM

end Mir
