import Determinants
import SubsequenceFacts
import TerminalBridge

namespace Delta3.Balanced15

/-- The complete finite integer-orientation statement checked in this packet.
Real-coordinate convexity and hull-transfer theorems are not asserted here. -/
theorem balanced15_finite_obstruction :
    (∀ i j : Index, i < j → (point i).1 < (point j).1) ∧
    (∀ a b c : Index, a < b → b < c → det a b c ≠ 0) ∧
    (∀ s : List Index, s.Sublist indices → s.length = 5 → cap s = false) ∧
    (∀ s : List Index, s.Sublist indices → s.length = 7 → signConvex s = false) ∧
    (¬∃ A : Index → Prop, TerminalSafe A ∧ HitsSix A) :=
  ⟨increasing_x, ordered_triples_nondegenerate, five_subsequence_not_cap,
    seven_subsequence_not_signConvex, no_terminal_selection⟩

#print axioms balanced15_finite_obstruction

end Delta3.Balanced15
