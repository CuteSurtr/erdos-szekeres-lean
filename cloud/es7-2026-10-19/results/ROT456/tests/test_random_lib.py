import os
import sys, math, random, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rv, gen
CERT={4:os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'), 'ES8SYM', 'sets', 'c4_52pts_13layers.pts'),6:os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'), 'ES8SYM', 'sets', 'c6_54pts_9layers.pts'),5:os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'), 'ES8SYM', 'sets3', 'c5_56pts_11layers_centre.pts')}
def read_reps(m, fn):
    W=[tuple(int(x) for x in l.split()) for l in open(fn) if l.strip() and not l.startswith('#')]
    Z=rv.zpow(m); W2=[]
    for w in W:
        x,y=rv.wval(w,Z)
        if abs(x)+abs(y) < rv.D(10)**-40: continue   # centre
        W2.append(w)
    left=set(W2); reps=[]
    if len(left)!=len(W2): raise RuntimeError('dup points')
    while left:
        w=min(left); orb=[w]
        for _ in range(m-1): orb.append(rv.shift(orb[-1]))
        for x in orb:
            if x not in left: raise RuntimeError('not an orbit')
            left.remove(x)
        reps.append(w)
    return reps, len(W)-len(W2)
