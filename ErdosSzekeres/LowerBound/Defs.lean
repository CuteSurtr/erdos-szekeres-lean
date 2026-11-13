import ErdosSzekeres.Basic
import ErdosSzekeres.OrientationGeometry

/-! Definitions for the classical Erdős–Szekeres lower-bound construction.

Points are compared by their first coordinate. A `σ`-chain is a set whose
horizontally increasing triples all have orientation of the sign of `σ`: for
`σ = 1` it is a cup and for `σ = -1` a cap. A pair of blocks is *stacked*
when the second lies to the right of the first and far above it (`σ = 1`) or
far below it (`σ = -1`); only the signs of mixed triples are recorded. -/

namespace ErdosSzekeres.LowerBound

/-- Distinct first coordinates. -/
def DistinctX (s : Finset Point) : Prop :=
  Set.InjOn (fun p : Point => p 0) (s : Set Point)

/-- Every horizontally increasing triple has orientation of the sign of `σ`. -/
def IsChain (σ : ℝ) (t : Finset Point) : Prop :=
  ∀ a ∈ t, ∀ b ∈ t, ∀ c ∈ t, a 0 < b 0 → b 0 < c 0 → 0 < σ * orient a b c

/-- Every `σ`-chain contained in `s` has at most `m` points. -/
def ChainBound (σ : ℝ) (m : ℕ) (s : Finset Point) : Prop :=
  ∀ t ⊆ s, IsChain σ t → t.card ≤ m

/-- Every subset of `s` in convex position has at most `m` points. -/
def ConvexBound (m : ℕ) (s : Finset Point) : Prop :=
  ∀ t ⊆ s, ConvexPosition t → t.card ≤ m

/-- `B` lies to the right of `A`, and every mixed triple has the orientation
it would have if `B` were moved far above `A` (`σ > 0`) or far below it
(`σ < 0`). -/
structure Stacked (σ : ℝ) (A B : Finset Point) : Prop where
  left_lt : ∀ a ∈ A, ∀ b ∈ B, a 0 < b 0
  pair_left : ∀ a ∈ A, ∀ a' ∈ A, ∀ b ∈ B, a 0 < a' 0 → 0 < σ * orient a a' b
  pair_right : ∀ a ∈ A, ∀ b ∈ B, ∀ b' ∈ B, b 0 < b' 0 → σ * orient a b b' < 0

theorem IsChain.mono {σ : ℝ} {s t : Finset Point} (hs : IsChain σ s) (ht : t ⊆ s) :
    IsChain σ t :=
  fun a ha b hb c hc hab hbc => hs a (ht ha) b (ht hb) c (ht hc) hab hbc

theorem ChainBound.mono {σ : ℝ} {m m' : ℕ} {s : Finset Point}
    (h : ChainBound σ m s) (hm : m ≤ m') : ChainBound σ m' s :=
  fun t ht hc => (h t ht hc).trans hm

theorem ConvexBound.mono {m m' : ℕ} {s : Finset Point}
    (h : ConvexBound m s) (hm : m ≤ m') : ConvexBound m' s :=
  fun t ht hc => (h t ht hc).trans hm

/-- A point set all of whose convex subsets are smaller than `n` has no convex `n`-gon. -/
theorem not_hasConvexNGon_of_convexBound {n : ℕ} {s : Finset Point}
    (h : ConvexBound (n - 1) s) (hn : 1 ≤ n) : ¬ HasConvexNGon n s := by
  rintro ⟨t, hts, htn, htc⟩
  have := h t hts htc
  omega

end ErdosSzekeres.LowerBound
