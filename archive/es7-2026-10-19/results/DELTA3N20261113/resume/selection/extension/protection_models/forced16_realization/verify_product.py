#!/usr/bin/env python3
"""Independent exact replay of a bracket-product obstruction; no finder imports."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--signs',type=Path,required=True)
    ap.add_argument('--certificate',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();resource.setrlimit(resource.RLIMIT_AS,(600<<20,600<<20))
    signs=args.signs.read_text().strip();triples=list(combinations(range(16),3))
    assert len(signs)==len(triples)==560 and set(signs)<={'+','-'}
    sigma=dict(zip(triples,[1 if c=='+' else -1 for c in signs]))
    cert=json.loads(args.certificate.read_text())
    assert cert['signs_sha256']==hashlib.sha256(args.signs.read_bytes()).hexdigest()
    def bracket(t):
        v=list(t);parity=1
        for j in range(2):
            for k in range(2-j):
                if v[k]>v[k+1]:v[k],v[k+1]=v[k+1],v[k];parity=-parity
        return tuple(v),parity*sigma[tuple(v)]
    balance=Counter();lines=[];weight_sum=0
    assert cert['rows']
    for row in cert['rows']:
        a=row['root'];b,c,d,e=row['other'];assert len({a,b,c,d,e})==5
        assert all(0<=v<16 for v in (a,b,c,d,e))
        raw=[((a,b,c),(a,d,e)),((a,b,d),(a,c,e)),((a,b,e),(a,c,d))]
        terms=[];sg=[]
        for k,(u,v) in enumerate(raw):
            bu,su=bracket(u);bv,sv=bracket(v)
            terms.append((bu,bv));sg.append(su*sv*(1,-1,1)[k])
        L=row['large'];S=row['small'];assert 0<=L<3 and 0<=S<3 and L!=S
        assert sg.count(sg[L])==1 and sg[S]==-sg[L]
        w=row['weight'];assert type(w) is int and w>0
        for t in terms[L]:balance[t]+=w
        for t in terms[S]:balance[t]-=w
        weight_sum+=w
        lines.append({'root':a,'other':[b,c,d,e],'large_factors':terms[L],'small_factors':terms[S],'weight':w})
    assert all(v==0 for v in balance.values()),dict(balance)
    result={'status':'PASS','label':'EXACT CHECKED ALGEBRAIC OBSTRUCTION',
            'statement':'No real planar configuration in general position realizes these 560 signs.',
            'rows':len(lines),'weight_sum':weight_sum,'all_product_exponents_cancel':True,
            'certificate_sha256':hashlib.sha256(args.certificate.read_bytes()).hexdigest(),
            'signs_sha256':hashlib.sha256(args.signs.read_bytes()).hexdigest(),
            'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'checked_inequalities':lines}
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='checked_inequalities'}))


if __name__=='__main__':main()
