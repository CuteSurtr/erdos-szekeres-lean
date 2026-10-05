import ErdosSzekeres.HMPT.ProjectedCaps
import ErdosSzekeres.Suk.AlternatingAnchors
import ErdosSzekeres.Suk.ExtractionCounting

namespace ErdosSzekeres.HMPT

open Suk

/-- Increasing horizontal enumerations of the same finite point set agree. -/
theorem ordered_points_unique {m : ℕ} (p q : Fin m → Point)
    (hp : StrictMono (fun i => p i 0)) (hq : StrictMono (fun i => q i 0))
    (heq : Finset.univ.image p = Finset.univ.image q) : p = q := by
  classical
  have hcoord : (fun i => p i 0) = (fun i => q i 0) := by
    apply (hp.range_inj hq).mp
    have h := congrArg (fun s : Finset Point => (↑(s.image (fun x => x 0)) : Set ℝ)) heq
    simpa only [Finset.image_image, Function.comp_def, Finset.coe_image,
      Finset.coe_univ, Set.image_univ] using h
  funext i
  have hm : p i ∈ Finset.univ.image q := heq ▸ Finset.mem_image_of_mem p (Finset.mem_univ i)
  obtain ⟨j, _, hj⟩ := Finset.mem_image.mp hm
  have hji : j = i := hq.injective ((congrArg (fun x : Point => x 0) hj).trans (congrFun hcoord i))
  subst j
  exact hj.symm

/-- A convex polygon represented by its leftmost vertex and the remaining
vertices in ray-slope order. Projection turns those vertices into a cap. -/
structure ConvexFan (m : ℕ) where
  anchor : Point
  point : Fin m → Point
  right : ∀ i, anchor 0 < point i 0
  mono : StrictMono (fun i => projectFrom anchor (point i) 0)
  clockwise : ∀ i j k, i < j → j < k →
    orient (projectFrom anchor (point i)) (projectFrom anchor (point j))
      (projectFrom anchor (point k)) < 0
  convex : ConvexPosition (insert anchor (Finset.univ.image point))

@[ext] theorem ConvexFan.ext {m : ℕ} {C D : ConvexFan m}
    (ha : C.anchor = D.anchor) (hp : C.point = D.point) : C = D := by
  cases C
  cases D
  cases ha
  cases hp
  rfl

noncomputable def ConvexFan.vertices {m : ℕ} (C : ConvexFan m) : Finset Point :=
  insert C.anchor (Finset.univ.image C.point)

noncomputable def ConvexFan.projected {m : ℕ} (C : ConvexFan m) (i : Fin m) : Point :=
  projectFrom C.anchor (C.point i)

noncomputable def ConvexFan.projectedAnchors {m : ℕ} (C : ConvexFan m) : ClockwiseAnchors m :=
  ⟨C.projected, C.clockwise⟩

theorem ConvexFan.point_injective {m : ℕ} (C : ConvexFan m) : Function.Injective C.point := by
  intro i j h
  exact C.mono.injective (congrArg (fun p : Point => projectFrom C.anchor p 0) h)

theorem ConvexFan.anchor_not_mem_image {m : ℕ} (C : ConvexFan m) :
    C.anchor ∉ Finset.univ.image C.point := by
  classical
  rintro h
  obtain ⟨i, _, hi⟩ := Finset.mem_image.mp h
  exact (C.right i).ne (congrArg (fun p : Point => p 0) hi.symm)

theorem ConvexFan.card_vertices {m : ℕ} (C : ConvexFan m) : C.vertices.card = m + 1 := by
  classical
  simp [vertices, C.anchor_not_mem_image, Finset.card_image_of_injective _ C.point_injective]

theorem ConvexFan.anchor_mem {m : ℕ} (C : ConvexFan m) : C.anchor ∈ C.vertices := by
  classical
  exact Finset.mem_insert_self _ _

theorem ConvexFan.point_mem {m : ℕ} (C : ConvexFan m) (i : Fin m) : C.point i ∈ C.vertices := by
  classical
  exact Finset.mem_insert_of_mem (Finset.mem_image_of_mem C.point (Finset.mem_univ i))

theorem ConvexFan.anchor_le {m : ℕ} (C : ConvexFan m) {p : Point} (hp : p ∈ C.vertices) :
    C.anchor 0 ≤ p 0 := by
  classical
  rcases Finset.mem_insert.mp hp with rfl | hp
  · exact le_rfl
  · obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hp
    exact (C.right i).le

theorem ConvexFan.eq_of_anchor_projected_eq {m : ℕ} {C D : ConvexFan m}
    (ha : C.anchor = D.anchor) (hp : C.projected = D.projected) : C = D := by
  apply ConvexFan.ext ha
  funext i
  apply projectFrom_injOn D.anchor (ha ▸ C.right i) (D.right i)
  simpa only [ConvexFan.projected, ha] using congrFun hp i

/-- The vertex set uniquely determines both the projection anchor and the
ordered fan. Thus an anchor subset cannot carry extra hidden ordering choices. -/
theorem ConvexFan.vertices_injective (m : ℕ) : Function.Injective (@ConvexFan.vertices m) := by
  classical
  intro C D he
  have ha : C.anchor = D.anchor := by
    have hle := D.anchor_le (he ▸ C.anchor_mem)
    have hm : D.anchor ∈ C.vertices := he.symm ▸ D.anchor_mem
    rcases Finset.mem_insert.mp hm with hm | hm
    · exact hm.symm
    · obtain ⟨i, _, hi⟩ := Finset.mem_image.mp hm
      have hr := C.right i
      rw [hi] at hr
      exact (not_lt_of_ge hle hr).elim
  have hpoints : Finset.univ.image C.point = Finset.univ.image D.point := by
    have h := congrArg (fun s : Finset Point => s.erase C.anchor) he
    have hnot : D.anchor ∉ Finset.univ.image C.point := ha ▸ C.anchor_not_mem_image
    simpa only [ConvexFan.vertices, ha,
      Finset.erase_insert hnot, Finset.erase_insert D.anchor_not_mem_image] using h
  have hproj : C.projected = D.projected := by
    apply ordered_points_unique _ _ C.mono D.mono
    have h := congrArg (Finset.image (projectFrom C.anchor)) hpoints
    simpa only [Finset.image_image, Function.comp_def, ConvexFan.projected, ha] using h
  exact ConvexFan.eq_of_anchor_projected_eq ha hproj

/-- Alternating vertices together with the same projection anchor form a
smaller convex fan, with the inherited canonical order. -/
def ConvexFan.even {m : ℕ} (C : ConvexFan (2 * m)) : ConvexFan m where
  anchor := C.anchor
  point := evenVertices C.point
  right i := C.right _
  mono i j hij := C.mono (by change 2 * i.val < 2 * j.val; omega)
  clockwise i j k hij hjk := C.clockwise _ _ _
    (by change 2 * i.val < 2 * j.val; omega)
    (by change 2 * j.val < 2 * k.val; omega)
  convex := C.convex.mono (Finset.insert_subset_insert C.anchor (by
    intro p hp
    obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hp
    exact Finset.mem_image_of_mem C.point (Finset.mem_univ _)))

theorem ConvexFan.even_vertices_subset {m : ℕ} (C : ConvexFan (2 * m)) :
    C.even.vertices ⊆ C.vertices := by
  classical
  apply Finset.insert_subset_insert C.anchor
  intro p hp
  obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hp
  exact Finset.mem_image_of_mem C.point (Finset.mem_univ _)

/-- Every convex subset of an x-distinct general-position set has a convex
fan representation with exactly its original vertices. -/
theorem exists_convexFan {S : Finset Point} {m : ℕ}
    (hgp : GeneralPosition S) (hconv : ConvexPosition S) (hcard : S.card = m + 1)
    (hdist : ∀ p ∈ S, ∀ q ∈ S, p 0 = q 0 → p = q) :
    ∃ C : ConvexFan m, C.vertices = S := by
  classical
  obtain ⟨a, ha, hmin⟩ := Finset.exists_min_image S (fun p => p 0)
    (Finset.card_pos.mp (by omega))
  have hx : ∀ p ∈ S.erase a, a 0 < p 0 := by
    intro p hp
    obtain ⟨hpa, hpS⟩ := Finset.mem_erase.mp hp
    apply lt_of_le_of_ne (hmin p hpS)
    intro he
    exact hpa (hdist p hpS a ha he.symm)
  have herase : (S.erase a).card = m := by rw [Finset.card_erase_of_mem ha, hcard]; omega
  have h := exists_projected_cap (S := S.erase a) a
    (by simpa only [Finset.insert_erase ha] using hgp)
    (by simpa only [Finset.insert_erase ha] using hconv) hx
  have h' : ∃ p : Fin m → Point, Finset.univ.image p = S.erase a ∧ Function.Injective p ∧
      StrictMono (fun i => projectFrom a (p i) 0) ∧
      ∀ i j k, i < j → j < k →
        orient (projectFrom a (p i)) (projectFrom a (p j)) (projectFrom a (p k)) < 0 := by
    rw [← herase]
    exact h
  obtain ⟨p, hp, _, hmono, hc⟩ := h'
  let C : ConvexFan m := {
    anchor := a
    point := p
    right := fun i => hx (p i) (hp ▸ Finset.mem_image_of_mem p (Finset.mem_univ i))
    mono := hmono
    clockwise := hc
    convex := by rw [hp, Finset.insert_erase ha]; exact hconv }
  refine ⟨C, ?_⟩
  change insert a (Finset.univ.image p) = S
  rw [hp, Finset.insert_erase ha]

/-- Enumerating all convex subsets as fans preserves the family cardinality. -/
theorem exists_convexFan_family (S : Finset Point) (m : ℕ) (hgp : GeneralPosition S)
    (hdist : ∀ p ∈ S, ∀ q ∈ S, p 0 = q 0 → p = q) :
    ∃ F : Finset (ConvexFan m), F.card = (convexSubsets S (m + 1)).card ∧
      ∀ C ∈ F, C.vertices ⊆ S := by
  classical
  let U := convexSubsets S (m + 1)
  have h (u : U) : ∃ C : ConvexFan m, C.vertices = u.val :=
    exists_convexFan (hgp.mono (mem_convexSubsets.mp u.property).1)
      (mem_convexSubsets.mp u.property).2.2 (mem_convexSubsets.mp u.property).2.1
      (fun p hp q hq => hdist p ((mem_convexSubsets.mp u.property).1 hp)
        q ((mem_convexSubsets.mp u.property).1 hq))
  choose f hf using h
  have hinj : Function.Injective f := by
    intro u v he
    apply Subtype.ext
    rw [← hf u, ← hf v, he]
  refine ⟨U.attach.image f, ?_, ?_⟩
  · rw [Finset.card_image_of_injective _ hinj, Finset.card_attach]
  · intro C hC
    obtain ⟨u, _, rfl⟩ := Finset.mem_image.mp hC
    rw [hf]
    exact (mem_convexSubsets.mp u.property).1

end ErdosSzekeres.HMPT
