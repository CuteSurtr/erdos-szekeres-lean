"""Independent-from-encoder exact checker: brute caps, monotone hulls, all colors.

Uses Python unbounded integers and never imports encode/probe. No LRAT certification.
"""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path

def cross(p,a,b,c):
    ax,ay=p[a];bx,by=p[b];cx,cy=p[c]
    return (bx-ax)*(cy-ay)-(by-ay)*(cx-ax)

def cap(p,seq):
    return all(cross(p,*seq[t:t+3])<0 for t in range(len(seq)-2))

def convex(p,seq):
    hull=[]
    for a in seq:
        while len(hull)>1 and cross(p,hull[-2],hull[-1],a)<=0: hull.pop()
        hull.append(a)
    lower=len(hull)
    hull=[]
    for a in reversed(seq):
        while len(hull)>1 and cross(p,hull[-2],hull[-1],a)<=0: hull.pop()
        hull.append(a)
    return lower+len(hull)-2==len(seq)

def verify(prefix,colors=False,full=True):
    txt=Path(str(prefix)+'.points').read_text().split();m,n=map(int,txt[:2]);p=[list(map(int,txt[2+2*i:4+2*i])) for i in range(m)]
    assert all(p[i][0]<p[i+1][0] for i in range(m-1))
    assert all(cross(p,*t)!=0 for t in it.combinations(range(m),3))
    g=json.loads(Path(str(prefix)+'.geometry.json').read_text())
    caps={k:[t for t in it.combinations(range(m),k) if cap(p,t)] for k in (3,4,5)}
    assert not caps[5]
    ends4={t[-2:] for t in caps[4]}
    bad=[t for t in caps[3] if t[-2:] not in ends4]
    good=[t for t in caps[3] if t[-2:] in ends4]
    assert set(caps[4])==set(map(tuple,g['fourcaps']))
    assert set(bad)==set(map(tuple,g['rank3_triples']))
    assert set(good)==set(map(tuple,g['rank4_triples']))
    assert all(t[:3] in set(bad) for t in caps[4])
    if full:
        targets=[t for t in it.combinations(range(m),n-1) if convex(p,t)]
        forbidden=[t for t in it.combinations(range(m),n) if convex(p,t)]
        assert not forbidden
        assert set(targets)==set(map(tuple,g['polygons']))
    else:
        targets=[tuple(t) for t in g['polygons']]
        assert all(convex(p,t) for t in targets)
    # Clause set equality, with literal meaning fixed as index+1.
    for strong in (False,True):
        cnf=Path(str(prefix)+('.terminal.cnf' if strong else '.weak.cnf')).read_text().splitlines()
        actual=[tuple(map(int,line.split()[:-1])) for line in cnf if line and line[0] not in 'cp']
        expected=[tuple(-i-1 for i in t) for t in caps[4]+(bad if strong else [])]+[tuple(i+1 for i in t) for t in targets]
        assert len(actual)==len(expected) and set(actual)==set(expected)
    result=json.loads(Path(str(prefix)+'.result.json').read_text())
    for kind in ('terminal','weak'):
        model=result[kind]
        if model['outcome']!='SAT': continue
        a=set(model['A'])
        assert not any(set(t)<=a for t in caps[4])
        assert all(set(t)&a for t in targets)
        if kind=='terminal': assert not any(set(t)<=a for t in bad)
    report=dict(label='COMPUTED',stem=prefix.name,m=m,n=n,full_geometry=full,
                fourcaps=len(caps[4]),rank3_triples=len(bad),polygons=len(targets),
                clause_sets_match=True,models_checked=True,redundant_fourcap_lemma_checked=True)
    if colors:
        assert m<=22
        flags=bytearray(1<<m)
        for family,flag in ((caps[4],1),(bad,2),(targets,4)):
            for t in family:flags[sum(1<<i for i in t)]|=flag
        for b in range(m):
            stride=1<<b
            for base in range(0,1<<m,2*stride):
                for mask in range(base+stride,base+2*stride):flags[mask]|=flags[mask-stride]
        fullmask=(1<<m)-1;weak=[];strong=[]
        for a in range(1<<m):
            if flags[fullmask^a]&4: continue
            if not flags[a]&1:weak.append(a)
            if not flags[a]&3:strong.append(a)
        report.update(all_assignments=1<<m,weak_count=len(weak),terminal_count=len(strong),
                      weak_min_size=min(map(int.bit_count,weak),default=None),
                      terminal_min_size=min(map(int.bit_count,strong),default=None))
        if weak:
            best=min(weak,key=lambda z:(z.bit_count(),z))
            report['minimum_weak_A']=[i for i in range(m) if best>>i&1]
        if result['terminal']['outcome']=='UNSAT_UNCERTIFIED': assert not strong
    report['cnf_sha256']=hashlib.sha256(Path(str(prefix)+'.terminal.cnf').read_bytes()).hexdigest()
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('prefix',type=Path);ap.add_argument('--colors',action='store_true')
    ap.add_argument('--listed-only',action='store_true');ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();report=verify(a.prefix,a.colors,not a.listed_only)
    a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
