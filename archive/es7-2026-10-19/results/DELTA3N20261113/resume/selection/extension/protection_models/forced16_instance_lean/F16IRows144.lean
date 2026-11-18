import F16IData

namespace Delta3.Forced16Instance

set_option maxRecDepth 10000
set_option maxHeartbeats 10000000

theorem rows_144 : ((rows.drop 288).take 2).all rowValid = true := by
  decide +kernel

#print axioms rows_144

end Delta3.Forced16Instance
