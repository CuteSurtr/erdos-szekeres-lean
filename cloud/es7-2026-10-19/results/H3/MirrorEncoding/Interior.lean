import MirrorEncoding.Frame

/-!
# Sub-case (ii): the axis point is interior

For a `MirrorSet S c` with `c ∈ conv(S ∖ {c})` and distinct x-coordinates, the x-sorted
enumeration `P` of `S` satisfies:
* `P (N-1-i) = reflX (P i)` (`XSorted.eq_of_ptSet`: an x-sorted enumeration of a set is
  unique, and `i ↦ reflX (P (N-1-i))` is another one), so `sigOf P` is `MirSym N false`;
* `c = P ((N-1)/2)`, the axis point of the encoding;
* some other point is strictly above `c` and some strictly below (`axis_above_below`;
  otherwise `conv(S ∖ {c})` lies in an open half-plane, using general position for points
  at the height of `c`). For a pair `a, reflX a` with `a` left of the axis,
  `orient a c (reflX a) = 2 a.x (c.y - a.y)`, so the chord of a pair above `c` is a cup triple
  through `c` and one below is a cap triple: this is `AxisInterior`.

The distinct-x hypothesis is the only extra assumption; removing it is the target
`InteriorTieBreak` in `Targets.lean`.
-/

namespace Mir

open ETV ErdosSzekeres

theorem reflX_reflX (p : Point) : reflX (reflX p) = p := by
  ext i
  fin_cases i <;> simp

theorem reflX_injective : Function.Injective reflX := fun p q h => by
  rw [← reflX_reflX p, h, reflX_reflX]

theorem reflX_eq_self {p : Point} (hp : p 0 = 0) : reflX p = p := by
  ext i
  fin_cases i <;> simp [hp]

theorem orient_reflX (a b c : Point) : orient (reflX a) (reflX b) (reflX c) = -orient a b c := by
  simp only [orient, reflX_zero, reflX_one]
  ring

theorem orient_pair (p c : Point) (hc : c 0 = 0) :
    orient p c (reflX p) = 2 * p 0 * (c 1 - p 1) := by
  simp only [orient, reflX_zero, reflX_one, hc]
  ring

/-- Two x-sorted enumerations of the same set agree. -/
theorem XSorted.eq_of_ptSet {P P' : ℕ → Point} {N : ℕ} (h : XSorted P N) (h' : XSorted P' N)
    (hS : ptSet P N = ptSet P' N) : ∀ i, i < N → P i = P' i := by
  classical
  have hpre : ∀ i, i < N → ∃ j, j < N ∧ P j = P' i := by
    intro i hi
    have : P' i ∈ ptSet P N := by rw [hS]; exact mem_ptSet hi
    simpa [ptSet] using this
  let T : Finset ℝ := (Finset.range N).image fun i => P i 0
  have hT : T.card = N := by
    rw [Finset.card_image_of_injOn, Finset.card_range]
    intro a ha b hb hab
    simp only [Finset.coe_range, Set.mem_Iio] at ha hb
    rcases lt_trichotomy a b with hlt | heq | hgt
    · exact absurd hab (h a b hlt hb).ne
    · exact heq
    · exact absurd hab (h b a hgt ha).ne'
  let g : Fin N → ℝ := fun a => P a 0
  let g' : Fin N → ℝ := fun a => P' a 0
  have hg : ∀ a, g a ∈ T := fun a => Finset.mem_image.2 ⟨a, by simp, rfl⟩
  have hg' : ∀ a, g' a ∈ T := by
    intro a
    obtain ⟨j, hj, e⟩ := hpre a a.2
    exact Finset.mem_image.2 ⟨j, by simpa using hj, by simp only [g', e]⟩
  have sg : StrictMono g := fun a b hab => h a b hab b.2
  have sg' : StrictMono g' := fun a b hab => h' a b hab b.2
  have hgg : g = g' :=
    (Finset.orderEmbOfFin_unique hT hg sg).trans (Finset.orderEmbOfFin_unique hT hg' sg').symm
  intro i hi
  obtain ⟨j, hj, e⟩ := hpre i hi
  have hval : P i 0 = P j 0 := by
    have := congrFun hgg ⟨i, hi⟩
    simp only [g, g'] at this
    rw [this, e]
  have hij : i = j := by
    rcases lt_trichotomy i j with hlt | heq | hgt
    · exact absurd hval (h i j hlt hj).ne
    · exact heq
    · exact absurd hval (h j i hgt hi).ne'
  rw [← e, hij]

/-- In sub-case (ii) some point is strictly above `c` and some strictly below. -/
theorem axis_above_below {S : Finset Point} {c : Point} (hgp : GeneralPosition S)
    (hM : MirrorSet S c) (hin : c ∈ convexHull ℝ (↑(S.erase c) : Set Point)) :
    (∃ a ∈ S.erase c, c 1 < a 1) ∧ (∃ b ∈ S.erase c, b 1 < c 1) := by
  classical
  have hlin : IsLinearMap ℝ (fun q : Point => q 1) := ⟨fun _ _ => rfl, fun _ _ => rfl⟩
  -- no other point is at the height of `c`
  have hne : ∀ a ∈ S.erase c, a 1 ≠ c 1 := by
    intro a ha e
    obtain ⟨hac, haS⟩ := Finset.mem_erase.1 ha
    have hx := hM.off a haS hac
    have h0 := (generalPosition_iff_orient_ne_zero S).1 hgp a haS c hM.mem (reflX a)
      (hM.symm a haS) hac (fun e' => hx (by have := congrFun e' 0; simp at this; linarith))
      (fun e' => hM.off _ (hM.symm a haS) (fun e'' => hac (by
        rw [← reflX_reflX a, e'', reflX_eq_self hM.axis])) (by
        rw [← e', hM.axis]))
    apply h0
    rw [orient_pair a c hM.axis, e]
    ring
  constructor
  · by_contra hcon
    simp only [not_exists, not_and, not_lt] at hcon
    have hsub : (↑(S.erase c) : Set Point) ⊆ {w | w 1 < c 1} := by
      intro a ha
      exact lt_of_le_of_ne (hcon a ha) (hne a ha)
    have := convexHull_min hsub (convex_halfSpace_lt hlin (c 1)) hin
    exact lt_irrefl (c 1) this
  · by_contra hcon
    simp only [not_exists, not_and, not_lt] at hcon
    have hsub : (↑(S.erase c) : Set Point) ⊆ {w | c 1 < w 1} := by
      intro a ha
      exact lt_of_le_of_ne (hcon a ha) (hne a ha).symm
    have := convexHull_min hsub (convex_halfSpace_gt hlin (c 1)) hin
    exact lt_irrefl (c 1) this

/-- The x-sorted enumeration of a mirror set with distinct x-coordinates. -/
theorem exists_mirror_xsorted {S : Finset Point} {c : Point} (hM : MirrorSet S c)
    (hX : LowerBound.DistinctX S) :
    ∃ P : ℕ → Point, XSorted P S.card ∧ ptSet P S.card = S ∧
      (∀ i, i < S.card → P (S.card - 1 - i) = reflX (P i)) ∧ P (axisPt S.card) = c ∧
      (∀ i, i < axisPt S.card → P i 0 < 0) := by
  classical
  obtain ⟨P, hx, hP⟩ := exists_xsorted S hX
  set N := S.card with hN
  let P' : ℕ → Point := fun i => reflX (P (N - 1 - i))
  have hx' : XSorted P' N := by
    intro i j hij hj
    simp only [P', reflX_zero, neg_lt_neg_iff]
    exact hx _ _ (by omega) (by omega)
  have hP' : ptSet P' N = S := by
    ext q
    simp only [ptSet, Finset.mem_image, Finset.mem_range, P']
    constructor
    · rintro ⟨i, hi, rfl⟩
      exact hM.symm _ (by rw [← hP]; exact mem_ptSet (by omega))
    · intro hq
      have : reflX q ∈ ptSet P N := by rw [hP]; exact hM.symm q hq
      simp only [ptSet, Finset.mem_image, Finset.mem_range] at this
      obtain ⟨j, hj, e⟩ := this
      refine ⟨N - 1 - j, by omega, ?_⟩
      rw [show N - 1 - (N - 1 - j) = j by omega, e, reflX_reflX]
  have heq := XSorted.eq_of_ptSet hx hx' (hP.trans hP'.symm)
  have hpair : ∀ i, i < N → P (N - 1 - i) = reflX (P i) := by
    intro i hi
    rw [heq (N - 1 - i) (by omega)]
    simp only [P', show N - 1 - (N - 1 - i) = i by omega]
  have hcS : c ∈ ptSet P N := by rw [hP]; exact hM.mem
  simp only [ptSet, Finset.mem_image, Finset.mem_range] at hcS
  obtain ⟨m, hm, hPm⟩ := hcS
  have hmid : N - 1 - m = m := by
    have e := hpair m hm
    rw [hPm, reflX_eq_self hM.axis, ← hPm] at e
    exact hx.injOn (by simp; omega) (by simpa using hm) e
  have hm' : m = axisPt N := by
    simp only [axisPt]
    omega
  refine ⟨P, hx, hP, hpair, hm' ▸ hPm, ?_⟩
  intro i hi
  have := hx i m (by omega) hm
  rw [hPm, hM.axis] at this
  exact this

/-- **Sub-case (ii), signotope data from an enumeration.** Any enumeration `P` of `S` whose
orientation signs form a signotope, with `P (N-1-i) = reflX (P i)`, the axis point in the
middle and the points before it left of the axis, gives the hypotheses of
`interiorCnf_satisfiable`. -/
theorem interior_signotope_of_enum {S : Finset Point} {c : Point} {K : ℕ} (hK : 4 ≤ K)
    (hgp : GeneralPosition S) (hM : MirrorSet S c)
    (hin : c ∈ convexHull ℝ (↑(S.erase c) : Set Point)) (hno : ¬HasConvexNGon K S)
    (P : ℕ → Point) (hsig : IsSignotope S.card (sigOf P))
    (hinj : Set.InjOn P ↑(Finset.range S.card)) (hP : ptSet P S.card = S)
    (hpair : ∀ i, i < S.card → P (S.card - 1 - i) = reflX (P i))
    (hc : P (axisPt S.card) = c) (hleft : ∀ i, i < axisPt S.card → P i 0 < 0) :
    ∃ σ : Sig, IsSignotope S.card σ ∧ ¬HasGon σ S.card K ∧ MirSym S.card false σ ∧
      AxisInterior S.card σ := by
  classical
  set N := S.card with hN
  have hgpP : GeneralPosition (ptSet P N) := by rw [hP]; exact hgp
  have hmN : axisPt N < N := by
    have := Finset.card_pos.2 ⟨c, hM.mem⟩
    simp only [axisPt]
    omega
  have hmid : N - 1 - axisPt N = axisPt N := by
    apply hinj (by simp; omega) (by simpa using hmN)
    rw [hpair _ hmN, hc, reflX_eq_self hM.axis]
  refine ⟨sigOf P, hsig, fun hg => hno ?_, ?_, ?_⟩
  · rw [← hP]
    exact hasConvexNGon_of_hasGon' P hinj hgpP hsig hK hg
  · intro i j k _ hij hjk hk
    simp only [mm, lo, Bool.false_eq_true, if_false, Nat.add_zero, sigOf]
    rw [hpair i (by omega), hpair j (by omega), hpair k hk, orient_reflX]
    congr 1
    apply propext
    simp only [orient]
    constructor <;> intro h <;> linarith
  · obtain ⟨⟨a, ha, hab⟩, ⟨b, hb, hbb⟩⟩ := axis_above_below hgp hM hin
    -- a point other than `c`, moved to the left of the axis, with its pair
    have pick : ∀ q ∈ S.erase c, ∃ i, i < axisPt N ∧ P i 1 = q 1 := by
      intro q hq
      obtain ⟨hqc, hqS⟩ := Finset.mem_erase.1 hq
      have : q ∈ ptSet P N := by rw [hP]; exact hqS
      simp only [ptSet, Finset.mem_image, Finset.mem_range] at this
      obtain ⟨j, hj, rfl⟩ := this
      have hjm : j ≠ axisPt N := fun e => hqc (by rw [e, hc])
      rcases lt_or_gt_of_ne hjm with hlt | hgt
      · exact ⟨j, hlt, rfl⟩
      · refine ⟨N - 1 - j, by omega, ?_⟩
        rw [hpair j hj, reflX_one]
    have chord : ∀ i, i < axisPt N →
        orient (P i) (P (axisPt N)) (P (N - 1 - i)) = 2 * P i 0 * (c 1 - P i 1) := by
      intro i hi
      have hiN : i < N := by omega
      rw [hpair i hiN, hc]
      exact orient_pair _ _ hM.axis
    have hk : ∀ i, i < axisPt N → axisPt N < N - 1 - i ∧ N - 1 - i < N := by
      intro i hi
      omega
    obtain ⟨i, hi, hia⟩ := pick a ha
    obtain ⟨i', hi', hib⟩ := pick b hb
    refine ⟨⟨i, N - 1 - i, hi, (hk i hi).1, (hk i hi).2, ?_⟩,
      ⟨i', N - 1 - i', hi', (hk i' hi').1, (hk i' hi').2, ?_⟩⟩
    · simp only [sigOf, decide_eq_true_eq, chord i hi]
      have := hleft i hi
      rw [hia]
      nlinarith
    · simp only [sigOf, decide_eq_false_iff_not, not_lt, chord i' hi']
      have := hleft i' hi'
      rw [hib]
      nlinarith

/-- **Sub-case (ii) with distinct x-coordinates, signotope data.** -/
theorem interior_signotope_of_distinctX {S : Finset Point} {c : Point} {K : ℕ} (hK : 4 ≤ K)
    (hgp : GeneralPosition S) (hM : MirrorSet S c) (hX : LowerBound.DistinctX S)
    (hin : c ∈ convexHull ℝ (↑(S.erase c) : Set Point)) (hno : ¬HasConvexNGon K S) :
    ∃ σ : Sig, IsSignotope S.card σ ∧ ¬HasGon σ S.card K ∧ MirSym S.card false σ ∧
      AxisInterior S.card σ := by
  obtain ⟨P, hx, hP, hpair, hc, hleft⟩ := exists_mirror_xsorted hM hX
  exact interior_signotope_of_enum hK hgp hM hin hno P (isSignotope_sigOf hx) hx.injOn hP
    hpair hc hleft

/-- **Sub-case (ii), point-set level, distinct x-coordinates.** -/
theorem interiorCnf_satisfiable_of_distinctX {S : Finset Point} {c : Point} {K : ℕ}
    (hK : 4 ≤ K) (hgp : GeneralPosition S) (hM : MirrorSet S c)
    (hX : LowerBound.DistinctX S) (hin : c ∈ convexHull ℝ (↑(S.erase c) : Set Point))
    (hno : ¬HasConvexNGon K S) (hN : 3 ≤ S.card) : DimacsSatisfiable (interiorCnf S.card K) := by
  obtain ⟨σ, hσ, hg, hS, hI⟩ := interior_signotope_of_distinctX hK hgp hM hX hin hno
  exact interiorCnf_satisfiable hN (by omega) hσ hg hS hI

end Mir
