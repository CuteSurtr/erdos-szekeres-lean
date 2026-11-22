import N66R15Chk.Check

/-! Kernel checks of certificate data validity (generated). -/

namespace N66R15Chk
open N66R15Enc

theorem certsOkC2 : ([core52, core53, core54, core55, core56, core57, core58, core59, core60, core61, core62, core63, core64, core65, core66, core67, core68, core69, core70, core71, core72, core73, core74, core75, core76, core77] : List Cert).all coreOk = true := by decide +kernel
theorem certsOkC3 : ([core78, core79, core80, core81, core82, core83, core84, core85, core86, core87, core88, core89, core90, core91, core92, core93, core94, core95, core96, core97, core98, core99, core100, core101, core102, core103] : List Cert).all coreOk = true := by decide +kernel

end N66R15Chk
