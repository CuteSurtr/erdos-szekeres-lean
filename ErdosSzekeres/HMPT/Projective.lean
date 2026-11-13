import ErdosSzekeres.Suk.Quadrilateral
import ErdosSzekeres.Suk.FourPoint

namespace ErdosSzekeres.HMPT

open Suk

/-- Project from `a` onto a chart with horizontal coordinate equal to the
ray slope. The domain used below is the open halfplane to the right of `a`.
The negative reciprocal makes convex fans become clockwise horizontal caps. -/
noncomputable def projectFrom (a p : Point) : Point :=
  ![(p 1 - a 1) / (p 0 - a 0), -(1 / (p 0 - a 0))]

noncomputable def unprojectFrom (a q : Point) : Point :=
  ![a 0 - 1 / q 1, a 1 - q 0 / q 1]

theorem unproject_projectFrom (a p : Point) (hp : p 0 - a 0 ≠ 0) :
    unprojectFrom a (projectFrom a p) = p := by
  ext i
  fin_cases i <;> simp [unprojectFrom, projectFrom]
  field_simp
  ring

theorem projectFrom_injOn (a : Point) :
    Set.InjOn (projectFrom a) {p : Point | a 0 < p 0} := by
  intro p hp q hq he
  have h := congrArg (unprojectFrom a) he
  simpa only [unproject_projectFrom a p (sub_ne_zero.mpr (ne_of_gt hp)),
    unproject_projectFrom a q (sub_ne_zero.mpr (ne_of_gt hq))] using h

theorem orient_projectFrom (a p q r : Point)
    (hp : p 0 - a 0 ≠ 0) (hq : q 0 - a 0 ≠ 0) (hr : r 0 - a 0 ≠ 0) :
    orient (projectFrom a p) (projectFrom a q) (projectFrom a r) =
      -orient p q r / ((p 0 - a 0) * (q 0 - a 0) * (r 0 - a 0)) := by
  simp only [orient, projectFrom, Matrix.cons_val_zero, Matrix.cons_val_one]
  field_simp
  ring

theorem orient_projectFrom_pos_iff (a p q r : Point)
    (hp : a 0 < p 0) (hq : a 0 < q 0) (hr : a 0 < r 0) :
    0 < orient (projectFrom a p) (projectFrom a q) (projectFrom a r) ↔ orient p q r < 0 := by
  rw [orient_projectFrom a p q r (sub_ne_zero.mpr hp.ne')
    (sub_ne_zero.mpr hq.ne') (sub_ne_zero.mpr hr.ne')]
  have hd := mul_pos (mul_pos (sub_pos.mpr hp) (sub_pos.mpr hq)) (sub_pos.mpr hr)
  rw [div_pos_iff_of_pos_right hd, neg_pos]

theorem orient_projectFrom_neg_iff (a p q r : Point)
    (hp : a 0 < p 0) (hq : a 0 < q 0) (hr : a 0 < r 0) :
    orient (projectFrom a p) (projectFrom a q) (projectFrom a r) < 0 ↔ 0 < orient p q r := by
  rw [orient_projectFrom a p q r (sub_ne_zero.mpr hp.ne')
    (sub_ne_zero.mpr hq.ne') (sub_ne_zero.mpr hr.ne')]
  have hd := mul_pos (mul_pos (sub_pos.mpr hp) (sub_pos.mpr hq)) (sub_pos.mpr hr)
  rw [div_lt_iff₀ hd, zero_mul, neg_lt_zero]

theorem orient_projectFrom_ne_zero_iff (a p q r : Point)
    (hp : a 0 < p 0) (hq : a 0 < q 0) (hr : a 0 < r 0) :
    orient (projectFrom a p) (projectFrom a q) (projectFrom a r) ≠ 0 ↔ orient p q r ≠ 0 := by
  rw [orient_projectFrom a p q r (sub_ne_zero.mpr hp.ne')
    (sub_ne_zero.mpr hq.ne') (sub_ne_zero.mpr hr.ne')]
  simp [sub_ne_zero.mpr hp.ne', sub_ne_zero.mpr hq.ne', sub_ne_zero.mpr hr.ne']

theorem generalPosition_projectFrom {S : Finset Point} (a : Point)
    (hgp : GeneralPosition S) (hx : ∀ p ∈ S, a 0 < p 0) :
    GeneralPosition (S.image (projectFrom a)) := by
  classical
  rw [generalPosition_iff_orient_ne_zero] at hgp ⊢
  intro p hp q hq r hr hpq hpr hqr
  obtain ⟨p', hp', rfl⟩ := Finset.mem_image.mp hp
  obtain ⟨q', hq', rfl⟩ := Finset.mem_image.mp hq
  obtain ⟨r', hr', rfl⟩ := Finset.mem_image.mp hr
  apply (orient_projectFrom_ne_zero_iff a p' q' r' (hx _ hp') (hx _ hq') (hx _ hr')).mpr
  exact hgp p' hp' q' hq' r' hr'
    (fun he => hpq (congrArg _ he)) (fun he => hpr (congrArg _ he))
    (fun he => hqr (congrArg _ he))

set_option maxHeartbeats 1000000 in
/-- Quadruple convexity is preserved on the positive-denominator chart.
The proof uses exact orientation signs, without assuming a projective hull theorem. -/
theorem convexPosition_four_projectFrom_iff (a p q r s : Point)
    (hp : a 0 < p 0) (hq : a 0 < q 0) (hr : a 0 < r 0) (hs : a 0 < s 0)
    (hpqr : orient p q r ≠ 0) (hpqs : orient p q s ≠ 0)
    (hprs : orient p r s ≠ 0) (hqrs : orient q r s ≠ 0) :
    ConvexPosition ({projectFrom a p, projectFrom a q, projectFrom a r, projectFrom a s} : Finset Point) ↔
      ConvexPosition ({p, q, r, s} : Finset Point) := by
  rw [convexPosition_four_iff_pair_separation _ _ _ _
      ((orient_projectFrom_ne_zero_iff a p q r hp hq hr).mpr hpqr)
      ((orient_projectFrom_ne_zero_iff a p q s hp hq hs).mpr hpqs)
      ((orient_projectFrom_ne_zero_iff a p r s hp hr hs).mpr hprs)
      ((orient_projectFrom_ne_zero_iff a q r s hq hr hs).mpr hqrs),
    convexPosition_four_iff_pair_separation _ _ _ _ hpqr hpqs hprs hqrs]
  simp only [mul_pos_iff, mul_neg_iff,
    orient_projectFrom_pos_iff a p q r hp hq hr, orient_projectFrom_neg_iff a p q r hp hq hr,
    orient_projectFrom_pos_iff a p q s hp hq hs, orient_projectFrom_neg_iff a p q s hp hq hs,
    orient_projectFrom_pos_iff a p r s hp hr hs, orient_projectFrom_neg_iff a p r s hp hr hs,
    orient_projectFrom_pos_iff a q r s hq hr hs, orient_projectFrom_neg_iff a q r s hq hr hs]
  tauto

/-- Pull back convexity by the projective chart, using four-point reduction. -/
theorem convexPosition_of_projectFrom {S : Finset Point} (a : Point)
    (hgp : GeneralPosition S) (hx : ∀ p ∈ S, a 0 < p 0) (hcard : 4 ≤ S.card)
    (hconv : ConvexPosition (S.image (projectFrom a))) : ConvexPosition S := by
  classical
  have hg := (generalPosition_iff_orient_ne_zero S).mp hgp
  apply convexPosition_of_four_subsets hcard
  intro T hTS hTcard
  obtain ⟨p, q, r, s, hpq, hpr, hps, hqr, hqs, hrs, rfl⟩ := Finset.card_eq_four.mp hTcard
  have hp := hTS (show p ∈ ({p, q, r, s} : Finset Point) by simp)
  have hq := hTS (show q ∈ ({p, q, r, s} : Finset Point) by simp)
  have hr := hTS (show r ∈ ({p, q, r, s} : Finset Point) by simp)
  have hs := hTS (show s ∈ ({p, q, r, s} : Finset Point) by simp)
  apply (convexPosition_four_projectFrom_iff a p q r s
    (hx p hp) (hx q hq) (hx r hr) (hx s hs)
    (hg p hp q hq r hr hpq hpr hqr) (hg p hp q hq s hs hpq hps hqs)
    (hg p hp r hr s hs hpr hps hrs) (hg q hq r hr s hs hqr hqs hrs)).mp
  simpa only [Finset.image_insert, Finset.image_singleton] using
    hconv.mono (Finset.image_subset_image hTS)

/-- A polygon found after projection yields a polygon in the original set.
This justifies applying the existing geometric engine inside the chart. -/
theorem hasConvexNGon_of_projectFrom {S : Finset Point} (a : Point) {n : ℕ}
    (hn : 4 ≤ n) (hgp : GeneralPosition S) (hx : ∀ p ∈ S, a 0 < p 0)
    (h : HasConvexNGon n (S.image (projectFrom a))) : HasConvexNGon n S := by
  classical
  obtain ⟨T, hT, hcard, hconv⟩ := h
  obtain ⟨U, hUS, hUT⟩ := Finset.subset_image_iff.mp hT
  have hinj : Set.InjOn (projectFrom a) (U : Set Point) :=
    (projectFrom_injOn a).mono (fun p hp => hx p (hUS hp))
  have hUcard : U.card = n := by
    rw [← Finset.card_image_of_injOn hinj, hUT]
    exact hcard
  refine ⟨U, hUS, hUcard, ?_⟩
  exact convexPosition_of_projectFrom a (hgp.mono hUS)
    (fun p hp => hx p (hUS hp)) (by omega) (hUT ▸ hconv)

end ErdosSzekeres.HMPT
