import AE33Enc.Basic

/-!
# AE33Enc.Clause: descriptors and the validity-checking clause builder `clauseOf` (Std-only)

A descriptor names one clause of l2enc's families together with the witness its soundness needs (DESIGN.md D1, D2,
§2). `clauseOf B d` checks the witness in B's integer orientation signs and returns the clause, in l2enc's literal
order, or `none`. Every returned literal is nonzero with `natAbs ≤ numVars B` (`bounded`), so the rendering parses
back (`EncB.parseDimacs_render`). Soundness (Mathlib side) is proved for every descriptor `clauseOf` accepts; the
generator `gen` (AE33Enc.Gen) only chooses which descriptors, in which order.
-/

namespace AE33

inductive Desc where
  /-- R2 (l2enc.cpp:133-159), new point `n + w`: S_t = ε_t · chi(a, t, n + w); `pol = false`: `[-Sx, Sy, -Sz]`,
  `pol = true`: `[Sx, -Sy, Sz]`. Witness: the three ε-weighted cone signs. -/
  | r2 (w a x y z : Nat) (ex ey ez : Int) (pol : Bool)
  /-- AC (l2enc.cpp:160-168): `[σ·chi(a,b,t), σ·chi(b,c,t), σ·chi(c,a,t)]`, σ = sign[abc], t = n + w. -/
  | ac (w a b c : Nat)
  /-- RAD (l2enc.cpp:221-227): forbid the term signs `sg` of (chi(b,p,q), chi(a,p,q), chi(a,b,q), chi(a,b,p)). -/
  | rad (a b : Nat) (sg : List Int)
  /-- GP (l2enc.cpp:215-220): forbid the term signs `sg` of the 3-term relation with pivot `e`. -/
  | gp (e f g h i : Nat) (sg : List Int)
  /-- OCT (l2enc.cpp:239-248), new point `n + w`: hexagon `q` with visible edge (q5, q0). -/
  | oct (w : Nat) (q : List Nat)
  /-- JK (l2enc.cpp:250-284): pentagon `Q` (ccw), slot `i` of p, edge `j` of Q1 for q. -/
  | jk (Q : List Nat) (i j : Nat)
  deriving Inhabited

def isUnit (e : Int) : Bool := e == 1 || e == -1

/-- Every literal nonzero with `natAbs ≤ nv`. -/
def bounded (nv : Nat) (cl : List Int) : Bool := cl.all fun l => l != 0 && decide (l.natAbs ≤ nv)

/-- `std::unique` on a sorted list: adjacent duplicates removed. -/
def dedupAdj : List Int → List Int
  | [] => []
  | a :: rest =>
    match rest with
    | [] => [a]
    | b :: _ => if a == b then dedupAdj rest else a :: dedupAdj rest

/-- `std::sort` then `std::unique` (ascending signed values). -/
def sortLits (l : List Int) : List Int := dedupAdj (l.mergeSort fun a b => decide (a ≤ b))

def taut (cl : List Int) : Bool := cl.any fun l => cl.contains (-l)

/-- All increasing index triples of `q` have orientation sign +1 in `B` (a ccw convex polygon). -/
def ccwOk (B : Array Pt) (q : List Nat) : Bool :=
  (List.range q.length).all fun i => (List.range q.length).all fun j => (List.range q.length).all fun k =>
    !(decide (i < j) && decide (j < k)) || osgn B (q.getD i 0) (q.getD j 0) (q.getD k 0) == 1

def radPred (s : List Int) : Bool :=
  match s with
  | [s0, s1, s2, s3] => s0 == -s1 && -s1 == s2 && s2 == -s3
  | _ => false

def gpPred (s : List Int) : Bool :=
  match s with
  | [s0, s1, s2, s3, s4, s5] => s0 * s1 == -s2 * s3 && -s2 * s3 == s4 * s5
  | _ => false

/-- The clause forbidding the term signs `sg`: one literal per literal term (`-ℓ` if the sign is +1, `ℓ` if −1),
sorted and adjacent-unique (l2enc's `forbid_terms` without shortening). Requires `pred sg` and every constant term
equal to its sign. -/
def forbidClause (nv : Nat) (terms : List Term) (sg : List Int) (pred : List Int → Bool) : Option (List Int) :=
  if terms.length == sg.length && sg.all isUnit && pred sg &&
      (terms.zip sg).all (fun ts => match ts.1 with | .const c => c == ts.2 | .lit _ => true) then
    let cl := sortLits ((terms.zip sg).filterMap fun ts =>
      match ts.1 with
      | .lit l => some (if ts.2 == 1 then -l else l)
      | .const _ => none)
    if bounded nv cl && !cl.isEmpty then some cl else none
  else none

/-- The JK clause for pentagon `Q`, slot `i`, edge `j` (l2enc.cpp:250-284), without the witness check. -/
def jkClause (B : Array Pt) (Q : List Nat) (i j : Nat) : Option (List Int) :=
  let n := B.size
  let qa := Q.getD ((i + 4) % 5) 0
  let qb := Q.getD i 0
  let qc := Q.getD ((i + 1) % 5) 0
  let qd := Q.getD ((i + 2) % 5) 0
  let Q1 := Q.take (i + 1) ++ [n] ++ Q.drop (i + 1)
  let u := Q1.getD ((j + 5) % 6) 0
  let v := Q1.getD j 0
  let w := Q1.getD ((j + 1) % 6) 0
  let z := Q1.getD ((j + 2) % 6) 0
  match (chi B qb qc n).neg, chi B qa qb n, chi B qc qd n,
      (chi B v w (n + 1)).neg, chi B u v (n + 1), chi B w z (n + 1) with
  | .lit c1, .lit c2, .lit c3, .lit c4, .lit c5, .lit c6 =>
    let cl := sortLits [-c1, -c2, -c3, -c4, -c5, -c6]
    if taut cl || cl.isEmpty || !bounded (numVars B) cl then none else some cl
  | _, _, _, _, _, _ => none

/-- **The clause of a descriptor**, if its witness checks out in `B`. -/
def clauseOf (B : Array Pt) (d : Desc) : Option (List Int) :=
  let n := B.size
  let nv := numVars B
  match d with
  | .r2 w a x y z ex ey ez pol =>
    if decide (w < 2) && decide (a < n) && decide (x < n) && decide (y < n) && decide (z < n) &&
        a != x && a != y && a != z && x != y && y != z && x != z &&
        isUnit ex && isUnit ey && isUnit ez &&
        ex * ey * osgn B a x y == 1 && ey * ez * osgn B a y z == 1 && ex * ez * osgn B a x z == 1 then
      match chi B a x (n + w), chi B a y (n + w), chi B a z (n + w) with
      | .lit lx, .lit ly, .lit lz =>
        let cl := if pol then [ex * lx, -(ey * ly), ez * lz] else [-(ex * lx), ey * ly, ez * lz]
        if bounded nv cl then some cl else none
      | _, _, _ => none
    else none
  | .ac w a b c =>
    if decide (w < 2) && decide (a < n) && decide (b < n) && decide (c < n) && a != b && b != c && a != c &&
        isUnit (osgn B a b c) then
      match chi B a b (n + w), chi B b c (n + w), chi B c a (n + w) with
      | .lit l1, .lit l2, .lit l3 =>
        let s := osgn B a b c
        let cl := [s * l1, s * l2, s * l3]
        if bounded nv cl then some cl else none
      | _, _, _ => none
    else none
  | .rad a b sg =>
    if decide (a < n) && decide (b < n) && a != b then
      forbidClause nv [chi B b n (n + 1), chi B a n (n + 1), chi B a b (n + 1), chi B a b n] sg radPred
    else none
  | .gp e f g h i sg =>
    if decide (e < n + 2) && decide (f < n + 2) && decide (g < n + 2) && decide (h < n + 2) &&
        decide (i < n + 2) && decide [e, f, g, h, i].Nodup then
      forbidClause nv [chi B e f g, chi B e h i, chi B e f h, chi B e g i, chi B e f i, chi B e g h] sg gpPred
    else none
  | .oct w q =>
    match q with
    | [q0, q1, _, _, q4, q5] =>
      if decide (w < 2) && q.all (fun t => decide (t < n)) && decide q.Nodup && ccwOk B q then
        match chi B q5 q0 (n + w), chi B q4 q5 (n + w), chi B q0 q1 (n + w) with
        | .lit l1, .lit l2, .lit l3 =>
          let cl := [l1, -l2, -l3]
          if bounded nv cl then some cl else none
        | _, _, _ => none
      else none
    | _ => none
  | .jk Q i j =>
    if Q.length == 5 && Q.all (fun t => decide (t < n)) && decide Q.Nodup && ccwOk B Q &&
        decide (i < 5) && decide (j < 6) then
      jkClause B Q i j
    else none

end AE33
