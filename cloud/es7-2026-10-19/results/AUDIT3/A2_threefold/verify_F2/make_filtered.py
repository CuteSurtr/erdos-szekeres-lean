#!/usr/bin/env python3
"""verify_F2: write filtered copies of the 280 C3FINAL record files, dropping sigma_cubes.py-format
records (records with a "cube" field) from a chosen set of source directories; every other line is
copied byte for byte.  One output tree per variant:
  all      : drop every sigma_cubes.py-format record (C3SIG, C3SIG2, C3W3S)
  C3SIG    : drop only those in C3SIG/
  C3SIG2   : drop only those in C3SIG2/
  C3W3S    : drop only those in C3W3S/
  none     : drop nothing (control; identical copies)
Writes OUTROOT/<variant>/<relative path> and OUTROOT/<variant>/files.txt (absolute paths, in the
order of compose_files.txt).
usage: python -I -B make_filtered.py RESULTS_DIR OUTROOT"""
import json
import os
import sys

RD, OUT = sys.argv[1:3]
files = [l.strip() for l in open(os.path.join(RD, "C3FINAL", "compose_files.txt")) if l.strip()]
variants = {"all": {"C3SIG", "C3SIG2", "C3W3S"}, "C3SIG": {"C3SIG"}, "C3SIG2": {"C3SIG2"},
            "C3W3S": {"C3W3S"}, "none": set()}
summary = {}
for v, drop in variants.items():
    kept = dropped = 0
    paths = []
    for f in files:
        src = os.path.join(RD, f)
        dst = os.path.join(OUT, v, f)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        top = f.split("/")[0]
        with open(src, "rb") as fi, open(dst, "wb") as fo:
            for line in fi:
                if line.strip() and top in drop:
                    r = json.loads(line)
                    if "cube" in r:
                        dropped += 1
                        continue
                fo.write(line)
                kept += 1
        paths.append(dst)
    with open(os.path.join(OUT, v, "files.txt"), "w") as fl:
        fl.write("\n".join(paths) + "\n")
    summary[v] = {"lines_kept": kept, "sigma_cubes_records_dropped": dropped}
print(json.dumps(summary, indent=1))
