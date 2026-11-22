import AE33Geo.Sem

/-!
# AE33Geo.Sound: every clause `clauseOf` accepts is satisfied by the real assignment (DESIGN.md §2)

Hypotheses (`Ctx`): the base has 31 points, `pt 0..30` realize its labelled order type, all triples of `pt 0..32`
are non-degenerate, and no 7 indices containing 31 (p) or 32 (q) form a positive chain (no convex 7-gon through p
or q). Families: R2 (GP identity at the pivot, ε-weighted), AC (barycentric identity), RAD (Radon identity),
GP (3-term Plücker identity), OCT and JK (`insert_pos`, i.e. the slot lemma).
-/

namespace AE33Geo
open ErdosSzekeres AE33

structure Ctx (B : Array Pt) (pt : ℕ → Point) : Prop where
  size : B.size = 31
  real : Realizes31 B pt
  gp : ∀ i j k, i < 33 → j < 33 → k < 33 → i ≠ j → j ≠ k → i ≠ k → orient (pt i) (pt j) (pt k) ≠ 0
  no7 : ∀ L : List ℕ, L.length = 7 → (∀ x ∈ L, x < 33) → PosChain (fun r => pt (L.getD r 0)) 7 →
    31 ∉ L ∧ 32 ∉ L

theorem ac_id (a b c t : Point) : orient a b t + orient b c t + orient c a t = orient a b c := by
  simp only [orient]; ring

theorem rad_id (a b p q : Point) : orient b p q - orient a p q + orient a b q - orient a b p = 0 := by
  simp only [orient]; ring

theorem gp_id (e f g h i : Point) :
    orient e f g * orient e h i - orient e f h * orient e g i + orient e f i * orient e g h = 0 := by
  simp only [orient]; ring

theorem mem_dedupAdj (x : ℤ) (l : List ℤ) : x ∈ dedupAdj l ↔ x ∈ l := by
  induction l with
  | nil => simp [dedupAdj]
  | cons a rest ih =>
    cases rest with
    | nil => simp [dedupAdj]
    | cons b rest' =>
      have e : dedupAdj (a :: b :: rest') =
          if a == b then dedupAdj (b :: rest') else a :: dedupAdj (b :: rest') := rfl
      rw [e]
      split_ifs with h
      · rw [ih]; simp only [beq_iff_eq] at h; subst h; simp
      · simp only [List.mem_cons] at ih ⊢
        rw [ih]

theorem mem_sortLits (x : ℤ) (l : List ℤ) : x ∈ sortLits l ↔ x ∈ l := by
  unfold sortLits; rw [mem_dedupAdj, List.mem_mergeSort]

theorem of_ite_eq_some {α : Type} {c : Bool} {o : Option α} {v : α}
    (h : (if c = true then o else none) = some v) : c = true ∧ o = some v := by
  by_cases hc : c = true
  · rw [if_pos hc] at h; exact ⟨hc, h⟩
  · rw [if_neg hc] at h; cases h

theorem of_ite_none_eq_some {α : Type} {c : Bool} {a v : α}
    (h : (if c = true then none else some a) = some v) : a = v := by
  by_cases hc : c = true
  · rw [if_pos hc] at h; cases h
  · rw [if_neg hc] at h; cases h; rfl

section
variable {B : Array Pt} {pt : ℕ → Point}

theorem Ctx.lit (C : Ctx B pt) {i j k : ℕ} (hi : i < 33) (hj : j < 33) (hk : k < 33)
    (hij : i ≠ j) (hjk : j ≠ k) (hik : i ≠ k) (hnew : 31 ≤ i ∨ 31 ≤ j ∨ 31 ≤ k) :
    ∃ l, chi B i j k = .lit l ∧ l ≠ 0 ∧ (EncB.LitSat (realAssign pt) l ↔ 0 < orient (pt i) (pt j) (pt k)) :=
  chi_spec C.size pt hi hj hk hij hjk hik hnew (C.gp i j k hi hj hk hij hjk hik)

theorem litSat_unit {ν : ℕ → Bool} {l : ℤ} {O : ℝ} {e : ℤ} (he : e = 1 ∨ e = -1) (hl : l ≠ 0)
    (hO : O ≠ 0) (hs : EncB.LitSat ν l ↔ 0 < O) : EncB.LitSat ν (e * l) ↔ 0 < (e : ℝ) * O := by
  rcases he with rfl | rfl
  · simp [hs]
  · rw [neg_one_mul, litSat_neg hl, hs]
    push_cast
    constructor
    · intro h; have := lt_of_le_of_ne (not_lt.1 h) hO; linarith
    · intro h; linarith

theorem litSat_neg_iff {ν : ℕ → Bool} {l : ℤ} {O : ℝ} (hl : l ≠ 0) (hO : O ≠ 0)
    (hs : EncB.LitSat ν l ↔ 0 < O) : EncB.LitSat ν (-l) ↔ O < 0 := by
  rw [litSat_neg hl, hs]
  constructor
  · intro h; exact lt_of_le_of_ne (not_lt.1 h) hO
  · intro h; linarith

theorem cone_pos (C : Ctx B pt) {a x y : ℕ} (ha : a < 31) (hx : x < 31) (hy : y < 31)
    {ex ey : ℤ} (hex : ex = 1 ∨ ex = -1) (hey : ey = 1 ∨ ey = -1)
    (hc : ex * ey * osgn B a x y = 1) : 0 < (ex : ℝ) * ey * orient (pt a) (pt x) (pt y) := by
  obtain ⟨h1, h2⟩ := osgn_spec C.real ha hx hy
  have hneg : osgn B a x y = -1 → orient (pt a) (pt x) (pt y) < 0 := by
    intro h; have := h2.1 h; rw [or23] at this; linarith
  rcases hex with rfl | rfl <;> rcases hey with rfl | rfl
  · have : osgn B a x y = 1 := by linarith
    have := h1.1 this; push_cast; linarith
  · have : osgn B a x y = -1 := by linarith
    have := hneg this; push_cast; linarith
  · have : osgn B a x y = -1 := by linarith
    have := hneg this; push_cast; linarith
  · have : osgn B a x y = 1 := by linarith
    have := h1.1 this; push_cast; linarith

/-! ## R2 -/

theorem sound_r2 (C : Ctx B pt) {w a x y z : ℕ} {ex ey ez : ℤ} {pol : Bool} {cl : List ℤ}
    (h : clauseOf B (.r2 w a x y z ex ey ez pol) = some cl) : ∃ l ∈ cl, EncB.LitSat (realAssign pt) l := by
  simp only [clauseOf, C.size] at h
  obtain ⟨hc, h⟩ := of_ite_eq_some h
  simp only [Bool.and_eq_true, decide_eq_true_eq, bne_iff_ne, ne_eq, beq_iff_eq, isUnit, Bool.or_eq_true,
    and_assoc] at hc
  obtain ⟨hw, ha, hx, hy, hz, hax, hay, haz, hxy, hyz, hxz, hex, hey, hez, c1, c2, c3⟩ := hc
  obtain ⟨lx, hlx, hlx0, hsx⟩ := C.lit (i := a) (j := x) (k := 31 + w) (by omega) (by omega) (by omega)
    hax (by omega) (by omega) (by omega)
  obtain ⟨ly, hly, hly0, hsy⟩ := C.lit (i := a) (j := y) (k := 31 + w) (by omega) (by omega) (by omega)
    hay (by omega) (by omega) (by omega)
  obtain ⟨lz, hlz, hlz0, hsz⟩ := C.lit (i := a) (j := z) (k := 31 + w) (by omega) (by omega) (by omega)
    haz (by omega) (by omega) (by omega)
  rw [hlx, hly, hlz] at h
  have gx := C.gp a x (31 + w) (by omega) (by omega) (by omega) hax (by omega) (by omega)
  have gy := C.gp a y (31 + w) (by omega) (by omega) (by omega) hay (by omega) (by omega)
  have gz := C.gp a z (31 + w) (by omega) (by omega) (by omega) haz (by omega) (by omega)
  have sx := litSat_unit hex hlx0 gx hsx
  have sy := litSat_unit hey hly0 gy hsy
  have sz := litSat_unit hez hlz0 gz hsz
  have hex0 : ex * lx ≠ 0 := by rcases hex with rfl | rfl <;> omega
  have hey0 : ey * ly ≠ 0 := by rcases hey with rfl | rfl <;> omega
  have hez0 : ez * lz ≠ 0 := by rcases hez with rfl | rfl <;> omega
  have kXY := cone_pos C ha hx hy hex hey c1
  have kYZ := cone_pos C ha hy hz hey hez c2
  have kXZ := cone_pos C ha hx hz hex hez c3
  have key : ((ex : ℝ) * ez * orient (pt a) (pt x) (pt z)) * (ey * orient (pt a) (pt y) (pt (31 + w))) =
      ((ey : ℝ) * ez * orient (pt a) (pt y) (pt z)) * (ex * orient (pt a) (pt x) (pt (31 + w))) +
      ((ex : ℝ) * ey * orient (pt a) (pt x) (pt y)) * (ez * orient (pt a) (pt z) (pt (31 + w))) := by
    linear_combination ((ex : ℝ) * ey * ez) * gp3 (pt a) (pt x) (pt y) (pt z) (pt (31 + w))
  by_contra hall
  push_neg at hall
  rcases pol with _ | _
  · simp only [↓reduceIte, Bool.false_eq_true] at h
    obtain ⟨-, h⟩ := of_ite_eq_some h
    cases h
    have n1 := hall (-(ex * lx)) (by simp)
    have n2 := hall (ey * ly) (by simp)
    have n3 := hall (-(ez * lz)) (by simp)
    rw [litSat_neg hex0, not_not, sx] at n1
    rw [sy] at n2
    rw [litSat_neg hez0, not_not, sz] at n3
    nlinarith [mul_pos kYZ n1, mul_pos kXY n3, mul_nonneg kXZ.le (neg_nonneg.2 (not_lt.1 n2))]
  · simp only [↓reduceIte] at h
    obtain ⟨-, h⟩ := of_ite_eq_some h
    cases h
    have n1 := hall (ex * lx) (by simp)
    have n2 := hall (-(ey * ly)) (by simp)
    have n3 := hall (ez * lz) (by simp)
    rw [sx] at n1
    rw [litSat_neg hey0, not_not, sy] at n2
    rw [sz] at n3
    nlinarith [mul_pos kXZ n2, mul_nonneg kYZ.le (neg_nonneg.2 (not_lt.1 n1)),
      mul_nonneg kXY.le (neg_nonneg.2 (not_lt.1 n3))]

/-! ## AC -/

theorem sound_ac (C : Ctx B pt) {w a b c : ℕ} {cl : List ℤ}
    (h : clauseOf B (.ac w a b c) = some cl) : ∃ l ∈ cl, EncB.LitSat (realAssign pt) l := by
  simp only [clauseOf, C.size] at h
  obtain ⟨hc, h⟩ := of_ite_eq_some h
  simp only [Bool.and_eq_true, decide_eq_true_eq, bne_iff_ne, ne_eq, isUnit, Bool.or_eq_true, beq_iff_eq,
    and_assoc] at hc
  obtain ⟨hw, ha, hb, hc', hab, hbc, hac, hs⟩ := hc
  obtain ⟨l1, h1, h10, hs1⟩ := C.lit (i := a) (j := b) (k := 31 + w) (by omega) (by omega) (by omega)
    hab (by omega) (by omega) (by omega)
  obtain ⟨l2, h2, h20, hs2⟩ := C.lit (i := b) (j := c) (k := 31 + w) (by omega) (by omega) (by omega)
    hbc (by omega) (by omega) (by omega)
  obtain ⟨l3, h3, h30, hs3⟩ := C.lit (i := c) (j := a) (k := 31 + w) (by omega) (by omega) (by omega)
    (Ne.symm hac) (by omega) (by omega) (by omega)
  rw [h1, h2, h3] at h
  simp only at h
  obtain ⟨-, h⟩ := of_ite_eq_some h
  cases h
  have g1 := C.gp a b (31 + w) (by omega) (by omega) (by omega) hab (by omega) (by omega)
  have g2 := C.gp b c (31 + w) (by omega) (by omega) (by omega) hbc (by omega) (by omega)
  have g3 := C.gp c a (31 + w) (by omega) (by omega) (by omega) (Ne.symm hac) (by omega) (by omega)
  have e1 := litSat_unit hs h10 g1 hs1
  have e2 := litSat_unit hs h20 g2 hs2
  have e3 := litSat_unit hs h30 g3 hs3
  have hO : 0 < (osgn B a b c : ℝ) * orient (pt a) (pt b) (pt c) := by
    obtain ⟨o1, o2⟩ := osgn_spec C.real ha hb hc'
    rcases hs with h | h
    · rw [h]; push_cast; rw [one_mul]; exact o1.1 h
    · rw [h]; have := o2.1 h; rw [or23] at this; push_cast; linarith
  by_contra hall
  push_neg at hall
  have n1 := hall (osgn B a b c * l1) (by simp)
  have n2 := hall (osgn B a b c * l2) (by simp)
  have n3 := hall (osgn B a b c * l3) (by simp)
  rw [e1] at n1
  rw [e2] at n2
  rw [e3] at n3
  have hid := ac_id (pt a) (pt b) (pt c) (pt (31 + w))
  have : (osgn B a b c : ℝ) * orient (pt a) (pt b) (pt (31 + w)) +
      (osgn B a b c : ℝ) * orient (pt b) (pt c) (pt (31 + w)) +
      (osgn B a b c : ℝ) * orient (pt c) (pt a) (pt (31 + w)) =
      (osgn B a b c : ℝ) * orient (pt a) (pt b) (pt c) := by rw [← hid]; ring
  linarith [not_lt.1 n1, not_lt.1 n2, not_lt.1 n3]

/-! ## The forbidden-sign families (RAD, GP) -/

theorem forbid_unpack {nv : ℕ} {terms : List Term} {sg : List ℤ} {pred : List ℤ → Bool} {cl : List ℤ}
    (h : forbidClause nv terms sg pred = some cl) :
    terms.length = sg.length ∧ (∀ s ∈ sg, s = 1 ∨ s = -1) ∧ pred sg = true ∧
    ∀ r, r < terms.length →
      (∀ c, terms.getD r (.const 0) = .const c → c = sg.getD r 0) ∧
      (∀ l, terms.getD r (.const 0) = .lit l → (if sg.getD r 0 == 1 then -l else l) ∈ cl) := by
  unfold forbidClause at h
  obtain ⟨hc, h⟩ := of_ite_eq_some h
  dsimp only at h
  obtain ⟨-, h⟩ := of_ite_eq_some h
  cases h
  simp only [Bool.and_eq_true, beq_iff_eq, List.all_eq_true] at hc
  obtain ⟨⟨⟨hlen, hunit⟩, hpred⟩, hall⟩ := hc
  refine ⟨hlen, fun s hs => by simpa [isUnit] using hunit s hs, hpred, fun r hr => ?_⟩
  have hr' : r < sg.length := hlen ▸ hr
  have hz : (terms[r], sg[r]) ∈ terms.zip sg := by
    rw [List.mem_iff_getElem]
    exact ⟨r, by simp [List.length_zip]; omega, by simp [List.getElem_zip]⟩
  have hgt : terms.getD r (.const 0) = terms[r] := by simp [List.getD_eq_getElem?_getD, hr]
  have hgs : sg.getD r 0 = sg[r] := by simp [List.getD_eq_getElem?_getD, hr']
  rw [hgt, hgs]
  refine ⟨fun c hc => ?_, fun l hl => ?_⟩
  · have := hall _ hz
    simp only [hc] at this
    simpa using this
  · rw [mem_sortLits]
    exact List.mem_filterMap.2 ⟨_, hz, by simp [hl]⟩

/-- The real sign of one term of a forbidden-sign clause, when the clause is falsified. -/
theorem term_sign (C : Ctx B pt) {α β γ : ℕ} (hα : α < 33) (hβ : β < 33) (hγ : γ < 33)
    (hαβ : α ≠ β) (hβγ : β ≠ γ) (hαγ : α ≠ γ) {s : ℤ} (hs : s = 1 ∨ s = -1) {cl : List ℤ}
    (hconst : ∀ c, chi B α β γ = .const c → c = s)
    (hlit : ∀ l, chi B α β γ = .lit l → (if s == 1 then -l else l) ∈ cl)
    (hfals : ∀ l ∈ cl, ¬ EncB.LitSat (realAssign pt) l) :
    0 < (s : ℝ) * orient (pt α) (pt β) (pt γ) := by
  have hg := C.gp α β γ hα hβ hγ hαβ hβγ hαγ
  by_cases hnew : 31 ≤ α ∨ 31 ≤ β ∨ 31 ≤ γ
  · obtain ⟨l, hl, hl0, hsl⟩ := C.lit hα hβ hγ hαβ hβγ hαγ hnew
    have hm := hfals _ (hlit l hl)
    rcases hs with rfl | rfl
    · simp only [beq_self_eq_true, if_true] at hm
      rw [litSat_neg_iff hl0 hg hsl] at hm
      push_cast; rw [one_mul]; exact lt_of_le_of_ne (not_lt.1 hm) (Ne.symm hg)
    · have e : ((-1 : ℤ) == 1) = false := by decide
      simp only [e, Bool.false_eq_true, if_false] at hm
      rw [hsl] at hm
      push_cast; have := lt_of_le_of_ne (not_lt.1 hm) hg; linarith
  · push_neg at hnew
    obtain ⟨_, _, _, _, h3, _, _⟩ := sort3_spec α β γ hαβ hβγ hαγ
    have hc : chi B α β γ = .const (osgn B α β γ) := by
      simp only [chi, C.size]
      rw [if_pos (by omega)]
    have := hconst _ hc
    obtain ⟨o1, o2⟩ := osgn_spec C.real hnew.1 hnew.2.1 hnew.2.2
    rcases hs with rfl | rfl
    · push_cast; rw [one_mul]; exact o1.1 this
    · have := o2.1 this; rw [or23] at this; push_cast; linarith

theorem sound_rad (C : Ctx B pt) {a b : ℕ} {sg : List ℤ} {cl : List ℤ}
    (hd : clauseOf B (.rad a b sg) = some cl) : ∃ l ∈ cl, EncB.LitSat (realAssign pt) l := by
  simp only [clauseOf, C.size] at hd
  obtain ⟨hc, hd⟩ := of_ite_eq_some hd
  simp only [Bool.and_eq_true, decide_eq_true_eq, bne_iff_ne, ne_eq, and_assoc] at hc
  obtain ⟨ha, hb, hab⟩ := hc
  obtain ⟨hlen, hunit, hpred, hterm⟩ := forbid_unpack hd
  rcases sg with _ | ⟨s0, _ | ⟨s1, _ | ⟨s2, _ | ⟨s3, _ | ⟨s4, sg⟩⟩⟩⟩⟩ <;> simp at hlen
  simp only [radPred, Bool.and_eq_true, beq_iff_eq] at hpred
  obtain ⟨⟨f1, f2⟩, f3⟩ := hpred
  have u0 := hunit s0 (by simp)
  by_contra hall
  push_neg at hall
  have t0 := term_sign C (α := b) (β := 31) (γ := 32) (by omega) (by omega) (by omega) (by omega) (by omega)
    (by omega) u0 (fun c hc => by simpa [hc] using (hterm 0 (by simp)).1 c)
    (fun l hl => by simpa [hl] using (hterm 0 (by simp)).2 l) hall
  have t1 := term_sign C (α := a) (β := 31) (γ := 32) (by omega) (by omega) (by omega) (by omega) (by omega)
    (by omega) (hunit s1 (by simp)) (fun c hc => by simpa [hc] using (hterm 1 (by simp)).1 c)
    (fun l hl => by simpa [hl] using (hterm 1 (by simp)).2 l) hall
  have t2 := term_sign C (α := a) (β := b) (γ := 32) (by omega) (by omega) (by omega) hab (by omega)
    (by omega) (hunit s2 (by simp)) (fun c hc => by simpa [hc] using (hterm 2 (by simp)).1 c)
    (fun l hl => by simpa [hl] using (hterm 2 (by simp)).2 l) hall
  have t3 := term_sign C (α := a) (β := b) (γ := 31) (by omega) (by omega) (by omega) hab (by omega)
    (by omega) (hunit s3 (by simp)) (fun c hc => by simpa [hc] using (hterm 3 (by simp)).1 c)
    (fun l hl => by simpa [hl] using (hterm 3 (by simp)).2 l) hall
  have r1 : (s0 : ℝ) = -s1 := by exact_mod_cast f1
  have r2 : -(s1 : ℝ) = s2 := by exact_mod_cast f2
  have r3 : (s2 : ℝ) = -s3 := by exact_mod_cast f3
  have hid := rad_id (pt a) (pt b) (pt 31) (pt 32)
  have key : (s0 : ℝ) * orient (pt b) (pt 31) (pt 32) + (s1 : ℝ) * orient (pt a) (pt 31) (pt 32) +
      (s2 : ℝ) * orient (pt a) (pt b) (pt 32) + (s3 : ℝ) * orient (pt a) (pt b) (pt 31) = 0 := by
    linear_combination (s0 : ℝ) * hid + orient (pt a) (pt 31) (pt 32) * r1 -
      orient (pt a) (pt b) (pt 32) * r2 - orient (pt a) (pt b) (pt 32) * r1 +
      orient (pt a) (pt b) (pt 31) * r3 + orient (pt a) (pt b) (pt 31) * r2 +
      orient (pt a) (pt b) (pt 31) * r1
  linarith

theorem sound_gp (C : Ctx B pt) {e f g h i : ℕ} {sg : List ℤ} {cl : List ℤ}
    (hd : clauseOf B (.gp e f g h i sg) = some cl) : ∃ l ∈ cl, EncB.LitSat (realAssign pt) l := by
  simp only [clauseOf, C.size] at hd
  obtain ⟨hc, hd⟩ := of_ite_eq_some hd
  simp only [Bool.and_eq_true, decide_eq_true_eq, and_assoc] at hc
  obtain ⟨he, hf, hg, hh, hi, hnd⟩ := hc
  simp only [List.nodup_cons, List.mem_cons, List.mem_singleton, not_or, List.not_mem_nil,
    not_false_eq_true, List.nodup_nil, and_true] at hnd
  obtain ⟨⟨hef, heg, heh, hei⟩, ⟨hfg, hfh, hfi⟩, ⟨hgh, hgi⟩, hhi⟩ := hnd
  obtain ⟨hlen, hunit, hpred, hterm⟩ := forbid_unpack hd
  rcases sg with _ | ⟨s0, _ | ⟨s1, _ | ⟨s2, _ | ⟨s3, _ | ⟨s4, _ | ⟨s5, _ | ⟨s6, sg⟩⟩⟩⟩⟩⟩⟩ <;>
    simp at hlen
  simp only [gpPred, Bool.and_eq_true, beq_iff_eq] at hpred
  obtain ⟨f1, f2⟩ := hpred
  by_contra hall
  push_neg at hall
  have t0 := term_sign C (α := e) (β := f) (γ := g) he hf hg hef hfg heg (hunit s0 (by simp))
    (fun c hc => by simpa [hc] using (hterm 0 (by simp)).1 c)
    (fun l hl => by simpa [hl] using (hterm 0 (by simp)).2 l) hall
  have t1 := term_sign C (α := e) (β := h) (γ := i) he hh hi heh hhi hei (hunit s1 (by simp))
    (fun c hc => by simpa [hc] using (hterm 1 (by simp)).1 c)
    (fun l hl => by simpa [hl] using (hterm 1 (by simp)).2 l) hall
  have t2 := term_sign C (α := e) (β := f) (γ := h) he hf hh hef hfh heh (hunit s2 (by simp))
    (fun c hc => by simpa [hc] using (hterm 2 (by simp)).1 c)
    (fun l hl => by simpa [hl] using (hterm 2 (by simp)).2 l) hall
  have t3 := term_sign C (α := e) (β := g) (γ := i) he hg hi heg hgi hei (hunit s3 (by simp))
    (fun c hc => by simpa [hc] using (hterm 3 (by simp)).1 c)
    (fun l hl => by simpa [hl] using (hterm 3 (by simp)).2 l) hall
  have t4 := term_sign C (α := e) (β := f) (γ := i) he hf hi hef hfi hei (hunit s4 (by simp))
    (fun c hc => by simpa [hc] using (hterm 4 (by simp)).1 c)
    (fun l hl => by simpa [hl] using (hterm 4 (by simp)).2 l) hall
  have t5 := term_sign C (α := e) (β := g) (γ := h) he hg hh heg hgh heh (hunit s5 (by simp))
    (fun c hc => by simpa [hc] using (hterm 5 (by simp)).1 c)
    (fun l hl => by simpa [hl] using (hterm 5 (by simp)).2 l) hall
  have g1 : (s0 : ℝ) * s1 = -((s2 : ℝ) * s3) := by
    have : s0 * s1 = -(s2 * s3) := by rw [f1]; ring
    exact_mod_cast this
  have g2 : (s0 : ℝ) * s1 = s4 * s5 := by
    have : s0 * s1 = s4 * s5 := by rw [f1, f2]
    exact_mod_cast this
  have hid := gp_id (pt e) (pt f) (pt g) (pt h) (pt i)
  have key : ((s0 : ℝ) * orient (pt e) (pt f) (pt g)) * ((s1 : ℝ) * orient (pt e) (pt h) (pt i)) +
      ((s2 : ℝ) * orient (pt e) (pt f) (pt h)) * ((s3 : ℝ) * orient (pt e) (pt g) (pt i)) +
      ((s4 : ℝ) * orient (pt e) (pt f) (pt i)) * ((s5 : ℝ) * orient (pt e) (pt g) (pt h)) = 0 := by
    linear_combination ((s0 : ℝ) * s1) * hid + (orient (pt e) (pt f) (pt h) * orient (pt e) (pt g) (pt i)) * g1 -
      (orient (pt e) (pt f) (pt i) * orient (pt e) (pt g) (pt h)) * g2
  nlinarith [mul_pos t0 t1, mul_pos t2 t3, mul_pos t4 t5]

/-! ## Polygons from the orientation table -/

theorem posChain_of_ccwOk (C : Ctx B pt) {q : List ℕ} (hq : ∀ x ∈ q, x < 31) (hok : ccwOk B q = true) :
    PosChain (fun r => pt (q.getD r 0)) q.length := by
  intro a b c hab hbc hc
  have hmem : ∀ r, r < q.length → q.getD r 0 < 31 := fun r hr => by
    apply hq; rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hr]; exact List.getElem_mem hr
  unfold ccwOk at hok
  rw [List.all_eq_true] at hok
  have h1 := hok a (List.mem_range.2 (by omega))
  rw [List.all_eq_true] at h1
  have h2 := h1 b (List.mem_range.2 (by omega))
  rw [List.all_eq_true] at h2
  have h3 := h2 c (List.mem_range.2 hc)
  simp only [hab, hbc, decide_true, Bool.and_self, Bool.not_true, Bool.false_or, beq_iff_eq] at h3
  exact (osgn_spec C.real (hmem a (by omega)) (hmem b (by omega)) (hmem c hc)).1.1 h3

theorem getD_mem_of_lt {L : List ℕ} {r : ℕ} (hr : r < L.length) : L.getD r 0 ∈ L := by
  rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hr]; exact List.getElem_mem hr

theorem getD_ne_of_nodup {L : List ℕ} (hL : L.Nodup) {a b : ℕ} (ha : a < L.length) (hb : b < L.length)
    (hab : a ≠ b) : L.getD a 0 ≠ L.getD b 0 := by
  rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem ha, List.getD_eq_getElem?_getD,
    List.getElem?_eq_getElem hb]
  simp only [Option.getD_some]
  intro h
  exact hab ((List.Nodup.getElem_inj_iff hL).1 h)

/-! ## OCT -/

theorem sound_oct (C : Ctx B pt) {w : ℕ} {q : List ℕ} {cl : List ℤ}
    (hd : clauseOf B (.oct w q) = some cl) : ∃ l ∈ cl, EncB.LitSat (realAssign pt) l := by
  rcases q with _ | ⟨q0, _ | ⟨q1, _ | ⟨q2, _ | ⟨q3, _ | ⟨q4, _ | ⟨q5, _ | ⟨q6, q⟩⟩⟩⟩⟩⟩⟩ <;>
    simp only [clauseOf, reduceCtorEq] at hd
  simp only [C.size] at hd
  obtain ⟨hc, hd⟩ := of_ite_eq_some hd
  simp only [Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true, and_assoc] at hc
  obtain ⟨hw, hlt, hnd, hok⟩ := hc
  have hq : ∀ x ∈ [q0, q1, q2, q3, q4, q5], x < 31 := fun x hx => by simpa using hlt x hx
  have l0 : q0 < 31 := hq q0 (by simp)
  have l1 : q1 < 31 := hq q1 (by simp)
  have l2 : q2 < 31 := hq q2 (by simp)
  have l3 : q3 < 31 := hq q3 (by simp)
  have l4 : q4 < 31 := hq q4 (by simp)
  have l5 : q5 < 31 := hq q5 (by simp)
  have d50 : q5 ≠ q0 := getD_ne_of_nodup (L := [q0, q1, q2, q3, q4, q5]) hnd (a := 5) (b := 0)
    (by simp) (by simp) (by omega)
  have d45 : q4 ≠ q5 := getD_ne_of_nodup (L := [q0, q1, q2, q3, q4, q5]) hnd (a := 4) (b := 5)
    (by simp) (by simp) (by omega)
  have d01 : q0 ≠ q1 := getD_ne_of_nodup (L := [q0, q1, q2, q3, q4, q5]) hnd (a := 0) (b := 1)
    (by simp) (by simp) (by omega)
  obtain ⟨m1, hm1, hm10, hsm1⟩ := C.lit (i := q5) (j := q0) (k := 31 + w) (by omega) (by omega)
    (by omega) d50 (by omega) (by omega) (by omega)
  obtain ⟨m2, hm2, hm20, hsm2⟩ := C.lit (i := q4) (j := q5) (k := 31 + w) (by omega) (by omega)
    (by omega) d45 (by omega) (by omega) (by omega)
  obtain ⟨m3, hm3, hm30, hsm3⟩ := C.lit (i := q0) (j := q1) (k := 31 + w) (by omega) (by omega)
    (by omega) d01 (by omega) (by omega) (by omega)
  rw [hm1, hm2, hm3] at hd
  simp only at hd
  obtain ⟨-, hd⟩ := of_ite_eq_some hd
  cases hd
  by_contra hall
  push_neg at hall
  have n1 := hall m1 (by simp)
  have n2 := hall (-m2) (by simp)
  have n3 := hall (-m3) (by simp)
  have g1 := C.gp q5 q0 (31 + w) (by omega) (by omega) (by omega) d50 (by omega) (by omega)
  rw [hsm1] at n1
  rw [litSat_neg hm20, not_not, hsm2] at n2
  rw [litSat_neg hm30, not_not, hsm3] at n3
  have hpos := posChain_of_ccwOk C hq hok
  have H := insert_pos (P := pt) (c := [q0, q1, q2, q3, q4, q5]) (m := 6) rfl (by norm_num) hpos
    (j := 5) (by norm_num) (t := 31 + w) (by simpa using n2)
    (by simp only [List.getD_cons_succ, List.getD_cons_zero]; exact lt_of_le_of_ne (not_lt.1 n1) g1)
    (by simpa using n3)
  have hL : ([q0, q1, q2, q3, q4, q5].take (5 + 1) ++ [31 + w] ++ [q0, q1, q2, q3, q4, q5].drop (5 + 1)) =
      [q0, q1, q2, q3, q4, q5, 31 + w] := by simp
  rw [hL] at H
  have := C.no7 [q0, q1, q2, q3, q4, q5, 31 + w] (by simp)
    (fun x hx => by simp only [List.mem_cons, List.mem_singleton, List.not_mem_nil, or_false] at hx; omega) H
  rcases (by omega : w = 0 ∨ w = 1) with rfl | rfl
  · exact this.1 (by simp)
  · exact this.2 (by simp)

/-! ## JK -/

theorem sound_jk (C : Ctx B pt) {Q : List ℕ} {i j : ℕ} {cl : List ℤ}
    (hd : clauseOf B (.jk Q i j) = some cl) : ∃ l ∈ cl, EncB.LitSat (realAssign pt) l := by
  simp only [clauseOf, C.size] at hd
  obtain ⟨hc, hd⟩ := of_ite_eq_some hd
  simp only [Bool.and_eq_true, beq_iff_eq, decide_eq_true_eq, List.all_eq_true, and_assoc] at hc
  obtain ⟨hlen, hlt, hnd, hok, hi, hj⟩ := hc
  unfold jkClause at hd
  simp only [C.size] at hd
  -- the pentagon and the hexagon Q1
  have hQ : ∀ x ∈ Q, x < 31 := fun x hx => by simpa using hlt x hx
  set Q1 := Q.take (i + 1) ++ [31] ++ Q.drop (i + 1) with hQ1
  have hQ1len : Q1.length = 6 := by simp [hQ1, List.length_take, List.length_drop, hlen]; omega
  have hQ1lt : ∀ x ∈ Q1, x < 32 := by
    intro x hx
    simp only [hQ1, List.mem_append, List.mem_singleton] at hx
    rcases hx with (hx | hx) | hx
    · have := hQ x (List.mem_of_mem_take hx); omega
    · omega
    · have := hQ x (List.mem_of_mem_drop hx); omega
  have hQ1nd : Q1.Nodup := by
    have hperm : Q1.Perm (31 :: Q) := by
      rw [hQ1, List.append_assoc]
      have := (List.perm_middle (a := 31) (l₁ := Q.take (i + 1)) (l₂ := Q.drop (i + 1)))
      rw [List.singleton_append]
      exact this.trans (by rw [List.take_append_drop])
    rw [hperm.nodup_iff, List.nodup_cons]
    exact ⟨fun h => by have := hQ 31 h; omega, hnd⟩
  have mQ : ∀ r, r < 5 → Q.getD r 0 < 31 := fun r hr => hQ _ (getD_mem_of_lt (by omega))
  have mQ1 : ∀ r, r < 6 → Q1.getD r 0 < 32 := fun r hr => hQ1lt _ (getD_mem_of_lt (by omega))
  have dQ : ∀ a b, a < 5 → b < 5 → a ≠ b → Q.getD a 0 ≠ Q.getD b 0 :=
    fun a b ha hb hab => getD_ne_of_nodup hnd (by omega) (by omega) hab
  have dQ1 : ∀ a b, a < 6 → b < 6 → a ≠ b → Q1.getD a 0 ≠ Q1.getD b 0 :=
    fun a b ha hb hab => getD_ne_of_nodup hQ1nd (by omega) (by omega) hab
  have hm5 : ∀ r, r % 5 < 5 := fun r => Nat.mod_lt _ (by norm_num)
  have hm6 : ∀ r, r % 6 < 6 := fun r => Nat.mod_lt _ (by norm_num)
  -- the six literals
  obtain ⟨k1, hk1, hk10, hsk1⟩ := C.lit (i := Q.getD i 0) (j := Q.getD ((i + 1) % 5) 0) (k := 31)
    (by have := mQ i hi; omega) (by have := mQ _ (hm5 (i + 1)); omega) (by norm_num)
    (dQ _ _ hi (hm5 _) (by omega)) (by have := mQ _ (hm5 (i + 1)); omega) (by have := mQ i hi; omega)
    (by omega)
  obtain ⟨k2, hk2, hk20, hsk2⟩ := C.lit (i := Q.getD ((i + 4) % 5) 0) (j := Q.getD i 0) (k := 31)
    (by have := mQ _ (hm5 (i + 4)); omega) (by have := mQ i hi; omega) (by norm_num)
    (dQ _ _ (hm5 _) hi (by omega)) (by have := mQ i hi; omega) (by have := mQ _ (hm5 (i + 4)); omega)
    (by omega)
  obtain ⟨k3, hk3, hk30, hsk3⟩ := C.lit (i := Q.getD ((i + 1) % 5) 0) (j := Q.getD ((i + 2) % 5) 0)
    (k := 31) (by have := mQ _ (hm5 (i + 1)); omega) (by have := mQ _ (hm5 (i + 2)); omega) (by norm_num)
    (dQ _ _ (hm5 _) (hm5 _) (by omega)) (by have := mQ _ (hm5 (i + 2)); omega)
    (by have := mQ _ (hm5 (i + 1)); omega) (by omega)
  obtain ⟨k4, hk4, hk40, hsk4⟩ := C.lit (i := Q1.getD j 0) (j := Q1.getD ((j + 1) % 6) 0) (k := 32)
    (by have := mQ1 j hj; omega) (by have := mQ1 _ (hm6 (j + 1)); omega) (by norm_num)
    (dQ1 _ _ hj (hm6 _) (by omega)) (by have := mQ1 _ (hm6 (j + 1)); omega) (by have := mQ1 j hj; omega)
    (by omega)
  obtain ⟨k5, hk5, hk50, hsk5⟩ := C.lit (i := Q1.getD ((j + 5) % 6) 0) (j := Q1.getD j 0) (k := 32)
    (by have := mQ1 _ (hm6 (j + 5)); omega) (by have := mQ1 j hj; omega) (by norm_num)
    (dQ1 _ _ (hm6 _) hj (by omega)) (by have := mQ1 j hj; omega) (by have := mQ1 _ (hm6 (j + 5)); omega)
    (by omega)
  obtain ⟨k6, hk6, hk60, hsk6⟩ := C.lit (i := Q1.getD ((j + 1) % 6) 0) (j := Q1.getD ((j + 2) % 6) 0)
    (k := 32) (by have := mQ1 _ (hm6 (j + 1)); omega) (by have := mQ1 _ (hm6 (j + 2)); omega) (by norm_num)
    (dQ1 _ _ (hm6 _) (hm6 _) (by omega)) (by have := mQ1 _ (hm6 (j + 2)); omega)
    (by have := mQ1 _ (hm6 (j + 1)); omega) (by omega)
  rw [hk1, hk2, hk3, hk4, hk5, hk6] at hd
  simp only [Term.neg, neg_neg] at hd
  have hcl := of_ite_none_eq_some hd
  subst hcl
  by_contra hall
  push_neg at hall
  have n1 := hall k1 (by rw [mem_sortLits]; simp)
  have n2 := hall (-k2) (by rw [mem_sortLits]; simp)
  have n3 := hall (-k3) (by rw [mem_sortLits]; simp)
  have n4 := hall k4 (by rw [mem_sortLits]; simp)
  have n5 := hall (-k5) (by rw [mem_sortLits]; simp)
  have n6 := hall (-k6) (by rw [mem_sortLits]; simp)
  rw [hsk1] at n1
  rw [litSat_neg hk20, not_not, hsk2] at n2
  rw [litSat_neg hk30, not_not, hsk3] at n3
  rw [hsk4] at n4
  rw [litSat_neg hk50, not_not, hsk5] at n5
  rw [litSat_neg hk60, not_not, hsk6] at n6
  have g1 := C.gp (Q.getD i 0) (Q.getD ((i + 1) % 5) 0) 31 (by have := mQ i hi; omega)
    (by have := mQ _ (hm5 (i + 1)); omega) (by norm_num) (dQ _ _ hi (hm5 _) (by omega))
    (by have := mQ _ (hm5 (i + 1)); omega) (by have := mQ i hi; omega)
  have g4 := C.gp (Q1.getD j 0) (Q1.getD ((j + 1) % 6) 0) 32 (by have := mQ1 j hj; omega)
    (by have := mQ1 _ (hm6 (j + 1)); omega) (by norm_num) (dQ1 _ _ hj (hm6 _) (by omega))
    (by have := mQ1 _ (hm6 (j + 1)); omega) (by have := mQ1 j hj; omega)
  -- step 1: p into the pentagon
  have hposQ : PosChain (fun r => pt (Q.getD r 0)) 5 := by
    have := posChain_of_ccwOk C hQ hok; rwa [hlen] at this
  have e5 : (i + 5 - 1) % 5 = (i + 4) % 5 := by congr 1
  have H1 := insert_pos (P := pt) (c := Q) (m := 5) hlen (by norm_num) hposQ hi (t := 31)
    (by rw [e5]; exact n2) (lt_of_le_of_ne (not_lt.1 n1) g1) n3
  -- step 2: q into the hexagon
  have e6 : (j + 6 - 1) % 6 = (j + 5) % 6 := by congr 1
  have H2 := insert_pos (P := pt) (c := Q1) (m := 6) hQ1len (by norm_num) H1 hj (t := 32)
    (by rw [e6]; exact n5) (lt_of_le_of_ne (not_lt.1 n4) g4) n6
  set Q2 := Q1.take (j + 1) ++ [32] ++ Q1.drop (j + 1) with hQ2
  have hQ2len : Q2.length = 7 := by simp [hQ2, List.length_take, List.length_drop, hQ1len]; omega
  have hQ2lt : ∀ x ∈ Q2, x < 33 := by
    intro x hx
    simp only [hQ2, List.mem_append, List.mem_singleton] at hx
    rcases hx with (hx | hx) | hx
    · have := hQ1lt x (List.mem_of_mem_take hx); omega
    · omega
    · have := hQ1lt x (List.mem_of_mem_drop hx); omega
  have h32 : 32 ∈ Q2 := by simp [hQ2]
  exact (C.no7 Q2 hQ2len hQ2lt H2).2 h32

/-! ## All families -/

/-- **Soundness**: every clause that `clauseOf` returns is satisfied by the real assignment. -/
theorem clauseOf_sound (C : Ctx B pt) {d : Desc} {cl : List ℤ} (h : clauseOf B d = some cl) :
    ∃ l ∈ cl, EncB.LitSat (realAssign pt) l := by
  cases d with
  | r2 => exact sound_r2 C h
  | ac => exact sound_ac C h
  | rad => exact sound_rad C h
  | gp => exact sound_gp C h
  | oct => exact sound_oct C h
  | jk => exact sound_jk C h

/-- **The CNF is satisfied by the real assignment.** -/
theorem cnf_sat (C : Ctx B pt) : EncB.DimacsSatisfiable (cnf B) := by
  refine ⟨realAssign pt, fun cl hcl => ?_⟩
  obtain ⟨d, hd, -⟩ := mem_cnf hcl
  obtain ⟨l, hl, hs⟩ := clauseOf_sound C hd
  exact ⟨l, hl, hs⟩

end
end AE33Geo
