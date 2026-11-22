import RowChk.Check

/-! Every entry of `cores` is a core certificate (kernel check). -/

namespace RowChk
open RowEnc

def isCore : Cert → Bool
  | .core _ _ => true
  | .tmpl _ _ _ => false

set_option maxRecDepth 100000 in
theorem cores_isCore : cores.all isCore = true := by decide +kernel

end RowChk
