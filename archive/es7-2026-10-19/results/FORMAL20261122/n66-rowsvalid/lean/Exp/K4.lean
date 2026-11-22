import N66Enc.States
open N66Enc

def cntGo : List Bool → Nat → Nat
  | [], n => n
  | b :: l, n => match n with
    | k => cntGo l (if b then k + 1 else k)

-- 280 ttF evaluations (a = 5, b = 9..12, all c)
theorem k4 : cntGo (([9, 10, 11, 12] : List (Fin 70)).flatMap fun b => (List.finRange 70).map fun c => ttF ⟨5, by decide⟩ b c) 0 = 66 := by decide +kernel
