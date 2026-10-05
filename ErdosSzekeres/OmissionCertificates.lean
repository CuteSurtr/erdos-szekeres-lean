import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic

namespace ErdosSzekeres.OmissionCertificates

open scoped BigOperators

/-- Total integer weight of the omission rows containing a state. -/
def load {ι ρ : Type*} [Fintype ρ] [DecidableEq ι]
    (support : ρ → Finset ι) (weight : ρ → ℕ) (i : ι) : ℕ :=
  ∑ r, if i ∈ support r then weight r else 0

/-- An exact weighted certificate bounds every Boolean hole assignment.
The excess term pays for states whose total row weight exceeds the capacity.
This is purely finite arithmetic; geometric necessity of the rows is separate. -/
theorem weighted_capacity_bound {ι ρ : Type*} [Fintype ι] [Fintype ρ]
    [DecidableEq ι] (support : ρ → Finset ι) (demand weight : ρ → ℕ)
    (holes : ι → ℕ) (capacity : ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r, demand r ≤ ∑ i ∈ support r, holes i) :
    ∑ r, weight r * demand r ≤
      capacity * (∑ i, holes i) + ∑ i, (load support weight i - capacity) := by
  classical
  have transpose : (∑ r, weight r * ∑ i ∈ support r, holes i) =
      ∑ i, load support weight i * holes i := by
    simp only [load, Finset.sum_mul, Finset.mul_sum, ite_mul, zero_mul]
    rw [Finset.sum_comm]
    congr 1
    funext r
    simp
  calc
    ∑ r, weight r * demand r ≤ ∑ r, weight r * ∑ i ∈ support r, holes i :=
      Finset.sum_le_sum fun r _ => Nat.mul_le_mul_left _ (hrows r)
    _ = ∑ i, load support weight i * holes i := transpose
    _ ≤ ∑ i, (capacity * holes i + (load support weight i - capacity)) := by
      apply Finset.sum_le_sum
      intro i _
      have hi := hbool i
      have hz : holes i = 0 ∨ holes i = 1 := by omega
      rcases hz with hz | hz <;> simp only [hz, mul_zero, mul_one]
      · exact Nat.zero_le _
      · omega
    _ = capacity * (∑ i, holes i) + ∑ i, (load support weight i - capacity) := by
      rw [Finset.sum_add_distrib, Finset.mul_sum]

/-- A strict integer margin excludes every assignment within a hole budget. -/
theorem excludes_budget {ι ρ : Type*} [Fintype ι] [Fintype ρ] [DecidableEq ι]
    (support : ρ → Finset ι) (demand weight : ρ → ℕ) (capacity budget : ℕ)
    (hmargin : capacity * budget + ∑ i, (load support weight i - capacity) <
      ∑ r, weight r * demand r) :
    ¬ ∃ holes : ι → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧ (∑ i, holes i) ≤ budget := by
  rintro ⟨holes, hbool, hrows, hbudget⟩
  have h := weighted_capacity_bound support demand weight holes capacity hbool hrows
  have hb := Nat.mul_le_mul_left capacity hbudget
  omega

/-- Splitting a hole assignment into fixed missing states and the unassigned
states preserves every row sum exactly. -/
theorem sum_after_fixing {ι : Type*} [DecidableEq ι]
    (s missing occupied : Finset ι) (holes : ι → ℕ)
    (hm : ∀ i ∈ missing, holes i = 1) (hz : ∀ i ∈ occupied, holes i = 0) :
    ∑ i ∈ s, holes i = (s ∩ missing).card +
      ∑ i ∈ s \ (missing ∪ occupied), holes i := by
  classical
  calc
    ∑ i ∈ s, holes i = ∑ i ∈ s,
        ((if i ∈ missing then 1 else 0) +
          (if i ∈ missing ∪ occupied then 0 else holes i)) := by
      apply Finset.sum_congr rfl
      intro i _
      by_cases him : i ∈ missing
      · simp [him, hm i him]
      · by_cases hiz : i ∈ occupied
        · simp [him, hiz, hz i hiz]
        · simp [him, hiz]
    _ = (s ∩ missing).card + ∑ i ∈ s \ (missing ∪ occupied), holes i := by
      rw [Finset.sum_add_distrib, Finset.sum_boole, Finset.filter_mem_eq_inter,
        Finset.sum_ite]
      simp only [Nat.cast_id, Finset.sum_const_zero, zero_add,
        Finset.filter_notMem_eq_sdiff]

/-- The exact weighted test remains sound at a branch with fixed zero and one
values. Natural subtraction clips each residual row demand at zero, matching
the integer tree checker. -/
theorem conditioned_excludes_budget {ι ρ : Type*} [Fintype ι] [Fintype ρ]
    [DecidableEq ι] (support : ρ → Finset ι) (demand weight : ρ → ℕ)
    (missing occupied : Finset ι) (capacity budget : ℕ)
    (hmargin : capacity * (budget - missing.card) +
        ∑ i, (load (fun r => support r \ (missing ∪ occupied)) weight i - capacity) <
        ∑ r, weight r * (demand r - (support r ∩ missing).card)) :
    ¬ ∃ holes : ι → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ budget ∧
      (∀ i ∈ missing, holes i = 1) ∧ (∀ i ∈ occupied, holes i = 0) := by
  classical
  rintro ⟨holes, hbool, hrows, hbudget, hm, hz⟩
  let remaining : ι → ℕ := fun i => if i ∈ missing ∪ occupied then 0 else holes i
  have sum_remaining (s : Finset ι) :
      ∑ i ∈ s, remaining i = ∑ i ∈ s \ (missing ∪ occupied), holes i := by
    dsimp only [remaining]
    rw [Finset.sum_ite]
    simp only [Finset.sum_const_zero, zero_add, Finset.filter_notMem_eq_sdiff]
  apply excludes_budget (fun r => support r \ (missing ∪ occupied))
    (fun r => demand r - (support r ∩ missing).card) weight capacity
    (budget - missing.card) hmargin
  refine ⟨remaining, ?_, ?_, ?_⟩
  · intro i
    have hi := hbool i
    dsimp [remaining]
    split_ifs <;> omega
  · intro r
    have hr := hrows r
    rw [sum_after_fixing (support r) missing occupied holes hm hz] at hr
    rw [sum_remaining]
    have hd : (support r \ (missing ∪ occupied)) \ (missing ∪ occupied) =
        support r \ (missing ∪ occupied) := by ext i; simp
    rw [hd]
    omega
  · have ht := sum_after_fixing Finset.univ missing occupied holes hm hz
    rw [Finset.univ_inter] at ht
    rw [sum_remaining]
    omega

/-- A finite proof tree. The two children of a split cover both Boolean values.
There are no pending or oracle constructors. -/
inductive CertificateTree (ι ρ : Type*) where
  | overBudget
  | weighted (capacity : ℕ) (weight : ρ → ℕ)
  | split (i : ι) (zero one : CertificateTree ι ρ)

/-- Computable integer checks for a proof tree under a partial assignment. -/
def CertificateTree.check {ι ρ : Type*} [Fintype ι] [Fintype ρ] [DecidableEq ι]
    (support : ρ → Finset ι) (demand : ρ → ℕ) (budget : ℕ)
    (missing occupied : Finset ι) : CertificateTree ι ρ → Bool
  | .overBudget => decide (budget < missing.card)
  | .weighted capacity weight => decide (
      capacity * (budget - missing.card) +
        ∑ i, (load (fun r => support r \ (missing ∪ occupied)) weight i - capacity) <
        ∑ r, weight r * (demand r - (support r ∩ missing).card))
  | .split i zero one =>
      zero.check support demand budget missing (insert i occupied) &&
      one.check support demand budget (insert i missing) occupied

/-- Soundness of the recursive arithmetic checker, including branch coverage. -/
theorem CertificateTree.check_sound {ι ρ : Type*} [Fintype ι] [Fintype ρ]
    [DecidableEq ι] (tree : CertificateTree ι ρ)
    (support : ρ → Finset ι) (demand : ρ → ℕ) (budget : ℕ)
    (missing occupied : Finset ι)
    (hcheck : tree.check support demand budget missing occupied = true) :
    ¬ ∃ holes : ι → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ budget ∧
      (∀ i ∈ missing, holes i = 1) ∧ (∀ i ∈ occupied, holes i = 0) := by
  classical
  induction tree generalizing missing occupied with
  | overBudget =>
      simp only [check, decide_eq_true_eq] at hcheck
      rintro ⟨holes, _, _, hb, hm, hz⟩
      have ht := sum_after_fixing Finset.univ missing occupied holes hm hz
      rw [Finset.univ_inter] at ht
      omega
  | weighted capacity weight =>
      simp only [check, decide_eq_true_eq] at hcheck
      exact conditioned_excludes_budget support demand weight missing occupied capacity budget hcheck
  | split i zero one ihzero ihone =>
      simp only [check, Bool.and_eq_true] at hcheck
      rintro ⟨holes, hbool, hrows, hb, hm, hz⟩
      have hi := hbool i
      have cases : holes i = 0 ∨ holes i = 1 := by omega
      rcases cases with hzero | hone
      · apply ihzero missing (insert i occupied) hcheck.1
        refine ⟨holes, hbool, hrows, hb, hm, ?_⟩
        intro j hj
        rcases Finset.mem_insert.mp hj with rfl | hj
        · exact hzero
        · exact hz j hj
      · apply ihone (insert i missing) occupied hcheck.2
        refine ⟨holes, hbool, hrows, hb, ?_, hz⟩
        intro j hj
        rcases Finset.mem_insert.mp hj with rfl | hj
        · exact hone
        · exact hm j hj

/-- A tree checked at the empty assignment excludes the original hole budget. -/
theorem CertificateTree.excludes_of_check {ι ρ : Type*} [Fintype ι] [Fintype ρ]
    [DecidableEq ι] (tree : CertificateTree ι ρ)
    (support : ρ → Finset ι) (demand : ρ → ℕ) (budget : ℕ)
    (hcheck : tree.check support demand budget ∅ ∅ = true) :
    ¬ ∃ holes : ι → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧ (∑ i, holes i) ≤ budget := by
  rintro ⟨holes, hbool, hrows, hb⟩
  exact tree.check_sound support demand budget ∅ ∅ hcheck
    ⟨holes, hbool, hrows, hb, by simp, by simp⟩

/-- A small kernel-checked control: hitting every edge of a triangle needs
at least two holes. Its certificate uses all three rows with unit weights. -/
theorem triangle_excludes_one :
    ¬ ∃ holes : Fin 3 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r : Fin 3, 1 ≤ ∑ i ∈ Finset.univ.erase r, holes i) ∧
      (∑ i, holes i) ≤ 1 := by
  apply (CertificateTree.weighted 2 (fun _ : Fin 3 => 1)).excludes_of_check
    (fun r : Fin 3 => Finset.univ.erase r) (fun _ => 1) 1
  decide +kernel

end ErdosSzekeres.OmissionCertificates
