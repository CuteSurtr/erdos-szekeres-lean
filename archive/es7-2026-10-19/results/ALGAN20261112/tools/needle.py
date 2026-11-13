import ctypes, math, sys
lib=ctypes.CDLL('./libcnt9.so'); lib.countk.restype=ctypes.c_longlong
P=ctypes.POINTER(ctypes.c_double)
lib.countk.argtypes=[ctypes.c_int,P,P,ctypes.c_int,P]
def countk(X,Y,K):
    n=len(X); XA=(ctypes.c_double*n)(*X); YA=(ctypes.c_double*n)(*Y); md=ctypes.c_double(0)
    c=lib.countk(n,XA,YA,K,ctypes.byref(md)); return c,md.value
def layers(f,m):
    L=[]; rows=[list(map(int,l.split())) for l in open(f) if l.strip() and not l.startswith('#')]
    for o in range(len(rows)//m):
        w=rows[o*m]; z=sum(wj*complex(math.cos(2*math.pi*j/m),math.sin(2*math.pi*j/m)) for j,wj in enumerate(w))
        L.append([abs(z),math.atan2(z.imag,z.real)])
    return L
def pts(L,m):
    X=[];Y=[]
    for r,t in L:
        for k in range(m): X.append(r*math.cos(t+2*math.pi*k/m)); Y.append(r*math.sin(t+2*math.pi*k/m))
    return X,Y
def unwrap(L,m,group):
    # bring phases of group near the first member (mod 2pi/m)
    W=2*math.pi/m; t0=L[group[0]][1]
    for i in group: L[i][1]=t0+((L[i][1]-t0+W/2)%W-W/2)
def compress(L,groups,eps,m):
    L2=[list(x) for x in L]
    for g in groups:
        unwrap(L2,m,g); tb=sum(L2[i][1] for i in g)/len(g)
        for i in g: L2[i][1]=tb+eps*(L2[i][1]-tb)
    return L2
f,m,K=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]); groups=eval(sys.argv[4])
L=layers(f,m)
for eps in [1,0.5,0.2,0.1,0.03,0.01,0.003,0.001]:
    X,Y=pts(compress(L,groups,eps,m),m)
    c,md=countk(X,Y,K); c4,_=countk(X,Y,4)
    print('eps=%-6g convex%d=%d  convex4=%d  min_rel_det=%.2e'%(eps,K,c,c4,md))
