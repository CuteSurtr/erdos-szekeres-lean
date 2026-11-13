import math, random
exec(open('twolayer.py').read().split('m,K=int')[0])
random.seed(7); bad=0; tot=0
for m in range(3,12):
    K=m+1; h=math.pi/m
    for trial in range(400):
        D=random.uniform(1e-4,2*math.pi/m-1e-4); dl=min(D,2*math.pi/m-D)
        G=math.cos(h+dl)/math.cos(h)
        for rho in (G*(1-random.uniform(1e-5,0.3)), G*(1+random.uniform(1e-5,0.05))):
            if rho<=0 or rho>=1: continue
            has=countk(*pts(m,rho,D),K)>0; tot+=1
            if has!=(rho>G): bad+=1; print('MISMATCH m',m,'D',D,'rho',rho,'G',G,'has',has)
    print('m=%d done, mismatches so far %d'%(m,bad))
print('total tests',tot,'mismatches',bad)
