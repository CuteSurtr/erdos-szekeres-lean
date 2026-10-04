import ErdosSzekeres.Suk.PairSupports

namespace ErdosSzekeres.Suk

/-- Consecutive edges of a clockwise cap support each vertex on the side
of a common anchor. At the final vertex use the preceding edge. -/
theorem negative_cap_support_indices {m : ℕ} (p : Fin m → Point) (a : Point)
    (hm : 2 ≤ m)
    (hanchor : ∀ i j, i < j → orient (p i) (p j) a < 0)
    (hcap : ∀ i j k, i < j → j < k → orient (p i) (p j) (p k) < 0) :
    ∀ i, ∃ j, i ≠ j ∧ ∀ k, k ≠ i → k ≠ j →
      0 < orient (p i) (p j) a * orient (p i) (p j) (p k) := by
  intro i
  by_cases hn : i.val + 1 < m
  · let j : Fin m := ⟨i.val + 1, hn⟩
    have hij : i < j := by change i.val < i.val + 1; omega
    refine ⟨j, hij.ne, ?_⟩
    intro k hki hkj
    have hk : k < i ∨ j < k := by
      have hki' : k.val ≠ i.val := fun h => hki (Fin.ext h)
      have hkj' : k.val ≠ j.val := fun h => hkj (Fin.ext h)
      change k.val < i.val ∨ i.val + 1 < k.val
      dsimp [j] at hkj'
      omega
    apply mul_pos_of_neg_of_neg (hanchor i j hij)
    rcases hk with hk | hk
    · simpa only [orient_cycle (p k) (p i) (p j)] using hcap k i j hk hij
    · exact hcap i j k hij hk
  · let j : Fin m := ⟨i.val - 1, by omega⟩
    have hji : j < i := by change i.val - 1 < i.val; omega
    have hia : 0 < orient (p i) (p j) a := by
      have he : orient (p i) (p j) a = -orient (p j) (p i) a := by
        simp only [orient]
        ring
      rw [he]
      exact neg_pos.mpr (hanchor j i hji)
    refine ⟨j, hji.ne.symm, ?_⟩
    intro k hki hkj
    have hk : k < j := by
      have hki' : k.val ≠ i.val := fun h => hki (Fin.ext h)
      have hkj' : k.val ≠ j.val := fun h => hkj (Fin.ext h)
      change k.val < i.val - 1
      dsimp [j] at hkj'
      omega
    have he : orient (p i) (p j) (p k) = -orient (p k) (p j) (p i) := by
      simp only [orient]
      ring
    apply mul_pos hia
    rw [he]
    exact neg_pos.mpr (hcap k j i hk hji)

/-- The supporting-edge condition needed by antichain gluing follows from
ordinary clockwise cap triples and the anchor-side inequalities. -/
theorem pair_supports_of_negative_cap {m : ℕ} (p : Fin m → Point) (a : Point)
    (hm : 2 ≤ m) (hp : Function.Injective p)
    (hanchor : ∀ i j, i < j → orient (p i) (p j) a < 0)
    (hcap : ∀ i j k, i < j → j < k → orient (p i) (p j) (p k) < 0) :
    ∀ x ∈ Finset.univ.image p, ∃ y ∈ Finset.univ.image p, x ≠ y ∧
      ∀ z ∈ Finset.univ.image p, z ≠ x → z ≠ y → 0 < orient x y a * orient x y z := by
  classical
  intro x hx
  obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hx
  obtain ⟨j, hij, hs⟩ := negative_cap_support_indices p a hm hanchor hcap i
  refine ⟨p j, Finset.mem_image_of_mem p (Finset.mem_univ j), hp.ne hij, ?_⟩
  intro z hz hzx hzy
  obtain ⟨k, _, rfl⟩ := Finset.mem_image.mp hz
  exact hs k (fun he => hzx (congrArg p he)) (fun he => hzy (congrArg p he))

end ErdosSzekeres.Suk
