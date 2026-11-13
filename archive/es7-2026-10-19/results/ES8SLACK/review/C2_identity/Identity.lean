/-
Claim C2 arithmetic, kernel-checked without Mathlib.
`binom` is Pascal's recursion (independent of Mathlib's `Nat.choose`).
-/

def binom : Nat → Nat → Nat
  | _, 0 => 1
  | 0, _ + 1 => 0
  | n + 1, k + 1 => binom n k + binom n (k + 1)

-- balanced states: down-sets of [5]x[5]
theorem balanced_count : binom 10 5 = 252 := by decide
-- residual states: down-sets of [4]x[6] minus those with (1,6) maximal
theorem residual_count : binom 10 4 = 210 ∧ binom 8 3 = 56 ∧ binom 10 4 - binom 8 3 = 154 := by decide
-- Mojarrad–Vlachos Theorem 1.1 at n = 8: C(2n-5,n-2) - C(2n-8,n-3) + 2
theorem mv_at_8 : binom (2*8-5) (8-2) - binom (2*8-8) (8-3) + 2 = 408 := by decide
-- the accounting identity
theorem states_plus_two : binom 10 5 + (binom 10 4 - binom 8 3) + 2
    = binom 11 6 - binom 8 5 + 2 := by decide
theorem accounting : 252 + 154 + 2 = 408 ∧ 64 + 33 = 97 ∧ 408 - 97 = 311 ∧
    (252 - 64) + (154 - 33) + 1 + 1 = 311 := by decide
-- the constants used by Final311/Final.lean: 251 - budget, 153 - budget, B + R + 2
theorem lean_constants : 251 - 63 = 188 ∧ 153 - 32 = 121 ∧ (251 - 63) + (153 - 32) + 2 = 311 := by decide

#print axioms balanced_count
#print axioms residual_count
#print axioms mv_at_8
#print axioms states_plus_two
#print axioms accounting
#print axioms lean_constants
