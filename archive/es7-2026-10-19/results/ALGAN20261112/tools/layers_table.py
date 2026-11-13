"""Layer radii, phases and two-layer slack of an m-fold exact .pts file (rows w_0..w_{m-1}, point = sum w_j zeta^j)."""
import math, sys
def layers(f,m):
    L=[]; rows=[list(map(int,l.split())) for l in open(f) if l.strip() and not l.startswith('#')]
    for o in range(len(rows)//m):
        w=rows[o*m]; z=sum(wj*complex(math.cos(2*math.pi*j/m),math.sin(2*math.pi*j/m)) for j,wj in enumerate(w))
        L.append((abs(z),math.atan2(z.imag,z.real)))
    return L
f,m=sys.argv[1],int(sys.argv[2]); h=math.pi/m; W=2*math.pi/m
fb=lambda d: math.cos(h)/math.cos(h-d)          # nesting (K = 2m)
G=lambda d: math.cos(h+d)/math.cos(h)            # Lemma 2 (K = m+1)
L=layers(f,m); r0=L[0][0]
print('# %s  m=%d t=%d   delta = reduced phase offset to previous layer'%(f,m,len(L)))
print(' i    r/r0     psi(deg)   ratio   delta   ratio/f   (1-f)/(1-ratio)   ratio/G')
for i,(r,t) in enumerate(L):
    s=''
    if i:
        D=(t-L[i-1][1])%W; d=min(D,W-D); rr=r/L[i-1][0]
        s='%7.4f %7.3f %8.4f %10.3f %10.4f'%(rr,math.degrees(d),rr/fb(d),(1-fb(d))/(1-rr),rr/G(d))
    print('%2d %9.5f %9.3f  %s'%(i,r/r0,math.degrees((t-L[0][1])%W),s))
