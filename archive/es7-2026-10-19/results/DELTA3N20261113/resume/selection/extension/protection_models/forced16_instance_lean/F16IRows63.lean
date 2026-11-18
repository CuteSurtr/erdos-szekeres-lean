import F16IData

namespace Delta3.Forced16Instance

set_option maxRecDepth 10000
set_option maxHeartbeats 10000000

theorem rows_63 : ((rows.drop 126).take 2).all rowValid = true := by
  decide +kernel

#print axioms rows_63

end Delta3.Forced16Instance
