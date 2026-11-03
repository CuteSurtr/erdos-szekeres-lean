import os
import sys, math, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rv, gen
from test_random_lib import read_reps, CERT
K=8
for m,t in ((6,9),(4,13),(5,11)):
    T0=time.time()
    fn=os.path.join(os.environ.get('CNFDIR', '.'), 'm%dK8t%d.cnf')%(m,t)
    meta=json.load(open(fn+'.json'))
    reps,nc=read_reps(m,CERT[m])
    cfg=rv.layered(m,reps)
    assert cfg['t']==t, (cfg['t'],t)
    sg=rv.otable(cfg)
    E=gen.Enc(m,K,t)
    assert E.ntriplevars==meta['ntriple'], 'ntriple mismatch'
    assert {'%d,%d'%k:v for k,v in E.Y.items()}==meta['Y'], 'Y mismatch'
    assert {str(k):v for k,v in E.H.items()}=={str(k):v for k,v in meta['H'].items()}, 'H mismatch'
    val,nb=rv.assign(E,cfg,sg)
    nv=meta['nv']; A=bytearray(nv+1)
    for v,b in val.items(): A[v]=1 if b else 0
    rng=meta['ranges']
    def fam(i):
        for f,(a,b) in rng.items():
            if a<=i<b: return f
    for pas in (1,2):
        bad=[]; idx=0
        with open(fn) as f:
            hdr=f.readline().split(); assert int(hdr[2])==nv
            for line in f:
                cl=[int(x) for x in line.split()[:-1]]
                sat=False
                for l in cl:
                    if (l>0 and A[l]==1) or (l<0 and A[-l]==0): sat=True; break
                if not sat:
                    if pas==1:
                        pos=[l for l in cl if l>nb]
                        if len(pos)==1: A[pos[0]]=1
                        else: bad.append(idx)
                    else: bad.append(idx)
                idx+=1
        assert idx==meta['ncl']
    print('m=%d t=%d centre_removed=%d layers=%d psi=%s theta=%s sep=%.3g nviol=%d fams=%s nchain_true=%d time=%.0fs mindet=%s'%(
        m,t,nc,cfg['t'],[round(x,4) for x in cfg['psi']],[round(x,4) for x in cfg['theta']],cfg['sep'],len(bad),
        sorted(set(fam(b) for b in bad)), sum(A[nb+1:]), time.time()-T0, rv.MINDET[0]), flush=True)
print('DONE', flush=True)
