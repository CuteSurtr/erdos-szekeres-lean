"""Enumerate ALL signotopes on m points with no a-cap and no convex n-gon (blocking clauses), and for each one
list every working Delta (brute force over subsets).  Small m only.  Output: jsonl with sign string and Deltas."""
import sys, itertools, json
from eager_cert import Enc, exact_sets
from pysat.solvers import Cadical153
comb = itertools.combinations
a, n, m, form = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
limit = int(sys.argv[5]) if len(sys.argv) > 5 else 10**9
E = Enc(a, n, m, form == 'strong')
tris = list(comb(range(m), 3))
out = open('enum_a%d_n%d_m%d_%s.jsonl' % (a, n, m, form), 'w')
cnt = 0; nod = 0
with Cadical153(bootstrap_with=E.base) as s:
    while cnt < limit and s.solve():
        mod = s.get_model(); o = {t: mod[E.tri[t] - 1] > 0 for t in tris}
        s.add_clause([-mod[E.tri[t] - 1] for t in tris])
        caps, gons = exact_sets(E, o)
        capm = [sum(1 << i for i in K) for K in caps]; gonm = [sum(1 << i for i in G) for G in gons]
        W = []
        for D in range(1 << m):
            if any(D & K == K for K in capm): continue
            if any(D & G == 0 for G in gonm): continue
            if E.strong and any(D & G == G for G in gonm): continue
            W.append(D)
        if not W: nod += 1
        out.write(json.dumps({'s': ''.join('+' if o[t] else '-' for t in tris), 'ngon': len(gons), 'ncap': len(caps), 'W': W}) + '\n')
        cnt += 1
print(a, n, m, form, 'signotopes', cnt, 'without Delta', nod, flush=True)
