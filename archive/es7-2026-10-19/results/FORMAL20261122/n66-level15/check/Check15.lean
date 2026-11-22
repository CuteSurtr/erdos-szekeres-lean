import N66G15.End

/-!
Statement check of item n66-level15 (compiled read-only against this directory's oleans; writes no olean). Prints
the axioms of the main theorems, the compiled statement and the definitions in it, checks the level-15 constants by
`rfl`, and restates the end theorem with every non-data definition unfolded by hand (accepted iff definitionally
equal to the compiled one), as the level-14 review did (n66enc/review/ReviewN66.lean).
-/

open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks

/-! ## 1. Axioms -/
#print axioms N66G15.n66_bound_54_of_cubes
#print axioms N66E15.fullUnsat_of_text
#print axioms N66E15.printClause_mem
#print axioms N66E15.printClauses_mem
#print axioms N66E15.base_unsat_of_cubes
#print axioms N66G15.no_model_of_cubes
#print axioms N66G15.holds_card
#print axioms N66G15.holes_le
#print axioms N66G15.capCup55_holds
#print axioms N66G15.mirror_holds
#print axioms N66G15.lexChoice
#print axioms N66G15.leaves105_length
#print axioms N66G15.n66Bound_unfold

/-! ## 2. The statement as compiled, and the definitions in it -/
#check @N66G15.n66_bound_54_of_cubes
#print OmissionZRow.N66Bound
#print N66E15.CubesUnsat105
#print N66E15.fullCnf
#print N66E15.fullS
#print N66E15.leaves105
#print N66E15.R0_15
#print N66G15.RowsValid
#print N66G15.RowValid
#print N66G15.InClass

/-! ## 3. Level-15 constants (definitional) -/
example : N66E15.kBound = 15 := rfl
example : N66E15.nLits = 68 := rfl
example : N66E15.nvHeader = 1647847 := rfl
example : N66E15.leaves105.length = 105 := N66G15.leaves105_length
example : ∀ M : N66G15.Model, 55 ≤ M.n → M.holes ≤ 15 := N66G15.holes_le
example : ∀ M : N66G15.Model, M.holes ≤ 15 → M.Holds N66E15.cardClauses := N66G15.holds_card

/-! ## 4. The end theorem with every non-data definition unfolded by hand -/
theorem check15_unfolded :
    (∀ c ∈ N66E15.leaves105, ¬ ∃ ν : ℕ → Bool, ∀ cl ∈ N66E15.fullCnf N66E15.R0_15 c, ∃ l ∈ cl,
        (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false)) →
    (∀ T ∈ N66E15.R0_15, ∀ n (c : Configuration n),
        (¬ c.HasCap 6 ∧ ¬ c.HasCup 6 ∧ ¬ HasConvexNGon 8 (Finset.univ.image c.point)) →
        ∃ s ∈ T, ¬ ∃ v < n, N66E15.stateList.idxOf
          (ErdosSzekeres.Omission.ActualRanks.column c.cup v 0,
           ErdosSzekeres.Omission.ActualRanks.column c.cup v 1,
           ErdosSzekeres.Omission.ActualRanks.column c.cup v 2,
           ErdosSzekeres.Omission.ActualRanks.column c.cup v 3) = s.val) →
    ∀ n (c : Configuration n), ¬ c.HasCap 6 → ¬ c.HasCup 6 →
      ¬ HasConvexNGon 8 (Finset.univ.image c.point) → n ≤ 54 :=
  N66G15.n66_bound_54_of_cubes

#print axioms check15_unfolded
