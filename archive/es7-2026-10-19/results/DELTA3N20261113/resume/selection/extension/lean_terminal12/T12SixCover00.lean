import T12SixBlock00

set_option maxRecDepth 32768

namespace Delta3.Terminal12

theorem six_cover_00 :
    ((choose 6 indices).drop 0).take 512 = sixBlock00 := by
  decide +kernel

#print axioms six_cover_00

end Delta3.Terminal12
