import os
import sys, math, random, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rv, gen
from test_random_lib import read_reps, CERT
K=8; rng=random.Random(5); budget=float(sys.argv[1])
for m in (6,5,4):
    reps,_=read_reps(m,CERT[m])
    for t in (3,4,5,6):
        E,_,_=gen.build(m,K,t); subs=list(itertools.combinations(range(len(reps)),t)); rng.shuffle(subs)
        tb=time.time(); ok=bad=0
        for sub in subs:
            if time.time()-tb>budget: break
            cfg=rv.layered(m,[reps[j] for j in sub]); sg=rv.otable(cfg); val,nb=rv.assign(E,cfg,sg)
            b=rv.evaluate(E.cls,val,nb,E.nv)
            if b: bad+=1; print('VIOLATION', m, t, sub, b[:5], flush=True)
            else: ok+=1
        print('m=%d t=%d subsets tested %d/%d ok=%d bad=%d'%(m,t,ok+bad,len(subs),ok,bad), flush=True)
print('DONE', flush=True)
