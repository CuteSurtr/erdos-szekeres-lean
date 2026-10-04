import ErdosSzekeres.Definitions
import Mathlib.Tactic.NormNum

namespace ErdosSzekeres

theorem GeneralPosition.mono {s t : Finset Point} (hs : GeneralPosition s) (ht : t ⊆ s) :
    GeneralPosition t := by
  intro a ha b hb c hc hab hac hbc
  exact hs a (ht ha) b (ht hb) c (ht hc) hab hac hbc

theorem ConvexPosition.mono {s t : Finset Point} (hs : ConvexPosition s) (ht : t ⊆ s) :
    ConvexPosition t :=
  ConvexIndependent.mono hs (by simpa using ht)

theorem convexPosition_iff (s : Finset Point) :
    ConvexPosition s ↔ ∀ p ∈ (s : Set Point),
      p ∉ convexHull ℝ ((s : Set Point) \ {p}) :=
  convexIndependent_set_iff_notMem_convexHull_diff

theorem HasConvexNGon.mono {s t : Finset Point} {n : ℕ}
    (hs : HasConvexNGon n s) (hst : s ⊆ t) : HasConvexNGon n t := by
  obtain ⟨u, hus, hu, hc⟩ := hs
  exact ⟨u, hus.trans hst, hu, hc⟩

theorem HasConvexNGon.card_le {s : Finset Point} {n : ℕ}
    (hs : HasConvexNGon n s) : n ≤ s.card := by
  obtain ⟨t, ht, rfl, _⟩ := hs
  exact Finset.card_le_card ht

/-- The exact-cardinality and at-least-cardinality formulations agree. -/
theorem forcesConvexNGon_iff_exact (N n : ℕ) :
    ForcesConvexNGon N n ↔
      ∀ s : Finset Point, GeneralPosition s → s.card = N → HasConvexNGon n s := by
  constructor
  · intro h s hgp hcard
    exact h s hgp hcard.ge
  · intro h s hgp hcard
    obtain ⟨t, hts, ht⟩ := Finset.exists_subset_card_eq hcard
    exact (h t (hgp.mono hts) ht).mono hts

theorem ForcesConvexNGon.mono {N M n : ℕ} (h : ForcesConvexNGon N n) (hNM : N ≤ M) :
    ForcesConvexNGon M n := by
  intro s hgp hs
  exact h s hgp (hNM.trans hs)

/-- A small bridge between Mathlib's affine and convex independence APIs. -/
theorem convexIndependent_of_affineIndependent {ι : Type*} {p : ι → Point}
    (h : AffineIndependent ℝ p) : ConvexIndependent ℝ p := by
  intro s i hi
  exact (h.mem_affineSpan_iff i s).mp (convexHull_subset_affineSpan _ hi)

theorem convexPosition_of_card_three {s : Finset Point}
    (hgp : GeneralPosition s) (hcard : s.card = 3) : ConvexPosition s := by
  classical
  obtain ⟨a, b, c, hab, hac, hbc, rfl⟩ := Finset.card_eq_three.mp hcard
  have hn := hgp a (by simp) b (by simp) c (by simp) hab hac hbc
  have ha : AffineIndependent ℝ ![a, b, c] := affineIndependent_iff_not_collinear_set.mpr hn
  have hc := (convexIndependent_of_affineIndependent ha).range
  have hr : Set.range ![a, b, c] = (↑({a, b, c} : Finset Point) : Set Point) := by
    ext p
    simp [Matrix.range_cons, Matrix.range_empty, or_comm, or_left_comm]
  rw [hr] at hc
  exact hc

/-- First proved case of the conjecture, valid for every real configuration. -/
theorem forces_triangle : ForcesConvexNGon 3 3 := by
  apply (forcesConvexNGon_iff_exact 3 3).mpr
  intro s hgp hs
  exact ⟨s, Finset.Subset.refl s, hs, convexPosition_of_card_three hgp hs⟩

theorem conjecture_case_three : ForcesConvexNGon (conjecturedBound 3) 3 := by
  simpa [conjecturedBound] using forces_triangle

theorem conjecture_implies_seven (h : ErdosSzekeresConjecture) : HeptagonConjecture := by
  have h7 := h 7 (by norm_num)
  simpa [HeptagonConjecture, conjecturedBound] using h7

/-- A genuine geometric witness at the threshold would disprove the universal claim. -/
theorem counterexample_refutes_conjecture {n : ℕ} {s : Finset Point}
    (hn : 3 ≤ n) (hgp : GeneralPosition s) (hsize : conjecturedBound n ≤ s.card)
    (havoid : ¬ HasConvexNGon n s) : ¬ ErdosSzekeresConjecture := by
  intro h
  exact havoid (h n hn s hgp hsize)

end ErdosSzekeres
