#!/usr/bin/env python3
"""Make deliberately broken copies of a CNF to check that symval2.py detects encoding errors.
  unitflip  : negate the first unit clause (a centre fact)
  dropk     : delete the first all-negative clause over non-orientation variables (a K-set clause)
  sbflip    : negate the last unit clause (a sector/order symmetry-breaking clause)
  defdrop   : delete the first definitional clause of a level-4 convexity flag
  topdefdrop: delete the first definitional clause of a level-(K-1) convexity flag
usage: mutate.py CNF NX OUTPREFIX
"""
import sys

cnf, nx, outp = sys.argv[1], int(sys.argv[2]), sys.argv[3]
hdr, cls = None, []
for line in open(cnf):
    if line.startswith("c"):
        continue
    if line.startswith("p"):
        hdr = line.split()
        continue
    cls.append(list(map(int, line.split()))[:-1])


def write(name, cl):
    with open(f"{outp}_{name}.cnf", "w") as f:
        f.write(f"p cnf {hdr[2]} {len(cl)}\n")
        for c in cl:
            f.write(" ".join(map(str, c)) + " 0\n")


units = [i for i, c in enumerate(cls) if len(c) == 1]
c1 = [list(c) for c in cls]; c1[units[0]] = [-c1[units[0]][0]]; write("unitflip", c1)
kidx = next(i for i, c in enumerate(cls) if all(l < 0 and -l > nx for l in c))
write("dropk", cls[:kidx] + cls[kidx + 1:])
c3 = [list(c) for c in cls]; c3[units[-1]] = [-c3[units[-1]][0]]; write("sbflip", c3)
didx = next(i for i, c in enumerate(cls) if sum(1 for l in c if l > nx) == 1 and all(abs(l) <= nx or l > 0 for l in c))
write("defdrop", cls[:didx] + cls[didx + 1:])
# the definitional clause of a top-level flag conv_{K-1}: head + K-1 negative aux literals
kk = len(cls[kidx])
tidx = next(i for i, c in enumerate(cls) if sum(1 for l in c if l > nx) == 1 and sum(1 for l in c if l < -nx) == kk - 1
            and all(abs(l) > nx for l in c))
write("topdefdrop", cls[:tidx] + cls[tidx + 1:])
print("units", len(units), "kidx", kidx, "didx", didx)
