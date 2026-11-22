import AE33Geo.Radius1
open Lean in
#eval show CoreM Unit from do
  for m in (← getEnv).header.moduleNames do
    IO.println s!"MODULE {m}"
