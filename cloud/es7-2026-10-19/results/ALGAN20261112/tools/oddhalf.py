"""Sanity check (floats, evidence only) of the odd-m half-plane step of Lemma 2:
X = {v_0..v_h, w_0..w_h}, h=(m-1)/2, offset D in (0, pi/m]. Claim: X is not in convex position whenever rho < f_m(D)
(nested layers), for odd m >= 5; it can be for m = 3."""
import math, random
def hull_all(pts):
    P=sorted(pts)
    def cross(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[];up=[]
    for p in P:
        while len(lo)>=2 and cross(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(up)>=2 and cross(up[-2],up[-1],p)<=0: up.pop()
        up.append(p)
    return len(lo)+len(up)-2==len(P)
random.seed(1); bad={}; tot={}; conv_above_f={}
for m in (3,5,7,9,11,13):
    h=(m-1)//2
    for _ in range(4000):
        D=random.uniform(1e-3,1)*math.pi/m
        f=math.cos(math.pi/m)/math.cos(math.pi/m-D); G=math.cos(math.pi/m+D)/math.cos(math.pi/m)
        rho=random.choice([random.uniform(0.05,G),random.uniform(G,f)*0.999999+0*G]) if G>0.05 else random.uniform(G,f)
        X=[(math.cos(2*math.pi*k/m),math.sin(2*math.pi*k/m)) for k in range(h+1)]+[(rho*math.cos(D+2*math.pi*k/m),rho*math.sin(D+2*math.pi*k/m)) for k in range(h+1)]
        tot[m]=tot.get(m,0)+1
        if hull_all(X): bad[m]=bad.get(m,0)+1
        rho2=random.uniform(f,1)*0.999+0.001*f
        X2=X[:h+1]+[(rho2*math.cos(D+2*math.pi*k/m),rho2*math.sin(D+2*math.pi*k/m)) for k in range(h+1)]
        if rho2>f and hull_all(X2): conv_above_f[m]=conv_above_f.get(m,0)+1
for m in tot: print('m',m,'cases rho<f',tot[m],'X convex',bad.get(m,0),'| control rho>f: X convex in',conv_above_f.get(m,0),'cases')
