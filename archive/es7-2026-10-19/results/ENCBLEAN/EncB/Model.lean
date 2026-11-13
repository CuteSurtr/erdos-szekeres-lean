import EncB.Coded

/-!
# The combinatorial interface of M3 (`DESIGN.md` §2.2–2.3): `Model`, the intended assignment, the unit specs

Frozen by the M3 interface unit U0 (plan `M3PLAN.md`). Std-only.

* `Model m K t` is `DESIGN.md` §2.2 with `Valid` replaced by Coded's `PtOk` (the same body). Its fields are what
  `encB_satisfiable` consumes and what M6 (`modelOfLabelling`) must prove; no field was added or changed.
* The intended assignment (`DESIGN.md` §2.3, KS Def. k8s:def:assign) is `tauOf`: chain variables by `ChainFrom`,
  every other variable by the computable `baseVal` (Y ↦ `psiLt`, orbit ↦ `chi` of the sorted triple, H and
  `Var.other` ↦ false). `Var.other` is M2's fifth constructor; `DESIGN.md` §2.3's match lacked it.
  `ChainFrom` takes `m t chi`, not the model, so the early-warning test evaluates the same definitions.
* Unit specifications, so that the units can be proved in parallel and assume each other only as hypotheses:
  `OlitSpec` (proved in U0, `olitSpec`), `OrbListSpec` (U1), `RkMono`/`PatternSpec` (U4, consumed by U3),
  `SortedSix`/`WordSpec` (U5, consumed by U4), `SortSpec`/`ObjLtSpec` (proved in U0).
-/

namespace EncB

/-! ## Labels, objects, circular order -/

/-- The rotation `ρ` on labels. -/
def rot (m : Nat) (a : Pt) : Pt := (a.1, (a.2 + 1) % m)

def Distinct3 (a b d : Pt) : Prop := a ≠ b ∧ a ≠ d ∧ b ≠ d

/-- Labels of the chain family for pivot layer `i` (gen_b2.py:159); `mem_chainQ` ties it to `chainQ`. -/
def InQ (m t i : Nat) (a : Pt) : Prop := i ≤ a.1 ∧ a.1 < t ∧ a.2 < m ∧ a ≠ (i, 0)

/-- Cell of an object (`(a, true)` = point of label `a`, `(a, false)` = its antipode), in units of `2π/m`. -/
def cell (m : Nat) (o : Pt × Bool) : Nat := if o.2 then o.1.2 else (o.1.2 + m / 2) % m

/-- The circular order of objects counterclockwise from the direction of `(0,0)`: by cell, then by ψ. -/
def objLt (m : Nat) (psiLt : Nat → Nat → Bool) (o o' : Pt × Bool) : Prop :=
  cell m o < cell m o' ∨ (cell m o = cell m o' ∧ psiLt o.1.1 o'.1.1 = true)

/-- `z` lies strictly inside the counterclockwise arc from `x` to `y`. -/
def ccwIn {α : Type} (lt : α → α → Prop) (x z y : α) : Prop :=
  (lt x z ∧ lt z y) ∨ (lt y x ∧ lt x z) ∨ (lt z y ∧ lt y x)

def objs6 (a b d : Pt) : List (Pt × Bool) :=
  [(a, true), (b, true), (d, true), (a, false), (b, false), (d, false)]

def KeysDistinct (m : Nat) (psiLt : Nat → Nat → Bool) (a b d : Pt) : Prop :=
  ∀ o ∈ objs6 a b d, ∀ o' ∈ objs6 a b d, o ≠ o' → objLt m psiLt o o' ∨ objLt m psiLt o' o

def ArcHasAntipode (m : Nat) (psiLt : Nat → Nat → Bool) (a b d x y : Pt) : Prop :=
  ∃ z ∈ [a, b, d], ccwIn (objLt m psiLt) (x, true) (z, false) (y, true)

/-- Rule A pattern: `a → b → d` counterclockwise and each of the three arcs holds an antipode. -/
def AltCCW (m : Nat) (psiLt : Nat → Nat → Bool) (a b d : Pt) : Prop :=
  KeysDistinct m psiLt a b d ∧ ccwIn (objLt m psiLt) (a, true) (b, true) (d, true) ∧
  ArcHasAntipode m psiLt a b d a b ∧ ArcHasAntipode m psiLt a b d b d ∧
  ArcHasAntipode m psiLt a b d d a

/-- Rule B pattern: `a → b → d` counterclockwise and the arcs `(a,b)`, `(b,d)` hold no antipode. -/
def BlockCCW (m : Nat) (psiLt : Nat → Nat → Bool) (a b d : Pt) : Prop :=
  KeysDistinct m psiLt a b d ∧ ccwIn (objLt m psiLt) (a, true) (b, true) (d, true) ∧
  ¬ ArcHasAntipode m psiLt a b d a b ∧ ¬ ArcHasAntipode m psiLt a b d b d

instance (m : Nat) (psiLt : Nat → Nat → Bool) (o o' : Pt × Bool) : Decidable (objLt m psiLt o o') :=
  inferInstanceAs (Decidable (_ ∨ _))
instance {α : Type} (lt : α → α → Prop) [DecidableRel lt] (x z y : α) : Decidable (ccwIn lt x z y) :=
  inferInstanceAs (Decidable (_ ∨ _))
instance (m : Nat) (psiLt : Nat → Nat → Bool) (a b d : Pt) : Decidable (KeysDistinct m psiLt a b d) :=
  inferInstanceAs (Decidable (∀ o ∈ objs6 a b d, _))
instance (m : Nat) (psiLt : Nat → Nat → Bool) (a b d x y : Pt) :
    Decidable (ArcHasAntipode m psiLt a b d x y) :=
  inferInstanceAs (Decidable (∃ z ∈ [a, b, d], _))
instance (m : Nat) (psiLt : Nat → Nat → Bool) (a b d : Pt) : Decidable (AltCCW m psiLt a b d) :=
  inferInstanceAs (Decidable (_ ∧ _))
instance (m : Nat) (psiLt : Nat → Nat → Bool) (a b d : Pt) : Decidable (BlockCCW m psiLt a b d) :=
  inferInstanceAs (Decidable (_ ∧ _))
instance (m t i : Nat) (a : Pt) : Decidable (InQ m t i a) := inferInstanceAs (Decidable (_ ∧ _))
instance (a b d : Pt) : Decidable (Distinct3 a b d) := inferInstanceAs (Decidable (_ ∧ _))

/-! ## The model -/

/-- `chi a b d` means orient(P a, P b, P d) > 0; `psiLt i j` means ψ_i < ψ_j. -/
structure Model (m K t : Nat) where
  chi   : Pt → Pt → Pt → Bool
  psiLt : Nat → Nat → Bool
  psiLt_irrefl : ∀ i, psiLt i i = false
  psiLt_trans  : ∀ i j k, psiLt i j = true → psiLt j k = true → psiLt i k = true
  psiLt_total  : ∀ i j, i < t → j < t → i ≠ j → psiLt i j = true ∨ psiLt j i = true
  psiLt_zero   : ∀ i, 0 < i → i < t → psiLt 0 i = true
  chi_rot   : ∀ a b d, PtOk m t a → PtOk m t b → PtOk m t d →
                chi (rot m a) (rot m b) (rot m d) = chi a b d
  chi_cycle : ∀ a b d, PtOk m t a → PtOk m t b → PtOk m t d → Distinct3 a b d →
                chi b d a = chi a b d
  chi_swap  : ∀ a b d, PtOk m t a → PtOk m t b → PtOk m t d → Distinct3 a b d →
                chi a d b = !chi a b d
  ruleA : ∀ a b d, PtOk m t a → PtOk m t b → PtOk m t d → Distinct3 a b d →
            AltCCW m psiLt a b d → chi a b d = true
  ruleB : ∀ a b d, PtOk m t a → PtOk m t b → PtOk m t d → Distinct3 a b d →
            BlockCCW m psiLt a b d → b.1 ≤ a.1 → b.1 ≤ d.1 → chi a b d = true
  nest  : ∀ i j k, i < j → j < t → k < m → chi (i, 0) (i, 1) (j, k) = true
  noChain : ∀ i, i < t → ∀ q : Nat → Pt,
      (∀ s, s < K - 1 → InQ m t i (q s)) →
      (∀ s, s + 1 < K - 1 → chi (i, 0) (q s) (q (s + 1)) = true) →
      (∀ s, s + 2 < K - 1 → chi (q s) (q (s + 1)) (q (s + 2)) = true) → False

/-! ## The intended assignment -/

/-- A chain of length `l` for pivot `(i,0)` starting with `a, b` (KS:560-563). -/
def ChainFrom (m t : Nat) (chi : Pt → Pt → Pt → Bool) (i l : Nat) (a b : Pt) : Prop :=
  ∃ q : Nat → Pt, q 0 = a ∧ q 1 = b ∧ (∀ s, s < l → InQ m t i (q s)) ∧
    (∀ s, s + 1 < l → chi (i, 0) (q s) (q (s + 1)) = true) ∧
    (∀ s, s + 2 < l → chi (q s) (q (s + 1)) (q (s + 2)) = true)

/-- Values of the non-chain variables (computable; the early-warning test evaluates exactly this). -/
def baseVal (chi : Pt → Pt → Pt → Bool) (psiLt : Nat → Nat → Bool) : Var → Bool
  | .y i j => psiLt i j
  | .orb [a, b, d] => chi a b d
  | _ => false

/-- The intended assignment on variables. -/
def tauOf (m t : Nat) (chi : Pt → Pt → Pt → Bool) (psiLt : Nat → Nat → Bool) : Var → Prop
  | .f i l a b => ChainFrom m t chi i l a b
  | v => baseVal chi psiLt v = true

def Model.τ {m K t : Nat} (M : Model m K t) : Var → Prop := tauOf m t M.chi M.psiLt

/-- The assignment on codes, as `dimacsSat_of_holds` consumes it. -/
def Model.τc {m K t : Nat} (M : Model m K t) (n : Nat) : Prop := M.τ (decodeCode m K t n)

/-! ## Unit specifications
`OlitSpec`, `SortSpec`, `ObjLtSpec` are proved in U0 (`olitSpec`, `sortSpec`, `Obj.lt_iff`).
`OrbListSpec` is proved by U1 and `PatternSpec` by U4 (`patternSpec_of`); U3 takes both as hypotheses.
`WordSpec` is proved by U5 (`wordSpec`); U4 takes it as a hypothesis. -/

/-- **U0** (`olitSpec`). `olit` is the orientation literal. -/
def OlitSpec {m K t : Nat} (M : Model m K t) : Prop :=
  ∀ (P Q R : Pt) (l : Int), PtOk m t P → PtOk m t Q → PtOk m t R →
    olit m (orbVarC m t) P Q R = some l → l ≠ 0 ∧ (CodeLitHolds M.τc l ↔ M.chi P Q R = true)

/-- **U1** (`orbListSpec`). Orbit representatives are three distinct valid labels. -/
def OrbListSpec (m t : Nat) : Prop :=
  ∀ c ∈ orbList m t, ∃ a b d, c = [a, b, d] ∧ PtOk m t a ∧ PtOk m t b ∧ PtOk m t d ∧ Distinct3 a b d

/-- A rank that respects ψ on the layers of `c` (one direction suffices). -/
def RkMono (psiLt : Nat → Nat → Bool) (rk : Nat → Nat) (c : List Pt) : Prop :=
  ∀ x ∈ c, ∀ y ∈ c, rk x.1 < rk y.1 → psiLt x.1 y.1 = true

/-- **U4** (`patternSpec_of`). A pattern whose ranks respect ψ yields no literal or a true one. -/
def PatternSpec {m K t : Nat} (M : Model m K t) : Prop :=
  ∀ (a b d : Pt) (rk h : Nat → Nat) (l : Int), PtOk m t a → PtOk m t b → PtOk m t d → Distinct3 a b d →
    RkMono M.psiLt rk [a, b, d] →
    (patternLit m false (orbVarC m t) [a, b, d] (orbCode m t [a, b, d]) rk h).1 = some l →
    CodeLitHolds M.τc l

/-- **U0** (`sortSpec`). Insertion sort permutes, and sorts under a strict total order on the elements. -/
def SortSpec : Prop :=
  ∀ (α : Type) (lt : α → α → Bool) (l : List α),
    (insSort lt l).Perm l ∧
    (l.Nodup → (∀ x ∈ l, lt x x = false) →
      (∀ x ∈ l, ∀ y ∈ l, ∀ z ∈ l, lt x y = true → lt y z = true → lt x z = true) →
      (∀ x ∈ l, ∀ y ∈ l, x ≠ y → lt x y = true ∨ lt y x = true) →
      (insSort lt l).Pairwise (fun x y => lt x y = true))

/-- **U0** (`Obj.lt_iff`). `Obj.lt` is Python's tuple order. -/
def ObjLtSpec : Prop :=
  ∀ a b : Obj, Obj.lt a b = true ↔
    (a.J < b.J ∨ (a.J = b.J ∧ (a.r < b.r ∨ (a.r = b.r ∧
      (a.kind < b.kind ∨ (a.kind = b.kind ∧ a.idx < b.idx))))))

/-- The object `(label, is-point)` of a code entry `o` of the pattern of the triple `c` (gen_b2.py:110-111). -/
def objImg (c : List Pt) (o : Obj) : Pt × Bool := (c.getD o.idx (0, 0), o.kind == 1)

/-- What sorting the six code objects of `[a, b, d]` gives: they are the six objects of `a, b, d`, in `objLt` order. -/
structure SortedSix (m : Nat) (psiLt : Nat → Nat → Bool) (a b d : Pt) (S : List Obj) : Prop where
  length : S.length = 6
  sorted : S.Pairwise fun o o' => objLt m psiLt (objImg [a, b, d] o) (objImg [a, b, d] o')
  cover  : ∀ x ∈ objs6 a b d, x ∈ S.map (objImg [a, b, d])
  idx_lt : ∀ o ∈ S, o.idx < 3
  points : ((S.filter (·.kind == 1)).map (·.idx)).Perm [0, 1, 2]

/-- **U5** (`wordSpec`). The cyclic word of six sorted objects (gen_b2.py:119-130) gives the `Model`'s rule-A
pattern (alternating word) and rule-B pattern (any three cyclically consecutive points). -/
def WordSpec : Prop :=
  ∀ (m : Nat) (psiLt : Nat → Nat → Bool) (a b d : Pt) (S : List Obj),
    (∀ i, psiLt i i = false) → (∀ i j k, psiLt i j = true → psiLt j k = true → psiLt i k = true) →
    Distinct3 a b d → SortedSix m psiLt a b d S →
    ((S.map (·.kind) = [1, 0, 1, 0, 1, 0] ∨ S.map (·.kind) = [0, 1, 0, 1, 0, 1]) →
      AltCCW m psiLt
        ([a, b, d].getD (((S.filter (·.kind == 1)).map (·.idx)).getD 0 0) (0, 0))
        ([a, b, d].getD (((S.filter (·.kind == 1)).map (·.idx)).getD 1 0) (0, 0))
        ([a, b, d].getD (((S.filter (·.kind == 1)).map (·.idx)).getD 2 0) (0, 0))) ∧
    (∀ st, st < 6 → (S.map (·.kind)).getD (st % 6) 0 = 1 → (S.map (·.kind)).getD ((st + 1) % 6) 0 = 1 →
      (S.map (·.kind)).getD ((st + 2) % 6) 0 = 1 →
      BlockCCW m psiLt ([a, b, d].getD (S.getD (st % 6) default).idx (0, 0))
        ([a, b, d].getD (S.getD ((st + 1) % 6) default).idx (0, 0))
        ([a, b, d].getD (S.getD ((st + 2) % 6) default).idx (0, 0)))

end EncB
