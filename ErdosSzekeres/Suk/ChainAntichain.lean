import ErdosSzekeres.Vendor.DilworthTheorem
import Mathlib.Algebra.Order.BigOperators.Group.Finset

namespace ErdosSzekeres.Suk
open scoped BigOperators

/-- Integer form of the chain/antichain alternative used in Suk's proof.
The relation is any partial order; its geometric construction is separate. -/
theorem chain_or_antichain {α : Type*} [PartialOrder α] (s : Finset α)
    (a b : ℕ) (ha : 1 ≤ a) (hb : 1 ≤ b)
    (hsize : (a - 1) * (b - 1) < s.card) :
    (∃ c ⊆ s, DilworthTheorem.IsChain (c : Set α) ∧ a ≤ c.card) ∨
    (∃ t ⊆ s, DilworthTheorem.IsAntichain (t : Set α) ∧ b ≤ t.card) := by
  classical
  by_contra h
  push_neg at h
  have hanti : ∀ t ⊆ s, DilworthTheorem.IsAntichain (t : Set α) → t.card ≤ b - 1 := by
    intro t ht hta
    have := h.2 t ht hta
    omega
  obtain ⟨C, hCchain, hCcover, _⟩ := DilworthTheorem.dilworth_theorem s (b - 1) hanti
  have hCsmall : ∀ i, (C i).card ≤ a - 1 := by
    intro i
    have hCi : C i ⊆ s := by
      rw [← hCcover]
      exact Finset.subset_biUnion_of_mem C (Finset.mem_univ i)
    have := h.1 (C i) hCi (hCchain i)
    omega
  have hcard : s.card ≤ (b - 1) * (a - 1) := by
    calc
      s.card = (Finset.univ.biUnion C).card := congrArg Finset.card hCcover.symm
      _ ≤ ∑ i : Fin (b - 1), (C i).card := Finset.card_biUnion_le
      _ ≤ ∑ _i : Fin (b - 1), (a - 1) := Finset.sum_le_sum (fun i _ => hCsmall i)
      _ = (b - 1) * (a - 1) := by simp
  rw [Nat.mul_comm] at hcard
  omega

end ErdosSzekeres.Suk
