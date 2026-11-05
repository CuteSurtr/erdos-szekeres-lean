import CompactChecker.Fcat62
open CompactChecker
set_option profiler true
set_option maxRecDepth 100000
noncomputable def loopSum (f : ℕ → ℕ) (n : ℕ) : ℕ :=
  Nat.rec (motive := fun _ => ℕ) 0 (fun i acc => f (i * 3) + acc) n
-- 1000 trie lookups (dem)
theorem l1 : Nat.ble 1 (loopSum fcat62.dem 1000) = true := by decide +kernel
-- 1000 calls without descent
theorem l2 : Nat.ble 1 (loopSum fcat62_r0.dem 1000) = true := by decide +kernel
-- 1000 calls, plain arithmetic
theorem l3 : Nat.ble 1 (loopSum (fun k => k % 2 + k / 2) 1000) = true := by decide +kernel
