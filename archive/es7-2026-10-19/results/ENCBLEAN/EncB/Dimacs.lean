/-!
# DIMACS semantics and the numbering of codes (Std-only)

* `DimacsSat` / `DimacsSatisfiable` are copied verbatim from H `ETVEncoding/Dimacs.lean:18,23` (with `Nat`/`Int`
  for `ℕ`/`ℤ`, the same terms), and `LitSat` from H3 `MirrorEncoding/Sound.lean:56`.
* `numberStep` / `numberMap` / `decode` and `numberStep_foldl` / `numberMap_getD` / `decode_numberMap` follow H
  `ETVEncoding/Clauses.lean:148-157` and `Dimacs.lean:27-91`, with one change: the map from codes to numbers is an
  `Array Nat` indexed by the code (0 = no number yet) instead of a `Std.HashMap`. The kernel can evaluate an `Array`
  (H's `HashMap` goes through `USize`, whose size the kernel cannot reduce), so `decide +kernel` can run `encB` on tiny
  instances (`EncB/KernelCheckB.lean`). The array has `1 + (largest code)` entries, so every code is in bounds.
* The two Mathlib lemmas H's proofs use, `List.idxOf_cons_ne` and `List.getElem_idxOf` (Mathlib
  `Data/List/Basic.lean:487,551`), are re-proved here from core (`EncB.idxOf_cons_ne`, `EncB.getElem_idxOf`).
* `dedupStep` keeps the first occurrence of each code (`allCodes` in `EncB/Coded.lean`); `mem_dedup_foldl` says that
  nothing is lost, whatever the size of the `seen` array.
-/

namespace EncB

/-! ### DIMACS semantics -/

/-- A Boolean assignment of variable numbers satisfies a list of DIMACS clauses (H `Dimacs.lean:18`). -/
def DimacsSat (cls : List (List Int)) (ν : Nat → Bool) : Prop :=
  ∀ c ∈ cls, ∃ l ∈ c, (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false)

/-- The DIMACS formula has a model (H `Dimacs.lean:23`). An UNSAT certificate for the file is a proof of the
negation of this proposition (trust item E3). -/
def DimacsSatisfiable (cls : List (List Int)) : Prop := ∃ ν, DimacsSat cls ν

/-- A DIMACS literal holds under `ν` (H3 `Sound.lean:56`). -/
def LitSat (ν : Nat → Bool) (z : Int) : Prop :=
  (0 < z ∧ ν z.natAbs = true) ∨ (z < 0 ∧ ν z.natAbs = false)

theorem dimacsSat_iff {cls : List (List Int)} {ν : Nat → Bool} :
    DimacsSat cls ν ↔ ∀ c ∈ cls, ∃ l ∈ c, LitSat ν l := Iff.rfl

/-! ### Two list lemmas (Mathlib's `List.idxOf_cons_ne` and `List.getElem_idxOf`, re-proved from core) -/

theorem idxOf_cons_ne {α : Type} [BEq α] [LawfulBEq α] {a v : α} (l : List α) (h : a ≠ v) :
    (a :: l).idxOf v = l.idxOf v + 1 := by
  rw [List.idxOf_cons]
  have : (a == v) = false := by simpa using h
  rw [this]
  rfl

theorem getElem_idxOf {α : Type} [BEq α] [LawfulBEq α] :
    ∀ {l : List α} {v : α} (h : l.idxOf v < l.length), l[l.idxOf v] = v
  | [], _, h => absurd h (Nat.not_lt_zero _)
  | a :: l, v, h => by
    by_cases hav : a = v
    · subst hav
      simp only [List.idxOf_cons_self, List.getElem_cons_zero]
    · have h' : l.idxOf v < l.length := by
        rw [idxOf_cons_ne l hav, List.length_cons] at h
        omega
      simp only [idxOf_cons_ne l hav, List.getElem_cons_succ]
      exact getElem_idxOf h'

/-! ### Arrays used as finite maps -/

theorem getD_setIfInBounds {α : Type} (xs : Array α) (i j : Nat) (a d : α) :
    (xs.setIfInBounds i a).getD j d = if i = j ∧ i < xs.size then a else xs.getD j d := by
  simp only [Array.getD_eq_getD_getElem?, Array.getElem?_setIfInBounds]
  by_cases hij : i = j
  · subst hij
    by_cases hi : i < xs.size <;> simp [hi]
  · simp [hij]

theorem getD_replicate {α : Type} (n i : Nat) (a : α) : (Array.replicate n a).getD i a = a := by
  simp only [Array.getD_eq_getD_getElem?, Array.getElem?_replicate]
  split <;> rfl

theorem le_foldl_max : ∀ (l : List Nat) (a : Nat), a ≤ l.foldl max a ∧ ∀ x ∈ l, x ≤ l.foldl max a
  | [], a => ⟨Nat.le_refl a, fun _ hx => absurd hx (List.not_mem_nil)⟩
  | b :: l, a => by
    obtain ⟨h1, h2⟩ := le_foldl_max l (max a b)
    simp only [List.foldl_cons]
    refine ⟨Nat.le_trans (Nat.le_max_left a b) h1, fun x hx => ?_⟩
    rcases List.mem_cons.1 hx with rfl | hx
    · exact Nat.le_trans (Nat.le_max_right a x) h1
    · exact h2 x hx

/-! ### The numbering: `1 +` the first position in the list -/

/-- One step of Python's `new()`: give `v` the next number unless it already has one (H `Clauses.lean:150`). -/
def numberStep (p : Array Nat × Nat) (v : Nat) : Array Nat × Nat :=
  (if p.1.getD v 0 == 0 then p.1.setIfInBounds v p.2 else p.1, p.2 + 1)

/-- Map each code to `1 +` its first position in the list (H `Clauses.lean:154`); entry 0 = no number. -/
def numberMap (l : List Nat) : Array Nat :=
  (l.foldl numberStep (Array.replicate (l.foldl max 0 + 1) 0, 1)).1

theorem size_numberStep_foldl : ∀ (l : List Nat) (p : Array Nat × Nat),
    (l.foldl numberStep p).1.size = p.1.size
  | [], _ => rfl
  | a :: l, p => by
    rw [List.foldl_cons, size_numberStep_foldl l]
    simp only [numberStep]
    split <;> simp

/-- H `Dimacs.lean:27`, for the array map. -/
theorem numberStep_foldl (v : Nat) : ∀ (l : List Nat) (arr : Array Nat) (c : Nat), 0 < c →
    (∀ x ∈ l, x < arr.size) →
    (l.foldl numberStep (arr, c)).1.getD v 0 =
      if arr.getD v 0 ≠ 0 then arr.getD v 0 else if v ∈ l then c + l.idxOf v else 0
  | [], arr, c, _, _ => by
    simp only [List.foldl_nil, List.not_mem_nil, if_false]
    by_cases h : arr.getD v 0 = 0 <;> simp [h]
  | a :: l, arr, c, hc, hb => by
    have ha : a < arr.size := hb a List.mem_cons_self
    obtain ⟨arr', harr'⟩ :
        ∃ arr', arr' = (if arr.getD a 0 == 0 then arr.setIfInBounds a c else arr) := ⟨_, rfl⟩
    have hstep : (a :: l).foldl numberStep (arr, c) = l.foldl numberStep (arr', c + 1) := by
      rw [harr']; rfl
    have hsz : arr'.size = arr.size := by
      rw [harr']
      by_cases h0 : (arr.getD a 0 == 0) = true
      · rw [if_pos h0, Array.size_setIfInBounds]
      · rw [if_neg h0]
    have hb' : ∀ x ∈ l, x < arr'.size := fun x hx => hsz ▸ hb x (List.mem_cons_of_mem a hx)
    have ih := numberStep_foldl v l arr' (c + 1) (Nat.succ_pos c) hb'
    -- the value of `arr'` at `v`
    have hval : arr'.getD v 0 = if arr.getD a 0 = 0 ∧ a = v then c else arr.getD v 0 := by
      rw [harr']
      by_cases h0 : arr.getD a 0 = 0
      · have h0' : (arr.getD a 0 == 0) = true := by rw [h0]; rfl
        rw [if_pos h0', getD_setIfInBounds]
        by_cases hav : a = v
        · rw [if_pos ⟨hav, ha⟩, if_pos ⟨h0, hav⟩]
        · rw [if_neg (fun h => hav h.1), if_neg (fun h => hav h.2)]
      · have h0' : ¬(arr.getD a 0 == 0) = true := fun h => h0 (by simpa using h)
        rw [if_neg h0', if_neg (fun h => h0 h.1)]
    rw [hstep, ih, hval]
    have hc0 : ¬c = 0 := by omega
    by_cases hv : arr.getD v 0 = 0
    · by_cases hav : a = v
      · subst hav
        simp [hv, hc0, -Array.getD_eq_getD_getElem?]
      · have hva : ¬v = a := fun e => hav e.symm
        by_cases hvl : v ∈ l
        · simp [hv, hav, hva, hvl, idxOf_cons_ne l hav, -Array.getD_eq_getD_getElem?]
          omega
        · simp [hv, hav, hva, hvl, -Array.getD_eq_getD_getElem?]
    · have e : ¬(arr.getD a 0 = 0 ∧ a = v) := fun h => hv (h.2 ▸ h.1)
      rw [if_neg e, if_pos hv, if_pos hv]

/-- H `Dimacs.lean:77`. -/
theorem numberMap_getD {l : List Nat} {v : Nat} (h : v ∈ l) :
    (numberMap l).getD v 0 = l.idxOf v + 1 := by
  have hb : ∀ x ∈ l, x < (Array.replicate (l.foldl max 0 + 1) 0).size := by
    intro x hx
    simp only [Array.size_replicate]
    exact Nat.lt_succ_of_le ((le_foldl_max l 0).2 x hx)
  have := numberStep_foldl v l _ 1 Nat.one_pos hb
  rw [getD_replicate] at this
  simp only [numberMap, this, ne_eq, not_true_eq_false, if_false, if_pos h]
  omega

/-- Recover a code from its number (H `Dimacs.lean:85`). -/
def decode (l : List Nat) (n : Nat) : Nat := l.getD (n - 1) 0

/-- H `Dimacs.lean:87`. -/
theorem decode_numberMap {l : List Nat} {v : Nat} (h : v ∈ l) :
    decode l ((numberMap l).getD v 0) = v := by
  rw [numberMap_getD h, decode, Nat.add_sub_cancel, List.getD_eq_getElem?_getD,
    List.getElem?_eq_getElem (List.idxOf_lt_length_of_mem h), Option.getD_some]
  exact getElem_idxOf _

theorem numberMap_getD_le {l : List Nat} {v : Nat} (h : v ∈ l) :
    1 ≤ (numberMap l).getD v 0 ∧ (numberMap l).getD v 0 ≤ l.length := by
  rw [numberMap_getD h]
  have := List.idxOf_lt_length_of_mem h
  omega

/-! ### Keeping the first occurrence of each code -/

/-- Skip `x` if it was seen; otherwise mark it and prepend it to the (reversed) output. -/
def dedupStep {α : Type} (key : α → Nat) (st : Array Bool × List α) (x : α) : Array Bool × List α :=
  if st.1.getD (key x) false then st else (st.1.setIfInBounds (key x) true, x :: st.2)

/-- `l` without repetitions (by `key`), first occurrences kept, in order. `S` bounds the keys (only the
deduplication, never the membership lemma, depends on it). -/
def dedupBy {α : Type} (key : α → Nat) (S : Nat) (l : List α) : List α :=
  (l.foldl (dedupStep key) (Array.replicate S false, [])).2.reverse

/-- Every code marked as seen is in the output. -/
def SeenInv (st : Array Bool × List Nat) : Prop := ∀ x, st.1.getD x false = true → x ∈ st.2

theorem seenInv_init (S : Nat) : SeenInv (Array.replicate S false, []) := by
  intro x hx
  rw [getD_replicate] at hx
  exact absurd hx (by decide)

theorem dedupStep_spec (st : Array Bool × List Nat) (x : Nat) (h : SeenInv st) :
    SeenInv (dedupStep id st x) ∧ x ∈ (dedupStep id st x).2 ∧ ∀ y ∈ st.2, y ∈ (dedupStep id st x).2 := by
  unfold dedupStep
  by_cases hx : st.1.getD (id x) false = true
  · simp only [hx, if_true]
    exact ⟨h, h x hx, fun _ hy => hy⟩
  · simp only [hx, Bool.false_eq_true, if_false]
    refine ⟨?_, List.mem_cons_self, fun y hy => List.mem_cons_of_mem _ hy⟩
    intro y hy
    simp only [getD_setIfInBounds] at hy
    split at hy
    · next hxy => exact hxy.1 ▸ List.mem_cons_self
    · exact List.mem_cons_of_mem _ (h y hy)

/-- Nothing is lost: every element of `l` (and of the previous output) is in the output. -/
theorem mem_dedup_foldl : ∀ (l : List Nat) (st : Array Bool × List Nat), SeenInv st →
    SeenInv (l.foldl (dedupStep id) st) ∧ (∀ y ∈ l, y ∈ (l.foldl (dedupStep id) st).2) ∧
      ∀ y ∈ st.2, y ∈ (l.foldl (dedupStep id) st).2
  | [], st, h => ⟨h, fun _ hy => absurd hy List.not_mem_nil, fun _ hy => hy⟩
  | a :: l, st, h => by
    obtain ⟨h1, h2, h3⟩ := dedupStep_spec st a h
    obtain ⟨i1, i2, i3⟩ := mem_dedup_foldl l (dedupStep id st a) h1
    refine ⟨i1, fun y hy => ?_, fun y hy => i3 y (h3 y hy)⟩
    rcases List.mem_cons.1 hy with rfl | hy
    · exact i3 _ h2
    · exact i2 y hy

end EncB
