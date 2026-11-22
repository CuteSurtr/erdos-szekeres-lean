/-!
# N66E15.Atoms: the variables of the N66 relaxation (Std-only)

One constructor per kind of DIMACS variable that the generator allocates (coupled5.py:37-43, lazymono.py:30,61-62,
70, pysat seqcounter aux, p2_sb.py:36). All fields are `Fin`-bounded, so `code` is injective on the whole type and
`atomOfCode (code a) = a` (`atomOfCode_code`). The codes are small (< 28,533,817) so that `EncB.numberMap` can index
an array by them (`N66E15.Alloc`).

| constructor | Python | meaning (DESIGN.md §2.2) |
|---|---|---|
| `before i j` (i < j) | `('before', i, j)` | owner of state i left of owner of state j |
| `capGe i j k`, `cupGe i j k` (k = 2..4) | `('cap_ge', i, j, k)`, `('cup_ge', …)` | label coordinate of the pair ≥ k |
| `orient i j k` (i < j < k) | `('orientation', i, j, k)` | orientation of the owners in state-index order |
| `convex i j k l` | `('convex_four', …)` | allocated, used by no clause |
| `sel s` | `sel[s]` | state s occupied |
| `chC k a b c`, `chU k a b c` (k = 3..5) | `C[k,a,b,c]`, `U[k,a,b,c]` | a k-cap (k-cup) starts at a and ends with (b, c) |
| `ce p q`, `ue p q` | `CE[(p,q)]`, `UE[(p,q)]` | a 5-cap (5-cup) from p to q |
| `cnt a j` | seqcounter aux s(a, j) | at least j holes among the first a hole literals |
| `sbe j` | `e_j` of p2_sb.py | the first j+1 pairs agree |
-/

namespace N66E15

inductive Atom
  | before (i j : Fin 70)
  | capGe (i j : Fin 70) (k : Fin 5)
  | cupGe (i j : Fin 70) (k : Fin 5)
  | orient (i j k : Fin 70)
  | convex (i j k l : Fin 70)
  | sel (s : Fin 70)
  | chC (k : Fin 6) (a b c : Fin 70)
  | chU (k : Fin 6) (a b c : Fin 70)
  | ce (p q : Fin 70)
  | ue (p q : Fin 70)
  | cnt (a : Fin 68) (j : Fin 15)
  | sbe (j : Fin 27)
  deriving DecidableEq, Repr

namespace Atom

/-- Contiguous code ranges, one per constructor (see the module docstring). -/
def code : Atom → Nat
  | before i j => i.val * 70 + j.val
  | capGe i j k => 4900 + (i.val * 70 + j.val) * 5 + k.val
  | cupGe i j k => 29400 + (i.val * 70 + j.val) * 5 + k.val
  | orient i j k => 53900 + (i.val * 70 + j.val) * 70 + k.val
  | convex i j k l => 396900 + ((i.val * 70 + j.val) * 70 + k.val) * 70 + l.val
  | sel s => 24406900 + s.val
  | chC k a b c => 24406970 + ((k.val * 70 + a.val) * 70 + b.val) * 70 + c.val
  | chU k a b c => 26464970 + ((k.val * 70 + a.val) * 70 + b.val) * 70 + c.val
  | ce p q => 28522970 + p.val * 70 + q.val
  | ue p q => 28527870 + p.val * 70 + q.val
  | cnt a j => 28532770 + a.val * 15 + j.val
  | sbe j => 28533790 + j.val

/-- The digit `x % 70` as a `Fin 70`. -/
def d70 (x : Nat) : Fin 70 := ⟨x % 70, Nat.mod_lt _ (by decide)⟩

/-- Inverse of `code` (any value for codes outside the ranges). -/
def ofCode (c : Nat) : Atom :=
  if c < 4900 then before (d70 (c / 70)) (d70 c)
  else if c < 29400 then
    let x := c - 4900
    capGe (d70 (x / 5 / 70)) (d70 (x / 5)) ⟨x % 5, Nat.mod_lt _ (by decide)⟩
  else if c < 53900 then
    let x := c - 29400
    cupGe (d70 (x / 5 / 70)) (d70 (x / 5)) ⟨x % 5, Nat.mod_lt _ (by decide)⟩
  else if c < 396900 then
    let x := c - 53900
    orient (d70 (x / 4900)) (d70 (x / 70)) (d70 x)
  else if c < 24406900 then
    let x := c - 396900
    convex (d70 (x / 343000)) (d70 (x / 4900)) (d70 (x / 70)) (d70 x)
  else if c < 24406970 then sel (d70 (c - 24406900))
  else if c < 26464970 then
    let x := c - 24406970
    chC ⟨x / 343000 % 6, Nat.mod_lt _ (by decide)⟩ (d70 (x / 4900)) (d70 (x / 70)) (d70 x)
  else if c < 28522970 then
    let x := c - 26464970
    chU ⟨x / 343000 % 6, Nat.mod_lt _ (by decide)⟩ (d70 (x / 4900)) (d70 (x / 70)) (d70 x)
  else if c < 28527870 then
    let x := c - 28522970
    ce (d70 (x / 70)) (d70 x)
  else if c < 28532770 then
    let x := c - 28527870
    ue (d70 (x / 70)) (d70 x)
  else if c < 28533790 then
    let x := c - 28532770
    cnt ⟨x / 15 % 68, Nat.mod_lt _ (by decide)⟩ ⟨x % 15, Nat.mod_lt _ (by decide)⟩
  else sbe ⟨(c - 28533790) % 27, Nat.mod_lt _ (by decide)⟩

end Atom

/-- A structured literal: `(true, a)` is the atom, `(false, a)` its negation. -/
abbrev SLit := Bool × Atom

def SLit.neg (l : SLit) : SLit := (!l.1, l.2)

end N66E15
