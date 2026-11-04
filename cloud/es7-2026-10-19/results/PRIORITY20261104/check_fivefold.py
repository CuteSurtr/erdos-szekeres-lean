"""Independent exact expansion of the GP14 eight-area identity and its derivation."""
from fractions import Fraction as F
import json
from pathlib import Path

def q(a, b=0): return F(a), F(b)
def add(x,y): return x[0]+y[0], x[1]+y[1]
def neg(x): return -x[0], -x[1]
def mul(x,y): return x[0]*y[0]+5*x[1]*y[1], x[0]*y[1]+x[1]*y[0]
Z, ONE, S = q(0), q(1), q(0,1)
PHI, TAU = q(F(1,2), F(1,2)), q(F(-1,2), F(1,2))
I = [[ONE,Z],[Z,ONE]]
R = [[Z,q(-1)],[ONE,TAU]]
def mm(A,B): return [[add(mul(A[i][0],B[0][j]),mul(A[i][1],B[1][j])) for j in range(2)] for i in range(2)]
def sm(c,A): return [[mul(c,e) for e in row] for row in A]
def ma(*As):
    out = [[Z,Z],[Z,Z]]
    for A in As: out = [[add(out[i][j],A[i][j]) for j in range(2)] for i in range(2)]
    return out
Rs = [I]
for _ in range(5): Rs.append(mm(Rs[-1],R))
O = [[Z,Z],[Z,Z]]

# Polynomials in eight independent seed coordinates; keys are sorted variable tuples.
def pa(*Ps):
    out = {}
    for P in Ps:
        for m,c in P.items(): out[m] = add(out.get(m,Z),c)
    return {m:c for m,c in out.items() if c != Z}
def ps(c,P): return {m:mul(c,v) for m,v in P.items() if mul(c,v) != Z}
def pm(P,Q):
    out = {}
    for m,c in P.items():
        for n,d in Q.items():
            mn=tuple(sorted(m+n)); out[mn]=add(out.get(mn,Z),mul(c,d))
    return {m:c for m,c in out.items() if c != Z}
def point(orbit,phase):
    x,y={(2*orbit,):ONE},{(2*orbit+1,):ONE}
    M=Rs[phase]
    return pa(ps(M[0][0],x),ps(M[0][1],y)),pa(ps(M[1][0],x),ps(M[1][1],y))
def det(p,r): return pa(pm(p[0],r[1]),ps(q(-1),pm(p[1],r[0])))
def area(p,r,t): return pa(det(p,r),det(r,t),det(t,p))
mapping={5:point(0,0)}
for base,orbit in [(35,1),(40,2),(45,3)]:
    for j in range(5): mapping[base+j]=point(orbit,j)
rows=[((5,35,39),q(-1)),((5,36,37),q(-1)),
      ((5,40,45),ONE),((5,41,47),ONE),
      ((35,45,49),q(-1)),((35,46,47),q(-1)),
      ((5,38,46),neg(S)),((5,43,46),PHI)]
expanded=pa(*(ps(c,area(*(mapping[i] for i in ids))) for ids,c in rows))
a,b,c,d=point(0,0),point(1,0),point(2,0),point(3,0)
def P(x,orbit): return pa(area(x,point(orbit,0),point(orbit,4)),area(x,point(orbit,1),point(orbit,2)))
Q=pa(area(a,c,d),area(a,point(2,1),point(3,2)),ps(PHI,area(a,point(2,3),point(3,1))))
checks={
 'R^5=I':Rs[5]==I,
 'I+R+phi R^3=0':ma(I,R,sm(PHI,Rs[3]))==O,
 'I-R^4+R-R^2=-sqrt5 R^3':ma(I,sm(q(-1),Rs[4]),R,sm(q(-1),Rs[2]))==sm(neg(S),Rs[3]),
 'I+R^2+phi R=sqrt5 R':ma(I,Rs[2],sm(PHI,R))==sm(S,R),
 'B=A sqrt5':q(-15,13)==mul(q(13,-3),S),
 'C=A phi':q(-1,5)==mul(q(13,-3),PHI),
 'eight_actual_normalized_triangle_rows_sum_to_zero':expanded=={},
 'P(a;b)=-sqrt5 det(a,b3)':P(a,1)==ps(neg(S),det(a,point(1,3))),
 'P(b0;d)=-sqrt5 det(b0,d3)':P(b,3)==ps(neg(S),det(b,point(3,3))),
 'Q=-sqrt5 det(a,d1)':Q==ps(neg(S),det(a,point(3,1))),
 'det(b3,d1)=det(b0,d3)':det(point(1,3),point(3,1))==det(b,point(3,3)),
}
assert all(checks.values()), checks
result={'checks':checks,'source':'../ROTREFINE20261104/m5_quadratic.md, fully GP-consistent source section',
        'normalized_rows':[{'triangle':list(ids),'weight_Qsqrt5':[str(c[0]),str(c[1])]} for ids,c in rows],
        'arithmetic':'fractions.Fraction pairs in Q(sqrt(5)); formal polynomials in 8 independent seed coordinates',
        'scope':'Algebraic derivation only; source model binding and signs rely on previously retained exact campaign checks.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
