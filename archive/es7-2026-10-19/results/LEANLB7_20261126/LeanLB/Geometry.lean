import LeanLB.Statement
import LeanLB.Bridge
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.LinearCombination

/-!
# Lattice coordinates of the point sets

* `embedZ A B q = q.1 • A + q.2 • B` and `embed A B s n = embedZ A B (n - s)`; the latter multiplies
  orientation determinants by `A.1 * B.2 - A.2 * B.1` (`embed_scaling`).
* `cycPoint m w = embedZ A B (lat w)` for `m = 3, 4, 6` (`cycPoint_four`, `cycPoint_six`,
  `cycPoint_three`), and `intPoint w = embedZ (1,0) (0,1) (latXY w)`.
* The rotations (and the reflection) act on lattice coordinates by integer matrices.
-/

namespace LeanLB

open ErdosSzekeres Real

/-- `q.1 • A + q.2 • B`. -/
noncomputable def embedZ (A B : ℝ × ℝ) (q : ℤ × ℤ) : Point :=
  ![(q.1 : ℝ) * A.1 + (q.2 : ℝ) * B.1, (q.1 : ℝ) * A.2 + (q.2 : ℝ) * B.2]

/-- Undo the translation of the checker's coordinates. -/
def unshift (s : ℤ × ℤ) (n : NP) : ℤ × ℤ := ((n.1 : ℤ) - s.1, (n.2 : ℤ) - s.2)

/-- The map from the checker's coordinates to the plane. -/
noncomputable def embed (A B : ℝ × ℝ) (s : ℤ × ℤ) (n : NP) : Point := embedZ A B (unshift s n)

theorem embed_scaling (A B : ℝ × ℝ) (s : ℤ × ℤ) (h : 0 < A.1 * B.2 - A.2 * B.1) :
    OrientScaling (embed A B s) (A.1 * B.2 - A.2 * B.1) := by
  refine ⟨h, fun a b c => ?_⟩
  simp only [orient, embed, embedZ, unshift, oz, Matrix.cons_val_zero, Matrix.cons_val_one]
  push_cast
  ring

/-! ## Lattice coordinates of the rows -/

/-- `Σ w_j i^j = (w₀ - w₂) + (w₁ - w₃) i`. -/
def lat4 (w : List ℤ) : ℤ × ℤ := (w.getD 0 0 - w.getD 2 0, w.getD 1 0 - w.getD 3 0)

/-- `Σ w_j ζ^j = a + bζ` for `ζ = e^{iπ/3}` (`ζ² = ζ - 1`). -/
def lat6 (w : List ℤ) : ℤ × ℤ :=
  (w.getD 0 0 - w.getD 2 0 - w.getD 3 0 + w.getD 5 0, w.getD 1 0 + w.getD 2 0 - w.getD 4 0 - w.getD 5 0)

/-- `Σ w_j ω^j = a + bω` for `ω = e^{2πi/3}` (`ω² = -1 - ω`). -/
def lat3 (w : List ℤ) : ℤ × ℤ := (w.getD 0 0 - w.getD 2 0, w.getD 1 0 - w.getD 2 0)

/-- A row `x y`. -/
def latXY (w : List ℤ) : ℤ × ℤ := (w.getD 0 0, w.getD 1 0)

theorem sqrt3_sq : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)

theorem pi_mul_div (j m : ℕ) : 2 * π * (j : ℝ) / (m : ℝ) = 2 * π * j / m := rfl

theorem cycPoint_four (w : List ℤ) : cycPoint 4 w = embedZ (1, 0) (0, 1) (lat4 w) := by
  have h1 : 2 * π * ((1 : ℕ) : ℝ) / ((4 : ℕ) : ℝ) = π / 2 := by push_cast; ring
  have h2 : 2 * π * ((2 : ℕ) : ℝ) / ((4 : ℕ) : ℝ) = π := by push_cast; ring
  have h3 : 2 * π * ((3 : ℕ) : ℝ) / ((4 : ℕ) : ℝ) = π / 2 + π := by push_cast; ring
  simp only [cycPoint, unitRoot, Finset.sum_range_succ, Finset.sum_range_zero, zero_add]
  rw [h1, h2, h3]
  simp only [Nat.cast_zero, mul_zero, zero_div, Real.cos_zero, Real.sin_zero, Real.cos_pi_div_two,
    Real.sin_pi_div_two, Real.cos_pi, Real.sin_pi, Real.cos_add_pi, Real.sin_add_pi]
  funext i
  fin_cases i <;> simp [embedZ, lat4] <;> ring

theorem cycPoint_six (w : List ℤ) :
    cycPoint 6 w = embedZ (1, 0) (1 / 2, Real.sqrt 3 / 2) (lat6 w) := by
  have h1 : 2 * π * ((1 : ℕ) : ℝ) / ((6 : ℕ) : ℝ) = π / 3 := by push_cast; ring
  have h2 : 2 * π * ((2 : ℕ) : ℝ) / ((6 : ℕ) : ℝ) = π - π / 3 := by push_cast; ring
  have h3 : 2 * π * ((3 : ℕ) : ℝ) / ((6 : ℕ) : ℝ) = π := by push_cast; ring
  have h4 : 2 * π * ((4 : ℕ) : ℝ) / ((6 : ℕ) : ℝ) = π / 3 + π := by push_cast; ring
  have h5 : 2 * π * ((5 : ℕ) : ℝ) / ((6 : ℕ) : ℝ) = (π - π / 3) + π := by push_cast; ring
  simp only [cycPoint, unitRoot, Finset.sum_range_succ, Finset.sum_range_zero, zero_add]
  rw [h1, h2, h3, h4, h5]
  simp only [Nat.cast_zero, mul_zero, zero_div, Real.cos_zero, Real.sin_zero, Real.cos_pi_div_three,
    Real.sin_pi_div_three, Real.cos_pi, Real.sin_pi, Real.cos_add_pi, Real.sin_add_pi,
    Real.cos_pi_sub, Real.sin_pi_sub]
  funext i
  fin_cases i <;> simp [embedZ, lat6] <;> ring

theorem cycPoint_three (w : List ℤ) :
    cycPoint 3 w = embedZ (1, 0) (-1 / 2, Real.sqrt 3 / 2) (lat3 w) := by
  have h1 : 2 * π * ((1 : ℕ) : ℝ) / ((3 : ℕ) : ℝ) = π - π / 3 := by push_cast; ring
  have h2 : 2 * π * ((2 : ℕ) : ℝ) / ((3 : ℕ) : ℝ) = π / 3 + π := by push_cast; ring
  simp only [cycPoint, unitRoot, Finset.sum_range_succ, Finset.sum_range_zero, zero_add]
  rw [h1, h2]
  simp only [Nat.cast_zero, mul_zero, zero_div, Real.cos_zero, Real.sin_zero, Real.cos_pi_div_three,
    Real.sin_pi_div_three, Real.cos_add_pi, Real.sin_add_pi, Real.cos_pi_sub, Real.sin_pi_sub]
  funext i
  fin_cases i <;> simp [embedZ, lat3] <;> ring

theorem intPoint_eq (w : List ℤ) : intPoint w = embedZ (1, 0) (0, 1) (latXY w) := by
  funext i
  fin_cases i <;> simp [intPoint, embedZ, latXY]

/-! ## Symmetries in lattice coordinates -/

theorem rot_four (q : ℤ × ℤ) :
    rotAbout 0 (2 * π / 4) (embedZ (1, 0) (0, 1) q) = embedZ (1, 0) (0, 1) (-q.2, q.1) := by
  have h : 2 * π / 4 = π / 2 := by ring
  rw [h]
  funext i
  fin_cases i <;> simp [rotAbout, embedZ, Real.cos_pi_div_two, Real.sin_pi_div_two]

theorem rot_six (q : ℤ × ℤ) :
    rotAbout 0 (2 * π / 6) (embedZ (1, 0) (1 / 2, Real.sqrt 3 / 2) q) =
      embedZ (1, 0) (1 / 2, Real.sqrt 3 / 2) (-q.2, q.1 + q.2) := by
  have h : 2 * π / 6 = π / 3 := by ring
  rw [h]
  funext i
  fin_cases i <;> simp [rotAbout, embedZ, Real.cos_pi_div_three, Real.sin_pi_div_three]
  · linear_combination (-(q.2 : ℝ) / 4) * sqrt3_sq
  · ring

theorem rot_three (q : ℤ × ℤ) :
    rotAbout 0 (2 * π / 3) (embedZ (1, 0) (-1 / 2, Real.sqrt 3 / 2) q) =
      embedZ (1, 0) (-1 / 2, Real.sqrt 3 / 2) (-q.2, q.1 - q.2) := by
  have h : 2 * π / 3 = π - π / 3 := by ring
  rw [h]
  funext i
  fin_cases i <;> simp [rotAbout, embedZ, Real.cos_pi_div_three, Real.sin_pi_div_three,
    Real.cos_pi_sub, Real.sin_pi_sub]
  · linear_combination (-(q.2 : ℝ) / 4) * sqrt3_sq
  · ring

theorem rot_two (q : ℤ × ℤ) :
    rotAbout 0 (2 * π / 2) (embedZ (1, 0) (0, 1) q) = embedZ (1, 0) (0, 1) (-q.1, -q.2) := by
  have h : 2 * π / 2 = π := by ring
  rw [h]
  funext i
  fin_cases i <;> simp [rotAbout, embedZ]

theorem refl_x (q : ℤ × ℤ) :
    lineRefl 1 0 0 (embedZ (1, 0) (0, 1) q) = embedZ (1, 0) (0, 1) (-q.1, q.2) := by
  funext i
  fin_cases i <;> simp [lineRefl, embedZ] <;> ring

/-! ## Generic assembly lemmas -/

theorem map_eq_of_link {P : List ℤ → Point} {lat : List ℤ → ℤ × ℤ} {E : ℤ × ℤ → Point}
    {φ : NP → Point} {g : NP → ℤ × ℤ} (rows : List (List ℤ)) (N : List NP)
    (hP : ∀ w, P w = E (lat w)) (hφ : ∀ n, φ n = E (g n)) (h : rows.map lat = N.map g) :
    rows.map P = N.map φ := by
  have e1 : rows.map P = (rows.map lat).map E := by
    rw [List.map_map]; exact List.map_congr_left (fun w _ => hP w)
  have e2 : N.map φ = (N.map g).map E := by
    rw [List.map_map]; exact List.map_congr_left (fun n _ => hφ n)
  rw [e1, e2, h]

theorem invariant_of_rows {f : Point → Point} {P : List ℤ → Point} {R : List ℤ → List ℤ}
    (rows : List (List ℤ)) (hR : ∀ w, f (P w) = P (R w)) (hmem : ∀ w ∈ rows, R w ∈ rows) :
    Invariant f (rows.map P).toFinset := by
  classical
  intro p hp
  rw [List.mem_toFinset, List.mem_map] at hp
  obtain ⟨w, hw, rfl⟩ := hp
  rw [hR, List.mem_toFinset]
  exact List.mem_map_of_mem (hmem w hw)

/-! ## The symmetries on rows -/

/-- Cyclic shift of a `.pts` row of length 6: multiplication by `ζ`. -/
def shift6 (w : List ℤ) : List ℤ :=
  [w.getD 5 0, w.getD 0 0, w.getD 1 0, w.getD 2 0, w.getD 3 0, w.getD 4 0]

/-- Cyclic shift of a `.pts` row of length 4: multiplication by `i`. -/
def shift4 (w : List ℤ) : List ℤ := [w.getD 3 0, w.getD 0 0, w.getD 1 0, w.getD 2 0]

/-- Multiplication by `ω` of a row `a b` (`a + bω ↦ -b + (a - b)ω`). -/
def mulOmega (w : List ℤ) : List ℤ := [-(lat3 w).2, (lat3 w).1 - (lat3 w).2]

/-- Half-turn of a row `x y`. -/
def negXY (w : List ℤ) : List ℤ := [-w.getD 0 0, -w.getD 1 0]

/-- Reflection of a row `x y` in the line `x = 0`. -/
def reflXY (w : List ℤ) : List ℤ := [-w.getD 0 0, w.getD 1 0]

theorem lat6_shift6 (w : List ℤ) : lat6 (shift6 w) = (-(lat6 w).2, (lat6 w).1 + (lat6 w).2) := by
  ext <;> simp [lat6, shift6] <;> ring

theorem lat4_shift4 (w : List ℤ) : lat4 (shift4 w) = (-(lat4 w).2, (lat4 w).1) := by
  ext <;> simp [lat4, shift4]

theorem lat3_mulOmega (w : List ℤ) :
    lat3 (mulOmega w) = (-(lat3 w).2, (lat3 w).1 - (lat3 w).2) := by
  simp [lat3, mulOmega]

theorem latXY_negXY (w : List ℤ) : latXY (negXY w) = (-(latXY w).1, -(latXY w).2) := by
  simp [latXY, negXY]

theorem latXY_reflXY (w : List ℤ) : latXY (reflXY w) = (-(latXY w).1, (latXY w).2) := by
  simp [latXY, reflXY]

end LeanLB
