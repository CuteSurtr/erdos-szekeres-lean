import ErdosSzekeres.HMPT.Projective
import ErdosSzekeres.Suk.SupportSequence
import Mathlib.Data.Finset.Sort
import Mathlib.Data.Finset.Max

namespace ErdosSzekeres.HMPT

open Suk

theorem projectFrom_x_diff (a p q : Point)
    (hp : p 0 - a 0 ≠ 0) (hq : q 0 - a 0 ≠ 0) :
    projectFrom a q 0 - projectFrom a p 0 =
      orient a p q / ((p 0 - a 0) * (q 0 - a 0)) := by
  simp only [projectFrom, Matrix.cons_val_zero, orient]
  field_simp

theorem projectFrom_x_lt_iff (a p q : Point) (hp : a 0 < p 0) (hq : a 0 < q 0) :
    projectFrom a p 0 < projectFrom a q 0 ↔ 0 < orient a p q := by
  rw [← sub_pos, projectFrom_x_diff a p q (sub_ne_zero.mpr hp.ne') (sub_ne_zero.mpr hq.ne'),
    div_pos_iff_of_pos_right (mul_pos (sub_pos.mpr hp) (sub_pos.mpr hq))]

/-- No two rays from the anchor have the same slope in general position. -/
theorem projectFrom_distinct_x {S : Finset Point} (a : Point)
    (hgp : GeneralPosition (insert a S)) (hx : ∀ p ∈ S, a 0 < p 0)
    {p q : Point} (hp : p ∈ S) (hq : q ∈ S) (hpq : p ≠ q) :
    projectFrom a p 0 ≠ projectFrom a q 0 := by
  intro he
  have hdet := projectFrom_x_diff a p q (sub_ne_zero.mpr (hx p hp).ne')
    (sub_ne_zero.mpr (hx q hq).ne')
  rw [he, sub_self] at hdet
  have horient : orient a p q = 0 :=
    (div_eq_zero_iff.mp hdet.symm).resolve_right
      (mul_ne_zero (sub_ne_zero.mpr (hx p hp).ne') (sub_ne_zero.mpr (hx q hq).ne'))
  exact (generalPosition_iff_orient_ne_zero _).mp hgp a (by simp) p
    (Finset.mem_insert_of_mem hp) q (Finset.mem_insert_of_mem hq)
    (fun he => (hx p hp).ne (congrArg (fun z : Point => z 0) he))
    (fun he => (hx q hq).ne (congrArg (fun z : Point => z 0) he)) hpq horient

/-- A convex fan projects to clockwise triples when ordered by ray slope. -/
theorem projected_fan_clockwise {S : Finset Point} (a : Point)
    (hgp : GeneralPosition (insert a S)) (hconv : ConvexPosition (insert a S))
    (hx : ∀ p ∈ S, a 0 < p 0)
    {p q r : Point} (hp : p ∈ S) (hq : q ∈ S) (hr : r ∈ S)
    (hpq : projectFrom a p 0 < projectFrom a q 0)
    (hqr : projectFrom a q 0 < projectFrom a r 0) :
    orient (projectFrom a p) (projectFrom a q) (projectFrom a r) < 0 := by
  have hne (u v : Point) (h : projectFrom a u 0 < projectFrom a v 0) : u ≠ v := by
    rintro rfl
    exact lt_irrefl _ h
  have hg := (generalPosition_iff_orient_ne_zero _).mp hgp p (Finset.mem_insert_of_mem hp)
    q (Finset.mem_insert_of_mem hq) r (Finset.mem_insert_of_mem hr)
    (hne _ _ hpq) (hne _ _ (hpq.trans hqr)) (hne _ _ hqr)
  have hpa : 0 < orient p q a := by
    rw [orient_cycle a p q]
    exact (projectFrom_x_lt_iff a p q (hx p hp) (hx q hq)).mp hpq
  have hpb : 0 < orient p r a := by
    rw [orient_cycle a p r]
    exact (projectFrom_x_lt_iff a p r (hx p hp) (hx r hr)).mp (hpq.trans hqr)
  have hpc : 0 < orient q r a := by
    rw [orient_cycle a q r]
    exact (projectFrom_x_lt_iff a q r (hx q hq) (hx r hr)).mp hqr
  apply (orient_projectFrom_neg_iff a p q r (hx p hp) (hx q hq) (hx r hr)).mpr
  apply (convexPosition_four_iff_positive_of_anchor p q r a hg hpa hpb hpc).mp
  exact hconv.mono (by simp [Finset.insert_subset_iff, hp, hq, hr])

/-- Enumerate the remaining vertices of a convex polygon so that their
projective images form an actual clockwise horizontal cap. All vertices are
retained; no large-cup/cap extraction or loss of half the polygon is used. -/
theorem exists_projected_cap {S : Finset Point} (a : Point)
    (hgp : GeneralPosition (insert a S)) (hconv : ConvexPosition (insert a S))
    (hx : ∀ p ∈ S, a 0 < p 0) :
    ∃ p : Fin S.card → Point,
      Finset.univ.image p = S ∧ Function.Injective p ∧
      StrictMono (fun i => projectFrom a (p i) 0) ∧
      ∀ i j k, i < j → j < k →
        orient (projectFrom a (p i)) (projectFrom a (p j)) (projectFrom a (p k)) < 0 := by
  classical
  let X := S.image (fun p => projectFrom a p 0)
  have hinj : Set.InjOn (fun p => projectFrom a p 0) (S : Set Point) := by
    intro p hp q hq he
    by_contra hne
    exact projectFrom_distinct_x a hgp hx hp hq hne he
  have hc : X.card = S.card := Finset.card_image_of_injOn hinj
  let e := X.orderEmbOfFin hc
  have hget (i : Fin S.card) : ∃ p ∈ S, projectFrom a p 0 = e i :=
    Finset.mem_image.mp (Finset.orderEmbOfFin_mem X hc i)
  choose p hmem he using hget
  have heq : (fun i => projectFrom a (p i) 0) = e := funext he
  have hmono : StrictMono (fun i => projectFrom a (p i) 0) := by
    rw [heq]
    exact e.strictMono
  have hp : Function.Injective p := by
    intro i j he
    exact hmono.injective (congrArg (fun z : Point => projectFrom a z 0) he)
  refine ⟨p, ?_, hp, hmono, ?_⟩
  · apply Finset.eq_of_subset_of_card_le
    · intro q hq
      obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hq
      exact hmem i
    · simp [Finset.card_image_of_injective _ hp]
  · intro i j k hij hjk
    exact projected_fan_clockwise a hgp hconv hx (hmem i) (hmem j) (hmem k)
      (hmono hij) (hmono hjk)

end ErdosSzekeres.HMPT
