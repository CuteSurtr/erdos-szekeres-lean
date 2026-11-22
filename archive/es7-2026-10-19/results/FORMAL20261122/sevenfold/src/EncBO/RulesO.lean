import EncBO.ModelO
import EncB.SoundRules
import EncB.SoundWord

/-!
# The pattern literals of odd `m` are sound (`patternSpecO`)

For odd `m`, gen_b2.py's six objects of a triple `[a, b, d]` with ranks `rk` and bits `h` have the cell indices
`J = (2k + h) mod 2m` (point) and `(J + m) mod 2m` (antipode) (`objsOdd`, the `if odd` branch of `patternLit`).
When the bits are the model's (`h x.1 = hbit hb x.1`) these six objects are **exactly** ENCBLEAN's even-`m`
objects at `2m` of the lifted labels `liftO hb a, liftO hb b, liftO hb d` (`objsOdd_eq`). ENCBLEAN's sorting lemma
`Rules.sortSix` and cyclic-word lemma `wordSpec` (both quantified over `m`) then apply at `2m`, and the rules of
`ModelO` (stated at `2m` on lifted labels) give the literal. The rule-B literal is `olit m` of the original labels
(`patternCore` keeps `c = [a, b, d]`).
-/

namespace EncB

namespace RulesO

open Rules

/-- The objects of `c` for odd `m` (gen_b2.py:104-111, the `if odd` branch of `patternLit`). -/
def objsOdd (m : Nat) (rk h : Nat → Nat) (c : List Pt) : List Obj :=
  (c.zip (List.range c.length)).flatMap fun pi =>
    let (p, idx) := pi
    let (J, Ja) :=
      let J := (2 * p.2 + h p.1) % (2 * m)
      (J, (J + m) % (2 * m))
    [⟨J, rk p.1, 1, idx⟩, ⟨Ja, rk p.1, 0, idx⟩]

/-- The literal of an odd pattern is `patternCore` of its objects (the two differ only in the count of Python
assertion failures, the second component). -/
theorem patternLit_odd_fst (m : Nat) (orbVar : List Pt → Option Nat) (c : List Pt) (v : Nat) (rk h : Nat → Nat) :
    (patternLit m true orbVar c v rk h).1 = (patternCore m orbVar c v (objsOdd m rk h c)).1 := by
  simp only [patternLit, patternCore, objsOdd, ite_true, Bool.false_eq_true, if_false]
  split <;> rfl

theorem objsOdd_three (m : Nat) (rk h : Nat → Nat) (a b d : Pt) :
    objsOdd m rk h [a, b, d] =
      [⟨(2 * a.2 + h a.1) % (2 * m), rk a.1, 1, 0⟩, ⟨((2 * a.2 + h a.1) % (2 * m) + m) % (2 * m), rk a.1, 0, 0⟩,
       ⟨(2 * b.2 + h b.1) % (2 * m), rk b.1, 1, 1⟩, ⟨((2 * b.2 + h b.1) % (2 * m) + m) % (2 * m), rk b.1, 0, 1⟩,
       ⟨(2 * d.2 + h d.1) % (2 * m), rk d.1, 1, 2⟩, ⟨((2 * d.2 + h d.1) % (2 * m) + m) % (2 * m), rk d.1, 0, 2⟩] :=
  rfl

/-- **The odd objects are the even objects at `2m` of the lifted labels**, when the bits are the model's. -/
theorem objsOdd_eq {m : Nat} {hb : Nat → Bool} {rk h : Nat → Nat} {a b d : Pt}
    (ha : a.2 < m) (hb' : b.2 < m) (hd : d.2 < m) (hh : ∀ x ∈ [a, b, d], h x.1 = hbit hb x.1) :
    objsOdd m rk h [a, b, d] = objsEven (2 * m) rk [liftO hb a, liftO hb b, liftO hb d] := by
  have e : ∀ x : Pt, x.2 < m → h x.1 = hbit hb x.1 → (2 * x.2 + h x.1) % (2 * m) = (liftO hb x).2 := by
    intro x hx hhx
    have := hbit_le_one hb x.1
    rw [hhx]
    exact Nat.mod_eq_of_lt (by omega)
  have hm2 : 2 * m / 2 = m := by omega
  rw [objsOdd_three, objsEven_three, e a ha (hh a (by simp)), e b hb' (hh b (by simp)),
    e d hd (hh d (by simp)), hm2]
  rfl

/-- Reading a lifted triple at an index is lifting the reading (out of range both give `(0, 0)`, since
`hb 0 = true`). -/
theorem getD_liftO {hb : Nat → Bool} (h0 : hb 0 = true) (a b d : Pt) :
    ∀ i, [liftO hb a, liftO hb b, liftO hb d].getD i (0, 0) = liftO hb ([a, b, d].getD i (0, 0))
  | 0 => rfl
  | 1 => rfl
  | 2 => rfl
  | n + 3 => by
    simp only [List.getD_cons_succ, List.getD_nil]
    exact (liftO_zero h0).symm

theorem distinct3_of_lift {hb : Nat → Bool} {x y z : Pt} (h : Distinct3 (liftO hb x) (liftO hb y) (liftO hb z)) :
    Distinct3 x y z :=
  ⟨fun e => h.1 (by rw [e]), fun e => h.2.1 (by rw [e]), fun e => h.2.2 (by rw [e])⟩

theorem distinct3_lift {hb : Nat → Bool} {x y z : Pt} (h : Distinct3 x y z) :
    Distinct3 (liftO hb x) (liftO hb y) (liftO hb z) :=
  ⟨fun e => h.1 (liftO_inj e), fun e => h.2.1 (liftO_inj e), fun e => h.2.2 (liftO_inj e)⟩

theorem rkMono_lift {psiLt : Nat → Nat → Bool} {hb : Nat → Bool} {rk : Nat → Nat} {a b d : Pt}
    (h : RkMono psiLt rk [a, b, d]) : RkMono psiLt rk [liftO hb a, liftO hb b, liftO hb d] := by
  have back : ∀ x ∈ [liftO hb a, liftO hb b, liftO hb d], ∃ x0 ∈ [a, b, d], x.1 = x0.1 := by
    intro x hx
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
    rcases hx with rfl | rfl | rfl
    · exact ⟨a, by simp, rfl⟩
    · exact ⟨b, by simp, rfl⟩
    · exact ⟨d, by simp, rfl⟩
  intro x hx y hy hxy
  obtain ⟨x0, hx0, ex⟩ := back x hx
  obtain ⟨y0, hy0, ey⟩ := back y hy
  rw [ex, ey] at hxy ⊢
  exact h x0 hx0 y0 hy0 hxy

end RulesO

/-- **Odd `PatternSpec`.** A pattern whose ranks respect ψ and whose bits are the model's yields no literal or a
true one. -/
def PatternSpecO {m K t : Nat} (M : ModelO m K t) : Prop :=
  ∀ (a b d : Pt) (rk h : Nat → Nat) (l : Int), PtOk m t a → PtOk m t b → PtOk m t d → Distinct3 a b d →
    RkMono M.psiLt rk [a, b, d] → (∀ x ∈ [a, b, d], h x.1 = hbit M.hb x.1) →
    (patternLit m true (orbVarC m t) [a, b, d] (orbCode m t [a, b, d]) rk h).1 = some l →
    CodeLitHolds M.τc l

open RulesO Rules in
theorem patternSpecO {m K t : Nat} (M : ModelO m K t) : PatternSpecO M := by
  intro a b d rk h l ha hb hd hdist hrk hh hl
  rw [patternLit_odd_fst, objsOdd_eq ha.2 hb.2 hd.2 hh] at hl
  obtain ⟨hkeys, hcase⟩ := patternCore_cases hl
  have hSS := sortSix (2 * m) M.psiLt (liftO M.hb a) (liftO M.hb b) (liftO M.hb d) rk M.psiLt_irrefl
    M.psiLt_trans (distinct3_lift hdist) (rkMono_lift hrk) hkeys
  obtain ⟨hA, hB⟩ := wordSpec (2 * m) M.psiLt (liftO M.hb a) (liftO M.hb b) (liftO M.hb d) _ M.psiLt_irrefl
    M.psiLt_trans (distinct3_lift hdist) hSS
  have hpk := ptOk_getD3 ha hb hd
  rcases hcase with ⟨hkinds, rfl⟩ | ⟨st, hst, h0, h1, h2, hle1, hle2, hol⟩
  · have hAlt := hA hkinds
    rw [getD_liftO M.hb_zero, getD_liftO M.hb_zero, getD_liftO M.hb_zero] at hAlt
    have hlt : ∀ x ∈ ((insSort Obj.lt (objsEven (2 * m) rk [liftO M.hb a, liftO M.hb b, liftO M.hb d])).filter
        (·.kind == 1)).map (·.idx), x < 3 :=
      fun x hx => by
        have := hSS.points.mem_iff.1 hx
        simp only [List.mem_cons, List.not_mem_nil, or_false] at this
        omega
    have hchi := M.ruleA _ _ _ (hpk _ (getD3_lt hlt 0)) (hpk _ (getD3_lt hlt 1)) (hpk _ (getD3_lt hlt 2))
      (distinct3_of_lift (distinct_of_ccw M.psiLt_irrefl M.psiLt_trans hAlt.2.1)) hAlt
    rw [chi_perm3O M ha hb hd hdist hSS.points] at hchi
    have ho := holds_orbO M ha hb hd
    split
    · next hpos => rw [ho]; rwa [if_pos hpos] at hchi
    · next hneg =>
      rw [codeLitHolds_neg (by simp only [orbCode, oBase]; omega), ho]
      rw [if_neg hneg] at hchi
      simpa using hchi
  · have hBlk := hB st hst h0 h1 h2
    rw [getD_liftO M.hb_zero, getD_liftO M.hb_zero, getD_liftO M.hb_zero] at hBlk
    have hx := hpk _ (idx_getD_lt hSS.idx_lt (st % 6))
    have hy := hpk _ (idx_getD_lt hSS.idx_lt ((st + 1) % 6))
    have hz := hpk _ (idx_getD_lt hSS.idx_lt ((st + 2) % 6))
    have hchi := M.ruleB _ _ _ hx hy hz
      (distinct3_of_lift (distinct_of_ccw M.psiLt_irrefl M.psiLt_trans hBlk.2.1)) hBlk hle1 hle2
    exact ((olitSpecO M _ _ _ l hx hy hz hol).2).2 hchi

/-- info: 'EncB.patternSpecO' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms patternSpecO

end EncB
