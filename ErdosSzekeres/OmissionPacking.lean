import ErdosSzekeres.OmissionCertificates

namespace ErdosSzekeres.OmissionCertificates

open scoped BigOperators

/-- Pack a bounded coefficient vector into one natural number. -/
def pack {n : ℕ} (base : ℕ) (coefficient : Fin n → ℕ) : ℕ :=
  ∑ i, coefficient i * base ^ i.val

theorem pack_succ {n : ℕ} (base : ℕ) (coefficient : Fin (n + 1) → ℕ) :
    pack base coefficient = coefficient 0 + base * pack base (fun i => coefficient i.succ) := by
  simp only [pack, Fin.sum_univ_succ, Fin.val_zero, pow_zero, mul_one,
    Fin.val_succ, pow_succ, Finset.mul_sum]
  congr 1
  apply Finset.sum_congr rfl
  intro i _
  ring

/-- Equal packed numbers have equal digits when all coefficients are below the
base. This lets certificate checks aggregate sparse rows with big integers. -/
theorem pack_injective_of_lt {n base : ℕ} (hb : 1 < base)
    {f g : Fin n → ℕ} (hf : ∀ i, f i < base) (hg : ∀ i, g i < base)
    (heq : pack base f = pack base g) : f = g := by
  induction n with
  | zero => funext i; exact Fin.elim0 i
  | succ n ih =>
      rw [pack_succ, pack_succ] at heq
      have hzero : f 0 = g 0 := by
        have hm := congrArg (fun x => x % base) heq
        simpa [Nat.add_mod, Nat.mod_eq_of_lt (hf 0), Nat.mod_eq_of_lt (hg 0)] using hm
      have htail : pack base (fun i => f i.succ) = pack base (fun i => g i.succ) := by
        rw [hzero] at heq
        exact Nat.eq_of_mul_eq_mul_left (by omega) (Nat.add_left_cancel heq)
      have he := ih (fun i => hf i.succ) (fun i => hg i.succ) htail
      funext i
      refine Fin.cases hzero (fun j => ?_) i
      exact congrFun he j

/-- Sparse row encoding: a support contributes one base-power for each state. -/
def rowCode {n : ℕ} (base : ℕ) (support : Finset (Fin n)) : ℕ :=
  ∑ i ∈ support, base ^ i.val

theorem pack_load {n : ℕ} {ρ : Type*} [Fintype ρ] (base : ℕ)
    (support : ρ → Finset (Fin n)) (weight : ρ → ℕ) :
    pack base (load support weight) = ∑ r, weight r * rowCode base (support r) := by
  classical
  simp only [pack, load, rowCode, Finset.sum_mul, Finset.mul_sum, ite_mul, zero_mul]
  rw [Finset.sum_comm]
  congr 1
  funext r
  simp

/-- A packed equality and a no-carry bound certify all column loads at once. -/
theorem load_eq_of_packed {n base : ℕ} {ρ : Type*} [Fintype ρ]
    (support : ρ → Finset (Fin n)) (weight : ρ → ℕ) (coefficients : Fin n → ℕ)
    (hb : 1 < base) (hw : (∑ r, weight r) < base)
    (hc : ∀ i, coefficients i < base)
    (heq : pack base coefficients = ∑ r, weight r * rowCode base (support r)) :
    coefficients = load support weight := by
  apply pack_injective_of_lt hb hc
  · intro i
    apply lt_of_le_of_lt ?_ hw
    unfold load
    apply Finset.sum_le_sum
    intro r _
    split_ifs <;> omega
  · rwa [pack_load]

end ErdosSzekeres.OmissionCertificates
