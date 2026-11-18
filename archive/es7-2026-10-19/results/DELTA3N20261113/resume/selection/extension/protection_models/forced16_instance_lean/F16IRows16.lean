import F16IData

namespace Delta3.Forced16Instance

set_option maxRecDepth 10000
set_option maxHeartbeats 10000000

theorem rows_16 : ((rows.drop 32).take 2).all rowValid = true := by
  decide +kernel

#print axioms rows_16

end Delta3.Forced16Instance
