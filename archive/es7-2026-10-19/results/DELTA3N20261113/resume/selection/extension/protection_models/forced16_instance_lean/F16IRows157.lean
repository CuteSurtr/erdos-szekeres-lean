import F16IData

namespace Delta3.Forced16Instance

set_option maxRecDepth 10000
set_option maxHeartbeats 10000000

theorem rows_157 : ((rows.drop 314).take 2).all rowValid = true := by
  decide +kernel

#print axioms rows_157

end Delta3.Forced16Instance
