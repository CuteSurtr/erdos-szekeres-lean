import sys, numpy as np, random, itertools
exec(open('ana.py').read().split('sets=load')[0])
sets=load(sys.argv[1],0); random.seed(1); S=random.sample(sets,150)
T=None
def enc_dec(P,q,rot):
    if rot:
        th=0.1234; R=np.array([[np.cos(th),-np.sin(th)],[np.sin(th),np.cos(th)]]); P=P@R.T
    P=P[np.argsort(P[:,0])]
    d=np.diff(P,axis=0)
    out=[]
    for c in (0,1):
        s=np.sign(d[:,c]); m=np.log2(np.abs(d[:,c])+1e-9)
        m=np.round(m*q)/q
        out.append(s*2**m)
    D=np.stack(out,1)
    return P, np.vstack([P[:1],P[:1]+np.cumsum(D,0)])
for rot in [0,1]:
  for q in [2,4,8,16]:
    fl=[]
    for P in S:
        P0,Q=enc_dec(P,q,rot)
        fl.append(np.mean(signs(Q)!=signs(P0)))
    fl=np.array(fl)
    print('rot',rot,'q',q,'mean flip %.4f'%fl.mean(),'median %.4f'%np.median(fl),'exact',sum(fl==0))
