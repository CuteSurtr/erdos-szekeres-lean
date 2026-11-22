import RowChk.Check

/-! Kernel checks of certificate data validity (generated). -/

namespace RowChk
open RowEnc

theorem certsOkC4 : ([core104, core105, core106, core107, core108, core109, core110, core111, core112, core113, core114, core115, core116, core117, core118, core119, core120, core121, core122, core123, core124, core125, core126, core127, core128, core129] : List Cert).all coreOk = true := by decide +kernel
theorem certsOkC5 : ([core130, core131, core132, core133, core134, core135, core136, core137, core138, core139, core140, core141, core142, core143, core144, core145, core146, core147, core148, core149, core150, core151, core152, core153, core154, core155] : List Cert).all coreOk = true := by decide +kernel

end RowChk
