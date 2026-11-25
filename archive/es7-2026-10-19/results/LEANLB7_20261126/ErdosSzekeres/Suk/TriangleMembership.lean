import ErdosSzekeres.Suk.SupportingLines

namespace ErdosSzekeres.Suk

theorem orient_triangle_sum (a b c p : Point) :
    orient b c p + orient c a p + orient a b p = orient a b c := by
  simp only [orient]
  ring

/-- Membership in a positively oriented triangle is exactly membership in
its three closed supporting halfplanes. -/
theorem mem_triangle_iff_of_orient_pos (a b c p : Point) (h : 0 < orient a b c) :
    p ∈ convexHull ℝ ({a, b, c} : Set Point) ↔
      0 ≤ orient a b p ∧ 0 ≤ orient b c p ∧ 0 ≤ orient c a p := by
  constructor
  · intro hp
    have halfplane (x y : Point)
        (hx : 0 ≤ orient x y a) (hy : 0 ≤ orient x y b) (hz : 0 ≤ orient x y c) :
        0 ≤ orient x y p := by
      apply convexHull_min (t := {r : Point | 0 ≤ orient x y r}) ?_
        (convex_orient_nonnegative x y) hp
      intro r hr
      rcases hr with rfl | rfl | rfl <;> assumption
    refine ⟨halfplane a b ?_ ?_ h.le, halfplane b c ?_ ?_ ?_,
      halfplane c a ?_ ?_ ?_⟩ <;> simp only [orient] at * <;> nlinarith
  · rintro ⟨hab, hbc, hca⟩
    apply triangle_mem_of_weights a b c p
      (orient b c p / orient a b c) (orient c a p / orient a b c)
      (orient a b p / orient a b c)
      (div_nonneg hbc h.le) (div_nonneg hca h.le) (div_nonneg hab h.le)
    · rw [← add_div, ← add_div, orient_triangle_sum, div_self (ne_of_gt h)]
    · ext i
      simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
      field_simp [ne_of_gt h]
      fin_cases i <;> norm_num [orient] <;> ring

/-- An orientation-invariant triangle test, valid for either orientation of
the vertices. The nonzero hypothesis is essential for degenerate triangles. -/
theorem mem_triangle_iff_orient_products (a b c p : Point) (h : orient a b c ≠ 0) :
    p ∈ convexHull ℝ ({a, b, c} : Set Point) ↔
      0 ≤ orient a b c * orient a b p ∧
      0 ≤ orient a b c * orient b c p ∧
      0 ≤ orient a b c * orient c a p := by
  rcases lt_or_gt_of_ne h with hn | hp
  · have hs : ({a, b, c} : Set Point) = {a, c, b} := by ext x; simp [or_comm]
    rw [hs, mem_triangle_iff_of_orient_pos a c b p (by rw [orient_swap]; linarith)]
    have hac : orient a c p = -orient c a p := by simp only [orient]; ring
    have hcb : orient c b p = -orient b c p := by simp only [orient]; ring
    have hba : orient b a p = -orient a b p := by simp only [orient]; ring
    rw [hac, hcb, hba]
    have hm (z : ℝ) : 0 ≤ orient a b c * z ↔ z ≤ 0 := by
      constructor
      · intro hz; nlinarith
      · exact mul_nonneg_of_nonpos_of_nonpos hn.le
    simp only [neg_nonneg, hm]
    tauto
  · rw [mem_triangle_iff_of_orient_pos a b c p hp]
    simp only [mul_nonneg_iff_of_pos_left hp]

/-- If the line pq puts r and s strictly on the same side, p cannot lie
inside the nondegenerate triangle qrs. -/
theorem not_mem_triangle_of_same_side (p q r s : Point)
    (h : 0 < orient p q r * orient p q s) (hn : orient q r s ≠ 0) :
    p ∉ convexHull ℝ ({q, r, s} : Set Point) := by
  intro hp
  have ht := (mem_triangle_iff_orient_products q r s p hn).mp hp
  have h₁ : orient q r p = orient p q r := orient_cycle p q r
  have h₂ : orient s q p = -orient p q s := by simp only [orient]; ring
  rw [h₁, h₂] at ht
  have hm := mul_nonneg ht.1 ht.2.2
  have hpos := mul_pos h (sq_pos_of_ne_zero hn)
  nlinarith

/-- The two pair-lines miss the opposite segments. This four-point
criterion is the elementary geometric step used in HMPT Observation 3.5. -/
theorem convexPosition_four_of_pair_separation (a b c d : Point)
    (hab : 0 < orient a b c * orient a b d)
    (hcd : 0 < orient c d a * orient c d b) :
    ConvexPosition ({a, b, c, d} : Finset Point) := by
  classical
  have habc : orient a b c ≠ 0 := left_ne_zero_of_mul (ne_of_gt hab)
  have habd : orient a b d ≠ 0 := right_ne_zero_of_mul (ne_of_gt hab)
  have hcda : orient c d a ≠ 0 := left_ne_zero_of_mul (ne_of_gt hcd)
  have hcdb : orient c d b ≠ 0 := right_ne_zero_of_mul (ne_of_gt hcd)
  have hba : 0 < orient b a c * orient b a d := by
    convert hab using 1
    simp only [orient]
    ring
  have hdc : 0 < orient d c a * orient d c b := by
    convert hcd using 1
    simp only [orient]
    ring
  have ha := not_mem_triangle_of_same_side a b c d hab (by
    simpa only [orient_cycle b c d] using hcdb)
  have hb := not_mem_triangle_of_same_side b a c d hba (by
    simpa only [orient_cycle a c d] using hcda)
  have hc := not_mem_triangle_of_same_side c d a b hcd (by
    simpa only [orient_cycle d a b] using habd)
  have hd := not_mem_triangle_of_same_side d c a b hdc (by
    simpa only [orient_cycle c a b] using habc)
  rw [convexPosition_iff]
  intro p hp hmem
  simp only [Finset.coe_insert, Finset.coe_singleton, Set.mem_insert_iff,
    Set.mem_singleton_iff] at hp
  rcases hp with hp | hp | hp | hp <;> subst p
  · apply ha
    apply convexHull_mono (s := (↑({a, b, c, d} : Finset Point) : Set Point) \ {a}) ?_ hmem
    intro x hx
    simp only [Finset.coe_insert, Finset.coe_singleton, Set.mem_diff, Set.mem_insert_iff,
      Set.mem_singleton_iff] at hx ⊢
    tauto
  · apply hb
    apply convexHull_mono (s := (↑({a, b, c, d} : Finset Point) : Set Point) \ {b}) ?_ hmem
    intro x hx
    simp only [Finset.coe_insert, Finset.coe_singleton, Set.mem_diff, Set.mem_insert_iff,
      Set.mem_singleton_iff] at hx ⊢
    tauto
  · apply hc
    apply convexHull_mono (s := (↑({a, b, c, d} : Finset Point) : Set Point) \ {c}) ?_ hmem
    intro x hx
    simp only [Finset.coe_insert, Finset.coe_singleton, Set.mem_diff, Set.mem_insert_iff,
      Set.mem_singleton_iff] at hx ⊢
    tauto
  · apply hd
    apply convexHull_mono (s := (↑({a, b, c, d} : Finset Point) : Set Point) \ {d}) ?_ hmem
    intro x hx
    simp only [Finset.coe_insert, Finset.coe_singleton, Set.mem_diff, Set.mem_insert_iff,
      Set.mem_singleton_iff] at hx ⊢
    tauto

end ErdosSzekeres.Suk
