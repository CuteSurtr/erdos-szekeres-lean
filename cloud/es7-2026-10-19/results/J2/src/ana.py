import sys, numpy as np, random
def load(path, nfield):
    out=[]
    for line in open(path):
        t=line.split()
        if len(t)<4: continue
        k=3 if t[2]!="33" and t[3]=="32" else 2; n=int(t[k]); c=list(map(int,t[k+1:k+1+2*n]))
        out.append(np.array(c,dtype=np.float64).reshape(n,2))
    return out
def signs(P):
    n=len(P); i,j,k=np.triu_indices(n,1)[0],None,None
    import itertools
    T=np.array(list(itertools.combinations(range(n),3)))
    a,b,c=P[T[:,0]],P[T[:,1]],P[T[:,2]]
    return np.sign((b[:,0]-a[:,0])*(c[:,1]-a[:,1])-(b[:,1]-a[:,1])*(c[:,0]-a[:,0]))
sets=load(sys.argv[1],0)
random.seed(1)
S=random.sample(sets,200)
for mode in ['minmax','rank','whiten']:
  for G in [64,256,1024,4096]:
    fl=[]
    for P in S:
        s0=signs(P)
        if mode=='minmax':
            Q=(P-P.min(0))/(np.ptp(P,0)); Q=np.round(Q*(G-1))
        elif mode=='rank':
            Q=np.argsort(np.argsort(P,0),0).astype(float)*(G-1)/(len(P)-1); Q=np.round(Q)
        else:
            C=P-P.mean(0); U,s,Vt=np.linalg.svd(C,full_matrices=False); Q=U; Q=(Q-Q.min(0))/np.ptp(Q,0); Q=np.round(Q*(G-1))
        s1=signs(Q); fl.append(np.mean(s1!=s0))
    print(mode,G,'mean flip frac %.4f'%np.mean(fl),'exact %d/200'%sum(f==0 for f in fl))
# scale structure
r=[np.log2(np.ptp(P,0).max()/np.min([np.linalg.norm(P[i]-P[j]) for i in range(len(P)) for j in range(i)])) for P in S[:50]]
print('log2 extent/mindist', np.percentile(r,[0,50,100]))
