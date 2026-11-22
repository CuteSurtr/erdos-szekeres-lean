import RowGeo.Assembly

/-! Evidence for the named hypothesis `RowGeo.R0Parse : N66Enc.R0 = RowGeo.R1` (COMPUTED by compiled Lean, trust
item E4; the kernel cannot evaluate `N66Enc.R0`, DESIGN.md F4). -/

#eval N66Enc.R0.length
#eval RowGeo.R1.length
#eval (N66Enc.R0 == RowGeo.R1)
#eval decide (N66Enc.R0 = RowGeo.R1)
