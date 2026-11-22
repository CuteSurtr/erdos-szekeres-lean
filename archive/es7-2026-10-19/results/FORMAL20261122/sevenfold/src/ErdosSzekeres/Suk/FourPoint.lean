import ErdosSzekeres.Basic
import Mathlib.Analysis.Convex.Caratheodory
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.Tactic.Linarith

namespace ErdosSzekeres.Suk

/-- Carathéodory reduces any failure of convex position in the plane to at most
four points. No general-position assumption is needed for this version. -/
theorem convexPosition_of_subsets_card_le_four {s : Finset Point}
    (h : ∀ t ⊆ s, t.card ≤ 4 → ConvexPosition t) : ConvexPosition s := by
  classical
  rw [convexPosition_iff]
  intro p hp hmem
  let t := Caratheodory.minCardFinsetOfMemConvexHull hmem
  have ht : (t : Set Point) ⊆ (s : Set Point) \ {p} :=
    Caratheodory.minCardFinsetOfMemConvexHull_subseteq hmem
  have hpt : p ∉ t := by
    intro hpt
    exact (ht hpt).2 (Set.mem_singleton p)
  have hcard : t.card ≤ 3 := by
    have hi := (Caratheodory.affineIndependent_minCardFinsetOfMemConvexHull hmem).card_le_finrank_succ
    have hd := (vectorSpan ℝ (Set.range (fun p : t => (p : Point)))).finrank_le
    have hc := hi.trans (Nat.add_le_add_right hd 1)
    simpa [Point, t] using hc
  have hus : insert p t ⊆ s := by
    intro q hq
    rcases Finset.mem_insert.mp hq with rfl | hq
    · exact hp
    · exact (ht hq).1
  have hu := h (insert p t) hus (by rw [Finset.card_insert_of_notMem hpt]; omega)
  apply (convexPosition_iff _).mp hu p (by simp)
  apply convexHull_mono (s := (t : Set Point)) ?_
    (Caratheodory.mem_minCardFinsetOfMemConvexHull hmem)
  intro q hq
  exact ⟨Finset.mem_insert_of_mem hq, fun heq => hpt (heq ▸ hq)⟩

/-- Suk's Lemma 2.1 for sets with at least four points. In fact general position
is unnecessary once every four-point subset is convex independent. -/
theorem convexPosition_of_four_subsets {s : Finset Point} (hs : 4 ≤ s.card)
    (h : ∀ t ⊆ s, t.card = 4 → ConvexPosition t) : ConvexPosition s := by
  apply convexPosition_of_subsets_card_le_four
  intro t hts ht
  obtain ⟨u, htu, hus, hu⟩ := Finset.exists_subsuperset_card_eq hts ht hs
  exact (h u hus hu).mono htu

end ErdosSzekeres.Suk
