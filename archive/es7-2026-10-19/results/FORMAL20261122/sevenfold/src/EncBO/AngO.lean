import EncBO.RulesO
import EncB.SoundAng

/-!
# The angular clauses of odd `m` hold under the intended assignment (`angCl_soundO`)

For odd `m`, `angOutsC` is `angOuts` with `odd = true`; its entries are indexed by a rank permutation of the free
(nonzero) layers of the orbit representative **and** a bit tuple `hbits ∈ bitTuples n` (gen_b2.py:92-94), and the
premises are ENCBLEAN's Y premises (`Ang.premOf`) followed by one H literal per free layer (`hPremOf`,
gen_b2.py:101-102). As in ENCBLEAN's `angCl_sound`:

* (i) all premises true ⇒ the ranks respect ψ (`rkMono_of_premO`) and the bits are the model's
  (`hbits_of_prem`: the H literal of `L` holds iff `h L = hbit hb L`);
* (ii) some entry has ranks that respect ψ and the model's bits (`exists_rkMonoO`, `hbits = free.map (hbit hb)`);
* (iii) a unit clause is the literal of every entry, in particular of the one from (ii); a conditional clause holds
  through a false premise or, when all premises hold, through its literal by `patternSpecO`.

`rkMono_ofO`, `premF_holdsO`, `rkMono_of_premO`, `exists_rkMonoO` are copies of ENCBLEAN's `Ang` lemmas with
`Model` replaced by `ModelO` (same proof texts).
-/

namespace EncB

namespace AngO

open Ang

/-- `h` of gen_b2.py:93-94 (`h = {L: b for L, b in zip(free, hb)}; h[0] = 0`). -/
def hOf (free hbits : List Nat) (L : Nat) : Nat :=
  if L == 0 then 0 else (List.lookup L (free.zip hbits)).getD 0

/-- The H premise literals of gen_b2.py:101-102. -/
def hPremOf (hv : Nat → Int) (free : List Nat) (h : Nat → Nat) : List Int :=
  free.map (fun L => if h L == 0 then hv L else -(hv L))

/-- Every entry of `outs` (odd m) is a pattern: its premises and its `patternLit` literal. -/
theorem mem_angOuts_odd {m : Nat} {yv : Nat → Nat → Int} {hv : Nat → Int} {orbVar : List Pt → Option Nat}
    {c : List Pt} {v : Nat} {o : List Int × Option Int} (ho : o ∈ (angOuts m true yv hv orbVar c v).1) :
    ∃ ranks ∈ perms (List.range (freeOf c).length), ∃ hbits ∈ bitTuples (freeOf c).length,
      o = (premOf yv (freeOf c) (rkOf (freeOf c) ranks) ++ hPremOf hv (freeOf c) (hOf (freeOf c) hbits),
        (patternLit m true orbVar c v (rkOf (freeOf c) ranks) (hOf (freeOf c) hbits)).1) := by
  unfold angOuts at ho
  simp only [List.mem_map, List.mem_flatMap] at ho
  obtain ⟨x, ⟨ranks, hr, hx⟩, rfl⟩ := ho
  simp only [↓reduceIte] at hx
  obtain ⟨hbits, hb, rfl⟩ := hx
  exact ⟨ranks, hr, hbits, hb, rfl⟩

/-- The converse: every pattern is an entry (for the existence step). -/
theorem mem_angOuts_odd' {m : Nat} {yv : Nat → Nat → Int} {hv : Nat → Int} {orbVar : List Pt → Option Nat}
    {c : List Pt} {v : Nat} {ranks hbits : List Nat} (hr : ranks ∈ perms (List.range (freeOf c).length))
    (hb : hbits ∈ bitTuples (freeOf c).length) :
    (premOf yv (freeOf c) (rkOf (freeOf c) ranks) ++ hPremOf hv (freeOf c) (hOf (freeOf c) hbits),
        (patternLit m true orbVar c v (rkOf (freeOf c) ranks) (hOf (freeOf c) hbits)).1) ∈
      (angOuts m true yv hv orbVar c v).1 := by
  unfold angOuts
  simp only [List.mem_map, List.mem_flatMap]
  refine ⟨((premOf yv (freeOf c) (rkOf (freeOf c) ranks) ++ hPremOf hv (freeOf c) (hOf (freeOf c) hbits),
    (patternLit m true orbVar c v (rkOf (freeOf c) ranks) (hOf (freeOf c) hbits)).1),
    (patternLit m true orbVar c v (rkOf (freeOf c) ranks) (hOf (freeOf c) hbits)).2), ⟨ranks, hr, ?_⟩, rfl⟩
  simp only [↓reduceIte]
  exact ⟨hbits, hb, rfl⟩

/-- `angOutsC` is `angOuts` with `odd = true` for odd `m`. -/
theorem angOutsC_odd {m t : Nat} (hodd : m % 2 = 1) (c : List Pt) :
    angOutsC m t c = angOuts m true (yLit t) (hLit t) (orbVarC m t) c (orbCode m t c) := by
  have h : (m % 2 == 1) = true := by rw [hodd]; rfl
  rw [angOutsC, h]

/-! ### Bit tuples -/

theorem mem_bitTuples : ∀ (n : Nat) (bs : List Nat), bs ∈ bitTuples n ↔ bs.length = n ∧ ∀ b ∈ bs, b = 0 ∨ b = 1
  | 0, bs => by
    simp only [bitTuples, List.mem_singleton]
    constructor
    · rintro rfl
      exact ⟨rfl, fun b hb => absurd hb List.not_mem_nil⟩
    · rintro ⟨h, -⟩
      exact List.eq_nil_of_length_eq_zero h
  | n + 1, bs => by
    simp only [bitTuples, List.mem_flatMap, List.mem_map, List.mem_cons, List.not_mem_nil, or_false]
    constructor
    · rintro ⟨b, hb, bs', hbs', rfl⟩
      obtain ⟨hl, hall⟩ := (mem_bitTuples n bs').1 hbs'
      refine ⟨by simp [hl], fun x hx => ?_⟩
      rcases List.mem_cons.1 hx with rfl | hx
      · exact hb
      · exact hall x hx
    · rintro ⟨hl, hall⟩
      match bs, hl with
      | b :: bs', hl =>
        exact ⟨b, hall b List.mem_cons_self, bs',
          (mem_bitTuples n bs').2 ⟨by simpa using hl, fun x hx => hall x (List.mem_cons_of_mem _ hx)⟩, rfl⟩

theorem lookup_zip_mem : ∀ {l1 l2 : List Nat} {L v : Nat}, List.lookup L (l1.zip l2) = some v → v ∈ l2
  | [], _, _, _, h => by simp at h
  | _ :: _, [], _, _, h => by simp at h
  | a :: l1, b :: l2, L, v, h => by
    rw [List.zip_cons_cons, List.lookup_cons] at h
    by_cases hL : L = a
    · subst hL
      simp only [beq_self_eq_true] at h
      cases h
      exact List.mem_cons_self
    · have hb : (L == a) = false := by simpa using hL
      simp only [hb] at h
      exact List.mem_cons_of_mem _ (lookup_zip_mem h)

theorem hOf_01 {free hbits : List Nat} (hb : hbits ∈ bitTuples free.length) (L : Nat) :
    hOf free hbits L = 0 ∨ hOf free hbits L = 1 := by
  unfold hOf
  split
  · exact Or.inl rfl
  · cases hl : List.lookup L (free.zip hbits) with
    | none => exact Or.inl rfl
    | some v =>
      have := ((mem_bitTuples _ _).1 hb).2 v (lookup_zip_mem hl)
      simpa using this

theorem hLit_ne_zero (t i : Nat) : hLit t i ≠ 0 := by
  simp only [hLit, hCode]
  omega

theorem mem_hPremOf_ne_zero {t : Nat} {free : List Nat} {h : Nat → Nat} {p : Int}
    (hp : p ∈ hPremOf (hLit t) free h) : p ≠ 0 := by
  simp only [hPremOf, List.mem_map] at hp
  obtain ⟨L, _, rfl⟩ := hp
  split
  · exact hLit_ne_zero t L
  · exact Int.neg_ne_zero.2 (hLit_ne_zero t L)

/-- A true H premise fixes the bit to the model's. -/
theorem hPrem_holds {m K t : Nat} (M : ModelO m K t) {L : Nat} (hL : L < t) {hval : Nat}
    (h01 : hval = 0 ∨ hval = 1)
    (hp : CodeLitHolds M.τc (if hval == 0 then hLit t L else -(hLit t L))) : hval = hbit M.hb L := by
  rcases h01 with rfl | rfl
  · simp only [beq_self_eq_true, if_true] at hp
    have := (holds_hO M hL).1 hp
    simp only [hbit, this, if_true]
  · have hne : ((1 : Nat) == 0) = false := rfl
    simp only [hne, Bool.false_eq_true, if_false] at hp
    have h1 := (codeLitHolds_neg (hLit_ne_zero t L)).1 hp
    rw [holds_hO M hL] at h1
    simp only [hbit, Bool.not_eq_true] at h1 ⊢
    simp [h1]

/-! ### Copies of ENCBLEAN's rank lemmas for `ModelO` -/

theorem rkMono_ofO {m K t : Nat} (M : ModelO m K t) {c : List Pt} (hc : ∀ x ∈ c, PtOk m t x) {rk : Nat → Nat}
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

theorem premF_holdsO {m K t : Nat} (M : ModelO m K t) {rk : Nat → Nat} {p q : Nat} (hp : p < t) (hq : q < t)
    (hne : p ≠ q) (h : CodeLitHolds M.τc (premF (yLit t) rk (p, q))) :
    (rk p < rk q → M.psiLt p q = true) ∧ (rk q < rk p → M.psiLt q p = true) := by
  simp only [premF] at h
  by_cases hpq : p < q
  · simp only [hpq, if_true] at h
    by_cases hr : rk p < rk q
    · simp only [hr, decide_true, if_true] at h
      have h1 := (holds_yO M hp hq).1 h
      exact ⟨fun _ => h1, fun h' => absurd h' (by omega)⟩
    · simp only [hr, decide_false, Bool.false_eq_true, if_false] at h
      have h1 := (codeLitHolds_neg (yLit_ne_zero t p q)).1 h
      rw [holds_yO M hp hq] at h1
      refine ⟨fun h' => absurd h' hr, fun _ => ?_⟩
      rcases M.psiLt_total p q hp hq hne with h2 | h2
      · exact absurd h2 h1
      · exact h2
  · simp only [hpq, if_false] at h
    by_cases hr : rk q < rk p
    · simp only [hr, decide_true, if_true] at h
      have h1 := (holds_yO M hq hp).1 h
      exact ⟨fun h' => absurd h' (by omega), fun _ => h1⟩
    · simp only [hr, decide_false, Bool.false_eq_true, if_false] at h
      have h1 := (codeLitHolds_neg (yLit_ne_zero t q p)).1 h
      rw [holds_yO M hq hp] at h1
      refine ⟨fun _ => ?_, fun h' => absurd h' hr⟩
      rcases M.psiLt_total q p hq hp (Ne.symm hne) with h2 | h2
      · exact absurd h2 h1
      · exact h2

theorem rkMono_of_premO {m K t : Nat} (M : ModelO m K t) {c : List Pt} (hc : ∀ x ∈ c, PtOk m t x)
    {ranks : List Nat} (hall : ∀ p ∈ premOf (yLit t) (freeOf c) (rkOf (freeOf c) ranks), CodeLitHolds M.τc p) :
    RkMono M.psiLt (rkOf (freeOf c) ranks) c := by
  refine rkMono_ofO M hc (rkOf_zero _ _) (fun u hu v hv huv => ?_)
  have hne : u ≠ v := by
    rintro rfl
    exact Nat.lt_irrefl _ huv
  have hut := freeOf_lt hc hu
  have hvt := freeOf_lt hc hv
  rw [premOf_eq] at hall
  rcases mem_pairs_of_ne hu hv hne with h | h
  · exact (premF_holdsO M hut hvt hne (hall _ (List.mem_map_of_mem h))).1 huv
  · exact (premF_holdsO M hvt hut (Ne.symm hne) (hall _ (List.mem_map_of_mem h))).2 huv

theorem exists_rkMonoO {m K t : Nat} (M : ModelO m K t) {c : List Pt} (hc : ∀ x ∈ c, PtOk m t x) :
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
  · refine rkMono_ofO M hc (rkOf_zero _ _) (fun u hu v hv huv => ?_)
    have hr : ∀ L ∈ freeOf c, rkOf (freeOf c) ((freeOf c).map s.idxOf) L = s.idxOf L + 1 := by
      intro L hL
      have hL0 : (L == 0) = false := by simpa using (mem_freeOf.1 hL).2
      simp only [rkOf, hL0, lookup_zip_map hL, Option.map_some, Option.getD_some, Bool.false_eq_true, if_false]
    rw [hr u hu, hr v hv] at huv
    exact rel_of_idxOf_lt hss (hsp.mem_iff.2 hu) (hsp.mem_iff.2 hv) (by omega)

/-! ### (i) and (ii) for the bits -/

/-- (i) All H premises true ⇒ the bits are the model's on every layer of the triple. -/
theorem hbits_of_prem {m K t : Nat} (M : ModelO m K t) {c : List Pt} (hc : ∀ x ∈ c, PtOk m t x)
    {hbits : List Nat} (hb : hbits ∈ bitTuples (freeOf c).length)
    (hall : ∀ p ∈ hPremOf (hLit t) (freeOf c) (hOf (freeOf c) hbits), CodeLitHolds M.τc p) :
    ∀ x ∈ c, hOf (freeOf c) hbits x.1 = hbit M.hb x.1 := by
  intro x hx
  by_cases hx0 : x.1 = 0
  · rw [hx0]
    simp only [hOf, beq_self_eq_true, if_true, hbit, M.hb_zero]
  · have hL : x.1 ∈ freeOf c := mem_freeOf.2 ⟨⟨x, hx, rfl⟩, hx0⟩
    have hp := hall _ (List.mem_map_of_mem (f := fun L =>
      if hOf (freeOf c) hbits L == 0 then hLit t L else -(hLit t L)) hL)
    exact hPrem_holds M (hc x hx).1 (hOf_01 hb x.1) hp

/-- (ii) The model's bits form an entry of `bitTuples`, and `hOf` reads them back. -/
theorem exists_hbits {m K t : Nat} (M : ModelO m K t) (c : List Pt) :
    ∃ hbits ∈ bitTuples (freeOf c).length, ∀ x ∈ c, hOf (freeOf c) hbits x.1 = hbit M.hb x.1 := by
  refine ⟨(freeOf c).map (hbit M.hb), (mem_bitTuples _ _).2 ⟨List.length_map _, ?_⟩, ?_⟩
  · intro b hb
    obtain ⟨L, _, rfl⟩ := List.mem_map.1 hb
    have := hbit_le_one M.hb L
    omega
  · intro x hx
    by_cases hx0 : x.1 = 0
    · rw [hx0]
      simp only [hOf, beq_self_eq_true, if_true, hbit, M.hb_zero]
    · have hL : x.1 ∈ freeOf c := mem_freeOf.2 ⟨⟨x, hx, rfl⟩, hx0⟩
      have hL0 : (x.1 == 0) = false := by simpa using hx0
      simp only [hOf, hL0, Bool.false_eq_true, if_false, lookup_zip_map hL, Option.getD_some]

end AngO

open Ang AngO in
/-- **The angular clauses of odd `m`.** Every angular clause (unit or conditional) of an orbit representative holds
under the intended assignment of a `ModelO`, given that orbit representatives are three distinct valid labels
(`OrbListSpec`, proved by ENCBLEAN as `orbListSpec`) and `PatternSpecO` (`patternSpecO`). -/
theorem angCl_soundO {m K t : Nat} (M : ModelO m K t) (hodd : m % 2 = 1) (hOL : OrbListSpec m t)
    (hP : PatternSpecO M) :
    ∀ c ∈ orbList m t, ∀ cl ∈ angClOf (angOutsC m t c).1, ∃ x ∈ cl, CodeLitHolds M.τc x := by
  intro c hc cl hcl
  obtain ⟨a, b, d, rfl, ha, hb, hd, hdist⟩ := hOL c hc
  have hcOk : ∀ x ∈ [a, b, d], PtOk m t x := by
    intro x hx
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
    rcases hx with rfl | rfl | rfl <;> assumption
  rw [angOutsC_odd hodd] at hcl
  generalize hO : (angOuts m true (yLit t) (hLit t) (orbVarC m t) [a, b, d] (orbCode m t [a, b, d])).1 = O
    at hcl
  unfold angClOf at hcl
  split at hcl
  · next l hl =>
    obtain ⟨ranks, hr, hmono⟩ := exists_rkMonoO M hcOk
    obtain ⟨hbits, hbm, hhb⟩ := exists_hbits M [a, b, d]
    have hmem := mem_angOuts_odd' (m := m) (yv := yLit t) (hv := hLit t) (orbVar := orbVarC m t)
      (v := orbCode m t [a, b, d]) hr hbm
    rw [hO] at hmem
    have hlit := unitOf_some hl _ hmem
    rw [List.mem_singleton] at hcl
    subst hcl
    exact ⟨l, List.mem_singleton_self _, hP a b d _ _ l ha hb hd hdist hmono hhb hlit⟩
  · rw [List.mem_filterMap] at hcl
    obtain ⟨o, ho, hcl⟩ := hcl
    rw [← hO] at ho
    obtain ⟨ranks, hr, hbits, hbm, rfl⟩ := mem_angOuts_odd ho
    rw [Option.map_eq_some_iff] at hcl
    obtain ⟨l, hpl, rfl⟩ := hcl
    by_cases hall : ∀ p ∈ premOf (yLit t) (freeOf [a, b, d]) (rkOf (freeOf [a, b, d]) ranks) ++
        hPremOf (hLit t) (freeOf [a, b, d]) (hOf (freeOf [a, b, d]) hbits), CodeLitHolds M.τc p
    · have hY : ∀ p ∈ premOf (yLit t) (freeOf [a, b, d]) (rkOf (freeOf [a, b, d]) ranks), CodeLitHolds M.τc p :=
        fun p hp => hall p (List.mem_append_left _ hp)
      have hH : ∀ p ∈ hPremOf (hLit t) (freeOf [a, b, d]) (hOf (freeOf [a, b, d]) hbits), CodeLitHolds M.τc p :=
        fun p hp => hall p (List.mem_append_right _ hp)
      exact ⟨l, List.mem_append_right _ (List.mem_singleton_self _),
        hP a b d _ _ l ha hb hd hdist (rkMono_of_premO M hcOk hY) (hbits_of_prem M hcOk hbm hH) hpl⟩
    · obtain ⟨p, hp, hnp⟩ : ∃ p ∈ premOf (yLit t) (freeOf [a, b, d]) (rkOf (freeOf [a, b, d]) ranks) ++
          hPremOf (hLit t) (freeOf [a, b, d]) (hOf (freeOf [a, b, d]) hbits), ¬ CodeLitHolds M.τc p :=
        Classical.byContradiction fun hn => hall fun p hp => Classical.byContradiction fun hnp => hn ⟨p, hp, hnp⟩
      have hp0 : p ≠ 0 := by
        rcases List.mem_append.1 hp with hp | hp
        · exact mem_premOf_ne_zero hp
        · exact mem_hPremOf_ne_zero hp
      exact ⟨-p, List.mem_append_left _ (List.mem_map_of_mem hp), (codeLitHolds_neg hp0).2 hnp⟩

/-- info: 'EncB.angCl_soundO' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms angCl_soundO

end EncB
