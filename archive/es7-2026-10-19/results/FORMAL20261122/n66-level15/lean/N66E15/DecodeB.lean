import N66E15.Alloc
import N66E15.DecodeA

/-!
# N66E15.DecodeB: model transfer for the numbering (Std-only)

For any meaning `m : Atom → Bool` of the atoms, `decodeNum m : Nat → Bool` is an assignment of DIMACS variables with
`decodeNum m (num a) = m a` for **every** atom (`decodeNum_num`). Hence a structured clause list in which every
clause has a literal that agrees with `m` becomes, through `toDimacs`, a satisfied DIMACS list
(`dimacsSat_of_holds`). Soundness never depends on the numbers being Python's (ENCBLEAN D4): allocated atoms are
decoded through `EncB.decode`/`EncB.decode_numberMap`, the others through their own code (`Atom.ofCode_code`).

Proof hygiene: every lemma with arithmetic is proved for a variable allocation list `L` and instantiated at
`pyAlloc ()` by substitution only. Arithmetic over `nAlloc`/`pyMap` itself makes Lean evaluate the 1.65M-entry list:
`omega` with `pyMap.getD a.code 0` in context (scratch W7, 1.9 GB in 4 s), and the kernel's Nat extension on
`nAlloc + 1` ("deep recursion", 3.49 GB, build8).
-/

namespace N66E15
open Atom

theorem code_injective : Function.Injective Atom.code := fun a b h => by
  rw [← ofCode_code a, ← ofCode_code b, h]

theorem pyMap_eq : pyMap = EncB.numberMap (pyAlloc ()) := by unfold pyMap; rfl
theorem nAlloc_eq : nAlloc = (pyAlloc ()).length := by unfold nAlloc; rfl

/-- A code outside the list has no number (entry 0). -/
theorem numberMap_getD_of_not_mem {l : List Nat} {v : Nat} (h : v ∉ l) : (EncB.numberMap l).getD v 0 = 0 := by
  have hb : ∀ x ∈ l, x < (Array.replicate (l.foldl max 0 + 1) 0).size := by
    intro x hx
    simp only [Array.size_replicate]
    exact Nat.lt_succ_of_le ((EncB.le_foldl_max l 0).2 x hx)
  have := EncB.numberStep_foldl v l _ 1 Nat.one_pos hb
  rw [EncB.getD_replicate] at this
  simp only [EncB.numberMap, this, ne_eq, not_true_eq_false, if_false, if_neg h]

/-! ### Generic in the allocation list `L` -/

/-- The assignment induced by a meaning `m`, for the numbering `numWith (numberMap L) L.length`. -/
def decodeWith (L : List Nat) (m : Atom → Bool) (v : Nat) : Bool :=
  if 1 ≤ v ∧ v ≤ L.length then m (ofCode (EncB.decode L v)) else m (ofCode (v - (L.length + 1)))

theorem decodeWith_numWith (L : List Nat) (m : Atom → Bool) (a : Atom) :
    decodeWith L m (numWith (EncB.numberMap L) L.length a) = m a := by
  by_cases ha : a.code ∈ L
  · have hm := EncB.numberMap_getD ha
    have hle := EncB.numberMap_getD_le ha
    have hdec := EncB.decode_numberMap ha
    have hnum : numWith (EncB.numberMap L) L.length a = (EncB.numberMap L).getD a.code 0 := by
      simp only [numWith, hm, Nat.add_one_ne_zero, if_false]
    rw [hnum, decodeWith, if_pos hle, hdec, ofCode_code]
  · have h0 := numberMap_getD_of_not_mem ha
    have hnum : numWith (EncB.numberMap L) L.length a = L.length + 1 + a.code := by
      simp only [numWith, h0, if_true]
    have hout : ¬ (1 ≤ L.length + 1 + a.code ∧ L.length + 1 + a.code ≤ L.length) := by omega
    rw [hnum, decodeWith, if_neg hout, Nat.add_sub_cancel_left, ofCode_code]

theorem numWith_pos (L : List Nat) (a : Atom) : 0 < numWith (EncB.numberMap L) L.length a := by
  unfold numWith
  by_cases h : (EncB.numberMap L).getD a.code 0 = 0
  · simp only [h, if_true]; omega
  · simp only [h, if_false]; omega

/-! ### The instance `L = pyAlloc ()` (by substitution only) -/

/-- The assignment of DIMACS variables induced by a meaning of the atoms. -/
def decodeNum (m : Atom → Bool) : Nat → Bool := decodeWith (pyAlloc ()) m

theorem num_eq (a : Atom) : num a = numWith (EncB.numberMap (pyAlloc ())) (pyAlloc ()).length a := by
  unfold num
  rw [pyMap_eq, nAlloc_eq]

/-- **Model transfer for one atom.** -/
theorem decodeNum_num (m : Atom → Bool) (a : Atom) : decodeNum m (num a) = m a := by
  rw [num_eq]
  exact decodeWith_numWith (pyAlloc ()) m a

theorem num_pos (a : Atom) : 0 < num a := by
  rw [num_eq]
  exact numWith_pos (pyAlloc ()) a

/-- Generic: a positive DIMACS literal `k > 0`. -/
theorem litSat_pos (ν : Nat → Bool) (k : Nat) (hk : 0 < k) : EncB.LitSat ν (k : Int) ↔ ν k = true := by
  simp only [EncB.LitSat, Int.natAbs_natCast]
  constructor
  · rintro (⟨_, h⟩ | ⟨h, _⟩)
    · exact h
    · omega
  · intro h; exact Or.inl ⟨by omega, h⟩

/-- Generic: a negative DIMACS literal `-k`, `k > 0`. -/
theorem litSat_neg' (ν : Nat → Bool) (k : Nat) (hk : 0 < k) : EncB.LitSat ν (-(k : Int)) ↔ ν k = false := by
  simp only [EncB.LitSat, Int.natAbs_neg, Int.natAbs_natCast]
  constructor
  · rintro (⟨h, _⟩ | ⟨_, h⟩)
    · omega
    · exact h
  · intro h; exact Or.inr ⟨by omega, h⟩

/-- A structured literal agrees with the meaning iff its DIMACS literal holds. -/
theorem litSat_iff (m : Atom → Bool) (l : SLit) : EncB.LitSat (decodeNum m) (litInt l) ↔ m l.2 = l.1 := by
  obtain ⟨b, a⟩ := l
  cases b with
  | true =>
    simp only [litInt, if_true]
    rw [litSat_pos _ _ (num_pos a), decodeNum_num]
  | false =>
    simp only [litInt, Bool.false_eq_true, if_false]
    rw [litSat_neg' _ _ (num_pos a), decodeNum_num]

/-- **Model transfer for clause lists.** -/
theorem dimacsSat_of_holds (m : Atom → Bool) (F : List (List SLit))
    (h : ∀ cl ∈ F, ∃ l ∈ cl, m l.2 = l.1) : EncB.DimacsSat (F.map toDimacs) (decodeNum m) := by
  intro cl hcl
  obtain ⟨s, hs, rfl⟩ := List.mem_map.1 hcl
  obtain ⟨l, hl, hm⟩ := h s hs
  exact ⟨litInt l, List.mem_map_of_mem hl, (litSat_iff m l).2 hm⟩

end N66E15

#print axioms N66E15.ofCode_code
#print axioms N66E15.decodeNum_num
#print axioms N66E15.dimacsSat_of_holds
