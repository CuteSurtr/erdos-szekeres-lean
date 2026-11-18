import F16IData

namespace Delta3.Forced16Instance

set_option maxRecDepth 10000
set_option maxHeartbeats 10000000

theorem rows_64 : ((rows.drop 128).take 2).all rowValid = true := by
  decide +kernel

#print axioms rows_64

end Delta3.Forced16Instance
