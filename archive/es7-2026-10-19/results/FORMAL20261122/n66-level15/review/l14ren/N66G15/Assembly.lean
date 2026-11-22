import N66G15.Tail
import ErdosSzekeres.Omission.Realization
import LemmaZ

/-!
# N66G15.Assembly: `N66Bound 54` from the 132 verdicts, the used rows, and the named remaining facts

`n66_bound_54_of_gaps` is the end-to-end statement of the formalization **as it stands**: it is Lean-checked
modulo `CubesUnsat105` (the 132 cake_lpr verdicts, through the printer, E1-E6), `RowsValid R0_15` (the 11,884 used
rows) and the structure `Gaps`, whose fields are the facts not yet formalized (each a precise proposition, never an
axiom). Every field removed from `Gaps` by a later milestone shortens the hypothesis list; the statement is meant to
end as `n66_bound_54_of_cubes : CubesUnsat105 → RowsValid R0_15 → N66Bound 54` (DESIGN.md §1.1).
-/

namespace N66G15
open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks N66E15

/-- The N66 class: no 6-cap, no 6-cup, no convex octagon. -/
def InClass {n : ℕ} (c : Configuration n) : Prop :=
  ¬ c.HasCap 6 ∧ ¬ c.HasCup 6 ∧ ¬ HasConvexNGon 8 (Finset.univ.image c.point)

/-- **A demand-one row on `T`** (the record's claim "no set of the class occupies all states of T"): every
configuration of the class leaves some state of `T` unoccupied. -/
def RowValid (T : List (Fin 70)) : Prop :=
  ∀ n (c : Configuration n), InClass c → ∃ s ∈ T, ¬ n66Occ c.cup n s

def RowsValid (R : List (List (Fin 70))) : Prop := ∀ T ∈ R, RowValid T

/-- The transposition of states (`p2_sb.TAU`). -/
def tau (s : Fin 70) : Fin 70 := ⟨tauList.getD s.val 0 % 70, Nat.mod_lt _ (by decide)⟩

/-- LEX (p2_sb.py) for an occupancy predicate. -/
def LexOcc (x : Fin 70 → Prop) : Prop :=
  ∀ j : ℕ, ∀ p : Fin 70 × Fin 70, p ∈ sbPairs[j]? →
    (∀ t : ℕ, t < j → ∀ q : Fin 70 × Fin 70, q ∈ sbPairs[t]? → (x q.1 ↔ x q.2)) → x p.1 → x p.2

/-- **The facts not yet formalized** (DESIGN.md §4-§5), as hypotheses. -/
structure Gaps : Prop where
  /-- G3: a 5-cap and a 5-cup with common endpoints form a convex octagon. -/
  capCup55 : ∀ n (c : Configuration n), ¬ HasConvexNGon 8 (Finset.univ.image c.point) →
    ∀ p u u' q, q < n → SEPath c.cup false p u q 5 → SEPath c.cup true p u' q 5 → False
  /-- G4: the mirror image (x, y) ↦ (x, −y) is in the class and its occupancy is the τ-image. -/
  mirror : ∀ n (c : Configuration n), InClass c → ∃ c' : Configuration n, InClass c' ∧
    ∀ s, n66Occ c'.cup n s ↔ n66Occ c.cup n (tau s)
  /-- L6: an occupancy or its τ-image satisfies LEX (N66 README §6.7). -/
  lexChoice : ∀ x : Fin 70 → Prop, LexOcc x ∨ LexOcc (fun s => x (tau s))
  /-- L7: at least 56 points leave at most 14 of the states 2..69 unoccupied. -/
  holes : ∀ M : Model, 56 ≤ M.n → M.holes ≤ 14
  /-- 4.11: the first two points own states 0 and 1. -/
  fixed : ∀ M : Model, 2 ≤ M.n → M.Holds fixedUnits
  /-- 4.1-4.8: the eager families (state-dependent clauses, thresholds, transitivity, growth, chain starts, CE/UE). -/
  eager : ∀ M : Model, M.Holds (eagerStream ())
  /-- 4.9-4.10: chain steps and signotope packets. -/
  quad : ∀ M : Model, M.Holds quadStream

/-- G2: the triple colors of a configuration satisfy the packet (signotope) condition. -/
theorem signotope_of_config {n : ℕ} (c : Configuration n) :
    ∀ a b d e, a < b → b < d → d < e → e < n →
      PacketValid (c.cup a b d) (c.cup a b e) (c.cup a d e) (c.cup b d e) := by
  intro a b d e hab hbd hde hen
  have key : ∀ (i j k : ℕ) (hi : i < n) (hj : j < n) (hk : k < n),
      c.cup i j k = decide (0 < orient (c.point ⟨i, hi⟩) (c.point ⟨j, hj⟩) (c.point ⟨k, hk⟩)) := by
    intro i j k hi hj hk
    apply Bool.eq_iff_iff.2
    rw [show c.cup i j k = c.cup (⟨i, hi⟩ : Fin n) (⟨j, hj⟩ : Fin n) (⟨k, hk⟩ : Fin n) from rfl,
      Configuration.cup_true_iff]
    simp
  have hx : ∀ (i j : ℕ) (hi : i < n) (hj : j < n), i < j →
      c.point ⟨i, hi⟩ 0 < c.point ⟨j, hj⟩ 0 := fun i j hi hj h => c.xOrder h
  rw [key a b d (by omega) (by omega) (by omega), key a b e (by omega) (by omega) hen,
    key a d e (by omega) (by omega) hen, key b d e (by omega) (by omega) hen]
  exact packetValid_of_xordered _ _ _ _ (hx a b _ _ hab) (hx b d _ _ hbd) (hx d e _ _ hde)

/-- G1 + G2 (+ G3 as an argument): the `Model` of a configuration of the class. -/
noncomputable def modelOf {n : ℕ} (c : Configuration n) (hc : InClass c)
    (h55 : ∀ p u u' q, q < n → SEPath c.cup false p u q 5 → SEPath c.cup true p u' q 5 → False) : Model where
  n := n
  cup := c.cup
  noCap6 := c.avoids_of_noCap hc.1
  noCup6 := c.avoids_of_noCup hc.2.1
  signotope := signotope_of_config c
  noCapCup55 := h55

/-- **`N66Bound 54`, Lean-checked modulo `CubesUnsat105`, `RowsValid R0_15` and `Gaps`.** -/
theorem n66_bound_54_of_gaps (h : CubesUnsat105) (hR : RowsValid R0_15) (g : Gaps) : OmissionZRow.N66Bound 54 := by
  intro n c hcap hcup hoct
  by_contra hn
  have hn56 : 56 ≤ n := by omega
  have hc : InClass c := ⟨hcap, hcup, hoct⟩
  obtain ⟨c', hc', hlex⟩ : ∃ c' : Configuration n, InClass c' ∧ LexOcc (n66Occ c'.cup n) := by
    rcases g.lexChoice (n66Occ c.cup n) with hl | hl
    · exact ⟨c, hc, hl⟩
    · obtain ⟨c', hc', hocc⟩ := g.mirror n c hc
      refine ⟨c', hc', ?_⟩
      have heq : n66Occ c'.cup n = fun s => n66Occ c.cup n (tau s) := funext fun s => propext (hocc s)
      rw [heq]
      exact hl
  let M := modelOf c' hc' (g.capCup55 n c' hc'.2.2)
  have hMn : M.n = n := rfl
  apply no_model_of_cubes h M
  refine holds_baseS (g.eager M) (g.quad M) (g.fixed M (by rw [hMn]; omega)) ?_
    (holds_card M (g.holes M (by rw [hMn]; exact hn56)))
    (holds_sb M (fun j p hp hb h1 => hlex j p hp hb h1))
  intro cl hcl
  obtain ⟨T, hT, rfl⟩ := List.mem_map.1 hcl
  obtain ⟨s, hs, hno⟩ := hR T hT n c' hc'
  refine ⟨(false, Atom.sel s), List.mem_map_of_mem hs, ?_⟩
  simp only [meaning_sel, decide_eq_false_iff_not]
  exact hno

end N66G15

#print axioms N66G15.signotope_of_config
#print axioms N66G15.n66_bound_54_of_gaps
