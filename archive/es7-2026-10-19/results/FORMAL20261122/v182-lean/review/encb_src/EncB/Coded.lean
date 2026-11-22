import EncB.Gen
import EncB.Dimacs

/-!
# The functional twin `encB` of `gen` (milestone M2, `DESIGN.md` §3.1)

`genCoded m K t` is the clause list of `gen m K t` (gen_b2.py) with every variable replaced by a **closed-form
code** (`Var.code`), written with list functions only (`flatMap`, `filterMap`, `map`, `foldl`; no `do` loops, no
mutable counter). It calls Gen's helpers `canon`, `olit`, `angOuts`, `patternLit`, `unitOf`, `triples`, `pairs`,
`perms`, `insSort` unchanged and keeps Gen's loop order exactly, so the clauses come in Python's order:

| family | gen_b2.py | here |
|---|---|---|
| ψ-order transitivity | 79-81 | `transCl` |
| angular units / conditional clauses, orbits in first-seen order | 83-141 | `orbList`, `angOutsC`, `angClOf` |
| nesting units | 143-150 | `nestLits` |
| backward chains per pivot: base, extension, closing | 155-190 | `okList`, `extItems`, `levelStep`, `chainCl` |

The codes are `Y(i,j) ↦ 1 + i·t + j`, `H(i) ↦ t² + 1 + i`, `orb c ↦ oBase + triCode m N c`,
`F(piv,l,a,b) ↦ fBase + ((piv·FL + l)·N + ptCode a)·N + ptCode b` with `N = t·m`, `FL = max (K−1) 3`.
`decodeCode_code` inverts them on valid keys (no hypothesis on `K`).

`allCodes` lists the codes in the order of Python's `new()` calls: Y, H (odd m), the orbit codes in first-seen order,
then every code of `genCoded` in clause-stream order, each once (`dedupStep`). Every code that occurs in `genCoded`
is in `allCodes` **by construction** (`mem_allCodes`); that `allCodes` is exactly Python's order (so that the numbers
agree) is checked only by bytes. `encB` renumbers each code to `1 +` its position (`numberMap`, `EncB/Dimacs.lean`).

Filters (`orbList`'s deduplication, `forcedOf`/`isFalseIn`, the per-level key sets `keysOf`) only order, drop or
allocate; soundness (M3) treats each of them as arbitrary.

`orbVarC` returns a code only for a list of three distinct valid labels, so `olit` fails (`none`, no literal) exactly
where gen_b2.py raises `KeyError`, as in Gen (`orbTab` lookup, Gen:273-275). `diagCoded` recomputes Gen's `bad` and
`conflict` for the emitter's refusal (not used by any theorem).
-/

namespace EncB

/-! ## Variables and closed-form codes -/

/-- The variables of encoder B (`DESIGN.md` §2.3). `other n` is the image of a code outside every range. -/
inductive Var where
  /-- `Y'(i,j) = [ψ_i < ψ_j]` (gen_b2.py:36-39) -/
  | y (i j : Nat)
  /-- `Hb(i) = [θ_i < π/m]`, odd m only (gen_b2.py:40) -/
  | h (i : Nat)
  /-- the orbit variable of the canonical triple `c` (gen_b2.py:50-55) -/
  | orb (c : List Pt)
  /-- `F_l(a,b)` of pivot `(piv, 0)`: a chain of `l` labels starting `a, b` (gen_b2.py:161-165) -/
  | f (piv l : Nat) (a b : Pt)
  /-- not a code of any variable -/
  | other (n : Nat)
  deriving DecidableEq, Repr, Inhabited

/-- Chain levels held per pivot, Gen's `FL` (Gen:325). The levels that occur are `2 ≤ l ≤ max 2 (K − 2) < FL`. -/
def chainFL (K : Nat) : Nat := max (K - 1) 3

def yCode (t i j : Nat) : Nat := 1 + i * t + j
def hCode (t i : Nat) : Nat := t * t + 1 + i
def oBase (t : Nat) : Nat := t * t + t + 1
def orbCode (m t : Nat) (c : List Pt) : Nat := oBase t + triCode m (t * m) c
def fBase (m t : Nat) : Nat := oBase t + t * m * (t * m) * (t * m)
def fCode (m K t piv l : Nat) (a b : Pt) : Nat :=
  fBase m t + ((piv * chainFL K + l) * (t * m) + ptCode m a) * (t * m) + ptCode m b
/-- One more than the largest code of a valid variable. -/
def codeBound (m K t : Nat) : Nat := fBase m t + t * chainFL K * (t * m) * (t * m)

/-- The code of a variable. -/
def Var.code (m K t : Nat) : Var → Nat
  | .y i j => yCode t i j
  | .h i => hCode t i
  | .orb c => orbCode m t c
  | .f piv l a b => fCode m K t piv l a b
  | .other n => n

/-- A valid label: layer `< t`, sector `< m`. -/
def PtOk (m t : Nat) (p : Pt) : Prop := p.1 < t ∧ p.2 < m

/-- The keys on which the codes are injective. -/
def Var.Valid (m K t : Nat) : Var → Prop
  | .y i j => i < t ∧ j < t
  | .h i => i < t
  | .orb c => ∃ a b d, c = [a, b, d] ∧ PtOk m t a ∧ PtOk m t b ∧ PtOk m t d
  | .f piv l a b => piv < t ∧ l < chainFL K ∧ PtOk m t a ∧ PtOk m t b
  | .other _ => False

def ptOfCode (m x : Nat) : Pt := (x / m, x % m)

/-- Decode an orbit offset `x = triCode`. -/
def decOrb (m t x : Nat) : Var :=
  .orb [ptOfCode m (x / (t * m) / (t * m)), ptOfCode m (x / (t * m) % (t * m)), ptOfCode m (x % (t * m))]

/-- Decode a chain offset `x = ((piv·FL + l)·N + ptCode a)·N + ptCode b`. -/
def decF (m K t x : Nat) : Var :=
  .f (x / (t * m) / (t * m) / chainFL K) (x / (t * m) / (t * m) % chainFL K)
    (ptOfCode m (x / (t * m) % (t * m))) (ptOfCode m (x % (t * m)))

/-- The inverse of `Var.code` on valid keys (`decodeCode_code`). -/
def decodeCode (m K t n : Nat) : Var :=
  if n = 0 then .other 0
  else if n ≤ t * t then .y ((n - 1) / t) ((n - 1) % t)
  else if n < oBase t then .h (n - (t * t + 1))
  else if n < fBase m t then decOrb m t (n - oBase t)
  else if n < codeBound m K t then decF m K t (n - fBase m t)
  else .other n

/-! ### Arithmetic of the codes -/

theorem div_mul_add {a b N : Nat} (hb : b < N) : (a * N + b) / N = a := by
  have hN : 0 < N := Nat.lt_of_le_of_lt (Nat.zero_le _) hb
  rw [Nat.add_comm, Nat.add_mul_div_right _ _ hN, Nat.div_eq_of_lt hb, Nat.zero_add]

theorem mod_mul_add {a b N : Nat} (hb : b < N) : (a * N + b) % N = b := by
  rw [Nat.add_comm, Nat.add_mul_mod_self_right, Nat.mod_eq_of_lt hb]

theorem mul_add_lt {a b A N : Nat} (ha : a < A) (hb : b < N) : a * N + b < A * N := by
  have h1 : (a + 1) * N ≤ A * N := Nat.mul_le_mul_right _ ha
  rw [Nat.add_mul, Nat.one_mul] at h1
  omega

theorem ptCode_lt {m t : Nat} {p : Pt} (h : PtOk m t p) : ptCode m p < t * m := mul_add_lt h.1 h.2

theorem ptOfCode_ptCode {m t : Nat} {p : Pt} (h : PtOk m t p) : ptOfCode m (ptCode m p) = p := by
  simp only [ptOfCode, ptCode, div_mul_add h.2, mod_mul_add h.2]

/-- **Code decoding**: `decodeCode` inverts `Var.code` on valid keys (layer `< t`, sector `< m`, pivot `< t`,
chain level `< FL`). No hypothesis on `K`. -/
theorem decodeCode_code {m K t : Nat} : ∀ {v : Var}, v.Valid m K t → decodeCode m K t (v.code m K t) = v
  | .y i j, ⟨hi, hj⟩ => by
    have h1 : i * t + j < t * t := mul_add_lt hi hj
    have e : 1 + i * t + j - 1 = i * t + j := by omega
    simp only [Var.code, yCode, decodeCode]
    rw [if_neg (by omega), if_pos (by omega), e, div_mul_add hj, mod_mul_add hj]
  | .h i, hi => by
    have hi : i < t := hi
    simp only [Var.code, hCode, decodeCode, oBase]
    rw [if_neg (by omega), if_neg (by omega), if_pos (by omega)]
    congr 1
    omega
  | .orb c, ⟨a, b, d, hc, ha, hb, hd⟩ => by
    subst hc
    have pa := ptCode_lt ha
    have pb := ptCode_lt hb
    have pd := ptCode_lt hd
    have h1 : ptCode m a * (t * m) + ptCode m b < t * m * (t * m) := mul_add_lt pa pb
    have h2 : (ptCode m a * (t * m) + ptCode m b) * (t * m) + ptCode m d < t * m * (t * m) * (t * m) :=
      mul_add_lt h1 pd
    simp only [Var.code, orbCode, triCode, decodeCode, fBase]
    rw [if_neg (by simp only [oBase]; omega), if_neg (by simp only [oBase]; omega),
      if_neg (by omega), if_pos (by omega), Nat.add_sub_cancel_left]
    simp only [decOrb, div_mul_add pd, div_mul_add pb, mod_mul_add pb, mod_mul_add pd,
      ptOfCode_ptCode ha, ptOfCode_ptCode hb, ptOfCode_ptCode hd]
  | .f piv l a b, ⟨hp, hl, ha, hb⟩ => by
    have pa := ptCode_lt ha
    have pb := ptCode_lt hb
    have h1 : piv * chainFL K + l < t * chainFL K := mul_add_lt hp hl
    have h2 : (piv * chainFL K + l) * (t * m) + ptCode m a < t * chainFL K * (t * m) := mul_add_lt h1 pa
    have h3 : ((piv * chainFL K + l) * (t * m) + ptCode m a) * (t * m) + ptCode m b <
        t * chainFL K * (t * m) * (t * m) := mul_add_lt h2 pb
    simp only [Var.code, fCode, decodeCode, codeBound]
    rw [if_neg (by simp only [fBase, oBase]; omega), if_neg (by simp only [fBase, oBase]; omega),
      if_neg (by simp only [fBase, oBase]; omega), if_neg (by omega), if_pos (by omega),
      Nat.add_assoc (fBase m t), Nat.add_sub_cancel_left]
    simp only [decF, div_mul_add pb, div_mul_add pa, mod_mul_add pa, mod_mul_add pb, div_mul_add hl,
      mod_mul_add hl, ptOfCode_ptCode ha, ptOfCode_ptCode hb]

/-! ## The twin's lookups (gen_b2.py's dicts as closed forms) -/

/-- `pts` (gen_b2.py:51): layer-major. -/
def labels (m t : Nat) : List Pt := (rng 0 t).flatMap fun i => (rng 0 m).map fun k => (i, k)

def ptOkB (m t : Nat) (p : Pt) : Bool := decide (p.1 < t) && decide (p.2 < m)

/-- `c` is a key of `orb` iff it is three distinct valid labels (for the outputs of `canon`, which are the only
arguments `olit` passes). -/
def orbKeyOk (m t : Nat) : List Pt → Bool
  | [a, b, d] => ptOkB m t a && ptOkB m t b && ptOkB m t d && a != b && a != d && b != d
  | _ => false

/-- `orb[c]` as a code; `none` where Python raises `KeyError`. -/
def orbVarC (m t : Nat) (c : List Pt) : Option Nat :=
  if orbKeyOk m t c then some (orbCode m t c) else none

def yLit (t i j : Nat) : Int := (yCode t i j : Int)
def hLit (t i : Nat) : Int := (hCode t i : Int)

/-- The orbit representatives in order of first appearance over `combinations(pts, 3)` (gen_b2.py:50-55). -/
def orbList (m t : Nat) : List (List Pt) :=
  dedupBy (triCode m (t * m)) (t * m * (t * m) * (t * m))
    ((triples (labels m t)).map fun xyz => canon m [xyz.1, xyz.2.1, xyz.2.2])

/-! ## The four clause families, in gen_b2.py's order -/

/-- gen_b2.py:79-81. -/
def transCl (t : Nat) : List (List Int) :=
  (triples (rng 1 t)).flatMap fun ijk =>
    [[-(yLit t ijk.1 ijk.2.1), -(yLit t ijk.2.1 ijk.2.2), yLit t ijk.1 ijk.2.2],
     [yLit t ijk.1 ijk.2.1, yLit t ijk.2.1 ijk.2.2, -(yLit t ijk.1 ijk.2.2)]]

/-- gen_b2.py:86-133 for orbit `c`, with Gen's `angOuts`. -/
def angOutsC (m t : Nat) (c : List Pt) : List (List Int × Option Int) × Nat :=
  angOuts m (m % 2 == 1) (yLit t) (hLit t) (orbVarC m t) c (orbCode m t c)

/-- gen_b2.py:134-141: one unit clause, or one conditional clause per pattern with a literal. -/
def angClOf (outs : List (List Int × Option Int)) : List (List Int) :=
  match unitOf outs with
  | some l => [[l]]
  | none => outs.filterMap fun o => o.2.map fun l => o.1.map (fun x => -x) ++ [l]

/-- gen_b2.py:143-147: the nesting literals (Gen drops a failing `olit`, where Python raises). -/
def nestLits (m t : Nat) : List Int :=
  (rng 0 t).flatMap fun i => (rng (i + 1) t).flatMap fun j => (rng 0 m).filterMap fun k =>
    olit m (orbVarC m t) (i, 0) (i, 1) (j, k)

/-- gen_b2.py's `forced` after the angular units and the nesting units, indexed by code. -/
def forcedOf (S : Nat) (lits : List Int) : Array Int :=
  lits.foldl (fun fa l => fa.setIfInBounds l.natAbs l) (Array.replicate S 0)

/-- gen_b2.py:151-153 `is_false`. -/
def isFalseIn (fa : Array Int) (l : Int) : Bool :=
  let f := fa.getD l.natAbs 0
  f != 0 && f == -l

/-- gen_b2.py:159 `Q` for pivot `(i, 0)`. -/
def chainQ (m t i : Nat) : List Pt :=
  ((rng i t).flatMap fun j => (rng 0 m).map fun k => (j, k)).filter (· != ((i, 0) : Pt))

/-- gen_b2.py:166-172 `okpair`, in insertion order `(a ∈ Q, b ∈ Q)`; `Q` is `chainQ m t i`. -/
def okList (m t i : Nat) (Q : List Pt) (isF : Int → Bool) : List (Pt × Pt × Int) :=
  Q.flatMap fun a => Q.filterMap fun b =>
    if a != b then
      match olit m (orbVarC m t) (i, 0) a b with
      | none => none
      | some l => if isF l then none else some (a, b, l)
    else none

/-- Index of a label pair in a key-set array of size `N²`. -/
def pairCode (m N : Nat) (a b : Pt) : Nat := ptCode m a * N + ptCode m b

/-- gen_b2.py:177-190 at level `lev`, given the key set of level `lev` (`keys`): the clauses with the pair `(a, b)`
whose `F_{lev+1}` they mention. `(a, b) ∈ okpair` is recomputed as `olit p a b = some lab`, `¬ is_false lab`
(`a`, `b ∈ Q`, `a ≠ b`), and `lab` is that literal, as `okpair[(a, b)]` is. `Q` is `chainQ m t i`. -/
def extItems (m K t i lev : Nat) (Q : List Pt) (isF : Int → Bool) (keys : Array Bool)
    (okL : List (Pt × Pt × Int)) : List (Pt × Pt × List Int) :=
  okL.flatMap fun e =>
    if keys.getD (pairCode m (t * m) e.1 e.2.1) false then
      Q.filterMap fun a =>
        if a == e.1 || a == e.2.1 then none
        else match olit m (orbVarC m t) (i, 0) a e.1 with
          | none => none
          | some lab =>
            if isF lab then none
            else match olit m (orbVarC m t) a e.1 e.2.1 with
              | none => none
              | some lt =>
                if isF lt then none
                else if lev + 1 < K - 1 then
                  some (a, e.1, [-(fCode m K t i lev e.1 e.2.1 : Int), -lab, -lt,
                    (fCode m K t i (lev + 1) a e.1 : Int)])
                else some (a, e.1, [-(fCode m K t i lev e.1 e.2.1 : Int), -lab, -lt])
    else []

/-- The key set of a level: the pairs whose `F` variable exists (Python's `(lev, b, c) in F`). -/
def keysOf (m t : Nat) (ps : List (Pt × Pt)) : Array Bool :=
  ps.foldl (fun ks p => ks.setIfInBounds (pairCode m (t * m) p.1 p.2) true)
    (Array.replicate (t * m * (t * m)) false)

/-- One level of gen_b2.py:176: emit its clauses and pass on the key set of the next level. -/
def levelStep (m K t i : Nat) (Q : List Pt) (isF : Int → Bool) (okL : List (Pt × Pt × Int))
    (st : Array Bool × List (List Int)) (lev : Nat) : Array Bool × List (List Int) :=
  let items := extItems m K t i lev Q isF st.1 okL
  (keysOf m t (items.map fun it => (it.1, it.2.1)), st.2 ++ items.map (·.2.2))

/-- gen_b2.py:157-190 for pivot `(i, 0)`: base clauses `[F₂(a,b), −l]`, then levels `2 .. K−2`. -/
def chainCl (m K t : Nat) (isF : Int → Bool) (i : Nat) : List (List Int) :=
  let Q := chainQ m t i
  let okL := okList m t i Q isF
  okL.map (fun e => [(fCode m K t i 2 e.1 e.2.1 : Int), -e.2.2]) ++
  ((rng 2 (K - 1)).foldl (levelStep m K t i Q isF okL) (keysOf m t (okL.map fun e => (e.1, e.2.1)), [])).2

/-- **The coded clause list** (gen_b2.py:77-190 with closed-form codes). -/
def genCoded (m K t : Nat) : List (List Int) :=
  let ad := (orbList m t).map fun c => (angOutsC m t c).1
  let nest := nestLits m t
  let isF := isFalseIn (forcedOf (fBase m t) (ad.filterMap unitOf ++ nest))
  transCl t ++ ad.flatMap angClOf ++ nest.map (fun l => [l]) ++ (rng 0 t).flatMap (chainCl m K t isF)

/-! ## Numbering: the order of Python's `new()` calls -/

/-- The variables allocated before any clause is written: Y (gen_b2.py:36-39), H (:40), orbits (:50-55). -/
def prefixCodes (m t : Nat) : List Nat :=
  ((rng 1 t).flatMap fun i => (rng (i + 1) t).map (yCode t i)) ++
  (if m % 2 == 1 then (rng 1 t).map (hCode t) else []) ++
  (orbList m t).map (orbCode m t)

/-- The step that adds the codes of one clause. -/
def clauseStep (st : Array Bool × List Nat) (cl : List Int) : Array Bool × List Nat :=
  cl.foldl (fun st x => dedupStep id st x.natAbs) st

/-- `prefixCodes`, then the codes of `cls` in stream order, each once. -/
def allCodesOf (m K t : Nat) (cls : List (List Int)) : List Nat :=
  (cls.foldl clauseStep ((prefixCodes m t).foldl (dedupStep id)
    (Array.replicate (codeBound m K t) false, []))).2.reverse

/-- Replace a code literal by its DIMACS number, keeping the sign. -/
def renumberLit (nm : Array Nat) (x : Int) : Int :=
  if 0 < x then ((nm.getD x.natAbs 0 : Nat) : Int) else -((nm.getD x.natAbs 0 : Nat) : Int)

/-- Everything the emitter needs, computed once. -/
structure Enc where
  /-- the DIMACS clauses -/
  clauses : List (List Int)
  /-- the header's variable count -/
  nv : Nat
  /-- `allCodes`: the code of DIMACS variable `n` is entry `n − 1` -/
  codes : List Nat
  /-- `numberMap codes` -/
  nmap : Array Nat

/-- One evaluation of the twin: `genCoded`, `allCodes`, the numbering and the renumbered clauses. -/
def encode (m K t : Nat) : Enc :=
  let cls := genCoded m K t
  let codes := allCodesOf m K t cls
  let nm := numberMap codes
  { clauses := cls.map (fun cl => cl.map (renumberLit nm)), nv := codes.length, codes, nmap := nm }

/-- The codes in Python's `new()` order. -/
def allCodes (m K t : Nat) : List Nat := (encode m K t).codes

/-- **Encoder B, functional twin**: the DIMACS clauses. -/
def encB (m K t : Nat) : List (List Int) := (encode m K t).clauses

/-- The header's variable count. -/
def numVars (m K t : Nat) : Nat := (encode m K t).nv

theorem allCodes_eq (m K t : Nat) : allCodes m K t = allCodesOf m K t (genCoded m K t) := rfl

theorem encB_eq (m K t : Nat) :
    encB m K t = (genCoded m K t).map (fun cl => cl.map (renumberLit (numberMap (allCodes m K t)))) := rfl

theorem numVars_eq (m K t : Nat) : numVars m K t = (allCodes m K t).length := rfl

/-! ## Every code of `genCoded` has a number -/

theorem mem_dedup_clauses : ∀ (cls : List (List Int)) (st : Array Bool × List Nat), SeenInv st →
    SeenInv (cls.foldl clauseStep st) ∧ (∀ cl ∈ cls, ∀ x ∈ cl, x.natAbs ∈ (cls.foldl clauseStep st).2) ∧
      ∀ y ∈ st.2, y ∈ (cls.foldl clauseStep st).2
  | [], st, h => ⟨h, fun _ hc => absurd hc List.not_mem_nil, fun _ hy => hy⟩
  | cl :: cls, st, h => by
    have hstep : clauseStep st cl = (cl.map Int.natAbs).foldl (dedupStep id) st := by
      rw [clauseStep, List.foldl_map]
    obtain ⟨h1, h2, h3⟩ := mem_dedup_foldl (cl.map Int.natAbs) st h
    rw [← hstep] at h1 h2 h3
    obtain ⟨i1, i2, i3⟩ := mem_dedup_clauses cls (clauseStep st cl) h1
    refine ⟨i1, fun c hc x hx => ?_, fun y hy => i3 y (h3 y hy)⟩
    rcases List.mem_cons.1 hc with rfl | hc
    · exact i3 _ (h2 _ (List.mem_map_of_mem hx))
    · exact i2 c hc x hx

theorem mem_allCodesOf {m K t : Nat} {cls : List (List Int)} {cl : List Int} {x : Int} (hcl : cl ∈ cls)
    (hx : x ∈ cl) : x.natAbs ∈ allCodesOf m K t cls := by
  have h0 := (mem_dedup_foldl (prefixCodes m t) _ (seenInv_init (codeBound m K t))).1
  rw [allCodesOf, List.mem_reverse]
  exact (mem_dedup_clauses cls _ h0).2.1 cl hcl x hx

theorem mem_allCodes {m K t : Nat} {cl : List Int} {x : Int} (hcl : cl ∈ genCoded m K t) (hx : x ∈ cl) :
    x.natAbs ∈ allCodes m K t := mem_allCodesOf hcl hx

/-! ## Model transfer and well-formedness -/

/-- A code literal holds under a predicate `τc` on codes. -/
def CodeLitHolds (τc : Nat → Prop) (x : Int) : Prop := (0 < x ∧ τc x.natAbs) ∨ (x < 0 ∧ ¬τc x.natAbs)

/-- The Boolean assignment of DIMACS numbers induced by `τ` (H `Dimacs.lean:185`): number `n` is the variable
`decodeCode (decode allCodes n)`. -/
noncomputable def nuOf (m K t : Nat) (τ : Var → Prop) (n : Nat) : Bool :=
  @decide (τ (decodeCode m K t (decode (allCodes m K t) n))) (Classical.propDecidable _)

/-- **Model transfer** (pattern of H `Dimacs.lean:193`): if every clause of `genCoded` has a literal that holds
under `τ ∘ decodeCode`, the induced assignment satisfies `encB`. Membership of the codes in `allCodes` is by
construction (`mem_allCodes`). -/
theorem dimacsSat_of_holds {m K t : Nat} {τ : Var → Prop}
    (h : ∀ cl ∈ genCoded m K t, ∃ x ∈ cl, CodeLitHolds (fun n => τ (decodeCode m K t n)) x) :
    DimacsSat (encB m K t) (nuOf m K t τ) := by
  intro c hc
  rw [encB_eq, List.mem_map] at hc
  obtain ⟨cl, hcl, rfl⟩ := hc
  obtain ⟨x, hx, hhold⟩ := h cl hcl
  have hmem := mem_allCodes hcl hx
  have hdec := decode_numberMap hmem
  have hnum := numberMap_getD_le hmem
  refine ⟨renumberLit (numberMap (allCodes m K t)) x, List.mem_map_of_mem hx, ?_⟩
  rcases hhold with ⟨hpos, hτ⟩ | ⟨hneg, hτ⟩
  · left
    rw [renumberLit, if_pos hpos]
    refine ⟨by omega, ?_⟩
    rw [Int.natAbs_natCast, nuOf, hdec]
    exact @decide_eq_true _ (Classical.propDecidable _) hτ
  · right
    rw [renumberLit, if_neg (by omega)]
    refine ⟨by omega, ?_⟩
    rw [Int.natAbs_neg, Int.natAbs_natCast, nuOf, hdec]
    exact @decide_eq_false _ (Classical.propDecidable _) hτ

theorem dimacsSatisfiable_of_holds {m K t : Nat} (τ : Var → Prop)
    (h : ∀ cl ∈ genCoded m K t, ∃ x ∈ cl, CodeLitHolds (fun n => τ (decodeCode m K t n)) x) :
    DimacsSatisfiable (encB m K t) :=
  ⟨_, dimacsSat_of_holds h⟩

/-- **Well-formedness**: no literal `0`, every variable `≤` the header count. Symbolic in `m K t`. -/
theorem encB_wf {m K t : Nat} : ∀ cl ∈ encB m K t, ∀ l ∈ cl, l ≠ 0 ∧ l.natAbs ≤ numVars m K t := by
  intro c hc l hl
  rw [encB_eq, List.mem_map] at hc
  obtain ⟨cl, hcl, rfl⟩ := hc
  rw [List.mem_map] at hl
  obtain ⟨x, hx, rfl⟩ := hl
  have hnum := numberMap_getD_le (mem_allCodes hcl hx)
  rw [numVars_eq, renumberLit]
  split
  · rw [Int.natAbs_natCast]
    exact ⟨by omega, hnum.2⟩
  · rw [Int.natAbs_neg, Int.natAbs_natCast]
    exact ⟨by omega, hnum.2⟩

/-! ## Computable checks used as evidence by the emitter (no theorem depends on them) -/

/-- `Var.Valid` as a `Bool`. -/
def Var.validB (m K t : Nat) : Var → Bool
  | .y i j => decide (i < t) && decide (j < t)
  | .h i => decide (i < t)
  | .orb [a, b, d] => ptOkB m t a && ptOkB m t b && ptOkB m t d
  | .orb _ => false
  | .f piv l a b => decide (piv < t) && decide (l < chainFL K) && ptOkB m t a && ptOkB m t b
  | .other _ => false

/-- Every code of the list decodes to a valid variable whose code it is. -/
def codesDecode (m K t : Nat) (codes : List Nat) : Bool :=
  codes.all fun n => (decodeCode m K t n).validB m K t && (decodeCode m K t n).code m K t == n

/-! ## Gen's failure flags, for the emitter's refusal only -/

/-- Gen's `bad` and `conflict` for the twin: failures in the angular patterns (`angOuts`), in the nesting `olit`s
and in the `okpair` `olit`s, and the nesting conflict (gen_b2.py:148-149). An extension `olit a b c` cannot fail
once these pass: `a`, `b`, `c` are pairwise distinct labels of `Q`, so `canon` of them is a key of `orb`; it is
therefore not recounted (that would repeat the whole chain enumeration). Used only to refuse printing where
gen_b2.py raises; no theorem depends on it. -/
def diagCoded (m _K t : Nat) : Nat × Bool :=
  let ang := (orbList m t).map fun c => angOutsC m t c
  let nestRaw := (rng 0 t).flatMap fun i => (rng (i + 1) t).flatMap fun j => (rng 0 m).map fun k =>
    olit m (orbVarC m t) (i, 0) (i, 1) (j, k)
  let nest := nestRaw.filterMap id
  let units := (ang.map (·.1)).filterMap unitOf
  let conflict := (nest.foldl (fun (st : Array Int × Bool) l =>
      let f := st.1.getD l.natAbs 0
      (st.1.setIfInBounds l.natAbs l, st.2 || (f != 0 && f != l))) (forcedOf (fBase m t) units, false)).2
  let badOk := ((rng 0 t).map fun i =>
      let Q := chainQ m t i
      (Q.flatMap fun a => Q.filter fun b => a != b && (olit m (orbVarC m t) (i, 0) a b).isNone).length).sum
  ((ang.map (·.2)).sum + nestRaw.countP Option.isNone + badOk, conflict)

end EncB
