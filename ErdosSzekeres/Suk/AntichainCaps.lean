import ErdosSzekeres.Suk.SpikeSeparation
import ErdosSzekeres.Suk.PairSupports

namespace ErdosSzekeres.Suk

open scoped BigOperators

/-- Gluing for the antichain case with the local supporting-edge condition
explicit. The nonadjacent-region separation needed to extend those supports
to the entire union is proved from the geometric triangle order. -/
theorem ClockwiseAnchors.convexPosition_union_antichain_caps_of_supports {r : ℕ}
    (A : ClockwiseAnchors (r + 3)) (I : Finset (Fin r)) (S : Fin r → Finset Point)
    (hsep : ∀ i ∈ I, ∀ j ∈ I, i ≠ j → i.val + 1 < j.val ∨ j.val + 1 < i.val)
    (hspike : ∀ i ∈ I, ∀ p ∈ S i, p ∈ (A.frame i).spike)
    (hanti : ∀ i ∈ I, ∀ p ∈ S i, ∀ q ∈ S i, p ≠ q →
      q ∉ convexHull ℝ ({(A.frame i).a, (A.frame i).d, p} : Set Point))
    (hsupport : ∀ i ∈ I, ∀ p ∈ S i, ∃ q ∈ S i, p ≠ q ∧
      ∀ z ∈ S i, z ≠ p → z ≠ q →
        0 < orient p q (A.frame i).a * orient p q z) :
    ConvexPosition (I.biUnion S) := by
  classical
  apply convexPosition_of_pair_supports
  intro p hp
  obtain ⟨i, hi, hp⟩ := Finset.mem_biUnion.mp hp
  obtain ⟨q, hq, hpq, hs⟩ := hsupport i hi p hp
  refine ⟨q, orient p q (A.frame i).a, hpq, ?_⟩
  intro z hz hzp
  obtain ⟨j, hj, hz⟩ := Finset.mem_biUnion.mp hz
  by_cases hji : j = i
  · subst j
    by_cases hzq : z = q
    · exact Or.inl hzq
    · exact Or.inr (hs z hz hzp hzq)
  · right
    let p' : (A.frame i).spike := ⟨p, hspike i hi p hp⟩
    let q' : (A.frame i).spike := ⟨q, hspike i hi q hq⟩
    let z' : (A.frame j).spike := ⟨z, hspike j hj z hz⟩
    apply A.incomparable_pair_nonadjacent_same_side i j (hsep i hi j hj (Ne.symm hji)) p' q' z'
    · rw [AboveBase.le_iff]
      exact hanti i hi p hp q hq hpq
    · rw [AboveBase.le_iff]
      exact hanti i hi q hq p hp hpq.symm

/-- Cardinality-aware form of the antichain gluing theorem. The sum counts
distinct vertices because the selected nonadjacent spikes are disjoint. -/
theorem ClockwiseAnchors.hasConvexNGon_union_antichain_caps_of_supports {r n : ℕ}
    (A : ClockwiseAnchors (r + 3)) (I : Finset (Fin r)) (S : Fin r → Finset Point)
    {P : Finset Point}
    (hsep : ∀ i ∈ I, ∀ j ∈ I, i ≠ j → i.val + 1 < j.val ∨ j.val + 1 < i.val)
    (hspike : ∀ i ∈ I, ∀ p ∈ S i, p ∈ (A.frame i).spike)
    (hanti : ∀ i ∈ I, ∀ p ∈ S i, ∀ q ∈ S i, p ≠ q →
      q ∉ convexHull ℝ ({(A.frame i).a, (A.frame i).d, p} : Set Point))
    (hsupport : ∀ i ∈ I, ∀ p ∈ S i, ∃ q ∈ S i, p ≠ q ∧
      ∀ z ∈ S i, z ≠ p → z ≠ q →
        0 < orient p q (A.frame i).a * orient p q z)
    (hpoints : ∀ i ∈ I, S i ⊆ P) (hsize : n ≤ ∑ i ∈ I, (S i).card) :
    HasConvexNGon n P := by
  classical
  have hdis : (I : Set (Fin r)).PairwiseDisjoint S := by
    intro i hi j hj hij
    apply Finset.disjoint_left.mpr
    intro p hp hq
    exact Set.disjoint_left.mp (A.nonadjacent_spikes_disjoint i j (hsep i hi j hj hij))
      (hspike i hi p hp) (hspike j hj p hq)
  have hcard : n ≤ (I.biUnion S).card := by
    rw [Finset.card_biUnion hdis]
    exact hsize
  have hconv := A.convexPosition_union_antichain_caps_of_supports I S hsep hspike hanti hsupport
  exact (hconv.hasConvexNGon hcard).mono (Finset.biUnion_subset.mpr hpoints)

end ErdosSzekeres.Suk
