import CompactChecker.Chunk733G4
/-! Where the kernel time of `checkF2` goes on the 64-leaf chunk (6 November 2026).
Each theorem walks the same tree and masks as `treeF2` and forces one part of the
leaf test. Needs `build/CompactChecker/Chunk733G4.olean`. Times are per theorem
(`Elab.async false`). -/
open CompactChecker
set_option profiler true
set_option profiler.threshold 1
set_option Elab.async false
set_option maxRecDepth 100000
noncomputable section
def walk (f : ℕ → List ℕ → List ℕ → Bool) (t : PTree) : List ℕ → Bool :=
  PTree.rec (motive := fun _ => List ℕ → Bool) (fun _ => true) (fun cap ws mask => f cap ws mask)
    (fun v _ _ ihz iho mask => Bool.rec false (iho (setF 1 mask v)) (ihz (setF 2 mask v))) t
def BN : ℕ := Nat.pow 8388608 252
-- 1. tree walk and mask updates only
theorem b1 : walk (fun _ _ _ => true) Chunk733G4.b733 Chunk733G4.mask733 = true := by decide +kernel
-- 2. word decoding, no row lookups
theorem b2 : walk (fun _ ws _ => Nat.ble 0 (leafQ (fun r => r) 131072 536870912 4 ws))
    Chunk733G4.b733 Chunk733G4.mask733 = true := by decide +kernel
-- 3. the fused sum with cached row lookups
theorem b3 : walk (fun _ ws _ => Nat.ble 0 (leafQ (rowVal fcat62 3131 8388608 BN) 131072 536870912 4 ws))
    Chunk733G4.b733 Chunk733G4.mask733 = true := by decide +kernel
-- 4. mask cells only (one pass over each leaf's mask)
theorem b4 : walk (fun _ _ mask => Nat.ble 0 (List.rec (motive := fun _ => ℕ) 0 (fun v _ acc => Nat.add v acc) mask))
    Chunk733G4.b733 Chunk733G4.mask733 = true := by decide +kernel
-- 5. the fused sum and the digit loop
theorem b5 : walk (fun cap ws mask => Nat.ble 0 (colLoop 8388608 cap (bigF 252 8388608) mask
    (leafQ (rowVal fcat62 3131 8388608 BN) 131072 536870912 4 ws))) Chunk733G4.b733 Chunk733G4.mask733 = true := by
  decide +kernel
-- 6. the whole checker
theorem b6 : checkF2 fcat62 3131 252 62 8388608 131072 536870912 4 Chunk733G4.b733 Chunk733G4.mask733 = true := by
  decide +kernel
