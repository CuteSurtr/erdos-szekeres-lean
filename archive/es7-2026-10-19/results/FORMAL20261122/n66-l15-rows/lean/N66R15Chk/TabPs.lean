import N66R15Chk.Look

/-! Kernel checks of the table `psChkN` (generated). -/

namespace N66R15Chk

theorem ps_0 : (List.range' 0 10).all psChkN = true := by decide +kernel
theorem ps_10 : (List.range' 10 10).all psChkN = true := by decide +kernel
theorem ps_20 : (List.range' 20 10).all psChkN = true := by decide +kernel
theorem ps_30 : (List.range' 30 10).all psChkN = true := by decide +kernel
theorem ps_40 : (List.range' 40 10).all psChkN = true := by decide +kernel
theorem ps_50 : (List.range' 50 10).all psChkN = true := by decide +kernel
theorem ps_60 : (List.range' 60 10).all psChkN = true := by decide +kernel

theorem ps_all : (List.range 70).all psChkN = true := by
  have e : List.range 70 = List.range' 0 10 ++ List.range' 10 10 ++ List.range' 20 10 ++ List.range' 30 10 ++ List.range' 40 10 ++ List.range' 50 10 ++ List.range' 60 10 := by decide
  rw [e]; simp only [List.all_append, ps_0, ps_10, ps_20, ps_30, ps_40, ps_50, ps_60, Bool.and_self]

end N66R15Chk
