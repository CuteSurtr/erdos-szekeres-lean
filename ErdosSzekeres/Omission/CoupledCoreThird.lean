import ErdosSzekeres.Omission.CoupledLrat
import ErdosSzekeres.Omission.CoupledSemantics

namespace ErdosSzekeres.Omission.CoupledCoreThird
open Coupled
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

lrat_raw cnf_refutation
  (include_str "../../experiments/omission-coupled-demand-two-2026-10-10/core13.cnf")
  (include_str "../../experiments/omission-coupled-demand-two-2026-10-10/core13.lrat")

def support : List (Fin 154) := [16, 30, 39, 43, 50, 53, 62, 65, 68, 77, 89, 91, 101]

def states : Fin 13 → Fin 154 := support.get

def atoms : List (Atom 13) := [
  .before 0 1,
  .before 0 2,
  .before 0 3,
  .capGe 0 3 2,
  .capGe 0 3 3,
  .capGe 0 3 4,
  .cupGe 0 3 2,
  .cupGe 0 3 3,
  .cupGe 0 3 4,
  .cupGe 0 3 5,
  .before 0 4,
  .before 0 5,
  .before 0 6,
  .before 0 7,
  .before 0 8,
  .before 0 9,
  .before 0 10,
  .before 0 11,
  .before 0 12,
  .before 1 2,
  .cupGe 1 2 2,
  .before 1 3,
  .before 1 4,
  .before 1 5,
  .before 1 6,
  .before 1 7,
  .before 1 8,
  .before 1 9,
  .before 1 11,
  .before 1 12,
  .cupGe 1 12 2,
  .before 2 3,
  .before 2 4,
  .cupGe 2 4 3,
  .before 2 8,
  .before 2 10,
  .before 2 11,
  .before 2 12,
  .before 3 4,
  .before 3 5,
  .capGe 3 5 4,
  .cupGe 3 5 2,
  .cupGe 3 5 3,
  .cupGe 3 5 4,
  .before 3 6,
  .cupGe 3 6 5,
  .before 3 7,
  .before 3 8,
  .capGe 3 8 2,
  .capGe 3 8 3,
  .capGe 3 8 4,
  .cupGe 3 8 6,
  .before 3 9,
  .cupGe 3 9 6,
  .before 3 10,
  .cupGe 3 10 6,
  .before 3 11,
  .capGe 3 11 4,
  .before 3 12,
  .before 4 6,
  .cupGe 4 6 4,
  .before 4 7,
  .before 4 8,
  .before 4 10,
  .before 4 11,
  .before 4 12,
  .before 5 7,
  .cupGe 5 7 4,
  .cupGe 5 7 5,
  .before 5 8,
  .before 5 9,
  .before 5 10,
  .before 5 11,
  .before 5 12,
  .before 6 8,
  .before 6 9,
  .before 6 10,
  .before 6 11,
  .before 6 12,
  .before 7 8,
  .before 7 9,
  .capGe 7 9 2,
  .capGe 7 9 3,
  .capGe 7 9 4,
  .cupGe 7 9 5,
  .cupGe 7 9 6,
  .before 7 10,
  .before 7 11,
  .before 7 12,
  .before 8 9,
  .before 8 10,
  .before 8 11,
  .capGe 8 11 3,
  .capGe 8 11 4,
  .cupGe 8 11 2,
  .cupGe 8 11 3,
  .cupGe 8 11 4,
  .cupGe 8 11 5,
  .cupGe 8 11 6,
  .before 8 12,
  .before 9 10,
  .before 9 11,
  .before 9 12,
  .before 10 11,
  .before 10 12,
  .capGe 10 12 4,
  .cupGe 10 12 2,
  .cupGe 10 12 3,
  .cupGe 10 12 4,
  .cupGe 10 12 5,
  .cupGe 10 12 6,
  .before 11 12,
  .capGe 11 12 2,
  .capGe 11 12 3,
  .cupGe 11 12 2,
  .cupGe 11 12 3,
  .cupGe 11 12 4,
  .cupGe 11 12 5,
  .cupGe 11 12 6,
  .positive 0 1 2,
  .positive 0 1 3,
  .positive 0 1 4,
  .positive 0 1 6,
  .positive 0 1 8,
  .positive 0 1 10,
  .positive 0 1 11,
  .positive 0 1 12,
  .positive 0 2 3,
  .positive 0 2 4,
  .positive 0 2 6,
  .positive 0 2 8,
  .positive 0 2 10,
  .positive 0 2 11,
  .positive 0 2 12,
  .positive 0 3 4,
  .positive 0 3 5,
  .positive 0 3 6,
  .positive 0 3 7,
  .positive 0 3 8,
  .positive 0 3 9,
  .positive 0 3 10,
  .positive 0 3 11,
  .positive 0 3 12,
  .positive 0 4 6,
  .positive 0 4 8,
  .positive 0 4 10,
  .positive 0 4 11,
  .positive 0 4 12,
  .positive 0 5 7,
  .positive 0 5 9,
  .positive 0 5 10,
  .positive 0 5 11,
  .positive 0 5 12,
  .positive 0 6 8,
  .positive 0 6 10,
  .positive 0 6 11,
  .positive 0 6 12,
  .positive 0 7 9,
  .positive 0 7 10,
  .positive 0 7 11,
  .positive 0 7 12,
  .positive 0 8 10,
  .positive 0 8 11,
  .positive 0 9 10,
  .positive 0 9 11,
  .positive 0 9 12,
  .positive 0 10 11,
  .positive 0 10 12,
  .positive 0 11 12,
  .positive 1 2 3,
  .positive 1 2 4,
  .positive 1 2 6,
  .positive 1 2 8,
  .positive 1 2 10,
  .positive 1 2 11,
  .positive 1 2 12,
  .positive 1 3 4,
  .positive 1 3 6,
  .positive 1 3 8,
  .positive 1 3 10,
  .positive 1 4 6,
  .positive 1 4 8,
  .positive 1 4 10,
  .positive 1 4 11,
  .positive 1 4 12,
  .positive 1 6 8,
  .positive 1 6 10,
  .positive 1 6 11,
  .positive 1 6 12,
  .positive 1 8 10,
  .positive 1 10 11,
  .positive 1 10 12,
  .positive 1 11 12,
  .positive 2 3 4,
  .positive 2 3 6,
  .positive 2 3 8,
  .positive 2 3 10,
  .positive 2 4 6,
  .positive 2 4 8,
  .positive 2 4 10,
  .positive 2 4 11,
  .positive 2 4 12,
  .positive 2 6 8,
  .positive 2 6 10,
  .positive 2 6 11,
  .positive 2 6 12,
  .positive 2 8 10,
  .positive 2 10 11,
  .positive 2 10 12,
  .positive 2 11 12,
  .positive 3 4 6,
  .positive 3 4 8,
  .positive 3 4 10,
  .positive 3 5 7,
  .positive 3 5 8,
  .positive 3 5 9,
  .positive 3 5 10,
  .positive 3 5 11,
  .positive 3 5 12,
  .positive 3 6 8,
  .positive 3 6 9,
  .positive 3 6 10,
  .positive 3 7 8,
  .positive 3 7 9,
  .positive 3 7 10,
  .positive 3 7 11,
  .positive 3 7 12,
  .positive 3 8 9,
  .positive 3 8 10,
  .positive 3 8 11,
  .positive 3 8 12,
  .positive 3 9 10,
  .positive 3 9 11,
  .positive 3 9 12,
  .positive 3 10 11,
  .positive 3 10 12,
  .positive 3 11 12,
  .positive 4 6 8,
  .positive 4 6 10,
  .positive 4 6 11,
  .positive 4 6 12,
  .positive 4 7 9,
  .positive 4 8 10,
  .positive 4 10 11,
  .positive 4 10 12,
  .positive 4 11 12,
  .positive 5 7 8,
  .positive 5 7 9,
  .positive 5 7 10,
  .positive 5 7 11,
  .positive 5 7 12,
  .positive 5 8 9,
  .positive 5 8 10,
  .positive 5 8 11,
  .positive 5 8 12,
  .positive 5 9 10,
  .positive 5 9 11,
  .positive 5 9 12,
  .positive 5 10 11,
  .positive 5 10 12,
  .positive 5 11 12,
  .positive 6 8 9,
  .positive 6 8 10,
  .positive 6 10 11,
  .positive 6 10 12,
  .positive 6 11 12,
  .positive 7 8 9,
  .positive 7 8 10,
  .positive 7 8 11,
  .positive 7 8 12,
  .positive 7 9 10,
  .positive 7 9 11,
  .positive 7 9 12,
  .positive 7 10 11,
  .positive 7 10 12,
  .positive 7 11 12,
  .positive 8 9 10,
  .positive 8 9 11,
  .positive 8 9 12,
  .positive 8 10 11,
  .positive 8 10 12,
  .positive 8 11 12,
  .positive 9 10 11,
  .positive 9 10 12,
  .positive 9 11 12,
  .positive 10 11 12,
  .convex 0 1 2 3,
  .convex 0 1 2 4,
  .convex 0 1 2 6,
  .convex 0 1 2 8,
  .convex 0 1 2 10,
  .convex 0 1 2 11,
  .convex 0 1 2 12,
  .convex 0 1 3 4,
  .convex 0 1 3 6,
  .convex 0 1 3 8,
  .convex 0 1 3 10,
  .convex 0 1 4 6,
  .convex 0 1 4 8,
  .convex 0 1 4 10,
  .convex 0 1 4 11,
  .convex 0 1 4 12,
  .convex 0 1 6 8,
  .convex 0 1 6 10,
  .convex 0 1 6 11,
  .convex 0 1 6 12,
  .convex 0 1 8 10,
  .convex 0 1 10 11,
  .convex 0 1 10 12,
  .convex 0 1 11 12,
  .convex 0 2 3 4,
  .convex 0 2 3 6,
  .convex 0 2 3 8,
  .convex 0 2 3 10,
  .convex 0 2 4 6,
  .convex 0 2 4 8,
  .convex 0 2 4 10,
  .convex 0 2 4 11,
  .convex 0 2 4 12,
  .convex 0 2 6 8,
  .convex 0 2 6 10,
  .convex 0 2 6 11,
  .convex 0 2 6 12,
  .convex 0 2 8 10,
  .convex 0 2 10 11,
  .convex 0 2 10 12,
  .convex 0 2 11 12,
  .convex 0 3 4 6,
  .convex 0 3 4 8,
  .convex 0 3 4 10,
  .convex 0 3 5 7,
  .convex 0 3 5 9,
  .convex 0 3 5 10,
  .convex 0 3 5 11,
  .convex 0 3 5 12,
  .convex 0 3 6 8,
  .convex 0 3 6 10,
  .convex 0 3 7 9,
  .convex 0 3 7 10,
  .convex 0 3 7 11,
  .convex 0 3 7 12,
  .convex 0 3 8 10,
  .convex 0 3 9 10,
  .convex 0 3 9 11,
  .convex 0 3 9 12,
  .convex 0 3 10 11,
  .convex 0 3 10 12,
  .convex 0 3 11 12,
  .convex 0 4 6 8,
  .convex 0 4 6 10,
  .convex 0 4 6 11,
  .convex 0 4 6 12,
  .convex 0 4 8 10,
  .convex 0 4 10 11,
  .convex 0 4 10 12,
  .convex 0 4 11 12,
  .convex 0 5 7 9,
  .convex 0 5 7 10,
  .convex 0 5 7 11,
  .convex 0 5 7 12,
  .convex 0 5 9 10,
  .convex 0 5 9 11,
  .convex 0 5 9 12,
  .convex 0 5 10 11,
  .convex 0 5 10 12,
  .convex 0 5 11 12,
  .convex 0 6 8 10,
  .convex 0 6 10 11,
  .convex 0 6 10 12,
  .convex 0 6 11 12,
  .convex 0 7 9 10,
  .convex 0 7 9 11,
  .convex 0 7 9 12,
  .convex 0 7 10 11,
  .convex 0 7 10 12,
  .convex 0 7 11 12,
  .convex 0 9 10 11,
  .convex 0 9 10 12,
  .convex 0 9 11 12,
  .convex 0 10 11 12,
  .convex 1 2 3 4,
  .convex 1 2 3 6,
  .convex 1 2 3 8,
  .convex 1 2 3 10,
  .convex 1 2 4 6,
  .convex 1 2 4 8,
  .convex 1 2 4 10,
  .convex 1 2 4 11,
  .convex 1 2 4 12,
  .convex 1 2 6 8,
  .convex 1 2 6 10,
  .convex 1 2 6 11,
  .convex 1 2 6 12,
  .convex 1 2 8 10,
  .convex 1 2 10 11,
  .convex 1 2 10 12,
  .convex 1 2 11 12,
  .convex 1 3 4 6,
  .convex 1 3 4 8,
  .convex 1 3 4 10,
  .convex 1 3 6 8,
  .convex 1 3 6 10,
  .convex 1 3 8 10,
  .convex 1 4 6 8,
  .convex 1 4 6 10,
  .convex 1 4 6 11,
  .convex 1 4 6 12,
  .convex 1 4 8 10,
  .convex 1 4 10 11,
  .convex 1 4 10 12,
  .convex 1 4 11 12,
  .convex 1 6 8 10,
  .convex 1 6 10 11,
  .convex 1 6 10 12,
  .convex 1 6 11 12,
  .convex 1 10 11 12,
  .convex 2 3 4 6,
  .convex 2 3 4 8,
  .convex 2 3 4 10,
  .convex 2 3 6 8,
  .convex 2 3 6 10,
  .convex 2 3 8 10,
  .convex 2 4 6 8,
  .convex 2 4 6 10,
  .convex 2 4 6 11,
  .convex 2 4 6 12,
  .convex 2 4 8 10,
  .convex 2 4 10 11,
  .convex 2 4 10 12,
  .convex 2 4 11 12,
  .convex 2 6 8 10,
  .convex 2 6 10 11,
  .convex 2 6 10 12,
  .convex 2 6 11 12,
  .convex 2 10 11 12,
  .convex 3 4 6 8,
  .convex 3 4 6 10,
  .convex 3 4 8 10,
  .convex 3 5 7 8,
  .convex 3 5 7 9,
  .convex 3 5 7 10,
  .convex 3 5 7 11,
  .convex 3 5 7 12,
  .convex 3 5 8 9,
  .convex 3 5 8 10,
  .convex 3 5 8 11,
  .convex 3 5 8 12,
  .convex 3 5 9 10,
  .convex 3 5 9 11,
  .convex 3 5 9 12,
  .convex 3 5 10 11,
  .convex 3 5 10 12,
  .convex 3 5 11 12,
  .convex 3 6 8 10,
  .convex 3 7 8 9,
  .convex 3 7 8 10,
  .convex 3 7 8 11,
  .convex 3 7 8 12,
  .convex 3 7 9 10,
  .convex 3 7 9 11,
  .convex 3 7 9 12,
  .convex 3 7 10 11,
  .convex 3 7 10 12,
  .convex 3 7 11 12,
  .convex 3 8 9 10,
  .convex 3 8 9 11,
  .convex 3 8 9 12,
  .convex 3 8 10 11,
  .convex 3 8 10 12,
  .convex 3 8 11 12,
  .convex 3 9 10 11,
  .convex 3 9 10 12,
  .convex 3 9 11 12,
  .convex 3 10 11 12,
  .convex 4 6 8 10,
  .convex 4 6 10 11,
  .convex 4 6 10 12,
  .convex 4 6 11 12,
  .convex 4 10 11 12,
  .convex 5 7 8 9,
  .convex 5 7 8 10,
  .convex 5 7 8 11,
  .convex 5 7 8 12,
  .convex 5 7 9 10,
  .convex 5 7 9 11,
  .convex 5 7 9 12,
  .convex 5 7 10 11,
  .convex 5 7 10 12,
  .convex 5 7 11 12,
  .convex 5 8 9 10,
  .convex 5 8 9 11,
  .convex 5 8 9 12,
  .convex 5 8 10 11,
  .convex 5 8 10 12,
  .convex 5 8 11 12,
  .convex 5 9 10 11,
  .convex 5 9 10 12,
  .convex 5 9 11 12,
  .convex 5 10 11 12,
  .convex 6 10 11 12,
  .convex 7 8 9 10,
  .convex 7 8 9 11,
  .convex 7 8 9 12,
  .convex 7 8 10 11,
  .convex 7 8 10 12,
  .convex 7 8 11 12,
  .convex 7 9 10 11,
  .convex 7 9 10 12,
  .convex 7 9 11 12,
  .convex 7 10 11 12,
  .convex 8 9 10 11,
  .convex 8 9 10 12,
  .convex 8 9 11 12,
  .convex 8 10 11 12,
  .convex 9 10 11 12]

private def clause000 : Sat.Clause := [.pos 0]
private def clause001 : Sat.Clause := [.pos 1]
private def clause002 : Sat.Clause := [.neg 2, .pos 3, .pos 6]
private def clause003 : Sat.Clause := [.neg 2, .pos 3, .neg 6, .pos 7]
private def clause004 : Sat.Clause := [.neg 2, .pos 3, .neg 7, .pos 8]
private def clause005 : Sat.Clause := [.neg 2, .pos 3, .neg 8, .pos 9]
private def clause006 : Sat.Clause := [.neg 2, .neg 3, .pos 4, .pos 6]
private def clause007 : Sat.Clause := [.neg 2, .neg 3, .pos 4, .neg 6, .pos 7]
private def clause008 : Sat.Clause := [.neg 2, .neg 3, .pos 4, .neg 7, .pos 8]
private def clause009 : Sat.Clause := [.neg 2, .neg 3, .pos 4, .neg 8, .pos 9]
private def clause010 : Sat.Clause := [.neg 2, .neg 4, .pos 5, .neg 6, .pos 7]
private def clause011 : Sat.Clause := [.pos 2]
private def clause012 : Sat.Clause := [.pos 10]
private def clause013 : Sat.Clause := [.pos 11]
private def clause014 : Sat.Clause := [.pos 12]
private def clause015 : Sat.Clause := [.pos 13]
private def clause016 : Sat.Clause := [.pos 14]
private def clause017 : Sat.Clause := [.pos 15]
private def clause018 : Sat.Clause := [.pos 16]
private def clause019 : Sat.Clause := [.pos 17]
private def clause020 : Sat.Clause := [.pos 18]
private def clause021 : Sat.Clause := [.pos 19]
private def clause022 : Sat.Clause := [.pos 21]
private def clause023 : Sat.Clause := [.pos 22]
private def clause024 : Sat.Clause := [.pos 23]
private def clause025 : Sat.Clause := [.pos 24]
private def clause026 : Sat.Clause := [.pos 25]
private def clause027 : Sat.Clause := [.pos 27]
private def clause028 : Sat.Clause := [.pos 32]
private def clause029 : Sat.Clause := [.pos 35]
private def clause030 : Sat.Clause := [.neg 39, .neg 40, .pos 41]
private def clause031 : Sat.Clause := [.neg 39, .neg 40, .neg 41, .pos 42]
private def clause032 : Sat.Clause := [.pos 39]
private def clause033 : Sat.Clause := [.pos 46]
private def clause034 : Sat.Clause := [.neg 47, .pos 48, .neg 51]
private def clause035 : Sat.Clause := [.neg 47, .neg 48, .pos 49, .neg 51]
private def clause036 : Sat.Clause := [.neg 47, .neg 49, .pos 50, .neg 51]
private def clause037 : Sat.Clause := [.pos 52]
private def clause038 : Sat.Clause := [.pos 54]
private def clause039 : Sat.Clause := [.pos 59]
private def clause040 : Sat.Clause := [.pos 61]
private def clause041 : Sat.Clause := [.pos 63]
private def clause042 : Sat.Clause := [.pos 66]
private def clause043 : Sat.Clause := [.pos 70]
private def clause044 : Sat.Clause := [.pos 71]
private def clause045 : Sat.Clause := [.pos 75]
private def clause046 : Sat.Clause := [.pos 76]
private def clause047 : Sat.Clause := [.neg 80, .neg 81, .pos 82, .neg 84, .pos 85]
private def clause048 : Sat.Clause := [.neg 80, .neg 82, .pos 83, .neg 84, .pos 85]
private def clause049 : Sat.Clause := [.neg 80, .neg 83, .neg 84, .pos 85]
private def clause050 : Sat.Clause := [.pos 80]
private def clause051 : Sat.Clause := [.pos 86]
private def clause052 : Sat.Clause := [.pos 90]
private def clause053 : Sat.Clause := [.neg 91, .neg 92, .pos 93, .pos 94]
private def clause054 : Sat.Clause := [.neg 91, .neg 92, .pos 93, .neg 94, .pos 95]
private def clause055 : Sat.Clause := [.neg 91, .neg 92, .pos 93, .neg 95, .pos 96]
private def clause056 : Sat.Clause := [.neg 91, .neg 92, .pos 93, .neg 96, .pos 97]
private def clause057 : Sat.Clause := [.neg 91, .neg 92, .pos 93, .neg 97, .pos 98]
private def clause058 : Sat.Clause := [.neg 91, .neg 92, .pos 93, .neg 98]
private def clause059 : Sat.Clause := [.pos 91]
private def clause060 : Sat.Clause := [.pos 99]
private def clause061 : Sat.Clause := [.pos 100]
private def clause062 : Sat.Clause := [.pos 104, .neg 105, .neg 106, .pos 107]
private def clause063 : Sat.Clause := [.pos 104, .neg 105, .neg 107, .pos 108]
private def clause064 : Sat.Clause := [.pos 104, .neg 105, .neg 108, .pos 109]
private def clause065 : Sat.Clause := [.pos 104, .neg 105, .neg 109, .pos 110]
private def clause066 : Sat.Clause := [.pos 104, .neg 105, .neg 110]
private def clause067 : Sat.Clause := [.neg 111, .neg 112, .pos 113, .pos 114]
private def clause068 : Sat.Clause := [.neg 111, .neg 112, .pos 113, .neg 114, .pos 115]
private def clause069 : Sat.Clause := [.neg 111, .neg 112, .pos 113, .neg 115, .pos 116]
private def clause070 : Sat.Clause := [.neg 111, .neg 112, .pos 113, .neg 116, .pos 117]
private def clause071 : Sat.Clause := [.neg 111, .neg 112, .pos 113, .neg 117, .pos 118]
private def clause072 : Sat.Clause := [.neg 111, .neg 112, .pos 113, .neg 118]
private def clause073 : Sat.Clause := [.pos 111]
private def clause074 : Sat.Clause := [.neg 0, .neg 19, .pos 20, .neg 119]
private def clause075 : Sat.Clause := [.neg 0, .neg 29, .pos 30, .neg 126]
private def clause076 : Sat.Clause := [.neg 2, .neg 4, .neg 39, .pos 40, .pos 135]
private def clause077 : Sat.Clause := [.neg 2, .neg 5, .neg 39, .pos 135]
private def clause078 : Sat.Clause := [.neg 2, .neg 6, .neg 39, .pos 42, .neg 135]
private def clause079 : Sat.Clause := [.neg 2, .neg 7, .neg 39, .pos 43, .neg 135]
private def clause080 : Sat.Clause := [.neg 2, .neg 47, .pos 48, .pos 138]
private def clause081 : Sat.Clause := [.neg 2, .neg 9, .neg 47, .pos 51, .neg 138]
private def clause082 : Sat.Clause := [.neg 2, .neg 9, .neg 52, .pos 53, .neg 139]
private def clause083 : Sat.Clause := [.neg 2, .neg 9, .neg 54, .pos 55, .neg 140]
private def clause084 : Sat.Clause := [.neg 2, .neg 4, .neg 56, .pos 57, .pos 141]
private def clause085 : Sat.Clause := [.neg 17, .neg 111, .pos 112, .pos 168]
private def clause086 : Sat.Clause := [.neg 18, .pos 104, .pos 106, .pos 167]
private def clause087 : Sat.Clause := [.neg 19, .neg 20, .neg 32, .pos 33, .neg 170]
private def clause088 : Sat.Clause := [.neg 21, .pos 26, .neg 47]
private def clause089 : Sat.Clause := [.neg 23, .pos 29, .neg 73]
private def clause090 : Sat.Clause := [.neg 25, .pos 29, .neg 88]
private def clause091 : Sat.Clause := [.neg 26, .pos 28, .neg 91]
private def clause092 : Sat.Clause := [.neg 26, .pos 29, .neg 99]
private def clause093 : Sat.Clause := [.neg 27, .pos 29, .neg 102]
private def clause094 : Sat.Clause := [.neg 29, .neg 30, .pos 104, .pos 107, .pos 191]
private def clause095 : Sat.Clause := [.neg 32, .neg 33, .neg 59, .pos 60, .neg 197]
private def clause096 : Sat.Clause := [.neg 39, .neg 42, .neg 66, .pos 67, .neg 213]
private def clause097 : Sat.Clause := [.neg 39, .neg 43, .neg 66, .pos 68, .neg 213]
private def clause098 : Sat.Clause := [.neg 39, .pos 47, .neg 69]
private def clause099 : Sat.Clause := [.neg 46, .pos 47, .neg 79]
private def clause100 : Sat.Clause := [.neg 47, .neg 50, .neg 90, .pos 228]
private def clause101 : Sat.Clause := [.neg 47, .pos 56, .neg 91]
private def clause102 : Sat.Clause := [.neg 47, .neg 48, .neg 91, .pos 92, .pos 229]
private def clause103 : Sat.Clause := [.neg 47, .neg 51, .neg 91, .neg 229]
private def clause104 : Sat.Clause := [.pos 47, .neg 52, .pos 89]
private def clause105 : Sat.Clause := [.neg 52, .neg 53, .neg 100, .neg 231]
private def clause106 : Sat.Clause := [.neg 54, .neg 55, .neg 104, .neg 235]
private def clause107 : Sat.Clause := [.neg 56, .neg 57, .neg 111, .pos 236]
private def clause108 : Sat.Clause := [.pos 44, .pos 45, .neg 59, .neg 60, .neg 210]
private def clause109 : Sat.Clause := [.neg 61, .neg 80, .pos 81, .pos 241]
private def clause110 : Sat.Clause := [.neg 66, .neg 67, .neg 80, .pos 84, .neg 247]
private def clause111 : Sat.Clause := [.neg 66, .neg 68, .neg 80, .pos 85, .neg 247]
private def clause112 : Sat.Clause := [.pos 44, .neg 45, .neg 47, .pos 51, .pos 219]
private def clause113 : Sat.Clause := [.neg 80, .neg 85, .neg 100, .neg 270]
private def clause114 : Sat.Clause := [.neg 91, .neg 93, .neg 111, .pos 281]
private def clause115 : Sat.Clause := [.neg 100, .pos 102, .neg 104]
private def clause116 : Sat.Clause := [.neg 103, .pos 104, .neg 111]
private def clause117 : Sat.Clause := [.pos 104, .pos 105, .neg 111, .neg 113, .pos 285]
private def clause118 : Sat.Clause := [.pos 119]
private def clause119 : Sat.Clause := [.pos 120]
private def clause120 : Sat.Clause := [.pos 121]
private def clause121 : Sat.Clause := [.pos 122]
private def clause122 : Sat.Clause := [.pos 123]
private def clause123 : Sat.Clause := [.pos 124]
private def clause124 : Sat.Clause := [.pos 125]
private def clause125 : Sat.Clause := [.pos 126]
private def clause126 : Sat.Clause := [.pos 128]
private def clause127 : Sat.Clause := [.pos 129]
private def clause128 : Sat.Clause := [.pos 130]
private def clause129 : Sat.Clause := [.pos 131]
private def clause130 : Sat.Clause := [.pos 132]
private def clause131 : Sat.Clause := [.pos 133]
private def clause132 : Sat.Clause := [.pos 143]
private def clause133 : Sat.Clause := [.pos 144]
private def clause134 : Sat.Clause := [.pos 145]
private def clause135 : Sat.Clause := [.pos 146]
private def clause136 : Sat.Clause := [.pos 147]
private def clause137 : Sat.Clause := [.pos 153]
private def clause138 : Sat.Clause := [.pos 154]
private def clause139 : Sat.Clause := [.pos 155]
private def clause140 : Sat.Clause := [.pos 156]
private def clause141 : Sat.Clause := [.neg 161]
private def clause142 : Sat.Clause := [.neg 168]
private def clause143 : Sat.Clause := [.pos 169]
private def clause144 : Sat.Clause := [.pos 170]
private def clause145 : Sat.Clause := [.pos 171]
private def clause146 : Sat.Clause := [.pos 172]
private def clause147 : Sat.Clause := [.pos 173]
private def clause148 : Sat.Clause := [.pos 174]
private def clause149 : Sat.Clause := [.pos 175]
private def clause150 : Sat.Clause := [.neg 176]
private def clause151 : Sat.Clause := [.neg 177]
private def clause152 : Sat.Clause := [.neg 179]
private def clause153 : Sat.Clause := [.pos 180]
private def clause154 : Sat.Clause := [.pos 181]
private def clause155 : Sat.Clause := [.pos 182]
private def clause156 : Sat.Clause := [.pos 183]
private def clause157 : Sat.Clause := [.pos 184]
private def clause158 : Sat.Clause := [.pos 185]
private def clause159 : Sat.Clause := [.pos 186]
private def clause160 : Sat.Clause := [.pos 187]
private def clause161 : Sat.Clause := [.pos 188]
private def clause162 : Sat.Clause := [.neg 189]
private def clause163 : Sat.Clause := [.neg 192]
private def clause164 : Sat.Clause := [.neg 193]
private def clause165 : Sat.Clause := [.neg 194]
private def clause166 : Sat.Clause := [.neg 196]
private def clause167 : Sat.Clause := [.pos 197]
private def clause168 : Sat.Clause := [.pos 198]
private def clause169 : Sat.Clause := [.pos 199]
private def clause170 : Sat.Clause := [.pos 200]
private def clause171 : Sat.Clause := [.pos 201]
private def clause172 : Sat.Clause := [.pos 202]
private def clause173 : Sat.Clause := [.pos 203]
private def clause174 : Sat.Clause := [.pos 204]
private def clause175 : Sat.Clause := [.pos 205]
private def clause176 : Sat.Clause := [.neg 206]
private def clause177 : Sat.Clause := [.neg 209]
private def clause178 : Sat.Clause := [.pos 210]
private def clause179 : Sat.Clause := [.pos 212]
private def clause180 : Sat.Clause := [.pos 213]
private def clause181 : Sat.Clause := [.pos 214]
private def clause182 : Sat.Clause := [.pos 215]
private def clause183 : Sat.Clause := [.pos 216]
private def clause184 : Sat.Clause := [.pos 217]
private def clause185 : Sat.Clause := [.pos 218]
private def clause186 : Sat.Clause := [.pos 220]
private def clause187 : Sat.Clause := [.pos 221]
private def clause188 : Sat.Clause := [.pos 222]
private def clause189 : Sat.Clause := [.pos 223]
private def clause190 : Sat.Clause := [.pos 224]
private def clause191 : Sat.Clause := [.pos 225]
private def clause192 : Sat.Clause := [.pos 226]
private def clause193 : Sat.Clause := [.neg 227]
private def clause194 : Sat.Clause := [.neg 228]
private def clause195 : Sat.Clause := [.pos 231]
private def clause196 : Sat.Clause := [.pos 232]
private def clause197 : Sat.Clause := [.pos 233]
private def clause198 : Sat.Clause := [.pos 234]
private def clause199 : Sat.Clause := [.pos 235]
private def clause200 : Sat.Clause := [.neg 236]
private def clause201 : Sat.Clause := [.pos 237]
private def clause202 : Sat.Clause := [.pos 238]
private def clause203 : Sat.Clause := [.pos 239]
private def clause204 : Sat.Clause := [.pos 240]
private def clause205 : Sat.Clause := [.neg 241]
private def clause206 : Sat.Clause := [.neg 242]
private def clause207 : Sat.Clause := [.neg 245]
private def clause208 : Sat.Clause := [.pos 246]
private def clause209 : Sat.Clause := [.pos 247]
private def clause210 : Sat.Clause := [.pos 248]
private def clause211 : Sat.Clause := [.pos 249]
private def clause212 : Sat.Clause := [.pos 250]
private def clause213 : Sat.Clause := [.neg 251]
private def clause214 : Sat.Clause := [.neg 252]
private def clause215 : Sat.Clause := [.pos 255]
private def clause216 : Sat.Clause := [.pos 256]
private def clause217 : Sat.Clause := [.pos 257]
private def clause218 : Sat.Clause := [.pos 258]
private def clause219 : Sat.Clause := [.pos 259]
private def clause220 : Sat.Clause := [.neg 260]
private def clause221 : Sat.Clause := [.neg 262]
private def clause222 : Sat.Clause := [.neg 265]
private def clause223 : Sat.Clause := [.neg 266]
private def clause224 : Sat.Clause := [.neg 267]
private def clause225 : Sat.Clause := [.pos 270]
private def clause226 : Sat.Clause := [.pos 271]
private def clause227 : Sat.Clause := [.pos 272]
private def clause228 : Sat.Clause := [.pos 273]
private def clause229 : Sat.Clause := [.pos 274]
private def clause230 : Sat.Clause := [.neg 275]
private def clause231 : Sat.Clause := [.pos 276]
private def clause232 : Sat.Clause := [.pos 279]
private def clause233 : Sat.Clause := [.pos 280]
private def clause234 : Sat.Clause := [.neg 281]
private def clause235 : Sat.Clause := [.pos 282]
private def clause236 : Sat.Clause := [.pos 283]
private def clause237 : Sat.Clause := [.neg 284]
private def clause238 : Sat.Clause := [.neg 285]
private def clause239 : Sat.Clause := [.neg 0, .neg 19, .neg 31, .neg 119, .neg 120, .pos 127, .neg 169]
private def clause240 : Sat.Clause := [.neg 119, .neg 120, .neg 127, .neg 169, .pos 286]
private def clause241 : Sat.Clause := [.neg 119, .neg 121, .neg 128, .neg 170, .pos 287]
private def clause242 : Sat.Clause := [.neg 119, .neg 122, .neg 129, .neg 171, .pos 288]
private def clause243 : Sat.Clause := [.neg 119, .neg 123, .neg 130, .neg 172, .pos 289]
private def clause244 : Sat.Clause := [.neg 119, .neg 124, .neg 131, .neg 173, .pos 290]
private def clause245 : Sat.Clause := [.neg 119, .neg 125, .neg 132, .neg 174, .pos 291]
private def clause246 : Sat.Clause := [.neg 119, .neg 126, .neg 133, .neg 175, .pos 292]
private def clause247 : Sat.Clause := [.neg 0, .neg 22, .pos 38, .neg 120, .neg 121, .neg 134, .pos 176]
private def clause248 : Sat.Clause := [.neg 120, .neg 121, .pos 134, .pos 176, .pos 293]
private def clause249 : Sat.Clause := [.neg 0, .neg 24, .pos 44, .neg 120, .neg 122, .neg 136, .pos 177]
private def clause250 : Sat.Clause := [.neg 120, .neg 122, .pos 136, .pos 177, .pos 294]
private def clause251 : Sat.Clause := [.neg 0, .neg 21, .neg 47, .neg 120, .neg 123, .pos 138, .neg 178]
private def clause252 : Sat.Clause := [.neg 120, .neg 123, .pos 138, .pos 178, .pos 295]
private def clause253 : Sat.Clause := [.neg 120, .neg 124, .pos 140, .pos 179, .pos 296]
private def clause254 : Sat.Clause := [.neg 121, .neg 122, .neg 143, .neg 180, .pos 297]
private def clause255 : Sat.Clause := [.neg 121, .neg 123, .neg 144, .neg 181, .pos 298]
private def clause256 : Sat.Clause := [.neg 121, .neg 124, .neg 145, .neg 182, .pos 299]
private def clause257 : Sat.Clause := [.neg 121, .neg 125, .neg 146, .neg 183, .pos 300]
private def clause258 : Sat.Clause := [.neg 121, .neg 126, .neg 147, .neg 184, .pos 301]
private def clause259 : Sat.Clause := [.neg 122, .neg 123, .neg 153, .neg 185, .pos 302]
private def clause260 : Sat.Clause := [.neg 122, .neg 124, .neg 154, .neg 186, .pos 303]
private def clause261 : Sat.Clause := [.neg 122, .neg 125, .neg 155, .neg 187, .pos 304]
private def clause262 : Sat.Clause := [.neg 122, .neg 126, .neg 156, .neg 188, .pos 305]
private def clause263 : Sat.Clause := [.neg 123, .neg 124, .pos 161, .pos 189, .pos 306]
private def clause264 : Sat.Clause := [.neg 124, .neg 125, .neg 166, .neg 190, .pos 307]
private def clause265 : Sat.Clause := [.neg 0, .neg 29, .pos 104, .neg 124, .neg 126, .neg 167, .pos 191]
private def clause266 : Sat.Clause := [.neg 124, .neg 126, .neg 167, .neg 191, .pos 308]
private def clause267 : Sat.Clause := [.neg 125, .neg 126, .pos 168, .pos 192, .pos 309]
private def clause268 : Sat.Clause := [.neg 2, .pos 31, .neg 32, .pos 127, .neg 128, .pos 134, .pos 193]
private def clause269 : Sat.Clause := [.neg 127, .neg 128, .pos 134, .pos 193, .pos 310]
private def clause270 : Sat.Clause := [.neg 127, .neg 129, .pos 136, .pos 194, .pos 311]
private def clause271 : Sat.Clause := [.neg 1, .neg 31, .neg 47, .neg 127, .neg 130, .pos 138, .neg 195]
private def clause272 : Sat.Clause := [.neg 127, .neg 130, .pos 138, .pos 195, .pos 312]
private def clause273 : Sat.Clause := [.neg 127, .neg 131, .pos 140, .pos 196, .pos 313]
private def clause274 : Sat.Clause := [.neg 128, .neg 129, .neg 143, .neg 197, .pos 314]
private def clause275 : Sat.Clause := [.neg 128, .neg 130, .neg 144, .neg 198, .pos 315]
private def clause276 : Sat.Clause := [.neg 128, .neg 131, .neg 145, .neg 199, .pos 316]
private def clause277 : Sat.Clause := [.neg 128, .neg 132, .neg 146, .neg 200, .pos 317]
private def clause278 : Sat.Clause := [.neg 128, .neg 133, .neg 147, .neg 201, .pos 318]
private def clause279 : Sat.Clause := [.neg 129, .neg 130, .neg 153, .neg 202, .pos 319]
private def clause280 : Sat.Clause := [.neg 129, .neg 131, .neg 154, .neg 203, .pos 320]
private def clause281 : Sat.Clause := [.neg 129, .neg 132, .neg 155, .neg 204, .pos 321]
private def clause282 : Sat.Clause := [.neg 129, .neg 133, .neg 156, .neg 205, .pos 322]
private def clause283 : Sat.Clause := [.neg 130, .neg 131, .pos 161, .pos 206, .pos 323]
private def clause284 : Sat.Clause := [.neg 17, .neg 35, .pos 36, .neg 131, .neg 132, .neg 166, .pos 207]
private def clause285 : Sat.Clause := [.neg 131, .neg 132, .neg 166, .neg 207, .pos 324]
private def clause286 : Sat.Clause := [.neg 1, .neg 37, .pos 104, .neg 131, .neg 133, .neg 167, .pos 208]
private def clause287 : Sat.Clause := [.neg 131, .neg 133, .neg 167, .neg 208, .pos 325]
private def clause288 : Sat.Clause := [.neg 132, .neg 133, .pos 168, .pos 209, .pos 326]
private def clause289 : Sat.Clause := [.neg 2, .neg 38, .neg 59, .neg 134, .pos 136, .neg 143, .neg 210]
private def clause290 : Sat.Clause := [.pos 134, .pos 136, .neg 143, .neg 210, .pos 327]
private def clause291 : Sat.Clause := [.neg 2, .neg 38, .neg 62, .pos 134, .pos 138, .neg 144, .pos 211]
private def clause292 : Sat.Clause := [.pos 134, .pos 138, .neg 144, .neg 211, .pos 328]
private def clause293 : Sat.Clause := [.pos 134, .pos 140, .neg 145, .neg 212, .pos 329]
private def clause294 : Sat.Clause := [.neg 2, .neg 39, .neg 66, .neg 135, .pos 137, .pos 148, .neg 213]
private def clause295 : Sat.Clause := [.neg 2, .neg 39, .neg 66, .neg 135, .pos 137, .neg 148, .neg 213]
private def clause296 : Sat.Clause := [.neg 2, .neg 39, .neg 66, .neg 135, .neg 137, .pos 148, .neg 213]
private def clause297 : Sat.Clause := [.neg 135, .neg 137, .neg 148, .neg 213, .pos 330]
private def clause298 : Sat.Clause := [.neg 2, .neg 39, .neg 70, .neg 135, .pos 139, .pos 149, .neg 215]
private def clause299 : Sat.Clause := [.neg 2, .neg 39, .neg 70, .neg 135, .pos 139, .neg 149, .neg 215]
private def clause300 : Sat.Clause := [.neg 2, .neg 39, .neg 70, .neg 135, .neg 139, .pos 149, .neg 215]
private def clause301 : Sat.Clause := [.neg 135, .neg 139, .neg 149, .neg 215, .pos 331]
private def clause302 : Sat.Clause := [.neg 2, .neg 39, .neg 71, .pos 135, .neg 140, .pos 150, .neg 216]
private def clause303 : Sat.Clause := [.neg 2, .neg 39, .neg 71, .neg 135, .pos 140, .pos 150, .neg 216]
private def clause304 : Sat.Clause := [.neg 2, .neg 39, .neg 71, .neg 135, .pos 140, .neg 150, .neg 216]
private def clause305 : Sat.Clause := [.neg 2, .neg 39, .neg 71, .neg 135, .neg 140, .pos 150, .neg 216]
private def clause306 : Sat.Clause := [.pos 135, .pos 140, .neg 150, .neg 216, .pos 332]
private def clause307 : Sat.Clause := [.pos 135, .neg 140, .neg 150, .neg 216, .neg 332]
private def clause308 : Sat.Clause := [.neg 135, .neg 140, .neg 150, .neg 216, .pos 332]
private def clause309 : Sat.Clause := [.neg 135, .neg 141, .neg 151, .neg 217, .pos 333]
private def clause310 : Sat.Clause := [.neg 135, .neg 142, .neg 152, .neg 218, .pos 334]
private def clause311 : Sat.Clause := [.pos 136, .pos 138, .neg 153, .neg 219, .pos 335]
private def clause312 : Sat.Clause := [.neg 2, .neg 44, .neg 76, .neg 136, .pos 140, .neg 154, .neg 221]
private def clause313 : Sat.Clause := [.pos 136, .pos 140, .neg 154, .neg 221, .pos 336]
private def clause314 : Sat.Clause := [.neg 2, .neg 46, .neg 80, .neg 137, .neg 139, .pos 157, .neg 223]
private def clause315 : Sat.Clause := [.neg 137, .neg 139, .neg 157, .neg 223, .pos 337]
private def clause316 : Sat.Clause := [.neg 2, .neg 46, .neg 86, .pos 137, .neg 140, .pos 158, .neg 224]
private def clause317 : Sat.Clause := [.neg 2, .neg 46, .neg 86, .neg 137, .neg 140, .pos 158, .neg 224]
private def clause318 : Sat.Clause := [.neg 137, .neg 140, .neg 158, .neg 224, .pos 338]
private def clause319 : Sat.Clause := [.neg 137, .neg 141, .neg 159, .neg 225, .pos 339]
private def clause320 : Sat.Clause := [.neg 137, .neg 142, .neg 160, .neg 226, .pos 340]
private def clause321 : Sat.Clause := [.pos 138, .pos 140, .pos 161, .pos 228, .pos 341]
private def clause322 : Sat.Clause := [.neg 2, .neg 52, .neg 100, .pos 139, .neg 140, .pos 163, .neg 231]
private def clause323 : Sat.Clause := [.neg 2, .neg 52, .neg 100, .neg 139, .neg 140, .pos 163, .neg 231]
private def clause324 : Sat.Clause := [.pos 139, .neg 140, .neg 163, .neg 231, .neg 342]
private def clause325 : Sat.Clause := [.neg 139, .neg 140, .neg 163, .neg 231, .pos 342]
private def clause326 : Sat.Clause := [.neg 139, .neg 141, .neg 164, .neg 232, .pos 343]
private def clause327 : Sat.Clause := [.neg 2, .neg 52, .neg 102, .neg 139, .neg 142, .pos 165, .neg 233]
private def clause328 : Sat.Clause := [.neg 139, .neg 142, .neg 165, .neg 233, .pos 344]
private def clause329 : Sat.Clause := [.neg 140, .neg 141, .neg 166, .neg 234, .pos 345]
private def clause330 : Sat.Clause := [.neg 2, .neg 54, .neg 104, .neg 140, .pos 142, .neg 167, .neg 235]
private def clause331 : Sat.Clause := [.neg 140, .neg 142, .neg 167, .neg 235, .pos 346]
private def clause332 : Sat.Clause := [.neg 141, .neg 142, .pos 168, .pos 236, .pos 347]
private def clause333 : Sat.Clause := [.neg 143, .neg 144, .neg 153, .neg 237, .pos 348]
private def clause334 : Sat.Clause := [.neg 143, .neg 145, .neg 154, .neg 238, .pos 349]
private def clause335 : Sat.Clause := [.neg 143, .neg 146, .neg 155, .neg 239, .pos 350]
private def clause336 : Sat.Clause := [.neg 143, .neg 147, .neg 156, .neg 240, .pos 351]
private def clause337 : Sat.Clause := [.neg 144, .neg 145, .pos 161, .pos 242, .pos 352]
private def clause338 : Sat.Clause := [.neg 145, .neg 146, .neg 166, .neg 243, .pos 353]
private def clause339 : Sat.Clause := [.neg 10, .neg 65, .pos 104, .neg 145, .neg 147, .neg 167, .pos 244]
private def clause340 : Sat.Clause := [.neg 145, .neg 147, .neg 167, .neg 244, .pos 354]
private def clause341 : Sat.Clause := [.neg 146, .neg 147, .pos 168, .pos 245, .pos 355]
private def clause342 : Sat.Clause := [.neg 148, .neg 149, .neg 157, .neg 247, .pos 356]
private def clause343 : Sat.Clause := [.neg 148, .neg 150, .neg 158, .neg 248, .pos 357]
private def clause344 : Sat.Clause := [.neg 17, .neg 66, .pos 72, .neg 148, .pos 151, .neg 159, .neg 249]
private def clause345 : Sat.Clause := [.neg 148, .neg 151, .neg 159, .neg 249, .pos 358]
private def clause346 : Sat.Clause := [.neg 148, .neg 152, .neg 160, .neg 250, .pos 359]
private def clause347 : Sat.Clause := [.neg 149, .neg 150, .neg 163, .neg 255, .pos 360]
private def clause348 : Sat.Clause := [.neg 149, .neg 151, .neg 164, .neg 256, .pos 361]
private def clause349 : Sat.Clause := [.neg 149, .neg 152, .neg 165, .neg 257, .pos 362]
private def clause350 : Sat.Clause := [.neg 150, .neg 151, .neg 166, .neg 258, .pos 363]
private def clause351 : Sat.Clause := [.neg 11, .neg 71, .neg 104, .neg 150, .pos 152, .neg 167, .neg 259]
private def clause352 : Sat.Clause := [.neg 150, .neg 152, .neg 167, .neg 259, .pos 364]
private def clause353 : Sat.Clause := [.neg 11, .neg 72, .neg 111, .pos 151, .neg 152, .pos 168, .pos 260]
private def clause354 : Sat.Clause := [.neg 151, .neg 152, .pos 168, .pos 260, .pos 365]
private def clause355 : Sat.Clause := [.neg 153, .neg 154, .pos 161, .pos 262, .pos 366]
private def clause356 : Sat.Clause := [.neg 17, .neg 76, .pos 77, .neg 154, .neg 155, .neg 166, .pos 263]
private def clause357 : Sat.Clause := [.neg 154, .neg 155, .neg 166, .neg 263, .pos 367]
private def clause358 : Sat.Clause := [.neg 12, .neg 78, .pos 104, .neg 154, .neg 156, .neg 167, .pos 264]
private def clause359 : Sat.Clause := [.neg 18, .neg 76, .pos 78, .neg 154, .neg 156, .neg 167, .pos 264]
private def clause360 : Sat.Clause := [.neg 154, .neg 156, .neg 167, .neg 264, .pos 368]
private def clause361 : Sat.Clause := [.neg 155, .neg 156, .pos 168, .pos 265, .pos 369]
private def clause362 : Sat.Clause := [.neg 157, .neg 158, .neg 163, .neg 270, .pos 370]
private def clause363 : Sat.Clause := [.neg 17, .neg 80, .pos 87, .neg 157, .pos 159, .neg 164, .neg 271]
private def clause364 : Sat.Clause := [.neg 157, .neg 159, .neg 164, .neg 271, .pos 371]
private def clause365 : Sat.Clause := [.neg 157, .neg 160, .neg 165, .neg 272, .pos 372]
private def clause366 : Sat.Clause := [.neg 158, .neg 159, .neg 166, .neg 273, .pos 373]
private def clause367 : Sat.Clause := [.neg 13, .neg 86, .neg 104, .neg 158, .pos 160, .pos 167, .neg 274]
private def clause368 : Sat.Clause := [.neg 13, .neg 86, .neg 104, .neg 158, .pos 160, .neg 167, .neg 274]
private def clause369 : Sat.Clause := [.neg 13, .neg 86, .neg 104, .neg 158, .neg 160, .pos 167, .neg 274]
private def clause370 : Sat.Clause := [.neg 158, .neg 160, .neg 167, .neg 274, .pos 374]
private def clause371 : Sat.Clause := [.neg 13, .neg 87, .neg 111, .pos 159, .neg 160, .pos 168, .pos 275]
private def clause372 : Sat.Clause := [.neg 159, .neg 160, .pos 168, .pos 275, .pos 375]
private def clause373 : Sat.Clause := [.neg 14, .neg 91, .pos 103, .pos 161, .pos 162, .pos 166, .neg 279]
private def clause374 : Sat.Clause := [.neg 14, .neg 91, .pos 103, .pos 161, .neg 162, .pos 166, .neg 279]
private def clause375 : Sat.Clause := [.neg 17, .neg 100, .pos 101, .neg 163, .pos 164, .neg 166, .neg 282]
private def clause376 : Sat.Clause := [.neg 163, .neg 164, .neg 166, .neg 282, .pos 376]
private def clause377 : Sat.Clause := [.neg 15, .neg 100, .neg 104, .neg 163, .pos 165, .neg 167, .neg 283]
private def clause378 : Sat.Clause := [.neg 163, .neg 165, .neg 167, .neg 283, .pos 377]
private def clause379 : Sat.Clause := [.neg 15, .neg 101, .neg 111, .pos 164, .neg 165, .pos 168, .pos 284]
private def clause380 : Sat.Clause := [.neg 164, .neg 165, .pos 168, .pos 284, .pos 378]
private def clause381 : Sat.Clause := [.neg 16, .neg 103, .neg 111, .pos 166, .neg 167, .pos 168, .pos 285]
private def clause382 : Sat.Clause := [.neg 17, .pos 104, .neg 111, .pos 166, .neg 167, .pos 168, .pos 285]
private def clause383 : Sat.Clause := [.pos 166, .neg 167, .pos 168, .pos 285, .neg 379]
private def clause384 : Sat.Clause := [.neg 166, .neg 167, .pos 168, .pos 285, .pos 379]
private def clause385 : Sat.Clause := [.neg 169, .neg 170, .pos 176, .pos 193, .pos 380]
private def clause386 : Sat.Clause := [.neg 169, .neg 171, .pos 177, .pos 194, .pos 381]
private def clause387 : Sat.Clause := [.neg 21, .pos 31, .neg 34, .neg 169, .neg 172, .pos 178, .neg 195]
private def clause388 : Sat.Clause := [.neg 169, .neg 172, .pos 178, .pos 195, .pos 382]
private def clause389 : Sat.Clause := [.neg 169, .neg 173, .pos 179, .pos 196, .pos 383]
private def clause390 : Sat.Clause := [.neg 170, .neg 171, .neg 180, .neg 197, .pos 384]
private def clause391 : Sat.Clause := [.neg 170, .neg 172, .neg 181, .neg 198, .pos 385]
private def clause392 : Sat.Clause := [.neg 170, .neg 173, .neg 182, .neg 199, .pos 386]
private def clause393 : Sat.Clause := [.neg 170, .neg 174, .neg 183, .neg 200, .pos 387]
private def clause394 : Sat.Clause := [.neg 170, .neg 175, .neg 184, .neg 201, .pos 388]
private def clause395 : Sat.Clause := [.neg 171, .neg 172, .neg 185, .neg 202, .pos 389]
private def clause396 : Sat.Clause := [.neg 171, .neg 173, .neg 186, .neg 203, .pos 390]
private def clause397 : Sat.Clause := [.neg 171, .neg 174, .neg 187, .neg 204, .pos 391]
private def clause398 : Sat.Clause := [.neg 171, .neg 175, .neg 188, .neg 205, .pos 392]
private def clause399 : Sat.Clause := [.neg 172, .neg 173, .pos 189, .pos 206, .pos 393]
private def clause400 : Sat.Clause := [.neg 19, .pos 28, .neg 35, .neg 173, .neg 174, .pos 190, .neg 207]
private def clause401 : Sat.Clause := [.neg 173, .neg 174, .neg 190, .neg 207, .pos 394]
private def clause402 : Sat.Clause := [.neg 19, .neg 35, .neg 104, .neg 173, .neg 175, .pos 191, .neg 208]
private def clause403 : Sat.Clause := [.neg 173, .neg 175, .neg 191, .neg 208, .pos 395]
private def clause404 : Sat.Clause := [.neg 174, .neg 175, .pos 192, .pos 209, .pos 396]
private def clause405 : Sat.Clause := [.pos 176, .pos 177, .neg 180, .neg 210, .pos 397]
private def clause406 : Sat.Clause := [.neg 22, .pos 38, .neg 47, .pos 176, .pos 178, .neg 181, .pos 211]
private def clause407 : Sat.Clause := [.pos 176, .pos 178, .neg 181, .neg 211, .pos 398]
private def clause408 : Sat.Clause := [.pos 176, .pos 179, .neg 182, .neg 212, .pos 399]
private def clause409 : Sat.Clause := [.pos 177, .pos 178, .neg 185, .neg 219, .pos 400]
private def clause410 : Sat.Clause := [.pos 177, .pos 179, .neg 186, .neg 221, .pos 401]
private def clause411 : Sat.Clause := [.pos 178, .pos 179, .pos 189, .pos 228, .pos 402]
private def clause412 : Sat.Clause := [.neg 180, .neg 181, .neg 185, .neg 237, .pos 403]
private def clause413 : Sat.Clause := [.neg 180, .neg 182, .neg 186, .neg 238, .pos 404]
private def clause414 : Sat.Clause := [.neg 180, .neg 183, .neg 187, .neg 239, .pos 405]
private def clause415 : Sat.Clause := [.neg 180, .neg 184, .neg 188, .neg 240, .pos 406]
private def clause416 : Sat.Clause := [.neg 181, .neg 182, .pos 189, .pos 242, .pos 407]
private def clause417 : Sat.Clause := [.neg 182, .neg 183, .neg 190, .neg 243, .pos 408]
private def clause418 : Sat.Clause := [.neg 182, .neg 184, .neg 191, .neg 244, .pos 409]
private def clause419 : Sat.Clause := [.neg 183, .neg 184, .pos 192, .pos 245, .pos 410]
private def clause420 : Sat.Clause := [.neg 185, .neg 186, .pos 189, .pos 262, .pos 411]
private def clause421 : Sat.Clause := [.neg 186, .neg 187, .neg 190, .neg 263, .pos 412]
private def clause422 : Sat.Clause := [.neg 186, .neg 188, .neg 191, .neg 264, .pos 413]
private def clause423 : Sat.Clause := [.neg 187, .neg 188, .pos 192, .pos 265, .pos 414]
private def clause424 : Sat.Clause := [.neg 28, .pos 104, .neg 111, .pos 190, .neg 191, .pos 192, .pos 285]
private def clause425 : Sat.Clause := [.neg 190, .pos 191, .pos 192, .pos 285, .neg 415]
private def clause426 : Sat.Clause := [.neg 190, .neg 191, .pos 192, .pos 285, .pos 415]
private def clause427 : Sat.Clause := [.pos 193, .pos 194, .neg 197, .neg 210, .pos 416]
private def clause428 : Sat.Clause := [.neg 32, .pos 34, .neg 47, .pos 193, .neg 195, .neg 198, .neg 211]
private def clause429 : Sat.Clause := [.pos 193, .pos 195, .neg 198, .neg 211, .pos 417]
private def clause430 : Sat.Clause := [.pos 193, .pos 196, .neg 199, .neg 212, .pos 418]
private def clause431 : Sat.Clause := [.pos 194, .pos 195, .neg 202, .neg 219, .pos 419]
private def clause432 : Sat.Clause := [.pos 194, .pos 196, .neg 203, .neg 221, .pos 420]
private def clause433 : Sat.Clause := [.pos 195, .pos 196, .pos 206, .pos 228, .pos 421]
private def clause434 : Sat.Clause := [.neg 197, .neg 198, .neg 202, .neg 237, .pos 422]
private def clause435 : Sat.Clause := [.neg 197, .neg 199, .neg 203, .neg 238, .pos 423]
private def clause436 : Sat.Clause := [.neg 197, .neg 200, .neg 204, .neg 239, .pos 424]
private def clause437 : Sat.Clause := [.neg 197, .neg 201, .neg 205, .neg 240, .pos 425]
private def clause438 : Sat.Clause := [.neg 198, .neg 199, .pos 206, .pos 242, .pos 426]
private def clause439 : Sat.Clause := [.neg 32, .pos 36, .neg 63, .neg 199, .neg 200, .pos 207, .neg 243]
private def clause440 : Sat.Clause := [.neg 199, .neg 200, .neg 207, .neg 243, .pos 427]
private def clause441 : Sat.Clause := [.neg 32, .pos 37, .neg 63, .neg 199, .neg 201, .pos 208, .neg 244]
private def clause442 : Sat.Clause := [.neg 199, .neg 201, .neg 208, .neg 244, .pos 428]
private def clause443 : Sat.Clause := [.neg 200, .neg 201, .pos 209, .pos 245, .pos 429]
private def clause444 : Sat.Clause := [.neg 202, .neg 203, .pos 206, .pos 262, .pos 430]
private def clause445 : Sat.Clause := [.neg 203, .neg 204, .neg 207, .neg 263, .pos 431]
private def clause446 : Sat.Clause := [.neg 203, .neg 205, .neg 208, .neg 264, .pos 432]
private def clause447 : Sat.Clause := [.neg 204, .neg 205, .pos 209, .pos 265, .pos 433]
private def clause448 : Sat.Clause := [.neg 36, .pos 104, .neg 111, .pos 207, .neg 208, .pos 209, .pos 285]
private def clause449 : Sat.Clause := [.neg 36, .pos 104, .neg 111, .pos 207, .pos 208, .pos 209, .pos 285]
private def clause450 : Sat.Clause := [.pos 207, .neg 208, .pos 209, .pos 285, .neg 434]
private def clause451 : Sat.Clause := [.neg 207, .pos 208, .pos 209, .pos 285, .neg 434]
private def clause452 : Sat.Clause := [.neg 207, .neg 208, .pos 209, .pos 285, .pos 434]
private def clause453 : Sat.Clause := [.neg 47, .neg 59, .pos 62, .neg 210, .pos 211, .neg 219, .neg 237]
private def clause454 : Sat.Clause := [.neg 210, .neg 211, .neg 219, .neg 237, .pos 435]
private def clause455 : Sat.Clause := [.neg 210, .neg 212, .neg 221, .neg 238, .pos 436]
private def clause456 : Sat.Clause := [.pos 211, .neg 212, .pos 228, .pos 242, .neg 437]
private def clause457 : Sat.Clause := [.neg 211, .neg 212, .pos 228, .pos 242, .pos 437]
private def clause458 : Sat.Clause := [.neg 213, .neg 214, .neg 222, .neg 246, .pos 438]
private def clause459 : Sat.Clause := [.neg 213, .neg 215, .neg 223, .neg 247, .pos 439]
private def clause460 : Sat.Clause := [.neg 213, .neg 216, .neg 224, .neg 248, .pos 440]
private def clause461 : Sat.Clause := [.neg 213, .neg 217, .neg 225, .neg 249, .pos 441]
private def clause462 : Sat.Clause := [.neg 213, .neg 218, .neg 226, .neg 250, .pos 442]
private def clause463 : Sat.Clause := [.neg 214, .neg 215, .pos 227, .pos 251, .pos 443]
private def clause464 : Sat.Clause := [.neg 214, .neg 216, .pos 228, .pos 252, .pos 444]
private def clause465 : Sat.Clause := [.neg 214, .neg 217, .pos 229, .pos 253, .pos 445]
private def clause466 : Sat.Clause := [.neg 214, .neg 218, .pos 230, .pos 254, .pos 446]
private def clause467 : Sat.Clause := [.neg 215, .neg 216, .neg 231, .neg 255, .pos 447]
private def clause468 : Sat.Clause := [.neg 215, .neg 217, .neg 232, .neg 256, .pos 448]
private def clause469 : Sat.Clause := [.neg 215, .neg 218, .neg 233, .neg 257, .pos 449]
private def clause470 : Sat.Clause := [.neg 216, .neg 217, .neg 234, .neg 258, .pos 450]
private def clause471 : Sat.Clause := [.neg 216, .neg 218, .neg 235, .neg 259, .pos 451]
private def clause472 : Sat.Clause := [.neg 217, .neg 218, .pos 236, .pos 260, .pos 452]
private def clause473 : Sat.Clause := [.neg 47, .pos 74, .neg 75, .pos 219, .neg 220, .pos 227, .neg 261]
private def clause474 : Sat.Clause := [.neg 47, .pos 74, .neg 75, .pos 219, .neg 220, .pos 227, .pos 261]
private def clause475 : Sat.Clause := [.neg 44, .neg 74, .neg 90, .pos 219, .neg 221, .pos 228, .pos 262]
private def clause476 : Sat.Clause := [.neg 219, .neg 221, .pos 228, .pos 262, .pos 453]
private def clause477 : Sat.Clause := [.neg 222, .neg 223, .pos 227, .pos 266, .pos 454]
private def clause478 : Sat.Clause := [.neg 222, .neg 224, .pos 228, .pos 267, .pos 455]
private def clause479 : Sat.Clause := [.neg 46, .pos 56, .neg 91, .neg 222, .neg 225, .neg 229, .pos 268]
private def clause480 : Sat.Clause := [.neg 222, .neg 225, .pos 229, .pos 268, .pos 456]
private def clause481 : Sat.Clause := [.neg 222, .neg 226, .pos 230, .pos 269, .pos 457]
private def clause482 : Sat.Clause := [.neg 223, .neg 224, .neg 231, .neg 270, .pos 458]
private def clause483 : Sat.Clause := [.neg 223, .neg 225, .neg 232, .neg 271, .pos 459]
private def clause484 : Sat.Clause := [.neg 223, .neg 226, .neg 233, .neg 272, .pos 460]
private def clause485 : Sat.Clause := [.neg 224, .neg 225, .neg 234, .neg 273, .pos 461]
private def clause486 : Sat.Clause := [.neg 224, .neg 226, .neg 235, .neg 274, .pos 462]
private def clause487 : Sat.Clause := [.neg 225, .neg 226, .pos 236, .pos 275, .pos 463]
private def clause488 : Sat.Clause := [.pos 227, .pos 228, .neg 231, .neg 276, .pos 464]
private def clause489 : Sat.Clause := [.pos 227, .pos 229, .neg 232, .neg 277, .pos 465]
private def clause490 : Sat.Clause := [.pos 227, .pos 230, .neg 233, .neg 278, .pos 466]
private def clause491 : Sat.Clause := [.pos 47, .neg 54, .neg 103, .pos 228, .neg 229, .neg 234, .neg 279]
private def clause492 : Sat.Clause := [.pos 47, .neg 56, .pos 103, .pos 228, .neg 229, .neg 234, .neg 279]
private def clause493 : Sat.Clause := [.neg 54, .pos 56, .neg 91, .pos 228, .neg 229, .neg 234, .neg 279]
private def clause494 : Sat.Clause := [.pos 228, .pos 229, .neg 234, .neg 279, .pos 467]
private def clause495 : Sat.Clause := [.pos 47, .neg 54, .neg 104, .pos 228, .neg 230, .neg 235, .neg 280]
private def clause496 : Sat.Clause := [.pos 47, .neg 58, .pos 104, .pos 228, .neg 230, .neg 235, .neg 280]
private def clause497 : Sat.Clause := [.neg 54, .pos 58, .neg 99, .pos 228, .neg 230, .neg 235, .neg 280]
private def clause498 : Sat.Clause := [.pos 228, .pos 230, .neg 235, .neg 280, .pos 468]
private def clause499 : Sat.Clause := [.pos 228, .neg 230, .neg 235, .neg 280, .neg 468]
private def clause500 : Sat.Clause := [.pos 229, .pos 230, .pos 236, .pos 281, .pos 469]
private def clause501 : Sat.Clause := [.neg 229, .pos 230, .pos 236, .pos 281, .neg 469]
private def clause502 : Sat.Clause := [.neg 231, .neg 232, .neg 234, .neg 282, .pos 470]
private def clause503 : Sat.Clause := [.neg 231, .neg 233, .neg 235, .neg 283, .pos 471]
private def clause504 : Sat.Clause := [.neg 232, .neg 233, .pos 236, .pos 284, .pos 472]
private def clause505 : Sat.Clause := [.neg 234, .neg 235, .pos 236, .pos 285, .pos 473]
private def clause506 : Sat.Clause := [.neg 237, .neg 238, .pos 242, .pos 262, .pos 474]
private def clause507 : Sat.Clause := [.neg 59, .pos 64, .neg 76, .neg 238, .neg 239, .pos 243, .neg 263]
private def clause508 : Sat.Clause := [.neg 238, .neg 239, .pos 243, .neg 263, .neg 475]
private def clause509 : Sat.Clause := [.neg 238, .neg 239, .neg 243, .neg 263, .pos 475]
private def clause510 : Sat.Clause := [.neg 59, .pos 65, .neg 76, .neg 238, .neg 240, .pos 244, .neg 264]
private def clause511 : Sat.Clause := [.neg 238, .neg 240, .neg 244, .neg 264, .pos 476]
private def clause512 : Sat.Clause := [.neg 239, .neg 240, .pos 245, .pos 265, .pos 477]
private def clause513 : Sat.Clause := [.neg 64, .pos 104, .neg 111, .pos 243, .neg 244, .pos 245, .pos 285]
private def clause514 : Sat.Clause := [.neg 243, .neg 244, .pos 245, .pos 285, .pos 478]
private def clause515 : Sat.Clause := [.neg 246, .neg 247, .pos 251, .pos 266, .pos 479]
private def clause516 : Sat.Clause := [.neg 246, .neg 248, .pos 252, .pos 267, .pos 480]
private def clause517 : Sat.Clause := [.neg 66, .pos 72, .neg 91, .neg 246, .neg 249, .neg 253, .pos 268]
private def clause518 : Sat.Clause := [.neg 246, .neg 249, .pos 253, .pos 268, .pos 481]
private def clause519 : Sat.Clause := [.neg 246, .neg 250, .pos 254, .pos 269, .pos 482]
private def clause520 : Sat.Clause := [.neg 247, .neg 248, .neg 255, .neg 270, .pos 483]
private def clause521 : Sat.Clause := [.neg 247, .neg 249, .neg 256, .neg 271, .pos 484]
private def clause522 : Sat.Clause := [.neg 247, .neg 250, .neg 257, .neg 272, .pos 485]
private def clause523 : Sat.Clause := [.neg 248, .neg 249, .neg 258, .neg 273, .pos 486]
private def clause524 : Sat.Clause := [.neg 248, .neg 250, .neg 259, .neg 274, .pos 487]
private def clause525 : Sat.Clause := [.neg 249, .neg 250, .pos 260, .pos 275, .pos 488]
private def clause526 : Sat.Clause := [.pos 251, .pos 252, .neg 255, .neg 276, .pos 489]
private def clause527 : Sat.Clause := [.pos 69, .neg 70, .neg 101, .pos 251, .pos 253, .neg 256, .pos 277]
private def clause528 : Sat.Clause := [.pos 251, .pos 253, .neg 256, .neg 277, .pos 490]
private def clause529 : Sat.Clause := [.pos 251, .pos 254, .neg 257, .neg 278, .pos 491]
private def clause530 : Sat.Clause := [.pos 69, .neg 71, .neg 103, .pos 252, .neg 253, .neg 258, .neg 279]
private def clause531 : Sat.Clause := [.pos 252, .pos 253, .neg 258, .neg 279, .pos 492]
private def clause532 : Sat.Clause := [.pos 69, .neg 71, .neg 104, .pos 252, .neg 254, .neg 259, .neg 280]
private def clause533 : Sat.Clause := [.neg 71, .pos 73, .neg 99, .pos 252, .neg 254, .neg 259, .neg 280]
private def clause534 : Sat.Clause := [.pos 252, .pos 254, .neg 259, .neg 280, .pos 493]
private def clause535 : Sat.Clause := [.pos 252, .neg 254, .neg 259, .neg 280, .neg 493]
private def clause536 : Sat.Clause := [.pos 69, .neg 72, .neg 111, .neg 253, .pos 254, .pos 260, .pos 281]
private def clause537 : Sat.Clause := [.pos 253, .pos 254, .pos 260, .pos 281, .pos 494]
private def clause538 : Sat.Clause := [.neg 253, .pos 254, .pos 260, .pos 281, .neg 494]
private def clause539 : Sat.Clause := [.neg 255, .neg 256, .neg 258, .neg 282, .pos 495]
private def clause540 : Sat.Clause := [.neg 255, .neg 257, .neg 259, .neg 283, .pos 496]
private def clause541 : Sat.Clause := [.neg 256, .neg 257, .pos 260, .pos 284, .pos 497]
private def clause542 : Sat.Clause := [.neg 258, .neg 259, .pos 260, .pos 285, .pos 498]
private def clause543 : Sat.Clause := [.neg 77, .pos 104, .neg 111, .pos 263, .neg 264, .pos 265, .pos 285]
private def clause544 : Sat.Clause := [.neg 263, .neg 264, .pos 265, .pos 285, .pos 499]
private def clause545 : Sat.Clause := [.pos 266, .pos 267, .neg 270, .neg 276, .pos 500]
private def clause546 : Sat.Clause := [.pos 266, .pos 268, .neg 271, .neg 277, .pos 501]
private def clause547 : Sat.Clause := [.pos 266, .pos 269, .neg 272, .neg 278, .pos 502]
private def clause548 : Sat.Clause := [.pos 79, .neg 86, .neg 103, .pos 267, .neg 268, .neg 273, .neg 279]
private def clause549 : Sat.Clause := [.neg 86, .pos 87, .neg 91, .pos 267, .neg 268, .neg 273, .neg 279]
private def clause550 : Sat.Clause := [.pos 267, .pos 268, .neg 273, .neg 279, .pos 503]
private def clause551 : Sat.Clause := [.pos 79, .neg 86, .neg 104, .pos 267, .neg 269, .neg 274, .neg 280]
private def clause552 : Sat.Clause := [.neg 86, .pos 88, .neg 99, .pos 267, .neg 269, .neg 274, .neg 280]
private def clause553 : Sat.Clause := [.pos 267, .pos 269, .neg 274, .neg 280, .pos 504]
private def clause554 : Sat.Clause := [.pos 267, .neg 269, .neg 274, .neg 280, .neg 504]
private def clause555 : Sat.Clause := [.pos 79, .neg 87, .neg 111, .neg 268, .pos 269, .pos 275, .pos 281]
private def clause556 : Sat.Clause := [.pos 88, .neg 91, .neg 111, .neg 268, .pos 269, .pos 275, .pos 281]
private def clause557 : Sat.Clause := [.pos 268, .pos 269, .pos 275, .pos 281, .pos 505]
private def clause558 : Sat.Clause := [.neg 268, .pos 269, .pos 275, .pos 281, .neg 505]
private def clause559 : Sat.Clause := [.neg 270, .neg 271, .neg 273, .neg 282, .pos 506]
private def clause560 : Sat.Clause := [.neg 270, .neg 272, .neg 274, .neg 283, .pos 507]
private def clause561 : Sat.Clause := [.neg 271, .neg 272, .pos 275, .pos 284, .pos 508]
private def clause562 : Sat.Clause := [.neg 273, .neg 274, .pos 275, .pos 285, .pos 509]
private def clause563 : Sat.Clause := [.neg 89, .neg 100, .neg 103, .neg 276, .pos 277, .neg 279, .neg 282]
private def clause564 : Sat.Clause := [.neg 91, .neg 100, .pos 101, .neg 276, .pos 277, .neg 279, .neg 282]
private def clause565 : Sat.Clause := [.neg 276, .neg 277, .neg 279, .neg 282, .pos 510]
private def clause566 : Sat.Clause := [.neg 89, .neg 100, .neg 104, .neg 276, .pos 278, .neg 280, .neg 283]
private def clause567 : Sat.Clause := [.neg 99, .neg 100, .pos 102, .neg 276, .pos 278, .neg 280, .neg 283]
private def clause568 : Sat.Clause := [.neg 276, .pos 278, .neg 280, .neg 283, .neg 511]
private def clause569 : Sat.Clause := [.neg 276, .neg 278, .neg 280, .neg 283, .pos 511]
private def clause570 : Sat.Clause := [.pos 277, .neg 278, .pos 281, .pos 284, .neg 512]
private def clause571 : Sat.Clause := [.neg 277, .neg 278, .pos 281, .pos 284, .pos 512]
private def clause572 : Sat.Clause := [.neg 279, .neg 280, .pos 281, .pos 285, .pos 513]
private def clause573 : Sat.Clause := [.neg 282, .neg 283, .pos 284, .pos 285, .pos 514]
private def clause574 : Sat.Clause := [.neg 286, .neg 287, .neg 288, .neg 289, .neg 290, .neg 293, .neg 294, .neg 295, .neg 296, .neg 297, .neg 298, .neg 299, .neg 302, .neg 303, .neg 306, .neg 310, .neg 311, .neg 312, .neg 313, .neg 314, .neg 315, .neg 316, .neg 319, .neg 320, .neg 323, .neg 327, .neg 328, .neg 329, .neg 335, .neg 336, .neg 341, .neg 348, .neg 349, .neg 352, .neg 366, .neg 380, .neg 381, .neg 382, .neg 383, .neg 384, .neg 385, .neg 386, .neg 389, .neg 390, .neg 393, .neg 397, .neg 398, .neg 399, .neg 400, .neg 401, .neg 402, .neg 403, .neg 404, .neg 407, .neg 411, .neg 416, .neg 417, .neg 418, .neg 419, .neg 420, .neg 421, .neg 422, .neg 423, .neg 426, .neg 430, .neg 435, .neg 436, .neg 437, .neg 453, .neg 474]
private def clause575 : Sat.Clause := [.neg 287, .neg 288, .neg 290, .neg 291, .neg 292, .neg 297, .neg 299, .neg 300, .neg 301, .neg 303, .neg 304, .neg 305, .neg 307, .neg 308, .neg 309, .neg 314, .neg 316, .neg 317, .neg 318, .neg 320, .neg 321, .neg 322, .neg 324, .neg 325, .neg 326, .neg 349, .neg 350, .neg 351, .neg 353, .neg 354, .neg 355, .neg 367, .neg 368, .neg 369, .neg 379, .neg 384, .neg 386, .neg 387, .neg 388, .neg 390, .neg 391, .neg 392, .neg 394, .neg 395, .neg 396, .neg 404, .neg 405, .neg 406, .neg 408, .neg 409, .neg 410, .neg 412, .neg 413, .neg 414, .neg 415, .neg 423, .neg 424, .neg 425, .neg 427, .neg 428, .neg 429, .neg 431, .neg 432, .neg 433, .neg 434, .neg 475, .neg 476, .neg 477, .neg 478, .neg 499]
private def clause576 : Sat.Clause := [.neg 330, .neg 331, .neg 332, .neg 333, .neg 334, .neg 337, .neg 338, .neg 339, .neg 340, .neg 342, .neg 343, .neg 344, .neg 345, .neg 346, .neg 347, .neg 356, .neg 357, .neg 358, .neg 359, .neg 360, .neg 361, .neg 362, .neg 363, .neg 364, .neg 365, .neg 370, .neg 371, .neg 372, .neg 373, .neg 374, .neg 375, .neg 376, .neg 377, .neg 378, .neg 379, .neg 439, .neg 440, .neg 441, .neg 442, .neg 447, .neg 448, .neg 449, .neg 450, .neg 451, .neg 452, .neg 458, .neg 459, .neg 460, .neg 461, .neg 462, .neg 463, .neg 470, .neg 471, .neg 472, .neg 473, .neg 483, .neg 484, .neg 485, .neg 486, .neg 487, .neg 488, .neg 495, .neg 496, .neg 497, .neg 498, .neg 506, .neg 507, .neg 508, .neg 509, .neg 514]
private def clause577 : Sat.Clause := [.neg 438, .neg 439, .neg 440, .neg 441, .neg 442, .neg 443, .neg 444, .neg 445, .neg 446, .neg 447, .neg 448, .neg 449, .neg 450, .neg 451, .neg 452, .neg 454, .neg 455, .neg 456, .neg 457, .neg 458, .neg 459, .neg 460, .neg 461, .neg 462, .neg 463, .neg 464, .neg 465, .neg 466, .neg 467, .neg 468, .neg 469, .neg 470, .neg 471, .neg 472, .neg 473, .neg 479, .neg 480, .neg 481, .neg 482, .neg 483, .neg 484, .neg 485, .neg 486, .neg 487, .neg 488, .neg 489, .neg 490, .neg 491, .neg 492, .neg 493, .neg 494, .neg 495, .neg 496, .neg 497, .neg 498, .neg 500, .neg 501, .neg 502, .neg 503, .neg 504, .neg 505, .neg 506, .neg 507, .neg 508, .neg 509, .neg 510, .neg 511, .neg 512, .neg 513, .neg 514]

private def clauses : Sat.Fmla := [
  clause000, clause001, clause002, clause003, clause004, clause005, clause006, clause007, clause008, clause009, clause010, clause011, clause012, clause013, clause014, clause015, clause016, clause017, clause018, clause019, clause020, clause021, clause022, clause023, clause024, clause025, clause026, clause027, clause028, clause029, clause030, clause031, clause032, clause033, clause034, clause035, clause036, clause037, clause038, clause039, clause040, clause041, clause042, clause043, clause044, clause045, clause046, clause047, clause048, clause049, clause050, clause051, clause052, clause053, clause054, clause055, clause056, clause057, clause058, clause059, clause060, clause061, clause062, clause063, clause064, clause065, clause066, clause067, clause068, clause069, clause070, clause071, clause072, clause073, clause074, clause075, clause076, clause077, clause078, clause079, clause080, clause081, clause082, clause083, clause084, clause085, clause086, clause087, clause088, clause089, clause090, clause091, clause092, clause093, clause094, clause095, clause096, clause097, clause098, clause099, clause100, clause101, clause102, clause103, clause104, clause105, clause106, clause107, clause108, clause109, clause110, clause111, clause112, clause113, clause114, clause115, clause116, clause117, clause118, clause119, clause120, clause121, clause122, clause123, clause124, clause125, clause126, clause127, clause128, clause129, clause130, clause131, clause132, clause133, clause134, clause135, clause136, clause137, clause138, clause139, clause140, clause141, clause142, clause143, clause144, clause145, clause146, clause147, clause148, clause149, clause150, clause151, clause152, clause153, clause154, clause155, clause156, clause157, clause158, clause159, clause160, clause161, clause162, clause163, clause164, clause165, clause166, clause167, clause168, clause169, clause170, clause171, clause172, clause173, clause174, clause175, clause176, clause177, clause178, clause179, clause180, clause181, clause182, clause183, clause184, clause185, clause186, clause187, clause188, clause189, clause190, clause191, clause192, clause193, clause194, clause195, clause196, clause197, clause198, clause199, clause200, clause201, clause202, clause203, clause204, clause205, clause206, clause207, clause208, clause209, clause210, clause211, clause212, clause213, clause214, clause215, clause216, clause217, clause218, clause219, clause220, clause221, clause222, clause223, clause224, clause225, clause226, clause227, clause228, clause229, clause230, clause231, clause232, clause233, clause234, clause235, clause236, clause237, clause238, clause239, clause240, clause241, clause242, clause243, clause244, clause245, clause246, clause247, clause248, clause249, clause250, clause251, clause252, clause253, clause254, clause255, clause256, clause257, clause258, clause259, clause260, clause261, clause262, clause263, clause264, clause265, clause266, clause267, clause268, clause269, clause270, clause271, clause272, clause273, clause274, clause275, clause276, clause277, clause278, clause279, clause280, clause281, clause282, clause283, clause284, clause285, clause286, clause287, clause288, clause289, clause290, clause291, clause292, clause293, clause294, clause295, clause296, clause297, clause298, clause299, clause300, clause301, clause302, clause303, clause304, clause305, clause306, clause307, clause308, clause309, clause310, clause311, clause312, clause313, clause314, clause315, clause316, clause317, clause318, clause319, clause320, clause321, clause322, clause323, clause324, clause325, clause326, clause327, clause328, clause329, clause330, clause331, clause332, clause333, clause334, clause335, clause336, clause337, clause338, clause339, clause340, clause341, clause342, clause343, clause344, clause345, clause346, clause347, clause348, clause349, clause350, clause351, clause352, clause353, clause354, clause355, clause356, clause357, clause358, clause359, clause360, clause361, clause362, clause363, clause364, clause365, clause366, clause367, clause368, clause369, clause370, clause371, clause372, clause373, clause374, clause375, clause376, clause377, clause378, clause379, clause380, clause381, clause382, clause383, clause384, clause385, clause386, clause387, clause388, clause389, clause390, clause391, clause392, clause393, clause394, clause395, clause396, clause397, clause398, clause399, clause400, clause401, clause402, clause403, clause404, clause405, clause406, clause407, clause408, clause409, clause410, clause411, clause412, clause413, clause414, clause415, clause416, clause417, clause418, clause419, clause420, clause421, clause422, clause423, clause424, clause425, clause426, clause427, clause428, clause429, clause430, clause431, clause432, clause433, clause434, clause435, clause436, clause437, clause438, clause439, clause440, clause441, clause442, clause443, clause444, clause445, clause446, clause447, clause448, clause449, clause450, clause451, clause452, clause453, clause454, clause455, clause456, clause457, clause458, clause459, clause460, clause461, clause462, clause463, clause464, clause465, clause466, clause467, clause468, clause469, clause470, clause471, clause472, clause473, clause474, clause475, clause476, clause477, clause478, clause479, clause480, clause481, clause482, clause483, clause484, clause485, clause486, clause487, clause488, clause489, clause490, clause491, clause492, clause493, clause494, clause495, clause496, clause497, clause498, clause499, clause500, clause501, clause502, clause503, clause504, clause505, clause506, clause507, clause508, clause509, clause510, clause511, clause512, clause513, clause514, clause515, clause516, clause517, clause518, clause519, clause520, clause521, clause522, clause523, clause524, clause525, clause526, clause527, clause528, clause529, clause530, clause531, clause532, clause533, clause534, clause535, clause536, clause537, clause538, clause539, clause540, clause541, clause542, clause543, clause544, clause545, clause546, clause547, clause548, clause549, clause550, clause551, clause552, clause553, clause554, clause555, clause556, clause557, clause558, clause559, clause560, clause561, clause562, clause563, clause564, clause565, clause566, clause567, clause568, clause569, clause570, clause571, clause572, clause573, clause574, clause575, clause576, clause577]

private theorem formula_eq : cnf_refutation.formula = clauses := by rfl

variable {n : ℕ} (C : Context 13 n states)

-- Clause 1: empty_direction; source clause 29.
private theorem sound000 : C.clause (decodeClause atoms clause000) := by
  exact C.covered_clause _ _ (C.empty_clause 1 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 2: empty_direction; source clause 81.
private theorem sound001 : C.clause (decodeClause atoms clause001) := by
  exact C.covered_clause _ _ (C.empty_clause 2 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 3: domain; source clause 112.
private theorem sound002 : C.clause (decodeClause atoms clause002) := by
  exact C.covered_clause _ _ (C.domain_clause 0 3 (by decide) 1 1 (by decide +kernel)) (by decide +kernel)

-- Clause 4: domain; source clause 113.
private theorem sound003 : C.clause (decodeClause atoms clause003) := by
  exact C.covered_clause _ _ (C.domain_clause 0 3 (by decide) 1 2 (by decide +kernel)) (by decide +kernel)

-- Clause 5: domain; source clause 114.
private theorem sound004 : C.clause (decodeClause atoms clause004) := by
  exact C.covered_clause _ _ (C.domain_clause 0 3 (by decide) 1 3 (by decide +kernel)) (by decide +kernel)

-- Clause 6: domain; source clause 115.
private theorem sound005 : C.clause (decodeClause atoms clause005) := by
  exact C.covered_clause _ _ (C.domain_clause 0 3 (by decide) 1 4 (by decide +kernel)) (by decide +kernel)

-- Clause 7: domain; source clause 117.
private theorem sound006 : C.clause (decodeClause atoms clause006) := by
  exact C.covered_clause _ _ (C.domain_clause 0 3 (by decide) 2 1 (by decide +kernel)) (by decide +kernel)

-- Clause 8: domain; source clause 118.
private theorem sound007 : C.clause (decodeClause atoms clause007) := by
  exact C.covered_clause _ _ (C.domain_clause 0 3 (by decide) 2 2 (by decide +kernel)) (by decide +kernel)

-- Clause 9: domain; source clause 119.
private theorem sound008 : C.clause (decodeClause atoms clause008) := by
  exact C.covered_clause _ _ (C.domain_clause 0 3 (by decide) 2 3 (by decide +kernel)) (by decide +kernel)

-- Clause 10: domain; source clause 120.
private theorem sound009 : C.clause (decodeClause atoms clause009) := by
  exact C.covered_clause _ _ (C.domain_clause 0 3 (by decide) 2 4 (by decide +kernel)) (by decide +kernel)

-- Clause 11: domain; source clause 123.
private theorem sound010 : C.clause (decodeClause atoms clause010) := by
  exact C.covered_clause _ _ (C.domain_clause 0 3 (by decide) 3 2 (by decide +kernel)) (by decide +kernel)

-- Clause 12: empty_direction; source clause 133.
private theorem sound011 : C.clause (decodeClause atoms clause011) := by
  exact C.covered_clause _ _ (C.empty_clause 3 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 13: empty_direction; source clause 184.
private theorem sound012 : C.clause (decodeClause atoms clause012) := by
  exact C.covered_clause _ _ (C.empty_clause 4 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 14: empty_direction; source clause 235.
private theorem sound013 : C.clause (decodeClause atoms clause013) := by
  exact C.covered_clause _ _ (C.empty_clause 5 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 15: empty_direction; source clause 285.
private theorem sound014 : C.clause (decodeClause atoms clause014) := by
  exact C.covered_clause _ _ (C.empty_clause 6 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 16: empty_direction; source clause 335.
private theorem sound015 : C.clause (decodeClause atoms clause015) := by
  exact C.covered_clause _ _ (C.empty_clause 7 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 17: empty_direction; source clause 385.
private theorem sound016 : C.clause (decodeClause atoms clause016) := by
  exact C.covered_clause _ _ (C.empty_clause 8 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 18: empty_direction; source clause 434.
private theorem sound017 : C.clause (decodeClause atoms clause017) := by
  exact C.covered_clause _ _ (C.empty_clause 9 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 19: empty_direction; source clause 482.
private theorem sound018 : C.clause (decodeClause atoms clause018) := by
  exact C.covered_clause _ _ (C.empty_clause 10 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 20: empty_direction; source clause 531.
private theorem sound019 : C.clause (decodeClause atoms clause019) := by
  exact C.covered_clause _ _ (C.empty_clause 11 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 21: empty_direction; source clause 579.
private theorem sound020 : C.clause (decodeClause atoms clause020) := by
  exact C.covered_clause _ _ (C.empty_clause 12 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 22: empty_direction; source clause 633.
private theorem sound021 : C.clause (decodeClause atoms clause021) := by
  exact C.covered_clause _ _ (C.empty_clause 2 1 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 23: empty_direction; source clause 687.
private theorem sound022 : C.clause (decodeClause atoms clause022) := by
  exact C.covered_clause _ _ (C.empty_clause 3 1 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 24: empty_direction; source clause 740.
private theorem sound023 : C.clause (decodeClause atoms clause023) := by
  exact C.covered_clause _ _ (C.empty_clause 4 1 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 25: empty_direction; source clause 793.
private theorem sound024 : C.clause (decodeClause atoms clause024) := by
  exact C.covered_clause _ _ (C.empty_clause 5 1 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 26: empty_direction; source clause 845.
private theorem sound025 : C.clause (decodeClause atoms clause025) := by
  exact C.covered_clause _ _ (C.empty_clause 6 1 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 27: empty_direction; source clause 897.
private theorem sound026 : C.clause (decodeClause atoms clause026) := by
  exact C.covered_clause _ _ (C.empty_clause 7 1 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 28: empty_direction; source clause 995.
private theorem sound027 : C.clause (decodeClause atoms clause027) := by
  exact C.covered_clause _ _ (C.empty_clause 9 1 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 29: empty_direction; source clause 1244.
private theorem sound028 : C.clause (decodeClause atoms clause028) := by
  exact C.covered_clause _ _ (C.empty_clause 4 2 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 30: empty_direction; source clause 1555.
private theorem sound029 : C.clause (decodeClause atoms clause029) := by
  exact C.covered_clause _ _ (C.empty_clause 10 2 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 31: domain; source clause 1749.
private theorem sound030 : C.clause (decodeClause atoms clause030) := by
  exact C.covered_clause _ _ (C.domain_clause 3 5 (by decide) 4 1 (by decide +kernel)) (by decide +kernel)

-- Clause 32: domain; source clause 1750.
private theorem sound031 : C.clause (decodeClause atoms clause031) := by
  exact C.covered_clause _ _ (C.domain_clause 3 5 (by decide) 4 2 (by decide +kernel)) (by decide +kernel)

-- Clause 33: empty_direction; source clause 1755.
private theorem sound032 : C.clause (decodeClause atoms clause032) := by
  exact C.covered_clause _ _ (C.empty_clause 5 3 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 34: empty_direction; source clause 1858.
private theorem sound033 : C.clause (decodeClause atoms clause033) := by
  exact C.covered_clause _ _ (C.empty_clause 7 3 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 35: domain; source clause 1894.
private theorem sound034 : C.clause (decodeClause atoms clause034) := by
  exact C.covered_clause _ _ (C.domain_clause 3 8 (by decide) 1 6 (by decide +kernel)) (by decide +kernel)

-- Clause 36: domain; source clause 1896.
private theorem sound035 : C.clause (decodeClause atoms clause035) := by
  exact C.covered_clause _ _ (C.domain_clause 3 8 (by decide) 2 6 (by decide +kernel)) (by decide +kernel)

-- Clause 37: domain; source clause 1902.
private theorem sound036 : C.clause (decodeClause atoms clause036) := by
  exact C.covered_clause _ _ (C.domain_clause 3 8 (by decide) 3 6 (by decide +kernel)) (by decide +kernel)

-- Clause 38: empty_direction; source clause 1958.
private theorem sound037 : C.clause (decodeClause atoms clause037) := by
  exact C.covered_clause _ _ (C.empty_clause 9 3 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 39: empty_direction; source clause 2009.
private theorem sound038 : C.clause (decodeClause atoms clause038) := by
  exact C.covered_clause _ _ (C.empty_clause 10 3 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 40: empty_direction; source clause 2210.
private theorem sound039 : C.clause (decodeClause atoms clause039) := by
  exact C.covered_clause _ _ (C.empty_clause 6 4 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 41: empty_direction; source clause 2264.
private theorem sound040 : C.clause (decodeClause atoms clause040) := by
  exact C.covered_clause _ _ (C.empty_clause 7 4 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 42: empty_direction; source clause 2418.
private theorem sound041 : C.clause (decodeClause atoms clause041) := by
  exact C.covered_clause _ _ (C.empty_clause 10 4 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 43: empty_direction; source clause 2620.
private theorem sound042 : C.clause (decodeClause atoms clause042) := by
  exact C.covered_clause _ _ (C.empty_clause 7 5 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 44: empty_direction; source clause 2722.
private theorem sound043 : C.clause (decodeClause atoms clause043) := by
  exact C.covered_clause _ _ (C.empty_clause 9 5 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 45: empty_direction; source clause 2774.
private theorem sound044 : C.clause (decodeClause atoms clause044) := by
  exact C.covered_clause _ _ (C.empty_clause 10 5 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 46: empty_direction; source clause 3027.
private theorem sound045 : C.clause (decodeClause atoms clause045) := by
  exact C.covered_clause _ _ (C.empty_clause 9 6 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 47: empty_direction; source clause 3080.
private theorem sound046 : C.clause (decodeClause atoms clause046) := by
  exact C.covered_clause _ _ (C.empty_clause 10 6 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 48: domain; source clause 3269.
private theorem sound047 : C.clause (decodeClause atoms clause047) := by
  exact C.covered_clause _ _ (C.domain_clause 7 9 (by decide) 2 5 (by decide +kernel)) (by decide +kernel)

-- Clause 49: domain; source clause 3275.
private theorem sound048 : C.clause (decodeClause atoms clause048) := by
  exact C.covered_clause _ _ (C.domain_clause 7 9 (by decide) 3 5 (by decide +kernel)) (by decide +kernel)

-- Clause 50: domain; source clause 3281.
private theorem sound049 : C.clause (decodeClause atoms clause049) := by
  exact C.covered_clause _ _ (C.domain_clause 7 9 (by decide) 4 5 (by decide +kernel)) (by decide +kernel)

-- Clause 51: empty_direction; source clause 3283.
private theorem sound050 : C.clause (decodeClause atoms clause050) := by
  exact C.covered_clause _ _ (C.empty_clause 9 7 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 52: empty_direction; source clause 3336.
private theorem sound051 : C.clause (decodeClause atoms clause051) := by
  exact C.covered_clause _ _ (C.empty_clause 10 7 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 53: empty_direction; source clause 3539.
private theorem sound052 : C.clause (decodeClause atoms clause052) := by
  exact C.covered_clause _ _ (C.empty_clause 10 8 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 54: domain; source clause 3581.
private theorem sound053 : C.clause (decodeClause atoms clause053) := by
  exact C.covered_clause _ _ (C.domain_clause 8 11 (by decide) 3 1 (by decide +kernel)) (by decide +kernel)

-- Clause 55: domain; source clause 3582.
private theorem sound054 : C.clause (decodeClause atoms clause054) := by
  exact C.covered_clause _ _ (C.domain_clause 8 11 (by decide) 3 2 (by decide +kernel)) (by decide +kernel)

-- Clause 56: domain; source clause 3583.
private theorem sound055 : C.clause (decodeClause atoms clause055) := by
  exact C.covered_clause _ _ (C.domain_clause 8 11 (by decide) 3 3 (by decide +kernel)) (by decide +kernel)

-- Clause 57: domain; source clause 3584.
private theorem sound056 : C.clause (decodeClause atoms clause056) := by
  exact C.covered_clause _ _ (C.domain_clause 8 11 (by decide) 3 4 (by decide +kernel)) (by decide +kernel)

-- Clause 58: domain; source clause 3585.
private theorem sound057 : C.clause (decodeClause atoms clause057) := by
  exact C.covered_clause _ _ (C.domain_clause 8 11 (by decide) 3 5 (by decide +kernel)) (by decide +kernel)

-- Clause 59: domain; source clause 3586.
private theorem sound058 : C.clause (decodeClause atoms clause058) := by
  exact C.covered_clause _ _ (C.domain_clause 8 11 (by decide) 3 6 (by decide +kernel)) (by decide +kernel)

-- Clause 60: empty_direction; source clause 3593.
private theorem sound059 : C.clause (decodeClause atoms clause059) := by
  exact C.covered_clause _ _ (C.empty_clause 11 8 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 61: empty_direction; source clause 3646.
private theorem sound060 : C.clause (decodeClause atoms clause060) := by
  exact C.covered_clause _ _ (C.empty_clause 12 8 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 62: empty_direction; source clause 3700.
private theorem sound061 : C.clause (decodeClause atoms clause061) := by
  exact C.covered_clause _ _ (C.empty_clause 10 9 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 63: domain; source clause 3924.
private theorem sound062 : C.clause (decodeClause atoms clause062) := by
  exact C.covered_clause _ _ (C.domain_clause 12 10 (by decide) 4 2 (by decide +kernel)) (by decide +kernel)

-- Clause 64: domain; source clause 3925.
private theorem sound063 : C.clause (decodeClause atoms clause063) := by
  exact C.covered_clause _ _ (C.domain_clause 12 10 (by decide) 4 3 (by decide +kernel)) (by decide +kernel)

-- Clause 65: domain; source clause 3926.
private theorem sound064 : C.clause (decodeClause atoms clause064) := by
  exact C.covered_clause _ _ (C.domain_clause 12 10 (by decide) 4 4 (by decide +kernel)) (by decide +kernel)

-- Clause 66: domain; source clause 3927.
private theorem sound065 : C.clause (decodeClause atoms clause065) := by
  exact C.covered_clause _ _ (C.domain_clause 12 10 (by decide) 4 5 (by decide +kernel)) (by decide +kernel)

-- Clause 67: domain; source clause 3928.
private theorem sound066 : C.clause (decodeClause atoms clause066) := by
  exact C.covered_clause _ _ (C.domain_clause 12 10 (by decide) 4 6 (by decide +kernel)) (by decide +kernel)

-- Clause 68: domain; source clause 3941.
private theorem sound067 : C.clause (decodeClause atoms clause067) := by
  exact C.covered_clause _ _ (C.domain_clause 11 12 (by decide) 2 1 (by decide +kernel)) (by decide +kernel)

-- Clause 69: domain; source clause 3942.
private theorem sound068 : C.clause (decodeClause atoms clause068) := by
  exact C.covered_clause _ _ (C.domain_clause 11 12 (by decide) 2 2 (by decide +kernel)) (by decide +kernel)

-- Clause 70: domain; source clause 3943.
private theorem sound069 : C.clause (decodeClause atoms clause069) := by
  exact C.covered_clause _ _ (C.domain_clause 11 12 (by decide) 2 3 (by decide +kernel)) (by decide +kernel)

-- Clause 71: domain; source clause 3944.
private theorem sound070 : C.clause (decodeClause atoms clause070) := by
  exact C.covered_clause _ _ (C.domain_clause 11 12 (by decide) 2 4 (by decide +kernel)) (by decide +kernel)

-- Clause 72: domain; source clause 3945.
private theorem sound071 : C.clause (decodeClause atoms clause071) := by
  exact C.covered_clause _ _ (C.domain_clause 11 12 (by decide) 2 5 (by decide +kernel)) (by decide +kernel)

-- Clause 73: domain; source clause 3946.
private theorem sound072 : C.clause (decodeClause atoms clause072) := by
  exact C.covered_clause _ _ (C.domain_clause 11 12 (by decide) 2 6 (by decide +kernel)) (by decide +kernel)

-- Clause 74: empty_direction; source clause 3958.
private theorem sound073 : C.clause (decodeClause atoms clause073) := by
  exact C.covered_clause _ _ (C.empty_clause 12 11 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 75: growth; source clause 3988.
private theorem sound074 : C.clause (decodeClause atoms clause074) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 1 2 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 76: growth; source clause 4098.
private theorem sound075 : C.clause (decodeClause atoms clause075) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 1 12 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 77: growth; source clause 4261.
private theorem sound076 : C.clause (decodeClause atoms clause076) := by
  exact C.covered_clause _ _ (C.growth_clause false 0 3 5 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 78: growth; source clause 4262.
private theorem sound077 : C.clause (decodeClause atoms clause077) := by
  exact C.covered_clause _ _ (C.growth_clause false 0 3 5 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 79: growth; source clause 4264.
private theorem sound078 : C.clause (decodeClause atoms clause078) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 3 5 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 80: growth; source clause 4265.
private theorem sound079 : C.clause (decodeClause atoms clause079) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 3 5 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 81: growth; source clause 4292.
private theorem sound080 : C.clause (decodeClause atoms clause080) := by
  exact C.covered_clause _ _ (C.growth_clause false 0 3 8 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 82: growth; source clause 4300.
private theorem sound081 : C.clause (decodeClause atoms clause081) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 3 8 (by decide) (by decide) (by decide) 5) (by decide +kernel)

-- Clause 83: growth; source clause 4311.
private theorem sound082 : C.clause (decodeClause atoms clause082) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 3 9 (by decide) (by decide) (by decide) 5) (by decide +kernel)

-- Clause 84: growth; source clause 4322.
private theorem sound083 : C.clause (decodeClause atoms clause083) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 3 10 (by decide) (by decide) (by decide) 5) (by decide +kernel)

-- Clause 85: growth; source clause 4327.
private theorem sound084 : C.clause (decodeClause atoms clause084) := by
  exact C.covered_clause _ _ (C.growth_clause false 0 3 11 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 86: growth; source clause 5304.
private theorem sound085 : C.clause (decodeClause atoms clause085) := by
  exact C.covered_clause _ _ (C.growth_clause false 0 11 12 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 87: growth; source clause 5418.
private theorem sound086 : C.clause (decodeClause atoms clause086) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 12 10 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 88: growth; source clause 5584.
private theorem sound087 : C.clause (decodeClause atoms clause087) := by
  exact C.covered_clause _ _ (C.growth_clause true 1 2 4 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 89: order_transitive; source clause 5743.
private theorem sound088 : C.clause (decodeClause atoms clause088) := by
  exact C.covered_clause _ _ (C.transitive_clause 1 3 8 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 90: order_transitive; source clause 6029.
private theorem sound089 : C.clause (decodeClause atoms clause089) := by
  exact C.covered_clause _ _ (C.transitive_clause 1 5 12 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 91: order_transitive; source clause 6271.
private theorem sound090 : C.clause (decodeClause atoms clause090) := by
  exact C.covered_clause _ _ (C.transitive_clause 1 7 12 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 92: order_transitive; source clause 6381.
private theorem sound091 : C.clause (decodeClause atoms clause091) := by
  exact C.covered_clause _ _ (C.transitive_clause 1 8 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 93: order_transitive; source clause 6392.
private theorem sound092 : C.clause (decodeClause atoms clause092) := by
  exact C.covered_clause _ _ (C.transitive_clause 1 8 12 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 94: order_transitive; source clause 6513.
private theorem sound093 : C.clause (decodeClause atoms clause093) := by
  exact C.covered_clause _ _ (C.transitive_clause 1 9 12 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 95: growth; source clause 6871.
private theorem sound094 : C.clause (decodeClause atoms clause094) := by
  exact C.covered_clause _ _ (C.growth_clause true 1 12 10 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 96: growth; source clause 7301.
private theorem sound095 : C.clause (decodeClause atoms clause095) := by
  exact C.covered_clause _ _ (C.growth_clause true 2 4 6 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 97: growth; source clause 8885.
private theorem sound096 : C.clause (decodeClause atoms clause096) := by
  exact C.covered_clause _ _ (C.growth_clause true 3 5 7 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 98: growth; source clause 8886.
private theorem sound097 : C.clause (decodeClause atoms clause097) := by
  exact C.covered_clause _ _ (C.growth_clause true 3 5 7 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 99: order_transitive; source clause 8889.
private theorem sound098 : C.clause (decodeClause atoms clause098) := by
  exact C.covered_clause _ _ (C.transitive_clause 3 5 8 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 100: order_transitive; source clause 9131.
private theorem sound099 : C.clause (decodeClause atoms clause099) := by
  exact C.covered_clause _ _ (C.transitive_clause 3 7 8 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 101: growth; source clause 9278.
private theorem sound100 : C.clause (decodeClause atoms clause100) := by
  exact C.covered_clause _ _ (C.growth_clause false 3 8 10 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 102: order_transitive; source clause 9285.
private theorem sound101 : C.clause (decodeClause atoms clause101) := by
  exact C.covered_clause _ _ (C.transitive_clause 3 8 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 103: growth; source clause 9287.
private theorem sound102 : C.clause (decodeClause atoms clause102) := by
  exact C.covered_clause _ _ (C.growth_clause false 3 8 11 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 104: growth; source clause 9295.
private theorem sound103 : C.clause (decodeClause atoms clause103) := by
  exact C.covered_clause _ _ (C.growth_clause true 3 8 11 (by decide) (by decide) (by decide) 6) (by decide +kernel)

-- Clause 105: order_transitive; source clause 9384.
private theorem sound104 : C.clause (decodeClause atoms clause104) := by
  exact C.covered_clause _ _ (C.transitive_clause 3 9 8 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 106: growth; source clause 9405.
private theorem sound105 : C.clause (decodeClause atoms clause105) := by
  exact C.covered_clause _ _ (C.growth_clause true 3 9 10 (by decide) (by decide) (by decide) 6) (by decide +kernel)

-- Clause 107: growth; source clause 9548.
private theorem sound106 : C.clause (decodeClause atoms clause106) := by
  exact C.covered_clause _ _ (C.growth_clause true 3 10 12 (by decide) (by decide) (by decide) 6) (by decide +kernel)

-- Clause 108: growth; source clause 9663.
private theorem sound107 : C.clause (decodeClause atoms clause107) := by
  exact C.covered_clause _ _ (C.growth_clause false 3 11 12 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 109: growth; source clause 10437.
private theorem sound108 : C.clause (decodeClause atoms clause108) := by
  exact C.covered_clause _ _ (C.growth_clause true 4 6 3 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 110: growth; source clause 10595.
private theorem sound109 : C.clause (decodeClause atoms clause109) := by
  exact C.covered_clause _ _ (C.growth_clause false 4 7 9 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 111: growth; source clause 12054.
private theorem sound110 : C.clause (decodeClause atoms clause110) := by
  exact C.covered_clause _ _ (C.growth_clause true 5 7 9 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 112: growth; source clause 12055.
private theorem sound111 : C.clause (decodeClause atoms clause111) := by
  exact C.covered_clause _ _ (C.growth_clause true 5 7 9 (by decide) (by decide) (by decide) 5) (by decide +kernel)

-- Clause 113: growth; source clause 13133.
private theorem sound112 : C.clause (decodeClause atoms clause112) := by
  exact C.covered_clause _ _ (C.growth_clause true 6 3 8 (by decide) (by decide) (by decide) 5) (by decide +kernel)

-- Clause 114: growth; source clause 15213.
private theorem sound113 : C.clause (decodeClause atoms clause113) := by
  exact C.covered_clause _ _ (C.growth_clause true 7 9 10 (by decide) (by decide) (by decide) 6) (by decide +kernel)

-- Clause 115: growth; source clause 16923.
private theorem sound114 : C.clause (decodeClause atoms clause114) := by
  exact C.covered_clause _ _ (C.growth_clause false 8 11 12 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 116: order_transitive; source clause 18250.
private theorem sound115 : C.clause (decodeClause atoms clause115) := by
  exact C.covered_clause _ _ (C.transitive_clause 9 10 12 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 117: order_transitive; source clause 19823.
private theorem sound116 : C.clause (decodeClause atoms clause116) := by
  exact C.covered_clause _ _ (C.transitive_clause 10 11 12 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 118: growth; source clause 21399.
private theorem sound117 : C.clause (decodeClause atoms clause117) := by
  exact C.covered_clause _ _ (C.growth_clause false 11 12 10 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 119: fixed_sign; source clause 22859.
private theorem sound118 : C.clause (decodeClause atoms clause118) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 2 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 120: fixed_sign; source clause 22860.
private theorem sound119 : C.clause (decodeClause atoms clause119) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 3 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 121: fixed_sign; source clause 22861.
private theorem sound120 : C.clause (decodeClause atoms clause120) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 4 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 122: fixed_sign; source clause 22863.
private theorem sound121 : C.clause (decodeClause atoms clause121) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 123: fixed_sign; source clause 22865.
private theorem sound122 : C.clause (decodeClause atoms clause122) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 124: fixed_sign; source clause 22867.
private theorem sound123 : C.clause (decodeClause atoms clause123) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 125: fixed_sign; source clause 22868.
private theorem sound124 : C.clause (decodeClause atoms clause124) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 126: fixed_sign; source clause 22869.
private theorem sound125 : C.clause (decodeClause atoms clause125) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 127: fixed_sign; source clause 22870.
private theorem sound126 : C.clause (decodeClause atoms clause126) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 4 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 128: fixed_sign; source clause 22872.
private theorem sound127 : C.clause (decodeClause atoms clause127) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 129: fixed_sign; source clause 22874.
private theorem sound128 : C.clause (decodeClause atoms clause128) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 130: fixed_sign; source clause 22876.
private theorem sound129 : C.clause (decodeClause atoms clause129) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 131: fixed_sign; source clause 22877.
private theorem sound130 : C.clause (decodeClause atoms clause130) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 132: fixed_sign; source clause 22878.
private theorem sound131 : C.clause (decodeClause atoms clause131) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 133: fixed_sign; source clause 22879.
private theorem sound132 : C.clause (decodeClause atoms clause132) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 4 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 134: fixed_sign; source clause 22881.
private theorem sound133 : C.clause (decodeClause atoms clause133) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 4 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 135: fixed_sign; source clause 22883.
private theorem sound134 : C.clause (decodeClause atoms clause134) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 4 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 136: fixed_sign; source clause 22884.
private theorem sound135 : C.clause (decodeClause atoms clause135) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 4 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 137: fixed_sign; source clause 22885.
private theorem sound136 : C.clause (decodeClause atoms clause136) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 4 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 138: fixed_sign; source clause 22886.
private theorem sound137 : C.clause (decodeClause atoms clause137) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 6 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 139: fixed_sign; source clause 22888.
private theorem sound138 : C.clause (decodeClause atoms clause138) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 6 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 140: fixed_sign; source clause 22889.
private theorem sound139 : C.clause (decodeClause atoms clause139) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 6 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 141: fixed_sign; source clause 22890.
private theorem sound140 : C.clause (decodeClause atoms clause140) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 6 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 142: fixed_sign; source clause 22891.
private theorem sound141 : C.clause (decodeClause atoms clause141) := by
  exact C.covered_clause _ _ (C.fixed_negative 0 8 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 143: fixed_sign; source clause 22892.
private theorem sound142 : C.clause (decodeClause atoms clause142) := by
  exact C.covered_clause _ _ (C.fixed_negative 0 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 144: fixed_sign; source clause 22893.
private theorem sound143 : C.clause (decodeClause atoms clause143) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 3 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 145: fixed_sign; source clause 22894.
private theorem sound144 : C.clause (decodeClause atoms clause144) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 4 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 146: fixed_sign; source clause 22896.
private theorem sound145 : C.clause (decodeClause atoms clause145) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 147: fixed_sign; source clause 22898.
private theorem sound146 : C.clause (decodeClause atoms clause146) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 148: fixed_sign; source clause 22900.
private theorem sound147 : C.clause (decodeClause atoms clause147) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 149: fixed_sign; source clause 22901.
private theorem sound148 : C.clause (decodeClause atoms clause148) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 150: fixed_sign; source clause 22902.
private theorem sound149 : C.clause (decodeClause atoms clause149) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 151: fixed_sign; source clause 22903.
private theorem sound150 : C.clause (decodeClause atoms clause150) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 3 4 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 152: fixed_sign; source clause 22905.
private theorem sound151 : C.clause (decodeClause atoms clause151) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 3 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 153: fixed_sign; source clause 22908.
private theorem sound152 : C.clause (decodeClause atoms clause152) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 3 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 154: fixed_sign; source clause 22909.
private theorem sound153 : C.clause (decodeClause atoms clause153) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 155: fixed_sign; source clause 22911.
private theorem sound154 : C.clause (decodeClause atoms clause154) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 156: fixed_sign; source clause 22913.
private theorem sound155 : C.clause (decodeClause atoms clause155) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 157: fixed_sign; source clause 22914.
private theorem sound156 : C.clause (decodeClause atoms clause156) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 158: fixed_sign; source clause 22915.
private theorem sound157 : C.clause (decodeClause atoms clause157) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 159: fixed_sign; source clause 22916.
private theorem sound158 : C.clause (decodeClause atoms clause158) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 6 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 160: fixed_sign; source clause 22918.
private theorem sound159 : C.clause (decodeClause atoms clause159) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 6 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 161: fixed_sign; source clause 22919.
private theorem sound160 : C.clause (decodeClause atoms clause160) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 6 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 162: fixed_sign; source clause 22920.
private theorem sound161 : C.clause (decodeClause atoms clause161) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 6 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 163: fixed_sign; source clause 22921.
private theorem sound162 : C.clause (decodeClause atoms clause162) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 8 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 164: fixed_sign; source clause 22922.
private theorem sound163 : C.clause (decodeClause atoms clause163) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 165: fixed_sign; source clause 22923.
private theorem sound164 : C.clause (decodeClause atoms clause164) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 3 4 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 166: fixed_sign; source clause 22925.
private theorem sound165 : C.clause (decodeClause atoms clause165) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 3 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 167: fixed_sign; source clause 22928.
private theorem sound166 : C.clause (decodeClause atoms clause166) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 3 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 168: fixed_sign; source clause 22930.
private theorem sound167 : C.clause (decodeClause atoms clause167) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 4 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 169: fixed_sign; source clause 22932.
private theorem sound168 : C.clause (decodeClause atoms clause168) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 4 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 170: fixed_sign; source clause 22934.
private theorem sound169 : C.clause (decodeClause atoms clause169) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 4 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 171: fixed_sign; source clause 22935.
private theorem sound170 : C.clause (decodeClause atoms clause170) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 4 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 172: fixed_sign; source clause 22936.
private theorem sound171 : C.clause (decodeClause atoms clause171) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 4 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 173: fixed_sign; source clause 22941.
private theorem sound172 : C.clause (decodeClause atoms clause172) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 6 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 174: fixed_sign; source clause 22943.
private theorem sound173 : C.clause (decodeClause atoms clause173) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 6 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 175: fixed_sign; source clause 22944.
private theorem sound174 : C.clause (decodeClause atoms clause174) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 6 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 176: fixed_sign; source clause 22945.
private theorem sound175 : C.clause (decodeClause atoms clause175) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 6 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 177: fixed_sign; source clause 22946.
private theorem sound176 : C.clause (decodeClause atoms clause176) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 8 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 178: fixed_sign; source clause 22947.
private theorem sound177 : C.clause (decodeClause atoms clause177) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 179: fixed_sign; source clause 22948.
private theorem sound178 : C.clause (decodeClause atoms clause178) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 4 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 180: fixed_sign; source clause 22951.
private theorem sound179 : C.clause (decodeClause atoms clause179) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 4 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 181: fixed_sign; source clause 22952.
private theorem sound180 : C.clause (decodeClause atoms clause180) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 5 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 182: fixed_sign; source clause 22953.
private theorem sound181 : C.clause (decodeClause atoms clause181) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 5 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 183: fixed_sign; source clause 22954.
private theorem sound182 : C.clause (decodeClause atoms clause182) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 5 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 184: fixed_sign; source clause 22955.
private theorem sound183 : C.clause (decodeClause atoms clause183) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 5 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 185: fixed_sign; source clause 22956.
private theorem sound184 : C.clause (decodeClause atoms clause184) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 5 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 186: fixed_sign; source clause 22957.
private theorem sound185 : C.clause (decodeClause atoms clause185) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 5 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 187: fixed_sign; source clause 22958.
private theorem sound186 : C.clause (decodeClause atoms clause186) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 6 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 188: fixed_sign; source clause 22959.
private theorem sound187 : C.clause (decodeClause atoms clause187) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 6 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 189: fixed_sign; source clause 22960.
private theorem sound188 : C.clause (decodeClause atoms clause188) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 7 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 190: fixed_sign; source clause 22961.
private theorem sound189 : C.clause (decodeClause atoms clause189) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 7 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 191: fixed_sign; source clause 22962.
private theorem sound190 : C.clause (decodeClause atoms clause190) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 7 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 192: fixed_sign; source clause 22963.
private theorem sound191 : C.clause (decodeClause atoms clause191) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 7 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 193: fixed_sign; source clause 22964.
private theorem sound192 : C.clause (decodeClause atoms clause192) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 7 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 194: fixed_sign; source clause 22965.
private theorem sound193 : C.clause (decodeClause atoms clause193) := by
  exact C.covered_clause _ _ (C.fixed_negative 3 8 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 195: fixed_sign; source clause 22966.
private theorem sound194 : C.clause (decodeClause atoms clause194) := by
  exact C.covered_clause _ _ (C.fixed_negative 3 8 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 196: fixed_sign; source clause 22967.
private theorem sound195 : C.clause (decodeClause atoms clause195) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 9 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 197: fixed_sign; source clause 22968.
private theorem sound196 : C.clause (decodeClause atoms clause196) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 9 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 198: fixed_sign; source clause 22969.
private theorem sound197 : C.clause (decodeClause atoms clause197) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 9 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 199: fixed_sign; source clause 22970.
private theorem sound198 : C.clause (decodeClause atoms clause198) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 10 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 200: fixed_sign; source clause 22971.
private theorem sound199 : C.clause (decodeClause atoms clause199) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 10 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 201: fixed_sign; source clause 22972.
private theorem sound200 : C.clause (decodeClause atoms clause200) := by
  exact C.covered_clause _ _ (C.fixed_negative 3 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 202: fixed_sign; source clause 22978.
private theorem sound201 : C.clause (decodeClause atoms clause201) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 6 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 203: fixed_sign; source clause 22980.
private theorem sound202 : C.clause (decodeClause atoms clause202) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 6 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 204: fixed_sign; source clause 22981.
private theorem sound203 : C.clause (decodeClause atoms clause203) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 6 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 205: fixed_sign; source clause 22982.
private theorem sound204 : C.clause (decodeClause atoms clause204) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 6 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 206: fixed_sign; source clause 22983.
private theorem sound205 : C.clause (decodeClause atoms clause205) := by
  exact C.covered_clause _ _ (C.fixed_negative 4 7 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 207: fixed_sign; source clause 22985.
private theorem sound206 : C.clause (decodeClause atoms clause206) := by
  exact C.covered_clause _ _ (C.fixed_negative 4 8 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 208: fixed_sign; source clause 22986.
private theorem sound207 : C.clause (decodeClause atoms clause207) := by
  exact C.covered_clause _ _ (C.fixed_negative 4 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 209: fixed_sign; source clause 22989.
private theorem sound208 : C.clause (decodeClause atoms clause208) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 7 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 210: fixed_sign; source clause 22990.
private theorem sound209 : C.clause (decodeClause atoms clause209) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 7 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 211: fixed_sign; source clause 22991.
private theorem sound210 : C.clause (decodeClause atoms clause210) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 7 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 212: fixed_sign; source clause 22992.
private theorem sound211 : C.clause (decodeClause atoms clause211) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 7 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 213: fixed_sign; source clause 22993.
private theorem sound212 : C.clause (decodeClause atoms clause212) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 7 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 214: fixed_sign; source clause 22994.
private theorem sound213 : C.clause (decodeClause atoms clause213) := by
  exact C.covered_clause _ _ (C.fixed_negative 5 8 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 215: fixed_sign; source clause 22995.
private theorem sound214 : C.clause (decodeClause atoms clause214) := by
  exact C.covered_clause _ _ (C.fixed_negative 5 8 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 216: fixed_sign; source clause 22996.
private theorem sound215 : C.clause (decodeClause atoms clause215) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 9 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 217: fixed_sign; source clause 22997.
private theorem sound216 : C.clause (decodeClause atoms clause216) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 9 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 218: fixed_sign; source clause 22998.
private theorem sound217 : C.clause (decodeClause atoms clause217) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 9 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 219: fixed_sign; source clause 22999.
private theorem sound218 : C.clause (decodeClause atoms clause218) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 10 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 220: fixed_sign; source clause 23000.
private theorem sound219 : C.clause (decodeClause atoms clause219) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 10 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 221: fixed_sign; source clause 23001.
private theorem sound220 : C.clause (decodeClause atoms clause220) := by
  exact C.covered_clause _ _ (C.fixed_negative 5 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 222: fixed_sign; source clause 23004.
private theorem sound221 : C.clause (decodeClause atoms clause221) := by
  exact C.covered_clause _ _ (C.fixed_negative 6 8 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 223: fixed_sign; source clause 23006.
private theorem sound222 : C.clause (decodeClause atoms clause222) := by
  exact C.covered_clause _ _ (C.fixed_negative 6 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 224: fixed_sign; source clause 23007.
private theorem sound223 : C.clause (decodeClause atoms clause223) := by
  exact C.covered_clause _ _ (C.fixed_negative 7 8 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 225: fixed_sign; source clause 23008.
private theorem sound224 : C.clause (decodeClause atoms clause224) := by
  exact C.covered_clause _ _ (C.fixed_negative 7 8 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 226: fixed_sign; source clause 23009.
private theorem sound225 : C.clause (decodeClause atoms clause225) := by
  exact C.covered_clause _ _ (C.fixed_positive 7 9 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 227: fixed_sign; source clause 23010.
private theorem sound226 : C.clause (decodeClause atoms clause226) := by
  exact C.covered_clause _ _ (C.fixed_positive 7 9 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 228: fixed_sign; source clause 23011.
private theorem sound227 : C.clause (decodeClause atoms clause227) := by
  exact C.covered_clause _ _ (C.fixed_positive 7 9 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 229: fixed_sign; source clause 23012.
private theorem sound228 : C.clause (decodeClause atoms clause228) := by
  exact C.covered_clause _ _ (C.fixed_positive 7 10 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 230: fixed_sign; source clause 23013.
private theorem sound229 : C.clause (decodeClause atoms clause229) := by
  exact C.covered_clause _ _ (C.fixed_positive 7 10 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 231: fixed_sign; source clause 23014.
private theorem sound230 : C.clause (decodeClause atoms clause230) := by
  exact C.covered_clause _ _ (C.fixed_negative 7 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 232: fixed_sign; source clause 23015.
private theorem sound231 : C.clause (decodeClause atoms clause231) := by
  exact C.covered_clause _ _ (C.fixed_positive 8 9 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 233: fixed_sign; source clause 23016.
private theorem sound232 : C.clause (decodeClause atoms clause232) := by
  exact C.covered_clause _ _ (C.fixed_positive 8 10 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 234: fixed_sign; source clause 23017.
private theorem sound233 : C.clause (decodeClause atoms clause233) := by
  exact C.covered_clause _ _ (C.fixed_positive 8 10 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 235: fixed_sign; source clause 23018.
private theorem sound234 : C.clause (decodeClause atoms clause234) := by
  exact C.covered_clause _ _ (C.fixed_negative 8 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 236: fixed_sign; source clause 23019.
private theorem sound235 : C.clause (decodeClause atoms clause235) := by
  exact C.covered_clause _ _ (C.fixed_positive 9 10 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 237: fixed_sign; source clause 23020.
private theorem sound236 : C.clause (decodeClause atoms clause236) := by
  exact C.covered_clause _ _ (C.fixed_positive 9 10 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 238: fixed_sign; source clause 23021.
private theorem sound237 : C.clause (decodeClause atoms clause237) := by
  exact C.covered_clause _ _ (C.fixed_negative 9 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 239: fixed_sign; source clause 23022.
private theorem sound238 : C.clause (decodeClause atoms clause238) := by
  exact C.covered_clause _ _ (C.fixed_negative 10 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 240: packet; source clause 23030.
private theorem sound239 : C.clause (decodeClause atoms clause239) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 2 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 241: convex_four; source clause 23230.
private theorem sound240 : C.clause (decodeClause atoms clause240) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 242: convex_four; source clause 23438.
private theorem sound241 : C.clause (decodeClause atoms clause241) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 243: convex_four; source clause 23854.
private theorem sound242 : C.clause (decodeClause atoms clause242) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 244: convex_four; source clause 24270.
private theorem sound243 : C.clause (decodeClause atoms clause243) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 245: convex_four; source clause 24686.
private theorem sound244 : C.clause (decodeClause atoms clause244) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 246: convex_four; source clause 24894.
private theorem sound245 : C.clause (decodeClause atoms clause245) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 247: convex_four; source clause 25102.
private theorem sound246 : C.clause (decodeClause atoms clause246) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 248: packet; source clause 25118.
private theorem sound247 : C.clause (decodeClause atoms clause247) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 4 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 249: convex_four; source clause 25307.
private theorem sound248 : C.clause (decodeClause atoms clause248) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 3 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 250: packet; source clause 25534.
private theorem sound249 : C.clause (decodeClause atoms clause249) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 6 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 251: convex_four; source clause 25723.
private theorem sound250 : C.clause (decodeClause atoms clause250) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 252: packet; source clause 25942.
private theorem sound251 : C.clause (decodeClause atoms clause251) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 3 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 253: convex_four; source clause 26139.
private theorem sound252 : C.clause (decodeClause atoms clause252) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 3 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 254: convex_four; source clause 26555.
private theorem sound253 : C.clause (decodeClause atoms clause253) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 255: convex_four; source clause 27390.
private theorem sound254 : C.clause (decodeClause atoms clause254) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 4 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 256: convex_four; source clause 27806.
private theorem sound255 : C.clause (decodeClause atoms clause255) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 257: convex_four; source clause 28222.
private theorem sound256 : C.clause (decodeClause atoms clause256) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 4 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 258: convex_four; source clause 28430.
private theorem sound257 : C.clause (decodeClause atoms clause257) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 4 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 259: convex_four; source clause 28638.
private theorem sound258 : C.clause (decodeClause atoms clause258) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 260: convex_four; source clause 30510.
private theorem sound259 : C.clause (decodeClause atoms clause259) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 261: convex_four; source clause 30926.
private theorem sound260 : C.clause (decodeClause atoms clause260) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 262: convex_four; source clause 31134.
private theorem sound261 : C.clause (decodeClause atoms clause261) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 263: convex_four; source clause 31342.
private theorem sound262 : C.clause (decodeClause atoms clause262) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 6 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 264: convex_four; source clause 32795.
private theorem sound263 : C.clause (decodeClause atoms clause263) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 265: convex_four; source clause 34046.
private theorem sound264 : C.clause (decodeClause atoms clause264) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 266: packet; source clause 34062.
private theorem sound265 : C.clause (decodeClause atoms clause265) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 12 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 267: convex_four; source clause 34254.
private theorem sound266 : C.clause (decodeClause atoms clause266) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 268: convex_four; source clause 34459.
private theorem sound267 : C.clause (decodeClause atoms clause267) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 269: packet; source clause 34485.
private theorem sound268 : C.clause (decodeClause atoms clause268) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 2 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 270: convex_four; source clause 34667.
private theorem sound269 : C.clause (decodeClause atoms clause269) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 3 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 271: convex_four; source clause 35083.
private theorem sound270 : C.clause (decodeClause atoms clause270) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 272: packet; source clause 35302.
private theorem sound271 : C.clause (decodeClause atoms clause271) := by
  exact C.covered_clause _ _ (C.packet_clause 0 2 3 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 273: convex_four; source clause 35499.
private theorem sound272 : C.clause (decodeClause atoms clause272) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 3 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 274: convex_four; source clause 35915.
private theorem sound273 : C.clause (decodeClause atoms clause273) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 275: convex_four; source clause 36750.
private theorem sound274 : C.clause (decodeClause atoms clause274) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 4 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 276: convex_four; source clause 37166.
private theorem sound275 : C.clause (decodeClause atoms clause275) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 277: convex_four; source clause 37582.
private theorem sound276 : C.clause (decodeClause atoms clause276) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 4 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 278: convex_four; source clause 37790.
private theorem sound277 : C.clause (decodeClause atoms clause277) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 4 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 279: convex_four; source clause 37998.
private theorem sound278 : C.clause (decodeClause atoms clause278) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 280: convex_four; source clause 39870.
private theorem sound279 : C.clause (decodeClause atoms clause279) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 281: convex_four; source clause 40286.
private theorem sound280 : C.clause (decodeClause atoms clause280) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 282: convex_four; source clause 40494.
private theorem sound281 : C.clause (decodeClause atoms clause281) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 283: convex_four; source clause 40702.
private theorem sound282 : C.clause (decodeClause atoms clause282) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 6 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 284: convex_four; source clause 42155.
private theorem sound283 : C.clause (decodeClause atoms clause283) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 285: packet; source clause 43231.
private theorem sound284 : C.clause (decodeClause atoms clause284) := by
  exact C.covered_clause _ _ (C.packet_clause 0 11 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 286: convex_four; source clause 43406.
private theorem sound285 : C.clause (decodeClause atoms clause285) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 287: packet; source clause 43422.
private theorem sound286 : C.clause (decodeClause atoms clause286) := by
  exact C.covered_clause _ _ (C.packet_clause 0 2 12 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 288: convex_four; source clause 43614.
private theorem sound287 : C.clause (decodeClause atoms clause287) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 289: convex_four; source clause 43819.
private theorem sound288 : C.clause (decodeClause atoms clause288) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 290: packet; source clause 44037.
private theorem sound289 : C.clause (decodeClause atoms clause289) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 4 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 291: convex_four; source clause 44226.
private theorem sound290 : C.clause (decodeClause atoms clause290) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 4 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 292: packet; source clause 44447.
private theorem sound291 : C.clause (decodeClause atoms clause291) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 293: convex_four; source clause 44642.
private theorem sound292 : C.clause (decodeClause atoms clause292) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 294: convex_four; source clause 45058.
private theorem sound293 : C.clause (decodeClause atoms clause293) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 4 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 295: packet; source clause 45699.
private theorem sound294 : C.clause (decodeClause atoms clause294) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 296: packet; source clause 45701.
private theorem sound295 : C.clause (decodeClause atoms clause295) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 297: packet; source clause 45702.
private theorem sound296 : C.clause (decodeClause atoms clause296) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 298: convex_four; source clause 45902.
private theorem sound297 : C.clause (decodeClause atoms clause297) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 299: packet; source clause 46115.
private theorem sound298 : C.clause (decodeClause atoms clause298) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 300: packet; source clause 46117.
private theorem sound299 : C.clause (decodeClause atoms clause299) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 301: packet; source clause 46118.
private theorem sound300 : C.clause (decodeClause atoms clause300) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 302: convex_four; source clause 46318.
private theorem sound301 : C.clause (decodeClause atoms clause301) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 5 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 303: packet; source clause 46321.
private theorem sound302 : C.clause (decodeClause atoms clause302) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 304: packet; source clause 46323.
private theorem sound303 : C.clause (decodeClause atoms clause303) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 305: packet; source clause 46325.
private theorem sound304 : C.clause (decodeClause atoms clause304) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 306: packet; source clause 46326.
private theorem sound305 : C.clause (decodeClause atoms clause305) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 307: convex_four; source clause 46514.
private theorem sound306 : C.clause (decodeClause atoms clause306) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 308: convex_four; source clause 46518.
private theorem sound307 : C.clause (decodeClause atoms clause307) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true true) (by decide +kernel)

-- Clause 309: convex_four; source clause 46526.
private theorem sound308 : C.clause (decodeClause atoms clause308) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 310: convex_four; source clause 46734.
private theorem sound309 : C.clause (decodeClause atoms clause309) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 5 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 311: convex_four; source clause 46942.
private theorem sound310 : C.clause (decodeClause atoms clause310) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 5 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 312: convex_four; source clause 47346.
private theorem sound311 : C.clause (decodeClause atoms clause311) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 313: packet; source clause 47573.
private theorem sound312 : C.clause (decodeClause atoms clause312) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 314: convex_four; source clause 47762.
private theorem sound313 : C.clause (decodeClause atoms clause313) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 315: packet; source clause 48406.
private theorem sound314 : C.clause (decodeClause atoms clause314) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 316: convex_four; source clause 48606.
private theorem sound315 : C.clause (decodeClause atoms clause315) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 317: packet; source clause 48609.
private theorem sound316 : C.clause (decodeClause atoms clause316) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 318: packet; source clause 48614.
private theorem sound317 : C.clause (decodeClause atoms clause317) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 319: convex_four; source clause 48814.
private theorem sound318 : C.clause (decodeClause atoms clause318) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 320: convex_four; source clause 49022.
private theorem sound319 : C.clause (decodeClause atoms clause319) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 321: convex_four; source clause 49230.
private theorem sound320 : C.clause (decodeClause atoms clause320) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 322: convex_four; source clause 49631.
private theorem sound321 : C.clause (decodeClause atoms clause321) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 323: packet; source clause 50065.
private theorem sound322 : C.clause (decodeClause atoms clause322) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false true (by decide +kernel)) (by decide +kernel)

-- Clause 324: packet; source clause 50070.
private theorem sound323 : C.clause (decodeClause atoms clause323) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 325: convex_four; source clause 50262.
private theorem sound324 : C.clause (decodeClause atoms clause324) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true true) (by decide +kernel)

-- Clause 326: convex_four; source clause 50270.
private theorem sound325 : C.clause (decodeClause atoms clause325) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 327: convex_four; source clause 50478.
private theorem sound326 : C.clause (decodeClause atoms clause326) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 328: packet; source clause 50486.
private theorem sound327 : C.clause (decodeClause atoms clause327) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 329: convex_four; source clause 50686.
private theorem sound328 : C.clause (decodeClause atoms clause328) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 330: convex_four; source clause 50894.
private theorem sound329 : C.clause (decodeClause atoms clause329) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 331: packet; source clause 50901.
private theorem sound330 : C.clause (decodeClause atoms clause330) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 332: convex_four; source clause 51102.
private theorem sound331 : C.clause (decodeClause atoms clause331) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 333: convex_four; source clause 51307.
private theorem sound332 : C.clause (decodeClause atoms clause332) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 334: convex_four; source clause 53182.
private theorem sound333 : C.clause (decodeClause atoms clause333) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 335: convex_four; source clause 53598.
private theorem sound334 : C.clause (decodeClause atoms clause334) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 336: convex_four; source clause 53806.
private theorem sound335 : C.clause (decodeClause atoms clause335) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 337: convex_four; source clause 54014.
private theorem sound336 : C.clause (decodeClause atoms clause336) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 6 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 338: convex_four; source clause 55467.
private theorem sound337 : C.clause (decodeClause atoms clause337) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 339: convex_four; source clause 56718.
private theorem sound338 : C.clause (decodeClause atoms clause338) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 340: packet; source clause 56734.
private theorem sound339 : C.clause (decodeClause atoms clause339) := by
  exact C.covered_clause _ _ (C.packet_clause 0 4 12 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 341: convex_four; source clause 56926.
private theorem sound340 : C.clause (decodeClause atoms clause340) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 342: convex_four; source clause 57131.
private theorem sound341 : C.clause (decodeClause atoms clause341) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 343: convex_four; source clause 58798.
private theorem sound342 : C.clause (decodeClause atoms clause342) := by
  exact C.covered_clause _ _ (C.convex_clause 0 5 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 344: convex_four; source clause 59006.
private theorem sound343 : C.clause (decodeClause atoms clause343) := by
  exact C.covered_clause _ _ (C.convex_clause 0 5 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 345: packet; source clause 59045.
private theorem sound344 : C.clause (decodeClause atoms clause344) := by
  exact C.covered_clause _ _ (C.packet_clause 0 11 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 346: convex_four; source clause 59214.
private theorem sound345 : C.clause (decodeClause atoms clause345) := by
  exact C.covered_clause _ _ (C.convex_clause 0 5 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 347: convex_four; source clause 59422.
private theorem sound346 : C.clause (decodeClause atoms clause346) := by
  exact C.covered_clause _ _ (C.convex_clause 0 5 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 348: convex_four; source clause 60462.
private theorem sound347 : C.clause (decodeClause atoms clause347) := by
  exact C.covered_clause _ _ (C.convex_clause 0 5 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 349: convex_four; source clause 60670.
private theorem sound348 : C.clause (decodeClause atoms clause348) := by
  exact C.covered_clause _ _ (C.convex_clause 0 5 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 350: convex_four; source clause 60878.
private theorem sound349 : C.clause (decodeClause atoms clause349) := by
  exact C.covered_clause _ _ (C.convex_clause 0 5 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 351: convex_four; source clause 61086.
private theorem sound350 : C.clause (decodeClause atoms clause350) := by
  exact C.covered_clause _ _ (C.convex_clause 0 5 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 352: packet; source clause 61093.
private theorem sound351 : C.clause (decodeClause atoms clause351) := by
  exact C.covered_clause _ _ (C.packet_clause 0 5 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 353: convex_four; source clause 61294.
private theorem sound352 : C.clause (decodeClause atoms clause352) := by
  exact C.covered_clause _ _ (C.convex_clause 0 5 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 354: packet; source clause 61296.
private theorem sound353 : C.clause (decodeClause atoms clause353) := by
  exact C.covered_clause _ _ (C.packet_clause 0 5 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 355: convex_four; source clause 61499.
private theorem sound354 : C.clause (decodeClause atoms clause354) := by
  exact C.covered_clause _ _ (C.convex_clause 0 5 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 356: convex_four; source clause 62955.
private theorem sound355 : C.clause (decodeClause atoms clause355) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 357: packet; source clause 64031.
private theorem sound356 : C.clause (decodeClause atoms clause356) := by
  exact C.covered_clause _ _ (C.packet_clause 0 11 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 358: convex_four; source clause 64206.
private theorem sound357 : C.clause (decodeClause atoms clause357) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 359: packet; source clause 64222.
private theorem sound358 : C.clause (decodeClause atoms clause358) := by
  exact C.covered_clause _ _ (C.packet_clause 0 6 12 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 360: packet; source clause 64239.
private theorem sound359 : C.clause (decodeClause atoms clause359) := by
  exact C.covered_clause _ _ (C.packet_clause 0 12 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 361: convex_four; source clause 64414.
private theorem sound360 : C.clause (decodeClause atoms clause360) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 362: convex_four; source clause 64619.
private theorem sound361 : C.clause (decodeClause atoms clause361) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 363: convex_four; source clause 65662.
private theorem sound362 : C.clause (decodeClause atoms clause362) := by
  exact C.covered_clause _ _ (C.convex_clause 0 7 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 364: packet; source clause 65701.
private theorem sound363 : C.clause (decodeClause atoms clause363) := by
  exact C.covered_clause _ _ (C.packet_clause 0 11 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 365: convex_four; source clause 65870.
private theorem sound364 : C.clause (decodeClause atoms clause364) := by
  exact C.covered_clause _ _ (C.convex_clause 0 7 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 366: convex_four; source clause 66078.
private theorem sound365 : C.clause (decodeClause atoms clause365) := by
  exact C.covered_clause _ _ (C.convex_clause 0 7 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 367: convex_four; source clause 66286.
private theorem sound366 : C.clause (decodeClause atoms clause366) := by
  exact C.covered_clause _ _ (C.convex_clause 0 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 368: packet; source clause 66291.
private theorem sound367 : C.clause (decodeClause atoms clause367) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 369: packet; source clause 66293.
private theorem sound368 : C.clause (decodeClause atoms clause368) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 370: packet; source clause 66294.
private theorem sound369 : C.clause (decodeClause atoms clause369) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 371: convex_four; source clause 66494.
private theorem sound370 : C.clause (decodeClause atoms clause370) := by
  exact C.covered_clause _ _ (C.convex_clause 0 7 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 372: packet; source clause 66496.
private theorem sound371 : C.clause (decodeClause atoms clause371) := by
  exact C.covered_clause _ _ (C.packet_clause 0 7 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 373: convex_four; source clause 66699.
private theorem sound372 : C.clause (decodeClause atoms clause372) := by
  exact C.covered_clause _ _ (C.convex_clause 0 7 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 374: packet; source clause 67335.
private theorem sound373 : C.clause (decodeClause atoms clause373) := by
  exact C.covered_clause _ _ (C.packet_clause 0 8 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 375: packet; source clause 67340.
private theorem sound374 : C.clause (decodeClause atoms clause374) := by
  exact C.covered_clause _ _ (C.packet_clause 0 8 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 376: packet; source clause 67989.
private theorem sound375 : C.clause (decodeClause atoms clause375) := by
  exact C.covered_clause _ _ (C.packet_clause 0 11 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 377: convex_four; source clause 68158.
private theorem sound376 : C.clause (decodeClause atoms clause376) := by
  exact C.covered_clause _ _ (C.convex_clause 0 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 378: packet; source clause 68165.
private theorem sound377 : C.clause (decodeClause atoms clause377) := by
  exact C.covered_clause _ _ (C.packet_clause 0 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 379: convex_four; source clause 68366.
private theorem sound378 : C.clause (decodeClause atoms clause378) := by
  exact C.covered_clause _ _ (C.convex_clause 0 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 380: packet; source clause 68368.
private theorem sound379 : C.clause (decodeClause atoms clause379) := by
  exact C.covered_clause _ _ (C.packet_clause 0 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 381: convex_four; source clause 68571.
private theorem sound380 : C.clause (decodeClause atoms clause380) := by
  exact C.covered_clause _ _ (C.convex_clause 0 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 382: packet; source clause 68576.
private theorem sound381 : C.clause (decodeClause atoms clause381) := by
  exact C.covered_clause _ _ (C.packet_clause 0 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 383: packet; source clause 68600.
private theorem sound382 : C.clause (decodeClause atoms clause382) := by
  exact C.covered_clause _ _ (C.packet_clause 0 11 12 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 384: convex_four; source clause 68771.
private theorem sound383 : C.clause (decodeClause atoms clause383) := by
  exact C.covered_clause _ _ (C.convex_clause 0 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 385: convex_four; source clause 68779.
private theorem sound384 : C.clause (decodeClause atoms clause384) := by
  exact C.covered_clause _ _ (C.convex_clause 0 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 386: convex_four; source clause 68987.
private theorem sound385 : C.clause (decodeClause atoms clause385) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 387: convex_four; source clause 69403.
private theorem sound386 : C.clause (decodeClause atoms clause386) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 388: packet; source clause 69631.
private theorem sound387 : C.clause (decodeClause atoms clause387) := by
  exact C.covered_clause _ _ (C.packet_clause 1 3 2 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 389: convex_four; source clause 69819.
private theorem sound388 : C.clause (decodeClause atoms clause388) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 390: convex_four; source clause 70235.
private theorem sound389 : C.clause (decodeClause atoms clause389) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 391: convex_four; source clause 71070.
private theorem sound390 : C.clause (decodeClause atoms clause390) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 4 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 392: convex_four; source clause 71486.
private theorem sound391 : C.clause (decodeClause atoms clause391) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 393: convex_four; source clause 71902.
private theorem sound392 : C.clause (decodeClause atoms clause392) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 4 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 394: convex_four; source clause 72110.
private theorem sound393 : C.clause (decodeClause atoms clause393) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 4 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 395: convex_four; source clause 72318.
private theorem sound394 : C.clause (decodeClause atoms clause394) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 396: convex_four; source clause 74190.
private theorem sound395 : C.clause (decodeClause atoms clause395) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 397: convex_four; source clause 74606.
private theorem sound396 : C.clause (decodeClause atoms clause396) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 398: convex_four; source clause 74814.
private theorem sound397 : C.clause (decodeClause atoms clause397) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 399: convex_four; source clause 75022.
private theorem sound398 : C.clause (decodeClause atoms clause398) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 6 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 400: convex_four; source clause 76475.
private theorem sound399 : C.clause (decodeClause atoms clause399) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 401: packet; source clause 77669.
private theorem sound400 : C.clause (decodeClause atoms clause400) := by
  exact C.covered_clause _ _ (C.packet_clause 11 1 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 402: convex_four; source clause 77726.
private theorem sound401 : C.clause (decodeClause atoms clause401) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 403: packet; source clause 77734.
private theorem sound402 : C.clause (decodeClause atoms clause402) := by
  exact C.covered_clause _ _ (C.packet_clause 1 2 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 404: convex_four; source clause 77934.
private theorem sound403 : C.clause (decodeClause atoms clause403) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 405: convex_four; source clause 78139.
private theorem sound404 : C.clause (decodeClause atoms clause404) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 406: convex_four; source clause 78546.
private theorem sound405 : C.clause (decodeClause atoms clause405) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 4 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 407: packet; source clause 78790.
private theorem sound406 : C.clause (decodeClause atoms clause406) := by
  exact C.covered_clause _ _ (C.packet_clause 1 4 3 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 408: convex_four; source clause 78962.
private theorem sound407 : C.clause (decodeClause atoms clause407) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 409: convex_four; source clause 79378.
private theorem sound408 : C.clause (decodeClause atoms clause408) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 4 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 410: convex_four; source clause 81666.
private theorem sound409 : C.clause (decodeClause atoms clause409) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 411: convex_four; source clause 82082.
private theorem sound410 : C.clause (decodeClause atoms clause410) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 412: convex_four; source clause 83951.
private theorem sound411 : C.clause (decodeClause atoms clause411) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 413: convex_four; source clause 87502.
private theorem sound412 : C.clause (decodeClause atoms clause412) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 414: convex_four; source clause 87918.
private theorem sound413 : C.clause (decodeClause atoms clause413) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 415: convex_four; source clause 88126.
private theorem sound414 : C.clause (decodeClause atoms clause414) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 416: convex_four; source clause 88334.
private theorem sound415 : C.clause (decodeClause atoms clause415) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 6 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 417: convex_four; source clause 89787.
private theorem sound416 : C.clause (decodeClause atoms clause416) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 418: convex_four; source clause 91038.
private theorem sound417 : C.clause (decodeClause atoms clause417) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 419: convex_four; source clause 91246.
private theorem sound418 : C.clause (decodeClause atoms clause418) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 420: convex_four; source clause 91451.
private theorem sound419 : C.clause (decodeClause atoms clause419) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 421: convex_four; source clause 97275.
private theorem sound420 : C.clause (decodeClause atoms clause420) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 422: convex_four; source clause 98526.
private theorem sound421 : C.clause (decodeClause atoms clause421) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 423: convex_four; source clause 98734.
private theorem sound422 : C.clause (decodeClause atoms clause422) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 424: convex_four; source clause 98939.
private theorem sound423 : C.clause (decodeClause atoms clause423) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 425: packet; source clause 102920.
private theorem sound424 : C.clause (decodeClause atoms clause424) := by
  exact C.covered_clause _ _ (C.packet_clause 1 11 12 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 426: convex_four; source clause 103095.
private theorem sound425 : C.clause (decodeClause atoms clause425) := by
  exact C.covered_clause _ _ (C.convex_clause 1 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 427: convex_four; source clause 103099.
private theorem sound426 : C.clause (decodeClause atoms clause426) := by
  exact C.covered_clause _ _ (C.convex_clause 1 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 428: convex_four; source clause 103506.
private theorem sound427 : C.clause (decodeClause atoms clause427) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 4 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 429: packet; source clause 103813.
private theorem sound428 : C.clause (decodeClause atoms clause428) := by
  exact C.covered_clause _ _ (C.packet_clause 3 8 2 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 430: convex_four; source clause 103922.
private theorem sound429 : C.clause (decodeClause atoms clause429) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 431: convex_four; source clause 104338.
private theorem sound430 : C.clause (decodeClause atoms clause430) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 4 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 432: convex_four; source clause 106626.
private theorem sound431 : C.clause (decodeClause atoms clause431) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 433: convex_four; source clause 107042.
private theorem sound432 : C.clause (decodeClause atoms clause432) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 434: convex_four; source clause 108911.
private theorem sound433 : C.clause (decodeClause atoms clause433) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 435: convex_four; source clause 112462.
private theorem sound434 : C.clause (decodeClause atoms clause434) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 436: convex_four; source clause 112878.
private theorem sound435 : C.clause (decodeClause atoms clause435) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 437: convex_four; source clause 113086.
private theorem sound436 : C.clause (decodeClause atoms clause436) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 438: convex_four; source clause 113294.
private theorem sound437 : C.clause (decodeClause atoms clause437) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 6 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 439: convex_four; source clause 114747.
private theorem sound438 : C.clause (decodeClause atoms clause438) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 440: packet; source clause 115941.
private theorem sound439 : C.clause (decodeClause atoms clause439) := by
  exact C.covered_clause _ _ (C.packet_clause 11 2 4 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 441: convex_four; source clause 115998.
private theorem sound440 : C.clause (decodeClause atoms clause440) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 442: packet; source clause 116149.
private theorem sound441 : C.clause (decodeClause atoms clause441) := by
  exact C.covered_clause _ _ (C.packet_clause 12 2 4 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 443: convex_four; source clause 116206.
private theorem sound442 : C.clause (decodeClause atoms clause442) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 444: convex_four; source clause 116411.
private theorem sound443 : C.clause (decodeClause atoms clause443) := by
  exact C.covered_clause _ _ (C.convex_clause 2 4 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 445: convex_four; source clause 122235.
private theorem sound444 : C.clause (decodeClause atoms clause444) := by
  exact C.covered_clause _ _ (C.convex_clause 2 6 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 446: convex_four; source clause 123486.
private theorem sound445 : C.clause (decodeClause atoms clause445) := by
  exact C.covered_clause _ _ (C.convex_clause 2 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 447: convex_four; source clause 123694.
private theorem sound446 : C.clause (decodeClause atoms clause446) := by
  exact C.covered_clause _ _ (C.convex_clause 2 6 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 448: convex_four; source clause 123899.
private theorem sound447 : C.clause (decodeClause atoms clause447) := by
  exact C.covered_clause _ _ (C.convex_clause 2 6 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 449: packet; source clause 127880.
private theorem sound448 : C.clause (decodeClause atoms clause448) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 12 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 450: packet; source clause 127882.
private theorem sound449 : C.clause (decodeClause atoms clause449) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 12 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 451: convex_four; source clause 128051.
private theorem sound450 : C.clause (decodeClause atoms clause450) := by
  exact C.covered_clause _ _ (C.convex_clause 2 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 452: convex_four; source clause 128055.
private theorem sound451 : C.clause (decodeClause atoms clause451) := by
  exact C.covered_clause _ _ (C.convex_clause 2 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 453: convex_four; source clause 128059.
private theorem sound452 : C.clause (decodeClause atoms clause452) := by
  exact C.covered_clause _ _ (C.convex_clause 2 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 454: packet; source clause 129765.
private theorem sound453 : C.clause (decodeClause atoms clause453) := by
  exact C.covered_clause _ _ (C.packet_clause 3 8 4 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 455: convex_four; source clause 129934.
private theorem sound454 : C.clause (decodeClause atoms clause454) := by
  exact C.covered_clause _ _ (C.convex_clause 3 4 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 456: convex_four; source clause 130350.
private theorem sound455 : C.clause (decodeClause atoms clause455) := by
  exact C.covered_clause _ _ (C.convex_clause 3 4 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 457: convex_four; source clause 132211.
private theorem sound456 : C.clause (decodeClause atoms clause456) := by
  exact C.covered_clause _ _ (C.convex_clause 3 4 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 458: convex_four; source clause 132219.
private theorem sound457 : C.clause (decodeClause atoms clause457) := by
  exact C.covered_clause _ _ (C.convex_clause 3 4 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 459: convex_four; source clause 135342.
private theorem sound458 : C.clause (decodeClause atoms clause458) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 460: convex_four; source clause 135550.
private theorem sound459 : C.clause (decodeClause atoms clause459) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 461: convex_four; source clause 135758.
private theorem sound460 : C.clause (decodeClause atoms clause460) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 462: convex_four; source clause 135966.
private theorem sound461 : C.clause (decodeClause atoms clause461) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 463: convex_four; source clause 136174.
private theorem sound462 : C.clause (decodeClause atoms clause462) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 7 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 464: convex_four; source clause 136379.
private theorem sound463 : C.clause (decodeClause atoms clause463) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 465: convex_four; source clause 136587.
private theorem sound464 : C.clause (decodeClause atoms clause464) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 466: convex_four; source clause 136795.
private theorem sound465 : C.clause (decodeClause atoms clause465) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 467: convex_four; source clause 137003.
private theorem sound466 : C.clause (decodeClause atoms clause466) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 468: convex_four; source clause 137214.
private theorem sound467 : C.clause (decodeClause atoms clause467) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 469: convex_four; source clause 137422.
private theorem sound468 : C.clause (decodeClause atoms clause468) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 470: convex_four; source clause 137630.
private theorem sound469 : C.clause (decodeClause atoms clause469) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 471: convex_four; source clause 137838.
private theorem sound470 : C.clause (decodeClause atoms clause470) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 472: convex_four; source clause 138046.
private theorem sound471 : C.clause (decodeClause atoms clause471) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 473: convex_four; source clause 138251.
private theorem sound472 : C.clause (decodeClause atoms clause472) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 474: packet; source clause 139316.
private theorem sound473 : C.clause (decodeClause atoms clause473) := by
  exact C.covered_clause _ _ (C.packet_clause 3 8 6 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 475: packet; source clause 139317.
private theorem sound474 : C.clause (decodeClause atoms clause474) := by
  exact C.covered_clause _ _ (C.packet_clause 3 8 6 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 476: packet; source clause 139504.
private theorem sound475 : C.clause (decodeClause atoms clause475) := by
  exact C.covered_clause _ _ (C.packet_clause 3 6 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 477: convex_four; source clause 139707.
private theorem sound476 : C.clause (decodeClause atoms clause476) := by
  exact C.covered_clause _ _ (C.convex_clause 3 6 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 478: convex_four; source clause 141579.
private theorem sound477 : C.clause (decodeClause atoms clause477) := by
  exact C.covered_clause _ _ (C.convex_clause 3 7 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 479: convex_four; source clause 141787.
private theorem sound478 : C.clause (decodeClause atoms clause478) := by
  exact C.covered_clause _ _ (C.convex_clause 3 7 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 480: packet; source clause 141925.
private theorem sound479 : C.clause (decodeClause atoms clause479) := by
  exact C.covered_clause _ _ (C.packet_clause 8 11 3 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 481: convex_four; source clause 141995.
private theorem sound480 : C.clause (decodeClause atoms clause480) := by
  exact C.covered_clause _ _ (C.convex_clause 3 7 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 482: convex_four; source clause 142203.
private theorem sound481 : C.clause (decodeClause atoms clause481) := by
  exact C.covered_clause _ _ (C.convex_clause 3 7 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 483: convex_four; source clause 142414.
private theorem sound482 : C.clause (decodeClause atoms clause482) := by
  exact C.covered_clause _ _ (C.convex_clause 3 7 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 484: convex_four; source clause 142622.
private theorem sound483 : C.clause (decodeClause atoms clause483) := by
  exact C.covered_clause _ _ (C.convex_clause 3 7 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 485: convex_four; source clause 142830.
private theorem sound484 : C.clause (decodeClause atoms clause484) := by
  exact C.covered_clause _ _ (C.convex_clause 3 7 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 486: convex_four; source clause 143038.
private theorem sound485 : C.clause (decodeClause atoms clause485) := by
  exact C.covered_clause _ _ (C.convex_clause 3 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 487: convex_four; source clause 143246.
private theorem sound486 : C.clause (decodeClause atoms clause486) := by
  exact C.covered_clause _ _ (C.convex_clause 3 7 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 488: convex_four; source clause 143451.
private theorem sound487 : C.clause (decodeClause atoms clause487) := by
  exact C.covered_clause _ _ (C.convex_clause 3 7 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 489: convex_four; source clause 143650.
private theorem sound488 : C.clause (decodeClause atoms clause488) := by
  exact C.covered_clause _ _ (C.convex_clause 3 8 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 490: convex_four; source clause 143858.
private theorem sound489 : C.clause (decodeClause atoms clause489) := by
  exact C.covered_clause _ _ (C.convex_clause 3 8 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 491: convex_four; source clause 144066.
private theorem sound490 : C.clause (decodeClause atoms clause490) := by
  exact C.covered_clause _ _ (C.convex_clause 3 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 492: packet; source clause 144133.
private theorem sound491 : C.clause (decodeClause atoms clause491) := by
  exact C.covered_clause _ _ (C.packet_clause 8 3 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 493: packet; source clause 144136.
private theorem sound492 : C.clause (decodeClause atoms clause492) := by
  exact C.covered_clause _ _ (C.packet_clause 8 3 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 494: packet; source clause 144165.
private theorem sound493 : C.clause (decodeClause atoms clause493) := by
  exact C.covered_clause _ _ (C.packet_clause 8 11 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 495: convex_four; source clause 144274.
private theorem sound494 : C.clause (decodeClause atoms clause494) := by
  exact C.covered_clause _ _ (C.convex_clause 3 8 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 496: packet; source clause 144341.
private theorem sound495 : C.clause (decodeClause atoms clause495) := by
  exact C.covered_clause _ _ (C.packet_clause 8 3 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 497: packet; source clause 144344.
private theorem sound496 : C.clause (decodeClause atoms clause496) := by
  exact C.covered_clause _ _ (C.packet_clause 8 3 12 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 498: packet; source clause 144373.
private theorem sound497 : C.clause (decodeClause atoms clause497) := by
  exact C.covered_clause _ _ (C.packet_clause 8 12 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 499: convex_four; source clause 144482.
private theorem sound498 : C.clause (decodeClause atoms clause498) := by
  exact C.covered_clause _ _ (C.convex_clause 3 8 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 500: convex_four; source clause 144486.
private theorem sound499 : C.clause (decodeClause atoms clause499) := by
  exact C.covered_clause _ _ (C.convex_clause 3 8 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true true) (by decide +kernel)

-- Clause 501: convex_four; source clause 144687.
private theorem sound500 : C.clause (decodeClause atoms clause500) := by
  exact C.covered_clause _ _ (C.convex_clause 3 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 502: convex_four; source clause 144695.
private theorem sound501 : C.clause (decodeClause atoms clause501) := by
  exact C.covered_clause _ _ (C.convex_clause 3 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 503: convex_four; source clause 144910.
private theorem sound502 : C.clause (decodeClause atoms clause502) := by
  exact C.covered_clause _ _ (C.convex_clause 3 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 504: convex_four; source clause 145118.
private theorem sound503 : C.clause (decodeClause atoms clause503) := by
  exact C.covered_clause _ _ (C.convex_clause 3 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 505: convex_four; source clause 145323.
private theorem sound504 : C.clause (decodeClause atoms clause504) := by
  exact C.covered_clause _ _ (C.convex_clause 3 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 506: convex_four; source clause 145531.
private theorem sound505 : C.clause (decodeClause atoms clause505) := by
  exact C.covered_clause _ _ (C.convex_clause 3 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 507: convex_four; source clause 151355.
private theorem sound506 : C.clause (decodeClause atoms clause506) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 508: packet; source clause 152549.
private theorem sound507 : C.clause (decodeClause atoms clause507) := by
  exact C.covered_clause _ _ (C.packet_clause 11 4 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 509: convex_four; source clause 152604.
private theorem sound508 : C.clause (decodeClause atoms clause508) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true) (by decide +kernel)

-- Clause 510: convex_four; source clause 152606.
private theorem sound509 : C.clause (decodeClause atoms clause509) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 511: packet; source clause 152757.
private theorem sound510 : C.clause (decodeClause atoms clause510) := by
  exact C.covered_clause _ _ (C.packet_clause 12 4 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 512: convex_four; source clause 152814.
private theorem sound511 : C.clause (decodeClause atoms clause511) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 513: convex_four; source clause 153019.
private theorem sound512 : C.clause (decodeClause atoms clause512) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 514: packet; source clause 157000.
private theorem sound513 : C.clause (decodeClause atoms clause513) := by
  exact C.covered_clause _ _ (C.packet_clause 4 11 12 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 515: convex_four; source clause 157179.
private theorem sound514 : C.clause (decodeClause atoms clause514) := by
  exact C.covered_clause _ _ (C.convex_clause 4 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 516: convex_four; source clause 160507.
private theorem sound515 : C.clause (decodeClause atoms clause515) := by
  exact C.covered_clause _ _ (C.convex_clause 5 7 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 517: convex_four; source clause 160715.
private theorem sound516 : C.clause (decodeClause atoms clause516) := by
  exact C.covered_clause _ _ (C.convex_clause 5 7 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 518: packet; source clause 160853.
private theorem sound517 : C.clause (decodeClause atoms clause517) := by
  exact C.covered_clause _ _ (C.packet_clause 8 11 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 519: convex_four; source clause 160923.
private theorem sound518 : C.clause (decodeClause atoms clause518) := by
  exact C.covered_clause _ _ (C.convex_clause 5 7 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 520: convex_four; source clause 161131.
private theorem sound519 : C.clause (decodeClause atoms clause519) := by
  exact C.covered_clause _ _ (C.convex_clause 5 7 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 521: convex_four; source clause 161342.
private theorem sound520 : C.clause (decodeClause atoms clause520) := by
  exact C.covered_clause _ _ (C.convex_clause 5 7 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 522: convex_four; source clause 161550.
private theorem sound521 : C.clause (decodeClause atoms clause521) := by
  exact C.covered_clause _ _ (C.convex_clause 5 7 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 523: convex_four; source clause 161758.
private theorem sound522 : C.clause (decodeClause atoms clause522) := by
  exact C.covered_clause _ _ (C.convex_clause 5 7 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 524: convex_four; source clause 161966.
private theorem sound523 : C.clause (decodeClause atoms clause523) := by
  exact C.covered_clause _ _ (C.convex_clause 5 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 525: convex_four; source clause 162174.
private theorem sound524 : C.clause (decodeClause atoms clause524) := by
  exact C.covered_clause _ _ (C.convex_clause 5 7 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 526: convex_four; source clause 162379.
private theorem sound525 : C.clause (decodeClause atoms clause525) := by
  exact C.covered_clause _ _ (C.convex_clause 5 7 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 527: convex_four; source clause 162578.
private theorem sound526 : C.clause (decodeClause atoms clause526) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 528: packet; source clause 162646.
private theorem sound527 : C.clause (decodeClause atoms clause527) := by
  exact C.covered_clause _ _ (C.packet_clause 8 5 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 529: convex_four; source clause 162786.
private theorem sound528 : C.clause (decodeClause atoms clause528) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 530: convex_four; source clause 162994.
private theorem sound529 : C.clause (decodeClause atoms clause529) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 531: packet; source clause 163061.
private theorem sound530 : C.clause (decodeClause atoms clause530) := by
  exact C.covered_clause _ _ (C.packet_clause 8 5 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 532: convex_four; source clause 163202.
private theorem sound531 : C.clause (decodeClause atoms clause531) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 533: packet; source clause 163269.
private theorem sound532 : C.clause (decodeClause atoms clause532) := by
  exact C.covered_clause _ _ (C.packet_clause 8 5 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 534: packet; source clause 163301.
private theorem sound533 : C.clause (decodeClause atoms clause533) := by
  exact C.covered_clause _ _ (C.packet_clause 8 12 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 535: convex_four; source clause 163410.
private theorem sound534 : C.clause (decodeClause atoms clause534) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 536: convex_four; source clause 163414.
private theorem sound535 : C.clause (decodeClause atoms clause535) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true true) (by decide +kernel)

-- Clause 537: packet; source clause 163472.
private theorem sound536 : C.clause (decodeClause atoms clause536) := by
  exact C.covered_clause _ _ (C.packet_clause 8 5 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 538: convex_four; source clause 163615.
private theorem sound537 : C.clause (decodeClause atoms clause537) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 539: convex_four; source clause 163623.
private theorem sound538 : C.clause (decodeClause atoms clause538) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 540: convex_four; source clause 163838.
private theorem sound539 : C.clause (decodeClause atoms clause539) := by
  exact C.covered_clause _ _ (C.convex_clause 5 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 541: convex_four; source clause 164046.
private theorem sound540 : C.clause (decodeClause atoms clause540) := by
  exact C.covered_clause _ _ (C.convex_clause 5 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 542: convex_four; source clause 164251.
private theorem sound541 : C.clause (decodeClause atoms clause541) := by
  exact C.covered_clause _ _ (C.convex_clause 5 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 543: convex_four; source clause 164459.
private theorem sound542 : C.clause (decodeClause atoms clause542) := by
  exact C.covered_clause _ _ (C.convex_clause 5 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 544: packet; source clause 168440.
private theorem sound543 : C.clause (decodeClause atoms clause543) := by
  exact C.covered_clause _ _ (C.packet_clause 6 11 12 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 545: convex_four; source clause 168619.
private theorem sound544 : C.clause (decodeClause atoms clause544) := by
  exact C.covered_clause _ _ (C.convex_clause 6 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 546: convex_four; source clause 168818.
private theorem sound545 : C.clause (decodeClause atoms clause545) := by
  exact C.covered_clause _ _ (C.convex_clause 7 8 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 547: convex_four; source clause 169026.
private theorem sound546 : C.clause (decodeClause atoms clause546) := by
  exact C.covered_clause _ _ (C.convex_clause 7 8 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 548: convex_four; source clause 169234.
private theorem sound547 : C.clause (decodeClause atoms clause547) := by
  exact C.covered_clause _ _ (C.convex_clause 7 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 549: packet; source clause 169301.
private theorem sound548 : C.clause (decodeClause atoms clause548) := by
  exact C.covered_clause _ _ (C.packet_clause 8 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 550: packet; source clause 169333.
private theorem sound549 : C.clause (decodeClause atoms clause549) := by
  exact C.covered_clause _ _ (C.packet_clause 8 11 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 551: convex_four; source clause 169442.
private theorem sound550 : C.clause (decodeClause atoms clause550) := by
  exact C.covered_clause _ _ (C.convex_clause 7 8 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 552: packet; source clause 169509.
private theorem sound551 : C.clause (decodeClause atoms clause551) := by
  exact C.covered_clause _ _ (C.packet_clause 8 7 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 553: packet; source clause 169541.
private theorem sound552 : C.clause (decodeClause atoms clause552) := by
  exact C.covered_clause _ _ (C.packet_clause 8 12 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 554: convex_four; source clause 169650.
private theorem sound553 : C.clause (decodeClause atoms clause553) := by
  exact C.covered_clause _ _ (C.convex_clause 7 8 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 555: convex_four; source clause 169654.
private theorem sound554 : C.clause (decodeClause atoms clause554) := by
  exact C.covered_clause _ _ (C.convex_clause 7 8 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true true) (by decide +kernel)

-- Clause 556: packet; source clause 169712.
private theorem sound555 : C.clause (decodeClause atoms clause555) := by
  exact C.covered_clause _ _ (C.packet_clause 8 7 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 557: packet; source clause 169736.
private theorem sound556 : C.clause (decodeClause atoms clause556) := by
  exact C.covered_clause _ _ (C.packet_clause 8 11 12 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 558: convex_four; source clause 169855.
private theorem sound557 : C.clause (decodeClause atoms clause557) := by
  exact C.covered_clause _ _ (C.convex_clause 7 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 559: convex_four; source clause 169863.
private theorem sound558 : C.clause (decodeClause atoms clause558) := by
  exact C.covered_clause _ _ (C.convex_clause 7 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 560: convex_four; source clause 170078.
private theorem sound559 : C.clause (decodeClause atoms clause559) := by
  exact C.covered_clause _ _ (C.convex_clause 7 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 561: convex_four; source clause 170286.
private theorem sound560 : C.clause (decodeClause atoms clause560) := by
  exact C.covered_clause _ _ (C.convex_clause 7 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 562: convex_four; source clause 170491.
private theorem sound561 : C.clause (decodeClause atoms clause561) := by
  exact C.covered_clause _ _ (C.convex_clause 7 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 563: convex_four; source clause 170699.
private theorem sound562 : C.clause (decodeClause atoms clause562) := by
  exact C.covered_clause _ _ (C.convex_clause 7 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 564: packet; source clause 170709.
private theorem sound563 : C.clause (decodeClause atoms clause563) := by
  exact C.covered_clause _ _ (C.packet_clause 8 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 565: packet; source clause 170741.
private theorem sound564 : C.clause (decodeClause atoms clause564) := by
  exact C.covered_clause _ _ (C.packet_clause 8 11 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 566: convex_four; source clause 170910.
private theorem sound565 : C.clause (decodeClause atoms clause565) := by
  exact C.covered_clause _ _ (C.convex_clause 8 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 567: packet; source clause 170917.
private theorem sound566 : C.clause (decodeClause atoms clause566) := by
  exact C.covered_clause _ _ (C.packet_clause 8 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 568: packet; source clause 170949.
private theorem sound567 : C.clause (decodeClause atoms clause567) := by
  exact C.covered_clause _ _ (C.packet_clause 8 12 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 569: convex_four; source clause 171114.
private theorem sound568 : C.clause (decodeClause atoms clause568) := by
  exact C.covered_clause _ _ (C.convex_clause 8 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 570: convex_four; source clause 171118.
private theorem sound569 : C.clause (decodeClause atoms clause569) := by
  exact C.covered_clause _ _ (C.convex_clause 8 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 571: convex_four; source clause 171315.
private theorem sound570 : C.clause (decodeClause atoms clause570) := by
  exact C.covered_clause _ _ (C.convex_clause 8 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false) (by decide +kernel)

-- Clause 572: convex_four; source clause 171323.
private theorem sound571 : C.clause (decodeClause atoms clause571) := by
  exact C.covered_clause _ _ (C.convex_clause 8 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 573: convex_four; source clause 171531.
private theorem sound572 : C.clause (decodeClause atoms clause572) := by
  exact C.covered_clause _ _ (C.convex_clause 8 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 574: convex_four; source clause 171739.
private theorem sound573 : C.clause (decodeClause atoms clause573) := by
  exact C.covered_clause _ _ (C.convex_clause 9 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 575: no_octagon; source clause 171743.
private theorem sound574 : C.clause (decodeClause atoms clause574) := by
  exact C.no_octagon_clause {0, 1, 2, 3, 4, 6, 8, 10} (by decide +kernel) _ (by decide +kernel)

-- Clause 576: no_octagon; source clause 171754.
private theorem sound575 : C.clause (decodeClause atoms clause575) := by
  exact C.no_octagon_clause {0, 1, 2, 4, 6, 10, 11, 12} (by decide +kernel) _ (by decide +kernel)

-- Clause 577: no_octagon; source clause 171755.
private theorem sound576 : C.clause (decodeClause atoms clause576) := by
  exact C.no_octagon_clause {0, 3, 5, 7, 9, 10, 11, 12} (by decide +kernel) _ (by decide +kernel)

-- Clause 578: no_octagon; source clause 171760.
private theorem sound577 : C.clause (decodeClause atoms clause577) := by
  exact C.no_octagon_clause {3, 5, 7, 8, 9, 10, 11, 12} (by decide +kernel) _ (by decide +kernel)

private theorem all_sound : List.Forall (fun cl => C.clause (decodeClause atoms cl)) clauses := by
  exact And.intro (sound000 C) (And.intro (sound001 C) (And.intro (sound002 C) (And.intro (sound003 C) (And.intro (sound004 C) (And.intro (sound005 C) (And.intro (sound006 C) (And.intro (sound007 C) (And.intro (sound008 C) (And.intro (sound009 C) (And.intro (sound010 C) (And.intro (sound011 C) (And.intro (sound012 C) (And.intro (sound013 C) (And.intro (sound014 C) (And.intro (sound015 C) (And.intro (sound016 C) (And.intro (sound017 C) (And.intro (sound018 C) (And.intro (sound019 C) (And.intro (sound020 C) (And.intro (sound021 C) (And.intro (sound022 C) (And.intro (sound023 C) (And.intro (sound024 C) (And.intro (sound025 C) (And.intro (sound026 C) (And.intro (sound027 C) (And.intro (sound028 C) (And.intro (sound029 C) (And.intro (sound030 C) (And.intro (sound031 C) (And.intro (sound032 C) (And.intro (sound033 C) (And.intro (sound034 C) (And.intro (sound035 C) (And.intro (sound036 C) (And.intro (sound037 C) (And.intro (sound038 C) (And.intro (sound039 C) (And.intro (sound040 C) (And.intro (sound041 C) (And.intro (sound042 C) (And.intro (sound043 C) (And.intro (sound044 C) (And.intro (sound045 C) (And.intro (sound046 C) (And.intro (sound047 C) (And.intro (sound048 C) (And.intro (sound049 C) (And.intro (sound050 C) (And.intro (sound051 C) (And.intro (sound052 C) (And.intro (sound053 C) (And.intro (sound054 C) (And.intro (sound055 C) (And.intro (sound056 C) (And.intro (sound057 C) (And.intro (sound058 C) (And.intro (sound059 C) (And.intro (sound060 C) (And.intro (sound061 C) (And.intro (sound062 C) (And.intro (sound063 C) (And.intro (sound064 C) (And.intro (sound065 C) (And.intro (sound066 C) (And.intro (sound067 C) (And.intro (sound068 C) (And.intro (sound069 C) (And.intro (sound070 C) (And.intro (sound071 C) (And.intro (sound072 C) (And.intro (sound073 C) (And.intro (sound074 C) (And.intro (sound075 C) (And.intro (sound076 C) (And.intro (sound077 C) (And.intro (sound078 C) (And.intro (sound079 C) (And.intro (sound080 C) (And.intro (sound081 C) (And.intro (sound082 C) (And.intro (sound083 C) (And.intro (sound084 C) (And.intro (sound085 C) (And.intro (sound086 C) (And.intro (sound087 C) (And.intro (sound088 C) (And.intro (sound089 C) (And.intro (sound090 C) (And.intro (sound091 C) (And.intro (sound092 C) (And.intro (sound093 C) (And.intro (sound094 C) (And.intro (sound095 C) (And.intro (sound096 C) (And.intro (sound097 C) (And.intro (sound098 C) (And.intro (sound099 C) (And.intro (sound100 C) (And.intro (sound101 C) (And.intro (sound102 C) (And.intro (sound103 C) (And.intro (sound104 C) (And.intro (sound105 C) (And.intro (sound106 C) (And.intro (sound107 C) (And.intro (sound108 C) (And.intro (sound109 C) (And.intro (sound110 C) (And.intro (sound111 C) (And.intro (sound112 C) (And.intro (sound113 C) (And.intro (sound114 C) (And.intro (sound115 C) (And.intro (sound116 C) (And.intro (sound117 C) (And.intro (sound118 C) (And.intro (sound119 C) (And.intro (sound120 C) (And.intro (sound121 C) (And.intro (sound122 C) (And.intro (sound123 C) (And.intro (sound124 C) (And.intro (sound125 C) (And.intro (sound126 C) (And.intro (sound127 C) (And.intro (sound128 C) (And.intro (sound129 C) (And.intro (sound130 C) (And.intro (sound131 C) (And.intro (sound132 C) (And.intro (sound133 C) (And.intro (sound134 C) (And.intro (sound135 C) (And.intro (sound136 C) (And.intro (sound137 C) (And.intro (sound138 C) (And.intro (sound139 C) (And.intro (sound140 C) (And.intro (sound141 C) (And.intro (sound142 C) (And.intro (sound143 C) (And.intro (sound144 C) (And.intro (sound145 C) (And.intro (sound146 C) (And.intro (sound147 C) (And.intro (sound148 C) (And.intro (sound149 C) (And.intro (sound150 C) (And.intro (sound151 C) (And.intro (sound152 C) (And.intro (sound153 C) (And.intro (sound154 C) (And.intro (sound155 C) (And.intro (sound156 C) (And.intro (sound157 C) (And.intro (sound158 C) (And.intro (sound159 C) (And.intro (sound160 C) (And.intro (sound161 C) (And.intro (sound162 C) (And.intro (sound163 C) (And.intro (sound164 C) (And.intro (sound165 C) (And.intro (sound166 C) (And.intro (sound167 C) (And.intro (sound168 C) (And.intro (sound169 C) (And.intro (sound170 C) (And.intro (sound171 C) (And.intro (sound172 C) (And.intro (sound173 C) (And.intro (sound174 C) (And.intro (sound175 C) (And.intro (sound176 C) (And.intro (sound177 C) (And.intro (sound178 C) (And.intro (sound179 C) (And.intro (sound180 C) (And.intro (sound181 C) (And.intro (sound182 C) (And.intro (sound183 C) (And.intro (sound184 C) (And.intro (sound185 C) (And.intro (sound186 C) (And.intro (sound187 C) (And.intro (sound188 C) (And.intro (sound189 C) (And.intro (sound190 C) (And.intro (sound191 C) (And.intro (sound192 C) (And.intro (sound193 C) (And.intro (sound194 C) (And.intro (sound195 C) (And.intro (sound196 C) (And.intro (sound197 C) (And.intro (sound198 C) (And.intro (sound199 C) (And.intro (sound200 C) (And.intro (sound201 C) (And.intro (sound202 C) (And.intro (sound203 C) (And.intro (sound204 C) (And.intro (sound205 C) (And.intro (sound206 C) (And.intro (sound207 C) (And.intro (sound208 C) (And.intro (sound209 C) (And.intro (sound210 C) (And.intro (sound211 C) (And.intro (sound212 C) (And.intro (sound213 C) (And.intro (sound214 C) (And.intro (sound215 C) (And.intro (sound216 C) (And.intro (sound217 C) (And.intro (sound218 C) (And.intro (sound219 C) (And.intro (sound220 C) (And.intro (sound221 C) (And.intro (sound222 C) (And.intro (sound223 C) (And.intro (sound224 C) (And.intro (sound225 C) (And.intro (sound226 C) (And.intro (sound227 C) (And.intro (sound228 C) (And.intro (sound229 C) (And.intro (sound230 C) (And.intro (sound231 C) (And.intro (sound232 C) (And.intro (sound233 C) (And.intro (sound234 C) (And.intro (sound235 C) (And.intro (sound236 C) (And.intro (sound237 C) (And.intro (sound238 C) (And.intro (sound239 C) (And.intro (sound240 C) (And.intro (sound241 C) (And.intro (sound242 C) (And.intro (sound243 C) (And.intro (sound244 C) (And.intro (sound245 C) (And.intro (sound246 C) (And.intro (sound247 C) (And.intro (sound248 C) (And.intro (sound249 C) (And.intro (sound250 C) (And.intro (sound251 C) (And.intro (sound252 C) (And.intro (sound253 C) (And.intro (sound254 C) (And.intro (sound255 C) (And.intro (sound256 C) (And.intro (sound257 C) (And.intro (sound258 C) (And.intro (sound259 C) (And.intro (sound260 C) (And.intro (sound261 C) (And.intro (sound262 C) (And.intro (sound263 C) (And.intro (sound264 C) (And.intro (sound265 C) (And.intro (sound266 C) (And.intro (sound267 C) (And.intro (sound268 C) (And.intro (sound269 C) (And.intro (sound270 C) (And.intro (sound271 C) (And.intro (sound272 C) (And.intro (sound273 C) (And.intro (sound274 C) (And.intro (sound275 C) (And.intro (sound276 C) (And.intro (sound277 C) (And.intro (sound278 C) (And.intro (sound279 C) (And.intro (sound280 C) (And.intro (sound281 C) (And.intro (sound282 C) (And.intro (sound283 C) (And.intro (sound284 C) (And.intro (sound285 C) (And.intro (sound286 C) (And.intro (sound287 C) (And.intro (sound288 C) (And.intro (sound289 C) (And.intro (sound290 C) (And.intro (sound291 C) (And.intro (sound292 C) (And.intro (sound293 C) (And.intro (sound294 C) (And.intro (sound295 C) (And.intro (sound296 C) (And.intro (sound297 C) (And.intro (sound298 C) (And.intro (sound299 C) (And.intro (sound300 C) (And.intro (sound301 C) (And.intro (sound302 C) (And.intro (sound303 C) (And.intro (sound304 C) (And.intro (sound305 C) (And.intro (sound306 C) (And.intro (sound307 C) (And.intro (sound308 C) (And.intro (sound309 C) (And.intro (sound310 C) (And.intro (sound311 C) (And.intro (sound312 C) (And.intro (sound313 C) (And.intro (sound314 C) (And.intro (sound315 C) (And.intro (sound316 C) (And.intro (sound317 C) (And.intro (sound318 C) (And.intro (sound319 C) (And.intro (sound320 C) (And.intro (sound321 C) (And.intro (sound322 C) (And.intro (sound323 C) (And.intro (sound324 C) (And.intro (sound325 C) (And.intro (sound326 C) (And.intro (sound327 C) (And.intro (sound328 C) (And.intro (sound329 C) (And.intro (sound330 C) (And.intro (sound331 C) (And.intro (sound332 C) (And.intro (sound333 C) (And.intro (sound334 C) (And.intro (sound335 C) (And.intro (sound336 C) (And.intro (sound337 C) (And.intro (sound338 C) (And.intro (sound339 C) (And.intro (sound340 C) (And.intro (sound341 C) (And.intro (sound342 C) (And.intro (sound343 C) (And.intro (sound344 C) (And.intro (sound345 C) (And.intro (sound346 C) (And.intro (sound347 C) (And.intro (sound348 C) (And.intro (sound349 C) (And.intro (sound350 C) (And.intro (sound351 C) (And.intro (sound352 C) (And.intro (sound353 C) (And.intro (sound354 C) (And.intro (sound355 C) (And.intro (sound356 C) (And.intro (sound357 C) (And.intro (sound358 C) (And.intro (sound359 C) (And.intro (sound360 C) (And.intro (sound361 C) (And.intro (sound362 C) (And.intro (sound363 C) (And.intro (sound364 C) (And.intro (sound365 C) (And.intro (sound366 C) (And.intro (sound367 C) (And.intro (sound368 C) (And.intro (sound369 C) (And.intro (sound370 C) (And.intro (sound371 C) (And.intro (sound372 C) (And.intro (sound373 C) (And.intro (sound374 C) (And.intro (sound375 C) (And.intro (sound376 C) (And.intro (sound377 C) (And.intro (sound378 C) (And.intro (sound379 C) (And.intro (sound380 C) (And.intro (sound381 C) (And.intro (sound382 C) (And.intro (sound383 C) (And.intro (sound384 C) (And.intro (sound385 C) (And.intro (sound386 C) (And.intro (sound387 C) (And.intro (sound388 C) (And.intro (sound389 C) (And.intro (sound390 C) (And.intro (sound391 C) (And.intro (sound392 C) (And.intro (sound393 C) (And.intro (sound394 C) (And.intro (sound395 C) (And.intro (sound396 C) (And.intro (sound397 C) (And.intro (sound398 C) (And.intro (sound399 C) (And.intro (sound400 C) (And.intro (sound401 C) (And.intro (sound402 C) (And.intro (sound403 C) (And.intro (sound404 C) (And.intro (sound405 C) (And.intro (sound406 C) (And.intro (sound407 C) (And.intro (sound408 C) (And.intro (sound409 C) (And.intro (sound410 C) (And.intro (sound411 C) (And.intro (sound412 C) (And.intro (sound413 C) (And.intro (sound414 C) (And.intro (sound415 C) (And.intro (sound416 C) (And.intro (sound417 C) (And.intro (sound418 C) (And.intro (sound419 C) (And.intro (sound420 C) (And.intro (sound421 C) (And.intro (sound422 C) (And.intro (sound423 C) (And.intro (sound424 C) (And.intro (sound425 C) (And.intro (sound426 C) (And.intro (sound427 C) (And.intro (sound428 C) (And.intro (sound429 C) (And.intro (sound430 C) (And.intro (sound431 C) (And.intro (sound432 C) (And.intro (sound433 C) (And.intro (sound434 C) (And.intro (sound435 C) (And.intro (sound436 C) (And.intro (sound437 C) (And.intro (sound438 C) (And.intro (sound439 C) (And.intro (sound440 C) (And.intro (sound441 C) (And.intro (sound442 C) (And.intro (sound443 C) (And.intro (sound444 C) (And.intro (sound445 C) (And.intro (sound446 C) (And.intro (sound447 C) (And.intro (sound448 C) (And.intro (sound449 C) (And.intro (sound450 C) (And.intro (sound451 C) (And.intro (sound452 C) (And.intro (sound453 C) (And.intro (sound454 C) (And.intro (sound455 C) (And.intro (sound456 C) (And.intro (sound457 C) (And.intro (sound458 C) (And.intro (sound459 C) (And.intro (sound460 C) (And.intro (sound461 C) (And.intro (sound462 C) (And.intro (sound463 C) (And.intro (sound464 C) (And.intro (sound465 C) (And.intro (sound466 C) (And.intro (sound467 C) (And.intro (sound468 C) (And.intro (sound469 C) (And.intro (sound470 C) (And.intro (sound471 C) (And.intro (sound472 C) (And.intro (sound473 C) (And.intro (sound474 C) (And.intro (sound475 C) (And.intro (sound476 C) (And.intro (sound477 C) (And.intro (sound478 C) (And.intro (sound479 C) (And.intro (sound480 C) (And.intro (sound481 C) (And.intro (sound482 C) (And.intro (sound483 C) (And.intro (sound484 C) (And.intro (sound485 C) (And.intro (sound486 C) (And.intro (sound487 C) (And.intro (sound488 C) (And.intro (sound489 C) (And.intro (sound490 C) (And.intro (sound491 C) (And.intro (sound492 C) (And.intro (sound493 C) (And.intro (sound494 C) (And.intro (sound495 C) (And.intro (sound496 C) (And.intro (sound497 C) (And.intro (sound498 C) (And.intro (sound499 C) (And.intro (sound500 C) (And.intro (sound501 C) (And.intro (sound502 C) (And.intro (sound503 C) (And.intro (sound504 C) (And.intro (sound505 C) (And.intro (sound506 C) (And.intro (sound507 C) (And.intro (sound508 C) (And.intro (sound509 C) (And.intro (sound510 C) (And.intro (sound511 C) (And.intro (sound512 C) (And.intro (sound513 C) (And.intro (sound514 C) (And.intro (sound515 C) (And.intro (sound516 C) (And.intro (sound517 C) (And.intro (sound518 C) (And.intro (sound519 C) (And.intro (sound520 C) (And.intro (sound521 C) (And.intro (sound522 C) (And.intro (sound523 C) (And.intro (sound524 C) (And.intro (sound525 C) (And.intro (sound526 C) (And.intro (sound527 C) (And.intro (sound528 C) (And.intro (sound529 C) (And.intro (sound530 C) (And.intro (sound531 C) (And.intro (sound532 C) (And.intro (sound533 C) (And.intro (sound534 C) (And.intro (sound535 C) (And.intro (sound536 C) (And.intro (sound537 C) (And.intro (sound538 C) (And.intro (sound539 C) (And.intro (sound540 C) (And.intro (sound541 C) (And.intro (sound542 C) (And.intro (sound543 C) (And.intro (sound544 C) (And.intro (sound545 C) (And.intro (sound546 C) (And.intro (sound547 C) (And.intro (sound548 C) (And.intro (sound549 C) (And.intro (sound550 C) (And.intro (sound551 C) (And.intro (sound552 C) (And.intro (sound553 C) (And.intro (sound554 C) (And.intro (sound555 C) (And.intro (sound556 C) (And.intro (sound557 C) (And.intro (sound558 C) (And.intro (sound559 C) (And.intro (sound560 C) (And.intro (sound561 C) (And.intro (sound562 C) (And.intro (sound563 C) (And.intro (sound564 C) (And.intro (sound565 C) (And.intro (sound566 C) (And.intro (sound567 C) (And.intro (sound568 C) (And.intro (sound569 C) (And.intro (sound570 C) (And.intro (sound571 C) (And.intro (sound572 C) (And.intro (sound573 C) (And.intro (sound574 C) (And.intro (sound575 C) (And.intro (sound576 C) (sound577 C)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

theorem context_impossible (C : Context 13 n states) : False := by
  have h : (C.valuation atoms).satisfies_fmla cnf_refutation.formula := by
    rw [formula_eq]
    constructor
    intro cl hc
    exact C.satisfies_of_clause atoms cl ((List.forall_iff_forall_mem.mp (all_sound C)) cl hc)
  exact cnf_refutation (C.valuation atoms) h

#print axioms context_impossible
end ErdosSzekeres.Omission.CoupledCoreThird
