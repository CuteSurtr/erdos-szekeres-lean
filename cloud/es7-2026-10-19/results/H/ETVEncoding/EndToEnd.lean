import ETVEncoding.Kernel
import ETVEncoding.Rup

/-!
# End-to-end test on small instances

Each CNF below is produced by `lake exe trackb_dimacs` (byte-identical to `gen_cnf.py`), solved
by CaDiCaL with `--lrat --no-binary`, and converted by `scripts/lrat_to_lean.py`. Three
facts are then checked inside the kernel with `decide +kernel` (no `native_decide`, no new
axiom):

* `dimacsBSpec … = …Cnf`: the Lean generator produces exactly these clauses;
* `∀ p ∈ …Start, p.2 ∈ …Cnf`: the clauses the proof starts from are clauses of the file;
* `Rup.run …Start …Proof = true`: the verified RUP checker of `ETVEncoding.Rup` accepts.

With the soundness theorems this proves the classical value `ES(4) ≤ 5` through the
pipeline (encoding, `--hull`, `--mirror`) that an ES(7) certificate for `n33k7hm.cnf` would go
through. `ES(5) ≤ 9` the same way is in `ETVEncoding.EndToEnd9` (not built by default).
-/

namespace ETV

open ErdosSzekeres

set_option maxHeartbeats 0 in
def n5k4Cnf : List (List ℤ) := [
  [-1, 2, -4],
  [1, -2, 4],
  [-1, 2, -7],
  [1, -2, 7],
  [-1, 4, -7],
  [1, -4, 7],
  [-2, 4, -7],
  [2, -4, 7],
  [-1, 3, -5],
  [1, -3, 5],
  [-1, 3, -8],
  [1, -3, 8],
  [-1, 5, -8],
  [1, -5, 8],
  [-3, 5, -8],
  [3, -5, 8],
  [-2, 3, -6],
  [2, -3, 6],
  [-2, 3, -9],
  [2, -3, 9],
  [-2, 6, -9],
  [2, -6, 9],
  [-3, 6, -9],
  [3, -6, 9],
  [-4, 5, -6],
  [4, -5, 6],
  [-4, 5, -10],
  [4, -5, 10],
  [-4, 6, -10],
  [4, -6, 10],
  [-5, 6, -10],
  [5, -6, 10],
  [-7, 8, -9],
  [7, -8, 9],
  [-7, 8, -10],
  [7, -8, 10],
  [-7, 9, -10],
  [7, -9, 10],
  [-8, 9, -10],
  [8, -9, 10],
  [1, 11],
  [2, 12],
  [3, 13],
  [4, 14],
  [5, 15],
  [6, 16],
  [7, 17],
  [8, 18],
  [9, 19],
  [10, 20],
  [-11, 7],
  [-11, 8],
  [-12, 9],
  [-14, 10],
  [-17, 10],
  [-11, 21],
  [-12, 22],
  [-13, 23],
  [-14, 22],
  [-15, 23],
  [-16, 23],
  [-17, 24],
  [-18, 25],
  [-19, 25],
  [-20, 26],
  [-1, 27],
  [-2, 28],
  [-3, 29],
  [-4, 30],
  [-5, 31],
  [-6, 32],
  [-7, 33],
  [-8, 34],
  [-9, 35],
  [-10, 36],
  [-27, -7],
  [-27, -8],
  [-28, -9],
  [-30, -10],
  [-33, -10],
  [-27, 37],
  [-28, 38],
  [-29, 39],
  [-30, 38],
  [-31, 39],
  [-32, 39],
  [-33, 40],
  [-34, 41],
  [-35, 41],
  [-36, 42],
  [-21, -37],
  [-22, -38],
  [-23, -39],
  [-24, -40],
  [-25, -41],
  [-26, -42]
]

set_option maxHeartbeats 0 in
def n5k4Start : List (ℕ × List ℤ) := [
  (41, [1, 11]),
  (42, [2, 12]),
  (44, [4, 14]),
  (47, [7, 17]),
  (48, [8, 18]),
  (49, [9, 19]),
  (51, [-11, 7]),
  (52, [-11, 8]),
  (53, [-12, 9]),
  (54, [-14, 10]),
  (55, [-17, 10]),
  (57, [-12, 22]),
  (59, [-14, 22]),
  (62, [-17, 24]),
  (63, [-18, 25]),
  (64, [-19, 25]),
  (65, [-20, 26]),
  (66, [-1, 27]),
  (67, [-2, 28]),
  (69, [-4, 30]),
  (72, [-7, 33]),
  (73, [-8, 34]),
  (74, [-9, 35]),
  (75, [-10, 36]),
  (76, [-27, -7]),
  (77, [-27, -8]),
  (78, [-28, -9]),
  (79, [-30, -10]),
  (80, [-33, -10]),
  (81, [-27, 37]),
  (82, [-28, 38]),
  (84, [-30, 38]),
  (88, [-34, 41]),
  (89, [-35, 41]),
  (90, [-36, 42]),
  (91, [-21, -37]),
  (92, [-22, -38]),
  (94, [-24, -40]),
  (95, [-25, -41]),
  (96, [-26, -42])
]

set_option maxHeartbeats 0 in
def n5k4Proof : List Rup.Step := [
  .add 97 [-11] [51, 52, 72, 73, 80, 88, 54, 95, 44, 64, 69, 49, 84, 78, 92, 67, 57, 42],
  .add 98 [1] [97, 41],
  .add 99 [27] [98, 66],
  .add 100 [-7] [99, 76],
  .add 101 [-8] [99, 77],
  .add 102 [37] [99, 81],
  .add 103 [17] [100, 47],
  .add 104 [18] [101, 48],
  .add 105 [-21] [102, 91],
  .add 106 [10] [103, 55],
  .add 107 [24] [103, 62],
  .add 108 [25] [104, 63],
  .add 109 [36] [106, 75],
  .add 110 [-30] [106, 79],
  .add 111 [-33] [106, 80],
  .add 112 [-40] [107, 94],
  .add 113 [-41] [108, 95],
  .add 114 [42] [109, 90],
  .add 115 [-4] [110, 69],
  .add 116 [-34] [113, 88],
  .add 117 [-35] [113, 89],
  .add 118 [-26] [114, 96],
  .add 119 [14] [115, 44],
  .add 120 [-9] [117, 74],
  .add 121 [-20] [118, 65],
  .add 122 [22] [119, 59],
  .add 123 [19] [120, 49],
  .add 124 [-12] [120, 53],
  .add 125 [-38] [122, 92],
  .add 126 [2] [124, 42],
  .add 127 [-28] [125, 82],
  .add 128 [] [126, 127, 67]
]

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
theorem n5k4_cnf : dimacsBSpec 5 4 false false false true = n5k4Cnf := by
  decide +kernel

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
theorem n5k4_start : ∀ p ∈ n5k4Start, p.2 ∈ n5k4Cnf := by
  decide +kernel

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
theorem n5k4_run : Rup.run n5k4Start n5k4Proof = true := by
  decide +kernel

/-- `gen_cnf.py 5 4 ` is unsatisfiable. -/
theorem n5k4_unsat : ¬DimacsSatisfiable (dimacsB 5 4 false false false true) := by
  rw [dimacsB_eq_spec (by norm_num), n5k4_cnf]
  exact Rup.not_dimacsSatisfiable_of_run n5k4_start n5k4_run

set_option maxHeartbeats 0 in
def n5k4hmCnf : List (List ℤ) := [
  [-1, 2, -4],
  [1, -2, 4],
  [-1, 2, -7],
  [1, -2, 7],
  [-1, 4, -7],
  [1, -4, 7],
  [-2, 4, -7],
  [2, -4, 7],
  [-1, 3, -5],
  [1, -3, 5],
  [-1, 3, -8],
  [1, -3, 8],
  [-1, 5, -8],
  [1, -5, 8],
  [-3, 5, -8],
  [3, -5, 8],
  [-2, 3, -6],
  [2, -3, 6],
  [-2, 3, -9],
  [2, -3, 9],
  [-2, 6, -9],
  [2, -6, 9],
  [-3, 6, -9],
  [3, -6, 9],
  [-4, 5, -6],
  [4, -5, 6],
  [-4, 5, -10],
  [4, -5, 10],
  [-4, 6, -10],
  [4, -6, 10],
  [-5, 6, -10],
  [5, -6, 10],
  [-7, 8, -9],
  [7, -8, 9],
  [-7, 8, -10],
  [7, -8, 10],
  [-7, 9, -10],
  [7, -9, 10],
  [-8, 9, -10],
  [8, -9, 10],
  [1, 11],
  [2, 12],
  [3, 13],
  [4, 14],
  [5, 15],
  [6, 16],
  [7, 17],
  [8, 18],
  [9, 19],
  [10, 20],
  [-11, 7],
  [-11, 8],
  [-12, 9],
  [-14, 10],
  [-17, 10],
  [-11, 21],
  [-12, 22],
  [-13, 23],
  [-14, 22],
  [-15, 23],
  [-16, 23],
  [-17, 24],
  [-18, 25],
  [-19, 25],
  [-20, 26],
  [-1, 27],
  [-2, 28],
  [-3, 29],
  [-4, 30],
  [-5, 31],
  [-6, 32],
  [-7, 33],
  [-8, 34],
  [-9, 35],
  [-10, 36],
  [-27, -7],
  [-27, -8],
  [-28, -9],
  [-30, -10],
  [-33, -10],
  [-27, 37],
  [-28, 38],
  [-29, 39],
  [-30, 38],
  [-31, 39],
  [-32, 39],
  [-33, 40],
  [-34, 41],
  [-35, 41],
  [-36, 42],
  [-21, -37],
  [-22, -38],
  [-23, -39],
  [-24, -40],
  [-25, -41],
  [-26, -42],
  [1],
  [2],
  [3],
  [4],
  [5],
  [6]
]

set_option maxHeartbeats 0 in
def n5k4hmStart : List (ℕ × List ℤ) := [
  (42, [2, 12]),
  (44, [4, 14]),
  (47, [7, 17]),
  (48, [8, 18]),
  (49, [9, 19]),
  (51, [-11, 7]),
  (53, [-12, 9]),
  (55, [-17, 10]),
  (59, [-14, 22]),
  (62, [-17, 24]),
  (63, [-18, 25]),
  (65, [-20, 26]),
  (66, [-1, 27]),
  (67, [-2, 28]),
  (69, [-4, 30]),
  (74, [-9, 35]),
  (75, [-10, 36]),
  (76, [-27, -7]),
  (77, [-27, -8]),
  (79, [-30, -10]),
  (80, [-33, -10]),
  (81, [-27, 37]),
  (82, [-28, 38]),
  (88, [-34, 41]),
  (89, [-35, 41]),
  (90, [-36, 42]),
  (91, [-21, -37]),
  (92, [-22, -38]),
  (94, [-24, -40]),
  (95, [-25, -41]),
  (96, [-26, -42]),
  (97, [1])
]

set_option maxHeartbeats 0 in
def n5k4hmProof : List Rup.Step := [
  .add 103 [27] [97, 66],
  .add 104 [-7] [103, 76],
  .add 105 [-8] [103, 77],
  .add 106 [37] [103, 81],
  .add 107 [17] [104, 47],
  .add 108 [-11] [104, 51],
  .add 109 [18] [105, 48],
  .add 110 [-21] [106, 91],
  .add 111 [10] [107, 55],
  .add 112 [24] [107, 62],
  .add 113 [25] [109, 63],
  .add 114 [36] [111, 75],
  .add 115 [-30] [111, 79],
  .add 116 [-33] [111, 80],
  .add 117 [-40] [112, 94],
  .add 118 [-41] [113, 95],
  .add 119 [42] [114, 90],
  .add 120 [-4] [115, 69],
  .add 121 [-34] [118, 88],
  .add 122 [-35] [118, 89],
  .add 123 [-26] [119, 96],
  .add 124 [14] [120, 44],
  .add 125 [-9] [122, 74],
  .add 126 [-20] [123, 65],
  .add 127 [22] [124, 59],
  .add 128 [19] [125, 49],
  .add 129 [-12] [125, 53],
  .add 130 [-38] [127, 92],
  .add 131 [2] [129, 42],
  .add 132 [-28] [130, 82],
  .add 133 [] [131, 132, 67]
]

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
theorem n5k4hm_cnf : dimacsBSpec 5 4 true true false true = n5k4hmCnf := by
  decide +kernel

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
theorem n5k4hm_start : ∀ p ∈ n5k4hmStart, p.2 ∈ n5k4hmCnf := by
  decide +kernel

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
theorem n5k4hm_run : Rup.run n5k4hmStart n5k4hmProof = true := by
  decide +kernel

/-- `gen_cnf.py 5 4 --hull --mirror` is unsatisfiable. -/
theorem n5k4hm_unsat : ¬DimacsSatisfiable (dimacsB 5 4 true true false true) := by
  rw [dimacsB_eq_spec (by norm_num), n5k4hm_cnf]
  exact Rup.not_dimacsSatisfiable_of_run n5k4hm_start n5k4hm_run

/-- `ES(4) ≤ 5` through the plain track-B encoding. -/
theorem forces_quadrilateral_5 : ForcesConvexNGon 5 4 :=
  forcesConvexNGon_of_unsat_trackB n5k4_unsat (by norm_num) (by norm_num)

/-- `ES(4) ≤ 5` through the `--hull --mirror` encoding. -/
theorem forces_quadrilateral_5_hm : ForcesConvexNGon 5 4 :=
  forcesConvexNGon_of_unsat_hull n5k4hm_unsat (by norm_num) (by norm_num)

end ETV
