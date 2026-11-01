import ErdosSzekeres.Definitions
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Topology.MetricSpace.Isometry

/-!
Independent check of the sup-metric pitfall noted in `SymmetricReduction.lean` (1 November 2026).

`eDist2`, `IsEucIsometry`, `rotAbout`, `halfTurn`, `reflLine` are copied verbatim from
`SymmetricReduction.lean` (sections 2-3).  `Point` is the repository's `ErdosSzekeres.Point`
(`abbrev Point := Fin 2 → ℝ`).
-/

namespace SupMetricCheck

open ErdosSzekeres

/-! ### Verbatim copies of the definitions in `SymmetricReduction.lean` -/

def eDist2 (p q : Point) : ℝ := (p 0 - q 0) ^ 2 + (p 1 - q 1) ^ 2

def IsEucIsometry (g : Point → Point) : Prop := ∀ p q, eDist2 (g p) (g q) = eDist2 p q

noncomputable def rotAbout (c : Point) (θ : ℝ) (p : Point) : Point :=
  ![c 0 + Real.cos θ * (p 0 - c 0) - Real.sin θ * (p 1 - c 1),
    c 1 + Real.sin θ * (p 0 - c 0) + Real.cos θ * (p 1 - c 1)]

def halfTurn (c p : Point) : Point := ![2 * c 0 - p 0, 2 * c 1 - p 1]

def reflLine (a u : Point) (p : Point) : Point :=
  let d := (p 0 - a 0) * u 0 + (p 1 - a 1) * u 1
  ![a 0 + 2 * d * u 0 - (p 0 - a 0), a 1 + 2 * d * u 1 - (p 1 - a 1)]

/-! ### (A) The ambient `dist` on `Point` is the sup metric -/

/-- Route 1: unfold Mathlib's Pi metric (`dist_pi_def`, which is `rfl`) and compute the
`Finset.sup` over `univ = {0, 1}`. -/
theorem dist_point_eq_max (p q : Point) : dist p q = max |p 0 - q 0| |p 1 - q 1| := by
  rw [dist_pi_def, Finset.univ_fin2, Finset.sup_insert, Finset.sup_singleton]
  simp [Real.dist_eq]

/-- Route 2: `le_antisymm` with `dist_pi_le_iff` and `dist_le_pi_dist`. -/
theorem dist_point_eq_max' (p q : Point) : dist p q = max |p 0 - q 0| |p 1 - q 1| := by
  apply le_antisymm
  · refine (dist_pi_le_iff (le_max_of_le_left (abs_nonneg _))).2 fun i => ?_
    fin_cases i
    · simp [Real.dist_eq]
    · simp [Real.dist_eq]
  · refine max_le ?_ ?_
    · simpa [Real.dist_eq] using dist_le_pi_dist p q 0
    · simpa [Real.dist_eq] using dist_le_pi_dist p q 1

/-- Lean's `dist` from `(0,0)` to `(3,4)` is `4`. -/
theorem dist_0_34 : dist (![0, 0] : Point) ![3, 4] = 4 := by
  rw [dist_point_eq_max]
  norm_num

/-- The Euclidean squared distance is `25` (distance `5`). -/
theorem eDist2_0_34 : eDist2 ![0, 0] ![3, 4] = 25 := by
  norm_num [eDist2]

theorem dist_0_34_ne_5 : dist (![0, 0] : Point) ![3, 4] ≠ 5 := by
  rw [dist_0_34]; norm_num

/-! ### (B) Euclidean rotations by 2π/3 and 2π/5 are not Mathlib `Isometry`s of `Point` -/

/-- Any rotation whose angle has `sin θ ≠ 0` and `cos θ ≠ 0` fails to preserve the sup distance:
it fixes `c` and sends `c + e₀` (sup distance `1` from `c`) to `c + (cos θ, sin θ)`
(sup distance `max |cos θ| |sin θ| < 1`). -/
theorem not_isometry_rotAbout (c : Point) (θ : ℝ) (hs : Real.sin θ ≠ 0) (hc : Real.cos θ ≠ 0) :
    ¬ Isometry (rotAbout c θ) := by
  intro h
  have e0 : rotAbout c θ c 0 - rotAbout c θ ![c 0 + 1, c 1] 0 = -Real.cos θ := by
    simp only [rotAbout, Matrix.cons_val_zero, Matrix.cons_val_one]; ring
  have e1 : rotAbout c θ c 1 - rotAbout c θ ![c 0 + 1, c 1] 1 = -Real.sin θ := by
    simp only [rotAbout, Matrix.cons_val_zero, Matrix.cons_val_one]; ring
  have f0 : c 0 - (![c 0 + 1, c 1] : Point) 0 = -1 := by
    simp only [Matrix.cons_val_zero]; ring
  have f1 : c 1 - (![c 0 + 1, c 1] : Point) 1 = 0 := by
    simp only [Matrix.cons_val_zero, Matrix.cons_val_one]; ring
  have h1 := h.dist_eq c ![c 0 + 1, c 1]
  rw [dist_point_eq_max, dist_point_eq_max, e0, e1, f0, f1, abs_neg, abs_neg, abs_neg, abs_one,
    abs_zero, max_eq_left zero_le_one] at h1
  have hpy := Real.sin_sq_add_cos_sq θ
  have hs2 : 0 < Real.sin θ ^ 2 := lt_of_le_of_ne (sq_nonneg _) (Ne.symm (pow_ne_zero 2 hs))
  have hc2 : 0 < Real.cos θ ^ 2 := lt_of_le_of_ne (sq_nonneg _) (Ne.symm (pow_ne_zero 2 hc))
  have hca : |Real.cos θ| < 1 := (sq_lt_one_iff_abs_lt_one _).1 (by linarith)
  have hsa : |Real.sin θ| < 1 := (sq_lt_one_iff_abs_lt_one _).1 (by linarith)
  have hm : max |Real.cos θ| |Real.sin θ| < 1 := max_lt hca hsa
  linarith

theorem not_isometry_rot_threefold (c : Point) : ¬ Isometry (rotAbout c (2 * Real.pi / 3)) := by
  have hpi := Real.pi_pos
  apply not_isometry_rotAbout
  · exact (Real.sin_pos_of_pos_of_lt_pi (by positivity) (by linarith)).ne'
  · exact (Real.cos_neg_of_pi_div_two_lt_of_lt (by linarith) (by linarith)).ne

theorem not_isometry_rot_fivefold (c : Point) : ¬ Isometry (rotAbout c (2 * Real.pi / 5)) := by
  have hpi := Real.pi_pos
  apply not_isometry_rotAbout
  · exact (Real.sin_pos_of_pos_of_lt_pi (by positivity) (by linarith)).ne'
  · exact (Real.cos_pos_of_mem_Ioo ⟨by linarith, by linarith⟩).ne'

/-! ### (C) The same rotations do satisfy `IsEucIsometry` -/

theorem isEucIsometry_rotAbout (c : Point) (θ : ℝ) : IsEucIsometry (rotAbout c θ) := by
  intro p q
  simp only [eDist2, rotAbout, Matrix.cons_val_zero, Matrix.cons_val_one]
  have h := Real.sin_sq_add_cos_sq θ
  linear_combination ((p 0 - q 0) ^ 2 + (p 1 - q 1) ^ 2) * h

/-! ### (D) Controls: the half-turn and quarter-turn *are* sup isometries -/

theorem isometry_halfTurn (c : Point) : Isometry (halfTurn c) := by
  refine Isometry.of_dist_eq fun p q => ?_
  have e0 : halfTurn c p 0 - halfTurn c q 0 = -(p 0 - q 0) := by
    simp only [halfTurn, Matrix.cons_val_zero]; ring
  have e1 : halfTurn c p 1 - halfTurn c q 1 = -(p 1 - q 1) := by
    simp only [halfTurn, Matrix.cons_val_zero, Matrix.cons_val_one]; ring
  rw [dist_point_eq_max, dist_point_eq_max, e0, e1, abs_neg, abs_neg]

theorem isometry_rot_quarter (c : Point) : Isometry (rotAbout c (2 * Real.pi / 4)) := by
  have hθ : 2 * Real.pi / 4 = Real.pi / 2 := by ring
  refine Isometry.of_dist_eq fun p q => ?_
  have e0 : rotAbout c (2 * Real.pi / 4) p 0 - rotAbout c (2 * Real.pi / 4) q 0 = -(p 1 - q 1) := by
    simp only [rotAbout, hθ, Real.cos_pi_div_two, Real.sin_pi_div_two, Matrix.cons_val_zero]; ring
  have e1 : rotAbout c (2 * Real.pi / 4) p 1 - rotAbout c (2 * Real.pi / 4) q 1 = p 0 - q 0 := by
    simp only [rotAbout, hθ, Real.cos_pi_div_two, Real.sin_pi_div_two, Matrix.cons_val_zero,
      Matrix.cons_val_one]; ring
  rw [dist_point_eq_max, dist_point_eq_max, e0, e1, abs_neg, max_comm]

/-! ### (E) A mirror with a generic axis is not a sup isometry either -/

theorem unit_34 : (![3 / 5, 4 / 5] : Point) 0 ^ 2 + (![3 / 5, 4 / 5] : Point) 1 ^ 2 = 1 := by
  norm_num

theorem not_isometry_reflLine_34 : ¬ Isometry (reflLine 0 ![3 / 5, 4 / 5]) := by
  intro h
  have e0 : reflLine 0 ![3 / 5, 4 / 5] 0 0 - reflLine 0 ![3 / 5, 4 / 5] ![1, 0] 0 = 7 / 25 := by
    simp only [reflLine, Matrix.cons_val_zero, Matrix.cons_val_one,
      Pi.zero_apply]; norm_num
  have e1 : reflLine 0 ![3 / 5, 4 / 5] 0 1 - reflLine 0 ![3 / 5, 4 / 5] ![1, 0] 1 = -(24 / 25) := by
    simp only [reflLine, Matrix.cons_val_zero, Matrix.cons_val_one,
      Pi.zero_apply]; norm_num
  have h1 := h.dist_eq 0 ![1, 0]
  rw [dist_point_eq_max, dist_point_eq_max, e0, e1] at h1
  norm_num at h1

end SupMetricCheck

#print axioms SupMetricCheck.dist_point_eq_max
#print axioms SupMetricCheck.dist_point_eq_max'
#print axioms SupMetricCheck.dist_0_34
#print axioms SupMetricCheck.dist_0_34_ne_5
#print axioms SupMetricCheck.not_isometry_rot_threefold
#print axioms SupMetricCheck.not_isometry_rot_fivefold
#print axioms SupMetricCheck.isEucIsometry_rotAbout
#print axioms SupMetricCheck.isometry_halfTurn
#print axioms SupMetricCheck.isometry_rot_quarter
#print axioms SupMetricCheck.not_isometry_reflLine_34
