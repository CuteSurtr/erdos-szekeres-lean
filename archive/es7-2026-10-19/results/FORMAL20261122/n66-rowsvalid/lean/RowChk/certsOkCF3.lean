import RowChk.Check

/-! Kernel checks of certificate data validity (generated). -/

namespace RowChk
open RowEnc

theorem certsOkC6 : ([core156, core157, core158, core159, core160, core161, core162, core163, core164, core165, core166, core167, core168, core169, core170, core171, core172, core173, core174, core175, core176, core177, core178, core179, core180, core181] : List Cert).all coreOk = true := by decide +kernel
theorem certsOkC7 : ([core182, core183, core184, core185, core186, core187, core188, core189, core190, core191, core192, core193, core194, core195, core196, core197, core198, core199, core200, core201, core202, core203, core204, core205, core206, core207] : List Cert).all coreOk = true := by decide +kernel

end RowChk
