import ErdosSzekeres.Suk.SpikeDichotomy
import Mathlib.Data.Finset.Max

namespace ErdosSzekeres.HMPT

open Suk

/-- A bounded family of natural-number witnesses has an attained maximum. -/
theorem exists_max_bounded {P : ℕ → Prop} {N : ℕ}
    (hne : ∃ n, P n) (hbound : ∀ n, P n → n ≤ N) :
    ∃ n, P n ∧ ∀ m, P m → m ≤ n := by
  classical
  let s := (Finset.range (N + 1)).filter P
  have hs : s.Nonempty := by
    obtain ⟨n, hn⟩ := hne
    exact ⟨n, Finset.mem_filter.mpr ⟨Finset.mem_range.mpr (by have := hbound n hn; omega), hn⟩⟩
  obtain ⟨n, hn, hm⟩ := Finset.exists_max_image s id hs
  refine ⟨n, (Finset.mem_filter.mp hn).2, ?_⟩
  intro m hp
  exact hm m (Finset.mem_filter.mpr
    ⟨Finset.mem_range.mpr (by have := hbound m hp; omega), hp⟩)

/-- Choose an actual largest subset satisfying a predicate, including the empty case. -/
theorem exists_max_card_subset {α : Type*} (s : Finset α) (P : Finset α → Prop)
    (hP : P ∅) :
    ∃ t ⊆ s, P t ∧ ∀ u ⊆ s, P u → u.card ≤ t.card := by
  classical
  let F := s.powerset.filter P
  have hF : F.Nonempty := ⟨∅, by simp [F, hP]⟩
  obtain ⟨t, ht, hmax⟩ := Finset.exists_max_image F Finset.card hF
  obtain ⟨hts, htP⟩ := Finset.mem_filter.mp ht
  refine ⟨t, Finset.mem_powerset.mp hts, htP, ?_⟩
  intro u hus hu
  exact hmax u (Finset.mem_filter.mpr ⟨Finset.mem_powerset.mpr hus, hu⟩)

/-- Incomparability in the geometric outer-base triangle order. -/
def SpikeAntichain (F : CapFrame) (s : Finset Point) : Prop :=
  ∀ p ∈ s, ∀ q ∈ s, p ≠ q → q ∉ convexHull ℝ ({F.a, F.d, p} : Set Point)

theorem SpikeAntichain.mono {F : CapFrame} {s t : Finset Point}
    (h : SpikeAntichain F s) (ht : t ⊆ s) : SpikeAntichain F t :=
  fun p hp q hq hpq => h p (ht hp) q (ht hq) hpq

/-- HMPT's region-size inequality, with attained chain and antichain maxima
in the actual geometric order. No general-position or nonemptiness assumption
is needed for this part. -/
theorem exists_max_chain_antichain (F : CapFrame) (s : Finset Point)
    (hspike : ∀ p ∈ s, p ∈ F.spike) :
    ∃ (C : SpikeChain F) (T : Finset Point),
      C.points ⊆ s ∧ T ⊆ s ∧ SpikeAntichain F T ∧
      (∀ D : SpikeChain F, D.points ⊆ s → D.length ≤ C.length) ∧
      (∀ U ⊆ s, SpikeAntichain F U → U.card ≤ T.card) ∧
      s.card ≤ C.length * T.card := by
  classical
  let E : SpikeChain F := ⟨0, Fin.elim0, fun i => Fin.elim0 i⟩
  have hE : E.points ⊆ s := by simp [SpikeChain.points, E]
  obtain ⟨v, ⟨C, hC, hCs⟩, hv⟩ := exists_max_bounded (N := s.card)
    (P := fun v => ∃ C : SpikeChain F, C.length = v ∧ C.points ⊆ s)
    ⟨0, E, rfl, hE⟩ (by
      rintro v ⟨C, rfl, hC⟩
      simpa only [C.card_points] using Finset.card_le_card hC)
  obtain ⟨T, hTs, hT, hTmax⟩ := exists_max_card_subset s (SpikeAntichain F)
    (by simp [SpikeAntichain])
  have hCmax (D : SpikeChain F) (hD : D.points ⊆ s) : D.length ≤ C.length := by
    rw [hC]
    exact hv D.length ⟨D, rfl, hD⟩
  refine ⟨C, T, hCs, hTs, hT, hCmax, hTmax, ?_⟩
  by_contra! hsize
  rcases F.spike_chain_or_antichain s hspike C.length T.card hsize with
    ⟨D, hD, hDs⟩ | ⟨U, hUs, hU, hUa⟩
  · exact (not_lt_of_ge (hCmax D hDs)) hD
  · exact (not_lt_of_ge (hTmax U hUs hUa)) hU

end ErdosSzekeres.HMPT
