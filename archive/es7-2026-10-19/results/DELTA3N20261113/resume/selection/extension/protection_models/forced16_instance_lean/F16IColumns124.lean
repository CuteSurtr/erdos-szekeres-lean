import F16IData

namespace Delta3.Forced16Instance

set_option maxRecDepth 10000
set_option maxHeartbeats 10000000

theorem columns_124 : ((vars.drop 496).take 4).all balanced = true := by
  decide +kernel

#print axioms columns_124

end Delta3.Forced16Instance
