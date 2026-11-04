"""Exact positive kernel recovery over Q(sqrt(5)); no numerical verdict trusted."""
from fractions import Fraction as F
import math,time
Z=(F(0),F(0));O=(F(1),F(0))
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def neg(a):return (-a[0],-a[1])
def mul(a,b):return (a[0]*b[0]+5*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def div(a,b):
    den=b[0]*b[0]-5*b[1]*b[1]
    if not den:raise ZeroDivisionError
    return mul(a,(b[0]/den,-b[1]/den))
def sign(a):
    x,y=a
    if x>=0 and y>=0:return int(x>0 or y>0)
    if x<=0 and y<=0:return -int(x<0 or y<0)
    v=x*x-5*y*y
    return (1 if v>0 else -1 if v<0 else 0)*(1 if x>0 else -1)
def recover(rows,approx,nvars,seconds=15):
    start=time.monotonic();count=len(rows)
    M=[[row.get(j,Z) for row in rows]+[Z] for j in range(nvars)]
    M.append([O]*count+[O]);pr=0;pivots=[]
    for col in range(count):
        if time.monotonic()-start>seconds:raise TimeoutError('exact field recovery budget')
        r=next((r for r in range(pr,len(M)) if M[r][col]!=Z),None)
        if r is None:continue
        M[pr],M[r]=M[r],M[pr];pivot=M[pr][col];M[pr]=[div(x,pivot) for x in M[pr]]
        for r in range(len(M)):
            if r!=pr and M[r][col]!=Z:
                factor=M[r][col];M[r]=[add(x,neg(mul(factor,y))) for x,y in zip(M[r],M[pr])]
        pivots.append(col);pr+=1
    if any(all(x==Z for x in row[:-1]) and row[-1]!=Z for row in M):raise ValueError('inconsistent support')
    weights=[(F(float(x)).limit_denominator(10**8),F(0)) for x in approx]
    free=set(range(count))-set(pivots)
    for r,col in enumerate(pivots):
        x=M[r][-1]
        for j in free:x=add(x,neg(mul(M[r][j],weights[j])))
        weights[col]=x
    if any(sign(x)<=0 for x in weights):raise ValueError('nonpositive recovered weight')
    total=[Z]*nvars
    for row,w in zip(rows,weights):
        for j,c in row.items():total[j]=add(total[j],mul(c,w))
    if any(x!=Z for x in total):raise ValueError('nonzero exact residual')
    den=math.lcm(*(x.denominator for w in weights for x in w))
    pairs=[(int(x*den),int(y*den)) for x,y in weights]
    gcd=math.gcd(*(abs(x) for w in pairs for x in w))
    return [(x//gcd,y//gcd) for x,y in pairs]
