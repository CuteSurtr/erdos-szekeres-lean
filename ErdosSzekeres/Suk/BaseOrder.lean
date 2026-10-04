import ErdosSzekeres.Suk.BaseChart

namespace ErdosSzekeres.Suk

structure BaseSegment where
  left : Point
  right : Point
  distinct : left ≠ right

@[ext] structure AboveBase (B : BaseSegment) where
  val : Point
  property : 0 < orient B.left B.right val

noncomputable def BaseSegment.frame (B : BaseSegment) : Point ≃ᵃ[ℝ] Point :=
  baseFrame B.left B.right B.distinct

/-- Every point on the positive side of an arbitrary base admits normalized
upper-half-plane coordinates. No assumption of an existing chart is required. -/
noncomputable def AboveBase.normalize {B : BaseSegment} (p : AboveBase B) : UpperPoint :=
  ⟨B.frame.symm p.val, by
    have h := orient_baseFrame_base B.left B.right B.distinct (B.frame.symm p.val)
    change orient B.left B.right (B.frame (B.frame.symm p.val)) = _ at h
    rw [B.frame.apply_symm_apply] at h
    have hp := p.property
    rw [h] at hp
    exact pos_of_mul_pos_right hp (baseLength_sq_pos B.left B.right B.distinct).le⟩

theorem AboveBase.normalize_injective (B : BaseSegment) :
    Function.Injective (@AboveBase.normalize B) := by
  intro p q h
  apply AboveBase.ext
  apply B.frame.symm.injective
  exact congrArg UpperPoint.val h

noncomputable instance (B : BaseSegment) : PartialOrder (AboveBase B) :=
  PartialOrder.lift AboveBase.normalize (AboveBase.normalize_injective B)

theorem AboveBase.le_iff {B : BaseSegment} (p q : AboveBase B) :
    p ≤ q ↔ q.val ∈ convexHull ℝ ({B.left, B.right, p.val} : Set Point) := by
  change p.normalize ≤ q.normalize ↔ _
  rw [baseFrame_triangle B.left B.right B.distinct]
  change B.frame (B.frame.symm q.val) ∈
    convexHull ℝ ({B.left, B.right, B.frame (B.frame.symm p.val)} : Set Point) ↔ _
  simp only [AffineEquiv.apply_symm_apply]

/-- The strict order is exactly the relation in Suk's Section 3. -/
theorem AboveBase.lt_iff {B : BaseSegment} (p q : AboveBase B) :
    p < q ↔ p ≠ q ∧ q.val ∈ convexHull ℝ ({B.left, B.right, p.val} : Set Point) := by
  rw [lt_iff_le_and_ne, AboveBase.le_iff, and_comm]

/-- The separating-line determinant test holds for every nondegenerate base. -/
theorem AboveBase.incomparable_same_side {B : BaseSegment} (p q : AboveBase B)
    (hpq : ¬ p ≤ q) (hqp : ¬ q ≤ p) :
    0 < orient p.val q.val B.left * orient p.val q.val B.right := by
  have h := incomparable_base_same_side p.normalize q.normalize hpq hqp
  have h₀ := orient_baseFrame B.left B.right B.distinct
    p.normalize.val q.normalize.val ![0, 0]
  have h₁ := orient_baseFrame B.left B.right B.distinct
    p.normalize.val q.normalize.val ![1, 0]
  change orient (B.frame (B.frame.symm p.val)) (B.frame (B.frame.symm q.val))
      (baseFrame B.left B.right B.distinct ![0, 0]) = _ at h₀
  change orient (B.frame (B.frame.symm p.val)) (B.frame (B.frame.symm q.val))
      (baseFrame B.left B.right B.distinct ![1, 0]) = _ at h₁
  simp only [AffineEquiv.apply_symm_apply, baseFrame_zero, baseFrame_one] at h₀ h₁
  rw [h₀, h₁]
  have hn := baseLength_sq_pos B.left B.right B.distinct
  convert mul_pos (mul_pos hn hn) h using 1
  ring

theorem orient_segment_ne_zero_of_same_side (p q a b : Point)
    (hside : 0 < orient p q a * orient p q b) {r : Point}
    (hr : r ∈ segment ℝ a b) : orient p q r ≠ 0 := by
  obtain ⟨u, v, hu, hv, huv, rfl⟩ := hr
  have he : orient p q (u • a + v • b) = u * orient p q a + v * orient p q b := by
    simp only [orient, Pi.add_apply, Pi.smul_apply, smul_eq_mul]
    linear_combination (p 1 * q 0 - p 0 * q 1) * huv
  rw [he]
  by_cases hu0 : u = 0
  · have hv1 : v = 1 := by linarith
    simpa [hu0, hv1] using right_ne_zero_of_mul (ne_of_gt hside)
  have hu' : 0 < u := lt_of_le_of_ne hu (Ne.symm hu0)
  rcases mul_pos_iff.mp hside with ⟨ha, hb⟩ | ⟨ha, hb⟩
  · exact ne_of_gt (add_pos_of_pos_of_nonneg (mul_pos hu' ha) (mul_nonneg hv hb.le))
  · exact ne_of_lt (add_neg_of_neg_of_nonpos (mul_neg_of_pos_of_neg hu' ha)
      (mul_nonpos_of_nonneg_of_nonpos hv hb.le))

/-- No line through an incomparable pair meets the base segment. -/
theorem AboveBase.incomparable_base_not_collinear {B : BaseSegment} (p q : AboveBase B)
    (hpq : ¬ p ≤ q) (hqp : ¬ q ≤ p) {r : Point}
    (hr : r ∈ segment ℝ B.left B.right) : ¬ Collinear ℝ ({p.val, q.val, r} : Set Point) := by
  rw [← orient_eq_zero_iff_collinear]
  exact orient_segment_ne_zero_of_same_side _ _ _ _ (p.incomparable_same_side q hpq hqp) hr

/-- A chain pair has the complementary geometry: its line meets the base. -/
theorem AboveBase.line_meets_base {B : BaseSegment} (p q : AboveBase B)
    (hpq : p < q) : ∃ r ∈ segment ℝ B.left B.right,
      Collinear ℝ ({p.val, q.val, r} : Set Point) := by
  obtain ⟨t, ht₀, ht₁, ht⟩ := triangleOrder_line_meets_base p.normalize q.normalize hpq
  refine ⟨B.frame ![t, 0], ?_, ?_⟩
  · have hseg : ![t, 0] ∈ segment ℝ (![0, 0] : Point) ![1, 0] := by
      refine ⟨1 - t, t, by linarith, ht₀, by ring, ?_⟩
      ext i
      fin_cases i <;> simp
    have hm := Set.mem_image_of_mem B.frame.toAffineMap hseg
    rw [image_segment] at hm
    change B.frame ![t, 0] ∈ segment ℝ
      (baseFrame B.left B.right B.distinct ![0, 0])
      (baseFrame B.left B.right B.distinct ![1, 0]) at hm
    simpa only [baseFrame_zero, baseFrame_one] using hm
  · rw [← orient_eq_zero_iff_collinear]
    have h := orient_baseFrame B.left B.right B.distinct
      p.normalize.val q.normalize.val ![t, 0]
    change orient (B.frame (B.frame.symm p.val)) (B.frame (B.frame.symm q.val))
      (B.frame ![t, 0]) = _ at h
    simpa only [AffineEquiv.apply_symm_apply, ht, mul_zero] using h

end ErdosSzekeres.Suk
