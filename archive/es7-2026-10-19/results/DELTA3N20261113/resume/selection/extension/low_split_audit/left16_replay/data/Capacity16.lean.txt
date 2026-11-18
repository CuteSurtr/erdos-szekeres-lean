import ErdosSzekeres.Omission.BaekGeometry

/-! Draft specialization of the existing Baek bound and its geometric bridge.
Not part of a checked claim until the separately recorded bounded replay passes. -/

namespace Delta3.LowSplitCapacity

open ErdosSzekeres ErdosSzekeres.Omission
open ErdosSzekeres.Omission.ActualRanks
open ErdosSzekeres.Omission.BaekGeometry
open ErdosSzekeres.Omission.BoundaryGeometry
open ErdosSzekeres.Omission.ListGeometry

theorem four_cap_or_seven_gon {α : Type*} [LinearOrder α]
    (C : Config α) (S : Finset α) (size : 17 ≤ S.card) :
    C.HasNCap 4 S ∨ C.HasNGon 7 S := by
  exact _root_.main 4 C S (by norm_num; exact size)

/-- The existing boundary construction works at every cardinality. -/
theorem hasNGon_real {n q : ℕ} (c : Configuration n)
    (gon : (colorConfig c.cup true).HasNGon q (Finset.range n)) :
    HasConvexNGon q (Finset.univ.image c.point) := by
  obtain ⟨xs, ys, hgon, xi, yi⟩ := gon
  let k := xs.length - 2
  let l := ys.length - 2
  have hx : xs.length = k + 2 := by have := hgon.1.1; dsimp [k]; omega
  have hy : ys.length = l + 2 := by have := hgon.1.2.2.1; dsimp [l]; omega
  have count : l + k + 2 = q := by have := hgon.2; omega
  have h := boundary_polygon (boundaryOfGon c xs ys k l hx hy xi yi hgon.1)
    (Finset.univ.image c.point) (by
      simpa only [Finset.coe_image, Finset.coe_univ, Set.image_univ] using
        boundaryOfGon_inside c xs ys k l hx hy xi yi hgon.1)
  simpa only [count] using h

/-- A genuine ordered real configuration without a four-cap or heptagon
has at most sixteen points. This is a specialization, not a new bound. -/
theorem geometric_capacity16 {n : ℕ} (c : Configuration n)
    (noCap : ¬c.HasCap 4)
    (noGon : ¬HasConvexNGon 7 (Finset.univ.image c.point)) : n ≤ 16 := by
  by_contra hn
  have size : 17 ≤ (Finset.range n).card := by
    simpa only [Finset.card_range] using (show 17 ≤ n by omega)
  rcases four_cap_or_seven_gon (colorConfig c.cup true) (Finset.range n) size with h | h
  · exact noCap (hasCap_of_list c h)
  · exact noGon (hasNGon_real c h)

#print axioms four_cap_or_seven_gon
#print axioms hasNGon_real
#print axioms geometric_capacity16

end Delta3.LowSplitCapacity
