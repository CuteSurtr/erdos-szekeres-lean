import EncB.SoundOrbit
import EncB.SoundChain
import EncB.SoundAng
import EncB.SoundRules
import EncB.SoundWord

/-!
# M3: `encB_satisfiable` (combinatorial soundness of encoder B, Std-only)

Every clause of `genCoded m K t` (Coded.lean:281-285) holds under the intended assignment `Model.τ` of a `Model`
(`EncB/Model.lean`), family by family:

| family (Coded) | gen_b2.py | theorem | file |
|---|---|---|---|
| ψ-order transitivity `transCl` | 79-81 | `transCl_sound` | SoundOrbit.lean |
| angular units / conditional clauses `angClOf (angOutsC m t c).1`, `c ∈ orbList m t` | 83-141 | `angCl_sound` (with `orbListSpec`, `patternSpec_of wordSpec`) | SoundAng, SoundOrbit, SoundRules, SoundWord |
| nesting units `nestLits` | 143-150 | `nestLits_sound` | SoundOrbit.lean |
| chains `chainCl m K t isF i`, any filter `isF` | 154-190 | `chainCl_sound` | SoundChain.lean |

`dimacsSatisfiable_of_holds` (Coded.lean:404) transfers this to the DIMACS list `encB m K t`. Even `m` only
(`heven`); `hm : 2 ≤ m` makes `(i, 1)` a valid label in the nesting family. Nothing here evaluates `encB 6 8 11`.
-/

namespace EncB

theorem genCoded_sound {m K t : Nat} (heven : m % 2 = 0) (hm : 2 ≤ m) (M : Model m K t) :
    ∀ cl ∈ genCoded m K t, ∃ x ∈ cl, CodeLitHolds M.τc x := by
  intro cl hcl
  simp only [genCoded, List.mem_append, List.mem_flatMap, List.mem_map] at hcl
  rcases hcl with ((hcl | ⟨outs, ⟨c, hc, rfl⟩, hcl⟩) | ⟨l, hl, rfl⟩) | ⟨i, hi, hcl⟩
  · exact transCl_sound M cl hcl
  · exact angCl_sound M heven (orbListSpec m t) (patternSpec_of wordSpec M) c hc cl hcl
  · exact ⟨l, List.mem_singleton_self _, nestLits_sound M hm l hl⟩
  · exact chainCl_sound M _ i hi cl hcl

/-- **M3.** The DIMACS formula `encB m K t` is satisfiable whenever a `Model m K t` exists (even `m ≥ 2`). -/
theorem encB_satisfiable {m K t : Nat} (heven : m % 2 = 0) (hm : 2 ≤ m) (M : Model m K t) :
    DimacsSatisfiable (encB m K t) :=
  dimacsSatisfiable_of_holds M.τ (genCoded_sound heven hm M)

/-- The instance of `DESIGN.md` §1.1. The side conditions are proof terms, not `decide`: `scripts/audit.sh` forbids
`decide`/`rfl`/`simp`/`omega`/`example` in any declaration that mentions `encB 6 8 11`. -/
theorem encB_satisfiable_6811 (M : Model 6 8 11) : DimacsSatisfiable (encB 6 8 11) :=
  encB_satisfiable (Nat.mul_mod_right 2 3) (Nat.le_add_left 2 4) M

/-- info: 'EncB.encB_satisfiable' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms encB_satisfiable

/-- info: 'EncB.encB_satisfiable_6811' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms encB_satisfiable_6811

end EncB
