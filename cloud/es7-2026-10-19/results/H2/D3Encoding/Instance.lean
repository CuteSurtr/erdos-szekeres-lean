import D3Encoding.Main

/-!
# The 33-point instance

`t = 11` (`N = 33`, five 6-orbits and one 3-orbit), `K = 7`. The group-closure side
condition is checked by `decide` (34 points, 6 × 6 compositions).
-/

namespace D3

theorem groupClosed_11 : GroupClosed 11 := by
  unfold GroupClosed
  decide

end D3
