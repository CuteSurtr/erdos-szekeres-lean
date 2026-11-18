import F16IData

namespace Delta3.Forced16Instance

set_option maxRecDepth 10000
set_option maxHeartbeats 10000000

theorem rows_30 : ((rows.drop 60).take 2).all rowValid = true := by
  decide +kernel

#print axioms rows_30

end Delta3.Forced16Instance
