import ctypes, math, sys
lib=ctypes.CDLL('./libcnt9.so'); lib.countk.restype=ctypes.c_longlong
P=ctypes.POINTER(ctypes.c_double); lib.countk.argtypes=[ctypes.c_int,P,P,ctypes.c_int,P]
def countk(X,Y,K):
    n=len(X); XA=(ctypes.c_double*n)(*X); YA=(ctypes.c_double*n)(*Y); md=ctypes.c_double(0)
    return lib.countk(n,XA,YA,K,ctypes.byref(md))
def pts(m,rho,D):
    X=[];Y=[]
    for r,t in ((1.0,0.0),(rho,D)):
        for k in range(m): X.append(r*math.cos(t+2*math.pi*k/m)); Y.append(r*math.sin(t+2*math.pi*k/m))
    return X,Y
def g(m,K,D):
    lo,hi=0.0,1.0  # find inf rho with a convex K-gon (assume monotone in rho)
    if countk(*pts(m,0.999999,D),K)==0: return None
    for _ in range(50):
        mid=(lo+hi)/2
        if countk(*pts(m,mid,D),K)>0: hi=mid
        else: lo=mid
    return hi
m,K=int(sys.argv[1]),int(sys.argv[2]); h=math.pi/m
f=lambda D: math.cos(h)/math.cos(h-abs(D))
for Ddeg in [0.01,0.05,0.1,0.2,0.375,0.5,1,2,3,5,8,11.25,15,20,22.4]:
    if Ddeg>=180/m: continue
    D=math.radians(Ddeg); gv=g(m,K,D)
    print('D=%6.3f deg  nesting f=%.6f   2-layer K-gon threshold g=%s   g/f=%s'%(Ddeg,f(D),'%.6f'%gv if gv else 'none','%.6f'%(gv/f(D)) if gv else '-'))
