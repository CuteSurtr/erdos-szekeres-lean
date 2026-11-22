import EncB.SortLemmas
import EncB.SoundOlit

/-!
# M3 unit U1: the orbit list, ψ-order transitivity and the nesting units

Frozen statements (plan `docs/M3PLAN.md` §2.2, unit U1):

* `orbListSpec`: every entry of `orbList m t` is a list `[a, b, d]` of three distinct valid labels. `orbList` is
  `dedupBy` of `canon` over `triples (labels m t)`; `dedupBy` keeps only input entries (`Orbit.mem_dedupBy`),
  `labels` has no repetition (`Orbit.labels_nodup`), and `canon tri` is the sorted image of `tri` under one
  rotation (`Orbit.canon_eq`), which is injective on valid labels (`Orbit.rotBy_inj`).
* `transCl_sound`: the two ψ-order transitivity clauses hold (`psiLt_trans`; `psiLt_total` and `psiLt_irrefl`).
* `nestLits_sound`: the nesting units hold (`olitSpec` and `Model.nest`; `2 ≤ m` makes `(i, 1)` valid).

Std-only; every helper lives in `EncB.Orbit`.
-/

namespace EncB

namespace Orbit

/-! ### `dedupBy` keeps only entries of its input -/

theorem mem_dedup_foldl_of {α : Type} (key : α → Nat) {x : α} :
    ∀ (l : List α) (st : Array Bool × List α), x ∈ (l.foldl (dedupStep key) st).2 → x ∈ st.2 ∨ x ∈ l
  | [], _, h => Or.inl h
  | a :: l, st, h => by
    rw [List.foldl_cons] at h
    rcases mem_dedup_foldl_of key l (dedupStep key st a) h with h' | h'
    · unfold dedupStep at h'
      split at h'
      · exact Or.inl h'
      · rcases List.mem_cons.1 h' with rfl | h''
        · exact Or.inr List.mem_cons_self
        · exact Or.inl h''
    · exact Or.inr (List.mem_cons_of_mem _ h')

theorem mem_dedupBy {α : Type} {key : α → Nat} {S : Nat} {l : List α} {x : α} (h : x ∈ dedupBy key S l) :
    x ∈ l := by
  rw [dedupBy, List.mem_reverse] at h
  rcases mem_dedup_foldl_of key l _ h with h | h
  · exact absurd h List.not_mem_nil
  · exact h

/-! ### `labels` has no repetition -/

theorem labels_nodup (m t : Nat) : (labels m t).Nodup := by
  unfold labels
  rw [List.Nodup, List.pairwise_flatMap]
  refine ⟨fun i _ => ?_, ?_⟩
  · rw [List.pairwise_map]
    exact (rng_pairwise 0 m).imp fun h e => by
      simp only [Prod.mk.injEq] at e
      omega
  · refine (rng_pairwise 0 t).imp fun {i j} h => ?_
    intro x hx y hy e
    rw [List.mem_map] at hx hy
    obtain ⟨k, _, rfl⟩ := hx
    obtain ⟨k', _, rfl⟩ := hy
    simp only [Prod.mk.injEq] at e
    omega

/-! ### `canon` is a sorted rotation -/

/-- A fold whose step always returns `some` of a value with property `P` (given `P` of the previous `some`)
returns `some` of such a value, once the accumulator is `some` or the list is nonempty. -/
theorem foldl_some {α β : Type} (P : α → Prop) (f : Option α → β → Option α)
    (hf : ∀ o x, (∀ b, o = some b → P b) → ∃ b, f o x = some b ∧ P b) :
    ∀ (l : List β) (o : Option α), (∀ b, o = some b → P b) → (o.isSome ∨ l ≠ []) →
      ∃ b, l.foldl f o = some b ∧ P b
  | [], o, ho, hne => by
    rcases hne with hs | hne
    · cases o with
      | none => simp at hs
      | some b => exact ⟨b, rfl, ho b rfl⟩
    · exact absurd rfl hne
  | x :: l, o, ho, _ => by
    obtain ⟨b, hb, hPb⟩ := hf o x ho
    rw [List.foldl_cons]
    refine foldl_some P f hf l (f o x) (fun b' e => ?_) (Or.inl (by rw [hb]; rfl))
    rw [hb] at e
    cases e
    exact hPb

theorem foldl_getD {α β : Type} (P : α → Prop) (f : Option α → β → Option α)
    (hf : ∀ o x, (∀ b, o = some b → P b) → ∃ b, f o x = some b ∧ P b) (l : List β) (d : α) (hne : l ≠ []) :
    P ((l.foldl f none).getD d) := by
  obtain ⟨b, hb, hPb⟩ := foldl_some P f hf l none (fun _ e => by cases e) (Or.inr hne)
  rw [hb]
  exact hPb

theorem canon_eq (m : Nat) {tri : List Pt} (hne : tri ≠ []) :
    ∃ s, canon m tri = insSort ptLt (tri.map (rotBy m s)) := by
  unfold canon
  dsimp only
  refine foldl_getD (fun b => ∃ s, b = insSort ptLt (tri.map (rotBy m s))) _ ?_ tri [] hne
  intro o x ho
  cases o with
  | none => exact ⟨_, rfl, negMod m x.2, rfl⟩
  | some b =>
    dsimp only
    split
    · exact ⟨_, rfl, negMod m x.2, rfl⟩
    · exact ⟨b, rfl, ho b rfl⟩

/-! ### Rotation is injective on valid sectors -/

theorem add_mod_cases {m s u : Nat} (hu : u < m) :
    (u + s) % m = if u + s % m < m then u + s % m else u + s % m - m := by
  have hr : s % m < m := Nat.mod_lt _ (by omega)
  rw [Nat.add_mod, Nat.mod_eq_of_lt hu]
  split
  · exact Nat.mod_eq_of_lt ‹_›
  · rw [Nat.mod_eq_sub_mod (by omega), Nat.mod_eq_of_lt (by omega)]

theorem rotBy_inj {m s : Nat} {x y : Pt} (hx : x.2 < m) (hy : y.2 < m) (h : rotBy m s x = rotBy m s y) :
    x = y := by
  simp only [rotBy, Prod.mk.injEq] at h
  obtain ⟨h1, h2⟩ := h
  have hr : s % m < m := Nat.mod_lt _ (by omega)
  rw [add_mod_cases hx, add_mod_cases hy] at h2
  have h3 : x.2 = y.2 := by
    split at h2 <;> split at h2 <;> omega
  exact Prod.ext h1 h3

/-- `canon` of distinct valid labels: valid labels, no repetition, the same length. -/
theorem canon_props {m t : Nat} {tri : List Pt} (hne : tri ≠ []) (hall : ∀ p ∈ tri, PtOk m t p)
    (hnd : tri.Nodup) :
    (∀ p ∈ canon m tri, PtOk m t p) ∧ (canon m tri).Nodup ∧ (canon m tri).length = tri.length := by
  obtain ⟨s, hs⟩ := canon_eq m hne
  have hp := insSort_perm ptLt (tri.map (rotBy m s))
  rw [hs]
  refine ⟨fun p hp' => ?_, hp.nodup_iff.2 ?_, by rw [hp.length_eq, List.length_map]⟩
  · obtain ⟨q, hq, rfl⟩ := List.mem_map.1 (hp.mem_iff.1 hp')
    exact ptOk_rotBy (hall q hq)
  · rw [List.Nodup, List.pairwise_map]
    exact hnd.imp_of_mem fun ha hb hne e => hne (rotBy_inj (hall _ ha).2 (hall _ hb).2 e)

theorem three_of {m t : Nat} : ∀ {c : List Pt}, (∀ p ∈ c, PtOk m t p) → c.Nodup → c.length = 3 →
    ∃ a b d, c = [a, b, d] ∧ PtOk m t a ∧ PtOk m t b ∧ PtOk m t d ∧ Distinct3 a b d
  | [a, b, d], hok, hnd, _ => by
    simp only [List.nodup_cons, List.mem_cons, List.not_mem_nil, or_false, not_or, List.nodup_nil,
      not_false_eq_true, and_true] at hnd
    exact ⟨a, b, d, rfl, hok a (by simp), hok b (by simp), hok d (by simp), hnd.1.1, hnd.1.2, hnd.2⟩

/-! ### Literals of the ψ order -/

theorem yLit_ne (t i j : Nat) : yLit t i j ≠ 0 := by
  simp only [yLit, yCode]
  omega

theorem holds_ny {m K t : Nat} (M : Model m K t) {i j : Nat} (hi : i < t) (hj : j < t) :
    CodeLitHolds M.τc (-(yLit t i j)) ↔ M.psiLt i j = false := by
  rw [codeLitHolds_neg (yLit_ne t i j), holds_y M hi hj, Bool.not_eq_true]

end Orbit

/-! ## The frozen statements of U1 -/

theorem orbListSpec (m t : Nat) : OrbListSpec m t := by
  intro c hc
  unfold orbList at hc
  have hc' := Orbit.mem_dedupBy hc
  rw [List.mem_map] at hc'
  obtain ⟨⟨x, y, z⟩, hxyz, rfl⟩ := hc'
  dsimp only
  have hsub := sublist_of_mem_triples hxyz
  have hnd : [x, y, z].Nodup := hsub.nodup (Orbit.labels_nodup m t)
  have hall : ∀ p ∈ [x, y, z], PtOk m t p := fun p hp => mem_labels.1 (hsub.subset hp)
  obtain ⟨hok, hnd', hlen⟩ := Orbit.canon_props (List.cons_ne_nil _ _) hall hnd
  exact Orbit.three_of hok hnd' hlen

theorem transCl_sound {m K t : Nat} (M : Model m K t) :
    ∀ cl ∈ transCl t, ∃ x ∈ cl, CodeLitHolds M.τc x := by
  intro cl hcl
  simp only [transCl, List.mem_flatMap, List.mem_cons, List.not_mem_nil, or_false] at hcl
  obtain ⟨⟨i, j, k⟩, hijk, hcl⟩ := hcl
  have hsub := sublist_of_mem_triples hijk
  have hpw := (rng_pairwise 1 t).sublist hsub
  simp only [List.pairwise_cons, List.mem_cons, List.not_mem_nil, or_false, forall_eq_or_imp, forall_eq,
    List.Pairwise.nil, and_true] at hpw
  have hk : k ∈ rng 1 t := hsub.subset (by simp)
  rw [mem_rng] at hk
  have hi : i < t := by omega
  have hj : j < t := by omega
  have hk : k < t := hk.2
  rcases hcl with rfl | rfl
  · -- `[-Y(i,j), -Y(j,k), Y(i,k)]`
    cases hij : M.psiLt i j
    · exact ⟨_, List.mem_cons_self, (Orbit.holds_ny M hi hj).2 hij⟩
    cases hjk : M.psiLt j k
    · exact ⟨_, List.mem_cons_of_mem _ List.mem_cons_self, (Orbit.holds_ny M hj hk).2 hjk⟩
    exact ⟨_, by simp, (holds_y M hi hk).2 (M.psiLt_trans i j k hij hjk)⟩
  · -- `[Y(i,j), Y(j,k), -Y(i,k)]`
    cases hij : M.psiLt i j
    · cases hjk : M.psiLt j k
      · refine ⟨_, by simp, (Orbit.holds_ny M hi hk).2 ?_⟩
        cases hik : M.psiLt i k
        · rfl
        · exfalso
          have hji : M.psiLt j i = true :=
            (M.psiLt_total i j hi hj (by omega)).resolve_left (Bool.eq_false_iff.1 hij)
          have hkj : M.psiLt k j = true :=
            (M.psiLt_total j k hj hk (by omega)).resolve_left (Bool.eq_false_iff.1 hjk)
          have hii := M.psiLt_trans i k i hik (M.psiLt_trans k j i hkj hji)
          rw [M.psiLt_irrefl] at hii
          exact Bool.false_ne_true hii
      · exact ⟨_, List.mem_cons_of_mem _ List.mem_cons_self, (holds_y M hj hk).2 hjk⟩
    · exact ⟨_, List.mem_cons_self, (holds_y M hi hj).2 hij⟩

theorem nestLits_sound {m K t : Nat} (M : Model m K t) (hm : 2 ≤ m) :
    ∀ l ∈ nestLits m t, CodeLitHolds M.τc l := by
  intro l hl
  simp only [nestLits, List.mem_flatMap, List.mem_filterMap, mem_rng] at hl
  obtain ⟨i, hi, j, hj, k, hk, h⟩ := hl
  have h0 : PtOk m t (i, 0) := show i < t ∧ 0 < m from ⟨by omega, by omega⟩
  have h1 : PtOk m t (i, 1) := show i < t ∧ 1 < m from ⟨by omega, by omega⟩
  have h2 : PtOk m t (j, k) := show j < t ∧ k < m from ⟨by omega, by omega⟩
  exact ((olitSpec M (i, 0) (i, 1) (j, k) l h0 h1 h2 h).2).2 (M.nest i j k (by omega) (by omega) (by omega))

/-! ## Axioms -/

/-- info: 'EncB.orbListSpec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms orbListSpec

/-- info: 'EncB.transCl_sound' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms transCl_sound

/-- info: 'EncB.nestLits_sound' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms nestLits_sound

end EncB
