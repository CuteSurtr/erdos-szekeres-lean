import WeightedEnvelope

/-!
# Minimal field adapter for Lean's built-in arithmetic tactic

This reconstructs the ordinary `Field.toGrindField` adapter from
`Mathlib.Algebra.Field.Basic`, using already imported field laws. Avoiding that larger import
keeps this bounded task within its resident-memory allocation. It adds no algebraic assumption.
-/

namespace Delta3.WeightedEnvelope

def grindField (K : Type*) [Field K] : Lean.Grind.Field K :=
  { CommRing.toGrindCommRing K, ‹Field K› with
    zpow := ⟨fun a n ↦ a ^ n⟩
    zpow_zero := zpow_zero
    zpow_succ a n := by simp only [← Int.natCast_add_one, zpow_natCast, pow_succ]
    zpow_neg := zpow_neg
    zero_ne_one := zero_ne_one' K }

#print axioms grindField

end Delta3.WeightedEnvelope
