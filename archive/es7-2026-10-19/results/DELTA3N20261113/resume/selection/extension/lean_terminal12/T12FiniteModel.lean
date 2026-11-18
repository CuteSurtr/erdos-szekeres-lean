/-! Exact integer orientation predicates for one finite, indexed fixture.
No real convex-hull interpretation is assumed by these definitions. -/

namespace Delta3.Terminal12

abbrev Index := Fin 12
abbrev Point := Int × Int

def point (i : Index) : Point :=
  match i.val with
  | 0 => (0, 0)
  | 1 => (37, -35)
  | 2 => (38, -248)
  | 3 => (84, -270)
  | 4 => (472, -427)
  | 5 => (653, -757)
  | 6 => (665, -793)
  | 7 => (666, -717)
  | 8 => (683, -718)
  | 9 => (736, -567)
  | 10 => (926, -895)
  | _ => (1000, 0)

def det (a b c : Index) : Int :=
  ((point b).1 - (point a).1) * ((point c).2 - (point a).2) -
    ((point b).2 - (point a).2) * ((point c).1 - (point a).1)

def indices : List Index := [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

/-- All length-k subsequences, retaining their source order. -/
def choose {α : Type} : Nat → List α → List (List α)
  | 0, _ => [[]]
  | _ + 1, [] => []
  | k + 1, a :: s => (choose k s).map (a :: ·) ++ choose (k + 1) s

def tripleCap : List Index → Bool
  | [a, b, c] => decide (det a b c < 0)
  | _ => false

/-- All ordered triples in the supplied index list have negative determinant. -/
def cap (s : List Index) : Bool := (choose 3 s).all tripleCap

/-- The four-point orientation criterion from the repository, evaluated on integers. -/
def quadConvex : List Index → Bool
  | [a, b, c, d] =>
    let x := decide (0 < det a b c)
    let y := decide (0 < det a b d)
    let z := decide (0 < det a c d)
    let w := decide (0 < det b c d)
    decide ((x = y ∧ z = w) ∨ (x ≠ z ∧ y ≠ w) ∨ (y = z ∧ x = w))
  | _ => false

/-- Finite orientation predicate: every four-element subsequence passes the criterion. -/
def signConvex (s : List Index) : Bool := (choose 4 s).all quadConvex

/-- There is an ambient four-cap ending with the specified ordered pair. -/
def terminalPair (b c : Index) : Bool :=
  indices.any fun u => indices.any fun v =>
    decide (u < v ∧ v < b ∧ b < c) && cap [u, v, b, c]

/-- A determinant-based finite terminal condition on a chosen set of indices. -/
def TerminalSafe (A : Index → Prop) : Prop :=
  ∀ a b c : Index, a < b → b < c → det a b c < 0 →
    A a → A b → A c → terminalPair b c = true

/-- Every ordered five-tuple passing the four-point tests meets the chosen set. -/
def HitsFive (A : Index → Prop) : Prop :=
  ∀ a b c d e : Index, a < b → b < c → c < d → d < e →
    signConvex [a, b, c, d, e] = true → A a ∨ A b ∨ A c ∨ A d ∨ A e

theorem indices_complete (i : Index) : i ∈ indices := by decide +revert

theorem increasing_x : ∀ i j : Index, i < j → (point i).1 < (point j).1 := by decide

theorem det_probe : det 0 1 2 = -7846 := by decide

#print axioms indices_complete
#print axioms increasing_x
#print axioms det_probe

end Delta3.Terminal12
