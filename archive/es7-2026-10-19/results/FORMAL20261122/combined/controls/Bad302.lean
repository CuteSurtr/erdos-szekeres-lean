-- combined part 3 negative control (PART3.md §4): the same proof term cannot give ES(8) ≤ 301; this file MUST FAIL
-- to compile (expected: a type mismatch at the theorem below). Compiled without -o.
import Combined.ES302Final

theorem bad301 (cubes : N66R15Enc.CubesUnsat105R) (certs : N66R15Geo.RowCertsUnsat)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA) :
    ErdosSzekeres.ForcesConvexNGon 301 8 :=
  Combined.es302_verdicts cubes certs hP hQ hU hA
