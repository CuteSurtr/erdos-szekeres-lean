#!/usr/bin/env python3
"""s3520-gate: offline test of drive_v3.py (import only; main() is not run, nothing is launched or written).
Checks: the 3520 entry, the Final text against res-slices-fv's compiled glue dry run FinalTest3520.lean, the six-slice
specialisation text, the exporter command keys, and that the v2 slices are unchanged."""
import importlib.util
import sys
from pathlib import Path

G = Path("/home/jay/research/data/formalize-20261122/s3520-gate")
F = Path("/home/jay/research/data/formalize-20261122/res-slices-fv")


def load(p):
    spec = importlib.util.spec_from_file_location(p.stem, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


v3, v2 = load(G / "tools/drive_v3.py"), load(G / "tools/drive.py")
s = next(x for x in v3.SLICES if x["tag"] == "3520")
assert [x["tag"] for x in v3.SLICES] == [x["tag"] for x in v2.SLICES] + ["3520"]
for a, b in zip(v2.SLICES, v3.SLICES):
    assert a == b, a["tag"]
ft = v3.final_text(s)
dry = (F / "lean/RS/FinalTest3520.lean").read_text()
want_rw = "rw [List.length_append, List.length_append, Res118.rows_lengths.1, Res118.rows_lengths.2.1,\n    Res118.rows_lengths.2.2.2]"
assert want_rw in dry and s["rw"] == want_rw.replace(",\n    ", ", ")
assert "theorem s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20 := by" in ft
assert "apply Res118.slice_of_root cat3520_ok" in ft and "exact RS3520.root" in ft and "import RS3520.Root" in ft
assert "#print axioms RS.s35_20" in ft
done = {"s33_18": "3318", "s34_18": "3418", "s34_19": "3419", "s35_18": "3518", "s35_19": "3519", "s35_20": "3520"}
sp = v3.spec_text(done)
assert "(s35_20 :" not in sp and "RS.s35_20" in sp and "import RS.Final3520" in sp
assert "Res118.residual_bound_118_of_slices n66 vP vQ vU vA RS.s33_18 RS.s34_18 RS.s34_19 RS.s35_18 RS.s35_19 RS.s35_20" in sp
assert v3.CEST_A == 500 and v3.CEST_B == 10 and s["exporter"] == "tools/slice_export_v3.py" and s["join_mem"] == 2000 and s["join_rt"] == 21600
assert s["master"].endswith("b35s20/bb-s1/master.json") and s["extra"].endswith("b35s20-v169/extra.json")
print(ft)
print(sp)
print("drive_v3 offline test: OK")
