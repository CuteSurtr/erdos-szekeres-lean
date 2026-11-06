/-!
# Encoder B in Lean: a port of `C6UPPER/encb/gen_b2.py`

`EncB.gen m K t` computes the clause list that `gen_b2.py m K t OUT` writes (gen_b2.py SHA-256
`3d47459a9723b5f7344205f3f2d7463e0be00b41c5070155e5da8dbf78fd40ba`): the same variables with the same
numbers, the same clauses in the same order, and the literals of each clause in the same order.
`EncB/Emit.lean` prints it in gen_b2.py's DIMACS layout. Both branches are ported: odd m (with the
half-sector variables `Hb`) and even m.

How the Python data structures are mirrored:
* a label `(i, k)` is `Pt := Nat × Nat`; Python's `<` on tuples and lists is `ptLt` / `lexLt`;
* `sorted` is a stable insertion sort `insSort`; every list sorted here has pairwise distinct entries
  (labels of a triple, the objects `((J, rank), kind, idx)`, layer numbers after `set`), so any correct
  sort gives Python's result;
* `itertools.combinations(_, 2)`, `combinations(_, 3)`, `permutations(range(n))` and
  `product([0, 1], repeat=n)` are `pairs`, `triples`, `perms`, `bitTuples`, each in itertools' order;
* a Python dict is an `Array` indexed by a code of the key that is injective on the keys that occur
  (labels have layer `< t` and sector `< m`); the entry 0 means "key absent", which is safe because every
  stored value is a nonzero variable or literal. Where Python *iterates* a dict (`orb`, `okpair`), the
  insertion order is kept in a separate `Array` (`orbList`, `okList`); the dicts `F`, `forced`, `Yv`,
  `Hv` are only looked up. Each key is inserted once, so insertion order is loop order;
* the counter `nv` with `new()` is a mutable `nv` in `Id.run do`; `fv` (gen_b2.py:161-165) is inlined
  where it is called, in the same position relative to the clause it belongs to.

Where gen_b2.py raises (its `assert`s, a `KeyError`, the `RuntimeError` of `olit`, and the nesting
`RuntimeError('conflict')`), the port drops the literal or clause and counts the event in `bad` (or sets
`conflict`); the emitter then refuses to print, so its observable behaviour matches Python's crash.
`bad` stays 0 whenever m ≥ 2 (all labels of a triple are distinct). On the tested grid gen_b2.py raises exactly on
(m,K,t) = (2,4,3), (2,5,4) (nesting conflict) and (1,4,2) (`KeyError`), and the port refuses exactly these.

Python's floats are not involved: gen_b2.py computes the angular configuration with integers only
(`J = 2k + h` or `J = k`, ranks, `%`, `//`), and so does this port.

Everything is a plain total `def` (structural recursion or `for` over lists): no `partial`, `unsafe`,
`implemented_by`, `extern` or `native_decide` in this package, so the exe runs the definition the kernel
reduces (trusting the Lean compiler and core's `Array`/`List`/`String` runtime code, as for any `lake exe`).
-/

namespace EncB

/-- A label `(i, k)`: layer `i` (0 = outermost), direction sector `k`. -/
abbrev Pt := Nat × Nat

/-- Python's `range(a, b)`. -/
def rng (a b : Nat) : List Nat := List.range' a (b - a)

/-- Python's `<` on `(i, k)` tuples. -/
def ptLt (a b : Pt) : Bool := a.1 < b.1 || (a.1 == b.1 && a.2 < b.2)

/-- Python's `<` on lists for an element order `lt`: lexicographic, a proper prefix is smaller. -/
def lexLt {α : Type} [BEq α] (lt : α → α → Bool) : List α → List α → Bool
  | [], [] => false
  | [], _ :: _ => true
  | _ :: _, [] => false
  | a :: as, b :: bs => lt a b || (a == b && lexLt lt as bs)

/-- Insert `x` before the first entry that is not smaller than `x`. -/
def insertBy {α : Type} (lt : α → α → Bool) (x : α) : List α → List α
  | [] => [x]
  | y :: ys => if lt y x then y :: insertBy lt x ys else x :: y :: ys

/-- Stable insertion sort (Python's `sorted` is stable as well). -/
def insSort {α : Type} (lt : α → α → Bool) (l : List α) : List α :=
  l.foldr (insertBy lt) []

/-- `itertools.combinations(l, 2)`. -/
def pairs {α : Type} : List α → List (α × α)
  | [] => []
  | x :: xs => xs.map (fun y => (x, y)) ++ pairs xs

/-- `itertools.combinations(l, 3)`. -/
def triples {α : Type} : List α → List (α × α × α)
  | [] => []
  | x :: xs => (pairs xs).map (fun yz => (x, yz.1, yz.2)) ++ triples xs

/-- `itertools.permutations(l)` for `l` increasing and duplicate-free: lexicographic order.
The first argument is fuel, equal to `l.length` at the top call. -/
def permsAux : Nat → List Nat → List (List Nat)
  | 0, _ => [[]]
  | fuel + 1, l => l.flatMap fun x => (permsAux fuel (l.erase x)).map (x :: ·)

/-- `itertools.permutations(l)`, `l` increasing. -/
def perms (l : List Nat) : List (List Nat) := permsAux l.length l

/-- `itertools.product([0, 1], repeat=n)`: the last coordinate changes fastest. -/
def bitTuples : Nat → List (List Nat)
  | 0 => [[]]
  | n + 1 => [0, 1].flatMap fun b => (bitTuples n).map (b :: ·)

/-- `perm_sign` (gen_b2.py:56-62): `(-1) ^ (number of inversions)`. -/
def permSign (a : List Nat) : Int :=
  if (pairs a).countP (fun xy => decide (xy.2 < xy.1)) % 2 == 0 then 1 else -1

/-- Python's `(-k) % m` (for `m > 0`). -/
def negMod (m k : Nat) : Nat := (m - k % m) % m

/-- `[(i, (k + s) % m) for (i, k) in tri]` with `s = (-k0) % m` (gen_b2.py:45-46, 68-69), unsorted. -/
def rotate (m k0 : Nat) (tri : List Pt) : List Pt :=
  let s := negMod m k0
  tri.map fun p => (p.1, (p.2 + s) % m)

/-- `canon` (gen_b2.py:42-49): the smallest sorted rotation that moves one of the labels to sector 0. -/
def canon (m : Nat) (tri : List Pt) : List Pt :=
  let step (best : Option (List Pt)) (p0 : Pt) : Option (List Pt) :=
    let rt := insSort ptLt (rotate m p0.2 tri)
    match best with
    | none => some rt
    | some b => if lexLt ptLt rt b then some rt else some b
  (tri.foldl step none).getD []

/-- `olit` (gen_b2.py:63-76): the literal of `orient(P, Q, R) = +`. `orbVar c` is `orb[c]`.
`none` where Python raises (no rotation matches, or `c` is not a key of `orb`); for three distinct
labels neither happens. -/
def olit (m : Nat) (orbVar : List Pt → Option Nat) (P Q R : Pt) : Option Int :=
  let tri := [P, Q, R]
  let c := canon m tri
  match tri.find? (fun p0 => insSort ptLt (rotate m p0.2 tri) == c) with
  | none => none
  | some p0 =>
    let rt := rotate m p0.2 tri
    -- `order = sorted(range(3), key=lambda r: rt[r])`
    let order := (insSort (fun x y => ptLt x.1 y.1) (rt.zip [0, 1, 2])).map (·.2)
    match orbVar c with
    | none => none
    | some v => some (if permSign order > 0 then (v : Int) else -(v : Int))

/-- An entry `((J, rank), kind, idx)` of `objs` (gen_b2.py:110-111). `kind` is 0 for `'A'` (antipode)
and 1 for `'P'` (point); Python compares the characters, and `'A' < 'P'`. -/
structure Obj where
  J : Nat
  r : Nat
  kind : Nat
  idx : Nat
  deriving BEq, Inhabited

/-- Python's `<` on `((J, r), kind, idx)`. -/
def Obj.lt (a b : Obj) : Bool :=
  lexLt (fun x y => decide (x < y)) [a.J, a.r, a.kind, a.idx] [b.J, b.r, b.kind, b.idx]

/-- One pattern of orbit `c` with variable `v` (gen_b2.py:103-133), given the ranks `rk` and the
half-sector bits `h`: the literal (`none` = no clause) and the number of Python assertion failures. -/
def patternLit (m : Nat) (odd : Bool) (orbVar : List Pt → Option Nat) (c : List Pt) (v : Nat)
    (rk h : Nat → Nat) : Option Int × Nat :=
  -- gen_b2.py:104-111  points and antipodes as keys (J, rank)
  let objs : List Obj := (c.zip (List.range c.length)).flatMap fun pi =>
    let (p, idx) := pi
    let (J, Ja) :=
      if odd then
        let J := (2 * p.2 + h p.1) % (2 * m)
        (J, (J + m) % (2 * m))
      else (p.2, (p.2 + m / 2) % m)
    [⟨J, rk p.1, 1, idx⟩, ⟨Ja, rk p.1, 0, idx⟩]
  let keys := objs.map fun o => (o.J, o.r)
  -- gen_b2.py:113-116  `len(set(keys)) < 6`: no clause (`assert not odd`)
  if (pairs keys).any (fun kk => kk.1 == kk.2) then
    (none, if odd then 1 else 0)
  else
    -- gen_b2.py:118-119
    let objs := insSort Obj.lt objs
    let kinds := objs.map (·.kind)
    let v' : Int := v
    if kinds == [1, 0, 1, 0, 1, 0] || kinds == [0, 1, 0, 1, 0, 1] then
      -- gen_b2.py:121-124  rule A: sign of the ccw order of the three points
      let seq := (objs.filter (·.kind == 1)).map (·.idx)
      (some (if permSign seq > 0 then v' else -v'), 0)
    else
      -- gen_b2.py:126-128  `st = (kinds + kinds).find('PPP')`: the first cyclic start of three P's
      let isP (x : Nat) : Bool := kinds.getD (x % 6) 0 == 1
      match (List.range 6).find? (fun x => isP x && isP (x + 1) && isP (x + 2)) with
      | none => (none, 1)
      | some st =>
        -- gen_b2.py:129-132  rule B, emitted only if the middle point is outermost
        let seq := [0, 1, 2].map fun r => (objs.getD ((st + r) % 6) default).idx
        let a := c.getD (seq.getD 0 0) (0, 0)
        let b := c.getD (seq.getD 1 0) (0, 0)
        let cc := c.getD (seq.getD 2 0) (0, 0)
        if decide (b.1 ≤ a.1) && decide (b.1 ≤ cc.1) then
          match olit m orbVar a b cc with
          | none => (none, 1)
          | some l => (some l, 0)
        else (none, 0)

/-- All patterns of orbit `c` with variable `v` (gen_b2.py:86-133): the list `outs` of
(premise literals, literal), in Python's order, and the number of Python assertion failures. -/
def angOuts (m : Nat) (odd : Bool) (yv : Nat → Nat → Int) (hv : Nat → Int)
    (orbVar : List Pt → Option Nat) (c : List Pt) (v : Nat) : List (List Int × Option Int) × Nat :=
  -- gen_b2.py:86-87
  let Ls := insSort (fun a b => decide (a < b)) (c.map (·.1)).eraseDups
  let free := Ls.filter (· != 0)
  let res := (perms (List.range free.length)).flatMap fun ranks =>
    -- gen_b2.py:90-91  rk = {L: r + 1 for L, r in zip(free, ranks)}; rk[0] = 0
    let rk (L : Nat) : Nat :=
      if L == 0 then 0 else ((List.lookup L (free.zip ranks)).map (· + 1)).getD 0
    (bitTuples (if odd then free.length else 0)).map fun hb =>
      -- gen_b2.py:93-94  h = {L: b for L, b in zip(free, hb)}; h[0] = 0
      let h (L : Nat) : Nat := if L == 0 then 0 else (List.lookup L (free.zip hb)).getD 0
      -- gen_b2.py:96-102  premise literals
      let prem : List Int :=
        (pairs free).map (fun ab =>
          let (a_, b_) := ab
          let lit := if a_ < b_ then yv a_ b_ else yv b_ a_
          let truth := if a_ < b_ then decide (rk a_ < rk b_) else decide (rk b_ < rk a_)
          if truth then lit else -lit)
        ++ (if odd then free.map (fun L => if h L == 0 then hv L else -(hv L)) else [])
      let (lit, nbad) := patternLit m odd orbVar c v rk h
      ((prem, lit), nbad)
  (res.map (·.1), (res.map (·.2)).sum)

/-- gen_b2.py:134-135: the common literal when every pattern gives the same literal (never `None`). -/
def unitOf (outs : List (List Int × Option Int)) : Option Int :=
  match outs with
  | (_, some l) :: rest => if rest.all (fun o => o.2 == some l) then some l else none
  | _ => none

/-- Index of a label in the arrays below (injective for layer `< t`, sector `< m`). -/
def ptCode (m : Nat) (p : Pt) : Nat := p.1 * m + p.2

/-- Index of a sorted triple in the orbit table of size `N ^ 3`, `N = t * m`. -/
def triCode (m N : Nat) : List Pt → Nat
  | [a, b, c] => (ptCode m a * N + ptCode m b) * N + ptCode m c
  | _ => N * N * N

/-- What `gen_b2.py m K t` computes. -/
structure Result where
  /-- the final value of the counter `nv[0]` -/
  nv : Nat
  /-- `cls`, in order -/
  clauses : Array (List Int)
  /-- `Yv[(i, j)]` at index `i * t + j` (0 = absent) -/
  ytab : Array Nat
  nunit : Nat
  ncond : Nat
  nchain : Nat
  /-- events where gen_b2.py raises (0 on every instance it accepts) -/
  bad : Nat
  /-- gen_b2.py:148-149 `RuntimeError('conflict')` -/
  conflict : Bool

/-- Encoder B: `gen_b2.py m K t` (gen_b2.py:27-190). -/
def gen (m K t : Nat) : Result := Id.run do
  let odd := m % 2 == 1
  let mut nv : Nat := 0
  -- gen_b2.py:36-39  Y'(i, j) = [psi_i < psi_j], 1 ≤ i < j < t
  let mut ytab : Array Nat := Array.replicate (t * t) 0
  for i in rng 1 t do
    for j in rng (i + 1) t do
      nv := nv + 1
      ytab := ytab.setIfInBounds (i * t + j) nv
  -- gen_b2.py:40  Hb(i) = [theta_i < pi/m], 1 ≤ i < t, odd m only
  let mut htab : Array Nat := Array.replicate t 0
  if odd then
    for i in rng 1 t do
      nv := nv + 1
      htab := htab.setIfInBounds i nv
  let ytabF := ytab
  let htabF := htab
  let yv (i j : Nat) : Int := (ytabF.getD (i * t + j) 0 : Nat)
  let hv (i : Nat) : Int := (htabF.getD i 0 : Nat)
  -- gen_b2.py:50-55  one variable per rotation orbit of label triples, in order of first appearance
  let N := t * m
  let pts : List Pt := (rng 0 t).flatMap fun i => (rng 0 m).map fun k => (i, k)
  let mut orbTab : Array Nat := Array.replicate (N * N * N) 0
  let mut orbList : Array (List Pt × Nat) := #[]
  for xyz in triples pts do
    let (x, y, z) := xyz
    let c := canon m [x, y, z]
    let code := triCode m N c
    if orbTab.getD code 0 == 0 then
      nv := nv + 1
      orbTab := orbTab.setIfInBounds code nv
      orbList := orbList.push (c, nv)
  let orbTabF := orbTab
  let orbVar (c : List Pt) : Option Nat :=
    let v := orbTabF.getD (triCode m N c) 0
    if v == 0 then none else some v
  let mut cls : Array (List Int) := #[]
  -- gen_b2.py:79-81  psi order transitivity
  for ijk in triples (rng 1 t) do
    let (i, j, k) := ijk
    cls := cls.push [-(yv i j), -(yv j k), yv i k]
    cls := cls.push [yv i j, yv j k, -(yv i k)]
  -- gen_b2.py:83-141  exact angular configurations, orbits in insertion order
  let mut forced : Array Int := Array.replicate (nv + 1) 0
  let mut nunit := 0
  let mut ncond := 0
  let mut bad := 0
  for cv in orbList do
    let (c, v) := cv
    let (outs, nb) := angOuts m odd yv hv orbVar c v
    bad := bad + nb
    match unitOf outs with
    | some l =>
      -- gen_b2.py:136-137
      cls := cls.push [l]
      forced := forced.setIfInBounds l.natAbs l
      nunit := nunit + 1
    | none =>
      -- gen_b2.py:139-141
      for o in outs do
        match o.2 with
        | some l =>
          cls := cls.push (o.1.map (fun x => -x) ++ [l])
          ncond := ncond + 1
        | none => pure ()
  -- gen_b2.py:143-150  nesting units
  let mut conflict := false
  for i in rng 0 t do
    for j in rng (i + 1) t do
      for k in rng 0 m do
        match olit m orbVar (i, 0) (i, 1) (j, k) with
        | none => bad := bad + 1
        | some l =>
          cls := cls.push [l]
          let f := forced.getD l.natAbs 0
          if f != 0 && f != l then conflict := true
          forced := forced.setIfInBounds l.natAbs l
  -- gen_b2.py:151-153
  let forcedF := forced
  let isFalse (l : Int) : Bool :=
    let f := forcedF.getD l.natAbs 0
    f != 0 && f == -l
  -- gen_b2.py:155-190  backward chains, pivot p = (i, 0) for each layer i
  let mut nchain := 0
  let L := K - 1
  let FL := max L 3  -- levels held by the array `F`: 0 .. FL - 1 (every level that occurs)
  for i in rng 0 t do
    let p : Pt := (i, 0)
    -- gen_b2.py:159
    let Q : List Pt := ((rng i t).flatMap fun j => (rng 0 m).map fun k => (j, k)).filter (· != p)
    let pc (a b : Pt) : Nat := ptCode m a * N + ptCode m b
    let fc (l : Nat) (a b : Pt) : Nat := (l * N + ptCode m a) * N + ptCode m b
    -- gen_b2.py:160  F = {} for each pivot
    let mut F : Array Nat := Array.replicate (FL * N * N) 0
    -- gen_b2.py:166-172  okpair, insertion order kept in okList
    let mut okArr : Array Int := Array.replicate (N * N) 0
    let mut okList : Array (Pt × Pt × Int) := #[]
    for a in Q do
      for b in Q do
        if a != b then
          match olit m orbVar p a b with
          | none => bad := bad + 1
          | some l =>
            if !isFalse l then
              okArr := okArr.setIfInBounds (pc a b) l
              okList := okList.push (a, b, l)
    -- gen_b2.py:174-175  o(p,a,b) => F_2(a,b):  [fv(2, a, b), -l]
    for e in okList do
      let (a, b, l) := e
      let mut f := F.getD (fc 2 a b) 0
      if f == 0 then
        nv := nv + 1
        F := F.setIfInBounds (fc 2 a b) nv
        f := nv
      cls := cls.push [(f : Int), -l]
      nchain := nchain + 1
    -- gen_b2.py:176-190  F_lev(b,c) & o(p,a,b) & o(a,b,c) => F_{lev+1}(a,b)  (closing when lev + 1 = L)
    for lev in rng 2 L do
      for e in okList do
        let (b, c, _) := e
        let fbc := F.getD (fc lev b c) 0
        if fbc == 0 then continue
        for a in Q do
          if a == b || a == c then continue
          let lab := okArr.getD (pc a b) 0
          if lab == 0 then continue
          match olit m orbVar a b c with
          | none => bad := bad + 1
          | some lt =>
            if isFalse lt then continue
            if lev + 1 < L then
              let mut f := F.getD (fc (lev + 1) a b) 0
              if f == 0 then
                nv := nv + 1
                F := F.setIfInBounds (fc (lev + 1) a b) nv
                f := nv
              cls := cls.push [-(fbc : Int), -lab, -lt, (f : Int)]
            else
              cls := cls.push [-(fbc : Int), -lab, -lt]
            nchain := nchain + 1
  return { nv, clauses := cls, ytab := ytabF, nunit, ncond, nchain, bad, conflict }

end EncB
