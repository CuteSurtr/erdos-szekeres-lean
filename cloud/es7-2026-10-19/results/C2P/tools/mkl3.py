#!/usr/bin/env python3
"""Third-layer work list for second-layer subcases that did not close directly (C2P follow-up).

For each SUBCASE (for example P8_3-11) it writes cubes3/SUBCASE.txt with tools/l3cubes.py (the 364 third-layer cubes,
13 remaining classes) and appends to the list: the cover SUBCASE/cover (cap 3600 s) and then the third-layer units
SUBCASE/W (cap 1800 s), so that lane3.py can run them.
usage: mkl3.py C2P_DIR MAP.json OUT_LIST SUBCASE...   (C2P_DIR holds cubes/ and receives cubes3/)"""
import os, subprocess, sys
D, mapf, out, subs = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
here = os.path.dirname(os.path.abspath(__file__))
os.makedirs(f"{D}/cubes3", exist_ok=True)
rows = []
for sub in subs:
    case = sub.split("_")[0]
    f3 = f"{D}/cubes3/{sub}.txt"
    subprocess.run([sys.executable, f"{here}/l3cubes.py", mapf, f"{D}/cubes/{case}_cubes.txt", sub, f3], check=True)
    rows.append((f"{sub}/cover", case, "cover3", 3600))
    for l in open(f3):
        name = l.split(" ", 1)[0]
        rows.append((name, case, "Q3" if name.split("/")[1].count("-") == 1 else "H3", 1800))
with open(out, "w") as f:
    f.write("idx\tunit\tcase\tkind\tcap_s\n")
    for i, r in enumerate(rows): f.write(f"{i}\t" + "\t".join(map(str, r)) + "\n")
print(len(subs), "subcases,", len(rows), "units")
