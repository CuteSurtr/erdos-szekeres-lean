import T12FiniteModel

/-! Auxiliary declarations for the separately checked real-coordinate bridge. -/

namespace Delta3.Terminal12.RealBridge

theorem distinct_det_ne : ∀ a b c : Index, a ≠ b → a ≠ c → b ≠ c → det a b c ≠ 0 := by
  decide +kernel

theorem indices_nodup : indices.Nodup := by decide +kernel

theorem indices_sorted : indices.Pairwise (· ≤ ·) := by decide +kernel

/-- Soundness complements the frozen enumerator-completeness theorem. -/
theorem choose_sound {α : Type} {xs ys : List α} {k : Nat} (h : xs ∈ choose k ys) :
    xs.Sublist ys ∧ xs.length = k := by
  induction ys generalizing k xs with
  | nil =>
    cases k with
    | zero =>
      have he : xs = [] := by simpa only [choose, List.mem_cons, List.not_mem_nil, or_false] using h
      subst xs
      exact ⟨.slnil, rfl⟩
    | succ k => exact False.elim (List.not_mem_nil h)
  | cons a ys ih =>
    cases k with
    | zero =>
      have he : xs = [] := by simpa only [choose, List.mem_cons, List.not_mem_nil, or_false] using h
      subst xs
      exact ⟨List.nil_sublist _, rfl⟩
    | succ k =>
      rcases List.mem_append.mp h with h | h
      · obtain ⟨zs, hz, rfl⟩ := List.mem_map.mp h
        obtain ⟨hsub, hlen⟩ := ih hz
        exact ⟨hsub.cons₂ a, congrArg Nat.succ hlen⟩
      · obtain ⟨hsub, hlen⟩ := ih h
        exact ⟨hsub.cons a, hlen⟩

#print axioms distinct_det_ne
#print axioms indices_nodup
#print axioms indices_sorted
#print axioms choose_sound

end Delta3.Terminal12.RealBridge
