import sys, json; sys.path.insert(0,'/opt/audit'); import mycube as M
icnf = [set(map(int,l.split()[1:-1])) for l in open(sys.argv[1]) if l.startswith('a')]
recs = [json.loads(l) for l in open(sys.argv[2])]
bad = 0; contra = 0; upin = 0
for c, r in zip(icnf, recs):
    mine = M.cube(r['U'], r['L'])
    if mine != c: bad += 1; print("DIFF", r['case'], len(mine), len(c))
    if any(-l in mine for l in mine): contra += 1
    if r['hull_ccw'] != M.hull(r['U'], r['L']): print("HULLDIFF", r['case'])
    if not M.UP(r['U']) <= mine: print("UP not in cube", r['case'])
    else: upin += 1
print("cube mismatches:", bad, "self-contradictory cubes:", contra, "UP(U) subset of cube:", upin, "/", len(recs))
# which cubes conflict with F's unit X(1,2,3)?
x123 = M.orb(1,2,3)
print("var X(1,2,3) =", x123, "; cubes containing -X(1,2,3):", [r['case'] for c,r in zip(icnf,recs) if -x123 in c][:40], sum(1 for c in icnf if -x123 in c))
