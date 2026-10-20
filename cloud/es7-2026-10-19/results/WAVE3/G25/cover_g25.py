import sys
def rd(p):
    out=[]
    for l in open(p):
        assert l.startswith("a ") and l.endswith(" 0\n"), l
        out.append(frozenset(map(int,l.split()[1:-1])))
    return out
def covered(cs):  # do the cubes cover the whole assignment space?
    if any(len(c)==0 for c in cs): return True
    if not cs: return False
    v=abs(next(iter(cs[0])))
    return all(covered([c-{s*v} for c in cs if -s*v not in c]) for s in (1,-1))
given,leaves=rd(sys.argv[1]),rd(sys.argv[2])
ok=0
for g in given:
    sub=[l-g for l in leaves if not any(-x in g for x in l)]
    ok+=covered(sub)
print("given",len(given),"covered",ok,"leaves",len(leaves),"extend_given",sum(any(g<=l for g in given) for l in leaves))
