import Mathlib.Tactic

namespace ErdosSzekeres.Suk

/-- A finite version of the case split in Suk's Section 3. Blocks of r indices
are separated by one unused index. If there is no good block, one bad index per
block gives t pairwise nonadjacent bad indices. -/
theorem consecutive_or_separated (good : ℕ → Prop) (k r t : ℕ)
    (hsize : t * (r + 1) ≤ k) :
    (∃ start : ℕ, start + r ≤ k ∧ ∀ j < r, good (start + j)) ∨
    (∃ f : Fin t → ℕ, (∀ i, f i < k ∧ ¬ good (f i)) ∧
      ∀ i j, i < j → f i + 1 < f j) := by
  classical
  by_cases hrun : ∃ start : ℕ, start + r ≤ k ∧ ∀ j < r, good (start + j)
  · exact Or.inl hrun
  right
  have block_bound (i : Fin t) : i.val * (r + 1) + r ≤ k := by
    have h := Nat.mul_le_mul_right (r + 1) (show i.val + 1 ≤ t by omega)
    nlinarith
  have bad (i : Fin t) : ∃ j, j < r ∧ ¬ good (i.val * (r + 1) + j) := by
    by_contra! h
    exact hrun ⟨i.val * (r + 1), block_bound i, h⟩
  choose offset ho hg using bad
  let f : Fin t → ℕ := fun i => i.val * (r + 1) + offset i
  refine ⟨f, ?_, ?_⟩
  · intro i
    exact ⟨by dsimp [f]; have := block_bound i; have := ho i; omega, hg i⟩
  · intro i j hij
    have hij' : i.val + 1 ≤ j.val := hij
    have h := Nat.mul_le_mul_right (r + 1) hij'
    have hi := ho i
    dsimp [f]
    nlinarith

end ErdosSzekeres.Suk
