/-
Adapted from Jineon Baek's erdos-tuza-valtr proof code, distributed in
Michael Schroeder's version-1 archive, DOI 10.5281/zenodo.22842891.
Licensed under Apache-2.0; see docs/APACHE-2.0.txt and docs/THIRD_PARTY.md.
Changes: local imports and compatibility with Lean/Mathlib v4.24.0.
-/
import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Data.Finset.Basic
import ErdosSzekeres.Vendor.ETV.Config.Default
import ErdosSzekeres.Vendor.ETV.Etv.Default

set_option linter.unusedVariables false
set_option linter.unusedSimpArgs false
set_option linter.unnecessarySeqFocus false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false


open scoped Classical

noncomputable section

variable {α : Type _} [LinearOrder α] (C : Config α)

def Config.MainGoal (n : ℕ) : Prop :=
  ∀ S : Finset α,
    Nat.choose (n + 2) 2 + 2 ≤ S.card →
      ¬C.HasNCap 4 S → ¬C.HasNCup (n + 3) S → ∃ p q r s, C.HasInterweavedLaced (n + 2) S p q r s

def Config.MainGoalWlog (n : ℕ) : Prop :=
  ∀ S : Finset α,
    ¬C.HasJoin (n + 2) (n + 1) S →
      Nat.choose (n + 2) 2 + 2 ≤ S.card →
        ¬C.HasNCap 4 S → ¬C.HasNCup (n + 3) S → ∃ p q r s, C.HasInterweavedLaced (n + 2) S p q r s
