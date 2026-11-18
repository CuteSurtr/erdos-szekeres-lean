"""Second implementation of positive witnesses; imports no finder geometry.

This is a within-track replay, not the parent's independent audit.
"""
from fractions import Fraction
from itertools import combinations
import argparse
import json
from pathlib import Path


def orientation(p,a,b,c):
    return p[a][0]*(p[b][1]-p[c][1])+p[b][0]*(p[c][1]-p[a][1])+p[c][0]*(p[a][1]-p[b][1])


def maxima(p,vertices):
    ids=sorted(vertices);cap=cup=gon=min(2,len(ids))
    for ia,first in enumerate(ids[:-1]):
        up,down={},{}
        for ic in range(ia+1,len(ids)):
            last=ids[ic];up[first,last]=down[first,last]=2
            for ib in range(ia+1,ic):
                mid=ids[ib]
                up[mid,last]=max((up[x,mid]+1 for x in ids[ia:ib] if up[x,mid]>0 and orientation(p,x,mid,last)>0),default=0)
                down[mid,last]=max((down[x,mid]+1 for x in ids[ia:ib] if down[x,mid]>0 and orientation(p,x,mid,last)<0),default=0)
            upper=max(down[x,last] for x in ids[ia:ic])
            lower=max(up[x,last] for x in ids[ia:ic])
            cap=max(cap,upper);cup=max(cup,lower);gon=max(gon,upper+lower-2)
    return {'maxcap':cap,'maxcup':cup,'maxgon':gon}


def rational_line(p,a,b):
    slope=Fraction(p[b][1]-p[a][1],p[b][0]-p[a][0])
    height=p[a][1]+slope*(p[-1][0]-p[a][0])
    return slope,height


def replay(p,n,A,certificates):
    m=len(p)
    assert all(type(v)is int for q in p for v in q)
    assert all(p[i][0]<p[i+1][0] for i in range(m-1))
    assert all(orientation(p,*t)!=0 for t in combinations(range(m),3))
    whole=maxima(p,range(m));assert whole['maxcap']<5 and whole['maxgon']<n
    assert len(A)==len(set(A)) and all(type(i)is int and 0<=i<m for i in A)
    red=maxima(p,A);assert red['maxcap']<4
    blue=maxima(p,[i for i in range(m) if i not in set(A)]);assert blue['maxgon']<n-1
    expected={t for t in combinations(sorted(A),3) if orientation(p,*t)<0};seen=set();two=0
    for row in certificates:
        t=tuple(row['triple']);assert t in expected and t not in seen;seen.add(t)
        slope,height=rational_line(p,t[-2],t[-1]);ss=hh=weight=Fraction(0)
        supports=row['supports'];assert 1<=len(supports)<=2
        for item in supports:
            c=item['fourcap'];assert len(c)==4 and c==sorted(set(c))
            assert all(0<=i<m for i in c) and all(orientation(p,*v)<0 for v in combinations(c,3))
            s,h=rational_line(p,c[-2],c[-1]);w=Fraction(item['weight']);assert w>=0
            weight+=w;ss+=w*s;hh+=w*h
        assert weight==1 and ss>=slope and hh>=height
        two+=len(supports)==2
    assert expected==seen
    return {'full':whole,'selected':red,'complement':blue,'cap_triples_checked':len(seen),'two_line_certificates':two}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('case',type=Path);ap.add_argument('--out',type=Path)
    args=ap.parse_args();inp=json.loads((args.case/'input.json').read_text());r=json.loads((args.case/'result.json').read_text())
    result=replay(inp['P'],inp['n'],r['A'],json.loads((args.case/'certificates.json').read_text()))
    out=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.out:
        with args.out.open('x') as f:f.write(out)
    print(out,end='')
if __name__=='__main__':main()
