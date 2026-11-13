import EncB.SoundOlit
import EncB.SortLemmas

/-! U3 (`EncB/SoundAng.lean`) starting point (compiled by the M3 judge): the entries of `angOuts` for even m. -/

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
  simp only [Bool.false_eq_true, if_false, bitTuples, List.map_cons, List.map_nil, List.mem_singleton] at hx
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
  simp only [Bool.false_eq_true, if_false, bitTuples, List.map_cons, List.map_nil, List.mem_singleton]
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

end EncB.Ang
