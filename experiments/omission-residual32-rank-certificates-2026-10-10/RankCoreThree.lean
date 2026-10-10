import ErdosSzekeres.Omission.CoupledLrat
import ErdosSzekeres.Omission.CoupledSemantics

namespace ErdosSzekeres.Omission.CoupledCoreRankSearchThree
open Coupled
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

lrat_raw cnf_refutation
  (include_str "core-three.cnf")
  (include_str "core-three.lrat")

def support : List (Fin 154) := [33, 43, 53, 65, 75, 77, 87, 89, 91, 99, 110, 111, 118]

def states : Fin 13 → Fin 154 := support.get

def atoms : List (Atom 13) := [
  .before 0 1,
  .capGe 0 1 2,
  .capGe 0 1 3,
  .capGe 0 1 4,
  .cupGe 0 1 2,
  .before 0 2,
  .before 0 3,
  .before 0 4,
  .before 0 5,
  .before 0 6,
  .before 0 7,
  .before 0 8,
  .before 0 9,
  .before 0 10,
  .capGe 0 10 2,
  .capGe 0 10 3,
  .capGe 0 10 4,
  .cupGe 0 10 2,
  .before 0 11,
  .before 1 2,
  .cupGe 1 2 2,
  .cupGe 1 2 3,
  .before 1 3,
  .before 1 4,
  .before 1 5,
  .before 1 6,
  .before 1 7,
  .before 1 8,
  .before 1 9,
  .before 1 10,
  .cupGe 1 10 2,
  .before 1 11,
  .before 2 3,
  .cupGe 2 3 3,
  .cupGe 2 3 4,
  .before 2 5,
  .before 2 7,
  .before 2 8,
  .before 2 10,
  .before 2 11,
  .before 3 4,
  .before 3 5,
  .cupGe 3 5 4,
  .cupGe 3 5 5,
  .before 3 7,
  .before 3 8,
  .before 3 9,
  .before 3 10,
  .before 3 11,
  .before 4 6,
  .before 4 8,
  .before 4 9,
  .before 4 10,
  .before 4 11,
  .before 4 12,
  .before 5 6,
  .before 5 7,
  .cupGe 5 7 5,
  .cupGe 5 7 6,
  .before 5 10,
  .cupGe 5 10 5,
  .before 5 11,
  .before 6 8,
  .before 6 9,
  .before 6 10,
  .before 6 11,
  .before 7 9,
  .cupGe 7 9 6,
  .before 7 10,
  .capGe 7 10 2,
  .cupGe 7 10 6,
  .before 7 11,
  .capGe 7 11 2,
  .capGe 7 11 3,
  .capGe 7 11 4,
  .cupGe 7 11 2,
  .cupGe 7 11 3,
  .cupGe 7 11 4,
  .cupGe 7 11 5,
  .before 8 9,
  .before 8 10,
  .capGe 8 10 2,
  .capGe 8 10 3,
  .cupGe 8 10 2,
  .before 8 11,
  .before 9 10,
  .capGe 9 10 4,
  .cupGe 9 10 2,
  .cupGe 9 10 3,
  .cupGe 9 10 4,
  .cupGe 9 10 5,
  .cupGe 9 10 6,
  .before 9 11,
  .before 9 12,
  .before 10 11,
  .capGe 10 11 3,
  .capGe 10 11 4,
  .cupGe 10 11 3,
  .cupGe 10 11 4,
  .cupGe 10 11 5,
  .cupGe 10 11 6,
  .before 10 12,
  .before 11 12,
  .positive 0 1 2,
  .positive 0 1 3,
  .positive 0 1 4,
  .positive 0 1 5,
  .positive 0 1 6,
  .positive 0 1 7,
  .positive 0 1 8,
  .positive 0 1 9,
  .positive 0 1 10,
  .positive 0 1 11,
  .positive 0 1 12,
  .positive 0 2 3,
  .positive 0 2 5,
  .positive 0 2 7,
  .positive 0 2 8,
  .positive 0 2 10,
  .positive 0 3 5,
  .positive 0 3 7,
  .positive 0 3 8,
  .positive 0 3 10,
  .positive 0 3 11,
  .positive 0 4 6,
  .positive 0 4 8,
  .positive 0 4 9,
  .positive 0 4 10,
  .positive 0 4 11,
  .positive 0 4 12,
  .positive 0 5 7,
  .positive 0 5 8,
  .positive 0 5 10,
  .positive 0 5 11,
  .positive 0 6 8,
  .positive 0 6 9,
  .positive 0 6 10,
  .positive 0 6 11,
  .positive 0 6 12,
  .positive 0 7 8,
  .positive 0 7 10,
  .positive 0 8 9,
  .positive 0 8 10,
  .positive 0 8 11,
  .positive 0 8 12,
  .positive 0 9 10,
  .positive 0 9 11,
  .positive 0 9 12,
  .positive 0 10 11,
  .positive 0 10 12,
  .positive 0 11 12,
  .positive 1 2 3,
  .positive 1 2 5,
  .positive 1 2 7,
  .positive 1 2 8,
  .positive 1 2 10,
  .positive 1 2 11,
  .positive 1 3 4,
  .positive 1 3 5,
  .positive 1 3 7,
  .positive 1 3 8,
  .positive 1 3 10,
  .positive 1 3 11,
  .positive 1 4 6,
  .positive 1 4 8,
  .positive 1 4 9,
  .positive 1 4 10,
  .positive 1 4 11,
  .positive 1 4 12,
  .positive 1 5 6,
  .positive 1 5 7,
  .positive 1 5 8,
  .positive 1 5 10,
  .positive 1 5 11,
  .positive 1 6 8,
  .positive 1 6 9,
  .positive 1 6 10,
  .positive 1 6 11,
  .positive 1 6 12,
  .positive 1 7 8,
  .positive 1 7 10,
  .positive 1 7 11,
  .positive 1 8 9,
  .positive 1 8 10,
  .positive 1 8 11,
  .positive 1 8 12,
  .positive 1 9 10,
  .positive 1 9 11,
  .positive 1 9 12,
  .positive 1 10 11,
  .positive 1 10 12,
  .positive 1 11 12,
  .positive 2 3 4,
  .positive 2 3 5,
  .positive 2 3 7,
  .positive 2 3 8,
  .positive 2 3 9,
  .positive 2 3 10,
  .positive 2 3 11,
  .positive 2 4 11,
  .positive 2 5 6,
  .positive 2 5 7,
  .positive 2 5 8,
  .positive 2 5 10,
  .positive 2 5 11,
  .positive 2 6 11,
  .positive 2 7 8,
  .positive 2 7 10,
  .positive 2 7 11,
  .positive 2 8 10,
  .positive 2 8 11,
  .positive 2 9 10,
  .positive 2 9 11,
  .positive 2 10 11,
  .positive 2 10 12,
  .positive 2 11 12,
  .positive 3 4 11,
  .positive 3 5 6,
  .positive 3 5 7,
  .positive 3 5 8,
  .positive 3 5 10,
  .positive 3 5 11,
  .positive 3 6 11,
  .positive 3 7 8,
  .positive 3 7 9,
  .positive 3 7 10,
  .positive 3 7 11,
  .positive 3 8 10,
  .positive 3 8 11,
  .positive 3 9 11,
  .positive 3 10 11,
  .positive 3 10 12,
  .positive 3 11 12,
  .positive 4 6 8,
  .positive 4 6 9,
  .positive 4 6 10,
  .positive 4 6 11,
  .positive 4 6 12,
  .positive 4 8 9,
  .positive 4 8 11,
  .positive 4 8 12,
  .positive 4 9 10,
  .positive 4 9 11,
  .positive 4 9 12,
  .positive 4 10 11,
  .positive 4 10 12,
  .positive 4 11 12,
  .positive 5 6 10,
  .positive 5 6 11,
  .positive 5 7 8,
  .positive 5 7 9,
  .positive 5 7 10,
  .positive 5 7 11,
  .positive 5 8 10,
  .positive 5 8 11,
  .positive 5 9 11,
  .positive 5 10 11,
  .positive 5 10 12,
  .positive 5 11 12,
  .positive 6 8 9,
  .positive 6 8 10,
  .positive 6 8 11,
  .positive 6 8 12,
  .positive 6 9 10,
  .positive 6 9 11,
  .positive 6 9 12,
  .positive 6 10 11,
  .positive 6 10 12,
  .positive 6 11 12,
  .positive 7 8 10,
  .positive 7 8 11,
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
  .convex 0 1 2 5,
  .convex 0 1 2 7,
  .convex 0 1 2 8,
  .convex 0 1 2 10,
  .convex 0 1 3 5,
  .convex 0 1 3 7,
  .convex 0 1 3 8,
  .convex 0 1 3 10,
  .convex 0 1 4 6,
  .convex 0 1 4 8,
  .convex 0 1 4 9,
  .convex 0 1 4 10,
  .convex 0 1 4 11,
  .convex 0 1 4 12,
  .convex 0 1 5 7,
  .convex 0 1 5 8,
  .convex 0 1 5 10,
  .convex 0 1 6 8,
  .convex 0 1 6 9,
  .convex 0 1 6 10,
  .convex 0 1 6 11,
  .convex 0 1 6 12,
  .convex 0 1 7 8,
  .convex 0 1 7 10,
  .convex 0 1 8 9,
  .convex 0 1 8 10,
  .convex 0 1 8 11,
  .convex 0 1 8 12,
  .convex 0 1 9 10,
  .convex 0 1 9 11,
  .convex 0 1 9 12,
  .convex 0 1 10 11,
  .convex 0 1 10 12,
  .convex 0 1 11 12,
  .convex 0 2 3 5,
  .convex 0 2 3 7,
  .convex 0 2 3 8,
  .convex 0 2 3 10,
  .convex 0 2 5 7,
  .convex 0 2 5 8,
  .convex 0 2 5 10,
  .convex 0 2 7 8,
  .convex 0 2 7 10,
  .convex 0 2 8 10,
  .convex 0 3 5 7,
  .convex 0 3 5 8,
  .convex 0 3 5 10,
  .convex 0 3 7 8,
  .convex 0 3 7 10,
  .convex 0 3 8 10,
  .convex 0 4 6 8,
  .convex 0 4 6 9,
  .convex 0 4 6 10,
  .convex 0 4 6 11,
  .convex 0 4 6 12,
  .convex 0 4 8 9,
  .convex 0 4 8 11,
  .convex 0 4 8 12,
  .convex 0 4 9 10,
  .convex 0 4 9 11,
  .convex 0 4 9 12,
  .convex 0 4 10 11,
  .convex 0 4 10 12,
  .convex 0 4 11 12,
  .convex 0 5 7 8,
  .convex 0 5 7 10,
  .convex 0 5 8 10,
  .convex 0 6 8 9,
  .convex 0 6 8 11,
  .convex 0 6 8 12,
  .convex 0 6 9 10,
  .convex 0 6 9 11,
  .convex 0 6 9 12,
  .convex 0 6 10 11,
  .convex 0 6 10 12,
  .convex 0 6 11 12,
  .convex 0 7 8 10,
  .convex 0 8 9 11,
  .convex 0 8 9 12,
  .convex 0 8 11 12,
  .convex 0 9 10 11,
  .convex 0 9 10 12,
  .convex 0 9 11 12,
  .convex 0 10 11 12,
  .convex 1 2 3 5,
  .convex 1 2 3 7,
  .convex 1 2 3 8,
  .convex 1 2 3 10,
  .convex 1 2 3 11,
  .convex 1 2 5 7,
  .convex 1 2 5 8,
  .convex 1 2 5 10,
  .convex 1 2 5 11,
  .convex 1 2 7 8,
  .convex 1 2 7 10,
  .convex 1 2 7 11,
  .convex 1 2 8 10,
  .convex 1 2 8 11,
  .convex 1 2 10 11,
  .convex 1 3 5 7,
  .convex 1 3 5 8,
  .convex 1 3 5 10,
  .convex 1 3 5 11,
  .convex 1 3 7 8,
  .convex 1 3 7 10,
  .convex 1 3 7 11,
  .convex 1 3 8 10,
  .convex 1 3 8 11,
  .convex 1 3 10 11,
  .convex 1 4 6 8,
  .convex 1 4 6 9,
  .convex 1 4 6 10,
  .convex 1 4 6 11,
  .convex 1 4 6 12,
  .convex 1 4 8 9,
  .convex 1 4 8 11,
  .convex 1 4 8 12,
  .convex 1 4 9 10,
  .convex 1 4 9 11,
  .convex 1 4 9 12,
  .convex 1 4 10 11,
  .convex 1 4 10 12,
  .convex 1 4 11 12,
  .convex 1 5 7 8,
  .convex 1 5 7 10,
  .convex 1 5 7 11,
  .convex 1 5 8 10,
  .convex 1 5 8 11,
  .convex 1 5 10 11,
  .convex 1 6 8 9,
  .convex 1 6 8 11,
  .convex 1 6 8 12,
  .convex 1 6 9 10,
  .convex 1 6 9 11,
  .convex 1 6 9 12,
  .convex 1 6 10 11,
  .convex 1 6 10 12,
  .convex 1 6 11 12,
  .convex 1 7 8 10,
  .convex 1 7 8 11,
  .convex 1 7 10 11,
  .convex 1 8 9 11,
  .convex 1 8 9 12,
  .convex 1 8 10 11,
  .convex 1 8 11 12,
  .convex 1 9 10 11,
  .convex 1 9 10 12,
  .convex 1 9 11 12,
  .convex 1 10 11 12,
  .convex 2 3 5 7,
  .convex 2 3 5 8,
  .convex 2 3 5 10,
  .convex 2 3 5 11,
  .convex 2 3 7 8,
  .convex 2 3 7 10,
  .convex 2 3 7 11,
  .convex 2 3 8 10,
  .convex 2 3 8 11,
  .convex 2 3 10 11,
  .convex 2 5 7 8,
  .convex 2 5 7 10,
  .convex 2 5 7 11,
  .convex 2 5 8 10,
  .convex 2 5 8 11,
  .convex 2 5 10 11,
  .convex 2 7 8 10,
  .convex 2 7 8 11,
  .convex 2 7 10 11,
  .convex 2 8 10 11,
  .convex 3 5 7 8,
  .convex 3 5 7 10,
  .convex 3 5 7 11,
  .convex 3 5 8 10,
  .convex 3 5 8 11,
  .convex 3 5 10 11,
  .convex 3 7 8 10,
  .convex 3 7 8 11,
  .convex 3 7 10 11,
  .convex 3 8 10 11,
  .convex 4 6 8 9,
  .convex 4 6 8 11,
  .convex 4 6 8 12,
  .convex 4 6 9 10,
  .convex 4 6 9 11,
  .convex 4 6 9 12,
  .convex 4 6 10 11,
  .convex 4 6 10 12,
  .convex 4 6 11 12,
  .convex 4 8 9 11,
  .convex 4 8 9 12,
  .convex 4 8 11 12,
  .convex 4 9 10 11,
  .convex 4 9 10 12,
  .convex 4 9 11 12,
  .convex 4 10 11 12,
  .convex 5 7 8 10,
  .convex 5 7 8 11,
  .convex 5 7 10 11,
  .convex 5 8 10 11,
  .convex 6 8 9 11,
  .convex 6 8 9 12,
  .convex 6 8 11 12,
  .convex 6 9 10 11,
  .convex 6 9 10 12,
  .convex 6 9 11 12,
  .convex 6 10 11 12,
  .convex 7 8 10 11,
  .convex 8 9 11 12,
  .convex 9 10 11 12]

private def clause000 : Sat.Clause := [.neg 0, .pos 1, .pos 4]
private def clause001 : Sat.Clause := [.neg 0, .neg 1, .pos 2, .pos 4]
private def clause002 : Sat.Clause := [.neg 0, .neg 2, .pos 3, .pos 4]
private def clause003 : Sat.Clause := [.pos 0]
private def clause004 : Sat.Clause := [.pos 5]
private def clause005 : Sat.Clause := [.pos 6]
private def clause006 : Sat.Clause := [.pos 7]
private def clause007 : Sat.Clause := [.pos 8]
private def clause008 : Sat.Clause := [.pos 9]
private def clause009 : Sat.Clause := [.pos 10]
private def clause010 : Sat.Clause := [.pos 12]
private def clause011 : Sat.Clause := [.neg 13, .pos 14, .pos 17]
private def clause012 : Sat.Clause := [.neg 13, .neg 14, .pos 15, .pos 17]
private def clause013 : Sat.Clause := [.neg 13, .neg 15, .pos 16, .pos 17]
private def clause014 : Sat.Clause := [.pos 13]
private def clause015 : Sat.Clause := [.pos 18]
private def clause016 : Sat.Clause := [.pos 19]
private def clause017 : Sat.Clause := [.pos 22]
private def clause018 : Sat.Clause := [.pos 23]
private def clause019 : Sat.Clause := [.pos 24]
private def clause020 : Sat.Clause := [.pos 25]
private def clause021 : Sat.Clause := [.pos 26]
private def clause022 : Sat.Clause := [.pos 28]
private def clause023 : Sat.Clause := [.pos 29]
private def clause024 : Sat.Clause := [.pos 32]
private def clause025 : Sat.Clause := [.pos 35]
private def clause026 : Sat.Clause := [.pos 36]
private def clause027 : Sat.Clause := [.pos 38]
private def clause028 : Sat.Clause := [.pos 40]
private def clause029 : Sat.Clause := [.pos 41]
private def clause030 : Sat.Clause := [.pos 44]
private def clause031 : Sat.Clause := [.pos 46]
private def clause032 : Sat.Clause := [.pos 47]
private def clause033 : Sat.Clause := [.pos 49]
private def clause034 : Sat.Clause := [.pos 51]
private def clause035 : Sat.Clause := [.pos 54]
private def clause036 : Sat.Clause := [.pos 55]
private def clause037 : Sat.Clause := [.pos 56]
private def clause038 : Sat.Clause := [.pos 59]
private def clause039 : Sat.Clause := [.pos 63]
private def clause040 : Sat.Clause := [.pos 66]
private def clause041 : Sat.Clause := [.neg 68, .pos 69, .neg 70]
private def clause042 : Sat.Clause := [.pos 68]
private def clause043 : Sat.Clause := [.pos 71, .neg 72, .pos 73, .pos 75]
private def clause044 : Sat.Clause := [.pos 71, .neg 72, .pos 73, .neg 75, .pos 76]
private def clause045 : Sat.Clause := [.pos 71, .neg 72, .pos 73, .neg 76, .pos 77]
private def clause046 : Sat.Clause := [.pos 71, .neg 72, .pos 73, .neg 77, .pos 78]
private def clause047 : Sat.Clause := [.pos 71, .neg 73, .pos 74, .pos 75]
private def clause048 : Sat.Clause := [.pos 71, .neg 73, .pos 74, .neg 75, .pos 76]
private def clause049 : Sat.Clause := [.pos 71, .neg 73, .pos 74, .neg 76, .pos 77]
private def clause050 : Sat.Clause := [.pos 71, .neg 73, .pos 74, .neg 77, .pos 78]
private def clause051 : Sat.Clause := [.pos 71, .neg 74, .neg 75, .pos 76]
private def clause052 : Sat.Clause := [.pos 71, .neg 74, .neg 76, .pos 77]
private def clause053 : Sat.Clause := [.pos 71, .neg 74, .neg 77, .pos 78]
private def clause054 : Sat.Clause := [.neg 80, .pos 81, .pos 83]
private def clause055 : Sat.Clause := [.neg 80, .neg 81, .pos 82, .pos 83]
private def clause056 : Sat.Clause := [.pos 80]
private def clause057 : Sat.Clause := [.pos 84]
private def clause058 : Sat.Clause := [.pos 85, .neg 86, .pos 87]
private def clause059 : Sat.Clause := [.pos 85, .neg 86, .neg 87, .pos 88]
private def clause060 : Sat.Clause := [.pos 85, .neg 86, .neg 88, .pos 89]
private def clause061 : Sat.Clause := [.pos 85, .neg 86, .neg 89, .pos 90]
private def clause062 : Sat.Clause := [.pos 85, .neg 86, .neg 90, .pos 91]
private def clause063 : Sat.Clause := [.pos 93]
private def clause064 : Sat.Clause := [.neg 94, .neg 95, .pos 96, .neg 97, .pos 98]
private def clause065 : Sat.Clause := [.neg 94, .neg 95, .pos 96, .neg 98, .pos 99]
private def clause066 : Sat.Clause := [.neg 94, .neg 95, .pos 96, .neg 99, .pos 100]
private def clause067 : Sat.Clause := [.neg 94, .neg 95, .pos 96, .neg 100]
private def clause068 : Sat.Clause := [.pos 101]
private def clause069 : Sat.Clause := [.pos 102]
private def clause070 : Sat.Clause := [.neg 0, .neg 19, .pos 20, .neg 103]
private def clause071 : Sat.Clause := [.neg 0, .neg 4, .neg 19, .pos 21, .neg 103]
private def clause072 : Sat.Clause := [.neg 0, .pos 11, .neg 27]
private def clause073 : Sat.Clause := [.neg 0, .neg 3, .neg 27, .pos 109]
private def clause074 : Sat.Clause := [.neg 0, .neg 29, .pos 30, .neg 111]
private def clause075 : Sat.Clause := [.neg 5, .pos 11, .neg 37]
private def clause076 : Sat.Clause := [.neg 6, .pos 11, .neg 45]
private def clause077 : Sat.Clause := [.neg 11, .neg 80, .pos 83, .neg 142]
private def clause078 : Sat.Clause := [.pos 11, .neg 12, .pos 79]
private def clause079 : Sat.Clause := [.neg 13, .neg 17, .neg 94, .pos 97, .neg 148]
private def clause080 : Sat.Clause := [.neg 13, .neg 16, .neg 101, .pos 149]
private def clause081 : Sat.Clause := [.neg 19, .neg 20, .neg 32, .pos 33, .neg 151]
private def clause082 : Sat.Clause := [.neg 19, .neg 21, .neg 32, .pos 34, .neg 151]
private def clause083 : Sat.Clause := [.neg 25, .pos 27, .neg 62]
private def clause084 : Sat.Clause := [.pos 27, .neg 28, .pos 79]
private def clause085 : Sat.Clause := [.neg 29, .neg 30, .neg 94, .pos 97, .neg 189]
private def clause086 : Sat.Clause := [.neg 32, .neg 33, .neg 41, .pos 42, .neg 193]
private def clause087 : Sat.Clause := [.neg 32, .neg 34, .neg 41, .pos 43, .neg 193]
private def clause088 : Sat.Clause := [.neg 32, .pos 39, .neg 48]
private def clause089 : Sat.Clause := [.neg 35, .pos 39, .neg 61]
private def clause090 : Sat.Clause := [.neg 36, .pos 39, .neg 71]
private def clause091 : Sat.Clause := [.neg 39, .pos 71, .pos 75, .pos 208]
private def clause092 : Sat.Clause := [.neg 41, .neg 42, .neg 56, .pos 57, .neg 218]
private def clause093 : Sat.Clause := [.neg 41, .neg 43, .neg 56, .pos 58, .neg 218]
private def clause094 : Sat.Clause := [.neg 41, .neg 42, .neg 59, .pos 60, .neg 220]
private def clause095 : Sat.Clause := [.neg 41, .pos 48, .neg 61]
private def clause096 : Sat.Clause := [.neg 44, .pos 48, .neg 71]
private def clause097 : Sat.Clause := [.neg 49, .pos 50, .neg 62]
private def clause098 : Sat.Clause := [.pos 50, .neg 51, .pos 79]
private def clause099 : Sat.Clause := [.neg 56, .neg 57, .neg 68, .pos 70, .neg 251]
private def clause100 : Sat.Clause := [.neg 56, .neg 58, .neg 68, .neg 251]
private def clause101 : Sat.Clause := [.neg 56, .pos 61, .neg 71]
private def clause102 : Sat.Clause := [.neg 59, .neg 60, .neg 94, .pos 100, .neg 256]
private def clause103 : Sat.Clause := [.neg 62, .neg 80, .pos 83, .neg 260]
private def clause104 : Sat.Clause := [.pos 62, .neg 63, .pos 79]
private def clause105 : Sat.Clause := [.neg 63, .pos 64, .neg 85]
private def clause106 : Sat.Clause := [.neg 66, .neg 67, .neg 93, .neg 273]
private def clause107 : Sat.Clause := [.neg 68, .neg 69, .neg 94, .pos 95, .pos 274]
private def clause108 : Sat.Clause := [.neg 68, .neg 70, .neg 94, .neg 274]
private def clause109 : Sat.Clause := [.neg 68, .neg 70, .neg 101, .neg 275]
private def clause110 : Sat.Clause := [.neg 0, .pos 4, .pos 11, .neg 109]
private def clause111 : Sat.Clause := [.pos 11, .neg 13, .pos 17, .pos 142]
private def clause112 : Sat.Clause := [.neg 80, .neg 82, .pos 85, .pos 86, .neg 277]
private def clause113 : Sat.Clause := [.neg 80, .neg 83, .neg 94, .pos 97, .neg 280]
private def clause114 : Sat.Clause := [.pos 71, .pos 72, .neg 84, .pos 270]
private def clause115 : Sat.Clause := [.pos 85, .neg 91, .neg 93, .pos 284]
private def clause116 : Sat.Clause := [.neg 94, .neg 96, .neg 102, .pos 286]
private def clause117 : Sat.Clause := [.neg 66, .pos 67, .pos 71, .neg 78, .neg 272]
private def clause118 : Sat.Clause := [.pos 103]
private def clause119 : Sat.Clause := [.pos 104]
private def clause120 : Sat.Clause := [.pos 105]
private def clause121 : Sat.Clause := [.pos 106]
private def clause122 : Sat.Clause := [.pos 107]
private def clause123 : Sat.Clause := [.pos 108]
private def clause124 : Sat.Clause := [.pos 110]
private def clause125 : Sat.Clause := [.pos 111]
private def clause126 : Sat.Clause := [.pos 112]
private def clause127 : Sat.Clause := [.pos 113]
private def clause128 : Sat.Clause := [.pos 114]
private def clause129 : Sat.Clause := [.pos 115]
private def clause130 : Sat.Clause := [.pos 116]
private def clause131 : Sat.Clause := [.pos 118]
private def clause132 : Sat.Clause := [.pos 119]
private def clause133 : Sat.Clause := [.pos 120]
private def clause134 : Sat.Clause := [.pos 122]
private def clause135 : Sat.Clause := [.pos 124]
private def clause136 : Sat.Clause := [.pos 126]
private def clause137 : Sat.Clause := [.pos 128]
private def clause138 : Sat.Clause := [.pos 129]
private def clause139 : Sat.Clause := [.pos 130]
private def clause140 : Sat.Clause := [.pos 132]
private def clause141 : Sat.Clause := [.pos 135]
private def clause142 : Sat.Clause := [.pos 137]
private def clause143 : Sat.Clause := [.pos 138]
private def clause144 : Sat.Clause := [.pos 140]
private def clause145 : Sat.Clause := [.neg 143]
private def clause146 : Sat.Clause := [.pos 146]
private def clause147 : Sat.Clause := [.pos 147]
private def clause148 : Sat.Clause := [.neg 150]
private def clause149 : Sat.Clause := [.pos 151]
private def clause150 : Sat.Clause := [.pos 152]
private def clause151 : Sat.Clause := [.pos 153]
private def clause152 : Sat.Clause := [.pos 154]
private def clause153 : Sat.Clause := [.pos 155]
private def clause154 : Sat.Clause := [.neg 157]
private def clause155 : Sat.Clause := [.pos 158]
private def clause156 : Sat.Clause := [.pos 159]
private def clause157 : Sat.Clause := [.pos 160]
private def clause158 : Sat.Clause := [.pos 161]
private def clause159 : Sat.Clause := [.pos 163]
private def clause160 : Sat.Clause := [.pos 164]
private def clause161 : Sat.Clause := [.pos 165]
private def clause162 : Sat.Clause := [.pos 166]
private def clause163 : Sat.Clause := [.pos 167]
private def clause164 : Sat.Clause := [.pos 168]
private def clause165 : Sat.Clause := [.neg 169]
private def clause166 : Sat.Clause := [.pos 170]
private def clause167 : Sat.Clause := [.pos 171]
private def clause168 : Sat.Clause := [.pos 172]
private def clause169 : Sat.Clause := [.pos 174]
private def clause170 : Sat.Clause := [.pos 175]
private def clause171 : Sat.Clause := [.pos 176]
private def clause172 : Sat.Clause := [.pos 177]
private def clause173 : Sat.Clause := [.pos 178]
private def clause174 : Sat.Clause := [.pos 179]
private def clause175 : Sat.Clause := [.pos 180]
private def clause176 : Sat.Clause := [.neg 182]
private def clause177 : Sat.Clause := [.neg 183]
private def clause178 : Sat.Clause := [.neg 184]
private def clause179 : Sat.Clause := [.neg 185]
private def clause180 : Sat.Clause := [.pos 186]
private def clause181 : Sat.Clause := [.pos 187]
private def clause182 : Sat.Clause := [.pos 188]
private def clause183 : Sat.Clause := [.neg 190]
private def clause184 : Sat.Clause := [.neg 191]
private def clause185 : Sat.Clause := [.neg 192]
private def clause186 : Sat.Clause := [.pos 193]
private def clause187 : Sat.Clause := [.pos 194]
private def clause188 : Sat.Clause := [.pos 195]
private def clause189 : Sat.Clause := [.pos 197]
private def clause190 : Sat.Clause := [.pos 199]
private def clause191 : Sat.Clause := [.neg 200]
private def clause192 : Sat.Clause := [.pos 201]
private def clause193 : Sat.Clause := [.pos 202]
private def clause194 : Sat.Clause := [.pos 203]
private def clause195 : Sat.Clause := [.pos 205]
private def clause196 : Sat.Clause := [.pos 206]
private def clause197 : Sat.Clause := [.pos 207]
private def clause198 : Sat.Clause := [.neg 209]
private def clause199 : Sat.Clause := [.neg 210]
private def clause200 : Sat.Clause := [.pos 211]
private def clause201 : Sat.Clause := [.pos 212]
private def clause202 : Sat.Clause := [.neg 214]
private def clause203 : Sat.Clause := [.neg 215]
private def clause204 : Sat.Clause := [.pos 216]
private def clause205 : Sat.Clause := [.neg 217]
private def clause206 : Sat.Clause := [.pos 218]
private def clause207 : Sat.Clause := [.pos 219]
private def clause208 : Sat.Clause := [.pos 220]
private def clause209 : Sat.Clause := [.pos 222]
private def clause210 : Sat.Clause := [.pos 223]
private def clause211 : Sat.Clause := [.neg 224]
private def clause212 : Sat.Clause := [.pos 225]
private def clause213 : Sat.Clause := [.neg 227]
private def clause214 : Sat.Clause := [.neg 228]
private def clause215 : Sat.Clause := [.pos 229]
private def clause216 : Sat.Clause := [.neg 231]
private def clause217 : Sat.Clause := [.neg 232]
private def clause218 : Sat.Clause := [.pos 233]
private def clause219 : Sat.Clause := [.pos 234]
private def clause220 : Sat.Clause := [.pos 235]
private def clause221 : Sat.Clause := [.pos 236]
private def clause222 : Sat.Clause := [.pos 237]
private def clause223 : Sat.Clause := [.neg 238]
private def clause224 : Sat.Clause := [.neg 239]
private def clause225 : Sat.Clause := [.neg 240]
private def clause226 : Sat.Clause := [.pos 241]
private def clause227 : Sat.Clause := [.pos 242]
private def clause228 : Sat.Clause := [.pos 243]
private def clause229 : Sat.Clause := [.neg 245]
private def clause230 : Sat.Clause := [.neg 246]
private def clause231 : Sat.Clause := [.pos 247]
private def clause232 : Sat.Clause := [.pos 248]
private def clause233 : Sat.Clause := [.pos 249]
private def clause234 : Sat.Clause := [.neg 250]
private def clause235 : Sat.Clause := [.pos 251]
private def clause236 : Sat.Clause := [.neg 253]
private def clause237 : Sat.Clause := [.neg 254]
private def clause238 : Sat.Clause := [.pos 255]
private def clause239 : Sat.Clause := [.neg 257]
private def clause240 : Sat.Clause := [.neg 258]
private def clause241 : Sat.Clause := [.neg 259]
private def clause242 : Sat.Clause := [.neg 261]
private def clause243 : Sat.Clause := [.neg 262]
private def clause244 : Sat.Clause := [.pos 263]
private def clause245 : Sat.Clause := [.pos 264]
private def clause246 : Sat.Clause := [.pos 265]
private def clause247 : Sat.Clause := [.neg 267]
private def clause248 : Sat.Clause := [.neg 268]
private def clause249 : Sat.Clause := [.neg 269]
private def clause250 : Sat.Clause := [.neg 270]
private def clause251 : Sat.Clause := [.pos 271]
private def clause252 : Sat.Clause := [.pos 272]
private def clause253 : Sat.Clause := [.pos 273]
private def clause254 : Sat.Clause := [.neg 276]
private def clause255 : Sat.Clause := [.pos 278]
private def clause256 : Sat.Clause := [.pos 279]
private def clause257 : Sat.Clause := [.pos 280]
private def clause258 : Sat.Clause := [.pos 281]
private def clause259 : Sat.Clause := [.neg 282]
private def clause260 : Sat.Clause := [.neg 284]
private def clause261 : Sat.Clause := [.neg 285]
private def clause262 : Sat.Clause := [.neg 286]
private def clause263 : Sat.Clause := [.neg 103, .neg 104, .neg 114, .neg 151, .pos 287]
private def clause264 : Sat.Clause := [.neg 103, .neg 106, .neg 115, .neg 152, .pos 288]
private def clause265 : Sat.Clause := [.neg 103, .neg 108, .neg 116, .neg 153, .pos 289]
private def clause266 : Sat.Clause := [.neg 103, .pos 109, .pos 117, .neg 154, .pos 290]
private def clause267 : Sat.Clause := [.neg 103, .neg 111, .neg 118, .neg 155, .pos 291]
private def clause268 : Sat.Clause := [.neg 104, .neg 106, .neg 119, .neg 158, .pos 292]
private def clause269 : Sat.Clause := [.neg 104, .neg 108, .neg 120, .neg 159, .pos 293]
private def clause270 : Sat.Clause := [.neg 104, .pos 109, .pos 121, .neg 160, .pos 294]
private def clause271 : Sat.Clause := [.neg 104, .neg 111, .neg 122, .neg 161, .pos 295]
private def clause272 : Sat.Clause := [.neg 105, .neg 107, .neg 124, .neg 163, .pos 296]
private def clause273 : Sat.Clause := [.neg 0, .neg 23, .neg 50, .neg 105, .neg 109, .pos 125, .neg 164]
private def clause274 : Sat.Clause := [.neg 11, .neg 23, .pos 27, .neg 105, .pos 109, .neg 125, .neg 164]
private def clause275 : Sat.Clause := [.neg 105, .neg 109, .neg 125, .neg 164, .pos 297]
private def clause276 : Sat.Clause := [.neg 105, .neg 110, .neg 126, .neg 165, .pos 298]
private def clause277 : Sat.Clause := [.neg 0, .neg 23, .neg 52, .neg 105, .neg 111, .pos 127, .neg 166]
private def clause278 : Sat.Clause := [.neg 105, .neg 111, .neg 127, .neg 166, .pos 299]
private def clause279 : Sat.Clause := [.neg 105, .neg 112, .neg 128, .neg 167, .pos 300]
private def clause280 : Sat.Clause := [.neg 105, .neg 113, .neg 129, .neg 168, .pos 301]
private def clause281 : Sat.Clause := [.neg 106, .neg 108, .neg 130, .neg 170, .pos 302]
private def clause282 : Sat.Clause := [.neg 106, .pos 109, .pos 131, .neg 171, .pos 303]
private def clause283 : Sat.Clause := [.neg 106, .neg 111, .neg 132, .neg 172, .pos 304]
private def clause284 : Sat.Clause := [.neg 107, .neg 109, .neg 134, .neg 174, .pos 305]
private def clause285 : Sat.Clause := [.neg 107, .neg 110, .neg 135, .neg 175, .pos 306]
private def clause286 : Sat.Clause := [.neg 0, .neg 25, .neg 64, .neg 107, .neg 111, .pos 136, .neg 176]
private def clause287 : Sat.Clause := [.neg 107, .neg 111, .neg 136, .neg 176, .pos 307]
private def clause288 : Sat.Clause := [.neg 107, .neg 112, .neg 137, .neg 177, .pos 308]
private def clause289 : Sat.Clause := [.neg 107, .neg 113, .neg 138, .neg 178, .pos 309]
private def clause290 : Sat.Clause := [.neg 108, .pos 109, .pos 139, .neg 179, .pos 310]
private def clause291 : Sat.Clause := [.neg 108, .neg 111, .neg 140, .neg 180, .pos 311]
private def clause292 : Sat.Clause := [.neg 109, .neg 110, .pos 141, .pos 182, .pos 312]
private def clause293 : Sat.Clause := [.pos 109, .neg 111, .neg 142, .pos 183, .pos 313]
private def clause294 : Sat.Clause := [.neg 109, .neg 112, .pos 143, .pos 184, .pos 314]
private def clause295 : Sat.Clause := [.neg 109, .neg 113, .pos 144, .pos 185, .pos 315]
private def clause296 : Sat.Clause := [.neg 0, .neg 28, .neg 85, .neg 110, .neg 111, .pos 145, .neg 186]
private def clause297 : Sat.Clause := [.neg 110, .neg 111, .neg 145, .neg 186, .pos 316]
private def clause298 : Sat.Clause := [.neg 110, .neg 112, .neg 146, .neg 187, .pos 317]
private def clause299 : Sat.Clause := [.neg 110, .neg 113, .neg 147, .neg 188, .pos 318]
private def clause300 : Sat.Clause := [.neg 111, .neg 112, .pos 148, .pos 189, .pos 319]
private def clause301 : Sat.Clause := [.neg 111, .neg 113, .pos 149, .pos 190, .pos 320]
private def clause302 : Sat.Clause := [.neg 112, .neg 113, .pos 150, .pos 191, .pos 321]
private def clause303 : Sat.Clause := [.neg 114, .neg 115, .neg 119, .neg 193, .pos 322]
private def clause304 : Sat.Clause := [.neg 114, .neg 116, .neg 120, .neg 194, .pos 323]
private def clause305 : Sat.Clause := [.neg 114, .pos 117, .pos 121, .neg 195, .pos 324]
private def clause306 : Sat.Clause := [.neg 114, .neg 118, .neg 122, .neg 197, .pos 325]
private def clause307 : Sat.Clause := [.neg 115, .neg 116, .neg 130, .neg 201, .pos 326]
private def clause308 : Sat.Clause := [.neg 115, .pos 117, .pos 131, .neg 202, .pos 327]
private def clause309 : Sat.Clause := [.neg 115, .neg 118, .neg 132, .neg 203, .pos 328]
private def clause310 : Sat.Clause := [.neg 116, .pos 117, .pos 139, .neg 206, .pos 329]
private def clause311 : Sat.Clause := [.neg 116, .neg 118, .neg 140, .neg 207, .pos 330]
private def clause312 : Sat.Clause := [.neg 5, .pos 11, .neg 38, .neg 117, .neg 118, .neg 142, .pos 209]
private def clause313 : Sat.Clause := [.pos 117, .neg 118, .neg 142, .pos 209, .pos 331]
private def clause314 : Sat.Clause := [.neg 119, .neg 120, .neg 130, .neg 218, .pos 332]
private def clause315 : Sat.Clause := [.neg 119, .pos 121, .pos 131, .neg 219, .pos 333]
private def clause316 : Sat.Clause := [.neg 119, .neg 122, .neg 132, .neg 220, .pos 334]
private def clause317 : Sat.Clause := [.neg 6, .neg 48, .pos 61, .neg 119, .neg 123, .neg 133, .pos 221]
private def clause318 : Sat.Clause := [.neg 120, .pos 121, .pos 139, .neg 223, .pos 335]
private def clause319 : Sat.Clause := [.neg 120, .neg 122, .neg 140, .neg 225, .pos 336]
private def clause320 : Sat.Clause := [.neg 6, .pos 11, .neg 47, .neg 121, .neg 122, .neg 142, .pos 227]
private def clause321 : Sat.Clause := [.pos 121, .neg 122, .neg 142, .pos 227, .pos 337]
private def clause322 : Sat.Clause := [.neg 6, .neg 48, .pos 94, .neg 122, .pos 123, .neg 148, .neg 230]
private def clause323 : Sat.Clause := [.neg 11, .neg 49, .pos 50, .neg 124, .pos 125, .neg 134, .neg 233]
private def clause324 : Sat.Clause := [.neg 124, .neg 125, .neg 134, .neg 233, .pos 338]
private def clause325 : Sat.Clause := [.neg 124, .neg 126, .neg 135, .neg 234, .pos 339]
private def clause326 : Sat.Clause := [.neg 124, .neg 127, .neg 136, .neg 235, .pos 340]
private def clause327 : Sat.Clause := [.neg 124, .neg 128, .neg 137, .neg 236, .pos 341]
private def clause328 : Sat.Clause := [.neg 124, .neg 129, .neg 138, .neg 237, .pos 342]
private def clause329 : Sat.Clause := [.neg 125, .neg 126, .pos 141, .pos 238, .pos 343]
private def clause330 : Sat.Clause := [.neg 7, .neg 50, .neg 84, .pos 125, .neg 128, .pos 143, .pos 239]
private def clause331 : Sat.Clause := [.neg 125, .neg 128, .pos 143, .pos 239, .pos 344]
private def clause332 : Sat.Clause := [.neg 125, .neg 129, .pos 144, .pos 240, .pos 345]
private def clause333 : Sat.Clause := [.neg 126, .neg 127, .neg 145, .neg 241, .pos 346]
private def clause334 : Sat.Clause := [.neg 126, .neg 128, .neg 146, .neg 242, .pos 347]
private def clause335 : Sat.Clause := [.neg 126, .neg 129, .neg 147, .neg 243, .pos 348]
private def clause336 : Sat.Clause := [.neg 7, .neg 52, .neg 94, .neg 127, .neg 128, .pos 148, .neg 244]
private def clause337 : Sat.Clause := [.neg 127, .neg 128, .pos 148, .pos 244, .pos 349]
private def clause338 : Sat.Clause := [.neg 13, .pos 52, .neg 54, .pos 127, .neg 129, .pos 149, .pos 245]
private def clause339 : Sat.Clause := [.neg 127, .neg 129, .pos 149, .pos 245, .pos 350]
private def clause340 : Sat.Clause := [.neg 128, .neg 129, .pos 150, .pos 246, .pos 351]
private def clause341 : Sat.Clause := [.neg 130, .pos 131, .pos 139, .neg 249, .pos 352]
private def clause342 : Sat.Clause := [.neg 130, .neg 132, .neg 140, .neg 251, .pos 353]
private def clause343 : Sat.Clause := [.neg 8, .pos 11, .neg 59, .neg 131, .neg 132, .neg 142, .pos 253]
private def clause344 : Sat.Clause := [.pos 131, .neg 132, .neg 142, .pos 253, .pos 354]
private def clause345 : Sat.Clause := [.neg 18, .neg 59, .pos 61, .neg 132, .pos 133, .neg 148, .neg 256]
private def clause346 : Sat.Clause := [.neg 9, .neg 62, .neg 79, .pos 134, .neg 135, .pos 141, .pos 259]
private def clause347 : Sat.Clause := [.neg 11, .pos 62, .neg 63, .pos 134, .neg 135, .pos 141, .pos 259]
private def clause348 : Sat.Clause := [.neg 134, .neg 135, .pos 141, .pos 259, .pos 355]
private def clause349 : Sat.Clause := [.neg 9, .neg 62, .neg 80, .pos 134, .neg 136, .pos 142, .pos 260]
private def clause350 : Sat.Clause := [.neg 9, .neg 62, .neg 84, .pos 134, .neg 137, .pos 143, .pos 261]
private def clause351 : Sat.Clause := [.neg 134, .neg 137, .pos 143, .pos 261, .pos 356]
private def clause352 : Sat.Clause := [.neg 134, .neg 138, .pos 144, .pos 262, .pos 357]
private def clause353 : Sat.Clause := [.neg 9, .neg 63, .neg 85, .neg 135, .pos 136, .neg 145, .neg 263]
private def clause354 : Sat.Clause := [.neg 13, .neg 63, .pos 64, .neg 135, .pos 136, .neg 145, .neg 263]
private def clause355 : Sat.Clause := [.neg 135, .neg 136, .neg 145, .neg 263, .pos 358]
private def clause356 : Sat.Clause := [.neg 135, .neg 137, .neg 146, .neg 264, .pos 359]
private def clause357 : Sat.Clause := [.neg 135, .neg 138, .neg 147, .neg 265, .pos 360]
private def clause358 : Sat.Clause := [.neg 13, .pos 64, .neg 65, .neg 136, .neg 137, .pos 148, .neg 266]
private def clause359 : Sat.Clause := [.neg 13, .pos 64, .neg 65, .pos 136, .neg 137, .pos 148, .neg 266]
private def clause360 : Sat.Clause := [.neg 136, .neg 137, .pos 148, .pos 266, .pos 361]
private def clause361 : Sat.Clause := [.neg 136, .neg 138, .pos 149, .pos 267, .pos 362]
private def clause362 : Sat.Clause := [.neg 137, .neg 138, .pos 150, .pos 268, .pos 363]
private def clause363 : Sat.Clause := [.neg 10, .pos 11, .neg 68, .neg 139, .neg 140, .neg 142, .pos 269]
private def clause364 : Sat.Clause := [.pos 139, .neg 140, .neg 142, .pos 269, .pos 364]
private def clause365 : Sat.Clause := [.neg 12, .pos 79, .neg 80, .neg 141, .pos 142, .neg 145, .neg 277]
private def clause366 : Sat.Clause := [.neg 12, .pos 79, .neg 84, .neg 141, .pos 143, .neg 146, .neg 278]
private def clause367 : Sat.Clause := [.pos 141, .pos 143, .neg 146, .neg 278, .pos 365]
private def clause368 : Sat.Clause := [.neg 11, .neg 79, .neg 93, .neg 141, .pos 144, .neg 147, .neg 279]
private def clause369 : Sat.Clause := [.pos 141, .pos 144, .neg 147, .neg 279, .pos 366]
private def clause370 : Sat.Clause := [.neg 11, .neg 80, .neg 101, .neg 142, .pos 144, .neg 149, .neg 281]
private def clause371 : Sat.Clause := [.pos 11, .neg 13, .neg 101, .pos 142, .neg 144, .neg 149, .neg 281]
private def clause372 : Sat.Clause := [.neg 11, .neg 84, .neg 102, .pos 143, .neg 144, .pos 150, .pos 282]
private def clause373 : Sat.Clause := [.pos 143, .pos 144, .pos 150, .pos 282, .pos 367]
private def clause374 : Sat.Clause := [.neg 145, .neg 146, .pos 148, .pos 283, .pos 368]
private def clause375 : Sat.Clause := [.neg 13, .pos 85, .neg 93, .pos 145, .neg 147, .pos 149, .pos 284]
private def clause376 : Sat.Clause := [.neg 145, .neg 147, .pos 149, .pos 284, .pos 369]
private def clause377 : Sat.Clause := [.neg 146, .neg 147, .pos 150, .pos 285, .pos 370]
private def clause378 : Sat.Clause := [.neg 13, .neg 94, .neg 102, .pos 148, .neg 149, .pos 150, .pos 286]
private def clause379 : Sat.Clause := [.neg 18, .pos 94, .neg 101, .pos 148, .pos 149, .pos 150, .pos 286]
private def clause380 : Sat.Clause := [.neg 18, .pos 94, .neg 101, .pos 148, .neg 149, .pos 150, .pos 286]
private def clause381 : Sat.Clause := [.pos 148, .pos 149, .pos 150, .pos 286, .pos 371]
private def clause382 : Sat.Clause := [.neg 151, .neg 152, .neg 158, .neg 193, .pos 372]
private def clause383 : Sat.Clause := [.neg 151, .neg 153, .neg 159, .neg 194, .pos 373]
private def clause384 : Sat.Clause := [.neg 151, .neg 154, .neg 160, .neg 195, .pos 374]
private def clause385 : Sat.Clause := [.neg 151, .neg 155, .neg 161, .neg 197, .pos 375]
private def clause386 : Sat.Clause := [.neg 19, .neg 32, .neg 48, .neg 151, .pos 156, .pos 162, .neg 198]
private def clause387 : Sat.Clause := [.neg 19, .neg 32, .neg 48, .neg 151, .neg 156, .pos 162, .neg 198]
private def clause388 : Sat.Clause := [.neg 31, .neg 32, .pos 39, .neg 151, .pos 156, .neg 162, .neg 198]
private def clause389 : Sat.Clause := [.neg 151, .neg 156, .neg 162, .neg 198, .pos 376]
private def clause390 : Sat.Clause := [.neg 152, .neg 153, .neg 170, .neg 201, .pos 377]
private def clause391 : Sat.Clause := [.neg 152, .neg 154, .neg 171, .neg 202, .pos 378]
private def clause392 : Sat.Clause := [.neg 152, .neg 155, .neg 172, .neg 203, .pos 379]
private def clause393 : Sat.Clause := [.neg 19, .neg 35, .neg 61, .neg 152, .neg 156, .pos 173, .neg 204]
private def clause394 : Sat.Clause := [.neg 152, .neg 156, .neg 173, .neg 204, .pos 380]
private def clause395 : Sat.Clause := [.neg 153, .neg 154, .neg 179, .neg 206, .pos 381]
private def clause396 : Sat.Clause := [.neg 153, .neg 155, .neg 180, .neg 207, .pos 382]
private def clause397 : Sat.Clause := [.neg 153, .neg 156, .neg 181, .neg 208, .pos 383]
private def clause398 : Sat.Clause := [.neg 154, .neg 155, .pos 183, .pos 209, .pos 384]
private def clause399 : Sat.Clause := [.neg 19, .pos 31, .neg 84, .neg 154, .pos 156, .pos 184, .pos 210]
private def clause400 : Sat.Clause := [.neg 154, .neg 156, .pos 184, .pos 210, .pos 385]
private def clause401 : Sat.Clause := [.neg 19, .neg 39, .pos 94, .neg 155, .pos 156, .neg 189, .neg 213]
private def clause402 : Sat.Clause := [.neg 155, .neg 156, .neg 189, .neg 213, .pos 386]
private def clause403 : Sat.Clause := [.neg 31, .neg 40, .pos 48, .pos 157, .pos 162, .neg 167, .neg 216]
private def clause404 : Sat.Clause := [.neg 22, .pos 31, .neg 40, .pos 157, .pos 162, .neg 167, .neg 216]
private def clause405 : Sat.Clause := [.neg 158, .neg 159, .neg 170, .neg 218, .pos 387]
private def clause406 : Sat.Clause := [.neg 158, .neg 160, .neg 171, .neg 219, .pos 388]
private def clause407 : Sat.Clause := [.neg 158, .neg 161, .neg 172, .neg 220, .pos 389]
private def clause408 : Sat.Clause := [.neg 158, .neg 162, .neg 173, .neg 221, .pos 390]
private def clause409 : Sat.Clause := [.neg 159, .neg 160, .neg 179, .neg 223, .pos 391]
private def clause410 : Sat.Clause := [.neg 159, .neg 161, .neg 180, .neg 225, .pos 392]
private def clause411 : Sat.Clause := [.neg 22, .neg 48, .pos 71, .neg 159, .pos 162, .neg 181, .neg 226]
private def clause412 : Sat.Clause := [.neg 159, .neg 162, .neg 181, .neg 226, .pos 393]
private def clause413 : Sat.Clause := [.neg 160, .neg 161, .pos 183, .pos 227, .pos 394]
private def clause414 : Sat.Clause := [.neg 160, .neg 162, .pos 184, .pos 228, .pos 395]
private def clause415 : Sat.Clause := [.neg 22, .neg 48, .pos 94, .neg 161, .pos 162, .neg 189, .neg 230]
private def clause416 : Sat.Clause := [.neg 161, .neg 162, .neg 189, .neg 230, .pos 396]
private def clause417 : Sat.Clause := [.neg 163, .neg 164, .neg 174, .neg 233, .pos 397]
private def clause418 : Sat.Clause := [.neg 163, .neg 165, .neg 175, .neg 234, .pos 398]
private def clause419 : Sat.Clause := [.neg 163, .neg 166, .neg 176, .neg 235, .pos 399]
private def clause420 : Sat.Clause := [.neg 163, .neg 167, .neg 177, .neg 236, .pos 400]
private def clause421 : Sat.Clause := [.neg 163, .neg 168, .neg 178, .neg 237, .pos 401]
private def clause422 : Sat.Clause := [.neg 164, .neg 165, .pos 182, .pos 238, .pos 402]
private def clause423 : Sat.Clause := [.neg 164, .neg 167, .pos 184, .pos 239, .pos 403]
private def clause424 : Sat.Clause := [.neg 164, .neg 168, .pos 185, .pos 240, .pos 404]
private def clause425 : Sat.Clause := [.neg 165, .neg 166, .neg 186, .neg 241, .pos 405]
private def clause426 : Sat.Clause := [.neg 165, .neg 167, .neg 187, .neg 242, .pos 406]
private def clause427 : Sat.Clause := [.neg 165, .neg 168, .neg 188, .neg 243, .pos 407]
private def clause428 : Sat.Clause := [.neg 29, .pos 52, .neg 53, .neg 166, .neg 167, .pos 189, .neg 244]
private def clause429 : Sat.Clause := [.neg 166, .neg 167, .pos 189, .pos 244, .pos 408]
private def clause430 : Sat.Clause := [.neg 166, .neg 168, .pos 190, .pos 245, .pos 409]
private def clause431 : Sat.Clause := [.neg 167, .neg 168, .pos 191, .pos 246, .pos 410]
private def clause432 : Sat.Clause := [.neg 31, .neg 55, .pos 61, .pos 169, .pos 173, .neg 177, .neg 248]
private def clause433 : Sat.Clause := [.neg 24, .pos 31, .neg 55, .pos 169, .pos 173, .neg 177, .neg 248]
private def clause434 : Sat.Clause := [.neg 170, .neg 171, .neg 179, .neg 249, .pos 411]
private def clause435 : Sat.Clause := [.neg 170, .neg 172, .neg 180, .neg 251, .pos 412]
private def clause436 : Sat.Clause := [.neg 170, .neg 173, .neg 181, .neg 252, .pos 413]
private def clause437 : Sat.Clause := [.neg 171, .neg 172, .pos 183, .pos 253, .pos 414]
private def clause438 : Sat.Clause := [.neg 171, .neg 173, .pos 184, .pos 254, .pos 415]
private def clause439 : Sat.Clause := [.neg 172, .pos 173, .neg 189, .neg 256, .neg 416]
private def clause440 : Sat.Clause := [.neg 172, .neg 173, .neg 189, .neg 256, .pos 416]
private def clause441 : Sat.Clause := [.neg 174, .neg 175, .pos 182, .pos 259, .pos 417]
private def clause442 : Sat.Clause := [.neg 174, .neg 177, .pos 184, .pos 261, .pos 418]
private def clause443 : Sat.Clause := [.neg 174, .neg 178, .pos 185, .pos 262, .pos 419]
private def clause444 : Sat.Clause := [.neg 175, .neg 176, .neg 186, .neg 263, .pos 420]
private def clause445 : Sat.Clause := [.neg 175, .neg 177, .neg 187, .neg 264, .pos 421]
private def clause446 : Sat.Clause := [.neg 175, .neg 178, .neg 188, .neg 265, .pos 422]
private def clause447 : Sat.Clause := [.neg 25, .neg 64, .neg 94, .neg 176, .neg 177, .pos 189, .neg 266]
private def clause448 : Sat.Clause := [.neg 176, .neg 177, .pos 189, .pos 266, .pos 423]
private def clause449 : Sat.Clause := [.neg 176, .neg 178, .pos 190, .pos 267, .pos 424]
private def clause450 : Sat.Clause := [.neg 177, .neg 178, .pos 191, .pos 268, .pos 425]
private def clause451 : Sat.Clause := [.neg 179, .neg 180, .pos 183, .pos 269, .pos 426]
private def clause452 : Sat.Clause := [.pos 27, .neg 31, .pos 71, .neg 179, .pos 181, .pos 184, .pos 270]
private def clause453 : Sat.Clause := [.neg 26, .pos 31, .neg 84, .neg 179, .pos 181, .pos 184, .pos 270]
private def clause454 : Sat.Clause := [.neg 179, .neg 181, .pos 184, .pos 270, .pos 427]
private def clause455 : Sat.Clause := [.neg 26, .neg 71, .pos 94, .neg 180, .pos 181, .neg 189, .neg 274]
private def clause456 : Sat.Clause := [.neg 180, .pos 181, .neg 189, .neg 274, .neg 428]
private def clause457 : Sat.Clause := [.neg 180, .neg 181, .neg 189, .neg 274, .pos 428]
private def clause458 : Sat.Clause := [.neg 28, .pos 79, .neg 80, .pos 182, .pos 183, .neg 186, .pos 277]
private def clause459 : Sat.Clause := [.pos 182, .pos 184, .neg 187, .neg 278, .pos 429]
private def clause460 : Sat.Clause := [.pos 182, .pos 185, .neg 188, .neg 279, .pos 430]
private def clause461 : Sat.Clause := [.pos 27, .neg 31, .pos 94, .pos 183, .pos 184, .pos 189, .neg 280]
private def clause462 : Sat.Clause := [.neg 29, .pos 31, .neg 84, .pos 183, .pos 184, .pos 189, .neg 280]
private def clause463 : Sat.Clause := [.pos 183, .pos 184, .neg 189, .neg 280, .pos 431]
private def clause464 : Sat.Clause := [.pos 184, .pos 185, .pos 191, .pos 282, .pos 432]
private def clause465 : Sat.Clause := [.neg 29, .pos 85, .neg 92, .neg 186, .neg 187, .pos 189, .neg 283]
private def clause466 : Sat.Clause := [.neg 29, .pos 85, .neg 92, .neg 186, .neg 187, .neg 189, .neg 283]
private def clause467 : Sat.Clause := [.neg 186, .neg 187, .pos 189, .pos 283, .pos 433]
private def clause468 : Sat.Clause := [.neg 186, .neg 188, .pos 190, .pos 284, .pos 434]
private def clause469 : Sat.Clause := [.neg 187, .neg 188, .pos 191, .pos 285, .pos 435]
private def clause470 : Sat.Clause := [.pos 189, .pos 190, .pos 191, .pos 286, .pos 436]
private def clause471 : Sat.Clause := [.neg 39, .neg 40, .pos 48, .pos 192, .pos 198, .neg 199, .neg 216]
private def clause472 : Sat.Clause := [.neg 32, .pos 39, .neg 40, .pos 192, .pos 198, .neg 199, .neg 216]
private def clause473 : Sat.Clause := [.neg 193, .neg 194, .neg 201, .neg 218, .pos 437]
private def clause474 : Sat.Clause := [.neg 193, .neg 195, .neg 202, .neg 219, .pos 438]
private def clause475 : Sat.Clause := [.neg 193, .neg 197, .neg 203, .neg 220, .pos 439]
private def clause476 : Sat.Clause := [.neg 193, .neg 198, .neg 204, .neg 221, .pos 440]
private def clause477 : Sat.Clause := [.neg 194, .neg 195, .neg 206, .neg 223, .pos 441]
private def clause478 : Sat.Clause := [.neg 194, .neg 197, .neg 207, .neg 225, .pos 442]
private def clause479 : Sat.Clause := [.neg 194, .neg 198, .neg 208, .neg 226, .pos 443]
private def clause480 : Sat.Clause := [.neg 195, .neg 197, .pos 209, .pos 227, .pos 444]
private def clause481 : Sat.Clause := [.neg 195, .neg 198, .pos 210, .pos 228, .pos 445]
private def clause482 : Sat.Clause := [.neg 39, .neg 46, .pos 48, .pos 196, .pos 198, .neg 212, .neg 229]
private def clause483 : Sat.Clause := [.neg 39, .neg 46, .pos 48, .neg 196, .pos 198, .neg 212, .neg 229]
private def clause484 : Sat.Clause := [.neg 32, .neg 48, .pos 94, .neg 197, .pos 198, .neg 213, .neg 230]
private def clause485 : Sat.Clause := [.neg 197, .neg 198, .neg 213, .neg 230, .pos 446]
private def clause486 : Sat.Clause := [.neg 39, .neg 55, .pos 61, .pos 200, .pos 204, .neg 205, .neg 248]
private def clause487 : Sat.Clause := [.neg 35, .pos 39, .neg 55, .pos 200, .pos 204, .neg 205, .neg 248]
private def clause488 : Sat.Clause := [.neg 201, .neg 202, .neg 206, .neg 249, .pos 447]
private def clause489 : Sat.Clause := [.neg 201, .neg 203, .neg 207, .neg 251, .pos 448]
private def clause490 : Sat.Clause := [.neg 201, .neg 204, .neg 208, .neg 252, .pos 449]
private def clause491 : Sat.Clause := [.neg 202, .neg 203, .pos 209, .pos 253, .pos 450]
private def clause492 : Sat.Clause := [.neg 202, .neg 204, .pos 210, .pos 254, .pos 451]
private def clause493 : Sat.Clause := [.neg 35, .neg 61, .pos 94, .neg 203, .pos 204, .neg 213, .neg 256]
private def clause494 : Sat.Clause := [.neg 203, .pos 204, .neg 213, .neg 256, .neg 452]
private def clause495 : Sat.Clause := [.neg 203, .neg 204, .neg 213, .neg 256, .pos 452]
private def clause496 : Sat.Clause := [.neg 206, .neg 207, .pos 209, .pos 269, .pos 453]
private def clause497 : Sat.Clause := [.pos 37, .neg 39, .pos 71, .neg 206, .pos 208, .pos 210, .pos 270]
private def clause498 : Sat.Clause := [.neg 36, .pos 39, .neg 84, .neg 206, .pos 208, .pos 210, .pos 270]
private def clause499 : Sat.Clause := [.neg 206, .neg 208, .pos 210, .pos 270, .pos 454]
private def clause500 : Sat.Clause := [.neg 36, .neg 71, .pos 94, .neg 207, .pos 208, .neg 213, .neg 274]
private def clause501 : Sat.Clause := [.neg 207, .neg 208, .neg 213, .neg 274, .pos 455]
private def clause502 : Sat.Clause := [.pos 37, .neg 39, .pos 94, .pos 209, .pos 210, .pos 213, .neg 280]
private def clause503 : Sat.Clause := [.neg 38, .pos 39, .neg 84, .pos 209, .pos 210, .pos 213, .neg 280]
private def clause504 : Sat.Clause := [.pos 209, .pos 210, .neg 213, .neg 280, .pos 456]
private def clause505 : Sat.Clause := [.neg 39, .pos 85, .pos 94, .neg 211, .neg 212, .pos 213, .pos 283]
private def clause506 : Sat.Clause := [.neg 39, .pos 94, .neg 101, .pos 213, .pos 214, .pos 215, .pos 286]
private def clause507 : Sat.Clause := [.neg 41, .pos 48, .neg 55, .pos 217, .pos 221, .neg 222, .neg 248]
private def clause508 : Sat.Clause := [.neg 218, .neg 219, .neg 223, .neg 249, .pos 457]
private def clause509 : Sat.Clause := [.neg 218, .neg 220, .neg 225, .neg 251, .pos 458]
private def clause510 : Sat.Clause := [.neg 41, .neg 61, .pos 71, .neg 218, .pos 221, .neg 226, .neg 252]
private def clause511 : Sat.Clause := [.neg 218, .neg 221, .neg 226, .neg 252, .pos 459]
private def clause512 : Sat.Clause := [.neg 219, .neg 220, .pos 227, .pos 253, .pos 460]
private def clause513 : Sat.Clause := [.pos 45, .neg 48, .pos 61, .neg 219, .pos 221, .pos 228, .pos 254]
private def clause514 : Sat.Clause := [.neg 219, .neg 221, .pos 228, .pos 254, .pos 461]
private def clause515 : Sat.Clause := [.neg 41, .neg 61, .pos 94, .neg 220, .pos 221, .neg 230, .neg 256]
private def clause516 : Sat.Clause := [.neg 220, .neg 221, .neg 230, .neg 256, .pos 462]
private def clause517 : Sat.Clause := [.neg 223, .neg 225, .pos 227, .pos 269, .pos 463]
private def clause518 : Sat.Clause := [.pos 45, .neg 48, .pos 71, .neg 223, .pos 226, .pos 228, .pos 270]
private def clause519 : Sat.Clause := [.neg 44, .pos 48, .neg 84, .neg 223, .pos 226, .pos 228, .pos 270]
private def clause520 : Sat.Clause := [.neg 223, .neg 226, .pos 228, .pos 270, .pos 464]
private def clause521 : Sat.Clause := [.neg 48, .neg 66, .pos 71, .pos 224, .pos 226, .neg 229, .neg 272]
private def clause522 : Sat.Clause := [.neg 44, .neg 71, .pos 94, .neg 225, .pos 226, .neg 230, .neg 274]
private def clause523 : Sat.Clause := [.neg 225, .neg 226, .neg 230, .neg 274, .pos 465]
private def clause524 : Sat.Clause := [.pos 45, .neg 48, .pos 94, .pos 227, .pos 228, .pos 230, .neg 280]
private def clause525 : Sat.Clause := [.neg 47, .pos 48, .neg 84, .pos 227, .pos 228, .pos 230, .neg 280]
private def clause526 : Sat.Clause := [.pos 227, .pos 228, .neg 230, .neg 280, .pos 466]
private def clause527 : Sat.Clause := [.neg 48, .pos 94, .neg 101, .pos 230, .pos 231, .pos 232, .pos 286]
private def clause528 : Sat.Clause := [.neg 233, .neg 234, .pos 238, .pos 259, .pos 467]
private def clause529 : Sat.Clause := [.neg 233, .neg 236, .pos 239, .pos 261, .pos 468]
private def clause530 : Sat.Clause := [.neg 233, .neg 237, .pos 240, .pos 262, .pos 469]
private def clause531 : Sat.Clause := [.neg 234, .neg 235, .neg 241, .neg 263, .pos 470]
private def clause532 : Sat.Clause := [.neg 234, .neg 236, .neg 242, .neg 264, .pos 471]
private def clause533 : Sat.Clause := [.neg 234, .neg 237, .neg 243, .neg 265, .pos 472]
private def clause534 : Sat.Clause := [.neg 49, .pos 53, .neg 94, .neg 235, .neg 236, .neg 244, .pos 266]
private def clause535 : Sat.Clause := [.neg 235, .neg 236, .pos 244, .pos 266, .pos 473]
private def clause536 : Sat.Clause := [.neg 235, .neg 237, .pos 245, .pos 267, .pos 474]
private def clause537 : Sat.Clause := [.neg 236, .neg 237, .pos 246, .pos 268, .pos 475]
private def clause538 : Sat.Clause := [.pos 238, .pos 239, .neg 242, .neg 278, .pos 476]
private def clause539 : Sat.Clause := [.pos 238, .pos 240, .neg 243, .neg 279, .pos 477]
private def clause540 : Sat.Clause := [.pos 239, .pos 240, .pos 246, .pos 282, .pos 478]
private def clause541 : Sat.Clause := [.neg 241, .neg 242, .pos 244, .pos 283, .pos 479]
private def clause542 : Sat.Clause := [.neg 241, .neg 243, .pos 245, .pos 284, .pos 480]
private def clause543 : Sat.Clause := [.neg 242, .neg 243, .pos 246, .pos 285, .pos 481]
private def clause544 : Sat.Clause := [.pos 244, .pos 245, .pos 246, .pos 286, .pos 482]
private def clause545 : Sat.Clause := [.neg 244, .pos 245, .pos 246, .pos 286, .neg 482]
private def clause546 : Sat.Clause := [.neg 55, .neg 64, .neg 94, .neg 247, .neg 248, .pos 256, .neg 266]
private def clause547 : Sat.Clause := [.neg 249, .neg 251, .pos 253, .pos 269, .pos 483]
private def clause548 : Sat.Clause := [.neg 56, .pos 61, .neg 84, .neg 249, .pos 252, .pos 254, .pos 270]
private def clause549 : Sat.Clause := [.neg 249, .neg 252, .pos 254, .pos 270, .pos 484]
private def clause550 : Sat.Clause := [.neg 61, .neg 66, .pos 71, .pos 250, .pos 252, .neg 255, .neg 272]
private def clause551 : Sat.Clause := [.neg 56, .neg 71, .pos 94, .neg 251, .pos 252, .neg 256, .neg 274]
private def clause552 : Sat.Clause := [.neg 251, .neg 252, .neg 256, .neg 274, .pos 485]
private def clause553 : Sat.Clause := [.neg 59, .pos 61, .neg 84, .pos 253, .pos 254, .pos 256, .neg 280]
private def clause554 : Sat.Clause := [.pos 253, .pos 254, .neg 256, .neg 280, .pos 486]
private def clause555 : Sat.Clause := [.neg 61, .pos 94, .neg 101, .pos 256, .pos 257, .pos 258, .pos 286]
private def clause556 : Sat.Clause := [.pos 259, .pos 261, .neg 264, .neg 278, .pos 487]
private def clause557 : Sat.Clause := [.pos 259, .pos 262, .neg 265, .neg 279, .pos 488]
private def clause558 : Sat.Clause := [.pos 261, .pos 262, .pos 268, .pos 282, .pos 489]
private def clause559 : Sat.Clause := [.neg 63, .pos 65, .neg 94, .neg 263, .neg 264, .neg 266, .pos 283]
private def clause560 : Sat.Clause := [.neg 263, .neg 264, .pos 266, .pos 283, .pos 490]
private def clause561 : Sat.Clause := [.neg 263, .neg 265, .pos 267, .pos 284, .pos 491]
private def clause562 : Sat.Clause := [.neg 264, .neg 265, .pos 268, .pos 285, .pos 492]
private def clause563 : Sat.Clause := [.pos 266, .pos 267, .pos 268, .pos 286, .pos 493]
private def clause564 : Sat.Clause := [.neg 266, .pos 267, .pos 268, .pos 286, .neg 493]
private def clause565 : Sat.Clause := [.neg 68, .pos 71, .neg 84, .pos 269, .pos 270, .pos 274, .neg 280]
private def clause566 : Sat.Clause := [.pos 269, .pos 270, .neg 274, .neg 280, .pos 494]
private def clause567 : Sat.Clause := [.neg 66, .neg 85, .neg 94, .neg 271, .neg 272, .pos 274, .neg 283]
private def clause568 : Sat.Clause := [.neg 66, .neg 92, .pos 94, .neg 271, .neg 272, .neg 274, .pos 283]
private def clause569 : Sat.Clause := [.neg 71, .pos 85, .pos 94, .neg 271, .neg 272, .pos 274, .pos 283]
private def clause570 : Sat.Clause := [.neg 71, .pos 94, .neg 101, .pos 274, .pos 275, .pos 276, .pos 286]
private def clause571 : Sat.Clause := [.neg 84, .neg 85, .pos 92, .neg 277, .neg 278, .neg 280, .pos 283]
private def clause572 : Sat.Clause := [.pos 79, .neg 84, .pos 94, .neg 277, .neg 278, .neg 280, .pos 283]
private def clause573 : Sat.Clause := [.neg 79, .neg 85, .neg 101, .pos 277, .neg 279, .neg 281, .pos 284]
private def clause574 : Sat.Clause := [.neg 278, .neg 279, .pos 282, .pos 285, .pos 495]
private def clause575 : Sat.Clause := [.pos 92, .neg 93, .neg 94, .neg 283, .pos 284, .pos 285, .pos 286]
private def clause576 : Sat.Clause := [.pos 283, .pos 284, .pos 285, .pos 286, .pos 496]
private def clause577 : Sat.Clause := [.neg 283, .pos 284, .pos 285, .pos 286, .neg 496]
private def clause578 : Sat.Clause := [.neg 287, .neg 288, .neg 289, .neg 290, .neg 291, .neg 292, .neg 293, .neg 294, .neg 295, .neg 302, .neg 303, .neg 304, .neg 310, .neg 311, .neg 313, .neg 322, .neg 323, .neg 324, .neg 325, .neg 326, .neg 327, .neg 328, .neg 329, .neg 330, .neg 331, .neg 332, .neg 333, .neg 334, .neg 335, .neg 336, .neg 337, .neg 352, .neg 353, .neg 354, .neg 364, .neg 372, .neg 373, .neg 374, .neg 375, .neg 377, .neg 378, .neg 379, .neg 381, .neg 382, .neg 384, .neg 387, .neg 388, .neg 389, .neg 391, .neg 392, .neg 394, .neg 411, .neg 412, .neg 414, .neg 426, .neg 437, .neg 438, .neg 439, .neg 441, .neg 442, .neg 444, .neg 447, .neg 448, .neg 450, .neg 453, .neg 457, .neg 458, .neg 460, .neg 463, .neg 483]
private def clause579 : Sat.Clause := [.neg 296, .neg 297, .neg 298, .neg 300, .neg 301, .neg 305, .neg 306, .neg 308, .neg 309, .neg 312, .neg 314, .neg 315, .neg 317, .neg 318, .neg 321, .neg 338, .neg 339, .neg 341, .neg 342, .neg 343, .neg 344, .neg 345, .neg 347, .neg 348, .neg 351, .neg 355, .neg 356, .neg 357, .neg 359, .neg 360, .neg 363, .neg 365, .neg 366, .neg 367, .neg 370, .neg 397, .neg 398, .neg 400, .neg 401, .neg 402, .neg 403, .neg 404, .neg 406, .neg 407, .neg 410, .neg 417, .neg 418, .neg 419, .neg 421, .neg 422, .neg 425, .neg 429, .neg 430, .neg 432, .neg 435, .neg 467, .neg 468, .neg 469, .neg 471, .neg 472, .neg 475, .neg 476, .neg 477, .neg 478, .neg 481, .neg 487, .neg 488, .neg 489, .neg 492, .neg 495]
private def clause580 : Sat.Clause := [.neg 296, .neg 298, .neg 299, .neg 300, .neg 301, .neg 306, .neg 307, .neg 308, .neg 309, .neg 316, .neg 317, .neg 318, .neg 319, .neg 320, .neg 321, .neg 339, .neg 340, .neg 341, .neg 342, .neg 346, .neg 347, .neg 348, .neg 349, .neg 350, .neg 351, .neg 358, .neg 359, .neg 360, .neg 361, .neg 362, .neg 363, .neg 368, .neg 369, .neg 370, .neg 371, .neg 398, .neg 399, .neg 400, .neg 401, .neg 405, .neg 406, .neg 407, .neg 408, .neg 409, .neg 410, .neg 420, .neg 421, .neg 422, .neg 423, .neg 424, .neg 425, .neg 433, .neg 434, .neg 435, .neg 436, .neg 470, .neg 471, .neg 472, .neg 473, .neg 474, .neg 475, .neg 479, .neg 480, .neg 481, .neg 482, .neg 490, .neg 491, .neg 492, .neg 493, .neg 496]
private def clause581 : Sat.Clause := [.neg 372, .neg 373, .neg 374, .neg 375, .neg 376, .neg 377, .neg 378, .neg 379, .neg 380, .neg 381, .neg 382, .neg 383, .neg 384, .neg 385, .neg 386, .neg 387, .neg 388, .neg 389, .neg 390, .neg 391, .neg 392, .neg 393, .neg 394, .neg 395, .neg 396, .neg 411, .neg 412, .neg 413, .neg 414, .neg 415, .neg 416, .neg 426, .neg 427, .neg 428, .neg 431, .neg 437, .neg 438, .neg 439, .neg 440, .neg 441, .neg 442, .neg 443, .neg 444, .neg 445, .neg 446, .neg 447, .neg 448, .neg 449, .neg 450, .neg 451, .neg 452, .neg 453, .neg 454, .neg 455, .neg 456, .neg 457, .neg 458, .neg 459, .neg 460, .neg 461, .neg 462, .neg 463, .neg 464, .neg 465, .neg 466, .neg 483, .neg 484, .neg 485, .neg 486, .neg 494]

private def clauses : Sat.Fmla := [
  clause000, clause001, clause002, clause003, clause004, clause005, clause006, clause007, clause008, clause009, clause010, clause011, clause012, clause013, clause014, clause015, clause016, clause017, clause018, clause019, clause020, clause021, clause022, clause023, clause024, clause025, clause026, clause027, clause028, clause029, clause030, clause031, clause032, clause033, clause034, clause035, clause036, clause037, clause038, clause039, clause040, clause041, clause042, clause043, clause044, clause045, clause046, clause047, clause048, clause049, clause050, clause051, clause052, clause053, clause054, clause055, clause056, clause057, clause058, clause059, clause060, clause061, clause062, clause063, clause064, clause065, clause066, clause067, clause068, clause069, clause070, clause071, clause072, clause073, clause074, clause075, clause076, clause077, clause078, clause079, clause080, clause081, clause082, clause083, clause084, clause085, clause086, clause087, clause088, clause089, clause090, clause091, clause092, clause093, clause094, clause095, clause096, clause097, clause098, clause099, clause100, clause101, clause102, clause103, clause104, clause105, clause106, clause107, clause108, clause109, clause110, clause111, clause112, clause113, clause114, clause115, clause116, clause117, clause118, clause119, clause120, clause121, clause122, clause123, clause124, clause125, clause126, clause127, clause128, clause129, clause130, clause131, clause132, clause133, clause134, clause135, clause136, clause137, clause138, clause139, clause140, clause141, clause142, clause143, clause144, clause145, clause146, clause147, clause148, clause149, clause150, clause151, clause152, clause153, clause154, clause155, clause156, clause157, clause158, clause159, clause160, clause161, clause162, clause163, clause164, clause165, clause166, clause167, clause168, clause169, clause170, clause171, clause172, clause173, clause174, clause175, clause176, clause177, clause178, clause179, clause180, clause181, clause182, clause183, clause184, clause185, clause186, clause187, clause188, clause189, clause190, clause191, clause192, clause193, clause194, clause195, clause196, clause197, clause198, clause199, clause200, clause201, clause202, clause203, clause204, clause205, clause206, clause207, clause208, clause209, clause210, clause211, clause212, clause213, clause214, clause215, clause216, clause217, clause218, clause219, clause220, clause221, clause222, clause223, clause224, clause225, clause226, clause227, clause228, clause229, clause230, clause231, clause232, clause233, clause234, clause235, clause236, clause237, clause238, clause239, clause240, clause241, clause242, clause243, clause244, clause245, clause246, clause247, clause248, clause249, clause250, clause251, clause252, clause253, clause254, clause255, clause256, clause257, clause258, clause259, clause260, clause261, clause262, clause263, clause264, clause265, clause266, clause267, clause268, clause269, clause270, clause271, clause272, clause273, clause274, clause275, clause276, clause277, clause278, clause279, clause280, clause281, clause282, clause283, clause284, clause285, clause286, clause287, clause288, clause289, clause290, clause291, clause292, clause293, clause294, clause295, clause296, clause297, clause298, clause299, clause300, clause301, clause302, clause303, clause304, clause305, clause306, clause307, clause308, clause309, clause310, clause311, clause312, clause313, clause314, clause315, clause316, clause317, clause318, clause319, clause320, clause321, clause322, clause323, clause324, clause325, clause326, clause327, clause328, clause329, clause330, clause331, clause332, clause333, clause334, clause335, clause336, clause337, clause338, clause339, clause340, clause341, clause342, clause343, clause344, clause345, clause346, clause347, clause348, clause349, clause350, clause351, clause352, clause353, clause354, clause355, clause356, clause357, clause358, clause359, clause360, clause361, clause362, clause363, clause364, clause365, clause366, clause367, clause368, clause369, clause370, clause371, clause372, clause373, clause374, clause375, clause376, clause377, clause378, clause379, clause380, clause381, clause382, clause383, clause384, clause385, clause386, clause387, clause388, clause389, clause390, clause391, clause392, clause393, clause394, clause395, clause396, clause397, clause398, clause399, clause400, clause401, clause402, clause403, clause404, clause405, clause406, clause407, clause408, clause409, clause410, clause411, clause412, clause413, clause414, clause415, clause416, clause417, clause418, clause419, clause420, clause421, clause422, clause423, clause424, clause425, clause426, clause427, clause428, clause429, clause430, clause431, clause432, clause433, clause434, clause435, clause436, clause437, clause438, clause439, clause440, clause441, clause442, clause443, clause444, clause445, clause446, clause447, clause448, clause449, clause450, clause451, clause452, clause453, clause454, clause455, clause456, clause457, clause458, clause459, clause460, clause461, clause462, clause463, clause464, clause465, clause466, clause467, clause468, clause469, clause470, clause471, clause472, clause473, clause474, clause475, clause476, clause477, clause478, clause479, clause480, clause481, clause482, clause483, clause484, clause485, clause486, clause487, clause488, clause489, clause490, clause491, clause492, clause493, clause494, clause495, clause496, clause497, clause498, clause499, clause500, clause501, clause502, clause503, clause504, clause505, clause506, clause507, clause508, clause509, clause510, clause511, clause512, clause513, clause514, clause515, clause516, clause517, clause518, clause519, clause520, clause521, clause522, clause523, clause524, clause525, clause526, clause527, clause528, clause529, clause530, clause531, clause532, clause533, clause534, clause535, clause536, clause537, clause538, clause539, clause540, clause541, clause542, clause543, clause544, clause545, clause546, clause547, clause548, clause549, clause550, clause551, clause552, clause553, clause554, clause555, clause556, clause557, clause558, clause559, clause560, clause561, clause562, clause563, clause564, clause565, clause566, clause567, clause568, clause569, clause570, clause571, clause572, clause573, clause574, clause575, clause576, clause577, clause578, clause579, clause580, clause581]

private theorem formula_eq : cnf_refutation.formula = clauses := by rfl

variable {n : ℕ} (C : Context 13 n states)

-- Clause 1: domain; source clause 7.
private theorem sound000 : C.clause (decodeClause atoms clause000) := by
  exact C.covered_clause _ _ (C.domain_clause 0 1 (by decide) 1 1 (by decide +kernel)) (by decide +kernel)

-- Clause 2: domain; source clause 13.
private theorem sound001 : C.clause (decodeClause atoms clause001) := by
  exact C.covered_clause _ _ (C.domain_clause 0 1 (by decide) 2 1 (by decide +kernel)) (by decide +kernel)

-- Clause 3: domain; source clause 19.
private theorem sound002 : C.clause (decodeClause atoms clause002) := by
  exact C.covered_clause _ _ (C.domain_clause 0 1 (by decide) 3 1 (by decide +kernel)) (by decide +kernel)

-- Clause 4: empty_direction; source clause 30.
private theorem sound003 : C.clause (decodeClause atoms clause003) := by
  exact C.covered_clause _ _ (C.empty_clause 1 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 5: empty_direction; source clause 83.
private theorem sound004 : C.clause (decodeClause atoms clause004) := by
  exact C.covered_clause _ _ (C.empty_clause 2 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 6: empty_direction; source clause 135.
private theorem sound005 : C.clause (decodeClause atoms clause005) := by
  exact C.covered_clause _ _ (C.empty_clause 3 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 7: empty_direction; source clause 186.
private theorem sound006 : C.clause (decodeClause atoms clause006) := by
  exact C.covered_clause _ _ (C.empty_clause 4 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 8: empty_direction; source clause 237.
private theorem sound007 : C.clause (decodeClause atoms clause007) := by
  exact C.covered_clause _ _ (C.empty_clause 5 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 9: empty_direction; source clause 287.
private theorem sound008 : C.clause (decodeClause atoms clause008) := by
  exact C.covered_clause _ _ (C.empty_clause 6 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 10: empty_direction; source clause 337.
private theorem sound009 : C.clause (decodeClause atoms clause009) := by
  exact C.covered_clause _ _ (C.empty_clause 7 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 11: empty_direction; source clause 434.
private theorem sound010 : C.clause (decodeClause atoms clause010) := by
  exact C.covered_clause _ _ (C.empty_clause 9 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 12: domain; source clause 465.
private theorem sound011 : C.clause (decodeClause atoms clause011) := by
  exact C.covered_clause _ _ (C.domain_clause 0 10 (by decide) 1 1 (by decide +kernel)) (by decide +kernel)

-- Clause 13: domain; source clause 471.
private theorem sound012 : C.clause (decodeClause atoms clause012) := by
  exact C.covered_clause _ _ (C.domain_clause 0 10 (by decide) 2 1 (by decide +kernel)) (by decide +kernel)

-- Clause 14: domain; source clause 472.
private theorem sound013 : C.clause (decodeClause atoms clause013) := by
  exact C.covered_clause _ _ (C.domain_clause 0 10 (by decide) 3 1 (by decide +kernel)) (by decide +kernel)

-- Clause 15: empty_direction; source clause 483.
private theorem sound014 : C.clause (decodeClause atoms clause014) := by
  exact C.covered_clause _ _ (C.empty_clause 10 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 16: empty_direction; source clause 532.
private theorem sound015 : C.clause (decodeClause atoms clause015) := by
  exact C.covered_clause _ _ (C.empty_clause 11 0 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 17: empty_direction; source clause 634.
private theorem sound016 : C.clause (decodeClause atoms clause016) := by
  exact C.covered_clause _ _ (C.empty_clause 2 1 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 18: empty_direction; source clause 687.
private theorem sound017 : C.clause (decodeClause atoms clause017) := by
  exact C.covered_clause _ _ (C.empty_clause 3 1 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 19: empty_direction; source clause 739.
private theorem sound018 : C.clause (decodeClause atoms clause018) := by
  exact C.covered_clause _ _ (C.empty_clause 4 1 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 20: empty_direction; source clause 791.
private theorem sound019 : C.clause (decodeClause atoms clause019) := by
  exact C.covered_clause _ _ (C.empty_clause 5 1 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 21: empty_direction; source clause 842.
private theorem sound020 : C.clause (decodeClause atoms clause020) := by
  exact C.covered_clause _ _ (C.empty_clause 6 1 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 22: empty_direction; source clause 893.
private theorem sound021 : C.clause (decodeClause atoms clause021) := by
  exact C.covered_clause _ _ (C.empty_clause 7 1 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 23: empty_direction; source clause 990.
private theorem sound022 : C.clause (decodeClause atoms clause022) := by
  exact C.covered_clause _ _ (C.empty_clause 9 1 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 24: empty_direction; source clause 1040.
private theorem sound023 : C.clause (decodeClause atoms clause023) := by
  exact C.covered_clause _ _ (C.empty_clause 10 1 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 25: empty_direction; source clause 1190.
private theorem sound024 : C.clause (decodeClause atoms clause024) := by
  exact C.covered_clause _ _ (C.empty_clause 3 2 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 26: empty_direction; source clause 1296.
private theorem sound025 : C.clause (decodeClause atoms clause025) := by
  exact C.covered_clause _ _ (C.empty_clause 5 2 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 27: empty_direction; source clause 1400.
private theorem sound026 : C.clause (decodeClause atoms clause026) := by
  exact C.covered_clause _ _ (C.empty_clause 7 2 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 28: empty_direction; source clause 1550.
private theorem sound027 : C.clause (decodeClause atoms clause027) := by
  exact C.covered_clause _ _ (C.empty_clause 10 2 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 29: empty_direction; source clause 1702.
private theorem sound028 : C.clause (decodeClause atoms clause028) := by
  exact C.covered_clause _ _ (C.empty_clause 4 3 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 30: empty_direction; source clause 1756.
private theorem sound029 : C.clause (decodeClause atoms clause029) := by
  exact C.covered_clause _ _ (C.empty_clause 5 3 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 31: empty_direction; source clause 1862.
private theorem sound030 : C.clause (decodeClause atoms clause030) := by
  exact C.covered_clause _ _ (C.empty_clause 7 3 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 32: empty_direction; source clause 1963.
private theorem sound031 : C.clause (decodeClause atoms clause031) := by
  exact C.covered_clause _ _ (C.empty_clause 9 3 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 33: empty_direction; source clause 2015.
private theorem sound032 : C.clause (decodeClause atoms clause032) := by
  exact C.covered_clause _ _ (C.empty_clause 10 3 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 34: empty_direction; source clause 2221.
private theorem sound033 : C.clause (decodeClause atoms clause033) := by
  exact C.covered_clause _ _ (C.empty_clause 6 4 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 35: empty_direction; source clause 2373.
private theorem sound034 : C.clause (decodeClause atoms clause034) := by
  exact C.covered_clause _ _ (C.empty_clause 9 4 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 36: empty_direction; source clause 2525.
private theorem sound035 : C.clause (decodeClause atoms clause035) := by
  exact C.covered_clause _ _ (C.empty_clause 12 4 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 37: empty_direction; source clause 2579.
private theorem sound036 : C.clause (decodeClause atoms clause036) := by
  exact C.covered_clause _ _ (C.empty_clause 6 5 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 38: empty_direction; source clause 2633.
private theorem sound037 : C.clause (decodeClause atoms clause037) := by
  exact C.covered_clause _ _ (C.empty_clause 7 5 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 39: empty_direction; source clause 2789.
private theorem sound038 : C.clause (decodeClause atoms clause038) := by
  exact C.covered_clause _ _ (C.empty_clause 10 5 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 40: empty_direction; source clause 3046.
private theorem sound039 : C.clause (decodeClause atoms clause039) := by
  exact C.covered_clause _ _ (C.empty_clause 9 6 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 41: empty_direction; source clause 3306.
private theorem sound040 : C.clause (decodeClause atoms clause040) := by
  exact C.covered_clause _ _ (C.empty_clause 9 7 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 42: domain; source clause 3342.
private theorem sound041 : C.clause (decodeClause atoms clause041) := by
  exact C.covered_clause _ _ (C.domain_clause 7 10 (by decide) 1 6 (by decide +kernel)) (by decide +kernel)

-- Clause 43: empty_direction; source clause 3360.
private theorem sound042 : C.clause (decodeClause atoms clause042) := by
  exact C.covered_clause _ _ (C.empty_clause 10 7 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 44: domain; source clause 3419.
private theorem sound043 : C.clause (decodeClause atoms clause043) := by
  exact C.covered_clause _ _ (C.domain_clause 11 7 (by decide) 2 1 (by decide +kernel)) (by decide +kernel)

-- Clause 45: domain; source clause 3420.
private theorem sound044 : C.clause (decodeClause atoms clause044) := by
  exact C.covered_clause _ _ (C.domain_clause 11 7 (by decide) 2 2 (by decide +kernel)) (by decide +kernel)

-- Clause 46: domain; source clause 3421.
private theorem sound045 : C.clause (decodeClause atoms clause045) := by
  exact C.covered_clause _ _ (C.domain_clause 11 7 (by decide) 2 3 (by decide +kernel)) (by decide +kernel)

-- Clause 47: domain; source clause 3422.
private theorem sound046 : C.clause (decodeClause atoms clause046) := by
  exact C.covered_clause _ _ (C.domain_clause 11 7 (by decide) 2 4 (by decide +kernel)) (by decide +kernel)

-- Clause 48: domain; source clause 3425.
private theorem sound047 : C.clause (decodeClause atoms clause047) := by
  exact C.covered_clause _ _ (C.domain_clause 11 7 (by decide) 3 1 (by decide +kernel)) (by decide +kernel)

-- Clause 49: domain; source clause 3426.
private theorem sound048 : C.clause (decodeClause atoms clause048) := by
  exact C.covered_clause _ _ (C.domain_clause 11 7 (by decide) 3 2 (by decide +kernel)) (by decide +kernel)

-- Clause 50: domain; source clause 3427.
private theorem sound049 : C.clause (decodeClause atoms clause049) := by
  exact C.covered_clause _ _ (C.domain_clause 11 7 (by decide) 3 3 (by decide +kernel)) (by decide +kernel)

-- Clause 51: domain; source clause 3428.
private theorem sound050 : C.clause (decodeClause atoms clause050) := by
  exact C.covered_clause _ _ (C.domain_clause 11 7 (by decide) 3 4 (by decide +kernel)) (by decide +kernel)

-- Clause 52: domain; source clause 3431.
private theorem sound051 : C.clause (decodeClause atoms clause051) := by
  exact C.covered_clause _ _ (C.domain_clause 11 7 (by decide) 4 2 (by decide +kernel)) (by decide +kernel)

-- Clause 53: domain; source clause 3432.
private theorem sound052 : C.clause (decodeClause atoms clause052) := by
  exact C.covered_clause _ _ (C.domain_clause 11 7 (by decide) 4 3 (by decide +kernel)) (by decide +kernel)

-- Clause 54: domain; source clause 3433.
private theorem sound053 : C.clause (decodeClause atoms clause053) := by
  exact C.covered_clause _ _ (C.domain_clause 11 7 (by decide) 4 4 (by decide +kernel)) (by decide +kernel)

-- Clause 55: domain; source clause 3545.
private theorem sound054 : C.clause (decodeClause atoms clause054) := by
  exact C.covered_clause _ _ (C.domain_clause 8 10 (by decide) 1 1 (by decide +kernel)) (by decide +kernel)

-- Clause 56: domain; source clause 3551.
private theorem sound055 : C.clause (decodeClause atoms clause055) := by
  exact C.covered_clause _ _ (C.domain_clause 8 10 (by decide) 2 1 (by decide +kernel)) (by decide +kernel)

-- Clause 57: empty_direction; source clause 3567.
private theorem sound056 : C.clause (decodeClause atoms clause056) := by
  exact C.covered_clause _ _ (C.empty_clause 10 8 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 58: empty_direction; source clause 3620.
private theorem sound057 : C.clause (decodeClause atoms clause057) := by
  exact C.covered_clause _ _ (C.empty_clause 11 8 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 59: domain; source clause 3743.
private theorem sound058 : C.clause (decodeClause atoms clause058) := by
  exact C.covered_clause _ _ (C.domain_clause 10 9 (by decide) 4 1 (by decide +kernel)) (by decide +kernel)

-- Clause 60: domain; source clause 3744.
private theorem sound059 : C.clause (decodeClause atoms clause059) := by
  exact C.covered_clause _ _ (C.domain_clause 10 9 (by decide) 4 2 (by decide +kernel)) (by decide +kernel)

-- Clause 61: domain; source clause 3745.
private theorem sound060 : C.clause (decodeClause atoms clause060) := by
  exact C.covered_clause _ _ (C.domain_clause 10 9 (by decide) 4 3 (by decide +kernel)) (by decide +kernel)

-- Clause 62: domain; source clause 3746.
private theorem sound061 : C.clause (decodeClause atoms clause061) := by
  exact C.covered_clause _ _ (C.domain_clause 10 9 (by decide) 4 4 (by decide +kernel)) (by decide +kernel)

-- Clause 63: domain; source clause 3747.
private theorem sound062 : C.clause (decodeClause atoms clause062) := by
  exact C.covered_clause _ _ (C.domain_clause 10 9 (by decide) 4 5 (by decide +kernel)) (by decide +kernel)

-- Clause 64: empty_direction; source clause 3830.
private theorem sound063 : C.clause (decodeClause atoms clause063) := by
  exact C.covered_clause _ _ (C.empty_clause 12 9 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 65: domain; source clause 3874.
private theorem sound064 : C.clause (decodeClause atoms clause064) := by
  exact C.covered_clause _ _ (C.domain_clause 10 11 (by decide) 3 3 (by decide +kernel)) (by decide +kernel)

-- Clause 66: domain; source clause 3875.
private theorem sound065 : C.clause (decodeClause atoms clause065) := by
  exact C.covered_clause _ _ (C.domain_clause 10 11 (by decide) 3 4 (by decide +kernel)) (by decide +kernel)

-- Clause 67: domain; source clause 3876.
private theorem sound066 : C.clause (decodeClause atoms clause066) := by
  exact C.covered_clause _ _ (C.domain_clause 10 11 (by decide) 3 5 (by decide +kernel)) (by decide +kernel)

-- Clause 68: domain; source clause 3877.
private theorem sound067 : C.clause (decodeClause atoms clause067) := by
  exact C.covered_clause _ _ (C.domain_clause 10 11 (by decide) 3 6 (by decide +kernel)) (by decide +kernel)

-- Clause 69: empty_direction; source clause 3936.
private theorem sound068 : C.clause (decodeClause atoms clause068) := by
  exact C.covered_clause _ _ (C.empty_clause 12 10 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 70: empty_direction; source clause 3990.
private theorem sound069 : C.clause (decodeClause atoms clause069) := by
  exact C.covered_clause _ _ (C.empty_clause 12 11 (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 71: growth; source clause 4020.
private theorem sound070 : C.clause (decodeClause atoms clause070) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 1 2 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 72: growth; source clause 4021.
private theorem sound071 : C.clause (decodeClause atoms clause071) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 1 2 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 73: order_transitive; source clause 4081.
private theorem sound072 : C.clause (decodeClause atoms clause072) := by
  exact C.covered_clause _ _ (C.transitive_clause 0 1 8 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 74: growth; source clause 4085.
private theorem sound073 : C.clause (decodeClause atoms clause073) := by
  exact C.covered_clause _ _ (C.growth_clause false 0 1 8 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 75: growth; source clause 4108.
private theorem sound074 : C.clause (decodeClause atoms clause074) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 1 10 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 76: order_transitive; source clause 4202.
private theorem sound075 : C.clause (decodeClause atoms clause075) := by
  exact C.covered_clause _ _ (C.transitive_clause 0 2 8 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 77: order_transitive; source clause 4323.
private theorem sound076 : C.clause (decodeClause atoms clause076) := by
  exact C.covered_clause _ _ (C.transitive_clause 0 3 8 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 78: growth; source clause 4955.
private theorem sound077 : C.clause (decodeClause atoms clause077) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 8 10 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 79: order_transitive; source clause 5060.
private theorem sound078 : C.clause (decodeClause atoms clause078) := by
  exact C.covered_clause _ _ (C.transitive_clause 0 9 8 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 80: growth; source clause 5209.
private theorem sound079 : C.clause (decodeClause atoms clause079) := by
  exact C.covered_clause _ _ (C.growth_clause true 0 10 11 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 81: growth; source clause 5218.
private theorem sound080 : C.clause (decodeClause atoms clause080) := by
  exact C.covered_clause _ _ (C.growth_clause false 0 10 12 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 82: growth; source clause 5605.
private theorem sound081 : C.clause (decodeClause atoms clause081) := by
  exact C.covered_clause _ _ (C.growth_clause true 1 2 3 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 83: growth; source clause 5606.
private theorem sound082 : C.clause (decodeClause atoms clause082) := by
  exact C.covered_clause _ _ (C.growth_clause true 1 2 3 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 84: order_transitive; source clause 6138.
private theorem sound083 : C.clause (decodeClause atoms clause083) := by
  exact C.covered_clause _ _ (C.transitive_clause 1 6 8 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 85: order_transitive; source clause 6512.
private theorem sound084 : C.clause (decodeClause atoms clause084) := by
  exact C.covered_clause _ _ (C.transitive_clause 1 9 8 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 86: growth; source clause 6661.
private theorem sound085 : C.clause (decodeClause atoms clause085) := by
  exact C.covered_clause _ _ (C.growth_clause true 1 10 11 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 87: growth; source clause 7201.
private theorem sound086 : C.clause (decodeClause atoms clause086) := by
  exact C.covered_clause _ _ (C.growth_clause true 2 3 5 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 88: growth; source clause 7202.
private theorem sound087 : C.clause (decodeClause atoms clause087) := by
  exact C.covered_clause _ _ (C.growth_clause true 2 3 5 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 89: order_transitive; source clause 7260.
private theorem sound088 : C.clause (decodeClause atoms clause088) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 3 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 90: order_transitive; source clause 7502.
private theorem sound089 : C.clause (decodeClause atoms clause089) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 5 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 91: order_transitive; source clause 7744.
private theorem sound090 : C.clause (decodeClause atoms clause090) := by
  exact C.covered_clause _ _ (C.transitive_clause 2 7 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 92: growth; source clause 8200.
private theorem sound091 : C.clause (decodeClause atoms clause091) := by
  exact C.covered_clause _ _ (C.growth_clause true 2 11 7 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 93: growth; source clause 8918.
private theorem sound092 : C.clause (decodeClause atoms clause092) := by
  exact C.covered_clause _ _ (C.growth_clause true 3 5 7 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 94: growth; source clause 8919.
private theorem sound093 : C.clause (decodeClause atoms clause093) := by
  exact C.covered_clause _ _ (C.growth_clause true 3 5 7 (by decide) (by decide) (by decide) 5) (by decide +kernel)

-- Clause 95: growth; source clause 8951.
private theorem sound094 : C.clause (decodeClause atoms clause094) := by
  exact C.covered_clause _ _ (C.growth_clause true 3 5 10 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 96: order_transitive; source clause 8954.
private theorem sound095 : C.clause (decodeClause atoms clause095) := by
  exact C.covered_clause _ _ (C.transitive_clause 3 5 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 97: order_transitive; source clause 9196.
private theorem sound096 : C.clause (decodeClause atoms clause096) := by
  exact C.covered_clause _ _ (C.transitive_clause 3 7 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 98: order_transitive; source clause 10494.
private theorem sound097 : C.clause (decodeClause atoms clause097) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 6 8 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 99: order_transitive; source clause 10868.
private theorem sound098 : C.clause (decodeClause atoms clause098) := by
  exact C.covered_clause _ _ (C.transitive_clause 4 9 8 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 100: growth; source clause 12098.
private theorem sound099 : C.clause (decodeClause atoms clause099) := by
  exact C.covered_clause _ _ (C.growth_clause true 5 7 10 (by decide) (by decide) (by decide) 5) (by decide +kernel)

-- Clause 101: growth; source clause 12099.
private theorem sound100 : C.clause (decodeClause atoms clause100) := by
  exact C.covered_clause _ _ (C.growth_clause true 5 7 10 (by decide) (by decide) (by decide) 6) (by decide +kernel)

-- Clause 102: order_transitive; source clause 12100.
private theorem sound101 : C.clause (decodeClause atoms clause101) := by
  exact C.covered_clause _ _ (C.transitive_clause 5 7 11 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 103: growth; source clause 12472.
private theorem sound102 : C.clause (decodeClause atoms clause102) := by
  exact C.covered_clause _ _ (C.growth_clause true 5 10 11 (by decide) (by decide) (by decide) 5) (by decide +kernel)

-- Clause 104: growth; source clause 13667.
private theorem sound103 : C.clause (decodeClause atoms clause103) := by
  exact C.covered_clause _ _ (C.growth_clause true 6 8 10 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 105: order_transitive; source clause 13772.
private theorem sound104 : C.clause (decodeClause atoms clause104) := by
  exact C.covered_clause _ _ (C.transitive_clause 6 9 8 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 106: order_transitive; source clause 13783.
private theorem sound105 : C.clause (decodeClause atoms clause105) := by
  exact C.covered_clause _ _ (C.transitive_clause 6 9 10 (by decide) (by decide) (by decide)) (by decide +kernel)

-- Clause 107: growth; source clause 15267.
private theorem sound106 : C.clause (decodeClause atoms clause106) := by
  exact C.covered_clause _ _ (C.growth_clause true 7 9 12 (by decide) (by decide) (by decide) 6) (by decide +kernel)

-- Clause 108: growth; source clause 15369.
private theorem sound107 : C.clause (decodeClause atoms clause107) := by
  exact C.covered_clause _ _ (C.growth_clause false 7 10 11 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 109: growth; source clause 15377.
private theorem sound108 : C.clause (decodeClause atoms clause108) := by
  exact C.covered_clause _ _ (C.growth_clause true 7 10 11 (by decide) (by decide) (by decide) 6) (by decide +kernel)

-- Clause 110: growth; source clause 15388.
private theorem sound109 : C.clause (decodeClause atoms clause109) := by
  exact C.covered_clause _ _ (C.growth_clause true 7 10 12 (by decide) (by decide) (by decide) 6) (by decide +kernel)

-- Clause 111: growth; source clause 15636.
private theorem sound110 : C.clause (decodeClause atoms clause110) := by
  exact C.covered_clause _ _ (C.growth_clause true 8 0 1 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 112: growth; source clause 15724.
private theorem sound111 : C.clause (decodeClause atoms clause111) := by
  exact C.covered_clause _ _ (C.growth_clause true 8 0 10 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 113: growth; source clause 16811.
private theorem sound112 : C.clause (decodeClause atoms clause112) := by
  exact C.covered_clause _ _ (C.growth_clause false 8 10 9 (by decide) (by decide) (by decide) 3) (by decide +kernel)

-- Clause 114: growth; source clause 16825.
private theorem sound113 : C.clause (decodeClause atoms clause113) := by
  exact C.covered_clause _ _ (C.growth_clause true 8 10 11 (by decide) (by decide) (by decide) 2) (by decide +kernel)

-- Clause 115: growth; source clause 16919.
private theorem sound114 : C.clause (decodeClause atoms clause114) := by
  exact C.covered_clause _ _ (C.growth_clause false 8 11 7 (by decide) (by decide) (by decide) 1) (by decide +kernel)

-- Clause 116: growth; source clause 19744.
private theorem sound115 : C.clause (decodeClause atoms clause115) := by
  exact C.covered_clause _ _ (C.growth_clause true 10 9 12 (by decide) (by decide) (by decide) 6) (by decide +kernel)

-- Clause 117: growth; source clause 19859.
private theorem sound116 : C.clause (decodeClause atoms clause116) := by
  exact C.covered_clause _ _ (C.growth_clause false 10 11 12 (by decide) (by decide) (by decide) 4) (by decide +kernel)

-- Clause 118: growth; source clause 20931.
private theorem sound117 : C.clause (decodeClause atoms clause117) := by
  exact C.covered_clause _ _ (C.growth_clause true 11 7 9 (by decide) (by decide) (by decide) 5) (by decide +kernel)

-- Clause 119: fixed_sign; source clause 22891.
private theorem sound118 : C.clause (decodeClause atoms clause118) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 2 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 120: fixed_sign; source clause 22892.
private theorem sound119 : C.clause (decodeClause atoms clause119) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 3 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 121: fixed_sign; source clause 22893.
private theorem sound120 : C.clause (decodeClause atoms clause120) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 4 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 122: fixed_sign; source clause 22894.
private theorem sound121 : C.clause (decodeClause atoms clause121) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 5 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 123: fixed_sign; source clause 22895.
private theorem sound122 : C.clause (decodeClause atoms clause122) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 124: fixed_sign; source clause 22896.
private theorem sound123 : C.clause (decodeClause atoms clause123) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 125: fixed_sign; source clause 22897.
private theorem sound124 : C.clause (decodeClause atoms clause124) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 126: fixed_sign; source clause 22898.
private theorem sound125 : C.clause (decodeClause atoms clause125) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 127: fixed_sign; source clause 22899.
private theorem sound126 : C.clause (decodeClause atoms clause126) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 128: fixed_sign; source clause 22900.
private theorem sound127 : C.clause (decodeClause atoms clause127) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 1 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 129: fixed_sign; source clause 22901.
private theorem sound128 : C.clause (decodeClause atoms clause128) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 3 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 130: fixed_sign; source clause 22902.
private theorem sound129 : C.clause (decodeClause atoms clause129) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 5 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 131: fixed_sign; source clause 22903.
private theorem sound130 : C.clause (decodeClause atoms clause130) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 132: fixed_sign; source clause 22904.
private theorem sound131 : C.clause (decodeClause atoms clause131) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 2 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 133: fixed_sign; source clause 22905.
private theorem sound132 : C.clause (decodeClause atoms clause132) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 3 5 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 134: fixed_sign; source clause 22906.
private theorem sound133 : C.clause (decodeClause atoms clause133) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 3 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 135: fixed_sign; source clause 22907.
private theorem sound134 : C.clause (decodeClause atoms clause134) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 3 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 136: fixed_sign; source clause 22908.
private theorem sound135 : C.clause (decodeClause atoms clause135) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 4 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 137: fixed_sign; source clause 22909.
private theorem sound136 : C.clause (decodeClause atoms clause136) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 4 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 138: fixed_sign; source clause 22910.
private theorem sound137 : C.clause (decodeClause atoms clause137) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 4 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 139: fixed_sign; source clause 22911.
private theorem sound138 : C.clause (decodeClause atoms clause138) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 4 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 140: fixed_sign; source clause 22912.
private theorem sound139 : C.clause (decodeClause atoms clause139) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 5 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 141: fixed_sign; source clause 22913.
private theorem sound140 : C.clause (decodeClause atoms clause140) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 5 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 142: fixed_sign; source clause 22914.
private theorem sound141 : C.clause (decodeClause atoms clause141) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 6 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 143: fixed_sign; source clause 22915.
private theorem sound142 : C.clause (decodeClause atoms clause142) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 6 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 144: fixed_sign; source clause 22916.
private theorem sound143 : C.clause (decodeClause atoms clause143) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 6 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 145: fixed_sign; source clause 22917.
private theorem sound144 : C.clause (decodeClause atoms clause144) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 7 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 146: fixed_sign; source clause 22918.
private theorem sound145 : C.clause (decodeClause atoms clause145) := by
  exact C.covered_clause _ _ (C.fixed_negative 0 8 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 147: fixed_sign; source clause 22919.
private theorem sound146 : C.clause (decodeClause atoms clause146) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 9 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 148: fixed_sign; source clause 22920.
private theorem sound147 : C.clause (decodeClause atoms clause147) := by
  exact C.covered_clause _ _ (C.fixed_positive 0 9 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 149: fixed_sign; source clause 22921.
private theorem sound148 : C.clause (decodeClause atoms clause148) := by
  exact C.covered_clause _ _ (C.fixed_negative 0 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 150: fixed_sign; source clause 22922.
private theorem sound149 : C.clause (decodeClause atoms clause149) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 3 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 151: fixed_sign; source clause 22923.
private theorem sound150 : C.clause (decodeClause atoms clause150) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 5 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 152: fixed_sign; source clause 22924.
private theorem sound151 : C.clause (decodeClause atoms clause151) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 153: fixed_sign; source clause 22925.
private theorem sound152 : C.clause (decodeClause atoms clause152) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 154: fixed_sign; source clause 22926.
private theorem sound153 : C.clause (decodeClause atoms clause153) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 2 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 155: fixed_sign; source clause 22927.
private theorem sound154 : C.clause (decodeClause atoms clause154) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 3 4 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 156: fixed_sign; source clause 22928.
private theorem sound155 : C.clause (decodeClause atoms clause155) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 3 5 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 157: fixed_sign; source clause 22929.
private theorem sound156 : C.clause (decodeClause atoms clause156) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 3 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 158: fixed_sign; source clause 22930.
private theorem sound157 : C.clause (decodeClause atoms clause157) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 3 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 159: fixed_sign; source clause 22931.
private theorem sound158 : C.clause (decodeClause atoms clause158) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 3 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 160: fixed_sign; source clause 22933.
private theorem sound159 : C.clause (decodeClause atoms clause159) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 161: fixed_sign; source clause 22935.
private theorem sound160 : C.clause (decodeClause atoms clause160) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 162: fixed_sign; source clause 22936.
private theorem sound161 : C.clause (decodeClause atoms clause161) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 163: fixed_sign; source clause 22937.
private theorem sound162 : C.clause (decodeClause atoms clause162) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 164: fixed_sign; source clause 22938.
private theorem sound163 : C.clause (decodeClause atoms clause163) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 165: fixed_sign; source clause 22939.
private theorem sound164 : C.clause (decodeClause atoms clause164) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 4 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 166: fixed_sign; source clause 22940.
private theorem sound165 : C.clause (decodeClause atoms clause165) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 5 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 167: fixed_sign; source clause 22941.
private theorem sound166 : C.clause (decodeClause atoms clause166) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 5 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 168: fixed_sign; source clause 22942.
private theorem sound167 : C.clause (decodeClause atoms clause167) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 5 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 169: fixed_sign; source clause 22943.
private theorem sound168 : C.clause (decodeClause atoms clause168) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 5 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 170: fixed_sign; source clause 22945.
private theorem sound169 : C.clause (decodeClause atoms clause169) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 6 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 171: fixed_sign; source clause 22946.
private theorem sound170 : C.clause (decodeClause atoms clause170) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 6 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 172: fixed_sign; source clause 22947.
private theorem sound171 : C.clause (decodeClause atoms clause171) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 6 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 173: fixed_sign; source clause 22948.
private theorem sound172 : C.clause (decodeClause atoms clause172) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 6 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 174: fixed_sign; source clause 22949.
private theorem sound173 : C.clause (decodeClause atoms clause173) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 6 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 175: fixed_sign; source clause 22950.
private theorem sound174 : C.clause (decodeClause atoms clause174) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 7 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 176: fixed_sign; source clause 22952.
private theorem sound175 : C.clause (decodeClause atoms clause175) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 7 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 177: fixed_sign; source clause 22953.
private theorem sound176 : C.clause (decodeClause atoms clause176) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 8 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 178: fixed_sign; source clause 22954.
private theorem sound177 : C.clause (decodeClause atoms clause177) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 8 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 179: fixed_sign; source clause 22955.
private theorem sound178 : C.clause (decodeClause atoms clause178) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 8 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 180: fixed_sign; source clause 22956.
private theorem sound179 : C.clause (decodeClause atoms clause179) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 8 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 181: fixed_sign; source clause 22957.
private theorem sound180 : C.clause (decodeClause atoms clause180) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 9 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 182: fixed_sign; source clause 22958.
private theorem sound181 : C.clause (decodeClause atoms clause181) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 9 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 183: fixed_sign; source clause 22959.
private theorem sound182 : C.clause (decodeClause atoms clause182) := by
  exact C.covered_clause _ _ (C.fixed_positive 1 9 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 184: fixed_sign; source clause 22960.
private theorem sound183 : C.clause (decodeClause atoms clause183) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 10 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 185: fixed_sign; source clause 22961.
private theorem sound184 : C.clause (decodeClause atoms clause184) := by
  exact C.covered_clause _ _ (C.fixed_negative 1 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 186: fixed_sign; source clause 22962.
private theorem sound185 : C.clause (decodeClause atoms clause185) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 3 4 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 187: fixed_sign; source clause 22963.
private theorem sound186 : C.clause (decodeClause atoms clause186) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 3 5 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 188: fixed_sign; source clause 22964.
private theorem sound187 : C.clause (decodeClause atoms clause187) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 3 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 189: fixed_sign; source clause 22965.
private theorem sound188 : C.clause (decodeClause atoms clause188) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 3 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 190: fixed_sign; source clause 22966.
private theorem sound189 : C.clause (decodeClause atoms clause189) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 3 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 191: fixed_sign; source clause 22973.
private theorem sound190 : C.clause (decodeClause atoms clause190) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 4 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 192: fixed_sign; source clause 22975.
private theorem sound191 : C.clause (decodeClause atoms clause191) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 5 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 193: fixed_sign; source clause 22976.
private theorem sound192 : C.clause (decodeClause atoms clause192) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 5 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 194: fixed_sign; source clause 22977.
private theorem sound193 : C.clause (decodeClause atoms clause193) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 5 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 195: fixed_sign; source clause 22978.
private theorem sound194 : C.clause (decodeClause atoms clause194) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 5 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 196: fixed_sign; source clause 22983.
private theorem sound195 : C.clause (decodeClause atoms clause195) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 6 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 197: fixed_sign; source clause 22985.
private theorem sound196 : C.clause (decodeClause atoms clause196) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 7 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 198: fixed_sign; source clause 22987.
private theorem sound197 : C.clause (decodeClause atoms clause197) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 7 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 199: fixed_sign; source clause 22989.
private theorem sound198 : C.clause (decodeClause atoms clause198) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 8 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 200: fixed_sign; source clause 22990.
private theorem sound199 : C.clause (decodeClause atoms clause199) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 8 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 201: fixed_sign; source clause 22992.
private theorem sound200 : C.clause (decodeClause atoms clause200) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 9 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 202: fixed_sign; source clause 22993.
private theorem sound201 : C.clause (decodeClause atoms clause201) := by
  exact C.covered_clause _ _ (C.fixed_positive 2 9 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 203: fixed_sign; source clause 22995.
private theorem sound202 : C.clause (decodeClause atoms clause202) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 10 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 204: fixed_sign; source clause 22996.
private theorem sound203 : C.clause (decodeClause atoms clause203) := by
  exact C.covered_clause _ _ (C.fixed_negative 2 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 205: fixed_sign; source clause 23003.
private theorem sound204 : C.clause (decodeClause atoms clause204) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 4 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 206: fixed_sign; source clause 23005.
private theorem sound205 : C.clause (decodeClause atoms clause205) := by
  exact C.covered_clause _ _ (C.fixed_negative 3 5 6 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 207: fixed_sign; source clause 23006.
private theorem sound206 : C.clause (decodeClause atoms clause206) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 5 7 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 208: fixed_sign; source clause 23007.
private theorem sound207 : C.clause (decodeClause atoms clause207) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 5 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 209: fixed_sign; source clause 23008.
private theorem sound208 : C.clause (decodeClause atoms clause208) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 5 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 210: fixed_sign; source clause 23013.
private theorem sound209 : C.clause (decodeClause atoms clause209) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 6 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 211: fixed_sign; source clause 23015.
private theorem sound210 : C.clause (decodeClause atoms clause210) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 7 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 212: fixed_sign; source clause 23016.
private theorem sound211 : C.clause (decodeClause atoms clause211) := by
  exact C.covered_clause _ _ (C.fixed_negative 3 7 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 213: fixed_sign; source clause 23017.
private theorem sound212 : C.clause (decodeClause atoms clause212) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 7 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 214: fixed_sign; source clause 23019.
private theorem sound213 : C.clause (decodeClause atoms clause213) := by
  exact C.covered_clause _ _ (C.fixed_negative 3 8 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 215: fixed_sign; source clause 23020.
private theorem sound214 : C.clause (decodeClause atoms clause214) := by
  exact C.covered_clause _ _ (C.fixed_negative 3 8 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 216: fixed_sign; source clause 23023.
private theorem sound215 : C.clause (decodeClause atoms clause215) := by
  exact C.covered_clause _ _ (C.fixed_positive 3 9 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 217: fixed_sign; source clause 23025.
private theorem sound216 : C.clause (decodeClause atoms clause216) := by
  exact C.covered_clause _ _ (C.fixed_negative 3 10 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 218: fixed_sign; source clause 23026.
private theorem sound217 : C.clause (decodeClause atoms clause217) := by
  exact C.covered_clause _ _ (C.fixed_negative 3 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 219: fixed_sign; source clause 23029.
private theorem sound218 : C.clause (decodeClause atoms clause218) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 6 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 220: fixed_sign; source clause 23030.
private theorem sound219 : C.clause (decodeClause atoms clause219) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 6 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 221: fixed_sign; source clause 23031.
private theorem sound220 : C.clause (decodeClause atoms clause220) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 6 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 222: fixed_sign; source clause 23032.
private theorem sound221 : C.clause (decodeClause atoms clause221) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 6 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 223: fixed_sign; source clause 23033.
private theorem sound222 : C.clause (decodeClause atoms clause222) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 6 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 224: fixed_sign; source clause 23035.
private theorem sound223 : C.clause (decodeClause atoms clause223) := by
  exact C.covered_clause _ _ (C.fixed_negative 4 8 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 225: fixed_sign; source clause 23036.
private theorem sound224 : C.clause (decodeClause atoms clause224) := by
  exact C.covered_clause _ _ (C.fixed_negative 4 8 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 226: fixed_sign; source clause 23037.
private theorem sound225 : C.clause (decodeClause atoms clause225) := by
  exact C.covered_clause _ _ (C.fixed_negative 4 8 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 227: fixed_sign; source clause 23038.
private theorem sound226 : C.clause (decodeClause atoms clause226) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 9 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 228: fixed_sign; source clause 23039.
private theorem sound227 : C.clause (decodeClause atoms clause227) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 9 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 229: fixed_sign; source clause 23040.
private theorem sound228 : C.clause (decodeClause atoms clause228) := by
  exact C.covered_clause _ _ (C.fixed_positive 4 9 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 230: fixed_sign; source clause 23041.
private theorem sound229 : C.clause (decodeClause atoms clause229) := by
  exact C.covered_clause _ _ (C.fixed_negative 4 10 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 231: fixed_sign; source clause 23042.
private theorem sound230 : C.clause (decodeClause atoms clause230) := by
  exact C.covered_clause _ _ (C.fixed_negative 4 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 232: fixed_sign; source clause 23046.
private theorem sound231 : C.clause (decodeClause atoms clause231) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 6 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 233: fixed_sign; source clause 23047.
private theorem sound232 : C.clause (decodeClause atoms clause232) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 6 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 234: fixed_sign; source clause 23049.
private theorem sound233 : C.clause (decodeClause atoms clause233) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 7 8 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 235: fixed_sign; source clause 23050.
private theorem sound234 : C.clause (decodeClause atoms clause234) := by
  exact C.covered_clause _ _ (C.fixed_negative 5 7 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 236: fixed_sign; source clause 23051.
private theorem sound235 : C.clause (decodeClause atoms clause235) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 7 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 237: fixed_sign; source clause 23053.
private theorem sound236 : C.clause (decodeClause atoms clause236) := by
  exact C.covered_clause _ _ (C.fixed_negative 5 8 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 238: fixed_sign; source clause 23054.
private theorem sound237 : C.clause (decodeClause atoms clause237) := by
  exact C.covered_clause _ _ (C.fixed_negative 5 8 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 239: fixed_sign; source clause 23057.
private theorem sound238 : C.clause (decodeClause atoms clause238) := by
  exact C.covered_clause _ _ (C.fixed_positive 5 9 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 240: fixed_sign; source clause 23059.
private theorem sound239 : C.clause (decodeClause atoms clause239) := by
  exact C.covered_clause _ _ (C.fixed_negative 5 10 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 241: fixed_sign; source clause 23060.
private theorem sound240 : C.clause (decodeClause atoms clause240) := by
  exact C.covered_clause _ _ (C.fixed_negative 5 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 242: fixed_sign; source clause 23062.
private theorem sound241 : C.clause (decodeClause atoms clause241) := by
  exact C.covered_clause _ _ (C.fixed_negative 6 8 9 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 243: fixed_sign; source clause 23063.
private theorem sound242 : C.clause (decodeClause atoms clause242) := by
  exact C.covered_clause _ _ (C.fixed_negative 6 8 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 244: fixed_sign; source clause 23064.
private theorem sound243 : C.clause (decodeClause atoms clause243) := by
  exact C.covered_clause _ _ (C.fixed_negative 6 8 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 245: fixed_sign; source clause 23065.
private theorem sound244 : C.clause (decodeClause atoms clause244) := by
  exact C.covered_clause _ _ (C.fixed_positive 6 9 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 246: fixed_sign; source clause 23066.
private theorem sound245 : C.clause (decodeClause atoms clause245) := by
  exact C.covered_clause _ _ (C.fixed_positive 6 9 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 247: fixed_sign; source clause 23067.
private theorem sound246 : C.clause (decodeClause atoms clause246) := by
  exact C.covered_clause _ _ (C.fixed_positive 6 9 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 248: fixed_sign; source clause 23068.
private theorem sound247 : C.clause (decodeClause atoms clause247) := by
  exact C.covered_clause _ _ (C.fixed_negative 6 10 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 249: fixed_sign; source clause 23069.
private theorem sound248 : C.clause (decodeClause atoms clause248) := by
  exact C.covered_clause _ _ (C.fixed_negative 6 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 250: fixed_sign; source clause 23071.
private theorem sound249 : C.clause (decodeClause atoms clause249) := by
  exact C.covered_clause _ _ (C.fixed_negative 7 8 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 251: fixed_sign; source clause 23072.
private theorem sound250 : C.clause (decodeClause atoms clause250) := by
  exact C.covered_clause _ _ (C.fixed_negative 7 8 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 252: fixed_sign; source clause 23074.
private theorem sound251 : C.clause (decodeClause atoms clause251) := by
  exact C.covered_clause _ _ (C.fixed_positive 7 9 10 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 253: fixed_sign; source clause 23075.
private theorem sound252 : C.clause (decodeClause atoms clause252) := by
  exact C.covered_clause _ _ (C.fixed_positive 7 9 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 254: fixed_sign; source clause 23076.
private theorem sound253 : C.clause (decodeClause atoms clause253) := by
  exact C.covered_clause _ _ (C.fixed_positive 7 9 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 255: fixed_sign; source clause 23078.
private theorem sound254 : C.clause (decodeClause atoms clause254) := by
  exact C.covered_clause _ _ (C.fixed_negative 7 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 256: fixed_sign; source clause 23079.
private theorem sound255 : C.clause (decodeClause atoms clause255) := by
  exact C.covered_clause _ _ (C.fixed_positive 8 9 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 257: fixed_sign; source clause 23080.
private theorem sound256 : C.clause (decodeClause atoms clause256) := by
  exact C.covered_clause _ _ (C.fixed_positive 8 9 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 258: fixed_sign; source clause 23081.
private theorem sound257 : C.clause (decodeClause atoms clause257) := by
  exact C.covered_clause _ _ (C.fixed_positive 8 10 11 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 259: fixed_sign; source clause 23082.
private theorem sound258 : C.clause (decodeClause atoms clause258) := by
  exact C.covered_clause _ _ (C.fixed_positive 8 10 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 260: fixed_sign; source clause 23083.
private theorem sound259 : C.clause (decodeClause atoms clause259) := by
  exact C.covered_clause _ _ (C.fixed_negative 8 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 261: fixed_sign; source clause 23084.
private theorem sound260 : C.clause (decodeClause atoms clause260) := by
  exact C.covered_clause _ _ (C.fixed_negative 9 10 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 262: fixed_sign; source clause 23085.
private theorem sound261 : C.clause (decodeClause atoms clause261) := by
  exact C.covered_clause _ _ (C.fixed_negative 9 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 263: fixed_sign; source clause 23086.
private theorem sound262 : C.clause (decodeClause atoms clause262) := by
  exact C.covered_clause _ _ (C.fixed_negative 10 11 12 (by decide) (by decide) (by decide) (by decide +kernel)) (by decide +kernel)

-- Clause 264: convex_four; source clause 23294.
private theorem sound263 : C.clause (decodeClause atoms clause263) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 265: convex_four; source clause 23710.
private theorem sound264 : C.clause (decodeClause atoms clause264) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 266: convex_four; source clause 24126.
private theorem sound265 : C.clause (decodeClause atoms clause265) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 267: convex_four; source clause 24328.
private theorem sound266 : C.clause (decodeClause atoms clause266) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true) (by decide +kernel)

-- Clause 268: convex_four; source clause 24750.
private theorem sound267 : C.clause (decodeClause atoms clause267) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 269: convex_four; source clause 25582.
private theorem sound268 : C.clause (decodeClause atoms clause268) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 3 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 270: convex_four; source clause 25998.
private theorem sound269 : C.clause (decodeClause atoms clause269) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 3 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 271: convex_four; source clause 26200.
private theorem sound270 : C.clause (decodeClause atoms clause270) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 3 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true) (by decide +kernel)

-- Clause 272: convex_four; source clause 26622.
private theorem sound271 : C.clause (decodeClause atoms clause271) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 273: convex_four; source clause 27454.
private theorem sound272 : C.clause (decodeClause atoms clause272) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 4 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 274: packet; source clause 27670.
private theorem sound273 : C.clause (decodeClause atoms clause273) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 275: packet; source clause 27701.
private theorem sound274 : C.clause (decodeClause atoms clause274) := by
  exact C.covered_clause _ _ (C.packet_clause 0 8 1 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 276: convex_four; source clause 27870.
private theorem sound275 : C.clause (decodeClause atoms clause275) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 4 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 277: convex_four; source clause 28078.
private theorem sound276 : C.clause (decodeClause atoms clause276) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 4 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 278: packet; source clause 28086.
private theorem sound277 : C.clause (decodeClause atoms clause277) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 4 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 279: convex_four; source clause 28286.
private theorem sound278 : C.clause (decodeClause atoms clause278) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 4 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 280: convex_four; source clause 28494.
private theorem sound279 : C.clause (decodeClause atoms clause279) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 4 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 281: convex_four; source clause 28702.
private theorem sound280 : C.clause (decodeClause atoms clause280) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 282: convex_four; source clause 29118.
private theorem sound281 : C.clause (decodeClause atoms clause281) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 283: convex_four; source clause 29320.
private theorem sound282 : C.clause (decodeClause atoms clause282) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true) (by decide +kernel)

-- Clause 284: convex_four; source clause 29742.
private theorem sound283 : C.clause (decodeClause atoms clause283) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 285: convex_four; source clause 30574.
private theorem sound284 : C.clause (decodeClause atoms clause284) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 286: convex_four; source clause 30782.
private theorem sound285 : C.clause (decodeClause atoms clause285) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 6 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 287: packet; source clause 30790.
private theorem sound286 : C.clause (decodeClause atoms clause286) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 288: convex_four; source clause 30990.
private theorem sound287 : C.clause (decodeClause atoms clause287) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 289: convex_four; source clause 31198.
private theorem sound288 : C.clause (decodeClause atoms clause288) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 290: convex_four; source clause 31406.
private theorem sound289 : C.clause (decodeClause atoms clause289) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 6 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 291: convex_four; source clause 31608.
private theorem sound290 : C.clause (decodeClause atoms clause290) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true) (by decide +kernel)

-- Clause 292: convex_four; source clause 32030.
private theorem sound291 : C.clause (decodeClause atoms clause291) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 293: convex_four; source clause 32651.
private theorem sound292 : C.clause (decodeClause atoms clause292) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 294: convex_four; source clause 32853.
private theorem sound293 : C.clause (decodeClause atoms clause293) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false) (by decide +kernel)

-- Clause 295: convex_four; source clause 33067.
private theorem sound294 : C.clause (decodeClause atoms clause294) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 296: convex_four; source clause 33275.
private theorem sound295 : C.clause (decodeClause atoms clause295) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 297: packet; source clause 33286.
private theorem sound296 : C.clause (decodeClause atoms clause296) := by
  exact C.covered_clause _ _ (C.packet_clause 0 1 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 298: convex_four; source clause 33486.
private theorem sound297 : C.clause (decodeClause atoms clause297) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 299: convex_four; source clause 33694.
private theorem sound298 : C.clause (decodeClause atoms clause298) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 300: convex_four; source clause 33902.
private theorem sound299 : C.clause (decodeClause atoms clause299) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 301: convex_four; source clause 34107.
private theorem sound300 : C.clause (decodeClause atoms clause300) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 302: convex_four; source clause 34315.
private theorem sound301 : C.clause (decodeClause atoms clause301) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 303: convex_four; source clause 34523.
private theorem sound302 : C.clause (decodeClause atoms clause302) := by
  exact C.covered_clause _ _ (C.convex_clause 0 1 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 304: convex_four; source clause 34942.
private theorem sound303 : C.clause (decodeClause atoms clause303) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 3 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 305: convex_four; source clause 35358.
private theorem sound304 : C.clause (decodeClause atoms clause304) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 3 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 306: convex_four; source clause 35560.
private theorem sound305 : C.clause (decodeClause atoms clause305) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 3 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true) (by decide +kernel)

-- Clause 307: convex_four; source clause 35982.
private theorem sound306 : C.clause (decodeClause atoms clause306) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 308: convex_four; source clause 38478.
private theorem sound307 : C.clause (decodeClause atoms clause307) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 309: convex_four; source clause 38680.
private theorem sound308 : C.clause (decodeClause atoms clause308) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true) (by decide +kernel)

-- Clause 310: convex_four; source clause 39102.
private theorem sound309 : C.clause (decodeClause atoms clause309) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 311: convex_four; source clause 40968.
private theorem sound310 : C.clause (decodeClause atoms clause310) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true) (by decide +kernel)

-- Clause 312: convex_four; source clause 41390.
private theorem sound311 : C.clause (decodeClause atoms clause311) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 313: packet; source clause 42117.
private theorem sound312 : C.clause (decodeClause atoms clause312) := by
  exact C.covered_clause _ _ (C.packet_clause 8 0 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 314: convex_four; source clause 42213.
private theorem sound313 : C.clause (decodeClause atoms clause313) := by
  exact C.covered_clause _ _ (C.convex_clause 0 2 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false) (by decide +kernel)

-- Clause 315: convex_four; source clause 45966.
private theorem sound314 : C.clause (decodeClause atoms clause314) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 316: convex_four; source clause 46168.
private theorem sound315 : C.clause (decodeClause atoms clause315) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true) (by decide +kernel)

-- Clause 317: convex_four; source clause 46590.
private theorem sound316 : C.clause (decodeClause atoms clause316) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 318: packet; source clause 46606.
private theorem sound317 : C.clause (decodeClause atoms clause317) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 11 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 319: convex_four; source clause 48456.
private theorem sound318 : C.clause (decodeClause atoms clause318) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true) (by decide +kernel)

-- Clause 320: convex_four; source clause 48878.
private theorem sound319 : C.clause (decodeClause atoms clause319) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 321: packet; source clause 49605.
private theorem sound320 : C.clause (decodeClause atoms clause320) := by
  exact C.covered_clause _ _ (C.packet_clause 8 0 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 322: convex_four; source clause 49701.
private theorem sound321 : C.clause (decodeClause atoms clause321) := by
  exact C.covered_clause _ _ (C.convex_clause 0 3 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false) (by decide +kernel)

-- Clause 323: packet; source clause 50760.
private theorem sound322 : C.clause (decodeClause atoms clause322) := by
  exact C.covered_clause _ _ (C.packet_clause 0 3 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 324: packet; source clause 53077.
private theorem sound323 : C.clause (decodeClause atoms clause323) := by
  exact C.covered_clause _ _ (C.packet_clause 0 8 4 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 325: convex_four; source clause 53246.
private theorem sound324 : C.clause (decodeClause atoms clause324) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 326: convex_four; source clause 53454.
private theorem sound325 : C.clause (decodeClause atoms clause325) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 6 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 327: convex_four; source clause 53662.
private theorem sound326 : C.clause (decodeClause atoms clause326) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 328: convex_four; source clause 53870.
private theorem sound327 : C.clause (decodeClause atoms clause327) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 329: convex_four; source clause 54078.
private theorem sound328 : C.clause (decodeClause atoms clause328) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 6 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 330: convex_four; source clause 55323.
private theorem sound329 : C.clause (decodeClause atoms clause329) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 331: packet; source clause 55536.
private theorem sound330 : C.clause (decodeClause atoms clause330) := by
  exact C.covered_clause _ _ (C.packet_clause 0 4 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 332: convex_four; source clause 55739.
private theorem sound331 : C.clause (decodeClause atoms clause331) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 333: convex_four; source clause 55947.
private theorem sound332 : C.clause (decodeClause atoms clause332) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 334: convex_four; source clause 56158.
private theorem sound333 : C.clause (decodeClause atoms clause333) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 335: convex_four; source clause 56366.
private theorem sound334 : C.clause (decodeClause atoms clause334) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 336: convex_four; source clause 56574.
private theorem sound335 : C.clause (decodeClause atoms clause335) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 337: packet; source clause 56582.
private theorem sound336 : C.clause (decodeClause atoms clause336) := by
  exact C.covered_clause _ _ (C.packet_clause 0 4 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 338: convex_four; source clause 56779.
private theorem sound337 : C.clause (decodeClause atoms clause337) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 339: packet; source clause 56805.
private theorem sound338 : C.clause (decodeClause atoms clause338) := by
  exact C.covered_clause _ _ (C.packet_clause 0 10 4 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 340: convex_four; source clause 56987.
private theorem sound339 : C.clause (decodeClause atoms clause339) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 341: convex_four; source clause 57195.
private theorem sound340 : C.clause (decodeClause atoms clause340) := by
  exact C.covered_clause _ _ (C.convex_clause 0 4 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 342: convex_four; source clause 58648.
private theorem sound341 : C.clause (decodeClause atoms clause341) := by
  exact C.covered_clause _ _ (C.convex_clause 0 5 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true) (by decide +kernel)

-- Clause 343: convex_four; source clause 59070.
private theorem sound342 : C.clause (decodeClause atoms clause342) := by
  exact C.covered_clause _ _ (C.convex_clause 0 5 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 344: packet; source clause 59797.
private theorem sound343 : C.clause (decodeClause atoms clause343) := by
  exact C.covered_clause _ _ (C.packet_clause 8 0 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 345: convex_four; source clause 59893.
private theorem sound344 : C.clause (decodeClause atoms clause344) := by
  exact C.covered_clause _ _ (C.convex_clause 0 5 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false) (by decide +kernel)

-- Clause 346: packet; source clause 60981.
private theorem sound345 : C.clause (decodeClause atoms clause345) := by
  exact C.covered_clause _ _ (C.packet_clause 0 11 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 347: packet; source clause 62608.
private theorem sound346 : C.clause (decodeClause atoms clause346) := by
  exact C.covered_clause _ _ (C.packet_clause 0 6 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 348: packet; source clause 62629.
private theorem sound347 : C.clause (decodeClause atoms clause347) := by
  exact C.covered_clause _ _ (C.packet_clause 0 8 6 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 349: convex_four; source clause 62811.
private theorem sound348 : C.clause (decodeClause atoms clause348) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 350: packet; source clause 62816.
private theorem sound349 : C.clause (decodeClause atoms clause349) := by
  exact C.covered_clause _ _ (C.packet_clause 0 6 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 351: packet; source clause 63024.
private theorem sound350 : C.clause (decodeClause atoms clause350) := by
  exact C.covered_clause _ _ (C.packet_clause 0 6 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 352: convex_four; source clause 63227.
private theorem sound351 : C.clause (decodeClause atoms clause351) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 353: convex_four; source clause 63435.
private theorem sound352 : C.clause (decodeClause atoms clause352) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 354: packet; source clause 63445.
private theorem sound353 : C.clause (decodeClause atoms clause353) := by
  exact C.covered_clause _ _ (C.packet_clause 0 6 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 355: packet; source clause 63477.
private theorem sound354 : C.clause (decodeClause atoms clause354) := by
  exact C.covered_clause _ _ (C.packet_clause 0 10 6 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 356: convex_four; source clause 63646.
private theorem sound355 : C.clause (decodeClause atoms clause355) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 357: convex_four; source clause 63854.
private theorem sound356 : C.clause (decodeClause atoms clause356) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 358: convex_four; source clause 64062.
private theorem sound357 : C.clause (decodeClause atoms clause357) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 359: packet; source clause 64079.
private theorem sound358 : C.clause (decodeClause atoms clause358) := by
  exact C.covered_clause _ _ (C.packet_clause 0 10 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 360: packet; source clause 64084.
private theorem sound359 : C.clause (decodeClause atoms clause359) := by
  exact C.covered_clause _ _ (C.packet_clause 0 10 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true false (by decide +kernel)) (by decide +kernel)

-- Clause 361: convex_four; source clause 64267.
private theorem sound360 : C.clause (decodeClause atoms clause360) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 362: convex_four; source clause 64475.
private theorem sound361 : C.clause (decodeClause atoms clause361) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 363: convex_four; source clause 64683.
private theorem sound362 : C.clause (decodeClause atoms clause362) := by
  exact C.covered_clause _ _ (C.convex_clause 0 6 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 364: packet; source clause 64997.
private theorem sound363 : C.clause (decodeClause atoms clause363) := by
  exact C.covered_clause _ _ (C.packet_clause 8 0 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 365: convex_four; source clause 65093.
private theorem sound364 : C.clause (decodeClause atoms clause364) := by
  exact C.covered_clause _ _ (C.convex_clause 0 7 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false) (by decide +kernel)

-- Clause 366: packet; source clause 66784.
private theorem sound365 : C.clause (decodeClause atoms clause365) := by
  exact C.covered_clause _ _ (C.packet_clause 0 9 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 367: packet; source clause 66992.
private theorem sound366 : C.clause (decodeClause atoms clause366) := by
  exact C.covered_clause _ _ (C.packet_clause 0 9 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 368: convex_four; source clause 67170.
private theorem sound367 : C.clause (decodeClause atoms clause367) := by
  exact C.covered_clause _ _ (C.convex_clause 0 8 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 369: packet; source clause 67189.
private theorem sound368 : C.clause (decodeClause atoms clause368) := by
  exact C.covered_clause _ _ (C.packet_clause 0 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 370: convex_four; source clause 67378.
private theorem sound369 : C.clause (decodeClause atoms clause369) := by
  exact C.covered_clause _ _ (C.convex_clause 0 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 371: packet; source clause 67605.
private theorem sound370 : C.clause (decodeClause atoms clause370) := by
  exact C.covered_clause _ _ (C.packet_clause 0 8 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 372: packet; source clause 67653.
private theorem sound371 : C.clause (decodeClause atoms clause371) := by
  exact C.covered_clause _ _ (C.packet_clause 8 0 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 373: packet; source clause 67808.
private theorem sound372 : C.clause (decodeClause atoms clause372) := by
  exact C.covered_clause _ _ (C.packet_clause 0 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 374: convex_four; source clause 67999.
private theorem sound373 : C.clause (decodeClause atoms clause373) := by
  exact C.covered_clause _ _ (C.convex_clause 0 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 375: convex_four; source clause 68219.
private theorem sound374 : C.clause (decodeClause atoms clause374) := by
  exact C.covered_clause _ _ (C.convex_clause 0 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 376: packet; source clause 68245.
private theorem sound375 : C.clause (decodeClause atoms clause375) := by
  exact C.covered_clause _ _ (C.packet_clause 0 10 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 377: convex_four; source clause 68427.
private theorem sound376 : C.clause (decodeClause atoms clause376) := by
  exact C.covered_clause _ _ (C.convex_clause 0 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 378: convex_four; source clause 68635.
private theorem sound377 : C.clause (decodeClause atoms clause377) := by
  exact C.covered_clause _ _ (C.convex_clause 0 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 379: packet; source clause 68640.
private theorem sound378 : C.clause (decodeClause atoms clause378) := by
  exact C.covered_clause _ _ (C.packet_clause 0 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 380: packet; source clause 68659.
private theorem sound379 : C.clause (decodeClause atoms clause379) := by
  exact C.covered_clause _ _ (C.packet_clause 0 11 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 381: packet; source clause 68661.
private theorem sound380 : C.clause (decodeClause atoms clause380) := by
  exact C.covered_clause _ _ (C.packet_clause 0 11 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 382: convex_four; source clause 68831.
private theorem sound381 : C.clause (decodeClause atoms clause381) := by
  exact C.covered_clause _ _ (C.convex_clause 0 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 383: convex_four; source clause 69262.
private theorem sound382 : C.clause (decodeClause atoms clause382) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 384: convex_four; source clause 69678.
private theorem sound383 : C.clause (decodeClause atoms clause383) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 385: convex_four; source clause 69886.
private theorem sound384 : C.clause (decodeClause atoms clause384) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 386: convex_four; source clause 70302.
private theorem sound385 : C.clause (decodeClause atoms clause385) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 387: packet; source clause 70307.
private theorem sound386 : C.clause (decodeClause atoms clause386) := by
  exact C.covered_clause _ _ (C.packet_clause 1 2 3 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 388: packet; source clause 70310.
private theorem sound387 : C.clause (decodeClause atoms clause387) := by
  exact C.covered_clause _ _ (C.packet_clause 1 2 3 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 389: packet; source clause 70341.
private theorem sound388 : C.clause (decodeClause atoms clause388) := by
  exact C.covered_clause _ _ (C.packet_clause 1 11 2 3 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 390: convex_four; source clause 70510.
private theorem sound389 : C.clause (decodeClause atoms clause389) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 3 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 391: convex_four; source clause 72798.
private theorem sound390 : C.clause (decodeClause atoms clause390) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 392: convex_four; source clause 73006.
private theorem sound391 : C.clause (decodeClause atoms clause391) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 393: convex_four; source clause 73422.
private theorem sound392 : C.clause (decodeClause atoms clause392) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 394: packet; source clause 73430.
private theorem sound393 : C.clause (decodeClause atoms clause393) := by
  exact C.covered_clause _ _ (C.packet_clause 1 2 5 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 395: convex_four; source clause 73630.
private theorem sound394 : C.clause (decodeClause atoms clause394) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 5 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 396: convex_four; source clause 75294.
private theorem sound395 : C.clause (decodeClause atoms clause395) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 397: convex_four; source clause 75710.
private theorem sound396 : C.clause (decodeClause atoms clause396) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 398: convex_four; source clause 75918.
private theorem sound397 : C.clause (decodeClause atoms clause397) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 399: convex_four; source clause 76539.
private theorem sound398 : C.clause (decodeClause atoms clause398) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 400: packet; source clause 76671.
private theorem sound399 : C.clause (decodeClause atoms clause399) := by
  exact C.covered_clause _ _ (C.packet_clause 8 11 1 2 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 401: convex_four; source clause 76747.
private theorem sound400 : C.clause (decodeClause atoms clause400) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 402: packet; source clause 77592.
private theorem sound401 : C.clause (decodeClause atoms clause401) := by
  exact C.covered_clause _ _ (C.packet_clause 1 2 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 403: convex_four; source clause 77790.
private theorem sound402 : C.clause (decodeClause atoms clause402) := by
  exact C.covered_clause _ _ (C.convex_clause 1 2 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 404: packet; source clause 79491.
private theorem sound403 : C.clause (decodeClause atoms clause403) := by
  exact C.covered_clause _ _ (C.packet_clause 1 11 3 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 405: packet; source clause 79602.
private theorem sound404 : C.clause (decodeClause atoms clause404) := by
  exact C.covered_clause _ _ (C.packet_clause 11 1 3 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 406: convex_four; source clause 80286.
private theorem sound405 : C.clause (decodeClause atoms clause405) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 407: convex_four; source clause 80494.
private theorem sound406 : C.clause (decodeClause atoms clause406) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 408: convex_four; source clause 80910.
private theorem sound407 : C.clause (decodeClause atoms clause407) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 409: convex_four; source clause 81118.
private theorem sound408 : C.clause (decodeClause atoms clause408) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 5 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 410: convex_four; source clause 82782.
private theorem sound409 : C.clause (decodeClause atoms clause409) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 411: convex_four; source clause 83198.
private theorem sound410 : C.clause (decodeClause atoms clause410) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 412: packet; source clause 83208.
private theorem sound411 : C.clause (decodeClause atoms clause411) := by
  exact C.covered_clause _ _ (C.packet_clause 1 3 11 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 413: convex_four; source clause 83406.
private theorem sound412 : C.clause (decodeClause atoms clause412) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 414: convex_four; source clause 84027.
private theorem sound413 : C.clause (decodeClause atoms clause413) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 415: convex_four; source clause 84235.
private theorem sound414 : C.clause (decodeClause atoms clause414) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 416: packet; source clause 85080.
private theorem sound415 : C.clause (decodeClause atoms clause415) := by
  exact C.covered_clause _ _ (C.packet_clause 1 3 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 417: convex_four; source clause 85278.
private theorem sound416 : C.clause (decodeClause atoms clause416) := by
  exact C.covered_clause _ _ (C.convex_clause 1 3 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 418: convex_four; source clause 87566.
private theorem sound417 : C.clause (decodeClause atoms clause417) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 6 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 419: convex_four; source clause 87774.
private theorem sound418 : C.clause (decodeClause atoms clause418) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 6 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 420: convex_four; source clause 87982.
private theorem sound419 : C.clause (decodeClause atoms clause419) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 6 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 421: convex_four; source clause 88190.
private theorem sound420 : C.clause (decodeClause atoms clause420) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 6 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 422: convex_four; source clause 88398.
private theorem sound421 : C.clause (decodeClause atoms clause421) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 6 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 423: convex_four; source clause 89643.
private theorem sound422 : C.clause (decodeClause atoms clause422) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 424: convex_four; source clause 90059.
private theorem sound423 : C.clause (decodeClause atoms clause423) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 425: convex_four; source clause 90267.
private theorem sound424 : C.clause (decodeClause atoms clause424) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 426: convex_four; source clause 90478.
private theorem sound425 : C.clause (decodeClause atoms clause425) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 427: convex_four; source clause 90686.
private theorem sound426 : C.clause (decodeClause atoms clause426) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 428: convex_four; source clause 90894.
private theorem sound427 : C.clause (decodeClause atoms clause427) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 429: packet; source clause 90911.
private theorem sound428 : C.clause (decodeClause atoms clause428) := by
  exact C.covered_clause _ _ (C.packet_clause 1 10 4 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 430: convex_four; source clause 91099.
private theorem sound429 : C.clause (decodeClause atoms clause429) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 431: convex_four; source clause 91307.
private theorem sound430 : C.clause (decodeClause atoms clause430) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 432: convex_four; source clause 91515.
private theorem sound431 : C.clause (decodeClause atoms clause431) := by
  exact C.covered_clause _ _ (C.convex_clause 1 4 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 433: packet; source clause 92387.
private theorem sound432 : C.clause (decodeClause atoms clause432) := by
  exact C.covered_clause _ _ (C.packet_clause 1 11 5 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 434: packet; source clause 92498.
private theorem sound433 : C.clause (decodeClause atoms clause433) := by
  exact C.covered_clause _ _ (C.packet_clause 11 1 5 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 435: convex_four; source clause 92974.
private theorem sound434 : C.clause (decodeClause atoms clause434) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 436: convex_four; source clause 93390.
private theorem sound435 : C.clause (decodeClause atoms clause435) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 437: convex_four; source clause 93598.
private theorem sound436 : C.clause (decodeClause atoms clause436) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 438: convex_four; source clause 94219.
private theorem sound437 : C.clause (decodeClause atoms clause437) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 439: convex_four; source clause 94427.
private theorem sound438 : C.clause (decodeClause atoms clause438) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 440: convex_four; source clause 95466.
private theorem sound439 : C.clause (decodeClause atoms clause439) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 441: convex_four; source clause 95470.
private theorem sound440 : C.clause (decodeClause atoms clause440) := by
  exact C.covered_clause _ _ (C.convex_clause 1 5 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 442: convex_four; source clause 97131.
private theorem sound441 : C.clause (decodeClause atoms clause441) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 443: convex_four; source clause 97547.
private theorem sound442 : C.clause (decodeClause atoms clause442) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 444: convex_four; source clause 97755.
private theorem sound443 : C.clause (decodeClause atoms clause443) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 445: convex_four; source clause 97966.
private theorem sound444 : C.clause (decodeClause atoms clause444) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 446: convex_four; source clause 98174.
private theorem sound445 : C.clause (decodeClause atoms clause445) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 447: convex_four; source clause 98382.
private theorem sound446 : C.clause (decodeClause atoms clause446) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 448: packet; source clause 98390.
private theorem sound447 : C.clause (decodeClause atoms clause447) := by
  exact C.covered_clause _ _ (C.packet_clause 1 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 449: convex_four; source clause 98587.
private theorem sound448 : C.clause (decodeClause atoms clause448) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 450: convex_four; source clause 98795.
private theorem sound449 : C.clause (decodeClause atoms clause449) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 451: convex_four; source clause 99003.
private theorem sound450 : C.clause (decodeClause atoms clause450) := by
  exact C.covered_clause _ _ (C.convex_clause 1 6 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 452: convex_four; source clause 99419.
private theorem sound451 : C.clause (decodeClause atoms clause451) := by
  exact C.covered_clause _ _ (C.convex_clause 1 7 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 453: packet; source clause 99534.
private theorem sound452 : C.clause (decodeClause atoms clause452) := by
  exact C.covered_clause _ _ (C.packet_clause 8 1 11 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 454: packet; source clause 99551.
private theorem sound453 : C.clause (decodeClause atoms clause453) := by
  exact C.covered_clause _ _ (C.packet_clause 8 11 1 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 455: convex_four; source clause 99627.
private theorem sound454 : C.clause (decodeClause atoms clause454) := by
  exact C.covered_clause _ _ (C.convex_clause 1 7 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 456: packet; source clause 100472.
private theorem sound455 : C.clause (decodeClause atoms clause455) := by
  exact C.covered_clause _ _ (C.packet_clause 1 7 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 457: convex_four; source clause 100666.
private theorem sound456 : C.clause (decodeClause atoms clause456) := by
  exact C.covered_clause _ _ (C.convex_clause 1 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 458: convex_four; source clause 100670.
private theorem sound457 : C.clause (decodeClause atoms clause457) := by
  exact C.covered_clause _ _ (C.convex_clause 1 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 459: packet; source clause 101110.
private theorem sound458 : C.clause (decodeClause atoms clause458) := by
  exact C.covered_clause _ _ (C.packet_clause 1 9 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 460: convex_four; source clause 101490.
private theorem sound459 : C.clause (decodeClause atoms clause459) := by
  exact C.covered_clause _ _ (C.convex_clause 1 8 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 461: convex_four; source clause 101698.
private theorem sound460 : C.clause (decodeClause atoms clause460) := by
  exact C.covered_clause _ _ (C.convex_clause 1 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 462: packet; source clause 101774.
private theorem sound461 : C.clause (decodeClause atoms clause461) := by
  exact C.covered_clause _ _ (C.packet_clause 8 1 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 463: packet; source clause 101791.
private theorem sound462 : C.clause (decodeClause atoms clause462) := by
  exact C.covered_clause _ _ (C.packet_clause 8 11 1 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 464: convex_four; source clause 101906.
private theorem sound463 : C.clause (decodeClause atoms clause463) := by
  exact C.covered_clause _ _ (C.convex_clause 1 8 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 465: convex_four; source clause 102319.
private theorem sound464 : C.clause (decodeClause atoms clause464) := by
  exact C.covered_clause _ _ (C.convex_clause 1 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 466: packet; source clause 102351.
private theorem sound465 : C.clause (decodeClause atoms clause465) := by
  exact C.covered_clause _ _ (C.packet_clause 1 10 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 467: packet; source clause 102354.
private theorem sound466 : C.clause (decodeClause atoms clause466) := by
  exact C.covered_clause _ _ (C.packet_clause 1 10 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 468: convex_four; source clause 102539.
private theorem sound467 : C.clause (decodeClause atoms clause467) := by
  exact C.covered_clause _ _ (C.convex_clause 1 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 469: convex_four; source clause 102747.
private theorem sound468 : C.clause (decodeClause atoms clause468) := by
  exact C.covered_clause _ _ (C.convex_clause 1 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 470: convex_four; source clause 102955.
private theorem sound469 : C.clause (decodeClause atoms clause469) := by
  exact C.covered_clause _ _ (C.convex_clause 1 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 471: convex_four; source clause 103151.
private theorem sound470 : C.clause (decodeClause atoms clause470) := by
  exact C.covered_clause _ _ (C.convex_clause 1 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 472: packet; source clause 104451.
private theorem sound471 : C.clause (decodeClause atoms clause471) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 3 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 473: packet; source clause 104562.
private theorem sound472 : C.clause (decodeClause atoms clause472) := by
  exact C.covered_clause _ _ (C.packet_clause 11 2 3 4 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 474: convex_four; source clause 105246.
private theorem sound473 : C.clause (decodeClause atoms clause473) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 475: convex_four; source clause 105454.
private theorem sound474 : C.clause (decodeClause atoms clause474) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 5 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 476: convex_four; source clause 105870.
private theorem sound475 : C.clause (decodeClause atoms clause475) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 477: convex_four; source clause 106078.
private theorem sound476 : C.clause (decodeClause atoms clause476) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 5 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 478: convex_four; source clause 107742.
private theorem sound477 : C.clause (decodeClause atoms clause477) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 479: convex_four; source clause 108158.
private theorem sound478 : C.clause (decodeClause atoms clause478) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 480: convex_four; source clause 108366.
private theorem sound479 : C.clause (decodeClause atoms clause479) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 481: convex_four; source clause 108987.
private theorem sound480 : C.clause (decodeClause atoms clause480) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 482: convex_four; source clause 109195.
private theorem sound481 : C.clause (decodeClause atoms clause481) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 483: packet; source clause 109651.
private theorem sound482 : C.clause (decodeClause atoms clause482) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 3 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 484: packet; source clause 109653.
private theorem sound483 : C.clause (decodeClause atoms clause483) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 3 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 485: packet; source clause 110040.
private theorem sound484 : C.clause (decodeClause atoms clause484) := by
  exact C.covered_clause _ _ (C.packet_clause 2 3 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 486: convex_four; source clause 110238.
private theorem sound485 : C.clause (decodeClause atoms clause485) := by
  exact C.covered_clause _ _ (C.convex_clause 2 3 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 487: packet; source clause 117347.
private theorem sound486 : C.clause (decodeClause atoms clause486) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 5 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 488: packet; source clause 117458.
private theorem sound487 : C.clause (decodeClause atoms clause487) := by
  exact C.covered_clause _ _ (C.packet_clause 11 2 5 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 489: convex_four; source clause 117934.
private theorem sound488 : C.clause (decodeClause atoms clause488) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 490: convex_four; source clause 118350.
private theorem sound489 : C.clause (decodeClause atoms clause489) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 491: convex_four; source clause 118558.
private theorem sound490 : C.clause (decodeClause atoms clause490) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 492: convex_four; source clause 119179.
private theorem sound491 : C.clause (decodeClause atoms clause491) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 493: convex_four; source clause 119387.
private theorem sound492 : C.clause (decodeClause atoms clause492) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 494: packet; source clause 120232.
private theorem sound493 : C.clause (decodeClause atoms clause493) := by
  exact C.covered_clause _ _ (C.packet_clause 2 5 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 495: convex_four; source clause 120426.
private theorem sound494 : C.clause (decodeClause atoms clause494) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true) (by decide +kernel)

-- Clause 496: convex_four; source clause 120430.
private theorem sound495 : C.clause (decodeClause atoms clause495) := by
  exact C.covered_clause _ _ (C.convex_clause 2 5 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 497: convex_four; source clause 124379.
private theorem sound496 : C.clause (decodeClause atoms clause496) := by
  exact C.covered_clause _ _ (C.convex_clause 2 7 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 498: packet; source clause 124494.
private theorem sound497 : C.clause (decodeClause atoms clause497) := by
  exact C.covered_clause _ _ (C.packet_clause 8 2 11 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 499: packet; source clause 124511.
private theorem sound498 : C.clause (decodeClause atoms clause498) := by
  exact C.covered_clause _ _ (C.packet_clause 8 11 2 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 500: convex_four; source clause 124587.
private theorem sound499 : C.clause (decodeClause atoms clause499) := by
  exact C.covered_clause _ _ (C.convex_clause 2 7 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 501: packet; source clause 125432.
private theorem sound500 : C.clause (decodeClause atoms clause500) := by
  exact C.covered_clause _ _ (C.packet_clause 2 7 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 502: convex_four; source clause 125630.
private theorem sound501 : C.clause (decodeClause atoms clause501) := by
  exact C.covered_clause _ _ (C.convex_clause 2 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 503: packet; source clause 126734.
private theorem sound502 : C.clause (decodeClause atoms clause502) := by
  exact C.covered_clause _ _ (C.packet_clause 8 2 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 504: packet; source clause 126751.
private theorem sound503 : C.clause (decodeClause atoms clause503) := by
  exact C.covered_clause _ _ (C.packet_clause 8 11 2 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 505: convex_four; source clause 126866.
private theorem sound504 : C.clause (decodeClause atoms clause504) := by
  exact C.covered_clause _ _ (C.convex_clause 2 8 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 506: packet; source clause 127339.
private theorem sound505 : C.clause (decodeClause atoms clause505) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 10 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 507: packet; source clause 127939.
private theorem sound506 : C.clause (decodeClause atoms clause506) := by
  exact C.covered_clause _ _ (C.packet_clause 2 11 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 508: packet; source clause 134930.
private theorem sound507 : C.clause (decodeClause atoms clause507) := by
  exact C.covered_clause _ _ (C.packet_clause 11 3 5 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 509: convex_four; source clause 135406.
private theorem sound508 : C.clause (decodeClause atoms clause508) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 7 8 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 510: convex_four; source clause 135822.
private theorem sound509 : C.clause (decodeClause atoms clause509) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 511: packet; source clause 135832.
private theorem sound510 : C.clause (decodeClause atoms clause510) := by
  exact C.covered_clause _ _ (C.packet_clause 3 5 11 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 512: convex_four; source clause 136030.
private theorem sound511 : C.clause (decodeClause atoms clause511) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 7 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 513: convex_four; source clause 136651.
private theorem sound512 : C.clause (decodeClause atoms clause512) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 514: packet; source clause 136766.
private theorem sound513 : C.clause (decodeClause atoms clause513) := by
  exact C.covered_clause _ _ (C.packet_clause 8 3 11 5 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 515: convex_four; source clause 136859.
private theorem sound514 : C.clause (decodeClause atoms clause514) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 516: packet; source clause 137704.
private theorem sound515 : C.clause (decodeClause atoms clause515) := by
  exact C.covered_clause _ _ (C.packet_clause 3 5 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 517: convex_four; source clause 137902.
private theorem sound516 : C.clause (decodeClause atoms clause516) := by
  exact C.covered_clause _ _ (C.convex_clause 3 5 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 518: convex_four; source clause 141851.
private theorem sound517 : C.clause (decodeClause atoms clause517) := by
  exact C.covered_clause _ _ (C.convex_clause 3 7 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 519: packet; source clause 141966.
private theorem sound518 : C.clause (decodeClause atoms clause518) := by
  exact C.covered_clause _ _ (C.packet_clause 8 3 11 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 520: packet; source clause 141983.
private theorem sound519 : C.clause (decodeClause atoms clause519) := by
  exact C.covered_clause _ _ (C.packet_clause 8 11 3 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 521: convex_four; source clause 142059.
private theorem sound520 : C.clause (decodeClause atoms clause520) := by
  exact C.covered_clause _ _ (C.convex_clause 3 7 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 522: packet; source clause 142515.
private theorem sound521 : C.clause (decodeClause atoms clause521) := by
  exact C.covered_clause _ _ (C.packet_clause 3 11 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 523: packet; source clause 142904.
private theorem sound522 : C.clause (decodeClause atoms clause522) := by
  exact C.covered_clause _ _ (C.packet_clause 3 7 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 524: convex_four; source clause 143102.
private theorem sound523 : C.clause (decodeClause atoms clause523) := by
  exact C.covered_clause _ _ (C.convex_clause 3 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 525: packet; source clause 144206.
private theorem sound524 : C.clause (decodeClause atoms clause524) := by
  exact C.covered_clause _ _ (C.packet_clause 8 3 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 526: packet; source clause 144223.
private theorem sound525 : C.clause (decodeClause atoms clause525) := by
  exact C.covered_clause _ _ (C.packet_clause 8 11 3 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 527: convex_four; source clause 144338.
private theorem sound526 : C.clause (decodeClause atoms clause526) := by
  exact C.covered_clause _ _ (C.convex_clause 3 8 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 528: packet; source clause 145411.
private theorem sound527 : C.clause (decodeClause atoms clause527) := by
  exact C.covered_clause _ _ (C.packet_clause 3 11 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 529: convex_four; source clause 151211.
private theorem sound528 : C.clause (decodeClause atoms clause528) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 8 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 530: convex_four; source clause 151627.
private theorem sound529 : C.clause (decodeClause atoms clause529) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 531: convex_four; source clause 151835.
private theorem sound530 : C.clause (decodeClause atoms clause530) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 8 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 532: convex_four; source clause 152046.
private theorem sound531 : C.clause (decodeClause atoms clause531) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 533: convex_four; source clause 152254.
private theorem sound532 : C.clause (decodeClause atoms clause532) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 534: convex_four; source clause 152462.
private theorem sound533 : C.clause (decodeClause atoms clause533) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 535: packet; source clause 152597.
private theorem sound534 : C.clause (decodeClause atoms clause534) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 4 6 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 536: convex_four; source clause 152667.
private theorem sound535 : C.clause (decodeClause atoms clause535) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 537: convex_four; source clause 152875.
private theorem sound536 : C.clause (decodeClause atoms clause536) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 538: convex_four; source clause 153083.
private theorem sound537 : C.clause (decodeClause atoms clause537) := by
  exact C.covered_clause _ _ (C.convex_clause 4 6 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 539: convex_four; source clause 155570.
private theorem sound538 : C.clause (decodeClause atoms clause538) := by
  exact C.covered_clause _ _ (C.convex_clause 4 8 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 540: convex_four; source clause 155778.
private theorem sound539 : C.clause (decodeClause atoms clause539) := by
  exact C.covered_clause _ _ (C.convex_clause 4 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 541: convex_four; source clause 156399.
private theorem sound540 : C.clause (decodeClause atoms clause540) := by
  exact C.covered_clause _ _ (C.convex_clause 4 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 542: convex_four; source clause 156619.
private theorem sound541 : C.clause (decodeClause atoms clause541) := by
  exact C.covered_clause _ _ (C.convex_clause 4 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 543: convex_four; source clause 156827.
private theorem sound542 : C.clause (decodeClause atoms clause542) := by
  exact C.covered_clause _ _ (C.convex_clause 4 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 544: convex_four; source clause 157035.
private theorem sound543 : C.clause (decodeClause atoms clause543) := by
  exact C.covered_clause _ _ (C.convex_clause 4 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 545: convex_four; source clause 157231.
private theorem sound544 : C.clause (decodeClause atoms clause544) := by
  exact C.covered_clause _ _ (C.convex_clause 4 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 546: convex_four; source clause 157239.
private theorem sound545 : C.clause (decodeClause atoms clause545) := by
  exact C.covered_clause _ _ (C.convex_clause 4 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 547: packet; source clause 159750.
private theorem sound546 : C.clause (decodeClause atoms clause546) := by
  exact C.covered_clause _ _ (C.packet_clause 5 6 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 548: convex_four; source clause 160779.
private theorem sound547 : C.clause (decodeClause atoms clause547) := by
  exact C.covered_clause _ _ (C.convex_clause 5 7 8 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 549: packet; source clause 160911.
private theorem sound548 : C.clause (decodeClause atoms clause548) := by
  exact C.covered_clause _ _ (C.packet_clause 8 11 5 7 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 550: convex_four; source clause 160987.
private theorem sound549 : C.clause (decodeClause atoms clause549) := by
  exact C.covered_clause _ _ (C.convex_clause 5 7 8 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 551: packet; source clause 161443.
private theorem sound550 : C.clause (decodeClause atoms clause550) := by
  exact C.covered_clause _ _ (C.packet_clause 5 11 7 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 552: packet; source clause 161832.
private theorem sound551 : C.clause (decodeClause atoms clause551) := by
  exact C.covered_clause _ _ (C.packet_clause 5 7 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true false false (by decide +kernel)) (by decide +kernel)

-- Clause 553: convex_four; source clause 162030.
private theorem sound552 : C.clause (decodeClause atoms clause552) := by
  exact C.covered_clause _ _ (C.convex_clause 5 7 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true true true) (by decide +kernel)

-- Clause 554: packet; source clause 163151.
private theorem sound553 : C.clause (decodeClause atoms clause553) := by
  exact C.covered_clause _ _ (C.packet_clause 8 11 5 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 555: convex_four; source clause 163266.
private theorem sound554 : C.clause (decodeClause atoms clause554) := by
  exact C.covered_clause _ _ (C.convex_clause 5 8 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 556: packet; source clause 164339.
private theorem sound555 : C.clause (decodeClause atoms clause555) := by
  exact C.covered_clause _ _ (C.packet_clause 5 11 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 557: convex_four; source clause 167010.
private theorem sound556 : C.clause (decodeClause atoms clause556) := by
  exact C.covered_clause _ _ (C.convex_clause 6 8 9 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 558: convex_four; source clause 167218.
private theorem sound557 : C.clause (decodeClause atoms clause557) := by
  exact C.covered_clause _ _ (C.convex_clause 6 8 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 559: convex_four; source clause 167839.
private theorem sound558 : C.clause (decodeClause atoms clause558) := by
  exact C.covered_clause _ _ (C.convex_clause 6 8 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 560: packet; source clause 167989.
private theorem sound559 : C.clause (decodeClause atoms clause559) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 6 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 561: convex_four; source clause 168059.
private theorem sound560 : C.clause (decodeClause atoms clause560) := by
  exact C.covered_clause _ _ (C.convex_clause 6 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 562: convex_four; source clause 168267.
private theorem sound561 : C.clause (decodeClause atoms clause561) := by
  exact C.covered_clause _ _ (C.convex_clause 6 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 563: convex_four; source clause 168475.
private theorem sound562 : C.clause (decodeClause atoms clause562) := by
  exact C.covered_clause _ _ (C.convex_clause 6 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 564: convex_four; source clause 168671.
private theorem sound563 : C.clause (decodeClause atoms clause563) := by
  exact C.covered_clause _ _ (C.convex_clause 6 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 565: convex_four; source clause 168679.
private theorem sound564 : C.clause (decodeClause atoms clause564) := by
  exact C.covered_clause _ _ (C.convex_clause 6 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 566: packet; source clause 169391.
private theorem sound565 : C.clause (decodeClause atoms clause565) := by
  exact C.covered_clause _ _ (C.packet_clause 8 11 7 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 567: convex_four; source clause 169506.
private theorem sound566 : C.clause (decodeClause atoms clause566) := by
  exact C.covered_clause _ _ (C.convex_clause 7 8 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true true) (by decide +kernel)

-- Clause 568: packet; source clause 169942.
private theorem sound567 : C.clause (decodeClause atoms clause567) := by
  exact C.covered_clause _ _ (C.packet_clause 7 9 10 11 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 569: packet; source clause 169950.
private theorem sound568 : C.clause (decodeClause atoms clause568) := by
  exact C.covered_clause _ _ (C.packet_clause 7 9 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false true (by decide +kernel)) (by decide +kernel)

-- Clause 570: packet; source clause 169979.
private theorem sound569 : C.clause (decodeClause atoms clause569) := by
  exact C.covered_clause _ _ (C.packet_clause 7 11 10 9 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 571: packet; source clause 170579.
private theorem sound570 : C.clause (decodeClause atoms clause570) := by
  exact C.covered_clause _ _ (C.packet_clause 7 11 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false true (by decide +kernel)) (by decide +kernel)

-- Clause 572: packet; source clause 170799.
private theorem sound571 : C.clause (decodeClause atoms clause571) := by
  exact C.covered_clause _ _ (C.packet_clause 8 11 9 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 573: packet; source clause 170823.
private theorem sound572 : C.clause (decodeClause atoms clause572) := by
  exact C.covered_clause _ _ (C.packet_clause 9 8 11 10 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false true false (by decide +kernel)) (by decide +kernel)

-- Clause 574: packet; source clause 170978.
private theorem sound573 : C.clause (decodeClause atoms clause573) := by
  exact C.covered_clause _ _ (C.packet_clause 8 9 10 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false true true false (by decide +kernel)) (by decide +kernel)

-- Clause 575: convex_four; source clause 171387.
private theorem sound574 : C.clause (decodeClause atoms clause574) := by
  exact C.covered_clause _ _ (C.convex_clause 8 9 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true true false false) (by decide +kernel)

-- Clause 576: packet; source clause 171669.
private theorem sound575 : C.clause (decodeClause atoms clause575) := by
  exact C.covered_clause _ _ (C.packet_clause 10 11 9 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false true true (by decide +kernel)) (by decide +kernel)

-- Clause 577: convex_four; source clause 171791.
private theorem sound576 : C.clause (decodeClause atoms clause576) := by
  exact C.covered_clause _ _ (C.convex_clause 9 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) false false false false) (by decide +kernel)

-- Clause 578: convex_four; source clause 171799.
private theorem sound577 : C.clause (decodeClause atoms clause577) := by
  exact C.covered_clause _ _ (C.convex_clause 9 10 11 12 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) true false false false) (by decide +kernel)

-- Clause 579: no_octagon; source clause 171809.
private theorem sound578 : C.clause (decodeClause atoms clause578) := by
  exact C.no_octagon_clause {0, 1, 2, 3, 5, 7, 8, 10} (by decide +kernel) _ (by decide +kernel)

-- Clause 580: no_octagon; source clause 171817.
private theorem sound579 : C.clause (decodeClause atoms clause579) := by
  exact C.no_octagon_clause {0, 1, 4, 6, 8, 9, 11, 12} (by decide +kernel) _ (by decide +kernel)

-- Clause 581: no_octagon; source clause 171818.
private theorem sound580 : C.clause (decodeClause atoms clause580) := by
  exact C.no_octagon_clause {0, 1, 4, 6, 9, 10, 11, 12} (by decide +kernel) _ (by decide +kernel)

-- Clause 582: no_octagon; source clause 171824.
private theorem sound581 : C.clause (decodeClause atoms clause581) := by
  exact C.no_octagon_clause {1, 2, 3, 5, 7, 8, 10, 11} (by decide +kernel) _ (by decide +kernel)

private theorem all_sound : List.Forall (fun cl => C.clause (decodeClause atoms cl)) clauses := by
  exact And.intro (sound000 C) (And.intro (sound001 C) (And.intro (sound002 C) (And.intro (sound003 C) (And.intro (sound004 C) (And.intro (sound005 C) (And.intro (sound006 C) (And.intro (sound007 C) (And.intro (sound008 C) (And.intro (sound009 C) (And.intro (sound010 C) (And.intro (sound011 C) (And.intro (sound012 C) (And.intro (sound013 C) (And.intro (sound014 C) (And.intro (sound015 C) (And.intro (sound016 C) (And.intro (sound017 C) (And.intro (sound018 C) (And.intro (sound019 C) (And.intro (sound020 C) (And.intro (sound021 C) (And.intro (sound022 C) (And.intro (sound023 C) (And.intro (sound024 C) (And.intro (sound025 C) (And.intro (sound026 C) (And.intro (sound027 C) (And.intro (sound028 C) (And.intro (sound029 C) (And.intro (sound030 C) (And.intro (sound031 C) (And.intro (sound032 C) (And.intro (sound033 C) (And.intro (sound034 C) (And.intro (sound035 C) (And.intro (sound036 C) (And.intro (sound037 C) (And.intro (sound038 C) (And.intro (sound039 C) (And.intro (sound040 C) (And.intro (sound041 C) (And.intro (sound042 C) (And.intro (sound043 C) (And.intro (sound044 C) (And.intro (sound045 C) (And.intro (sound046 C) (And.intro (sound047 C) (And.intro (sound048 C) (And.intro (sound049 C) (And.intro (sound050 C) (And.intro (sound051 C) (And.intro (sound052 C) (And.intro (sound053 C) (And.intro (sound054 C) (And.intro (sound055 C) (And.intro (sound056 C) (And.intro (sound057 C) (And.intro (sound058 C) (And.intro (sound059 C) (And.intro (sound060 C) (And.intro (sound061 C) (And.intro (sound062 C) (And.intro (sound063 C) (And.intro (sound064 C) (And.intro (sound065 C) (And.intro (sound066 C) (And.intro (sound067 C) (And.intro (sound068 C) (And.intro (sound069 C) (And.intro (sound070 C) (And.intro (sound071 C) (And.intro (sound072 C) (And.intro (sound073 C) (And.intro (sound074 C) (And.intro (sound075 C) (And.intro (sound076 C) (And.intro (sound077 C) (And.intro (sound078 C) (And.intro (sound079 C) (And.intro (sound080 C) (And.intro (sound081 C) (And.intro (sound082 C) (And.intro (sound083 C) (And.intro (sound084 C) (And.intro (sound085 C) (And.intro (sound086 C) (And.intro (sound087 C) (And.intro (sound088 C) (And.intro (sound089 C) (And.intro (sound090 C) (And.intro (sound091 C) (And.intro (sound092 C) (And.intro (sound093 C) (And.intro (sound094 C) (And.intro (sound095 C) (And.intro (sound096 C) (And.intro (sound097 C) (And.intro (sound098 C) (And.intro (sound099 C) (And.intro (sound100 C) (And.intro (sound101 C) (And.intro (sound102 C) (And.intro (sound103 C) (And.intro (sound104 C) (And.intro (sound105 C) (And.intro (sound106 C) (And.intro (sound107 C) (And.intro (sound108 C) (And.intro (sound109 C) (And.intro (sound110 C) (And.intro (sound111 C) (And.intro (sound112 C) (And.intro (sound113 C) (And.intro (sound114 C) (And.intro (sound115 C) (And.intro (sound116 C) (And.intro (sound117 C) (And.intro (sound118 C) (And.intro (sound119 C) (And.intro (sound120 C) (And.intro (sound121 C) (And.intro (sound122 C) (And.intro (sound123 C) (And.intro (sound124 C) (And.intro (sound125 C) (And.intro (sound126 C) (And.intro (sound127 C) (And.intro (sound128 C) (And.intro (sound129 C) (And.intro (sound130 C) (And.intro (sound131 C) (And.intro (sound132 C) (And.intro (sound133 C) (And.intro (sound134 C) (And.intro (sound135 C) (And.intro (sound136 C) (And.intro (sound137 C) (And.intro (sound138 C) (And.intro (sound139 C) (And.intro (sound140 C) (And.intro (sound141 C) (And.intro (sound142 C) (And.intro (sound143 C) (And.intro (sound144 C) (And.intro (sound145 C) (And.intro (sound146 C) (And.intro (sound147 C) (And.intro (sound148 C) (And.intro (sound149 C) (And.intro (sound150 C) (And.intro (sound151 C) (And.intro (sound152 C) (And.intro (sound153 C) (And.intro (sound154 C) (And.intro (sound155 C) (And.intro (sound156 C) (And.intro (sound157 C) (And.intro (sound158 C) (And.intro (sound159 C) (And.intro (sound160 C) (And.intro (sound161 C) (And.intro (sound162 C) (And.intro (sound163 C) (And.intro (sound164 C) (And.intro (sound165 C) (And.intro (sound166 C) (And.intro (sound167 C) (And.intro (sound168 C) (And.intro (sound169 C) (And.intro (sound170 C) (And.intro (sound171 C) (And.intro (sound172 C) (And.intro (sound173 C) (And.intro (sound174 C) (And.intro (sound175 C) (And.intro (sound176 C) (And.intro (sound177 C) (And.intro (sound178 C) (And.intro (sound179 C) (And.intro (sound180 C) (And.intro (sound181 C) (And.intro (sound182 C) (And.intro (sound183 C) (And.intro (sound184 C) (And.intro (sound185 C) (And.intro (sound186 C) (And.intro (sound187 C) (And.intro (sound188 C) (And.intro (sound189 C) (And.intro (sound190 C) (And.intro (sound191 C) (And.intro (sound192 C) (And.intro (sound193 C) (And.intro (sound194 C) (And.intro (sound195 C) (And.intro (sound196 C) (And.intro (sound197 C) (And.intro (sound198 C) (And.intro (sound199 C) (And.intro (sound200 C) (And.intro (sound201 C) (And.intro (sound202 C) (And.intro (sound203 C) (And.intro (sound204 C) (And.intro (sound205 C) (And.intro (sound206 C) (And.intro (sound207 C) (And.intro (sound208 C) (And.intro (sound209 C) (And.intro (sound210 C) (And.intro (sound211 C) (And.intro (sound212 C) (And.intro (sound213 C) (And.intro (sound214 C) (And.intro (sound215 C) (And.intro (sound216 C) (And.intro (sound217 C) (And.intro (sound218 C) (And.intro (sound219 C) (And.intro (sound220 C) (And.intro (sound221 C) (And.intro (sound222 C) (And.intro (sound223 C) (And.intro (sound224 C) (And.intro (sound225 C) (And.intro (sound226 C) (And.intro (sound227 C) (And.intro (sound228 C) (And.intro (sound229 C) (And.intro (sound230 C) (And.intro (sound231 C) (And.intro (sound232 C) (And.intro (sound233 C) (And.intro (sound234 C) (And.intro (sound235 C) (And.intro (sound236 C) (And.intro (sound237 C) (And.intro (sound238 C) (And.intro (sound239 C) (And.intro (sound240 C) (And.intro (sound241 C) (And.intro (sound242 C) (And.intro (sound243 C) (And.intro (sound244 C) (And.intro (sound245 C) (And.intro (sound246 C) (And.intro (sound247 C) (And.intro (sound248 C) (And.intro (sound249 C) (And.intro (sound250 C) (And.intro (sound251 C) (And.intro (sound252 C) (And.intro (sound253 C) (And.intro (sound254 C) (And.intro (sound255 C) (And.intro (sound256 C) (And.intro (sound257 C) (And.intro (sound258 C) (And.intro (sound259 C) (And.intro (sound260 C) (And.intro (sound261 C) (And.intro (sound262 C) (And.intro (sound263 C) (And.intro (sound264 C) (And.intro (sound265 C) (And.intro (sound266 C) (And.intro (sound267 C) (And.intro (sound268 C) (And.intro (sound269 C) (And.intro (sound270 C) (And.intro (sound271 C) (And.intro (sound272 C) (And.intro (sound273 C) (And.intro (sound274 C) (And.intro (sound275 C) (And.intro (sound276 C) (And.intro (sound277 C) (And.intro (sound278 C) (And.intro (sound279 C) (And.intro (sound280 C) (And.intro (sound281 C) (And.intro (sound282 C) (And.intro (sound283 C) (And.intro (sound284 C) (And.intro (sound285 C) (And.intro (sound286 C) (And.intro (sound287 C) (And.intro (sound288 C) (And.intro (sound289 C) (And.intro (sound290 C) (And.intro (sound291 C) (And.intro (sound292 C) (And.intro (sound293 C) (And.intro (sound294 C) (And.intro (sound295 C) (And.intro (sound296 C) (And.intro (sound297 C) (And.intro (sound298 C) (And.intro (sound299 C) (And.intro (sound300 C) (And.intro (sound301 C) (And.intro (sound302 C) (And.intro (sound303 C) (And.intro (sound304 C) (And.intro (sound305 C) (And.intro (sound306 C) (And.intro (sound307 C) (And.intro (sound308 C) (And.intro (sound309 C) (And.intro (sound310 C) (And.intro (sound311 C) (And.intro (sound312 C) (And.intro (sound313 C) (And.intro (sound314 C) (And.intro (sound315 C) (And.intro (sound316 C) (And.intro (sound317 C) (And.intro (sound318 C) (And.intro (sound319 C) (And.intro (sound320 C) (And.intro (sound321 C) (And.intro (sound322 C) (And.intro (sound323 C) (And.intro (sound324 C) (And.intro (sound325 C) (And.intro (sound326 C) (And.intro (sound327 C) (And.intro (sound328 C) (And.intro (sound329 C) (And.intro (sound330 C) (And.intro (sound331 C) (And.intro (sound332 C) (And.intro (sound333 C) (And.intro (sound334 C) (And.intro (sound335 C) (And.intro (sound336 C) (And.intro (sound337 C) (And.intro (sound338 C) (And.intro (sound339 C) (And.intro (sound340 C) (And.intro (sound341 C) (And.intro (sound342 C) (And.intro (sound343 C) (And.intro (sound344 C) (And.intro (sound345 C) (And.intro (sound346 C) (And.intro (sound347 C) (And.intro (sound348 C) (And.intro (sound349 C) (And.intro (sound350 C) (And.intro (sound351 C) (And.intro (sound352 C) (And.intro (sound353 C) (And.intro (sound354 C) (And.intro (sound355 C) (And.intro (sound356 C) (And.intro (sound357 C) (And.intro (sound358 C) (And.intro (sound359 C) (And.intro (sound360 C) (And.intro (sound361 C) (And.intro (sound362 C) (And.intro (sound363 C) (And.intro (sound364 C) (And.intro (sound365 C) (And.intro (sound366 C) (And.intro (sound367 C) (And.intro (sound368 C) (And.intro (sound369 C) (And.intro (sound370 C) (And.intro (sound371 C) (And.intro (sound372 C) (And.intro (sound373 C) (And.intro (sound374 C) (And.intro (sound375 C) (And.intro (sound376 C) (And.intro (sound377 C) (And.intro (sound378 C) (And.intro (sound379 C) (And.intro (sound380 C) (And.intro (sound381 C) (And.intro (sound382 C) (And.intro (sound383 C) (And.intro (sound384 C) (And.intro (sound385 C) (And.intro (sound386 C) (And.intro (sound387 C) (And.intro (sound388 C) (And.intro (sound389 C) (And.intro (sound390 C) (And.intro (sound391 C) (And.intro (sound392 C) (And.intro (sound393 C) (And.intro (sound394 C) (And.intro (sound395 C) (And.intro (sound396 C) (And.intro (sound397 C) (And.intro (sound398 C) (And.intro (sound399 C) (And.intro (sound400 C) (And.intro (sound401 C) (And.intro (sound402 C) (And.intro (sound403 C) (And.intro (sound404 C) (And.intro (sound405 C) (And.intro (sound406 C) (And.intro (sound407 C) (And.intro (sound408 C) (And.intro (sound409 C) (And.intro (sound410 C) (And.intro (sound411 C) (And.intro (sound412 C) (And.intro (sound413 C) (And.intro (sound414 C) (And.intro (sound415 C) (And.intro (sound416 C) (And.intro (sound417 C) (And.intro (sound418 C) (And.intro (sound419 C) (And.intro (sound420 C) (And.intro (sound421 C) (And.intro (sound422 C) (And.intro (sound423 C) (And.intro (sound424 C) (And.intro (sound425 C) (And.intro (sound426 C) (And.intro (sound427 C) (And.intro (sound428 C) (And.intro (sound429 C) (And.intro (sound430 C) (And.intro (sound431 C) (And.intro (sound432 C) (And.intro (sound433 C) (And.intro (sound434 C) (And.intro (sound435 C) (And.intro (sound436 C) (And.intro (sound437 C) (And.intro (sound438 C) (And.intro (sound439 C) (And.intro (sound440 C) (And.intro (sound441 C) (And.intro (sound442 C) (And.intro (sound443 C) (And.intro (sound444 C) (And.intro (sound445 C) (And.intro (sound446 C) (And.intro (sound447 C) (And.intro (sound448 C) (And.intro (sound449 C) (And.intro (sound450 C) (And.intro (sound451 C) (And.intro (sound452 C) (And.intro (sound453 C) (And.intro (sound454 C) (And.intro (sound455 C) (And.intro (sound456 C) (And.intro (sound457 C) (And.intro (sound458 C) (And.intro (sound459 C) (And.intro (sound460 C) (And.intro (sound461 C) (And.intro (sound462 C) (And.intro (sound463 C) (And.intro (sound464 C) (And.intro (sound465 C) (And.intro (sound466 C) (And.intro (sound467 C) (And.intro (sound468 C) (And.intro (sound469 C) (And.intro (sound470 C) (And.intro (sound471 C) (And.intro (sound472 C) (And.intro (sound473 C) (And.intro (sound474 C) (And.intro (sound475 C) (And.intro (sound476 C) (And.intro (sound477 C) (And.intro (sound478 C) (And.intro (sound479 C) (And.intro (sound480 C) (And.intro (sound481 C) (And.intro (sound482 C) (And.intro (sound483 C) (And.intro (sound484 C) (And.intro (sound485 C) (And.intro (sound486 C) (And.intro (sound487 C) (And.intro (sound488 C) (And.intro (sound489 C) (And.intro (sound490 C) (And.intro (sound491 C) (And.intro (sound492 C) (And.intro (sound493 C) (And.intro (sound494 C) (And.intro (sound495 C) (And.intro (sound496 C) (And.intro (sound497 C) (And.intro (sound498 C) (And.intro (sound499 C) (And.intro (sound500 C) (And.intro (sound501 C) (And.intro (sound502 C) (And.intro (sound503 C) (And.intro (sound504 C) (And.intro (sound505 C) (And.intro (sound506 C) (And.intro (sound507 C) (And.intro (sound508 C) (And.intro (sound509 C) (And.intro (sound510 C) (And.intro (sound511 C) (And.intro (sound512 C) (And.intro (sound513 C) (And.intro (sound514 C) (And.intro (sound515 C) (And.intro (sound516 C) (And.intro (sound517 C) (And.intro (sound518 C) (And.intro (sound519 C) (And.intro (sound520 C) (And.intro (sound521 C) (And.intro (sound522 C) (And.intro (sound523 C) (And.intro (sound524 C) (And.intro (sound525 C) (And.intro (sound526 C) (And.intro (sound527 C) (And.intro (sound528 C) (And.intro (sound529 C) (And.intro (sound530 C) (And.intro (sound531 C) (And.intro (sound532 C) (And.intro (sound533 C) (And.intro (sound534 C) (And.intro (sound535 C) (And.intro (sound536 C) (And.intro (sound537 C) (And.intro (sound538 C) (And.intro (sound539 C) (And.intro (sound540 C) (And.intro (sound541 C) (And.intro (sound542 C) (And.intro (sound543 C) (And.intro (sound544 C) (And.intro (sound545 C) (And.intro (sound546 C) (And.intro (sound547 C) (And.intro (sound548 C) (And.intro (sound549 C) (And.intro (sound550 C) (And.intro (sound551 C) (And.intro (sound552 C) (And.intro (sound553 C) (And.intro (sound554 C) (And.intro (sound555 C) (And.intro (sound556 C) (And.intro (sound557 C) (And.intro (sound558 C) (And.intro (sound559 C) (And.intro (sound560 C) (And.intro (sound561 C) (And.intro (sound562 C) (And.intro (sound563 C) (And.intro (sound564 C) (And.intro (sound565 C) (And.intro (sound566 C) (And.intro (sound567 C) (And.intro (sound568 C) (And.intro (sound569 C) (And.intro (sound570 C) (And.intro (sound571 C) (And.intro (sound572 C) (And.intro (sound573 C) (And.intro (sound574 C) (And.intro (sound575 C) (And.intro (sound576 C) (And.intro (sound577 C) (And.intro (sound578 C) (And.intro (sound579 C) (And.intro (sound580 C) (sound581 C)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

theorem context_impossible (C : Context 13 n states) : False := by
  have h : (C.valuation atoms).satisfies_fmla cnf_refutation.formula := by
    rw [formula_eq]
    constructor
    intro cl hc
    exact C.satisfies_of_clause atoms cl ((List.forall_iff_forall_mem.mp (all_sound C)) cl hc)
  exact cnf_refutation (C.valuation atoms) h

#print axioms context_impossible
end ErdosSzekeres.Omission.CoupledCoreRankSearchThree
