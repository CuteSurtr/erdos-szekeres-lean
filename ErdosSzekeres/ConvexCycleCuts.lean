import ErdosSzekeres.Suk.OrientationClique

namespace ErdosSzekeres

/-- The geometric clause used by the repair searches: an ordering of k distinct
labels must contain a nonpositive ordered triple if the configuration avoids
convex k-gons. The ordering need not have come from a previous solver model. -/
def ConvexCycleCut {N k : ℕ} (p : Fin N → Point) (e : Fin k ↪ Fin N) : Prop :=
  ∃ i j l : Fin k, i < j ∧ j < l ∧ orient (p (e i)) (p (e j)) (p (e l)) ≤ 0

theorem hasConvexNGon_of_positive_cycle {N k : ℕ} (hk : 4 ≤ k)
    (p : Fin N → Point) (hp : Function.Injective p) (e : Fin k ↪ Fin N)
    {P : Finset Point} (hmem : ∀ i, p (e i) ∈ P)
    (h : ∀ i j l : Fin k, i < j → j < l → 0 < orient (p (e i)) (p (e j)) (p (e l))) :
    HasConvexNGon k P := by
  classical
  let q := fun i => p (e i)
  have hq : Function.Injective q := hp.comp e.injective
  refine ⟨Finset.univ.image q, ?_, ?_, ?_⟩
  · rintro x hx
    obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hx
    exact hmem i
  · simp [Finset.card_image_of_injective _ hq]
  · apply Suk.convexPosition_of_positive_triples q hq Finset.univ (by simpa using hk)
    intro i _ j _ l _ hij hjl
    exact h i j l hij hjl

/-- Each exported cycle clause is valid for every injective realization of the
labels. Consequently it can be reused when different coordinates or different
subsets of points are allowed to move. This does not verify an SMT solver. -/
theorem convexCycleCut_of_avoids {N k : ℕ} (hk : 4 ≤ k)
    (p : Fin N → Point) (hp : Function.Injective p) (e : Fin k ↪ Fin N)
    {P : Finset Point} (hmem : ∀ i, p (e i) ∈ P)
    (havoid : ¬ HasConvexNGon k P) : ConvexCycleCut p e := by
  by_contra! hn
  apply havoid (hasConvexNGon_of_positive_cycle hk p hp e hmem ?_)
  intro i j l hij hjl
  have hnot : ¬ orient (p (e i)) (p (e j)) (p (e l)) ≤ 0 := by
    intro he
    exact hn ⟨i, j, l, hij, hjl, he⟩
  exact lt_of_not_ge hnot

end ErdosSzekeres
