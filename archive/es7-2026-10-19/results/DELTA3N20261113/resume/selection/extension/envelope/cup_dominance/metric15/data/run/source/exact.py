"""Exposure by integer cross-products; fractions only for final certificates."""
from fractions import Fraction as Q
from itertools import combinations


def determinant(p,a,b,c):
    return (p[b][0]-p[a][0])*(p[c][1]-p[a][1])-(p[b][1]-p[a][1])*(p[c][0]-p[a][0])


def line(p,pair):
    a,b=pair;dx=p[b][0]-p[a][0];dy=p[b][1]-p[a][1]
    return dy,p[b][1]*dx+dy*(p[-1][0]-p[b][0]),dx


def interval(q,ambient):
    """Return exposure endpoints/witness, or at most two dominance supports."""
    low,high=(0,1),None;lower=upper=None
    for pair,ell in ambient.items():
        ds=q[0]*ell[2]-ell[0]*q[2]
        dz=q[1]*ell[2]-ell[1]*q[2]
        # One ambient line dominates slope and height.
        if ds<=0 and dz<=0:
            return {'safe':True,'supports':[(pair,'1')]}
        if ds>0:
            bound=(-dz,ds)
            if bound[0]*low[1]>low[0]*bound[1]:low,lower=bound,pair
        elif ds<0:
            bound=(dz,-ds)
            if high is None or bound[0]*high[1]<high[0]*bound[1]:high,upper=bound,pair
        # Equal slopes with dz>0 impose no constraint.
    if high is not None and low[0]*high[1]>=high[0]*low[1]:
        assert lower is not None and upper is not None
        q_s=Q(q[0],q[2]);lm,lp=ambient[lower],ambient[upper]
        w=(Q(lp[0],lp[2])-q_s)/(Q(lp[0],lp[2])-Q(lm[0],lm[2]))
        assert 0<w<1
        assert w*Q(lm[1],lm[2])+(1-w)*Q(lp[1],lp[2])>=Q(q[1],q[2])
        return {'safe':True,'supports':[(lower,str(w)),(upper,str(1-w))]}
    lo=Q(*low);hi=None if high is None else Q(*high)
    t=lo+1 if hi is None else (lo+hi)/2
    assert t>0 and all(Q(q[0],q[2])*t+Q(q[1],q[2])>Q(e[0],e[2])*t+Q(e[1],e[2]) for e in ambient.values())
    return {'safe':False,'interval':[str(lo),None if hi is None else str(hi)],'witness_t':str(t)}


def build(p,geo):
    pair_caps={}
    for cap in geo['caps4']:pair_caps.setdefault(tuple(cap[-2:]),cap)
    ambient={pair:line(p,pair) for pair in pair_caps}
    states={pair:interval(line(p,pair),ambient) for pair in sorted({tuple(t[-2:]) for t in geo['caps3']})}
    bad=[t for t in geo['caps3'] if not states[tuple(t[-2:])]['safe']]
    report={'ambient':[{'pair':list(pair),'fourcap':pair_caps[pair]} for pair in pair_caps],
            'pairs':[dict(pair=list(pair),**row) for pair,row in states.items()],
            'exposed_triples':bad}
    return report,states


def certificate(p,geo,states,A):
    aset=set(A);four={}
    for c in geo['caps4']:four.setdefault(tuple(c[-2:]),c)
    result=[]
    for t in geo['caps3']:
        if set(t)<=aset:
            state=states[tuple(t[-2:])];assert state['safe']
            result.append({'triple':t,'supports':[{'fourcap':four[tuple(pair)],'weight':w} for pair,w in state['supports']]})
    return result


def orientations(p):
    return [1 if determinant(p,*t)>0 else -1 if determinant(p,*t)<0 else 0 for t in combinations(range(len(p)),3)]


def vary(p,seed,scale=1024):
    """One y-coordinate move, 7/8 of the first exact orientation boundary.

    All x's remain fixed up to a positive common scale. Rational movement
    is rounded toward zero after scaling, so strict bounds stay strict.
    No floating point or random library version dependency.
    """
    m=len(p);v=seed%m;direction=1 if (seed//m)%2==0 else -1
    bound=None
    for a,b,c in combinations(range(m),3):
        if v not in (a,b,c):continue
        z=determinant(p,a,b,c)
        coef=(p[c][0]-p[b][0] if v==a else -(p[c][0]-p[a][0]) if v==b else p[b][0]-p[a][0])*direction
        if z*coef<0:
            bnd=Q(abs(z),abs(coef))
            if bound is None or bnd<bound:bound=bnd
    if bound is None:
        bound=Q(max(1,max(y for x,y in p)-min(y for x,y in p)),4)
    step=bound*Q(7,8)*scale;step=step.numerator//step.denominator
    out=[[x*scale,y*scale] for x,y in p];out[v][1]+=direction*step
    assert orientations(p)==orientations(out)
    return out,{'vertex':v,'direction':direction,'scale':scale,'integer_step':step,'orientation_boundary':str(bound),'changed':step!=0}
