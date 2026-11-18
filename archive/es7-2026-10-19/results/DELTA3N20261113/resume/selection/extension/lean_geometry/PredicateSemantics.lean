import FiniteModel

namespace Delta3.Balanced15

/-- The terminal Boolean test is exactly an existential ambient four-cap test. -/
theorem terminalPair_iff (b c : Index) :
    terminalPair b c = true ↔
      ∃ u v : Index, u < v ∧ v < b ∧ b < c ∧ cap [u, v, b, c] = true := by
  simp only [terminalPair, List.any_eq_true, Bool.and_eq_true, decide_eq_true_eq]
  constructor
  · rintro ⟨u, _, v, _, ⟨huv, hvb, hbc⟩, hcap⟩
    exact ⟨u, v, huv, hvb, hbc, hcap⟩
  · rintro ⟨u, v, huv, hvb, hbc, hcap⟩
    exact ⟨u, indices_complete u, v, indices_complete v, ⟨huv, hvb, hbc⟩, hcap⟩

#print axioms terminalPair_iff

end Delta3.Balanced15
