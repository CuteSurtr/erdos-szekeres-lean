import D3Encoding.Triples

/-!
# The triple table is consistent and complete
-/

namespace D3

open Std

/-- The DIMACS meaning of a literal (as `ETV.DimacsSat`). -/
def LitSat (ν : Nat → Bool) (l : Int) : Prop :=
  (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false)

/-- Invariant of the triple table: keys are increasing triples, variables are in `1..n`,
signs are `±1`, and `e.2 · χ(S)` depends only on the variable `e.1`. -/
def TInv (χ : Nat → Nat → Nat → Int) (P : Nat) (tv : TV) (n : Nat) : Prop :=
  ∀ (S : Nat × Nat × Nat) (e : Nat × Int), tv[S]? = some e → ValidT P S ∧ 1 ≤ e.1 ∧ e.1 ≤ n ∧ (e.2 = 1 ∨ e.2 = -1) ∧
    ∀ (S' : Nat × Nat × Nat) (e' : Nat × Int), tv[S']? = some e' → e'.1 = e.1 → e'.2 * chiT χ S' = e.2 * chiT χ S

theorem getElem?_insertIfNew_of_some {tv : TV} {k S : Nat × Nat × Nat} {v e : Nat × Int}
    (h : tv[S]? = some e) : (tv.insertIfNew k v)[S]? = some e := by
  rw [HashMap.getElem?_insertIfNew]
  split
  · rename_i h'
    exfalso; apply h'.2
    have : k = S := by simpa using h'.1
    subst this
    exact HashMap.mem_iff_isSome_getElem?.2 (by simp [h])
  · exact h

section
variable {t : Nat} {χ : Nat → Nat → Nat → Int}

theorem insertOrbit_spec (hχ : Chirotope t χ) {a b c v : Nat} (ha : a < 3 * t + 1)
    (hb : b < 3 * t + 1) (hc : c < 3 * t + 1) (hab : a ≠ b) (hac : a ≠ c) (hbc : b ≠ c) :
    ∀ (gs : List ((Nat → Nat) × Int)), (∀ g ∈ gs, g ∈ group t) → ∀ tv0 : TV,
      (∀ (S : Nat × Nat × Nat) (e : Nat × Int), (gs.foldl (orbitStep a b c v) tv0)[S]? = some e →
        tv0[S]? = some e ∨ (e.1 = v ∧ e.2 * chiT χ S = χ a b c ∧ ValidT (3 * t + 1) S ∧
          (e.2 = 1 ∨ e.2 = -1))) ∧
      (∀ (S : Nat × Nat × Nat) (e : Nat × Int), tv0[S]? = some e → (gs.foldl (orbitStep a b c v) tv0)[S]? = some e)
  | [], _, tv0 => ⟨fun S e h => Or.inl h, fun S e h => h⟩
  | g :: gs, hgs, tv0 => by
    simp only [List.foldl_cons]
    obtain ⟨ih1, ih2⟩ := insertOrbit_spec hχ ha hb hc hab hac hbc gs
      (fun g' hg' => hgs g' (List.mem_cons_of_mem _ hg')) (orbitStep a b c v tv0 g)
    have hg := hgs g (List.mem_cons_self ..)
    obtain ⟨hlt, -, hinj, hsg⟩ := group_perm g hg
    have hga := hlt a ha
    have hgb := hlt b hb
    have hgc := hlt c hc
    have d1 : g.1 a ≠ g.1 b := fun h => hab (hinj _ _ ha hb h)
    have d2 : g.1 a ≠ g.1 c := fun h => hac (hinj _ _ ha hc h)
    have d3 : g.1 b ≠ g.1 c := fun h => hbc (hinj _ _ hb hc h)
    obtain ⟨hV, hs, hrel⟩ := paritySort_spec hga hgb hgc d1 d2 d3
    have hrel' := hrel χ hχ.swap12 hχ.swap23
    have heq := hχ.equiv g hg a b c ha hb hc
    refine ⟨fun S e h => ?_, fun S e h => ih2 S e (getElem?_insertIfNew_of_some h)⟩
    rcases ih1 S e h with h1 | h1
    · rw [orbitStep, HashMap.getElem?_insertIfNew] at h1
      split at h1
      · rename_i h'
        have : (paritySort (g.1 a) (g.1 b) (g.1 c)).1 = S := by simpa using h'.1
        subst this
        cases h1
        refine Or.inr ⟨rfl, ?_, hV, ?_⟩
        · simp only
          rw [heq] at hrel'
          rcases hs with hs | hs <;> rcases hsg with hsg | hsg <;> rw [hs, hsg] at hrel' ⊢ <;>
            omega
        · rcases hs with hs | hs <;> rcases hsg with hsg | hsg <;> simp [hs, hsg]
      · exact Or.inl h1
    · exact Or.inr h1

theorem insertOrbit_self {t a b c v : Nat} (hab : a < b) (hbc : b < c) (hc : c < 3 * t + 1)
    (tv : TV) : ((insertOrbit t a b c v tv)[(a, b, c)]?).isSome := by
  unfold insertOrbit
  have key : ∀ (gs : List ((Nat → Nat) × Int)) (tv : TV), (tv[(a, b, c)]?).isSome →
      ((gs.foldl (orbitStep a b c v) tv)[(a, b, c)]?).isSome := by
    intro gs
    induction gs with
    | nil => intro tv h; exact h
    | cons g gs ih =>
      intro tv h
      simp only [List.foldl_cons]
      apply ih
      obtain ⟨e, he⟩ := Option.isSome_iff_exists.1 h
      rw [orbitStep, getElem?_insertIfNew_of_some he]; rfl
  have hg : group t = (rot (3 * t) 0, 1) :: (group t).tail := rfl
  rw [hg, List.foldl_cons]
  apply key
  unfold orbitStep
  simp only
  have h0 : ∀ i, i < 3 * t + 1 → rot (3 * t) 0 i = i := by
    intro i hi; unfold rot; split <;> omega
  rw [h0 a (by omega), h0 b (by omega), h0 c hc]
  have : (paritySort a b c).1 = (a, b, c) := by simp [paritySort, hab, hbc]
  rw [this, HashMap.getElem?_insertIfNew]
  split
  · rfl
  · rename_i h
    have hm : (a, b, c) ∈ tv :=
      Classical.byContradiction fun hm => h ⟨by simp, hm⟩
    exact HashMap.mem_iff_isSome_getElem?.1 hm

theorem tripleStep_spec (hχ : Chirotope t χ) :
    ∀ (l : List (List Nat)), (∀ T ∈ l, T ∈ combs (List.range (3 * t + 1)) 3) →
      ∀ st : TV × Nat, TInv χ (3 * t + 1) st.1 st.2 →
        TInv χ (3 * t + 1) (l.foldl (tripleStep t) st).1 (l.foldl (tripleStep t) st).2 ∧
        (∀ S : Nat × Nat × Nat, (st.1[S]?).isSome → ((l.foldl (tripleStep t) st).1[S]?).isSome) ∧
        (∀ a b c, [a, b, c] ∈ l → ((l.foldl (tripleStep t) st).1[(a, b, c)]?).isSome)
  | [], _, st, h => ⟨h, fun _ h => h, by simp⟩
  | T :: l, hl, st, hinv => by
    obtain ⟨a, b, c, rfl, hab, hbc, hc⟩ := mem_combs3.1 (hl T (List.mem_cons_self ..))
    simp only [List.foldl_cons]
    -- the step
    have hstep : TInv χ (3 * t + 1) (tripleStep t st [a, b, c]).1 (tripleStep t st [a, b, c]).2 ∧
        (∀ S : Nat × Nat × Nat, (st.1[S]?).isSome → ((tripleStep t st [a, b, c]).1[S]?).isSome) ∧
        ((tripleStep t st [a, b, c]).1[(a, b, c)]?).isSome := by
      by_cases hcon : st.1.contains (a, b, c) = true
      · have e : tripleStep t st [a, b, c] = st := by simp only [tripleStep, hcon, if_true]
        rw [e]
        refine ⟨hinv, fun _ h => h, ?_⟩
        rw [HashMap.contains_eq_isSome_getElem?] at hcon
        exact hcon
      · have e : tripleStep t st [a, b, c] = (insertOrbit t a b c (st.2 + 1) st.1, st.2 + 1) := by
          simp only [tripleStep, hcon]
          rfl
        rw [e]
        refine ⟨?_, ?_, insertOrbit_self hab hbc hc _⟩
        · obtain ⟨h1, -⟩ := insertOrbit_spec hχ (a := a) (b := b) (c := c) (v := st.2 + 1) (by omega) (by omega) hc
            (by omega) (by omega) (by omega) (group t) (fun g hg => hg) st.1
          intro S e hS
          rcases h1 S e hS with h | ⟨hv, hrel, hV, hs⟩
          · obtain ⟨hV, k1, k2, hs, hcons⟩ := hinv S e h
            refine ⟨hV, k1, by omega, hs, fun S' e' hS' he' => ?_⟩
            rcases h1 S' e' hS' with h' | ⟨hv', -, -, -⟩
            · exact hcons S' e' h' he'
            · omega
          · refine ⟨hV, by omega, by omega, hs, fun S' e' hS' he' => ?_⟩
            rcases h1 S' e' hS' with h' | ⟨hv', hrel', -, -⟩
            · have := (hinv S' e' h').2.2.1; omega
            · rw [hrel, hrel']
        · intro S hS
          obtain ⟨e, he⟩ := Option.isSome_iff_exists.1 hS
          obtain ⟨-, h2⟩ := insertOrbit_spec hχ (a := a) (b := b) (c := c) (v := st.2 + 1) (by omega) (by omega) hc
            (by omega) (by omega) (by omega) (group t) (fun g hg => hg) st.1
          rw [insertOrbit, h2 S e he]; rfl
    obtain ⟨ih1, ih2, ih3⟩ := tripleStep_spec hχ l
      (fun T hT => hl T (List.mem_cons_of_mem _ hT)) _ hstep.1
    refine ⟨ih1, fun S hS => ih2 S (hstep.2.1 S hS), fun x y z hxyz => ?_⟩
    rcases List.mem_cons.1 hxyz with h | h
    · cases h
      exact ih2 _ hstep.2.2
    · exact ih3 x y z h

/-- The final table: consistent, and every increasing triple below `3 t + 1` is a key. -/
theorem triples_spec (hχ : Chirotope t χ) :
    TInv χ (3 * t + 1) (triples t).1 (triples t).2 ∧
    ∀ a b c, a < b → b < c → c < 3 * t + 1 → ((triples t).1[(a, b, c)]?).isSome := by
  obtain ⟨h1, -, h3⟩ := tripleStep_spec hχ (combs (List.range (3 * t + 1)) 3)
    (fun T hT => hT) ({}, 0) (by intro S e h; simp at h)
  refine ⟨h1, fun a b c hab hbc hc => h3 a b c ?_⟩
  exact mem_combs3.2 ⟨a, b, c, rfl, hab, hbc, hc⟩

end

/-- The intended value of triple variable `v`. -/
def NuT (χ : Nat → Nat → Nat → Int) (tv : TV) (v : Nat) : Prop :=
  ∃ (S : Nat × Nat × Nat) (e : Nat × Int), tv[S]? = some e ∧ e.1 = v ∧ e.2 * chiT χ S = 1

theorem lit_spec {t : Nat} {χ : Nat → Nat → Nat → Int} (hχ : Chirotope t χ) {tv : TV} {n : Nat}
    (hinv : TInv χ (3 * t + 1) tv n)
    (hcov : ∀ a b c, a < b → b < c → c < 3 * t + 1 → (tv[(a, b, c)]?).isSome)
    {ν : Nat → Bool} (hν : ∀ v, 1 ≤ v → v ≤ n → (ν v = true ↔ NuT χ tv v))
    {a b c : Nat} (ha : a < 3 * t + 1) (hb : b < 3 * t + 1) (hc : c < 3 * t + 1)
    (hab : a ≠ b) (hac : a ≠ c) (hbc : b ≠ c) {s : Int} (hs : s = 1 ∨ s = -1) :
    LitSat ν (s * lit tv a b c) ↔ s * χ a b c = 1 := by
  obtain ⟨hV, hp, hrel⟩ := paritySort_spec ha hb hc hab hac hbc
  have hrel' := hrel χ hχ.swap12 hχ.swap23
  rcases hS : (paritySort a b c).1 with ⟨x, y, z⟩
  rw [hS] at hV hrel'
  simp only [ValidT] at hV
  obtain ⟨e, he⟩ := Option.isSome_iff_exists.1 (hcov x y z hV.1 hV.2.1 hV.2.2)
  obtain ⟨-, he1, he2, hes, hcons⟩ := hinv _ e he
  have hχS : chiT χ (x, y, z) = 1 ∨ chiT χ (x, y, z) = -1 :=
    hχ.sign x y z (by omega) (by omega) hV.2.2
      (by omega) (by omega)
      (by omega)
  have hnu : ν e.1 = true ↔ e.2 * chiT χ (x, y, z) = 1 := by
    rw [hν e.1 he1 he2]
    constructor
    · rintro ⟨S', e', hS', he', h1⟩
      rw [← hcons S' e' hS' he']; exact h1
    · intro h; exact ⟨_, e, he, rfl, h⟩
  have hlit : lit tv a b c = (paritySort a b c).2 * e.2 * (e.1 : Int) := by
    simp only [lit, HashMap.getD_eq_getD_getElem?, hS, he, Option.getD_some]
  rw [hlit, hrel']
  generalize (paritySort a b c).2 = p at hp ⊢
  generalize chiT χ (x, y, z) = w at hχS hnu ⊢
  obtain ⟨v, sg⟩ := e
  simp only at hnu he1 ⊢
  unfold LitSat
  rcases hs with rfl | rfl <;> rcases hp with rfl | rfl <;> rcases hes with rfl | rfl <;>
    rcases hχS with rfl | rfl <;> simp at hnu ⊢ <;> simp [hnu] <;> omega

end D3
