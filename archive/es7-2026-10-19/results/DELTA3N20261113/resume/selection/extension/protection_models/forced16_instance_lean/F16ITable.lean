import F16IPairs

namespace Delta3.Forced16Instance

set_option maxRecDepth 10000
set_option maxHeartbeats 10000000

def expectedTriples : List Triple :=
  (List.range 16).flatMap fun a =>
    (List.range 16).flatMap fun b =>
      (List.range 16).filterMap fun c =>
        if a < b ∧ b < c then some ⟨a, b, c⟩ else none

/-- The table enumerates all increasing triples in lexicographic order. -/
theorem triples_exact : triples = expectedTriples := by decide +kernel

theorem weight_sum : Delta3.Forced16Algebra.natTotal rows Row.weight =
    19282471848322771 := by decide +kernel

#print axioms triples_exact
#print axioms weight_sum

end Delta3.Forced16Instance
