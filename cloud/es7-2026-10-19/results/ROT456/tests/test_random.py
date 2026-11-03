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
def rand_reps(m, t, rng):
    c,s=math.cos(2*math.pi/m), math.sin(2*math.pi/m)
    r=1.0; reps=[]
    for i in range(t):
        a0=rng.uniform(0,2*math.pi); x,y=r*math.cos(a0)*1e9, r*math.sin(a0)*1e9
        b=round(y/s); a=round(x-b*c)
        reps.append(tuple([a,b]+[0]*(m-2)))
        r*=rng.choice([rng.uniform(0.2,0.6), rng.uniform(0.5,0.98)])
    return reps
K=8
seed=int(sys.argv[1]); budget=float(sys.argv[2]); ms=[int(x) for x in sys.argv[3].split(',')]
rng=random.Random(seed)
out={}
T0=time.time()
for m in ms:
    reps_cert,nc=read_reps(m, CERT[m])
    for t in (3,4,5,6):
        E,cnt,st=gen.build(m,K,t)
        nv=E.nv
        ranges=E.ranges
        def fam(idx):
            for f,(a,b) in ranges.items():
                if a<=idx<b: return f
        rec=dict(rand_ok=0, rand_with_kgon_caught=0, rand_with_kgon_missed=0, rand_nokgon_violations=0, nonchain_viol=0,
                 rejected=0, cert_subsets_ok=0, cert_subsets_bad=0, ncl=E.ncls, maxconv_hist={})
        tb=time.time()
        # subsets of the certificate set (valid configurations: nested, GP, no convex 8-gon)
        nsub = 6
        for it in range(nsub):
            sub=sorted(rng.sample(range(len(reps_cert)), t))
            cfg=rv.layered(m,[reps_cert[j] for j in sub])
            sg=rv.otable(cfg); val,nb=rv.assign(E,cfg,sg)
            bad=rv.evaluate(E.cls,val,nb,nv)
            mc=rv.maxconvex_xy(cfg,sg,K)
            if bad or mc>=K: rec['cert_subsets_bad']+=1; rec.setdefault('cert_bad_detail',[]).append((sub,mc,[fam(b) for b in bad[:5]]))
            else: rec['cert_subsets_ok']+=1
        # random cyclotomic configurations
        while time.time()-tb < budget:
            reps=rand_reps(m,t,rng)
            try:
                cfg=rv.layered(m,reps); sg=rv.otable(cfg)
            except RuntimeError as e:
                rec['rejected']+=1; continue
            val,nb=rv.assign(E,cfg,sg)
            bad=rv.evaluate(E.cls,val,nb,nv)
            fams=[fam(b) for b in bad]
            nonch=[f for f in fams if f!='chain']
            if nonch:
                rec['nonchain_viol']+=1; rec.setdefault('nonchain_detail',[]).append((reps,[E.cls[b] for b in bad if fam(b)!='chain'][:3]))
            mc=rv.maxconvex_xy(cfg,sg,K)
            rec['maxconv_hist'][mc]=rec['maxconv_hist'].get(mc,0)+1
            if mc>=K:
                if any(f=='chain' for f in fams): rec['rand_with_kgon_caught']+=1
                else: rec['rand_with_kgon_missed']+=1; rec.setdefault('missed_detail',[]).append(reps)
            else:
                if bad: rec['rand_nokgon_violations']+=1; rec.setdefault('viol_detail',[]).append((reps,fams[:5]))
                else: rec['rand_ok']+=1
        out['m%dK%dt%d'%(m,K,t)]=rec
        print('m=%d t=%d'%(m,t), json.dumps(rec, default=str)[:600], 'mindet=%s'%rv.MINDET[0], 'elapsed %.0f'%(time.time()-T0), flush=True)
        del E
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'random_%s.json')%sys.argv[3].replace(',','_'),'w'), default=str)
print('DONE', flush=True)
