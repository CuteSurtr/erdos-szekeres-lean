import F16IData

namespace Delta3.Forced16Instance

set_option maxRecDepth 10000
set_option maxHeartbeats 10000000

theorem rows_57 : ((rows.drop 114).take 2).all rowValid = true := by
  decide +kernel

#print axioms rows_57

end Delta3.Forced16Instance
