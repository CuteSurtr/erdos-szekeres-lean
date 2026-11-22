import N66Enc.States
open N66Enc

def cntGo : List Bool → Nat → Nat
  | [], n => n
  | b :: l, n => match n with
    | k => cntGo l (if b then k + 1 else k)

-- 70 ttF evaluations (a = 5, b = 9, all c)
theorem k3 : cntGo ((List.finRange 70).map fun c => ttF ⟨5, by decide⟩ ⟨9, by decide⟩ c) 0 =
    10 := by decide +kernel
