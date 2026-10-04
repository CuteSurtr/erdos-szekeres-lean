import ErdosSzekeres.Definitions
import Mathlib.Analysis.SpecialFunctions.Log.Base
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Algebra.Order.Floor.Defs

namespace ErdosSzekeres.Suk

noncomputable def exponent (C : ℝ) (n : ℕ) : ℝ :=
  n + C * (n : ℝ) ^ ((2 : ℝ) / 3) * Real.logb 2 n

/-- Exact floor convention used in Suk's proof. -/
noncomputable def threshold (C : ℝ) (n : ℕ) : ℕ :=
  ⌊(2 : ℝ) ^ exponent C n⌋₊

/-- Theorem 1.1 of arXiv:1604.08657v2 as a proof target.
This is a proposition definition, not an axiom or a proved theorem. -/
def UpperBoundWithConstant (C : ℝ) : Prop :=
  ∃ n₀ : ℕ, 3 ≤ n₀ ∧ ∀ n : ℕ, n₀ ≤ n → ForcesConvexNGon (threshold C n) n

def Theorem2016 : Prop := UpperBoundWithConstant 6

end ErdosSzekeres.Suk
