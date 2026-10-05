import ErdosSzekeres.Suk.CupsCaps
import Mathlib.Combinatorics.Enumerative.DoubleCounting
import Mathlib.Data.Finset.Powerset
import Mathlib.Data.Nat.Choose.Bounds

namespace ErdosSzekeres.Suk

open Finset

/-- The family of genuinely convex k-subsets, not an abstract coloring family. -/
noncomputable def convexSubsets (s : Finset Point) (k : ℕ) : Finset (Finset Point) := by
  classical
  exact (s.powersetCard k).filter ConvexPosition

@[simp] theorem mem_convexSubsets {s u : Finset Point} {k : ℕ} :
    u ∈ convexSubsets s k ↔ u ⊆ s ∧ u.card = k ∧ ConvexPosition u := by
  classical
  simp [convexSubsets, and_assoc]

private theorem supersets_card_le {α : Type*} [DecidableEq α]
    (s u : Finset α) (m : ℕ) (hus : u ⊆ s) :
    ((s.powersetCard m).filter (fun v => u ⊆ v)).card ≤
      (s.card - u.card).choose (m - u.card) := by
  rw [← card_sdiff_of_subset hus, ← card_powersetCard]
  apply card_le_card_of_injOn (fun v => v \ u)
  · intro v hv
    obtain ⟨hv, huv⟩ := mem_filter.mp hv
    obtain ⟨hvs, hvc⟩ := mem_powersetCard.mp hv
    apply mem_powersetCard.mpr
    refine ⟨sdiff_subset_sdiff hvs (Subset.refl u), ?_⟩
    rw [card_sdiff_of_subset huv, hvc]
  · intro v hv w hw he
    change v \ u = w \ u at he
    have huv := (mem_filter.mp hv).2
    have huw := (mem_filter.mp hw).2
    calc
      v = (v \ u) ∪ u := (sdiff_union_of_subset huv).symm
      _ = (w \ u) ∪ u := by rw [he]
      _ = w := sdiff_union_of_subset huw

/-- Density from a finite covering family. This form also counts cups and
caps, so positive-fraction extraction can retain their horizontal ordering. -/
theorem uniform_family_density {α : Type*} [DecidableEq α]
    (s : Finset α) (F : Finset (Finset α)) (k m : ℕ)
    (hkm : k ≤ m) (hm : m ≤ s.card)
    (hF : ∀ u ∈ F, u ⊆ s ∧ u.card = k)
    (hcover : ∀ v ∈ s.powersetCard m, ∃ u ∈ F, u ⊆ v) :
    s.card.choose k ≤ F.card * m.choose k := by
  classical
  have hlo : ∀ v ∈ s.powersetCard m,
      1 ≤ (F.bipartiteAbove (fun v u => u ⊆ v) v).card := by
    intro v hv
    obtain ⟨u, hu, huv⟩ := hcover v hv
    exact Nat.succ_le_iff.mpr (card_pos.mpr ⟨u, (mem_bipartiteAbove _).mpr ⟨hu, huv⟩⟩)
  have hhi : ∀ u ∈ F,
      ((s.powersetCard m).bipartiteBelow (fun v u => u ⊆ v) u).card ≤
        (s.card - k).choose (m - k) := by
    intro u hu
    simpa [bipartiteBelow, (hF u hu).2] using supersets_card_le s u m (hF u hu).1
  have hcount : s.card.choose m ≤ F.card * (s.card - k).choose (m - k) := by
    simpa only [card_powersetCard, mul_one] using
      card_mul_le_card_mul (fun v u : Finset α => u ⊆ v) hlo hhi
  have h := Nat.mul_le_mul_right (m.choose k) hcount
  rw [Nat.choose_mul hm hkm] at h
  apply le_of_mul_le_mul_right (a := (s.card - k).choose (m - k)) ?_
    (Nat.choose_pos (Nat.sub_le_sub_right hm k))
  simpa [mul_assoc, mul_left_comm, mul_comm] using h

/-- Double counting the incidences between convex k-subsets and all m-subsets.
This is the first counting step in positive-fraction extraction. -/
theorem convex_subsets_count (s : Finset Point) (k m : ℕ)
    (hgp : GeneralPosition s) (hforce : ForcesConvexNGon m k) :
    s.card.choose m ≤ (convexSubsets s k).card * (s.card - k).choose (m - k) := by
  classical
  have hlo : ∀ v ∈ s.powersetCard m,
      1 ≤ ((convexSubsets s k).bipartiteAbove (fun v u => u ⊆ v) v).card := by
    intro v hv
    obtain ⟨hvs, hvc⟩ := mem_powersetCard.mp hv
    obtain ⟨u, huv, huc, hconv⟩ := hforce v (hgp.mono hvs) hvc.ge
    apply Nat.succ_le_iff.mpr
    apply card_pos.mpr
    refine ⟨u, (mem_bipartiteAbove _).mpr ⟨?_, huv⟩⟩
    exact mem_filter.mpr ⟨mem_powersetCard.mpr ⟨huv.trans hvs, huc⟩, hconv⟩
  have hhi : ∀ u ∈ convexSubsets s k,
      ((s.powersetCard m).bipartiteBelow (fun v u => u ⊆ v) u).card ≤
        (s.card - k).choose (m - k) := by
    intro u hu
    change u ∈ (s.powersetCard k).filter ConvexPosition at hu
    obtain ⟨hu, _⟩ := mem_filter.mp hu
    obtain ⟨hus, huc⟩ := mem_powersetCard.mp hu
    simpa [bipartiteBelow, huc] using supersets_card_le s u m hus
  simpa only [card_powersetCard, mul_one] using
    card_mul_le_card_mul (fun v u : Finset Point => u ⊆ v) hlo hhi

/-- An unconditional supply of convex subsets in every real general-position
configuration, obtained from the checked classical cups-caps upper bound. -/
theorem convex_subsets_count_classical (s : Finset Point) (k : ℕ)
    (hk : 3 ≤ k) (hgp : GeneralPosition s) :
    s.card.choose ((2 * k - 4).choose (k - 2) + 1) ≤
      (convexSubsets s k).card * (s.card - k).choose
        ((2 * k - 4).choose (k - 2) + 1 - k) :=
  convex_subsets_count s k _ hgp (classical_upper_bound k hk)

/-- The familiar density form, with no division and hence no rounding ambiguity. -/
theorem convex_subsets_density (s : Finset Point) (k m : ℕ)
    (hkm : k ≤ m) (hm : m ≤ s.card) (hgp : GeneralPosition s)
    (hforce : ForcesConvexNGon m k) :
    s.card.choose k ≤ (convexSubsets s k).card * m.choose k := by
  have h := Nat.mul_le_mul_right (m.choose k) (convex_subsets_count s k m hgp hforce)
  rw [Nat.choose_mul hm hkm] at h
  apply le_of_mul_le_mul_right (a := (s.card - k).choose (m - k)) ?_
    (Nat.choose_pos (Nat.sub_le_sub_right hm k))
  simpa [mul_assoc, mul_left_comm, mul_comm] using h

theorem classical_exponential_bound (k : ℕ) (hk : 3 ≤ k) :
    ForcesConvexNGon (4 ^ k) k := by
  apply (classical_upper_bound k hk).mono
  calc
    (2 * k - 4).choose (k - 2) + 1 ≤ 2 ^ (2 * k - 4) :=
      Nat.succ_le_of_lt (Nat.choose_lt_two_pow _ _ (by omega))
    _ ≤ 2 ^ (2 * k) := Nat.pow_le_pow_right (by decide) (Nat.sub_le _ _)
    _ = 4 ^ k := by rw [pow_mul]; norm_num

/-- This is the convex-subset supply used at the start of Pór–Valtr's
positive-fraction argument, before choosing alternating anchors. -/
theorem convex_subsets_density_exponential (s : Finset Point) (k : ℕ)
    (hk : 3 ≤ k) (hsize : 4 ^ k ≤ s.card) (hgp : GeneralPosition s) :
    s.card.choose k ≤ (convexSubsets s k).card * (4 ^ k).choose k := by
  have hkpow : k ≤ 4 ^ k := (Nat.lt_pow_self (n := k) (a := 4) (by decide)).le
  exact convex_subsets_density s k (4 ^ k) hkpow hsize hgp
    (classical_exponential_bound k hk)

end ErdosSzekeres.Suk
