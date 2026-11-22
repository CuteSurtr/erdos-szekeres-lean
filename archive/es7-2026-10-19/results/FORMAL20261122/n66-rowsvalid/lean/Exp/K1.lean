import N66Enc.States
open N66Enc

/-- tail-recursive count with a forced accumulator -/
def cntGo : List Bool → Nat → Nat
  | [], n => n
  | b :: l, n => match n with
    | k => cntGo l (if b then k + 1 else k)

def row (a : Fin 70) : List Bool :=
  (List.finRange 70).flatMap fun b => (List.finRange 70).map fun c => ttF a b c

set_option maxRecDepth 100000 in
theorem k1 : cntGo (row ⟨5, by decide⟩) 0 = 356 := by decide +kernel
