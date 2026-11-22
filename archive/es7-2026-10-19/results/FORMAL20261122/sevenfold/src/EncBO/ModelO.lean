import EncB.SoundOlit

/-!
# The combinatorial interface for odd `m` (`ModelO`), its intended assignment, and the literal semantics

Std-only. Built on ENCBLEAN's `EncB` package (imported read-only, unchanged). For odd `m` encoder B
(gen_b2.py, ported as `EncB.gen` and its functional twin `EncB.encB`) has, besides the variables of the even case,
the half-sector variables `H(i) = [θ_i < π/m]` (`Var.h`, gen_b2.py:40), and its angular patterns carry one bit
`h L ∈ {0,1}` per free layer (gen_b2.py:93-94) with the cell indices `J = (2k + h) mod 2m` of a point and
`(J + m) mod 2m` of its antipode (gen_b2.py:107-109).

**The cut.** `ModelO m K t` has the fields of ENCBLEAN's `Model m K t` (same names, same statements) plus the
half-sector bits `hb : ℕ → Bool` (`hb i` means `θ_i < π/m`, so the encoder's bit is `hbit hb i = 0`) with
`hb_zero : hb 0 = true`. Its two angular rules are stated on the **half-sector grid**: the label `a = (i, k)` is
lifted to `liftO hb a = (i, 2k + hbit hb i)`, a label of the `2m` directions `φ + ψ_i + s·π/m`, and the rules are
ENCBLEAN's `AltCCW`/`BlockCCW` **at `2m`** on the lifted labels. At `2m` (even) ENCBLEAN's `cell (2m) (a', false)`
is `(a'.2 + m) mod 2m`, which is exactly the encoder's antipode cell, so the circular order of the six objects of a
triple is ENCBLEAN's `objLt (2m) psiLt` on the lifted labels, and ψ is the phase modulo `π/m`.
-/

namespace EncB

/-- The encoder's half-sector bit of layer `i` (gen_b2.py:93-94): `0` iff `θ_i < π/m` (`hb i = true`). -/
def hbit (hb : Nat → Bool) (i : Nat) : Nat := if hb i then 0 else 1

/-- The label on the half-sector grid of `2m` directions: `(i, k) ↦ (i, 2k + hbit i)`. -/
def liftO (hb : Nat → Bool) (a : Pt) : Pt := (a.1, 2 * a.2 + hbit hb a.1)

/-- What `encB_satisfiable_odd` consumes (odd `m`). `chi a b d` means orient(P a, P b, P d) > 0, `psiLt i j`
means ψ_i < ψ_j with ψ = θ mod π/m, and `hb i` means θ_i < π/m. -/
structure ModelO (m K t : Nat) where
  chi   : Pt → Pt → Pt → Bool
  psiLt : Nat → Nat → Bool
  hb    : Nat → Bool
  psiLt_irrefl : ∀ i, psiLt i i = false
  psiLt_trans  : ∀ i j k, psiLt i j = true → psiLt j k = true → psiLt i k = true
  psiLt_total  : ∀ i j, i < t → j < t → i ≠ j → psiLt i j = true ∨ psiLt j i = true
  psiLt_zero   : ∀ i, 0 < i → i < t → psiLt 0 i = true
  hb_zero      : hb 0 = true
  chi_rot   : ∀ a b d, PtOk m t a → PtOk m t b → PtOk m t d →
                chi (rot m a) (rot m b) (rot m d) = chi a b d
  chi_cycle : ∀ a b d, PtOk m t a → PtOk m t b → PtOk m t d → Distinct3 a b d →
                chi b d a = chi a b d
  chi_swap  : ∀ a b d, PtOk m t a → PtOk m t b → PtOk m t d → Distinct3 a b d →
                chi a d b = !chi a b d
  ruleA : ∀ a b d, PtOk m t a → PtOk m t b → PtOk m t d → Distinct3 a b d →
            AltCCW (2 * m) psiLt (liftO hb a) (liftO hb b) (liftO hb d) → chi a b d = true
  ruleB : ∀ a b d, PtOk m t a → PtOk m t b → PtOk m t d → Distinct3 a b d →
            BlockCCW (2 * m) psiLt (liftO hb a) (liftO hb b) (liftO hb d) → b.1 ≤ a.1 → b.1 ≤ d.1 →
              chi a b d = true
  nest  : ∀ i j k, i < j → j < t → k < m → chi (i, 0) (i, 1) (j, k) = true
  noChain : ∀ i, i < t → ∀ q : Nat → Pt,
      (∀ s, s < K - 1 → InQ m t i (q s)) →
      (∀ s, s + 1 < K - 1 → chi (i, 0) (q s) (q (s + 1)) = true) →
      (∀ s, s + 2 < K - 1 → chi (q s) (q (s + 1)) (q (s + 2)) = true) → False

/-! ## The intended assignment (H ↦ `hb`; everything else as ENCBLEAN's `tauOf`) -/

/-- Values of the non-chain variables for odd `m`. -/
def baseValO (chi : Pt → Pt → Pt → Bool) (psiLt : Nat → Nat → Bool) (hb : Nat → Bool) : Var → Bool
  | .y i j => psiLt i j
  | .h i => hb i
  | .orb [a, b, d] => chi a b d
  | _ => false

/-- The intended assignment on variables (odd `m`). -/
def tauOfO (m t : Nat) (chi : Pt → Pt → Pt → Bool) (psiLt : Nat → Nat → Bool) (hb : Nat → Bool) : Var → Prop
  | .f i l a b => ChainFrom m t chi i l a b
  | v => baseValO chi psiLt hb v = true

def ModelO.τ {m K t : Nat} (M : ModelO m K t) : Var → Prop := tauOfO m t M.chi M.psiLt M.hb

/-- The assignment on codes, as `dimacsSat_of_holds` consumes it. -/
def ModelO.τc {m K t : Nat} (M : ModelO m K t) (n : Nat) : Prop := M.τ (decodeCode m K t n)

/-! ## Literal semantics (copies of ENCBLEAN's `ModelLemmas` statements for `ModelO`) -/

theorem ModelO.τc_code {m K t : Nat} (M : ModelO m K t) {v : Var} (hv : v.Valid m K t) :
    M.τc (v.code m K t) = M.τ v := by
  simp only [ModelO.τc, decodeCode_code hv]

theorem holds_yO {m K t : Nat} (M : ModelO m K t) {i j : Nat} (hi : i < t) (hj : j < t) :
    CodeLitHolds M.τc (yLit t i j) ↔ M.psiLt i j = true := by
  have h := M.τc_code (v := .y i j) ⟨hi, hj⟩
  simp only [Var.code] at h
  rw [yLit, codeLitHolds_pos (by simp only [yCode]; omega), h]
  rfl

theorem holds_hO {m K t : Nat} (M : ModelO m K t) {i : Nat} (hi : i < t) :
    CodeLitHolds M.τc (hLit t i) ↔ M.hb i = true := by
  have h := M.τc_code (v := .h i) hi
  simp only [Var.code] at h
  rw [hLit, codeLitHolds_pos (by simp only [hCode]; omega), h]
  rfl

theorem holds_orbO {m K t : Nat} (M : ModelO m K t) {a b d : Pt} (ha : PtOk m t a) (hb : PtOk m t b)
    (hd : PtOk m t d) : CodeLitHolds M.τc (orbCode m t [a, b, d] : Int) ↔ M.chi a b d = true := by
  have h := M.τc_code (v := .orb [a, b, d]) ⟨a, b, d, rfl, ha, hb, hd⟩
  simp only [Var.code] at h
  rw [codeLitHolds_pos (by simp only [orbCode, oBase]; omega), h]
  rfl

theorem holds_fO {m K t : Nat} (M : ModelO m K t) {i l : Nat} {a b : Pt} (hi : i < t) (hl : l < chainFL K)
    (ha : PtOk m t a) (hb : PtOk m t b) :
    CodeLitHolds M.τc (fCode m K t i l a b : Int) ↔ ChainFrom m t M.chi i l a b := by
  have h := M.τc_code (v := .f i l a b) ⟨hi, hl, ha, hb⟩
  simp only [Var.code] at h
  rw [codeLitHolds_pos (by simp only [fCode, fBase, oBase]; omega), h]
  rfl

/-- `chi` of a reordered triple (copy of ENCBLEAN's `chi_perm3` for `ModelO`). -/
theorem chi_perm3O {m K t : Nat} (M : ModelO m K t) {c0 c1 c2 : Pt} (h0 : PtOk m t c0) (h1 : PtOk m t c1)
    (h2 : PtOk m t c2) (hd : Distinct3 c0 c1 c2) {s : List Nat} (hs : s.Perm [0, 1, 2]) :
    M.chi ([c0, c1, c2].getD (s.getD 0 0) (0, 0)) ([c0, c1, c2].getD (s.getD 1 0) (0, 0))
        ([c0, c1, c2].getD (s.getD 2 0) (0, 0)) =
      (if permSign s > 0 then M.chi c0 c1 c2 else !M.chi c0 c1 c2) := by
  obtain ⟨d01, d02, d12⟩ := hd
  have cyc := M.chi_cycle
  have swp := M.chi_swap
  rcases perm012_cases hs with rfl | rfl | rfl | rfl | rfl | rfl
  · rfl
  · simp only [List.getD, List.getElem?_cons_zero, List.getElem?_cons_succ, Option.getD_some]
    rw [swp c0 c1 c2 h0 h1 h2 ⟨d01, d02, d12⟩]; rfl
  · simp only [List.getD, List.getElem?_cons_zero, List.getElem?_cons_succ, Option.getD_some]
    rw [← cyc c1 c0 c2 h1 h0 h2 ⟨Ne.symm d01, d12, d02⟩, swp c0 c1 c2 h0 h1 h2 ⟨d01, d02, d12⟩]; rfl
  · simp only [List.getD, List.getElem?_cons_zero, List.getElem?_cons_succ, Option.getD_some]
    rw [cyc c0 c1 c2 h0 h1 h2 ⟨d01, d02, d12⟩]; rfl
  · simp only [List.getD, List.getElem?_cons_zero, List.getElem?_cons_succ, Option.getD_some]
    rw [← cyc c0 c1 c2 h0 h1 h2 ⟨d01, d02, d12⟩, cyc c1 c2 c0 h1 h2 h0 ⟨d12, Ne.symm d01, Ne.symm d02⟩]; rfl
  · simp only [List.getD, List.getElem?_cons_zero, List.getElem?_cons_succ, Option.getD_some]
    rw [swp c2 c0 c1 h2 h0 h1 ⟨Ne.symm d02, Ne.symm d12, d01⟩,
      ← cyc c0 c1 c2 h0 h1 h2 ⟨d01, d02, d12⟩, cyc c1 c2 c0 h1 h2 h0 ⟨d12, Ne.symm d01, Ne.symm d02⟩]; rfl

/-! ## `olit` is the orientation literal (copy of ENCBLEAN's `olitSpec` for `ModelO`) -/

theorem chi_rotByO {m K t : Nat} (M : ModelO m K t) {a b d : Pt} (ha : PtOk m t a) (hb : PtOk m t b)
    (hd : PtOk m t d) : ∀ s, M.chi (rotBy m s a) (rotBy m s b) (rotBy m s d) = M.chi a b d
  | 0 => by
    simp only [rotBy, Nat.add_zero, Nat.mod_eq_of_lt ha.2, Nat.mod_eq_of_lt hb.2, Nat.mod_eq_of_lt hd.2]
  | s + 1 => by
    rw [rotBy_succ, rotBy_succ, rotBy_succ,
      M.chi_rot _ _ _ (ptOk_rotBy ha) (ptOk_rotBy hb) (ptOk_rotBy hd), chi_rotByO M ha hb hd s]

theorem olitSpecO {m K t : Nat} (M : ModelO m K t) :
    ∀ (P Q R : Pt) (l : Int), PtOk m t P → PtOk m t Q → PtOk m t R →
      olit m (orbVarC m t) P Q R = some l → l ≠ 0 ∧ (CodeLitHolds M.τc l ↔ M.chi P Q R = true) := by
  intro P Q R l hP hQ hR h
  simp only [olit] at h
  split at h
  · exact absurd h (by simp)
  · next p0 hfind =>
    split at h
    · exact absurd h (by simp)
    · next v hv =>
      obtain ⟨rfl, a, b, d, hc, ha, hb, hd, hdist⟩ := orbVarC_some hv
      have hsort := List.find?_some hfind
      simp only [beq_iff_eq] at hsort
      have hrt : rotate m p0.2 [P, Q, R] =
          [rotBy m (negMod m p0.2) P, rotBy m (negMod m p0.2) Q, rotBy m (negMod m p0.2) R] := rfl
      have hchi := (chi_rotByO M hP hQ hR (negMod m p0.2)).symm
      have hP' := ptOk_rotBy (s := negMod m p0.2) hP
      have hQ' := ptOk_rotBy (s := negMod m p0.2) hQ
      have hR' := ptOk_rotBy (s := negMod m p0.2) hR
      generalize rotBy m (negMod m p0.2) P = P' at hrt hchi hP'
      generalize rotBy m (negMod m p0.2) Q = Q' at hrt hchi hQ'
      generalize rotBy m (negMod m p0.2) R = R' at hrt hchi hR'
      rw [hrt] at hsort h
      rw [hchi]
      have hl := Option.some.inj h
      subst hl
      rw [hc] at hsort ⊢
      simp only [List.zip_cons_cons, List.zip_nil_right, insSort, List.foldr, insertBy] at hsort ⊢
      refine ⟨by split <;> simp only [orbCode, oBase] <;> omega, ?_⟩
      have key : ∀ s : List Nat, s.Perm [0, 1, 2] →
          [P', Q', R'].getD (s.getD 0 0) (0, 0) = a → [P', Q', R'].getD (s.getD 1 0) (0, 0) = b →
          [P', Q', R'].getD (s.getD 2 0) (0, 0) = d →
          (CodeLitHolds M.τc (if permSign s > 0 then (orbCode m t [a, b, d] : Int)
            else -(orbCode m t [a, b, d] : Int)) ↔ M.chi P' Q' R' = true) := by
        intro s hs e0 e1 e2
        have hd' : Distinct3 P' Q' R' := by
          rw [← e0, ← e1, ← e2] at hdist
          obtain ⟨d1, d2, d3⟩ := hdist
          rcases perm012_cases hs with rfl | rfl | rfl | rfl | rfl | rfl <;>
            simp only [List.getD, List.getElem?_cons_zero, List.getElem?_cons_succ, Option.getD_some] at d1 d2 d3 <;>
            exact ⟨by first | exact d1 | exact d2 | exact d3 | exact Ne.symm d1 | exact Ne.symm d2 | exact Ne.symm d3,
              by first | exact d1 | exact d2 | exact d3 | exact Ne.symm d1 | exact Ne.symm d2 | exact Ne.symm d3,
              by first | exact d1 | exact d2 | exact d3 | exact Ne.symm d1 | exact Ne.symm d2 | exact Ne.symm d3⟩
        have hp := chi_perm3O M hP' hQ' hR' hd' hs
        rw [e0, e1, e2] at hp
        have ho := holds_orbO M ha hb hd
        split
        · next hpos => rw [ho, hp, if_pos hpos]
        · next hneg =>
          rw [codeLitHolds_neg (by simp only [orbCode, oBase]; omega), ho, hp, if_neg hneg]
          cases M.chi P' Q' R' <;> simp
      cases hA : ptLt R' Q' <;> cases hB : ptLt R' P' <;> cases hC : ptLt Q' P' <;>
        simp only [hA, hB, hC, insertBy, if_true, if_false, Bool.false_eq_true, List.cons.injEq, and_true,
          List.map_cons, List.map_nil] at hsort ⊢ <;>
        obtain ⟨e0, e1, e2⟩ := hsort <;>
        exact key _ (by decide) (by simp [e0]) (by simp [e1]) (by simp [e2])

/-! ## Facts about the lift -/

theorem hbit_le_one (hb : Nat → Bool) (i : Nat) : hbit hb i ≤ 1 := by
  unfold hbit; split <;> omega

theorem hbit_zero_iff (hb : Nat → Bool) (i : Nat) : hbit hb i = 0 ↔ hb i = true := by
  unfold hbit; split <;> simp_all

theorem liftO_fst (hb : Nat → Bool) (a : Pt) : (liftO hb a).1 = a.1 := rfl

theorem liftO_snd_lt {hb : Nat → Bool} {m : Nat} {a : Pt} (h : a.2 < m) : (liftO hb a).2 < 2 * m := by
  have := hbit_le_one hb a.1
  simp only [liftO]
  omega

theorem liftO_inj {hb : Nat → Bool} {a b : Pt} (h : liftO hb a = liftO hb b) : a = b := by
  simp only [liftO, Prod.mk.injEq] at h
  obtain ⟨h1, h2⟩ := h
  rw [h1] at h2
  exact Prod.ext h1 (by omega)

theorem liftO_zero {hb : Nat → Bool} (h0 : hb 0 = true) : liftO hb (0, 0) = (0, 0) := by
  simp only [liftO, hbit, h0, if_true]

end EncB
