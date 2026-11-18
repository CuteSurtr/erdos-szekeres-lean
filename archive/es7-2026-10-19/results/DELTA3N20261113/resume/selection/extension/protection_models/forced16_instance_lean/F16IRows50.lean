import F16IData

namespace Delta3.Forced16Instance

set_option maxRecDepth 10000
set_option maxHeartbeats 10000000

theorem rows_50 : ((rows.drop 100).take 2).all rowValid = true := by
  decide +kernel

#print axioms rows_50

end Delta3.Forced16Instance
