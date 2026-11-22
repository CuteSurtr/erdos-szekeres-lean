import N66R15Chk.TabDr0
import N66R15Chk.TabDr1

/-! The table `drChkN` agrees on all 70 rows (generated). -/

namespace N66R15Chk

theorem dr_all : (List.range 70).all drChkN = true := by
  have e : List.range 70 = List.range' 0 5 ++ List.range' 5 5 ++ List.range' 10 5 ++ List.range' 15 5 ++ List.range' 20 5 ++ List.range' 25 5 ++ List.range' 30 5 ++ List.range' 35 5 ++ List.range' 40 5 ++ List.range' 45 5 ++ List.range' 50 5 ++ List.range' 55 5 ++ List.range' 60 5 ++ List.range' 65 5 := by decide
  rw [e]; simp only [List.all_append, dr_0, dr_5, dr_10, dr_15, dr_20, dr_25, dr_30, dr_35, dr_40, dr_45, dr_50, dr_55, dr_60, dr_65, Bool.and_self]

end N66R15Chk
