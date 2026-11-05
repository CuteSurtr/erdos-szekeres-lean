import CompactChecker.Fast2

/-!
# Path masks and the composition of separately checked subtrees (6 November 2026)

For the full ES(8) ≤ 311 recheck the certificate trees are cut into many subtrees
(chunks, and blocks inside chunks). Every exported exclusion is stated for the mask
of its path from the export root:

* `pmask M p` is the mask `M` with the decisions of the path `p` applied, innermost
  decision first: `pmask M ((v, x) :: p) = (pmask M p).set v x` (`x = 2`: state `v`
  occupied, the zero branch; `x = 1`: missing, the one branch).
* `split_pm` combines the exclusions of the two children of a branch on `v`. Its
  hypotheses mention `pmask M ((v, 2) :: p)` and `pmask M ((v, 1) :: p)` literally, so a
  child theorem stated with the literal path `(v, 2) :: p` fits without computation.

Both functions are written with recursors, like the rest of `Fast2.lean`, so a
`checkF2 … (pmask M p) = true` block check evaluates the mask cheaply in the kernel.
-/

namespace CompactChecker

open ErdosSzekeres.OmissionCertificates
open scoped BigOperators

noncomputable section

/-- `n` zeros (the mask with no state fixed), by the recursor. -/
def zerosF (n : ℕ) : List ℕ :=
  Nat.rec (motive := fun _ => List ℕ) [] (fun _ acc => 0 :: acc) n

/-- The mask after the path `p` (innermost decision first) from the mask `M`. -/
def pmask (M : List ℕ) (p : List (ℕ × ℕ)) : List ℕ :=
  List.rec (motive := fun _ => List ℕ) M (fun e _ acc => setF e.2 acc e.1) p

theorem zerosF_eq (n : ℕ) : zerosF n = List.replicate n 0 := by
  induction n with
  | zero => rfl
  | succ n ih =>
      show 0 :: zerosF n = _
      rw [ih, List.replicate_succ]

theorem pmask_nil (M : List ℕ) : pmask M [] = M := rfl

theorem pmask_cons (M : List ℕ) (v x : ℕ) (p : List (ℕ × ℕ)) :
    pmask M ((v, x) :: p) = (pmask M p).set v x := by
  show setF x (pmask M p) v = _
  exact setF_eq x _ v

/-- Composition of the two children of a branch on `v` below the path `p`. -/
theorem split_pm (c : FCat) (m n budget : ℕ) (M : List ℕ) (p : List (ℕ × ℕ)) (v : ℕ)
    (hz : ¬ ∃ holes : Fin n → ℕ, FFeas c m n budget (pmask M ((v, 2) :: p)) holes)
    (ho : ¬ ∃ holes : Fin n → ℕ, FFeas c m n budget (pmask M ((v, 1) :: p)) holes) :
    ¬ ∃ holes : Fin n → ℕ, FFeas c m n budget (pmask M p) holes := by
  rw [pmask_cons] at hz ho
  exact split_feas c m n budget (pmask M p) v hz ho

/-! ## The two export roots: no state fixed, or only state `0` occupied -/

theorem getD_zeros (n i : ℕ) : (zerosF n).getD i 0 = 0 := by
  rw [zerosF_eq, List.getD_eq_getElem?_getD, List.getElem?_replicate]
  split_ifs <;> rfl

theorem getD_zeros_set (n v x i : ℕ) :
    ((zerosF n).set v x).getD i 0 = if i = v ∧ v < n then x else 0 := by
  rw [zerosF_eq, List.getD_eq_getElem?_getD, List.getElem?_set, List.getElem?_replicate]
  by_cases hiv : v = i
  · subst hiv
    by_cases hv : v < n <;> simp [hv]
  · simp only [hiv, if_false, Ne.symm hiv, false_and, if_false]
    split_ifs <;> rfl

/-- At the balanced root no state is fixed. -/
theorem mset_zeros (n v : ℕ) (hv : v ≠ 0) : mset n (pmask (zerosF n) []) v = ∅ := by
  ext i
  simp only [Finset.notMem_empty, iff_false, mem_mset, pmask_nil, getD_zeros]
  exact Ne.symm hv

/-- At the residual root (the zero branch of state `0`) state `0` is occupied and
nothing else is fixed. -/
theorem mem_mset_zero_occupied {n : ℕ} (v : ℕ) (i : Fin n)
    (hi : i ∈ mset n (pmask (zerosF n) [(0, 2)]) v) : (i.val = 0 ∧ v = 2) ∨ v = 0 := by
  rw [mem_mset, pmask_cons, pmask_nil, getD_zeros_set] at hi
  split_ifs at hi with h
  · exact Or.inl ⟨h.1, hi.symm⟩
  · exact Or.inr hi.symm

#print axioms split_pm
#print axioms mset_zeros
#print axioms mem_mset_zero_occupied

end

end CompactChecker
