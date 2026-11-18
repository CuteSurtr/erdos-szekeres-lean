#!/usr/bin/env python3
"""Exact real-coordinate and deliberate-corruption controls for the proof replay."""
import argparse
import copy
from itertools import combinations
import json
from pathlib import Path
import random
import resource
import subprocess
import sys


def det(P,a,b,c):
    x,y=P[a];u,v=P[b];w,z=P[c]
    return x*(v-z)+u*(z-y)+w*(y-v)


def real_control(P):
    ds=[det(P,*t) for t in combinations(range(16),3)]
    assert all(ds)
    identities=0;strict_rows=0
    for a in range(16):
        for b,c,d,e in combinations([x for x in range(16) if x!=a],4):
            terms=[det(P,a,b,c)*det(P,a,d,e),
                   -det(P,a,b,d)*det(P,a,c,e),
                   det(P,a,b,e)*det(P,a,c,d)]
            assert sum(terms)==0 and all(terms)
            sg=[x>0 for x in terms]
            assert len(set(sg))==2
            k=next(i for i,s in enumerate(sg) if sg.count(s)==1)
            for j in range(3):
                if j==k:continue
                assert abs(terms[k])>abs(terms[j]);strict_rows+=1
            identities+=1
    return {'P':P,'minimum_absolute_determinant':min(map(abs,ds)),
            'positive_orientation_count':sum(x>0 for x in ds),
            'exact_GP_identities':identities,'strict_product_inequalities':strict_rows,'PASS':True}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--checker',type=Path,required=True)
    ap.add_argument('--signs',type=Path,required=True);ap.add_argument('--certificate',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    resource.setrlimit(resource.RLIMIT_AS,(600<<20,600<<20));args.out.mkdir(parents=True,exist_ok=False)
    (args.out/'source.py').write_bytes(Path(__file__).read_bytes())
    rng=random.Random(20261114)
    P=[[i,rng.randrange(-1000000,1000001)] for i in range(16)]
    checks=[real_control([[i,i*i] for i in range(16)]),real_control(P)]
    original=json.loads(args.certificate.read_text());rejects=[]
    for name in ('altered_weight','reversed_inequality'):
        changed=copy.deepcopy(original)
        if name=='altered_weight':changed['rows'][0]['weight']+=1
        else:
            row=changed['rows'][0];row['large'],row['small']=row['small'],row['large']
        path=args.out/(name+'.json');path.write_text(json.dumps(changed,indent=2)+'\n')
        command=[sys.executable,'-B',str(args.checker),'--signs',str(args.signs),
                 '--certificate',str(path),'--out',str(args.out/(name+'.receipt.json'))]
        with (args.out/(name+'.log')).open('w') as log:
            proc=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,timeout=3)
        assert proc.returncode!=0 and not (args.out/(name+'.receipt.json')).exists()
        rejects.append({'mutation':name,'returncode':proc.returncode,'correctly_rejected':True})
    receipt={'status':'PASS','real_coordinate_controls':checks,'negative_controls':rejects,
             'scope':'Controls supplement the written algebraic proof and independent exact certificate replay.'}
    (args.out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'status':'PASS','real_point_sets':len(checks),'identities':sum(x['exact_GP_identities'] for x in checks),
                      'strict_product_inequalities':sum(x['strict_product_inequalities'] for x in checks),
                      'negative_controls':rejects}))


if __name__=='__main__':main()
