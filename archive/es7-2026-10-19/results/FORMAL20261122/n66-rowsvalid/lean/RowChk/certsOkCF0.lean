import RowChk.Check

/-! Kernel checks of certificate data validity (generated). -/

namespace RowChk
open RowEnc

theorem certsOkC0 : ([core0, core1, core2, core3, core4, core5, core6, core7, core8, core9, core10, core11, core12, core13, core14, core15, core16, core17, core18, core19, core20, core21, core22, core23, core24, core25] : List Cert).all coreOk = true := by decide +kernel
theorem certsOkC1 : ([core26, core27, core28, core29, core30, core31, core32, core33, core34, core35, core36, core37, core38, core39, core40, core41, core42, core43, core44, core45, core46, core47, core48, core49, core50, core51] : List Cert).all coreOk = true := by decide +kernel

end RowChk
