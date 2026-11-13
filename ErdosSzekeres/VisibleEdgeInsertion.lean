import ErdosSzekeres.Suk.PairSupports

/-!
Isolated structural lemma motivated by the nine-state omission obstruction.
These theorems concern ordinary real planar points and have no catalog,
rank, avoidance, or general-position assumptions hidden in a context.
-/

namespace ErdosSzekeres.VisibleEdgeInsertion

open Suk

/-- An exterior point can be adjoined while preserving convex independence
when every old vertex keeps a supporting pair-line that strictly separates
the new point and every old point other than the support partner. -/
theorem convexPosition_insert_of_retained_pair_supports (s : Finset Point) (a : Point)
    (outside : a ∉ convexHull ℝ (s : Set Point))
    (retained : ∀ p ∈ s, ∃ (q : Point) (c : ℝ), p ≠ q ∧
      0 < c * orient p q a ∧
      ∀ r ∈ s, r ≠ p → r = q ∨ 0 < c * orient p q r) :
    ConvexPosition (insert a s) := by
  classical
  rw [convexPosition_iff]
  intro p hp hmem
  change p ∈ insert a s at hp
  rcases Finset.mem_insert.mp hp with hpa | hp
  · subst p
    apply outside
    apply convexHull_mono (s := ((insert a s : Finset Point) : Set Point) \ {a}) ?_ hmem
    intro r hr
    have hm : r ∈ insert a s := hr.1
    rcases Finset.mem_insert.mp hm with hra | hr'
    · subst r
      exact False.elim (hr.2 (Set.mem_singleton a))
    · exact hr'
  · obtain ⟨q, c, hpq, hnew, hside⟩ := retained p hp
    have hsub : (((insert a s : Finset Point) : Set Point) \ {p}) ⊆
        insert q {r : Point | 0 < c * orient p q r} := by
      intro r hr
      have hrp : r ≠ p := by simpa using hr.2
      have hm : r ∈ insert a s := hr.1
      rcases Finset.mem_insert.mp hm with rfl | hr'
      · exact Or.inr hnew
      · exact hside r hr' hrp
    have h := convexHull_min hsub (convex_insert_scaled_orient_positive p q c) hmem
    rcases h with h | h
    · exact hpq h
    · simp [orient] at h

/-- A finite directed edge family supports a set on its left. Endpoints
are distinct members of the set; every other member lies strictly left. -/
def SupportsOnLeft (s : Finset Point) (edges : Finset (Point × Point)) : Prop :=
  ∀ e ∈ edges, e.1 ∈ s ∧ e.2 ∈ s ∧ e.1 ≠ e.2 ∧
    ∀ r ∈ s, r ≠ e.1 → r ≠ e.2 → 0 < orient e.1 e.2 r

/-- One visible edge can be replaced by an exterior point. The remaining
support edges must still meet every old vertex. This finite coverage
condition replaces any implicit cyclic-order or polygon representation. -/
theorem convexPosition_insert_of_one_visible_edge
    (s : Finset Point) (edges : Finset (Point × Point)) (a u v : Point)
    (supporting : SupportsOnLeft s edges)
    (visible : (u, v) ∈ edges) (outside : orient u v a < 0)
    (inside : ∀ e ∈ edges, e ≠ (u, v) → 0 < orient e.1 e.2 a)
    (covered : ∀ p ∈ s, ∃ e ∈ edges, e ≠ (u, v) ∧ (p = e.1 ∨ p = e.2)) :
    ConvexPosition (insert a s) := by
  classical
  have hs : (s : Set Point) ⊆ {r : Point | 0 ≤ orient u v r} := by
    intro r hr
    obtain ⟨_, _, _, he⟩ := supporting (u, v) visible
    by_cases hu : r = u
    · subst r; dsimp [orient]; nlinarith
    by_cases hv : r = v
    · subst r; dsimp [orient]; nlinarith
    exact (he r hr hu hv).le
  have hout : a ∉ convexHull ℝ (s : Set Point) := by
    intro h
    exact (not_le_of_gt outside) (convexHull_min hs (convex_orient_nonnegative u v) h)
  apply convexPosition_insert_of_retained_pair_supports s a hout
  intro p hp
  obtain ⟨e, he, hne, hendpoint⟩ := covered p hp
  obtain ⟨_, _, distinct, sides⟩ := supporting e he
  have newSide := inside e he hne
  rcases hendpoint with rfl | rfl
  · refine ⟨e.2, 1, distinct, by simpa using newSide, ?_⟩
    intro r hr hrp
    by_cases hrq : r = e.2
    · exact Or.inl hrq
    · exact Or.inr (by simpa using sides r hr hrp hrq)
  · refine ⟨e.1, -1, distinct.symm, ?_, ?_⟩
    · have swap : orient e.2 e.1 a = -orient e.1 e.2 a := by
        simp only [orient]; ring
      rw [swap]
      simpa using newSide
    · intro r hr hrp
      by_cases hrq : r = e.1
      · exact Or.inl hrq
      · right
        have swap : orient e.2 e.1 r = -orient e.1 e.2 r := by
          simp only [orient]; ring
        rw [swap]
        simpa using sides r hr hrq hrp

#print axioms convexPosition_insert_of_retained_pair_supports
#print axioms convexPosition_insert_of_one_visible_edge

end ErdosSzekeres.VisibleEdgeInsertion
