import ES8Geo.Interface

/-! # Polar data without a point set (`PolarData`)

ENCBLEAN's `PolarLabelling m t T c` minus `T` and its field `mem_layer`: radii, phases and an offset. ENCBLEAN's
ArcBridge (rules A/B) uses only the fields kept here, so its copy `Geo7/ArcData.lean` proves the rules for
`PolarData`. For odd `m` the data used is at `2m` directions per layer (the half-sector grid of a sevenfold set),
which is not the layer structure of any point set, hence no `mem_layer`. -/

namespace EncB.Geo7
open ErdosSzekeres ErdosSzekeres.LayerLemma

/-- Radii, phases `ψ 0 = 0 < ψ i < 2π/m` (pairwise distinct) and an offset `φ`; point `(i,k)` at
`polar c (r i) (φ + ψ i + k·2π/m)`. -/
structure PolarData (m t : ℕ) (c : Point) where
  r : ℕ → ℝ
  ψ : ℕ → ℝ
  φ : ℝ
  r_pos  : ∀ i : ℕ, i < t → 0 < r i
  r_anti : ∀ i j : ℕ, i ≤ j → j < t → r j ≤ r i
  ψ_zero : ψ 0 = 0
  ψ_pos  : ∀ i : ℕ, 0 < i → i < t → 0 < ψ i
  ψ_lt   : ∀ i : ℕ, i < t → ψ i < 2 * Real.pi / m
  ψ_inj  : ∀ i j : ℕ, i < t → j < t → ψ i = ψ j → i = j

namespace PolarData

variable {m t : ℕ} {c : Point}

/-- The label map (as `PolarLabelling.P`). -/
noncomputable def P (L : PolarData m t c) (a : EncB.Pt) : Point :=
  polar c (L.r a.1) (L.φ + L.ψ a.1 + (a.2 : ℝ) * (2 * Real.pi / m))

/-- `chi a b d` iff `orient (P a) (P b) (P d) > 0`. -/
noncomputable def chi (L : PolarData m t c) (a b d : EncB.Pt) : Bool :=
  decide (0 < orient (L.P a) (L.P b) (L.P d))

/-- `psiLt i j` iff `ψ i < ψ j`. -/
noncomputable def psiLt (L : PolarData m t c) (i j : ℕ) : Bool :=
  decide (L.ψ i < L.ψ j)

end PolarData

end EncB.Geo7
