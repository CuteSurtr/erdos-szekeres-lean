import LeanLB.Geometry
import LeanLB.G.Five

/-!
# The row symmetries of the k = 7 sets that the k = 8 package did not need

* `mulZeta3`: rotation by 60° of an Eisenstein row `a + bω` (`ω = e^{2πi/3}`; `c6_30points.txt`):
  multiplication by `ζ = e^{iπ/3} = 1 + ω`, so `a + bω ↦ (a - b) + aω` (`rot_six_eis`).
* `rot90XY`: rotation by 90° of an integer row `(x, y)` (`c4_28points.txt`): `(x, y) ↦ (-y, x)`.
* `G.mulZ5`: rotation by 72° of a row `c0 c1 c2 c3` = `Σ c_j z^j`, `z = e^{2πi/5}` (`c5_31points.txt`):
  multiplication by `z`, written again in the basis `1, z, z², z³` with `1 + z + z² + z³ + z⁴ = 0`
  (`G.rot_cycPoint_mulZ5`, from the k = 8 package's `rot_cycPoint` and `cycPoint_five`).
-/

namespace LeanLB

open ErdosSzekeres Real

/-- Multiplication by `ζ = 1 + ω` of an Eisenstein row: `a + bω ↦ (a - b) + aω`. -/
def mulZeta3 (w : List ℤ) : List ℤ := [(lat3 w).1 - (lat3 w).2, (lat3 w).1]

theorem lat3_mulZeta3 (w : List ℤ) :
    lat3 (mulZeta3 w) = ((lat3 w).1 - (lat3 w).2, (lat3 w).1) := by
  simp [mulZeta3, lat3]

theorem rot_six_eis (q : ℤ × ℤ) :
    rotAbout 0 (2 * π / 6) (embedZ (1, 0) (-1 / 2, Real.sqrt 3 / 2) q) =
      embedZ (1, 0) (-1 / 2, Real.sqrt 3 / 2) (q.1 - q.2, q.1) := by
  have h : 2 * π / 6 = π / 3 := by ring
  rw [h]
  funext i
  fin_cases i <;> simp [rotAbout, embedZ, Real.cos_pi_div_three, Real.sin_pi_div_three]
  · linear_combination (-(q.2 : ℝ) / 4) * sqrt3_sq
  · ring

/-- Rotation by 90° of an integer row: `(x, y) ↦ (-y, x)`. -/
def rot90XY (w : List ℤ) : List ℤ := [-w.getD 1 0, w.getD 0 0]

theorem latXY_rot90XY (w : List ℤ) : latXY (rot90XY w) = (-(latXY w).2, (latXY w).1) := by
  simp [rot90XY, latXY]

end LeanLB

namespace LeanLB.G

open ErdosSzekeres Real

/-- Multiplication by `z = e^{2πi/5}` of `Σ_{j<5} w_j z^j`, in the basis `1, z, z², z³`:
`z · Σ w_j z^j = w₄ + w₀z + w₁z² + w₂z³ + w₃z⁴ = (w₄ - w₃) + (w₀ - w₃)z + (w₁ - w₃)z² + (w₂ - w₃)z³`. -/
def mulZ5 (w : List ℤ) : List ℤ :=
  [w.getD 4 0 - w.getD 3 0, w.getD 0 0 - w.getD 3 0, w.getD 1 0 - w.getD 3 0, w.getD 2 0 - w.getD 3 0]

theorem cycShift_five (w : List ℤ) :
    cycShift 5 w = [w.getD 4 0, w.getD 0 0, w.getD 1 0, w.getD 2 0, w.getD 3 0] := by
  simp [cycShift, List.range_succ]

theorem lat5_cycShift_five (w : List ℤ) : lat5 (cycShift 5 w) = lat5 (mulZ5 w) := by
  rw [cycShift_five]
  ext <;> simp [lat5, mulZ5] <;> ring

theorem rot_cycPoint_mulZ5 (w : List ℤ) :
    rotAbout 0 (2 * π / 5) (cycPoint 5 w) = cycPoint 5 (mulZ5 w) := by
  have h := rot_cycPoint 5 (by norm_num) w
  push_cast at h
  rw [h, cycPoint_five, cycPoint_five, lat5_cycShift_five]

end LeanLB.G
