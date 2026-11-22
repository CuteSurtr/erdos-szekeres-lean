import N66R15Chk.Check

/-! Every entry of `cores` is a core certificate (kernel check). -/

namespace N66R15Chk
open N66R15Enc

def isCore : Cert → Bool
  | .core _ _ => true
  | .tmpl _ _ _ => false

set_option maxRecDepth 100000 in
theorem cores_isCore : cores.all isCore = true := by decide +kernel

end N66R15Chk
