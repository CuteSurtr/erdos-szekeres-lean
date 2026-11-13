import ErdosSzekeres.Suk.OrientationClique
import Mathlib.Data.Sum.Order
import Mathlib.Data.Finset.Sum

namespace ErdosSzekeres.Suk

/-- Concatenate a positive clique with a reversed negative clique. The two
mixed-triple conditions are precisely the cross-region separation obligations. -/
theorem convexPosition_glue_orientation {ι κ : Type*} [LinearOrder ι] [LinearOrder κ]
    (p : ι → Point) (q : κ → Point) (hp : Function.Injective p) (hq : Function.Injective q)
    (hne : ∀ i j, p i ≠ q j) (s : Finset ι) (t : Finset κ) (hcard : 4 ≤ s.card + t.card)
    (hpos : ∀ i ∈ s, ∀ j ∈ s, ∀ k ∈ s, i < j → j < k → 0 < orient (p i) (p j) (p k))
    (hneg : ∀ i ∈ t, ∀ j ∈ t, ∀ k ∈ t, i < j → j < k → orient (q i) (q j) (q k) < 0)
    (hppq : ∀ i ∈ s, ∀ j ∈ s, ∀ k ∈ t, i < j → 0 < orient (p i) (p j) (q k))
    (hqqp : ∀ i ∈ t, ∀ j ∈ t, ∀ k ∈ s, i < j → orient (q i) (q j) (p k) < 0) :
    ConvexPosition (s.image p ∪ t.image q) := by
  classical
  let r : ι ⊕ₗ κᵒᵈ → Point := Sum.elim p q
  let u : Finset (ι ⊕ₗ κᵒᵈ) := (s.disjSum (t : Finset κᵒᵈ)).map toLex.toEmbedding
  have hinl (i : ι) : toLex (Sum.inl i : ι ⊕ κᵒᵈ) ∈ u ↔ i ∈ s := by simp [u]
  have hinr (i : κᵒᵈ) : toLex (Sum.inr i : ι ⊕ κᵒᵈ) ∈ u ↔ i ∈ t := by simp [u]
  have hr : Function.Injective r := by
    intro i j he
    rcases i with i | i <;> rcases j with j | j
    · exact congrArg Sum.inl (hp he)
    · exact (hne i j he).elim
    · exact (hne j i he.symm).elim
    · exact congrArg Sum.inr (hq he)
  have hc := convexPosition_of_positive_triples r hr u (by simpa [u] using hcard) (by
    intro i hi j hj k hk hij hjk
    rcases i with i | i <;> rcases j with j | j <;> rcases k with k | k
    · exact hpos i ((hinl i).mp hi) j ((hinl j).mp hj) k ((hinl k).mp hk) (Sum.Lex.inl_lt_inl_iff.mp hij) (Sum.Lex.inl_lt_inl_iff.mp hjk)
    · exact hppq i ((hinl i).mp hi) j ((hinl j).mp hj) k ((hinr k).mp hk) (Sum.Lex.inl_lt_inl_iff.mp hij)
    · exact (Sum.Lex.not_inr_lt_inl hjk).elim
    · have hn := hqqp k ((hinr k).mp hk) j ((hinr j).mp hj) i ((hinl i).mp hi) ((Sum.Lex.inr_lt_inr_iff (α := ι) (β := κᵒᵈ)).mp hjk)
      change 0 < orient (p i) (q j) (q k)
      have he : orient (p i) (q j) (q k) = -orient (q k) (q j) (p i) := by
        simp only [orient]
        ring
      rw [he]
      exact neg_pos.mpr hn
    · exact (Sum.Lex.not_inr_lt_inl hij).elim
    · exact (Sum.Lex.not_inr_lt_inl hij).elim
    · exact (Sum.Lex.not_inr_lt_inl hjk).elim
    · have hn := hneg k ((hinr k).mp hk) j ((hinr j).mp hj) i ((hinr i).mp hi) ((Sum.Lex.inr_lt_inr_iff (α := ι) (β := κᵒᵈ)).mp hjk) ((Sum.Lex.inr_lt_inr_iff (α := ι) (β := κᵒᵈ)).mp hij)
      change 0 < orient (q i) (q j) (q k)
      have he : orient (q i) (q j) (q k) = -orient (q k) (q j) (q i) := by
        simp only [orient]
        ring
      rw [he]
      exact neg_pos.mpr hn)
  have he : u.image r = s.image p ∪ t.image q := by
    ext x
    simp only [Finset.mem_image, Finset.mem_union]
    constructor
    · rintro ⟨i, hi, rfl⟩
      rcases i with i | i
      · exact Or.inl ⟨i, (hinl i).mp hi, rfl⟩
      · exact Or.inr ⟨i, (hinr i).mp hi, rfl⟩
    · rintro (⟨i, hi, rfl⟩ | ⟨i, hi, rfl⟩)
      · exact ⟨toLex (Sum.inl i), (hinl i).mpr hi, rfl⟩
      · exact ⟨toLex (Sum.inr i), (hinr i).mpr hi, rfl⟩
  rwa [he] at hc

end ErdosSzekeres.Suk
