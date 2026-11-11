import LeanLB.Geometry

/-!
# Rotation of `cycPoint` by `2π/m`: a cyclic shift of the coefficients

`rot_cycPoint`: `rotAbout 0 (2π/m) (Σ_j w_j ζ^j) = Σ_j (cycShift m w)_j ζ^j`, where
`cycShift m w = [w_{m-1}, w_0, …, w_{m-2}]`.
-/

namespace LeanLB

open ErdosSzekeres Real

/-- The cyclic shift `[w_{m-1}, w_0, …, w_{m-2}]` of the first `m` coefficients (multiplication by
`ζ_m`). -/
def cycShift (m : ℕ) (w : List ℤ) : List ℤ :=
  (List.range m).map (fun j => w.getD ((j + m - 1) % m) 0)

theorem cycShift_getD (m : ℕ) (w : List ℤ) {j : ℕ} (hj : j < m) :
    (cycShift m w).getD j 0 = w.getD ((j + m - 1) % m) 0 := by
  unfold cycShift
  rw [List.getD_eq_getElem?_getD, List.getElem?_map, List.getElem?_range hj]
  rfl

/-- `rotAbout 0 θ` as a linear map. -/
noncomputable def rotLin (θ : ℝ) : Point →ₗ[ℝ] Point where
  toFun := rotAbout 0 θ
  map_add' p q := by
    funext i; fin_cases i <;> simp [rotAbout] <;> ring
  map_smul' c p := by
    funext i; fin_cases i <;> simp [rotAbout] <;> ring

theorem rot_unitRoot (m j : ℕ) :
    rotAbout 0 (2 * π / m) (unitRoot m j) = unitRoot m (j + 1) := by
  have h : 2 * π * ((j + 1 : ℕ) : ℝ) / (m : ℝ) = 2 * π / m + 2 * π * j / m := by push_cast; ring
  funext i
  fin_cases i <;> simp only [rotAbout, unitRoot, h, Real.cos_add, Real.sin_add] <;> simp

theorem unitRoot_self (m : ℕ) (hm : 0 < m) : unitRoot m m = unitRoot m 0 := by
  have h : 2 * π * (m : ℝ) / (m : ℝ) = 2 * π := by
    field_simp
  unfold unitRoot
  rw [h]
  simp

theorem rot_cycPoint (m : ℕ) (hm : 0 < m) (w : List ℤ) :
    rotAbout 0 (2 * π / m) (cycPoint m w) = cycPoint m (cycShift m w) := by
  obtain ⟨n, rfl⟩ : ∃ n, m = n + 1 := ⟨m - 1, by omega⟩
  have hlin : rotAbout 0 (2 * π / ((n + 1 : ℕ) : ℝ)) (cycPoint (n + 1) w) =
      ∑ j ∈ Finset.range (n + 1), ((w.getD j 0 : ℤ) : ℝ) • unitRoot (n + 1) (j + 1) := by
    have e1 : rotAbout 0 (2 * π / ((n + 1 : ℕ) : ℝ)) (cycPoint (n + 1) w) =
        rotLin (2 * π / ((n + 1 : ℕ) : ℝ)) (cycPoint (n + 1) w) := rfl
    rw [e1, cycPoint, map_sum]
    refine Finset.sum_congr rfl (fun j _ => ?_)
    rw [map_smul]
    exact congrArg _ (rot_unitRoot (n + 1) j)
  rw [hlin, cycPoint, Finset.sum_range_succ, Finset.sum_range_succ', unitRoot_self (n + 1) hm]
  rw [cycShift_getD _ _ (by omega : 0 < n + 1)]
  have hsum : ∀ j ∈ Finset.range n,
      ((w.getD j 0 : ℤ) : ℝ) • unitRoot (n + 1) (j + 1) =
      (((cycShift (n + 1) w).getD (j + 1) 0 : ℤ) : ℝ) • unitRoot (n + 1) (j + 1) := by
    intro j hj
    rw [Finset.mem_range] at hj
    rw [cycShift_getD _ _ (by omega : j + 1 < n + 1)]
    congr 3
    rw [show j + 1 + (n + 1) - 1 = j + (n + 1) by omega, Nat.add_mod_right, Nat.mod_eq_of_lt (by omega)]
  rw [Finset.sum_congr rfl hsum]
  congr 3
  rw [show 0 + (n + 1) - 1 = n by omega, Nat.mod_eq_of_lt (by omega)]

end LeanLB
