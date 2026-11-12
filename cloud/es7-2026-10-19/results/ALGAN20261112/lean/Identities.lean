import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

/-! Identities used in ALGAN20261112 (checked with `lean_run_code` in the repository project, Lean v4.24.0;
each `#print axioms` gives [propext, Classical.choice, Quot.sound]). Not part of the library build. -/

open Real

/-- det(w₀ - v₀, w₁ - v₀) for v₀ = (1,0), w₀ = ρ e^{iD}, w₁ = ρ e^{i(D+2a)}, a = π/m. -/
theorem twoLayer_orient_identity (ρ D a : ℝ) :
    ρ ^ 2 * sin (2 * a) - ρ * sin (D + 2 * a) + ρ * sin D
      = 2 * ρ * sin a * (ρ * cos a - cos (D + a)) := by
  have h1 : sin (D + 2 * a) - sin D = 2 * sin a * cos (D + a) := by
    rw [sin_sub_sin]; ring_nf
  have h2 : sin (2 * a) = 2 * sin a * cos a := sin_two_mul a
  have h3 : ρ * sin (D + 2 * a) - ρ * sin D = ρ * (2 * sin a * cos (D + a)) := by
    rw [← h1]; ring
  rw [h2]; linear_combination (-1 : ℝ) * h3

/-- G/f = 1 - sin²D/cos²a, in product form. -/
theorem threshold_product (a D : ℝ) :
    cos (a + D) * cos (a - D) = cos a ^ 2 - sin D ^ 2 := by
  rw [cos_add, cos_sub]
  linear_combination (cos a ^ 2) * (sin_sq_add_cos_sq D) - (sin D ^ 2) * (sin_sq_add_cos_sq a)

theorem g_lt_f (a D : ℝ) (hD : sin D ≠ 0) :
    cos (a + D) * cos (a - D) < cos a ^ 2 := by
  rw [threshold_product]; have := sq_pos_of_ne_zero hD; linarith

/-- bracket [a b c] = det(b - a, c - a). -/
def br (a b c : ℝ × ℝ) : ℝ := (b.1 - a.1) * (c.2 - a.2) - (b.2 - a.2) * (c.1 - a.1)
/-- rotation by +90°. -/
def rot (p : ℝ × ℝ) : ℝ × ℝ := (-p.2, p.1)

/-- Fourfold Pythagorean bracket relation. -/
theorem pyth_bracket (p s : ℝ × ℝ) :
    br p (-p) s ^ 2 + br p (-p) (rot s) ^ 2 = br p (rot p) (-p) * br s (rot s) (-s) := by
  simp only [br, rot, Prod.fst_neg, Prod.snd_neg]; ring

/-- Orbit-sum identity for a 4-fold orbit. -/
theorem orbit_sum (p q s : ℝ × ℝ) :
    br p q s + br p q (rot s) + br p q (-s) + br p q (rot (rot (rot s))) = 4 * br p q 0 := by
  simp only [br, rot, Prod.fst_neg, Prod.snd_neg, Prod.fst_zero, Prod.snd_zero]; ring
