import RowChk.Look

/-! Kernel checks of the table `canChkN` (generated). -/

namespace RowChk

theorem can_0 : (List.range' 0 10).all canChkN = true := by decide +kernel
theorem can_10 : (List.range' 10 10).all canChkN = true := by decide +kernel
theorem can_20 : (List.range' 20 10).all canChkN = true := by decide +kernel
theorem can_30 : (List.range' 30 10).all canChkN = true := by decide +kernel
theorem can_40 : (List.range' 40 10).all canChkN = true := by decide +kernel
theorem can_50 : (List.range' 50 10).all canChkN = true := by decide +kernel
theorem can_60 : (List.range' 60 10).all canChkN = true := by decide +kernel

theorem can_all : (List.range 70).all canChkN = true := by
  have e : List.range 70 = List.range' 0 10 ++ List.range' 10 10 ++ List.range' 20 10 ++ List.range' 30 10 ++ List.range' 40 10 ++ List.range' 50 10 ++ List.range' 60 10 := by decide
  rw [e]; simp only [List.all_append, can_0, can_10, can_20, can_30, can_40, can_50, can_60, Bool.and_self]

end RowChk
