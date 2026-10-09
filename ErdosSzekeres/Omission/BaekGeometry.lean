/-
Adapted from Michael Schroeder, version-1 archive, 19 September 2026,
DOI 10.5281/zenodo.22842891. MIT, copyright (c) 2026 Michael Schroeder.
See docs/SCHROEDER-MIT.txt. Changes: local namespaces and Lean 4.24 APIs.
-/
import ErdosSzekeres.Omission.BoundaryGeometry
import ErdosSzekeres.Omission.ListGeometry
import ErdosSzekeres.Omission.Baek

namespace ErdosSzekeres.Omission.BaekGeometry
open BoundaryGeometry ListGeometry PlanarChains ActualRanks

noncomputable def arcOfList (p : Nat→Point) (xs : List Nat) (k : Nat) (len : xs.length=k+2)
    (sorted : xs.Pairwise (·<·))
    (ordered : ∀ a∈xs, ∀ b∈xs, a<b → p a 0<p b 0)
    (positive : OrderedTriples (fun a b d => 0<orient (p a) (p b) (p d)) xs) : CupArc k where
  point := fun i => p (xs.get ⟨i.val,by omega⟩)
  xOrder := by
    intro i j hij
    exact ordered _ (xs.get_mem _) _ (xs.get_mem _) (List.Sorted.rel_get_of_lt sorted hij)
  positive := by
    intro i j d hij hjd
    exact positive _ (xs.get_mem _) _ (xs.get_mem _) _ (xs.get_mem _)
      (List.Sorted.rel_get_of_lt sorted hij) (List.Sorted.rel_get_of_lt sorted hjd)

noncomputable def cupArc {n} (c : Configuration n) (xs : List Nat) (k : Nat) (len : xs.length=k+2)
    (inside : xs.In (Finset.range n)) (cup : (colorConfig c.cup true).Cup xs) : CupArc k :=
  arcOfList (pointAt c) xs k len cup.1.pairwise
    (fun a ha b hb ab => pointAt_order c (Finset.mem_range.mp (inside a ha))
      (Finset.mem_range.mp (inside b hb)) ab) (cup_list_all c xs inside cup)

noncomputable def capArc {n} (c : Configuration n) (xs : List Nat) (k : Nat) (len : xs.length=k+2)
    (inside : xs.In (Finset.range n)) (cap : (colorConfig c.cup true).Cap xs) : CupArc k :=
  arcOfList (fun i => reflect (pointAt c i)) xs k len cap.1.pairwise
    (fun a ha b hb ab => pointAt_order c (Finset.mem_range.mp (inside a ha))
      (Finset.mem_range.mp (inside b hb)) ab) (by
        intro a ha b hb d hd ab bd
        rw [orient_reflect]
        exact neg_pos.mpr (cap_list_all c xs inside cap a ha b hb d hd ab bd))

theorem same_first (xs ys : List Nat) (k l : Nat) (hx : xs.length=k+2) (hy : ys.length=l+2)
    (eq : xs.head?=ys.head?) :
    xs.get ⟨0,by omega⟩=ys.get ⟨0,by omega⟩ := by
  rw [List.head?_eq_getElem?,List.head?_eq_getElem?,
    List.getElem?_eq_getElem (by omega),List.getElem?_eq_getElem (by omega)] at eq
  exact Option.some.inj eq

theorem same_last (xs ys : List Nat) (k l : Nat) (hx : xs.length=k+2) (hy : ys.length=l+2)
    (eq : xs.getLast?=ys.getLast?) :
    xs.get ⟨k+1,by omega⟩=ys.get ⟨l+1,by omega⟩ := by
  have xeq : xs.getLast?=some (xs.get ⟨k+1,by omega⟩) := by
    rw [List.getLast?_eq_getElem?]
    simp only [hx,show k+2-1=k+1 by omega]
    exact List.getElem?_eq_getElem (by omega)
  have yeq : ys.getLast?=some (ys.get ⟨l+1,by omega⟩) := by
    rw [List.getLast?_eq_getElem?]
    simp only [hy,show l+2-1=l+1 by omega]
    exact List.getElem?_eq_getElem (by omega)
  rw [xeq,yeq] at eq
  exact Option.some.inj eq

noncomputable def boundaryOfGon {n} (c : Configuration n) (xs ys : List Nat) (k l : Nat)
    (hx : xs.length=k+2) (hy : ys.length=l+2)
    (xi : xs.In (Finset.range n)) (yi : ys.In (Finset.range n))
    (gon : (colorConfig c.cup true).Gon xs ys) : Boundary l k where
  lower := cupArc c ys l hy yi gon.2.2.2.1
  upperReflected := capArc c xs k hx xi gon.2.1
  first_eq := by
    change pointAt c (ys.get ⟨0,by omega⟩)=reflect (reflect (pointAt c (xs.get ⟨0,by omega⟩)))
    rw [reflect_reflect]
    exact congrArg (pointAt c) (same_first xs ys k l hx hy gon.2.2.2.2.1).symm
  last_eq := by
    change pointAt c (ys.get ⟨l+1,by omega⟩)=reflect (reflect (pointAt c (xs.get ⟨k+1,by omega⟩)))
    rw [reflect_reflect]
    exact congrArg (pointAt c) (same_last xs ys k l hx hy gon.2.2.2.2.2).symm

theorem boundaryOfGon_inside {n} (c : Configuration n) (xs ys : List Nat) (k l : Nat)
    (hx : xs.length=k+2) (hy : ys.length=l+2)
    (xi : xs.In (Finset.range n)) (yi : ys.In (Finset.range n))
    (gon : (colorConfig c.cup true).Gon xs ys) :
    (boundaryOfGon c xs ys k l hx hy xi yi gon).points⊆Set.range c.point := by
  intro v hv
  rcases hv with ⟨j,rfl⟩ | ⟨j,rfl⟩
  · change pointAt c (ys.get ⟨j.val,by omega⟩)∈Set.range c.point
    have bound := Finset.mem_range.mp (yi _ (ys.get_mem ⟨j.val,by omega⟩))
    exact ⟨⟨_,bound⟩,(pointAt_eq c _ bound).symm⟩
  · change reflect (reflect (pointAt c (xs.get ⟨j.val,by omega⟩)))∈Set.range c.point
    rw [reflect_reflect]
    have bound := Finset.mem_range.mp (xi _ (xs.get_mem ⟨j.val,by omega⟩))
    exact ⟨⟨_,bound⟩,(pointAt_eq c _ bound).symm⟩

/-- Baek's exact list-boundary predicate implies an actual convex octagon in
Mathlib's real convex-hull sense, with the same ambient points. -/
theorem hasNGon_octagon {n} (c : Configuration n)
    (gon : (colorConfig c.cup true).HasNGon 8 (Finset.range n)) :
    HasConvexNGon 8 (Finset.univ.image c.point) := by
  obtain ⟨xs,ys,hgon,xi,yi⟩ := gon
  let k := xs.length-2
  let l := ys.length-2
  have hx : xs.length=k+2 := by have := hgon.1.1; dsimp [k]; omega
  have hy : ys.length=l+2 := by have := hgon.1.2.2.1; dsimp [l]; omega
  have eight : l+k+2=8 := by have := hgon.2; omega
  have h := boundary_polygon (boundaryOfGon c xs ys k l hx hy xi yi hgon.1)
    (Finset.univ.image c.point) (by
      simpa only [Finset.coe_image, Finset.coe_univ, Set.image_univ] using
        boundaryOfGon_inside c xs ys k l hx hy xi yi hgon.1)
  simpa only [eight] using h

/-- The 23-point four-cap/octagon theorem on any induced subset of the actual
configuration. Its octagon premise is geometric, not a Config placeholder. -/
theorem geometric_capacity22 {n} (c : Configuration n) (S : Finset Nat)
    (inside : S⊆Finset.range n) (noCap : ¬(colorConfig c.cup true).HasNCap 4 S)
    (noOctagon : ¬HasConvexNGon 8 (Finset.univ.image c.point)) : S.card≤22 := by
  apply Baek.capacity22 (colorConfig c.cup true) S noCap
  intro gon
  obtain ⟨xs,ys,hgon,xi,yi⟩ := gon
  apply noOctagon
  apply hasNGon_octagon c
  exact ⟨xs,ys,hgon,fun a ha=>inside (xi a ha),fun a ha=>inside (yi a ha)⟩

end ErdosSzekeres.Omission.BaekGeometry
