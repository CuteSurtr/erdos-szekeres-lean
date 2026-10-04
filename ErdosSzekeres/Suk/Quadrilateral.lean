import ErdosSzekeres.Suk.TriangleMembership

namespace ErdosSzekeres.Suk

private theorem excluded_triangle {s : Finset Point} (hc : ConvexPosition s)
    (p a b c : Point) (hp : p ∈ s) (ha : a ∈ s) (hb : b ∈ s) (hd : c ∈ s)
    (hpa : p ≠ a) (hpb : p ≠ b) (hpc : p ≠ c) :
    p ∉ convexHull ℝ ({a, b, c} : Set Point) := by
  intro h
  apply (convexPosition_iff s).mp hc p hp
  apply convexHull_mono (s := ({a, b, c} : Set Point)) ?_ h
  intro x hx
  rcases hx with rfl | rfl | rfl
  · exact ⟨ha, fun he => hpa he.symm⟩
  · exact ⟨hb, fun he => hpb he.symm⟩
  · exact ⟨hd, fun he => hpc he.symm⟩

/-- Exact sign characterization of a nondegenerate convex quadrilateral.
The forward proof exhausts the sixteen possible signs of its four triples. -/
theorem convexPosition_four_iff_pair_separation (a b c d : Point)
    (h₀ : orient a b c ≠ 0) (h₁ : orient a b d ≠ 0)
    (h₂ : orient a c d ≠ 0) (h₃ : orient b c d ≠ 0) :
    ConvexPosition ({a, b, c, d} : Finset Point) ↔
      (0 < orient a b c * orient a b d ∧ 0 < orient a c d * orient b c d) ∨
      (orient a b c * orient a c d < 0 ∧ orient a b d * orient b c d < 0) ∨
      (0 < orient a b d * orient a c d ∧ 0 < orient a b c * orient b c d) := by
  classical
  constructor
  · intro hc
    have hab : a ≠ b := by intro he; subst b; simp [orient] at h₀
    have hac : a ≠ c := by intro he; subst c; apply h₀; simp [orient]
    have had : a ≠ d := by intro he; subst d; apply h₁; simp [orient]
    have hbc : b ≠ c := by intro he; subst c; apply h₀; simp only [orient]; ring
    have hbd : b ≠ d := by intro he; subst d; apply h₁; simp only [orient]; ring
    have hcd : c ≠ d := by intro he; subst d; apply h₂; simp only [orient]; ring
    have ha := excluded_triangle hc a b c d (by simp) (by simp) (by simp) (by simp) hab hac had
    have hb := excluded_triangle hc b a c d (by simp) (by simp) (by simp) (by simp) hab.symm hbc hbd
    have hcn := excluded_triangle hc c a b d (by simp) (by simp) (by simp) (by simp) hac.symm hbc.symm hcd
    have hd := excluded_triangle hc d a b c (by simp) (by simp) (by simp) (by simp) had.symm hbd.symm hcd.symm
    rw [mem_triangle_iff_orient_products b c d a h₃] at ha
    rw [mem_triangle_iff_orient_products a c d b h₂] at hb
    rw [mem_triangle_iff_orient_products a b d c h₁] at hcn
    rw [mem_triangle_iff_orient_products a b c d h₀] at hd
    have hba : orient d b a = -orient a b d := by simp only [orient]; ring
    have hcb : orient a c b = -orient a b c := orient_swap a b c
    have hdc : orient d a c = orient a c d := by simp only [orient]; ring
    have hdb : orient b d c = -orient b c d := orient_swap b c d
    have hca : orient c a d = -orient a c d := by simp only [orient]; ring
    rw [orient_cycle a b c, orient_cycle a c d, hba] at ha
    rw [hcb, orient_cycle b c d, orient_cycle b d a, orient_cycle a b d] at hb
    rw [hdb, hdc] at hcn
    rw [hca] at hd
    have hsum : orient a b c - orient a b d + orient a c d - orient b c d = 0 := by
      simp only [orient]
      ring
    rcases lt_or_gt_of_ne h₀ with h₀ | h₀ <;>
      rcases lt_or_gt_of_ne h₁ with h₁ | h₁ <;>
      rcases lt_or_gt_of_ne h₂ with h₂ | h₂ <;>
      rcases lt_or_gt_of_ne h₃ with h₃ | h₃
    · left; constructor <;> nlinarith only [h₀, h₁, h₂, h₃]
    · exfalso; apply hcn; refine ⟨?_, ?_, ?_⟩ <;> nlinarith only [h₀, h₁, h₂, h₃]
    · exfalso; apply hd; refine ⟨?_, ?_, ?_⟩ <;> nlinarith only [h₀, h₁, h₂, h₃]
    · left; constructor <;> nlinarith only [h₀, h₁, h₂, h₃]
    · exfalso; apply ha; refine ⟨?_, ?_, ?_⟩ <;> nlinarith only [h₀, h₁, h₂, h₃]
    · exfalso; linarith only [hsum, h₀, h₁, h₂, h₃]
    · right; left; constructor <;> nlinarith only [h₀, h₁, h₂, h₃]
    · exfalso; apply hb; refine ⟨?_, ?_, ?_⟩ <;> nlinarith only [h₀, h₁, h₂, h₃]
    · exfalso; apply hb; refine ⟨?_, ?_, ?_⟩ <;> nlinarith only [h₀, h₁, h₂, h₃]
    · right; left; constructor <;> nlinarith only [h₀, h₁, h₂, h₃]
    · exfalso; linarith only [hsum, h₀, h₁, h₂, h₃]
    · exfalso; apply ha; refine ⟨?_, ?_, ?_⟩ <;> nlinarith only [h₀, h₁, h₂, h₃]
    · left; constructor <;> nlinarith only [h₀, h₁, h₂, h₃]
    · exfalso; apply hd; refine ⟨?_, ?_, ?_⟩ <;> nlinarith only [h₀, h₁, h₂, h₃]
    · exfalso; apply hcn; refine ⟨?_, ?_, ?_⟩ <;> nlinarith only [h₀, h₁, h₂, h₃]
    · left; constructor <;> nlinarith only [h₀, h₁, h₂, h₃]
  · rintro (h | h | h)
    · apply convexPosition_four_of_pair_separation a b c d h.1
      simpa only [orient_cycle] using h.2
    · have ht := convexPosition_four_of_pair_separation a c b d
        (by rw [orient_swap a b c]; nlinarith [h.1])
        (by rw [orient_cycle a b d, orient_swap b c d]; nlinarith [h.2])
      convert ht using 1
      ext x
      simp [or_left_comm]
    · have ht := convexPosition_four_of_pair_separation a d b c
        (by rw [orient_swap a b d, orient_swap a c d]; nlinarith [h.1])
        (by rw [orient_cycle a b c]; exact h.2)
      convert ht using 1
      ext x
      simp [or_left_comm, or_comm]

private theorem products_same_sign (x x' y y' : ℝ) (hx : 0 < x * x') (hy : 0 < y * y') :
    (0 < x * y ↔ 0 < x' * y') ∧ (x * y < 0 ↔ x' * y' < 0) := by
  rcases mul_pos_iff.mp hx with hx | hx <;>
    rcases mul_pos_iff.mp hy with hy | hy <;>
    rcases hx with ⟨hx, hx'⟩ <;> rcases hy with ⟨hy, hy'⟩ <;>
    constructor <;> constructor <;> intro h <;> nlinarith only [hx, hx', hy, hy', h]

/-- Moving the fourth point within the same open region of the three
pair-lines preserves convex position. No convexity of a surrounding region
or combinatorial order-type axiom is assumed. -/
theorem convexPosition_four_same_cell (a b c p q : Point)
    (habc : orient a b c ≠ 0)
    (hab : 0 < orient a b p * orient a b q)
    (hac : 0 < orient a c p * orient a c q)
    (hbc : 0 < orient b c p * orient b c q) :
    ConvexPosition ({a, b, c, p} : Finset Point) ↔
      ConvexPosition ({a, b, c, q} : Finset Point) := by
  have hp₁ := left_ne_zero_of_mul (ne_of_gt hab)
  have hp₂ := left_ne_zero_of_mul (ne_of_gt hac)
  have hp₃ := left_ne_zero_of_mul (ne_of_gt hbc)
  have hq₁ := right_ne_zero_of_mul (ne_of_gt hab)
  have hq₂ := right_ne_zero_of_mul (ne_of_gt hac)
  have hq₃ := right_ne_zero_of_mul (ne_of_gt hbc)
  have hd : 0 < orient a b c * orient a b c := mul_self_pos.mpr habc
  have hde := products_same_sign _ _ _ _ hd hab
  have hfg := products_same_sign _ _ _ _ hac hbc
  have hdf := products_same_sign _ _ _ _ hd hac
  have heg := products_same_sign _ _ _ _ hab hbc
  have hef := products_same_sign _ _ _ _ hab hac
  have hdg := products_same_sign _ _ _ _ hd hbc
  rw [convexPosition_four_iff_pair_separation a b c p habc hp₁ hp₂ hp₃,
    convexPosition_four_iff_pair_separation a b c q habc hq₁ hq₂ hq₃]
  simp only [hde.1, hfg.1, hdf.2, heg.2, hef.1, hdg.1]

/-- Three ordered points whose pair-lines all put an anchor on the positive
side form a convex quadrilateral with it exactly in the positive color. -/
theorem convexPosition_four_iff_positive_of_anchor (a b c p : Point)
    (hn : orient a b c ≠ 0) (hab : 0 < orient a b p)
    (hac : 0 < orient a c p) (hbc : 0 < orient b c p) :
    ConvexPosition ({a, b, c, p} : Finset Point) ↔ 0 < orient a b c := by
  rw [convexPosition_four_iff_pair_separation a b c p hn
    (ne_of_gt hab) (ne_of_gt hac) (ne_of_gt hbc)]
  constructor
  · rintro (h | h | h)
    · exact pos_of_mul_pos_left h.1 hab.le
    · have ht := mul_pos hab hbc
      linarith [h.2]
    · exact pos_of_mul_pos_left h.2 hbc.le
  · intro h
    exact Or.inl ⟨mul_pos h hab, mul_pos hac hbc⟩

theorem convexPosition_four_iff_negative_of_anchor (a b c p : Point)
    (hn : orient a b c ≠ 0) (hab : orient a b p < 0)
    (hac : orient a c p < 0) (hbc : orient b c p < 0) :
    ConvexPosition ({a, b, c, p} : Finset Point) ↔ orient a b c < 0 := by
  rw [convexPosition_four_iff_pair_separation a b c p hn
    (ne_of_lt hab) (ne_of_lt hac) (ne_of_lt hbc)]
  constructor
  · rintro (h | h | h)
    · by_contra! ht
      have := mul_nonpos_of_nonneg_of_nonpos ht hab.le
      linarith [h.1]
    · have ht := mul_pos_of_neg_of_neg hab hbc
      linarith [h.2]
    · by_contra! ht
      have := mul_nonpos_of_nonneg_of_nonpos ht hbc.le
      linarith [h.2]
  · intro h
    exact Or.inl ⟨mul_pos_of_neg_of_neg h hab, mul_pos_of_neg_of_neg hac hbc⟩

end ErdosSzekeres.Suk
