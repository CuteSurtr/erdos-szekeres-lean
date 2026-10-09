import Root

open scoped BigOperators

namespace OmissionBalanced

/-- At most 192 of the 252 literal states can be occupied when every catalog
row has its required number of holes. This has no geometric hypotheses. -/
theorem occupied_card_le (occupied : Finset (Fin 252))
    (hrows : ∀ r, demand r ≤ (support r \ occupied).card) :
    occupied.card ≤ 192 := by
  classical
  by_contra h
  have hcard := Finset.card_add_card_compl occupied
  have hbudget : occupiedᶜ.card ≤ 59 := by
    simp only [Fintype.card_fin] at hcard
    omega
  apply excludes_budget
  refine ⟨fun i => if i ∈ occupied then 0 else 1, ?_, ?_, ?_⟩
  · intro i
    dsimp only
    split_ifs <;> omega
  · intro r
    simpa [Finset.sum_ite, Finset.filter_notMem_eq_sdiff] using hrows r
  · simpa [Finset.sum_ite, Finset.filter_notMem_eq_sdiff] using hbudget

#print axioms code_correct
#print axioms excludes_budget
#print axioms occupied_card_le

end OmissionBalanced
