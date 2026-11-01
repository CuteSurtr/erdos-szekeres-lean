import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Data.Sign.Basic
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

/-!
# `ES8SYM/proofs/layers.md`, Lemma 1: polar orientation formula

For points `p_k = (cos φ_k, sin φ_k) / u_k` with `u_k > 0`,
`orient(p₁, p₂, p₃) = sign (u₁ sin(φ₃ - φ₂) + u₂ sin(φ₁ - φ₃) + u₃ sin(φ₂ - φ₁))`,
where `orient = sign det [[x_k, y_k, 1]]`.  We also check the cross-product form used by the exact checkers, and the
consequence for layered configurations: with a layer map `L : ι → Fin t` and layer variables `u : Fin t → ℝ`
(`u o = 1 / r_o > 0`), every orientation is the sign of a linear form in `u` whose coefficient vector depends only on
the phases.
-/

open Real

namespace C7

/-- The value identity behind Lemma 1 (no positivity needed, only `u_k ≠ 0`). -/
theorem det_mul_eq (φ₁ φ₂ φ₃ u₁ u₂ u₃ : ℝ) (h₁ : u₁ ≠ 0) (h₂ : u₂ ≠ 0) (h₃ : u₃ ≠ 0) :
    Matrix.det !![cos φ₁ / u₁, sin φ₁ / u₁, 1; cos φ₂ / u₂, sin φ₂ / u₂, 1; cos φ₃ / u₃, sin φ₃ / u₃, 1]
        * (u₁ * u₂ * u₃)
      = u₁ * sin (φ₃ - φ₂) + u₂ * sin (φ₁ - φ₃) + u₃ * sin (φ₂ - φ₁) := by
  rw [Matrix.det_fin_three]
  simp only [Matrix.of_apply, Matrix.cons_val', Matrix.cons_val_zero, Matrix.cons_val_one,
    Matrix.cons_val_two, Matrix.head_cons, Matrix.tail_cons, Matrix.empty_val', Matrix.cons_val_fin_one,
    Matrix.head_fin_const]
  rw [sin_sub, sin_sub, sin_sub]
  field_simp
  ring

/-- Lemma 1 as stated (determinant convention). -/
theorem orient_polar (φ₁ φ₂ φ₃ u₁ u₂ u₃ : ℝ) (h₁ : 0 < u₁) (h₂ : 0 < u₂) (h₃ : 0 < u₃) :
    SignType.sign
        (Matrix.det !![cos φ₁ / u₁, sin φ₁ / u₁, 1; cos φ₂ / u₂, sin φ₂ / u₂, 1; cos φ₃ / u₃, sin φ₃ / u₃, 1])
      = SignType.sign (u₁ * sin (φ₃ - φ₂) + u₂ * sin (φ₁ - φ₃) + u₃ * sin (φ₂ - φ₁)) := by
  rw [← det_mul_eq φ₁ φ₂ φ₃ u₁ u₂ u₃ h₁.ne' h₂.ne' h₃.ne', sign_mul,
    sign_pos (by positivity : (0 : ℝ) < u₁ * u₂ * u₃), mul_one]

/-- Cross-product orientation `(q - p) × (r - p)` (the convention of the exact checkers). -/
def cross (p q r : ℝ × ℝ) : ℝ := (q.1 - p.1) * (r.2 - p.2) - (q.2 - p.2) * (r.1 - p.1)

/-- The point with phase `φ` and inverse radius `u`. -/
noncomputable def pt (φ u : ℝ) : ℝ × ℝ := (cos φ / u, sin φ / u)

theorem orient_polar_cross (φ₁ φ₂ φ₃ u₁ u₂ u₃ : ℝ) (h₁ : 0 < u₁) (h₂ : 0 < u₂) (h₃ : 0 < u₃) :
    SignType.sign (cross (pt φ₁ u₁) (pt φ₂ u₂) (pt φ₃ u₃))
      = SignType.sign (u₁ * sin (φ₃ - φ₂) + u₂ * sin (φ₁ - φ₃) + u₃ * sin (φ₂ - φ₁)) := by
  have key : cross (pt φ₁ u₁) (pt φ₂ u₂) (pt φ₃ u₃) * (u₁ * u₂ * u₃)
      = u₁ * sin (φ₃ - φ₂) + u₂ * sin (φ₁ - φ₃) + u₃ * sin (φ₂ - φ₁) := by
    simp only [cross, pt]
    rw [sin_sub, sin_sub, sin_sub]
    field_simp
    ring
  rw [← key, sign_mul, sign_pos (by positivity : (0 : ℝ) < u₁ * u₂ * u₃), mul_one]

/-- Coefficient vector (in the layer variables) of the linear form attached to the triple `(i, j, k)`.
It depends only on the phases `φ` and the layer map `L`, not on the radii. -/
noncomputable def coef {ι : Type*} {t : ℕ} (L : ι → Fin t) (φ : ι → ℝ) (i j k : ι) : Fin t → ℝ :=
  Pi.single (L i) (sin (φ k - φ j)) + Pi.single (L j) (sin (φ i - φ k)) + Pi.single (L k) (sin (φ j - φ i))

/-- Consequence of Lemma 1: in a layered configuration (point `i` has phase `φ i` and lies on layer `L i` of inverse
radius `u (L i) > 0`), every orientation is the sign of the linear form `u ↦ ∑ₒ coef(i,j,k)ₒ uₒ`. -/
theorem orient_layered {ι : Type*} {t : ℕ} (L : ι → Fin t) (φ : ι → ℝ) (u : Fin t → ℝ) (hu : ∀ o, 0 < u o)
    (i j k : ι) :
    SignType.sign (cross (pt (φ i) (u (L i))) (pt (φ j) (u (L j))) (pt (φ k) (u (L k))))
      = SignType.sign (∑ o, coef L φ i j k o * u o) := by
  rw [orient_polar_cross _ _ _ _ _ _ (hu _) (hu _) (hu _)]
  congr 1
  simp only [coef, Pi.add_apply, add_mul, Finset.sum_add_distrib, Pi.single_apply, ite_mul, zero_mul,
    Finset.sum_ite_eq', Finset.mem_univ, if_true]
  ring

/-- Hence, for fixed phases, the order type is constant along rays (central arrangement): scaling all `u` by
`λ > 0` changes no orientation. -/
theorem orient_layered_scale {ι : Type*} {t : ℕ} (L : ι → Fin t) (φ : ι → ℝ) (u : Fin t → ℝ) (hu : ∀ o, 0 < u o)
    (lam : ℝ) (hl : 0 < lam) (i j k : ι) :
    SignType.sign (cross (pt (φ i) (lam * u (L i))) (pt (φ j) (lam * u (L j))) (pt (φ k) (lam * u (L k))))
      = SignType.sign (cross (pt (φ i) (u (L i))) (pt (φ j) (u (L j))) (pt (φ k) (u (L k)))) := by
  have h := orient_layered L φ (fun o => lam * u o) (fun o => mul_pos hl (hu o)) i j k
  simp only at h
  rw [h, orient_layered L φ u hu i j k]
  have : (∑ o, coef L φ i j k o * (lam * u o)) = lam * ∑ o, coef L φ i j k o * u o := by
    rw [Finset.mul_sum]; exact Finset.sum_congr rfl (fun o _ => by ring)
  rw [this, sign_mul, sign_pos hl, one_mul]

/-! ### The instance in the claim: nested regular `m`-gons with radii `r o > 0` and phases `θ o`.
Point `(o, k)` is `r o * (cos φ, sin φ)` with `φ = θ o + 2πk/m`; the layer variable is `u o = 1 / r o`. -/

noncomputable def phase (m : ℕ) {t : ℕ} (θ : Fin t → ℝ) (p : Fin t × Fin m) : ℝ :=
  θ p.1 + 2 * π * ((p.2 : ℕ) : ℝ) / m

noncomputable def ngonPt (m : ℕ) {t : ℕ} (θ r : Fin t → ℝ) (p : Fin t × Fin m) : ℝ × ℝ :=
  (r p.1 * cos (phase m θ p), r p.1 * sin (phase m θ p))

theorem ngonPt_eq_pt (m : ℕ) {t : ℕ} (θ r : Fin t → ℝ) (hr : ∀ o, 0 < r o) (p : Fin t × Fin m) :
    ngonPt m θ r p = pt (phase m θ p) (1 / r p.1) := by
  have h := (hr p.1).ne'
  simp only [ngonPt, pt]
  ext <;> simp only [div_div_eq_mul_div, div_one, mul_comm]

/-- C7 for nested regular `m`-gons: every orientation is the sign of a linear form in the variables `1 / r o`
whose coefficient vector `coef Prod.fst (phase m θ) a b c` depends only on the phases `θ` (and `m`), not on `r`. -/
theorem nested_regular_orient (m : ℕ) {t : ℕ} (θ r : Fin t → ℝ) (hr : ∀ o, 0 < r o) (a b c : Fin t × Fin m) :
    SignType.sign (cross (ngonPt m θ r a) (ngonPt m θ r b) (ngonPt m θ r c))
      = SignType.sign (∑ o, coef Prod.fst (phase m θ) a b c o * (1 / r o)) := by
  rw [ngonPt_eq_pt m θ r hr a, ngonPt_eq_pt m θ r hr b, ngonPt_eq_pt m θ r hr c]
  exact orient_layered Prod.fst (phase m θ) (fun o => 1 / r o) (fun o => by have := hr o; positivity) a b c

/-- Scope remark (not part of Lemma 1, which needs `u` finite): triples with the centre `O = (0,0)` have an
orientation that depends on the phases only. -/
theorem orient_centre (φ₁ φ₂ u₁ u₂ : ℝ) (h₁ : 0 < u₁) (h₂ : 0 < u₂) :
    SignType.sign (cross (pt φ₁ u₁) (pt φ₂ u₂) (0, 0)) = SignType.sign (sin (φ₂ - φ₁)) := by
  have key : cross (pt φ₁ u₁) (pt φ₂ u₂) (0, 0) * (u₁ * u₂) = sin (φ₂ - φ₁) := by
    simp only [cross, pt]
    rw [sin_sub]
    field_simp
    ring
  rw [← key, sign_mul, sign_pos (by positivity : (0 : ℝ) < u₁ * u₂), mul_one]

end C7

#print axioms C7.orient_polar
#print axioms C7.orient_polar_cross
#print axioms C7.orient_layered
#print axioms C7.orient_layered_scale
#print axioms C7.nested_regular_orient
#print axioms C7.orient_centre
