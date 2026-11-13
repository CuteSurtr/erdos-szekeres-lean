import ErdosSzekeres.Suk.SupportFiber
import ErdosSzekeres.Suk.SupportCoarsening
import ErdosSzekeres.Suk.ProductSelection

namespace ErdosSzekeres.Suk

open scoped BigOperators

/-- A sufficiently large family of clockwise horizontal configurations
forces a populated support sequence. The bound accounts explicitly for
anchor choices and three uncontrolled alternating endpoint vertices. -/
theorem rich_support_of_dense_caps {m k B : ℕ} (S : Finset Point)
    (F : Finset (Fin (2 * (m + 3)) → Point)) (hkm : k + 2 ≤ m)
    (hpoints : ∀ p ∈ F, ∀ i, p i ∈ S)
    (hmono : ∀ p ∈ F, StrictMono (fun i => p i 0))
    (hclockwise : ∀ p ∈ F, ∀ i j l, i < j → j < l → orient (p i) (p j) (p l) < 0)
    (hsize : S.card ^ (m + 3) * (S.card ^ 3 *
      (B ^ (m - k - 2) * S.card ^ (k + 2))) < F.card) :
    ∃ (C : ClockwiseAnchors (k + 3)) (R : Fin k → Finset Point),
      StrictMono (fun i => C.point i 0) ∧ (∀ i, C.point i ∈ S) ∧
      (∀ i, R i ⊆ S) ∧ (∀ i, ∀ p ∈ R i, p ∈ (C.frame i).spike) ∧
      ∀ i, B < (R i).card := by
  classical
  obtain ⟨a, _, hlarge⟩ := exists_large_alternating_fiber S F hpoints hsize
  let G := F.filter (fun p => evenVertices p = a)
  obtain ⟨p, hp⟩ := Finset.card_pos.mp (show 0 < G.card from (Nat.zero_le _).trans_lt hlarge)
  have hpF := (Finset.mem_filter.mp hp).1
  let C : ClockwiseAnchors (2 * (m + 3)) := ⟨p, hclockwise p hpF⟩
  let A := C.even
  have hbound := support_fiber_card_le S A G
    (fun q hq => hpoints q (Finset.mem_filter.mp hq).1)
    (fun q hq => (Finset.mem_filter.mp hq).2.trans (Finset.mem_filter.mp hp).2.symm)
    (fun q hq => hclockwise q (Finset.mem_filter.mp hq).1)
  let sizes : Fin m → ℕ := fun i => ((A.frame i).region S).card
  have hprod : B ^ (m - k - 2) * S.card ^ (k + 2) < ∏ i, sizes i :=
    lt_of_mul_lt_mul_left (hlarge.trans_le hbound) (Nat.zero_le _)
  have hsizes : ∀ i ∈ (Finset.univ : Finset (Fin m)), sizes i ≤ S.card := by
    intro i _
    exact Finset.card_le_card ((A.frame i).region_subset S)
  obtain ⟨I, _, hI, hrich⟩ := many_large_factors Finset.univ sizes (k + 3) B S.card
    (by simpa using hkm) hsizes (by simpa [Nat.sub_sub, Nat.add_sub_add_right] using hprod)
  apply A.extract_rich_spikes (Q := fun i => (A.frame i).region S) (I := I)
  · intro i j hij
    apply hmono p hpF
    change 2 * i.val < 2 * j.val
    omega
  · exact hI.ge
  · intro i
    exact hpoints p hpF _
  · intro i _
    exact (A.frame i).region_subset S
  · intro i _ q hq
    exact ((A.frame i).mem_region S q).mp hq |>.2
  · exact hrich

end ErdosSzekeres.Suk
