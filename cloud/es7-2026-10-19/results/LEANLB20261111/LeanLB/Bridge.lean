import LeanLB.CheckerSound
import ErdosSzekeres.Basic
import ErdosSzekeres.OrientationGeometry
import ErdosSzekeres.Suk.TriangleMembership

/-!
# From the checker to the repository's definitions

`lowerBound_of_check`: let `φ` map lattice points to the plane so that every orientation
determinant is multiplied by one positive constant (`OrientScaling φ det`; an affine map of positive
determinant does this). If `gpOK L` and `checkAll B L` evaluate to `true`, then the image of `L` has
`L.length` points, is in general position (`ErdosSzekeres.GeneralPosition`) and has no `B + 2`
points in convex position (`¬ ErdosSzekeres.HasConvexNGon (B + 2) _`).
-/

namespace LeanLB

open ErdosSzekeres

/-- `φ` multiplies every orientation determinant by the positive constant `det`. -/
def OrientScaling (φ : NP → Point) (det : ℝ) : Prop :=
  0 < det ∧ ∀ a b c, orient (φ a) (φ b) (φ c) = det * (oz a b c : ℝ)

theorem orient_self12 (x c : Point) : orient x x c = 0 := by unfold orient; ring
theorem orient_self23 (a x : Point) : orient a x x = 0 := by unfold orient; ring
theorem orient_self13 (x b : Point) : orient x b x = 0 := by unfold orient; ring

/-- Points in convex position satisfy the four-point sign condition. -/
theorem convexSigns_of_convexPosition {φ : NP → Point} {det : ℝ} (hφ : OrientScaling φ det)
    (U : Finset NP) (hgp : ∀ a ∈ U, ∀ b ∈ U, ∀ c ∈ U, a ≠ b → a ≠ c → b ≠ c → oz a b c ≠ 0)
    (hconv : ConvexPosition (U.image φ)) : ConvexSigns U := by
  classical
  intro p hp a ha b hb c hc h1 h2 h3
  by_contra hneg
  have hab := (ne_of_opos h1).2.2
  have hac := (ne_of_opos h2).2.2
  have hbc := (ne_of_opos h3).2.2
  rw [opos_iff] at h1 h2 h3
  have hneg' : oz a b c < 0 := by
    rw [opos_iff, not_lt] at hneg
    exact lt_of_le_of_ne hneg (hgp a ha b hb c hc hab hac hbc)
  have hd := hφ.1
  have e := hφ.2
  have hpac : orient (φ p) (φ a) (φ c) ≠ 0 := by
    rw [e]; exact mul_ne_zero hd.ne' (by exact_mod_cast h2.ne')
  have hmem : φ b ∈ convexHull ℝ ({φ p, φ a, φ c} : Set Point) := by
    rw [Suk.mem_triangle_iff_orient_products _ _ _ _ hpac, e, e, e, e]
    have q1 : (0 : ℝ) < oz p a c := by exact_mod_cast h2
    have q2 : (0 : ℝ) < oz p a b := by exact_mod_cast h1
    have q3 : (0 : ℝ) < oz a c b := by rw [oz_swap23]; exact_mod_cast neg_pos.mpr hneg'
    have q4 : (0 : ℝ) < oz c p b := by
      rw [show oz c p b = oz p b c by rw [oz_cycle, oz_cycle]]; exact_mod_cast h3
    refine ⟨?_, ?_, ?_⟩ <;> positivity
  have hpb : φ p ≠ φ b := by
    intro h
    have := e p a b
    rw [h, orient_self13] at this
    have : (0 : ℝ) < det * oz p a b := mul_pos hd (by exact_mod_cast h1)
    linarith
  have hab' : φ a ≠ φ b := by
    intro h
    have := e p a b
    rw [h, orient_self23] at this
    have : (0 : ℝ) < det * oz p a b := mul_pos hd (by exact_mod_cast h1)
    linarith
  have hcb : φ c ≠ φ b := by
    intro h
    have := e p b c
    rw [h, orient_self23] at this
    have : (0 : ℝ) < det * oz p b c := mul_pos hd (by exact_mod_cast h3)
    linarith
  have hsub : ({φ p, φ a, φ c} : Set Point) ⊆ ((U.image φ : Finset Point) : Set Point) \ {φ b} := by
    intro x hx
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hx
    rcases hx with rfl | rfl | rfl
    · exact ⟨Finset.mem_coe.mpr (Finset.mem_image_of_mem φ hp), hpb⟩
    · exact ⟨Finset.mem_coe.mpr (Finset.mem_image_of_mem φ ha), hab'⟩
    · exact ⟨Finset.mem_coe.mpr (Finset.mem_image_of_mem φ hc), hcb⟩
  exact (convexPosition_iff _).mp hconv (φ b)
    (Finset.mem_coe.mpr (Finset.mem_image_of_mem φ hb)) (convexHull_mono hsub hmem)

theorem exists_third {L : List NP} (hnd : L.Nodup) (h3 : 3 ≤ L.length) (a b : NP) :
    ∃ c ∈ L, c ≠ a ∧ c ≠ b := by
  classical
  have hcard : 3 ≤ L.toFinset.card := by rw [List.toFinset_card_of_nodup hnd]; exact h3
  have h1 : 1 ≤ ((L.toFinset.erase a).erase b).card := by
    have := Finset.pred_card_le_card_erase (s := L.toFinset.erase a) (a := b)
    have := Finset.pred_card_le_card_erase (s := L.toFinset) (a := a)
    omega
  obtain ⟨c, hc⟩ := Finset.card_pos.mp (by omega : 0 < ((L.toFinset.erase a).erase b).card)
  simp only [Finset.mem_erase, List.mem_toFinset] at hc
  exact ⟨c, hc.2.2, hc.2.1, hc.1⟩

/-- **The bridge.** -/
theorem lowerBound_of_check {L : List NP} {B : ℕ} (hB : 1 ≤ B) (h3 : 3 ≤ L.length)
    (hgp : gpOK L = true) (hchk : checkAll B L = true) {φ : NP → Point} {det : ℝ}
    (hφ : OrientScaling φ det) :
    ((L.map φ).toFinset).card = L.length ∧ GeneralPosition (L.map φ).toFinset ∧
      ¬ HasConvexNGon (B + 2) (L.map φ).toFinset := by
  classical
  obtain ⟨hnd, hoz⟩ := gpOK_sound L hgp
  have hinj : ∀ x ∈ L, ∀ y ∈ L, φ x = φ y → x = y := by
    intro x hx y hy hxy
    by_contra hne
    obtain ⟨c, hc, hca, hcb⟩ := exists_third hnd h3 x y
    have h := hφ.2 x y c
    rw [hxy, orient_self12] at h
    have hz : (oz x y c : ℝ) ≠ 0 := by exact_mod_cast hoz x hx y hy c hc hne hca.symm hcb.symm
    have := mul_ne_zero hφ.1.ne' hz
    exact this h.symm
  refine ⟨?_, ?_, ?_⟩
  · rw [List.toFinset_card_of_nodup (hnd.map_on hinj), List.length_map]
  · rw [generalPosition_iff_orient_ne_zero]
    intro x hx y hy z hz hxy hxz hyz
    simp only [List.mem_toFinset, List.mem_map] at hx hy hz
    obtain ⟨a, ha, rfl⟩ := hx
    obtain ⟨b, hb, rfl⟩ := hy
    obtain ⟨c, hc, rfl⟩ := hz
    rw [hφ.2]
    refine mul_ne_zero hφ.1.ne' ?_
    exact_mod_cast hoz a ha b hb c hc (fun h => hxy (h ▸ rfl)) (fun h => hxz (h ▸ rfl))
      (fun h => hyz (h ▸ rfl))
  · rintro ⟨T, hTS, hTcard, hTconv⟩
    set U : Finset NP := L.toFinset.filter (fun x => φ x ∈ T) with hU
    have himg : U.image φ = T := by
      ext t
      simp only [hU, Finset.mem_image, Finset.mem_filter, List.mem_toFinset]
      constructor
      · rintro ⟨x, ⟨_, hx⟩, rfl⟩; exact hx
      · intro ht
        have := hTS ht
        simp only [List.mem_toFinset, List.mem_map] at this
        obtain ⟨x, hx, rfl⟩ := this
        exact ⟨x, ⟨hx, ht⟩, rfl⟩
    have hUL : ∀ x ∈ U, x ∈ L := fun x hx => by
      simp only [hU, Finset.mem_filter, List.mem_toFinset] at hx; exact hx.1
    have hcs : ConvexSigns U := by
      refine convexSigns_of_convexPosition hφ U ?_ (himg ▸ hTconv)
      intro a ha b hb c hc hab hac hbc
      exact hoz a (hUL a ha) b (hUL b hb) c (hUL c hc) hab hac hbc
    have hle := card_le_of_check hB hchk U hUL hcs
    have hge : T.card ≤ U.card := by rw [← himg]; exact Finset.card_image_le
    omega

end LeanLB
