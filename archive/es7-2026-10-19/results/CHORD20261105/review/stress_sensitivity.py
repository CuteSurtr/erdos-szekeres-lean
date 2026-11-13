#!/usr/bin/env python3
"""Sensitivity check of stress.py: mutated chord clauses (orientation literal negated; Y literal flipped; Y literal
dropped) must be caught by the same random-configuration evaluation.  Reports how many mutated clauses are
violated in at least one of N configurations."""
import sys, json, random
import stress
from indep_enc import NTRIP
rng = random.Random(77)
N = int(sys.argv[1])
C = stress.CHORD
neg = [[(-x if abs(x) <= NTRIP else x) for x in c] for c in C]
flip = [[(x if abs(x) <= NTRIP else -x) for x in c] for c in C if len(c) == 2]
drop = [[x for x in c if abs(x) <= NTRIP] for c in C if len(c) == 2]
caught = {'neg': set(), 'flipY': set(), 'dropY': set()}
modes = ['uniform', 'multiscale', 'phase_edge', 'phase_cluster', 'mixed']
for n in range(N):
    rs, th = stress.gen(rng, modes[n % 5])
    for name, cls in (('neg', neg), ('flipY', flip), ('dropY', drop)):
        v, _ = stress.evaluate(rs, th, cls)
        caught[name] |= {tuple(c) for c in v}
print(json.dumps({'configs': N, 'neg_caught': len(caught['neg']), 'neg_total': len(neg),
                  'flipY_caught': len(caught['flipY']), 'flipY_total': len(flip),
                  'dropY_caught': len(caught['dropY']), 'dropY_total': len(drop)}))
# which binary clauses were never caught with the Y literal dropped, and are they subsumed by base units?
D = '<six10-work-dir>'
bu = set()
for line in open(D + '/cegar/base/encA_6_8_10.cnf'):
    if line[0] in 'cp':
        continue
    l = line.split()
    if len(l) == 2:
        bu.add(int(l[0]))
    if len(bu) > 0 and line.startswith('-5711') and False:
        break
unc = [c for c in C if len(c) == 2 and tuple(x for x in c if abs(x) <= NTRIP) not in caught['dropY']]
from indep_enc import TRIPLE_OF
sub = [c for c in unc if any(x in bu for x in c)]
lay = {}
for c in unc:
    L = [x for x in c if abs(x) <= NTRIP][0]; t = TRIPLE_OF[abs(L)]
    ls = [x // 6 for x in t]; j = max(set(ls), key=ls.count); i = min(set(ls), key=ls.count)
    ks = sorted((x % 6) for x in t if x // 6 == j); d = (ks[1] - ks[0]) % 6; d = min(d, 6 - d)
    key = 'p_inner' if i > j else 'p_outer'
    lay[(key, 'chord_sep_%d' % d)] = lay.get((key, 'chord_sep_%d' % d), 0) + 1
print(json.dumps({'dropY_uncaught': len(unc), 'of_which_base_unit_subsumed': len(sub),
                  'uncaught_by_type': {str(k): v for k, v in lay.items()}}))
