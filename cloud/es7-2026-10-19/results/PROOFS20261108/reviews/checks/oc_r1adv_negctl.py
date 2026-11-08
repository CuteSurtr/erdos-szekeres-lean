import itertools, random, math
from fractions import Fraction as F
def orient(a,b,d): return (b[0]-a[0])*(d[1]-a[1])-(b[1]-a[1])*(d[0]-a[0])
def toIcoMod(p,a,b):
    n=(b-a)//p; return b-n*p
def sgn(t):
    seen=set();cyc=0
    for i in range(3):
        if i not in seen:
            cyc+=1;j=i
            while j not in seen: seen.add(j); j=t[j]
    return (-1)**(3-cyc)
rnd=random.Random(3); fails={'trunc_mod':0,'sign_only_s1':0,'pi_over_m':0}
for _ in range(2000):
    N=rnd.randint(2,9);u=F(1);J=rnd.randint(-30,-1);psi=F(rnd.randint(0,9),10)
    tr=int(math.fmod(J,N))  # C-style remainder
    if toIcoMod(N*u,F(0),J*u+psi)!=tr*u+psi: fails['trunc_mod']+=1
# encoder with only sgn(s1): m=4 exact
for _ in range(500):
    c=(F(0),F(0)); rho=lambda p:(-p[1],p[0])
    base=[(F(rnd.randint(-9,9)),F(rnd.randint(-9,9))) for _ in range(2)]
    P=lambda lab: (lambda p:[p:=rho(p) for _ in range(lab[1]%4)] and p or p)(base[lab[0]])
    def P(lab):
        p=base[lab[0]]
        for _ in range(lab[1]%4): p=rho(p)
        return p
    labs=[(i,k) for i in range(2) for k in range(4)]
    T=tuple(rnd.sample(labs,3)); s1=rnd.choice(list(itertools.permutations(range(3)))); s2=rnd.choice(list(itertools.permutations(range(3))))
    T0=tuple(T[s1[i]] for i in range(3)); C=tuple(((T0[s2[i]][0],(T0[s2[i]][1]+1)%4)) for i in range(3))
    PT=[P(x) for x in T]
    if orient(*PT)==0: continue
    v=orient(*[P(x) for x in C]); lit=(0<v) if sgn(s1)==1 else not(0<v)
    if lit!=(0<orient(*PT)): fails['sign_only_s1']+=1
# Remark (3): beta-alpha = pi/4 is k*pi/m for m=4 (k=1) but not k*2pi/m
fails['pi_over_m'] = int(F(1,4)/F(1,4)==1 and (F(1,4)/F(2,4)).denominator!=1)
print(fails)
