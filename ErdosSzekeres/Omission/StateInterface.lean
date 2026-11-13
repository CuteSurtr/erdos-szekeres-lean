/-
Adapted from Michael Schroeder, version-1 archive, 19 September 2026,
DOI 10.5281/zenodo.22842891, formal/sources/ES8/Admissible.lean.
Code: MIT, copyright (c) 2026 Michael Schroeder; see docs/SCHROEDER-MIT.txt.
Catalog data: CC BY 4.0; see docs/THIRD_PARTY.md.
Changes: local namespaces/imports, Lean/Mathlib 4.24 compatibility, kernel-only checks.
-/
import Std

/-! The discrete interface. This module does NOT assert that an arbitrary
Boolean coloring is planar, or that it produces a convex octagon. -/
namespace ErdosSzekeres.Omission.StateInterface

abbrev Label := Nat × Nat
abbrev State := Label → Prop

/-- Coordinates are cap first, cup second, as in the ES8 manuscript. -/
def IncreasingLabels (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (d : Nat → Nat → Label) : Prop :=
  ∀ u v w, u < v → v < w → w < n →
    (cup u v w = false → (d u v).1 < (d v w).1) ∧
    (cup u v w = true → (d u v).2 < (d v w).2)

def Incoming (d : Nat → Nat → Label) (v : Nat) : State :=
  fun z => ∃ u, u < v ∧ z.1 ≤ (d u v).1 ∧ z.2 ≤ (d u v).2

def AdmissibleStates (n : Nat) (d : Nat → Nat → Label)
    (I : Nat → State) : Prop :=
  ∀ u v, u < v → v < n → I v (d u v) ∧ ¬ I u (d u v)

/-- Strict pair growth implies the directed state-difference property. -/
theorem incoming_admissible (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (d : Nat → Nat → Label) (growth : IncreasingLabels n cup d) :
    AdmissibleStates n d (Incoming d) := by
  intro u v huv hvn
  constructor
  · exact ⟨u, huv, Nat.le_refl _, Nat.le_refl _⟩
  · rintro ⟨t, htu, hp, hq⟩
    have hg := growth t u v htu huv hvn
    cases hc : cup t u v with
    | false => have hh := hg.1 hc; omega
    | true => have hh := hg.2 hc; omega

theorem states_distinct (n : Nat) (d : Nat → Nat → Label) (I : Nat → State)
    (admissible : AdmissibleStates n d I)
    (u v : Nat) (huv : u < v) (hvn : v < n) : I u ≠ I v := by
  intro equal
  have hp := admissible u v huv hvn
  exact hp.2 (equal ▸ hp.1)

/-- Inclusion fixes the owner order; no order is imposed on incomparable states. -/
theorem inclusion_forces_order (n : Nat) (d : Nat → Nat → Label) (I : Nat → State)
    (admissible : AdmissibleStates n d I)
    (u v : Nat) (hun : u < n) (_hvn : v < n) (different : u ≠ v)
    (inclusion : ∀ z, I u z → I v z) : u < v := by
  by_cases huv : u < v
  · exact huv
  · have hvu : v < u := by omega
    have hp := admissible v u hvu hun
    exact False.elim (hp.2 (inclusion _ hp.1))

/-- Bounds on ALL possible labels in the two directed differences force a cap. -/
theorem forced_cap (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (d : Nat → Nat → Label) (I : Nat → State)
    (growth : IncreasingLabels n cup d) (admissible : AdmissibleStates n d I)
    (u v w : Nat) (huv : u < v) (hvw : v < w) (hwn : w < n)
    (separation : ∀ a b, I v a → ¬ I u a → I w b → ¬ I v b → b.2 ≤ a.2) :
    cup u v w = false := by
  have ha := admissible u v huv (by omega)
  have hb := admissible v w hvw hwn
  have sep := separation (d u v) (d v w) ha.1 ha.2 hb.1 hb.2
  cases hc : cup u v w with
  | false => rfl
  | true => have hg := (growth u v w huv hvw hwn).2 hc; omega

theorem forced_cup (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (d : Nat → Nat → Label) (I : Nat → State)
    (growth : IncreasingLabels n cup d) (admissible : AdmissibleStates n d I)
    (u v w : Nat) (huv : u < v) (hvw : v < w) (hwn : w < n)
    (separation : ∀ a b, I v a → ¬ I u a → I w b → ¬ I v b → b.1 ≤ a.1) :
    cup u v w = true := by
  have ha := admissible u v huv (by omega)
  have hb := admissible v w hvw hwn
  have sep := separation (d u v) (d v w) ha.1 ha.2 hb.1 hb.2
  cases hc : cup u v w with
  | false => have hg := (growth u v w huv hvw hwn).1 hc; omega
  | true => rfl

end ErdosSzekeres.Omission.StateInterface
