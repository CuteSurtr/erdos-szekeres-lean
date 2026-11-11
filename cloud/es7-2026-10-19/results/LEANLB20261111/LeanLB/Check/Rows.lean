import LeanLB.Data.C4N52
import LeanLB.Data.C6N60
import LeanLB.Data.C2N64
import LeanLB.Data.MirN46
import LeanLB.Data.C3N61
import LeanLB.Data.C5N56
import LeanLB.Data.C7N64

/-! Every row has exactly the expected number of entries, so `cycPoint m` and `intPoint` use every
entry of every row (they read entries with `List.getD`). Not needed by the proofs; documentation. -/

namespace LeanLB

theorem c4N52_rowlen : ∀ w ∈ c4N52Rows, w.length = 4 := by decide +kernel
theorem c6N60_rowlen : ∀ w ∈ c6N60Rows, w.length = 6 := by decide +kernel
theorem c2N64_rowlen : ∀ w ∈ c2N64Rows, w.length = 2 := by decide +kernel
theorem mirN46_rowlen : ∀ w ∈ mirN46Rows, w.length = 2 := by decide +kernel
theorem c3N61_rowlen : ∀ w ∈ c3N61Rows, w.length = 2 := by decide +kernel
theorem c5N56_rowlen : ∀ w ∈ c5N56Rows, w.length = 5 := by decide +kernel
theorem c7N64_rowlen : ∀ w ∈ c7N64Rows, w.length = 7 := by decide +kernel

end LeanLB
