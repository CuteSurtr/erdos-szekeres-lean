import Capacity16

/-! Draft n=6 specialization; not checked until its separate replay passes. -/

namespace Delta3.LowSplitCapacity

open ErdosSzekeres ErdosSzekeres.Omission
open ErdosSzekeres.Omission.ActualRanks
open ErdosSzekeres.Omission.ListGeometry

theorem four_cap_or_six_gon {α : Type*} [LinearOrder α]
    (C : Config α) (S : Finset α) (size : 12 ≤ S.card) :
    C.HasNCap 4 S ∨ C.HasNGon 6 S := by
  exact _root_.main 3 C S (by norm_num; exact size)

theorem geometric_capacity11 {n : ℕ} (c : Configuration n)
    (noCap : ¬c.HasCap 4)
    (noGon : ¬HasConvexNGon 6 (Finset.univ.image c.point)) : n ≤ 11 := by
  by_contra hn
  have size : 12 ≤ (Finset.range n).card := by
    simpa only [Finset.card_range] using (show 12 ≤ n by omega)
  rcases four_cap_or_six_gon (colorConfig c.cup true) (Finset.range n) size with h | h
  · exact noCap (hasCap_of_list c h)
  · exact noGon (hasNGon_real c h)

#print axioms four_cap_or_six_gon
#print axioms geometric_capacity11

end Delta3.LowSplitCapacity
