import ETVEncoding.Rup

/-!
# Packed certificates

Long list literals are slow to elaborate, so larger clause lists and LRAT proofs are passed
to the kernel as one natural number. The kernel's GMP-backed `Nat` arithmetic decodes them.
The number is read in base `2^20`, least significant digit first. Digit `1` ends a group;
digit `d ≥ 2` is the payload `d - 2`. A literal `l` is stored as `2|l|` (positive) or
`2|l| + 1` (negative). Decoding is just a computable function, so a wrong number can only
make a check fail; it cannot make one succeed.
-/

namespace ETV.Packed

def base : ℕ := 2 ^ 20

/-- The base-`2^20` digits of `n`, least significant first (at most `fuel` of them). -/
def digits : ℕ → ℕ → List ℕ
  | 0, _ => []
  | fuel + 1, n => if n = 0 then [] else n % base :: digits fuel (n / base)

/-- Split a digit list into groups ended by `1`; payloads are `d - 2`. -/
def groups : List ℕ → List ℕ → List (List ℕ)
  | [], _ => []
  | d :: ds, cur => if d = 1 then cur.reverse :: groups ds [] else groups ds ((d - 2) :: cur)

def lit (x : ℕ) : ℤ := if x % 2 = 0 then ((x / 2 : ℕ) : ℤ) else -((x / 2 : ℕ) : ℤ)

/-- Clauses: one group per clause. -/
def clauses (fuel code : ℕ) : List (List ℤ) :=
  (groups (digits fuel code) []).map (·.map lit)

/-- Start clauses: one group `id :: lits` per clause. -/
def numbered (fuel code : ℕ) : List (ℕ × List ℤ) :=
  (groups (digits fuel code) []).map fun g => (g.headD 0, g.tail.map lit)

/-- Proof steps: two groups per step, `id :: lits` and the hints. -/
def stepsOf : List (List ℕ) → List Rup.Step
  | g :: h :: rest => .add (g.headD 0) (g.tail.map lit) h :: stepsOf rest
  | _ => []

def steps (fuel code : ℕ) : List Rup.Step := stepsOf (groups (digits fuel code) [])

end ETV.Packed
