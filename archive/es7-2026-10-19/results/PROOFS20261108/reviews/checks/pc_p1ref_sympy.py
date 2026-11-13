import sympy as sp
c0,c1,ra,rb,rd,al,be,de,x,y,r,th,ph = sp.symbols('c0 c1 ra rb rd alpha beta delta x y r theta phi', real=True)
def orient(a,b,d):
    return (b[0]-a[0])*(d[1]-a[1])-(b[1]-a[1])*(d[0]-a[0])
def polar(r,t):
    return (c0+r*sp.cos(t), c1+r*sp.sin(t))
A,B,D = polar(ra,al),polar(rb,be),polar(rd,de)
# (a) polar formula
lhs = orient(A,B,D); rhs = ra*rb*sp.sin(be-al)+rb*rd*sp.sin(de-be)+rd*ra*sp.sin(al-de)
print("(a)", sp.simplify(sp.expand_trig(lhs-rhs)))
# bracket identity [v-u,w-u] = [u,v]+[v,w]+[w,u]
u0,u1,v0,v1,w0,w1 = sp.symbols('u0 u1 v0 v1 w0 w1', real=True)
br = lambda p,q: p[0]*q[1]-p[1]*q[0]
print("bracket", sp.expand(br((v0-u0,v1-u1),(w0-u0,w1-u1)) - (br((u0,u1),(v0,v1))+br((v0,v1),(w0,w1))+br((w0,w1),(u0,u1)))))
print("bracket2", sp.expand(br((v0-u0,v1-u1),(w0-u0,w1-u1)) - (br((v0,v1),(w0,w1))-br((v0,v1),(u0,u1))-br((u0,u1),(w0,w1))+br((u0,u1),(u0,u1)))))
# [u,v] = ra rb sin(beta-alpha)
print("[u,v]", sp.simplify(sp.expand_trig(br((ra*sp.cos(al),ra*sp.sin(al)),(rb*sp.cos(be),rb*sp.sin(be))) - ra*rb*sp.sin(be-al))))
# (b) centre
print("(b)", sp.simplify(sp.expand_trig(orient(A,B,(c0,c1)) - ra*rb*sp.sin(be-al))))
# (d) sin x + sin y - sin(x+y) = sin x (1-cos y) + sin y (1-cos x)
print("(d)", sp.simplify(sp.expand_trig(sp.sin(x)+sp.sin(y)-sp.sin(x+y) - (sp.sin(x)*(1-sp.cos(y))+sp.sin(y)*(1-sp.cos(x))))))
# (e) decomposition
O = ra*rb*sp.sin(x)+rb*rd*sp.sin(y)-rd*ra*sp.sin(x+y)
dec = ra*(rb-rd)*sp.sin(x)+rd*(rb-ra)*sp.sin(y)+ra*rd*(sp.sin(x)+sp.sin(y)-sp.sin(x+y))
print("(e)", sp.simplify(O-dec))
# (e) O equals polar formula with beta=alpha+x, delta=alpha+x+y
print("(e')", sp.simplify(sp.expand_trig(rhs.subs({be:al+x, de:al+x+y}) - O)))
# halfplane: (p0-c0)cos phi + (p1-c1) sin phi = r cos(theta - phi)
P = polar(r,th)
print("halfplane", sp.simplify(sp.expand_trig((P[0]-c0)*sp.cos(ph)+(P[1]-c1)*sp.sin(ph) - r*sp.cos(th-ph))))
# dist2_polar
print("dist2", sp.simplify((P[0]-c0)**2+(P[1]-c1)**2 - r**2))
# sin(arccos t) = sqrt(1-t^2) on [-1,1]
t = sp.symbols('t', real=True)
print("sin arccos", sp.simplify(sp.sin(sp.acos(t)) - sp.sqrt(1-t**2)))
# periodicity
k = sp.symbols('k', integer=True)
print("period", sp.simplify(sp.cos(th+2*sp.pi*k)-sp.cos(th)), sp.simplify(sp.sin(th+2*sp.pi*k)-sp.sin(th)))
# sin(alpha - delta) = sin(alpha - delta + 2pi)
print("sin2pi", sp.simplify(sp.sin(al-de+2*sp.pi)-sp.sin(al-de)))
# remark gaps example (0, pi, 3pi/2)
a_,b_,d_ = 0, sp.pi, 3*sp.pi/2
print("gaps ex:", b_-a_, d_-b_, a_+2*sp.pi-d_, "disjuncts:", d_-a_, a_+2*sp.pi-b_, b_+2*sp.pi-d_)
