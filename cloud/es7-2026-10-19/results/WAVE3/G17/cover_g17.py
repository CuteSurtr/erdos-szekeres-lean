import json, sys
def rd(p):
    out=[]
    for l in open(p):
        assert l.startswith("a ") and l.endswith(" 0\n"), repr(l)
        out.append(frozenset(map(int, l.split()[1:-1])))
    return out
leaves = rd(sys.argv[2]); given = [frozenset(c) for c in json.load(open(sys.argv[1]))[sys.argv[3]]]
def covered(asg, Ls):
    # Ls: leaves consistent with asg, with literals already in asg removed
    if any(not l for l in Ls): return True
    if not Ls: return False
    v = abs(next(iter(Ls[0])))
    for s in (v, -v):
        sub = [l - {s} for l in Ls if -s not in l]
        if not covered(asg | {s}, sub): return False
    return True
bad = 0
for c in given:
    Ls = [l - c for l in leaves if not any(-x in c for x in l)]
    if not covered(c, Ls): bad += 1
print("given", len(given), "not covered", bad, "leaves", len(leaves))
