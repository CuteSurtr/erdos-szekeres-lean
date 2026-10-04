import ErdosSzekeres.Suk.TriangleOrder
import Mathlib.LinearAlgebra.FiniteDimensional.Basic

namespace ErdosSzekeres.Suk

theorem baseLength_sq_pos (a b : Point) (hab : a ≠ b) :
    0 < (b 0 - a 0) ^ 2 + (b 1 - a 1) ^ 2 := by
  by_contra! h
  have hx : b 0 = a 0 := by nlinarith [sq_nonneg (b 1 - a 1)]
  have hy : b 1 = a 1 := by nlinarith [sq_nonneg (b 0 - a 0)]
  apply hab
  ext i
  fin_cases i <;> simp_all

noncomputable def baseLinearMap (a b : Point) : Point →ₗ[ℝ] Point where
  toFun x := ![(b 0 - a 0) * x 0 - (b 1 - a 1) * x 1,
    (b 1 - a 1) * x 0 + (b 0 - a 0) * x 1]
  map_add' x y := by ext i; fin_cases i <;> simp <;> ring
  map_smul' c x := by ext i; fin_cases i <;> simp <;> ring

theorem baseLinearMap_injective (a b : Point) (hab : a ≠ b) :
    Function.Injective (baseLinearMap a b) := by
  have hnorm : (b 0 - a 0) ^ 2 + (b 1 - a 1) ^ 2 ≠ 0 := by
    exact ne_of_gt (baseLength_sq_pos a b hab)
  intro x y h
  have h₀ := congrArg (fun p : Point => p 0) h
  have h₁ := congrArg (fun p : Point => p 1) h
  simp only [baseLinearMap, LinearMap.coe_mk, AddHom.coe_mk,
    Matrix.cons_val_zero, Matrix.cons_val_one] at h₀ h₁
  have hx : x 0 = y 0 := by
    apply mul_left_cancel₀ hnorm
    linear_combination (b 0 - a 0) * h₀ + (b 1 - a 1) * h₁
  have hy : x 1 = y 1 := by
    apply mul_left_cancel₀ hnorm
    linear_combination -(b 1 - a 1) * h₀ + (b 0 - a 0) * h₁
  ext i
  fin_cases i <;> assumption

/-- A concrete affine normalization exists for every nondegenerate base segment. -/
noncomputable def baseFrame (a b : Point) (hab : a ≠ b) : Point ≃ᵃ[ℝ] Point :=
  (LinearEquiv.ofInjectiveEndo (baseLinearMap a b) (baseLinearMap_injective a b hab)).toAffineEquiv.trans
    (AffineEquiv.constVAdd ℝ Point a)

@[simp] theorem baseFrame_zero (a b : Point) (hab : a ≠ b) :
    baseFrame a b hab ![0, 0] = a := by
  ext i
  fin_cases i <;> simp [baseFrame, baseLinearMap, vadd_eq_add]

@[simp] theorem baseFrame_one (a b : Point) (hab : a ≠ b) :
    baseFrame a b hab ![1, 0] = b := by
  ext i
  fin_cases i <;> simp [baseFrame, baseLinearMap, vadd_eq_add]

theorem orient_baseFrame (a b : Point) (hab : a ≠ b) (p q r : Point) :
    orient (baseFrame a b hab p) (baseFrame a b hab q) (baseFrame a b hab r) =
      ((b 0 - a 0) ^ 2 + (b 1 - a 1) ^ 2) * orient p q r := by
  simp [orient, baseFrame, baseLinearMap, vadd_eq_add]
  ring

theorem orient_baseFrame_base (a b : Point) (hab : a ≠ b) (p : Point) :
    orient a b (baseFrame a b hab p) =
      ((b 0 - a 0) ^ 2 + (b 1 - a 1) ^ 2) * p 1 := by
  have h := orient_baseFrame a b hab ![0, 0] ![1, 0] p
  simpa [orient] using h

theorem baseFrame_triangle (a b : Point) (hab : a ≠ b) (p q : UpperPoint) :
    p ≤ q ↔ baseFrame a b hab q.val ∈
      convexHull ℝ ({a, b, baseFrame a b hab p.val} : Set Point) := by
  rw [triangleOrder_iff]
  have h := (baseFrame a b hab).toAffineMap.image_convexHull
    ({![0, 0], ![1, 0], p.val} : Set Point)
  have hi : (baseFrame a b hab).toAffineMap ''
      ({![0, 0], ![1, 0], p.val} : Set Point) = {a, b, baseFrame a b hab p.val} := by
    simp only [Set.image_insert_eq, Set.image_singleton]
    change {baseFrame a b hab ![0, 0], baseFrame a b hab ![1, 0],
      baseFrame a b hab p.val} = _
    rw [baseFrame_zero, baseFrame_one]
  rw [hi] at h
  rw [← h]
  constructor
  · exact Set.mem_image_of_mem _
  · rintro ⟨x, hx, he⟩
    have he' : x = q.val := (baseFrame a b hab).injective he
    simpa [he'] using hx

end ErdosSzekeres.Suk
