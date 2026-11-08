from sympy import symbols, expand, simplify
n0,n1,c,p0,p1,q0,q1,a0,a1,b0,b1,d0,d1 = symbols('n0 n1 c p0 p1 q0 q1 a0 a1 b0 b1 d0 d1')
s = n0**2+n1**2
def frame(x,y): return (n1*(x-c*n0)-n0*(y-c*n1), n0*(x-c*n0)+n1*(y-c*n1))
def unframe(x,y): return (n1*x+n0*y+c*n0, -n0*x+n1*y+c*n1)
def lineRefl(x,y):
    lam = n0*x+n1*y-c
    return (x-2*lam*n0, y-2*lam*n1)
def mir(x,y): return (x,-y)
def orient(a,b,d): return (b[0]-a[0])*(d[1]-a[1])-(b[1]-a[1])*(d[0]-a[0])
ok = True
# frame formula
f = frame(p0,p1)
ok &= expand(f[0]-(n1*p0-n0*p1))==0 and expand(f[1]-(n0*p0+n1*p1-c*s))==0
# unframe(frame p): coordinate certificates (p0 - c n0), (p1 - c n1)
uf = unframe(*f)
ok &= expand(uf[0]-p0-(p0-c*n0)*(s-1))==0
ok &= expand(uf[1]-p1-(p1-c*n1)*(s-1))==0
# frame(unframe q): certificates q0, q1
fu = frame(*unframe(q0,q1))
ok &= expand(fu[0]-q0-q0*(s-1))==0 and expand(fu[1]-q1-q1*(s-1))==0
# frame(lineRefl p) vs mir(frame p): first coord by ring, second with -2(n0p0+n1p1)
fl = frame(*lineRefl(p0,p1)); mf = mir(*frame(p0,p1))
ok &= expand(fl[0]-mf[0])==0
ok &= expand(fl[1]-mf[1]-(-2*(n0*p0+n1*p1))*(s-1))==0
# orient_frame: certificate orient(a,b,d)
A=(a0,a1);B=(b0,b1);D=(d0,d1)
o = orient(frame(*A),frame(*B),frame(*D))
ok &= expand(o-orient(A,B,D)-orient(A,B,D)*(s-1))==0
# mir identities of Lemma orient-mir
P=(p0,p1)
ok &= expand(orient(mir(*A),mir(*B),mir(*D))+orient(A,B,D))==0
ok &= expand(orient(A,B,mir(*D))-(orient(A,B,D)-2*d1*(b0-a0)))==0
ok &= expand(orient(mir(*A),mir(*B),D)+orient(A,B,mir(*D)))==0
# cap_below_lines middle case identity: orient(ci,cj,mir cl) = -(xj-xi)yl - yi(xj-xl) - yj(xl-xi)
xi,yi,xj,yj,xl,yl = symbols('xi yi xj yj xl yl')
ok &= expand(orient((xi,yi),(xj,yj),mir(xl,yl)) - (-(xj-xi)*yl - yi*(xj-xl) - yj*(xl-xi)))==0
# slope(b): a1=0: orient(p,a,q) = (a0-p0) q1 + p1 (q0-a0)
pa0,pa1,aa0,qa0,qa1 = symbols('pa0 pa1 aa0 qa0 qa1')
ok &= expand(orient((pa0,pa1),(aa0,0),(qa0,qa1)) - ((aa0-pa0)*qa1 + pa1*(qa0-aa0)))==0
# injOn_x: orient(p,q,mir p) with q0=p0 is 0
ok &= expand(orient((p0,p1),(p0,q1),(p0,-p1)))==0
print('all identities hold:', ok)
