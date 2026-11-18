import F16IData

namespace Delta3.Forced16Instance

set_option maxRecDepth 10000
set_option maxHeartbeats 10000000

theorem columns_105 : ((vars.drop 420).take 4).all balanced = true := by
  decide +kernel

#print axioms columns_105

end Delta3.Forced16Instance
