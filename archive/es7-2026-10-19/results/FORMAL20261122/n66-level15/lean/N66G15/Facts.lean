import N66G15.Assembly

/-!
# N66G15.Facts: kernel-checked counts and the imported statement

* `leaves105_length`: the split tree has 105 leaves (the hash binding binds 105 printed texts, one per leaf).
* `n66Bound_unfold`: the imported `OmissionZRow.N66Bound` (LemmaZ.olean) is, by `rfl`, the formula of the task.
* `holds_eager_of_parts`: the eager stream is the five families (so `Gaps.eager` splits into five fields).
-/

namespace N66G15
open ErdosSzekeres ErdosSzekeres.Omission N66E15

theorem leaves105_length : leaves105.length = 105 := by decide +kernel

/-- The imported statement is the task's `N66Bound` (checked, not assumed). -/
theorem n66Bound_unfold (B : ℕ) : OmissionZRow.N66Bound B =
    (∀ n : ℕ, ∀ c : Configuration n, ¬ c.HasCap 6 → ¬ c.HasCup 6 →
      ¬ HasConvexNGon 8 (Finset.univ.image c.point) → n ≤ B) := rfl

theorem holds_eager_of_parts {M : Model} (h1 : M.Holds (pairClauses ())) (h2 : M.Holds (posClauses ()))
    (h3 : M.Holds (threshClauses ())) (h4 : M.Holds (tripleClauses ())) (h5 : M.Holds (ceueClauses ())) :
    M.Holds (eagerStream ()) := by
  intro cl hcl
  unfold eagerStream at hcl
  simp only [List.mem_append] at hcl
  rcases hcl with (((h | h) | h) | h) | h
  · exact h1 cl h
  · exact h2 cl h
  · exact h3 cl h
  · exact h4 cl h
  · exact h5 cl h

end N66G15

#print axioms N66G15.leaves105_length
#print axioms N66G15.n66Bound_unfold
#print axioms N66G15.holds_eager_of_parts
