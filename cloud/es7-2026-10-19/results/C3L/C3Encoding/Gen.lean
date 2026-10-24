import Std.Data.HashSet

/-!
# The C3a base CNF (`results/C3a/c3cnf.py`, chain variant), generated on the Lean side

`results/C3-S/tools/gen_case.py m k none` is `C3Enc(m, k).build()` with the defaults
`sb = True, xsig = False, gon = "chain", acy = False`. This file follows `C3Enc.__init__` and
`C3Enc.build` loop by loop; see `PLAN.md` for the variable and clause families.

Points are the labels `0, …, n-1`, `n = 3m`; the rotation is `R i = (i - m) mod n`.
Variables are numbered in the order Python allocates them:

* `C`: one variable per `R`-orbit of sorted triples (`_orbits` with the `eps` factor);
* `s[r]`, `r < m`;
* `inv(i,j)` and then `B(i,j)` for `i < j` in `itertools.combinations` order;
* `T`: one variable per `R`-orbit (`_orbits` with factor `1`);
* `Y(x,b,c)`, then `W(r,x,a,b)` for `2 ≤ r ≤ k-2`.

Literal tables are arrays indexed by `key3 n i j k = (i*n + j)*n + k` (value `0` = unset).
Clauses pass through `addCl` (= `C3Enc.add`: drop tautologies, distinct literals sorted by
absolute value). Only the string formatting in `Emit.lean` is outside this file.
-/

namespace C3

/-- `itertools.combinations(range(n), 2)`. -/
def pairs (n : Nat) : List (Nat × Nat) :=
  (List.range n).flatMap fun i => (List.range' (i + 1) (n - (i + 1))).map fun j => (i, j)

/-- `itertools.combinations(range(n), 3)`. -/
def triples (n : Nat) : List (Nat × Nat × Nat) :=
  (pairs n).flatMap fun (i, j) => (List.range' (j + 1) (n - (j + 1))).map fun k => (i, j, k)

/-- `itertools.combinations(range(n), 4)`. -/
def quads (n : Nat) : List (Nat × Nat × Nat × Nat) :=
  (triples n).flatMap fun (i, j, k) =>
    (List.range' (k + 1) (n - (k + 1))).map fun l => (i, j, k, l)

/-- `itertools.permutations(xs, 2)`. -/
def perms2 (xs : List Nat) : List (Nat × Nat) :=
  xs.flatMap fun a => (xs.filter (· != a)).map fun b => (a, b)

/-- The labels other than `x`. -/
def others (n x : Nat) : List Nat := (List.range n).filter (· != x)

def key3 (n i j k : Nat) : Nat := (i * n + j) * n + k

/-- `parity_sort`: the sorted triple and the sign of the sorting permutation. -/
def paritySort (a b c : Nat) : (Nat × Nat × Nat) × Int :=
  let inv := (if a > b then 1 else 0) + (if a > c then 1 else 0) + (if b > c then 1 else 0)
  let lo := min a (min b c)
  let hi := max a (max b c)
  ((lo, a + b + c - lo - hi, hi), if inv % 2 = 1 then -1 else 1)

/-- The rotation on labels, `R i = (i - m) mod 3m`. -/
def rot (m i : Nat) : Nat := (i + 2 * m) % (3 * m)

def eps (m i : Nat) : Int := if i < m then 1 else -1

/-- `C3Enc._orbits`: a literal for every sorted triple, one fresh variable per `R`-orbit,
starting after `nv0`. With `useEps` the factor is `eps i * eps j * eps k` (the `C` table),
otherwise `1` (the `T` table). Returns the table and the last variable used. -/
def orbits (m : Nat) (useEps : Bool) (nv0 : Nat) : Array Int × Nat := Id.run do
  let n := 3 * m
  let mut lit : Array Int := Array.replicate (n * n * n) 0
  let mut nv := nv0
  for (i, j, k) in triples n do
    if lit[key3 n i j k]! == 0 then
      nv := nv + 1
      lit := lit.set! (key3 n i j k) nv
      let mut cur := (i, j, k)
      let mut cl : Int := nv
      for _ in [0:3] do
        let (a, b, c) := cur
        let ((x, y, z), par) := paritySort (rot m a) (rot m b) (rot m c)
        let f : Int := if useEps then eps m a * eps m b * eps m c else 1
        let nl := par * f * cl
        if lit[key3 n x y z]! == 0 then
          lit := lit.set! (key3 n x y z) nl
        cur := (x, y, z)
        cl := nl
  return (lit, nv)

/-- The variables and literal tables of `C3Enc(m, k)` (everything `__init__` allocates). -/
structure Tables where
  m : Nat
  n : Nat
  /-- the `C` table (`chi'` per orbit) -/
  C : Array Int
  /-- number of `C` variables (`C_vars`) -/
  nC : Nat
  /-- `inv(i,j)`, indexed by `i*n + j` -/
  inv : Array Nat
  /-- `B(i,j)`, `i < j`, indexed by `i*n + j` -/
  Bv : Array Nat
  /-- the `T` table (`chi_S` per orbit) -/
  T : Array Int
  /-- last variable allocated by `__init__` -/
  nv : Nat

def mkTables (m : Nat) : Tables := Id.run do
  let n := 3 * m
  let (C, nC) := orbits m true 0
  let mut nv := nC + m
  let mut inv : Array Nat := Array.replicate (n * n) 0
  for (i, j) in pairs n do
    nv := nv + 1
    inv := inv.set! (i * n + j) nv
  let mut Bv : Array Nat := Array.replicate (n * n) 0
  for (i, j) in pairs n do
    nv := nv + 1
    Bv := Bv.set! (i * n + j) nv
  let (T, nv') := orbits m false nv
  return { m, n, C, nC, inv, Bv, T, nv := nv' }

namespace Tables
variable (E : Tables)

/-- `s[r]` -/
def s (r : Nat) : Int := E.nC + 1 + r

/-- `C3Enc.sig`: the literal "`sigma_i = 1`". -/
def sig (i : Nat) : Int := if i / E.m == 1 then -E.s (i % E.m) else E.s (i % E.m)

def Cl (i j k : Nat) : Int := E.C[key3 E.n i j k]!
def Tl (i j k : Nat) : Int := E.T[key3 E.n i j k]!
def invv (i j : Nat) : Int := E.inv[i * E.n + j]!
def Bvv (i j : Nat) : Int := E.Bv[i * E.n + j]!

/-- `C3Enc.B` -/
def B (p q : Nat) : Int := if p < q then E.Bvv p q else -E.Bvv q p

/-- `C3Enc.ccw` -/
def ccw (p q r : Nat) : Int :=
  let ((a, b, c), par) := paritySort p q r
  par * E.Tl a b c

end Tables

/-- `C3Enc.add`: `none` for a tautology, else the distinct literals sorted by `abs`. -/
def addCl (c : List Int) : Option (List Int) :=
  if c.any fun l => c.contains (-l) then none
  else some (c.eraseDups.mergeSort fun a b => a.natAbs ≤ b.natAbs)

/-- Push `addCl c` (if not a tautology). -/
def push (acc : Array (List Int)) (c : List Int) : Array (List Int) :=
  match addCl c with
  | some d => acc.push d
  | none => acc

/-- `C3Enc.xor0`: clauses for "an even number of `lits` is true". `cnt` keeps the absolute
values in first-occurrence order (as a Python dict does), `const` the number of negative
literals mod 2. -/
def xor0 (acc : Array (List Int)) (lits : List Int) : Array (List Int) := Id.run do
  let mut cnt : Array (Nat × Bool) := #[]
  let mut const := false
  for l in lits do
    if l < 0 then const := !const
    match cnt.findIdx? (·.1 == l.natAbs) with
    | some p => cnt := cnt.modify p fun (v, c) => (v, !c)
    | none => cnt := cnt.push (l.natAbs, true)
  let vs := (cnt.filter (·.2)).toList.map (·.1)
  let L := vs.length
  let mut acc := acc
  for b in [0:2 ^ L] do
    -- `itertools.product((0, 1), repeat=L)`: the first variable is the most significant bit
    let bits := (List.range L).map fun p => (b >>> (L - 1 - p)) % 2 == 1
    if ((bits.filter id).length % 2 == 1) != const then
      acc := push acc ((vs.zip bits).map fun (v, bt) => if bt then -(v : Int) else v)
  if L == 0 && const then acc := acc.push []
  return acc

/-- Section `sig`: signotope axioms on `chi'`; clauses equal as sorted tuples are written once. -/
def secSig (E : Tables) (acc : Array (List Int)) : Array (List Int) := Id.run do
  let mut acc := acc
  let mut seen : Std.HashSet (List Int) := {}
  for (i, j, k, l) in quads E.n do
    let s : Array Int := #[E.Cl i j k, E.Cl i j l, E.Cl i k l, E.Cl j k l]
    for (p, q, r) in triples 4 do
      for c in [[-s[p]!, s[q]!, -s[r]!], [s[p]!, -s[q]!, s[r]!]] do
        let key := c.mergeSort fun a b => a ≤ b
        if !seen.contains key then
          seen := seen.insert key
          acc := push acc c
  return acc

/-- Section `sb`: `sigma_0 = 0`. -/
def secSb (E : Tables) (acc : Array (List Int)) : Array (List Int) := push acc [-E.sig 0]

/-- Section `prefix`. -/
def secPrefix (E : Tables) (acc : Array (List Int)) : Array (List Int) :=
  (triples E.n).foldl (init := acc) fun acc (i, j, k) =>
    let c := E.Cl i j k
    let a := E.invv i j
    let b := E.invv i k
    let d := E.invv j k
    push (push (push (push acc [-c, -b, a]) [-c, -d, b]) [c, -b, d]) [c, -a, b]

/-- Section `forced`. -/
def secForced (E : Tables) (acc : Array (List Int)) : Array (List Int) :=
  (pairs E.n).foldl (init := acc) fun acc (i, j) =>
    let si := E.sig i
    let sj := E.sig j
    let v := E.invv i j
    push (push acc [si, -sj, v]) [-si, sj, -v]

/-- Section `xorB`: `B_ij = inv_ij xor sigma_i xor sigma_j`. -/
def secXorB (E : Tables) (acc : Array (List Int)) : Array (List Int) :=
  (pairs E.n).foldl (init := acc) fun acc (i, j) =>
    xor0 acc [E.Bvv i j, E.invv i j, E.sig i, E.sig j]

/-- Section `xorT`: `T = C xor sigma_i xor sigma_j xor sigma_k`, once per `T`-variable, at the
first triple (in dict order = lexicographic order of the orbit representatives) carrying it. -/
def secXorT (E : Tables) (acc : Array (List Int)) : Array (List Int) := Id.run do
  let mut acc := acc
  let mut done : Std.HashSet Nat := {}
  for (i, j, k) in triples E.n do
    let tl := E.Tl i j k
    if !done.contains tl.natAbs then
      done := done.insert tl.natAbs
      acc := xor0 acc [tl, E.Cl i j k, E.sig i, E.sig j, E.sig k]
  return acc

/-- The chain variables: `Y(x,b,c)` from `E.nv + 1`, then `W(r,x,a,b)`, `2 ≤ r ≤ k-2`.
`Y` is indexed by `key3`, `W` by `(r - 2) * n^3 + key3`. Returns the last variable. -/
def chainVars (E : Tables) (k : Nat) : Array Nat × Array Nat × Nat := Id.run do
  let n := E.n
  let mut nv := E.nv
  let mut Y : Array Nat := Array.replicate (n * n * n) 0
  for x in List.range n do
    for (b, c) in perms2 (others n x) do
      nv := nv + 1
      Y := Y.set! (key3 n x b c) nv
  let mut W : Array Nat := Array.replicate ((k - 3) * n * n * n) 0
  for r in List.range' 2 (k - 3) do
    for x in List.range n do
      for (a, b) in perms2 (others n x) do
        nv := nv + 1
        W := W.set! ((r - 2) * n * n * n + key3 n x a b) nv
  return (Y, W, nv)

/-- Sections `Y`, `W`, `gon` (the `gon` bodies are collected during `W` and written last). -/
def secChain (E : Tables) (k : Nat) (acc : Array (List Int)) : Array (List Int) := Id.run do
  let n := E.n
  let (Y, W, _) := chainVars E k
  let y := fun x b c => (Y[key3 n x b c]! : Int)
  let w := fun r x a b => (W[(r - 2) * n * n * n + key3 n x a b]! : Int)
  let mut acc := acc
  for x in List.range n do
    for (b, c) in perms2 (others n x) do
      acc := push acc [-E.B x c, -E.ccw x b c, y x b c]
  for x in List.range n do
    for (a, b) in perms2 (others n x) do
      acc := push acc [-E.B x a, -y x a b, w 2 x a b]
  let mut gon : Array (List Int) := #[]
  for r in List.range' 2 (k - 3) do
    for x in List.range n do
      let os := others n x
      for (a, b) in perms2 os do
        for c in os do
          if c != a && c != b then
            let body := [-w r x a b, -y x b c, -E.ccw a b c]
            if r + 1 ≤ k - 2 then
              acc := push acc (body ++ [w (r + 1) x b c])
            else
              gon := gon.push body
  for g in gon do
    acc := push acc g
  return acc

/-- Number of variables of `C3Enc(m, k)` after `build()`. -/
def numVars (m k : Nat) : Nat := (chainVars (mkTables m) k).2.2

/-- The clause list of `gen_case.py m k none` (= `C3Enc(m, k).build()`). -/
def baseClauses (m k : Nat) : Array (List Int) :=
  let E := mkTables m
  secChain E k <| secXorT E <| secXorB E <| secForced E <| secPrefix E <| secSb E <|
    secSig E #[]

end C3
