"""Exhaustive small coordinate controls, plus exact line edge cases."""
import argparse
from fractions import Fraction as Q
from itertools import combinations
import json
from pathlib import Path
import random
import subprocess
from exact import build,interval,line,vary,orientations
from verify import maxima,orientation


def convex(p,ids):
    hull=[]
    for sequence in (ids,tuple(reversed(ids))):
        part=[]
        for v in sequence:
            while len(part)>1 and orientation(p,part[-2],part[-1],v)<=0:part.pop()
            part.append(v)
        hull.extend(part[:-1])
    return len(set(hull))==len(ids)


def brute(p):
    caps=[];polys=[];cups=[]
    for k in range(2,len(p)+1):
        for z in combinations(range(len(p)),k):
            if all(orientation(p,*t)<0 for t in combinations(z,3)):caps.append(z)
            if all(orientation(p,*t)>0 for t in combinations(z,3)):cups.append(z)
            if convex(p,z):polys.append(z)
    return caps,cups,polys


def finite_safe(q,lines):
    if not lines:return False
    q=(Q(q[0],q[2]),Q(q[1],q[2]));ls=[(Q(a,c),Q(b,c)) for a,b,c in lines]
    tests={Q(0)}
    for (s,z),(u,w) in combinations(ls,2):
        if s!=u:
            t=(w-z)/(s-u)
            if t>0:tests.add(t)
    return q[0]<=max(s for s,z in ls) and all(q[0]*t+q[1]<=max(s*t+z for s,z in ls) for t in tests)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--binary',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--boundary',type=Path,required=True)
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=False);rng=random.Random(202611140501)
    rows=[]
    for j in range(48):
        m=5+j%4
        while True:
            p=[[i,rng.randrange(-1000,1001)] for i in range(m)]
            if all(orientation(p,*t)!=0 for t in combinations(range(m),3)):break
        rows.append((f'random{j}',p,6+j%3))
    for n in (6,7,8):
        r=json.loads((args.boundary/f'n{n}-boundary.json').read_text());rows.append((f'boundary{n}',r['P'][:-1],n))
    rows.extend([('invalid-fivecap',[[i,-i*i] for i in range(7)],8),('invalid-ngon',[[i,i*i] for i in range(7)],7),('empty-ambient',[[i,i*i] for i in range(6)],7),('old-fourcap',[[0,0],[1,3],[2,5],[3,6],[4,100],[5,120],[6,130]],6)])
    checked=[]
    for name,p,n in rows:
        path=args.out/(name+'.points');path.write_text(f'{len(p)} {n}\n'+''.join(f'{x} {y}\n' for x,y in p))
        proc=subprocess.run([str(args.binary),str(path)],capture_output=True,text=True,timeout=3)
        (args.out/(name+'.geometry.json')).write_text(proc.stdout);(args.out/(name+'.stderr')).write_text(proc.stderr)
        assert proc.returncode in (0,4)
        g=json.loads(proc.stdout);caps,cups,polys=brute(p)
        expected={'maxcap':max(map(len,caps)),'maxcup':max(map(len,cups)),'maxgon':max(map(len,polys))}
        assert all(g[k]==v for k,v in expected.items()) and maxima(p,range(len(p)))==expected
        valid=expected['maxcap']<5 and expected['maxgon']<n
        assert valid==g['valid']==(proc.returncode==0)
        if valid:
            assert {tuple(t) for t in g['caps3']}=={t for t in caps if len(t)==3}
            assert {tuple(t) for t in g['caps4']}=={t for t in caps if len(t)==4}
            assert {tuple(t) for t in g['targets']}=={t for t in polys if len(t)==n-1}
            report,states=build(p,g);ambient=[line(p,t[-2:]) for t in g['caps4']]
            for pair,s in states.items():assert s['safe']==finite_safe(line(p,pair),ambient)
            for seed in (1,len(p)+1,123):
                v,meta=vary(p,seed);assert orientations(p)==orientations(v)
            if name=='old-fourcap':assert all(states[t[-2:]]['safe'] for t in combinations(range(4),3))
        checked.append({'name':name,'valid':valid,**expected})
    algebra=[]
    lines={(0,1):(0,2,1),(2,3):(2,-2,1)}
    for q,safe in [((1,0,1),True),((1,1,1),False),((2,-1,1),False),((3,-100,1),False),((0,3,1),False),((0,2,1),True)]:
        r=interval(q,lines);assert r['safe']==safe==finite_safe(q,list(lines.values()));algebra.append({'q':q,**r})
    assert len(algebra[0]['supports'])==2 and algebra[1]['interval']==['1','3']
    assert interval((0,0,1),{})['interval']==['0',None]
    assert interval((0,0,1),{(0,1):(1,0,1)})['safe']
    assert interval((0,0,1),{(0,1):(0,-1,1)})['interval']==['0',None]
    out={'label':'COMPUTED','geometry_cases':checked,'valid':sum(r['valid'] for r in checked),'invalid':sum(not r['valid'] for r in checked),'algebra':algebra,'all_passed':True}
    (args.out/'summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'cases':len(checked),'valid':out['valid'],'invalid':out['invalid'],'all_passed':True}))
if __name__=='__main__':main()
