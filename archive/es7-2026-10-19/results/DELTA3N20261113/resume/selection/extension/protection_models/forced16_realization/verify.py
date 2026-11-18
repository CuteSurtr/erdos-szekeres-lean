#!/usr/bin/env python3
"""Independent exact acceptance; imports no finder or numeric library."""
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    resource.setrlimit(resource.RLIMIT_AS,(600<<20,600<<20))
    parser=argparse.ArgumentParser();parser.add_argument('--candidate',type=Path,required=True)
    parser.add_argument('--signs',type=Path,required=True);parser.add_argument('--out',type=Path,required=True)
    a=parser.parse_args();start=time.monotonic()
    raw=json.loads(a.candidate.read_text());P=raw['P'];signs=a.signs.read_text().strip()
    assert len(P)==16 and len(signs)==560
    assert all(len(p)==2 and all(type(z)is int for z in p) for p in P)
    assert all(P[i][0]<P[i+1][0] for i in range(15))
    ds=[]
    for (i,j,k),s in zip(combinations(range(16),3),signs):
        x,y=P[i];u,v=P[j];w,z=P[k]
        d=x*v+u*z+w*y-y*u-v*w-z*x
        assert d and (d>0)==(s=='+'),(i,j,k,d,s)
        ds.append(d)
    result={'label':'COMPUTED independent exact integer determinant verification','status':'PASS',
            'P':P,'m':16,'n':7,'strict_signs_checked':len(ds),'minimum_absolute_determinant':min(map(abs,ds)),
            'candidate_sha256':sha(a.candidate),'signs_sha256':sha(a.signs),
            'checker_sha256':sha(Path(__file__)),'seconds':time.monotonic()-start}
    with a.out.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({'status':'EXACT_INTEGER_REALIZATION_VERIFIED','minimum_absolute_determinant':result['minimum_absolute_determinant']}),flush=True)


if __name__=='__main__':main()
