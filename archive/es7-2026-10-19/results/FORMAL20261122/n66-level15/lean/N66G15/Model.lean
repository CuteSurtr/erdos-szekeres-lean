import ErdosSzekeres.Omission.BalancedStates
import ErdosSzekeres.OrientationPackets
import N66E15.Bridge

/-!
# N66G15.Model: the combinatorial interface and the intended assignment (DESIGN.md §2, frozen at M0)

A `Model` is an x-ordered point set given only by the colors of its increasing triples (`cup i j k = true`:
positive orientation). Labels, states, owners and occupancy are derived with the library's `ActualRanks`
(`labels`, `column`). `Model.meaning` is the intended assignment of DESIGN.md §2.2; `no_model_of_cubes` turns the
105 verdicts (through `N66E15.base_unsat_of_cubes`) into: no `Model` satisfies every clause of `baseS R0_15`.
-/

namespace N66G15
open ErdosSzekeres ErdosSzekeres.Omission.ActualRanks N66E15

/-- A strictly increasing path of `k ≥ 2` indices from `p` ending with the pair `(u, v)`, consecutive triples of
color `color` (`true` = cup, `false` = cap). -/
inductive SEPath (cup : ℕ → ℕ → ℕ → Bool) (color : Bool) (p : ℕ) : ℕ → ℕ → ℕ → Prop
  | two {v : ℕ} : p < v → SEPath cup color p p v 2
  | step {t u v k : ℕ} : SEPath cup color p t u k → u < v → cup t u v = color → SEPath cup color p u v (k + 1)

/-- **The combinatorial interface** (DESIGN.md §2.1). -/
structure Model where
  n : ℕ
  cup : ℕ → ℕ → ℕ → Bool
  noCap6 : Avoids n cup false 6
  noCup6 : Avoids n cup true 6
  signotope : ∀ a b c d, a < b → b < c → c < d → d < n →
    PacketValid (cup a b c) (cup a b d) (cup a c d) (cup b c d)
  noCapCup55 : ∀ p u u' q, q < n → SEPath cup false p u q 5 → SEPath cup true p u' q 5 → False

/-! ## States and occupancy (from the triple colors alone) -/

/-- The state of point `v`: the column heights of its incoming state in the 4 × 4 box. -/
noncomputable def profOf (cup : ℕ → ℕ → ℕ → Bool) (v : ℕ) : Prof :=
  (column cup v 0, column cup v 1, column cup v 2, column cup v 3)

/-- The N66 state index (etv order, `N66E15.stateList`) of point `v`. -/
noncomputable def idxOf (cup : ℕ → ℕ → ℕ → Bool) (v : ℕ) : ℕ := stateList.idxOf (profOf cup v)

/-- State `s` is occupied: some point of the configuration has it. -/
def n66Occ (cup : ℕ → ℕ → ℕ → Bool) (n : ℕ) (s : Fin 70) : Prop := ∃ v < n, idxOf cup v = s.val

/-- The orientation of the points `(u, v, w)` in that order, from the color of the sorted triple and the parity of
the sorting permutation (`coupled5.orient`). -/
def ori3 (cup : ℕ → ℕ → ℕ → Bool) (u v w : ℕ) : Bool :=
  if u < v then
    if v < w then cup u v w
    else if u < w then !cup u w v
    else cup w u v
  else
    if u < w then !cup v u w
    else if v < w then cup v w u
    else !cup w v u

namespace Model
variable (M : Model)

def occ (s : Fin 70) : Prop := n66Occ M.cup M.n s

/-- The points of states `i` and `j` (in this order) exist and are in x-order. -/
def Bef (i j : Fin 70) : Prop := ∃ u v, u < v ∧ v < M.n ∧ idxOf M.cup u = i.val ∧ idxOf M.cup v = j.val

/-- The pair label of the points of states `i`, `j` (in x-order) has cap coordinate ≥ k (`cup = false`) or cup
coordinate ≥ k (`cup = true`). -/
def LabGe (cup : Bool) (i j : Fin 70) (k : ℕ) : Prop :=
  ∃ u v, u < v ∧ v < M.n ∧ ((idxOf M.cup u = i.val ∧ idxOf M.cup v = j.val) ∨
    (idxOf M.cup u = j.val ∧ idxOf M.cup v = i.val)) ∧
    k ≤ (if cup then (labels M.cup u v).2 else (labels M.cup u v).1)

/-- The points of states `i`, `j`, `k` exist and are positively oriented in that order. -/
def Ori (i j k : Fin 70) : Prop :=
  ∃ u v w, u < M.n ∧ v < M.n ∧ w < M.n ∧ idxOf M.cup u = i.val ∧ idxOf M.cup v = j.val ∧
    idxOf M.cup w = k.val ∧ ori3 M.cup u v w = true

/-- A k-path of color `color` starts at the point of state `a` and ends with the points of states `(b, c)`. -/
def Chain (color : Bool) (k : ℕ) (a b c : Fin 70) : Prop :=
  ∃ p u v, v < M.n ∧ idxOf M.cup p = a.val ∧ idxOf M.cup u = b.val ∧ idxOf M.cup v = c.val ∧
    SEPath M.cup color p u v k

/-- A 5-path of color `color` goes from the point of state `p` to the point of state `q`. -/
def End5 (color : Bool) (p q : Fin 70) : Prop :=
  ∃ x u y, y < M.n ∧ idxOf M.cup x = p.val ∧ idxOf M.cup y = q.val ∧ SEPath M.cup color x u y 5

/-- Holes among states `2..a+1` (the first `a` hole literals of the counter). -/
noncomputable def holesUpTo (a : ℕ) : ℕ := by
  classical
  exact ((List.range a).filter fun i => ¬ M.occ ⟨(i + 2) % 70, Nat.mod_lt _ (by decide)⟩).length

/-- The first `j + 1` SB pairs agree. -/
def PairsAgree (j : ℕ) : Prop := ∀ t ≤ j, ∀ p ∈ sbPairs[t]?, (M.occ p.1 ↔ M.occ p.2)

open Classical in
/-- **The intended assignment** (DESIGN.md §2.2). -/
noncomputable def meaning : Atom → Bool
  | .before i j => decide (M.Bef i j)
  | .capGe i j k => decide (M.LabGe false i j k.val)
  | .cupGe i j k => decide (M.LabGe true i j k.val)
  | .orient i j k => decide (M.Ori i j k)
  | .convex _ _ _ _ => false
  | .sel s => decide (M.occ s)
  | .chC k a b c => decide (M.Chain false k.val a b c)
  | .chU k a b c => decide (M.Chain true k.val a b c)
  | .ce p q => decide (M.End5 false p q)
  | .ue p q => decide (M.End5 true p q)
  | .cnt a j => decide (j.val ≤ M.holesUpTo a.val)
  | .sbe j => decide (M.PairsAgree j.val)

/-- Every clause of `F` has a literal that agrees with the intended assignment. -/
def Holds (F : List (List SLit)) : Prop := ∀ cl ∈ F, ∃ l ∈ cl, M.meaning l.2 = l.1

end Model

/-- **From the 105 verdicts:** no `Model` satisfies every clause of the cube-free relaxation over `R0_15`. -/
theorem no_model_of_cubes (h : CubesUnsat105) (M : Model) (hM : M.Holds (baseS R0_15)) : False :=
  base_unsat_of_cubes h ⟨_, dimacsSat_of_holds M.meaning (baseS R0_15) hM⟩

theorem holds_baseS {M : Model} {R : List (List (Fin 70))}
    (he : M.Holds (eagerStream ())) (hq : M.Holds quadStream) (hf : M.Holds fixedUnits)
    (hr : M.Holds (R.map rowClause)) (hc : M.Holds cardClauses) (hs : M.Holds sbClauses) :
    M.Holds (baseS R) := by
  intro cl hcl
  simp only [baseS, List.mem_append] at hcl
  rcases hcl with ((((h | h) | h) | h) | h) | h
  · exact he cl h
  · exact hq cl h
  · exact hf cl h
  · exact hr cl h
  · exact hc cl h
  · exact hs cl h

end N66G15

#print axioms N66G15.no_model_of_cubes
#print axioms N66G15.holds_baseS
