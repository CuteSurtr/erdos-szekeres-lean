import F16IData

namespace Delta3.Forced16Instance

set_option maxRecDepth 10000
set_option maxHeartbeats 10000000

theorem columns_118 : ((vars.drop 472).take 4).all balanced = true := by
  decide +kernel

#print axioms columns_118

end Delta3.Forced16Instance
