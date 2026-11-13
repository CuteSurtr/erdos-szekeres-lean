import ETVEncoding.TrackB

/-!
# Soundness of `--hull` and `--mirror` (`gen_cnf.py N K --hull [--mirror]`)

`--hull` asks for the normal form `X(0,i,j) = true` for all `0 < i < j`: point `0` is an
extreme point and the others are sorted around it. Concretely, take `p` the leftmost point
and sort the others by the slope seen from `p`. The orientations of this sequence form a
signotope: for triples avoiding `p` this is the projective map
`q ↦ (slope p q, 1/(q.x - p.x))`, which multiplies every orientation by a positive factor
and sorts the images by x. Its gons are convex gons of the point set, because convexity
only depends on orientation signs.

`--mirror` adds the lex-leader `X(1,2,3) → X(N-3,N-2,N-1)`. Reflecting the point set in the
x-axis keeps `p` leftmost, reverses the slope order and turns `σ(i,j,k)` into
`σ(N-k,N-j,N-i)` on the points other than `p`, which swaps the two sides of the clause.
-/

namespace ETV

open ErdosSzekeres

/-! ### Gons of an arbitrary indexed point family -/

/-- A `K`-gon of the orientation signotope of any injective family in general position is a
convex `K`-gon (`K ≥ 4`). The family need not be sorted by x. -/
theorem hasConvexNGon_of_hasGon' (Q : ℕ → Point) {N K : ℕ}
    (hinj : Set.InjOn Q ↑(Finset.range N)) (hgp : GeneralPosition (ptSet Q N))
    (hσ : IsSignotope N (sigOf Q)) (hK : 4 ≤ K) (h : HasGon (sigOf Q) N K) :
    HasConvexNGon K (ptSet Q N) := by
  classical
  have hne : ∀ i j k, i < j → j < k → k < N → orient (Q i) (Q j) (Q k) ≠ 0 := by
    intro i j k hij hjk hk
    have hi : i ∈ (↑(Finset.range N) : Set ℕ) := by simp; omega
    have hj : j ∈ (↑(Finset.range N) : Set ℕ) := by simp; omega
    have hk' : k ∈ (↑(Finset.range N) : Set ℕ) := by simp; omega
    refine (generalPosition_iff_orient_ne_zero _).1 hgp _ (mem_ptSet (by omega)) _
      (mem_ptSet (by omega)) _ (mem_ptSet hk) ?_ ?_ ?_
    · exact fun e => (ne_of_lt hij) (hinj hi hj e)
    · exact fun e => (ne_of_lt (lt_trans hij hjk)) (hinj hi hk' e)
    · exact fun e => (ne_of_lt hjk) (hinj hj hk' e)
  obtain ⟨G, hcard, hGN, hquad⟩ := h.vertices hσ
  have hinjG : Set.InjOn Q ↑G := by
    intro i hi j hj hij
    exact hinj (by simpa using hGN i hi) (by simpa using hGN j hj) hij
  refine ⟨G.image Q, ?_, ?_, ?_⟩
  · intro p hp
    simp only [Finset.mem_image] at hp
    obtain ⟨i, hi, rfl⟩ := hp
    exact mem_ptSet (hGN i hi)
  · rw [Finset.card_image_of_injOn hinjG, hcard]
  · apply Suk.convexPosition_of_four_subsets (by rw [Finset.card_image_of_injOn hinjG]; omega)
    intro T hT hT4
    obtain ⟨U, hUG, rfl⟩ := Finset.subset_image_iff.1 hT
    have hU4 : U.card = 4 := by
      rw [Finset.card_image_of_injOn (hinjG.mono (by simpa using hUG))] at hT4
      exact hT4
    let e := U.orderEmbOfFin hU4
    have hem (i : Fin 4) : e i ∈ G := hUG (Finset.orderEmbOfFin_mem U hU4 i)
    have hT' : U.image Q = {Q (e 0), Q (e 1), Q (e 2), Q (e 3)} := by
      rw [← Finset.image_orderEmbOfFin_univ U hU4, Finset.image_image]
      have hf : (Finset.univ : Finset (Fin 4)) = {0, 1, 2, 3} := by decide
      rw [hf]
      simp [e]
    rw [hT']
    have h01 : e 0 < e 1 := e.strictMono (by decide)
    have h12 : e 1 < e 2 := e.strictMono (by decide)
    have h23 : e 2 < e 3 := e.strictMono (by decide)
    have h3N : e 3 < N := hGN _ (hem 3)
    rw [convexPosition_four_iff_signs _ _ _ _ (hne _ _ _ h01 h12 (by omega))
      (hne _ _ _ h01 (lt_trans h12 h23) h3N) (hne _ _ _ (lt_trans h01 h12) h23 h3N)
      (hne _ _ _ h12 h23 h3N)]
    left
    exact hquad _ (hem 0) _ (hem 1) _ (hem 2) _ (hem 3) h01 h12 h23

/-! ### The projective normal form -/

/-- Slope of `q` seen from `p`. -/
noncomputable def slope (p q : Point) : ℝ := (q 1 - p 1) / (q 0 - p 0)

/-- The projective map sending `p` to vertical infinity. -/
noncomputable def proj (p q : Point) : Point := ![slope p q, 1 / (q 0 - p 0)]

theorem orient_proj (p a b c : Point) (ha : a 0 - p 0 ≠ 0) (hb : b 0 - p 0 ≠ 0)
    (hc : c 0 - p 0 ≠ 0) :
    orient a b c =
      orient (proj p a) (proj p b) (proj p c) * ((a 0 - p 0) * (b 0 - p 0) * (c 0 - p 0)) := by
  simp only [orient, proj, slope, Matrix.cons_val_zero, Matrix.cons_val_one]
  field_simp
  ring

theorem orient_from (p a b : Point) (ha : a 0 - p 0 ≠ 0) (hb : b 0 - p 0 ≠ 0) :
    orient p a b = (a 0 - p 0) * (b 0 - p 0) * (slope p b - slope p a) := by
  simp only [orient, slope]
  field_simp

/-- `Q 0` is strictly left of `Q 1, …, Q (N-1)`, which are sorted by slope seen from `Q 0`. -/
structure HullFrame (Q : ℕ → Point) (N : ℕ) : Prop where
  right : ∀ i, 1 ≤ i → i < N → Q 0 0 < Q i 0
  slope_lt : ∀ i j, 1 ≤ i → i < j → j < N → slope (Q 0) (Q i) < slope (Q 0) (Q j)

theorem HullFrame.hullForm {Q : ℕ → Point} {N : ℕ} (h : HullFrame Q N) :
    HullForm N (sigOf Q) := by
  intro i j hi hij hj
  have h1 := h.right i hi (by omega)
  have h2 := h.right j (by omega) hj
  have h3 := h.slope_lt i j hi hij hj
  simp only [sigOf, decide_eq_true_eq]
  rw [orient_from _ _ _ (by linarith) (by linarith)]
  apply mul_pos (mul_pos (by linarith) (by linarith))
  linarith

theorem HullFrame.isSignotope {Q : ℕ → Point} {N : ℕ} (h : HullFrame Q N) :
    IsSignotope N (sigOf Q) := by
  intro i j k l hij hjk hkl hl
  rcases Nat.eq_zero_or_pos i with rfl | hi
  · have e1 := h.hullForm j k (by omega) hjk (by omega)
    have e2 := h.hullForm j l (by omega) (by omega) hl
    have e3 := h.hullForm k l (by omega) hkl hl
    rw [e1, e2, e3]
    cases sigOf Q j k l <;> decide
  · let R := fun m => proj (Q 0) (Q m)
    have hpos : ∀ m, 1 ≤ m → m < N → 0 < Q m 0 - Q 0 0 := fun m h1 h2 => by
      have := h.right m h1 h2
      linarith
    have sgn : ∀ a b c, 1 ≤ a → a < b → b < c → c < N →
        sigOf Q a b c = decide (0 < orient (R a) (R b) (R c)) := by
      intro a b c ha hab hbc hc
      have pa := hpos a ha (by omega)
      have pb := hpos b (by omega) (by omega)
      have pc := hpos c (by omega) hc
      simp only [sigOf, R]
      have hprod : 0 < (Q a 0 - Q 0 0) * (Q b 0 - Q 0 0) * (Q c 0 - Q 0 0) :=
        mul_pos (mul_pos pa pb) pc
      rw [decide_eq_decide, orient_proj (Q 0) (Q a) (Q b) (Q c) pa.ne' pb.ne' pc.ne']
      exact mul_pos_iff_of_pos_right hprod
    rw [sgn i j k hi hij hjk (by omega), sgn i j l hi hij (by omega) hl,
      sgn i k l hi (by omega) hkl hl, sgn j k l (by omega) hjk hkl hl]
    have x1 : R i 0 < R j 0 := h.slope_lt i j hi hij (by omega)
    have x2 : R j 0 < R k 0 := h.slope_lt j k (by omega) hjk (by omega)
    have x3 : R k 0 < R l 0 := h.slope_lt k l (by omega) hkl hl
    exact packetValid_of_xordered _ _ _ _ x1 x2 x3

theorem HullFrame.injOn {Q : ℕ → Point} {N : ℕ} (h : HullFrame Q N) :
    Set.InjOn Q ↑(Finset.range N) := by
  have key : ∀ i j, i < j → j < N → Q i ≠ Q j := by
    intro i j hlt hj e
    rcases Nat.eq_zero_or_pos i with rfl | hi0
    · have := h.right j (by omega) hj
      rw [← e] at this
      exact lt_irrefl _ this
    · have := h.slope_lt i j hi0 hlt hj
      rw [e] at this
      exact lt_irrefl _ this
  intro i hi j hj hij
  simp only [Finset.coe_range, Set.mem_Iio] at hi hj
  rcases lt_trichotomy i j with hlt | heq | hgt
  · exact absurd hij (key i j hlt hj)
  · exact heq
  · exact absurd hij.symm (key j i hgt hi)

/-- Every finite set in general position with distinct x-coordinates has a hull frame. -/
theorem exists_hullFrame (S : Finset Point) (hgp : GeneralPosition S)
    (hS : LowerBound.DistinctX S) (hne : S.Nonempty) :
    ∃ Q : ℕ → Point, HullFrame Q S.card ∧ ptSet Q S.card = S := by
  classical
  obtain ⟨p, hp, hmin⟩ := S.exists_min_image (fun q => q 0) hne
  have hright : ∀ q ∈ S.erase p, p 0 < q 0 := by
    intro q hq
    obtain ⟨hqp, hq⟩ := Finset.mem_erase.1 hq
    rcases eq_or_lt_of_le (hmin q hq) with e | e
    · exact absurd (hS hq hp e.symm) hqp
    · exact e
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
  have hQ : ∀ i, 1 ≤ i → i < S.card → Q i ∈ S.erase p ∧ f (Q i) = P' (i - 1) := by
    intro i hi hiN
    obtain ⟨q, hq, hfq⟩ := hmemP' (i - 1) (by omega)
    have : Q i = q := by
      simp only [Q, if_neg (show i ≠ 0 by omega)]
      rw [← hfq, hfinv q hq]
    rw [this]
    exact ⟨hq, hfq⟩
  refine ⟨Q, ⟨?_, ?_⟩, ?_⟩
  · intro i hi hiN
    have hQ0 : Q 0 = p := by simp [Q]
    rw [hQ0]
    exact hright _ (hQ i hi hiN).1
  · intro i j hi hij hj
    have hQ0 : Q 0 = p := by simp [Q]
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

/-! ### Reflection in the x-axis -/

/-- The reflection `(x, y) ↦ (x, -y)`. -/
def reflY : Point →ₗ[ℝ] Point where
  toFun p := ![p 0, -p 1]
  map_add' p q := by
    ext i
    fin_cases i
    all_goals simp
    all_goals ring
  map_smul' c p := by
    ext i
    fin_cases i
    all_goals simp

@[simp] theorem reflY_zero (p : Point) : reflY p 0 = p 0 := rfl

@[simp] theorem reflY_one (p : Point) : reflY p 1 = -p 1 := rfl

theorem reflY_reflY (p : Point) : reflY (reflY p) = p := by
  ext i
  fin_cases i <;> simp

theorem reflY_injective : Function.Injective reflY := fun p q h => by
  rw [← reflY_reflY p, h, reflY_reflY]

theorem orient_reflY (a b c : Point) : orient (reflY a) (reflY b) (reflY c) = -orient a b c := by
  simp only [orient, reflY_zero, reflY_one]
  ring

/-- The mirrored frame: `p` reflected, then the other points reflected in reverse order. -/
def mirrorFrame (Q : ℕ → Point) (N : ℕ) : ℕ → Point :=
  fun i => if i = 0 then reflY (Q 0) else reflY (Q (N - i))

theorem HullFrame.mirror {Q : ℕ → Point} {N : ℕ} (h : HullFrame Q N) :
    HullFrame (mirrorFrame Q N) N := by
  have hsl : ∀ q, slope (reflY (Q 0)) (reflY q) = -slope (Q 0) q := by
    intro q
    simp only [slope, reflY_zero, reflY_one]
    ring
  have hm0 : mirrorFrame Q N 0 = reflY (Q 0) := by simp [mirrorFrame]
  have hmi : ∀ i, i ≠ 0 → mirrorFrame Q N i = reflY (Q (N - i)) := by
    intro i hi
    simp [mirrorFrame, hi]
  constructor
  · intro i hi hiN
    rw [hm0, hmi i (by omega), reflY_zero, reflY_zero]
    exact h.right (N - i) (by omega) (by omega)
  · intro i j hi hij hj
    rw [hm0, hmi i (by omega), hmi j (by omega), hsl, hsl]
    have := h.slope_lt (N - j) (N - i) (by omega) (by omega) (by omega)
    linarith

theorem sigOf_mirrorFrame {Q : ℕ → Point} {N i j k : ℕ} (hi : 1 ≤ i) (hij : i < j)
    (hjk : j < k) :
    sigOf (mirrorFrame Q N) i j k = sigOf Q (N - k) (N - j) (N - i) := by
  simp only [sigOf, mirrorFrame, if_neg (show i ≠ 0 by omega), if_neg (show j ≠ 0 by omega),
    if_neg (show k ≠ 0 by omega), orient_reflY]
  congr 1
  apply propext
  simp only [orient]
  constructor <;> intro h <;> linarith

theorem ptSet_mirrorFrame {Q : ℕ → Point} {N : ℕ} (hN : 1 ≤ N) :
    ptSet (mirrorFrame Q N) N = (ptSet Q N).image reflY := by
  classical
  ext q
  simp only [ptSet, Finset.mem_image, Finset.mem_range]
  constructor
  · rintro ⟨i, hi, rfl⟩
    rcases Nat.eq_zero_or_pos i with rfl | hi0
    · exact ⟨Q 0, ⟨0, hN, rfl⟩, by simp [mirrorFrame]⟩
    · exact ⟨Q (N - i), ⟨N - i, by omega, rfl⟩, by
        simp [mirrorFrame, show i ≠ 0 by omega]⟩
  · rintro ⟨_, ⟨i, hi, rfl⟩, rfl⟩
    rcases Nat.eq_zero_or_pos i with rfl | hi0
    · exact ⟨0, hN, by simp [mirrorFrame]⟩
    · refine ⟨N - i, by omega, ?_⟩
      simp only [mirrorFrame, if_neg (show N - i ≠ 0 by omega),
        show N - (N - i) = i by omega]

/-! ### Soundness at the point-set level -/

theorem generalPosition_image_reflY {S : Finset Point} (h : GeneralPosition S) :
    GeneralPosition (S.image reflY) := by
  classical
  rw [generalPosition_iff_orient_ne_zero] at h ⊢
  intro a ha b hb c hc hab hac hbc
  obtain ⟨a', ha', rfl⟩ := Finset.mem_image.1 ha
  obtain ⟨b', hb', rfl⟩ := Finset.mem_image.1 hb
  obtain ⟨c', hc', rfl⟩ := Finset.mem_image.1 hc
  rw [orient_reflY, neg_ne_zero]
  exact h a' ha' b' hb' c' hc' (fun e => hab (e ▸ rfl)) (fun e => hac (e ▸ rfl))
    (fun e => hbc (e ▸ rfl))

theorem not_hasConvexNGon_image_reflY {S : Finset Point} {K : ℕ}
    (h : ¬HasConvexNGon K S) : ¬HasConvexNGon K (S.image reflY) := by
  classical
  rintro ⟨T', hT', hcard, hconv⟩
  apply h
  refine ⟨T'.image reflY, ?_, ?_, ?_⟩
  · intro q hq
    obtain ⟨t, ht, rfl⟩ := Finset.mem_image.1 hq
    obtain ⟨s, hs, rfl⟩ := Finset.mem_image.1 (hT' ht)
    rw [reflY_reflY]
    exact hs
  · rw [Finset.card_image_of_injective _ reflY_injective, hcard]
  · apply convexPosition_of_image_linear reflY reflY_injective
    have : (T'.image reflY).image reflY = T' := by
      rw [Finset.image_image]
      conv_rhs => rw [← Finset.image_id (s := T')]
      apply Finset.image_congr
      intro p _
      exact reflY_reflY p
    rw [this]
    exact hconv

/-- **What an UNSAT certificate for `gen_cnf.py N K --hull [--mirror] [--no-mono]` proves**
(`N ≥ 3`, `K ≥ 4`): every `N` points in general position contain a convex `K`-gon. -/
theorem forcesConvexNGon_of_unsat_hull {N K : ℕ} {mirror mono : Bool}
    (hunsat : ¬DimacsSatisfiable (dimacsB N K true mirror false mono)) (hN : 3 ≤ N)
    (hK : 4 ≤ K) : ForcesConvexNGon N K := by
  apply distinctXReduction N K
  intro S hgp hS hcard
  subst hcard
  by_contra hno
  have hne : S.Nonempty := Finset.card_pos.1 (by omega)
  obtain ⟨Q, hQ, hQS⟩ := exists_hullFrame S hgp hS hne
  -- a hull frame of a set with no convex `K`-gon has no `K`-gon
  have noGon : ∀ Q' : ℕ → Point, HullFrame Q' S.card → GeneralPosition (ptSet Q' S.card) →
      ¬HasConvexNGon K (ptSet Q' S.card) → ¬HasGon (sigOf Q') S.card K :=
    fun Q' hQ' hgp' hno' hg =>
      hno' (hasConvexNGon_of_hasGon' Q' hQ'.injOn hgp' hQ'.isSignotope hK hg)
  have hgpQ : GeneralPosition (ptSet Q S.card) := by rw [hQS]; exact hgp
  have hnoQ : ¬HasConvexNGon K (ptSet Q S.card) := by rw [hQS]; exact hno
  by_cases hm : MirrorForm S.card (sigOf Q)
  · exact hunsat (dimacsB_satisfiable_of_signotope hN (by omega) hQ.isSignotope
      (noGon Q hQ hgpQ hnoQ) (fun _ => hQ.hullForm) (fun _ => hm) (by simp))
  · have hQ' := hQ.mirror
    have hpt := ptSet_mirrorFrame (Q := Q) (N := S.card) (by omega)
    have hgpQ' : GeneralPosition (ptSet (mirrorFrame Q S.card) S.card) := by
      rw [hpt]; exact generalPosition_image_reflY hgpQ
    have hnoQ' : ¬HasConvexNGon K (ptSet (mirrorFrame Q S.card) S.card) := by
      rw [hpt]; exact not_hasConvexNGon_image_reflY hnoQ
    refine hunsat (dimacsB_satisfiable_of_signotope hN (by omega) hQ'.isSignotope
      (noGon _ hQ' hgpQ' hnoQ') (fun _ => hQ'.hullForm) (fun _ => ?_) (by simp))
    intro h7 h123
    exfalso
    apply hm
    intro _ _
    have e := sigOf_mirrorFrame (Q := Q) (N := S.card) (i := 1) (j := 2) (k := 3)
      (by omega) (by omega) (by omega)
    rw [e] at h123
    by_contra hfalse
    have hfalse' : sigOf Q (S.card - 3) (S.card - 2) (S.card - 1) = false := by simpa using hfalse
    rw [hfalse'] at h123
    exact Bool.false_ne_true h123

/-- `n33k7hm.cnf`, the file of the ES(7) SAT runs, is `gen_cnf.py 33 7 --hull --mirror`, i.e.
`dimacsB 33 7 true true false true` (byte-identical; see the README). Its unsatisfiability
would prove the heptagon case of the Erdős–Szekeres conjecture. -/
theorem heptagonConjecture_of_unsat_n33k7hm
    (h : ¬DimacsSatisfiable (dimacsB 33 7 true true false true)) : HeptagonConjecture :=
  forcesConvexNGon_of_unsat_hull h (by norm_num) (by norm_num)

end ETV
