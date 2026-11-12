import math, itertools
exec(open('which9.py').read().split('m=8')[0])
m=8
for Ddeg,g in [(0.375,0.997268),(5,0.960094),(15,0.858719)]:
    D=math.radians(Ddeg)
    A=pts(m,g*(1-2e-6),D); B=pts(m,g*(1+2e-6),D)
    o=lambda P,a,b,c: (P[b][1][0]-P[a][1][0])*(P[c][1][1]-P[a][1][1])-(P[b][1][1]-P[a][1][1])*(P[c][1][0]-P[a][1][0])
    ch=[(A[a][0],A[b][0],A[c][0]) for a,b,c in itertools.combinations(range(16),3) if (o(A,a,b,c)>0)!=(o(B,a,b,c)>0)]
    print('D=',Ddeg,'triples flipping at threshold:',ch[:10], len(ch))
    # candidate closed forms
    h=math.pi/m
    c1=math.cos(2*h)/math.cos(2*h-D)  # w_k on chord v_{k}v_{k+2}? 
    print('  g=%.6f  cos(2pi/m)/cos(2pi/m-D)=%.6f'%(g,c1))
