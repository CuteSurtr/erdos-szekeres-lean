import math, itertools, random
exec(open('which9.py').read().split('m=8')[0])
exec(open('twolayer.py').read().split('def pts')[0])
def P2(m,rho,D):
    X=[];Y=[]
    for r,t in ((1.0,0.0),(rho,D)):
        for k in range(m): X.append(r*math.cos(t+2*math.pi*k/m)); Y.append(r*math.sin(t+2*math.pi*k/m))
    return X,Y
random.seed(3); bad=0; tot=0
for m in range(4,14):
    h=math.pi/m
    for D in [1e-6,1e-4,1e-3,0.01,0.05]+[random.uniform(0,2*math.pi/m) for _ in range(300)]:
        if D<=0 or D>=2*math.pi/m: continue
        dl=min(D,2*math.pi/m-D); G=math.cos(h+dl)/math.cos(h)
        for rho in [G*(1-x) for x in (1e-7,1e-5,1e-3,0.05,0.3,0.7)]+[G*(1+1e-6)]:
            if rho<=0: continue
            tot+=1; has=countk(*P2(m,rho,D),m+1)>0
            if has!=(rho>G): bad+=1; print('MISMATCH m',m,'D',D,'rho/G',rho/G)
print('tests',tot,'mismatches',bad)
