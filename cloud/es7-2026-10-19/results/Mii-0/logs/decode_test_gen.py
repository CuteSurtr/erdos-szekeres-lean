import sys,random,itertools,subprocess,json
sys.path.insert(0,'/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C/scripts')
from mirlib import *
rng=random.Random(int(sys.argv[1]))
P=mirror_set(16,1,rng,where='interior')
Q=xsorted(P); X=orientations(Q)
idx={t:n+1 for n,t in enumerate(itertools.combinations(range(1,34),3))}
open('m.txt','w').write(' '.join(str(idx[t] if v else -idx[t]) for t,v in X.items()))
r=subprocess.run(['/home/user/bin/cgon','count','7'],input=''.join(f'{x} {y}\n' for x,y in P),capture_output=True,text=True)
print('cgon:',r.stdout.strip())
