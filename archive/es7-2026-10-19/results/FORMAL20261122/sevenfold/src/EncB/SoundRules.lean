import EncB.SoundOlit
import EncB.SortLemmas

/-! U4 (`EncB/SoundRules.lean`) starting point (compiled by the M3 judge): `patternLit` (even m) factored through `patternCore`, and its two branches. -/

namespace EncB.Rules

/-- The objects of `c` for even `m` (gen_b2.py:104-111, the `else` branch of Gen:147-151). -/
def objsEven (m : Nat) (rk : Nat → Nat) (c : List Pt) : List Obj :=
  (c.zip (List.range c.length)).flatMap fun pi =>
    let (p, idx) := pi
    let (J, Ja) := ((p.2, (p.2 + m / 2) % m) : Nat × Nat)
    [⟨J, rk p.1, 1, idx⟩, ⟨Ja, rk p.1, 0, idx⟩]

/-- `patternLit` (Gen:142-181) after the objects are built, for even `m`. -/
def patternCore (m : Nat) (orbVar : List Pt → Option Nat) (c : List Pt) (v : Nat) (objs : List Obj) :
    Option Int × Nat :=
  let keys := objs.map fun o => (o.J, o.r)
  if (pairs keys).any (fun kk => kk.1 == kk.2) then
    (none, if false then 1 else 0)
  else
    let objs := insSort Obj.lt objs
    let kinds := objs.map (·.kind)
    let v' : Int := v
    if kinds == [1, 0, 1, 0, 1, 0] || kinds == [0, 1, 0, 1, 0, 1] then
      let seq := (objs.filter (·.kind == 1)).map (·.idx)
      (some (if permSign seq > 0 then v' else -v'), 0)
    else
      let isP (x : Nat) : Bool := kinds.getD (x % 6) 0 == 1
      match (List.range 6).find? (fun x => isP x && isP (x + 1) && isP (x + 2)) with
      | none => (none, 1)
      | some st =>
        let seq := [0, 1, 2].map fun r => (objs.getD ((st + r) % 6) default).idx
        let a := c.getD (seq.getD 0 0) (0, 0)
        let b := c.getD (seq.getD 1 0) (0, 0)
        let cc := c.getD (seq.getD 2 0) (0, 0)
        if decide (b.1 ≤ a.1) && decide (b.1 ≤ cc.1) then
          match olit m orbVar a b cc with
          | none => (none, 1)
          | some l => (some l, 0)
        else (none, 0)

theorem patternLit_even (m : Nat) (orbVar : List Pt → Option Nat) (c : List Pt) (v : Nat) (rk h : Nat → Nat) :
    patternLit m false orbVar c v rk h = patternCore m orbVar c v (objsEven m rk c) := rfl

theorem objsEven_three (m : Nat) (rk : Nat → Nat) (a b d : Pt) :
    objsEven m rk [a, b, d] =
      [⟨a.2, rk a.1, 1, 0⟩, ⟨(a.2 + m / 2) % m, rk a.1, 0, 0⟩,
       ⟨b.2, rk b.1, 1, 1⟩, ⟨(b.2 + m / 2) % m, rk b.1, 0, 1⟩,
       ⟨d.2, rk d.1, 1, 2⟩, ⟨(d.2 + m / 2) % m, rk d.1, 0, 2⟩] := rfl

/-- Decomposition of a pattern literal into rule A and rule B, with the sorted list abstracted. -/
theorem patternCore_cases {m : Nat} {orbVar : List Pt → Option Nat} {c : List Pt} {v : Nat}
    {objs : List Obj} {l : Int} (hl : (patternCore m orbVar c v objs).1 = some l) :
    (pairs (objs.map fun o => (o.J, o.r))).any (fun kk => kk.1 == kk.2) = false ∧
    (((insSort Obj.lt objs).map (·.kind) = [1, 0, 1, 0, 1, 0] ∨
        (insSort Obj.lt objs).map (·.kind) = [0, 1, 0, 1, 0, 1]) ∧
        l = (if permSign (((insSort Obj.lt objs).filter (·.kind == 1)).map (·.idx)) > 0
          then (v : Int) else -(v : Int)) ∨
     ∃ st, st < 6 ∧ ((insSort Obj.lt objs).map (·.kind)).getD (st % 6) 0 = 1 ∧
        ((insSort Obj.lt objs).map (·.kind)).getD ((st + 1) % 6) 0 = 1 ∧
        ((insSort Obj.lt objs).map (·.kind)).getD ((st + 2) % 6) 0 = 1 ∧
        (c.getD ((insSort Obj.lt objs).getD ((st + 1) % 6) default).idx (0, 0)).1 ≤
          (c.getD ((insSort Obj.lt objs).getD (st % 6) default).idx (0, 0)).1 ∧
        (c.getD ((insSort Obj.lt objs).getD ((st + 1) % 6) default).idx (0, 0)).1 ≤
          (c.getD ((insSort Obj.lt objs).getD ((st + 2) % 6) default).idx (0, 0)).1 ∧
        olit m orbVar (c.getD ((insSort Obj.lt objs).getD (st % 6) default).idx (0, 0))
          (c.getD ((insSort Obj.lt objs).getD ((st + 1) % 6) default).idx (0, 0))
          (c.getD ((insSort Obj.lt objs).getD ((st + 2) % 6) default).idx (0, 0)) = some l) := by
  unfold patternCore at hl
  generalize insSort Obj.lt objs = S at hl ⊢
  by_cases hk : ((pairs (objs.map fun o => (o.J, o.r))).any fun kk => kk.1 == kk.2) = true
  · rw [if_pos hk] at hl; simp at hl
  · rw [if_neg hk] at hl
    refine ⟨by simpa only [Bool.not_eq_true] using hk, ?_⟩
    by_cases halt : (S.map (·.kind) == [1, 0, 1, 0, 1, 0] || S.map (·.kind) == [0, 1, 0, 1, 0, 1]) = true
    · rw [if_pos halt] at hl
      left
      simp only [Bool.or_eq_true, beq_iff_eq] at halt
      exact ⟨halt, (Option.some.inj hl).symm⟩
    · rw [if_neg halt] at hl
      right
      dsimp only at hl
      split at hl
      · simp at hl
      · next st hst =>
        have hst6 : st < 6 := List.mem_range.1 (List.mem_of_find?_eq_some hst)
        have hp := List.find?_some hst
        simp only [Bool.and_eq_true, beq_iff_eq] at hp
        refine ⟨st, hst6, hp.1.1, hp.1.2, hp.2, ?_⟩
        simp only [List.map_cons, List.map_nil, List.getD_cons_zero, List.getD_cons_succ,
          Nat.add_zero] at hl
        by_cases hle : (decide ((c.getD (S.getD ((st + 1) % 6) default).idx (0, 0)).1 ≤
            (c.getD (S.getD (st % 6) default).idx (0, 0)).1) &&
            decide ((c.getD (S.getD ((st + 1) % 6) default).idx (0, 0)).1 ≤
            (c.getD (S.getD ((st + 2) % 6) default).idx (0, 0)).1)) = true
        · rw [if_pos hle] at hl
          simp only [Bool.and_eq_true, decide_eq_true_eq] at hle
          split at hl
          · simp at hl
          · next l' hol =>
            have := Option.some.inj hl
            subst this
            exact ⟨hle.1, hle.2, hol⟩
        · rw [if_neg hle] at hl; simp at hl

/-- U4-internal: sorting the six code objects (not frozen; U4 proves it as `sortSix`). -/
def SortSixStmt : Prop :=
  ∀ (m : Nat) (psiLt : Nat → Nat → Bool) (a b d : Pt) (rk : Nat → Nat),
    (∀ i, psiLt i i = false) → (∀ i j k, psiLt i j = true → psiLt j k = true → psiLt i k = true) →
    Distinct3 a b d → RkMono psiLt rk [a, b, d] →
    (pairs ((objsEven m rk [a, b, d]).map fun o => (o.J, o.r))).any (fun kk => kk.1 == kk.2) = false →
    SortedSix m psiLt a b d (insSort Obj.lt (objsEven m rk [a, b, d]))

theorem getD3_lt {l : List Nat} (h : ∀ x ∈ l, x < 3) (j : Nat) : l.getD j 0 < 3 := by
  rw [List.getD_eq_getElem?_getD]
  cases hj : l[j]? with
  | none => simp
  | some x => simpa using h x (List.mem_of_getElem? hj)

theorem ptOk_getD3 {m t : Nat} {a b d : Pt} (ha : PtOk m t a) (hb : PtOk m t b) (hd : PtOk m t d) :
    ∀ i, i < 3 → PtOk m t ([a, b, d].getD i (0, 0))
  | 0, _ => ha
  | 1, _ => hb
  | 2, _ => hd

theorem distinct_of_ccw {m : Nat} {psiLt : Nat → Nat → Bool} (hirr : ∀ i, psiLt i i = false)
    (htr : ∀ i j k, psiLt i j = true → psiLt j k = true → psiLt i k = true) {x y z : Pt}
    (h : ccwIn (objLt m psiLt) (x, true) (y, true) (z, true)) : Distinct3 x y z := by
  obtain ⟨h1, h2, h3⟩ := ccwIn_distinct (objLt_irrefl hirr) (objLt_asymm hirr htr) h
  exact ⟨fun e => h1 (by rw [e]), fun e => h2 (by rw [e]), fun e => h3 (by rw [e])⟩

theorem idx_getD_lt {S : List Obj} (h : ∀ o ∈ S, o.idx < 3) (k : Nat) : (S.getD k default).idx < 3 := by
  rw [List.getD_eq_getElem?_getD]
  cases hk : S[k]? with
  | none => show (default : Obj).idx < 3; decide
  | some o => exact h o (List.mem_of_getElem? hk)

theorem patternSpec_of_sort (hS : SortSixStmt) (hW : WordSpec) {m K t : Nat} (M : Model m K t) :
    PatternSpec M := by
  intro a b d rk h l ha hb hd hdist hrk hl
  rw [patternLit_even] at hl
  obtain ⟨hkeys, hcase⟩ := patternCore_cases hl
  have hSS := hS m M.psiLt a b d rk M.psiLt_irrefl M.psiLt_trans hdist hrk hkeys
  obtain ⟨hA, hB⟩ := hW m M.psiLt a b d _ M.psiLt_irrefl M.psiLt_trans hdist hSS
  have hpk := ptOk_getD3 ha hb hd
  rcases hcase with ⟨hkinds, rfl⟩ | ⟨st, hst, h0, h1, h2, hle1, hle2, hol⟩
  · have hAlt := hA hkinds
    have hlt : ∀ x ∈ ((insSort Obj.lt (objsEven m rk [a, b, d])).filter (·.kind == 1)).map (·.idx), x < 3 :=
      fun x hx => by
        have := hSS.points.mem_iff.1 hx
        simp only [List.mem_cons, List.not_mem_nil, or_false] at this
        omega
    have hchi := M.ruleA _ _ _ (hpk _ (getD3_lt hlt 0)) (hpk _ (getD3_lt hlt 1)) (hpk _ (getD3_lt hlt 2))
      (distinct_of_ccw M.psiLt_irrefl M.psiLt_trans hAlt.2.1) hAlt
    rw [chi_perm3 M ha hb hd hdist hSS.points] at hchi
    have ho := holds_orb M ha hb hd
    split
    · next hpos => rw [ho]; rwa [if_pos hpos] at hchi
    · next hneg =>
      rw [codeLitHolds_neg (by simp only [orbCode, oBase]; omega), ho]
      rw [if_neg hneg] at hchi
      simpa using hchi
  · have hBlk := hB st hst h0 h1 h2
    have hx := hpk _ (idx_getD_lt hSS.idx_lt (st % 6))
    have hy := hpk _ (idx_getD_lt hSS.idx_lt ((st + 1) % 6))
    have hz := hpk _ (idx_getD_lt hSS.idx_lt ((st + 2) % 6))
    have hchi := M.ruleB _ _ _ hx hy hz (distinct_of_ccw M.psiLt_irrefl M.psiLt_trans hBlk.2.1) hBlk hle1 hle2
    exact ((olitSpec M _ _ _ l hx hy hz hol).2).2 hchi


/-! ### U4: sorting the six code objects (`sortSix`) -/

/-- No equal pair among `pairs l` means `l` is duplicate-free. -/
private theorem pairwise_ne_of_pairs {β : Type} [BEq β] [LawfulBEq β] :
    ∀ l : List β, (pairs l).any (fun kk => kk.1 == kk.2) = false → l.Pairwise (· ≠ ·)
  | [], _ => List.Pairwise.nil
  | x :: xs, h => by
    simp only [pairs, List.any_append, Bool.or_eq_false_iff] at h
    refine List.pairwise_cons.2 ⟨fun y hy e => ?_, pairwise_ne_of_pairs xs h.2⟩
    subst e
    have h1 := List.any_eq_false.1 h.1 (x, x) (List.mem_map.2 ⟨x, hy, rfl⟩)
    simp at h1

/-- A function with pairwise distinct values on `l` is injective on `l`. -/
private theorem eq_of_pairwise_ne {α β : Type} (f : α → β) {l : List α}
    (h : l.Pairwise (fun x y => f x ≠ f y)) {x y : α} (hx : x ∈ l) (hy : y ∈ l) (hxy : f x = f y) : x = y := by
  induction h with
  | nil => exact absurd hx List.not_mem_nil
  | @cons z l hz _ ih =>
    rcases List.mem_cons.1 hx with rfl | hx' <;> rcases List.mem_cons.1 hy with rfl | hy'
    · rfl
    · exact absurd hxy (hz y hy')
    · exact absurd hxy.symm (hz x hx')
    · exact ih hx' hy'

private theorem olt_trans (x y z : Obj) (h1 : Obj.lt x y = true) (h2 : Obj.lt y z = true) :
    Obj.lt x z = true := by
  rw [Obj.lt_iff] at h1 h2 ⊢
  omega

private theorem olt_total (x y : Obj) (h : (x.J, x.r) ≠ (y.J, y.r)) :
    Obj.lt x y = true ∨ Obj.lt y x = true := by
  have h' : ¬ (x.J = y.J ∧ x.r = y.r) := fun ⟨h1, h2⟩ => h (by rw [h1, h2])
  rw [Obj.lt_iff, Obj.lt_iff]
  omega

/-- On each of the six objects: the cell of its image is `J`, its rank is `r`, its point is one of `a, b, d`. -/
private theorem objsEven_mem {m : Nat} {rk : Nat → Nat} {a b d : Pt} {o : Obj}
    (ho : o ∈ objsEven m rk [a, b, d]) :
    cell m (objImg [a, b, d] o) = o.J ∧ rk (objImg [a, b, d] o).1.1 = o.r ∧
      (objImg [a, b, d] o).1 ∈ [a, b, d] ∧ o.idx < 3 := by
  rw [objsEven_three] at ho
  simp only [List.mem_cons, List.not_mem_nil, or_false] at ho
  rcases ho with rfl | rfl | rfl | rfl | rfl | rfl <;>
    exact ⟨rfl, rfl, by simp [objImg], by simp⟩

theorem sortSix : SortSixStmt := by
  intro m psiLt a b d rk _ _ _ hrk hkeys
  have hpw := pairwise_ne_of_pairs _ hkeys
  rw [List.pairwise_map] at hpw
  have hinj : ∀ {x y : Obj}, x ∈ objsEven m rk [a, b, d] → y ∈ objsEven m rk [a, b, d] →
      (x.J, x.r) = (y.J, y.r) → x = y :=
    fun hx hy e => eq_of_pairwise_ne (fun o : Obj => (o.J, o.r)) hpw hx hy e
  have hnd : (objsEven m rk [a, b, d]).Nodup := hpw.imp fun h e => h (by rw [e])
  have hsort := insSort_pairwise Obj.lt _ hnd (fun x _ y _ z _ => olt_trans x y z)
    (fun x hx y hy hne => olt_total x y fun e => hne (hinj hx hy e))
  have hperm := insSort_perm Obj.lt (objsEven m rk [a, b, d])
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · rw [hperm.length_eq, objsEven_three]
    rfl
  · refine hsort.imp_of_mem ?_
    intro o o' ho ho' hlt
    have ho1 := objsEven_mem (hperm.mem_iff.1 ho)
    have ho2 := objsEven_mem (hperm.mem_iff.1 ho')
    have hne : ¬ (o.J = o'.J ∧ o.r = o'.r) := fun ⟨h1, h2⟩ => by
      have e := hinj (hperm.mem_iff.1 ho) (hperm.mem_iff.1 ho') (by rw [h1, h2])
      subst e
      rw [Obj.lt_irrefl] at hlt
      exact Bool.false_ne_true hlt
    rw [Obj.lt_iff] at hlt
    unfold objLt
    rw [ho1.1, ho2.1]
    by_cases hJ : o.J < o'.J
    · exact Or.inl hJ
    · refine Or.inr ⟨by omega, hrk _ ho1.2.2.1 _ ho2.2.2.1 ?_⟩
      rw [ho1.2.1, ho2.2.1]
      omega
  · have himg : (objsEven m rk [a, b, d]).map (objImg [a, b, d]) =
        [(a, true), (a, false), (b, true), (b, false), (d, true), (d, false)] := by
      rw [objsEven_three]
      rfl
    intro x hx
    rw [(hperm.map _).mem_iff, himg]
    simp only [objs6, List.mem_cons, List.not_mem_nil, or_false] at hx ⊢
    rcases hx with h | h | h | h | h | h <;> simp [h]
  · intro o ho
    exact (objsEven_mem (hperm.mem_iff.1 ho)).2.2.2
  · have h3 : ((objsEven m rk [a, b, d]).filter (·.kind == 1)).map (·.idx) = [0, 1, 2] := by
      rw [objsEven_three]
      rfl
    exact ((hperm.filter _).map _).trans (List.Perm.of_eq h3)

end EncB.Rules

namespace EncB

/-- U4 (frozen): every pattern literal of an orbit holds in a model, given the cyclic-word statement `WordSpec`
(proved by U5 as `wordSpec`). -/
theorem patternSpec_of (hW : WordSpec) {m K t : Nat} (M : Model m K t) : PatternSpec M :=
  Rules.patternSpec_of_sort Rules.sortSix hW M

end EncB

/-- info: 'EncB.patternSpec_of' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms EncB.patternSpec_of
