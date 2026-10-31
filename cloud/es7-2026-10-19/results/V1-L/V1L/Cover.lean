import MirrorEncoding.CoverCore
import V1L.Leaves

/-!
# The cover fact, by kernel evaluation

`coverCheck hullLeaves = true`, checked by the Lean kernel (`decide +kernel`: the kernel
reduces `coverCheck hullLeaves` to `true`; no `native_decide`, no compiler, no extra axiom).
With `Mir.covers_of_coverCheck` this says that every assignment satisfies some leaf cube.
-/

namespace V1L

open Mir

set_option maxHeartbeats 0 in
theorem hullLeaves_coverCheck : coverCheck hullLeaves = true := by decide +kernel

theorem hullLeaves_length : hullLeaves.length = 1198 := by decide +kernel

end V1L
