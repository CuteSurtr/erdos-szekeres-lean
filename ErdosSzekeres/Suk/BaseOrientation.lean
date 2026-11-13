import ErdosSzekeres.Suk.ChainColoring

namespace ErdosSzekeres.Suk

theorem AboveBase.orient_eq_normalized {B : BaseSegment} (p q r : AboveBase B) :
    orient p.val q.val r.val =
      ((B.right 0 - B.left 0) ^ 2 + (B.right 1 - B.left 1) ^ 2) *
        orient p.normalize.val q.normalize.val r.normalize.val := by
  have h := orient_baseFrame B.left B.right B.distinct p.normalize.val q.normalize.val r.normalize.val
  change orient (B.frame (B.frame.symm p.val)) (B.frame (B.frame.symm q.val))
    (B.frame (B.frame.symm r.val)) = _ at h
  simpa only [AffineEquiv.apply_symm_apply] using h

theorem AboveBase.orient_pos_iff_normalized {B : BaseSegment} (p q r : AboveBase B) :
    0 < orient p.val q.val r.val ↔ 0 < orient p.normalize.val q.normalize.val r.normalize.val := by
  rw [p.orient_eq_normalized q r]
  exact mul_pos_iff_of_pos_left (baseLength_sq_pos B.left B.right B.distinct)

/-- Ordered pairs place the left and right base endpoints on opposite weak
sides. General position turns these into strict inequalities. -/
theorem AboveBase.pair_orientation_sides {B : BaseSegment} (p q : AboveBase B) (hpq : p ≤ q) :
    orient p.val q.val B.left ≤ 0 ∧ 0 ≤ orient p.val q.val B.right := by
  obtain ⟨hc₀, hc₁⟩ := (triangleOrder_cross_products p.normalize q.normalize).mp hpq
  have h₀ : orient p.normalize.val q.normalize.val ![0, 0] ≤ 0 := by
    simp only [orient, Matrix.cons_val_zero, Matrix.cons_val_one]
    nlinarith
  have h₁ : 0 ≤ orient p.normalize.val q.normalize.val ![1, 0] := by
    simp only [orient, Matrix.cons_val_zero, Matrix.cons_val_one]
    nlinarith
  have e₀ := orient_baseFrame B.left B.right B.distinct p.normalize.val q.normalize.val ![0, 0]
  have e₁ := orient_baseFrame B.left B.right B.distinct p.normalize.val q.normalize.val ![1, 0]
  change orient (B.frame (B.frame.symm p.val)) (B.frame (B.frame.symm q.val))
      (baseFrame B.left B.right B.distinct ![0, 0]) = _ at e₀
  change orient (B.frame (B.frame.symm p.val)) (B.frame (B.frame.symm q.val))
      (baseFrame B.left B.right B.distinct ![1, 0]) = _ at e₁
  simp only [AffineEquiv.apply_symm_apply, baseFrame_zero, baseFrame_one] at e₀ e₁
  rw [e₀, e₁]
  have hn := (baseLength_sq_pos B.left B.right B.distinct).le
  exact ⟨mul_nonpos_of_nonneg_of_nonpos hn h₀, mul_nonneg hn h₁⟩

theorem AboveBase.positive_transitive (B : BaseSegment) : TripleTransitive
    (fun p q r : AboveBase B => 0 < orient p.val q.val r.val) := by
  intro a b c d hab hbc hcd h₀ h₁
  rw [AboveBase.orient_pos_iff_normalized] at h₀ h₁
  dsimp only
  rw [AboveBase.orient_pos_iff_normalized, AboveBase.orient_pos_iff_normalized]
  exact upperPoint_positive_transitive _ _ _ _ hab hbc hcd h₀ h₁

theorem AboveBase.nonpositive_transitive (B : BaseSegment) : TripleTransitive
    (fun p q r : AboveBase B => ¬ 0 < orient p.val q.val r.val) := by
  intro a b c d hab hbc hcd h₀ h₁
  rw [AboveBase.orient_pos_iff_normalized] at h₀ h₁
  dsimp only
  rw [AboveBase.orient_pos_iff_normalized, AboveBase.orient_pos_iff_normalized]
  exact upperPoint_nonpositive_transitive _ _ _ _ hab hbc hcd h₀ h₁

end ErdosSzekeres.Suk
