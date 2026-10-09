import ErdosSzekeres.HMPT.BinomialRefinement
import Mathlib.Tactic.NormNum.NatLog

set_option maxRecDepth 10000
set_option maxHeartbeats 1000000

namespace ErdosSzekeres.HMPT.BinomialRefinementExample

/-- A small arithmetic regression example for the exponent comparison.
It makes no claim of numerical competitiveness for the small target n=4. -/
theorem strict_exponent_example :
    twoScaleExponent 3 4 26 = 129 ∧ twoScaleFactorialExponent 3 4 26 = 128 := by
  norm_num [twoScaleExponent, twoScaleFactorialExponent, twoScaleProduct,
    supportProductBound, Nat.choose]

#print axioms strict_exponent_example

end ErdosSzekeres.HMPT.BinomialRefinementExample
