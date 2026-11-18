import F16IData

namespace Delta3.Forced16Instance

set_option maxRecDepth 10000
set_option maxHeartbeats 10000000

theorem rows_82 : ((rows.drop 164).take 2).all rowValid = true := by
  decide +kernel

#print axioms rows_82

end Delta3.Forced16Instance
