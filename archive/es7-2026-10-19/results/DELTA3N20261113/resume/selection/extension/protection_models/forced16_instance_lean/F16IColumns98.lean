import F16IData

namespace Delta3.Forced16Instance

set_option maxRecDepth 10000
set_option maxHeartbeats 10000000

theorem columns_98 : ((vars.drop 392).take 4).all balanced = true := by
  decide +kernel

#print axioms columns_98

end Delta3.Forced16Instance
