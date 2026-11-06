import ES8Geo.Capstone2
import ES8Geo.KeyOrder
import ES8Geo.Orbit
import EncB.Compose

/-! # The M5/M6 interface (DESIGN.md §2.1, §2.4), frozen 2026-11-07 before the M5/M6 units start

`PolarLabelling m t T c` is the output of M5 (`labelling_of_counterexample`) and the input of M6
(`modelOfLabelling`). Layer `i < t` of `T` is the regular `m`-gon
`P(i,k) = polar c (r i) (φ + ψ i + k·2π/m)`, whose points are hull vertices of `peel T i`.

Deviation from the text of DESIGN.md §2.1: the binders of the fields are typed (`i k : ℕ`). In §2.1 the
`k` of `mem_layer` is untyped and occurs only as `(k : ℝ)`, so Lean would elaborate it as a real number and
the field would claim membership for every real `k`, which is false for any actual configuration. -/

namespace EncB.Geo
open ErdosSzekeres ErdosSzekeres.LayerLemma

/-- A polar labelling of the layers of `T` about `c`: layer `i` is the regular `m`-gon
    `P(i,k) = polar c (r i) (φ + ψ i + k·2π/m)` (k : ℕ), made of hull vertices of `peel T i`.
    `ψ 0 = 0 < ψ i < 2π/m` (i ≥ 1), pairwise distinct; radii positive and weakly decreasing. -/
structure PolarLabelling (m t : ℕ) (T : Finset Point) (c : Point) where
  r : ℕ → ℝ
  ψ : ℕ → ℝ
  φ : ℝ
  r_pos  : ∀ i : ℕ, i < t → 0 < r i
  r_anti : ∀ i j : ℕ, i ≤ j → j < t → r j ≤ r i
  ψ_zero : ψ 0 = 0
  ψ_pos  : ∀ i : ℕ, 0 < i → i < t → 0 < ψ i
  ψ_lt   : ∀ i : ℕ, i < t → ψ i < 2 * Real.pi / m
  ψ_inj  : ∀ i j : ℕ, i < t → j < t → ψ i = ψ j → i = j
  mem_layer : ∀ i k : ℕ, i < t →
    polar c (r i) (φ + ψ i + (k : ℝ) * (2 * Real.pi / m)) ∈ hullVerts (peel T i)

namespace PolarLabelling

variable {m t : ℕ} {T : Finset Point} {c : Point}

/-- The label map. It is total; it matters only on valid labels (`EncB.PtOk m t`). -/
noncomputable def P (L : PolarLabelling m t T c) (a : EncB.Pt) : Point :=
  polar c (L.r a.1) (L.φ + L.ψ a.1 + (a.2 : ℝ) * (2 * Real.pi / m))

/-- The intended orientation table: `chi a b d` iff `orient (P a) (P b) (P d) > 0`. -/
noncomputable def chi (L : PolarLabelling m t T c) (a b d : EncB.Pt) : Bool :=
  decide (0 < orient (L.P a) (L.P b) (L.P d))

/-- The intended phase order: `psiLt i j` iff `ψ i < ψ j`. -/
noncomputable def psiLt (L : PolarLabelling m t T c) (i j : ℕ) : Bool :=
  decide (L.ψ i < L.ψ j)

end PolarLabelling

end EncB.Geo
