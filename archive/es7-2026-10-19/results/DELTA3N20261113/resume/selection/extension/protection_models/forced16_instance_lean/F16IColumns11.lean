import F16IData

namespace Delta3.Forced16Instance

set_option maxRecDepth 10000
set_option maxHeartbeats 10000000

theorem columns_11 : ((vars.drop 44).take 4).all balanced = true := by
  decide +kernel

#print axioms columns_11

end Delta3.Forced16Instance
