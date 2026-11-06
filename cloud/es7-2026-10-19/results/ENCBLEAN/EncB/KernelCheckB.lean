import EncB.Gen
import EncB.Coded
import EncB.Cover

/-!
# Kernel evaluation of the twin `EncB.encB` on tiny instances, and the axiom audit of M2

The kernel (not the compiled exe) evaluates `encB` and `numVars` on (3,4,1), (3,4,2) (odd m), (6,4,1) and (4,5,1)
(even m) and compares them with the clause lists gen_b2.py writes. The first two are the literals of
`EncB/KernelCheck.lean`, where the kernel checks `gen` against them, so there kernel-evaluated `encB` = `gen` =
gen_b2.py. The (6,4,1) and (4,5,1) lists were written by gen_b2.py `3d47459a…` into scratch files whose SHA-256
equals the `ref/hashes.tsv` row (`dd42c2e8…`, `6b5cccde…`); (4,5,1) is also checked against `gen`. It also checks on
(3,4,2) that every code of `allCodes` decodes to a valid variable whose code it is (`codesDecode`).
`decide +kernel` adds no axiom. `encB 6 8 11` is never evaluated by the kernel (`DESIGN.md` D9).
-/

namespace EncB

theorem encB_3_4_1 : numVars 3 4 1 = 2 ∧ encB 3 4 1 = [[1], [2, -1]] := by
  decide +kernel

theorem encB_3_4_2 : numVars 3 4 2 = 22 ∧
    encB 3 4 2 =
      [[2], [4], [5], [1, 6], [7], [-1, 8], [9], [3], [4], [5], [10, -2], [11, -3], [12, -4], [13, -5], [14, -4], [15, -6], [16, -7], [17, -5], [18, 6], [19, -8], [20, -3], [21, 8], [-14, 6, 8], [-16, -3, 8], [-17, -6, -8], [-17, 8, -7], [-18, -4, -7], [-19, -4, -6], [-19, -6, -9], [-20, -7, 6], [-21, -5, 6], [22, -9]] := by
  decide +kernel

/-- Even m. (4,4,2), Gen's even instance in `KernelCheck.lean`, does not fit: the kernel needs more than 8 GB for
`encB 4 4 2` (`allCodes 4 4 2` alone took 28 s and 5.5 GB; its seen-array has 903 entries; see the README). (6,4,1)
has angular units and base and closing chain clauses, but no nesting. -/
theorem encB_6_4_1 : numVars 6 4 1 = 20 ∧
    encB 6 4 1 =
      [[1], [4], [5, -1], [6, -2], [7, -3], [8, -1], [9, -3], [10, -4], [11, -2], [12, 2], [13, 3], [14, -2], [15, -3], [16, 3], [17, 2], [18, -1], [19, 2], [20, 3], [-5, 2, -1], [-5, 3, -2], [-6, 3, -3], [-7, 2, 3], [-8, 3, 2], [-9, -1, -1], [-9, 2, -2], [-10, -1, -2], [-10, 2, -3], [-11, -1, -3], [-11, 3, 2], [-12, -3, -1], [-12, 2, 3], [-13, 3, 2], [-14, -2, -3], [-14, -3, -1], [-14, 3, -1], [-15, -2, -4], [-15, -3, -2], [-16, -4, -2], [-16, -2, -3], [-17, -3, 3], [-18, -3, -2], [-18, -4, -3], [-18, -2, -1], [-19, -1, 3], [-19, -3, -2], [-19, -1, -3], [-20, -2, 2], [-20, -1, -1]] := by
  decide +kernel

/-- A chain of two levels (K = 5). Every other kernel instance, here and in `KernelCheck.lean`, has K = 4, where
`rng 2 (K - 1) = [2]` is one closing level. At (4,5,1) level 2 takes the branch `lev + 1 < K - 1` of `extItems`:
6 extension clauses `[-F₂(b,c), -lab, -lt, F₃(a,b)]`, whose F₃ are the variables 8-13. Level 3 then closes on the
key set of F₃ that `levelStep` passes on: 6 clauses `[-F₃(b,c), -lab, -lt]`. The list is gen_b2.py's
(SHA-256 `6b5cccde…` = the `ref/hashes.tsv` row). -/
theorem encB_4_5_1 : numVars 4 5 1 = 13 ∧
    encB 4 5 1 =
      [[2, -1], [3, -1], [4, 1], [5, -1], [6, 1], [7, 1], [-2, 1, -1, 8], [-3, 1, 1, 9], [-4, 1, 1, 10], [-5, -1, -1, 11], [-6, -1, -1, 12], [-7, -1, 1, 13], [-11, 1, -1], [-13, 1, 1], [-9, 1, 1], [-12, -1, -1], [-8, -1, -1], [-10, -1, 1]] := by
  decide +kernel

/-- The same (4,5,1) list for M1's `gen` (Gen's own kernel instances in `KernelCheck.lean` all have K = 4). -/
theorem gen_4_5_1 : (gen 4 5 1).nv = 13 ∧ (gen 4 5 1).bad = 0 ∧ (gen 4 5 1).conflict = false ∧
    (gen 4 5 1).clauses.toList =
      [[2, -1], [3, -1], [4, 1], [5, -1], [6, 1], [7, 1], [-2, 1, -1, 8], [-3, 1, 1, 9], [-4, 1, 1, 10], [-5, -1, -1, 11], [-6, -1, -1, 12], [-7, -1, 1, 13], [-11, 1, -1], [-13, 1, 1], [-9, 1, 1], [-12, -1, -1], [-8, -1, -1], [-10, -1, 1]] := by
  decide +kernel

theorem codesDecode_3_4_2 : codesDecode 3 4 2 (allCodes 3 4 2) = true := by
  decide +kernel

/-! Axiom audit: every M2 theorem uses at most `propext`, `Classical.choice`, `Quot.sound`; no `sorryAx`, no
`Lean.ofReduceBool`. The definitions `encB` and `genCoded` use none. -/

/-- info: 'EncB.encB' does not depend on any axioms -/
#guard_msgs in #print axioms encB

/-- info: 'EncB.genCoded' does not depend on any axioms -/
#guard_msgs in #print axioms genCoded

/-- info: 'EncB.numberMap_getD' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms numberMap_getD

/-- info: 'EncB.decode_numberMap' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms decode_numberMap

/-- info: 'EncB.decodeCode_code' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in #print axioms decodeCode_code

/-- info: 'EncB.mem_allCodes' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in #print axioms mem_allCodes

/-- info: 'EncB.dimacsSat_of_holds' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms dimacsSat_of_holds

/-- info: 'EncB.dimacsSatisfiable_of_holds' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms dimacsSatisfiable_of_holds

/-- info: 'EncB.encB_wf' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms encB_wf

/-- info: 'EncB.covers_signPatterns' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms covers_signPatterns

/-- info: 'EncB.not_dimacsSatisfiable_of_cover' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in #print axioms not_dimacsSatisfiable_of_cover

/-- info: 'EncB.encB_unsat_of_cubes64' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms encB_unsat_of_cubes64

/-- info: 'EncB.encB_6_4_1' does not depend on any axioms -/
#guard_msgs in #print axioms encB_6_4_1

/-- info: 'EncB.encB_4_5_1' does not depend on any axioms -/
#guard_msgs in #print axioms encB_4_5_1

/-- info: 'EncB.gen_4_5_1' depends on axioms: [propext] -/
#guard_msgs in #print axioms gen_4_5_1

end EncB
