#!/usr/bin/env python3
"""Write LeanLB/Data/<Name>.lean for the six k = 7 sets, with the k = 8 generator `gen_data.py` (copied verbatim
from LEANLB20261111/scripts) and only its table replaced. Usage: gen_data7.py [--check]
Kinds: m3 = Eisenstein row `a b` = a + b*omega (SYMMAX README "Coordinates": 3-fold and 6-fold files);
xy = integer point; m5 = row `c0 c1 c2 c3` = sum c_j z^j, z = e^(2 pi i/5) (missing coefficient 0)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_data

gen_data.SETS = [
    ("C3N31", "SYMMAX/c3_31points.txt", "m3"),
    ("C6N30", "SYMMAX/c6_30points.txt", "m3"),
    ("C4N28", "SYMMAX/c4_28points.txt", "xy"),
    ("C2N32", "SYM2/sym7_32points.txt", "xy"),
    ("MirN32", "SYMMAX/mirror_32points.txt", "xy"),
    ("C5N31", "SYMMAX/c5_31points.txt", "m5"),
]

if __name__ == "__main__":
    gen_data.main()
