import T12SixBlock01

set_option maxRecDepth 32768

namespace Delta3.Terminal12

theorem six_cover_01 :
    ((choose 6 indices).drop 512).take 512 = sixBlock01 := by
  decide +kernel

#print axioms six_cover_01

end Delta3.Terminal12
