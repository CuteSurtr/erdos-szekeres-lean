#!/usr/bin/env python3
"""Exact integer verification of the certified 54-point set and its reflection.

No trigonometry or Decimal arithmetic is used. A pair (X,Y) represents the
complex point X + sqrt(3)*Y*i; the omitted common factor 1/2 is positive.
"""
from fractions import Fraction as F
import hashlib
import importlib.util
import json
import math
import resource
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('independent_oracle',HERE/'adversarial.py')
O=importlib.util.module_from_spec(spec);spec.loader.exec_module(O)
SOURCE=O.ROOT/'ES8SYM/sets/c6_54pts_9layers.pts'


def convert(w):
    return (F(2*w[0]+w[1]-w[2]-2*w[3]-w[4]+w[5]),F(w[1]+w[2]-w[4]-w[5]))


def normalized_layers(points,mirror):
    points=[(x,-y if mirror else y) for x,y in points]
    groups=[points[i:i+6] for i in range(0,len(points),6)]
    for group in groups:
        assert set(O.orbit6(group[0]))==set(group),'not a regular rotation orbit'
    groups.sort(key=lambda g:g[0][0]**2+3*g[0][1]**2,reverse=True)
    u,v=groups[0][0]
    normalized=[]
    for group in groups:
        rotated=[(x*u+3*y*v,y*u-x*v) for x,y in group]
        # Sector [0,pi/3): tan(theta)/sqrt(3) is in [0,1).
        sector=[(x,y) for x,y in rotated if x>0 and 0<=y<x]
        assert len(sector)==1,'ambiguous phase sector'
        normalized.append(sector[0])
    assert normalized[0][1]==0
    assert all(0<y<x for x,y in normalized[1:]),'nongeneric phase zero'
    phase=[y/x for x,y in normalized]
    assert len(set(phase))==9,'nongeneric coincident phases'
    return normalized,phase


def main():
    start=time.monotonic()
    raw=SOURCE.read_bytes()
    rows=[list(map(int,line.split())) for line in raw.decode().splitlines() if line and not line.startswith('#')]
    assert len(rows)==54 and all(len(w)==6 for w in rows)
    points=list(map(convert,rows))
    print(json.dumps({'source':'ES8SYM/sets/c6_54pts_9layers.pts','sha256':hashlib.sha256(raw).hexdigest(),
                      'rigor':'exact computation','arithmetic':'integer/rational Q(sqrt(3)); no trigonometry'}),flush=True)
    encoders=O.build_encoders(6,9)
    yvalues=[]
    for mirror in (False,True):
        seeds,phase=normalized_layers(points,mirror)
        integer_points=O.points6(seeds)
        signs,mind=O.geometry(integer_points,6)
        assert signs is not None and mind>0
        yvalues.append(phase[1]<phase[2])
        for name,clauses,mp,fixedvars in encoders:
            assert len(clauses)==1040348
            fixed={v:signs[tuple(c)]>0 for c,v in mp['triples']}
            fixed.update({v:phase[i]<phase[j] for i,j,v in mp['Y']})
            assert not mp['H']
            geom_bad,chain_bad=O.horn_test(clauses,fixed,fixedvars)
            assert geom_bad==0 and chain_bad==0,(name,mirror,geom_bad,chain_bad)
            print(json.dumps({'case':'mirror' if mirror else 'original','encoder':name,'clauses':len(clauses),
                              'geometry_violations':geom_bad,'chain_violations':chain_bad,'Y12':yvalues[-1],
                              'nonzero_triples':math.comb(54,3),'strict_nesting':True,
                              'phase_order':sorted(range(9),key=lambda i:phase[i])}),flush=True)
    assert yvalues[0]!=yvalues[1]
    print(json.dumps({'status':'PASS','Y12_original':yvalues[0],'Y12_mirror':yvalues[1],
                      'elapsed_seconds':round(time.monotonic()-start,3),
                      'maximum_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}),flush=True)


if __name__=='__main__': main()
