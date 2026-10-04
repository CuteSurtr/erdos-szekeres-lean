import ErdosSzekeres.Suk.Statement
import Mathlib.Analysis.SpecialFunctions.Pow.Real

namespace ErdosSzekeres.HMPT

/-- Final 2020 version, Remark 1.4, not the older preprint's constant. -/
noncomputable def publishedCoefficient : ℝ := 8 * Real.sqrt 2 / 3

noncomputable def threshold (C : ℝ) (n : ℕ) : ℕ :=
  ⌊(2 : ℝ) ^ ((n : ℝ) + C * Real.sqrt ((n : ℝ) * Real.logb 2 n))⌋₊

/-- A precise epsilon formulation of an asymptotic leading coefficient.
This definition does not assert an upper bound. -/
def UpperBoundWithLeadingCoefficient (C : ℝ) : Prop :=
  ∀ ε : ℝ, 0 < ε → ∃ n₀ : ℕ, 3 ≤ n₀ ∧
    ∀ n : ℕ, n₀ ≤ n → ForcesConvexNGon (threshold (C + ε) n) n

/-- Target for formalizing the published theorem for ordinary point sets.
Pseudo-configurations and convex-body extensions are outside this definition. -/
def Theorem2020 : Prop := UpperBoundWithLeadingCoefficient publishedCoefficient

/-- A strict leading-coefficient improvement is a research target, not a theorem.
Finite experiments or changes hidden inside the published o(1) do not prove it. -/
def StrictImprovement : Prop :=
  ∃ C : ℝ, 0 ≤ C ∧ C < publishedCoefficient ∧ UpperBoundWithLeadingCoefficient C

end ErdosSzekeres.HMPT
