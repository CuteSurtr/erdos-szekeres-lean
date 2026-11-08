import math, random
random.seed(7)
PI=math.pi
def polar(c,r,t): return (c[0]+r*math.cos(t), c[1]+r*math.sin(t))
def orient(a,b,d): return (b[0]-a[0])*(d[1]-a[1])-(b[1]-a[1])*(d[0]-a[0])
def inArc(s,g,th):
    t=th-s; r=t%(2*PI); lift=r if r>0 else 2*PI
    return lift<g
def AHA(a,b,d,s,g): return inArc(s,g,a+PI) or inArc(s,g,b+PI) or inArc(s,g,d+PI)
def H(a,b,d): return (AHA(a,b,d,a,b-a),AHA(a,b,d,b,d-b),AHA(a,b,d,d,a+2*PI-d))
def RB(a,b,d): h=H(a,b,d); return not h[0] and not h[1]
def RD(a,b,d): h=H(a,b,d); return not h[1] and not h[2]
def RA(a,b,d): h=H(a,b,d); return not h[2] and not h[0]
def Alt(a,b,d): h=H(a,b,d); return all(h)
def toIco(al,th): return al+((th-al)%(2*PI))
eps=1e-9
cnt={'B':0,'D':0,'A':0,'alt':0,'phase':0,'sign_i':0,'sign_ii':0}; bad=[]
for _ in range(200000):
    c=(random.uniform(-3,3),random.uniform(-3,3))
    ra,rb,rd=[random.uniform(0.05,5) for _ in range(3)]
    al=random.uniform(-20,20); be=random.uniform(-20,20); de=random.uniform(-20,20)
    a=polar(c,ra,al); b=polar(c,rb,be); d=polar(c,rd,de)
    O=orient(a,b,d)
    bp=toIco(al,be); dp=toIco(al,de)
    if abs(bp-al)<eps or abs(dp-al)<eps: continue
    gaps_ok=lambda x,y,z: abs(y-x-PI)>1e-7 and abs(z-y-PI)>1e-7 and abs(x+2*PI-z-PI)>1e-7
    if bp<dp and gaps_ok(al,bp,dp):
        x,y,z=al,bp,dp
        ok=True
        if RA(x,y,z) and not (rb<=ra and rd<=ra): ok=False
        if RB(x,y,z) and not (ra<=rb and rd<=rb): ok=False
        if RD(x,y,z) and not (rb<=rd and ra<=rd): ok=False
        if ok:
            cnt['sign_i']+=1
            if not O>0: bad.append(('sign i',O))
        # rules directly on sorted (x,y,z) with radii (ra,rb,rd)
        if Alt(x,y,z):
            cnt['alt']+=1
            if not O>0: bad.append(('alt',O))
        if RB(x,y,z) and abs(x+2*PI-z-PI)>1e-7 and ra<=rb and rd<=rb:
            cnt['B']+=1
            if not O>0: bad.append(('B',O))
        if RD(x,y,z) and abs(y-x-PI)>1e-7 and rb<=rd and ra<=rd:
            cnt['D']+=1
            if not O>0: bad.append(('D',O))
        if RA(x,y,z) and abs(z-y-PI)>1e-7 and rb<=ra and rd<=ra:
            cnt['A']+=1
            if not O>0: bad.append(('A',O))
    if dp<bp and gaps_ok(al,dp,bp):
        x,y,z=al,dp,bp
        ok=True
        if RA(x,y,z) and not (rd<=ra and rb<=ra): ok=False
        if RB(x,y,z) and not (ra<=rd and rb<=rd): ok=False
        if RD(x,y,z) and not (rd<=rb and ra<=rb): ok=False
        if ok:
            cnt['sign_ii']+=1
            if not O<0: bad.append(('sign ii',O))
print(cnt, "violations:", len(bad), bad[:5])
