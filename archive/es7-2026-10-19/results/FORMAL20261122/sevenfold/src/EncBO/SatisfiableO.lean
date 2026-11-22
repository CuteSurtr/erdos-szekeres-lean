import EncBO.SoundO
import EncBO.AngO

/-!
# M3 for odd `m`: `encB_satisfiable_odd` (combinatorial soundness of encoder B, Std-only)

Every clause of `genCoded m K t` (ENCBLEAN's Coded.lean) holds under the intended assignment `ModelO.τ` of a
`ModelO`, family by family:

| family (Coded) | gen_b2.py | theorem | file |
|---|---|---|---|
| ψ-order transitivity `transCl` | 79-81 | `transCl_soundO` | SoundO.lean |
| angular units / conditional clauses (odd: Y and H premises) | 83-141 | `angCl_soundO` (with ENCBLEAN's `orbListSpec`, `patternSpecO`) | AngO.lean, RulesO.lean |
| nesting units `nestLits` | 143-150 | `nestLits_soundO` | SoundO.lean |
| chains `chainCl m K t isF i`, any filter `isF` | 154-190 | `chainCl_soundO` | SoundO.lean |

ENCBLEAN's `dimacsSatisfiable_of_holds` (Coded.lean:404, generic in the assignment) transfers this to the DIMACS
list `encB m K t`. Odd `m ≥ 2` (so `m ≥ 3`); `hm : 2 ≤ m` makes `(i, 1)` a valid label in the nesting family.
Nothing here evaluates `encB 7 8 10`.
-/

namespace EncB

theorem genCoded_soundO {m K t : Nat} (hodd : m % 2 = 1) (hm : 2 ≤ m) (M : ModelO m K t) :
    ∀ cl ∈ genCoded m K t, ∃ x ∈ cl, CodeLitHolds M.τc x := by
  intro cl hcl
  simp only [genCoded, List.mem_append, List.mem_flatMap, List.mem_map] at hcl
  rcases hcl with ((hcl | ⟨outs, ⟨c, hc, rfl⟩, hcl⟩) | ⟨l, hl, rfl⟩) | ⟨i, hi, hcl⟩
  · exact transCl_soundO M cl hcl
  · exact angCl_soundO M hodd (orbListSpec m t) (patternSpecO M) c hc cl hcl
  · exact ⟨l, List.mem_singleton_self _, nestLits_soundO M hm l hl⟩
  · exact chainCl_soundO M _ i hi cl hcl

/-- **M3, odd `m`.** The DIMACS formula `encB m K t` is satisfiable whenever a `ModelO m K t` exists (odd `m ≥ 3`). -/
theorem encB_satisfiable_odd {m K t : Nat} (hodd : m % 2 = 1) (hm : 2 ≤ m) (M : ModelO m K t) :
    DimacsSatisfiable (encB m K t) :=
  dimacsSatisfiable_of_holds M.τ (genCoded_soundO hodd hm M)

/-- The numerals of the instance, kept away from any mention of `encB 7 8 10`. -/
theorem seven_odd : 7 % 2 = 1 ∧ 2 ≤ 7 := by decide

/-- The instance (7,8,10) of C7UPPER. The side conditions come from `seven_odd`; no tactic touches `encB 7 8 10`. -/
theorem encB_satisfiable_7810 (M : ModelO 7 8 10) : DimacsSatisfiable (encB 7 8 10) :=
  encB_satisfiable_odd seven_odd.1 seven_odd.2 M

/-- info: 'EncB.encB_satisfiable_odd' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms encB_satisfiable_odd

/-- info: 'EncB.encB_satisfiable_7810' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms encB_satisfiable_7810

end EncB
