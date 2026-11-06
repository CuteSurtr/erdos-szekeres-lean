import EncB.SoundOlit
import EncB.SortLemmas

/-!
# U3: the angular clauses hold under the intended assignment (`angCl_sound`, even m)

For an orbit representative `c = [a, b, d]` (`OrbListSpec`, U1, a hypothesis here), `angOutsC` is `angOuts` with
`odd = false` (`angOutsC_even`); its entries are the patterns `(premOf …, patternLit …)` indexed by the rank
permutations of the free (nonzero) layers of `c` (`mem_angOuts_even`, and the converse `mem_angOuts_even'`).

* (i) If every premise of a pattern holds, its ranks respect ψ (`rkMono_of_prem`): layer 0 has rank 0 and is ψ-first
  (`psiLt_zero`); two free layers form a pair of `pairs free` whose premise fixes their ψ order (`premF_holds`).
* (ii) Some pattern has ranks that respect ψ (`exists_rkMono`): the positions of the free layers in their ψ-sorted
  list (`insSort M.psiLt`), a permutation of `range n`.
* (iii) A unit clause `[l]` is the literal of every pattern (`unitOf_some`), in particular of the one from (ii), so
  `PatternSpec` (U4, a hypothesis here) gives `l`. A conditional clause `-prem ++ [l]` holds through a false premise
  or, when all premises hold, through `l` by (i) and `PatternSpec`.

The bridges `mem_angOuts_even`, `mem_angOuts_even'`, `angOutsC_even`, `unitOf_some` are the M3 judge's start file;
`patternLit` and `angOuts` are never unfolded at a concrete list.
-/

namespace EncB.Ang

/-- `free` of gen_b2.py:86-87. -/
def freeOf (c : List Pt) : List Nat :=
  (insSort (fun a b => decide (a < b)) (c.map (·.1)).eraseDups).filter (· != 0)

/-- `rk` of gen_b2.py:90-91. -/
def rkOf (free ranks : List Nat) (L : Nat) : Nat :=
  if L == 0 then 0 else ((List.lookup L (free.zip ranks)).map (· + 1)).getD 0

/-- The premise literals of gen_b2.py:96-100 (even m: no H literals). -/
def premOf (yv : Nat → Nat → Int) (free : List Nat) (rk : Nat → Nat) : List Int :=
  (pairs free).map (fun ab =>
    let (a_, b_) := ab
    let lit := if a_ < b_ then yv a_ b_ else yv b_ a_
    let truth := if a_ < b_ then decide (rk a_ < rk b_) else decide (rk b_ < rk a_)
    if truth then lit else -lit)

/-- Every entry of `outs` (even m) is a pattern: its premises and its `patternLit` literal. -/
theorem mem_angOuts_even {m : Nat} {yv : Nat → Nat → Int} {hv : Nat → Int} {orbVar : List Pt → Option Nat}
    {c : List Pt} {v : Nat} {o : List Int × Option Int} (ho : o ∈ (angOuts m false yv hv orbVar c v).1) :
    ∃ ranks ∈ perms (List.range (freeOf c).length), ∃ h : Nat → Nat,
      o = (premOf yv (freeOf c) (rkOf (freeOf c) ranks),
        (patternLit m false orbVar c v (rkOf (freeOf c) ranks) h).1) := by
  unfold angOuts at ho
  simp only [List.mem_map, List.mem_flatMap] at ho
  obtain ⟨x, ⟨ranks, hr, hx⟩, rfl⟩ := ho
  simp only [Bool.false_eq_true, if_false, bitTuples, List.mem_singleton] at hx
  obtain ⟨hb, rfl, rfl⟩ := hx
  exact ⟨ranks, hr, fun L => if L == 0 then 0 else (List.lookup L ((freeOf c).zip [])).getD 0,
    by simp only [List.append_nil]; rfl⟩

/-- The converse: every pattern is an entry (for the existence step). -/
theorem mem_angOuts_even' {m : Nat} {yv : Nat → Nat → Int} {hv : Nat → Int} {orbVar : List Pt → Option Nat}
    {c : List Pt} {v : Nat} {ranks : List Nat} (hr : ranks ∈ perms (List.range (freeOf c).length)) :
    ∃ h : Nat → Nat, (premOf yv (freeOf c) (rkOf (freeOf c) ranks),
        (patternLit m false orbVar c v (rkOf (freeOf c) ranks) h).1) ∈ (angOuts m false yv hv orbVar c v).1 := by
  let h0 : Nat → Nat := fun L => if L == 0 then 0 else (List.lookup L ((freeOf c).zip [])).getD 0
  refine ⟨h0, ?_⟩
  unfold angOuts
  simp only [List.mem_map, List.mem_flatMap]
  refine ⟨((premOf yv (freeOf c) (rkOf (freeOf c) ranks),
    (patternLit m false orbVar c v (rkOf (freeOf c) ranks) h0).1),
    (patternLit m false orbVar c v (rkOf (freeOf c) ranks) h0).2), ⟨ranks, hr, ?_⟩, rfl⟩
  simp only [Bool.false_eq_true, if_false, bitTuples, List.mem_singleton]
  refine ⟨[], rfl, ?_⟩
  simp only [List.append_nil]
  rfl

/-- `angOutsC` is `angOuts` with `odd = false` for even `m`. -/
theorem angOutsC_even {m t : Nat} (heven : m % 2 = 0) (c : List Pt) :
    angOutsC m t c = angOuts m false (yLit t) (hLit t) (orbVarC m t) c (orbCode m t c) := by
  have hodd : (m % 2 == 1) = false := by rw [heven]; rfl
  rw [angOutsC, hodd]

/-- A unit of `angClOf` is the literal of every entry. -/
theorem unitOf_some {outs : List (List Int × Option Int)} {l : Int} (h : unitOf outs = some l) :
    ∀ o ∈ outs, o.2 = some l := by
  unfold unitOf at h
  split at h
  · next l' rest =>
    split at h
    · next hall =>
      cases h
      intro o ho
      rcases List.mem_cons.1 ho with rfl | ho
      · rfl
      · simpa using List.all_eq_true.1 hall o ho
    · cases h
  · cases h

/-! ### `eraseDups` on `Nat` (accumulator invariant of `eraseDupsBy.loop`) -/

theorem mem_loop {x : Nat} : ∀ (as bs : List Nat),
    x ∈ List.eraseDupsBy.loop (fun a b => a == b) as bs ↔ x ∈ as ∨ x ∈ bs
  | [], bs => by simp only [List.eraseDupsBy.loop, List.mem_reverse, List.not_mem_nil, false_or]
  | a :: as, bs => by
    unfold List.eraseDupsBy.loop
    split
    · next h =>
      rw [mem_loop as bs]
      have ha : a ∈ bs := by
        obtain ⟨y, hy, hay⟩ := List.any_eq_true.1 h
        rw [beq_iff_eq] at hay
        exact hay ▸ hy
      constructor
      · rintro (h | h)
        · exact Or.inl (List.mem_cons_of_mem _ h)
        · exact Or.inr h
      · rintro (h | h)
        · rcases List.mem_cons.1 h with rfl | h
          · exact Or.inr ha
          · exact Or.inl h
        · exact Or.inr h
    · rw [mem_loop as (a :: bs), List.mem_cons, List.mem_cons]
      constructor
      · rintro (h | h | h)
        · exact Or.inl (Or.inr h)
        · exact Or.inl (Or.inl h)
        · exact Or.inr h
      · rintro ((h | h) | h)
        · exact Or.inr (Or.inl h)
        · exact Or.inl h
        · exact Or.inr (Or.inr h)

theorem nodup_loop : ∀ (as bs : List Nat), bs.Nodup →
    (List.eraseDupsBy.loop (fun a b => a == b) as bs).Nodup
  | [], bs, h => by
    simp only [List.eraseDupsBy.loop]
    exact (List.reverse_perm bs).nodup_iff.2 h
  | a :: as, bs, h => by
    unfold List.eraseDupsBy.loop
    split
    · exact nodup_loop as bs h
    · next hf =>
      refine nodup_loop as (a :: bs) (List.nodup_cons.2 ⟨fun ha => ?_, h⟩)
      have : bs.any (fun b => a == b) = true := List.any_eq_true.2 ⟨a, ha, beq_self_eq_true a⟩
      rw [this] at hf
      exact Bool.noConfusion hf

theorem mem_eraseDups {x : Nat} {l : List Nat} : x ∈ l.eraseDups ↔ x ∈ l := by
  show x ∈ List.eraseDupsBy.loop (fun a b => a == b) l [] ↔ x ∈ l
  rw [mem_loop]
  simp only [List.not_mem_nil, or_false]

theorem nodup_eraseDups (l : List Nat) : l.eraseDups.Nodup :=
  nodup_loop l [] List.nodup_nil

/-! ### `free`: the nonzero layers of the triple, each once -/

theorem mem_freeOf {c : List Pt} {L : Nat} : L ∈ freeOf c ↔ (∃ x ∈ c, x.1 = L) ∧ L ≠ 0 := by
  unfold freeOf
  rw [List.mem_filter, (insSort_perm _ _).mem_iff, mem_eraseDups, List.mem_map, bne_iff_ne]

theorem nodup_freeOf (c : List Pt) : (freeOf c).Nodup := by
  unfold freeOf
  exact List.Nodup.sublist List.filter_sublist ((insSort_perm _ _).nodup_iff.2 (nodup_eraseDups _))

theorem freeOf_lt {m t : Nat} {c : List Pt} (hc : ∀ x ∈ c, PtOk m t x) {L : Nat} (hL : L ∈ freeOf c) : L < t := by
  obtain ⟨⟨x, hx, rfl⟩, _⟩ := mem_freeOf.1 hL
  exact (hc x hx).1

theorem rkOf_zero (free ranks : List Nat) : rkOf free ranks 0 = 0 := rfl

/-- `RkMono` reduces to the free layers: layer 0 has rank 0 and is ψ-first (`psiLt_zero`). -/
theorem rkMono_of {m K t : Nat} (M : Model m K t) {c : List Pt} (hc : ∀ x ∈ c, PtOk m t x) {rk : Nat → Nat}
    (h0 : rk 0 = 0) (hfree : ∀ u ∈ freeOf c, ∀ v ∈ freeOf c, rk u < rk v → M.psiLt u v = true) :
    RkMono M.psiLt rk c := by
  intro x hx y hy hrk
  by_cases hy0 : y.1 = 0
  · rw [hy0, h0] at hrk
    exact absurd hrk (Nat.not_lt_zero _)
  by_cases hx0 : x.1 = 0
  · rw [hx0]
    exact M.psiLt_zero _ (Nat.pos_of_ne_zero hy0) (hc y hy).1
  exact hfree _ (mem_freeOf.2 ⟨⟨x, hx, rfl⟩, hx0⟩) _ (mem_freeOf.2 ⟨⟨y, hy, rfl⟩, hy0⟩) hrk

/-! ### Premises -/

/-- One premise literal (the body of `premOf`'s map). -/
def premF (yv : Nat → Nat → Int) (rk : Nat → Nat) (ab : Nat × Nat) : Int :=
  let (a_, b_) := ab
  let lit := if a_ < b_ then yv a_ b_ else yv b_ a_
  let truth := if a_ < b_ then decide (rk a_ < rk b_) else decide (rk b_ < rk a_)
  if truth then lit else -lit

theorem premOf_eq (yv : Nat → Nat → Int) (free : List Nat) (rk : Nat → Nat) :
    premOf yv free rk = (pairs free).map (premF yv rk) := rfl

theorem yLit_ne_zero (t i j : Nat) : yLit t i j ≠ 0 := by
  simp only [yLit, yCode]
  omega

theorem premF_ne_zero (t : Nat) (rk : Nat → Nat) (u v : Nat) : premF (yLit t) rk (u, v) ≠ 0 := by
  simp only [premF]
  split <;> split <;> first | exact yLit_ne_zero _ _ _ | exact Int.neg_ne_zero.2 (yLit_ne_zero _ _ _)

theorem mem_premOf_ne_zero {t : Nat} {free : List Nat} {rk : Nat → Nat} {p : Int}
    (hp : p ∈ premOf (yLit t) free rk) : p ≠ 0 := by
  rw [premOf_eq, List.mem_map] at hp
  obtain ⟨⟨u, v⟩, _, rfl⟩ := hp
  exact premF_ne_zero t rk u v

/-- A true premise gives ψ in the direction of the ranks (either orientation of the pair). -/
theorem premF_holds {m K t : Nat} (M : Model m K t) {rk : Nat → Nat} {p q : Nat} (hp : p < t) (hq : q < t)
    (hne : p ≠ q) (h : CodeLitHolds M.τc (premF (yLit t) rk (p, q))) :
    (rk p < rk q → M.psiLt p q = true) ∧ (rk q < rk p → M.psiLt q p = true) := by
  simp only [premF] at h
  by_cases hpq : p < q
  · simp only [hpq, if_true] at h
    by_cases hr : rk p < rk q
    · simp only [hr, decide_true, if_true] at h
      have h1 := (holds_y M hp hq).1 h
      exact ⟨fun _ => h1, fun h' => absurd h' (by omega)⟩
    · simp only [hr, decide_false, Bool.false_eq_true, if_false] at h
      have h1 := (codeLitHolds_neg (yLit_ne_zero t p q)).1 h
      rw [holds_y M hp hq] at h1
      refine ⟨fun h' => absurd h' hr, fun _ => ?_⟩
      rcases M.psiLt_total p q hp hq hne with h2 | h2
      · exact absurd h2 h1
      · exact h2
  · simp only [hpq, if_false] at h
    by_cases hr : rk q < rk p
    · simp only [hr, decide_true, if_true] at h
      have h1 := (holds_y M hq hp).1 h
      exact ⟨fun h' => absurd h' (by omega), fun _ => h1⟩
    · simp only [hr, decide_false, Bool.false_eq_true, if_false] at h
      have h1 := (codeLitHolds_neg (yLit_ne_zero t q p)).1 h
      rw [holds_y M hq hp] at h1
      refine ⟨fun _ => ?_, fun h' => absurd h' hr⟩
      rcases M.psiLt_total q p hq hp (Ne.symm hne) with h2 | h2
      · exact absurd h2 h1
      · exact h2

/-- (i) All premises true ⇒ the ranks respect ψ. -/
theorem rkMono_of_prem {m K t : Nat} (M : Model m K t) {c : List Pt} (hc : ∀ x ∈ c, PtOk m t x)
    {ranks : List Nat} (hall : ∀ p ∈ premOf (yLit t) (freeOf c) (rkOf (freeOf c) ranks), CodeLitHolds M.τc p) :
    RkMono M.psiLt (rkOf (freeOf c) ranks) c := by
  refine rkMono_of M hc (rkOf_zero _ _) (fun u hu v hv huv => ?_)
  have hne : u ≠ v := by
    rintro rfl
    exact Nat.lt_irrefl _ huv
  have hut := freeOf_lt hc hu
  have hvt := freeOf_lt hc hv
  rw [premOf_eq] at hall
  rcases mem_pairs_of_ne hu hv hne with h | h
  · exact (premF_holds M hut hvt hne (hall _ (List.mem_map_of_mem h))).1 huv
  · exact (premF_holds M hvt hut (Ne.symm hne) (hall _ (List.mem_map_of_mem h))).2 huv

/-! ### (ii) A pattern whose ranks respect ψ exists -/

theorem lookup_zip_map {f : Nat → Nat} : ∀ {l : List Nat} {L : Nat}, L ∈ l →
    List.lookup L (l.zip (l.map f)) = some (f L)
  | [], _, h => absurd h List.not_mem_nil
  | a :: l, L, h => by
    rw [List.map_cons, List.zip_cons_cons, List.lookup_cons]
    by_cases hL : L = a
    · subst hL
      simp only [beq_self_eq_true]
    · have hb : (L == a) = false := by simpa using hL
      simp only [hb]
      exact lookup_zip_map (List.mem_of_ne_of_mem hL h)

theorem idxOf_map_self : ∀ {l : List Nat}, l.Nodup → l.map l.idxOf = List.range l.length
  | [], _ => rfl
  | a :: l, h => by
    rw [List.nodup_cons] at h
    rw [List.map_cons, List.idxOf_cons_self, List.length_cons, List.range_succ_eq_map]
    congr 1
    rw [← idxOf_map_self h.2, List.map_map]
    apply List.map_congr_left
    intro x hx
    have hb : (a == x) = false := by
      simp only [beq_eq_false_iff_ne, ne_eq]
      rintro rfl
      exact h.1 hx
    simp only [Function.comp, List.idxOf_cons, hb, cond_false, Nat.succ_eq_add_one]

theorem rel_of_idxOf_lt {R : Nat → Nat → Prop} : ∀ {s : List Nat}, s.Pairwise R → ∀ {x y : Nat},
    x ∈ s → y ∈ s → s.idxOf x < s.idxOf y → R x y
  | [], _, _, _, hx, _, _ => absurd hx List.not_mem_nil
  | z :: s, hp, x, y, hx, hy, hlt => by
    rw [List.pairwise_cons] at hp
    rw [List.idxOf_cons, List.idxOf_cons] at hlt
    by_cases hzy : z = y
    · subst hzy
      cases hzx : (z == x) <;> simp only [hzx, beq_self_eq_true, cond_true, cond_false] at hlt <;> omega
    · have hy' : y ∈ s := List.mem_of_ne_of_mem (Ne.symm hzy) hy
      by_cases hzx : z = x
      · subst hzx
        exact hp.1 y hy'
      · have hx' : x ∈ s := List.mem_of_ne_of_mem (Ne.symm hzx) hx
        have b1 : (z == x) = false := by simpa using hzx
        have b2 : (z == y) = false := by simpa using hzy
        simp only [b1, b2, cond_false] at hlt
        exact rel_of_idxOf_lt hp.2 hx' hy' (by omega)

/-- The ranks of the ψ-sorted free layers form a pattern that respects ψ. -/
theorem exists_rkMono {m K t : Nat} (M : Model m K t) {c : List Pt} (hc : ∀ x ∈ c, PtOk m t x) :
    ∃ ranks ∈ perms (List.range (freeOf c).length), RkMono M.psiLt (rkOf (freeOf c) ranks) c := by
  have hnd := nodup_freeOf c
  have hsp : (insSort M.psiLt (freeOf c)).Perm (freeOf c) := insSort_perm _ _
  have hss : (insSort M.psiLt (freeOf c)).Pairwise (fun x y => M.psiLt x y = true) :=
    insSort_pairwise _ _ hnd (fun x _ y _ z _ => M.psiLt_trans x y z)
      (fun x hx y hy hne => M.psiLt_total x y (freeOf_lt hc hx) (freeOf_lt hc hy) hne)
  generalize insSort M.psiLt (freeOf c) = s at hsp hss
  refine ⟨(freeOf c).map s.idxOf, mem_perms List.nodup_range ?_, ?_⟩
  · have := (hsp.map s.idxOf).symm
    rw [idxOf_map_self (hsp.nodup_iff.2 hnd), hsp.length_eq] at this
    exact this
  · refine rkMono_of M hc (rkOf_zero _ _) (fun u hu v hv huv => ?_)
    have hr : ∀ L ∈ freeOf c, rkOf (freeOf c) ((freeOf c).map s.idxOf) L = s.idxOf L + 1 := by
      intro L hL
      have hL0 : (L == 0) = false := by simpa using (mem_freeOf.1 hL).2
      simp only [rkOf, hL0, lookup_zip_map hL, Option.map_some, Option.getD_some, Bool.false_eq_true, if_false]
    rw [hr u hu, hr v hv] at huv
    exact rel_of_idxOf_lt hss (hsp.mem_iff.2 hu) (hsp.mem_iff.2 hv) (by omega)

end EncB.Ang

namespace EncB

open Ang in
/-- **U3.** Every angular clause (unit or conditional) of an orbit representative holds under the intended
assignment, given that orbit representatives are three distinct valid labels (`OrbListSpec`, U1) and that a
pattern whose ranks respect ψ yields no literal or a true one (`PatternSpec`, U4). -/
theorem angCl_sound {m K t : Nat} (M : Model m K t) (heven : m % 2 = 0) (hOL : OrbListSpec m t)
    (hP : PatternSpec M) :
    ∀ c ∈ orbList m t, ∀ cl ∈ angClOf (angOutsC m t c).1, ∃ x ∈ cl, CodeLitHolds M.τc x := by
  intro c hc cl hcl
  obtain ⟨a, b, d, rfl, ha, hb, hd, hdist⟩ := hOL c hc
  have hcOk : ∀ x ∈ [a, b, d], PtOk m t x := by
    intro x hx
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
    rcases hx with rfl | rfl | rfl <;> assumption
  rw [angOutsC_even heven] at hcl
  generalize hO : (angOuts m false (yLit t) (hLit t) (orbVarC m t) [a, b, d] (orbCode m t [a, b, d])).1 = O
    at hcl
  unfold angClOf at hcl
  split at hcl
  · next l hl =>
    obtain ⟨ranks, hr, hmono⟩ := exists_rkMono M hcOk
    obtain ⟨h, hmem⟩ := mem_angOuts_even' (m := m) (yv := yLit t) (hv := hLit t) (orbVar := orbVarC m t)
      (v := orbCode m t [a, b, d]) hr
    rw [hO] at hmem
    have hlit := unitOf_some hl _ hmem
    rw [List.mem_singleton] at hcl
    subst hcl
    exact ⟨l, List.mem_singleton_self _, hP a b d _ h l ha hb hd hdist hmono hlit⟩
  · rw [List.mem_filterMap] at hcl
    obtain ⟨o, ho, hcl⟩ := hcl
    rw [← hO] at ho
    obtain ⟨ranks, hr, h, rfl⟩ := mem_angOuts_even ho
    rw [Option.map_eq_some_iff] at hcl
    obtain ⟨l, hpl, rfl⟩ := hcl
    by_cases hall : ∀ p ∈ premOf (yLit t) (freeOf [a, b, d]) (rkOf (freeOf [a, b, d]) ranks), CodeLitHolds M.τc p
    · exact ⟨l, List.mem_append_right _ (List.mem_singleton_self _),
        hP a b d _ h l ha hb hd hdist (rkMono_of_prem M hcOk hall) hpl⟩
    · obtain ⟨p, hp, hnp⟩ : ∃ p ∈ premOf (yLit t) (freeOf [a, b, d]) (rkOf (freeOf [a, b, d]) ranks),
          ¬ CodeLitHolds M.τc p :=
        Classical.byContradiction fun hn => hall fun p hp => Classical.byContradiction fun hnp => hn ⟨p, hp, hnp⟩
      exact ⟨-p, List.mem_append_left _ (List.mem_map_of_mem hp), (codeLitHolds_neg (mem_premOf_ne_zero hp)).2 hnp⟩

/-- info: 'EncB.angCl_sound' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms angCl_sound

end EncB
