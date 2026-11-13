import CompactChecker.Chunk733F
open CompactChecker
set_option profiler true
set_option maxRecDepth 100000
noncomputable def agg (f : ℕ → List ℕ → ℕ) (t : PTree) : ℕ :=
  PTree.rec (motive := fun _ => ℕ) 0 (fun cap es => f cap es) (fun _ _ _ a b => a + b) t
-- 1. entries traversal only (no lookup)
theorem b1 : Nat.ble 1 (agg (fun _ es => sumF (fun _ => 1) 131072 es) Chunk733F.tree) = true := by decide +kernel
-- 2. demand lookups
theorem b2 : Nat.ble 1 (agg (fun _ es => sumF fcat62.dem 131072 es) Chunk733F.tree) = true := by decide +kernel
-- 3. code lookups (packed sum)
theorem b3 : Nat.ble 1 (agg (fun _ es => sumF fcat62.code 131072 es) Chunk733F.tree) = true := by decide +kernel
-- 4. code sum + digits + pack
theorem b4 : Nat.ble 1 (agg (fun _ es => packF 4194304 (digitsF 4194304 252 (sumF fcat62.code 131072 es))) Chunk733F.tree) = true := by decide +kernel
