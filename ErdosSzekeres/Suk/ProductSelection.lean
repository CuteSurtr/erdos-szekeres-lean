import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.Finset.Powerset
import Mathlib.Tactic

namespace ErdosSzekeres.Suk

open scoped BigOperators

/-- A prescribed set of small factors bounds the entire product. -/
theorem product_le_of_small_subset {ι : Type*} (I J : Finset ι) (f : ι → ℕ) (B N : ℕ)
    (hJI : J ⊆ I) (hsmall : ∀ i ∈ J, f i ≤ B) (hbound : ∀ i ∈ I, f i ≤ N) :
    (∏ i ∈ I, f i) ≤ B ^ J.card * N ^ (I.card - J.card) := by
  classical
  calc
    (∏ i ∈ I, f i) = (∏ i ∈ J, f i) * ∏ i ∈ I \ J, f i :=
      by rw [mul_comm]; exact (Finset.prod_sdiff hJI).symm
    _ ≤ B ^ J.card * N ^ (I \ J).card :=
      Nat.mul_le_mul (Finset.prod_le_pow_card _ _ _ hsmall)
        (Finset.prod_le_pow_card _ _ _ (fun i hi => hbound i (Finset.mem_sdiff.mp hi).1))
    _ = B ^ J.card * N ^ (I.card - J.card) := by rw [Finset.card_sdiff_of_subset hJI]

/-- A large product forces many factors to exceed a target size. All
quantities are natural numbers; no division or rounding is hidden. -/
theorem many_large_factors {ι : Type*} (I : Finset ι) (f : ι → ℕ) (q B N : ℕ)
    (hq : q ≤ I.card + 1) (hbound : ∀ i ∈ I, f i ≤ N)
    (hprod : B ^ (I.card + 1 - q) * N ^ (q - 1) < ∏ i ∈ I, f i) :
    ∃ J ⊆ I, J.card = q ∧ ∀ i ∈ J, B < f i := by
  classical
  let L := I.filter (fun i => B < f i)
  have hcard : q ≤ L.card := by
    by_contra! hn
    have hL : L ⊆ I := Finset.filter_subset _ _
    have hsmallcard : I.card + 1 - q ≤ (I \ L).card := by
      rw [Finset.card_sdiff_of_subset hL]
      omega
    obtain ⟨J, hJ, hJcard⟩ := Finset.exists_subset_card_eq hsmallcard
    have hJI : J ⊆ I := hJ.trans Finset.sdiff_subset
    have hs : ∀ i ∈ J, f i ≤ B := by
      intro i hi
      obtain ⟨hiI, hiL⟩ := Finset.mem_sdiff.mp (hJ hi)
      by_contra! hg
      exact hiL (Finset.mem_filter.mpr ⟨hiI, hg⟩)
    have hb := product_le_of_small_subset I J f B N hJI hs hbound
    have hexp : I.card - J.card = q - 1 := by omega
    rw [hexp, hJcard] at hb
    omega
  obtain ⟨J, hJL, hJcard⟩ := Finset.exists_subset_card_eq hcard
  exact ⟨J, hJL.trans (Finset.filter_subset _ _), hJcard,
    fun i hi => (Finset.mem_filter.mp (hJL hi)).2⟩

end ErdosSzekeres.Suk
