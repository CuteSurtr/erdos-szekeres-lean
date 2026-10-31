# G5 independent cover check: every given cube T is covered by the leaves, i.e. every
# full assignment extending T extends some leaf. Rejects lines not of the form "a ... 0".
import json, sys
def rd(p):
    out = []
    for l in open(p):
        assert l.startswith("a ") and l.endswith(" 0\n"), repr(l)
        out.append(frozenset(map(int, l.split()[1:-1])))
    return out
tops = [frozenset(c) for c in json.load(open(sys.argv[1]))[sys.argv[2]]]
leaves = rd(sys.argv[3])
def covered(asg, ls):
    ls = [l for l in ls if not any(-x in asg for x in l)]
    if not ls: return False
    for l in ls:
        if l <= asg: return True
    # branch on a literal of the first live leaf not yet assigned
    v = next(abs(x) for x in ls[0] if x not in asg)
    return covered(asg | {v}, ls) and covered(asg | {-v}, ls)
bad = [sorted(t) for t in tops if not covered(t, leaves)]
print("given", len(tops), "leaves", len(leaves), "uncovered", len(bad))
print("s COVERED" if not bad else "s NOT COVERED")
