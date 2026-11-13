import ctypes, math
exec(open('twolayer.py').read().split('def pts')[0])
def ptsL(m,L):
    X=[];Y=[]
    for r,t in L:
        for k in range(m): X.append(r*math.cos(t+2*math.pi*k/m)); Y.append(r*math.sin(t+2*math.pi*k/m))
    return X,Y
m=8;K=9;h=math.pi/m
G=lambda d: math.cos(h+abs(d))/math.cos(h)
def best(D1,D2,N=60):
    # maximise rho1*rho2 (min radial drop) over a grid, 9-gon free
    g1,g2=G(D1),G(D2)
    bestv=None
    for i in range(N):
        r1=g1*(1-0.2*i/N)
        lo,hi=0.0,g2
        # monotone in r2? bisection for largest r2 keeping 9-gon free (verify)
        if countk(*ptsL(m,[(1,0),(r1,D1),(r1*1e-9+r1*0,D1)]),K)<0: pass
        for _ in range(40):
            mid=(lo+hi)/2
            if countk(*ptsL(m,[(1,0),(r1,D1),(r1*mid,D1+D2)]),K)==0: lo=mid
            else: hi=mid
        if lo>0 and (bestv is None or r1*lo>bestv[0]): bestv=(r1*lo,r1,lo)
    return bestv
print(' d(deg)  pattern    max rho1*rho2   drop=-log   2-layer sum Phi(D1)+Phi(D2)   pair(0,2) Phi(D1+D2)')
for d in [0.5,1,2,5,10]:
    dr=math.radians(d)
    for name,(D1,D2) in [('up-up',(dr,dr)),('up-down',(dr,-dr))]:
        b=best(D1,D2); drop=-math.log(b[0])
        print('%6.2f  %-8s  %.6f  %.6f   %.6f   %.6f   (rho1=%.5f rho2=%.5f)'%(d,name,b[0],drop,-math.log(G(D1))-math.log(G(D2)),-math.log(G(D1+D2)),b[1],b[2]))
