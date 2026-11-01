"""Sanity test (not a proof): images of the 72-hole balanced witness under T, C, TC
satisfy the 2,685 base rows (forced by invariance) and also all 3,131 rows (as they must
if the 446 cuts are Boolean consequences of the base rows)."""
import json, sys
d = json.load(open(sys.argv[1])); P = json.load(open(sys.argv[2])); W = json.load(open(sys.argv[3]))
rows = [(c['support'], c['rhs']) for c in d['constraints']]
T, C = P['T'], P['C']; TC = [T[C[i]] for i in range(252)]
holes = set(W['balanced_v2_72_hole_witness'])
def viol(H, rr): return sum(1 for s, r in rr if sum(1 for i in s if i in H) < r)
print('witness: %d holes, violations base %d all %d' % (len(holes), viol(holes, rows[:2685]), viol(holes, rows)))
for nm, p in (('T', T), ('C', C), ('TC', TC)):
    # (h o p)(i) = h(p(i)) : i is a hole of h o p iff p(i) is a hole of h
    Hp = {i for i in range(252) if p[i] in holes}
    print('h o %s: %d holes, violations base %d all3131 %d' % (nm, len(Hp), viol(Hp, rows[:2685]), viol(Hp, rows)))
