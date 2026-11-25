import LeanLB.Statement7

/-! Every row has exactly the expected number of entries, so `cycPoint m` and `intPoint` use every
entry of every row (they read entries with `List.getD`). Not needed by the proofs; documentation. -/

namespace LeanLB

theorem c3N31_rowlen : ∀ w ∈ c3N31Rows, w.length = 2 := by decide +kernel
theorem c6N30_rowlen : ∀ w ∈ c6N30Rows, w.length = 2 := by decide +kernel
theorem c4N28_rowlen : ∀ w ∈ c4N28Rows, w.length = 2 := by decide +kernel
theorem c2N32_rowlen : ∀ w ∈ c2N32Rows, w.length = 2 := by decide +kernel
theorem mirN32_rowlen : ∀ w ∈ mirN32Rows, w.length = 2 := by decide +kernel
theorem c5N31_rowlen : ∀ w ∈ c5N31Rows, w.length = 4 := by decide +kernel

end LeanLB
