import MirrorEncoding.Sound
import ETVEncoding.Hull

/-!
# Sub-case (i): the axis point is a hull vertex

Points sets here are mirror-symmetric under `reflX : (x, y) ↦ (-x, y)`, with exactly one
point `c` on the axis (`MirrorSet`). Sub-case (i) is `c ∉ conv(S ∖ {c})`.

The proof follows `results/C`:
1. `extreme_axis_split`: if `c` is extreme, all other points are strictly below `c` or all
   are strictly above it (otherwise `c` lies between the midpoints of two mirror pairs).
2. The linear map `rotA : (x, y) ↦ (-y, x)` (if `c` is on top) or `rotB : (x, y) ↦ (y, x)`
   (if `c` is at the bottom) makes `c` strictly leftmost, keeps it on the new mirror axis
   (the x-axis, mirror `reflY`), and preserves general position and the absence of convex
   `K`-gons. Sorting the other points by slope from `c` is then the projective normal form
   of `--hull` (`ETV.HullFrame`): `c` becomes vertical infinity, and the slope seen from `c`
   is C's `x / (y₀ - y)`.
3. A hull frame of a set is determined by the set and its first point
   (`HullFrame.eq_of_ptSet`). The mirrored frame `ETV.mirrorFrame Q N` is a hull frame of the
   same set with the same first point, so it is `Q` itself; hence
   `σ(N-k, N-j, N-i) = σ(i, j, k)` for `1 ≤ i`, which is `MirSym N true σ`.
-/

namespace Mir

open ETV ErdosSzekeres

/-! ### A hull frame starting at a given leftmost point -/

/-- `exists_hullFrame` without the distinct-x hypothesis: `p` only has to be strictly left of
all the other points. -/
theorem exists_hullFrame_at (S : Finset Point) (hgp : GeneralPosition S) {p : Point}
    (hp : p ∈ S) (hright : ∀ q ∈ S.erase p, p 0 < q 0) :
    ∃ Q : ℕ → Point, HullFrame Q S.card ∧ ptSet Q S.card = S ∧ Q 0 = p := by
  classical
  have hne : S.Nonempty := ⟨p, hp⟩
  let f : Point → Point := fun q => ![slope p q, q 0]
  let finv : Point → Point := fun w => ![w 1, p 1 + w 0 * (w 1 - p 0)]
  have hfinv : ∀ q ∈ S.erase p, finv (f q) = q := by
    intro q hq
    have hd : q 0 - p 0 ≠ 0 := (sub_pos.2 (hright q hq)).ne'
    ext i
    fin_cases i
    · simp [finv, f]
    · simp only [finv, f, slope, Matrix.cons_val_zero, Matrix.cons_val_one]
      field_simp
      simp
  have hfinj : Set.InjOn f ↑(S.erase p) := by
    intro a ha b hb hab
    rw [← hfinv a ha, ← hfinv b hb, hab]
  let S' := (S.erase p).image f
  have hS' : LowerBound.DistinctX S' := by
    intro u hu v hv huv
    simp only [S', Finset.coe_image, Set.mem_image, Finset.mem_coe] at hu hv
    obtain ⟨a, ha, rfl⟩ := hu
    obtain ⟨b, hb, rfl⟩ := hv
    have hsl : slope p a = slope p b := huv
    by_contra hab
    have hab' : a ≠ b := fun e => hab (by rw [e])
    have ha' := Finset.mem_erase.1 ha
    have hb' := Finset.mem_erase.1 hb
    have h0 := (generalPosition_iff_orient_ne_zero S).1 hgp p hp a ha'.2 b hb'.2
      (Ne.symm ha'.1) (Ne.symm hb'.1) hab'
    apply h0
    rw [orient_from p a b (sub_pos.2 (hright a ha)).ne' (sub_pos.2 (hright b hb)).ne', hsl]
    ring
  obtain ⟨P', hx', hP'⟩ := exists_xsorted S' hS'
  have hcard' : S'.card + 1 = S.card := by
    rw [Finset.card_image_of_injOn hfinj, Finset.card_erase_of_mem hp]
    have := Finset.card_pos.2 hne
    omega
  have hmemP' : ∀ i, i < S'.card → ∃ q ∈ S.erase p, f q = P' i := by
    intro i hi
    have : P' i ∈ S' := by rw [← hP']; exact mem_ptSet hi
    simpa [S'] using this
  let Q : ℕ → Point := fun i => if i = 0 then p else finv (P' (i - 1))
  have hQ0 : Q 0 = p := by simp [Q]
  have hQ : ∀ i, 1 ≤ i → i < S.card → Q i ∈ S.erase p ∧ f (Q i) = P' (i - 1) := by
    intro i hi hiN
    obtain ⟨q, hq, hfq⟩ := hmemP' (i - 1) (by omega)
    have : Q i = q := by
      simp only [Q, if_neg (show i ≠ 0 by omega)]
      rw [← hfq, hfinv q hq]
    rw [this]
    exact ⟨hq, hfq⟩
  refine ⟨Q, ⟨?_, ?_⟩, ?_, hQ0⟩
  · intro i hi hiN
    rw [hQ0]
    exact hright _ (hQ i hi hiN).1
  · intro i j hi hij hj
    rw [hQ0]
    have e1 : slope p (Q i) = P' (i - 1) 0 := by
      rw [← (hQ i hi (by omega)).2]
      rfl
    have e2 : slope p (Q j) = P' (j - 1) 0 := by
      rw [← (hQ j (by omega) hj).2]
      rfl
    rw [e1, e2]
    exact hx' (i - 1) (j - 1) (by omega) (by omega)
  · ext q
    constructor
    · intro hq
      simp only [ptSet, Finset.mem_image, Finset.mem_range] at hq
      obtain ⟨i, hi, rfl⟩ := hq
      rcases Nat.eq_zero_or_pos i with rfl | hi0
      · simpa [Q] using hp
      · exact Finset.mem_of_mem_erase (hQ i hi0 hi).1
    · intro hq
      simp only [ptSet, Finset.mem_image, Finset.mem_range]
      by_cases hqp : q = p
      · exact ⟨0, Finset.card_pos.2 hne, by simp [Q, hqp]⟩
      · have hq' : q ∈ S.erase p := Finset.mem_erase.2 ⟨hqp, hq⟩
        have : f q ∈ ptSet P' S'.card := by
          rw [hP']
          exact Finset.mem_image_of_mem f hq'
        simp only [ptSet, Finset.mem_image, Finset.mem_range] at this
        obtain ⟨m, hm, hPm⟩ := this
        refine ⟨m + 1, by omega, ?_⟩
        simp only [Q, if_neg (Nat.succ_ne_zero m), Nat.add_sub_cancel, hPm]
        exact hfinv q hq'

/-! ### Uniqueness of hull frames -/

/-- Two hull frames of the same set with the same first point agree. -/
theorem HullFrame.eq_of_ptSet {Q Q' : ℕ → Point} {N : ℕ} (h : HullFrame Q N)
    (h' : HullFrame Q' N) (hS : ptSet Q N = ptSet Q' N) (h0 : Q 0 = Q' 0) :
    ∀ i, i < N → Q i = Q' i := by
  classical
  -- every `Q' i` (`i ≥ 1`) is some `Q j` with `j ≥ 1`
  have hpre : ∀ i, 1 ≤ i → i < N → ∃ j, 1 ≤ j ∧ j < N ∧ Q j = Q' i := by
    intro i hi hiN
    have : Q' i ∈ ptSet Q N := by rw [hS]; exact mem_ptSet hiN
    simp only [ptSet, Finset.mem_image, Finset.mem_range] at this
    obtain ⟨j, hj, hji⟩ := this
    refine ⟨j, ?_, hj, hji⟩
    rcases Nat.eq_zero_or_pos j with rfl | hj0
    · exfalso
      rw [h0] at hji
      have := h'.injOn (by simp; omega) (by simpa using hiN) hji
      omega
    · exact hj0
  let sl : (ℕ → Point) → ℕ → ℝ := fun R m => slope (Q 0) (R m)
  have hmono : ∀ a b, 1 ≤ a → a < b → b < N → sl Q a < sl Q b := fun a b ha hab hb =>
    h.slope_lt a b ha hab hb
  have hmono' : ∀ a b, 1 ≤ a → a < b → b < N → sl Q' a < sl Q' b := fun a b ha hab hb => by
    simp only [sl, h0]
    exact h'.slope_lt a b ha hab hb
  let T : Finset ℝ := (Finset.Ico 1 N).image (sl Q)
  have hT : T.card = N - 1 := by
    rw [Finset.card_image_of_injOn, Nat.card_Ico]
    intro a ha b hb hab
    simp only [Finset.coe_Ico, Set.mem_Ico] at ha hb
    rcases lt_trichotomy a b with hlt | heq | hgt
    · exact absurd hab (hmono a b ha.1 hlt hb.2).ne
    · exact heq
    · exact absurd hab (hmono b a hb.1 hgt ha.2).ne'
  let g : Fin (N - 1) → ℝ := fun a => sl Q (a + 1)
  let g' : Fin (N - 1) → ℝ := fun a => sl Q' (a + 1)
  have hg : ∀ a, g a ∈ T := fun a =>
    Finset.mem_image.2 ⟨a + 1, Finset.mem_Ico.2 ⟨by omega, by omega⟩, rfl⟩
  have hg' : ∀ a, g' a ∈ T := by
    intro a
    obtain ⟨j, hj1, hjN, hj⟩ := hpre (a + 1) (by omega) (by omega)
    exact Finset.mem_image.2 ⟨j, Finset.mem_Ico.2 ⟨hj1, hjN⟩, by simp only [sl, g', hj]⟩
  have sg : StrictMono g := fun a b hab => hmono _ _ (by omega) (by simpa using hab) (by omega)
  have sg' : StrictMono g' := fun a b hab =>
    hmono' _ _ (by omega) (by simpa using hab) (by omega)
  have e1 := Finset.orderEmbOfFin_unique hT hg sg
  have e2 := Finset.orderEmbOfFin_unique hT hg' sg'
  have hgg : g = g' := e1.trans e2.symm
  intro i hi
  rcases Nat.eq_zero_or_pos i with rfl | hi0
  · exact h0
  · obtain ⟨j, hj1, hjN, hj⟩ := hpre i hi0 hi
    have hval : sl Q i = sl Q j := by
      have := congrFun hgg ⟨i - 1, by omega⟩
      simp only [g, g', show i - 1 + 1 = i by omega] at this
      rw [this]
      simp only [sl, hj]
    have hij : i = j := by
      rcases lt_trichotomy i j with hlt | heq | hgt
      · exact absurd hval (hmono i j hi0 hlt hjN).ne
      · exact heq
      · exact absurd hval (hmono j i hj1 hgt hi).ne'
    rw [← hj, hij]

/-! ### The frame theorem -/

theorem reflY_eq_self {p : Point} (hp : p 1 = 0) : reflY p = p := by
  ext i
  fin_cases i <;> simp [hp]

/-- **Sub-case (i) in the hull frame.** Let `S` be in general position, symmetric under the
reflection `reflY` in the x-axis, with a point `p` on the x-axis strictly left of all other
points. If `S` has no convex `K`-gon (`K ≥ 4`), then `hullCnf S.card K` is satisfiable. -/
theorem hullCnf_satisfiable_of_frame {S : Finset Point} {K : ℕ} (hK : 4 ≤ K)
    (hgp : GeneralPosition S) {p : Point} (hp : p ∈ S) (hp1 : p 1 = 0)
    (hsym : ∀ q ∈ S, reflY q ∈ S) (hright : ∀ q ∈ S.erase p, p 0 < q 0)
    (hno : ¬HasConvexNGon K S) : DimacsSatisfiable (hullCnf S.card K) := by
  classical
  obtain ⟨Q, hQ, hQS, hQ0⟩ := exists_hullFrame_at S hgp hp hright
  have hN : 1 ≤ S.card := Finset.card_pos.2 ⟨p, hp⟩
  set N := S.card with hNdef
  have hQ' := hQ.mirror
  have himg : S.image reflY = S := by
    apply Finset.eq_of_subset_of_card_le
    · intro q hq
      obtain ⟨r, hr, rfl⟩ := Finset.mem_image.1 hq
      exact hsym r hr
    · rw [Finset.card_image_of_injective _ reflY_injective]
  have hpt : ptSet (mirrorFrame Q N) N = ptSet Q N := by
    rw [ptSet_mirrorFrame hN, hQS, himg]
  have h0 : mirrorFrame Q N 0 = Q 0 := by
    simp only [mirrorFrame, if_true, hQ0, reflY_eq_self hp1]
  have heq := HullFrame.eq_of_ptSet hQ' hQ hpt h0
  have hsymσ : MirSym N true (sigOf Q) := by
    intro i j k hi hij hjk hk
    simp only [mm, lo, if_true] at hi ⊢
    have e := sigOf_mirrorFrame (Q := Q) (N := N) hi hij hjk
    have e' : sigOf (mirrorFrame Q N) i j k = sigOf Q i j k := by
      simp only [sigOf, heq i (by omega), heq j (by omega), heq k hk]
    rw [show N - 1 + 1 = N by omega, ← e, e']
  have hgpQ : GeneralPosition (ptSet Q N) := by rw [hQS]; exact hgp
  have hnoQ : ¬HasConvexNGon K (ptSet Q N) := by rw [hQS]; exact hno
  have hgon : ¬HasGon (sigOf Q) N K := fun hg =>
    hnoQ (hasConvexNGon_of_hasGon' Q hQ.injOn hgpQ hQ.isSignotope hK hg)
  exact hullCnf_satisfiable (by omega) hQ.isSignotope hgon hQ.hullForm hsymσ

/-! ### Mirror-symmetric sets in standard position -/

/-- The reflection `(x, y) ↦ (-x, y)` in the y-axis. -/
def reflX : Point →ₗ[ℝ] Point where
  toFun p := ![-p 0, p 1]
  map_add' p q := by
    ext i
    fin_cases i
    all_goals simp
    all_goals ring
  map_smul' c p := by
    ext i
    fin_cases i
    all_goals simp

@[simp] theorem reflX_zero (p : Point) : reflX p 0 = -p 0 := rfl

@[simp] theorem reflX_one (p : Point) : reflX p 1 = p 1 := rfl

/-- A set symmetric under `reflX` with exactly one point `c` on the axis: `c` and mirror
pairs `{q, reflX q}`. For `|S| = 33` these are the 16 pairs of `results/C`. -/
structure MirrorSet (S : Finset Point) (c : Point) : Prop where
  mem : c ∈ S
  axis : c 0 = 0
  symm : ∀ q ∈ S, reflX q ∈ S
  off : ∀ q ∈ S, q ≠ c → q 0 ≠ 0

/-- If `c` is extreme, the other points are all strictly below or all strictly above it. -/
theorem extreme_axis_split {S : Finset Point} {c : Point} (hM : MirrorSet S c)
    (hext : c ∉ convexHull ℝ (↑(S.erase c) : Set Point)) :
    (∀ q ∈ S.erase c, q 1 < c 1) ∨ (∀ q ∈ S.erase c, c 1 < q 1) := by
  classical
  by_contra hcon
  simp only [not_or, not_forall, not_lt, exists_prop] at hcon
  obtain ⟨⟨a, ha, hac⟩, ⟨b, hb, hbc⟩⟩ := hcon
  apply hext
  have mem_e : ∀ q ∈ S.erase c, reflX q ∈ S.erase c := by
    intro q hq
    obtain ⟨hqc, hqS⟩ := Finset.mem_erase.1 hq
    refine Finset.mem_erase.2 ⟨fun e => hM.off q hqS hqc ?_, hM.symm q hqS⟩
    have := congrFun e 0
    simp only [reflX_zero, hM.axis] at this
    linarith
  let H := convexHull ℝ (↑(S.erase c) : Set Point)
  have hconv : Convex ℝ H := convex_convexHull ℝ _
  have sub : ∀ q ∈ S.erase c, q ∈ H := fun q hq => subset_convexHull ℝ _ (Finset.mem_coe.2 hq)
  -- the midpoint of a mirror pair is the axis point at the same height
  have mid : ∀ q ∈ S.erase c, (![0, q 1] : Point) ∈ H := by
    intro q hq
    have := hconv (sub q hq) (sub _ (mem_e q hq)) (by norm_num : (0 : ℝ) ≤ 1 / 2)
      (by norm_num : (0 : ℝ) ≤ 1 / 2) (by norm_num)
    convert this using 1
    ext i
    fin_cases i
    · simp
    · simp
      ring
  have hc : c = ![0, c 1] := by
    ext i
    fin_cases i <;> simp [hM.axis]
  suffices hs : (![0, c 1] : Point) ∈ H by rwa [← hc] at hs
  rcases eq_or_lt_of_le hac with hae | hal
  · rw [hae]; exact mid a ha
  · rcases eq_or_lt_of_le hbc with hbe | hbl
    · rw [← hbe]; exact mid b hb
    · -- `c 1 = t * a 1 + (1 - t) * b 1` with `t = (c 1 - b 1) / (a 1 - b 1)`
      have hd : 0 < a 1 - b 1 := by linarith
      set t := (c 1 - b 1) / (a 1 - b 1) with ht
      have t0 : 0 ≤ t := div_nonneg (by linarith) hd.le
      have t1 : 0 ≤ 1 - t := by
        rw [ht, sub_nonneg, div_le_one hd]
        linarith
      have := hconv (mid a ha) (mid b hb) t0 t1 (by ring)
      convert this using 1
      ext i
      fin_cases i
      · simp
      · simp only [Fin.isValue, Fin.mk_one, Matrix.cons_val_one, Matrix.cons_val_zero,
          Pi.add_apply, Pi.smul_apply, smul_eq_mul]
        rw [ht]
        field_simp
        ring

/-! ### Linear changes of coordinates -/

theorem generalPosition_image_linear {S : Finset Point} (f : Point →ₗ[ℝ] Point)
    (_hf : Function.Injective f) (s : ℝ) (hs : s ≠ 0)
    (horient : ∀ a b c, orient (f a) (f b) (f c) = s * orient a b c)
    (h : GeneralPosition S) : GeneralPosition (S.image f) := by
  classical
  rw [generalPosition_iff_orient_ne_zero] at h ⊢
  intro a ha b hb c hc hab hac hbc
  obtain ⟨a', ha', rfl⟩ := Finset.mem_image.1 ha
  obtain ⟨b', hb', rfl⟩ := Finset.mem_image.1 hb
  obtain ⟨c', hc', rfl⟩ := Finset.mem_image.1 hc
  rw [horient]
  exact mul_ne_zero hs (h a' ha' b' hb' c' hc' (fun e => hab (e ▸ rfl))
    (fun e => hac (e ▸ rfl)) (fun e => hbc (e ▸ rfl)))

theorem not_hasConvexNGon_image_linear {S : Finset Point} {K : ℕ} (f : Point →ₗ[ℝ] Point)
    (hf : Function.Injective f) (h : ¬HasConvexNGon K S) :
    ¬HasConvexNGon K (S.image f) := by
  classical
  rintro ⟨T', hT', hcard, hconv⟩
  apply h
  let T := S.filter fun q => f q ∈ T'
  have hTimg : T.image f = T' := by
    ext w
    simp only [T, Finset.mem_image, Finset.mem_filter]
    constructor
    · rintro ⟨q, ⟨_, hq⟩, rfl⟩
      exact hq
    · intro hw
      obtain ⟨q, hq, rfl⟩ := Finset.mem_image.1 (hT' hw)
      exact ⟨q, ⟨hq, hw⟩, rfl⟩
  refine ⟨T, Finset.filter_subset _ _, ?_, ?_⟩
  · rw [← hcard, ← hTimg, Finset.card_image_of_injective _ hf]
  · apply convexPosition_of_image_linear f hf
    rw [hTimg]
    exact hconv

/-- `(x, y) ↦ (-y, x)`: the rotation by 90°, used when `c` is the top point. -/
def rotA : Point →ₗ[ℝ] Point where
  toFun p := ![-p 1, p 0]
  map_add' p q := by
    ext i
    fin_cases i
    all_goals simp
    all_goals ring
  map_smul' c p := by
    ext i
    fin_cases i
    all_goals simp

/-- `(x, y) ↦ (y, x)`, used when `c` is the bottom point. -/
def rotB : Point →ₗ[ℝ] Point where
  toFun p := ![p 1, p 0]
  map_add' p q := by
    ext i
    fin_cases i
    all_goals simp
  map_smul' c p := by
    ext i
    fin_cases i
    all_goals simp

@[simp] theorem rotA_zero (p : Point) : rotA p 0 = -p 1 := rfl
@[simp] theorem rotA_one (p : Point) : rotA p 1 = p 0 := rfl
@[simp] theorem rotB_zero (p : Point) : rotB p 0 = p 1 := rfl
@[simp] theorem rotB_one (p : Point) : rotB p 1 = p 0 := rfl

theorem rotA_injective : Function.Injective rotA := fun p q h => by
  ext i
  have h0 := congrFun h 0
  have h1 := congrFun h 1
  simp only [rotA_zero, rotA_one, neg_inj] at h0 h1
  fin_cases i
  · exact h1
  · exact h0

theorem rotB_injective : Function.Injective rotB := fun p q h => by
  ext i
  have h0 := congrFun h 0
  have h1 := congrFun h 1
  simp only [rotB_zero, rotB_one] at h0 h1
  fin_cases i
  · exact h1
  · exact h0

theorem orient_rotA (a b c : Point) : orient (rotA a) (rotA b) (rotA c) = 1 * orient a b c := by
  simp only [orient, rotA_zero, rotA_one]
  ring

theorem orient_rotB (a b c : Point) :
    orient (rotB a) (rotB b) (rotB c) = (-1) * orient a b c := by
  simp only [orient, rotB_zero, rotB_one]
  ring

/-- The common step for both rotations. -/
theorem hullCnf_of_rot {S : Finset Point} {c : Point} {K : ℕ} (hK : 4 ≤ K)
    (hgp : GeneralPosition S) (hM : MirrorSet S c) (hno : ¬HasConvexNGon K S)
    (f : Point →ₗ[ℝ] Point) (hf : Function.Injective f) (s : ℝ) (hs : s ≠ 0)
    (horient : ∀ a b c, orient (f a) (f b) (f c) = s * orient a b c)
    (hcomm : ∀ q, f (reflX q) = reflY (f q)) (hc1 : f c 1 = 0)
    (hleft : ∀ q ∈ S.erase c, f c 0 < f q 0) : DimacsSatisfiable (hullCnf S.card K) := by
  classical
  have hcard : (S.image f).card = S.card := Finset.card_image_of_injective _ hf
  rw [← hcard]
  refine hullCnf_satisfiable_of_frame hK (generalPosition_image_linear f hf s hs horient hgp)
    (Finset.mem_image_of_mem f hM.mem) hc1 ?_ ?_ (not_hasConvexNGon_image_linear f hf hno)
  · intro w hw
    obtain ⟨q, hq, rfl⟩ := Finset.mem_image.1 hw
    rw [← hcomm]
    exact Finset.mem_image_of_mem f (hM.symm q hq)
  · intro w hw
    obtain ⟨hwc, hw⟩ := Finset.mem_erase.1 hw
    obtain ⟨q, hq, rfl⟩ := Finset.mem_image.1 hw
    exact hleft q (Finset.mem_erase.2 ⟨fun e => hwc (e ▸ rfl), hq⟩)

/-- **Sub-case (i), point-set level.** A mirror-symmetric set in general position whose
axis point `c` is a vertex of the convex hull, with no convex `K`-gon (`K ≥ 4`), makes
`hullCnf S.card K` satisfiable. For `|S| = 33`, `K = 7` this is `hm33k7.sub.cnf`. -/
theorem hullCnf_satisfiable_of_mirrorSet {S : Finset Point} {c : Point} {K : ℕ} (hK : 4 ≤ K)
    (hgp : GeneralPosition S) (hM : MirrorSet S c)
    (hext : c ∉ convexHull ℝ (↑(S.erase c) : Set Point)) (hno : ¬HasConvexNGon K S) :
    DimacsSatisfiable (hullCnf S.card K) := by
  rcases extreme_axis_split hM hext with htop | hbot
  · refine hullCnf_of_rot hK hgp hM hno rotA rotA_injective 1 one_ne_zero orient_rotA ?_
      (by simp [hM.axis]) ?_
    · intro q
      ext i
      fin_cases i <;> simp
    · intro q hq
      simp only [rotA_zero]
      linarith [htop q hq]
  · refine hullCnf_of_rot hK hgp hM hno rotB rotB_injective (-1) (by norm_num) orient_rotB ?_
      (by simp [hM.axis]) ?_
    · intro q
      ext i
      fin_cases i <;> simp
    · intro q hq
      simp only [rotB_zero]
      exact hbot q hq

/-- **What an UNSAT certificate for `hm33k7.sub.cnf` proves.** -/
theorem hasConvexNGon_of_unsat_hull {S : Finset Point} {c : Point}
    (hunsat : ¬DimacsSatisfiable (hullCnf 33 7)) (hgp : GeneralPosition S)
    (hcard : S.card = 33) (hM : MirrorSet S c)
    (hext : c ∉ convexHull ℝ (↑(S.erase c) : Set Point)) : HasConvexNGon 7 S := by
  by_contra hno
  exact hunsat (hcard ▸ hullCnf_satisfiable_of_mirrorSet (by norm_num) hgp hM hext hno)

end Mir
