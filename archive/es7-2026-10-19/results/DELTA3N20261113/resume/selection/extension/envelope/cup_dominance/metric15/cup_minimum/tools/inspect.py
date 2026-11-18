"""Inspect four predetermined line certificates using exact arithmetic."""
import argparse
from fractions import Fraction as Q
import hashlib
from itertools import combinations
import json
import os
from pathlib import Path


def determinant(p, a, b, c):
    return ((p[b][0]-p[a][0])*(p[c][1]-p[a][1])
            -(p[b][1]-p[a][1])*(p[c][0]-p[a][0]))


def line(p, pair, M):
    a,b=pair
    slope=Q(p[b][1]-p[a][1],p[b][0]-p[a][0])
    return slope,Q(p[a][1])+slope*(M-p[a][0])


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--original',type=Path,required=True)
    ap.add_argument('--balanced',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    A=[2,3,6,9];support=[4,7,12,13];tail=support[-2:]
    result={'label':'COMPUTED exact rational certificates',
            'index_base':0,'selected_A':A,'parameter':'X=max_x+t, t>0',
            'difference':'ambient_terminal_line(X)-selected_terminal_line(X)=slope_difference*t+intercept_difference',
            'rational_format':'reduced numerator/denominator strings; denominator one omitted',
            'cases':[]}
    reference=None
    for name,path in [('original',args.original),('balanced',args.balanced)]:
        raw=path.read_bytes();source=json.loads(raw);p=source['P']
        assert len(p)==15 and all(type(z)is int for pt in p for z in pt)
        assert all(p[i][0]<p[i+1][0] for i in range(14))
        dets=[determinant(p,*t) for t in combinations(range(15),3)]
        assert all(dets)
        signs=''.join('+' if d>0 else '-' for d in dets)
        assert signs==source['orientation_signs']
        if reference is None:reference=signs
        assert signs==reference
        triples=[list(t) for t in combinations(A,3) if determinant(p,*t)<0]
        assert triples==[[2,3,6],[2,3,9]]
        assert all(determinant(p,*t)<0 for t in combinations(support,3))
        M=p[-1][0];rows=[]
        for triple in triples:
            pair=triple[-2:];cup=sorted(set(pair+tail))
            assert tail[0]>=pair[0] and tail[1]>=pair[1]
            assert all(determinant(p,*t)>0 for t in combinations(cup,3))
            s,z=line(p,pair,M);u,w=line(p,tail,M)
            ds,dz=u-s,w-z
            assert ds>0 and dz>0
            # Check both coefficients by separate integer cross products.
            a,b=pair;c,d=tail
            dx=p[b][0]-p[a][0];dy=p[b][1]-p[a][1]
            ex=p[d][0]-p[c][0];ey=p[d][1]-p[c][1]
            assert ds==Q(ey*dx-dy*ex,ex*dx)
            assert dz==Q((p[c][1]*ex+ey*(M-p[c][0]))*dx
                         -(p[a][1]*dx+dy*(M-p[a][0]))*ex,ex*dx)
            rows.append({'selected_cap_triple':triple,'selected_tail_pair':pair,
                         'ambient_fourcap':support,'ambient_tail_pair':tail,
                         'cup_union':cup,'slope_difference':str(ds),
                         'intercept_difference':str(dz)})
        result['cases'].append({'name':name,'input_sha256':hashlib.sha256(raw).hexdigest(),
                                'P':p,'max_x':M,'certificates':rows})
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open('x') as f:
        json.dump(result,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
        os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)
    print(json.dumps({r['name']:r['certificates'] for r in result['cases']}))


if __name__=='__main__':main()
