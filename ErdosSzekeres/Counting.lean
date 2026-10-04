import Mathlib.Data.Nat.Choose.Vandermonde
import Mathlib.Data.Nat.Choose.Bounds
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.Real.Sqrt
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

/-!
Arithmetic tools for investigating the counting step of the HMPT bound.
These are unconditional arithmetic lemmas, not a formalization of the geometric
HMPT reduction. In particular, none asserts a new bound on `ForcesConvexNGon`.
-/
namespace ErdosSzekeres.Counting

open scoped BigOperators

/-- One term in Vandermonde's sum. -/
theorem choose_mul_le (a b r s : ℕ) :
    a.choose r * b.choose s ≤ (a + b).choose (r + s) := by
  rw [Nat.add_choose_eq]
  exact Finset.single_le_sum (f := fun ij : ℕ × ℕ => a.choose ij.1 * b.choose ij.2)
    (a := (r, s)) (fun _ _ => Nat.zero_le _) (by simp)

/-- Retain the binomial budget across all parts instead of bounding each by a power. -/
theorem prod_choose_le {ι : Type*} (t : Finset ι) (a b : ι → ℕ) :
    (∏ i ∈ t, (a i).choose (b i)) ≤ (∑ i ∈ t, a i).choose (∑ i ∈ t, b i) := by
  classical
  induction t using Finset.induction_on with
  | empty => simp
  | @insert i t hi ih =>
      simp only [Finset.prod_insert hi, Finset.sum_insert hi]
      exact (Nat.mul_le_mul_left _ ih).trans (choose_mul_le _ _ _ _)

/-- Increasing the selected budget while keeping its complement fixed. -/
theorem choose_add_mono {a b : ℕ} (d : ℕ) (h : a ≤ b) :
    (a + d).choose a ≤ (b + d).choose b := by
  rw [Nat.choose_symm_add, Nat.choose_symm_add (a := b)]
  exact Nat.choose_le_choose d (Nat.add_le_add_right h d)

/-- Abstract horizontal-chain budget: `m i` represents `cᵢ - 1`, `d` bounds `dᵢ - 1`.
The geometric interpretation and its hypotheses remain separate proof obligations. -/
theorem horizontal_product_le {ι : Type*} (t : Finset ι) (m : ι → ℕ)
    (d M : ℕ) (hbudget : ∑ i ∈ t, m i ≤ M) :
    (∏ i ∈ t, (m i + d).choose (m i)) ≤ (M + t.card * d).choose M := by
  have h := prod_choose_le t (fun i => m i + d) m
  simp only [Finset.sum_add_distrib, Finset.sum_const, smul_eq_mul] at h
  exact h.trans (choose_add_mono _ hbudget)

/-- Compose extraction and chain-counting estimates. The assumptions must be
proved from geometry before this can yield a bound on convex polygons. -/
theorem combine_budgets {ι : Type*} (t : Finset ι) (sizes m : ι → ℕ)
    (N k E V d M : ℕ)
    (hextract : N ^ k ≤ 2 ^ E * ∏ i ∈ t, sizes i)
    (hparts : (∏ i ∈ t, sizes i) ≤ 2 ^ V * ∏ i ∈ t, (m i + d).choose (m i))
    (hbudget : ∑ i ∈ t, m i ≤ M) :
    N ^ k ≤ 2 ^ (E + V) * (M + t.card * d).choose M := by
  calc
    N ^ k ≤ 2 ^ E * ∏ i ∈ t, sizes i := hextract
    _ ≤ 2 ^ E * (2 ^ V * ∏ i ∈ t, (m i + d).choose (m i)) :=
      Nat.mul_le_mul_left _ hparts
    _ ≤ 2 ^ E * (2 ^ V * (M + t.card * d).choose M) :=
      Nat.mul_le_mul_left _ (Nat.mul_le_mul_left _ (horizontal_product_le t m d M hbudget))
    _ = 2 ^ (E + V) * (M + t.card * d).choose M := by rw [pow_add, mul_assoc]

/-- An algebraic limit on optimizing a fixed two-term penalty. It is not a lower
bound on the Erdős–Szekeres number, nor a barrier to other geometric arguments. -/
theorem penalty_ge {A B k : ℝ} (hA : 0 ≤ A) (hB : 0 ≤ B) (hk : 0 < k) :
    2 * Real.sqrt (A * B) ≤ A * k + B / k := by
  have hs := Real.sq_sqrt (mul_nonneg hA hB)
  have hsq := sq_nonneg (A * k - Real.sqrt (A * B))
  by_cases hzero : A = 0
  · subst A
    simp only [zero_mul, Real.sqrt_zero, mul_zero, zero_add]
    exact div_nonneg hB hk.le
  · have hpos : 0 < A := lt_of_le_of_ne hA (Ne.symm hzero)
    apply (le_of_mul_le_mul_left (a := A * k) ?_ (mul_pos hpos hk))
    field_simp
    nlinarith

end ErdosSzekeres.Counting
