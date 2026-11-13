/-
Adapted from Michael Schroeder, version-1 archive, 19 September 2026,
DOI 10.5281/zenodo.22842891, ES8SlopePartition.lean.
Code: MIT, copyright (c) 2026 Michael Schroeder; see docs/SCHROEDER-MIT.txt.
Changes: real points as Fin 2 → ℝ, local geometry and namespaces, Lean 4.24.
-/
import ErdosSzekeres.Omission.MinimumSlope
import ErdosSzekeres.Omission.Subsets

namespace ErdosSzekeres.Omission.SlopePartition
open ActualRanks MinimumSlope Subsets

noncomputable def upper {n} {c : Configuration n} (m : MinNeighbors c) : Finset (Fin n) :=
  Finset.univ.filter (fun u=>u<m.neighbor u)
noncomputable def lower {n} {c : Configuration n} (m : MinNeighbors c) : Finset (Fin n) :=
  Finset.univ.filter (fun u=>m.neighbor u<u)

theorem upper_mem {n} {c : Configuration n} (m : MinNeighbors c) (u : Fin n) :
    u∈upper m ↔ u<m.neighbor u := by simp [upper]
theorem lower_mem {n} {c : Configuration n} (m : MinNeighbors c) (u : Fin n) :
    u∈lower m ↔ m.neighbor u<u := by simp [lower]

theorem partition_cover {n} {c : Configuration n} (m : MinNeighbors c) : upper m∪lower m=Finset.univ := by
  ext u
  simp only [Finset.mem_union,upper_mem,lower_mem,Finset.mem_univ,iff_true]
  exact (lt_or_gt_of_ne (m.different u)).symm

theorem partition_disjoint {n} {c : Configuration n} (m : MinNeighbors c) : Disjoint (upper m) (lower m) := by
  apply Finset.disjoint_left.mpr
  intro u hu hl
  exact lt_asymm ((upper_mem m u).mp hu) ((lower_mem m u).mp hl)

theorem natSet_bounded {n} (S : Finset (Fin n)) : natSet S⊆Finset.range n := by
  intro u hu
  obtain ⟨v,_,rfl⟩ := Finset.mem_image.mp hu
  exact Finset.mem_range.mpr v.isLt

theorem natSet_member {n} (S : Finset (Fin n)) (u : Fin n) : u.val∈natSet S ↔ u∈S := by
  constructor
  · intro h; obtain ⟨v,hv,eq⟩ := Finset.mem_image.mp h
    have he : v=u := Fin.ext eq
    simpa only [he] using hv
  · exact fun h=>Finset.mem_image.mpr ⟨u,h,rfl⟩

theorem split_last_two (xs : List Nat) (len : 2≤xs.length) : ∃ ys u v, xs=ys++[u,v] := by
  induction xs using List.reverseRecOn with
  | nil => simp at len
  | append_singleton ys v ih =>
    induction ys using List.reverseRecOn with
    | nil => simp at len
    | append_singleton zs u ih' => exact ⟨zs,u,v,by simp⟩

/-- Recover an attained ending path from its exact concrete cup/cap list. -/
theorem ending_of_cup (cup : Nat→Nat→Nat→Bool) (color : Bool) (xs : List Nat) (u v : Nat)
    (chain : (colorConfig cup color).Cup (xs++[u,v])) : EndingPath cup color u v (xs.length+2) := by
  induction xs using List.reverseRecOn generalizing u v with
  | nil => exact .pair (by simpa using chain.1)
  | append_singleton xs t ih =>
    have chain' : (colorConfig cup color).Cup (xs++[t,u,v]) := by simpa using chain
    have parts := Config.Cup.append_cons3.mp chain'
    have path := ih t u parts.1
    have uv : u<v := by simpa using parts.2.2.1
    have result := EndingPath.step path uv parts.2.1
    simpa [Nat.add_assoc] using result

theorem upper_no_six_cap {n} {c : Configuration n} (m : MinNeighbors c)
    (noCap : ¬(colorConfig c.cup true).HasNCap 7 (Finset.range n)) :
    ¬(colorConfig c.cup true).HasNCap 6 (natSet (upper m)) := by
  rintro ⟨xs,⟨chain,len⟩,inside⟩
  obtain ⟨ys,u,v,rfl⟩ := split_last_two xs (by omega)
  have cup := (false_cup_iff_cap c.cup _).mpr chain
  have path := ending_of_cup c.cup false ys u v cup
  have uv := (length_bounds path).2.2
  have vm := inside v (by simp)
  have vn := Finset.mem_range.mp (natSet_bounded (upper m) vm)
  have un : u<n := by omega
  let vf : Fin n := ⟨v,vn⟩
  let uf : Fin n := ⟨u,un⟩
  have vr : vf<m.neighbor vf := (upper_mem m vf).mp ((natSet_member (upper m) vf).mp vm)
  have negative := cap_to_right m uf vf uv vr
  have color : c.cup u v (m.neighbor vf).val=false := by
    cases he : c.cup u v (m.neighbor vf).val with
    | false => rfl
    | true =>
      have positive := (c.cup_true_iff uf vf (m.neighbor vf)).mp he
      linarith
  have extended := EndingPath.step path vr color
  have length : ys.length+2+1=7 := by simpa using congrArg (fun x : Nat=>x+1) len
  rw [length] at extended
  exact avoids_of_no_cap n 7 c.cup noCap v (m.neighbor vf) (m.neighbor vf).isLt extended

theorem lower_no_seven_cup {n} {c : Configuration n} (m : MinNeighbors c)
    (noOctagon : ¬HasConvexNGon 8 (Finset.univ.image c.point)) :
    ¬(colorConfig c.cup true).HasNCup 7 (natSet (lower m)) := by
  rintro ⟨xs,⟨chain,len⟩,inside⟩
  cases xs with
  | nil => simp at len
  | cons u xs =>
    cases xs with
    | nil => simp at len
    | cons v xs =>
      have uv := (List.isChain_cons_cons.mp chain.1).1
      have um := inside u (by simp)
      have vm := inside v (by simp)
      have un := Finset.mem_range.mp (natSet_bounded (lower m) um)
      have vn := Finset.mem_range.mp (natSet_bounded (lower m) vm)
      let uf : Fin n := ⟨u,un⟩
      let vf : Fin n := ⟨v,vn⟩
      have ul : m.neighbor uf<uf := (lower_mem m uf).mp ((natSet_member (lower m) uf).mp um)
      have positive := cup_from_left m uf vf uv ul
      have color := (c.cup_true_iff (m.neighbor uf) uf vf).mpr positive
      have extended : (colorConfig c.cup true).Cup ((m.neighbor uf).val::u::v::xs) :=
        ⟨List.isChain_cons_cons.mpr ⟨ul,chain.1⟩,List.chain3'_cons.mpr ⟨color,chain.2⟩⟩
      apply noOctagon
      apply ListGeometry.hasNCup_octagon c
      refine ⟨(m.neighbor uf).val::u::v::xs,⟨extended,by simpa using congrArg (fun x : Nat=>x+1) len⟩,?_⟩
      intro a ha
      rcases List.mem_cons.mp ha with rfl | ha
      · exact Finset.mem_range.mpr (m.neighbor uf).isLt
      · exact natSet_bounded (lower m) (inside a ha)

noncomputable def junctions {n} {c : Configuration n} (m : MinNeighbors c) : Finset (Fin n) := by
  classical
  exact (upper m).filter (fun u=>JunctionOn c.cup (natSet (upper m)) u.val)

noncomputable def residualPart {n} {c : Configuration n} (m : MinNeighbors c) := upper m\junctions m
noncomputable def balancedPart {n} {c : Configuration n} (m : MinNeighbors c) := lower m∪junctions m

theorem natSet_mono {n} {S T : Finset (Fin n)} (h : S⊆T) : natSet S⊆natSet T := Finset.image_subset_image h

theorem junction_mono (cup : Nat→Nat→Nat→Bool) {S T : Finset Nat} (hST : S⊆T)
    (u : Nat) (h : JunctionOn cup S u) : JunctionOn cup T u := by
  obtain ⟨xs,ys,a,b,xlen,ylen,xchain,ychain,xinside,yinside⟩ := h
  exact ⟨xs,ys,a,b,xlen,ylen,xchain,ychain,fun p hp=>hST (xinside p hp),fun p hp=>hST (yinside p hp)⟩

theorem junction_owner_mem (cup : Nat→Nat→Nat→Bool) (S : Finset Nat) (u : Nat)
    (h : JunctionOn cup S u) : u∈S := by
  obtain ⟨xs,ys,a,b,_,_,_,_,inside,_⟩ := h
  exact inside u (by simp)

theorem junctions_subset {n} {c : Configuration n} (m : MinNeighbors c) : junctions m⊆upper m := by
  classical
  exact Finset.filter_subset _ _

theorem residual_subset {n} {c : Configuration n} (m : MinNeighbors c) : residualPart m⊆upper m :=
  Finset.sdiff_subset

theorem residual_no_junction {n} {c : Configuration n} (m : MinNeighbors c) :
    NoJunctionOn c.cup (natSet (residualPart m)) := by
  classical
  intro u h
  obtain ⟨v,hv,eq⟩ := Finset.mem_image.mp (junction_owner_mem c.cup _ u h)
  have inUpper := (Finset.mem_sdiff.mp hv).1
  have notJunction := (Finset.mem_sdiff.mp hv).2
  apply notJunction
  apply Finset.mem_filter.mpr
  refine ⟨inUpper,?_⟩
  rw [eq]
  exact junction_mono c.cup (natSet_mono (residual_subset m)) u h

theorem residual_no_six_cap {n} {c : Configuration n} (m : MinNeighbors c)
    (noCap : ¬(colorConfig c.cup true).HasNCap 7 (Finset.range n)) :
    ¬(colorConfig c.cup true).HasNCap 6 (natSet (residualPart m)) := by
  rintro ⟨xs,hcap,inside⟩
  exact upper_no_six_cap m noCap ⟨xs,hcap,fun u hu=>natSet_mono (residual_subset m) (inside u hu)⟩

theorem parts_cover {n} {c : Configuration n} (m : MinNeighbors c) :
    balancedPart m∪residualPart m=Finset.univ := by
  classical
  ext u
  have covered : u∈upper m ∨ u∈lower m := by
    have := Finset.mem_univ u
    rw [←partition_cover m,Finset.mem_union] at this
    exact this
  simp only [balancedPart,residualPart,Finset.mem_union,Finset.mem_sdiff,Finset.mem_univ,iff_true]
  tauto

theorem balanced_no_seven_cap {n} {c : Configuration n} (m : MinNeighbors c)
    (noCap : ¬(colorConfig c.cup true).HasNCap 7 (Finset.range n)) :
    ¬(colorConfig c.cup true).HasNCap 7 (natSet (balancedPart m)) := by
  rintro ⟨xs,hcap,inside⟩
  exact noCap ⟨xs,hcap,fun u hu=>natSet_bounded _ (inside u hu)⟩


end ErdosSzekeres.Omission.SlopePartition
