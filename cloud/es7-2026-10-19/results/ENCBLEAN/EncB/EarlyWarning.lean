import EncB.Model

/-!
# M3 early-warning test (unit U6, `docs/M3PLAN.md` §4): evidence only, never a kernel computation

Run by `scripts/ew_test.sh`, i.e. `lake env lean --run EncB/EarlyWarning.lean`: `main` is interpreted from the
compiler's IR. Nothing here is a theorem; nothing is evaluated by the kernel, by `decide` in a proof or by `#eval`;
`EncB.lean` does not import this file, and it writes no `.olean`.

The question is whether the frozen interface (`EncB/Model.lean`) can be wrong in a way the proofs of U1–U5 would
find only late. For exact concrete configurations it builds a `Model`-shaped `chi` and `psiLt`, checks every
`Model` field as a Boolean statement over the valid labels (with the interface's own `Decidable` instances for
`AltCCW`, `BlockCCW`, `InQ`, `Distinct3`), and evaluates every clause of `genCoded m K t` under the interface's own
assignment `tauOf` through `decodeCode`: `baseVal` on Y, H, orbit and other codes, and chain codes by a level DP,
the least fixpoint of the base and extension clauses read as definitions, which is `ChainFrom` (not proved equal).

Parts (plan §4):
* (a) SIX60: layer representatives of `SIX60/sets/c6_60pts_{A,B,C,D}` in the Eisenstein basis `(1, ζ)`,
  `ζ = e^{iπ/3}`: `a + bζ` is `(a, b)`, the rotation by `2π/6` is `(a, b) ↦ (−b, a + b)`, and the orientation is the
  sign of the integer determinant (the basis is positively oriented). Label `(i, k)` is `ζ^k · rep i`; every
  `rep i` lies in `[0, π/3)`, so `ψ_i` is its direction. Mirror: `rep i ↦ (b, a)` (`(a, 0)` stays), i.e.
  `ψ_i ↦ π/3 − ψ_i`.
* (b) non-monotone ψ: whole-layer subsets of A and D (peel order kept).
* (c) m = 4: nested squares on the Gaussian integers (rotation `(a, b) ↦ (−b, a)`).
* (d) the conclusions of `SortedSix` and `WordSpec` on every ordered triple of distinct labels with distinct keys.
* (e) plan A's regular m-gons with exact coordinates in `ℤ[√3]`.
* Controls, each of which must be detected (plan §4 table).

Pass criterion: the `EW SUMMARY` line; `main` returns 0 iff it says PASS.
-/

namespace EncB.EW

/-! ## Exact point sets -/

abbrev E := Int × Int

def det (p q r : E) : Int := (q.1 - p.1) * (r.2 - p.2) - (q.2 - p.2) * (r.1 - p.1)

/-- Rotation by `2π/6` in the Eisenstein basis. -/
def rotEis (p : E) : E := (-p.2, p.1 + p.2)

/-- Rotation by `2π/4` on the Gaussian integers. -/
def rotGau (p : E) : E := (-p.2, p.1)

def iterE (f : E → E) : Nat → E → E
  | 0, p => p
  | n + 1, p => iterE f n (f p)

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

/-- Whole layers of a set, in the given order. -/
def pick (reps : List E) (ix : List Nat) : List E := ix.map fun i => reps.getD i (0, 0)

/-- Nested squares: reps in the sector `[0, π/2)`, radii decreasing. -/
def sq2 : List E := [(1000, 0), (300, 37)]
def sq3 : List E := [(1000, 0), (300, 37), (180, 61)]
def sq4 : List E := [(1000, 0), (300, 37), (180, 61), (101, 29)]

/-! ### `ℤ[√3]` (plan A's synthetic regular polygons, `m ∈ {4, 6}`) -/

/-- `a + b√3`. -/
structure Z3 where
  a : Int
  b : Int

instance : Add Z3 := ⟨fun x y => ⟨x.a + y.a, x.b + y.b⟩⟩
instance : Sub Z3 := ⟨fun x y => ⟨x.a - y.a, x.b - y.b⟩⟩
instance : Mul Z3 := ⟨fun x y => ⟨x.a * y.a + 3 * x.b * y.b, x.a * y.b + x.b * y.a⟩⟩

/-- The exact sign of `a + b√3` (`√3` is irrational, so `a² = 3b²` only at `0`). -/
def Z3.sign (x : Z3) : Int :=
  if x.a ≥ 0 && x.b ≥ 0 then (if x.a == 0 && x.b == 0 then 0 else 1)
  else if x.a ≤ 0 && x.b ≤ 0 then -1
  else
    let d := x.a * x.a - 3 * x.b * x.b
    if x.a > 0 then (if d > 0 then 1 else -1) else (if d > 0 then -1 else 1)

/-- `(2 cos (2πk/m), 2 sin (2πk/m))` for `m ∈ {4, 6}`. -/
def rotTab (m k : Nat) : Z3 × Z3 :=
  if m == 6 then
    match k % 6 with
    | 0 => (⟨2, 0⟩, ⟨0, 0⟩) | 1 => (⟨1, 0⟩, ⟨0, 1⟩) | 2 => (⟨-1, 0⟩, ⟨0, 1⟩)
    | 3 => (⟨-2, 0⟩, ⟨0, 0⟩) | 4 => (⟨-1, 0⟩, ⟨0, -1⟩) | _ => (⟨1, 0⟩, ⟨0, -1⟩)
  else
    match k % 4 with
    | 0 => (⟨2, 0⟩, ⟨0, 0⟩) | 1 => (⟨0, 0⟩, ⟨2, 0⟩) | 2 => (⟨-2, 0⟩, ⟨0, 0⟩) | _ => (⟨0, 0⟩, ⟨-2, 0⟩)

/-- `2 · P(i, k)`: the layer vector `vs[i]` (direction `ψ_i`) rotated by `2πk/m`. -/
def z3Pt (m : Nat) (vs : List E) (p : Pt) : Z3 × Z3 :=
  let v := vs.getD p.1 (0, 0)
  let cs := rotTab m p.2
  let x : Z3 := ⟨v.1, 0⟩
  let y : Z3 := ⟨v.2, 0⟩
  (cs.1 * x - cs.2 * y, cs.2 * x + cs.1 * y)

def orientZ3 (A B C : Z3 × Z3) : Z3 := (B.1 - A.1) * (C.2 - A.2) - (B.2 - A.2) * (C.1 - A.1)

/-- Layer vectors: layer 0 at angle 0, inner layers at distinct angles in `(0, 2π/m)`. -/
def vs6 : List E := [(4096, 0), (1700, 900), (800, 150), (330, 280)]
def vs4 : List E := [(1000, 0), (400, 300), (100, 160), (60, 20)]
/-- Radius ratios close to the apothem bound, another ψ order. -/
def vs6b : List E := [(10000, 0), (7000, 3000), (5500, 600), (3700, 2700), (2800, 1500)]

/-! ## A configuration: `chi` tabulated on valid labels, ψ by ranks -/

structure Cfg where
  name : String
  m : Nat
  K : Nat
  t : Nat
  /-- `chi a b d` for valid labels, at `(ptCode a · N + ptCode b) · N + ptCode d`, `N = t · m` -/
  chiTab : Array Bool
  /-- the ψ rank of each layer `< t` -/
  rank : Array Nat
  /-- distinct valid triples with orientation 0 (general position fails) -/
  degen : Nat

/-- `chi`: the table on valid labels, `false` elsewhere (every `Model` field constrains valid labels only, and
`decodeCode` only produces valid ones). -/
def Cfg.chi (C : Cfg) (a b d : Pt) : Bool :=
  let N := C.t * C.m
  ptOkB C.m C.t a && ptOkB C.m C.t b && ptOkB C.m C.t d &&
    C.chiTab.getD ((ptCode C.m a * N + ptCode C.m b) * N + ptCode C.m d) false

/-- Layers `≥ t` rank above all others, in index order. -/
def Cfg.rk (C : Cfg) (i : Nat) : Nat := if i < C.t then C.rank.getD i 0 else i + C.t

def Cfg.psiLt (C : Cfg) (i j : Nat) : Bool := decide (C.rk i < C.rk j)

/-- All ordered triples of valid labels, in `ptCode` order. -/
def triplesL (m t : Nat) : List (Pt × Pt × Pt) :=
  let L := labels m t
  L.flatMap fun a => L.flatMap fun b => L.map fun d => (a, b, d)

/-- `rank i = #{j < t : ψ_j < ψ_i}` for directions `vs` in one open half-plane. -/
def ranksOf (vs : List E) (t : Nat) : Array Nat :=
  ((List.range t).map fun i => ((List.range t).filter fun j =>
    decide (0 < det (0, 0) (vs.getD j (0, 0)) (vs.getD i (0, 0)))).length).toArray

/-- A configuration from an exact orientation `sgn` (only its sign is used); `neg` mirrors `chi` (a mutant). -/
def mkCfg (name : String) (m K t : Nat) (sgn : Pt → Pt → Pt → Int) (rank : Array Nat) (neg : Bool) : Cfg :=
  let tr := triplesL m t
  { name, m, K, t, rank,
    chiTab := (tr.map fun x => decide (0 < sgn x.1 x.2.1 x.2.2) != neg).toArray,
    degen := (tr.filter fun x => decide (Distinct3 x.1 x.2.1 x.2.2) && sgn x.1 x.2.1 x.2.2 == 0).length }

/-- Lattice sets: label `(i, k)` is `rotE^k (reps i)`; ψ from `psiReps` (normally `reps`). -/
def latCfg (name : String) (rotE : E → E) (reps : List E) (m K t : Nat) (psiReps : List E := reps) : Cfg :=
  let pt (a : Pt) : E := iterE rotE a.2 (reps.getD a.1 (0, 0))
  mkCfg name m K t (fun a b d => det (pt a) (pt b) (pt d)) (ranksOf psiReps t) false

def z3Cfg (name : String) (vs : List E) (m K t : Nat) (neg : Bool := false) : Cfg :=
  mkCfg name m K t (fun a b d => (orientZ3 (z3Pt m vs a) (z3Pt m vs b) (z3Pt m vs d)).sign) (ranksOf vs t) neg

/-! ## Chain variables, the assignment, laws and clauses -/

abbrev Tabs := Array (Array (Array Bool))

/-- Level tables for pivot `(i, 0)`, entry `l ≤ K` over `pairCode` of `a, b ∈ chainQ m t i`: level 2 is
`chi p a b`, level `l + 1` is `chi p a b ∧ ∃ c ∈ Q, chi a b c ∧ (level l) b c`. -/
def chainTabs (C : Cfg) (i : Nat) : Array (Array Bool) :=
  let N := C.t * C.m
  let Q := chainQ C.m C.t i
  let p : Pt := (i, 0)
  let QQ := Q.flatMap fun a => Q.map fun b => (a, b)
  let empty : Array Bool := Array.replicate (N * N) false
  let lvl2 := QQ.foldl (fun arr ab =>
    if C.chi p ab.1 ab.2 then arr.setIfInBounds (pairCode C.m N ab.1 ab.2) true else arr) empty
  let next (prev : Array Bool) : Array Bool := QQ.foldl (fun arr ab =>
    if C.chi p ab.1 ab.2 && Q.any (fun c => prev.getD (pairCode C.m N ab.2 c) false && C.chi ab.1 ab.2 c)
    then arr.setIfInBounds (pairCode C.m N ab.1 ab.2) true else arr) empty
  (List.range (C.K + 1)).foldl (fun tabs l =>
    if l < 2 then tabs.push empty
    else if l == 2 then tabs.push lvl2
    else tabs.push (next (tabs.getD (l - 1) empty))) #[]

def Cfg.tabs (C : Cfg) : Tabs := ((List.range C.t).map (chainTabs C)).toArray

/-- `ChainFrom C.m C.t C.chi i l a b`: levels 0 and 1 by the definition, levels `≥ 2` from the tables. -/
def chainB (C : Cfg) (T : Tabs) (i l : Nat) (a b : Pt) : Bool :=
  if l == 0 then true
  else if l == 1 then decide (InQ C.m C.t i a)
  else decide (InQ C.m C.t i a) && decide (InQ C.m C.t i b) &&
    ((T.getD i #[]).getD l #[]).getD (pairCode C.m (C.t * C.m) a b) false

/-- `tauOf C.m C.t C.chi C.psiLt`, computably. -/
def tauB (C : Cfg) (T : Tabs) : Var → Bool
  | .f i l a b => chainB C T i l a b
  | v => baseVal C.chi C.psiLt v

/-- `CodeLitHolds (tauOf … ∘ decodeCode)`. -/
def litB (C : Cfg) (T : Tabs) (x : Int) : Bool :=
  let v := tauB C T (decodeCode C.m C.K C.t x.natAbs)
  if 0 < x then v else if x < 0 then !v else false

/-- Failures of each `Model` field (and of general position) over valid labels; `psiLt` laws on `0 .. t+1`.
Second component: how often the rules apply. -/
def lawReport (C : Cfg) (T : Tabs) : List (String × Nat) × List (String × Nat) :=
  let m := C.m
  let t := C.t
  let ch := C.chi
  let ps := C.psiLt
  let L := labels m t
  let tr := triplesL m t
  let dist := tr.filter fun x => decide (Distinct3 x.1 x.2.1 x.2.2)
  let r2 := List.range (t + 2)
  let rt := List.range t
  let alt := dist.filter fun x => decide (AltCCW m ps x.1 x.2.1 x.2.2)
  let blk := dist.filter fun x => decide (x.2.1.1 ≤ x.1.1) && decide (x.2.1.1 ≤ x.2.2.1) &&
    decide (BlockCCW m ps x.1 x.2.1 x.2.2)
  ([("gp_fail", C.degen),
    ("psiLt_irrefl_fail", (r2.filter fun i => ps i i).length),
    ("psiLt_trans_fail", (r2.flatMap fun i => r2.flatMap fun j => r2.filter fun k =>
      ps i j && ps j k && !ps i k).length),
    ("psiLt_total_fail", (rt.flatMap fun i => rt.filter fun j => i != j && !ps i j && !ps j i).length),
    ("psiLt_zero_fail", (rt.filter fun i => 0 < i && !ps 0 i).length),
    ("chi_rot_fail", (tr.filter fun x => ch (rot m x.1) (rot m x.2.1) (rot m x.2.2) != ch x.1 x.2.1 x.2.2).length),
    ("chi_cycle_fail", (dist.filter fun x => ch x.2.1 x.2.2 x.1 != ch x.1 x.2.1 x.2.2).length),
    ("chi_swap_fail", (dist.filter fun x => ch x.1 x.2.2 x.2.1 != !ch x.1 x.2.1 x.2.2).length),
    ("ruleA_fail", (alt.filter fun x => !ch x.1 x.2.1 x.2.2).length),
    ("ruleB_fail", (blk.filter fun x => !ch x.1 x.2.1 x.2.2).length),
    ("nest_fail", (rt.flatMap fun i => rt.flatMap fun j => (List.range m).filter fun k =>
      decide (i < j) && !ch (i, 0) (i, 1) (j, k)).length),
    ("noChain_fail", (rt.flatMap fun i => L.flatMap fun a => L.filter fun b =>
      chainB C T i (C.K - 1) a b).length)],
   [("altccw_triples", alt.length), ("blockccw_outer_triples", blk.length)])

/-- Per family of `genCoded` (its own pieces, in its order): `(family, clauses, unsatisfied)`; then the totals of
`genCoded` itself and whether the four families concatenate to it. -/
def clauseReport (C : Cfg) (T : Tabs) : List (String × Nat × Nat) × Nat × Nat × Bool :=
  let m := C.m
  let K := C.K
  let t := C.t
  let unsat (cls : List (List Int)) : Nat := (cls.filter fun cl => !cl.any (litB C T)).length
  let ad := (orbList m t).map fun c => (angOutsC m t c).1
  let nest := nestLits m t
  let isF := isFalseIn (forcedOf (fBase m t) (ad.filterMap unitOf ++ nest))
  let fam := [("trans", transCl t), ("ang", ad.flatMap angClOf), ("nest", nest.map fun l => [l]),
    ("chain", (rng 0 t).flatMap (chainCl m K t isF))]
  let gc := genCoded m K t
  (fam.map (fun f => (f.1, f.2.length, unsat f.2)), gc.length, unsat gc, fam.flatMap (·.2) == gc)

/-! ## Runs -/

/-- What a run must show. -/
inductive Kind where
  /-- every law holds and no clause is unsatisfied -/
  | base
  /-- only `noChain` fails, and only chain clauses are unsatisfied -/
  | chainCtrl
  /-- `ruleA`, `ruleB` or `nest` fails, and some clause is unsatisfied -/
  | rulesCtrl
  /-- some clause is unsatisfied -/
  | clauseCtrl

def Kind.str : Kind → String
  | .base => "base"
  | .chainCtrl => "control(noChain)"
  | .rulesCtrl => "control(rules)"
  | .clauseCtrl => "control(clauses)"

def Kind.isBase : Kind → Bool
  | .base => true
  | _ => false

structure Out where
  kind : Kind
  lawsOk : Bool
  unsat : Nat
  split : Bool
  ok : Bool

def runCfg (part : String) (kind : Kind) (C : Cfg) : IO Out := do
  let t0 ← IO.monoMsNow
  let T := C.tabs
  let (laws, info) := lawReport C T
  let (fam, n, u, split) := clauseReport C T
  let lawsOk := laws.all (·.2 == 0)
  let badLaws := (laws.filter (·.2 != 0)).map (·.1)
  let badFams := (fam.filter (·.2.2 != 0)).map (·.1)
  let ok := split && match kind with
    | .base => lawsOk && u == 0
    | .chainCtrl => badLaws == ["noChain_fail"] && badFams == ["chain"]
    | .rulesCtrl => u != 0 && badLaws.any (fun s => s == "ruleA_fail" || s == "ruleB_fail" || s == "nest_fail")
    | .clauseCtrl => u != 0
  IO.println s!"== ({part}) {C.name} (m,K,t)=({C.m},{C.K},{C.t}) {kind.str}: {if ok then "as expected" else "UNEXPECTED"}"
  let cv := ((List.range C.t).flatMap fun i => (List.range (C.K + 1)).map fun l =>
    (((T.getD i #[]).getD l #[]).toList.filter id).length).sum
  IO.println s!"   laws    {laws}"
  IO.println s!"   info    {info ++ [("chainvars_true", cv)]}, psi ranks {C.rank.toList}"
  IO.println s!"   clauses {fam.flatMap (fun f => [(f.1 ++ "_clauses", f.2.1), (f.1 ++ "_UNSAT", f.2.2)]) ++
    [("genCoded_clauses", n), ("genCoded_UNSAT", u)]}, families = genCoded: {split}"
  let t1 ← IO.monoMsNow
  IO.println s!"   ({t1 - t0} ms)"
  return { kind, lawsOk, unsat := u, split, ok }

/-! ## (d) The conclusions of `SortedSix` and `WordSpec` -/

/-- Verbatim copy of `EncB.Rules.objsEven` (U4's start file; `patternLit_even` there is `rfl`). -/
def objsEven (m : Nat) (rk : Nat → Nat) (c : List Pt) : List Obj :=
  (c.zip (List.range c.length)).flatMap fun pi =>
    let (p, idx) := pi
    let (J, Ja) := ((p.2, (p.2 + m / 2) % m) : Nat × Nat)
    [⟨J, rk p.1, 1, idx⟩, ⟨Ja, rk p.1, 0, idx⟩]

def psiOf (perm : List Nat) (i j : Nat) : Bool := decide (perm.idxOf i < perm.idxOf j)

def sortedSixB (m : Nat) (psiLt : Nat → Nat → Bool) (a b d : Pt) (S : List Obj) : Bool :=
  S.length == 6 &&
  decide (S.Pairwise fun o o' => objLt m psiLt (objImg [a, b, d] o) (objImg [a, b, d] o')) &&
  (objs6 a b d).all (fun x => (S.map (objImg [a, b, d])).contains x) &&
  S.all (fun o => decide (o.idx < 3)) &&
  ((S.filter (·.kind == 1)).map (·.idx)).isPerm [0, 1, 2]

/-- Over all ordered triples of distinct labels of `labels m t` whose six keys are distinct (the triples
`patternLit` does not skip), with `rk = idxOf` in `perm`: `(triples, violations, alternating, with a PPP run)`.
`swap` is the negative control: it exchanges the first two picks of both conclusions. -/
def wordCheck (swap : Bool) (m t : Nat) (perm : List Nat) : Nat × Nat × Nat × Nat :=
  let psiLt := psiOf perm
  let rk : Nat → Nat := fun L => perm.idxOf L
  let labs := labels m t
  let trip := labs.flatMap fun a => labs.flatMap fun b => labs.filterMap fun d =>
    if a != b && a != d && b != d then some (a, b, d) else none
  trip.foldl (fun (acc : Nat × Nat × Nat × Nat) abd =>
    let (a, b, d) := abd
    let c := [a, b, d]
    let objs := objsEven m rk c
    if (pairs (objs.map fun o => (o.J, o.r))).any (fun kk => kk.1 == kk.2) then acc
    else
      let S := insSort Obj.lt objs
      let kinds := S.map (·.kind)
      let seq := (S.filter (·.kind == 1)).map (·.idx)
      let i0 := if swap then 1 else 0
      let i1 := if swap then 0 else 1
      let alt := kinds == [1, 0, 1, 0, 1, 0] || kinds == [0, 1, 0, 1, 0, 1]
      let altOk := !alt || decide (AltCCW m psiLt (c.getD (seq.getD i0 0) (0, 0))
        (c.getD (seq.getD i1 0) (0, 0)) (c.getD (seq.getD 2 0) (0, 0)))
      let isRun (st : Nat) : Bool :=
        kinds.getD (st % 6) 0 == 1 && kinds.getD ((st + 1) % 6) 0 == 1 && kinds.getD ((st + 2) % 6) 0 == 1
      let blkOk := (List.range 6).all fun st => !isRun st ||
        decide (BlockCCW m psiLt (c.getD (S.getD ((st + i0) % 6) default).idx (0, 0))
          (c.getD (S.getD ((st + i1) % 6) default).idx (0, 0))
          (c.getD (S.getD ((st + 2) % 6) default).idx (0, 0)))
      let ok := sortedSixB m psiLt a b d S && altOk && blkOk
      (acc.1 + 1, acc.2.1 + (if ok then 0 else 1), acc.2.2.1 + (if alt then 1 else 0),
        acc.2.2.2 + (if (List.range 6).any isRun then 1 else 0)))
    (0, 0, 0, 0)

def psiPerms : List (List Nat) := [[0, 1, 2, 3], [0, 3, 1, 2], [0, 2, 3, 1], [0, 3, 2, 1]]

/-! ## Main -/

def main : IO UInt32 := do
  IO.println "EW: M3 early-warning test (docs/M3PLAN.md section 4), interpreted by `lean --run`; evidence only"
  let mut outs : Array Out := #[]
  -- (a) SIX60, base runs
  for (n, s) in [("A", setA), ("B", setB), ("C", setC), ("D", setD)] do
    outs := outs.push (← runCfg "a" .base (latCfg n rotEis s 6 8 3))
    outs := outs.push (← runCfg "a" .base (latCfg (n ++ "-mirror") rotEis (mirror s) 6 8 3))
  for (n, s) in [("A", setA), ("A-mirror", mirror setA), ("B-mirror", mirror setB), ("D", setD)] do
    outs := outs.push (← runCfg "a" .base (latCfg n rotEis s 6 8 5))
  -- (b) non-monotone psi: whole layers in peel order
  for (n, s) in [("A[0,2,5,7,9]", pick setA [0, 2, 5, 7, 9]), ("D[0,3,6,9]", pick setD [0, 3, 6, 9])] do
    outs := outs.push (← runCfg "b" .base (latCfg n rotEis s 6 8 s.length))
    outs := outs.push (← runCfg "b" .base (latCfg (n ++ "-mirror") rotEis (mirror s) 6 8 s.length))
  -- (c) m = 4: nested squares; sq4 at K = 6 contains a convex hexagon (control)
  for (n, s) in [("sq2", sq2), ("sq3", sq3), ("sq4", sq4)] do
    for K in [6, 8] do
      let kind := if n == "sq4" && K == 6 then Kind.chainCtrl else Kind.base
      outs := outs.push (← runCfg "c" kind (latCfg n rotGau s 4 K s.length))
      outs := outs.push (← runCfg "c" kind (latCfg (n ++ "-mirror") rotGau (mirror s) 4 K s.length))
  -- (e) plan A's regular polygons in Z[sqrt 3]
  outs := outs.push (← runCfg "e" .base (z3Cfg "vs6" vs6 6 8 2))
  outs := outs.push (← runCfg "e" .base (z3Cfg "vs6" vs6 6 8 3))
  outs := outs.push (← runCfg "e" .base (z3Cfg "vs4" vs4 4 8 3))
  outs := outs.push (← runCfg "e" .base (z3Cfg "vs6b" vs6b 6 10 3))
  -- controls
  outs := outs.push (← runCfg "ctl" .chainCtrl (latCfg "A K=5" rotEis setA 6 5 3))
  outs := outs.push (← runCfg "ctl" .clauseCtrl (latCfg "chi(A)/psi(A-mirror)" rotEis setA 6 8 4 (mirror setA)))
  outs := outs.push (← runCfg "ctl" .rulesCtrl (z3Cfg "vs6 mirrored chi" vs6 6 8 3 true))
  -- (d) SortedSix / WordSpec conclusions, and the swapped-picks control
  let t0 ← IO.monoMsNow
  let mut wTrip := 0
  let mut wViol := 0
  for m in [2, 4, 6, 8] do
    for p in psiPerms do
      let r := wordCheck false m 4 p
      IO.println s!"== (d) WordCheck m={m} t=4 psi order {p}: (triples, violations, alternating, with PPP) {r}"
      wTrip := wTrip + r.1
      wViol := wViol + r.2.1
  let mut mTrip := 0
  let mut mViol := 0
  for p in psiPerms do
    let r := wordCheck true 6 4 p
    IO.println s!"== (ctl) WordCheck swapped picks m=6 t=4 psi order {p}: (triples, violations, alternating, with PPP) {r}"
    mTrip := mTrip + r.1
    mViol := mViol + r.2.1
  let t1 ← IO.monoMsNow
  IO.println s!"   ({t1 - t0} ms)"
  -- summary
  let bases := outs.filter (·.kind.isBase)
  let ctrls := outs.filter (!·.kind.isBase)
  let c1 := outs.all fun o => !o.lawsOk || o.unsat == 0
  let c2 := bases.all (·.ok)
  let c3 := wViol == 0 && wTrip > 0
  let wOk := mTrip > 0 && mViol == mTrip
  let c4 := ctrls.all (·.ok) && wOk
  let split := outs.all (·.split)
  let pass := c1 && c2 && c3 && c4 && split
  IO.println (s!"EW SUMMARY: {if pass then "PASS" else "FAIL"} | runs {outs.size} (base {bases.size}, " ++
    s!"controls {ctrls.size} + WordCheck swap) | (1) all laws hold => 0 unsatisfied clauses, every run: {c1} | " ++
    s!"(2) base runs: laws hold, 0 unsatisfied: {(bases.filter (·.ok)).size}/{bases.size} | " ++
    s!"(3) WordCheck violations {wViol} of {wTrip} triples | " ++
    s!"(4) controls detected {(ctrls.filter (·.ok)).size + (if wOk then 1 else 0)}/{ctrls.size + 1} " ++
    s!"(WordCheck swap: {mViol} of {mTrip} triples fail) | families = genCoded, every run: {split}")
  return (if pass then 0 else 1)

end EncB.EW

/-- The entry point of `lean --run` (it looks up the root name `main`). -/
def main : IO UInt32 := EncB.EW.main

/-- info: 'EncB.EW.main' depends on axioms: [propext] -/
#guard_msgs in #print axioms EncB.EW.main
