import N66Enc.Rows
open N66Enc

def lenGo : List Char → Nat → Nat
  | [], n => n
  | _ :: l, n => match n with
    | k => lenGo l (k + 1)

theorem k2 : lenGo rowsText.data 0 = 507715 := by decide +kernel
