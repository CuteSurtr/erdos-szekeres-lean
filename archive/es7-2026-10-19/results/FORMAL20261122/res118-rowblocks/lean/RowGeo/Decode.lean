import RowEnc.Enc

/-!
# RowGeo.Decode: model transfer through the numbering, and the meaning of `finish` (core only)

* `ofCode` inverts `Atm.code` up to `Atm.norm` (indices mod 16, thresholds mod 8): `ofCode_code`.
* For any meaning `m : Atm → Bool`, `decodeWith L m` is a DIMACS assignment with
  `decodeWith L m (numWith (numberMap L) L.length a) = m a.norm` for **every** atom (`decodeWith_numWith`; the
  n66enc `DecodeB` pattern over ENCBLEAN's `EncB.numberMap`). No property of the numbering is assumed.
* `finish_sat`: if a raw clause has a literal that holds (`LSem m`), the clause `finish` makes of it (if any) has a
  literal that holds under `decodeWith L m`. `rowCnf_sat`: the same for the whole CNF.
-/

namespace RowGeo
open RowEnc

def _root_.RowEnc.Atm.norm : Atm → Atm
  | .bef i j => .bef (i % 16) (j % 16)
  | .cap i j t => .cap (i % 16) (j % 16) (t % 8)
  | .cup i j t => .cup (i % 16) (j % 16) (t % 8)
  | .ori i j l => .ori (i % 16) (j % 16) (l % 16)
  | .cvx i j l m => .cvx (i % 16) (j % 16) (l % 16) (m % 16)

def ofCode (c : Nat) : Atm :=
  if c < 256 then .bef (c / 16) (c % 16)
  else if c < 2304 then .cap ((c - 256) / 8 / 16) ((c - 256) / 8 % 16) ((c - 256) % 8)
  else if c < 4352 then .cup ((c - 2304) / 8 / 16) ((c - 2304) / 8 % 16) ((c - 2304) % 8)
  else if c < 8448 then .ori ((c - 4352) / 16 / 16) ((c - 4352) / 16 % 16) ((c - 4352) % 16)
  else .cvx ((c - 8448) / 16 / 16 / 16) ((c - 8448) / 16 / 16 % 16) ((c - 8448) / 16 % 16) ((c - 8448) % 16)

set_option maxRecDepth 8000 in
theorem ofCode_code (a : Atm) : ofCode a.code = a.norm := by
  cases a with
  | bef i j =>
    simp only [Atm.code, ofCode, Atm.norm]
    rw [if_pos (by omega)]
    simp only [Atm.bef.injEq]
    refine ⟨?_, ?_⟩ <;> omega
  | cap i j t =>
    simp only [Atm.code, ofCode, Atm.norm]
    rw [if_neg (by omega), if_pos (by omega)]
    simp only [Atm.cap.injEq]
    refine ⟨?_, ?_, ?_⟩ <;> omega
  | cup i j t =>
    simp only [Atm.code, ofCode, Atm.norm]
    rw [if_neg (by omega), if_neg (by omega), if_pos (by omega)]
    simp only [Atm.cup.injEq]
    refine ⟨?_, ?_, ?_⟩ <;> omega
  | ori i j l =>
    simp only [Atm.code, ofCode, Atm.norm]
    rw [if_neg (by omega), if_neg (by omega), if_neg (by omega), if_pos (by omega)]
    simp only [Atm.ori.injEq]
    refine ⟨?_, ?_, ?_⟩ <;> omega
  | cvx i j l m =>
    simp only [Atm.code, ofCode, Atm.norm]
    rw [if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega)]
    simp only [Atm.cvx.injEq]
    refine ⟨?_, ?_, ?_, ?_⟩ <;> omega

theorem norm_norm (a : Atm) : a.norm.norm = a.norm := by
  cases a <;> simp only [Atm.norm, Nat.mod_mod]

/-- A code outside the list has no number (entry 0). -/
theorem numberMap_getD_of_not_mem {l : List Nat} {v : Nat} (h : v ∉ l) : (EncB.numberMap l).getD v 0 = 0 := by
  have hb : ∀ x ∈ l, x < (Array.replicate (l.foldl max 0 + 1) 0).size := by
    intro x hx
    simp only [Array.size_replicate]
    exact Nat.lt_succ_of_le ((EncB.le_foldl_max l 0).2 x hx)
  have := EncB.numberStep_foldl v l _ 1 Nat.one_pos hb
  rw [EncB.getD_replicate] at this
  simp only [EncB.numberMap, this, ne_eq, not_true_eq_false, if_false, if_neg h]

/-- The assignment induced by a meaning `m`, for the numbering `numWith (numberMap L) L.length`. -/
def decodeWith (L : List Nat) (m : Atm → Bool) (v : Nat) : Bool :=
  if 1 ≤ v ∧ v ≤ L.length then m (ofCode (EncB.decode L v)) else m (ofCode (v - (L.length + 1)))

theorem decodeWith_numWith (L : List Nat) (m : Atm → Bool) (a : Atm) :
    decodeWith L m (numWith (EncB.numberMap L) L.length a) = m a.norm := by
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

theorem numWith_pos (M : Array Nat) (N : Nat) (a : Atm) : 0 < numWith M N a := by
  unfold numWith
  by_cases h : M.getD a.code 0 = 0
  · simp only [h, if_true]; omega
  · simp only [h, if_false]; omega

theorem litSat_pos (ν : Nat → Bool) (k : Nat) (hk : 0 < k) : EncB.LitSat ν (k : Int) ↔ ν k = true := by
  simp only [EncB.LitSat, Int.natAbs_natCast]
  constructor
  · rintro (⟨_, h⟩ | ⟨h, _⟩)
    · exact h
    · omega
  · intro h; exact Or.inl ⟨by omega, h⟩

theorem litSat_neg' (ν : Nat → Bool) (k : Nat) (hk : 0 < k) : EncB.LitSat ν (-(k : Int)) ↔ ν k = false := by
  simp only [EncB.LitSat, Int.natAbs_neg, Int.natAbs_natCast]
  constructor
  · rintro (⟨h, _⟩ | ⟨_, h⟩)
    · omega
    · exact h
  · intro h; exact Or.inr ⟨by omega, h⟩

/-! ## `finish` -/

/-- A literal holds for the meaning `m` (atoms are read through `norm`). -/
def LSem (m : Atm → Bool) : Lit → Prop
  | .const b => b = true
  | .atom a b => m a.norm = b

theorem mem_dedupAdj : ∀ {l : List Int} {x : Int}, x ∈ l → x ∈ dedupAdj l
  | [], _, h => h
  | [_], _, h => h
  | a :: b :: t, x, h => by
    have ih : x ∈ b :: t → x ∈ dedupAdj (b :: t) := fun hx => mem_dedupAdj hx
    by_cases hab : a = b
    · simp only [dedupAdj, if_pos hab]
      rcases List.mem_cons.1 h with rfl | h
      · exact ih (hab ▸ List.mem_cons_self)
      · exact ih h
    · simp only [dedupAdj, if_neg hab]
      rcases List.mem_cons.1 h with rfl | h
      · exact List.mem_cons_self
      · exact List.mem_cons_of_mem _ (ih h)

theorem finish_sat (L : List Nat) (m : Atm → Bool) (cl : List Lit) (xs : List Int)
    (hf : finish (EncB.numberMap L) L.length cl = some xs) (hw : ∃ e ∈ cl, LSem m e) :
    ∃ x ∈ xs, EncB.LitSat (decodeWith L m) x := by
  obtain ⟨e, he, hs⟩ := hw
  unfold finish at hf
  by_cases h1 : cl.any Lit.isTrue = true
  · rw [if_pos h1] at hf; exact absurd hf (by simp)
  rw [if_neg h1] at hf
  cases e with
  | const b =>
    exact absurd (List.any_eq_true.2 ⟨.const b, he, by simpa [Lit.isTrue, LSem] using hs⟩) h1
  | atom a b =>
    simp only at hf
    split at hf
    · exact absurd hf (by simp)
    · have hx : (if b then (numWith (EncB.numberMap L) L.length a : Int)
          else -(numWith (EncB.numberMap L) L.length a : Int)) ∈
          cl.filterMap (Lit.toInt (EncB.numberMap L) L.length) :=
        List.mem_filterMap.2 ⟨.atom a b, he, rfl⟩
      simp only [Option.some.injEq] at hf
      refine ⟨_, hf ▸ mem_dedupAdj (List.mem_mergeSort.2 hx), ?_⟩
      have hp := numWith_pos (EncB.numberMap L) L.length a
      have hd := decodeWith_numWith L m a
      simp only [LSem] at hs
      cases b with
      | true => simp only [if_true]; rw [litSat_pos _ _ hp, hd, hs]
      | false => simp only [Bool.false_eq_true, if_false]; rw [litSat_neg' _ _ hp, hd, hs]

/-- **Model transfer for the whole CNF.** -/
theorem rowCnf_sat (S : List Nat) (m : Atm → Bool) (h : ∀ cl ∈ rawClauses S, ∃ e ∈ cl, LSem m e) :
    EncB.DimacsSat (rowCnf S) (decodeWith (allocCodes S.length) m) := by
  intro c hc
  unfold rowCnf at hc
  obtain ⟨cl, hcl, hfin⟩ := List.mem_filterMap.1 hc
  exact finish_sat _ m cl c hfin (h cl hcl)

end RowGeo
