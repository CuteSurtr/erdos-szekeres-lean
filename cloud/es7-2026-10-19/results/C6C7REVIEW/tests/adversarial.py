#!/usr/bin/env python3
"""Independent geometry and Horn-CNF oracle for the two octagon encoders.

Run from any directory: python3 -I C6C7REVIEW/tests/adversarial.py
No validator module is imported. Small generated formulas are held only in memory.
Hexagon coordinates (x, y) represent the real point (x, sqrt(3)*y); rational
coordinates are scaled to integers, so orientation and hull tests are exact.
Heptagon computations are floating-point evidence with a minimum determinant guard.
"""
import collections
import contextlib
from fractions import Fraction as F
import hashlib
import importlib.util
import io
import itertools as it
import json
import math
from pathlib import Path
import random
import sys
import time
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SEED = 202611040731
RNG = random.Random(SEED)
START = time.monotonic()


def cross(a, b):
    return a[0]*b[1]-a[1]*b[0]


def subtract(a,b):
    return (a[0]-b[0],a[1]-b[1])


def turn(a,b,c):
    return cross(subtract(b,a),subtract(c,a))


def orbit6(seed):
    out=[]; x,y=seed
    for _ in range(6):
        out.append((x,y)); x,y=(x-3*y)/2,(x+y)/2
    assert (x,y)==seed
    return out


def nested6(slopes, closeness):
    seeds=[(F(1),F(0))]
    for q,factor in zip(slopes,closeness):
        outer=orbit6(seeds[-1]); trial=orbit6((F(1),q)); bounds=[]
        for a,b in zip(outer,outer[1:]+outer[:1]):
            e=subtract(b,a)
            for c in trial:
                den=cross(e,c)
                if den<0: bounds.append(cross(e,a)/den)
        scale=min(bounds)*factor
        seeds.append((scale,scale*q))
    return seeds


def points6(seeds):
    points=[p for s in seeds for p in orbit6(s)]
    den=math.lcm(*(c.denominator for p in points for c in p))
    return [(int(x*den),int(y*den)) for x,y in points]


def mirror6(seeds):
    return [seeds[0]]+[((x+3*y)/2,(x-y)/2) for x,y in seeds[1:]]


def nested7(phase_fractions,closeness):
    angles=[0.0]+[x*2*math.pi/7 for x in phase_fractions]
    layers=[(1.0,0.0)]
    for theta,factor in zip(angles[1:],closeness):
        outer=[(layers[-1][0]*math.cos(layers[-1][1]+k*2*math.pi/7),
                layers[-1][0]*math.sin(layers[-1][1]+k*2*math.pi/7)) for k in range(7)]
        trial=[(math.cos(theta+k*2*math.pi/7),math.sin(theta+k*2*math.pi/7)) for k in range(7)]
        bounds=[]
        for a,b in zip(outer,outer[1:]+outer[:1]):
            e=subtract(b,a)
            for c in trial:
                den=cross(e,c)
                if den < 0: bounds.append(cross(e,a)/den)
        layers.append((min(bounds)*factor,theta))
    return layers


def points7(layers):
    return [(r*math.cos(th+2*math.pi*k/7),r*math.sin(th+2*math.pi*k/7))
            for r,th in layers for k in range(7)]


def geometry(points,m):
    n=len(points); signs={}; mind=None
    for a,b,c in it.combinations(range(n),3):
        d=turn(points[a],points[b],points[c]); ad=abs(d)
        mind=ad if mind is None else min(mind,ad)
        if not d: return None,0
        sg=1 if d>0 else -1
        for p in ((a,b,c),(b,c,a),(c,a,b)): signs[p]=sg
        for p in ((a,c,b),(c,b,a),(b,a,c)): signs[p]=-sg
    for i in range(n//m):
        for k in range(m):
            a=i*m+k; b=i*m+(k+1)%m
            assert all(signs[a,b,c]>0 for c in range((i+1)*m,n)), 'nesting'
    return signs,mind


def has_octagon(points,signs):
    """Enumerate all eight-subsets; independent monotone-chain convex hull."""
    order=sorted(range(len(points)),key=lambda v:points[v]); examined=0
    for subset in it.combinations(order,8):
        examined+=1
        lo=[]; hi=[]
        for x in subset:
            while len(lo)>1 and signs[lo[-2],lo[-1],x]<0: lo.pop()
            lo.append(x)
        for x in reversed(subset):
            while len(hi)>1 and signs[hi[-2],hi[-1],x]<0: hi.pop()
            hi.append(x)
        if len(lo)+len(hi)-2==8: return True,examined
    return False,examined


class KeepString(io.StringIO):
    def close(self):
        pass


def build_encoders(m,t):
    spec=importlib.util.spec_from_file_location('source_encoder_a',ROOT/'C7UPPER/gen.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    a,_,_=module.build(m,8,t)
    astr='p cnf %d %d\n'%(a.nv,len(a.cls))+''.join(' '.join(map(str,c))+' 0\n' for c in a.cls)
    buffers={}
    def memopen(filename,mode='r',*args,**kwargs):
        assert mode=='w'
        buffers[str(filename)]=KeepString(); return buffers[str(filename)]
    bfile=ROOT/'C6UPPER/encb/gen_b2.py'
    source=bfile.read_text()
    with patch.object(sys,'argv',['gen_b2.py',str(m),'8',str(t),'mem.cnf']),patch('builtins.open',memopen),contextlib.redirect_stdout(io.StringIO()):
        exec(compile(source,'gen_b2.py','exec'),{'__name__':'__main__'})
    btext=buffers['mem.cnf'].getvalue(); bm=json.loads(buffers['mem.cnf.map.json'].getvalue())
    bcls=[list(map(int,line.split()[:-1])) for line in btext.splitlines()[1:]]
    afixed={'triples':[(c,v) for c,v in a.tvar.items()], 'Y':[(i,j,v) for (i,j),v in a.Y.items()], 'H':list(a.H.items())}
    bfixed={'triples':[(tuple(i*m+k for i,k in c),v) for c,v in bm['orb']], 'Y':bm['Y'], 'H':bm['H']}
    ans=[]
    for name,cls,mp,txt in [('A',a.cls,afixed,astr),('B',bcls,bfixed,btext)]:
        fixedvars={v for _,v in mp['triples']}|{v for i,j,v in mp['Y']}|{v for i,v in mp['H']}
        ans.append((name,cls,mp,fixedvars))
        print(json.dumps({'formula':name,'m':m,'t':t,'clauses':len(cls),'sha256':hashlib.sha256(txt.encode()).hexdigest()}),flush=True)
    return ans


def horn_test(clauses,fixed,fixedvars):
    """Evaluate fixed geometry, then derive least model of remaining Horn CNF."""
    rule_head=[]; remaining=[]; uses=collections.defaultdict(list); queue=collections.deque()
    geom_bad=0; chain_bad=0
    for cl in clauses:
        if any(abs(l) in fixedvars and fixed[abs(l)]==(l>0) for l in cl): continue
        rem=[l for l in cl if abs(l) not in fixedvars]
        if not rem:
            geom_bad+=1; continue
        positives=[l for l in rem if l>0]; negatives=[-l for l in rem if l<0]
        assert len(positives)<=1,'non-Horn chain clause'
        idx=len(rule_head); rule_head.append(positives[0] if positives else 0);remaining.append(len(negatives))
        for var in negatives: uses[var].append(idx)
        if not negatives: queue.append(idx)
    true=set()
    while queue:
        idx=queue.popleft(); head=rule_head[idx]
        if not head: chain_bad+=1;continue
        if head in true: continue
        true.add(head)
        for nxt in uses[head]:
            remaining[nxt]-=1
            if not remaining[nxt]: queue.append(nxt)
    return geom_bad,chain_bad


def check_case(m,t,label,data,encoders,stats):
    points=points6(data) if m==6 else points7(data)
    signs,mind=geometry(points,m)
    if signs is None or (m==7 and mind<1e-10):
        stats['rejected_degenerate_or_guard']+=1;return
    if m==6:
        phase=[y/x for x,y in data]; halves={}
    else:
        unit=math.pi/m; phase=[th%unit for r,th in data]; halves={i:th<unit for i,(r,th) in enumerate(data)}
    kgon,examined=has_octagon(points,signs)
    vals=[]
    for name,clauses,mp,fixedvars in encoders:
        fixed={v:signs[tuple(c)]>0 for c,v in mp['triples']}
        fixed.update({v:phase[i]<phase[j] for i,j,v in mp['Y']})
        fixed.update({v:halves[i] for i,v in mp['H']})
        geom_bad,chain_bad=horn_test(clauses,fixed,fixedvars)
        assert geom_bad==0,(m,t,label,name,'geometry',geom_bad)
        assert bool(chain_bad)==kgon,(m,t,label,name,'chain',chain_bad,kgon)
        if not stats['mutant_geometry_'+name]:
            v=next(iter(fixed))
            mutant=[-v if fixed[v] else v]
            assert horn_test(clauses+[mutant],fixed,fixedvars)[0]==1
            stats['mutant_geometry_'+name]=1
        if kgon and not stats['mutant_deleted_chains_'+name]:
            geometric=[cl for cl in clauses if all(abs(l) in fixedvars for l in cl)]
            assert horn_test(geometric,fixed,fixedvars)==(0,0)
            stats['mutant_deleted_chains_'+name]=1
        vals.append({'encoder':name,'geometry_violations':geom_bad,'chain_detects_octagon':bool(chain_bad)})
    stats['accepted']+=1;stats['octagon' if kgon else 'octagon_free']+=1;stats['subsets_examined']+=examined
    print(json.dumps({'m':m,'t':t,'case':label,'rigor':'exact computation' if m==6 else 'evidence only',
                      'octagon':kgon,'subsets_examined':examined,'minimum_abs_determinant':str(mind), 'checks':vals}),flush=True)


def main():
    print(json.dumps({'seed':SEED,'deadline_seconds':900,'method':'independent hull oracle and generic Horn closure'}),flush=True)
    allstats={}
    for m,t in [(6,2),(6,3),(7,2),(7,3)]:
        encoders=build_encoders(m,t)
        stats=collections.Counter();allstats[f'm{m}t{t}']=stats
        cases=[]
        if m==6:
            profiles=[([F(1,10**6),F(3,7)],'phase_near_zero'),([F(999999,10**6),F(2,7)],'phase_near_wrap'),
                      ([F(1,3),F(1,3)+F(1,10**6)],'phase_near_equal'),([F(2,3),F(1,3)],'reverse_order')]
            for slopes,name in profiles:
                for factor in [F(1,5),F(7,10),F(999999,10**6)]:
                    d=nested6(slopes[:t-1],[factor]*(t-1))
                    cases.extend([(name+'_factor_'+str(factor),d),('mirror_'+name+'_factor_'+str(factor),mirror6(d))])
            for j in range(12 if t==2 else 8):
                slopes=RNG.sample(range(1,997),t-1)
                d=nested6([F(q,997) for q in slopes],[F(RNG.randrange(15,99),100) for _ in slopes])
                cases.append(('random_'+str(j),d))
        else:
            profiles=[([1e-5,0.37],'phase_near_zero'),([1-1e-5,0.24],'phase_near_wrap'),
                      ([0.5-1e-5,0.5+1e-5],'half_boundary'),([0.31,0.31001],'phase_near_equal')]
            for phases,name in profiles:
                for factor in [0.3,0.8,1-1e-5]:
                    d=nested7(phases[:t-1],[factor]*(t-1)); mir=[d[0]]+[(r,2*math.pi/7-th) for r,th in d[1:]]
                    cases.extend([(name+'_factor_'+str(factor),d),('mirror_'+name+'_factor_'+str(factor),mir)])
            for j in range(10 if t==2 else 6):
                ph=[RNG.uniform(0.01,0.99) for _ in range(t-1)]
                cases.append(('random_'+str(j),nested7(ph,[RNG.uniform(0.25,0.98) for _ in ph])))
        previous=None
        for label,data in cases:
            if label.startswith('mirror_'):
                if m==6 and t==3:
                    old=[y/x for x,y in previous]; reflected=[y/x for x,y in data]
                    assert (old[1]<old[2]) != (reflected[1]<reflected[2])
                    stats['reflection_Y12_checked']+=1
                if m==7:
                    assert (previous[1][1]<math.pi/7) != (data[1][1]<math.pi/7)
                    stats['reflection_H1_checked']+=1
            else:
                previous=data
            if time.monotonic()-START>900: raise TimeoutError('15 minute limit')
            check_case(m,t,label,data,encoders,stats)
        print(json.dumps({'summary':f'm{m}t{t}',**stats}),flush=True)
    print(json.dumps({'all_summaries':allstats,'elapsed_seconds':round(time.monotonic()-START,3),'status':'PASS'}),flush=True)


if __name__=='__main__': main()
