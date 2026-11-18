"""Exact all-right-half-line and representative-X enumeration of weak Deltas."""
import argparse
from fractions import Fraction as Q
from itertools import combinations
import json
from pathlib import Path
from check import cap

ap=argparse.ArgumentParser();ap.add_argument('prefix',type=Path);ap.add_argument('--out',required=True,type=Path)
args=ap.parse_args();prefix=args.prefix
raw=Path(str(prefix)+'.points').read_text().split();m,n=map(int,raw[:2]);p=[list(map(int,raw[2+2*i:4+2*i])) for i in range(m)]
assert m<=22
g=json.loads(Path(str(prefix)+'.geometry.json').read_text())
caps3=[t for t in combinations(range(m),3) if cap(p,t)]
caps4=[t for t in combinations(range(m),4) if cap(p,t)]
targets=g['polygons']

def line(pair):
    a,b=pair;slope=Q(p[b][1]-p[a][1],p[b][0]-p[a][0]);return slope,Q(p[a][1])-slope*p[a][0]
def val(l,x):return l[0]*x+l[1]
def mask(t):return sum(1<<i for i in t)
def vertices(a):return [i for i in range(m) if a>>i&1]
def fmt(q):return str(q)
last=Q(p[-1][0]);span=p[-1][0]-p[0][0]
by_slope={};pair_witness={}
for t in caps4:
    pair=tuple(t[-2:]);l=line(pair);pair_witness.setdefault(pair,t)
    if l[0] not in by_slope or l[1]>by_slope[l[0]][0][1]:by_slope[l[0]]=(l,pair)
assert by_slope
hull=[]
for slope in sorted(by_slope):
    l,pair=by_slope[slope]
    while hull:
        old,_,start=hull[-1];x=Q(old[1]-l[1],l[0]-old[0])
        if start is None or x>start:break
        hull.pop()
    hull.append((l,pair,None if not hull else x))
breaks=[start for l,pair,start in hull if start is not None and start>last]
def f4(x):return max(val(l,x) for l,pair,start in hull)
def line_safe_all(l):
    return l[0]<=hull[-1][0][0] and all(val(l,x)<=f4(x) for x in [last]+breaks)
badall=[t for t in caps3 if not line_safe_all(line(t[-2:]))]
badterm=[t for t in caps3 if tuple(t[-2:]) not in pair_witness]
flags=bytearray(1<<m)
for family,flag in ((caps4,1),(targets,2)):
    for t in family:flags[mask(t)]|=flag
for bit in range(m):
    step=1<<bit
    for base in range(0,1<<m,2*step):
        for z in range(base+step,base+2*step):flags[z]|=flags[z-step]
full=(1<<m)-1
weak=[a for a in range(1<<m) if not flags[a]&1 and not flags[full^a]&2]
def eligible(family):
    bs=[mask(t) for t in family]
    return [a for a in weak if all(a&b!=b for b in bs)]
def summarize(choices):
    return dict(count=len(choices),minimum_size=min(map(int.bit_count,choices),default=None),
                minimum_A=vertices(min(choices,key=lambda a:(a.bit_count(),a))) if choices else None)
allchoices=eligible(badall)
samples={last+1,last+span,last+100*span}
for i,x in enumerate(breaks):
    samples.add(x);samples.add(((breaks[i-1] if i else last)+x)/2)
if breaks:samples.add(breaks[-1]+max(span,1))
reports=[]
for x in sorted(samples):
    bad=[t for t in caps3 if val(line(t[-2:]),x)>f4(x)]
    summary=summarize(eligible(bad));summary.update(X=fmt(x),F4=fmt(f4(x)),forbidden_triples=len(bad))
    reports.append(summary)
allsummary=summarize(allchoices)
if allchoices:
    a=allsummary['minimum_A'];triples=[t for t in caps3 if set(t)<=set(a)]
    allsummary['threecaps']=[dict(vertices=t,terminal_pair=t[-2:],slope=fmt(line(t[-2:])[0]),
        intercept=fmt(line(t[-2:])[1]),ambient_rank=4 if tuple(t[-2:]) in pair_witness else 3,
        margins_at_breaks=[dict(X=fmt(x),F4_minus_line=fmt(f4(x)-val(line(t[-2:]),x))) for x in [last]+breaks],
        final_slope_margin=fmt(hull[-1][0][0]-line(t[-2:])[0])) for t in triples]
report=dict(label='COMPUTED',m=m,n=n,xmax=int(last),weak=summarize(weak),terminal=summarize(eligible(badterm)),
    all_X_strictly_right=allsummary,forbidden_terminal_triples=len(badterm),forbidden_all_X_triples=len(badall),
    F4_upper_envelope=[dict(slope=fmt(l[0]),intercept=fmt(l[1]),pair=pair,cap=pair_witness[pair],
                          starts=fmt(start) if start is not None else '-infinity') for l,pair,start in hull],
    right_halfline_breaks=[fmt(x) for x in breaks],representative_X=reports)
args.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
