import T12Determinants
import T12SubsequenceFacts
import T12TerminalBridge

namespace Delta3.Terminal12

/-- The complete finite integer-orientation statement checked in this packet.
Real-coordinate convexity and hull-transfer theorems are not asserted here. -/
theorem terminal12_finite_obstruction :
    (∀ i j : Index, i < j → (point i).1 < (point j).1) ∧
    (∀ a b c : Index, a < b → b < c → det a b c ≠ 0) ∧
    (∀ s : List Index, s.Sublist indices → s.length = 5 → cap s = false) ∧
    (∀ s : List Index, s.Sublist indices → s.length = 6 → signConvex s = false) ∧
    (¬∃ A : Index → Prop, TerminalSafe A ∧ HitsFive A) :=
  ⟨increasing_x, ordered_triples_nondegenerate, five_subsequence_not_cap,
    six_subsequence_not_signConvex, no_terminal_selection⟩

#print axioms terminal12_finite_obstruction

end Delta3.Terminal12
