import EncB.Model

/-!
# M3 early-warning test (prototype, scratch): a concrete exact model at a tiny instance

Layer representatives of the SIX60 sets (`SIX60/sets/c6_60pts_{A,B,C,D}.pts`), in the Eisenstein basis `(1, ζ)`,
`ζ = e^{iπ/3}`: the point `a + bζ` is `(a, b)`, rotation by `2π/6` is `(a, b) ↦ (−b, a + b)`, and the orientation
sign is the sign of the integer determinant in this basis (the basis is positively oriented). Label `(i, k)` is
`ζ^k · rep i`; every `rep i` lies in the sector `[0, π/3)`, so `ψ_i` is its direction. The mirror image of a set is
`rep i ↦ (b, a)` (`(a, 0)` stays), i.e. `ψ_i ↦ π/3 − ψ_i`.

Everything below is evaluated by `#eval` (the compiler's IR), never by the kernel.
-/

namespace EncB.EW

abbrev E := Int × Int

def rotE (p : E) : E := (-p.2, p.1 + p.2)
def rotEn : Nat → E → E
  | 0, p => p
  | n + 1, p => rotEn n (rotE p)
def det (p q r : E) : Int := (q.1 - p.1) * (r.2 - p.2) - (q.2 - p.2) * (r.1 - p.1)

def setA : List E := [(268435456, 0), (74257719, 6629426), (65544021, 6163452), (54071730, 10588904),
  (53501118, 10593050), (43264300, 15650877), (42748054, 15582152), (29453840, 15103124), (29453745, 15103180),
  (2569808, 3435)]
def setB : List E := [(268435456, 0), (84911, 75878), (82623, 75568), (69289, 76753), (68638, 76095),
  (60816, 78578), (60324, 78009), (53911, 72346), (50938, 73485), (225, 2559)]
def setC : List E := [(1000000000000, 0), (4171582596, 4220918302), (3901289731, 4222104075),
  (3775207400, 4222708268), (2106585128, 2441364552), (1983448959, 2441678397), (1939873218, 2455394490),
  (1895765476, 2420505141), (1812312622, 2442140453), (2641721, 3611115)]
def setD : List E := [(524288, 0), (131119, 11665), (131103, 11664), (107744, 21423), (107703, 21423),
  (88128, 30720), (86762, 30677), (56942, 30072), (56913, 30089), (5569, 389)]

def mirror (reps : List E) : List E := reps.map fun p => if p.2 == 0 then p else (p.2, p.1)

section
variable (reps : List E) (m K t : Nat)

def pt (a : Pt) : E := rotEn a.2 (reps.getD a.1 (0, 0))
def chi (a b d : Pt) : Bool := decide (0 < det (pt reps a) (pt reps b) (pt reps d))
/-- `rank i` = number of layers `j < t` with `ψ_j < ψ_i`; layers `≥ t` get ranks above all of them. -/
def rank (i : Nat) : Nat :=
  if i < t then ((List.range t).filter fun j =>
    decide (0 < det (0, 0) (reps.getD j (0, 0)) (reps.getD i (0, 0)))).length
  else i + t
def psiLt (i j : Nat) : Bool := decide (rank reps t i < rank reps t j)

def labelsV : List Pt := labels m t

/-- Chain tables for pivot `(i, 0)`: entry `l` holds the pairs `(a, b)` with `ChainFrom … i l a b`. -/
def chainTabs (i : Nat) : Array (Array Bool) :=
  let N := t * m
  let Q := chainQ m t i
  let p : Pt := (i, 0)
  let empty : Array Bool := Array.replicate (N * N) false
  let lvl2 := (Q.flatMap fun a => Q.map fun b => (a, b)).foldl (fun arr ab =>
      if chi reps p ab.1 ab.2 then arr.setIfInBounds (pairCode m N ab.1 ab.2) true else arr) empty
  let next (prev : Array Bool) : Array Bool :=
    (Q.flatMap fun a => Q.map fun b => (a, b)).foldl (fun arr ab =>
      if chi reps p ab.1 ab.2 && Q.any (fun c => prev.getD (pairCode m N ab.2 c) false && chi reps ab.1 ab.2 c)
      then arr.setIfInBounds (pairCode m N ab.1 ab.2) true else arr) empty
  (List.range (K + 1)).foldl (fun tabs l =>
    if l < 2 then tabs.push empty
    else if l == 2 then tabs.push lvl2
    else tabs.push (next (tabs.getD (l - 1) empty))) #[]

def allTabs : Array (Array (Array Bool)) := ((List.range t).map (chainTabs reps m K t)).toArray

def tauB (tabs : Array (Array (Array Bool))) : Var → Bool
  | .f i l a b => ((tabs.getD i #[]).getD l #[]).getD (pairCode m (t * m) a b) false
  | v => baseVal (chi reps) (psiLt reps t) v

def litB (tabs : Array (Array (Array Bool))) (x : Int) : Bool :=
  if 0 < x then tauB reps m t tabs (decodeCode m K t x.natAbs)
  else if x < 0 then !tauB reps m t tabs (decodeCode m K t x.natAbs) else false

def triplesV : List (Pt × Pt × Pt) :=
  (labelsV m t).flatMap fun a => (labelsV m t).flatMap fun b => (labelsV m t).map fun d => (a, b, d)

/-- The Bool versions of the `Model` fields (over valid labels; `psiLt` laws on `0 .. t+1`). -/
def lawReport : List (String × Nat) :=
  let ch := chi reps
  let ps := psiLt reps t
  let tr := triplesV m t
  let dist := tr.filter fun x => decide (Distinct3 x.1 x.2.1 x.2.2)
  let rng2 := List.range (t + 2)
  [("gp_fail", (dist.filter fun x => det (pt reps x.1) (pt reps x.2.1) (pt reps x.2.2) == 0).length),
   ("psi_irrefl_fail", (rng2.filter fun i => ps i i).length),
   ("psi_trans_fail", (rng2.flatMap fun i => rng2.flatMap fun j => rng2.filter fun k =>
      ps i j && ps j k && !ps i k).length),
   ("psi_total_fail", ((List.range t).flatMap fun i => (List.range t).filter fun j =>
      i != j && !ps i j && !ps j i).length),
   ("psi_zero_fail", ((List.range t).filter fun i => 0 < i && !ps 0 i).length),
   ("chi_rot_fail", (tr.filter fun x => ch (rot m x.1) (rot m x.2.1) (rot m x.2.2) != ch x.1 x.2.1 x.2.2).length),
   ("chi_cycle_fail", (dist.filter fun x => ch x.2.1 x.2.2 x.1 != ch x.1 x.2.1 x.2.2).length),
   ("chi_swap_fail", (dist.filter fun x => ch x.1 x.2.2 x.2.1 != !ch x.1 x.2.1 x.2.2).length),
   ("ruleA_fail", (dist.filter fun x => decide (AltCCW m ps x.1 x.2.1 x.2.2) && !ch x.1 x.2.1 x.2.2).length),
   ("ruleB_fail", (dist.filter fun x => decide (BlockCCW m ps x.1 x.2.1 x.2.2) &&
      decide (x.2.1.1 ≤ x.1.1) && decide (x.2.1.1 ≤ x.2.2.1) && !ch x.1 x.2.1 x.2.2).length),
   ("nest_fail", ((List.range t).flatMap fun i => (List.range t).flatMap fun j => (List.range m).filter fun k =>
      decide (i < j) && !ch (i, 0) (i, 1) (j, k)).length),
   ("noChain_fail", ((allTabs reps m K t).toList.map fun tabs =>
      ((tabs.getD (K - 1) #[]).toList.filter id).length).sum),
   ("altccw_triples", (dist.filter fun x => decide (AltCCW m ps x.1 x.2.1 x.2.2)).length),
   ("blockccw_outer_triples", (dist.filter fun x => decide (BlockCCW m ps x.1 x.2.1 x.2.2) &&
      decide (x.2.1.1 ≤ x.1.1) && decide (x.2.1.1 ≤ x.2.2.1)).length)]

/-- Unsatisfied clauses per family of `genCoded` (same pieces, same order). -/
def clauseReport : List (String × Nat) :=
  let tabs := allTabs reps m K t
  let sat (cl : List Int) : Bool := cl.any (litB reps m K t tabs)
  let ad := (orbList m t).map fun c => (angOutsC m t c).1
  let nest := nestLits m t
  let isF := isFalseIn (forcedOf (fBase m t) (ad.filterMap unitOf ++ nest))
  let fam := [("trans", transCl t), ("ang", ad.flatMap angClOf), ("nest", nest.map fun l => [l]),
    ("chain", (rng 0 t).flatMap (chainCl m K t isF))]
  let gc := genCoded m K t
  fam.flatMap (fun f => [(f.1 ++ "_clauses", f.2.length), (f.1 ++ "_UNSAT", (f.2.filter fun cl => !sat cl).length)]) ++
  [("genCoded_clauses", gc.length), ("genCoded_UNSAT", (gc.filter fun cl => !sat cl).length),
   ("chainvars_true", (tabs.toList.map fun tb => (tb.toList.map fun a => (a.toList.filter id).length).sum).sum)]

end

def run (name : String) (reps : List E) (m K t : Nat) : IO Unit := do
  IO.println s!"== {name} m={m} K={K} t={t}"
  IO.println s!"  laws    {lawReport reps m K t}"
  IO.println s!"  clauses {clauseReport reps m K t}"

end EncB.EW

/-- Whole-layer subsets of the exact sets (peel order kept, radii decreasing): non-monotone ψ orders. -/
def pick (reps : List EncB.EW.E) (ix : List Nat) : List EncB.EW.E := ix.map fun i => reps.getD i (0, 0)

open EncB.EW in
#eval do
  -- whole layers in peel order; layer 9 has the least phase, so psi is non-monotone in the index
  let a := pick setA [0, 2, 5, 7, 9]
  let d := pick setD [0, 3, 6, 9]
  for (n, s) in [("A[0,2,5,7,9]", a), ("A[0,2,5,7,9]-mirror", mirror a), ("D[0,3,6,9]", d), ("D[0,3,6,9]-mirror", mirror d)] do
    let ranks := (List.range s.length).map (rank s s.length)
    IO.println s!"{n} psi ranks by layer index: {ranks}"
    run n s 6 8 s.length
