import math, itertools, random
def orient(a,b,d): return (b[0]-a[0])*(d[1]-a[1])-(b[1]-a[1])*(d[0]-a[0])
def lin(w,a,y): return w[0]*(y[0]-a[0])+w[1]*(y[1]-a[1])
def rot(c,th,p): return (c[0]+math.cos(th)*(p[0]-c[0])-math.sin(th)*(p[1]-c[1]), c[1]+math.sin(th)*(p[0]-c[0])+math.cos(th)*(p[1]-c[1]))
def it(f,j,p):
    for _ in range(j): p=f(p)
    return p
bad=0
random.seed(1)
for trial in range(200):
    c=(random.uniform(-3,3),random.uniform(-3,3)); x=(random.uniform(-3,3),random.uniform(-3,3))
    for m in range(1,10):
        rho=lambda p,m=m,c=c: rot(c,2*math.pi/m,p)
        r2=(x[0]-c[0])**2+(x[1]-c[1])**2
        for j in range(0,m+1):
            o=orient(x,rho(x),it(rho,j,x))
            # orient_regular_nonneg: j<=m -> o >= 0
            if o < -1e-9: bad+=1; print('regular FAIL',m,j,o)
            # remark formula for 1<=j<=m
            if j>=1:
                f=4*r2*math.sin(math.pi/m)*math.sin(j*math.pi/m)*math.sin((j-1)*math.pi/m)
                if abs(o-f)>1e-8: bad+=1; print('remark formula FAIL',m,j,o,f)
                # zero exactly for j in {1,m} when m>=2
                if m>=2 and ((abs(o)<1e-9) != (j in (1,m))): bad+=1; print('remark zero-set FAIL',m,j,o)
            # lin_orbit_pos: 0<j<m
            if 0<j<m:
                l=lin((c[0]-x[0],c[1]-x[1]),x,it(rho,j,x))
                if l<=0: bad+=1; print('lin_orbit FAIL',m,j,l)
        if m>=3:
            o=orient(x,rho(x),it(rho,m-1,x))
            if o<=0: bad+=1; print('next_prev FAIL',m,o)
        # beyond the range j<=m the claim can fail (j=m+1 is j=1 again => 0; j>m fine); check j = m+2..2m for negativity existence
print('random checks bad =',bad)
# S4 instance: c=0, m=4
S4=[(2,0),(0,2),(-2,0),(0,-2),(.5,.5),(-.5,.5),(-.5,-.5),(.5,-.5)]
c=(0,0); rho=lambda p: rot(c,math.pi/2,p)
L0=S4[:4]; L1=S4[4:]
ok=True
for x in L0:
    for y in L1:
        if orient(x,rho(x),y)<=0: ok=False; print('nest FAIL',x,y)
        if (y[0]**2+y[1]**2) > (x[0]**2+x[1]**2): ok=False
    for y in S4:
        if y!=x and lin((c[0]-x[0],c[1]-x[1]),x,y)<=0: ok=False; print('halfplane FAIL',x,y)
for x in L1:
    for y in L1:
        if y!=x and lin((c[0]-x[0],c[1]-x[1]),x,y)<=0: ok=False; print('halfplane L1 FAIL',x,y)
print('S4 checks ok =',ok)
# m=2 remark: orient(x, rho x, y) = 0 for y on segment
x=(1.3,0.4); c=(0.2,-0.7); rx=rot(c,math.pi,x)
for lam in [0,0.25,0.5,1]:
    y=((1-lam)*x[0]+lam*rx[0],(1-lam)*x[1]+lam*rx[1]); print('m=2 segment orient', round(orient(x,rx,y),12))
